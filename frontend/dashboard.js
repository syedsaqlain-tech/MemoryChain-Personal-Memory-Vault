const ctx=document.getElementById("memoryChart");

const memoryChart=new Chart(ctx,{

type:"bar",

data:{

labels:["Total","Blockchain"],

datasets:[{

label:"Memory Statistics",

data:[0,0],

borderWidth:1

}]

},

options:{

responsive:true

}

});

async function loadChart(){

const response=await fetch("http://127.0.0.1:5000/dashboard_stats");

const data=await response.json();

memoryChart.data.datasets[0].data=[

data.total_memories,

data.blockchain_memories

];

memoryChart.update();

}

loadChart();
async function loadDashboard(){

const response=await fetch("http://127.0.0.1:5000/dashboard_stats");

const data=await response.json();

document.getElementById("total").innerHTML=data.total_memories;

document.getElementById("blockchain").innerHTML=data.blockchain_memories;

document.getElementById("users").innerHTML=data.users;

}
function updateClock(){

const now=new Date();

document.getElementById("date").innerHTML=
now.toLocaleDateString();

document.getElementById("time").innerHTML=
now.toLocaleTimeString();

}

setInterval(updateClock,1000);

updateClock();

loadDashboard();

function logout(){

window.location.href="login.html";

}
async function loadRecentMemories(){

const response = await fetch("http://127.0.0.1:5000/recent_memories");

const data = await response.json();

let html = "";

data.forEach(memory=>{

html += `
<div class="recent-card">

<h3>${memory.title}</h3>

<p>${memory.description}</p>

</div>
`;

});

document.getElementById("recentMemories").innerHTML = html;

}

loadRecentMemories();