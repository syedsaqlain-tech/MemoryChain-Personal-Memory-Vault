async function login() {

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Please enter Email and Password.");
        return;
    }

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                credentials: "include",

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok && data.success) {

            alert("Login Successful");

            window.location.href = "dashboard.html";

        } else {

            alert(data.message || "Invalid Email or Password.");

        }

    } catch (error) {

        console.error("Login Error:", error);

        alert("Unable to connect to the server.");

    }
}