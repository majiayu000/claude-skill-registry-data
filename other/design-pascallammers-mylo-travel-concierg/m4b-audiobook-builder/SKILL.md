---
name: m4b-audiobook-builder
description: Build and merge M4B audiobooks on Linux from multiple audio files or multi-part M4B sets, with chapter generation, metadata normalization, UTF-8/Russian encoding handling, and validation. Use when combining MP3/M4A/AAC/FLAC/OGG/WAV into one M4B, merging split M4B parts, or fixing audiobook chapters and metadata.
---

# M4B Audiobook Builder

## Overview

Build a single player-friendly M4B from many audio parts or merge existing M4B parts while preserving metadata, normalizing text to UTF-8, and generating chapters. Keep details in `references/guide.md` and use the helper script for repeatable inputs.

## Workflow

1. Confirm the scenario (mixed audio files vs existing M4B parts) and collect target metadata (title, author, performer/narrator, cover art) from the source files metadata, folder names, and file names. Cover art may be embedded in the metadata of the source audio files or provided separately as file `cover.jpg` or same.
2. Determine actual playback order; do not assume lexical filename order for multi-part M4B sets.
3. Choose the best merge order, metadata source, and cover image source yourself using metadata and sidecar/embedded art, then draft a single action plan that proposes those choices.
4. Normalize filenames and tags to UTF-8, assuming Russian for any non-UTF-8 text.
5. Show all the metadata and the order to the user and ask them to confirm the action plan (or adjust it) once before merging. Batch order, metadata, and cover questions into this one confirmation. After confirmation, do not ask follow-ups; proceed to merge/recode and apply the confirmed metadata.
6. Minimize model queries: batch related checks by combining multiple console commands and present consolidated outputs.
7. Generate concat lists and chapters:
   - For mixed audio files, run the helper script to emit `files.txt` and `meta.txt`.
   - For existing M4B parts, generate only `files.txt` and follow the reference for chapter merging.
   - If per-file chapters are too fine-grained compared to the real book chapters, prefer per-directory chapters or a curated chapter list.
8. Build the output M4B with ffmpeg:
   - Re-encode heterogeneous inputs.
   - If a source codec is exotic or poorly supported, re-encode to a well-supported codec (AAC for M4B is the default).
   - Use multi-threaded modes where supported (e.g., ffmpeg `-threads`) to speed up transcoding.
   - If the merge is long-running, set a sufficiently long command timeout in your runner up front (e.g., Codex CLI `timeout_ms`) to avoid re-runs.
   - If inputs may contain embedded cover art (common in MP3), map audio only (e.g., `-map 0:a:0 -vn`) to avoid accidental video streams.
   - Use `-c copy` only when M4B parts share compatible codecs.
9. Apply audiobook metadata and cover art. Treat author and performer as distinct fields (author for `albumArtist`, performer/narrator for `artist`) and format person names as `Last First`. If cover art found, embed it in the final M4B.
10. Validate with `mediainfo`, `mp4info`, and a target player.

## Helper Script

Run:

```bash
python3 scripts/build_m4b_inputs.py --root . --recursive --chapter-mode dir --files-out files.txt --meta-out meta.txt --ffmpeg-out ffmpeg.sh --output-m4b book.m4b
```

Use this to create:

- `files.txt` for ffmpeg concat input
- `meta.txt` for ffmpeg chapter metadata
- `ffmpeg.sh` with a ready-to-run ffmpeg command line (use `--no-ffmpeg-out` to skip)
- `atomicparsley.sh` with a ready-to-run metadata command (use `--no-atomicparsley-out` to skip)

To generate a safe output filename like `Author - Title.m4b`, supply `--output-author` and `--output-title` (invalid filesystem characters are replaced). The script reorders author names to `Last First` by default when building the filename (use `--name-order keep` to preserve input). If omitted and `--output-m4b` is left at `book.m4b`, the script derives author/title from the first input's tags and falls back to the folder name. If `--output-m4b` lacks the extension, `.m4b` is appended.

```bash
python3 scripts/build_m4b_inputs.py --root . --chapter-mode file --files-out files.txt --meta-out meta.txt --output-author "Author" --output-title "Title"
```

Use `--chapter-mode file` for per-file chapters, or `--chapter-mode none` to generate only `files.txt`. For file chapters, the script prefers embedded track titles when present and falls back to filenames.
Use `--chapter-mode file` only when file boundaries match real chapters; otherwise prefer `dir` or a curated chapter list.

For multi-part M4B sets, propose a merge order before any concat work:

```bash
python3 scripts/propose_m4b_order.py --root . --files-out files.txt
```

Use the proposed order and metadata/cover suggestions to build an action plan and ask the user to confirm before merging.

Extract and embed cover art (sidecar image or embedded metadata):

```bash
python3 scripts/cover_art.py --root . --recursive --output cover.jpg --embed book.m4b
```

## References

Use `references/guide.md` for detailed commands, chapter formats, and scenario-specific procedures.
