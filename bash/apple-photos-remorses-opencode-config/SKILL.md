---
name: apple-photos
description: >
  Search and export photos from Tommy's Apple Photos (iCloud Photos) library on this Mac by content:
  AI caption, OCR text in the image, labels, people, places and dates, with osxphotos. Exports a fast
  local preview or the full original downloaded from iCloud, without opening the Photos app. Use when the
  user asks to find a photo, screenshot, receipt, document, sticker or picture in their photos or camera
  roll, or to send one to Discord.
---

# apple-photos

Read the Photos library database directly with [osxphotos](https://github.com/RhetTbull/osxphotos) (via `uv`). No Photos UI, no focus stealing. Works because the shell has Full Disk Access.

- **Library:** `~/Pictures/Photos Library default.photoslibrary` (~10k items, all in iCloud). The other `.photoslibrary` folders in `~/Pictures` are empty or tiny; ignore them.
- **Most originals are not on disk** (iCloud "optimize storage"). Local preview JPEGs exist for almost all of them.

## 1. Search

`scripts/search.py` matches every term (AND, substring) against the AI caption, OCR text, labels, place, people, title, keywords and filename. Loads in ~2s.

```bash
S=~/.config/opencode/skills/apple-photos/scripts/search.py
uv run -q $S router sticker                         # newest first, 20 max
uv run -q $S --from 2026-10-01 --label Document     # date range + exact label
uv run -q $S --person 'Name' --limit 5 --json       # json includes caption and OCR words
uv run -q $S --screenshot wifi                      # screenshots only
uv run -q $S --help
```

Each result prints `preview:`, the path of Photos' own preview JPEG (~1024 px) inside the library. **Read it directly** to check the photo; no export needed. Captions are vague, so always look before you claim a match.

Tips:
- Search in **English** for captions and labels (`receipt`, `screenshot`, `whiteboard`). OCR text keeps the image's language (`fattura`, `password`).
- OCR words are single lowercase tokens: search `wifi`, not `wi-fi network`.
- List all labels with counts: `uvx osxphotos labels --library "$HOME/Pictures/Photos Library default.photoslibrary"`.
- For anything the script lacks (albums, favorites, screenshots only, videos), use `uvx osxphotos query --help` (never truncate it) or write a small `uv run` script with `osxphotos.PhotosDB(...).photos()`; each photo has `.search_info.detected_text`, `.ai_caption`, `.labels`, `.persons`, `.place`, `.date`.

## 2. Export

```bash
L="$HOME/Pictures/Photos Library default.photoslibrary"
OUT=/private/var/folders/8w/wvmrpgms5hngywvs8s99xnmm0000gn/T/opencode/photos; mkdir -p $OUT

# fast: local preview JPEG (~1k px), enough to look at or send
uvx osxphotos export $OUT --library "$L" --uuid <UUID> --preview-if-missing

# full original from iCloud through PhotoKit (no Photos window)
uvx osxphotos export $OUT --library "$L" --uuid <UUID> --download-missing --use-photokit
```

- The destination folder must exist first, or export fails with `Path ... does not exist`.
- Repeat `--uuid` to export several in one call.
- Always pass `--use-photokit` with `--download-missing`. Without it osxphotos drives the Photos app with AppleScript, which can bring it to the front.
- Download the original only when the preview is too small (small print on stickers, receipts, documents).
- HEIC originals: convert before reading or uploading, `sips -s format jpeg in.HEIC --out out.jpg`.
- Never upload files from inside the `.photoslibrary` folder: copy or export them to the temp folder first.

## 3. Send it

Upload the exported file with `kimaki upload-to-discord <files>`, several files in one call.

## Rules

- **Private data.** Photos contain IDs, passwords and documents. Never print OCR text of sensitive photos into Discord; describe what you found and upload the image only when the user asked for it.
- **Read-only.** Never modify the library (no `osxphotos import`, `batch-edit`, `timewarp`, keyword writes) unless the user asks. Never delete photos; if the user wants cleanup, put them in an album and let them delete in Photos.app (30-day Recently Deleted).
- Results skip hidden photos and Recently Deleted, like Photos search does.
- Search the database, never run OCR yourself: Photos already indexed the text (`search_info.detected_text`). osxphotos `--detected-text` re-runs Vision on every file and is very slow.
- Full Disk Access is what makes this work. If the library cannot be opened (`unable to open database`), tell the user to grant Full Disk Access to the app running OpenCode; do not try workarounds.
- MCP alternative if ever needed: [sweetrb/apple-photos-mcp](https://github.com/sweetrb/apple-photos-mcp) (same osxphotos backend, read-only by default).
