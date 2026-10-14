---
name: whisper-extract
description: |
  Extract, transcribe, and summarize audio or video files using OpenAI Whisper. Use this skill
  whenever the user wants to transcribe audio or video, extract what was said in a recording,
  get a transcript of a meeting/interview/lecture/podcast, or generate a summary of spoken content.
  Also trigger when the user mentions files like .mp3, .mp4, .wav, .m4a, .ogg, .flac, .webm,
  .mkv, .mov and wants text out of them. Generates a .md file with an AI summary followed by
  the full literal transcript.
  También se activa en castellano: "transcribir", "transcripción", "extraer audio",
  "qué dice este audio", "transcribir reunión", "transcribir entrevista",
  "pasar audio a texto", "resumir grabación", "transcribir este video",
  "extraer texto de audio", "transcript", "whisper", "grabar y resumir".
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.1.1"
---

# Whisper Extract

Transcribe audio or video with Whisper, then produce a `.md` file containing an AI summary
followed by the complete literal transcript.

## Prerequisite check

Before doing anything else, verify that Whisper is installed:

```bash
whisper --help > /dev/null 2>&1 && echo "OK" || echo "NOT FOUND"
```

If not found, tell the user to run:

```bash
pipx install openai-whisper
brew install ffmpeg   # if ffmpeg is missing
```

The `turbo` model requires `openai-whisper` >= 20240930; if the install is older, tell the
user to run `pipx upgrade openai-whisper`.

Then stop and wait — do not proceed until Whisper is available.

---

## Step 1: Gather required information

Ask the following in a **single message** if the user has not already provided them.
Never ask more than once, and never ask for things already mentioned in the conversation.

**Required:**
- **Audio/video file path** — absolute or relative path to the file (mp3, mp4, wav, m4a, ogg, flac, webm, mkv, mov, mpeg, mpga, oga, wma).
- **Language** — spoken language in the recording. Examples: `Spanish`, `English`, `Portuguese`. If unsure, say "auto-detect" and Whisper will figure it out (slower).
- **Recording context** — a short description of what this is (e.g., "team meeting about Q3 roadmap", "interview with a candidate", "product demo call", "lecture on clean architecture"). This is used to write a better summary.

**Optional (ask only if not obvious):**
- **Whisper model** — default is `turbo` (recommended speed/accuracy balance). Options: `tiny` (fastest, less accurate), `base`, `small`, `medium`, `turbo`, `large-v3` (most accurate, slower). Ask only if the user wants a different speed/accuracy trade-off.
- **Output directory** — where to save the `.md` file. Default: same directory as the audio file.
- **Output language for summary** — language for the summary and headings. Default: same as the recording language. If the user wants the summary in a different language, note it.

Wait for the user's answers before proceeding to Step 2.

---

## Step 2: Transcribe with Whisper

Run Whisper on the provided file. Use the `--output_format json` flag to capture word-level
timing and text cleanly, and `--output_dir` to control where the raw output goes. Clear
`/tmp/whisper-extract-temp` first so leftovers from a previous run cannot be picked up.

```bash
whisper "<file_path>" --model <model> --language <language_code_or_auto> --output_format json --output_dir /tmp/whisper-extract-temp
```

> **Important:** Always emit this as a **single line** — never split with `\` continuations.
> A trailing space after `\` is not a line continuation in zsh; it becomes an escaped space
> that Whisper receives as a second (empty) file path, causing ffmpeg to fail with
> `Error opening input file  .`

Language codes: `es` for Spanish, `en` for English, `pt` for Portuguese, `fr` for French, etc.
For auto-detect, omit `--language` entirely.

**If the file is large (> 1 hour):** Whisper will take several minutes. Tell the user:
> "Starting transcription — this may take a few minutes depending on file length and model."

After the command completes, read the JSON file in `/tmp/whisper-extract-temp/` whose basename
matches the input file, and extract the `text` field. This is the full raw transcript.

If Whisper fails (file not found, unsupported format, ffmpeg missing), report the exact error
and suggest a fix before continuing.

---

## Step 3: Generate the summary

Given the full transcript text and the recording context provided by the user, produce a
structured summary. Write it in the output language chosen in Step 1.

The summary must cover:

1. **What this recording is about** — one or two sentences.
2. **Key topics discussed** — bulleted list of the main themes or agenda items covered.
3. **Key decisions or conclusions** — if any were reached (skip this section if the recording is
   a lecture or monologue with no decisions).
4. **Action items** — concrete next steps mentioned, with owner if stated (skip if none mentioned).
5. **Notable quotes or moments** — 1-3 verbatim fragments that best capture the essence of the
   conversation (optional but highly recommended for interviews and meetings).

Keep the summary concise: aim for 150-300 words. Do not pad it.

---

## Step 4: Write the .md file

Construct and save the output Markdown file.

### File naming

Use this pattern: `YYYY-MM-DD-<slugified-context>.md`

Examples:
- `2026-04-14-team-meeting-q3-roadmap.md`
- `2026-04-14-candidate-interview-backend.md`
- `2026-04-14-lecture-clean-architecture.md`

If today's date is available in context, use it. Otherwise, use the file's modification date
via `stat` or just omit the date prefix and use the slugified context alone.

### File structure

Use this exact template:

```markdown
---
title: "<recording context>"
date: YYYY-MM-DD
model: <whisper model used>
language: <detected or specified language>
source: "<original filename>"
duration: "<approximate duration if available>"
---

# <Descriptive title based on context>

## Summary

<The summary generated in Step 3>

---

## Full Transcript

<The complete literal transcript from Whisper, paragraph-formatted>
```

**Transcript formatting rules:**
- Do NOT split the transcript into fake speaker turns unless Whisper detected them.
- Preserve the raw text exactly as Whisper returned it — do not paraphrase or clean up grammar.
- Wrap long monolithic output into readable paragraphs by inserting a blank line roughly every
  10-15 sentences. This makes the file easier to navigate without altering the content.

Save the file to the chosen output directory using the current runtime's file-write capability.

---

## Step 5: Confirm and show the result

After saving, show the user:

1. Full path to the `.md` file.
2. The summary section (so they can read it immediately without opening the file).
3. A one-line note about transcript length: `Transcript: ~N words`.

Do not dump the entire transcript in the chat — it's in the file. If the user wants to
search or quote from the transcript, they can open the file.

---

## Error handling

| Problem | Action |
|---|---|
| `whisper: command not found` | Tell user to run `pipx install openai-whisper` |
| `ffmpeg not found` | Tell user to run `brew install ffmpeg` |
| File not found | Ask user to confirm the path; suggest `ls` to check |
| Unsupported format | Tell user to convert with `ffmpeg -i input.xyz output.mp3` |
| Transcription empty / very short | Warn user — likely a silent file or wrong path |
| Unknown model `turbo` | Tell user to run `pipx upgrade openai-whisper` (needs >= 20240930) |
| Out of memory | Suggest a smaller model (`medium`, `small`) |

---

## Tone

Write the summary in the same language as the recording (or the output language if specified).
Be concise and factual — the summary serves as a quick reference, not a narrative essay.
The transcript is the source of truth; the summary is the lens.
