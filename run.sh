#!/bin/bash
# Run the Python Study Sheet GUI

# Ensure tkhtmlview is installed
pip show tkhtmlview > /dev/null 2>&1 || pip install tkhtmlview

# Ensure PyQt6 and PyQt6-WebEngine are installed
pip show PyQt6 > /dev/null 2>&1 || pip install PyQt6
pip show PyQt6-WebEngine > /dev/null 2>&1 || pip install PyQt6-WebEngine

# Run the viewer
python3 view_study_sheet_qt.py
