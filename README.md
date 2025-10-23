# Video Subtitler

A Python script that extracts audio from video files and generates subtitles using OpenAI's Whisper speech recognition model.

## Features

- Extracts audio from any video format supported by moviepy
- Uses Whisper AI for accurate speech-to-text transcription
- Generates industry-standard SRT subtitle files
- Supports multiple languages with auto-detection
- Multiple model sizes for speed/accuracy tradeoff
- Automatic timestamp generation

## Prerequisites

- Python 3.8 or higher
- FFmpeg (required by moviepy)

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html or use Chocolatey:
```bash
choco install ffmpeg
```

## Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Note: The first time you run the script, Whisper will download the selected model (100MB-3GB depending on model size).

## Usage

### Basic Usage

```bash
python video_subtitler.py path/to/video.mp4
```

This will create a subtitle file named `video.srt` in the same directory.

### Advanced Options

```bash
python video_subtitler.py path/to/video.mp4 -o output.srt -m small -l en
```

#### Arguments

- `video_path` (required): Path to the input video file
- `-o, --output`: Output subtitle file path (default: same name as video with .srt extension)
- `-m, --model`: Whisper model size (default: base)
  - `tiny`: Fastest, least accurate (~1GB RAM)
  - `base`: Good balance (default, ~1GB RAM)
  - `small`: Better accuracy (~2GB RAM)
  - `medium`: High accuracy (~5GB RAM)
  - `large`: Best accuracy (~10GB RAM)
- `-l, --language`: Language code (e.g., 'en', 'es', 'fr', 'de'). Auto-detects if not specified
- `--keep-audio`: Keep the extracted audio file

### Examples

Generate subtitles with auto-detected language:
```bash
python video_subtitler.py my_video.mp4
```

Use a larger model for better accuracy:
```bash
python video_subtitler.py my_video.mp4 -m medium
```

Specify language and custom output path:
```bash
python video_subtitler.py lecture.mp4 -o subtitles/lecture_en.srt -l en
```

Keep the extracted audio file:
```bash
python video_subtitler.py video.mp4 --keep-audio
```

## Output Format

The script generates SRT (SubRip) subtitle files, which are compatible with most video players and editing software. Example format:

```
1
00:00:00,000 --> 00:00:02,500
Hello, this is the first subtitle.

2
00:00:02,500 --> 00:00:05,000
This is the second subtitle.
```

## Supported Video Formats

Any format supported by moviepy/FFmpeg:
- MP4, AVI, MOV, MKV, FLV, WMV, WebM, and many more

## Testing

The project includes a comprehensive test suite using pytest.

### Running Tests

1. First, create sample test videos:
```bash
python tests/create_sample_videos.py
```

2. Run the test suite:
```bash
pytest
```

3. Run tests with coverage report:
```bash
pytest --cov=video_subtitler --cov-report=html
```

4. Run only fast tests (exclude slow transcription tests):
```bash
pytest -m "not slow"
```

### Test Structure

- `tests/test_video_subtitler.py` - Main test suite
  - Unit tests for utility functions (timestamp formatting, etc.)
  - Integration tests for audio extraction
  - SRT file generation tests
  - Full workflow integration tests
- `tests/create_sample_videos.py` - Creates small sample videos for testing
- `pytest.ini` - Pytest configuration

## Troubleshooting

**Error: ffmpeg not found**
- Install FFmpeg using the instructions in Prerequisites

**Out of memory error**
- Use a smaller model size (e.g., `-m tiny` or `-m base`)

**Poor transcription quality**
- Try a larger model (e.g., `-m medium` or `-m large`)
- Specify the correct language with `-l` option

## License

MIT License - feel free to use and modify as needed.
