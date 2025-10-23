#!/usr/bin/env python3
"""
Create small sample video files with spoken English for testing
Uses gTTS (Google Text-to-Speech) to generate realistic spoken audio
"""

import numpy as np
from moviepy import (
    VideoClip, AudioFileClip, concatenate_videoclips,
    TextClip, CompositeVideoClip
)
import os
from pathlib import Path
import tempfile

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False
    print("Warning: gTTS not installed. Install with: pip install gtts")


def make_frame(t, color, width=320, height=240):
    """Create a single color frame"""
    return np.full((height, width, 3), color, dtype=np.uint8)


def create_tts_audio(text, output_path, lang='en'):
    """Create audio file from text using Google TTS"""
    if not HAS_GTTS:
        raise ImportError("gTTS is required. Install with: pip install gtts")

    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)


def create_video_with_speech(output_path, text, color=[100, 150, 200], fps=24):
    """Create a video with spoken text"""
    print(f"Creating video with speech: '{text}'")

    # Create TTS audio in a temporary file
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_audio:
        temp_audio_path = tmp_audio.name

    try:
        # Generate speech
        create_tts_audio(text, temp_audio_path)

        # Load the audio to get duration
        audio_clip = AudioFileClip(temp_audio_path)
        duration = audio_clip.duration

        # Create video clip with colored background
        def frame_function(t):
            return make_frame(t, color)

        video = VideoClip(frame_function, duration=duration)
        video.fps = fps

        # Add audio to video
        video = video.with_audio(audio_clip)

        # Write video file
        video.write_videofile(str(output_path), codec='libx264', audio_codec='aac')
        video.close()
        audio_clip.close()

        print(f"Created: {output_path} (duration: {duration:.1f}s)")

    finally:
        # Cleanup temporary audio file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


def create_video_with_multiple_sentences(output_path, sentences, fps=24):
    """Create a video with multiple spoken sentences (different segments)"""
    print(f"Creating multi-segment video with {len(sentences)} segments")

    clips = []
    colors = [
        [255, 150, 150],  # Light red
        [150, 255, 150],  # Light green
        [150, 150, 255],  # Light blue
        [255, 255, 150],  # Light yellow
        [255, 150, 255],  # Light magenta
    ]

    temp_files = []

    try:
        for i, text in enumerate(sentences):
            color = colors[i % len(colors)]

            # Create TTS audio
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_audio:
                temp_audio_path = tmp_audio.name
                temp_files.append(temp_audio_path)

            create_tts_audio(text, temp_audio_path)

            # Load audio
            audio_clip = AudioFileClip(temp_audio_path)
            duration = audio_clip.duration

            # Create video segment
            def frame_function(t, c=color):
                return make_frame(t, c)

            video_segment = VideoClip(frame_function, duration=duration)
            video_segment.fps = fps
            video_segment = video_segment.with_audio(audio_clip)

            clips.append(video_segment)

        # Concatenate all segments
        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(str(output_path), codec='libx264', audio_codec='aac')

        # Close all clips
        final_video.close()
        for clip in clips:
            clip.close()

        print(f"Created: {output_path}")

    finally:
        # Cleanup temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def create_silent_video(output_path, duration=2, fps=24):
    """Create a video without audio"""
    print(f"Creating silent video")

    def frame_function(t):
        return make_frame(t, [100, 100, 100])

    video = VideoClip(frame_function, duration=duration)
    video.fps = fps

    video.write_videofile(str(output_path), codec='libx264')
    video.close()
    print(f"Created: {output_path}")


def main():
    """Create all sample videos with spoken English"""
    if not HAS_GTTS:
        print("ERROR: gTTS library is required to generate test videos.")
        print("Please install it with: pip install gtts")
        return 1

    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    print("Creating sample videos with spoken English for testing...")
    print("This may take a minute...\n")

    # Video 1: Simple greeting
    create_video_with_speech(
        fixtures_dir / "simple_video.mp4",
        "Hello, this is a simple test video.",
        color=[120, 180, 220]
    )

    # Video 2: Very short phrase (for quick tests)
    create_video_with_speech(
        fixtures_dir / "short_video.mp4",
        "Testing one two three.",
        color=[220, 120, 120]
    )

    # Video 3: Silent video (no audio)
    create_silent_video(
        fixtures_dir / "silent_video.mp4",
        duration=2
    )

    # Video 4: Multiple segments with different sentences
    create_video_with_multiple_sentences(
        fixtures_dir / "multi_segment.mp4",
        [
            "This is the first segment.",
            "Now we are in the second part.",
            "And finally, the third section."
        ]
    )

    # Video 5: Longer phrase for testing accuracy
    create_video_with_speech(
        fixtures_dir / "text_video.mp4",
        "Welcome to the video subtitler test suite. This application can extract audio from videos and generate accurate subtitles.",
        color=[180, 140, 200]
    )

    print("\nAll sample videos created successfully!")
    print(f"Location: {fixtures_dir}")
    return 0


if __name__ == "__main__":
    exit(main())
