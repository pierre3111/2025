// This is a simple example; you can add more advanced logic based on your needs.

// Show a message after email submission (you can add this to your collect_email view redirect if needed)
function showEmailSubmittedMessage() {
    alert('Thank you! Your email has been submitted.');
}

// Example auto-refresh function (optional)
function autoRefreshGallery(intervalInSeconds) {
    setTimeout(function() {
        location.reload();
    }, intervalInSeconds * 1000);
}

// Optional: Auto-refresh gallery every 30 seconds
// Uncomment if you want this behavior
// autoRefreshGallery(30);
