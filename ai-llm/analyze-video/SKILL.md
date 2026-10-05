---
name: analyze-video
metadata: {packVersion: 1.3.0}
description: >
  Analyze a reference video and reverse-engineer its style into a reusable Seedance 2.0
  prompting template for the Novoads API. The output is a new formula file — like
  seedance-2-ugc.md — that captures the video's structure, pacing, camera work, edit style
  and tone so it can be recreated with any product, any person, in any setting. Use this
  whenever someone provides a video they want to use as a style reference, says "I want to
  make videos like this", "deconstruct this video", "turn this into a template", "analyze
  this style", or drops a video file and wants to recreate that format repeatedly.
---

# Analyze video → reusable prompting template

Someone found a video style they love. Your job is to deconstruct it into a reusable
prompting template — a formula they can plug any product, person or setting into and get
that same style back from `seedance-2.0`.

The output is **not** a single prompt. It is a **formula file** saved into
`skills/novoads-api/prompting/prompt-library/`, built the way
[seedance-2-ugc.md](../novoads-api/prompting/prompt-library/seedance-2-ugc.md) is built: layers, variables,
option banks, rules, and a worked example, so the agent can generate unlimited prompts in
that style.

**Nothing in steps 1 to 6 touches the API.** Frame extraction, transcription and analysis
are local work on the user's own file: no calls, no credits. Only step 7, the optional test
render, spends anything, and it runs through the two gates in [SKILL.md](../novoads-api/SKILL.md)
like every other generation.

**There is a hosted alternative, and it is not the default.** `POST /v1/analyses` reads an
uploaded ad into a structured breakdown (hook boundary, beat timeline, on-screen text,
casting, layer zones) in one synchronous call, at a **flat fee per analysis** that does not move
with length. Price it through `POST /v1/estimates` with `{"kind":"analysis"}` first. Two reasons it
is the fallback and not the front door here: the local path costs nothing and reads the whole
runtime, while `/analyses` defaults to the first 20 seconds (120 is the ceiling, and raising
it trades hook precision for coverage). Reach for it when ffmpeg is not installed, when the
user wants zone labels rather than prose, or when the frame read has already failed. Offer it
with the price attached and let the user choose; never substitute it silently for step 1.

**The 15-second constraint is the whole design problem.** `seedance-2.0` and
`seedance-2.0-mini` take any integer 4 to 15 seconds, and the reference video is usually
30 to 60. Your template has to distil the style into what fits one 15-second clip, and say
how to recreate the longer arc across a series of clips.

## Dependencies

- **ffmpeg** / **ffprobe** — required for frame and audio extraction (step 1).
  `brew install ffmpeg` on macOS.
- **whisper** — optional, for transcription (step 2). `pip3 install openai-whisper`. If it
  is unavailable, ask the user to paste the dialogue instead.

Neither is a Novoads dependency. Both run locally on the user's file.

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

## Inputs

- **Video file** (required): path to `.mp4`, `.mov`, `.webm` or similar.
- **Style name** (optional): what to call the template — `car-review`, `unboxing-hype`,
  `skeptic-converted`. If they do not give one, name it from what you observe.

## Step 1: Extract frames and audio

```bash
bash "skills/analyze-video/scripts/extract-frames.sh" \
  "<video_path>" "/tmp/video-analysis" <num_frames>
```

Frame count by source duration:

| Source duration | Frames |
|---|---|
| Under 10s | 8 |
| 10–20s | 12 |
| 20–30s | 16 |
| Over 30s | 20 |

Read `metadata.txt` for duration, resolution and fps.

## Step 2: Transcribe the audio

Try, in order:

1. `whisper` CLI: `whisper /tmp/video-analysis/audio.wav --model base --output_format txt --output_dir /tmp/video-analysis`
2. Python whisper inline.
3. Neither available → ask the user for the dialogue, or to install whisper.

The transcript is where pacing lives: speech rhythm, filler words, how dialogue interleaves
with action. All of that defines the style, and all of it has to survive into the template.

## Step 3: Study the reference templates

Read the shipped formulas before you write one. They are the standard your output has to
meet:

- [seedance-2-ugc.md](../novoads-api/prompting/prompt-library/seedance-2-ugc.md) — 9-layer UGC formula, the richest example
- [seedance-2-premium-reveal.md](../novoads-api/prompting/prompt-library/seedance-2-premium-reveal.md) — dark-void reveal, no person
- [seedance-2-product-hero.md](../novoads-api/prompting/prompt-library/seedance-2-product-hero.md) — elemental product hero, no person
- [seedance-2-studio-lookbook.md](../novoads-api/prompting/prompt-library/seedance-2-studio-lookbook.md) — studio lookbook with voiceover
- [seedance-2-feature-walkthrough.md](../novoads-api/prompting/prompt-library/seedance-2-feature-walkthrough.md) — feature demo, multi-clip series

And the platform guide, which every one of them defers to:

- [seedance-2.md](../novoads-api/prompting/prompt-library/seedance-2.md) — request fields, the grid, prompt craft, what the estimate flags, the adaptation checklist

Notice what they share:

- They name **layers** — the structural building blocks of the style.
- Each layer has a **pattern**: a repeatable sentence shape with `{{VARIABLES}}`.
- Variables come with **option banks**, not blanks.
- They state **rules** that explain why a choice matters.
- They declare a **mode** — `startImageAssetId` or `referenceAssetIds` — at the top.
- They carry a **worked example** that has been priced live.

Your template has to hit that depth to be usable.

## Step 4: Analyze the frames — find what defines this style

Read **all** the extracted frames. You are not describing one video; you are isolating the
transferable pattern.

For every dimension ask: "is this specific to THIS VIDEO — the person, the product, the
room — or is it THE STYLE?" Only the style goes into the template. The specifics become
variables.

### Structure and pacing

- How long is the source? How many distinct beats?
- Which 2–3 beats are essential — the ones without which it stops being this style?
- What is the arc? Hook → demo → proof → verdict, or something else?
- Fast cuts or held shots? How long is each beat?
- Silent beats, or wall-to-wall dialogue?
- **The compression question:** if you had to carry the whole feel in 3 beats and 2–3
  spoken lines, which moments survive?

### Camera and framing

- Filming perspective: selfie, propped phone, second operator, screen recording?
- How does framing change between beats — tighter, wider, same angle throughout?
- Is there a signature move that *is* the style?

### Edit style

- Jump cuts, continuous take, time-lapse, split screen?
- Transitions: hard cuts, dissolves, text?
- Recurring motifs: close-up product inserts, reaction face, before/after?

### Dialogue and script structure

- Hook format: question, bold claim, mid-action, reaction?
- Scripted, improvised, voiceover, text-on-screen?
- Speech patterns that carry the tone: filler words, sentence length, vocabulary.
- How lines relate to what the hands are doing.

### Tone and energy

- 3–4 emotion words for the vibe.
- Energy arc: builds, flat, peaks then drops?
- Relationship to the viewer: friend, expert, skeptic, fan?

### Lighting and technical quality

- Light source and direction: natural, ring light, moody, blown out?
- Phone or polished? Which technical "flaws" are load-bearing?
- Audio character: phone mic, lapel, voiceover, room tone?

### What makes this style DIFFERENT

The most important pass. After cataloguing everything above, name the 2–3 things that
separate this from a generic UGC clip or a generic product review — the pacing, the hook
format, the way the product enters frame, the edit rhythm. Those become the core of the
template; everything else is scaffolding.

### The 15-second plan

Before building anything, map the style onto one clip:

- **What is the minimum viable version?** Which beats are essential, which are nice to
  have. Fifteen seconds has to carry the thing that makes someone say "oh, *that* kind of
  video".
- **Does it need a series?** If the power is in a narrative arc or a feature rundown, it
  needs 2–3 clips. If it is a vibe or a single moment, one clip is enough.
- **How many spoken lines fit?** Delivery measures **2.0 words per second** (~13 characters a
  second, spaces included) after ~0.5s of leading silence. Fifteen seconds is 2–3 short
  sentences, and the slack is what leaves room for a silent beat. Count the source's lines and keep the ones
  carrying the voice.
- **What is the beat skeleton?** 15 seconds is 2–3 beats: hook → core moment → kicker.

### Which mode the style wants

Every formula in this library declares one, because they are mutually exclusive on the API
and the choice follows from the style:

| If the style… | Mode | Why |
|---|---|---|
| opens on the product itself, held up or sitting on a surface | `startImageAssetId` | the product photo is literally the first frame |
| builds a scene the product was never photographed in — a void, a splash, a studio set | `referenceAssetIds` | the model has to composite it, not animate a flat photo |
| holds one person across a series of clips | `referenceAssetIds` | `@Image1` the product, `@Image2` the person — Seedance re-casts on every cut, and a repeated description does not hold a face |

Write the answer into the template. A formula that leaves the mode open produces prompts
whose `@Image1` tokens point at nothing.

## Step 5: Build the template

Create a self-contained markdown file. Someone should be able to read it and write prompts
in this style without ever seeing the source video.

### Template structure

```markdown
# [Style name] — Seedance 2.0

**Use when:** [the kind of video this produces]

**Model guide:** read [seedance-2.md](../novoads-api/prompting/prompt-library/seedance-2.md) first for the request fields, the grid,
and the platform rules.

**Mode:** `startImageAssetId` or `referenceAssetIds` — say which, and what each `@ImageN`
slot holds. The two are separate modes and a body carrying both is a `400`.

## What defines this style

[2–3 paragraphs of theory. This is what lets a prompt writer make good variable choices
instead of filling blanks.]

## Things to know before you write a word

[The route-specific traps. If the style speaks, say that the line is rendered and
lip-synced in this same call and that gate 1 applies. If it is silent, say that silence has
to be declared in the prose.]
mandatory.]

## The structure

[The layers of THIS style. Do not force-fit the 9-layer UGC model. Five layers, twelve
layers — let the video decide.]

## Layer-by-layer formula

### Layer N: [Name]

[What this layer does and why it matters here.]

**Pattern:**
\```
[The repeatable sentence shape with {{VARIABLES}}]
\```

| Variable | Options | Notes |
|---|---|---|
| `VARIABLE_NAME` | option 1, option 2, option 3 | [guidance] |

### [... more layers ...]

## Beat structure (one 15-second clip)

[The 3-beat framework: hook, core, kicker. Which beats speak and which are silent. Two to
three spoken lines total.]

## Multi-clip strategy (if applicable)

[How to split across 2–3 clips, what each one covers, and what holds identity across them:
the same `referenceAssetIds` in every call plus the actor tag repeated verbatim.]

## Tone and pacing guide

[Energy, speech patterns, rhythm, with a pacing-cue bank specific to this style.]

## Technical specs

[Lighting, camera quality, audio character — including the flaws that make it authentic.]

## Complete template

[One copy-paste block for ONE 15-second clip, every variable marked {{PLACEHOLDER}}.
Max 3 beats, max 2–3 spoken lines. This is the unit.]

## Example prompt

[The template filled in for a DIFFERENT product, person and setting than the source video.
Price it at POST /v1/estimates before shipping it.]

## Adaptation checklist

[The style-specific checks, then the standard ones from seedance-2.md.]

## Generating from this template

[The call sequence — see step 7 of analyze-video for the block to paste here.]
```

### Rules the template has to teach

These are not style preferences. Each one is a defect found in a shipped formula, and a
template that omits them manufactures the same defect in every prompt written from it.

- **Every prompt is one clip of 4 to 15 seconds.** If the style needs more, the template
  ships a multi-clip strategy — never a longer prompt.

- **Keep prompts between 100 and 260 words.** Shorter prompts produce vague results; longer
  ones overwhelm the model and cause it to lose focus on key details. Do not pad to hit the
  floor and do not cut a beat's framing to stay under the ceiling.

- **Variables are curated choices, not blanks.** "Any lighting" is useless. "Natural window
  light, overhead kitchen light, golden-hour balcony light" is a decision the writer can
  actually make.

- **Declare the mode and address references as `@Image1`, `@Image2`, …** The tokens resolve
  **positionally** against `referenceAssetIds` in the order the array is sent, and a token
  pointing past the end of the array is refused before the charge. If the style uses a
  start frame instead, say so and use no tokens at all.


- **If the style is silent, say so in prose** — `a silent product film with no spoken
  dialogue`, `silent b-roll`. Seedance renders audio from the prompt, so a film that never
  declares silence can come back with an invented voice on it. Do not put on-screen text in
  double quotes and call it done — the model reads a quoted string as a line to speak.

- **No forbidden words:** `cinematic`, `professional`, `stunning`, `8k`, `studio`,
  `perfect`. Nothing on the API rejects or reports them — this is craft advice, and the
  reason to drop them is the render. Replace one with the real thing: the light source,
  the surface, the flaw.

- **Prose, never a bulleted prompt.** A run of `Label: value` pairs or `-` lines comes back
  **rendered as literal text on screen**. Use timestamps — `[00:00]`, `[00:05]` — for
  multi-beat pacing instead.

- **One primary action per shot**, with two or three comma-joined cues on it. A second
  action chained with `then` / `and then` / `followed by` renders as a smear. Split it into
  two shots.

- **Repeat the actor tag verbatim.** `the same woman` resolves to nobody; identity does not
  carry across a cut.

- **The example must use different content than the source.** If the source was a woman
  reviewing a serum in her bedroom, the example is a guy reviewing a protein bar in his
  kitchen. That is what proves the template generalises.

- **Dialogue has to fit.** Count the words: **2.0 per second** measured, so a `D`-second
  clip holds about `2.0 × (D − 0.5)` once the leading silence is paid for. If the source
  talks fast, say so in the template and keep each line punchy.

- **No credit numbers anywhere in the template.** Prices come from a live
  `POST /v1/estimates` in the session that spends them. A template that quotes a number
  teaches the next agent to skip the call.

## Step 6: Save, register and present

1. Save to `skills/novoads-api/prompting/prompt-library/seedance-2-<style-name>.md`.
2. **Add a row to the style directory** in
   [seedance-2.md](../novoads-api/prompting/prompt-library/seedance-2.md) so the new formula is reachable —
   user goal, file link, key trait, matching the rows already there. A formula nothing
   points at is a formula nobody reads.
3. Summarise in chat: the style you identified, its layers, what makes it distinct, and the
   path you saved it to.
4. Ask: *"Want me to price a test prompt from this template and render it, to prove it
   works?"*

If they say yes, write the prompt for a different product, person and setting than the
source — that is the actual test — and run step 7.

## Step 7: Render a test clip (optional, and it costs credits)

The template is the deliverable; this step only proves it. It runs the full sequence from
[SKILL.md](../novoads-api/SKILL.md), and **both gates apply**.

1. **Upload the product photo** if the prompt references one:

   ```bash
   curl -sS -X POST https://api.novoads.ai/v1/uploads \
     -H "Authorization: Bearer $NOVOADS_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"contentType":"image/jpeg","sizeBytes":248193}'
   ```

   then PUT the raw bytes to the `uploadUrl` it returns, sending back **exactly** the
   headers it returned. The `assetId` is durable and reusable across calls, models and
   sessions — upload once and keep the id.

2. **Price it — gate 2.** `POST /v1/estimates` with `kind: "video"`, the `prompt`, the
   `model` and `durationSeconds`. It charges nothing and it is the only source of a price. It also
   returns an advisory `warnings` array of craft notes (verified live 2026-08-04) — read them,
   but they are substring matches that false-positive, and the checklist above is still the
   real quality gate. Show the number and get a yes before spending.

3. **Confirm the spoken line — gate 1**, if the clip speaks. Numbered beats, word count
   against the duration, the `language` you are sending, an explicit yes. Approving the
   template is not approving the sentence.

4. **Generate:**

   ```bash
   curl -sS -X POST https://api.novoads.ai/v1/videos \
     -H "Authorization: Bearer $NOVOADS_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "seedance-2.0",
       "prompt": "<the filled-in prompt>",
       "durationSeconds": 15,
       "aspectRatio": "9:16",
       "language": "en",
       "referenceAssetIds": ["<assetId>"],
       "productId": "<uuid>"
     }'
   ```

   Swap `referenceAssetIds` for `startImageAssetId` if that is the template's mode. Never
   both. Returns `202` with `jobId` and `creditsCharged`.

5. **Poll** `GET /v1/generations/{jobId}` every 15 seconds until a **terminal** status —
   `succeeded`, `failed`, `blocked` or `canceled`. Not until `succeeded`: a loop waiting
   for success never returns on a job that died. `seedance-2.0` usually takes 3 to 8
   minutes, most often around 5; `seedance-2.0-mini` 2 to 3.

6. **Download** `GET /v1/generations/{jobId}/watch`, save under
   `outputs/<descriptive-subfolder>/`, and open the folder so the user can watch it.

**Draft on `seedance-2.0-mini` first.** It is the same grid, the same fields and the same
prompt at half the price, back in 2 to 3 minutes — and since the `assetId` is durable, the
final render on `seedance-2.0` reuses the same upload. A template validated on mini is a
template validated.

Paste this block into every template you generate, so the formula carries its own call
sequence:

```markdown
## Generating from this template

1. Upload the product photo: `POST /v1/uploads` → `assetId` (durable, reuse it).
2. Price it: `POST /v1/estimates` with `kind: "video"`, `model`, `durationSeconds`,
   `prompt`. It charges nothing, it is mandatory, and it is the only source of a price — show the number out loud
   before spending.
3. Confirm the spoken line with the user if the clip speaks (`SKILL.md` gate 1).
4. Generate: `POST /v1/videos`

\```json
{
  "model": "seedance-2.0",
  "prompt": "<your filled-in prompt>",
  "durationSeconds": 15,
  "aspectRatio": "9:16",
  "language": "en",
  "referenceAssetIds": ["<assetId>"]
}
\```

   `startImageAssetId` instead if that is this formula's mode — never both, that is a `400`.

5. Poll `GET /v1/generations/{jobId}` every 15s until a terminal status, then download from
   `GET /v1/generations/{jobId}/watch`.

Every clip in a series is its own call and its own charge. Five generations per
organization may be in flight at once.
```

## Related files

- [clone-video-ad/SKILL.md](../clone-video-ad/SKILL.md) — the sibling: same analysis, but the output is
  a generated video for the user's product instead of a template file.
- [scripts/extract-frames.sh](scripts/extract-frames.sh) — frame and audio extraction,
  shared by both skills.
- [seedance-2.md](../novoads-api/prompting/prompt-library/seedance-2.md) — the platform guide every generated template defers to. The other two live video models carry their own grids, and you need one the moment a template targets them rather than Seedance: [sora-2.md](../novoads-api/prompting/prompt-library/sora-2.md) when the first spoken word has to land immediately (it measured no leading silence, where Seedance front-loads 3–5s), [veo-3-1.md](../novoads-api/prompting/prompt-library/veo-3-1.md) when the user names Veo or the shot has to evolve over its runtime. Neither takes `referenceAssetIds`.
- [ugc-selfie-style.md](../novoads-api/prompting/prompt-library/ugc-selfie-style.md) — the cross-model UGC guide. Its *Core principles* transfer to Seedance; its per-model formulas do not — never port one across by find-and-replace.
- [../../SKILL.md](../novoads-api/SKILL.md) — the call sequence, the two gates, polling, download.
- [../../reference.md](../novoads-api/reference.md) — every endpoint, field, limit and error code.

## File map

```
skills/novoads-api/
├── SKILL.md                                  ← router: decision tree, gates, full sequence
├── reference.md                              ← endpoints, fields, limits, errors
└── prompting/
    ├── guide.md                              ← marketing brief → API
    ├── brand-voice-starter.md                ← template to copy into MASTER_CONTEXT.md
    ├── analyze-video/
    │   ├── SKILL.md                          ← THIS FILE — video → reusable template
    │   └── scripts/extract-frames.sh         ← ffmpeg frame + audio extraction
    ├── clone-video-ad/
    │   └── SKILL.md                          ← video → adapted video for the user's product
    └── prompt-library/
        ├── seedance-2.md                     ← Seedance 2.0 platform guide (read first)
        ├── seedance-2-ugc.md                 ← 9-layer UGC formula
        ├── seedance-2-premium-reveal.md      ← dark-void premium reveal
        ├── seedance-2-product-hero.md        ← elemental product hero
        ├── seedance-2-studio-lookbook.md     ← studio lookbook with voiceover
        ├── seedance-2-feature-walkthrough.md ← feature walkthrough demo
        ├── ugc-product-selfie.md             ← image formulas (product selfie)
        ├── product-showcase.md               ← image formulas (product showcase)
        ├── influencer-recreation.md          ← image formulas (likeness)
        ├── character-sheet.md                ← image formulas (character consistency)
        ├── character-sheet-gpt-image-2.md    ← the same on gpt-image-2
        ├── nano-banana.md                    ← image formulas (Nano Banana Pro)
        ├── sora-2.md · veo-3-1.md            ← the other two LIVE video models' grids
        └── kling-3.md · ugc-selfie-style.md  ← Kling 3.0 is on the API as `kling-v3-pro` (2.38.0); the selfie guide is cross-model
```

New formulas you write land in `prompt-library/` beside the Seedance files, and get a row
in `seedance-2.md`'s style directory.
