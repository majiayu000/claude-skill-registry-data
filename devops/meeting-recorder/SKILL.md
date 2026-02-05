---
name: meeting-recorder
description: Join Google Meet calls, transcribe audio in real-time, and participate via chat. Use when asked to join a meeting, transcribe a call, attend a video conference, or take meeting notes.
---

# Meeting Recorder

Join Google Meet calls as an active participant with real-time transcription.

## Prerequisites

1. Chrome automation skill must be installed and working
2. Run setup once: `~/.claude/skills/meeting-recorder/scripts/meeting-recorder-setup/setup.sh`

## Quick Start

### Join a Meeting
```bash
meeting-recorder join "https://meet.google.com/xxx-yyyy-zzz"
```

### Check Status
```bash
meeting-recorder status
```

### Read Live Transcript
```bash
# Current meeting
tail -f /tmp/meetings/current/transcript.txt

# Specific meeting
cat /tmp/meetings/abc-defg-hij/transcript.txt
```

### Send Chat Message
```bash
meeting-recorder chat "Hello from Claude!"
```

### Leave Meeting
```bash
meeting-recorder leave
```

### List Past Meetings
```bash
ls /tmp/meetings/
```

## Meeting Storage

Each meeting creates a directory at `/tmp/meetings/<meeting-id>/`:
- `transcript.txt` - Full transcript with timestamps
- `metadata.json` - Meeting info (URL, start time, status)
- `mentions.txt` - Detected questions/mentions for Claude

The `/tmp/meetings/current` symlink always points to the active meeting.

## Configuration

Edit `~/.meeting-recorder.json`:
```json
{
    "participant_name": "Claude Assistant",
    "meetings_dir": "/tmp/meetings",
    "mention_keywords": ["claude", "assistant", "ai"],
    "speaches_url": "ws://localhost:8000/v1/realtime",
    "transcription_model": "Systran/faster-distil-whisper-small.en"
}
```

## How It Works

1. Chrome navigates to meeting URL
2. Enters participant name and joins (camera/mic off)
3. PulseAudio captures Chrome's audio output
4. Audio is batched (5-second chunks) and sent to Speaches HTTP API
5. Transcription written to meeting directory
6. Claude can read transcript and respond via chat

## Active Participant Mode

Claude can monitor the transcript for mentions and questions:
- Check `/tmp/meetings/current/mentions.txt` for detected questions
- Respond via `meeting-recorder chat "response"`

For detailed documentation, see [REFERENCE.md](REFERENCE.md).
