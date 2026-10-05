---
name: ugc-ads
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Generate a handheld, phone-shot UGC clip — imperfect framing, one practical light, vertical, no cinematic grading, no beauty filter. It inverts the polish every other video skill here defaults to — a UGC clip that looks like an ad has failed. Use when a user wants a video that reads as filmed by a real customer rather than by an agency, e.g. "a real-looking phone unboxing of this product", "a creator first-impression clip for TikTok", "an honest review video, nothing slick", or "make it look like a customer shot it". Do not use for a polished brand ad (see seedance-ad-creative), plain catalog footage (see seedance-product-video), a dialogue scene between people (see seedance-short-drama), or a set of cheap vertical drafts to choose from (see shorts-reels).
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/ugc-ads
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
    emoji: "📱"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/ugc-ads
---

# ugc-ads: handheld, phone-shot, deliberately unpolished

Turns a product and a situation into a clip that reads as something a real
customer filmed on a phone — an unboxing, a first impression, a use-it-once
review. Amateur texture is the deliverable, not a compromise.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the UGC prompt
craft, the brief, the defaults and the pre-generation cost estimate;
`ofox-video-core` owns talking to the Ofox API correctly and safely (the
`OFOX_API_KEY` handling, the no-resubmit rule, error-code mapping,
download/verification, and reporting the downloaded file's absolute
`VIDEO_PATH`). **Read that skill's safety contract before using this one** —
it is not restated here.

The shared prompt craft — the vendor's formula, timestamps, transitions,
camera vocabulary, consistency locks and negative lists — is in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md);
the pre-prompt question rules in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md);
the spend rule in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
This file carries only what is specific to UGC.

## The inversion — read this before writing anything

**Every other video scenario in this repo is aimed at polish, and so is most
of the shared prompt guidance.** Its style vocabulary is full of cinematic
anchors, studio keys and hero frames; the ad skill's own archetypes are
Luxury, Playful and Minimalist-tech; its pacing shape is
hook → showcase → slow-motion climax → hero freeze. All of that is correct
for those scenarios and **wrong here**.

| The default, everywhere else | Here |
|---|---|
| Cinematic colour grade, warm rim light | Whatever the room's own light does, including bad white balance |
| A studio key, or golden hour | One practical source — a window, a ceiling lamp, a phone's own screen |
| Smooth, motivated camera moves | Handheld drift, a small re-frame, an arm that gets tired |
| Perfect framing, subject centred | The product half out of frame until a hand corrects it |
| A slow-motion climax and a hero freeze | A flat action chain with no climax, ending "naturally, not promotionally" |
| Skin that reads as clean | Skin that reads as skin |
| A seamless backdrop | An actual kitchen counter with other people's objects on it |
| `AVOID` is a backstop | `AVOID` is half the brief |

**The failure mode is silent, and nothing in the tooling catches it.** A clip
that comes back beautifully graded, stabilised and lit has not errored; it has
rendered exactly what it was asked for. It is just no longer UGC, and the only
place that gets noticed is in front of the audience it was meant to fool. So
the check has to happen in the prompt, before the money moves.

### The three habits that leak in

1. **Style words carried from another scenario.** `cinematic`, `8K`,
   `professional`, `studio`, `premium`, `glossy`, `film grain`, `shallow depth
   of field`, `rim light`, `colour grade`. Every one of them is a defect here.
   `film grain` is the subtle one: it is an anti-plastic anchor in the shared
   guidance and it is still *film*, which a phone is not.
2. **The ad beat structure.** The moment a timeline grows a climax and a hero
   frame, the clip is an ad with handheld camerawork bolted on. UGC-style
   prompts in the gallery are a flat chain of ordinary actions (cases 24–27).
3. **A camera that behaves.** "Handheld" written once in a style line, and
   then every beat describing a clean push-in, produces a clean push-in.

**Before submitting, re-read your own prompt for the words in habit 1.** That
takes seconds and is the single highest-value check in this skill.

### Where the anti-polish vocabulary lives — load it, don't rewrite it

It already exists, derived from real gallery cases, and it is deliberately
**not** copied into this file: one copy gets corrected and the other keeps the
old wording. In
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md):

| What you need | Section, in that file |
|---|---|
| The `AVOID` list itself | `Consistency locks and the negative list` → `Negative list — the frequent items` → the **UGC anti-polish** row (cases 25, 40). It covers colour grading, beauty filters and skin smoothing, dramatic slow motion, music, perfect lighting, and the CG look — quote that row, don't paraphrase it |
| Phone-capture style anchors | `Style anchor — the texture layer` → the **Consumer capture** row (cases 20, 25, 40) |
| Handheld camera phrasing | `Camera language` → `Camera movement` → the **Handheld / breathing** row |
| The viewpoint — never the phone's location | `Camera language` → `Camera position / angle`, and the **Phone POV** row under `Camera movement`. ⚠️ Read "The capture is part of the fiction" below **first**: those rows quote gallery prompts that place a phone somewhere in the room (`static phone propped on bathroom sink`), and measured here, that phrasing renders a phone in the shot. Take the viewpoint from them, not the prop |
| Autofocus and exposure misbehaviour | `Camera language` → `Focus` → the **Autofocus hunting (UGC texture)** row |
| The beat shape | `Pacing` → the closing note: UGC clips are a flat action chain with no climax |
| Why a prohibition alone is not enough | `The plastic look is designed out, not forbidden` — the four faults that produce the AI-render look and the positive sentence that crowds each one out |

That last row is the one to actually read. Its argument is the whole reason
this skill needs a positive half: **a prohibition removes a class of thing
without supplying what stands in its place**, and "not cinematic" leaves the
model to pick its default, which is the cinematic one. The scenario-specific
positive form is below, under "What actually reads as UGC".

## What has been tested, and what has not

**This scenario has two paid runs**, both `bytedance/seedance-2.5`, 8 seconds,
480p, 9:16, **88 cents each**, and both with the prompt filled in from this
file's own template by an agent working from this file and nothing else — so
what they tested was the whole chain (skill → agent → command → artifact)
rather than the API. Both were judged on frames extracted from the delivered
clip against criteria fixed before the run, not on `STATUS completed`.

| Run | Shape |
|---|---|
| `2ecbedec` (2026-09-15) | text-to-video, **no attached photo**, hands only |
| `ede33e6d` (2026-09-17) | **a real product photo attached** as the first frame, and **the corrected CAPTURE wording** |

### Run 1, `2ecbedec`

| What was checked | Result |
|---|---|
| **Does the anti-polish steering actually hold?** The criterion, written before the run: the clip must *not* look like the ad `seedance-ad-creative` would produce — no centred hero framing, no dramatic lighting, no shallow-focus beauty shot | **It held.** Off-centre, loosely composed framing; a single practical window light with real falloff; no grade |
| Hands only, no invented face | held — hands throughout, no face anywhere in the clip |
| The product | rendered as described, no drift |
| **The capture line** | **failed** — the line said where the phone was, and the model put a phone in the room. See the ⚠️ under "The capture is part of the fiction" |

### Run 2, `ede33e6d` — the corrected CAPTURE line, and three new findings

The correction made after run 1 had never itself been generated. It has now.

| What was checked | Result |
|---|---|
| **The corrected CAPTURE wording** — does converting the device from an object in the room into a viewpoint keep it out of the shot? | ✅ **It held.** Six sampled frames across the clip contain **no phone, no camera, no tripod and no lit screen**. One candidate object, enlarged, is an out-of-focus wooden desk item; the left-hand shape is a lamp arm with a blue practical behind it, which is the `SCENE` line's own "a warm lamp on the left" |
| The product, against the attached photo | held — wordmark, copper cap and gunmetal brushed finish all match the photo |
| Hands only, no invented face | held for the whole clip |
| The beat chain | ran in the written order |
| ❌ **The opening** | **a flash frame and a hard cut** — see below |
| ⚠️ **Anti-polish** | **weaker than run 1, and this run cannot say why** — see below |

**❌ The opening flash cut.** The attached photo was a white studio shot; the
`SCENE` was written as a desk at night. Background brightness at the top-left:
**250** at 0.00 / 0.04 / 0.08s, **33** from 0.12s onward. So the clip opens on
about a tenth of a second of the product photo and then **hard-cuts** into the
scene. This is a general mechanism, measured across three runs and written up
once in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)
→ "If the attached frame's background disagrees with your SCENE". **It hurts
this scenario more than any other**, because an unbroken, un-staged single take
is the entire product and the cut lands on frame one. Fixes, cheapest first:
write the `SCENE` as the place the photo was actually taken; or use a photo
already shot in the target setting; or trim the first 0.15s before delivery.

**⚠️ Anti-polish was weaker, and two variables changed at once.** Run 1's
pre-registered criterion was that the clip must not look like
`seedance-ad-creative`'s output. Run 2 leans toward polish: the bottle sits
near centre, the background is shallow-focus, the key light is warm with
falloff, and the steam is flattering. **But run 2 changed both the photo and
the CAPTURE wording**, so the cause is not attributable. A plausible
hypothesis — *attaching a clean studio product photo pulls the whole clip
toward polish* — is worth testing and is **not a finding**. The single-variable
run that would settle it: the same prompt, the same corrected CAPTURE line,
with and without the photo. Until then, **when a photo is attached, look
specifically for polish creeping in** and treat a re-roll without the photo as
a live option.

Read those as two clips, not a guarantee. One model, one duration, one tier,
one product, hands only, no dialogue. The anti-polish inversion is the claim
run 1 genuinely supports, because it was designed to falsify it and did not —
and run 2 is the reason that claim is now stated for the text-only path rather
than for the skill as a whole.

What it is built on besides that run:

- **Gallery practice.** The collected creator-style prompts (cases 23–27, plus
  30–33 for texture phrasing) are prompts somebody kept, with a finished video
  attached — on platforms and with parameters that are mostly unrecorded. That
  is evidence about what a good UGC prompt looks like, not about what this API
  does with one.
- **Mechanism facts measured in this repo**, which apply here because they are
  about the API rather than about the genre: an attached photoreal-person
  frame is refused at submission; asking the model for music has failed output
  moderation on copyright; a prohibition on a *class of object* holds better
  than one on a *tempo*; a camera move written only as a verb tends not to
  happen. Each is cited where it is used below.

Practical consequence: **two clips is still thin evidence.** Anything outside
those runs' parameters — a person on camera, a spoken line, a longer clip, a
different model, a higher tier — is still an experiment and should be priced
and described as one. The attached-photo path is no longer unrun, but its one
run carried two defects (the flash cut, the polish drift), so it is the path
to draft cheaply rather than the safe one. Draft small before anyone pays for
a deliverable — see "Several takes, and the cheap vertical route".

## Where the core skill lives

Resolve once, before the first call:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/ofox-video.sh" ] && echo "$d" && break
done
```

Examples below are written as `../ofox-video-core/...` (the skills.sh /
ClawHub / `npx ofox-skills` layout, where a skill's directory is named after
the skill). If the probe found a different directory — LobeHub unpacks each
skill as `ofoxai-skills-<name>`, so the sibling there is
`ofoxai-skills-ofox-video-core` — substitute it, in the `ofox-video.sh`
commands and in the `references/*.md` links alike.

**That `../` is relative to this skill's own directory**, which is also where
the probe has to run. From anywhere else nothing resolves — use the absolute
path the probe printed (candidates 3–5 are absolute already), or, in a clone
of this repo, `skills/ofox-video-core/references/ofox-video.sh` from the repo
root.

Nothing found → the core skill isn't installed; see "If the script isn't
found".

**This skill needs `ofox-video-core` 2.0.0 or newer.** From that version the
billable subcommands refuse to run without `--approved`, and every real-run
command below passes it. An older core does not know the flag and stops with
`unknown option '--approved'` before any request — nothing is submitted and
nothing is billed, so the fix is to update the core, never to drop the flag.

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

If it fails, follow `ofox-video-core`'s guidance (install `curl`/`jq`, or get
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the conversation,
and don't re-run this check on every subsequent request once it has passed.

`check` reports whether the key is **present**, not whether it is valid, and
makes no network call. It reads an ordinary environment variable in the shell
that runs the script — nothing is loaded from a `.env` file, so a project that
keeps the key in one has to source it into the same shell first.

A failing `check` is not a stop sign: `models`, `providers` and
`generate --dry-run` all run without a key, so the brief, the prompt and the
price can all be done first. See "Pricing a job with no API key".

## Before writing the prompt: the brief

The shared rules — the three tiers, one round of at most four questions, the
shape of a question, the "Let the AI decide" discipline, the order with the
approval gate, the fallback without `AskUserQuestion` — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
This section adds only this scenario's question set.

| Tier | UGC axes |
|---|---|
| **must-ask** | is there a product photo? It changes the whole route (see "People, products and what the API refuses"), and a photo that does not exist cannot be invented |
| **ask-if-open** | who is on camera, which action chain the clip follows, whether anyone speaks |
| **never-ask** | resolution, model, provider, duration when the user gave one, aspect ratio (vertical is this skill's default and saying so in the recap is enough). Two resolutions are **two rows in the cost table**, not a question |

Five axes, four question slots. If the round is full, ask in this order:
`Photo`, `On camera`, `Beat`, `Talk` — and let anything left fall to a default
named in the recap.

### The question set

| # | Tier | `header` | Question | Options (1 = recommended, last = delegation) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Photo` | Do you have a photo of the actual product? | **Yes — a local path (recommended)**: the real label and shape are locked into the opening frame, and everything the gallery collected that had to match a real SKU used one. **The photo must have no person in it** — not a hand, not a foot — or the job is refused at submission. / **No — describe it in text**: fine for a generic item; on a real product the label may drift. **No AI option** — a photo is a fact, not a taste. | No image attached and the user did not say there isn't one. |
| 2 | ask-if-open | `On camera` | Who is in frame? | **Hands only (recommended)**: the most common real unboxing shape, and it keeps faces out of a generated clip entirely — fewer anatomy risks, no identity to hold. / **A creator, filming themselves**: an arm's-length or a fixed low viewpoint — written as a viewpoint, never as a phone standing somewhere in the room (see "The capture is part of the fiction"); they are generated fresh from text, so they cannot be the same person in a second clip. / **A creator, filmed by someone else**: a friend holding the phone; allows a wider frame. / **Let the AI decide** — which means hands only. | The request doesn't say. |
| 3 | ask-if-open | `Beat` | What happens, in order? | **Unboxing (recommended)**: parcel → cut/open → lift the item out → turn it over → first use. / **First impression**: already unpacked, one use, one reaction. / **Before / after**: the state that motivated the purchase, then the result. / **Haul**: several items shown in one sitting. / **Let the AI decide**. | The request names a product but not an action. |
| 4 | ask-if-open | `Talk` | Does anyone speak? | **No — ambient sound only (recommended)**: room tone and the sounds the actions make; captions get added in an editor afterwards. / **One line at the end**: a single spontaneous-sounding sentence. / **Talking through it**: continuous commentary — budget the words per second, see "If the creator speaks". / **Let the AI decide**. | The request doesn't say, and the duration is long enough for a line. |

Not asked: aspect ratio (9:16 unless the user says otherwise), resolution and
duration (rows in the cost table), the model, the provider, the audio flag.

### Skip rows specific to UGC

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| a photo is attached, or a path is given | Photo | have one — and check it for hands, feet and faces before attaching |
| "unboxing", "just arrived", "opening the parcel" | Beat | unboxing chain |
| "review", "honest opinion", "what I think" | Beat + Talk | first impression, with a line |
| "no face", "just my hands", "POV" | On camera | hands only |
| "TikTok", "Reels", "Shorts", "vertical" | Aspect | 9:16, already the default |
| "for the landing page", "for the website" | — | that is probably `seedance-ad-creative`; check before assuming UGC |
| "polished", "cinematic", "premium", "hero shot" | — | the user is asking for the opposite of this skill — see "When NOT to use" |

### From answers to prompt — traceability

| Answer | Lands in |
|---|---|
| Photo: yes, path | `--frame-first-image PATH` (product alone), plus the anchor sentence at the top of the prompt; no `--aspect-ratio` flag — ⚠️ **so crop the photo to 9:16 first**, see below |
| Photo: no | a text PRODUCT line, and `--aspect-ratio 9:16` becomes effective |
| On camera | the CAPTURE line and what each beat says is in frame |
| Beat | the timeline's action chain |
| Talk | the AUDIO line, and a quoted line with a delivery note |
| Duration | `--duration` and the timestamps |

⚠️ **Those first two rows contradict each other on a landscape photo, and the
table used to hide it.** This file says 9:16 is the default and never asks
about it. But with a frame attached, `bytedance/seedance-2.5` forces
`aspect_ratio: adaptive` and the **clip takes the photo's shape** — so
attaching an ordinary landscape product shot, which is most product shots,
delivers a landscape clip. The vertical premise is cancelled by the very
route the table recommends, silently, and nothing errors.

**So crop the photo to the target ratio before attaching it.** That is a free,
local step, and it is what the measured run did: the product photo was cropped
to 9:16 (529x941) first, and the clip came back 480x854. Found by reading the
two rows against each other rather than by spending anything; the crop is the
fix, and putting the crop in the recap is how the user finds out it happened.

### The recap for this scenario

```
Brief:
- Product: the ceramic pour-over kettle — photo at /Users/me/shots/kettle.jpg (given)
- On camera: hands only (you chose)
- Beat: unboxing — parcel, open, lift out, turn, first pour (AI's pick)
- Talk: no dialogue, ambient sound only (AI's pick)
- Vertical 9:16, 10s, 480p draft — with a 720p row below
- Photo prep: your kettle.jpg is landscape, so I will crop it to 9:16 before
  attaching it — free and local. With a frame attached the clip takes the
  photo's shape, so an uncropped landscape photo would produce a landscape clip
- Note: the attached-photo route has one run behind it (8s/480p). It came back
  with the product right and two problems: a ~0.1s flash of the photo then a
  hard cut at the open, because the photo's background was not the scene; and
  a more polished look than the text-only run. The draft is still the
  experiment
```

Then the full prompt, then the cost table, all in one message — the order and
the rule for a change made at the gate are in `creative-brief.md`'s
`Order, with the approval gate`.

## What actually reads as UGC

Four positive levers. They are the substance of the clip; the AVOID list is
what stops the model reaching for its defaults underneath them.

### 1. The capture is part of the fiction — the phone is not

No other scenario in this repo has a CAPTURE line, and it is the single most
load-bearing sentence here. It carries three things nothing else supplies:
**where the frame sits**, **how imperfectly it is composed**, and **how the
lens misbehaves** — which together are most of what makes a clip read as
phone-shot. Write all three as properties of the shot: `a fixed viewpoint at
table height, a little low and a few degrees off level, so the near table
edge cuts across the bottom of the frame`; `the focus hunts once when the
hands move in`; `the exposure lifts when the white box fills the frame`. The
phrasing for the flaws is in the shared file's `Consumer capture` and
`Autofocus hunting (UGC texture)` rows; use it as written.

⚠️ **Never say where the phone is. It will be in the shot.** Measured on this
skill's one paid run, job `2ecbedec` (8s, 480p, 88 cents): the capture line
read *"the phone is propped against a biscuit tin at the back of the desk,
slightly too low and a little off-square"* — and the delivered clip has **a
phone sitting in the box, visible in every frame, with a small glowing
screen**, which also broke the same prompt's own `no legible text` clause.
The model has no concept of an off-screen camera. A noun given a position in
the room is set dressing, and set dressing is rendered. `propped against a
mug`, `on a tripod`, `wedged on a shelf`, `left recording on a bench` are all
the same trap, and the gallery's own UGC cases are written exactly that way
(`static phone propped on bathroom sink`), so the phrasing reads as
completely natural right up until you watch the clip.

**The split that works.** A phone named as *how the image was made* is a
format anchor and stays: `real phone capture texture`, `shot on a phone`,
`selfie viewpoint`. A phone named as *a thing at a place* is scene content
and has to go. Converting one is mechanical — `the phone is propped against a
mug at the back of the table, slightly too low` becomes `a fixed viewpoint
from the back of the table, at mug height and a little too low`. Identical
framing, no object. Then put **`a phone, a camera, a tripod or a lit screen
visible anywhere in the shot`** in AVOID as a backstop, phrased as objects,
which is the form this repo has measured holding (lever 4).

✅ **And the fix has now been generated, not just reasoned.** Job `ede33e6d`
(2026-09-17, 8s, 480p, 88 cents) ran the converted form — viewpoint wording,
no object, plus the AVOID backstop — and **six sampled frames contain no phone,
camera, tripod or lit screen**. The one candidate object, enlarged, is an
out-of-focus wooden desk item. So this is a rare pair: the failing
construction and its replacement have each been run once, on the same model
and tier. That is still one run each, and the conversion is a rule about
*wording*, not a guarantee about every room you describe.

**Nothing catches this before delivery**, which is why it is worth this much
space. That prompt passed `--dry-run`, passed `--print-payload`, and passed
this skill's own re-read-your-prompt-for-polish-words check. None of them can
see a rendered object. Only the extracted frames could.

⚠️ A frame that never re-frames is a tripod. Put one small correction in the
timeline — the view tilts up to catch the product, the framing drifts and
re-settles — as its own beat with its own stamp, and write it as something
**the frame** does, not as something a hand does to a phone. **A camera
behaviour written only as an adjective in a style line does not reliably
render**; the shared file's `A camera move needs its waypoint frames, not just
a verb` is the measured version of that, and it applies to sloppiness exactly
as it applies to an orbit.

### 2. One practical light, and let it be uneven

Name the source and where it is: a window to the left with the curtain half
drawn, one warm ceiling bulb, the blue-white of an overhead kitchen light.
Then say what it does *badly* — the near side of the product bright and the
far side falling into shadow, a colour cast on a white wall, a blown highlight
where the light hits gloss. The shared file's `The plastic look is designed
out, not forbidden` has the general form (name sources, let them fall off);
what UGC adds is that the unevenness is not a compromise to be minimised, it
is the evidence that nobody set up a light.

### 3. Framing that is a little wrong

The product entering frame off-centre and being corrected. The item's top
cropped for a second. A hand crossing the lens. Written as beats, not as a
style word. Two cautions:

- **Not so wrong that the product cannot be seen.** The clip still has a job.
  The shared `Camera language` note on readability outranking the effect is the
  right tie-breaker.
- **Imperfection is an event, so it needs a stamp**, for the reason in lever 1.

### 4. A real room, not a set — with one tension to manage

A UGC set is supposed to be cluttered: the counter has other objects on it,
the table has a used cup, there is a bag on a chair. **That directly conflicts
with the one measured rule this repo has about invented text.** The shared
file's `Unwanted text is designed out of the set, not forbidden in the list`
found, across four jobs, that a set with no lettered surface produces no
invented text and a set full of them produces it regardless of how strongly
the AVOID list forbids it — and a real room is full of them. Book spines,
packaging, a cereal box, a laptop.

The resolution is not to empty the room, which would cost the scenario its
whole point. It is:

- keep the **lettered carriers out of the frame or out of focus** — the
  shallow background a phone gives you at close range is doing that work
  already, and it is the one bit of optical softness that is UGC-native rather
  than cinematic;
- **name the carriers you do not want as objects** in the AVOID list, not as
  "text" — the same file records a bare "no text" failing on a busy set and an
  object-by-object exclusion holding on a desk;
- **accept the product's own packaging** as text you *want*, and lock it with
  a photo rather than describing it — see below.

## People, products and what the API refuses

Two measured `ofox-video-core` facts decide the route, and together they are
less restrictive than they first look:

- **A photoreal person in an attached frame is refused at submission** on
  `bytedance/seedance-2.5` (`input_moderation_failed`, nothing billed). It is
  a rule about the picture you attach. `--real-person true` lifts it —
  measured 2026-09-16 — but as an **authorisation** claim about a likeness
  the user has the right to use, not as a way past the check, so it is a
  question for the user and never a flag an agent adds:
  [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
  → "`--real-person true` lifts that refusal on 2.5".
- **A photoreal person generated from the prompt text is fine.** Several
  20–30 second text-to-video jobs built entirely around people have completed
  in this repo.

So a UGC clip with a person in it is not blocked; it splits:

| Half | How |
|---|---|
| The product must be exactly right (real label, real shape) | attach it as `--frame-first-image`, **with no person and no part of one anywhere in that image** — hands, feet and socks included |
| A person must appear | write them into the timeline as text, entering after the product is established |

That split is measured end to end on the ad scenario's job
`ac927785-92ef-4e28-97b9-ff8172ec5554` (a product-only first frame, a person
entering at 4s, the product's appearance unchanged at 19.6s). It is an ad, not
a UGC clip, so read it as the *route* being proven, not the genre.

**Hands are the UGC-native answer and they are also the safest one.** The same
job's lesson about anatomy — escalate how much of a body is in frame, keep the
full figure to one distant shot, never make a hand or a face the focal point —
matters more here than there, because a phone-close unboxing puts hands in the
middle of the frame by definition. Two things that help: keep the hand's job
simple (one action per beat, holding or turning rather than gesturing), and
keep the product, not the hand, as what the beat is about. A written size
limit on a limb is **not** a defence — one measured job wrote `only the
fingertips and the first knuckle ever visible` **twice**, once in the shot and
once in AVOID, and the render showed most of the finger and the hand to the
knuckles anyway. What kept that shot anatomically clean was the macro framing
and one simple action, not the limit.

**No person survives across jobs.** They are generated fresh each time, so a
second clip is a different creator. Only the product can be locked.

## The prompt template

Vocabulary is not repeated here — timestamp formats and segment lengths,
transition phrasing, camera and focus terms, the negative-list rows, asset
role sentences are all in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
What follows is the UGC shape.

If several images should supply appearance without locking the opening frame,
use the shared
[`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy).
Do not reproduce its payload or limits here; this file owns only the UGC role
each image plays.

Slots in `<angle brackets>`; optional lines in `[square brackets]`.

```
STYLE: <consumer-capture anchor, from the shared file's Consumer capture row — real phone capture texture, sensor noise, compression artefacts, autofocus hunting, exposure shifts>. Vertical. Nothing is graded, lit or staged.
CAPTURE: <the viewpoint, as a property of the shot and never as a phone standing somewhere: a fixed viewpoint from the back of the table, at mug height and a little too low, so the near table edge cuts across the bottom of the frame | a close handheld viewpoint that drifts and re-settles | an arm's-length frontal viewpoint>. <Its flaws for this clip: the focus hunts once when the hands move in; the exposure lifts when the white box fills the frame.>
SCENE: <a real room, named: a kitchen counter at the end of the day | a desk with the day's things still on it>. <The one light source, and where it is.> <What it does badly: the near side bright, the far side in shadow.>
PRODUCT: <shape, material, colour, and any text on it verbatim in quotes>.
         [@image1 supplies the product exactly — <shape, label, colour>; ignore its background.]
[PERSON: <only what is in frame — two hands, adult, no jewellery | a person in their 20s in a grey hoodie, seen from the chest up>. <No name, no wardrobe manifest: this is not a character that has to survive anything.>]

0–<N>s    <one ordinary action>. <What the frame does about it: it sits a touch low, the focus hunts, the view tilts up.> <the sound this action makes>
<N>–<M>s  <the next action in the chain — no transition word; these are beats in one continuous shot unless the clip genuinely cuts>
…
<…>–<T>s  <the last action just finishes>. <The shot keeps running for a moment after it.>

AUDIO: <room tone of the actual room>, <two or three sounds the actions make: cardboard tearing, tape, a lid, a cup on a counter>. [<Speaker>: "<one line, in the language to be spoken>" — spontaneous, slightly breathless, not scripted.] No music.
AVOID: <the UGC anti-polish row from prompt-structure.md's Negative list — the frequent items, quoted as written>; plus: a phone, a camera, a tripod or a lit screen visible anywhere in the shot; tripod stability, gimbal smoothness, a studio or seamless backdrop, a professional model or presenter, an advertising voiceover, a slogan, a logo card, an end card; <the lettered objects in this room you do not want: book spine, cereal box, magazine, laptop screen, poster>; music, score, soundtrack, instrumental, percussion, humming, singing.
```

Six things about that shape:

- **`CAPTURE:` describes the shot, never the phone**, and the AVOID list names
  the device as an object anyway. That slot was `DEVICE:` and read "where the
  phone is", which put a phone in the delivered clip on run `2ecbedec` — the
  ⚠️ under "The capture is part of the fiction" has that measurement. **The
  corrected wording has since been run and held**: job `ede33e6d`
  (2026-09-17), six sampled frames, no phone, camera, tripod or lit screen
  anywhere. So this line now has a measurement on **both** sides — the
  construction that fails and the conversion that fixes it — which is the
  strongest evidence any single line in this template carries. One run each;
  the conversion rule is still worth re-reading before you write the slot.
- **No header FORMAT line and no shot manifest.** UGC clips are short and
  single-shot; the shared file's `Short prompts (10 seconds or less)` says to
  skip the manifest, and a manifest is itself a tell.
- **The timeline is beats inside one continuous shot, not cuts.** Say
  `one continuous shot` in the first sentence if you mean it — the shared file
  records that a timestamped list without that declaration reads as a cut
  list. A real phone video does sometimes cut (they stopped and restarted);
  if you want that, say `hard cut` explicitly, because an unnamed boundary
  becomes one anyway.
- **No climax and no hero frame.** The chain just ends. Case 25's ending is
  the UGC close — but write it as `the shot keeps running for a moment`, not
  as case 25's own `the camera continues recording for a moment`, for the
  reason in the bullet above: the close is the last place you want to hand the
  model a device to render.
- **No music, ever.** Not a taste rule: a prompt asking this model for music
  came back `output_moderation_failed` on audio copyright in this repo
  (unbilled). Ambient and action sounds only; a track goes on in an editor.
  The shared file's `Asking for music can fail output moderation on copyright`
  has the measurement. Case 25 also lists music under STRICTLY AVOID for
  genre reasons, so both arguments point the same way.
- **The AVOID slot is a quote, not a paraphrase.** Open
  `prompt-structure.md`, find the UGC anti-polish row, and put its wording in.
  If that file is out of reach, see "If the script isn't found" — this is the
  one thing in this skill that genuinely degrades without it.

### Worked example — a 10-second vertical unboxing, hands only

Text-to-video, no photo. **This example has not been generated as written** —
it is the template filled in, not a clip anyone has paid for. Its `CAPTURE`
line and its last two beats are the *corrected* form of the construction that
put a phone in the shot on job `2ecbedec`. **That correction is no longer
reasoning alone**: the same corrected construction was generated on job
`ede33e6d` (2026-09-17, with a photo attached) and no device appeared. This
particular filled-in example is still unrun; the shape of its `CAPTURE` line
has a run behind it.

```
STYLE: real phone capture texture, slight sensor noise and compression artefacts, mild autofocus hunting, exposure shifting when a bright surface enters the frame. Vertical, one continuous shot. Nothing is graded, lit or staged.
CAPTURE: a fixed viewpoint from the back of the table, at mug height and a little too low, so the near table edge cuts across the bottom of the frame and the box sits right of centre. The focus hunts once when the hands move in, and the exposure lifts when the white box fills the frame.
SCENE: a kitchen table at the end of the day, a used cup and a set of keys pushed to one side. The only light is a window to the left with the curtain half drawn, so the near side of everything is bright and the far side falls into shadow; a cool cast on the white wall behind.
PRODUCT: a matte black cylindrical hand grinder with a walnut knob and a folding steel crank, in a plain white cardboard box with no printing on it.
PERSON: two adult hands, no jewellery, sleeves pushed up. Nothing above the wrists is ever in frame.

0-3s    a hand slides the white box into the middle of the table; it arrives off-centre and the far corner is cropped, and the hand nudges it straight. The focus hunts briefly on the tabletop before settling. Sound: cardboard on wood, a chair creaking off-screen.
3-6s    both hands work the tape at the seam, pull it off in one go and drop it beside the box; the flaps come up. Sound: tape tearing, the flaps.
6-8.5s  one hand lifts the grinder out. It comes up slightly out of frame at the top and the view tilts up a few degrees to catch it, then settles. The exposure drops as the dark body fills the frame.
8.5-10s the hands turn it over once, the crank folds out, and they set it down on the table. The shot keeps running for a moment after the hands stop.

AUDIO: kitchen room tone, a fridge hum, cardboard, tape, the crank clicking out, the grinder set down on wood. No dialogue. No music.
AVOID: cinematic color grading, beauty filters, artificial skin smoothing, dramatic slow motion, music, perfect lighting; no beauty filter, grading, cinematic/CG look, fisheye, vignette, or legible text; a phone, a camera, a tripod or a lit screen visible anywhere in the shot; tripod stability, gimbal smoothness, a studio or seamless backdrop, a professional model or presenter, an advertising voiceover, a slogan, a logo card, an end card; book spine, magazine, cereal box, laptop screen, poster, printed packaging other than the plain white box; music, score, soundtrack, instrumental, percussion, humming, singing; warped or extra fingers.
```

The AVOID list's first two clauses are the shared file's UGC anti-polish row
verbatim — that is what "quote it" means. Everything after them is what this
scenario adds on top.

⚠️ **One clause in that row fights a real product, and you have to notice
it.** It ends `…fisheye, vignette, or legible text` — written for a
text-only clip where every letter would be invented. If the brief is an
unboxing of a **real** product whose label the user wants readable, a blanket
`no legible text` is now pointed at the thing they are advertising. The
example above dodges it by giving the product a plain unprinted box, which is
a legitimate choice and not the only one. When the label has to be legible:

- **lock it in an attached first frame** rather than describing it — text
  approved on a still and then preserved is the reliable route, measured in
  this repo, and text rendered from a description is the classic failure;
- **drop the `legible text` clause** from the quoted row and replace it with
  the specific carriers you don't want (the lettered objects already listed in
  the AVOID slot), so the prohibition removes the background signage without
  removing the product's own label.

That is the one edit to the shared row this scenario routinely needs. Make it
deliberately and say you made it.

## If the creator speaks

One line usually beats a script. The shared file's
`Dialogue and sound` → `Density — two tiers, not one` gives the measured word
budgets: a talking-head runs about 3.5 words a second and a drama far below
that, so a 10-second clip of continuous commentary is a talking-head budget
and a single closing line is nowhere near it. Write the line in the language
it should be spoken in — that is what decides the voice's language.

The delivery note is where UGC lives: `spontaneous, slightly breathless, not
scripted` (case 25), a false start, a word repeated. An advertising cadence
in a handheld clip is the polish leak in audio form.

`--generate-audio` defaults to `true` on the server, which is what you want
for ambient sound. Set it `false` only if the user is laying their own audio
over the clip.

## Vertical by default

`--aspect-ratio 9:16` on pure text-to-video. Two things to know:

- **With a photo attached the flag stops being yours.** `ofox-video-core`
  forces `adaptive` on `bytedance/seedance-2.5` and defaults to it on other
  models that offer it, so the output follows the image. **Crop the photo to
  9:16 before generating — crop, never pad**, since padding bakes the bars
  into the video. Relay the `NOTE:` the script prints.
- **Not every model offers 9:16.** Aspect-ratio lists differ per model and
  they are catalog facts, so read them rather than assuming:
  `ofox-video.sh models`. A ratio the model doesn't have is rejected locally,
  free, before anything is submitted.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--aspect-ratio` | `9:16` on text-to-video; **not passed** when a photo is attached | UGC is vertical by default; with a frame attached the photo's crop decides the shape |
| `--model` | the script's own default, **unless the user named one**, which always wins | the id the request will really carry is the `MODEL` line a `generate --dry-run` prints, and that is the id the cost table has to name. See "Choosing a model" |
| `--duration` | short — a draft at the model's minimum, a deliverable in the low tens of seconds | a flat action chain has no reason to run long, and every second bills. `ofox-video.sh models` prints each model's range |
| `--resolution` | draft at the model's cheapest tier, then re-render the keeper higher. When the user named neither, put the next tier up as a **second row of the same cost table** rather than asking | UGC is the one genre where a lower tier costs the least credibility — sensor noise and compression are in the brief. Still read the draft's frames before shipping it |
| `--generate-audio` | leave at the server default (`true`) | room tone and action sounds are half of what makes it read as real |
| `--seed` | let the script roll one and keep it | printed as `SEED` and written to the `.json` sidecar, which is what lets "that take, rendered properly" be re-submitted at all. It does **not** reproduce it: measured, an identical request on a fixed seed came back a visibly different clip. Say a re-render is another roll aimed at the same shot before the user pays for it |
| `--frame-first-image` | only when a product photo exists, and only if it contains no person | the measured product-lock route; see "People, products and what the API refuses" |
| `--real-person` | leave unset | this skill's route does not need it — the product is the attached frame and the person is written in text. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person reference images, measured lifting seedance-2.5's submission refusal on 2026-09-16: an authorisation route, never a way past the check, only offered when the user holds the right to that likeness and has said so, and never set on their behalf. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

## Choosing a model

The model stays **never-ask** — the agent doesn't raise it. But never-ask is
not "never listen": if the user names a model id or a shorthand, use it.

**Model ids, prices, resolutions, durations and aspect ratios are deliberately
not written down in this file.** They are catalog facts, they change, and this
repo has recorded defects that trace to a hardcoded copy of somebody else's
value table. Read them live, free, with no API key:

```bash
bash ../ofox-video-core/references/ofox-video.sh models             # every model, its tiers and ranges
bash ../ofox-video-core/references/ofox-video.sh providers MODEL    # that model's per-resolution rates
```

`providers` with no model argument prints the flagship's matrix, not the
catalog — pass the id you actually mean. And the rate `models` shows is the
one at each model's **own default resolution**, which differs between models,
so it ranks rather than quotes. The number you put in front of a user comes
from `generate --dry-run` at the parameters you are about to send.

Two things worth saying to a user who is choosing: a cheaper model is a
different look, not just a smaller bill — which cuts both ways here, since
this is the scenario least harmed by a rough one. And **moderation policy is
per-model**, so a prompt refused on one model can be accepted on another.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the required columns and where the numbers must come from are
written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

Get the numbers from `--dry-run`, which validates everything and prints the
estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 10 --resolution 480p --aspect-ratio 9:16 \
  --out-dir /absolute/path/to/out
```

Relay the `Estimated cost:` line it prints — never a number of your own — then
wait for a yes, then re-run the identical command with `--dry-run` swapped
for `--approved`. The estimate a *real* run prints comes microseconds before
the request goes out, too late to relay. Pass the same `--out-dir` to both:
the dry run creates and enters it, so a bad path fails as exit `6` with
nothing submitted.

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
The rule above is still the rule, and it is still yours to follow.

The brief recap goes in the **same message** as the prompt and the table,
above them.

**The one cost anchor this skill has**, with the parameters it was measured
at attached, because a figure without its parameters is not a measurement:
`bytedance/seedance-2.5`, 8 seconds, 480p, 9:16, text-to-video, audio on —
**88 cents billed** (job `2ecbedec`). It is not a quote for another duration,
tier, model or for an image-to-video job, and it must never be scaled by hand
into one. The dry run at the parameters you are actually about to send is the
only number to show a user; this anchor is there to sanity-check that the dry
run is in the right neighbourhood, never to replace it.

Afterwards the **actual** bill is `VIDEO_COST` from the finished job. Report
it as money, not as the raw ten-decimal string.

## Several takes, and the cheap vertical route

A UGC clip is a roll like any other, and this one has an extra reason to roll:
the thing being judged — "does it read as real?" — is exactly the thing the
prompt can ask for and not get.

For several takes of one prompt, `batch` prices the whole set up front, waits
for the takes concurrently, and tiles a contact sheet:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 4 --duration 4 --resolution 480p \
  --aspect-ratio 9:16 --out-dir /absolute/path/to/out
```

Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`, and give the takes a row
each — if one take in four is usable, that clip cost the whole total. Hand
over the `CONTACT_SHEET` path on its own line, then the take paths beneath it;
each `TAKE` line carries `seed=N`.

**If the user wants several vertical drafts to choose from as the actual
deliverable — Shorts or Reels raw material rather than one clip —
[`shorts-reels`](../shorts-reels/SKILL.md) is that scenario**, and it carries
the cheap-tier ladder and the draft-then-promote flow. The two compose: write
the prompt with this skill's template, run the set through that one.

## Pricing a job with no API key

`models`, `providers` and `generate --dry-run` all work with `OFOX_API_KEY`
unset. So when a user hasn't signed up yet, **quote the job first and let them
decide whether it's worth registering** — don't open by sending them to a
signup form.

## If the script isn't found

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

Nothing is broken — this skill delegates all execution to `ofox-video-core`
and reaches it by relative path, and that path just missed. Two different
situations wear this message, so run the probe in "Where the core skill lives"
before deciding which:

- **The probe printed a directory** — the core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-video-core`). Re-run against what the probe printed.
- **The probe printed nothing** — `ofox-video-core` really is absent, and
  installing it is the user's call to make, not yours: an install writes
  outside this working directory, so hand over the command and let them run
  it rather than running it for them. Which command depends on the installer
  they already have — skills.sh is
  `npx skills add ofoxai/skills --skill ofox-video-core`, which asks for that
  one skill and answers none of the agent, scope or confirmation questions on
  the user's behalf; this repo's own wrapper is
  `npx ofox-skills ofox-video-core`, the same install with all three answered
  in advance (every agent, user-level, no prompts); on LobeHub or ClawHub,
  install `ofox-video-core` from the same publisher. Ask for the one skill
  that is missing rather than the whole repo, and give all three routes —
  pointing a LobeHub user at the skills.sh line alone reads as "abandon your
  installer", which isn't the advice.

Either way, name the missing skill and where it was expected rather than
relaying the raw path error, which names neither.

A broken link to a shared reference has the same two causes. **This skill
degrades more than most when that happens**, and it is worth saying so: the
question set, the template, the four levers and the defaults are all written
out here, but the anti-polish AVOID list is deliberately *not*, and that list
is half the brief. Without it, write the AVOID slot from the four categories
named in "Where the anti-polish vocabulary lives" — grading, beauty filters
and skin smoothing, dramatic slow motion, perfect lighting and the CG look —
and tell the user the canonical wording was unavailable.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md).
The ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely |
| `2` | Environment problem — `curl`/`jq` missing, or no `OFOX_API_KEY` | Ask the user to fix it; `check` reports the same |
| `3` | API rejected it, or the job ended failed/cancelled/expired | Read the mapped message; a rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `generate` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID` |

## How long to tell the user it will take

`generate` blocks while it polls, up to `--max-wait` (default 540s). A short
low-resolution vertical clip is usually one to three minutes. Say so before
starting, so the wait isn't silent.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) followed by `poll`. That way a timeout can never strand a
job whose id you never saw. For `batch`, the worst case is `takes x max-wait`
— lower `--max-wait` for drafts, or create and poll the takes yourself.

## Where the file lands

Always pass `--out-dir`, and **make it an absolute path**. Without it the
script writes to the current working directory — which, given that the
examples here run from this skill's own directory, would drop the user's video
inside an installed skill. Relay the **absolute** `VIDEO_PATH` the script
prints, on its own line.

Pass `--name` too — name the file after the clip rather than leaving the
script to guess from the prompt's opening words, which here describe a phone's
sensor noise. The clip lands as `<name>-<short job id>.mp4` with a `.json`
sidecar holding the full job id, the prompt, the seed and the real cost.

## Generating

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the UGC prompt built above>" \
  --name "<short clip name, e.g. hand grinder unboxing>" \
  --duration 10 \
  --resolution 480p \
  --aspect-ratio 9:16 \
  --out-dir /absolute/path/to/out
```

Drop `--aspect-ratio` when a product photo is attached — see "Vertical by
default".

`--approved` is not decoration: without it the script refuses, submits
nothing, and prints the quote-first steps instead. Add it only once the cost
table has actually gone in front of the user and come back with a yes — the
flag cannot check that for you.

This one call validates the parameters, submits the job, polls to completion,
downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, `SEED` and `VIDEO_COST`. Report the **actual** values from
that output — never the estimate, and never a path or cost you didn't see the
script print. Do not re-implement any of the request, poll or download logic
here.

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| The clip is beautiful and reads as an ad | Polish leaked in — style words carried from another scenario, a climax beat, or a camera that behaves | Re-read the prompt for `cinematic`, `studio`, `professional`, `film grain`, `rim light`, `shallow depth of field`, `slow motion`; flatten the beat chain; put the phone's misbehaviour in the timeline as stamped beats rather than in a style line. See "The inversion". New prompt, new cost table |
| A phone, camera or tripod is visible in the shot, sometimes with a lit screen | The prompt gave the filming device a position in the room, so the model treated it as set dressing. Measured on job `2ecbedec`, from the phrasing `the phone is propped against a biscuit tin at the back of the desk` | Rewrite the `CAPTURE` line as a viewpoint (`a fixed viewpoint at desk height, a little low and off-square`), convert any beat that has a hand touching the phone into something the frame does, and add `a phone, a camera, a tripod or a lit screen visible anywhere in the shot` to AVOID as objects. New prompt, new cost table — nothing in the tooling can catch this before delivery |
| The camera is smooth despite "handheld" | A camera texture written once as an adjective. The shared file's measured rule is that a move written only as a verb tends not to happen; the same applies to instability | Write the re-frame as a beat with its own timestamp, as something the frame does — "the view tilts up a few degrees to catch it, then settles" — never as a hand adjusting a phone |
| The lighting is flattering and even | The prompt named a light but not what it does badly | Name the source, its position, and the shadow or cast it leaves. Positive sentences, per the shared file's `The plastic look is designed out, not forbidden` |
| Invented signage or garbled lettering on the shelf behind | A real room is full of lettered surfaces, and the negative list is only partly obeyed on such a set (measured, four jobs) | Move the carriers out of frame or out of focus and forbid them **as objects** — book spine, box, magazine, laptop — not as "text". See lever 4 |
| Exit `3`, `input_moderation_failed` on an image job | The attached photo contains a person — a hand or a foot is enough | Attach a photo of the product alone and write the person in text. Nothing was billed |
| Exit `3`, `output_moderation_failed` mentioning audio copyright | The prompt asked for music | Rewrite AUDIO as room tone plus recorded sounds, keep the music words in AVOID, and re-run — a new request, safe immediately |
| Hands look wrong | Hands are the highest-risk anatomy and this genre puts them centre-frame | One simple action per beat, the product as the beat's subject rather than the hand, and no written "never more than X of the hand" clause — that was measured being ignored. Re-roll, or move to a wider framing |
| The product's label is wrong or drifts | Text rendered from a description is the classic failure | Attach a real product photo as the first frame; text approved on a still and then preserved is a different and reliable task |
| The clip has a music bed nobody asked for | `--generate-audio true` plus a prompt that didn't exclude music | Keep the music words in AVOID and name the ambient sounds you do want |
| Exit `1` on `--aspect-ratio 9:16` | The model doesn't offer that ratio | `ofox-video.sh models` lists each model's ratios. Nothing was submitted, so this is free to fix |
| The output isn't vertical even though 9:16 was passed | A frame is attached, so the ratio is `adaptive` and follows the image | Crop the photo to 9:16 and re-run. Crop, never pad |
| Exit `4`, timed out waiting | Still running upstream, not failed | `poll JOB_ID` with the id printed before the timeout; never re-run `generate` |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job exists | Don't guess or retry; tell the user to check https://app.ofox.ai |

## When NOT to use

- **A polished brand or product ad** — `seedance-ad-creative`. Its UGC-variant
  table is the ancestor of this skill; anything with a hero frame, a grade or
  a slogan belongs there.
- **Plain catalog or listing footage** — `seedance-product-video`.
- **A scene carried by people talking to each other** —
  `seedance-short-drama`. A creator talking to the camera about a product
  stays here; a conversation between characters does not.
- **Several cheap vertical drafts as the deliverable** — `shorts-reels`,
  which owns that ladder. Write the prompt here, run the set there.
- **The user can just film it.** A real unboxing on a real phone costs
  nothing, shows the actual product and cannot fail an authenticity check.
  Say so before quoting a job: this skill earns its keep when the product
  isn't in hand, when the volume is too high to film, or when the shot is
  needed before the stock arrives.
