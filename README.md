# 🧠 MemoryChain – Personal Memory Vault

MemoryChain is a personal digital memory vault developed as a BCA academic project. It allows users to securely upload, manage, download, edit, delete, and verify their personal memories and files.

The project combines a Flask web application, MySQL database, SHA-256 file hashing, and a Solidity smart contract running on a local Ganache blockchain.

---

## 📌 Project Overview

Digital memories and personal files can be accidentally modified or lost. It can also be difficult to verify whether a stored file is still the original file.

MemoryChain provides a personal vault where users can manage their memories while using:

- **MySQL** for user and memory records
- **SHA-256** for file-integrity verification
- **Solidity smart contract** for blockchain-based memory records
- **Ganache** as the local Ethereum blockchain
- **Flask** as the backend server

The application also provides user-specific memory access, so one user cannot view another user's memories.

---

## ✨ Features

### 👤 User Management
- User registration
- User login
- Session-based authentication
- User profile
- Logout

### 🗂️ Memory Management
- Upload a memory
- Upload a file with the memory
- View personal memories
- Download stored files
- Edit memory details
- Delete memories
- Search memories

### 🔐 File Integrity Verification
- Generates a SHA-256 hash for uploaded files
- Stores the file hash with the memory record
- Allows users to select a file and verify it
- Detects whether the selected file matches the stored hash

### ⛓️ Blockchain Integration
- Solidity smart contract
- Ganache local Ethereum blockchain
- Hardhat development environment
- Web3.py integration with Flask
- Stores memory information and file hashes on the blockchain
- Displays blockchain storage status in the application

### 👥 User Data Isolation
Each memory is associated with the logged-in user's account.

A user can access only their own memories.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌─────────────────────────────┐
              │     Frontend Web Pages      │
              │      HTML / CSS / JS        │
              └─────────────┬───────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │       Flask Backend        │
              │          Python            │
              └───────┬───────────┬─────────┘
                      │           │
             ┌────────▼─────┐    ┌▼─────────────────┐
             │ MySQL        │    │ SHA-256 Hashing  │
             │ Database     │    │ File Integrity   │
             └──────────────┘    └────────┬─────────┘
                                          │
                                          ▼
                              ┌──────────────────────┐
                              │ Web3.py / Blockchain │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │ Solidity Smart       │
                              │ Contract             │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │ Ganache Local        │
                              │ Ethereum Network     │
                              └──────────────────────┘
🔄 Application Workflow
Register
   ↓
Login
   ↓
Dashboard
   ↓
Profile
   ↓
Upload Memory
   ↓
Generate SHA-256 File Hash
   ↓
Store Memory Record in MySQL
   ↓
Store Memory Information on Blockchain
   ↓
View Memories
   ↓
Download / Edit / Delete
   ↓
Verify File Integrity
   ↓
Logout

⛓️ Blockchain Implementation
The project uses a Solidity smart contract named:

MemoryChain

The smart contract maintains memory records containing:

Title
Description
File Hash

The contract provides functions such as:

addMemory()
getMemory()
totalMemories()

Ganache is used as the local Ethereum blockchain for development and demonstration.
Hardhat is used for smart-contract development and deployment.
Web3.py connects the Flask backend with the deployed smart contract.

🔐 File Integrity Verification
MemoryChain uses SHA-256 hashing to verify file integrity.

Upload
File
 ↓
SHA-256
 ↓
File Hash
 ↓
MySQL + Blockchain


Verification
Selected File
 ↓
SHA-256
 ↓
New Hash
 ↓
Compare with Stored Hash
 ↓
Match → File Verified
If the file is modified, its SHA-256 hash changes, allowing the application to detect that it no longer matches the stored hash.

🗄️ Database
The project uses MySQL with the database:
memorychain
Main tables:

users
memories
activity_logs

users
Stores user account information.

memories
Stores memory information including:

Title
Description
Filename
Transaction hash
Blockchain index
User ID
activity_logs
Stores application activity information.

📁 Project Structure

MemoryChain-Personal-Memory-Vault/
│
├── backend/
│   ├── app.py
│   ├── blockchain.py
│   ├── abi.json
│   └── uploads/
│
├── contracts/
│   └── MemoryChain.sol
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── login.js
│   ├── register.html
│   ├── register.js
│   ├── dashboard.html
│   ├── dashboard.js
│   ├── profile.html
│   ├── profile.js
│   ├── upload.html
│   ├── upload.js
│   ├── view_memories.html
│   ├── view.js
│   ├── edit_memory.html
│   ├── edit.js
│   ├── verify.html
│   ├── verify.js
│   └── style.css
│
├── scripts/
│   └── deploy.js
│
├── hardhat.config.js
├── package.json
├── package-lock.json
├── .gitignore
├── .env
└── README.md
.env, uploaded files, Python cache files, and other local/generated files are excluded from the GitHub repository using .gitignore.

🛠️ Technologies Used
Frontend

HTML
CSS
JavaScript

Backend

Python
Flask
Database
MySQL
Blockchain
Solidity
Ethereum Smart Contract
Ganache
Hardhat
Web3.py

Security / Integrity

SHA-256 hashing
Flask Session-based authentication
User-specific access control

Development Tools

Visual Studio Code
Git & GitHub

▶️ How to Run MemoryChain
1. Start MySQL and create the `memorychain` database.

2. Start Ganache on:
   http://127.0.0.1:7545

3. Deploy the smart contract:
   cd blockchain
   npx hardhat run scripts/deploy.js --network ganache

4. Start Flask:
   cd backend
   python app.py

5. Open in browser:
   http://127.0.0.1:5000/frontend/index.html

Requirements: Python, MySQL, Node.js/npm, Ganache, and Hardhat.

📌 Future Enhancements
Possible future improvements include:

Cloud storage integration
Production blockchain deployment
Stronger authentication
Password hashing
Email verification
Password reset
Mobile application
Advanced search and filtering
Improved activity logging
Secure cloud deployment

🎓 Academic Project

Project: MemoryChain – Personal Memory Vault
Developer: Syed Saqlain
Course: Bachelor of Computer Applications (BCA)
College: St. Philomena's College (Autonomous), Mysuru
Purpose: Academic / Educational Project

