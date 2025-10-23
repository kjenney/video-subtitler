# Testing Guide

This document provides detailed information about testing the Video Subtitler application.

## Test Suite Overview

The test suite is built with pytest and includes:

- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test the complete workflow
- **Sample Video Generation**: Create small test videos automatically

## Quick Start

### Option 1: Using the test runner script (Recommended)

```bash
./run_tests.sh
```

This script will:
1. Check for Python and FFmpeg
2. Install dependencies if needed
3. Generate sample videos if they don't exist
4. Run the full test suite

### Option 2: Manual setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Create sample videos
python3 tests/create_sample_videos.py

# Run tests
pytest
```

## Test Categories

### Unit Tests

These test individual functions without external dependencies:

```bash
# Run only unit tests
pytest tests/test_video_subtitler.py::TestFormatTimestamp -v
pytest tests/test_video_subtitler.py::TestGenerateSRT -v
```

**Tested functions:**
- `format_timestamp()` - SRT timestamp formatting
- `generate_srt()` - SRT file generation
- Edge cases and error handling

### Integration Tests

These test the complete workflow with actual video files:

```bash
# Run integration tests
pytest tests/test_video_subtitler.py::TestIntegration -v
```

**Tested scenarios:**
- Audio extraction from video
- Complete video-to-subtitle workflow
- Command-line interface
- Different model sizes
- Error handling

### Slow Tests

Some tests involve AI transcription and take longer to run:

```bash
# Run all tests including slow ones
pytest

# Skip slow tests for quick validation
pytest -m "not slow"
```

## Sample Videos

The test suite uses small generated videos:

| Video File | Duration | Description |
|------------|----------|-------------|
| `simple_video.mp4` | 3s | Simple video with audio |
| `short_video.mp4` | 1s | Very short video for quick tests |
| `silent_video.mp4` | 2s | Video without audio track |
| `multi_segment.mp4` | 6s | Video with multiple segments |
| `text_video.mp4` | 3s | Video with text overlay |

### Regenerating Sample Videos

```bash
# Delete existing videos
rm -f tests/fixtures/*.mp4

# Generate new ones
python3 tests/create_sample_videos.py
```

## Running Specific Tests

### Run a specific test class
```bash
pytest tests/test_video_subtitler.py::TestFormatTimestamp -v
```

### Run a specific test
```bash
pytest tests/test_video_subtitler.py::TestFormatTimestamp::test_zero_seconds -v
```

### Run with verbose output
```bash
pytest -vv
```

### Run with output capture disabled (see print statements)
```bash
pytest -s
```

## Coverage Reports

Generate code coverage reports:

```bash
# Terminal report
pytest --cov=video_subtitler

# HTML report (opens in browser)
pytest --cov=video_subtitler --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Markers

Tests are categorized with markers:

- `@pytest.mark.slow` - Tests that take longer to run (AI transcription)
- `@pytest.mark.integration` - Integration tests (future use)
- `@pytest.mark.unit` - Unit tests (future use)

Use markers to run specific categories:

```bash
# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"
```

## Continuous Integration

For CI/CD pipelines, use these commands:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Generate test videos
python3 tests/create_sample_videos.py

# Run fast tests only (skip transcription)
pytest -m "not slow" --cov=video_subtitler --cov-report=xml

# Or run all tests with timeout
pytest --timeout=300
```

## Troubleshooting Tests

### FFmpeg not found
```
Error: FFmpeg is not installed
```
Install FFmpeg before running tests (see main README).

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'pytest'
```
Install test dependencies: `pip3 install -r requirements.txt`

### Sample videos not found
```
SKIPPED [1] Sample video not found
```
Generate sample videos: `python3 tests/create_sample_videos.py`

### Whisper model download
On first run, Whisper will download model files (~100MB for tiny model).
This happens automatically but requires internet connection.

### Test timeout
For slow machines, increase timeout:
```bash
pytest --timeout=600  # 10 minutes
```

## Writing New Tests

### Test Structure

```python
def test_something():
    """Test description"""
    # Arrange
    input_data = "test"

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_output
```

### Using Fixtures

```python
@pytest.fixture
def sample_data():
    """Provide test data"""
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

### Temporary Files

```python
import tempfile

def test_file_creation():
    with tempfile.NamedTemporaryFile(suffix='.srt') as tmp:
        # Test code here
        pass
    # File automatically cleaned up
```

## Test Checklist

Before submitting changes:

- [ ] All tests pass: `pytest`
- [ ] No new warnings: `pytest -v`
- [ ] Coverage maintained: `pytest --cov=video_subtitler`
- [ ] Fast tests pass: `pytest -m "not slow"`
- [ ] Code follows style guidelines
- [ ] New features have tests
- [ ] Documentation updated

## Performance Benchmarks

Typical test run times (on modern hardware):

- Unit tests: < 1 second
- Integration tests (without transcription): 5-10 seconds
- Full suite with transcription: 30-60 seconds
- Sample video generation: 10-20 seconds

## Additional Resources

- [Pytest documentation](https://docs.pytest.org/)
- [Pytest fixtures](https://docs.pytest.org/en/latest/fixture.html)
- [Testing best practices](https://docs.pytest.org/en/latest/goodpractices.html)
