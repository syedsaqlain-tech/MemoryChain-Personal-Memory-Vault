async function loadProfile() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/profile",
            {
                credentials: "include"
            }
        );

        const user = await response.json();

        if (!response.ok || user.success === false) {

            alert(user.message || "Please login first.");

            window.location.href = "login.html";

            return;
        }

        document.getElementById("name").innerHTML =
            user.name;

        document.getElementById("email").innerHTML =
            user.email;

    } catch (error) {

        console.error("Profile Error:", error);

        alert("Unable to load profile.");

    }
}

loadProfile();