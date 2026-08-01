const params = new URLSearchParams(window.location.search);

const id = params.get("id");

async function loadMemory(){

const response = await fetch(
"http://127.0.0.1:5000/memory/"+id
);

const data = await response.json();

document.getElementById("title").value = data.title;

document.getElementById("description").value = data.description;

}

async function updateMemory(){

const title = document.getElementById("title").value;

const description = document.getElementById("description").value;

const response = await fetch(

"http://127.0.0.1:5000/update_memory/"+id,

{

method:"PUT",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

title:title,

description:description

})

}

);

const data = await response.json();

alert(data.message);

window.location.href="view_memories.html";

}

loadMemory();