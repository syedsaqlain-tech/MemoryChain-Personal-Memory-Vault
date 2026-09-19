const params = new URLSearchParams(window.location.search);

const id = params.get("id");


async function loadMemory() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/memory/" + id,
            {
                credentials: "include"
            }
        );

        const data = await response.json();

        if (!response.ok || data.success === false) {

            alert(data.message || "Memory not found.");

            window.location.href = "view_memories.html";

            return;
        }

        document.getElementById("title").value = data.title;

        document.getElementById("description").value = data.description;

    } catch (error) {

        console.error("Load Memory Error:", error);

        alert("Unable to load memory.");

    }
}


async function updateMemory() {

    const title =
        document.getElementById("title").value.trim();

    const description =
        document.getElementById("description").value.trim();

    if (title === "" || description === "") {

        alert("Please fill all fields.");

        return;
    }

    try {

        const response = await fetch(

            "http://127.0.0.1:5000/update_memory/" + id,

            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                credentials: "include",

                body: JSON.stringify({

                    title: title,

                    description: description

                })
            }
        );

        const data = await response.json();

        alert(data.message);

        if (response.ok && data.success) {

            window.location.href = "view_memories.html";

        }

    } catch (error) {

        console.error("Update Memory Error:", error);

        alert("Unable to update memory.");

    }
}


loadMemory();