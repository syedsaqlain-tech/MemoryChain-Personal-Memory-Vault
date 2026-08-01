import os
import hashlib
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from blockchain import contract, web3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# ==========================
# Upload Folder
# ==========================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================
# MySQL Connection
# ==========================
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        autocommit=True,
        ssl_disabled=True
    )


# ==========================
# Helper Function
# ==========================
def get_cursor():
    db = get_db()
    cursor = db.cursor()
    return db, cursor


# ==========================
# Home API
# ==========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "MemoryChain",
        "backend": "Flask",
        "database": "MySQL",
        "blockchain": "Ethereum Ganache",
        "status": "Running Successfully"
    })
# ==========================
# Register API
# ==========================
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({
                "success": False,
                "message": "All fields are required."
            }), 400

        db, cursor = get_cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        if cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({
                "success": False,
                "message": "Email already registered."
            }), 400

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Registration Successful!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================
# Login API
# ==========================
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        db, cursor = get_cursor()

        cursor.execute(
            """
            SELECT id,name,email
            FROM users
            WHERE email=%s AND password=%s
            """,
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            return jsonify({
                "success": True,
                "message": "Login Successful!",
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2]
                }
            })

        return jsonify({
            "success": False,
            "message": "Invalid Email or Password!"
        }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ==========================
# Upload Memory API
# ==========================
@app.route("/upload", methods=["POST"])
def upload_memory():
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        file = request.files.get("file")

        if not title or not description:
            return jsonify({
                "success": False,
                "message": "Title and Description are required."
            }), 400

        if not file:
            return jsonify({
                "success": False,
                "message": "Please select a file."
            }), 400

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        # Generate SHA-256 Hash
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        db, cursor = get_cursor()

        # Save in MySQL first
        cursor.execute(
            """
            INSERT INTO memories
            (title, description, filename)
            VALUES (%s,%s,%s)
            """,
            (title, description, filename)
        )

        db.commit()

        memory_id = cursor.lastrowid

        transaction_hash = None
        blockchain_index = None

        # Store Hash on Blockchain
        try:
            account = web3.eth.accounts[0]

            tx = contract.functions.addMemory(
                title,
                description,
                file_hash
            ).transact({
                "from": account
            })

            receipt = web3.eth.wait_for_transaction_receipt(tx)

            transaction_hash = receipt.transactionHash.hex()

            blockchain_index = (
                contract.functions.totalMemories().call() - 1
            )

            cursor.execute(
                """
                UPDATE memories
                SET transaction_hash=%s,
                    blockchain_index=%s
                WHERE id=%s
                """,
                (
                    transaction_hash,
                    blockchain_index,
                    memory_id
                )
            )

            db.commit()

        except Exception as blockchain_error:
            print("Blockchain Error:", blockchain_error)

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Memory Uploaded Successfully!",
            "memory_id": memory_id,
            "file_hash": file_hash,
            "transaction_hash": transaction_hash,
            "blockchain_index": blockchain_index
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ==========================
# Get All Memories API
# ==========================
@app.route("/memories", methods=["GET"])
def get_memories():
    try:
        db, cursor = get_cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                filename,
                transaction_hash,
                blockchain_index
            FROM memories
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        memories = []

        for row in rows:
            memories.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "filename": row[3],
                "transaction_hash": row[4],
                "blockchain_index": row[5]
            })

        return jsonify(memories)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================
# Get Single Memory API
# ==========================
@app.route("/memory/<int:id>", methods=["GET"])
def get_memory(id):
    try:
        db, cursor = get_cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                filename,
                transaction_hash,
                blockchain_index
            FROM memories
            WHERE id=%s
        """, (id,))

        row = cursor.fetchone()

        cursor.close()
        db.close()

        if not row:
            return jsonify({
                "success": False,
                "message": "Memory not found."
            }), 404

        return jsonify({
            "success": True,
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "filename": row[3],
            "transaction_hash": row[4],
            "blockchain_index": row[5]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================
# Download File API
# ==========================
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename,
            as_attachment=True
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404
# ==========================
# Update Memory API
# ==========================
@app.route("/update_memory/<int:id>", methods=["PUT"])
def update_memory(id):
    try:
        data = request.get_json()

        title = data.get("title")
        description = data.get("description")

        if not title or not description:
            return jsonify({
                "success": False,
                "message": "Title and Description are required."
            }), 400

        db, cursor = get_cursor()

        cursor.execute(
            """
            UPDATE memories
            SET title=%s,
                description=%s
            WHERE id=%s
            """,
            (title, description, id)
        )

        db.commit()

        if cursor.rowcount == 0:
            cursor.close()
            db.close()

            return jsonify({
                "success": False,
                "message": "Memory not found."
            }), 404

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Memory Updated Successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================
# Delete Memory API
# ==========================
@app.route("/delete_memory/<int:id>", methods=["DELETE"])
def delete_memory(id):
    try:
        db, cursor = get_cursor()

        # Get filename before deleting
        cursor.execute(
            "SELECT filename FROM memories WHERE id=%s",
            (id,)
        )

        row = cursor.fetchone()

        if not row:
            cursor.close()
            db.close()

            return jsonify({
                "success": False,
                "message": "Memory not found."
            }), 404

        filename = row[0]

        cursor.execute(
            "DELETE FROM memories WHERE id=%s",
            (id,)
        )

        db.commit()

        cursor.close()
        db.close()

        # Delete uploaded file
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "success": True,
            "message": "Memory Deleted Successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================
# Profile API
# ==========================
@app.route("/profile", methods=["GET"])
def profile():
    try:
        db, cursor = get_cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                email
            FROM users
            ORDER BY id ASC
            LIMIT 1
        """)

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if not user:
            return jsonify({
                "success": False,
                "message": "No user found."
            }), 404

        return jsonify({
            "success": True,
            "id": user[0],
            "name": user[1],
            "email": user[2]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ==========================
# Verify File API
# ==========================
@app.route("/verify", methods=["POST"])
def verify_file():

    try:

        memory_id = request.form.get("id")
        file = request.files.get("file")

        if not memory_id:
            return jsonify({
                "success": False,
                "message": "Memory ID is required."
            }), 400

        if not file:
            return jsonify({
                "success": False,
                "message": "Please select a file."
            }), 400

        db, cursor = get_cursor()

        cursor.execute(
            """
            SELECT blockchain_index
            FROM memories
            WHERE id=%s
            """,
            (memory_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        db.close()

        if not row:
            return jsonify({
                "success": False,
                "message": "Memory not found."
            }), 404

        blockchain_index = row[0]

        if blockchain_index is None:
            return jsonify({
                "success": False,
                "message": "Memory not stored on Blockchain."
            }), 400

        uploaded_hash = hashlib.sha256(file.read()).hexdigest()

        blockchain_memory = contract.functions.getMemory(
            blockchain_index
        ).call()

        blockchain_hash = blockchain_memory[2]

        if uploaded_hash == blockchain_hash:

            return jsonify({
                "success": True,
                "verified": True,
                "message": "File Verified Successfully."
            })

        return jsonify({
            "success": True,
            "verified": False,
            "message": "File Modified."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ==========================
# Total Memories API
# ==========================
@app.route("/total_memories", methods=["GET"])
def total_memories():

    try:

        db, cursor = get_cursor()

        cursor.execute("SELECT COUNT(*) FROM memories")

        total = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "total": total
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ==========================
# Dashboard Stats API
# ==========================
@app.route("/dashboard_stats", methods=["GET"])
def dashboard_stats():

    try:

        db, cursor = get_cursor()

        cursor.execute("SELECT COUNT(*) FROM memories")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM memories
            WHERE transaction_hash IS NOT NULL
        """)
        blockchain = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users")
        users = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "total_memories": total,
            "blockchain_memories": blockchain,
            "users": users
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ==========================
# Recent Memories API
# ==========================
@app.route("/recent_memories", methods=["GET"])
def recent_memories():

    try:

        db, cursor = get_cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                filename
            FROM memories
            ORDER BY id DESC
            LIMIT 5
        """)

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        memories = []

        for row in rows:

            memories.append({

                "id": row[0],
                "title": row[1],
                "description": row[2],
                "filename": row[3]

            })

        return jsonify(memories)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
#run sever
if __name__ == "__main__":
    app.run(debug=True)