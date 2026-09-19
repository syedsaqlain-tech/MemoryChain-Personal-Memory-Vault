async function uploadMemory() {

    try {

        const title = document.getElementById("title").value.trim();
        const description = document.getElementById("description").value.trim();
        const file = document.getElementById("file").files[0];

        if (title === "" || description === "" || !file) {
            alert("Please fill all fields.");
            return;
        }

        let formData = new FormData();

        formData.append("title", title);
        formData.append("description", description);
        formData.append("file", file);

        const response = await fetch(
            "http://127.0.0.1:5000/upload",
            {
                method: "POST",

                credentials: "include",

                body: formData
            }
        );

        const data = await response.json();

        if (response.ok && data.success) {

            document.getElementById("status").innerHTML =
                data.message;

        } else {

            document.getElementById("status").innerHTML =
                data.message || "Upload failed.";

        }

    } catch (error) {

        console.error("Upload Error:", error);

        alert("Backend Connection Error");

    }
}