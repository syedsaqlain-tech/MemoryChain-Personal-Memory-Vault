const ctx = document.getElementById("memoryChart");

const memoryChart = new Chart(ctx, {
    type: "bar",

    data: {
        labels: ["Total", "Blockchain"],

        datasets: [{
            label: "Memory Statistics",
            data: [0, 0],
            borderWidth: 1
        }]
    },

    options: {
        responsive: true
    }
});

async function loadDashboard() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/dashboard_stats",
            {
                credentials: "include"
            }
        );

        const data = await response.json();

        if (!response.ok || data.success === false) {
            alert(data.message || "Please login first.");
            return;
        }

        // Update dashboard cards
        document.getElementById("total").innerHTML =
            data.total_memories;

        document.getElementById("blockchain").innerHTML =
            data.blockchain_memories;

        document.getElementById("users").innerHTML =
            data.users;

        // Update chart
        memoryChart.data.datasets[0].data = [
            data.total_memories,
            data.blockchain_memories
        ];

        memoryChart.update();

    } catch (error) {
        console.error("Dashboard Error:", error);
    }
}

async function loadRecentMemories() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/recent_memories",
            {
                credentials: "include"
            }
        );

        const data = await response.json();

        if (!response.ok || data.success === false) {
            console.error(
                data.message || "Unable to load recent memories."
            );
            return;
        }

        let html = "";

        data.forEach(memory => {

            html += `
                <div class="recent-card">

                    <h3>${memory.title}</h3>

                    <p>${memory.description}</p>

                </div>
            `;

        });

        document.getElementById("recentMemories").innerHTML = html;

    } catch (error) {
        console.error("Recent Memories Error:", error);
    }
}

function updateClock() {

    const now = new Date();

    document.getElementById("date").innerHTML =
        now.toLocaleDateString();

    document.getElementById("time").innerHTML =
        now.toLocaleTimeString();
}

function logout() {

    window.location.href = "login.html";
}


// Start dashboard
updateClock();

setInterval(updateClock, 1000);

loadDashboard();

loadRecentMemories();