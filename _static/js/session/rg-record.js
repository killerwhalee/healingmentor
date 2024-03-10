// Timestamps
let stopwatchInterval;
let stopwatchTime;
let clockTime;

// Stopwatch flags
let recording = false;

// Plotting Array
const timeList = [];
const valueList = [];
const recordedData = [];

// Stopwatch buttons
const stopwatch = document.getElementById("stopwatch");
const startStopButton = document.getElementById("startStopButton");
const saveButton = document.getElementById("saveButton");
const discardButton = document.getElementById("discardButton");

// Recorded inputs
const csvInput = document.getElementById("csvInput");
const timeInput = document.getElementById("timeInput");

// Audio effects
let audioCountdown = new Audio("/static/sounds/countdown.mp3");
let audioStart = new Audio("/static/sounds/start.mp3");
let audioFinish = new Audio("/static/sounds/finish.mp3");
let audioReward = new Audio("/static/sounds/reward.mp3");


function formatTime(milliseconds) {
    const seconds = milliseconds / 1000;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = (seconds % 60).toFixed(2);
    return `${seconds.toFixed(2)}`;
}

/**
 * Run stopwatch
 */
startStopButton.addEventListener("click", () => {
    if (recording) {
        const csvContent = recordedData.map(data => data.join(",")).join("\n");
        csvInput.value = encodeURI(csvContent);
        timeInput.value = stopwatch.innerText;

        audioFinish.play();

        // Clear interval
        clearInterval(stopwatchInterval);
        startStopButton.innerText = "Start";
        saveButton.disabled = false;

        var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
        plotModal();
        myModal.show();
    } else {
        // Clear previous data
        timeList.length = 0;
        valueList.length = 0;
        clockTime = new Date().getTime();

        audioStart.play();

        // Start interval
        stopwatchInterval = setInterval(() => {
            stopwatchTime = new Date().getTime() - clockTime;
            let time = (stopwatchTime / 1000).toFixed(2);
            let value = slider.value;

            stopwatch.innerText = formatTime(stopwatchTime);

            timeList.push(time);
            valueList.push(value);
            recordedData.push([time, value]);
        }, 50);

        startStopButton.innerText = "Stop";
        saveButton.disabled = true;

        if (modalChart) {
            modalChart.destroy();
        }
    }
    recording = !recording;
});

// Reset stopwatch text for discard button
discardButton.addEventListener("click", () => {
    stopwatch.innerText = "0.00";
});

/**
 * Draw chart for result modal
 */
var modalChart;

function plotModal() {
    // Take input from html
    const Chart = window.Chart;

    color = Math.floor(Math.random() * 240);
    light = Math.floor(Math.random() * 80);

    GRAPH = document.getElementById('plotting-modal');

    modalChart = new Chart(GRAPH, {
        type: 'line',
        data: {
            labels: timeList,
            datasets: [{
                data: valueList,
                fill: false,
                borderColor: `hsl(${color}, 100%, ${light}%)`,
                tension: 0.1
            }]
        },
        options: {
            elements: {
                point: {
                    pointStyle: false
                },
            },
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    type: 'linear'
                },
                y: {
                    display: false,
                    min: -5,
                    max: 105
                },
            },
        },
        plugins: []
    });
}
