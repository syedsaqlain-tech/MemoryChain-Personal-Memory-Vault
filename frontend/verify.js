async function verifyFile() {

    const id =
        document.getElementById("memoryId").value.trim();

    const file =
        document.getElementById("file").files[0];

    if (!id) {
        alert("Memory ID not found.");
        return;
    }

    if (!file) {
        alert("Please select a file.");
        return;
    }

    let formData = new FormData();

    formData.append("id", id);
    formData.append("file", file);

    document.getElementById("result").innerHTML =
        "⏳ Verifying...";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/verify",
            {
                method: "POST",

                credentials: "include",

                body: formData
            }
        );

        const data = await response.json();

        document.getElementById("result").innerHTML =
            data.message;

    } catch (error) {

        console.error("Verify Error:", error);

        document.getElementById("result").innerHTML =
            "Unable to connect to the server.";
    }
}