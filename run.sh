#!/bin/bash
# Run the Python Study Sheet GUI

# Ensure tkhtmlview is installed
pip show tkhtmlview > /dev/null 2>&1 || pip install tkhtmlview

# Run the viewer
python3 view_study_sheet.py
