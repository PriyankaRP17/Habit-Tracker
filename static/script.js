function togglePassword() {
    const passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

function togglePassword2() {
    const passwordField = document.getElementById("Input2");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

function togglePassword3() {
    const passwordField = document.getElementById("Input3");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

function createLineChart(canvasId) {
    const canvas = document.getElementById(canvasId);
    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: JSON.parse(canvas.dataset.labels),
            datasets: [{
                label: 'Habits Completed',
                data: JSON.parse(canvas.dataset.values),
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true,
                tension: 0.3
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

function createBarChart(canvasId) {
    const canvas = document.getElementById(canvasId);
    new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: JSON.parse(canvas.dataset.labels),
            datasets: [{
                label: 'Habit Frequency',
                data: JSON.parse(canvas.dataset.values),
                backgroundColor: 'rgba(177, 171, 122, 0.7)'
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

function createPieChart(canvasId) {
    const canvas = document.getElementById(canvasId);
    new Chart(canvas.getContext('2d'), {
        type: 'pie',
        data: {
            labels: JSON.parse(canvas.dataset.labels),
            datasets: [{
                label: 'Preferred Time',
                data: JSON.parse(canvas.dataset.values),
                backgroundColor: [
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(192, 114, 75, 0.7)',
                    'rgba(156, 145, 128, 0.7)'
                ]
            }]
        },
        options: { responsive: true }
    });
}

createLineChart('completionChart');
createBarChart('freqChart');
createPieChart('timeChart');


function checkReminders(preferredTimes) {
    const now = new Date();
    const hour = now.getHours();

    let currentSlot = "";
    if (hour >= 5 && hour < 12) {
        currentSlot = "Morning";
    } else if (hour >= 12 && hour < 18) {
        currentSlot = "Afternoon";
    } else {
        currentSlot = "Night";
    }

    const reminderBox = document.getElementById("reminderBox");

    if (preferredTimes.includes(currentSlot)) {
        reminderBox.style.display = "block";
        reminderBox.innerText = `⏰ Reminder: You have habits scheduled for ${currentSlot}. Don't forget to complete them!`;
    } else {
        reminderBox.style.display = "block";
        reminderBox.innerText = "Relax! No habits scheduled right now.";
    }
}

const timeChartEl = document.getElementById("timeChart");
const preferredTimes = timeChartEl.dataset.preferred
    ? JSON.parse(timeChartEl.dataset.preferred)
    : [];

checkReminders(preferredTimes);
setInterval(() => checkReminders(preferredTimes), 60000);
