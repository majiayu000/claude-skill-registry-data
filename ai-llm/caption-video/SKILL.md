---
name: caption-video
metadata: {packVersion: 1.3.0}
description: >-
  Burn timed, styled captions into a finished video on the local machine, without
  re-rendering the source. This is the manual fallback to the API's captioning
  endpoint, POST /v1/captions, which stays the default path: come here when the
  style the user wants is outside the API's presets, when the wording has to be
  hand-corrected before it is burned into the pixels, or when the source was
  rendered with audio disabled and the API refuses it. Transcribes the audio with
  Whisper, groups words into reading phrases, renders the captions in a real
  browser via HyperFrames, and composites them over the source with ffmpeg using
  a real alpha channel. Use when the user has an MP4 with speech and asks to add
  captions, subtitles, burned-in text, TikTok-style captions or word-by-word text
  to it, and the API path has been ruled out. Runs out of band, so it costs no
  credits and works on any video file whoever generated it. Not for generating
  video (use the video skills) and not for a separate .srt/.vtt sidecar file.
---

# Caption a finished video

Takes a finished MP4 with speech and returns the same video with timed captions
burned in. Nothing is regenerated: the source pixels and the source audio pass
through untouched, and the captions are composited on top.

**This skill makes no API calls.** It is ffmpeg + Whisper + HyperFrames on a
local file, so it costs no credits and needs no API key.

## Check the API path first

`POST /v1/captions` is the default, and it is one call against a finished asset
with a set of preset styles and no local toolchain at all. Read the
`novoads-api` skill's SKILL.md (*Burned-in captions*) for the call, and
[prompting/guide.md](prompting/guide.md) here for the full side by side. **Offer
both paths rather than picking silently**, because the API costs credits and this
skill costs a first-time setup.

> **REST key required. A Novoads MCP connector is not a substitute.** If
> `NOVOADS_API_KEY` is missing or still the placeholder, stop before any
> generation work and tell the user: "Before continuing, create an API key at
> <https://novoads.ai/dashboard/settings?tab=api> and paste it into `.env`."
> That holds even when `mcp__novoads__*` tools are connected and authenticated in
> the session. Never call `mcp__novoads__*` tools from this repo's workflows: they
> are a different surface with different behavior, including the units they quote
> costs in. Repo installs verify with `./scripts/check-novoads-env.sh`; a solo
> install checks `NOVOADS_API_KEY` in the environment.

**Pack version.** Every `/v1` response carries `X-Novoads-Pack-Version`; mention a newer pack at <https://github.com/novoads/agent-skills> only when that header names a version NEWER than this file's `metadata.packVersion` — equal or older is nothing to say, and it is never a reason to stop.

Come here instead when the user:

- wants a caption look the presets do not cover,
- has to hand-correct the words before they are burned in. Invented brand names
  are the usual reason: transcription mishears them, and the API gives you
  nowhere to fix it,
- is captioning enough footage that per-minute credits add up,
- has a line the API path burns **wrong**. Its renderer can truncate a word even
  when its own transcript is correct — see *Safety rules* below. There is nothing
  to fix on that path, so the local burn is the fix,
- or has a source rendered with `audioEnabled: false`, which the API refuses with
  a `409`. This skill can still caption it if the user supplies the words.

## When to use this skill

Trigger on phrases like:
- "add captions to this video" / "burn in subtitles"
- "TikTok-style captions" / "word-by-word captions"
- "caption this ad before I deploy it"
- the captions step of a video-ad pipeline, after the master is stitched

Do **not** use it to *generate* video — that's the `novoads-api` skill and the
style pipelines. Do not use it when the user wants a sidecar `.srt`/`.vtt`
subtitle file rather than pixels; Whisper alone covers that.

## Read order

1. **This file** — the pipeline shape, the gates, the hard-won rules.
2. **[prompting/guide.md](prompting/guide.md)** — the full recipe: Whisper model
   choice, the silence-offset transcription pattern, the word-grouping helper,
   the composition skeleton, the alpha composite, and the pitfall table.
3. **[shared/references/craft.md](../../references/craft.md)** § 3 — the
   trim-before-captioning doctrine step 1 below rests on, and § 1 for why the
   burned frames are the check rather than the transcript. Read it before you
   restate either rule anywhere; it holds one position per rule, and the copy is
   the failure mode.

## Prerequisites

- **ffmpeg** on PATH. Homebrew's build is fine here — this skill deliberately
  avoids the `subtitles`/`drawtext` filters, which Homebrew ships without.
- **Whisper** — `pip install openai-whisper`, or the bundled
  `npx hyperframes transcribe`.
- **Node + npx** for HyperFrames.
- **The finished video on disk.** Chat-pasted files are not accessible; ask for
  a real path.

## Workflow

1. **Trim dead space first, if any.** If the source has beats where VO ends and
   silent visual continues, tighten it *before* transcribing. Timestamps taken
   from an untightened master drift once the video is trimmed later.
2. **Initialize** a captioning project beside the source video.
3. **Transcribe** — pick the Whisper model by audio type (`medium.en` for the
   typical speech-over-music ad). **Transcribe a silence-trimmed copy and offset
   the timestamps back**; Whisper smears the first words across leading silence
   otherwise. The source file itself is never modified.
4. **Group** words into 3–5 word reading phrases, then eyeball `groups.json`.
5. **Render** the captions over a transparent background at the source's frame
   rate, and **composite** with ffmpeg using the alpha channel.
6. **Verify** the output: duration, resolution and frame rate match the source,
   audio is bit-identical, and the captions land on the words.

The guide carries the exact commands for each step.

## Rules that cost a whole render to rediscover

- **Composite with a real alpha channel, not a chroma key.** Render
  `--format mov` and let ffmpeg `overlay` use the alpha. A magenta key cannot
  cleanly remove a soft `text-shadow` — the shadow blends toward the key colour
  and leaves a purple halo on every glyph. Verified on a live clip 2026-08-03.
- **Never put `<video>` or `<audio>` in the composition.** HyperFrames wraps any
  `class="clip"` element in a managed timing wrapper that overrides your CSS and
  reserves an ~80px layout block — a hard black bar across the render.
- **Match the frame rate to the source.** HyperFrames defaults to 30fps; Seedance
  renders 24. Pass `--fps 24` for Seedance output. Mismatched rates produce
  judder and creeping caption drift.
- **Match the composition size to the source resolution** exactly, or the
  composite lands 1–2px off.
- **`-c:a copy`** on the composite, always. The source's narration/BGM/ducking
  mix is already correct; re-encoding it is pure loss.

## Safety rules

- **Never overwrite the source video.** Write to a new filename. The source is
  the only copy of an expensive render.
- **Read the transcript before rendering.** Whisper mis-hears brand names and
  numbers. Correcting `groups.json` costs seconds; a wrong caption burned into a
  deployed ad costs a re-render.
- **Show the user the grouped phrases** (or the first render) before treating the
  captions as final.
- **Read the burned frames, not just the transcript.** A correct transcript does
  not prove a correct caption. On 2026-08-12 the API path's `hustle` preset burned
  `BOTT.` for `bottle.` in every frame of a closing line while its own transcript
  had the word right — `bottle.` at 13.199–13.439s. The fault sat in the render
  layer, downstream of transcription, so every check that stopped at the words
  passed it. Compare the burned cards **word for word against the approved
  script** before shipping, and treat a truncated or garbled word as a failed run
  rather than a note. That take was charged and thrown away; the local burn is
  what shipped.

## Hand-off

The captioned MP4 is a finished creative. To publish it as a Meta ad, that's the
separate `meta-ad-builder` skill — which opts out of Meta's frame-modifying
Advantage+ enhancements precisely because these captions are burned into the
pixels.
