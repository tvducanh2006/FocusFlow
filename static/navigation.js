let isProcessing = false;

function navigate(direction) {
    if (isProcessing) return; // Prevent multiple clicks
    isProcessing = true;

    // Show the loading indicator
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'inline';
    }

    // Navigate to the desired view and direction
    const view = getCurrentView();
    window.location.href = `?direction=${direction}&view=${view}`;

    // Reset processing state after some delay
    setTimeout(() => {
        isProcessing = false;
    }, 1000); // Adjust delay if necessary
}

function getCurrentView() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('view') || 'month'; // Default to 'month' view
}
