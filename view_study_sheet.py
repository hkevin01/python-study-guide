from tkinter import Tk, Frame, BOTH
from tkhtmlview import HTMLLabel
import os

# Path to your HTML file
HTML_FILE = "python-study.html"

class StudySheetViewer(Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Study Sheet Viewer")
        self.geometry("900x700")
        self._load_html()

    def _load_html(self):
        if os.path.exists(HTML_FILE):
            with open(HTML_FILE, "r", encoding="utf-8") as f:
                html_content = f.read()
            html_label = HTMLLabel(self, html=html_content)
            html_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
        else:
            html_label = HTMLLabel(self, html="<h2>File not found</h2>")
            html_label.pack(fill=BOTH, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = StudySheetViewer()
    app.mainloop()
