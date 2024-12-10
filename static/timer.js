document.addEventListener("DOMContentLoaded", () => {
    let timer;
    let timeLeft = 25 * 60; // Default 25 minutes
    let isRunning = false;
    let mode = "work"; // Default mode
    let selectedTaskId = null; // Track selected task
    let selectedTaskName = "None";
    let remainingTime = 0; // Remaining time for the selected task

    const timerDisplay = document.getElementById("timer-display");
    const startButton = document.getElementById("start-button");
    const resetIcon = document.getElementById("reset-icon");
    const workMode = document.getElementById("work-mode");
    const shortBreakMode = document.getElementById("short-break-mode");
    const longBreakMode = document.getElementById("long-break-mode");
    const selectedTaskNameElement = document.getElementById("selected-task-name");
    const pomodoroTimer = document.querySelector(".pomodoro-timer");

    // Update the timer display
    const updateDisplay = () => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

        // Update remaining time display for the selected task
        if (selectedTaskId && mode === "work") {
            const taskRemainingTimeElement = document.getElementById(`remaining-time-${selectedTaskId}`);
            const taskHours = Math.floor(remainingTime / 3600);
            const taskMinutes = Math.floor((remainingTime % 3600) / 60);
            const taskSeconds = remainingTime % 60;

            taskRemainingTimeElement.textContent = `${String(taskHours).padStart(2, "0")}:${String(taskMinutes).padStart(2, "0")}:${String(taskSeconds).padStart(2, "0")}`;
        }
    };

    const resetTimer = () => {
        clearInterval(timer);
        isRunning = false;
        if (mode === "work") timeLeft = 25 * 60;
        else if (mode === "short-break") timeLeft = 5 * 60;
        else if (mode === "long-break") timeLeft = 15 * 60;

        updateDisplay();
        startButton.textContent = "START";
    };

    const switchMode = (newMode) => {
        mode = newMode;
        resetTimer();

        // Remove active class from all buttons and add it to the selected one
        [workMode, shortBreakMode, longBreakMode].forEach((button) => button.classList.remove("active-mode"));
        if (mode === "work") {
            workMode.classList.add("active-mode");
            pomodoroTimer.style.backgroundColor = "#8B0000";
        } else if (mode === "short-break") {
            shortBreakMode.classList.add("active-mode");
            pomodoroTimer.style.backgroundColor = "#5d9e9e";
        } else if (mode === "long-break") {
            longBreakMode.classList.add("active-mode");
            pomodoroTimer.style.backgroundColor = "#466fb3";
        }
    };

    const startTimer = () => {
        if (mode === "work" && !selectedTaskId) {
            alert("Please select a task before starting the Pomodoro timer.");
            return;
        }

        if (isRunning) {
            clearInterval(timer);
            isRunning = false;
            startButton.textContent = "START";
        } else {
            isRunning = true;
            startButton.textContent = "PAUSE";

            timer = setInterval(() => {
                if (timeLeft > 0) {
                    timeLeft--;

                    if (mode === "work" && selectedTaskId) {
                        remainingTime--;
                    }

                    updateDisplay();

                    // Update remaining time in the database every 5 seconds
                    if (mode === "work" && timeLeft % 5 === 0 && selectedTaskId) {
                        fetch("/update_remaining_time", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                task_id: selectedTaskId,
                                remaining_time: remainingTime,
                            }),
                        });
                    }
                } else {
                    clearInterval(timer);
                    isRunning = false;
                    alert(`${mode === "work" ? "Time for a break!" : "Back to work!"}`);
                    switchMode(mode === "work" ? "short-break" : "work");
                }
            }, 1000);
        }
    };

    const selectTask = (taskName, taskId, taskRemainingTime) => {
        selectedTaskName = taskName;
        selectedTaskId = taskId;
        remainingTime = parseInt(taskRemainingTime, 10); // Convert to seconds
        selectedTaskNameElement.textContent = taskName;
    };

    startButton.addEventListener("click", startTimer);
    resetIcon.addEventListener("click", resetTimer);

    workMode.addEventListener("click", () => switchMode("work"));
    shortBreakMode.addEventListener("click", () => switchMode("short-break"));
    longBreakMode.addEventListener("click", () => switchMode("long-break"));

    updateDisplay();

    // Expose the selectTask function globally for inline onclick
    window.selectTask = selectTask;
});
