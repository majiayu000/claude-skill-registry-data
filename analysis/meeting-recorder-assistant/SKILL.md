---
name: meeting-recorder-assistant
description: Intelligent meeting recording and transcription assistant with automated minutes generation, action item extraction, and sentiment analysis. Supports audio transcription, speaker diarization, meeting summarization, and task extraction. Use when users need to record meetings, transcribe audio, generate meeting minutes, extract action items, or analyze meeting content.
---

# Meeting Recorder Assistant

An intelligent meeting assistant that records, transcribes, and analyzes meetings to generate actionable insights.

## Features

- **Audio Recording**: Record meeting audio with timestamps
- **Speech-to-Text**: Transcribe audio to text with speaker identification
- **Meeting Minutes**: Auto-generate structured meeting summaries
- **Action Items**: Extract tasks and assignments from discussions
- **Sentiment Analysis**: Analyze meeting tone and engagement

## Usage

### Record and Transcribe

```python
from scripts.meeting_recorder import MeetingRecorder

# Initialize recorder
recorder = MeetingRecorder()

# Start recording
recorder.start_recording("/tmp/meeting_audio.wav")

# Stop and transcribe
transcript = recorder.stop_and_transcribe()
print(f"Transcript: {transcript['text']}")
```

### Generate Meeting Minutes

```python
from scripts.meeting_minutes import generate_minutes

# Generate structured minutes
minutes = generate_minutes(transcript_path="/tmp/transcript.json")
print(f"Summary: {minutes['summary']}")
print(f"Action Items: {minutes['action_items']}")
```

### Extract Action Items

```python
from scripts.action_extractor import extract_actions

# Extract tasks from transcript
actions = extract_actions("/tmp/transcript.txt")
for action in actions:
    print(f"- {action['task']} (Assigned: {action['assignee']})")
```

## Supported Audio Formats

- WAV
- MP3
- M4A
- OGG

## Output Formats

- JSON (structured data)
- Markdown (meeting minutes)
- TXT (transcript)
