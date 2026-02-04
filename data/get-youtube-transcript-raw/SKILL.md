---
name: get-youtube-transcript-raw
description: Capture a YouTube video transcript as raw material using `ytt`, storing it in the raw/ directory with minimal metadata for later distillation.
---

# Get YouTube Transcript (Raw)

## When to use

Use when you need the raw transcript (plus YouTube title/description) saved to `raw/` for later distillation.

**Keywords:** youtube, transcript, captions, ytt, raw, capture

## Inputs

Required:
- `url` (string): YouTube URL (e.g., `https://www.youtube.com/watch?v=...` or `https://youtu.be/...`)

Optional:
- `title_hint` (string): Used only if `ytt` can’t provide a title.

## Outputs

This skill produces:
1. A new Markdown file in `raw/` named `YYYYMMDD-HHMMSSZ--<slug>.md`
2. YAML front matter aligned with `docs/distillation/distillation-pipeline.md`:
   - `title` (best-effort)
   - `source_url` (the provided URL)
   - `captured_at` (UTC ISO timestamp)
   - `capture_type: youtube_transcript`
   - `capture_tool: ytt`
   - `raw_format: markdown`
   - `status: captured` (or `capture_failed` on failure)
3. Body content: the raw transcript text emitted by `ytt` (no summarization).

## Prerequisites

- `ytt` (this repo’s YouTube transcript utility)
- `python3` (used by the bundled script for slugging and safe YAML string escaping)

## Quick start

Capture directly (uses `ytt fetch --no-copy` internally):

```bash
./scripts/ytraw "<youtube_url>"
```

If the current environment can’t access YouTube (common in sandboxes), run `ytt` locally and pipe:

```bash
ytt fetch --no-copy "<youtube_url>" | ./scripts/ytraw
```

## Manual execution (Fallback)

If you encounter persistent issues capturing a transcript within the sandbox (e.g., network restrictions or tool failures), **inform the user they can run the script manually** on their local machine.

The script `./scripts/ytraw` is designed to extract the URL directly from the clipboard if no arguments are provided.

**Instructions for the user:**
1. Copy the YouTube URL to your clipboard.
2. Run the following command in your terminal:
   ```bash
   ./scripts/ytraw
   ```
3. If manual adjustments are required, you can edit the file directly. If you prefer the model to perform adjustments, share the file path or URL with it.

## Optional: shell alias (zsh)

Add to `~/.zshrc`:

```zsh
ytraw () { ytt fetch --no-copy "$1" | /path/to/repo/scripts/ytraw --from-stdin }
```

## References

- Pipeline and front matter schema: `docs/distillation/distillation-pipeline.md`
