---
name: youtube-transcript
description: Extract a YouTube transcript with yt-dlp, preserve all substantive spoken content, and save polished markdown with an intuitive filename and clear structure (metadata, overview, readable body, optional timestamp reference).
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

Extract and **publish** the transcript from a YouTube video: $ARGUMENTS

$ARGUMENTS should include:
- A YouTube URL (e.g. `https://www.youtube.com/watch?v=VIDEO_ID`, `https://youtu.be/VIDEO_ID`)
- Optionally: `--output DIR` — directory for the final `.md` file (default: `transcripts/`)
- Optionally: `--timestamps` — include a **Timestamped reference** section (default: include it when useful for long videos; omit only if user asks for plain prose only)
- Optionally: `--language LANG` — subtitle language code (default: `en`)

---

## Non-negotiable: content fidelity

The transcript is **source material**, not a summary. Every edit must preserve meaning and coverage.

1. **Do not remove substantive speech** — No paraphrasing that drops claims, examples, numbers, names, or definitions. No “condensing” that deletes sentences the speaker said.
2. **Safe cleanup only** — You may remove: VTT artifacts, duplicate **consecutive** lines from auto-captions, filler stutters only when they are exact repeats with no added meaning (`the the` → `the`), broken cue fragments that are **pure** duplicates of adjacent text, and obvious non-speech (`[Music]`, `[Applause]` — optional to keep in italics if they matter for context).
3. **Deduplication rule** — Collapse repeats **only** when the current line is identical (after trim) to the **immediately previous** line. Do not merge distinct sentences that happen to share a phrase.
4. **Verify before write** — After building the readable transcript, sanity-check against the raw cue list:
   - Rough **word count** of the cleaned body should be ≥ ~85–90% of the raw concatenated cue text (allowance for true duplicates and junk). If it drops far below, you removed too much — restore content.
   - If the video is long, spot-check **opening, middle, and closing** segments against the VTT: no missing paragraphs or skipped timestamp ranges.
5. **If unsure, keep the text** — When cleaning is ambiguous, preserve the longer/original wording.

---

## Before starting

1. **Parse the video ID** from the provided URL. Accept:
   - `youtube.com/watch?v=VIDEO_ID`
   - `youtu.be/VIDEO_ID`
   - `youtube.com/embed/VIDEO_ID`
   - `youtube.com/v/VIDEO_ID`
   - Bare video ID (11 characters, alphanumeric + `-` / `_`)
   - If none match, ask for a valid link.

2. **Check for `yt-dlp`**: `which yt-dlp`. If missing:
   ```
   yt-dlp is required. Install: pip install yt-dlp
   ```

3. **Ensure output directory exists** — Create `transcripts/` or the user’s `--output` directory.

---

## Step 1 — Fetch video metadata

```bash
yt-dlp --print title --print id --print uploader --print channel_id --print duration_string --print upload_date --no-download "VIDEO_URL"
```

Capture: **title**, **id**, **uploader** (channel name), **duration**, **upload_date**. Use these for the file header and filename.

---

## Step 2 — Download subtitles

Try in order until a `.vtt` exists:

### 2a — Manual subtitles
```bash
yt-dlp --write-subs --sub-lang LANG --skip-download --sub-format vtt -o "transcripts/%(id)s" "VIDEO_URL"
```

### 2b — Auto-generated (fallback)
```bash
yt-dlp --write-auto-subs --sub-lang LANG --skip-download --sub-format vtt -o "transcripts/%(id)s" "VIDEO_URL"
```

If neither produces `.vtt`:
```
No subtitles available (language: LANG). Captions may be disabled; try --language with another code.
```

Use a **60s timeout** on these commands; report timeout if it fails.

---

## Step 3 — Parse VTT (preserve content)

Read the `.vtt` and build an internal **cue list** before any prose shaping:

1. Strip `WEBVTT`, `Kind:`, `Language:`, cue IDs, positioning (`<c>`, `align:`, `position:`).
2. Strip HTML tags (`<b>`, `<i>`, `<u>`, `<font>`, etc.); keep the inner text.
3. Parse timestamps `HH:MM:SS.mmm --> HH:MM:SS.mmm` and attach text lines to each cue.
4. **Deduplicate** only consecutive identical lines (auto-subs).
5. Keep the **full cue sequence** in memory for verification and for the timestamped section.

**Paragraph breaks (readable body):** Join cues into paragraphs where:
- There is a **gap ≥ 3 seconds** between cues, or
- A clear **topic shift** (new section, rhetorical reset) without losing intervening sentences.

Do **not** drop cues to “improve flow.”

---

## Step 4 — Intuitive filename

Save as **kebab-case** from the video title, ASCII-only, lowercase, with a **short id suffix** for stability and deduplication.

**Pattern:** `{slug-from-title}-{video_id}.md`

- **Slug rules:** Lowercase; replace spaces and underscores with `-`; strip punctuation except hyphens; collapse multiple hyphens; max ~60 characters from the title portion (trim whole words if needed); keep the full 11-char `video_id` at the end.
- **Examples:**
  - Title “AutoResearch with Claude Code” + id `abc123xyz01` → `autoresearch-with-claude-code-abc123xyz01.md`
  - If the user’s project already uses a folder like `lab/youtube/ai/`, place the file there when they specify `--output lab/youtube/ai`.

**Never** use only the raw video id as the filename unless the user explicitly requests it.

---

## Step 5 — Markdown structure (organization)

Write one `.md` file with this **section order**. Adapt headings to the video (e.g. add `## Part 1 — …` only when the talk has clear movements), but keep the core blocks:

```markdown
---
title: "FULL VIDEO TITLE"
video_id: VIDEO_ID
url: https://www.youtube.com/watch?v=VIDEO_ID
channel: "CHANNEL / UPLOADER NAME"
duration: DURATION
uploaded: UPLOAD_DATE
extracted: ISO_DATE
subtitle_type: manual | auto-generated
language: LANG
source: youtube-transcript skill
---

# FULL VIDEO TITLE

Brief one- to three-sentence **overview** of what the video covers (accurate to the transcript; no invented claims).

## Key topics

- Bullet list of 3–8 themes **actually discussed** in the transcript (scan headings/cues; do not hallucinate).

## Transcript

Readable, **paragraph-structured** transcript. Use `###` subheadings only when the speaker clearly changes major topic or after long gaps (optional but improves scanability).

[All substantive spoken content belongs here — this is the canonical body.]

## Timestamped reference

Only if `--timestamps` is on, or by default for videos longer than ~15 minutes, or when the user will need to jump to moments:

Use one block per cue or group adjacent cues in the same minute:

`[MM:SS] Text...`

For videos under ~15 minutes with no timestamp flag, you may omit this section if the user asked for minimal output; otherwise include it.

## Chapters (optional)

If YouTube chapter titles are present in the description **or** obvious in the speech, add a small table: `| Start | Chapter |` with links `https://www.youtube.com/watch?v=VIDEO_ID&t=Xs`.

```

**Formatting habits:**
- Escape YAML double quotes in `title` / `channel` if needed.
- Use proper markdown lists and `###` for intra-transcript sections sparingly.
- No wall-of-giant-paragraph: break every ~4–8 sentences for readability **without** deleting sentences.

---

## Step 6 — Clean up

Delete the intermediate `.vtt` (and any `.part` files) after the markdown is written and verified.

---

## Output message to user

After saving:

```
## Transcript saved

- **Video**: TITLE
- **Channel**: UPLOADER
- **Duration**: DURATION
- **Subtitles**: manual | auto-generated
- **Approx. words** (body): N
- **Fidelity check**: raw cue words ≈ M; retained ratio OK / note if borderline
- **File**: path/to/slug-title-VIDEO_ID.md
```

---

## Error handling

- **Invalid URL** — Ask for a valid YouTube link.
- **yt-dlp missing** — Install instructions; stop.
- **No subtitles** — Clear message; suggest `--language`.
- **Network / timeout** — Report; suggest retry.
- **Language mismatch** — Try `en`, `en-US`, or list available tracks via `yt-dlp --list-subs` if needed.
