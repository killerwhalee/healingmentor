// Get references to the select element and the play button
const selectElement = document.getElementById("select-audio");
const playButton = document.getElementById("button-play");
const progressBar = document.getElementById("progress-bar");
const reportButton = document.getElementById("button-report");
const saveButton = document.getElementById("saveButton");

const lectureInput = document.getElementById("lecture-input");

let audioElement;

function updateProgressBar() {
    const currentTime = audioElement.currentTime;
    const duration = audioElement.duration;
    const progressPercentage = (currentTime / duration) * 100;

    progressBar.style.width = progressPercentage + "%";

    if (progressPercentage > 90) {
        reportButton.classList.remove("disabled");
        saveButton.disabled = false;
    }
}

selectElement.addEventListener("change", () => {
    const selectedOption = selectElement.options[selectElement.selectedIndex];

    lectureInput.value = selectedOption.value;
    
    audioElement.currentTime = 0;
    reportButton.classList.add("disabled");
    saveButton.disabled = true;
});

function togglePlayStop() {
    const audioId = selectElement.selectedIndex;

    audioElement = document.querySelector(`#audio-${audioId}`);

    if (audioElement) {
        if (audioElement.paused) {
            selectElement.disabled = true;
            audioElement.play();
            playButton.textContent = "Pause";
            audioElement.addEventListener("timeupdate", updateProgressBar);
        } else {
            selectElement.disabled = false;
            audioElement.pause();
            playButton.textContent = "Play";
        }
    }
}

// Add click event listener to the play button
playButton.addEventListener("click", togglePlayStop);