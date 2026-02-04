---
name: media-workflow
description: Complete end-to-end WhatsApp media processing workflow. Processes audio/images AND integrates them into chat.md in a single step. Use when you want to do the complete daily media processing (transcribe + OCR + integrate into chat).
---

# Media Workflow

## Overview

Automatski izvršava kompletan workflow obrade WhatsApp medija:
1. **Process media** → Transkribuje audio, OCR-uje slike
2. **Integrate** → Ubacuje procesirani sadržaj u chat.md fajlove
3. **Report** → Daje summary šta je obrađeno

**Što radi:**
- Poziva `gastrohem-media-processor` za audio/slike
- Poziva `chat-integrator` za integraciju u chat.md
- Sve u jednom koraku!

**Output:**
- `.json` audio transkripcije
- `.md` image summaries
- Ažuriran `chat.md` sa svim medijima integriranim
- Backup `chat.md.backup` prije izmjena

## When to Use This Skill

User says:
- "Process and integrate media"
- "Do complete media workflow"
- "Process today's WhatsApp media"
- "Process and merge media for 24.10"

**Default behavior:** Uses today's date, processes all departments

## Workflow

### Simple Usage

**Process and integrate for today (DEFAULT):**
```bash
python .claude/skills/media-workflow/scripts/run_workflow.py
```

**Process and integrate for specific date:**
```bash
python .claude/skills/media-workflow/scripts/run_workflow.py --scan-date 24.10
```

**Process and integrate specific folder:**
```bash
python .claude/skills/media-workflow/scripts/run_workflow.py --folder "gastrohem whatsapp/administracija/20.10 - 27.10/24.10"
```

**Dry run (preview changes):**
```bash
python .claude/skills/media-workflow/scripts/run_workflow.py --dry-run
```

### What Happens

**Step 1: Media Processing**
- Finds all folders for target date/folder
- Transcribes audio files in parallel (3 max)
- Creates `.json` audio transcriptions
- Performs OCR on images
- Creates `.md` image summaries

**Step 2: Integration**
- Extracts timestamps from filenames
- Parses existing chat.md entries
- Merges new + existing entries chronologically
- Creates backup: `chat.md.backup`
- Writes updated `chat.md`

**Step 3: Report**
- Summary of processed media
- List of integrated entries
- Any errors or skipped files

## Script Reference

### run_workflow.py

**Purpose:** Master workflow script

**Arguments:**
- `--scan-date DD.MM` - Process all departments for this date
- `--folder PATH` - Process specific folder
- `--base-path PATH` - Base path (default: "gastrohem whatsapp")
- `--dry-run` - Preview changes without writing
- `--no-backup` - Skip backup creation
- `--output-json FILE` - Save workflow results to JSON

**What it does:**
1. Runs `gastrohem-media-processor` script
2. Waits for media processing to complete
3. Runs `chat-integrator` script
4. Aggregates and reports results

## Best Practices

1. **Run daily** - Process media daily to avoid backlog
2. **Use --dry-run first** - Preview changes before committing (especially first time)
3. **Check results** - Review integrated content for accuracy
4. **Backups are automatic** - Backup created before any chat.md modifications

## Error Handling

**If audio transcription fails:**
- Skill continues with remaining files
- Reports failed files in summary

**If image OCR fails:**
- Skill continues with remaining files
- Reports failed files in summary

**If integration fails:**
- Backup remains intact
- Error logged with details

## Example Workflow

**User:** "Process media"

**Claude:**
1. Runs: `python .claude/skills/media-workflow/scripts/run_workflow.py`
2. **Step 1:** Processes media for today (26.10)
   - Finds 3 folders: administracija/26.10, finansije/26.10, adis-chat/26.10
   - Transcribes 2 audio files → `.json`
   - OCRs 3 images → `.md`
3. **Step 2:** Integrates into chat.md
   - Merges 5 entries into 3 chat.md files
   - Creates backups
4. **Step 3:** Reports
   - "Processed 2 audio + 3 images across 3 folders"
   - "Integrated 5 entries into chat.md"
   - "✅ Complete workflow finished successfully"

## Performance

- **Total time:** ~10-15 sec for típical daily folder
  - Media processing: ~5-8 sec (parallel)
  - Integration: ~2-3 sec
  - Overhead: ~1-2 sec

## Output Structure

After running workflow on folder `24.10`:
```
gastrohem whatsapp/administracija/20.10 - 27.10/24.10/
├── chat.md                    # Updated with integrated media
├── chat.md.backup             # Backup before integration
├── image.png
├── image.png.md               # OCR summary
├── WhatsApp Audio *.mp3
└── WhatsApp Audio *.mp3.json  # Audio transcription
```
