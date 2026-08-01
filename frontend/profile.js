async function loadProfile() {

    const response = await fetch("http://127.0.0.1:5000/profile");

    const user = await response.json();

    document.getElementById("name").innerHTML = user.name;

    document.getElementById("email").innerHTML = user.email;

}

loadProfile();