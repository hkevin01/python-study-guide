// Navigation functionality
function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    // Show selected page
    document.getElementById(pageId).classList.add('active');
    // Update button states
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    // Save to localStorage
    localStorage.setItem('lastPage', pageId);
}
// Load last viewed page
window.onload = function() {
    const lastPage = localStorage.getItem('lastPage') || 'page1';
    showPage(lastPage);
};
// Add search functionality
function addSearch() {
    const searchBox = document.createElement('input');
    searchBox.type = 'text';
    searchBox.placeholder = 'Search...';
    searchBox.className = 'search-box';
    searchBox.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            section.style.display = text.includes(searchTerm) ? 'block' : 'none';
        });
    });
    document.querySelector('header').appendChild(searchBox);
}
// Copy code functionality
function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre');
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.textContent = 'Copy';
        button.className = 'copy-btn';
        button.onclick = function() {
            navigator.clipboard.writeText(block.textContent);
            button.textContent = 'Copied!';
            setTimeout(() => button.textContent = 'Copy', 2000);
        };
        block.appendChild(button);
    });
}
// Highlight Python code
function highlightPythonCode(code) {
    const keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'break', 'continue', 'pass', 'raise', 'assert', 'lambda', 'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None', 'self', 'super', 'global', 'nonlocal'];
    const builtins = ['print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 'delattr', 'open', 'file', 'input', 'sum', 'min', 'max'];
    let highlighted = code;
    highlighted = highlighted.replace(/(["'])(?:(?=(\\?))\2.)*?\1/g, '<span class="string">$&</span>');
    highlighted = highlighted.replace(/#.*/g, '<span class="comment">$&</span>');
    highlighted = highlighted.replace(/\b\d+\.?\d*\b/g, '<span class="number">$&</span>');
    keywords.forEach(keyword => {
        const regex = new RegExp('\\b' + keyword + '\\b', 'g');
        highlighted = highlighted.replace(regex, '<span class="keyword">' + keyword + '</span>');
    });
    builtins.forEach(builtin => {
        const regex = new RegExp('\\b' + builtin + '\\b(?=\\()', 'g');
        highlighted = highlighted.replace(regex, '<span class="builtin">' + builtin + '</span>');
    });
    highlighted = highlighted.replace(/(\bdef\s+)(\w+)/g, '$1<span class="function">$2</span>');
    highlighted = highlighted.replace(/(\bclass\s+)(\w+)/g, '$1<span class="function">$2</span>');
    highlighted = highlighted.replace(/@\w+/g, '<span class="decorator">$&</span>');
    return highlighted;
}
document.addEventListener('DOMContentLoaded', function() {
    addSearch();
    addCopyButtons();
    document.querySelectorAll('pre code').forEach(function(block) {
        block.innerHTML = highlightPythonCode(block.textContent);
    });
});
