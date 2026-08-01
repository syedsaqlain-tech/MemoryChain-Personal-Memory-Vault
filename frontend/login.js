async function login(){

const email=document.getElementById("email").value;

const password=document.getElementById("password").value;

if(email==""||password==""){

alert("Please enter Email and Password");

return;

}

const response=await fetch("http://127.0.0.1:5000/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

email:email,

password:password

})

});

const data=await response.json();

if(data.success){

alert("Login Successful");

window.location.href="dashboard.html";

}else{

alert(data.message);

}

}
async function login(){

const email=document.getElementById("email").value;

const password=document.getElementById("password").value;

if(email==""||password==""){

alert("Please enter Email and Password");

return;

}

const response=await fetch("http://127.0.0.1:5000/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

email:email,

password:password

})

});

const data=await response.json();

if(data.success){

alert("Login Successful");

window.location.href="dashboard.html";

}else{

alert(data.message);

}

}