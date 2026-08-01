async function uploadMemory() {

    try {

        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const file = document.getElementById("file").files[0];

        if(title=="" || description=="" || !file){
            alert("Please fill all fields.");
            return;
        }

        let formData = new FormData();
        formData.append("title", title);
        formData.append("description", description);
        formData.append("file", file);

        const response = await fetch("http://127.0.0.1:5000/upload",{
            method:"POST",
            body:formData
        });

        const data = await response.json();

        document.getElementById("status").innerHTML = data.message;

    } catch(error){

        console.log(error);
        alert("Backend Connection Error");

    }
}