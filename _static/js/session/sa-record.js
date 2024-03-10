// Timestamps
let stopwatchInterval;
let stowatchTime;
let previousTime;
let lastPausedTime;
let nextPause = 60;

// Stopwatch flags
let recording = false;
let paused = false;

// Plotting array
const timeList = [];
const valueList = [];
const recordedData = [];
const rateData = {};

// Stopwatch buttons
const stopwatch = document.getElementById("stopwatch");
const startStopButton = document.getElementById("startStopButton");
const saveButton = document.getElementById("saveButton");
const discardButton = document.getElementById("discardButton");

// Recorded inputs
const csvInput = document.getElementById("csvInput");
const timeInput = document.getElementById("timeInput");
const rateInput = document.getElementById("rateInput");

// Modals
let resultModal = new bootstrap.Modal(document.getElementById('modal-result'));
let rateModal = new bootstrap.Modal(document.getElementById('modal-rate'));

// Audio effects
let audioCountdown = new Audio("/static/sounds/countdown.mp3");
let audioStart = new Audio("/static/sounds/start.mp3");
let audioAttention = new Audio(`/static/sounds/attention-${getRandomInt(6)}.mp3`);
let audioFinish = new Audio("/static/sounds/finish.mp3");


function formatTime(milliseconds) {
    const seconds = milliseconds / 1000;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = (seconds % 60).toFixed(2);
    return `${seconds.toFixed(2)}`;
}

function getRandomInt(n) {
    return Math.floor(Math.random() * (n + 1));
}

/**
 * Run stopwatch
 */
startStopButton.addEventListener("click", () => {
    if (recording) {
        const csvContent = recordedData.map(data => data.join(",")).join("\n");

        csvInput.value = encodeURI(csvContent);
        timeInput.value = stopwatch.innerText;
        rateInput.value = JSON.stringify(rateData);

        audioFinish.play();

        // Clear interval
        clearInterval(stopwatchInterval);
        startStopButton.innerText = "Start";
        saveButton.disabled = false;

        // Show modal
        plotModal();
        resultModal.show();
    } else {
        // Clear previous data
        timeList.length = 0;
        valueList.length = 0;

        // Set last paused time to current time
        previousTime = 0;
        lastPausedTime = new Date().getTime();

        // Play starting sound
        audioStart.play();

        // Start interval
        stopwatchInterval = setInterval(() => {
            if (!paused) {
                console.log("running");
                stopwatchTime = previousTime + (new Date().getTime() - lastPausedTime);
                let time = (stopwatchTime / 1000).toFixed(2);
                let value = slider.value;

                stopwatch.innerText = formatTime(stopwatchTime);

                timeList.push(time);
                valueList.push(value);
                recordedData.push([time, value]);

                // Pause the timer if time reached at nextPause
                if (time >= nextPause) {
                    paused = true;

                    audioAttention.play();
                    previousTime = stopwatchTime;
                    rateModal.show();
                }
            }
        }, 50);

        startStopButton.innerText = "Stop";
        saveButton.disabled = true;

        if (modalChart) {
            modalChart.destroy();
        }
    }
    recording = !recording;
});

// Call emoji elements
const emojis = document.querySelectorAll('.emoji');

// Add hover effect to emojis
emojis.forEach(emoji => {
    emoji.addEventListener('mouseenter', () => {
        emoji.classList.add('text-primary');
    });
    emoji.addEventListener('mouseleave', () => {
        emoji.classList.remove('text-primary');
    });
});

// Add click event listener to emojis
emojis.forEach(emoji => {
    emoji.addEventListener('click', () => {
        const score = emoji.dataset.score;
        rateData[nextPause] = score;

        let time = 30 * (2 ** score);
        if (score * Object.keys(rateData)[rateData.length - 1] == 4) {
            time = 180;
        }
        nextPause += time;

        lastPausedTime = new Date().getTime();
        audioAttention = new Audio(`/static/sounds/attention-${getRandomInt(6)}.mp3`);
        paused = false;
    });
});

// Reset stopwatch text for discard button
discardButton.addEventListener("click", () => {
    stopwatch.innerText = "0.00";
});

/**
 * Draw chart for result modal
 */
let modalChart;

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
