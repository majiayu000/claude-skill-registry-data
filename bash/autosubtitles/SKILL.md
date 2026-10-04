---
name: autosubtitles
description: Add styled, burned-in captions to a video, let the user pick a style and fix captions in a small review window, and (with AutoSubtitles Pro) generate SRT/VTT subtitle files. Use when the user asks to caption, subtitle or transcribe a video file on their machine.
license: MIT
compatibility: Requires Node.js 20+, Google Chrome or Microsoft Edge, and internet access. Needs an agent that can run shell commands on the user's machine.
metadata:
  author: autosubtitles
  homepage: https://autosubtitles.com/agent
  version: "0.3.1"
---

# AutoSubtitles

Captions a local video with the `autosubtitles` command. Speech is transcribed by AutoSubtitles and the captions are burned in locally, inside the user's own Chrome. Only the audio track is uploaded; the video stays on the machine.

Requires Node 20+ and Google Chrome or Microsoft Edge. Every command is `npx autosubtitles …`; add `--json` and read the single JSON object it prints.

## Setup: Free or Pro, once per conversation

Before the first render or review window:

```bash
npx autosubtitles plan --json
```

If `plan` is `pro`, carry on without asking. If it is `free`, tell the user the difference and ask which they want before you continue:

| | Free | Pro |
|---|---|---|
| Watermark | AutoSubtitles logo on the video | None |
| Resolution | Up to 720p | Up to 4K |
| Video length | Up to 10 minutes | No limit |
| Subtitle files (SRT, VTT, word timings) | No | Yes |

- **Free:** continue straight away.
- **Pro:** they get a license at https://autosubtitles.com, set `AUTOSUBTITLES_LICENSE_KEY` in their own shell, and start a new session so you can see it. Then run `plan` again.

If `reason` is `invalid_key`, `inactive` or `payment_failed`, say that a key is set but is not active, and ask the same question. Do not ask again once the user has chosen. If the plan is `free` and they only want subtitle files, or the video is longer than 10 minutes, do not run the command: tell them that needs Pro.

Never ask for, read, print or store a license key.

## Commands

| Command | Group | What it does | Reference |
|---|---|---|---|
| `caption <video>` | Caption | Burn captions in, in a named style. No window | [references/caption.md](references/caption.md) |
| `restyle <video>` | Caption | The same video in another style. Seconds: the transcript is cached | [references/caption.md](references/caption.md) |
| `live <video>` | Review | A window where the user picks a style, checks captions, and asks you for changes while they watch | [references/live.md](references/live.md) |
| `review <video>` | Review | The same window without the conversation: they pick, click Render, you get one result | [references/review.md](references/review.md) |
| `subtitles <video>` | Export (Pro) | SRT, VTT or word-timing files, with or without the video | [references/subtitles.md](references/subtitles.md) |
| `styles` | System | List the caption styles | [references/caption.md](references/caption.md) |
| `plan` | System | Free or Pro, and what each allows | Setup, above |

## Routing

- **No video and no clear request** (the user just invoked the skill): show the commands above as a short menu and ask what they want. Never start a render unasked.
- **An explicit or clearly implied command:** load its reference and follow it. "Caption talk.mp4 in Beast" is `caption`. "Try it in Karaoke instead" is `restyle`. "Give me an SRT" is `subtitles`.
- **A video but no style named, or the user wants to see styles or check captions:** open a window. Use `live` when you can keep a command running in the background and react when it finishes (Claude Code, Codex, Cursor). Otherwise use `review`.
- **Nobody at the computer** (a background job, a batch of files, a scheduled run): never open a window. Pick a style yourself and use `caption`.

A window is the exception, not the default: open one only where seeing the video changes the decision. When the user has already told you what they want, just do it.

## Errors

With `--json`, a failure prints `{ "ok": false, "error": { "code", "message" } }` and exits non-zero.

| Exit | Meaning | What to do |
|---|---|---|
| 2 | Bad arguments, unknown preset, file not found, or no live session open | Fix the command. `styles` lists valid styles |
| 3 | No Chrome or Edge installed | Ask the user to install Google Chrome |
| 4 | Needs Pro (subtitle files only, or a video over 10 minutes), or a rate limit | Tell the user what Pro adds. Do not retry |
| 5 | Transcription failed | Check the video has an audio track with speech, then retry once |
| 6 | Render failed, or the save was interrupted | Retry once. If it fails again, report the message |
