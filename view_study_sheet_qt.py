import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

HTML_FILE = "python-study.html"

class StudySheetViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Study Sheet Viewer (Qt)")
        self.setGeometry(100, 100, 900, 700)
        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)
        self.load_html()

    def load_html(self):
        abs_path = os.path.abspath(HTML_FILE)
        if os.path.exists(abs_path):
            self.webview.load(QUrl.fromLocalFile(abs_path))
        else:
            self.webview.setHtml("<h2>File not found</h2>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = StudySheetViewer()
    viewer.show()
    sys.exit(app.exec())
