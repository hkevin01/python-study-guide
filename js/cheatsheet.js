// Improved syntax highlighting and navigation for Python Study Guide

document.addEventListener('DOMContentLoaded', function() {
    // Navigation logic
    function showPage(pageId, btn) {
        var pages = document.querySelectorAll('.page');
        pages.forEach(function(page) {
            page.classList.remove('active');
        });
        var buttons = document.querySelectorAll('.nav-btn');
        buttons.forEach(function(b) {
            b.classList.remove('active');
        });
        var page = document.getElementById(pageId);
        if (page) {
            page.classList.add('active');
        }
        if (btn) {
            btn.classList.add('active');
        }
    }

    // Attach click handlers to nav buttons
    document.querySelectorAll('.nav-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var pageId = btn.getAttribute('data-page');
            showPage(pageId, btn);
        });
    });

    // Improved Python syntax highlighting (non-overlapping)
    document.querySelectorAll('pre code').forEach(function(block) {
        let html = block.textContent;
        // Comments first
        html = html.replace(/(#.*)/g, '<span class="py-comment">$1</span>');
        // Strings
        html = html.replace(/("[^"]*"|'[^']*')/g, '<span class="py-string">$1</span>');
        // Keywords (not inside strings/comments)
        html = html.replace(/\b(def|class|return|if|else|elif|for|while|try|except|import|from|as|with|pass|break|continue|lambda|yield|global|nonlocal|assert|del|raise|True|False|None)\b/g, '<span class="py-keyword">$1</span>');
        // Numbers
        html = html.replace(/\b([0-9]+)\b/g, '<span class="py-number">$1</span>');
        block.innerHTML = html;
    });
});
