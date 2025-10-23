#!/bin/bash
# Test runner script for video-subtitler

set -e

echo "Video Subtitler Test Runner"
echo "============================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg is not installed. Some tests may fail."
    echo "Install FFmpeg before running tests."
    echo ""
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "Dependencies already installed"
fi

echo ""
echo "Creating sample videos..."
if [ ! -d "tests/fixtures" ] || [ -z "$(ls -A tests/fixtures/*.mp4 2>/dev/null)" ]; then
    python3 tests/create_sample_videos.py
else
    echo "Sample videos already exist (delete tests/fixtures/*.mp4 to regenerate)"
fi

echo ""
echo "Running tests..."
python3 -m pytest "$@"
