---
name: gastrohem-media-processor
description: Automatically process unprocessed audio and image files in Gastrohem daily WhatsApp folders. This skill should be used when the user asks to transcribe audio files, perform OCR on images, or process media in daily folders (e.g., "Process media in today's folder", "Transcribe audio and OCR images in 24.10 folder"). Handles audio transcription using insanely-fast-whisper (parallelized, creates .json) and image OCR using Claude's vision capabilities (creates natural .md summaries with Gastrohem-relevant info).
---

# Gastrohem Media Processor

## Overview

Automatski procesira WhatsApp media fajlove (audio i slike) u Gastrohem dnevnim folderima.

**Što radi:**
- Transkribuje audio fajlove **paralelno** (3x brže) → kreira `.json` fajlove
- Identifikuje slike koje trebaju OCR → kreira `.md` fajlove sa prirodnim sažetkom
- **Default:** Koristi današnji datum automatski
- Skenira **SVE odjele** odjednom za dati datum

**Performance:**
- Audio: Do 3 fajla istovremeno (paralelno)
- Slike: Batch OCR (sve odjednom sa Claude vision)
- Scan: Nalazi sve foldere za datum u <1 sekundi

**Note:** Skill kreira `.json` za audio i `.md` za slike - dodavanje u `chat.md` je odvojen korak.

## When to Use This Skill

User says:
- "Process media"
- "Process today's media"
- "Transcribe audio files"
- "Process media for 24.10"
- "OCR images in today's folders"

**Default behavior:** Uses today's date, scans all departments automatically.

## Workflow

### Simple Usage

**Process all media for today (DEFAULT):**
```bash
python .claude/skills/gastrohem-media-processor/scripts/process_media.py
```
- Uses today's date automatically (26.10 danas)
- Scans ALL departments for folders matching today's date
- Transcribes audio in parallel
- Lists images needing OCR

**Process specific date:**
```bash
python .claude/skills/gastrohem-media-processor/scripts/process_media.py --scan-date 24.10
```

**Process specific folder:**
```bash
python .claude/skills/gastrohem-media-processor/scripts/process_media.py --folder "gastrohem whatsapp/administracija/20.10 - 27.10/24.10"
```

### What Happens

**Audio Processing:**
1. Finds all audio files (`.mp3`, `.ogg`, `.m4a`, `.wav`, `.opus`)
2. Skips files that already have `.json` transcriptions
3. Transcribes in parallel (3 concurrent processes)
4. Creates JSON: `{audio_filename}.json`
   ```json
   {
     "speakers": [],
     "chunks": [...],
     "text": "Full transcribed text here"
   }
   ```

**Image Processing:**
1. Finds all images (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`)
2. Checks which images DON'T have `.md` files
3. Returns list of images needing OCR
4. Claude reads images in parallel and creates natural summaries with Gastrohem-relevant info
5. Creates markdown: `{image_filename}.md`
   ```markdown
   # image.png

   **Poslao:** Mahir Kadic
   **Datum:** 26.10.2025 13:58

   ---

   [Natural language summary focusing on Gastrohem-relevant information:
    contacts, names, emails, phone numbers, business details, etc.]
   ```


## Script Reference

### Three Separate Scripts

The skill now uses three modular scripts for better organization:

#### 1. process_audio.py

**Purpose:** Audio transcription only (parallelized)

**Usage:**
```bash
python scripts/process_audio.py "path/to/folder" [--max-workers 3] [--output-json results.json]
```

**Arguments:**
- `folder` - Path to folder containing audio files
- `--max-workers N` - Max parallel processes (default: 3)
- `--no-skip-existing` - Re-transcribe files with existing JSON
- `--output-json FILE` - Save results to JSON

**What it does:**
- Finds audio files (`.mp3`, `.ogg`, `.m4a`, `.wav`, `.opus`)
- Skips files with existing `.json` transcriptions
- Transcribes in parallel (max 3 concurrent)
- Creates JSON files: `{audio_filename}.json`

**Requirements:** `insanely-fast-whisper` in PATH

---

#### 2. process_images.py

**Purpose:** Image OCR helper functions

**Usage:**
```bash
# List images needing OCR
python scripts/process_images.py "path/to/folder" [--output-json images.json]

# Use in Python for batch processing
from process_images import save_ocr_md, batch_save_ocr, get_images_needing_ocr
```

**Key functions:**
- `get_images_needing_ocr(folder_path)` - Returns list of images without `.md` files
- `save_ocr_md(image_file, summary, sender)` - Save natural summary to `.md` file
- `batch_save_ocr(ocr_results)` - Save multiple OCR results at once

**Markdown structure:**
```markdown
# image.png

**Poslao:** Mahir Kadic
**Datum:** 26.10.2025 13:58

---

Natural language summary focusing on Gastrohem-relevant information:
contacts, names, emails, phone numbers, business details, etc.
```

---

#### 3. process_media.py

**Purpose:** Master script combining audio + images

**Usage:**
```bash
# Scan all folders for a specific date
python scripts/process_media.py --scan-date DD.MM [--output-json results.json]

# Process a specific folder
python scripts/process_media.py --folder "path/to/folder" [--output-json results.json]
```

**Arguments:**
- `--scan-date DD.MM` - Scan all departments for this date
- `--folder PATH` - Process specific folder
- `--base-path PATH` - Base path (default: `gastrohem whatsapp`)
- `--no-skip-existing` - Re-process all files
- `--output-json FILE` - Save results to JSON

**What it does:**
- Calls `process_audio.py` for audio files
- Calls `process_images.py` to find images needing OCR
- Returns combined results

## Best Practices

1. **Use `--scan-date` for daily processing** - Automatically finds all folders for a specific date across all departments
2. **Process audio in parallel** - The script now handles up to 3 audio files simultaneously for faster processing
3. **Batch OCR images** - Read all images in parallel using Claude's vision for maximum efficiency
4. **Save results to JSON** - Use `--output-json` to keep a record of processing results
5. **Process regularly** - Process media files daily to avoid backlog
6. **Separate chat.md updates** - This skill creates JSON files; updating `chat.md` is a separate workflow

## Error Handling

**If transcription fails:**
- Check that `insanely-fast-whisper` is installed
- Verify the audio file is not corrupted
- Check that the device (mps) is available
- Manually transcribe if necessary

**If image OCR is unclear:**
- Request higher quality image from sender
- Focus on extracting key information rather than perfect transcription
- Note any illegible portions in the context field

## Example Workflows

**User:** "Process media"

**Claude:**
1. Runs: `python .claude/skills/gastrohem-media-processor/scripts/process_media.py`
2. Script uses today's date (26.10), scans all departments
3. Finds 3 folders: administracija/26.10, finansije/26.10, adis-chat/26.10
4. Transcribes 5 audio files in parallel → `.json` files created
5. Returns list of 3 images needing OCR
6. Claude reads all 3 images in parallel, creates natural summaries → `.md` files created
7. Reports: "Processed 5 audio and 3 images across 3 folders."

---

**User:** "Process media for 24.10"

**Claude:**
1. Runs: `python .claude/skills/gastrohem-media-processor/scripts/process_media.py --scan-date 24.10`
2. Same workflow for 24.10 date

## Performance Improvements (Nove Optimizacije)

**1. Paralelizacija Audio Transkripicja:**
- Do 3 audio fajla se transkribuju istovremeno
- Koristi `ThreadPoolExecutor` za paralelno izvršavanje
- **3x brže** nego prije

**2. Batch OCR za Slike:**
- Sve slike se mogu pročitati odjednom (parallel Read tool calls)
- Svaka slika dobija svoj `.md` fajl: `image.png.md`
- Prirodan sažetak sa fokusom na Gastrohem-relevantne informacije (kontakti, imena, brojevi, poslovni detalji)
- Helper funkcija `save_ocr_md()` za lako čuvanje

**3. Automatski Scan Svih Foldera:**
- **Default:** Koristi današnji datum (nije potrebno specificirati)
- Automatski pronalazi sve foldere za taj datum u SVIM odjelima
- Procesira sve odjednom

**Struktura Skripti:**
- `process_audio.py` - Audio only (paralelno)
- `process_images.py` - Image OCR helper functions
- `process_media.py` - Master skripta (kombinuje oba)

**Tipična brzina:**
- Audio: ~3-5 sec po fajlu (paralelno, 3 max)
- Slike: ~2-3 sec po slici (batch)
- Scan svih odjela: <1 sekunda
