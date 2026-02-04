---
name: audio-recorder
description: Expert in managing audio recordings using sox. **Use this skill whenever the user mentions "record", "recording", "start recording", "stop recording", "list records", or asks to capture audio from meetings or conversations.**
---

# Audio Recorder Skill

Expert in managing audio recordings using sox. **Use this skill whenever the user mentions "record", "recording", "start recording", "stop recording", or asks to capture audio from meetings or conversations.**

## Core Concepts

### Recording Storage

All recordings are stored in: `~/Downloads/Records/`

**Filename Format**: `YYYY-mm-dd_HH:MM:SS_<label>.ogg`

### PID Tracking

The recording script maintains a PID file at `~/Downloads/Records/.pid` to track active recordings.

**Important**: Only ONE recording can be active at a time.

### Recording Format

- **Audio Format**: OGG (Vorbis)
- **Tool**: sox
- **Quality**: Default sox settings (optimized for voice)
- **Input Device**: System default microphone

---

## Core Operations

### 1. Start Recording

**Triggers**:
- "start recording"
- "start record"
- "begin recording"
- "record this"
- "start recording [label]"
- "record one2one with [name]"
- "record [meeting name]"

**Script Command**:
```bash
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh start [label]
```

**Examples**:
- `record.sh start` → Creates file with "Unknown" label
- `record.sh start one2one_Marcelo` → Creates file with "one2one_Marcelo" label
- `record.sh start "Steering Committee"` → Creates file with "Steering_Committee" label

### 2. Stop Recording

**Triggers**:
- "stop recording"
- "stop record"
- "end recording"
- "finish recording"
- "done recording"

**Script Command**:
```bash
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh stop
```

### 3. Rename Recording Label

**Triggers**:
- "rename recording"
- "rename the recording"
- "rename recording to [label]"
- "rename the label to [label]"
- "change recording label"
- "rename it to [label]"

**Script Command**:
```bash
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh rename <new_label>
```

**Examples**:
- `record.sh rename Team_Meeting` → Renames to `YYYY-mm-dd_HH:MM:SS_Team_Meeting.ogg`
- `record.sh rename "one2one Sarah"` → Renames to `YYYY-mm-dd_HH:MM:SS_one2one_Sarah.ogg`

### 4. Check Recording Status

**Triggers**:
- "recording status"
- "check recording"
- "is recording active"
- "am I recording"
- "is there a recording in progress"
- "what am I recording"
- "how long have I been recording"

**Script Command**:
```bash
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh status
```

**Output**:
```
✓ Recording in progress (PID: 12345)

Label: one2one Marcelo
Started: 2025-11-11 at 14:30:45
Duration: 15m 32s

Full path: /Users/sebastien.morand/Downloads/Records/2025-11-11_14:30:45_one2one_Marcelo.ogg
Current size: 2.3M
```

### 5. List Recordings

**Triggers**:
- "list recordings"
- "list records"
- "show recordings"
- "show records"
- "what recordings do I have"
- "show all recordings"

**Commands**:
```bash
# Check for active recording
/Users/sebastien.morand/.claude/skills/audio-recorder/scripts/record.sh status

# List all recordings, don't add any other parameters or pipe
ls -lh ~/Downloads/Records/*.ogg
```

**Output Format**:

Display recordings in a clean table with these columns:
- **Filename**: The complete filename (YYYY-MM-DD_HH:MM:SS_label.ogg)
- **Size**: File size in human-readable format (KB, MB)
- **Date**: Recording date (YYYY-MM-DD)
- **Time**: Recording time (HH:MM)
- **Label**: Extracted from filename with underscores converted to spaces
- **Status**: "In Progress" or empty

Example:
```
| Filename                                  | Size  | Date       | Time  | Label              | Status      |
|-------------------------------------------|-------|------------|-------|--------------------| ------------|
| 2025-11-11_15:38:48_one2one_Marcelo.ogg   | 850K  | 2025-11-11 | 15:38 | one2one Marcelo    | In Progress |
| 2025-11-11_15:25:21_Production_Test.ogg   | 1.9M  | 2025-11-11 | 15:25 | Production Test    |             |
| 2025-11-11_15:15:33_Unknown.ogg           | 243K  | 2025-11-11 | 15:15 | Unknown            |             |
| 2025-11-11_15:05:12_test.ogg              | 975K  | 2025-11-11 | 15:05 | test               |             |

Total: 4 recordings
```

**Notes**:
- **IMPORTANT**: Always check for active recordings first to mark the status
- Never try to filter recodings 
- All recordings are stored in `~/Downloads/Records/`
- Files are named: `YYYY-mm-dd_HH:MM:SS_<label>.ogg`
- Most recent files appear first (sorted by modification time)
- Labels are extracted from filename and displayed with underscores converted to spaces
- Use markdown table format for clean, readable output
- Include total count at the bottom

### 6. Play Recording

**Triggers**:
- "play recording"
- "play [label]"
- "play the recording"
- "listen to recording"
- "play test4"
- "play one2one Jean"

**Process**:
1. If label is provided, find the recording file matching that label
2. Search for files in `~/Downloads/Records/` with the label in the filename
3. If multiple matches, use the most recent one
4. Play the recording using mplayer with quiet mode (no console output)
5. Confirm playback started and wait for completion

**Command**:
```bash
mplayer -really-quiet ~/Downloads/Records/*_<label>.ogg
```

**Examples**:
- `mplayer -really-quiet ~/Downloads/Records/*_test4.ogg` → Plays test4 recording
- `mplayer -really-quiet ~/Downloads/Records/*_one2one_Jean.ogg` → Plays one2one Jean recording
- `mplayer -really-quiet ~/Downloads/Records/2025-11-11_15:30:22_SteeringCommittee.ogg` → Plays specific file

**Behavior**:
- If multiple files match the label pattern, the shell glob will use the first match
- To play the most recent file with a label, sort by time and pick the latest
- Playback is synchronous - waits for file to finish playing
- Press `q` to quit playback early (if running interactively)

**Finding recordings by label**:
```bash
# Find most recent file matching label
ls -t ~/Downloads/Records/*_<label>.ogg 2>/dev/null | head -1

# Play most recent matching file
mplayer -really-quiet "$(ls -t ~/Downloads/Records/*_<label>.ogg 2>/dev/null | head -1)"
```

**Notes**:
- **IMPORTANT**: Use `-really-quiet` to suppress mplayer's verbose console output
- All recordings are OGG format, compatible with mplayer
- If label contains spaces, it will be stored with underscores in filename
- If file not found, mplayer will error: "File not found"

**Requirements**:
- **mplayer**: Must be installed (`brew install mplayer` on macOS)
- Alternative: Can use `afplay` on macOS (built-in), but mplayer provides better control
