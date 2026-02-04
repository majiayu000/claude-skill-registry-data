---
name: chat-integrator
description: Automatically integrates processed media (audio transcriptions and image summaries) into chat.md files at the correct timestamp position. Use this when you want to merge processed .json audio files and .md image summaries into the daily chat.md conversation log.
---

# Chat Integrator

## Overview

Automatski integriše procesirane medije (audio transkripcije i image summaries) u chat.md fajlove na pravom mjestu po timestamp-u.

**Što radi:**
- Nalazi sve `.json` audio transkripcije u folderu
- Nalazi sve `.md` image summaries u folderu
- Ekstraktuje timestamp iz imena fajla
- Ubacuje sadržaj u `chat.md` na hronološki pravom mjestu
- Održava postojeći sadržaj chat.md-a

**Output:**
- Ažuriran `chat.md` sa uključenim audio i slikama na pravim mjestima

## When to Use This Skill

User says:
- "Integrate media into chat"
- "Merge audio/images into chat.md"
- "Update chat.md with processed media"
- "Add transcriptions to chat"

## Workflow

### Simple Usage

**Integrate media for specific folder:**
```bash
python .claude/skills/chat-integrator/scripts/integrate_media.py "gastrohem whatsapp/administracija/20.10 - 27.10/24.10"
```

**Integrate media for specific date (scans all departments):**
```bash
python .claude/skills/chat-integrator/scripts/integrate_media.py --scan-date 24.10
```

**Integrate media for today:**
```bash
python .claude/skills/chat-integrator/scripts/integrate_media.py
```

### What Happens

1. **Scan folder** for processed media:
   - Audio: `*.mp3.json`, `*.ogg.json`, etc.
   - Images: `*.png.md`, `*.jpg.md`, etc.

2. **Extract timestamp** from filename:
   - `WhatsApp Audio 2025-10-24 at 16.36.50.mp3` → `[24. 10. 2025., 16:36:50]`
   - `image.png` → Uses file modification time

3. **Read content**:
   - Audio `.json`: Extract `text` field
   - Image `.md`: Extract summary content

4. **Parse chat.md**:
   - Read existing entries with timestamps
   - Identify insertion points

5. **Merge and sort**:
   - Combine existing + new entries
   - Sort by timestamp chronologically
   - Write back to `chat.md`

## Timestamp Format

**WhatsApp filename formats (supported):**
```
Format 1: WhatsApp [Audio/Image/Video] YYYY-MM-DD at HH.MM.SS
  - WhatsApp Audio 2025-10-24 at 16.36.50.mp3
  - WhatsApp Image 2025-10-24 at 22.42.33.png
  - WhatsApp Video 2025-10-24 at 14.30.45.mp4

Format 2: [AUDIO/PHOTO/IMAGE/VIDEO/PTT]-YYYY-MM-DD-HH-MM-SS
  - AUDIO-2025-10-26-15-00-32.mp3
  - PHOTO-2025-10-24-22-42-33.jpg
  - IMAGE-2025-10-26-09-15-23.png
  - VIDEO-2025-10-24-14-30-45.mp4
  - PTT-2025-10-24-18-20-10.ogg
```

**Extraction priority:**
1. WhatsApp format (Format 1 or 2) - extracts full date & time
2. Fallback to file modification time

**chat.md format:**
```
[24. 10. 2025., 16:36:50] Sender: message
```

## Entry Format in chat.md

**Audio entry:**
```markdown
[24. 10. 2025., 16:36:50] [AUDIO] Adis Kadric: Full transcribed text here...
```

**Image entry:**
```markdown
[24. 10. 2025., 09:15:23] [IMAGE] Mahir Kadic:

Summary of image content...
Key information extracted from image...
```

## Script Reference

### integrate_media.py

**Purpose:** Main script for integrating processed media into chat.md

**Arguments:**
- `folder` (optional) - Path to specific folder
- `--scan-date DD.MM` - Scan all departments for this date
- `--dry-run` - Preview changes without writing
- `--backup` - Create backup before modifying (default: true)

**What it does:**
1. Finds all `.json` and `.md` files (skips chat.md, summary.md)
2. Extracts timestamps from filenames
3. Reads content from each file
4. Parses existing chat.md
5. Merges entries chronologically
6. Writes updated chat.md

## Best Practices

1. **Always run after media processing** - First run `gastrohem-media-processor`, then `chat-integrator`
2. **Use --dry-run first** - Preview changes before committing
3. **Automatic backups** - Script creates `chat.md.backup` before modifying
4. **Run daily** - Integrate media daily to keep chat.md up-to-date
5. **Check results** - Review integrated content for accuracy

## Error Handling

**If timestamp extraction fails:**
- Falls back to file modification time
- Logs warning with filename

**If chat.md doesn't exist:**
- Creates new chat.md with integrated media

**If entry already exists:**
- Skips duplicate entries (checks by timestamp + content hash)

## Example Workflow

**User:** "Integrate media"

**Claude:**
1. Runs: `python .claude/skills/chat-integrator/scripts/integrate_media.py`
2. Scans today's folders across all departments
3. Finds 2 audio .json files and 1 image .md file
4. Extracts timestamps and content
5. Merges into existing chat.md chronologically
6. Reports: "Integrated 3 media entries into chat.md across 2 folders."
