---
name: vault-yt-digest
description: Digest a YouTube video into a vault note in `30_Resources/Web-Clips/` — pulls transcript, metadata, thumbnail, and (optionally) slide-change screenshots into a temp bundle, then Claude reads the bundle and writes the digest in the user's note style. Use when the user pastes a YouTube link and asks to "digest", "log", "note", "save", or "summarise" it for the vault. For talks/lectures with slides, pass `--shots` to also extract keyframes at scene changes (slide flips). Wraps the lower-level `tool-youtube-transcript` skill — prefer this skill when the goal is a vault-filed digest, not a raw transcript dump. NOT for a raw transcript dump (use tool-youtube-transcript, which this wraps) and NOT for a source PDF (use vault-source-digest).
---

# YouTube Digest Skill

Two-layer skill:

1. **`yt_digest.py`** — pure ingestion. Builds a temp bundle dir with transcript, metadata, thumbnail, and optionally slide screenshots. No LLM work.
2. **Claude (you)** — reads the bundle and writes the digest note. The script does not ghost-write the synthesis; the note voice is the user's, not a template.

## Setup

Already-installed dependencies on this machine:

- `youtube-transcript-api` (via `tool-youtube-transcript`)
- `yt-dlp` on `PATH` (the script resolves it with `shutil.which`, so the install location does not matter)
- `ffmpeg` at `C:\ffmpeg\bin\ffmpeg.exe` (only needed for `--shots`)

If any are missing, install: `pip install youtube-transcript-api yt-dlp` and download ffmpeg.

## Usage

```bash
# Minimal — transcript + meta + thumbnail
python "skills/vault-yt-digest/yt_digest.py" <url-or-id>

# Slide-heavy talk — also extract scene-change screenshots
python "skills/vault-yt-digest/yt_digest.py" <url-or-id> --shots

# Tune scene detection (lower threshold = more shots; default 0.4)
python "skills/vault-yt-digest/yt_digest.py" <url-or-id> --shots --shot-threshold 0.3 --max-shots 40

# Custom bundle dir (default: %TEMP%/yt-digest-<id>/)
python "skills/vault-yt-digest/yt_digest.py" <url> --out ./my-bundle
```

The script prints a JSON summary to stdout (bundle path, title, channel, duration, shot list) and progress to stderr.

## Bundle layout

```
yt-digest-<id>/
├── meta.json              # title, channel, duration_s, upload_date, url, thumbnail, description
├── transcript.txt         # plain text, one snippet per line
├── transcript_ts.txt      # with [hh:mm:ss] prefixes
├── thumbnail.jpg          # poster frame
└── shots/                 # only with --shots
    ├── 0001_000132.jpg    # NNNN_HHMMSS — frame index + approximate timestamp
    ├── 0002_000418.jpg
    ├── ...
    └── index.txt          # one line per shot: "HH:MM:SS\tfilename"
```

## Workflow when the user asks to digest a YouTube video

1. **Decide on `--shots`.** Pass it for talks/lectures with slides, tutorials with code on screen, anything visual. Skip it for podcasts, interviews, talking-head pieces — saves a video download (~50–200 MB) and ~30s of CPU.
2. **Run the script.** Bundle lands in `%TEMP%/yt-digest-<id>/`.
3. **Read the bundle** with the Read tool: `meta.json`, `transcript.txt` (use `limit`/`offset` for long videos), and any shots that look load-bearing (thumbnails of slides, diagrams).
4. **Copy the transcript into the vault** at `{vault}/30_Resources/Web-Clips/<YYYY-MM-DD> <Speaker> - <Title>.transcript.txt`.
5. **Copy useful slide shots** into a sibling `<...>.shots/` folder, renaming them by content if helpful (`01-cdlc-loop.jpg` rather than the raw timestamp name).
6. **Write the digest note** at `{vault}/30_Resources/Web-Clips/<YYYY-MM-DD> <Speaker> - <Title>.md` with frontmatter matching the existing pattern in that folder (see the Matt Pocock and Patrick Debois notes for shape). Embed shot images with `![](<note-stem>.shots/01-cdlc-loop.jpg)` when they pin down a concept the prose can't.
7. **Note structure** (mirror what's already in Web-Clips):
   - `## Thesis` — one paragraph.
   - One section per major argument or phase.
   - `## How this lands against EmptyOS` — strengths, gaps, concrete adoptions, real tensions.
   - `## What I take away` — 2–4 bullets.
8. **Don't dump the whole transcript** into the note; the transcript file is the receipt, the digest is the synthesis.
9. **Adopt into the `video-digest` app** so every surface (Claude Code CLI, EOS chat, web UI on `/video-digest/`) sees one source of truth and the hub badge / `video-digest:digested` event fire. Best-effort: skip if the daemon is unreachable, the digest is already in the vault either way.

   ```bash
   # Reads auth_token from emptyos.toml via tomllib (durable across formatting).
   TOKEN=$(python -c "import tomllib; print(tomllib.load(open('emptyos.toml','rb'))['network']['auth_token'])")
   curl -s -X POST "http://127.0.0.1:9000/video-digest/api/adopt" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"digest_path": "30_Resources/Web-Clips/<YYYY-MM-DD> <Speaker> - <Title>.md"}'
   ```

   Expected response: `{"ok": true, "item": {...}}`. On `{"ok": false, "error": "..."}` the digest is still saved to the vault — the adopt is just the cross-surface registration. Idempotent: re-adopting the same path updates the existing row.

## When to pass `--shots`

| Video type | `--shots`? | Why |
|---|---|---|
| Conference talk with slides | Yes | Diagrams, code, frameworks lose meaning without the visual |
| Tutorial with code on screen | Yes | Code samples in slides aren't always read aloud |
| Whiteboard / diagram-heavy | Yes | Spatial relationships matter |
| Podcast / interview | No | Pure audio content; thumbnail alone is enough |
| Talking head / vlog | No | No visual information beyond the speaker |
| Music video / film clip | No | Out of scope for a digest skill |

## Notes

- The shot timestamps are **approximate** — they come from even spacing across video duration after deduplication, not the actual frame PTS. Good enough for "around the 12-minute mark"; not good enough for precise quote-with-shot pairing. If precise alignment is needed, parse ffmpeg's `showinfo` stderr in a follow-up pass.
- Scene detection picks any visual change above threshold — a presenter walking across stage will trigger shots too. Spot-check the bundle before copying everything into the vault.
- The video download for `--shots` uses `≤480p` to keep bytes modest. Slides at 480p are still legible.
- This skill never auto-deploys, never publishes, never touches `data/`. It writes only to `%TEMP%` and (via Claude) to the vault.
- For videos with no captions, this skill fails the same way `tool-youtube-transcript` does. There's no Whisper fallback here yet.
