#!/usr/bin/env python3
"""
Video Subtitler - Extract audio from video and generate subtitles
"""

import argparse
import os
import sys
from pathlib import Path
import tempfile
from datetime import timedelta

try:
    import whisper
    from moviepy import VideoFileClip
except ImportError as e:
    print(f"Error: Required package not found: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)


def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60
    millis = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def extract_audio(video_path, output_audio_path):
    """Extract audio from video file"""
    print(f"Extracting audio from {video_path}...")
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_audio_path)
        video.close()
        print(f"Audio extracted to {output_audio_path}")
        return True
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False


def transcribe_audio(audio_path, model_name="base", language=None):
    """Transcribe audio using Whisper"""
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"Transcribing audio...")
    result = model.transcribe(
        audio_path,
        language=language,
        verbose=False,
        word_timestamps=True
    )

    return result


def generate_srt(segments, output_path):
    """Generate SRT subtitle file from transcription segments"""
    print(f"Generating subtitle file: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, start=1):
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text'].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

    print(f"Subtitle file created successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Extract audio from video and generate subtitles using Whisper AI"
    )
    parser.add_argument(
        "video_path",
        type=str,
        help="Path to the video file"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output subtitle file path (default: same name as video with .srt extension)"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base). Larger models are more accurate but slower"
    )
    parser.add_argument(
        "-l", "--language",
        type=str,
        help="Language code (e.g., 'en', 'es', 'fr'). Auto-detect if not specified"
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep the extracted audio file"
    )

    args = parser.parse_args()

    # Validate input file
    video_path = Path(args.video_path)
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = video_path.with_suffix('.srt')

    # Create temporary audio file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
        temp_audio_path = tmp_audio.name

    try:
        # Step 1: Extract audio
        if not extract_audio(str(video_path), temp_audio_path):
            sys.exit(1)

        # Step 2: Transcribe audio
        result = transcribe_audio(temp_audio_path, args.model, args.language)

        # Step 3: Generate SRT file
        generate_srt(result['segments'], str(output_path))

        print(f"\nSuccess! Subtitles saved to: {output_path}")

        if args.language is None and 'language' in result:
            print(f"Detected language: {result['language']}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # Cleanup temporary audio file
        if not args.keep_audio and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print("Temporary audio file removed")
        elif args.keep_audio:
            audio_output = video_path.with_suffix('.wav')
            os.rename(temp_audio_path, audio_output)
            print(f"Audio file saved to: {audio_output}")


if __name__ == "__main__":
    main()
