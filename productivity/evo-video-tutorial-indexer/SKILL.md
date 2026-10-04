---
name: evo-video-tutorial-indexer
description: A comprehensive skill for extracting chapter indices from tutorial videos using FFmpeg audio extraction, OpenAI Whisper ASR transcription with word-level timestamps, and semantic chapter alignment via fuzzy string matching.
---

# evo-video-tutorial-indexer

A comprehensive skill for extracting chapter indices from tutorial videos using
FFmpeg audio extraction, OpenAI Whisper ASR transcription with word-level timestamps,
and semantic chapter alignment via fuzzy string matching.

## Workflow

1. **Extract** audio from MP4 using FFmpeg (16kHz mono PCM WAV for optimal Whisper input)
2. **Transcribe** the audio using OpenAI Whisper with word-level timestamps enabled
3. **Analyze** transcript words using sliding window fuzzy matching to locate chapter boundaries
4. **Align** chapter titles to timestamps using multiple matching strategies and keyword heuristics
5. **Validate** structural requirements (monotonic timestamps, correct count, within duration)
6. **Output** JSON with video_info and chapters array

## Key Alignment Principles

- First chapter always starts at time 0
- Look for explicit verbal cues ("now let's...", "alright first...", "okay so...")
- Chapter timestamp = where speaker FIRST begins sustained discussion of that topic
- Short chapters (Save, Break, Great job!) may be just a few seconds
- Break/Continue pattern: break is a brief interruption, continue resumes same topic
- Timestamps must be strictly monotonically increasing
- All timestamps within [0, duration]
- Word-level timestamps via Whisper's cross-attention DTW provide much better precision than segment-level timestamps

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-video-tutorial-indexer/scripts')
from transcribe import extract_audio, transcribe_video
from chapter_detect import detect_chapters, enforce_monotonic
from utils import create_chapter, create_video_index, validate_chapters, write_index

# Step 1: Extract and transcribe
audio_path = extract_audio("/root/tutorial_video.mp4", "/tmp/tutorial_audio.wav")
transcript = transcribe_video(audio_path, model_size="base")

# Step 2: Detect chapters
chapter_titles = ["What we'll do", "How we'll get there", ...]
chapters = detect_chapters(chapter_titles, transcript, duration=1382)

# Step 3: Enforce constraints and validate
chapters = enforce_monotonic(chapters, duration=1382)
errors = validate_chapters(chapters, duration=1382)

# Step 4: Write output
index = create_video_index("In-Depth Floor Plan Tutorial Part 1", 1382, chapters)
write_index(index, '/root/tutorial_index.json')
```

## Scripts

- `scripts/utils.py` - Core utility functions for chapter creation, validation, and JSON output
- `scripts/transcribe.py` - FFmpeg audio extraction and Whisper transcription with optimal parameters
- `scripts/chapter_detect.py` - Sliding window fuzzy matching, keyword-based detection, and monotonic enforcement