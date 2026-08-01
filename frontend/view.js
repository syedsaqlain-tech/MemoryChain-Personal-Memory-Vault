async function loadMemories() {

    const response = await fetch("http://127.0.0.1:5000/memories");
    const memories = await response.json();

    const table = document.getElementById("tableBody");
    table.innerHTML = "";

    memories.forEach(memory => {

        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${memory.title}</td>
            <td>${memory.description}</td>
            <td>
                <a href="http://127.0.0.1:5000/download/${memory.filename}" target="_blank">
                    Download
                </a>
            </td>
            <td>${memory.transaction_hash ? "✅ Stored" : "❌ Not Stored"}</td>
            <td>
                <button onclick="editMemory(${memory.id})">✏️ Edit</button>
                <button onclick="verifyMemory(${memory.id})">🛡️ Verify</button>
                <button onclick="deleteMemory(${memory.id})">🗑️ Delete</button>
            </td>
        `;

        table.appendChild(row);

    });

}

function searchMemory() {

    let input = document.getElementById("searchBox").value.toLowerCase();

    let rows = document.querySelectorAll("#tableBody tr");

    rows.forEach(row => {

        let title = row.cells[0].innerText.toLowerCase();

        row.style.display = title.includes(input) ? "" : "none";

    });

}

function editMemory(id) {
    window.location.href = "edit_memory.html?id=" + id;
}

function verifyMemory(id) {
    window.location.href = "verify.html?id=" + id;
}

async function deleteMemory(id) {

    if(confirm("Delete this memory?")){

        const response = await fetch(
            "http://127.0.0.1:5000/delete_memory/" + id,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        alert(data.message);

        loadMemories();

    }

}

loadMemories();