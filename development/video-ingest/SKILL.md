---
name: video-ingest
description: Turn a video or audio recording — a local file OR a URL (YouTube, TikTok, Instagram, ...) — into vault knowledge using the crv (claude-real-video) CLI. Scene-aware keyframes + a Whisper transcript, frames correlated to what's being said, compiled into Raw source + Wiki notes with screenshots. Use when the user points at a recording, a meeting, a screen capture, or a reference video and wants it watched, transcribed, analyzed, or added to the vault.
---

# Video Ingest (crv → frames ⇄ transcript → LLM Wiki)

Actually *watch* a recording: `crv` extracts deduplicated keyframes + a Whisper
transcript; you then correlate what's SHOWN with what's SAID, and ingest it the
vault's way — full capture in `Raw/Sources/`, reusable knowledge compiled into
`Wiki/`, key screenshots in `assets/`. Follow `AGENTS.md` and the
`llm-wiki-ingest` skill for the compile step.

## Environment

- `crv` is the `claude-real-video` pip package (CLI: `crv`). Check `crv --help`;
  install with `pip install claude-real-video` if missing.
- `ffmpeg`/`ffprobe` must be reachable. If not on PATH (common on Windows),
  prepend for the run, e.g. `$env:PATH = "C:\ffmpeg\bin;" + $env:PATH`.
- On Windows PowerShell set `$env:PYTHONUTF8=1` in the same command (avoids a
  cosmetic Unicode crash on the final print; output still lands).
- Whisper on CPU is slow (~0.5–1× real-time). **Run crv in the background** and
  wait for completion; don't poll.

## Step 0 — Pick the right input

- **URL?** crv takes URLs directly (YouTube, TikTok, Instagram, ...):
  `crv "https://youtube.com/watch?v=..." -o <OUTDIR> ...`. For login-gated
  sites, `--cookies <netscape-file>` or `--cookies-from-browser <browser>`
  (the user's own account, authorized use only).
- **Audio-only file (.wav/.mp3)?** No frames → no "what's shown". Screen
  recorders (OBS) often save a big `.mkv`/`.mp4` **and** a small `.wav`
  sibling — prefer the video. Confirm streams with:
  `ffprobe -v error -show_entries stream=codec_type,codec_name:format=duration <file>`.

## Step 1 — Extract (background)

```powershell
$env:PYTHONUTF8=1
crv "<VIDEO-OR-URL>" -o "<SCRATCH-OUTDIR>" --lang en --whisper-model small `
    --adaptive --text-anchors --viewer --max-frames 200 `
    --why "Full examination for the vault: capture everything said and shown."
```

Use a scratch `<OUTDIR>` outside the vault. Produces `transcript.txt`, `frames/`
(`frame_001.jpg`… chronological), `MANIFEST.txt`, `viewer.html`. Frame selection
is **visual only** (scene change + dedup + a time floor): crv guarantees
*coverage of distinct screens*, not importance. Importance is judged next — by
you, using the transcript.

## Step 2 — Watch it: correlate frames ⇄ transcript

This is the step that makes the ingest worth anything.

1. Read `transcript.txt` in full. It has **no timestamps and no speaker
   labels**; Whisper often **hallucinates on trailing silence** — drop the
   nonsense tail. (Known quirk: domain terms get misheard consistently; when a
   word looks wrong everywhere, flag it as an open question instead of
   propagating it.)
2. Read the frames **in order**. Don't read all N blindly: do a **strided
   overview pass** (every ~8th frame) to map the arc of the recording, then
   read **densely** through the sections that matter (code, terminals, UIs,
   slides, whiteboards, diagrams).
3. **Align said ⇄ shown by chronological position**: frames and transcript both
   run start→end, so a frame ~40% through the frame list pairs with text ~40%
   through the transcript. Anchor pairs at unmistakable moments (a screen
   change that matches a topic change) and interpolate between anchors. Record
   the pairing explicitly in the Walkthrough ("What's said / What's shown").
4. **Redact secrets.** Recordings of dev work routinely expose tokens, keys,
   account IDs, URLs with credentials, passwords. Never transcribe secret
   values and **never copy a frame that shows one into the vault**. Transcribe
   other on-screen text/code verbatim where legible.

## Step 3 — Ingest the vault's way

- **Raw source** → `Raw/Sources/<date>-<slug>-recording.md` with source
  frontmatter (`Title`, `Author`, `Reference` = the URL or filename,
  `ContentType`, `Created`, `Processed: false`, `tags: [source]`). Body: a
  provenance note (crv flags, whisper model, frame count, redactions,
  transcript quality), a **Summary**, a chronological **Walkthrough**
  (What's said / What's shown pairs), the embedded screenshots, a **Key
  topics** list of `[[wikilinks]]`, and the **full transcript** appended at the
  end for searchability.
- **Screenshots** → copy only the important, secret-free frames into `assets/`
  with descriptive names; embed with `![[name.jpg]]`. Do **not** dump all
  frames or the source video into the vault (`Raw/Files/` is gitignored;
  `assets/` is committed).
- **Compile** → search first
  (`python scripts/wiki_tool.py search-catalog --query "…"`), then create or
  enrich focused `Wiki/` notes, each linked back to the Raw source in `sources`
  with an accurate `source_count`. Prefer enriching existing notes over
  duplicating. Capture ambiguity as **Open Questions**; never invent.

## Step 4 — Gate + commit

```bash
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

Commit the Raw source, `assets/` screenshots, compiled notes, and regenerated
artifacts together. Add a log note for substantial ingests.

## Notes

- Reference-video mode (a TikTok/YouTube the user wants studied, not archived):
  same Steps 0–2, then answer their question directly; only ingest to the vault
  if they want it kept.
- Optional crv flags: `--grid` (contact sheets), `--keep-audio`, `--report`,
  `--scene 0.2` (more frames), `--whisper-model medium` (better transcript).
- Big videos stay outside the vault; reference them by URL/filename in the Raw
  source's `Reference`.
