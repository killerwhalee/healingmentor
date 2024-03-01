// Get references to the select element and the play button
const selectElement = document.getElementById("select-audio");
const playButton = document.getElementById("button-play");
const progressBar = document.getElementById("progress-bar");
const reportButton = document.getElementById("button-report");

let audioElement;

function updateProgressBar() {
    const currentTime = audioElement.currentTime;
    const duration = audioElement.duration;
    const progressPercentage = (currentTime / duration) * 100;

    progressBar.style.width = progressPercentage + "%";

    if (progressPercentage > 90) {
        reportButton.classList.remove("disabled");
    }
}

selectElement.addEventListener("change", function () {
    reportButton.classList.add("disabled");
});

function togglePlayStop() {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const audioId = selectedOption.value;
    audioElement = document.querySelector(`#audio-${audioId}`);

    if (audioElement) {
        if (audioElement.paused) {
            selectElement.disabled = true;
            audioElement.play();
            playButton.textContent = "Stop";
            audioElement.addEventListener("timeupdate", updateProgressBar);
        } else {
            selectElement.disabled = false;
            audioElement.pause();
            audioElement.currentTime = 0;
            playButton.textContent = "Play";
        }
    }
}

// Add click event listener to the play button
playButton.addEventListener("click", togglePlayStop);