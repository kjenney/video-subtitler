# Video Subtitler

A Python script that extracts audio from video files and generates subtitles using OpenAI's Whisper speech recognition model.

## Features

- Extracts audio from any video format supported by moviepy
- Uses Whisper AI for accurate speech-to-text transcription
- **Audio preprocessing** to improve transcription quality:
  - Audio normalization to even out volume levels
  - Dynamic range compression to boost quiet sections
  - Noise reduction to remove background noise
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
- `-m, --model`: Whisper model size (default: small)
  - `tiny`: Fastest, least accurate (~1GB RAM)
  - `base`: Good balance (~1GB RAM)
  - `small`: Better accuracy (default, ~2GB RAM)
  - `medium`: High accuracy (~5GB RAM)
  - `large`: Best accuracy (~10GB RAM)
- `-l, --language`: Language code (e.g., 'en', 'es', 'fr', 'de'). Auto-detects if not specified
- `--sensitivity`: Voice detection sensitivity (0.2-0.4). Lower values catch softer voices (default: 0.3)
- `--temperature`: Transcription temperature for unusual audio (default: 0.5)
- `--preprocess`: Enable audio preprocessing (normalization, compression, and noise reduction)
- `--no-normalize`: Disable audio normalization (when --preprocess is enabled)
- `--no-compress`: Disable dynamic range compression (when --preprocess is enabled)
- `--no-denoise`: Disable noise reduction (when --preprocess is enabled)
- `--keep-audio`: Keep the extracted audio file(s)

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

Process video with quiet or uneven audio (recommended for lectures, podcasts):
```bash
python video_subtitler.py lecture.mp4 --preprocess
```

Preprocess with only noise reduction (skip normalization and compression):
```bash
python video_subtitler.py podcast.mp4 --preprocess --no-normalize --no-compress
```

Combine preprocessing with higher sensitivity for very quiet audio:
```bash
python video_subtitler.py quiet_video.mp4 --preprocess --sensitivity 0.2 -m medium
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

## Audio Preprocessing

The `--preprocess` flag enables audio enhancement before transcription, which can significantly improve subtitle quality for videos with:
- Quiet or soft-spoken audio
- Uneven volume levels
- Background noise or hiss
- Poor recording quality

### How It Works

1. **Noise Reduction**: Uses spectral gating to remove background noise and hiss
2. **Audio Normalization**: Applies EBU R128 loudness normalization to standardize volume levels
3. **Dynamic Range Compression**: Boosts quiet sections and compresses loud sections for more consistent audio

### When to Use Preprocessing

**Recommended for:**
- Lectures and presentations
- Podcasts with varying speaker volumes
- Home recordings or amateur videos
- Videos with background noise
- Quiet or soft-spoken content

**Not necessary for:**
- Professional studio recordings
- Videos with already high-quality audio
- Content that already has good, consistent volume

### Tips

- Combine `--preprocess` with `--sensitivity 0.2` for best results with very quiet audio
- Use `--keep-audio` to save both original and preprocessed audio files for comparison
- Preprocessing adds 10-30 seconds to processing time depending on video length
- You can disable individual preprocessing steps with `--no-normalize`, `--no-compress`, or `--no-denoise`

## Troubleshooting

**Error: ffmpeg not found**
- Install FFmpeg using the instructions in Prerequisites

**Out of memory error**
- Use a smaller model size (e.g., `-m tiny` or `-m base`)

**Poor transcription quality**
- Try a larger model (e.g., `-m medium` or `-m large`)
- Specify the correct language with `-l` option
- **For quiet or uneven audio**: Use `--preprocess` flag
- **For very quiet audio**: Combine `--preprocess --sensitivity 0.2`

**Missing subtitles for parts of the video**
- Use `--preprocess` to normalize audio levels
- Try `--sensitivity 0.2` for softer voices
- Use a larger model with `-m medium` or `-m large`

## License

MIT License - feel free to use and modify as needed.
