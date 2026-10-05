---
name: seedance-anime-drama
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Turn a novel/script excerpt into an anime-style storyboard shot using the Ofox image and video APIs. Runs a short creative brief first (how many shots, the aspect ratio before any image exists, which animation look; "Let the AI decide" is offered on the taste questions, never on a must-ask one, and never as the default), generates the character with ofox-image-core — one opening frame for a single shot, a design sheet to confirm plus one opening frame per shot for a sequence — then feeds each frame to ofox-video-core as `--frame-first-image`, so every shot starts on an image of that character rather than on a text description alone. Use when a user asks to turn a story excerpt into an anime video, e.g. "turn this novel excerpt into an anime video", "make an anime-style storyboard clip of this scene", "generate a manga-drama shot with this character", or "turn this chapter into an anime short with the same character in every shot". Do not use for realistic-human dialogue scenes with no anime styling (see seedance-short-drama), silent product/brand shots (see seedance-ad-creative), or plain catalog footage (see seedance-product-video).
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-anime-drama
metadata:
  author: ofoxai
  version: "2.0.1"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🎨"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-anime-drama
---

# seedance-anime-drama: anime storyboard shots with image-based character consistency

Turns one shot — or a short sequence — of a novel/script excerpt into an
anime-style video clip, using an image of the character as the frame each
shot starts from, not just a repeated text description.

This is the first scenario skill in this repo that orchestrates **two**
execution-layer skills rather than one:

1. [`ofox-image-core`](../ofox-image-core/SKILL.md) generates the character
   as an image (text-to-image).
2. [`ofox-video-core`](../ofox-video-core/SKILL.md) generates each shot,
   with that image passed in as `--frame-first-image`.

Neither core skill's request-building, error-mapping, or download/reporting
logic is duplicated here — this skill owns only the anime-specific prompt
craft, the pre-generation brief, the two-step orchestration order, and the
two approvals. **Read both core skills' safety contracts before using this
one** — neither is restated here.

Three shared references from `ofox-video-core` are load-bearing and are
linked, not copied:

- [`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md)
  — what to ask the user before a prompt exists: the three tiers, one round of
  at most four questions, the "Let the AI decide" discipline, the skip rows,
  and the anti-patterns. Read it before the brief section below, which adds
  this scenario's question set and the one axis a two-phase flow must settle
  before the first image is paid for.
- [`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)
  — the vendor's formula, the header-manifest → timeline → closing-block
  skeleton, timestamp formats and segment lengths, transition and camera
  vocabularies, consistency locks and negative lists, the two meanings of an
  attached image, endings. Load it before writing a prompt; this file adds
  only what is specific to anime.
- [`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
  — never spend before an approved cost table; this skill is its two-phase
  example.

## The mechanism — the whole point of this skill

The character exists as an image before any video is paid for, and every
shot **starts on an image of that character** (`--frame-first-image`) rather
than on a description the model interprets fresh each time. That is what
separates this skill from `seedance-short-drama`'s text-only consistency —
and it is available here because an anime character is not a photoreal
person, so Seedance 2.5's real-person refusal does not apply.

How many images that means depends on the shot count (the brief's first
question, and Step 1):

- **one shot** — one opening frame, fed to that shot;
- **several shots continuing one moment** — one opening frame for the first
  shot, then `chain` carries each job's closing frame into the next;
- **several shots cutting to new setups** — one opening frame per shot,
  written from the same character description word for word, each fed to its
  own shot; by default a design sheet comes first and is shown to the user to
  confirm the design (the brief's `Sheet` question can skip it). The sheet
  itself never goes to `--frame-first-image` (see "Two different images, do
  not confuse them").

A second, different way for an image to enter a shot — as an identity
reference that locks no frame (`input_references`) — is described under "Two
ways an image can enter a shot". The two are mutually exclusive per job.

## Where the two core skills live

This skill reaches **two** execution layers, so resolve both once, before the
first call:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/ofox-video.sh" ] && echo "$d" && break
done

for d in ../ofox-image-core \
         ../ofoxai-skills-ofox-image-core \
         ~/.agents/skills/ofox-image-core \
         ~/.agents/skills/ofoxai-skills-ofox-image-core \
         ~/.claude/skills/ofox-image-core; do
  [ -f "$d/references/ofox-image.sh" ] && echo "$d" && break
done
```

Examples below are written as `../ofox-video-core/...` and
`../ofox-image-core/...` (the skills.sh / ClawHub / `npx ofox-skills` layout,
where a skill's directory is named after the skill). If either probe found a
different directory — LobeHub unpacks each skill as `ofoxai-skills-<name>`,
so the siblings there are `ofoxai-skills-ofox-video-core` and
`ofoxai-skills-ofox-image-core` — substitute it, in the `ofox-video.sh` /
`ofox-image.sh` commands and in the `references/*.md` links alike. The two
resolve independently; one landing in a different place says nothing about
the other.

Either probe printing nothing → that core isn't installed, and Step 1 needs
`ofox-image-core` as surely as Step 2 needs `ofox-video-core`; see "If the
script isn't found".

**Step 2 needs `ofox-video-core` 2.0.0 or newer.** From that version the
billable subcommands refuse to run without `--approved`, and every real-run
`ofox-video.sh` command below passes it. An older core does not know the flag
and stops with `unknown option '--approved'` before any request — nothing is
submitted and nothing is billed, so the fix is to update the core, never to
drop the flag. Step 1's `ofox-image.sh` has no equivalent flag; the spend rule
binds there in exactly the same way, only the reminder is missing.

## Before generating: two availability checks

Run each once per session (not on every request):

```bash
bash ../ofox-image-core/references/ofox-image.sh check
bash ../ofox-video-core/references/ofox-video.sh check
```

If either fails, follow that core skill's own guidance (install `curl`/`jq`,
or get an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the
conversation, and don't re-run either check on every subsequent request once
both have passed.

## Shots, cuts and jobs

One job is one clip of 4–30 seconds, and a clip **can hold several shots
joined by hard cuts**. The gallery's animation prompts do this routinely —
case 11 asks for ten shots in 24s, case 18 for eight segments in 30s,
official case 29 for four shots in 15s. Write the timestamps as cut
boundaries and keep **2–5 seconds per shot**.

The measured envelope is **up to 10 shots in 30 seconds**, and separately
**up to 6 hard cuts** among one job's boundaries, at 480p and 720p, with cuts
landing within about ±1.5 seconds of their stamps. Job ids and the frame-by-frame readings are
under "Several shots in one job" in
`../ofox-video-core/references/prompt-structure.md`.

The item that used to matter most here is now closed: **a multi-cut job
that also carries a `--frame-first-image` — this skill's normal shape — has
been run twice**, at 15s/5 shots/4 cuts and 20s/7 shots/6 cuts (jobs
`7ae7d49e-7eb9-4165-9d95-09cd525d53ed` and
`ac927785-92ef-4e28-97b9-ff8172ec5554`, both `seedance-ad-creative` product
clips). Every cut happened *and* the attached frame held across all of them,
so the two do not trade off. What still has no measurement in this skill's
own shape is a multi-cut job on an **anime** frame — the frame-lock run here
was a single continuous take (`16023efe-48d6-45fe-8fd8-f5c6fbfe6519`) — but
the mechanism is the same, and the remaining gap is the art style, not the
cutting. Past 10 shots or 6 hard cuts, or at 1080p, treat a first attempt as
an experiment and price it as one.

One warning that comes with the one-take run: `16023efe` was rejected for
being static — a 20-second single take whose only movement was a very slow
push. If you pick one shot, make the camera **cross space**; the measurement
is under "Shot density, measured per case" in the shared file.

Three ways to lay a sequence out, and they compose:

| Route | What it gives | When |
|---|---|---|
| **Timestamped shots inside one job** | several cuts; one approval; one bill | the sequence fits in 30s and one seed and resolution suit every shot |
| **`chain`** (`ofox-video-core`) | each job's closing frame becomes the next job's opening frame; the results are joined into one file | consecutive shots that continue one moment; sequences past 30s; each shot priced and approved on its own |
| **Separate `generate` calls** | independent jobs | shots that cut to unrelated setups, each started from its own opening frame (Step 1) |

`chain` works in this scenario, and that is not a given: Seedance 2.5
image-to-video refuses frames containing a real person, so a live-action
sequence cannot be chained, but an anime character is not a photoreal person.
Continuity is strong on the run `ofox-video-core` recorded — the next shot
opens on very nearly the frame it was fed, then follows its own prompt (that
run was a static object, not a character).

Shot count is the user's call, not the skill's — it is the brief's must-ask
question, because it decides how many images and how many approvals follow.

## Before writing the prompt: the creative brief

The shared rules are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md)
— the three tiers, the one-round limit, the shape of a question, the "Let the
AI decide" discipline, the generic skip rows, the order with the approval
gate, the fallback for a runtime without `AskUserQuestion`, and the
anti-patterns. Read it before writing a prompt. This section adds only what
is specific to anime — including this scenario's instance of the shared
file's last anti-pattern, an axis a paid step freezes: **the aspect ratio has
to be settled before the image is paid for.**

Read the user's message and attachments first, and mark every axis of the
clip **settled** or **open**. Zero questions is common here: "just this one
shot, 9:16, in a 90s hand-drawn look, keep her lines" has settled every axis
— write the prompt.

| Tier | Anime axes |
|---|---|
| **must-ask** | how many shots this round; the aspect ratio **before** any image exists (the clip's shape follows the image); whether a character image the request implies actually exists |
| **ask-if-open** | the animation look; dialogue or no dialogue |
| **never-ask** | resolution, video model, image model, provider, duration once stated. For the **video** model specifically, never-ask means the agent doesn't raise it proactively — it does **not** mean overriding an explicit choice: if the user names a video model for Step 2 (an id, or a shorthand like "wan"/"hailuo"), that model is used instead of the `seedance-2.5` default. See "Choosing a video model" below. (Step 1's image model is a separate, unrelated choice and is unaffected.) |

### The anime questions

| # | Tier | Header | Question | Options — first is recommended; "Let the AI decide" comes last wherever it appears, and never on a must-ask row | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Shots` | How many shots this round? Each shot is a video job, and several shots also mean several opening frames. | `One shot first (recommended)` — see the character move before committing to a sequence / `<N> shots` — one row per shot in Approval 2; timestamped inside one job when they fit in 30s, otherwise `chain` or separate jobs / `Not sure — propose one` — the agent names N with the per-shot price and says why. **This is not a "Let the AI decide" option**: a must-ask axis never gets one, and the proposed count is only settled by the user's yes on Approval 2's rows | No shot count in the input. "Just this one shot" / "these three beats": skip. |
| 2 | must-ask | `Aspect` | The clip's shape follows the image (adaptive), so the image has to be made at the target ratio. Where will it be watched? | `9:16 vertical (recommended)` — mobile feeds / `16:9 landscape` — web, YouTube; the gallery's anime cases that state a ratio are 16:9 (cases 9, 18, 44) / `1:1 square` — grid feeds | No platform word and no ratio. **Before Approval 1**, and with **no "Let the AI decide"** — this is the axis a paid image freezes, so it is the one thing a blanket "you decide" does not cover. If the user still declines to choose, take 9:16, mark it `(AI's pick)` in the recap, and say in the same message that changing it later means paying for a second image. |
| 3 | ask-if-open | `Style` | Which animation look? It goes into the image and into every shot. | `Modern theatrical cel-shaded (recommended)` — clean line, flat vibrant colour, soft glow; the safest match for a contemporary excerpt, and the closest to the gallery's cel-shaded hybrid (case 18) / `Hand-drawn 90s TV anime` — fine ink lines, dramatic shadow, soft VHS grain, teal-and-orange (case 61) / `3D-stylised anime` — rounded appealing designs, sparkle and particle glow (case 10); swap in `Pixel 8-bit` (case 29) or `American retro cartoon, halftone dots` (case 11) when the story suggests it / `Let the AI decide` | No style word in the input. No school dominates the gallery — the recommendation is a convention, not a measured winner. |
| 4 | follow-up | `Sheet` | Several shots — confirm the design on a sheet before the opening frames? | `Sheet first (recommended)` — one extra image; catches a wrong design before N frames and N shots are paid / `Straight to shot 1's opening frame` — later frames copy its description word for word / `I have a character image` — give the path | Only when Q1 answered several shots. |
| 5 | ask-if-open | `Sound` | Lines, or ambience only? | `Dialogue in the excerpt's language (recommended)` / `No dialogue` — ambience and keyed sound effects, with any score added afterwards in an editor / `Let the AI decide`. Neither option asks the model to generate music: that has failed output moderation on audio copyright here (unbilled) | Only when the excerpt is narration without quoted speech. Quoted lines present: dialogue on, no question. |

If more than four are open, ask `Shots`, `Aspect`, `Style`, `Sound`; `Sheet`
is the follow-up. Never asked: the language of the lines, resolution, video
or image model, provider — all rows in the tables.

### Skip rows specific to anime

On top of the generic rows in `creative-brief.md`:

| Signal in the input | Axis | Value |
|---|---|---|
| A style word — "90s anime", "like Ghibli", "pixel", "Saturday-morning cartoon", "cel-shaded" | style | map to the nearest school in the `Style` options; do not ask |
| Quoted speech in the excerpt | sound | dialogue on, in the excerpt's language — the language is **never asked**; see "Prompt language follows the audio" |
| A character image attached | asset question | settled: skip the sheet, the image is the design; see "Two ways an image can enter a shot" for which route it takes |

### Every answer lands somewhere

| Answer | Where it goes |
|---|---|
| Shots | the number of video jobs and of rows in Approval 2; whether a sheet is generated |
| Aspect | the image is generated (or cropped/padded) at that ratio; the video inherits it through `adaptive` |
| Style | the style sandwich — first sentence, `STYLE` block, closing quality line — in the image prompt **and** every shot prompt |
| Sheet | the shape of Step 1: sheet first, or straight to shot 1's opening frame |
| Sound | the `AUDIO` block, and `--generate-audio` |

### Where the brief sits in the two-phase flow

This scenario pays twice, so the shared order runs once per phase:

```
read input → fill the brief → [open axes] one AskUserQuestion (Shots, Aspect, Style, Sound)
→ [Shots = several] one follow-up (Sheet)
→ write the image prompt → image --dry-run
→ one message: brief recap (AI's picks and inferred values marked) + image prompt + Approval 1 table, with the phase-2 preview
→ wait for an explicit yes → generate the image → show IMAGE_PATH
     (the second participation point: the user may send the design back here — that is a revision, not a new question round)
→ write the shot prompt → video --dry-run
→ one message: recap carried over + full shot prompt + Approval 2 table
→ wait for an explicit yes → generate → report the real bill
```

Everything that must be settled before an image exists — **aspect ratio**,
style, shot count — is asked before Approval 1; the ratio is must-ask for a
mechanical reason, not a matter of taste ("The opening frame decides the
output's shape"). Nothing is asked between Approval 1 and the image; the
image itself is the question.

The recap, in the same message as the table:

```
Brief
- Shots: one shot first (your choice)
- Aspect: 9:16 (inferred from "for Reels") — the image will be generated at 9:16
- Style: hand-drawn 90s TV anime, fine ink lines, soft VHS grain (AI's pick)
- Sound: dialogue in Japanese, as written in the excerpt (inferred from the quoted lines)
- Image: quality high, chain default model — row 1; video 8s 720p — row 2 (defaults)
```

## Prompt template

Load these sections of `../ofox-video-core/references/prompt-structure.md`
first: "Prompt skeleton: header manifest, timeline, closing block",
"Segmenting the timeline", "Transitions", "Camera language", "Pacing",
"Consistency locks and the negative list", "Dialogue and sound", "Reference
assets as visual anchors", "Endings". The vocabulary lives there and is not
repeated. What follows is the anime shape laid over that skeleton.

Four subsections in those pages carry most of what makes a fight or an action
beat read, and all four are measured on this skill's own jobs: **"The cause
chain"** (inside "Segmenting the timeline"), **"Rules that travel with the
vocabulary"** (inside "Camera language"), **"What a prohibition cannot buy:
timing and behaviour"**, and **"The plastic look is designed out, not
forbidden"** (the last two both inside "Consistency locks and the negative
list"). The plastic-look one matters here even though nothing in this scenario
is photoreal — for animation the plastic read is the 3D-CG read, and the positive
form is drawing vocabulary rather than a longer `AVOID` list.

Gallery evidence for the shape: all eight animation-adjacent prompts (cases
9, 10, 11, 18, 29, 44, 61, 63) name their style school in the first sentence;
five of the eight are timestamped; seven carry a negative list; the two fight
scenes (11, 44) share a cause-chain rule; four layer an analogue texture (VHS
grain, 35mm colours, 90s imperfections) over the school. Case 44 is in that
set for its continuity and cause-chain writing, not its look — it asks for
live action and forbids 3D and game CG outright. Chinese-language cases are
quoted in translation.

### 15–30 seconds: a manifest and timestamped segments

Slots in `<angle brackets>`; optional lines in `[square brackets]`. Two to
five seconds per shot for action, six to nine for a held emotional beat. As a
count rather than a length: this category's densest collected prompt is case
11 at **10 shots in 24 seconds** (2.4s each), case 18 runs 8 in 30s, and case
9's shot chain is six sizes in 30s — while the worked example below, adapted
from case 10, is the quiet end at four segments in 30s. Both ends are real;
the per-case measurements are in "Shot density, measured per case" in the
shared file. An action or fight beat written as four 7-second segments is
below every action prompt in the gallery.

```
[FORMAT: <ratio>, <T> seconds, <N shots, hard cuts on the timestamps | one continuous shot>]      — optional; must match the flags
STYLE: <school: cel-shaded modern theatrical anime | hand-drawn 90s TV anime, fine ink lines | 3D-stylised anime, rounded appealing designs | pixel 8-bit | 1969 American TV cartoon, thick outlines, halftone dots>, <texture layer: soft VHS grain | faded 35mm colours, gate weave | none>, <light: golden hour | neon | teal-and-orange | flat overcast>.
[@image1 supplies <tag>'s identity only: face, <hair>, <signature accessory>, <outfit>; ignore its background and pose.]      — identity-reference route only; omit when the shot starts on a frame
<TAG>: <age range, build>, <eyes>, <hair colour + style + signature accessory>, <clothing item by item, colours>, <bearing>. Referred to as "<tag>".
SCENE: <place, time, weather, light, palette>.
[CONTINUITY (sequel): the same <tag> as in PART 1. The first frame continues PART 1's final image exactly: <position, pose, action in progress>. No re-positioning, no re-facing, no slow preparation — the action continues on frame one.]
RULES — action: each shot is one continuous camera take, no jump to a new position inside a shot. Every strike runs visible target → body entry → strike motion → clear contact → immediate body reaction → balance change → next action; no reaction before contact; no effects in place of body motion. Effects allowed: SPEED LINES, SMEAR FRAME, IMPACT BURST, SHOCKWAVE RING, WOBBLE LINES — sparingly, only on <the decisive hits>. Onomatopoeia allowed: THWACK! POW! WHAM! — only on those.
RULES — quiet: one action per segment, long enough to read. No fast cutting, no time-lapse, no jump cuts.

[<segment title>, 0–<a>s] <shot size, camera position, movement>. <tag> <action A → B → C>. <the environment answers: petals lift, the light brightens>. [<Tag>: "<line>"]
<TRANSITION — name a kind on purpose; a hard cut is one of nine, and an unnamed boundary becomes one by default: HARD CUT. | Without cutting, <a sleeve / a banner / a passing body> sweeps across the lens and the camera comes out of the occlusion on <the next view>. | Without cutting, the camera pushes through <the doorway / the torii / the gap in the hedge> into <the next space>. | <an element inside the frame moves and carries the change — case 29's four shots inside one declared continuous take>. | <a speed ramp past the lens into the next beat — case 11>. | Without cutting, …>
[<segment title>, <a>–<b>s] … (each segment raises the stakes or the feeling one step)
[Ending, <x>–<T>s] <terminal pose: faces the lens | freeze | slow pull-back to a wide | arm raised>; hold one second.

AUDIO: <ambience> / <character sounds with a qualifier: laughter (pure joy, not mocking)> / <keyed sfx> / <what remains at the end> — or: No BGM, no narration, no subtitles. <Music only if the user accepts the risk: a prompt asking the model for a scored cue has failed `output_moderation_failed` on audio copyright, unbilled — see "Asking for music can fail output moderation on copyright" in the shared file.>
CONSISTENCY: <tag>'s face, facial proportions, skin tone, body type, hairstyle and colour, <accessory>, <clothing items> identical in every shot; strictly no random character changes; never change the visual style.
AVOID: subtitles, watermarks, logos; fast cutting and jump cuts (quiet scenes); photorealism, 3D game CG, plastic skin <or whichever school you are not making>; identity drift.
<Closing quality line: restate the school, expressive facial animation, <camera texture>, character design consistent throughout.>
```

What each anime slot is for, and where it comes from:

| Slot | Why it is here | Cases |
|---|---|---|
| **Style sandwich** — school in the first sentence, a `STYLE` block mid-prompt, a quality line at the end | All eight open with their school; 9, 18, 61 and 29 close by restating it | 9, 10, 18, 61, 29 |
| **The schools seen** (the `Style` question's vocabulary) | `dreamlike cinematic anime aesthetic … anime 3D-stylised (rounded, appealing designs)` · `modern retro-anime 3D cel-shaded hybrid … soft VHS grain, synthwave colour glow` · `hand-drawn Japanese anime, highly detailed ink lines, expressive eyes, dramatic shadows … the slight imperfections of 1990s animation` · `pixel wuxia, 8-bit` · `hand-drawn 2D character inspired by 1969 American TV cartoons … thick black outlines, halftone dots, print misregistration` · `painterly anime illustration, cel-and-gradient shading` | 10, 18, 61, 29, 11, 34 |
| **Cause chain** (action) | The chain itself, its two attached prohibitions, and a frame-by-frame reading of it landing on a real job now live in **"The cause chain: ordering what happens inside a segment"** in `../ofox-video-core/references/prompt-structure.md` — load it rather than re-deriving it here. Its short form: `visible target → body entry → real strike motion → clear contact → immediate body reaction → balance change → next action` | 44, 11; measured on `c192dbe6` |
| **Escalation curve** | each segment title raises the stakes (`REDIRECT → RUSH → PRESSURE WAVE → VORTEX BREAK → HYDRO DRILL → MAXIMUM FINISH`); `reactions grow louder after major punches`; the heaviest effects only on the decisive blow | 44, 11 |
| **Effects allow-list with a frequency rule** | `SPEED LINES, SMEAR FRAME, IMPACT BURST, IMPACT FLASH, SHOCKWAVE RING, WOBBLE LINES — use effects sparingly`; onomatopoeia `THWACK! POW! SMACK! WHAM! CRACK!` | 11 |
| **Terminal pose** | the referee raises the arm; faces the lens, serious and resolute; freeze; slow pull-back showing how small she is | 11, 9, 10, 29 |
| **Environment answers the emotion** (quiet scenes) | `the garden responds to her joy — the flowers glow brighter` | 10 |
| **One action per segment** (quiet and process scenes) | `Show only one salon action at a time … No fast cutting. No time-lapse. No jump cuts.` | 18 |
| **Consistency sentence with invariants** | `face, facial proportions, skin tone, body type, hairstyle, hair colour, all visible accessories, clothing`; `strictly no random character changes`; `keep the stylist and the customer consistent throughout` | 44, 61, 18 |
| **Sequel block** | `must be the same … continuing the fight from PART 1`; PART 1's final frame re-described in words as this clip's first; `no re-positioning, no re-facing, no slow preparation` — the text-level complement to `chain` across sessions | 44 |
| **`AUDIO` block** | itemised: ambience / character sounds with a qualifier / keyed sfx / what remains at the end; or `No BGM, no narration, no subtitles`. The gallery's music lines (case 10's music box, case 11's score) are the one part not to copy — an ad prompt asking for a cello note and a bell chime failed output moderation on audio copyright here, unbilled | 10, 44, 11 |
| **`AVOID`** | subtitles, watermarks, logos; fast cutting, jump cuts; `never make him realistic`, `no face swap, no AI plastic skin, no 3D, no game CG`; random character changes | 18, 44, 61, 11 |

### Choosing a transition, not defaulting to a cut

The shared "Transitions" section holds **nine** kinds with the phrasing to
copy for each: hard cut; one continuous shot with cuts forbidden; occlusion;
pass-through; morph; flash; match cut; speed ramp; narrative ordering words.
Load it and pick one per boundary — animation is the category where the
in-frame options are cheapest, because nothing has to stay photoreal across
the change.

| Kind | Animation-adjacent cases |
|---|---|
| Hard cut | 18 (eight timestamped segments, while forbidding *fast* cutting and jump cuts), 11 (ten numbered shots), 63 (four scene stamps in about 8s) |
| One continuous shot, cuts forbidden | 29 (four shots declared as one continuous take), 44 (`no jump cuts, no flicker`) |
| Speed ramp | 11 (`Return to normal speed as the human staggers backward`) |
| Narrative ordering words | 9 (`close-up → medium → tracking shot → low-angle foot shot → corridor wide → close-up`) |
| Morph | 54, 13 — outside this category, but the mechanism is case 29's in-frame element move |

Occlusion, pass-through, flash and match cut have no animation instance among
the 63; borrowing one is a deliberate choice rather than a documented
convention, and the phrasing to borrow is in the shared table.

### Worked example — adapted from case 10 (translated): 30 seconds, four segments, no dialogue

Case 10's own sound design is a music-box melody with strings and bells. This
version keeps everything else and replaces the scored cue with diegetic sound
only, because asking this model for music has failed output moderation on
audio copyright here (unbilled; shared file, "Asking for music can fail
output moderation on copyright"). A score can be laid over the delivered clip
afterwards, which is where case 10's melody would have to come from anyway.

```
STYLE: dreamlike cinematic anime, 3D-stylised with rounded, appealing designs; continuous sparkle and magic particles; golden-hour light, warm palette, bright cheerful colour.
THE GIRL: early teens, small and light; large round amber eyes, a soft round face; chestnut hair in two low bunches tied with pale-yellow ribbons; a cream sundress with a sky-blue sash; open, delighted. Referred to as "the girl".
SCENE: a magic garden at golden hour — tall glowing flowers, drifting motes of light, soft grass, a distant hedge in haze.
RULES — quiet: one action per segment, long enough to read. No fast cutting, no time-lapse, no jump cuts. Single character, no dialogue.

[Opening, 0–6s] Wide shot of the garden, light motes hanging in the air. The girl sits alone on the grass, looks up at the sky, and a bright smile breaks. The camera slowly orbits her.
[Delight, 6–15s] Medium shot. She springs up and turns once with her arms out; the garden answers — the flowers glow brighter, petals lift and circle her. She laughs (pure joy, not mocking; subtle, not over the top). The camera follows her.
[Wonder, 15–24s] Close-up. A small glowing bird lands on her fingertip; she goes still, eyes wide, then breathes out a smile. Behind her the light deepens toward gold. The camera drifts in a few centimetres.
[Ending, 24–30s] The camera pulls back slowly, showing how small she is in the vast garden. Freeze on this moment of quiet joy.

AUDIO: petals rustling, grass under her feet, a faint chime as the flowers brighten / her laughter (pure joy) / the bird's small trill and wingbeat / at the end only a light breeze remains. No music, no score, no instruments, no humming, no singing.
CONSISTENCY: the girl's face, proportions, skin tone, hair bunches and ribbons, cream sundress and blue sash identical in every segment; strictly no random character changes; never change the visual style.
AVOID: subtitles, watermarks, logos; fast cutting, jump cuts; photorealism, game CG, plastic skin; identity drift.
Dreamlike cinematic anime, expressive facial animation, soft cinematic depth of field, character design consistent throughout.
```

### 8–15 seconds: one shot, starting on the frame

This is the prompt that goes with `--frame-first-image`: it opens **on the
image**, so the first sentence says so and the character block can be short —
the frame carries the design. No manifest; the vendor's formula order in
three or four sentences, and a `one shot` declaration so any beats read as
performance, not cuts.

```
Start exactly on the opening frame. <Tag>, <appearance in one clause>, <place and light>. <School>, <texture layer>.
One shot, <T> seconds. <Shot size and movement>. <Tag> <action A → B → C>; <the environment answers>. [<Tag>: "<line>" — <delivery>.]
<Ending: faces the lens | freeze | the camera settles>; hold one second.
AUDIO: <ambience> / <keyed sfx> / <what remains at the end> — no music, no score, no instruments. CONSISTENCY: <tag>'s face, hair, <accessory>, <outfit> unchanged. AVOID: subtitles, watermarks; <the school you are not making>; identity drift.
```

Adapted from case 10's opening (translated), 8 seconds, from an opening frame
of the girl on the grass:

```
Start exactly on the opening frame. The girl — chestnut hair in two low bunches with pale-yellow ribbons, cream sundress, blue sash — sits alone on the grass of a magic garden at golden hour, light motes drifting. Dreamlike cinematic anime, 3D-stylised, rounded appealing designs, soft glow.
One shot, 8 seconds. Wide shot; the camera slowly orbits her a quarter turn. She looks up at the sky, a bright smile breaks, and the nearest flowers glow brighter in answer; two petals lift and drift past the lens.
The camera settles as the smile holds; hold one second.
AUDIO: petals rustling, grass shifting, a faint chime as the flowers brighten / no dialogue / no music, no score, no instruments. CONSISTENCY: her face, hair bunches, ribbons, sundress and sash unchanged. AVOID: subtitles, watermarks; photorealism, game CG; identity drift.
```

## Step 1: generate the image the shot will actually start from

Extracting the character description is **this skill's calling agent's own
reasoning to do — not something a script performs**. Read the user's
story/script excerpt and write a precise, reusable character description
covering:

- age and build
- hair (colour, length, style) and one signature accessory
- clothing (exact garments, colours)
- distinguishing features (scars, eye colour, etc.)

Carry the brief's `Style` answer — the school, its texture layer, its light —
into **this** prompt and into every shot prompt, so the image and the shots
stay consistent with each other, not just shot to shot.

### Two different images, do not confuse them

`--frame-first-image` is the **literal first frame of the video**, not a
style hint. That makes the classic "character reference sheet" the wrong
thing to feed it:

| Image | What it is for | Prompt shape |
|---|---|---|
| **Character sheet** | Locking a design and showing it to the user before several shots are paid for | multi-view, labels, plain background |
| **Opening frame** | The frame the shot animates away from | one in-scene illustration, no text, no panels |

Asking for a "character reference sheet" gets you exactly that: a real
multi-panel sheet with front/side/back views, an expression row, a palette
swatch and printed labels — and models will happily invent a name and letter
it across the top. Fed to `--frame-first-image`, the clip opens on that
grid of thumbnails and text and animates out of it. **Verified on a real
run**: a sheet generated from that wording came back with four views, three
expressions, a colour palette and the caption "HANA TANAKA", and had to be
thrown away and regenerated as a single in-scene image.

So pick by the brief's `Shots` and `Sheet` answers:

**One shot** (the common case) — you need an opening frame, and nothing else.
There is no second shot to stay consistent with, so a sheet buys nothing.

```bash
bash ../ofox-image-core/references/ofox-image.sh generate \
  --prompt "<character description>, <the shot's opening moment: setting, pose, camera angle>, <school + texture layer from the brief>, <the brief's ratio as a composition instruction, e.g. vertical 9:16 composition>, cinematic composition, no text, no panels, single illustration" \
  --quality high \
  --target-aspect <the brief's ratio, e.g. 9:16> \
  --out-dir <a directory for this project's generated assets>
```

The `no text, no panels, single illustration` tail is what keeps the model
from drifting back into sheet mode — it is not optional padding.

**`--target-aspect` is not optional on an opening frame**, and it is why the
hand-crop this section used to describe is gone. The ratio goes in the prompt
as a *composition* instruction because it changes how the character is framed
— but the delivered pixels are settled by the flag, which since
`ofox-image-core` 1.7.0 measures the written file and centre-crops it to
exactly that ratio, failing loudly rather than delivering something close.
The size enum this API accepts contains no 16:9 or 9:16 entry at all
(`1792x1024` is 1.75, `1024x1792` is 0.5714), so the crop is structural, not
a fallback for a model that misbehaves — and an attached frame forces
`aspect_ratio: adaptive`, which means a wrong-ratio image is charged at the
price of the clip it opens. `IMAGE_PATH` is the cropped file, so Step 2
attaches it unchanged; the API's untouched bytes stay alongside as
`IMAGE_PATH_UNCROPPED`. Needs `ffmpeg`/`ffprobe`, checked before anything is
spent. Detail: `ofox-image-core`'s "The size enum cannot express 16:9 or
9:16".

**Several shots, `Sheet first`** — generate the sheet once, show it to the
user, and get the design confirmed. Then write **each shot's own opening
frame** with the exact same character description, and feed each shot its
own frame. The sheet is a checking artifact; it is never passed to
`--frame-first-image`.

```bash
bash ../ofox-image-core/references/ofox-image.sh generate \
  --prompt "<character description>, <school + texture layer>, character reference sheet, plain neutral background, front-facing full body" \
  --quality medium \
  --out-dir <a directory for this project's generated assets>
```

**Why the two commands pass different `--quality` values.** The opening frame
*is* the clip's first frame, so its fidelity carries into the deliverable —
`high` is what the one real run of this step used. A sheet is a checking
artifact that never reaches a video and is discarded once the design is
confirmed, so `medium` is enough for a human to read a wrong wardrobe or a
missing accessory off it.

The sheet command also passes no `--target-aspect`, and that is deliberate
rather than an omission: the sheet is never attached to a video job, so its
ratio decides nothing. The flag is mandatory only where the frame's ratio
becomes a clip's ratio.

Neither is `standard`, which this skill passed until 1.9.1 and which the
chain's current head refuses outright: `openai/gpt-image-2` accepts only
`low`, `medium`, `high` and `auto` — its own enumeration, read off an HTTP
400 on 2026-09-04, `Invalid value: 'standard'. Supported values are: 'low',
'medium', 'high', and 'auto'`, nothing billed. Since `ofox-image-core` 1.7.0
that combination is rejected locally instead, exit `1` with no network call,
so a `--dry-run` catches it for free. That is not a change in this skill —
`microsoft/mai-image-2.5-flash` accepts `standard`, and these commands worked
verbatim until `ofox-image-core` made `gpt-image-2` the chain head on
2026-09-04. Pass one of the four accepted values, or pin `--model
microsoft/mai-image-2.5-flash` when that model's look is what you want.
Costs, and which of them is measured, are in Approval 1 below.

**Several shots, `Straight to shot 1`** — generate shot 1's opening frame as
in the one-shot case, show it, and write the later frames from the same
description. When consecutive shots continue one moment, only the first needs
a frame at all — `chain` carries the rest.

**`I have a character image`** — the user's file is the design. Whether it
becomes an opening frame or an identity reference is the next subsection.

### The opening frame decides the output's shape

`bytedance/seedance-2.5` forces `aspect_ratio: adaptive` whenever an image is
attached, so the clip comes out at **the image's** aspect ratio, whatever
`--aspect-ratio` says. On the other two models this skill offers, the script
applies `adaptive` as the default when you pass no `--aspect-ratio` — which
this skill never does — so the clip follows the image there too. That is why
the brief asks for the ratio **before**
Approval 1: the image has to be delivered at the target shape, which is what
`--target-aspect` on the Step 1 command is for. There is no video flag that
fixes it afterwards, and fixing it by regenerating is a second image bill —
followed by a second *video* bill, since the clip already came out the wrong
shape. A user-supplied image is the one case you crop yourself, and it is
cropping only, never padding.

**Don't pass `--model` here.** `ofox-image-core` resolves one from its
cheapest-first priority chain — defined in exactly one place, its
`MODEL_CHAIN` — and prints the id it settled on, before it prints any
estimate. Pass `--model` only when the user named a model themselves.

This skill used to hardcode `google/gemini-3.1-flash-image`, the
sixth-cheapest image model Ofox serves and 2.3x the chain's preferred rate,
with no recorded reason for the choice. That is what a scenario skill holding
its own model id buys you: prices move, the copy doesn't, and nobody notices
because nothing is wrong — it just costs more than it needs to.

Whichever model runs, **don't promise the user a specific output resolution**,
and don't trust the printed `SIZE` line for the ratio. Since
`ofox-image-core` 1.7.0 you do not have to do the measure-and-crop by hand
either — `--target-aspect`, on every command above, measures the written file
and crops it — but the underlying mess is worth knowing, because it is what
the flag exists to absorb and what `SIZE_ACTUAL` in the output reports.
**How far off `SIZE` lands depends on which model the chain resolved**, and
both cases are measured:

- `microsoft/mai-image-2.5-flash`, the chain's head until 2026-09-04, on
  three runs whose frames then went into video: a request for `1792x1024`
  came back with the API reporting `1354x774` while the file on disk was
  `1344x768` — three numbers, none of them matching, all three times.
  Cropping that file to `1344x756` (cropping only, never padding, so nothing
  is invented at the edges) is what produced an exact `1280x720` clip;
  feeding it uncropped delivers 1.75:1, which then sits letterboxed in a 16:9
  frame.
- `openai/gpt-image-2`, the head since then, on **one** run at the same
  requested size: the request, the response's `SIZE` echo and the file's real
  pixels all read `1792x1024`. One run, so do not read it as a guarantee.

Honouring the request is not the same as a usable ratio, which is why the
crop step survives either way: `1792x1024` is 1.75, not 16:9, so that frame
still had to be cropped to `1792x1008` before it was attached. The size enum
has no 16:9 or 9:16 entry on any model, so no `--size` value avoids it. Read
`SIZE_ACTUAL` rather than `SIZE`, and if you are cropping by hand for some
reason, use `sips -g pixelWidth -g pixelHeight <file>` or
`identify <file>` — cropping only, never padding. More in the failure table's
`SIZE` row and in `ofox-image-core`'s "The size enum cannot express 16:9 or
9:16".

The video that came out of the first bullet's `1344x756` crop is also the
proof the lock works: job
`16023efe-48d6-45fe-8fd8-f5c6fbfe6519`'s first delivered frame
matched the fed image on composition, both characters, wardrobe, the fence,
the sunset and the falling petals — and the two later product jobs show the
lock holding for a full 20 seconds and across six hard cuts ("What a frame
lock actually holds, measured" in the shared file). This is what
`--frame-first-image` buys over a repeated text description.

Take the printed `IMAGE_PATH` (an absolute path) and **show it to the user
as its own standalone line** — say whether it is the shot's opening frame or
a design sheet, since those get used differently. `ofox-image.sh` also prints
`IMAGE_COST`; relay it the same way you relay a video's cost.

Show the image to the user before spending on the shot. A wrong opening
frame is cheap to notice here and expensive to notice after the video is
paid for — a sheet that slipped through, an invented caption, a character
who is not who they pictured. This is the second participation point of the
flow, and the user may send the design back here without it counting as a
new question round.

If the story needs more than one character, repeat Step 1 once per
character who needs their own image — see "Multiple characters in one shot"
below for the v1 scoping limit on this.

### Two ways an image can enter a shot

"Reference assets as visual anchors" in the shared file has the full
comparison; the part that matters here:

| | Frame lock — this skill's mechanism | Identity reference — what the gallery's image-bearing anime prompts do |
|---|---|---|
| The image is … | the literal first frame; the shot animates away from it | a source of appearance; no frame is locked, the shot composes itself |
| Flag | `--frame-first-image PATH` (local file, auto base64) | none — `--extra-json '{"input_references":[…]}'` |
| Prompt | opens on the frame; short character block | follow the shared [`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy); for example, `@image1 supplies <tag>'s identity only: face, hair, accessory, outfit; ignore its background and pose.` |
| Ratio | `adaptive`, follows the image | ⚠️ **pass `--aspect-ratio` explicitly.** The one measured identity-reference job passed none and came back **portrait from two landscape references** — following neither the default nor the images. One observation, no explanation (`api-params.md`) |
| Status in this repo | exercised on real runs: a generated image fed as a first frame produced a clip that opens on it — that is how the sheet-as-frame mistake was caught — and `ofox-video-core` records a `chain` continuity run | the shared recipe owns the evidence and limits. This anime-specific route has still not been exercised on an anime character |

**They are mutually exclusive in one job** — the script rejects the
combination client-side (`references_conflict`). A shot either starts on a
frame or borrows an identity, not both. A user-supplied character image can
go either way; a sheet can only sensibly be the second (as a frame it
produces the grid problem above).

Neither route is affected by the real-person refusal for an anime character;
the identity route's behaviour with a real person is untested in this repo
and irrelevant here.

If you take the identity route, `--dry-run` it first like anything else.

✅ **A local image does not have to be hosted — if you shrink it first.** This
file used to say hosting was required, on the grounds that only the URL
element shape was documented. The API's own rejection message names `data:`
URIs as acceptable and the measured run sent two local files that way, so the
requirement was never real. But there is a size limit, and it is local rather
than the API's:

🚨 **An oversized reference does not fail the command — it is silently
dropped and you pay for the wrong job.** This is the single most expensive
thing to get wrong on this route, and it does not announce itself.

`--extra-json` takes its value as a command-line argument, so a `data:` URI
built into it is bounded by `ARG_MAX` (1,048,576 bytes on this machine).
Over the limit, `jq` **never executes**: the shell writes one line to stderr,
the command substitution yields an **empty string**, and `ofox-video.sh`
treats an empty `--extra-json` as *not passed* — skipping validation and
merging nothing. Measured 2026-09-17 with a 1.9 MB PNG:

```
(eval):10: argument list too long: jq
PAYLOAD {"model":"bytedance/seedance-2.5","prompt":"x","duration":8,
         "resolution":"720p","aspect_ratio":"16:9", ... }
STATUS dry_run
EXIT=0
```

**No `input_references` in the payload. Exit 0.** Without `--dry-run` that is
a submitted, fully billed **plain text-to-video** job that you believe is an
identity-reference job — and the clip that comes back just looks like the
model ignored your character sheet. There is no error to catch. The one
stderr line comes from the shell, not from the script, so it carries no
prefix and scrolls past above the normal output.

⚠️ **Do not generalise from `--frame-first-image`, which is safe.** There the
script does the encoding itself through a temp file and `jq --rawfile`, and
a 1.9 MB PNG goes through intact (verified the same day). The two paths
behave in **opposite** directions at the same file size.

**So do both of these, every time:**

1. **Downscale the reference first.** The measured r2v run used JPEGs at a
   768 px long edge — 33 KB and 43 KB. A character reference supplies
   appearance, not pixels. If the image genuinely must stay large, a hosted
   https URL is the alternative, and now a choice rather than a requirement.
2. **Build the JSON into a variable, check it, and confirm it reached the
   payload with your own eyes.** The check below is the only thing that
   catches this.

```bash
# 1. Shrink and re-encode first — the limit is local, not the API's.
sips -Z 768 -s format jpeg /path/to/character.png --out /tmp/ref.jpg

# 2. Build the JSON into a VARIABLE, never straight into the flag.
REF="data:image/jpeg;base64,$(base64 < /tmp/ref.jpg | tr -d '\n')"
EXTRA="$(jq -n --arg u "$REF" '{input_references:[{type:"image_url",image_url:{url:$u}}]}')"

# 3. Refuse to continue if it did not build. Empty here = reference dropped.
[ -n "$EXTRA" ] && printf '%s' "$EXTRA" | jq -e . >/dev/null \
  || { echo "extra-json did not build (ARG_MAX?) — the reference would be dropped silently"; exit 1; }

# 4. Dry-run WITH --print-payload, then read the payload yourself.
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run --print-payload \
  --prompt "@image1 supplies the girl's identity only: face, chestnut bunches with pale-yellow ribbons, cream sundress, blue sash; ignore its background and pose. <the rest of the shot prompt from the template>" \
  --extra-json "$EXTRA" \
  --aspect-ratio 16:9 \
  --duration 8 --resolution 720p --out-dir ./out
```

**Then confirm `input_references` is actually in the printed payload before
spending.** `--print-payload` writes to stderr, so:

```bash
... --dry-run --print-payload ... 2>&1 | grep '^PAYLOAD' | grep -c input_references
# 1 = the reference is really in the request. 0 = it was dropped; do NOT spend.
```

`--dry-run` is free and makes no network call. It is not, on its own, enough:
a dropped reference dry-runs perfectly happily. **The payload check is the
step that matters.**

Say in the approval message that the **mechanism** is measured
(`ofox-video-core`, job `0f5c8b4e`) but that **this skill has not run it on an
anime character**, so the user is still pricing an experiment.

## Step 2: generate each shot from its opening frame

Feed each shot the frame that was written for it:

- **one shot** — the single `IMAGE_PATH` from Step 1;
- **a chained sequence** — only the first job takes `--frame-first-image`;
  `chain` carries the closing frames forward;
- **shots that cut to new setups** — each shot's own opening frame from Step
  1, all written from the same character description word for word.

Always pass the **absolute `IMAGE_PATH`** a script printed — never a
relative path, a re-derived guess, or a sheet.

For each shot, build the prompt from "Prompt template" above — the 8–15s
frame-lock shape for a single shot, the 15–30s manifest when the job holds
several timestamped shots — then call:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the shot prompt from the template>" \
  --frame-first-image "<that shot's opening frame — the ABSOLUTE path printed in Step 1>" \
  --duration 8 \
  --resolution 720p \
  --out-dir ./out
```

`ofox-video-core` auto-base64-encodes a local file path like this one — no
need to upload it anywhere first.

`--approved` is not decoration: without it the script refuses, submits
nothing, and prints the quote-first steps instead. It belongs on this command
only once the two-phase cost table has gone in front of the user and come back
with a yes — the flag cannot check that for you. To price a shot without
sending it, swap `--approved` for `--dry-run`.

### `aspect_ratio: adaptive` is applied for you here — expected, not a bug

**Don't pass `--aspect-ratio` in Step 2.** Every shot here attaches a frame,
and `ofox-video-core` (1.22.0+) sends `adaptive` for you, printing a `NOTE:`
every time. Two different mechanisms reach the same place, and the flag is
wrong in both:

- on `bytedance/seedance-2.5`, the API **requires** `adaptive` with a frame
  attached, so the script forces it and the flag has no effect;
- on another model the user named (`alibaba/wan-3.0-prime`,
  `minimax/hailuo-3`), `adaptive` is the **default the script applies because
  you left the flag off**. Pass a ratio there and it is honoured instead —
  which would fight the opening frame rather than follow it.

The shape comes from the image either way (see "The opening frame decides the
output's shape"). On `ofox-video-core` older than 1.22.0, a non-seedance model
sent no `aspect_ratio` at all and the frame's shape could be silently lost —
check the core skill's version before running a shot on a named model.

## Multiple characters in one shot: out of scope for v1

This skill scopes to one primary character image per shot, matching
`ofox-video-core`'s single `--frame-first-image` slot. If a shot needs two
characters interacting:

- generate an opening frame for the primary/foreground character only
  (Step 1),
- pass that image as `--frame-first-image` for the shot,
- describe the secondary character in the shot's prompt text (appearance,
  action, dialogue) — the same text-only approach `seedance-short-drama`
  uses for all of its characters.

This is a real accuracy tradeoff, not a full solution: the secondary
character has no image-based consistency guarantee across shots. Treat it
as the workaround it is, not as feature parity with the primary character's
mechanism.

The gallery did solve multi-character consistency — official case 1 (two
leads, one appearance image each), case 11 (two fighters and a venue, three
images), case 44 (heroine and opponent, two images) — but with **several
identity references**, which maps to `input_references` with more than one
image. That route is documented and untested end-to-end here (see "Two ways
an image can enter a shot"); it is the obvious next step for a v2, not
something this version claims.

## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.

## Before you spend: two approvals, not one

**Never submit a paid job until the user has seen a cost table and said yes.**
The shared spec — the table's required columns, where the numbers must come
from, batch itemisation, and the two-phase rule this skill is the current
example of — is written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

This skill spends in **two** places, at different rates that scale
differently, and phase 2's prompt depends on what phase 1 produced — the clip
literally opens on that image. So it asks **twice**. A single combined
estimate up front would have the user paying for shots of a character they
have not seen yet, and "what the character looks like" is the entire thing
this skill sells.

The brief recap (see "Where the brief sits in the two-phase flow") goes in
the Approval 1 message, above the image prompt and the table; Approval 2
carries it forward unchanged unless the user revised the design.

### Approval 1 — the image (paid once per character, not once per shot)

```bash
bash ../ofox-image-core/references/ofox-image.sh generate --dry-run \
  --prompt "<character description + opening moment + style>" \
  --quality high --target-aspect <the brief's ratio> --out-dir ./assets
```

Dry-run it with the **same** `--target-aspect` the real call will use, not
without it: the flag resolves which `--size` gets requested, and the size is
half of what the estimate is priced at. Quoting a run without the flag and
then generating with it is a table for a different request.

The table row: the `MODEL` line from that output (the chain has already
resolved it — never write "the default"), type `image`, the quality and size
you passed, quantity 1, and whatever the `Estimated cost:` line says. With
`Sheet first` there are two image rows — the sheet and the first opening
frame — and say that later frames add one row each.

**Copy that line verbatim, label and all — do not substitute a figure of
your own.** The chain's head has been `openai/gpt-image-2` since 2026-09-04,
and it has two real measured points: about **0.6 cents** at `--quality low
--size 1024x1024`, and **15.4 cents** at `--quality high --size 1792x1024`
(5063 output tokens, the job's own reported `IMAGE_COST`). A 26x spread from
two flags, and on 2026-09-04 the cheap end of it was quoted for a frame that
billed the dear end.

Since `ofox-image-core` 1.7.0 the script does that arithmetic itself: it
quotes the measured point matching the request's own `--quality`/`--size`
pair, and where no point matches it quotes the **dearest** one, labelled
`ROUGH UPPER BOUND` with the pair it borrowed from named on the same line.
Which of the two you get here depends on the brief's ratio, and both are
correct:

- `--quality high --target-aspect 16:9` resolves `--size` to `1792x1024`,
  which *is* a measured pair — a plain `ROUGH ~15.19 cents`.
- `--quality high --target-aspect 9:16` resolves to `1024x1792`, and
  `--quality medium` for a sheet names no size at all. Neither has ever been
  measured, so both come back as the `UPPER BOUND` at the same 15.4-cent
  ceiling.

Relay whichever line you get, with its label. Say "ceiling" in the table when
it says `UPPER BOUND`, and add that the real bill may land well under it —
but do not replace it with a guess at what `medium` or a portrait frame would
cost, and do not drop it to the 0.6-cent point because that looks closer to
the request. Nothing is interpolated between two measured points. If the
chain resolves to a model nobody has measured at all, the line says "cannot
be predicted" instead; the shared gate's "When there is no estimate" says
what to do with that, and the answer is still to show the table and wait for
a yes.

Say plainly that this is paid **once per character** (once per frame when
several shots each get their own) — generating N shots of that character
does not repeat it.

**Preview phase 2 in the same message.** Dry-run one shot at the duration and
resolution you plan to use, and quote it as "and then roughly X per shot for N
shots". Nobody should agree to step 1 without knowing the size of step 2 —
especially when step 2 is the expensive half. The preview is legitimate
without the image existing yet: attaching a first frame does not move the job
to a pricier tier (see below), so the number does not change once the image
is real.

### Approval 2 — the shots (paid once per shot)

Ask again once the image exists and the user has seen it. Now the shot prompt
is writable, because the character is on screen rather than described.

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "<the shot prompt>" \
  --frame-first-image "<the absolute IMAGE_PATH from phase 1>" \
  --duration 8 --resolution 720p --out-dir ./out
```

This table carries three things the first one could not:

- **one row per shot**, not a single total — three 8-second 720p shots and one
  30-second 1080p shot can come to similar money and mean nothing alike;
- **what phase 1 actually billed** (`IMAGE_COST` from the real run, not the
  estimate), and
- **the running total** across both phases.

Attaching `--frame-first-image` does **not** move the job to the more
expensive v2v tier, now measured at both resolutions anyone here uses: 4s at
11 cents/s at 480p, and 20s at 24 cents/s at 720p — $4.80 on job
`16023efe-48d6-45fe-8fd8-f5c6fbfe6519`, the t2v rate, where v2v at 720p
would have been 30 cents/s. Only a *video* input moves the tier, and this
skill never sends one. The script picks the tier; take it from the dry run
rather than assuming either way.

After the yes, run the identical command with `--dry-run` swapped for
`--approved`. That flag is where the yes gets typed out: since
`ofox-video-core` 2.0.0 the four billable subcommands — `generate`, `create`,
`batch`, `chain` — refuse to run without it, while `--dry-run` never needs it,
so both quotes above stay free and keep working with no API key. Be exact
about what it does: it records a stance, it cannot prove one. Nothing in a
shell script can observe the conversation you had, and it can be typed without
showing anyone a price. What it changes is that spending without quoting is no
longer the default — it has to be written into the command, where a transcript
shows it. The two approvals above are still the rule, and they are still yours
to follow. Phase 1's `ofox-image.sh` has no equivalent flag; Approval 1 binds
there just as firmly, only the reminder is missing.

Afterwards, report both real figures — `IMAGE_COST` from phase 1 and
`VIDEO_COST` from each finished shot — and the total across the two phases.

## Prompt language follows the audio

Audio is generated on by default, and the model speaks **whatever language the
quoted lines are written in**. So keep dialogue in the user's own language —
if they give you Chinese lines, put Chinese in the prompt. Translating them to
match the English examples in this file produces an English-dubbed clip, and
the user only finds out after paying for it.

The rest of the prompt (setting, camera, lighting) can be English regardless;
it is the quoted speech that determines the spoken language.

Budget the lines by tier before writing them — "Density — two tiers, not one"
under "Dialogue and sound" in the shared file. Overrun means a longer clip or
fewer words, never a faster delivery.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` (Step 2, video) | `bytedance/seedance-2.5` (script default, no flag needed) — **unless the user named a different video model**, which always wins | current-generation model; see "Choosing a video model" for the other two options. This is the **video** step's model only — Step 1's image model is resolved separately by `ofox-image-core`'s own chain and is a different, out-of-scope choice |
| `--duration` | `8` for one shot; for several timestamped shots in one job, sum 2–5s per shot (the two verified runs fit three shots into 8s, both text-to-video — see "Shots, cuts and jobs") | the gallery's segmented anime prompts run 24–30s, so a sequence often wants the longer end; a single frame-lock shot rarely does |
| `--resolution` | `720p` — a `seedance-2.5`/`wan-3.0-prime` value. On `minimax/hailuo-3` use `768p`: that model has no `720p` tier | detail on line art and faces at a reasonable cost; `1080p` only for a hero shot the user will publish (`2k` on `hailuo-3`, which has no `1080p` either) |
| `--aspect-ratio` | not passed — `adaptive` follows the image on every model this skill offers; the ratio is settled by the brief before the image exists | see "The opening frame decides the output's shape" and "`aspect_ratio: adaptive` is applied for you here" |
| `--generate-audio` | `true` (server default) unless the brief's `Sound` answer is `No dialogue` and the user wants silence; ambience and score still need it on | dialogue needs an audio track |
| image `--quality` | `high` for an opening frame; `medium` for a design sheet | the opening frame is the clip's literal first frame, so its fidelity reaches the deliverable; a sheet is discarded once the design is confirmed. **Not `standard`** — the chain's head (`openai/gpt-image-2`) rejects it at submission, accepting only `low`, `medium`, `high`, `auto` |

## Choosing a video model

Scoped to **Step 2** (the video shot) — Step 1's image model (the character
frame or sheet) is a separate choice made by `ofox-image-core`'s own model
chain and is untouched here.

`model` stays **never-ask** for Step 2 — the agent doesn't raise it as a
question of its own. But never-ask is not "never listen": `bytedance/seedance-2.5`
is only the default because nobody asked for something else. If the user
names a model — an id (`alibaba/wan-3.0-prime`, `minimax/hailuo-3`), or a
shorthand like "wan" or "hailuo" — pass that as `--model` on the Step 2
`generate` call instead of the default. Never silently substitute
`seedance-2.5` for a model the user actually asked for.

| Model | Cheapest tier (catalog) | Max resolution | Duration | Aspect ratios | Real moderation data point |
|---|---|---|---|---|---|
| `bytedance/seedance-2.5` (default) | 480p, 11 cents/s | 1080p | 4–30s | 7, incl. 21:9 | **Rejected** a photoreal-portrait i2v reference (`input_moderation_failed`) and a Re:Zero/Rem-styled anime t2v prompt after it had already generated (`output_moderation_failed`, copyright) — both free, nothing billed. See `.trellis/spec/skills/external-api-integration.md`, "Gotcha: moderation policy is per-model, not a platform-wide constant". |
| `alibaba/wan-3.0-prime` ("wan") | 480p, 6.4 cents/s | 1080p | 2–30s — the shortest minimum of the three | 6 — no 21:9/9:21 | **Accepted** both of the clips seedance-2.5 rejected above, 12.8 cents each (2s/480p, its minimum) — including the Re:Zero/Rem-styled **anime** prompt, the content class this skill produces by default. Only these two content classes have been tested — not a general "no moderation" guarantee for this model. |
| `minimax/hailuo-3` ("hailuo") | 768p, 8 cents/s — no 480p tier | 2k, uniquely among the three, at 13 cents/s | 4–15s — the shortest **maximum** of the three, so it's out for anything past 15s | 7, incl. 21:9 | **Accepted** the same two clips, 32 cents each (4s/768p, its minimum). Same caveat: two content classes tested, not a blanket clearance. |

Price, max resolution, duration and aspect-ratio counts are catalog facts —
`GET https://api.ofox.ai/v1/models/catalog`, no API key needed, publicly
re-checkable any time — not results from a real generation. The moderation
column is the one column here that came from a real, paid API call, and it
is directly relevant to this skill: the anime t2v prompt that
`wan-3.0-prime` and `hailuo-3` both completed and `seedance-2.5` refused for
copyright is exactly the kind of prompt this scenario writes. Still, treat
it as evidence about that one tested prompt, not a guarantee for every
licensed-character request. `wan-3.0-prime` runs on two upstreams
(`alicloud`, `aliyun`) and `hailuo-3` on two (`minimax`, `novita`), neither of
which `ofox-video-core` currently pins the way Seedance's `byteplus`/`volcengine` pin works
below. Note also `hailuo-3`'s 15s duration cap against the gallery's
24–30s segmented anime prompts (see `--duration` above) — a long multi-shot
sequence may not fit it.

### What changes when the model changes

Step 2's defaults table was written for `seedance-2.5`. Two entries do not
carry over unchanged:

- **`--resolution 720p` does not exist on `minimax/hailuo-3`.** That model
  offers `768p` and `2k` only, so pass `--resolution 768p` there and price the
  approval table's video row at its rate. Sending `720p` is rejected by the
  script locally, before submission, for free — but the cost table is wrong
  before that point.
- **The opening frame's shape is applied by a different mechanism.** `adaptive`
  is *forced* on `seedance-2.5` and is the *default when you pass no
  `--aspect-ratio`* on the other two — see "`aspect_ratio: adaptive` is applied
  for you here". Keep leaving the flag off and both behave the same way; the
  script says which it did.

Both need `ofox-video-core` 1.22.0 or newer. Step 1 is unaffected: the image
model is `ofox-image-core`'s own chain and is not what the user named here.

## Several takes to choose from

Video generation is a slot machine — most takes go in the bin. When the user
wants options rather than one clip, use `batch` instead of running `generate`
repeatedly:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 4 --duration 8 --resolution 480p --out-dir ./out
```

It prices the whole batch up front, stops on the first failure instead of
burning the remaining takes, and produces a contact sheet — three frames per
take, one row each — so the user picks from one image instead of opening N
files. Price it the way the shared gate's "Batches get an itemised table, not
one total" requires: a row per take and `BATCH_COST_TOTAL`.

Hand the user the `CONTACT_SHEET` path on its own line, the same way you hand
over a video — in this flow it is the artifact they actually look at first,
since it is how they pick. Then list the individual take paths beneath it.

Each `TAKE` line carries `seed=N`. That seed is how "take 3 was the good one"
gets written down at all: re-running the same prompt with that seed on a
better model or higher resolution **aims at** that take. It does not return
it — measured 2026-09-15, three submissions of one byte-identical request on a
fixed seed came back as two visibly different clips and one refusal, so this
API is not reproducible even with nothing changed. Say that before the user
pays for the re-render; a promotion is another roll at the same shot.

A single `generate` prints a `SEED` line too, and records it in the clip's
`.json` sidecar along with the resolution and aspect ratio. So "that one was
good, give me it at 1080p" works off one clip — you do not need a batch to
get a handle worth re-submitting.

Worth offering when the user is exploring: draft cheap on
`bytedance/seedance-2.0-mini` at 480p, then render the winner on
`bytedance/seedance-2.5`. Four 8-second drafts cost about 64 cents on mini versus
$7.68 on 2.5 at 720p. But **don't switch models on their behalf** — a
different model is a different look, not just a different price.

## Pricing a job with no API key

**No API key needed** to find out what something costs. All three of these
work with `OFOX_API_KEY` unset:

```bash
bash ../ofox-video-core/references/ofox-video.sh models      # models and rates
bash ../ofox-video-core/references/ofox-video.sh providers   # full price matrix
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 15 --resolution 720p             # a real quote
```

So when a user hasn't signed up yet, **quote the job first and let them decide
whether it's worth registering.** Don't open by sending them to a signup form
— price it, show them the number, then point at
[app.ofox.ai](https://app.ofox.ai) if they want to proceed.

## If the script isn't found

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

Nothing is broken — this skill delegates all execution to the two core skills
and reaches them by relative path, and that path just missed. Two different
situations wear this same message, so run the probes in "Where the two core
skills live" before deciding which one it is. The same reading applies to
`../ofox-image-core/references/ofox-image.sh`, which Step 1 needs for the
opening frames:

- **The probe printed a directory** — that core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-video-core`, `ofoxai-skills-ofox-image-core`). Re-run
  the command against what the probe printed. Nothing needs installing.
- **The probe printed nothing** — that core really is absent, and installing
  it is the user's call to make, not yours: an install writes outside this
  working directory, so hand over the command and let them run it rather than
  running it for them. Which command depends on the installer they already
  have — skills.sh is `npx skills add ofoxai/skills --skill ofox-video-core`
  (or `npx skills add ofoxai/skills --skill ofox-image-core`), which asks for
  that one core and answers none of the agent, scope or confirmation questions
  on the user's behalf; this repo's own wrapper is
  `npx ofox-skills ofox-video-core` (or `npx ofox-skills ofox-image-core`),
  the same install with all three answered in advance (every agent,
  user-level, no prompts); on LobeHub or ClawHub, install the missing core
  from the same publisher. Ask for the one core that is missing rather than
  the whole repo, and give all three routes — pointing a LobeHub user at the
  skills.sh line alone reads as "abandon your installer", which isn't the
  advice. Name **which** core is missing — this skill needs both, and losing
  `ofox-image-core` alone stops Step 1 while Step 2 would still run.

Either way, say which skill is missing and where it is expected rather than
relaying the raw path error, which names neither.

An absent core takes the shared reference files with it. This skill packages
only its `SKILL.md` and `CHANGELOG.md`; `prompt-structure.md`,
`creative-brief.md`, `approval-gate.md` and the two `api-params.md` files
live in the core skills, so a link to any of them will not resolve either.
When a probe found a core and a link still doesn't resolve, the link is
pointing at the wrong directory name and wants the same substitution; when it
found nothing, the docs return with the install. Work can continue meanwhile
— the prompt templates, the brief's questions, the two-phase flow and the
defaults are written out here. Only the depth behind the general rules is
missing: the full camera and transition vocabulary, the wider question-flow
rules, and the gate's exact wording, which still applies before any money
moves.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md) —
the ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely |
| `2` | Environment problem — `curl`/`jq` missing, or no `OFOX_API_KEY` | Ask the user to fix it; `check` reports the same |
| `3` | API rejected it, or the job ended failed/cancelled/expired | Read the mapped message; a rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `generate` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID` instead of regenerating |

## How long to tell the user it will take

`generate` blocks while it polls, up to `--max-wait` (default 540s). A short
480p draft is usually one to three minutes; longer or higher-resolution jobs
take longer. Say so before starting, so the wait isn't silent.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) followed by `poll`, instead of `generate`. That way a
timeout can never strand a job whose id you never saw. For `batch`, the worst
case is `takes x max-wait` — lower `--max-wait` for drafts, or create and poll
each take yourself.

## Where the file lands

Always pass `--out-dir`. Without it the script writes to the current working
directory, which is usually the user's project root. Pick something sensible
(`./out`, or wherever the user asked) and relay the absolute `VIDEO_PATH` the
script prints, on its own line.

Pass `--name` too. You know what the shot is — you just wrote the prompt for
it — so name the file after the scene rather than leaving the script to guess
from the prompt's opening words, which describe the setting and the lighting.
The clip lands as `<name>-<short job id>.mp4` with a `.json` sidecar beside
it holding the full job id, the prompt and the real cost.

## Running the script

Paths in the examples above are written relative to **this skill's own
directory**, and they assume both cores sit beside it under their own names —
the skills.sh / ClawHub / `npx ofox-skills` layout. "Where the two core skills
live" at the top of this file has the probes for the other layouts;
substitute whatever they printed for `../ofox-video-core` and
`../ofox-image-core`. If you are running from somewhere else entirely, adjust
accordingly — from a clone's repo root they are
`skills/ofox-video-core/references/ofox-video.sh` and
`skills/ofox-image-core/references/ofox-image.sh`.

## Generating: putting the two steps together

Example full sequence for **one shot** (the character/shot content is
illustrative — the calling agent fills in the real content extracted from the
user's story, and the brief has already settled 9:16, the style and the shot
count):

```bash
# Step 1 — the shot's OPENING FRAME, not a sheet (--model omitted on purpose: the chain resolves it)
bash ../ofox-image-core/references/ofox-image.sh generate \
  --prompt "A teenage girl, silver bob haircut, navy school uniform with a red ribbon, sharp green eyes, standing at the edge of a school rooftop at sunset, wind in her hair, seen from a low medium shot with the city behind her; modern theatrical anime, cel-shaded, vibrant colours; vertical 9:16 composition; cinematic composition, no text, no panels, single illustration" \
  --quality high \
  --target-aspect 9:16 \
  --out-dir ./assets
# IMAGE_PATH is the cropped, exactly-9:16 file — that is the one Step 2 attaches.
# IMAGE_PATH_UNCROPPED is the API's untouched bytes, kept for a human who wants a different crop.

# Step 2 — the shot, opening on that exact frame (the SAME absolute IMAGE_PATH Step 1 printed)
# --approved goes on only after the two-phase table came back with a yes.
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "Start exactly on the opening frame. The silver-bobbed girl in the navy uniform stands at the rooftop edge at sunset; modern theatrical anime, cel-shaded. One shot, 8 seconds. Low medium shot, slow push-in. The wind lifts her hair; she looks toward the horizon, then says, quietly and without turning: \"I'm not going back.\" The camera settles; hold one second. AUDIO: wind, distant traffic, no music. CONSISTENCY: her face, silver bob, green eyes, uniform and red ribbon unchanged. AVOID: subtitles, watermarks; photorealism, game CG; identity drift." \
  --name "rooftop confession shot 1" \
  --frame-first-image "/absolute/path/to/assets/ofox_image_20260829183214_4821.png" \
  --duration 8 \
  --resolution 720p \
  --out-dir ./out
```

For **several shots that cut to new setups**, Step 1 runs once per shot for
its opening frame, each from the same character description — plus once for
the sheet when the brief's `Sheet` answer kept it (shown to the user, never
passed to the video); Step 2 runs once per shot with that shot's own frame.
For **shots that continue one moment**, use `chain` with shot 1's frame; see
`ofox-video-core`'s `chain` documentation.

Report the **actual** printed `IMAGE_PATH` / `VIDEO_PATH` / `VIDEO_COST`
from each script's own output — never an estimate, and never a path or cost
you didn't see a script print. Do not re-implement any of the
request/decode/poll/download logic here; always call into
`ofox-image.sh`/`ofox-video.sh`.

## Common failure modes and fixes

Combining both core skills' documented exit codes (full tables:
[`ofox-image-core/references/api-params.md`](../ofox-image-core/references/api-params.md),
[`ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus this skill's own:

| Step | Symptom | Cause | Fix |
|---|---|---|---|
| 1 (image) | Exit `1`, no network call made | Missing `--quality`, bad `--model`, or `--n` combined with Gemini | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| 1 (image) | Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-image-core`'s `check` and follow its install/signup guidance |
| 1 (image) | Exit `1`, `--quality '<v>' is not accepted by '<model>'`, no network call | `--quality standard` was passed and the chain resolved to `openai/gpt-image-2`, which accepts only `low`, `medium`, `high`, `auto`. Every command in this skill passed `standard` until 1.9.1, and they broke the day `ofox-image-core` made that model the chain head (2026-09-04) — not from anything changing here. Until `ofox-image-core` 1.7.0 this surfaced as exit `3` / HTTP 400 at submission (still unbilled); 1.7.0 validates `--quality` against the resolved model, so it is now caught locally, including under `--dry-run` | Pass `high` (an opening frame) or `medium` (a sheet), or pin `--model microsoft/mai-image-2.5-flash`, which does accept `standard`. Free to retry — nothing was submitted and nothing was charged |
| 1 (image) | Exit `3`, `error.type: image_generation_user_error`, upstream message *"Your request was rejected by the safety system"* | The **safety system** refused the prompt before generating. The message carries **no category**, so it does not say which clause did it. On 2026-09-06 this fired on a character frame for an anime fight, and a five-step bisect the next session isolated the trigger to one wardrobe word — `cropped`, in `cropped jacket`, most plausibly read as sexual content (the endpoint names no category, so that part is inference). The setting and the powers were each changed alone in a step that passed, so those two are cleared. The weapons and the covered faces are not — removing them did not lift the refusal, so neither is the cause on its own, and no `gpt-image-2` call that passed has carried them (route (b) is a different model). The explicit ages and the strike landing on a person are untested: the bisect started from a prompt that had already dropped both. Nothing billed | Two routes, and the second is the one that gets forgotten. (a) Change the suspect phrase — wardrobe wording first, before the subject matter; the earlier `1.10.0` advice to drop the age numbers and soften the clash has **no isolating evidence** behind it and the bisect points elsewhere. (b) Re-run the prompt unchanged on `--model microsoft/mai-image-2.5-flash`; an earlier run had `openai/gpt-image-2` refuse a bladed character sheet twice while that model produced it, blade kept. Route (b) is the one to reach for when the refused element is something the shot needs. Free to retry either way — nothing was submitted to a billed generation. Procedure for finding an unknown trigger: [`ofox-image-core/references/api-params.md`](../ofox-image-core/references/api-params.md), "When a refusal names no category, bisect rather than guess" |
| 1 (image) | Exit `3`, `error.type: invalid_request_error` | The request was rejected as malformed/unsupported. The confirmed error shape is `{"error":{"message","type","code"}}` — `error.code` is just the HTTP status as a number here, `error.type` is the real classifier | Read the printed `Upstream message`, fix the prompt/flags, retry — a rejected request has not been confirmed to bill |
| 1 (image) | Exit `4` | `--out-dir` could not be created or entered | Caught before any network call, so no money was spent finding this out. Fix `--out-dir` and retry |
| 1 (image) | Exit `5`, ambiguous network failure | No HTTP response at all — this is a synchronous, no-job-id API, so there's nothing to poll afterward | Do not guess or retry blindly; check `https://app.ofox.ai`'s usage/billing history first |
| 1 (image) | The image is a multi-panel sheet with labels when an opening frame was wanted | The prompt lacked the `no text, no panels, single illustration` tail, or said "reference sheet" | Regenerate as an in-scene single illustration; do not pass the sheet to `--frame-first-image` |
| 1 (image) | `SIZE` in the printed output doesn't match what you asked for | Three models, three behaviours: `google/gemini-3.1-flash-image` always generates at its native 1024x1024 and echoes the requested `size`; `microsoft/mai-image-2.5-flash` disagrees three ways (requested `1792x1024`, echoed `1354x774`, file `1344x768`, on three runs); `openai/gpt-image-2` matched exactly, on one run. So `SIZE` is unverified whichever model the chain resolved — see "The opening frame decides the output's shape" | Read `SIZE_ACTUAL`, measured from the written file, not `SIZE`. Don't promise the user a specific resolution; for a guaranteed *ratio* pass `--target-aspect` (or `--target-size`) so the script crops it — that is not a workaround, since the size enum has no 16:9 or 9:16 entry on any model. Cropping only, never padding |
| 2 (video) | Exit `1`, no network call made | Bad `--duration`/`--resolution`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| 2 (video) | Exit `1`, `references_conflict` | Both `--frame-first-image` and an `input_references` array in `--extra-json` were sent | Pick one route per job — see "Two ways an image can enter a shot" |
| 2 (video) | Exit `1`, "local image file ... exists but is not readable" | `--frame-first-image`'s path exists locally but this script/OS can't read it (permissions) — caught by `resolve_image_ref()` before any network call | Fix the file's permissions (confirm it's the exact `IMAGE_PATH` printed in Step 1) and retry — free, nothing was submitted |
| 2 (video) | Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| 2 (video) | Exit `3`, `error.code: insufficient_credits` | Ofox balance too low | No charge was made; the user needs to add credits at `https://app.ofox.ai` before retrying |
| 2 (video) | Exit `3`, `output_moderation_failed`, *"the output video may be related to copyright restrictions"*, **on both upstreams** | A frame this model itself generated was fed back in as the next job's `--frame-first-image`. Measured 2026-09-06: `c192dbe6`'s own delivered last frame was refused as `5440c21e` on `byteplus` and again as `c4cff71a` on `volcengine`. Neither billed. Since the two upstreams moderate differently, both refusing points at the content — a stylised anime frame reads as closer to existing IP on the way back in than the text-to-image frame that opened the sequence did | The usual switch-upstream fix does not help here. Either continue with the words route instead (see "Continuing a previous clip" in the shared file — measured working on `c2eb32e1`), or regenerate the continuation's opening frame through `ofox-image-core` rather than reusing a delivered video frame. Budget for this before planning a long chained series |
| 2 (video) | Exit `3`, job ends `failed`, `error.code: output_moderation_failed` | The generated output failed a post-generation content check, after the job ran — not billed (no `usage` field) | Retry with a brand-new `generate` call using a different prompt — a new request, safe to retry immediately |
| 2 (video) | Exit `3`, request rejected when the API tries to use the reference image (commonly `error.code: invalid_request`) | The `IMAGE_PATH` doesn't exist locally and isn't a URL either, so `resolve_image_ref()` passed it through unchanged and the API rejected it as an unusable value — `ofox-video-core`'s docs confirm `bad_data_uri`/`download_failed`/`unreachable`/`not_image`/`too_large` only for `--real-person`'s reference-photo validation, not for `--frame-first-image`/`frame_images`, so don't assume one of those five specific codes here | Confirm the exact `IMAGE_PATH` printed in Step 1 still exists and is a valid, readable image file, then retry |
| 2 (video) | Unexpected aspect ratio / frame shape in the output | `bytedance/seedance-2.5` + `--frame-first-image` always forces `aspect_ratio: adaptive` (printed as a `NOTE:`, never silent) — the output follows the image's own aspect ratio. On another model the user named, the same `adaptive` is applied as the default because this skill passes no `--aspect-ratio`; on `ofox-video-core` older than 1.22.0 nothing was applied there at all, which is its own cause of a wrong shape | Expected behavior, not a bug — the brief settles the ratio before Step 1 for exactly this reason, and `--target-aspect` on the Step 1 command is what keeps it. If it was missed, re-crop the existing frame (cropping only, never padding) and regenerate the shot — that is a second **video** bill, not a second image one |
| 2 (video) | A cut lands up to a second off its timestamp | Expected: the verified multi-shot runs placed cuts within about ±1s of the written stamps | Give each shot 2s or more of slack around a line or a decisive hit; if a cut must be frame-exact, use `chain` or separate jobs |
| 2 (video) | Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| 2 (video) | Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; check `https://app.ofox.ai` first, per `ofox-video-core`'s no-resubmit rule |
| 2 (video) | Exit `6`, `--out-dir` could not be created or entered | Local filesystem problem, not an API problem | The job itself is unaffected — fix `--out-dir` and re-run `poll JOB_ID --out-dir <a writable directory>`; do not re-run `generate` |
| both | Character looks visibly different between two shots | The opening frames were written from different character descriptions, the sheet was skipped and a frame drifted unnoticed, or the shot prompt lacks the `CONSISTENCY` line and the style sandwich | Write every frame from the same description word for word, check each frame against the confirmed sheet before Step 2, and keep the `CONSISTENCY` and `STYLE` lines in every shot prompt |

## When NOT to use

- Realistic-human dialogue scenes with no anime styling — use
  `seedance-short-drama` instead. That skill's character consistency is
  text-only (repeating the same description across stateless jobs); this
  skill starts every shot on an image of the character, but only for an
  anime art style — every prompt this skill builds bakes in the brief's
  `Style` answer, so it is not a general-purpose "add image consistency to
  any style" tool, and a photoreal frame would be refused anyway.
- Silent product/brand footage with no characters — use `seedance-ad-creative`
  instead.
- Plain catalog/listing product shots — use `seedance-product-video` instead.
- More than one character needing independent image-based consistency in the
  same shot — out of scope for v1 (see "Multiple characters in one shot"
  above); only one primary character gets an image per shot.
- Editing an existing character's outfit/appearance mid-story — this skill
  only does fresh text-to-image generation (`ofox-image-core` doesn't
  implement `/v1/images/edits`); generate a new Step-1 image instead, treated
  as a new "version" of the character from that point on.
