// navigation.js
// Handles navigation between study guide sections

function showPage(pageId) {
    // Hide all pages
    var pages = document.querySelectorAll('.page');
    pages.forEach(function(page) {
        page.classList.remove('active');
    });
    // Remove active class from all buttons
    var buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });
    // Show the selected page
    var page = document.getElementById(pageId);
    if (page) {
        page.classList.add('active');
    }
    // Set the clicked button as active
    var event = window.event;
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Optionally, you can add keyboard navigation or other features here
});
