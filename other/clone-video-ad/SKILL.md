---
name: clone-video-ad
metadata: {packVersion: 1.3.0}
description: >-
  Clones a VIDEO ad end to end for a different product or offer, on the Novoads API. The
  deliverable is a finished rendered MP4 — the WHOLE ad, not its opening, and not a
  template. Reads the source's style, pacing, camera work, dialogue and tone, adapts it
  into a Seedance 2.0 prompt, prices it, renders it, files the source beside the clones and
  diffs each clip's transcript against the approved script. Use for "clone this video ad",
  "recreate this video for my brand", "make this ad but for my product" when the source is
  a video, "clone my competitors' VIDEO ads", or a video ad handed over with a product
  photo. **Among cloners the source's medium decides, not the wording**: "clone this ad" plus a
  video lands here; a still, or nothing attached, is clone-image-ad, and animating a still
  as-is is image-to-motion. This pack has no hook-only skill: for the opening alone,
  clone the whole ad and cut. If it does not move, wrong skill.
---

# Clone ad — Seedance 2.0

Clone an existing video ad for a different product. You analyze the source frame by frame,
transcribe the dialogue, extract the visual style and beat structure, then generate a new
`seedance-2.0` video adapted for the user's product.

**How this differs from analyze-video:**

- **analyze-video** → the output is a reusable markdown formula saved to `prompt-library/`.
- **clone-video-ad** → the output is a rendered video delivered to the user.

Steps 1 to 3 are the same analysis in both. The only charge in that half is the transcript
in step 2 — a fraction of a credit, and free on a re-read of the same source. Everything
from step 9 on is the real spend.

## If `shared/` is missing from disk

`references/solo-install.md` — what a solo install lacks (`craft.md`, `caption-video`, the
b-roll scripts, `check-novoads-env.sh`, `MASTER_CONTEXT.md`) and how to fetch each. Skip it
inside the full pack.

## Read order

This skill links outward more than any other here, and its two biggest targets fan out again
(22 and 10 further links). **A file reached through another file gets skimmed, not read**, so
open these four directly, in order. Everything else is lookup.

1. **This file** — workflow, gates, the constraints that bite.
2. `../novoads-api/prompting/prompt-library/seedance-2.md` — fields, grid, prompt craft, what
   the estimate flags. Before composing a prompt, not when one fails.
3. **One** formula matched to the source, not all: `seedance-2-ugc.md` talking-head,
   `-feature-walkthrough` demo, `-premium-reveal` / `-product-hero` product-only,
   `-studio-lookbook` polished. Same directory as (2).
4. `../../shared/references/craft.md` § 1 — the transcribe-verify doctrine step 12 rests on.

`../novoads-api/SKILL.md` is the contract, not a step: open it when a response shape or an
error code needs settling.

## What this API changes about cloning

The analysis half is nearly untouched: frames and the beat structure are local work on the
user's file, and the transcript is one cheap API call instead of a local install (step 2).
The generation half has three differences worth knowing before you promise anything. All three were established with free `400` probes that reject
before any charge, and re-verified field-for-field against the deployed spec `2.12.0`
(2026-08-06):

| The old shape | Here |
|---|---|
| Chain clip 1 → clip 2 → clip 3 as reference **videos**, so each clip inherits the last | **Chaining a clip's output in is not how a series holds.** `referenceVideos` is `400 (root): Unrecognized key`; since API 2.35.0 the Seedance variants take mp4 references in `referenceVideoAssetIds` (see novoads-api), but this skill does not rely on them. What holds a series together is passing the **same image `assetId`s to every clip** plus repeating the actor tag verbatim — see step 5 |
| `audioEnabled: true` to switch speech on, `false` for a silent clone | **`audioEnabled` exists here now, on the two Seedance variants only** (added in spec `2.2.0`; `400 Unrecognized key` on `omni-flash`, `veo-3.1` and `sora-2`). It defaults to `true`, so a clone with dialogue needs nothing. Send `false` only for a deliberately silent clone — and **still write the silence into the prose**, because the flag mutes the render while the prose is what stops the model staging a talking shot. It does not change the price, and `POST /v1/estimates` refuses the field |
| Upload the source audio as `referenceAudios` to clone the voice | **There is no voice cloning on this API** (`referenceAudios` is `400 Unrecognized key`; the Seedance `referenceAudioAssetIds` field from API 2.35.0 takes an mp3 reference, and nothing in this pack has verified it matches a voice). Describe the voice in the prompt — age, accent, pace, energy — and accept that it is a different person's voice. Do not offer the user a voice match you cannot deliver |

Also gone, in the same probe: `endFrame`, `projectId` (this
API has products, not projects), `duration` (it is `durationSeconds`) and `referenceImages`
(it is `referenceAssetIds`).

**`resolution` was on that list and has come back.** It is a real field on `seedance-2.0` — `480p`, `720p`, `1080p`, `4k`, default `720p` (verified live against spec 2.12.0, 2026-08-06). A clone should normally match the source's tier, which for a social ad is `720p`; going above it is a **spend** decision (`1080p` ≈2.5x the base, `4k` ≈5x) that gets priced with `POST /v1/estimates` and approved like any other. **`480p` costs ≈half of `720p`** since the 2026-08-07 family reprice — measured live 2026-08-12, exactly half on both `seedance-2.0` and `seedance-2.5` — so it is a real draft tier, worth offering when a clone is a rehearsal rather than the deliverable. (The older line here, that it cost the same and bought nothing, described the pre-reprice deployment.) **A clone rendered as a series pays the multiplier on every clip** — check the tier before you fan out. On `seedance-2.0-mini` send it only where `GET /v1/models` lists more than one tier (API 2.34.0 on; before it Mini rendered 720p only and the key was a `400`).

**And one the old shape got wrong in the other direction:** aspect ratio is not
`9:16`-or-`16:9`. Seedance takes `16:9` `9:16` `1:1` `4:3` `3:4` `21:9` — probed live, `1:1`
and `4:3` both pass validation — so a square or landscape source clones at its own ratio
instead of being letterboxed into a vertical frame.

## Prerequisites

```bash
which ffmpeg || echo "MISSING — run: brew install ffmpeg"
./scripts/check-novoads-env.sh
```

**ffmpeg and a working key are the whole list.** `extract-frames.sh` needs ffmpeg; the
transcript comes from `POST /v1/transcripts` (step 2) and needs nothing installed. The env
check has to return 200 before step 9, and it is worth running first: discovering a bad key
after the user has approved a dialogue script is a bad look.

whisper is **optional, and only for working offline** — see the fallback in step 2. Do not
ask the user to install it before starting. A clean machine can clone an ad.

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

## Workflow

### Step 0: Gather inputs

**If no source video was handed over, do not ask "which ad?".** That puts the work back on
the user at the moment they asked us to do it. Run `spy-competitor-ads` and say what you are
about to do in one line, with a price and a way out:

> No clip attached. I'll sweep Arcads, Creatify and Icon for their **video** ads and clone
> the strongest. N credits for the sweeps; I'll price the render before it runs. Say "stop",
> or drop your own clip instead.

Four things that line carries, and nothing else:

- **`mediaType: "video"`, and it is not the user's choice.** A static sweep returns creatives
  this skill cannot open, so the mode is fixed here and stated rather than asked. Asking is a
  question with one correct answer.
- **The competitors by name**, so a wrong guess is corrected before it is paid for. Default to
  **three** when you picked them yourself; honor any list the user names.
- **The sweep total from a live `POST /v1/estimates` in this session**, never a number from
  memory or from this file — and quoted as *sweeps*, not as the run. A video render costs
  multiples of a sweep, and step 9 is where that number gets its own gate. A line that implies
  the sweep total is the whole cost is wrong even when every figure in it is real.
- **One word that stops it**, and the escape: they can hand over their own clip instead.

Then act. It is a proposal with a veto, **not a question and not a menu**. `spy-competitor-ads`
returns file paths and a ranked top three; take the top one unless the user picked otherwise,
and carry on into step 1 with that file.

If the sweep comes back empty, say so in one line and stop. It is a charged, correct result —
that brand has no fetchable video ads running — not a reason to re-sweep or to widen the mode.

| Input | Required | Notes |
|---|---|---|
| **Source video** | yes | The ad to clone. `.mp4`, `.mov`, `.webm`. Handed over, or swept for above |
| **Product photo** | strongly recommended | Becomes `startImageAssetId` or `@Image1` in `referenceAssetIds`. Without one, see "no photo" below — the answer is not "let Seedance invent it" |
| **Product / offer description** | if no photo | Features, audience, selling points. Used to rewrite the dialogue and the product references, and to generate a still if they want one |
| **A photo of the person** | optional | Only if the clone is a series — it is what holds one face across clips |
| **Brand voice** | optional | Check `MASTER_CONTEXT.md` first. If its brand blocks are empty, ask for tone and audience |

**Check `references/` at the repo root before asking.** `references/products/` for product
shots, `references/influencers/` for people, `references/aesthetics/` for style boards. If
the photo is already there, offer to use it. These folders ship empty — a `.gitkeep` is not
a product shot, so an empty listing means "ask", not "there is nothing to use".

**No photo? Three routes, in this order — and the last one is the expensive one.**

1. **A real photo of the real product.** Always the best clone. Ask for it first.
2. **Generate a still with `POST /v1/images`**: one call (a slow render answers `running`: poll `GET /v1/generations/{jobId}` for its `images[]`), priced through
   `POST /v1/estimates` and consented to like any other spend. Its response carries an
   **`assetId`** that goes straight into `referenceAssetIds` (step 10). This is the right
   answer for a concept product, a product that does not exist yet, or a user who simply
   has no usable shot. It does **not** eat a render slot: images have their own concurrency
   ceiling, counted apart from `POST /v1/videos` in both directions, so sourcing a still
   never delays a clip and clips in flight never delay the still.
3. **Describe it in the prompt text only.** Say plainly what this means: Seedance invents a
   design, renders it, and charges for it, and the same product will look different in
   every clip of a series. Reach for this when the product is generic enough not to matter.

If they hand over only a video and say "clone this for my product", ask for a photo or a
description before going any further. Cloning a style onto a product you cannot see is
guesswork the user pays for.

### Step 1: Extract frames and audio

Reuse the analyze-video script. Do not duplicate it.

```bash
bash "skills/analyze-video/scripts/extract-frames.sh" \
  "<source_video_path>" "/tmp/clone-video-ad-analysis" <num_frames>
```

| Source duration | Frames |
|---|---|
| Under 10s | 8 |
| 10–20s | 12 |
| 20–30s | 16 |
| Over 30s | 20 |
| The user asks for extreme precision, at any duration | 40–100 |

The script takes any count as its third argument — evenly spaced, no cap — so the top row
costs context, not credits. Use it when the ask is explicitly for a frame-by-frame read.

Outputs: `frame_001.jpg` … `frame_NNN.jpg`, `audio.wav` (16 kHz mono), and `metadata.txt`
with duration, resolution and fps. Read the duration — step 5 branches on it.

### Step 2: Transcribe the source

**The words come from the API.** Upload the source and transcribe it — two calls, nothing
installed:

```bash
# 1. mint an upload slot for the SOURCE video (measure the bytes, never estimate them)
curl -sS -X POST https://api.novoads.ai/v1/uploads \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H "Content-Type: application/json" \
  -d "{\"contentType\":\"video/mp4\",\"sizeBytes\":$(stat -f%z source.mp4)}"

# 2. PUT the bytes with EXACTLY the returned headers, then:
curl -sS -X POST https://api.novoads.ai/v1/transcripts \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H "Content-Type: application/json" \
  -d '{"assetId":"<the source assetId>"}'
```

`POST /v1/uploads` takes `video/mp4`, `video/quicktime` and `video/webm`: the three
formats step 0 accepts. The transcript comes back in the **same response**, not polled for:
`text`, `words[]` with `start`/`end`, `segments[]`, an `srt`, and the detected `language`.

**Uploading the source is for READING it, never for rendering from it.** See the boundary
in step 10 — the source's `assetId` must never reach `referenceAssetIds`,
`startImageAssetId`, or any other generation input.

Record the full transcript, the per-segment timestamps and text, the total word count, and
the language. The language matters twice: it is what you send as `language`, and it is what
you write the adapted prompt in. **The `segments[]` are beat candidates** — they are cut at
the source's own pauses, which is where step 3's beat map usually wants its boundaries.

Two things worth knowing:

- **Timings are in seconds**, matching `metadata.txt`. No conversion.
- **Re-transcribing the same source is free** — `creditsCharged: 0`, served from storage. Do
  not cache it by hand to avoid a charge that will not happen.

**Offline fallback — whisper.** Only when there is no key or no network:

```python
import whisper
result = whisper.load_model("base").transcribe("/tmp/clone-video-ad-analysis/audio.wav")
```

Two traps this pack has already paid for, the same ones
[broll-overlay](../../shared/skills/broll-overlay/SKILL.md) documents:

- **whisper reports milliseconds where this API reports seconds.** Convert, or every beat
  boundary lands 1000× off.
- **`whisper-cli` with no model downloaded returns an EMPTY transcript rather than an
  error.** Homebrew installs the binary with a test stub, so the failure is silent and reads
  exactly like an ad whose every line went missing. `pip3 install openai-whisper` **plus a
  model download** — the binary alone is not enough.

**A silent source.** `audio.wav` is left unwritten when there is no audio stream:
`extract-frames.sh` catches ffmpeg's failure, prints `No audio stream found (silent video)`
and exits `0`, so the missing file is the only signal you get. On the API path the same
thing surfaces as a transcript with no words.

```bash
test -f /tmp/clone-video-ad-analysis/audio.wav || echo "silent source — skip to step 3"
```

If no speech is detected — or there was no audio stream to begin with — note it and skip
the dialogue work in step 7. The clone is a visual-style clone, and it has to **declare its
own silence** twice: `audioEnabled: false` on the call and the silence written into the
prompt text (steps 6 and 8).

### Step 3: Compressed analysis

**There is a hosted alternative, and it is not the default.** `POST /v1/analyses` returns the
same class of read (hook boundary and the observable signal behind it, beat timeline,
on-screen text, casting, layer zones labelled by where their pixels come from) in one
synchronous call, flat **1 credit**, priced through `POST /v1/estimates` with
`{"kind":"analysis"}` first like every other spend. The pass below costs nothing, covers the
whole runtime, and you already have the frames on disk from step 1, so it stays the front
door. Reach for `/analyses` when ffmpeg is not installed, when the clone needs zone labels
rather than prose (`sourceType` tells you which zones are generated footage and which are
overlay, which is the one thing a frame read guesses at), or when this pass has already
failed. Two things to say out loud if you offer it: it is a charge, and it defaults to the
first 20 seconds, so a 40-second source needs `maxSeconds` raised or it reads the hook only.

Read **all** the extracted frames. For each, note:

**Structure and pacing** — how many beats, what the arc is (hook → demo → verdict? reveal →
detail → CTA?), how long each beat lasts against the segment timestamps.

**Camera and framing** — POV (selfie, handheld, tripod, propped phone, over-the-shoulder),
framing per beat (wide, medium, close-up, macro), movement (static, pan, dolly, handheld
shake), and any signature move: "leans into camera", "tilts the product toward the lens".

**Edit style** — transition type, visual rhythm, recurring motifs ("every other beat is an
extreme close-up").

**Dialogue and script structure** — hook format, speech pattern (casual or formal, filler
words, trailing thoughts, mid-sentence cuts), how many spoken lines, how many silent beats,
CTA style.

**Tone and energy** — emotion words, the energy arc, the speaker's relationship to the
viewer: friend, expert, skeptic, fan.

**Lighting and technical quality** — light source and direction, camera class, deliberate
flaws, audio character.

**Product references** — how the product is physically shown, which claims are called out,
what labels and text are visible on screen.

**What makes this ad distinctive** — the 2–3 traits that make it recognisable. These are the
ones that MUST transfer; everything else is negotiable.

This analysis stays in the conversation. It is not saved as a template file — that is
[analyze-video](../analyze-video/SKILL.md)'s job.

### Step 4: Present the analysis, and make it a contract

Show the breakdown before doing anything else, and derive the payload from it **out loud**,
so the user can correct a wrong reading before it costs anything:

```
📋 Source video analysis

Duration: 13.6s | Beats: 4 | Dialogue: 31 words (en) | Style: skeptic-converted UGC

Beat map:
  [00:00–00:03]  HOOK     — close-up, deadpan, "opening line"
  [00:03–00:07]  SHOW     — tilts product to camera, "feature call-out"
  [00:07–00:10]  DEMO     — (silent) applies the product, close-up on texture
  [00:10–00:13]  VERDICT  — back to medium, "closing line + CTA"

Defining traits (must transfer):
  1. [trait] — because [what it does for the ad]
  2. [trait] — because […]
  3. [trait] — because […]

What transfers to your product:
  ✅ Beat structure, pacing, camera angles, edit style, tone, energy
  ✅ Dialogue pattern, adapted to your product
  ✅ Lighting and technical-quality cues

What gets swapped:
  🔄 [source product] → your product
  🔄 [source claim] → your claim
  🔄 [source brand mention] → your brand

What that means for the call:
  • 13.6s ≤ 15s          → single clip, durationSeconds: 14
  • vertical source       → aspectRatio: "9:16"
  • speech detected (en)  → language: "en", dialogue gate applies
  • product photo given   → referenceAssetIds: ["@Image1 = your product"]

Proceed with the adaptation? (yes / adjust)
```

Wait for the answer. This is a reading of their video, not an approval to spend.

### Step 5: Decide the generation mode

```
┌─ Source ≤ 15 seconds?
│   YES → one clip. durationSeconds = the source duration, rounded to an integer in 4–15.
│   NO  → two routes, and the USER picks between them.
│         See "Over 15 seconds is a choice" below. Do not default to either.
│
├─ Do you have a product image — theirs, or one you generated?
│   YES → upload it (or reuse the assetId POST /v1/images already returned), then pick
│         one mode:
│           startImageAssetId  — the ad opens ON the product, held up or on a surface.
│                                It animates that photo as the literal first frame.
│           referenceAssetIds  — the ad builds a scene the product was never photographed
│                                in. It composites the references instead, and the prompt
│                                addresses them as @Image1, @Image2 … by array position.
│         Never both: a body carrying both is a 400 that says they are separate modes.
│   NO  → offer POST /v1/images before falling back to prose (step 0). Prose-only means
│         Seedance invents a design, renders it, charges for it, and re-invents it on
│         every clip of a series.
│
├─ Is it a series (the >15s route the user picked, not every >15s source)?
│   YES → referenceAssetIds, and pass the SAME ids to every clip:
│           @Image1 = the product, @Image2 = the person if one is on screen.
│         Repeat the actor tag verbatim in every clip. Never "the same woman".
│   NO  → either mode.
│
└─ Does the source speak?
    YES → the line is rendered and lip-synced in this same call. Gate 1 (step 7) applies.
    NO  → BOTH halves: send audioEnabled: false, AND declare the silence in the prompt
          prose ("silent b-roll, no spoken dialogue"). The flag mutes the render; the
          prose is what stops the model staging a talking shot. See step 8.
```

**Over 15 seconds is a choice, not a default.** A source longer than one clip's ceiling has
two routes, and which one is right depends on what the user is buying. Present both with
the tradeoff and let them pick — do not choose one and mention the other in passing.

| Route | What survives | What it costs |
|---|---|---|
| **One-shot compression** — the beats become jump cuts inside a single ≤15s render | Continuous voice, no stitching, one charge | The clone no longer matches the source's runtime or pacing, and those are transferable traits too |
| **Multi-clip series** — split at beat boundaries taken from the beat map, never from arithmetic | The source's runtime and pacing | Roughly twice the spend: a charge per clip, and any `resolution` tier paid per clip |

The evidence that one-shot is viable is #13's measured A/B — one render carrying its beats
internally came back at roughly half the spend of a stitched arm whose voice was absent for
half its runtime. **Cite that as viability, not superiority.** The stitched arm anchored
each clip with `startImageAssetId`, a different mechanism from the shared-`referenceAssetIds`
series described below, so it does not measure this route at all.

**A series is held by references, not by chaining.** The old pattern — render clip 1, feed
its output in as clip 2's reference video — is not how this skill holds a series: it passes the same image references to every clip.
That is not a downgrade. This repo's own animation rule says the same thing on its own
merits: *"Don't chain by using an animated end-frame as the next beat's anchor — drift
compounds"* (`skills/claymation-ad/references/formulas.md`). Every clip
anchoring to the same approved stills is the more stable pattern, and because the `assetId`
is **durable across calls, models and sessions**, it costs one upload for the whole series.
Re-uploading the same bytes mints a second asset and throws away the anchor.

**Fire the clips of a series concurrently, not sequentially** — nothing downstream depends
on an earlier clip's output any more. Five generations per organization may be in flight at
once; a sixth comes back `429` with `details.reason` of `concurrency_limit`, which is
solved by waiting for a slot and not by backing off harder.

**Offer the mini draft.** `seedance-2.0-mini` is the same grid and the same prompt at half the
price, back in 2–3 minutes instead of 3–8. Its fields are the same **except `resolution`**,
which it does not take at all — it renders 720p, and sending the key is a `400`. A clone is
exactly the case
for it: the first render is where you find out whether your reading of the source survived
into the prompt. Draft on mini, re-price with `model` set to the final tier, and show both
numbers side by side. `SKILL.md` makes the tier an explicit question, asked once per
workflow.

**Ask how many variations, and which kind — here, not at generation time.** Default 1. Two
different things share the word: the **same script rendered N times** (identical payload,
seed-level variety only) or **N script variants** (distinct dialogue adaptations on one beat
structure). A clone usually wants the second. Ask it now, because everything downstream needs
the answer: step 6 writes N scripts, step 7 gates them together, and step 9 prices each one
before the single yes. Asking at step 11 means the user approved a spend for one prompt and
is then handed three.

Tell the user which mode you picked and why.

### Step 6: Adapt for the user's product

The creative core. Working from step 3:

**Dialogue adaptation** (if the source speaks):

- Keep the **same conversational pattern**. Question hook in, question hook out. If the
  source runs on filler — "like", "okay so" — keep the filler; it is the style.
- Keep the **same number of spoken lines** and the **same silent-beat placement**.
- Keep the **same energy arc**: excited → calm, flat, or building.
- Replace product-specific references with the user's product name, features and claims.
- Match each line's **word count within about ±3 words** so the pacing survives.
- Read it back at a natural pace against the target duration: **2.0 words per second** measured
  (~13 chars/sec with spaces), so a `D`-second clip holds about `2.0 × (D − 0.5)` words.
- **Script variants.** If they asked for N *script variants* rather than N renders of one
  script (step 5), write N distinct adaptations that share the beat structure, the
  silent-beat placement and the per-line word counts, and differ in the hook angle, the
  claim emphasized, or the CTA. They are alternative readings of the same source, not
  escalating rewrites — do not let variant 3 drift into a different ad.

**Visual adaptation:**

- Keep the camera work, the framing per beat, and the edit style you analysed.
- Replace the product description: physical appearance, colours, materials, label details.
- Keep the setting, the lighting and the atmosphere.
- Keep the person description, unless the user wants a different persona.
- Keep the technical-flaw cues — phone quality, mic character, imperfect light. They are
  what makes it read as real.

**Prompt composition.** Read [seedance-2.md](../novoads-api/prompting/prompt-library/seedance-2.md) before
composing, and the closest formula for structure —
[seedance-2-ugc.md](../novoads-api/prompting/prompt-library/seedance-2-ugc.md) for a talking-head source,
[seedance-2-feature-walkthrough.md](../novoads-api/prompting/prompt-library/seedance-2-feature-walkthrough.md) for
a fast demo, [seedance-2-premium-reveal.md](../novoads-api/prompting/prompt-library/seedance-2-premium-reveal.md)
or [seedance-2-product-hero.md](../novoads-api/prompting/prompt-library/seedance-2-product-hero.md) for a
product-only source, [seedance-2-studio-lookbook.md](../novoads-api/prompting/prompt-library/seedance-2-studio-lookbook.md)
for a polished voiceover source. Cloning onto a different model reads that model's own grid first, never a Seedance formula carried across: [sora-2.md](../novoads-api/prompting/prompt-library/sora-2.md) when the source's hook speaks from frame one (it measured no leading silence, where Seedance front-loads 3–5s of it), [veo-3-1.md](../novoads-api/prompting/prompt-library/veo-3-1.md) when the user names Veo — neither takes `referenceAssetIds`, so a clone carrying both the actor and the product stays on Seedance. [ugc-selfie-style.md](../novoads-api/prompting/prompt-library/ugc-selfie-style.md) is the cross-model UGC guide: its *Core principles* transfer, its per-model formulas do not.

**If the mode is a one-shot compression, read
[seedance-2-ugc-v2.md](../novoads-api/prompting/prompt-library/seedance-2-ugc-v2.md) as well — for structure and
mode only.** Take the beats-inside-one-render mechanics from v2 and the prompt craft from
v1, which is the scope that file's own contract sets — and say which came from which when
you present the prompt, so a wrong borrow is visible before it renders. **Your source beat
map wins over its
beat doctrine.** v2 defaults to one-shot and tells you to keep silent beats out of the base;
a clone is not writing a base video, it is reproducing one. If the source has a silent beat,
the clone has a silent beat, and v2 does not get a vote on that.

Then:

- **Order:** Subject + Action + Camera + Style + Constraints, written as flowing prose.
  A bulleted prompt or a run of `Label: value` pairs comes back **rendered as literal text
  on screen**.
- **Keep prompts between 100 and 260 words.** Shorter prompts produce vague results; longer
  ones overwhelm the model and cause it to lose focus on key details.
- **Timestamps** — `[00:00]`, `[00:05]` — for multi-beat pacing, one main action per block.
- **`@Image1`** wherever the prompt points at a reference, matching the array order you will
  send. A token past the end of the array is refused before the charge. If the mode is
  `startImageAssetId`, use no tokens.
- **Consistency anchors:** *the product from `@Image1` remains visually unchanged in every
  shot*, *keep the outfit unchanged across all cuts*.
- **The label hold, whenever a label, package, bottle, box or screen is visible:** *the
  product label remains perfectly sharp and identical to the reference image with its text
  unchanged and fully legible*.
- **One primary action per shot**, two or three comma-joined cues on it. `then` /
  `and then` / `followed by` renders as a smear — split it into two shots.
- **No forbidden words:** `cinematic`, `professional`, `stunning`, `8k`, `studio`,
  `perfect`. Nothing on the API rejects or reports them — this is craft advice, and the
  reason to drop them is the render. Describe the real thing instead: the light source,
  the surface, the flaw.
- **Write it in the source's language** if that is what the user wants rendered. Nothing on
  the API pushes back on a Spanish or Portuguese prompt.

**Duration:** source ≤ 15s → match it, rounded to an integer in 4–15. Source > 15s → whichever
route the user picked in step 5: one ≤15s render for a compression, or one duration per clip
for a series. Never re-decide it here. Validate against the spoken word count; `SKILL.md`
carries the table.

### Step 7: Dialogue confirmation gate

**Mandatory** for any clone that speaks. The line inside the double quotes is what the
actor says out loud in the finished file, and it cannot be changed afterwards without
paying for the render again. Use the format from [SKILL.md](../novoads-api/SKILL.md):

```
📝 Dialogue script (please confirm before I generate)

  1. [HOOK]    "adapted line matching the source's hook pattern"
  2. [SHOW]    "adapted feature call-out for the user's product"
  3. [DEMO]    (silent beat — physical demonstration, no dialogue)
  4. [VERDICT] "adapted closing line / CTA"

Total spoken words: ~N  |  Target duration: Xs  |  language: en  |  Fits at natural pace: ✅

Approve this dialogue? (yes / edit / rewrite)
```

Rules:

- This gate is **separate** from the cost gate, and neither implies the other. Approving the
  analysis is not approving the sentences, and approving the sentences is not approving the
  spend.
- Never infer approval from an earlier yes about tone, beat map or mode.
- If they say edit, revise and re-present until they approve.
- Skip it only when the source is silent, say why you are skipping it, and check that both
  halves of the silence are in place: `audioEnabled: false` on the call and the silence
  written into the prompt prose. Neither one covers for the other.
- On a series, the gate covers **every clip**, presented together.
- On script variants, the gate covers **every variant**, also presented together — one
  block, one approval, however many scripts are in it. Never one gate per variant: the
  point of the block is that they are compared against each other before any is priced.

### Step 8: Language and audio

Three decisions:

1. **`language`** — declared, not controlling. **The prompt is what decides the spoken
   language**: the render says whatever the quoted line says, and nothing rejects a body
   whose `language` disagrees with it. Default the field from the `language` the transcript
   returned (step 2), state
   it in the gate above, and then actually write the dialogue in that language — the field
   records the ad for later reporting, it does not translate anything.
2. **Whether the clone speaks at all.** A silent source clones silent, and that takes
   **both halves**: `audioEnabled: false` in the `POST /v1/videos` body, **and** the
   silence written into the prompt prose (`silent b-roll, no spoken dialogue`). The flag
   mutes the render; the prose is what stops the model staging a talking shot. Prose alone
   pays for a generated voice track you then discard. Quoting on-screen text in the prompt
   is not enough either — the model reads a quoted string as a line to speak, which is the
   opposite of what you asked for. The flag is Seedance-only, and `POST /v1/estimates`
   refuses it: muting is not a discount.
3. **The voice.** It will not be the source's voice — there is no voice cloning here. If
   voice matters, describe it in the prompt (age, accent, pace, energy) and tell the user
   plainly that it is a soundalike, not a match.

### Step 9: Price it — the cost gate

**Never state a credit cost from memory, and never generate before showing a number that
came from a live call in this session.** There are no rate tables in this repo, in
`MASTER_CONTEXT.md`, or in the logs.

```bash
curl -sS -X POST https://api.novoads.ai/v1/estimates \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"video","model":"seedance-2.0","durationSeconds":14,"language":"en","prompt":"<the adapted prompt>"}'
```

Add `"resolution":"1080p"` to that body when the clone is going above the model's default —
see the bullet below.

Returns `credits`, `balance`, `sufficient` and a `warnings` array, plus `shortBy` and
`topUpUrl` when it is short. The body is strict and takes exactly six fields: `kind`,
`prompt`, `model`, `durationSeconds`, `language`, `resolution` — checked field-for-field
against `CreateEstimateRequestVideo` in spec `2.12.0` (2026-08-06). `aspectRatio`,
`audioEnabled`, the asset fields and `productId` are a `400` here.

- **Pass `model` explicitly.** It defaults to `seedance-2.0`, and mini is half the price —
  pricing the wrong tier is a quote that disagrees with the invoice.
- **Pass `resolution` whenever the tier is above the default.** It is the second price
  axis: the high tiers are their own credit schedules, not a surcharge on the low one.
  Leave it out and you quote `720p` and invoice whatever you actually render. On
  `seedance-2.0-mini` send it only where `GET /v1/models` lists more than one tier (API 2.34.0 on).
- **`language` is recorded, not priced.** It does not change what the model is sent and it
  does not move the number — the spoken language comes from the quoted line in your prompt.
  Send it anyway: it is what makes "how do our Spanish ads perform?" answerable later.
- **The `warnings` are advice, never a verdict.** Nothing here can refuse or reprice a
  call, so a weak clone prices, charges and renders exactly like a good one. They are
  substring matches and they **do false-positive** — read each against the prompt, and say
  so when you override one. Step 6's checklist is what actually stands between the two.
- **Price every clip and every variant, each with its own call.** A 3-clip series at 2
  script variants is 6 estimates and 6 charges. The estimates charge nothing and fire
  concurrently, and they are also the per-model length check and the prompt lint — a prompt
  that skipped one is a prompt nobody checked, and there is no second chance at submit
  time. Show the per-call number, the count and the total.
- **Warn when the total exceeds `balance`**, and quote `shortBy` and `topUpUrl` when they
  come back. `sufficient` is a snapshot, not a reservation.

Show the number, the count, the total and the balance. Get **one** yes covering the whole
set. Then generate.

### Step 10: Resolve the product and upload the references

1. `GET /v1/products` → read `.items[]` (not `.products` — verified live 2026-08-05) →
   `productId`. Default to the product named in `MASTER_CONTEXT.md`
   under "My workspace"; with exactly one product, save it there; with none, omit the field
   — it is optional. There is no folder or project ritual to run: folders are read-only on
   this API and there are no projects at all.

2. Upload each reference **once**:

   ```bash
   curl -sS -X POST https://api.novoads.ai/v1/uploads \
     -H "Authorization: Bearer $NOVOADS_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"contentType":"image/jpeg","sizeBytes":248193}'
   ```

   Returns `assetId`, `uploadUrl`, `method` and `headers`. PUT the raw bytes to `uploadUrl`
   with **exactly** those headers:

   ```bash
   curl -sS -X PUT "$UPLOAD_URL" \
     -H "Content-Type: image/jpeg" \
     -H "Content-Length: 248193" \
     --data-binary @product.jpg
   ```

   Both are signed into the URL: `image/jpeg; charset=utf-8` is a `403`, and so is a
   `Content-Length` that does not match the bytes. Measure `sizeBytes`, do not estimate it.

3. **A still you generated is already an asset — do not upload it again.** `POST /v1/images`
   returns `assetId` beside `url` on every image (deployed spec `2.11.0`). Pass that id
   straight into `referenceAssetIds` or `startImageAssetId`. Downloading the bytes and
   pushing them back through `POST /v1/uploads` mints a **second** asset and throws away the
   anchor the rest of the workflow is pinned to. The `url` expires in 3600 seconds; the
   `assetId` does not — chain from the id, never from the URL.

4. **Keep the `assetId`.** It is durable across calls, models and sessions — the whole
   series, the mini draft and the final render all reuse it. The presigned *upload URL*
   expires in 900 seconds; the id does not.

5. If a reference's longest side is under 1024 px, upscale with Lanczos to 1080 px on the
   long side and re-encode as RGB JPEG at quality 90–95. (No minimum is documented for this
   API; the practice carries over from a sibling API and is unverified here.)

**The source ad: upload it to READ it, never to RENDER from it.**

`POST /v1/uploads` takes video, and step 2 uses that on purpose — the source is uploaded so
`POST /v1/transcripts` can read its words. That is the whole extent of it. **The source's
`assetId` must never appear in `referenceAssetIds`, in `startImageAssetId`, or in any other
generation input.** It is input to your eyes and to the transcriber; it is never input to
the model that renders.

This is not a convention you have to remember — the API enforces it before any
charge. A source video's id in `referenceAssetIds` comes back:

```
400 invalid_input — referenceAssetIds accepts image uploads only; <id> is not one.
                    Video and audio references are not available on this endpoint.
```

`referenceAssetIds` takes **images only**: `image/jpeg`, `image/png`, `image/webp`. Since API 2.35.0
the Seedance variants take mp4 and mp3 references in their own fields (`referenceVideoAssetIds`, `referenceAudioAssetIds`; see novoads-api), and there the same `400`'s hint points at those two fields instead of the second line above; either way, a clone here is never built by feeding the original in.
What carries a source's style into a clone is your reading of it, written into the prompt.

### Step 11: Generate

```bash
curl -sS -X POST https://api.novoads.ai/v1/videos \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2.0",
    "prompt": "<the adapted prompt>",
    "durationSeconds": 14,
    "aspectRatio": "9:16",
    "language": "en",
    "referenceAssetIds": ["<product assetId>"],
    "productId": "<uuid>"
  }'
```

`startImageAssetId` instead of `referenceAssetIds` when that is the mode. Never both.

- Returns `202` with `jobId`, `status`, `creditsCharged` and `model`. **No `warnings` here** —
  but the **estimate does** return them (verified live 2026-08-05). Collect the craft advice at
  gate 2; there is no second chance at submit time.
- **Set `aspectRatio` and `durationSeconds` explicitly.** Seedance defaults to `16:9` and to
  5 seconds, and neither is what a cloned ad wants.
- **Carry `resolution` into this body whenever the estimate carried it.** The estimate
  priced the tier; this call is what renders it. Quote `1080p` at gate 2 and then omit the
  key here and the user approved one video and receives another — billed at the `720p`
  schedule, which is the quiet half of the same bug. `audioEnabled` is the mirror case: it
  belongs **only** here, because `POST /v1/estimates` refuses it.
- **The variation count came from step 5**, and by now it has been through gate 1 (step 7)
  and priced per variant (step 9). Do not ask again here, and do not fire a count the user
  has not approved a price for. Either kind is N calls and N charges — there is no batch
  parameter.
- **At most five in flight** across the organization, counting every clip and every
  variation. Fire five, then start the next as each reaches a terminal state.
- **Log each submission immediately** — one line appended to `logs/novoads-api.jsonl` with
  the timestamp, endpoint, model, `jobId`, `productId` and the request config: duration,
  aspect ratio, language, reference count, prompt **word count**. Never the prompt text,
  never the key, never a presigned URL. The log is observability, never a pricing source.

### Step 12: Poll, download, hand over

```bash
curl -sS https://api.novoads.ai/v1/generations/$JOB_ID \
  -H "Authorization: Bearer $NOVOADS_API_KEY"
```

- **Poll every 15 seconds until TERMINAL** — `succeeded`, `failed`, `blocked` or `canceled`
  — not until `succeeded`. A loop waiting only for success never returns on a job that
  already died. `queued` means charged and submitted but not yet rendering; it is normal.
- Tell the user the wait up front: `seedance-2.0` is usually **3 to 8 minutes**, most often
  around 5. `seedance-2.0-mini` is **2 to 3**.
- Update each job's log line with the terminal status and elapsed time, carrying `creditsCharged`
  over from the `202` — the poll response does **not** carry it. Never reconstruct it from a rate.

Download through `/watch`, which 302s to a URL signed at request time, so it never hands
you an expired link:

```bash
curl -sSL -o clone-01.mp4 https://api.novoads.ai/v1/generations/$JOB_ID/watch \
  -H "Authorization: Bearer $NOVOADS_API_KEY"
```

While the job is unfinished that endpoint is a `409` naming the current status.

Then:

1. Save under `outputs/<descriptive-subfolder>/` — `outputs/clone-northbrook-balm/`, not the
   job id — and name the files for what they are.
2. **Copy the source video in beside them**, as `source-<what-it-is>.mp4`. A copy, not a
   symlink and not the path it arrived on. A clone is only evidence next to the thing it
   cloned, and every other resting place for the source is temporary: `/tmp` is swept, a
   downloads folder is cleared, a competitor's URL rots. Measured 2026-08-06 — a finished
   three-variant run was reopened four days later with its three ads intact and its source
   gone, which left no way to show the clone had been faithful to anything.
3. **Transcribe every finished clip and diff it against the approved script.** (Doctrine: [shared/references/craft.md](../../shared/references/craft.md) § 1.) One
   `POST /v1/transcripts` per clip, 0.1 credits each, and it is the only thing that catches
   a spoken line that drifted. A reference image pins the **label**; nothing pins the
   **audio**, and the two fail independently. Measured 2026-08-06 across three clones of one
   source: the on-screen label was glyph-perfect in all three while the brand name was spoken
   as "Magnesium", "Magnesium" and "Magneum" — never once as written — and one clip swapped
   `L-theanine` for **`L-Thiamine`**, a different compound, in a script that had already
   passed the dialogue gate. Digits survived intact ("310 milligrams" rendered correctly).
   - **A coined or hyphenated brand name is the high-risk case**: the model resolves it to
     the nearest ordinary word. Spell it phonetically inside the quoted line and re-check.
   - Report the diff per clip. A clone that says the wrong brand name is a failed render
     even though the API returned `succeeded` and charged for it.
4. **Open the folder** so they can watch immediately: `open "<dir>"` on macOS, `xdg-open` on
   Linux, `explorer` on Windows. Try `open` first and fall back silently.
5. **Open the source video beside them**, then present the clones as a numbered list. The
   comparison that decides whether this worked is against the original, not among the
   variants — and after item 2 the source is sitting in the same folder.
6. For a series, present each clip, then offer to stitch with ffmpeg using **absolute
   paths**:

   ```bash
   printf "file '%s'\n" "$(pwd)/clip1.mp4" "$(pwd)/clip2.mp4" "$(pwd)/clip3.mp4" > /tmp/stitch-list.txt
   ffmpeg -y -f concat -safe 0 -i /tmp/stitch-list.txt -c copy stitched-clone.mp4
   ```

   Re-encode if the codecs differ. Hand back both the stitched file and the individual clips.
7. Report the total spend by summing the `creditsCharged` values the API returned — those,
   never a number you calculated from a rate.
8. If a job came back `failed` or `blocked`, say which and quote the `error` it carries.

Next steps worth offering: iterate the one beat that missed rather than re-firing the whole
set, hand the file to the `meta-ad-builder` skill to publish it as a Meta creative, or burn
captions on out of band with the `caption-video` skill — that one
makes no Novoads call and costs no credits.

## Seedance 2.0 constraints that bite during a clone

Full detail in [reference.md](../novoads-api/reference.md).

| Constraint | What it means here |
|---|---|
| `startImageAssetId` **XOR** `referenceAssetIds` | Separate modes on the model. A body with both is a `400` whose message says exactly that. Nothing is charged |
| `referenceAssetIds` ≤ **9**, images only | Ten is `Too big: expected array to have <=9 items`. A video asset id is refused here; from API 2.35.0 Seedance video and audio go in `referenceVideoAssetIds` and `referenceAudioAssetIds` |
| No `referenceVideos`, no `referenceAudios`, no `endFrame`, no `projectId` | All `400 Unrecognized key`. Nothing is charged, and no clone workflow can depend on them |
| `resolution` on **`seedance-2.0`**: `480p` `720p` `1080p` `4k`, default `720p` | Real, and re-verified against spec 2.12.0 (2026-08-06). **It multiplies the bill** — `1080p` ≈2.5x the base, `4k` ≈5x, and a series pays it per clip. Price the tier at `POST /v1/estimates`; `480p` is **≈half** the base since the 2026-08-07 reprice (measured live 2026-08-12), so it is a real draft tier. `400 Unrecognized key` on `sora-2` (and on `seedance-2.0-mini` and `veo-3.1` before API 2.34.0, which gives mini `480p`/`720p` and Veo `720p`/`1080p`: read `resolutions` from `GET /v1/models`), and a `400` on `omni-flash` wherever `GET /v1/models` lists only `720p` for it (where it lists more, Omni has its own tiers, `4k` included only when listed) |
| `audioEnabled` — **Seedance only**, optional, default `true` | Send `false` for a silent clone. `400 Unrecognized key` on the three non-Seedance video models, and on `POST /estimates` for every model |
| `durationSeconds` 4–15, integer | Out-of-grid values are rejected, never rounded. Default is **5** |
| `aspectRatio` `16:9` `9:16` `1:1` `4:3` `3:4` `21:9` | Default is **`16:9`**. Set it, or a vertical clone ships landscape |
| Prompt within the model's cap | Enforced on the estimate too, against whichever `model` you name |
| Audio is rendered from the prompt | The spoken line is lip-synced in this same call at no extra cost, which is why gate 1 exists. `audioEnabled: false` mutes the render; it does not give you a separate audio track to direct |
| Prompt rules are advisory and live on `/estimates` only | The estimate returns a `warnings` array of `{rule, message}` craft advice; `POST /videos` does not. None of it can refuse or reprice a call, so a weak prompt still renders and bills exactly like a strong one. The warnings are substring matches and **do false-positive** — read them, judge each against the prompt, and say so when you override one |
| Moderation is `422 content_policy` | The only refusal of a prompt for what it says, and the estimate skips it, so a clean quote can still be blocked. **Nothing is charged** |
| Five generations in flight per organization | A sixth is `429` with `details.reason: concurrency_limit`. Wait for a slot; backing off harder does nothing |
| No idempotency keys | Which is why a 500 is never blindly retried — see below |

## Error recovery

Branch on `error.code`, never on the message. Every error is
`{"error":{"code":…,"message":…,"requestId":…,"details":…}}`, and `requestId` is what to
quote when reporting a problem.

| Status / code | What happened | What to do |
|---|---|---|
| `400 invalid_input` | The request is **malformed** — an unknown key, an out-of-grid duration, a prompt over the model's ceiling. `details.issues` names each bad field. Never a judgement on the writing | Fix the field. Nothing was charged. Do not go looking for a prompt rule: none of them can 400 |
| `400` naming the two modes | `startImageAssetId` and `referenceAssetIds` were both sent | Pick one. Start frame to animate a photo, references to composite a scene |
| `401 unauthorized` | Missing, malformed or revoked key | `./scripts/check-novoads-env.sh`, then a new key at <https://novoads.ai/dashboard/settings?tab=api> |
| `402 insufficient_credits` | `details` carries `required` and `available` | Tell the user the gap. Do not retry |
| `403 forbidden` | `details.reason` is `plan_required` or `subscription_inactive` — the key is fine, the plan is not | Say which one it is; they are different fixes |
| `409 conflict` | `/watch` on a job that has not finished | Keep polling |
| `422 content_policy` | Moderation blocked the prompt. Nothing was charged | Rewrite the flagged idea or stop. Do not resend the same payload |
| `429 rate_limited` | Four causes; branch on `details.reason` | `concurrency_limit` → wait for a slot. `key_limit` (60/min) and `organization_limit` (180/min) → honour `Retry-After`. `client_limit` → pre-auth ceiling |
| `500 internal_error` | Possibly charged | **Do not retry blindly.** `GET /v1/generations` first: if the job is there, poll it instead of resubmitting |
| `502 provider_failed` | The model provider failed | Credits are refunded automatically |
| Job `status: failed` or `blocked` | Read the `error` on the job | If it is content-related, rewrite. If it is a provider failure, credits are already refunded |
| The clone looks nothing like the source | The reading was wrong, not the render | Go back to the beat map with the user before spending again. Change **one** element per iteration — framing, or pacing, or the anchor — never three |
| The label came back garbled | Seedance preserves logos and destroys printed text | Say in the prompt that the label stays sharp and unchanged, and check the reference photo actually shows it sharp |
| The clip **says** the wrong brand name | The reference image pinned the label, not the voice. There is no audio equivalent of a reference asset, so a coined name resolves to the nearest ordinary word — and the render still returns `succeeded` and still charges | Catch it with the transcript diff in step 12.3, never by ear on one playback. Respell the name phonetically inside the quoted line and re-render that clip only. The label being perfect tells you nothing about the audio |
| Source longer than 15s | Not a failure | Present the two routes from step 5 and let the user pick. Do not split on your own initiative |

## Related files

The formula library and the API contract are listed once, in **Read order** at the top — this
section does not repeat them. What is only here:

- [analyze-video/SKILL.md](../analyze-video/SKILL.md) — the template-making cousin: same
  analysis, output is a reusable formula instead of a video.
- [analyze-video/scripts/extract-frames.sh](../analyze-video/scripts/extract-frames.sh) —
  frame and audio extraction, shared by both.
- [novoads-api/reference.md](../novoads-api/reference.md) — every endpoint, field, limit and
  error code. A lookup, not a read-through.
