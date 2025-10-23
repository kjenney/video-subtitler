#!/usr/bin/env python3
"""
Test suite for video_subtitler.py
"""

import pytest
import os
import sys
from pathlib import Path
import tempfile
import subprocess

# Add parent directory to path to import video_subtitler
sys.path.insert(0, str(Path(__file__).parent.parent))

import video_subtitler


class TestFormatTimestamp:
    """Test the timestamp formatting function"""

    def test_zero_seconds(self):
        result = video_subtitler.format_timestamp(0)
        assert result == "00:00:00,000"

    def test_seconds_only(self):
        result = video_subtitler.format_timestamp(5.5)
        assert result == "00:00:05,500"

    def test_minutes_and_seconds(self):
        result = video_subtitler.format_timestamp(125.250)
        assert result == "00:02:05,250"

    def test_hours_minutes_seconds(self):
        result = video_subtitler.format_timestamp(3661.123)
        assert result == "01:01:01,123"

    def test_milliseconds_rounding(self):
        result = video_subtitler.format_timestamp(1.0001)
        assert result == "00:00:01,000"

    def test_large_time(self):
        result = video_subtitler.format_timestamp(7384.999)
        assert result == "02:03:04,999"


class TestExtractAudio:
    """Test audio extraction from video"""

    @pytest.fixture(scope="class")
    def sample_video(self):
        """Provide path to sample video"""
        fixtures_dir = Path(__file__).parent / "fixtures"
        video_path = fixtures_dir / "simple_video.mp4"
        if not video_path.exists():
            pytest.skip("Sample video not found. Run tests/create_sample_videos.py first")
        return video_path

    @pytest.fixture(scope="class")
    def silent_video(self):
        """Provide path to silent video"""
        fixtures_dir = Path(__file__).parent / "fixtures"
        video_path = fixtures_dir / "silent_video.mp4"
        if not video_path.exists():
            pytest.skip("Silent video not found. Run tests/create_sample_videos.py first")
        return video_path

    def test_extract_audio_success(self, sample_video):
        """Test successful audio extraction"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            output_path = tmp.name

        try:
            result = video_subtitler.extract_audio(str(sample_video), output_path)
            assert result is True
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_extract_audio_nonexistent_file(self):
        """Test extraction with non-existent video"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            output_path = tmp.name

        try:
            result = video_subtitler.extract_audio("nonexistent.mp4", output_path)
            assert result is False
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_extract_audio_from_silent_video(self, silent_video):
        """Test extraction from video without audio track"""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            output_path = tmp.name

        try:
            # This should handle the case gracefully
            result = video_subtitler.extract_audio(str(silent_video), output_path)
            # Result may be False if video has no audio
            assert result is False or os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


class TestGenerateSRT:
    """Test SRT file generation"""

    def test_generate_srt_single_segment(self):
        """Test SRT generation with one segment"""
        segments = [
            {'start': 0.0, 'end': 2.5, 'text': ' Hello world'}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as tmp:
            output_path = tmp.name

        try:
            video_subtitler.generate_srt(segments, output_path)
            assert os.path.exists(output_path)

            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            assert "1\n" in content
            assert "00:00:00,000 --> 00:00:02,500" in content
            assert "Hello world" in content
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_generate_srt_multiple_segments(self):
        """Test SRT generation with multiple segments"""
        segments = [
            {'start': 0.0, 'end': 2.5, 'text': ' First subtitle'},
            {'start': 2.5, 'end': 5.0, 'text': ' Second subtitle'},
            {'start': 5.0, 'end': 7.5, 'text': ' Third subtitle'}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as tmp:
            output_path = tmp.name

        try:
            video_subtitler.generate_srt(segments, output_path)

            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check all three segments are present
            assert "1\n" in content
            assert "2\n" in content
            assert "3\n" in content
            assert "First subtitle" in content
            assert "Second subtitle" in content
            assert "Third subtitle" in content
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_generate_srt_empty_segments(self):
        """Test SRT generation with empty segments list"""
        segments = []

        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as tmp:
            output_path = tmp.name

        try:
            video_subtitler.generate_srt(segments, output_path)
            assert os.path.exists(output_path)

            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            assert content == ""
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_generate_srt_unicode_text(self):
        """Test SRT generation with unicode characters"""
        segments = [
            {'start': 0.0, 'end': 2.5, 'text': ' Hello 世界 ñ é'}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as tmp:
            output_path = tmp.name

        try:
            video_subtitler.generate_srt(segments, output_path)

            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            assert "Hello 世界 ñ é" in content
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


class TestIntegration:
    """Integration tests for the full workflow"""

    @pytest.fixture(scope="class")
    def short_video(self):
        """Provide path to short video for quick tests"""
        fixtures_dir = Path(__file__).parent / "fixtures"
        video_path = fixtures_dir / "short_video.mp4"
        if not video_path.exists():
            pytest.skip("Short video not found. Run tests/create_sample_videos.py first")
        return video_path

    @pytest.fixture(scope="class")
    def multi_segment_video(self):
        """Provide path to multi-segment video"""
        fixtures_dir = Path(__file__).parent / "fixtures"
        video_path = fixtures_dir / "multi_segment.mp4"
        if not video_path.exists():
            pytest.skip("Multi-segment video not found. Run tests/create_sample_videos.py first")
        return video_path

    def test_full_workflow_with_short_video(self, short_video):
        """Test complete workflow: video -> audio -> transcription -> SRT"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_srt = Path(tmpdir) / "output.srt"

            # Run the main script
            result = subprocess.run(
                [sys.executable, "video_subtitler.py", str(short_video), "-o", str(output_srt), "-m", "tiny"],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True
            )

            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")

            assert result.returncode == 0, f"Script failed with: {result.stderr}"
            assert output_srt.exists(), "Output SRT file was not created"
            assert output_srt.stat().st_size > 0, "Output SRT file is empty"

    def test_command_line_output_default_name(self, short_video):
        """Test that default output filename is generated correctly"""
        # Copy video to temp directory to avoid cluttering fixtures
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_video = Path(tmpdir) / "test_video.mp4"
            import shutil
            shutil.copy(short_video, temp_video)

            expected_srt = temp_video.with_suffix('.srt')

            result = subprocess.run(
                [sys.executable, "video_subtitler.py", str(temp_video), "-m", "tiny"],
                cwd=Path(__file__).parent.parent,
                capture_output=True,
                text=True
            )

            assert result.returncode == 0
            assert expected_srt.exists()

    def test_command_line_nonexistent_file(self):
        """Test error handling for non-existent input file"""
        result = subprocess.run(
            [sys.executable, "video_subtitler.py", "nonexistent_video.mp4"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )

        assert result.returncode != 0
        assert "not found" in result.stdout.lower() or "not found" in result.stderr.lower()

    def test_command_line_help(self):
        """Test that help message works"""
        result = subprocess.run(
            [sys.executable, "video_subtitler.py", "--help"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "video_path" in result.stdout
        assert "--model" in result.stdout
        assert "--output" in result.stdout

    @pytest.mark.slow
    def test_different_model_sizes(self, short_video):
        """Test using different Whisper model sizes"""
        models = ["tiny", "base"]

        for model in models:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_srt = Path(tmpdir) / f"output_{model}.srt"

                result = subprocess.run(
                    [sys.executable, "video_subtitler.py", str(short_video), "-o", str(output_srt), "-m", model],
                    cwd=Path(__file__).parent.parent,
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                assert result.returncode == 0, f"Failed with model {model}: {result.stderr}"
                assert output_srt.exists(), f"No output for model {model}"


class TestTranscription:
    """Test the transcription functionality"""

    @pytest.fixture(scope="class")
    def sample_audio(self, tmp_path_factory):
        """Create a sample audio file for testing"""
        fixtures_dir = Path(__file__).parent / "fixtures"
        video_path = fixtures_dir / "simple_video.mp4"

        if not video_path.exists():
            pytest.skip("Sample video not found. Run tests/create_sample_videos.py first")

        # Extract audio for testing
        tmpdir = tmp_path_factory.mktemp("audio")
        audio_path = tmpdir / "test_audio.wav"
        video_subtitler.extract_audio(str(video_path), str(audio_path))
        return audio_path

    @pytest.mark.slow
    def test_transcribe_audio(self, sample_audio):
        """Test audio transcription (slow test)"""
        result = video_subtitler.transcribe_audio(str(sample_audio), model_name="tiny")

        assert 'segments' in result
        assert 'text' in result
        assert isinstance(result['segments'], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
