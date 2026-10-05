---
name: seedance-product-video
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Generate a clean, catalog-style e-commerce product video from a real product photo (or, for a generic or fictional product, a text description) using the Ofox video API (Seedance 2.5) — runs a short creative brief (product photo, target platform and aspect ratio, background, camera orbit or turntable) when the request leaves them open, writes a plain-background, literal-accuracy prompt (precise product description, a simple camera orbit or turntable motion, no dramatic cinematography), shows a cost estimate, then calls ofox-video-core to submit, poll, download, and report the real cost. Use when a user asks to turn a product photo into catalog/listing footage, e.g. "make this product photo a 360-degree white-background showcase", "turn this photo into a white-background product video", "make a clean turntable video of this item", or "give me a 5-second white-background rotation video of this product for my listing". Do not use for cinematic brand/mood advertising (see seedance-ad-creative) or for anything involving people/dialogue (see seedance-short-drama).
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-product-video
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
    emoji: "📦"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-product-video
---

# seedance-product-video: clean e-commerce product showcase videos

Turns a product photo — or, for a fictional or prototype product, a text
description — into a plain-background catalog/listing clip: a precise product
description plus a simple camera move, written as timestamped waypoints,
become a Seedance 2.5 prompt, which this skill submits, polls, downloads, and
reports the cost for.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the product-video
prompt craft, the creative brief, recommended defaults, and the
pre-generation cost estimate; `ofox-video-core` owns talking to the Ofox API
correctly and safely (the `OFOX_API_KEY` handling, the no-resubmit rule,
error-code mapping, download/verification, and reporting the downloaded
file's absolute `VIDEO_PATH`). **Read that skill's safety contract before
using this one** — it is not restated here.

The prompt structure shared by every Seedance scenario skill — the vendor's
formula, timestamp formats and segment lengths, camera vocabulary,
consistency locks and negative lists, the two meanings of an attached image
— lives in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
Load it before writing a prompt. This file only adds what is specific to
catalog footage.

The rules for the questions that come **before** a prompt exists are shared
the same way, in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md);
the brief section below carries only this scenario's question set.

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
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the
conversation, and don't re-run this check on every subsequent request once
it has passed.

## Before writing the prompt: the creative brief

The shared rules are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md)
— the three tiers, one round of at most four questions, the shape of a
question, the "Let the AI decide" discipline, the generic skip rows, the order
with the approval gate, the fallback for a runtime without
`AskUserQuestion`, and the anti-patterns. Read it before writing a prompt.
This section adds only what is specific to catalog footage.

For catalog footage two of the axes are not taste at all: without the photo
the product may come out wrong, and without the ratio the photo cannot be
prepared, because once an image is attached the output ratio follows the image
and cannot be changed afterwards — a wrong ratio is a paid clip in the bin.
Zero questions is still common: "5-second white-background orbit of this mug
for my Etsy listing" plus an attached photo has settled every axis.

| Tier | Product-video axes |
|---|---|
| **must-ask** | is there a product photo? which platform, hence which aspect ratio? Both come **first** — the answers decide the prompt route and the crop applied to the photo. |
| **ask-if-open** | background, the camera motion |
| **never-ask** | resolution, model, provider, audio (off in this scenario), duration. 720p vs 1080p is **two rows in the cost table**, not a question. Never-ask means the agent doesn't raise it — not that an explicit user choice gets overridden: a model named by id or by a shorthand ("wan", "hailuo") is used instead of the `seedance-2.5` default. See "Choosing a video model" below. |

If four slots are not enough: the two must-ask items first, then
`Background`, then `Motion`; anything left falls to a default and the cost
table.

**Neither must-ask question carries a "Let the AI decide" option.** A photo
that does not exist cannot be invented, and a ratio chosen after the image
exists is too late. The aspect question fills its slot with four platform
options instead; if the user answers "I don't know" in free text, fall to
`1:1` and mark it `(AI's pick)` in the recap.

### The product-video question set

| # | Tier | `header` | Question | Options (1 = recommended) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Photo` | Do you have a photo of the product? A listing is compared against the real item, so the photo is what keeps the shape and label right. | **Yes — I'll give a local path (recommended)**: image-to-video from the real photo; every gallery prompt that had to match a real product or logo used an image (cases 12, 13, 24). / **No — describe it in text**: acceptable for a generic item or a fictional brand (the gallery's product prompts, cases 16–19, are all text-only and all fictional); for a real SKU the result may not match the item — I will say so. **No AI option.** | No image attached and the user did not say "no photo". |
| 2 | must-ask | `Aspect` | Which platform is this for? It fixes the frame shape, and with a photo I have to crop or pad the photo to that shape before generating. | **1:1 marketplace grid (recommended)**: Amazon, Etsy, Shopify, eBay listings. / **9:16 TikTok Shop and mobile storefronts**. / **16:9 website product-detail page**. / **4:3 legacy catalog template**. **No AI option** — four platform options fill the slot; a free-text "don't know" falls to 1:1, marked (AI's pick). | No platform or ratio in the request. |
| 3 | ask-if-open | `Background` | What should sit behind the product? | **Pure white (recommended)**: what most marketplace listing rules ask for; no props, no shadows on the backdrop. / **Light grey studio**: a soft neutral surface with true reflections (the gallery's cleanest product prompt, case 17, uses a bright reflective surface with softbox light). / **Keep the photo's own background**: the scene stays as shot, pinned in place (case 41 locks its background geometry rather than removing it). / **Let the AI decide**. | No background word in the request. |
| 4 | ask-if-open | `Motion` | How should the product be shown? | **Camera orbits, product still (recommended)**: every rotation in the gallery is written as camera movement or as a hand turning the product (`360-degree orbit`, official case 42; `the camera slowly circles the build platform`, case 39). Answering this does not settle how the segment gets written — the words "the camera orbits" produced no orbit at all on a real run, and the option only delivers in the **waypoint** form of "3. Camera motion: waypoint pictures, not a camera verb" below, each waypoint carrying its own shot size, whose spacing between angles is approximate rather than scheduled and which covers about **half a turn**, not a circuit, on both clips that have been measured. / **Product turntable, camera fixed**: the classic listing spin. No gallery prompt writes it this way, and it has one run here (job `dc02f604`, t2v, 2026-09-16): the product did turn on its own vertical axis with the camera fixed, and five seconds covered only **a quarter to a third of a turn** rather than the "most of one turn" asked for — so if the user said "360", say that a full circuit does not fit in 5 seconds before quoting. 🚨 **And at 5 seconds do not combine this with the detail option in one clip** — measured on job `54a721ce`, a one-second DETAIL still pushes all the way to macro and the three turntable seconds then happen inside that macro, which is not a listing clip. Pick one move per short clip; see "Scaling the timestamps does not scale the camera move". / **Slow push-in on a detail**: one feature fills the frame (cases 19, 24, 39) — **on its own** at short durations, for the same reason. / **Let the AI decide**. | No motion word in the request. |

Not asked: 720p vs 1080p (two rows in the cost table); duration (5s for a
single orbit, 10–15s for the segmented template — a row, and the recap says
which); model, provider, the audio flag (off here).

### Skip rows specific to product-video

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| a product photo is attached, or a path is given | Photo | have one → image-to-video; do not ask whether there is one |
| eBay, "marketplace", "main image", "listing grid" | Aspect | `1:1` |
| TikTok Shop, "mobile store" | Aspect | `9:16` |
| "product page", "detail page" | Aspect | `16:9` |
| "catalog template", "4:3", "legacy" | Aspect | `4:3` |
| "white background", "white", "cut out", "clean" | Background | pure white |
| "grey", "studio", "neutral" | Background | light grey studio |
| "keep the background", "as shot", "in place" | Background | the photo's own background |
| "orbit", "circle around", "camera moves around" | Motion | camera orbits, product still |
| "spin", "turntable", "rotate", "360 on its axis" | Motion | product turntable, camera fixed — ⚠️ **and if they said "360", correct the length before spending.** One run (job `dc02f604`, 5s, t2v) shows the motion itself works: the product turned on its own vertical axis with the camera fixed, nothing tipping or sliding. What it does **not** do is finish a circuit — five seconds covered a quarter to a third of a turn against "most of one turn" asked for. So take the user's word for the motion, and in the same breath tell them a full 360 will not fit in 5 seconds, so they can choose more seconds or accept part of the surface. 🚨 **A 5-second clip is one move**: the photo-attached attempt at this (job `54a721ce`) also carried a one-second DETAIL and spent its whole rotation segment in a cap macro, so the turntable is still unmeasured with a frame attached and the way to measure it is a clip with no DETAIL in it |
| "close-up", "zoom in on the detail", "push in" | Motion | slow push-in on a detail |

### From answers to prompt — traceability

Every answer has to be findable in the prompt or the flags.

| Answer | Lands in |
|---|---|
| Photo: yes, path | `--frame-first-image PATH`, the `@image1 supplies the product exactly` sentence in the PRODUCT block, and the crop/pad step before generating |
| Photo: no | a text-only PRODUCT block, an expectation note in the recap, and `--aspect-ratio` becomes effective |
| Aspect | the crop/pad ratio for the photo (image-to-video), or `--aspect-ratio` (text-to-video) |
| Background | the SCENE line: `pure white surface and backdrop` / `light grey studio surface` / `keep the background exactly as in image1` |
| Motion | the ORBIT segment's camera sentence, or the compact template's single motion sentence |
| Duration | `--duration`, and the timestamps in the timeline |

### The recap for this scenario

```
Brief:
- Photo: /Users/me/shop/mug-front.jpg (given) — I will pad it to 1:1 first
- Aspect: 1:1 (inferred from "Etsy")
- Background: pure white (you chose)
- Motion: camera orbits 360 degrees, product still (AI's pick)
- Duration / resolution / audio: 5s / 720p / off — one row below; 1080p as a second row
```

Then the full prompt, then the cost table, all in one message — the order and
the rule for a change made at the gate are in `creative-brief.md`'s `Order,
with the approval gate`. Here a ratio change also means re-padding the photo.

## Prompt template

Vocabulary is not repeated here. Timestamp formats and segment lengths:
`Segmenting the timeline`; the orbit, push-in, macro and static terms:
`Camera language`; the closing blocks: `Consistency locks and the negative
list`; asset role sentences and the two image semantics: `Reference assets as
visual anchors`; freeze and settle endings: `Endings` — all headings in
`../ofox-video-core/references/prompt-structure.md`. What follows is the
catalog-specific shape.

The gallery's product prompts (cases 16–19, 37–41) share a first line that
names the format and places the product, a product block built from
material, colour and physical words rather than adjectives, and a short
action chain of three or four beats with one action per beat. The closing
blocks are common but not universal: a consistency lock in cases 19, 39 and
41, a negative list in 18, 38, 40 and 41, a technical tail in 16, 17, 19 and
39. None of the nine is a white-background listing clip — they are ads and
demos — so the plain background below is a marketplace convention, not a
gallery observation. The beat structure and the locks are the gallery's.

### Full template — 10–15s, three or four segments

One action per segment (case 18: `Show only one salon action at a time. Each
action must last long enough to show the process clearly`), 3–5s each (case
39 runs 4/3/4/4; case 41 about 2s per outfit). Slots in `<angle brackets>`;
optional lines in `[square brackets]`. `a`/`b`/`c` scale to the chosen
`--duration` — see "Scale the segments, don't copy the stamps" below the
template.

```
[<N> seconds, <1:1 | 9:16 | 16:9 | 4:3>.]                                  — optional; must match the flags (cases 18, 39, 41 write it; the vendor says it is not needed)
PRODUCT: <product name>, <main colour> with <accent colour>, <material and finish>, <shape and structural points>[, printed text verbatim: "<text>"][, accessories: <A>, <B>, <C>].
         The product stays identical in shape, colour, proportions and label throughout.          (cases 19, 24, 39, 41)
         [@image1 supplies the product exactly as it is; ignore its background.]
SCENE: the product centered on a <pure white | light grey | matte neutral> surface against a <pure white | neutral> backdrop; even studio softbox lighting, soft true reflections, no props, no shadows on the backdrop. Background and light do not change.   (case 17 for the surface and light; the white is a listing convention)

0–<a>s     [REVEAL, optional — <the box lid lifts away | a hand moves away from the lens | the product fades up from dark> to show the product]   (cases 17, 19, 41)
           | <static front view, product centered, camera still>.
<a>–<b>s   DETAIL — the camera pushes in to a macro of <the seam | hinge | logo | fabric weave>; reflections slide across the surface.   (cases 19, 39, 24)
<b>–<c>s   ORBIT — one single continuous camera move, no cut anywhere inside this segment. The camera travels around the product at constant height and constant speed, the product centered the whole way, and the frame shows a new side as it goes: at about <t1>s <what is in shot and what is out of sight — an appearance description, not a camera position>, <with the whole product in frame, <top> to <bottom>, and margin around it>; at about <t2>s <the same, for a view the first one could not see>, <the same framing clause again>. At every one of those views the entire product is inside the frame, nothing cropped. The product does not move, does not rotate on its axis and does not tip.   (the orbit is cases 42, 39; the waypoint form and the per-waypoint framing clause are both measured — "3. Camera motion" — and the budget and the loose timing are section 4. **Expect the move to cover about half a turn and stop there**: a written `by <c>s the camera is back on the exact front view of the opening shot` has now failed to bring the camera home on both measured clips, so if the clip must end on the opening view, put it in the next segment after the cut)
           | TURNTABLE — the product rotates slowly and steadily on its own vertical axis at a constant speed; the camera is completely fixed and centered, and the product stays in exactly the same place in frame and never tips, slides or floats.   (no gallery prompt; one run here, job `dc02f604` — the axis rotation and the fixed camera both landed, and no degree count is written because the one that was asked for did not)
<c>–<N>s   [ACCESSORIES — <A>, <B> lie on the surface to the <side> of the main unit and only to the <side>, both on the same line, evenly spaced and not touching each other or the product; nothing lies to the other side of the product; a slow macro pan across them]   (case 17; the "only to the <side>" wording is measured — the left/right axis holds, the same line does not, see the slot notes)
           | back to the front view; hold the final frame.   (cases 39, 40)

SOUND: none.                                                                — and `--generate-audio false`
AVOID: subtitles, logo overlays, watermarks, interface graphics; deformation, parts clipping through each other, duplicated accessories; floating objects; camera shake, zoom, sudden reframing; fast cuts, jump cuts; a CGI look.   (cases 38, 40, 41, 18, 24)
hyper-realistic textures, realistic reflections, smooth 60fps motion, 4K.   (cases 16, 17, 19, 24, 39 — a gallery habit, effect unverified; resolution comes from --resolution, not the prompt)
```

**Scale the segments, don't copy the stamps.** REVEAL, DETAIL and ORBIT
alone already run to about 12s at their default lengths, so a literal
`0–3s / 3–7s / 7–12s / 12–<N>s` reading only fits a 15s clip — at 10s or 12s
it leaves ACCESSORIES zero or negative seconds. Scale `a`, `b` and `c` to
the `--duration` actually chosen instead. The worked example below keeps the
same shape at a shorter total (3/6/10/12): REVEAL and DETAIL get one beat
each, ORBIT gets the single largest share because showing the product from
every angle is the point of a catalog clip, and ACCESSORIES — the one
segment that isn't the product itself — stays the smallest, 2–3s, never the
majority of the clip.

### 🚨 Scaling the timestamps does not scale the camera move, and at 5s that ruins the clip

**Measured 2026-09-17, and the result was unusable** — the first outright
failure of this template rather than of one segment inside it. Job
`54a721ce-61a1-46cf-b5bf-6973f31b8258`, seed `89984235`, 5s / 480p / 16:9,
`--generate-audio false`, a **real product photograph** attached as
`--frame-first-image`, timestamps scaled exactly as the paragraph above
instructs: `0–1s` static front, `1–2s` DETAIL, `2–5s` TURNTABLE.

| Time | What is on screen |
|---|---|
| 0.0s | the whole product, white background, wordmark legible — **the attached photo, anchored correctly** |
| 2.0s | **a macro of the cap** |
| 3.0 / 4.0 / 4.9s | still a macro of the cap |

So three of the five seconds — the entire turntable segment — happen inside a
macro, and the clip never returns to the whole product. As "a clean turntable
showcase for a listing", it is **not deliverable**.

**The cause is not the resolution and not the model.** A one-second DETAIL
push still pushes all the way to macro: shortening the segment shortened the
*time*, not the *distance travelled*. And nothing after it widens back out,
because the segment that follows inherits the framing it was handed — the same
inheritance already documented under "The orbit travels, but the product's
base or top is out of frame the whole way". The existing warning covered the
arithmetic (segments not fitting) and missed the physical consequence.

**The rule that follows, and it is a planning rule, not a prompt fix:**

> **At 5 seconds, do not put DETAIL in the same clip as TURNTABLE or ORBIT.**
> Pick one. A 5-second clip is one move. If the user wants both a detail and a
> rotation, that is either a longer clip or two clips, and both belong in the
> cost table as rows before anything is spent.

Where the boundary between "fine" and "ruined" sits is not measured — 12
seconds carries all four segments (three clips), five carries one. Nothing in
between has been run, so quote 8 or 10 seconds as an experiment rather than as
a known-good middle.

**Four segments do fit 12 seconds, and an uneven split is carried through.**
All three of this scenario's own clips were written at 3/3/4/2 in 12 seconds
— the worked example's own `3/6/10/12` stamps. The rejected one measured
3.12/2.88/3.7/2.3 and the third one 2.67/3.04/**4.00**/2.33, every segment
within 0.4s of plan and the orbit landing on its four seconds exactly
("Measured on this scenario's own clips" below).

Notes on the slots:

- **Write the consistency lock every time**, even though only some gallery
  prompts do — for a listing it is the whole point. The ones that carry it:
  `consistent diamond throughout the entire shot`
  (case 19), `Maintain perfect product consistency, including the frame
  shape, lenses, hinges, colors, materials, and proportions` (case 24), the
  dragon's `identity, anatomy, scale pattern, horns, wings and proportions
  must stay completely consistent` (case 39), `Keep every architectural line
  perfectly fixed across all cuts` (case 41).
- **Printed text goes in quotes, verbatim** (`yellow "Honey Crunch Cereal"
  box`, case 16). If the text must match a real package, that is a reason
  for the photo, not for more adjectives. **For a product that should carry
  no text at all, say so in the PRODUCT block and then exclude each carrier
  by name in AVOID** — `there is no printed text, no logo, no engraving, no
  etching and no marking anywhere on <each part>`, plus an AVOID list naming
  the product, the accessories, the surface and the backdrop one by one. That
  construction has produced a completely text-free set on all three of this
  scenario's text-to-video clips, including one whose accessory was a hard
  case lid — the classic place a brand name appears.
  ⚠️ **It only covers the surfaces you actually name, and a script that opens
  the product puts an unnamed one on camera.** In clip D the per-part list
  named the chest, the back, the sleeves, the hood and a sleeve patch — every
  one of them an outer surface — and the lining, which the presenter held open
  to the lens, came back carrying a neck brand label, a small tab and a
  care/spec panel. **If any beat opens, unzips, turns out or removes the
  product, extend the declaration to the lining, the inner collar and the
  inside of the pockets, and name the interior carriers in AVOID one by one**
  — neck label, care label, composition label, size tag, hang tag. That repair
  is inferred from the defect and has not been run.
- **Describe a part; do not count it.** The PRODUCT block's job is what each
  part looks like and where it sits — material, finish, colour, geometry. A
  count inside that description is the part most likely to drift: `a small
  barrel hinge of three interleaved knuckles` produced an interleaved barrel
  hinge with acetate on one side and the brushed bar on the other, held
  through a macro push-in and a full orbit, with **four** knuckle blocks in
  it. If a countable feature matters for a listing, check it on the draft —
  emphasis and a negative-list repeat have both failed to buy one ("Measured
  on this scenario's own clips", and `A description is honoured; a number
  attached to it is not` in the shared file).
- **The reveal is optional** and the only place the gallery's product prompts
  add any drama (a jewellery box opening, case 19; a storage box lid, case
  17; a palm leaving the lens, case 41). Keep it to one plain gesture; a
  cinematic reveal with mood lighting is `seedance-ad-creative`'s job.
- **Timestamps here are cut boundaries** between camera set-ups. Three shots
  in one job are verified on Ofox (see Several shots below); if the user
  wants the whole clip as one continuous move, drop the timestamps and use
  the compact template.
- **Write ORBIT as waypoint pictures, and give each one a shot size.** Naming
  the camera's move got no move at all on a real run; timestamped
  descriptions of *what the frame contains* got a camera that moved. The
  measurement — a controlled pair, one paragraph apart — plus what the
  waypoints did not buy is in "3. Camera motion: waypoint pictures, not a
  camera verb". What they do not buy is the **ending**: on both measured
  clips the move covered about half a turn and stopped, and the written
  return to the opening view did not bring it home.
- **A segment inherits the previous segment's framing unless told otherwise,
  and stating a shot size per waypoint has held once and failed once.**
  DETAIL sits immediately before ORBIT in this order, and on the first
  accepted clip the orbit stayed at DETAIL's macro closeness — several angles
  of the collar and the crank, the product's base out of frame the whole way,
  and one waypoint voided outright because it asked for a detail the
  inherited framing had already put outside the frame (§3). The third clip
  states the framing on every waypoint, keeps the same DETAIL-then-ORBIT
  order on purpose, and holds the whole product in frame with margin through
  the entire move. ⚠️ **A later ad clip in another scenario did the same
  thing and inherited the macro anyway** (`cb6b7870`, i2v, rejected — six
  frames of its orbit are all a close shot of the upper body). So write the
  shot size, because omitting it is measured to be worse, and then read a
  draft's frames instead of trusting it. **When the framing has to open up,
  the reliable place for the wider shot is after a cut** — both post-cut
  shot sizes in that same failing clip were delivered. §3, and the record
  in the shared file.
- **Name the side, and expect depth to slip anyway.** `in a row on the grey
  surface beside the standing grinder` split the row onto **both sides** of
  the product, identically in two clips. Writing `to the right of the glasses
  and only to the right ... nothing lies to the left` fixed exactly that — the
  left/right axis is controllable — while `both on the same line` did not: the
  cloth sits forward of and below the case rather than in line with it. One
  run each way, and on two accessories rather than the template's three. So
  name the side, and treat placement in depth as something to check on the
  draft rather than something the prompt settles.
- **`hold the final frame` buys a settle, not a freeze.** Two of the three
  clips held still through the last half second and one drifted visibly, from
  the same instruction — and the two that differ are the same-seed pair, one
  paragraph of prompt apart. Ask for it, expect the settle, and freeze in an
  editor when the last frame really has to stop.

### Compact template — 5s orbit

The single-motion clip most listings want. No segments, no header; vendor
formula order — subject first (shared file, `The vendor's own formula (ByteDance first-party)`).

```
<Product name>, <main colour>, <material and finish>, <shape point>[, "<label text verbatim>"]. Centered on a pure white surface against a pure white backdrop; even studio softbox lighting, true reflections, no props, no shadows. The camera orbits the product 360 degrees at constant height and speed; the product stays still and identical in shape, colour, proportions and label throughout. No subtitles, no logo overlays, no watermarks; no deformation, no floating parts; no camera shake, no zoom. Hyper-realistic textures, realistic reflections, smooth motion.
```

Swap the motion sentence for `The product rotates slowly and steadily on its
own vertical axis at a constant speed; the camera is completely fixed and
centered. The product stays in exactly the same place in frame and never tips,
slides or floats` when the brief chose the turntable. That is close to the
sentence that actually ran at 5 seconds (job `dc02f604`), and it is what
produced a real axis rotation with a fixed camera. **Leave the degree count
out of it** — the run asked for "most of one turn" and delivered a quarter to
a third, so a number there buys nothing and sets an expectation the clip will
not meet. The turntable phrasing still has **no gallery source**; it is the
listing convention, now with one run behind it. Sources for the rest: 5s +
`360-degree orbit` from official case 42;
surface and light from case 17; the lock from cases 19 and 24; the negative
list from cases 38 and 41.

**The compact template's own orbit sentence is the phrasing that failed at 12
seconds**, so at 5 seconds it is untested rather than safe: nothing in this
repo has run the one-sentence form. If the clip has to show more than one
side, prefer the full template's waypoint ORBIT even at a short duration, and
read the draft before paying for the final — see "3. Camera motion: waypoint
pictures, not a camera verb".

### Worked example — adapted from case 17

The community hair-dryer reveal, moved from prose into the full template at
12 seconds, 1:1. The original's purple leather storage box and "minimalist
luxury" wording are dropped for catalog neutrality; the lid reveal, the
copper-accent product block, the accessory row and the technical tail are
the original's. Timestamps are added.

Its ORBIT and ACCESSORIES segments are the two lines here that are neither
the original's nor a plain translation of it. Until 1.10.0 the orbit read
`the camera orbits the dryer 360 degrees at constant height; the product does
not move` — the exact phrasing that produced no orbit on a real run — so it is
written in the waypoint form that did produce one: two interior pictures as
appearance descriptions, each carrying its own framing clause, which is the
budget a four-second orbit was measured to absorb. **The closing return to
the front view is gone from it as of 1.11.0**, because it did not bring the
camera home on either measured clip; that view belongs in a shot of its own
after a cut. And ACCESSORIES now names a side, because `beside` was read as
"on either side of" twice ("3. Camera motion: waypoint pictures, not a camera
verb" and section 4 below; the slot notes above for the accessory reading).

```
12 seconds, 1:1.
PRODUCT: a hair dryer, deep blue body with copper accents, matte finish with polished copper trim, slim cylindrical barrel with a round rear intake; accessories: straight nozzle, diffuser nozzle, styling barrel. The product stays identical in shape, colour, proportions and trim throughout. @image1 supplies the product exactly as it is; ignore its background.
SCENE: the product centered on a pure white surface against a pure white backdrop; even studio softbox lighting, soft true reflections, no props, no shadows on the backdrop. Background and light do not change.

0–3s    REVEAL — a plain white box lid lifts away, showing the hair dryer standing upright.
3–6s    DETAIL — the camera pushes in to a macro of the copper trim and the intake grille; reflections slide across the surface.
6–10s   ORBIT — one continuous camera move, no cut inside this segment. The camera travels around the standing dryer anticlockwise at constant height and constant speed: at about 7s the copper trim reads as one thin bright line along the barrel and the nozzle mount is out of sight, with the whole dryer in frame from the top of the barrel to the base and margin around it; at about 8.5s the round rear intake grille fills the centre of the frame and no part of the nozzle mount shows, with the whole dryer in frame from the top of the barrel to the base and margin around it. At every one of those views the entire dryer is inside the frame, nothing cropped. The dryer does not move, does not rotate on its axis and does not tip.
10–12s  ACCESSORIES — the three nozzles lie on the surface to the right of the dryer and only to the right, in one line, evenly spaced and not touching each other or the dryer; nothing lies to the left of the dryer. A slow macro pan travels left to right from the dryer across the nozzles. Hold the final frame perfectly still for the last half second.

SOUND: none.
AVOID: subtitles, logo overlays, watermarks; deformation, clipping; floating objects; camera shake, zoom, sudden reframing; fast cuts.
hyper-realistic textures, realistic reflections, smooth 60fps motion.
```

## Measured on this scenario's own clips

Until 2026-09-05 this skill had generated nothing of its own — every figure it
quoted came from the gallery, from `seedance-ad-creative`'s product jobs, or
from `ofox-video-core`'s two three-shot test runs. It now has three, and they
come in two parts. Clips A and B are a controlled pair: **same seed
(`642303335`), same model, same flags, the same prompt text except one
paragraph** — the ORBIT segment. Clip C is an **independent** run a day later
on a different product at a different seed, written for one purpose: to test
the two fixes clip B's defects had produced. All three are
`bytedance/seedance-2.5` on `byteplus`, **pure text-to-video with no image
attached**, 12s, 720p, `--aspect-ratio 16:9`, `--generate-audio false`, billed
2.88 USD each (8.64 USD for the three).

**Three more clips sit outside that set and are written up where they belong.**
Clip D is a 30-second presenter clip that breaks this skill's own people
exclusion on purpose — "One clip outside this skill's own boundary" below.
Clip E is the **turntable** run of 2026-09-16 (job
`dc02f604-6c83-4837-b7fb-88e8df1876fb`, 5s, 480p, 1:1, t2v, 55 cents), which
finally puts a run behind the motion option the skip table has always pointed
at; it lives with that option, in "The turntable alternative: it works, and
its speed does not listen" under §3.

Clip F is the one that matters most to how this file should be read: the
**first run of this skill's headline route** — a real product photograph
attached as the first frame (job `54a721ce-61a1-46cf-b5bf-6973f31b8258`,
2026-09-17, 5s, 480p, 16:9, 55 cents). Until it, every clip above was **pure
text-to-video with a fictional product**, while the skill's own description
leads with turning a real product photo into listing footage. Its verdict is
split and both halves are load-bearing: **the photo anchor works** (frame 0 is
the photograph, wordmark legible) and **the delivered clip is unusable**,
because a one-second DETAIL segment pushed to macro and the three turntable
seconds happened inside it. Written up in 🚨 "Scaling the timestamps does not
scale the camera move" under the template, and in the turntable section.

| | Job | Outcome |
|---|---|---|
| Clip A | `1cf5ac46-058f-4615-a47b-067743f76f8c` | rejected — the ORBIT segment delivered no new angle |
| Clip B | `50f623b2-c54a-4d9d-9646-31dd06e2a926` | accepted 2026-09-05 |
| Clip C | `8efeb556-bf38-45ec-940b-a792ef74bfcf`, seed `616202922` | accepted 2026-09-06 |

The pair's subject was a fictional hand coffee grinder — walnut body, brushed
steel collar and crank arm, knurled steel base ring, accessories a glass jar
with a steel lid, a steel scoop and a wooden-handled brush, and **no printed
text anywhere by design** — written with the full template's four segments at
3/3/4/2. Versions in force when they ran: this skill 1.8.0, `ofox-video-core`
1.15.0. Clip B is the gallery's first `ofox`-sourced case in the
`product-video` category (`n: 1009`; the category's other four are
community-sourced).

Clip C's subject is a fictional pair of eyeglasses, chosen because it puts
every open question in one frame: a tortoiseshell acetate front holding two
clear lenses, two slim flat brushed-titanium temples folded flat against the
back, barrel hinges asked for as three interleaved knuckles — the one count
that drifted, see below — accessories a closed hard case and a folded
microfiber cloth, and again **no printed text anywhere by design**.
Same four segments at 3/3/4/2, delivered 2.67/3.04/4.00/2.33. It is
`n: 1011` in the gallery, and the two things it was built to test are the
per-waypoint shot size and the accessory placement — so it keeps the
DETAIL-macro-immediately-before-ORBIT ordering that caused clip B's framing
defect, rather than sidestepping it.

The ORBIT material is the headline finding and lives with the rule it
produced, in "3. Camera motion: waypoint pictures, not a camera verb". The
rest of what the template delivered:

| Slot | What was written | What rendered |
|---|---|---|
| REVEAL | a plain light grey box lid lifting straight up and out of the top of frame | exactly that — the optional reveal slot works as documented |
| DETAIL | macro on the knurled ring and the metal/wood seam, a slow straight push-in, a highlight sliding along the grooves | exactly that |
| ORBIT | clip A: the camera's move named. Clip B: four timestamped moments — three interior views and the return, none of them carrying a shot size. Clip C: three moments — two interior views and the return — **each with its own framing clause** | clip A: nothing. Clip B: the camera moved; two of the three interior views appeared, unevenly spaced, at the inherited macro closeness; about 180 degrees observable and the total **unmeasurable**. Clip C: **both** interior views appeared, both at their written framing, the whole product in frame throughout — and the move went front → side → rear and stopped, so the closing return did not land. Sections 3 and 4 |
| ACCESSORIES | clips A and B: three named items **in a row, beside** the standing grinder. Clip C: two named items **to the right and only to the right**, on the same line, with `nothing lies to the left`. All three: evenly spaced, not touching, **only in the final segment** | the items themselves: exactly that in all three — correct items, no duplication, none appearing early. AVOID named `no accessory appearing before the final segment` and `no duplicated accessory`, the two failure modes this slot risks, and all three prevented both. **The placement is half fixed**: `beside` split the row onto both sides in A and B identically; clip C's side constraint held and its single-line constraint did not — see below |

And what else the three showed — first the things that held, then the ones
that did not or that hold only with a hedge:

- **Zero invented text on all three, with no first frame to anchor
  anything.** The pair's set was bare metal, glass and wood — the glass jar's
  brushed steel screw lid is exactly where a brand name shows up, and it
  stayed blank. Clip C raised the difficulty on purpose: tortoiseshell
  acetate, brushed titanium, clear lenses, a dark hard case and a cloth, and
  a **hard case lid**, which is the classic carrier for a wordmark. A 5x zoom
  on it shows the mark there is a specular highlight, not lettering. This
  skill's own guidance says text-only prompts *avoid* readable text rather
  than controlling it; the construction that beat that — on all three — is
  the PRODUCT block's explicit `there is no printed text, no logo, no
  engraving, no etching and no marking anywhere on <each part>` plus an AVOID
  list naming each carrier one by one. Three clips, so it is good evidence
  for that construction, not a guarantee. ⚠️ **A fourth clip since found its
  boundary**: every carrier checked in these three is an *outer* surface, and
  when clip D put a garment's lining on camera the construction — which had
  named only outer surfaces — let three label-shaped objects through. See
  "One clip outside this skill's own boundary" below.
- **Thin protruding parts have now held three times.** The grinder's crank arm
  — a thin right-angle part — kept its length, thickness and bend through both
  clips of the pair, including clip B's orbit; clip C's two slim titanium
  temples kept exactly their length, width and thickness throughout, with no
  third temple. That part was the predicted main risk in each case. Clip C
  also kept the lenses clear and never mirrored, and never unfolded the
  temples.
- **A description of a part is honoured; a number attached to it is not.**
  Clip C's hinge is the cleanest instance yet. The *qualitative* half landed
  completely — a barrel hinge with interleaved knuckles, the mottled acetate
  edge on one side and the flat brushed temple bar on the other, unchanged
  through the macro push-in and through the whole orbit. The **count did
  not**: the prompt asked for three interleaved knuckles and a 5x
  magnification shows **four** knuckle blocks — two levels along the pin,
  each split into an acetate-side and a temple-side knuckle — plus a screw
  head top and bottom. It pairs with `seedance-ad-creative`'s AURA clip
  (`60fbea52-b14b-4796-80bf-03afe0aa4fa0`), where `never more of the hand
  than the fingertips and the first knuckle` was written twice and ignored,
  and with two findings already in this file: three interior waypoints
  written and two rendered, and `a full 360 degrees` producing no measurable
  total. **Note what this does not undercut.** The shot-size instruction that
  worked — `the whole pair in frame from temple tip to temple tip with
  margin` — is a **spatial description**, not a count, which is why it landed
  where the knuckle count did not. So "write it down and you get it" holds
  for what a thing looks like and where it sits in frame, and does not extend
  to how many of it there are. One nuance in the same clip, consistent with
  the shared file's negative-clause rule: the AVOID list's `no third temple`
  **held**, so a count written as a prohibition fared better than the same
  kind of count written as a positive requirement.
- **The consistency lock worked with no first frame at all.** Every earlier
  accepted clip in this repo that needed a product's identity held had an
  attached image doing that work. This is the first clean test of the text lock
  on its own, so the template's "write the consistency lock every time" now has
  direct evidence behind it rather than only a rationale.
- **`--generate-audio false` produced no audio stream at all** in the delivered
  file, not a silent track — all three times. The defaults table says the flag
  sets `generate_audio: false` on the request; this is the end-to-end result.
  (The one clip here that *needed* sound simply left the flag off and took the
  server's `true` default — clip D, below.)
- **`--aspect-ratio 16:9` took effect — the output is exactly 1280x720**, on
  all three. First clean confirmation of ratio control in this repo: every
  earlier product-adjacent clip attached a frame and was forced to
  `adaptive`. It works *because* the route is text-only, which is the point
  made under "A product photo" below.
- **The accessory row: the side is controllable, the depth is not.** `in a row
  on the grey surface beside the standing grinder` split the row so items sat
  on **both** sides of the grinder — identically in clips A and B, which makes
  it a stable reading of `beside` rather than a roll. Clip C wrote the repair:
  `two accessories lie on the grey surface to the right of the glasses and
  only to the right, both on the same line, evenly spaced and not touching
  each other or the glasses ... Nothing lies to the left of the glasses and
  nothing lies above or below that line.` **The left/right half held** —
  nothing on the left, which neither grinder clip managed. **The single-line
  half did not**: the cloth sits forward of and below the case rather than in
  line with it. One run each way, and on **two** accessories rather than the
  template's three. So name the side; leave the depth to be checked on the
  draft.
- **The duration budget held again, and the orbit got its four seconds
  exactly.** Clip C was written 3/3/4/2 and delivered 2.67/3.04/4.00/2.33 —
  every segment within 0.4s of plan, and the deliberately largest share
  landing on the number. Clip A was 3.12/2.88/3.7/2.3 on the same plan.
- **An explicit "no cut anywhere inside this segment" was not contradicted,
  which is weaker than "held".** In clip B the 0.25 detector pass reports
  boundaries at 3.12s and 6.29s and nothing inside the orbit. But the same
  pass also missed that segment's own closing boundary (next bullet), so a
  pass that cannot see one cut in this clip has not established the absence of
  another one three seconds earlier. The frames across the orbit are
  consistent with continuous travel; the detector's silence is not what
  establishes it.
- **The scene detector missed a real cut in all three clips, and no single
  lower threshold would have caught them.** Clip A's third boundary is at
  **9.750s** and appears only at **0.05**; clip B's is at **10.041667s** and
  needs **0.10**; clip C's is at **9.71s** and also needs **0.10**. None is
  visible at the 0.25 all three were first checked at, while the earlier
  boundaries were found in the same passes. A uniform grey studio under
  unchanging light is the known same-lighting blind spot, and these are the
  **fifth, sixth and seventh** confirmations of it in this repo — and its
  strongest form, because two of them are a controlled pair and the third is
  an independent clip that walked into it anyway. Lowering the default is not
  the fix: how far to lower it was only knowable after the frames had been
  read, which is the work the count was meant to save. Read frames either side
  of every written stamp. ⚠️ **A fourth clip hit the same blind spot
  outdoors** — clip D's 20.958s boundary needs 0.15, and both sides of it are
  the same person on the same path under the same overcast light. So this is
  not a studio artefact; it happens wherever a cut does not change the
  location. The record lives in `Checking the cuts: read frames,
  never a detector count alone` in
  [`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md),
  not here.
- **`hold the final frame` held in two of the three, and clip C's hold is
  complete.** Measured without an `-ss` pre-seek, which gives the first
  post-seek frame no predecessor to diff against and therefore scores it as a
  change: clip C has **zero** frames above a 0.0005 scene score after
  11.541667s, and the last frame above that threshold anywhere in the clip is
  at 11.375s — so the hold actually runs about **0.67s**. Clip A is still over
  its last half second; clip B, measured the same way, has **seven** frames
  above 0.0005. (An earlier reading of these two said one and six; both were
  the pre-seek artefact.) The two that disagree are the same-seed pair, one
  paragraph of prompt apart. Write the hold, expect a settle, and do the
  freeze in an editor if the last frame really has to be frozen.
- **The poll survived a transport fault, for the third consecutive clip.**
  `curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL` mid-poll, and the
  script retried the **poll, not the create**, six seconds later; the job had
  been running the whole time and completed normally. A resubmit there would
  have doubled a 2.88 USD bill. `ofox-video-core`'s "The rule has now survived
  a real transport fault" carries the record.

## One clip outside this skill's own boundary: a presenter on camera

**Read the first paragraph before you read the findings.** This skill's
`description` ends `Do not use for ... anything involving people/dialogue
(see seedance-short-drama)`, and clip D breaks that rule on purpose. It is
recorded here because it was run on this skill's execution layer and its
findings bear directly on the templates above — **not** because the exclusion
has been relaxed. The exclusion is unchanged, no new skill was created, and
whether spoken-presenter commerce footage deserves a scenario of its own is
an open question this one clip does not settle.

Why it was run at all: presenter-led commerce video sits in a gap none of the
four scenario skills covers. `seedance-product-video` excludes people and
dialogue, `seedance-short-drama` does not care whether a product's appearance
is accurate, `seedance-ad-creative` is brand-mood advertising. The call was to
borrow this skill's execution layer, ship one clip, and decide about
abstraction afterwards rather than build a directory first.

**It crosses a second line as well.** The product is fictional, and this
skill's own rule says a fictional product goes text-only rather than
generate-a-reference-then-animate. Clip D generated a first frame anyway,
because the whole point was to see whether a frame-locked product survives
being worn. What that trade cost is written up under "A product photo: when
it is required, when text is enough" — the rule for a **real** SKU is
untouched.

| | Job | Outcome |
|---|---|---|
| Clip D | `e378f058-f224-4450-94b4-798840ad139b`, seed `561877558` | accepted 2026-09-06 |

`bytedance/seedance-2.5` on `byteplus`, **30s, 720p, image-to-video** with a
generated product-only first frame, `aspect_ratio: adaptive` (forced by the
attached image), **audio left on**, billed **7.20 USD**; the first frame cost
a further **0.154615 USD** on `openai/gpt-image-2`, so 7.354615 USD in total.
Versions in force: this skill 1.11.0, `ofox-video-core` 1.18.0,
`ofox-image-core` 1.8.0. It is `n: 1012` in the gallery.

The subject is a fictional hardshell outdoor jacket — charcoal ripstop body,
a brick-orange yoke across the shoulders and upper chest, one centre main zip
with an orange pull, one diagonal chest pocket, two hand pockets, a
stiff-brimmed hood with two drawcords, hook-and-loop cuff tabs, and a **blank
triangular sleeve patch**, again with no printed text anywhere by design. Four
segments: product alone on a wooden hanger (0–8s), a presenter entering and
putting the jacket on (8–18s), an outdoor mountain-ridge scene (18–28s), a
held final frame (28–30s), with four short Chinese spoken lines across it.
The prompt was written in Chinese, so clauses quoted from it below —
`hard cut`, `no ... hang tag` — are given in translation, per this repo's
convention.

### Where this skill's defaults had to be overridden

| Default here | What clip D did |
|---|---|
| `--generate-audio false` | **left the flag off entirely**, taking the server's `true` default. A spoken clip needs the track. Delivered `nb_streams=2`, aac 32000 Hz stereo |
| 5s, or 10–15s for the segmented template | **30s** — three separate demands plus dialogue headroom do not fit 15 |
| "no dramatic cinematography" | 10 shots and 9 hard cuts. Once a person is in frame, shot sizes have to change |
| the `Motion` question's four options | all four are about the product alone; none of them fits a clip whose subject picks the product up |

### What held

- **The first-frame lock survives the product being worn — this clip's
  headline.** Every earlier piece of evidence for a frame-locked product in
  this repo had the product **sitting still**: clips A, B and C are studio
  objects on a table, and `seedance-ad-creative`'s sneaker clip
  (`ac927785-92ef-4e28-97b9-ff8172ec5554`) has a model **beside** the product,
  never wearing it. Clothing is the most deformable category there is —
  fabric, drape and creases all change on a body — so this was the predicted
  risk of the whole clip.

  It did not happen. Because "does it look like the same garment" is not a
  usable acceptance test, six discrete features that do not change under
  deformation were enumerated in advance and compared frame by frame against
  the attached image: **the two-tone colour split, the centre zip and its
  orange pull, the pocket set, the hood and its two drawcords, the cuff tabs,
  and the blank sleeve patch. All six held**, across the hanger, the body, the
  outdoor scene and the studio closer — the colour split, the strictest of
  them, never drifted. The sleeve patch was checked at 8x in two segments and
  is an outlined dark triangle with nothing inside it.

  **This is one clip.** One product, one seed, one run, no control; the cuff
  tabs are unreadable in the backlit outdoor segment, so strictly it is five
  of six features legible everywhere rather than six. Read it as: *the
  frame lock is not known to stop at "product sitting still" — it survived one
  garment being picked up, held open, put on and zipped.* Not as a guarantee.

  One nuance that keeps this honest: the delivered jacket reads **thicker and
  more insulated** than the attached shell. Nothing in the prompt locked
  loft, and the six features are all discrete. So a discrete-feature lock
  holding and a continuous property drifting are both true of the same clip.

- **A shot size on every waypoint, a third time.** Segment A wrote three
  framings — medium front, close push-in on the chest, medium-close from
  front-right — and got exactly those three, with no framing inherited from
  the shot before. Consistent with clip C. **The hedge:** in clip D those
  boundaries rendered as cuts, so the framings are partly delivered *by
  cutting*, which is not the same thing clips B and C measured (framing
  inheritance inside one continuous move). Do not stack this as a third
  identical confirmation. ⚠️ **And a later clip shows why that distinction
  matters rather than being pedantry**: `cb6b7870` stated a shot size on
  three waypoints *inside* a move and got none of them, while both of its
  post-cut shot sizes landed. Read this bullet as evidence for the post-cut
  case, not for the in-move one — §3.

- **"Product-only first frame, person written in text" has a second data
  point.** The first frame contains no person, no hand, no foot and no skin;
  submission passed with no `input_moderation_failed`, and a photoreal
  presenter appears from 6.7s and is on screen for the remaining 23 seconds.
  The first data point was the sneaker clip, where person and product shared
  a frame but never touched. Here the presenter **picks the product up, holds
  it open, and wears it** — so the route survives physical contact between
  the generated person and the frame-locked object. `--real-person` was not
  passed and is not needed on this route; it is for authorised real-person
  *reference images*, which is a different problem.

- **Nine hard cuts and ten shots in one job — a new maximum for this repo.**
  The previously recorded envelope was 3–10 shots and **up to 6 hard cuts**,
  from two different jobs. All nine boundaries here were confirmed by reading
  the frames either side, not by a detector count. And it was done with a
  first frame attached, dialogue on the track, and two locations. Still
  unmeasured: more than 10 shots, 1080p, the `volcengine` upstream, and what
  happens to a line of dialogue split across a cut. ⚠️ **Do not read this clip
  as settling that last one — the tempting reading is wrong.** Each line was
  *written* inside a single waypoint (9–11 / 15–17 / 22–24 / 26–28s), which
  makes it easy to say "no line crossed a cut"; but the cuts did not land on
  the written seconds, and two of them fall inside a written line's window —
  10.500s inside 9–11s, 27.750s inside 26–28s. Whether the spoken audio
  actually crosses them is **not known**, because the audio content was never
  checked here (see the not-verified note at the end of this section).

- **Every timestamped boundary became a hard cut — including the six that
  never said so.** Three boundaries were written `hard cut`; the other six were
  interior waypoints. All nine rendered as cuts. This is the shared file's
  rule (`Two things a timestamp can mean` — an unnamed boundary becomes a hard
  cut) confirmed 6 for 6 in a single job. **The cost, when you did not want
  it:** the 2–5s waypoint was written as `the camera pushes straight in to the
  chest` — a camera verb, describing a continuous move — and it delivered a
  cut. So a bare camera verb neither produces a move nor prevents a cut. If a
  segment must be continuous, `one continuous shot` has to be written.

- **Timestamp accuracy, and a shape worth watching.** Delivered against
  written: 2s→**2.000**, 5s→4.708, 8s→**6.708**, 11s→10.500, 14s→13.792,
  18s→17.625, 21s→20.958, 25s→24.833, 28s→27.750. Eight of nine within 0.5s;
  the outlier is the 8s cut at 1.29s early. **Eight land early and one lands
  exactly on its stamp; none lands late** — a shape no other clip in this repo
  has been checked for, and one clip is not a rule. ⚠️ Take the boundary from
  the frame's own timestamp, not from the midpoint of an `-ss` pair: `-ss 1.92`
  and `-ss 1.96` return the frames at 1.958333 and 2.000000, which straddle
  this cut without either of them being it.

### What did not

- **The zero-fake-text construction has a boundary, and clip D is where it
  broke: it only covers surfaces that face the camera by default.** Clips A,
  B and C all passed with the same construction — the PRODUCT block declaring
  `there is no printed text, no logo, no engraving ... anywhere on <each
  part>` plus an AVOID list naming each carrier. Clip D used it too, and the
  product's **outer** surfaces are clean throughout, sleeve patch included.

  Then at 13.2s the presenter holds the jacket open with the lining toward
  the lens, and there are **three label-shaped objects on it**: a brand label
  at the neck (an abstract mark over a row of glyph-like blobs), a small tab
  below it, and a bordered care/spec panel low on the lining with five or six
  rows of glyph-like blobs. At 6x and again at 12x none of them resolves into
  readable letters — so **no readable fake text**, but three carriers that
  `AVOID` had named outright (`no ... hang tag`, and the PRODUCT block's `no
  size tag, no care label`). Zero fake text is therefore **half-held**, not
  held.

  The cause is mechanical and visible in the prompt: the per-part naming
  listed `the chest, the back, the sleeves, the hood and that triangular
  patch` — **all outer surfaces, not one interior one**. The construction did
  not fail; it was never pointed at the surface that ended up on camera.

  **The fix follows from that and has not been run.** When the script has the
  product opened, turned inside out, unzipped or taken off, extend the
  no-text declaration to the **lining, the inner collar and the inside of any
  pocket**, and name the interior carriers in AVOID one by one — neck label,
  care label, composition label, size tag, hang tag. Until a clip is run that
  way this is a repair inferred from one defect, not a measured one.

- **A prohibition pinned to a second is only as reliable as the cut.** AVOID
  said no person, hand or skin before 8s. The presenter is fully in frame at
  **6.708s**, because the cut he was written behind landed 1.29s early. The
  instruction was not ignored; its time window moved. Anything of the form
  "not before second N" carries roughly the cut tolerance — about 1.3s here —
  so put the thing in a later segment rather than writing the prohibition
  harder.

- **"Completely still, no camera movement at all" delivered a settle.** Over
  the final 2.25s, 23 frames of 54 cross a 0.0005 scene score, but
  **zero** cross 0.005 and one crosses 0.002. Framing is identical at 28.0s
  and 29.9s, so the camera did not move; the residue is a living subject
  breathing. Consistent with what clips A–C showed about `hold the final
  frame` — and with a person in shot a freeze was never physically available.
  Freeze in an editor if the last frame has to stop.

- **A style clause could not be separated from its own scene.** The prompt
  asked for `no cinematic colour grading`, and the outdoor segment is dark,
  cold and backlit. The scene as written — a dawn ridge under low cloud —
  supplies exactly that light, so grading and location cannot be told apart
  here. Recorded as a deviation, not a violation; separating them needs a
  same-scene, same-seed pair, which was not run.

- **The scene detector missed a cut again — the eighth time in this repo, the
  fourth in a row in this scenario, and the first one outdoors.** The
  boundary at **20.958s** is absent at 0.25 and needs **0.15**; the other
  eight are found at 0.25. Both sides of the missed cut are the same person on
  the same gravel path under the same overcast light, differing only in shot
  size. The four clips here needed 0.05 / 0.10 / 0.10 / 0.15 — **four clips,
  four answers, and lowering the default is still not the fix**, because how
  far to lower it is only knowable once the frames have been read. What clip D
  adds is that the same-lighting blind spot is not a studio artefact: it
  happens under natural light too, wherever a cut does not change the location.

### Two smaller notes

- **The poll ran clean.** Clips A, B and C each lost their TLS connection
  mid-poll; clip D did not. Three of four, not four of four — worth stating so
  the fault does not get written up as inevitable. Wall clock was 439s, well
  inside the 1800s `--max-wait` that was set because a 30s job had previously
  taken about 1074s. The default 540s would have been enough, but only just.

- **`--size` was honoured on the first frame, which contradicts an earlier
  record.** `--size 1792x1024` produced a file measuring exactly 1792x1024
  before cropping, whereas the sneaker clip recorded requested / reported /
  actual as three different numbers. **This does not overturn that record**:
  no response-reported size was captured for clip D, so all that is known is
  that the file on disk matched the request. Capture `SIZE_REPORTED` next
  time. The crop to 1792x1008 (exact 16:9) then delivered an exact 1280x720
  clip, so the crop-before-generating discipline held as usual.

### What was not verified here

Read every claim above as sight-only. **The audio content was never checked.**
What was measured is that a track exists and what it is: `nb_streams=2`, aac
32000 Hz stereo, 130074 bps, 940 frames. Whether the four Chinese lines are
spoken accurately, whether the lip sync lands, and whether the ambience is
layered per segment as written were all judged by the repo owner on playback —
**his judgement, not a measurement here**, and the `accepted` verdict rests
partly on it. Do not restate any of it as a finding.

The frame checking was **not an exhaustive scan** either: a 1fps overview,
both sides of all nine boundaries, six full frames and three
high-magnification crops. It cannot rule out fake text or drift at a moment
that was not sampled — the lining labels were themselves missed on the first
pass and only found on a frame-by-frame recount.

## A product photo: when it is required, when text is enough

For a listing, a shopper compares the clip against the real item, so literal
accuracy (shape, printed text, logo, colour, material) matters more here than
in any other Seedance scenario — an invented detail is a real problem, not
an aesthetic one. The gallery splits the question in two, and so does this
skill:

| The product is… | Route | Evidence |
|---|---|---|
| a **real SKU** — a logo, a printed label, distinctive geometry (hinges, seams, a particular cap), brand packaging | **Photo required.** Image-to-video from the real photo. | every gallery prompt that had to match a real product, logo or package used an image (cases 12, 13, 24, 29); text-only prompts avoid readable text instead — `all labels illegible` (case 40), `unreadable signage` (case 7) |
| a **category prototype** or a fictional brand — "a matte white ceramic mug", "a blue-and-copper hair dryer", a made-up label the user is happy to have invented | Text is acceptable. Say so, and set expectations. | the gallery's four product-video prompts are all text-only and all fictional (cases 16–19); this skill's own two accepted clips are text-only on fictional products (jobs `50f623b2-c54a-4d9d-9646-31dd06e2a926` and `8efeb556-bf38-45ec-940b-a792ef74bfcf`), and each held both the product's identity across four segments — including two slim titanium temples and an interleaved barrel hinge on the second, whose knuckle *count* was the one thing that drifted — and a completely text-free set |

**An AI-generated product image is not a substitute for a photo of the real
product.** No gallery product case goes generate-an-image-then-animate; the
ones with images used real photos or the vendor's own white-model assets
(cases 24, 37). The reason follows from that split rather than from an
observed failure: a generated image can be wrong about the label, the cap and
the proportions in exactly the ways the video can — and then locks those
errors in as the first frame. If the user has no photo of a real SKU, say the
result may not match the item, and offer to proceed as a category prototype
rather than offering to generate a reference first.

⚠️ **The out-of-scope presenter clip broke this rule too, and it is worth
knowing exactly what that did and did not prove.** Its product was fictional,
and by the rule above that makes it a category prototype and therefore
text-only — instead a first frame was generated on `openai/gpt-image-2` and
attached. What that bought was real: the product's identity had to survive
being picked up and worn across four segments and two locations, and it did,
on six enumerated features. What it cost was exactly what this rule predicts —
the frame shape stopped being a flag and became a crop decided before
generating, and every invented detail in that image (including a lining the
video then furnished with labels) became binding. **Nothing here contradicts
the rule for a real SKU**, which is what the rule is actually about: a
generated image is still no substitute for a photo of a real product. What
the clip suggests, on one run, is narrower — for a *fictional* product that a
person has to handle for 20-odd seconds, a generated anchor may be worth the
control it costs. Treat that as an open question, not as permission.

**The text-only route keeps one control the photo route gives up: the aspect
ratio stays a flag.** With a photo attached, `bytedance/seedance-2.5` forces
`aspect_ratio: adaptive` and the clip comes out the photo's shape, so the
platform ratio is a crop made before generating. With no image,
`--aspect-ratio` takes effect — measured on the accepted clip, `16:9` in and
exactly 1280x720 out. So for a fictional or prototype product, following this
skill's own rule against generating a reference image is not only about not
locking in invented details; it is also what keeps the frame shape a
parameter rather than a pre-processing step.

**Prefer a local file over a remote URL** when the user has one available.
`ofox-video-core` auto-base64-encodes a local, readable file into the
request; real testing found this more reliable than a remote URL in at
least one case (an otherwise valid, publicly reachable image URL was
rejected by the upstream provider — likely host-side bot/hotlink
protection, not something under our control). A remote URL also works if
that's all the user has, it's just the less-reliable option of the two.

### Two ways to attach the photo

An attached image means one of two things, and the API has a field for each
(shared file, `Reference assets as visual anchors`):

| Meaning | Flag | What it does | Status in this repo |
|---|---|---|---|
| **First frame** — the clip starts on this exact picture | `--frame-first-image PATH` | locks the opening view to the photo; on `bytedance/seedance-2.5` forces `aspect_ratio: adaptive`, so the photo is cropped or padded to the target ratio **before** generating | verified with real runs; this skill's default route |
| **Identity reference** — the model borrows the product's appearance from several photos, no frame is locked | `input_references` through `--extra-json` | lets front, back, top and box photos inform the clip | Follow the shared [`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy). It owns the payload shape, canonical `@imageN` labels, array-order rule, dry-run guard, measured two-image boundary and nine-image ceiling. For this product route, pass `--aspect-ratio` explicitly. |

**The two are mutually exclusive** in one job: the script rejects a request
carrying both (`references_conflict`). For a single photo, the first-frame
route is the tested one and the default here. Reach for identity references
only when the user has several angles of the product and wants them all to
count.

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the compact template above>" \
  --frame-first-image "/path/to/local/product-photo.jpg" \
  --duration 5 --resolution 720p --generate-audio false
```

That is a real run — hence `--approved`, see "Before you spend" below. Swap it
for `--dry-run` to price the job without sending it.

**Do not pass `--aspect-ratio` here** for the default model
(`bytedance/seedance-2.5`) — `ofox-video-core` forces `aspect_ratio` to
`adaptive` whenever an image is attached with this model (verified against
the real API: every other value fails for image-to-video on this model),
overriding anything else and printing a notice when it does. **Don't pass it
on another model the user named either**: there, leaving it off is precisely
what makes the script send `adaptive`, and passing a ratio is honoured
instead. The output's frame shape follows the **photo's** shape, which is why
the brief settles the platform before anything is generated and the photo is
cropped or padded to that ratio first.

If the reference image includes an actual person (e.g. a hand modeling a
ring, a person wearing the product), Seedance 2.5 image-to-video refuses it
at submission (`input_moderation_failed`, nothing billed). `--real-person
true` **does lift that refusal on 2.5** (measured 2026-09-16) — but it is
Ofox's privacy-preserving preprocessing path for real-person references the
caller is **authorised** to use, an authorisation route rather than a way
past the check, so it is offered only when the user holds the right to that
person's likeness and says so, and never set on their behalf. For a product
video it is almost never what the job needs: the thing that must be exactly
right is the object, and the reliable route is still a photo of the product
alone with any person written into the prompt text. Evidence and limits:
[`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
→ "`--real-person true` lifts that refusal on 2.5". The `--real-person` path
validates the image server-side
and can fail with
`bad_data_uri`/`download_failed`/`unreachable`/`not_image`/`too_large` if the
image isn't a small, valid file the API can use — see the failure table
below.

## Writing a good product-video prompt

Keep the prompt plain and literal — this is the opposite instinct from
`seedance-ad-creative`'s cinematic mood-building. The templates above are
the shape; these are the four things that go into them.

### 1. Product description, precise and neutral

Shape, material, colour, finish, structural points, and any printed text
verbatim in quotes — the same precision `seedance-ad-creative` uses for
product accuracy, without its mood or brand-tone layer, since a catalog shot
has no brand story to tell. The gallery's product blocks are built from
physical words: `glowing copper accents`, `physically accurate diamond
refraction`, `realistic stainless-steel reflections` (cases 17, 19, 38).

```
A matte ceramic coffee mug, off-white, cylindrical with a curved handle, "MORNING" printed in dark grey on one side.
```

### 2. Explicit plain-background language

A pure white background is what marketplace listing rules ask for and what a
shopper expects of catalog footage. It is a **platform convention, not
something the gallery shows**: the gallery's cleanest product prompt (case
17) uses a bright reflective surface under studio softbox light, and case 41
pins a grey stone background in place rather than removing it. Whatever the
brief chose, state it directly instead of assuming the model will remove
whatever is behind the product in the reference photo:

```
Pure white surface and backdrop, clean studio background, no props, no shadows on the backdrop, even lighting.
```

### 3. Camera motion: waypoint pictures, not a camera verb

Describe the motion as a plain mechanical move, not a "shot". The default is
**the camera orbits, the product stays still**: every rotation in the
gallery's thirteen product-adjacent prompts is written as camera movement
(`360-degree orbit`, official case 42 — whose subject is a person, not a
product; `the camera slowly circles the build platform`, case 39; `smooth
spiral pull-out`, case 13) or as a hand turning the product (case 24) — none
writes a turntable with a fixed camera. The turntable stays as an
alternative because listing platforms and users ask for it by name.

**That gallery evidence is about which motion to pick. It says nothing about
how to write it, and how to write it turns out to decide whether the motion
happens at all.** This scenario's first two clips are a controlled pair on
exactly that: same seed (`642303335`), same model, same flags, the same prompt
text except the ORBIT paragraph — and a third, independent clip a day later
tested the two fixes their defects produced. Full parameters and job ids:
"Measured on
this scenario's own clips" above.

| | Clip A — rejected | Clip B — accepted |
|---|---|---|
| ORBIT written as | the camera's move: `the camera orbits the grinder a full 360 degrees at constant height and constant speed, ending back at the front view. The product does not move and does not rotate; only the camera travels.` | one continuous move with `no cut anywhere inside this segment`, then **four timestamped moments** — three interior views and the return — each describing what the frame contains at that point |
| What rendered | **no orbit at all** — from 6.0s to about 9.7s a near-static front view with a slight push-in, the crank arm pointing right in every frame. 3.7 of 12 seconds, the core segment of a catalog clip, delivered no new angle | **the camera moved.** Inside the segment the travel reads rear → side → front, about 180 degrees; whether it went further than that is unmeasurable — below. It also ends on the orientation the closing waypoint named, which this skill read as the return working; ⚠️ **clip C shows that was a coincidence of where the move began** — see "The closing return is not honoured" below. Two of the three interior views written appeared, unevenly spaced — see "4. A timestamp orders the pictures; it does not schedule them" |

**The camera moved, and the product is its own protractor.**
The grinder's crank arm rises from the centre of the collar and bends once at
a right angle, so it extends horizontally in one direction: from the **front
or the rear** it reads as running cleanly sideways, mirrored between the two,
and from either **side** it points along the optical axis and disappears
behind the collar, leaving only the knob visible above it. The clip's front
view is fixed by the frame at 2.8s, at the end of REVEAL: knob at the left,
arm extending cleanly sideways.

The ORBIT segment is continuous from the hard cut at 6.291667s to about 10s,
and inside it the frames read:

| Time | What the frame shows | Where the camera is |
|---|---|---|
| 6.40 – 8.40s, **six sampled frames** | knob at the right, arm sideways | the rear |
| ~8.80 – 9.20s, the crossing | arm entirely hidden, only the knob visible above the collar — dead centre above it at 9.00, offset right at 8.80 and left at 9.20 | a side — the one axis crossing visible on screen |
| 9.60 – 10.00s | knob back at the left, arm sideways — the 2.8s orientation | the front |

Two claims and one limitation, and the limitation is the point:

1. **The segment ends on the opening orientation** — ⚠️ **which this skill
   read as "the return landed", and clip C shows it was a coincidence.** The
   closing waypoint was written as a named frame, `back on the exact front
   view of the opening shot`, and clip B's last frame is that frame; but the
   move also *begins* at the rear, unasked, so half a turn from there arrives
   at the front regardless. Clip C began at the front and finished at the
   rear. (The 11.5s frame inside ACCESSORIES still shows the opening
   orientation, but it sits past the 10.04s boundary, so it corroborates the
   orientation and says nothing about travel.)
2. **The observable travel is rear → side → front, roughly 180 degrees.**
3. **The total travel is not measurable at all.** The written path's other
   half — front to rear — could only have happened across the hard cut at
   6.291667s, and a camera's azimuth is unreadable across a cut. Worse here
   than usual: the shot before that cut is DETAIL's macro of the knurled
   ring, which is rotationally near-symmetric and therefore carries no
   orientation cue at all. The segment simply *starts* at the rear. Whether
   the camera travelled there or was cut there cannot be told from this clip.

**So this skill does not claim the orbit completed a circuit, and it did
claim that once.** Two earlier readings of these same frames were published
and both were wrong, in opposite directions — one measured from the moving
segment's own first frame and under-read the travel, the other measured
across the hard cut and over-read it. Neither pair of endpoints was connected
by continuous motion. The general rule that came out of it lives in
`Measuring a camera's travel: only inside one continuous shot` in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md),
because it applies to checking any clip: **the honest form is "the move ends
where the frames say it ends; how far it travelled is unmeasurable here".**
That section also predicted what would make a rotation readable — an
asymmetric feature inside one continuous shot — and clip C is the case that
followed the recipe, which is where the measured half turn below comes from.

**What this pair cannot tell you is which half of a waypoint's wording did the
work.** Each of clip B's waypoints carried two kinds of description at once: a
camera-position label ("level with the right side", "directly behind the
grinder") *and* an appearance description ("the crank arm running away from
the lens in sharp foreshortening", "only the smooth back of the brushed steel
collar and the walnut knob beyond it are visible"). On the 8s waypoint those
two contradict each other — from directly behind, that arm does not point away
from the lens, it extends sideways — so the prompt held neither kind constant.
The rendered arm-hidden frame at about 9.0s matches that waypoint's
**appearance** clause while contradicting its **position** clause, and
nothing in this run separates the two. Read every "the waypoint appeared" statement here as "that
picture appeared somewhere in the move", never as "the model obeyed the
position label".

**The claim that survives is the one worth having, and it is about movement
versus no movement rather than about degrees.** A waypoint written as a
picture produced real travel, where a single sentence of camera motion
produced no movement at all: **describe each angle as a still picture with a
timestamp on it — a camera verb is not honoured.** Clip A is the negative
control and clip B the positive one, one variable apart, which is what makes
the prompt the attributable cause rather than the roll. That comparison is
still two runs; clip C is not part of it, since its prompt differs in every
paragraph, and what clip C adds is the framing fix, the extent and the
ending.

**Reasoning from that confound rather than measuring it: write a waypoint as
an appearance description, not a camera-position label.** Say what is in shot,
what is hidden and what is foreshortened; leave out where the camera stands.
Two reasons, neither of them a measurement: the appearance clause is the half
the model has to produce pixels for, and — as the 8s waypoint shows — the
position label is the half that can quietly contradict it while you are still
writing the prompt. The one clause with a measured outcome behind it is the
**framing** one — `with the whole pair in frame from temple tip to temple tip
and margin around it` — which clip C verified, and which is a spatial
description rather than a camera position or a count.

Two more things come from the same pair:

- ⚠️ **"The return worked" is withdrawn — see "The closing return is not
  honoured" below.** `by 10s the camera has returned to the exact front view
  of the opening shot` does point at a frame the clip already contains, and
  clip B's 10.0s frame is that frame — but clip B's move also *began*,
  unasked, at the rear, so half a turn from there lands on the front whether
  or not the clause did anything. Clip C began at the front and ended at the
  rear. Check the last frame of any orbit against the opening frame on the
  draft; do not plan on it matching.
- **Clip A's negative clause held while its positive one failed.** The product
  genuinely did not rotate. `The product does not move and does not rotate` is
  worth keeping in every orbit — it just does not produce the camera's travel
  by itself.

**Clip B's other remaining defect: the orbit inherited DETAIL's macro
framing.** Independent of the pacing in section 4, and unaffected by it. No
shot size was written on any waypoint, so the segment stayed as close as the
macro push-in before it — the base and the knurled ring are out of frame for
the whole orbit, which gives several angles of the collar and the crank and
never the whole product from the side or the back. For a catalog clip that is
a partial loss of the very thing the segment exists for.

**And it cost more than framing: it made one waypoint physically
unrenderable.** The 7s waypoint asked for the knurled ring seen edge-on — and
the knurled ring is outside the frame for the entire orbit, so half of that
waypoint's content had nowhere to appear. An unspecified shot size does not
merely crop the picture; it can silently delete part of what a waypoint asks
for, and then the missing beat reads as the model ignoring the waypoint when
in fact the prompt had already made it impossible.

**That fix has been run twice: it worked once and failed once.** Give every
waypoint its own shot size — "the whole product in frame, `<top>` to
`<bottom>`, with margin" — and close the paragraph with "at every one of
those views the entire product is inside the frame, nothing cropped". Clip C
(`8efeb556`, 2026-09-06, the eyeglasses) does exactly that on all three of
its waypoints and **deliberately keeps the same
DETAIL-macro-immediately-before-ORBIT ordering** that caused the inheritance
here, so the defect had every chance to recur. Every frame of its move holds
the whole product with margin, nothing cropped, where the grinder's base was
outside the frame for its entire orbit.

⚠️ **That was written up here as a verification, and one clip later it is
not one.** Job `cb6b7870-22f7-4a15-9168-8a013805775f` (2026-09-07, a
`seedance-ad-creative` flask spot, 15s, **i2v** with a generated first frame,
rejected) has the identical shape — a macro beat immediately before a
waypoint orbit, a shot size on all three waypoints (`a medium shot ... the
whole bottle from cap to base inside the frame with margin above and below`),
and a closing `the bottle stays fully in frame at every moment of the move`.
Six frames across that move are all a close shot of the bottle's upper body
with the base never in frame. So the honest state is **once held, once
failed**, and the differences between the two runs — i2v with a paid macro
first frame against t2v, a tall cylinder against a folded pair of glasses —
are unexamined. Write the shot size anyway: omitting it is measured to be
worse, and it cost clip B a whole waypoint. Then read the frames.

**The failing clip does settle one thing, and it is directly usable here.**
Its two *post-cut* shot sizes — a `medium-close shot` and a closing `medium
shot dead front, the whole bottle centred` — were both delivered, the last
one holding the whole product cap to base with margin. Combined with clip D's
hedge below, that makes three clips agreeing that **a shot size stated across
a cut is far more reliable than one stated inside a continuous move.** So
when a segment has to open the framing up, give the wider view its own shot
after a boundary rather than asking a move to widen mid-flight.

It generalises past this segment in one direction only: a segment inherits
the framing of the one before it unless told otherwise, and DETAIL sits
immediately before ORBIT in the recommended order. **The failure half is
measured twice over; the repair half is measured once and contradicted
once.**

**The closing return is not honoured.** This is the one place clip C
contradicts what this skill wrote rather than confirming it. Its orbit is one
continuous shot (cuts detected only at 2.67s, 5.71s and 9.71s) and its
subject carries an unambiguous asymmetric feature — the two folded temples,
which read as parallel bars from the rear and vanish along the optical axis
from the side — so azimuth is readable at **every** frame of the move rather
than only at its ends. What it reads:

| Time | What the frame shows | Camera |
|---|---|---|
| 6.0s | both lenses facing the lens, temples folded behind the front | the front, matching the opening shot |
| 7.5s | the frame front seen along its own length, the two lenses overlapping into one narrow shape | a side |
| ~9.6s | both folded temples as parallel bars, no lens surface facing the lens | the rear |

So the move went front → side → rear and **stopped at the rear**. The written
`by 10s the camera is back on the exact front view of the opening shot` never
landed inside the segment; the front view returns only after the hard cut
into ACCESSORIES. The azimuth advances monotonically with no dead stretch —
and that is the whole claim: whether the prompt's `constant speed` landed is
**not** established, because a scene-delta reading is not a clean
angular-velocity proxy on this subject (near the front view the same rotation
moves the picture much less).

Two things follow, and the second one costs this skill a claim:

- **About half a turn is now measured, not inferred.** Two clips, different
  products, different seeds, different prompts, agree on roughly 180 degrees
  — and clip C reads it frame by frame inside one continuous shot rather than
  from two endpoints. So write an orbit expecting **half a turn**, and choose
  the two interior views so that half a turn is worth watching. Clip B's own
  total stays unmeasurable; that is a fact about that clip, which no later run
  changes.
- **A written return has one coincidence and one plain failure behind it,
  which is no evidence at all.** If the clip has to end on the opening view,
  put that view in the next segment after the cut, where the timestamps have
  held to about a second on every run in this repo. That is why the template's
  ORBIT slot no longer carries a closing return line.

The waypoint form, as a slot to fill:

```
One single continuous camera move, no cut anywhere inside this segment. The camera travels around the standing <product> anticlockwise at a constant height and a constant speed, the <product> centered in frame the whole way, and what the frame shows changes as it goes: at about <t1>s <what is in shot and what is not — "the <feature> runs the other way across the frame and the <other feature> is out of sight">, with the whole <product> in frame from <top> to <bottom> and margin around it; at about <t2>s <the same, for a view the first one could not see — "the <protruding part> is hidden behind the body and only its <tip> shows above the <collar>">, with the whole <product> in frame from <top> to <bottom> and margin around it. At every one of those views the entire <product> is inside the frame, nothing cropped. The <product> itself does not move, does not rotate on its axis and does not tip — every change in the picture comes from the camera having travelled.
```

Each waypoint is an appearance clause and carries no camera position; each
carries its own framing, which clip C measured as the fix for an inherited
macro shot; and the timestamps are there to order them, not to schedule them.
**Two interior pictures for a segment of about four seconds**, and **no
closing return inside the move** — that line used to be here, and it is gone
because neither measured clip's camera came home. If the clip has to end on
the opening view, that view is the next segment, after the cut. The budget and
the reason for it are in "4. A timestamp orders the pictures; it does not
schedule them" below.

Use only orbit, push-in, macro pan and static from the shared file's `Camera
language`. Avoid `seedance-ad-creative`'s vocabulary (dolly-in with a speed
ramp, rack focus, rim light, moody backlight) — the point is to see the
product clearly from several angles, not to evoke a mood.

#### The turntable alternative: it works, and its speed does not listen

**It has now been run.** Job `dc02f604-6c83-4837-b7fb-88e8df1876fb`,
2026-09-16, seed `88995356`, `bytedance/seedance-2.5` on `byteplus`, **5
seconds at 480p, 1:1**, `--generate-audio false`, **text-to-video with no
product photo**, billed **55 cents**. Until that run this option had no
gallery source and no run at all behind it, while the skip table routed every
"spin", "turntable", "rotate" and "360 on its axis" straight to it.

What was sent, as the motion and camera paragraphs:

```
The mug rotates slowly and steadily on its own vertical axis, anticlockwise, completing most of one turn over the clip, so the steel band and the logo plate come around into view and continue past. The mug stays in exactly the same place in frame and never tips, slides or floats.
CAMERA: completely fixed. No pan, no tilt, no push, no orbit. The framing at the last frame is identical to the framing at the first.
```

**The behaviour is what the option promises.** The subject was a matte black
travel mug with a brushed steel band and a small logo plate, and the plate is
the protractor — the asymmetric feature that makes a rotation readable at all
(shared file, "Measuring a camera's travel: only inside one continuous shot"):

| Time | Where the logo plate is |
|---|---|
| 0.1s | a thin sliver at the left edge |
| 3.2s | fully face-on, centre of frame — the small lettering on the steel band comes round with it |
| 4.8s | travelling on toward the right edge |

Meanwhile the mug's position, its scale, its contact shadow, the background
and the framing are **unchanged from the first frame to the last**. So the
product genuinely turned on its own vertical axis, the camera genuinely stayed
put, and nothing tipped, slid or floated. That is the whole of what the
turntable option asks for.

⚠️ **The rate did not listen — and that is this file's existing rule, not a
new surprise.** The prompt asked for "most of one turn"; five seconds
delivered roughly **a quarter to a third**. Same grammar as "A description is
honoured; a number attached to it is not" in the shared file: the *rotating
product* rendered and the *how much of it* did not, exactly as `a full 360
degrees` produced about half a turn on both measured camera orbits.

**The calibration to put in front of a user: a full 360 does not fit in five
seconds.** Somebody who asks for "a 360-degree showcase" is asking for the one
thing this run did not deliver, so say it before the cost table and give them
the choice — a longer clip, or accepting that the clip shows part of the
surface rather than all of it. **Do not quote a seconds-per-turn figure**: one
run at one duration cannot support one, and inventing a helpful-sounding
number here would be the same move the prompt made.

**The photo-attached path has since been run, and it splits into good news and
a blocking problem.** Job `54a721ce-61a1-46cf-b5bf-6973f31b8258` (2026-09-17,
seed `89984235`, 5s / 480p / 16:9, a **real product photograph** as
`--frame-first-image`, 55 cents) is the first time this skill's headline route
— a real SKU, anchored on its own photo — has been generated at all.

- ✅ **The anchor works.** Frame 0 *is* the photograph: whole product, white
  background, wordmark legible. Everything this file says about attaching a
  photo for a real SKU held.
- ✅ **And the SCENE matching the photo bought a clean opening.** The prompt's
  SCENE described the white surface the photo was shot on, and there is **no
  cut at the top of the clip**. That is not luck — where a supplied frame's
  background *disagrees* with the written SCENE, the measured result is about
  0.1s of the photo and then a hard cut (`prompt-structure.md` → "If the
  attached frame's background disagrees with your SCENE"). This skill's
  white-surface convention is what keeps it out of that trap, so **keep
  writing the SCENE as the surface the photo is actually on**.
- ❌ **The turntable never happened as a turntable.** The clip was written
  `0–1s` static, `1–2s` DETAIL, `2–5s` TURNTABLE and it spent the whole
  rotation segment in a cap macro. Unusable as a listing clip. That is a
  **timeline** failure rather than a turntable failure, and it has its own
  section: 🚨 "Scaling the timestamps does not scale the camera move".

**So the turntable itself is still only measured on the text-to-video run
above.** `54a721ce` cannot speak to whether rotation behaves the same with a
frame attached, because its rotation segment was never framed wide enough to
read. That question is still open, and the way to answer it is a 5-second clip
with **no DETAIL segment in it**.

No longer duration has been run either, so whether more seconds buy a
proportionally bigger turn is unknown.

Whether the waypoint rule carries over to a rotating product — waypoints
describing **what the frame shows** as the product turns, rather than the
rotation as a verb and a quantity — is still an untested inference from the
camera-orbit pair. Worth noticing what the sentence that ran is made of: one
motion verb plus a quantity is the shape that produced *no movement at all*
when the verb belonged to the camera, and here the movement happened and only
the quantity was lost. That is a real difference between the two cases and one
run cannot explain it.

### 4. A timestamp orders the pictures; it does not schedule them

Same controlled pair as §3 — same seed, same flags, the ORBIT paragraph the
only difference, and the frame readings are up there. This is the half of that
run that is about *when*, and it has its own heading because it bites even
when everything in §3 went right: the pictures can all be honoured and the
timeline still not be the one you wrote.

Clip B's ORBIT ran 6–10s and was written as four evenly spaced moments: three
interior views at 7s, 8s and 9s, then the opening front view again by 10s.
What came back was neither evenly spaced nor as many views:

- **Three interior views were written; two rendered.** The frames hold the
  rear, one view with the arm hidden behind the collar, and the front again.
  One of the three written interior views never appeared as a distinct
  picture at all. And one of the three — which of the rendered pictures it
  corresponds to is exactly what the confound in §3 makes unattributable —
  was asking, in part, for a detail the inherited framing had already put
  outside the frame, so part of it could not have rendered wherever it
  landed (§3).
- **The move spends roughly half the segment on one view.** Sampled every 0.4s
  from 6.4s to 10.0s, **six** of the ten frames still show the crank pointing
  right — 6.40, 6.80, 7.20, 7.60, 8.00 and 8.40, with 8.80 the transition —
  so roughly 2 seconds near-stationary, and the rest of the move compressed
  into about 1.2 seconds.

Both of those are counts and durations rather than a per-waypoint schedule, on
purpose: which written waypoint each rendered frame corresponds to is the
confound described in §3, so "this waypoint was N seconds late" is not
something this run can support.

**Clip C is the run that can support it, and it behaves the same way.** Its
waypoints are distinct pictures that do not contradict themselves, so each
rendered frame is attributable: a side view written at 7.5s arrived **on
time**, a rear view written at 9s arrived about **0.6 seconds late**, and the
closing return never arrived at all. Two interior pictures written, two
rendered — the first run to hit the budget below exactly, and it lost only
the ending.

Two rules follow:

- **Do not plan a segment where a particular angle has to land on a particular
  second.** If a specific picture has to exist at a specific time — a cut, an
  overlay, a hand-off to another clip — make it a segment boundary, where
  timestamps have held to about a second across every run in this repo, not an
  interior waypoint.
- **Do not write more interior waypoints than the segment can absorb.** A
  four-second orbit delivered two interior pictures against three asked for
  on clip B, and two against two on clip C. More pictures do not buy more
  angles; they buy a beat that vanishes and a timeline nobody can check
  against. And **do not put the view that matters most at the end of the
  move** — that is the one both clips dropped.

Then check the draft by reading frames at the written stamps rather than
assuming them — the same discipline the cut check needs (`Checking the cuts:
read frames, never a detector count alone` in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)).

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | `bytedance/seedance-2.5` (script default, no flag needed) — **unless the user named a different model**, which always wins | current-generation model; see "Choosing a video model" for the other two options |
| `--duration` | `5` for the compact orbit; `10`–`15` for the segmented template | a full 360-degree orbit reads clearly in 5 seconds (official case 42 does it in 5s) and keeps cost low; three or four segments need 3–5s each; Seedance 2.5 accepts 4–30. The one clip here that ran past this range went to 30s, and it did so because it was carrying spoken lines and three separate demands — see "One clip outside this skill's own boundary" |
| `--resolution` | `720p` — a `seedance-2.5`/`wan-3.0-prime` value. On `minimax/hailuo-3` use `768p`: that model has no `720p` tier | catalog/listing thumbnails rarely benefit from more; show `1080p` as a second row in the cost table when the target platform might require it (`2k` on `hailuo-3`, which has no `1080p` either) |
| `--aspect-ratio` | settled by the brief's `Aspect` question (must-ask); `1:1` is the recommended option | e-commerce platforms vary: `1:1` fits most marketplace grids (Amazon, Etsy, Shopify), `4:3` matches older catalog templates, `9:16` suits mobile-first storefronts and TikTok Shop, `16:9` suits a website product-detail page. With a photo attached, don't pass the flag — the photo is cropped or padded to the ratio instead, per `Two ways to attach the photo` above. That holds on every model, for two different reasons: `seedance-2.5` overrides the flag with `adaptive`, and another model defaults to `adaptive` precisely because you left the flag off (pass it there and it is honoured, which is not what this route wants). On the text-only route the flag really does decide the frame: `16:9` in, exactly 1280x720 out, measured on this scenario's own clips |
| Motion | camera orbits, product still — **written as timestamped waypoint pictures**: two interior views, each carrying its own shot size, and **no closing return inside the move** | *Which* motion comes from the gallery: every rotation there is written as camera movement or as a hand turning the product, and none writes a fixed-camera turntable — which now has one run of its own (job `dc02f604`, t2v, 5s): the product turned on its vertical axis with the camera fixed, and covered a quarter to a third of a turn against "most of one turn" asked for, so a 5-second clip cannot deliver a full 360 on either route. *How to write it* is measured rather than inferred, and the default would not survive without it: `the camera orbits ... a full 360 degrees` produced no orbit at all (job `1cf5ac46-058f-4615-a47b-067743f76f8c`), and the same prompt at the same seed with the angles written out as pictures produced a camera that moved (job `50f623b2-c54a-4d9d-9646-31dd06e2a926`). Three things are settled on top of that by a third, independent clip (job `8efeb556-bf38-45ec-940b-a792ef74bfcf`): a **shot size on every waypoint** kept the whole product in frame there, where an unstated one inherits the previous segment's macro closeness — ⚠️ though a fourth clip stated it and inherited a macro anyway (`cb6b7870`), so treat it as necessary and not sufficient and put a widening shot after a cut; the move covers about **half a turn** and stops, measured frame by frame; and a written return to the opening view **does not bring the camera home**, so that view belongs in the next segment after the cut. **Spacing** stays approximate — an interior view can arrive late or be absorbed, so no angle should be planned to land on a given second. Write each view as an appearance description rather than a camera position, which is reasoning from clip B's confound rather than a measurement. See "3. Camera motion: waypoint pictures, not a camera verb" and "4. A timestamp orders the pictures; it does not schedule them" |
| `--generate-audio` | `false` (this scenario's default) | a silent product clip needs no audio track; this **overrides** the server's `generate_audio: true` default, unlike `seedance-short-drama`/`seedance-ad-creative` which leave audio on. Verified against `ofox-video-core`'s script: `--generate-audio false` sets `generate_audio: false` directly on the request — and measured end to end on all three of this scenario's clips, whose delivered files carry **no audio stream at all**, not a silent one. The one exception is the out-of-scope presenter clip, which left the flag off and took the server's `true` default; if a clip has spoken lines, this default is the wrong one and has to be dropped rather than set to `true` — omitting the flag is enough. |
| `--real-person` | leave unset (`false`) | Seedance 2.5 image-to-video refuses photoreal people at submission. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person references and was measured lifting that refusal on 2.5 (2026-09-16) — an authorisation route, never a way past the check, only offered when the user holds the right to the likeness and has said so. This scenario rarely wants it anyway: a photo of the product alone locks what actually has to be right, and a person can be written in text. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

## Choosing a video model

`model` stays **never-ask** — the agent doesn't raise it as a question of
its own. But never-ask is not "never listen": `bytedance/seedance-2.5` is
only the default because nobody asked for something else. If the user names
a model — an id (`alibaba/wan-3.0-prime`, `minimax/hailuo-3`), or a
shorthand like "wan" or "hailuo" — use that model, not the default. Never
silently substitute `seedance-2.5` for a model the user actually asked for.

| Model | Cheapest tier (catalog) | Max resolution | Duration | Aspect ratios | Real moderation data point |
|---|---|---|---|---|---|
| `bytedance/seedance-2.5` (default) | 480p, 11 cents/s | 1080p | 4–30s | 7, incl. 21:9 | **Rejected** a photoreal-portrait i2v reference (`input_moderation_failed`) and a Re:Zero/Rem-styled anime t2v prompt after it had already generated (`output_moderation_failed`, copyright) — both free, nothing billed. See `.trellis/spec/skills/external-api-integration.md`, "Gotcha: moderation policy is per-model, not a platform-wide constant". |
| `alibaba/wan-3.0-prime` ("wan") | 480p, 6.4 cents/s | 1080p | 2–30s — the shortest minimum of the three | 6 — no 21:9/9:21 (this skill's four `Aspect` options don't include either, but re-check the catalog before switching, since which other ratio is missing from the 6 hasn't been re-verified here) | **Accepted** both of the clips seedance-2.5 rejected above, 12.8 cents each (2s/480p, its minimum). Only these two content classes have been tested — not a general "no moderation" guarantee for this model. |
| `minimax/hailuo-3` ("hailuo") | 768p, 8 cents/s — no 480p tier | 2k, uniquely among the three, at 13 cents/s | 4–15s — the shortest **maximum** of the three, exactly at this skill's segmented-template ceiling and below its out-of-scope 30s presenter clip | 7, incl. 21:9 | **Accepted** the same two clips, 32 cents each (4s/768p, its minimum). Same caveat: two content classes tested, not a blanket clearance. |

Price, max resolution, duration and aspect-ratio counts are catalog facts —
`GET https://api.ofox.ai/v1/models/catalog`, no API key needed, publicly
re-checkable any time — not results from a real generation. The moderation
column is the one column here that came from a real, paid API call; treat
it as evidence about exactly those two tested content classes on that date,
not a blanket policy for either model. This scenario's own clips are mostly
inanimate products with no person in frame, so the moderation difference
matters least here of the four scenario skills — it becomes directly
relevant only for the out-of-scope presenter case (see "One clip outside
this skill's own boundary"). `wan-3.0-prime` runs on two upstreams
(`alicloud`, `aliyun`) and `hailuo-3` on two (`minimax`, `novita`), neither of
which `ofox-video-core` currently pins the way Seedance's `byteplus`/`volcengine` pin works
below.

### What changes when the model changes

The defaults table above was written for `seedance-2.5`. Two entries do not
carry over unchanged:

- **`--resolution 720p` does not exist on `minimax/hailuo-3`.** That model
  offers `768p` and `2k` only, so both rows of the cost table move there:
  `768p` for the listing clip, `2k` for the higher tier. Sending `720p` is
  rejected by the script locally, before submission, for free — but a cost
  table quoting a tier the model doesn't have is wrong before that.
- **The attached photo's shape is handled per model.** With
  `--frame-first-image`, `seedance-2.5` is *forced* to `aspect_ratio:
  adaptive`; `wan-3.0-prime` and `hailuo-3` *default* to it when you pass no
  `--aspect-ratio` (which this skill's photo route already does), and keep
  your value if you pass one. The script prints a `NOTE:` saying which — relay
  it. Cropping or padding the photo to the brief's ratio before generating is
  unchanged and is still what actually decides the output's shape.

Both need `ofox-video-core` 1.22.0 or newer. Before that, a non-seedance model
with a photo attached sent **no `aspect_ratio` at all**, so the photo's shape
could be lost with nothing printed to say so.

## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.

## Several shots: timestamps inside one job, `chain` across jobs

Two different tools, not alternatives.

**Cuts inside one job are written as timestamps** — the full template's
REVEAL → DETAIL → ORBIT → ACCESSORIES is one generation. Verified on Ofox on
2026-09-03: two three-shot prompts on `bytedance/seedance-2.5`, both pinned
to `byteplus`, 8s, 480p, 16:9, `--generate-audio false`, **pure
text-to-video with no image attached**. Both rendered all three shots with
hard cuts landing within about one second of the written timestamps — one in
the bare `0-3s: … Hard cut. 3-6s: …` form, one with a header manifest and
`SHOT N (a-bs)` + `HARD CUT`.

**Those two runs no longer set the ceiling, and the route this skill actually
uses has since been measured.** Two accepted `seedance-ad-creative` jobs at
720p attached a generated product image as `--frame-first-image` and cut
inside the same job: `7ae7d49e-7eb9-4165-9d95-09cd525d53ed` (15s, 5 shots, 4
hard cuts) and `ac927785-92ef-4e28-97b9-ff8172ec5554` (20s, 7 shots, 6 hard
cuts). Every written cut happened, and in both the attached frame held the
product's shape and colours across all of them — on the second, verified as
far as t=19.6s. So **the full template's four segments are inside the
measured envelope, image attached and all**; there is no need to fall back to
three, and no need to hedge about it in the recap. **The hard-cut ceiling has
since moved to 9**: the out-of-scope presenter clip
(`e378f058-f224-4450-94b4-798840ad139b`, 30s, 720p, image attached, dialogue
on the track, two locations) delivered **10 shots and 9 hard cuts**, all nine
confirmed by reading the frames either side. Still unmeasured: more than 10
shots in one job, 1080p, the `volcengine` upstream, and a line of dialogue
split across a cut. The record, including the reason a written `HARD CUT` can
still soften, is in the shared file's `Several shots in one job`.

**Every timestamp is a cut boundary unless you say otherwise, and that clip
confirmed it 6 for 6.** Of its nine boundaries, three were written `HARD CUT`
and six were interior waypoints with nothing said about the transition; all
nine rendered as cuts. One of those six was written as a camera verb — "the
camera pushes straight in to the chest" — and delivered a cut, so a bare
camera verb neither produces a move nor prevents one being cut around it.
Write `one continuous shot` on any segment that must not be cut.

**This scenario's own clips add the text-to-video half at 720p**: 12s, the
full template's four segments, all three boundaries written as `HARD CUT`, and
all three there on a frame-by-frame read — in **all three** clips, though a
scene detector at threshold 0.25 saw only two of the three in each of them.
The reverse instruction was not contradicted in either accepted clip: `one
single continuous camera move with no cut anywhere inside this segment`
produced no detected cut inside the orbit, and the frames are consistent with
that — but the same detector pass missed a real boundary in the same clip,
so read that as "not contradicted" rather than "verified". On clip C the
frames say more than consistency does: its orbit's azimuth advances
monotonically across the whole segment with no dead stretch, which is hard to
produce by cutting. Whether the prompt's `constant speed` landed is **not**
established either way — a scene-delta reading is not a clean angular-velocity
proxy here, because near the front view the same rotation changes the picture
much less. All three in
"Measured on this scenario's own clips" above.

**`chain` carries the last frame of one job into the first frame of the
next**, then joins the clips into one file. Use it when the sequence exceeds
one job's 30s ceiling, or when each shot needs its own approval, seed or
resolution — a 5s orbit approved first, then a 5s detail push-in as a second
decision. Each shot is a separately billed job; the run estimates the total
before spending and reports real per-shot cost. The real-person restriction
that blocks chaining live-action sequences doesn't apply to objects, so
product footage chains freely.

```bash
bash ../ofox-video-core/references/ofox-video.sh chain --approved \
  --shot "the product centered on a pure white surface and backdrop; the camera orbits it 360 degrees at constant height; the product does not move" \
  --shot "the camera pushes in to a macro of the same product's label, same white background, same light" \
  --duration 5 --resolution 720p --generate-audio false
```

That is a real run — hence `--approved`, see "Before you spend" below. Swap it
for `--dry-run` to price the whole sequence first, which is the order to work
in: one `chain` command commits every shot at once.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the table's required columns, where the numbers must come from, how
to itemise a batch and what to do when no estimate is possible are written
down once, for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
Follow it rather than improvising; everything below is only what this scenario
adds to it.

Get the numbers from `--dry-run`, which validates everything and prints the
estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 15 --resolution 720p --out-dir ./out
```

Relay the `Estimated cost:` line it prints — never a number of your own — then
wait for a yes, then re-run the identical command with `--dry-run` swapped for
`--approved`. The estimate a *real* run prints comes microseconds before the
request goes out, too late to relay; that is what `--dry-run` is for.

`--approved` is where that yes gets typed out, and it is why every real-run
command in this file carries it. Since `ofox-video-core` 2.0.0 the four
billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to run
without it, while `--dry-run` never needs it, so the quote above is still free
and still works with no API key. Be exact about what the flag does: it records
a stance, it cannot prove one. Nothing in a shell script can observe the
conversation you had, and it can be typed without showing anyone a price. What
it changes is that spending without quoting is no longer the default — it has
to be written into the command, where a transcript shows it. The rule above is
still the rule, and it is still yours to follow.

The brief recap (see the creative brief section) goes in the **same
message** as the prompt and the table, above them — the user approves the
choices, the prompt and the price together.

What this scenario's table usually needs a row for: the clip itself, at the
duration and resolution you settled on — plus one row per shot when a
`chain` sequence is planned, since each shot is a separately billed job.
When the choice between a 720p draft and a 1080p deliverable is still open,
dry-run both and show two rows.

Afterwards the **actual** bill is `VIDEO_COST` from the finished job, read
from `usage.video_cost`. Report it as money (`$3.60`), not as the raw
ten-decimal string. An estimate is never a bill.

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
files.

**Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`**, and give the takes a
row each — the approval gate wants the itemised shape, not just the sum. If
one take in four is usable, that clip cost the whole total; the per-take
figure understates it by 4x.

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

**A byte-identical prompt is necessary for a re-render to land anywhere near
its draft — and it is not sufficient.** Measured on this scenario's own pair:
both clips ran seed `642303335` and the grinder is visibly a different design
in each — a wide steel collar on a short body in one, a narrow collar on a
longer body with the crank pointing the other way in the other. One paragraph
of prompt text changed and the product's appearance moved with it. So "that
take was good, let me tweak one line and keep the look" is not something the
seed can do. Neither, on the evidence above, is "that take was good, give it
to me at 1080p, identical" — that is an aim, not a guarantee, and a product
clip is exactly where a client notices the difference. Price and describe a
promotion as another roll at the same shot.

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

Nothing is broken — this skill delegates all execution to `ofox-video-core`
and reaches it by relative path, and that path just missed. Two different
situations wear this same message, so run the probe in "Where the core skill
lives" before deciding which one it is:

- **The probe printed a directory** — the core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-video-core`). Re-run the command against what the
  probe printed. Nothing needs installing.
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

Either way, say which skill is missing and where it is expected rather than
relaying the raw path error, which names neither.

A broken link to a shared reference has the same two causes. This skill
packages only its `SKILL.md` and `CHANGELOG.md`, so `prompt-structure.md`,
`creative-brief.md`, `approval-gate.md` and `api-params.md` — all shipped by
`ofox-video-core` — are out of reach whenever the script is. If the probe
found a core, the links want the same directory-name substitution the
commands do; if it found nothing, they return with the install. The skill
remains usable without them: the prompt templates, the brief's question table
and the defaults are written out in this file. What is unavailable is the
depth behind the rules they reference — the full camera and consistency
vocabulary, the general question-flow rules, and the exact wording of the
spend gate, which applies regardless.

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
directory**, and they assume the core sits beside it under its own name —
the skills.sh / ClawHub / `npx ofox-skills` layout. "Where the core skill
lives" at the top of this file has the probe for the other layouts;
substitute whatever it printed for `../ofox-video-core`. If you are running
from somewhere else entirely, adjust accordingly — from a clone's repo root
it is `skills/ofox-video-core/references/ofox-video.sh`.

## Generating

With a product photo (the common case — prefer a local file path over a
remote URL when one is available; the photo already cropped or padded to the
platform's ratio):

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the product-video prompt built above>" \
  --name "<short product name, e.g. sneaker orbit>" \
  --frame-first-image "<local path or URL to the product photo>" \
  --duration 5 \
  --resolution 720p \
  --generate-audio false
```

No `--aspect-ratio` flag here on purpose, on any model — with an image
attached the default model forces `adaptive`, and a model the user named
defaults to `adaptive` **because** the flag is absent (see `Two ways to attach
the photo` and `What changes when the model changes`). Without a product photo
(category prototype or fictional brand) the flag does take effect, and is set
to the platform ratio the brief settled:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the product-video prompt built above>" \
  --duration 5 \
  --resolution 720p \
  --aspect-ratio 1:1 \
  --generate-audio false
```

`--approved` is not decoration on either of those: without it the script
refuses, submits nothing, and prints the quote-first steps instead. Add it
only once the cost table has actually gone in front of the user and come back
with a yes — the flag cannot check that for you.

This one call validates the parameters, submits the job, polls to
completion, downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, and `VIDEO_COST`. Report the **actual** values from that
output to the user — never the estimate, and never a path/cost you didn't
see the script print. Always state the printed `VIDEO_PATH` as its own
standalone absolute-path line in your reply, per `ofox-video-core`'s
reporting requirement. Do not re-implement any of the request/poll/download
logic here; always call into `ofox-video.sh`.

## Common failure modes and fixes

These are `ofox-video-core`'s documented exit codes and error codes
(full table: [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus the product-video-specific ones:

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, no network call made | Bad `--duration`/`--resolution`/`--aspect-ratio`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| Exit `1`, `references_conflict` | `--frame-first-image` and an `input_references` array in `--extra-json` in the same job | Pick one meaning — first frame, or identity references — and drop the other |
| Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| Exit `3`, `error.code: insufficient_credits` | Ofox balance too low | No charge was made; the user needs to add credits at `https://app.ofox.ai` before retrying |
| Exit `3`, `error.code: input_moderation_failed` on an image-to-video job | The reference photo contains a photoreal person (a hand, a model) — refused at submission on Seedance 2.5, nothing billed | Use a photo of the product alone, or crop the person out. Do **not** retry with `--real-person true`: it does lift this refusal on 2.5, but it asserts that the user holds the rights to that likeness, so it is never an error-recovery step — and here the product photo is the better fix anyway |
| Exit `3`, job ends `failed`, or `invalid_request` on create, with no other error code hint | Likely a moderation rejection: a reference photo showing someone else's trademarked packaging/logo without rights, or a prohibited product category, is commonly rejected | Remove or crop the flagged trademark/brand element from the reference photo or prompt, then call `generate` again — this is a **new** request, not a resubmission of the failed one, so it's safe to retry immediately |
| Exit `3`, job ends `failed`, `error.code: output_moderation_failed` | The generated **output** failed a post-generation content check — happens after the job ran, not at submission. Not billed (no `usage` field on the response) | Retry with a brand-new `generate` call using a different prompt or reference photo — a new request, not a resubmission of the failed one, so it's safe |
| `bad_data_uri` / `download_failed` / `unreachable` / `not_image` / `too_large` | `api-params.md` documents these as `real_person: true` image-validation failures, raised when Ofox fetches the reference image: it isn't a small, valid image the API can use (a remote URL that isn't publicly reachable, or a local file that failed to read/encode) | Prefer a local file (auto-base64'd, more reliable than some remote URLs — see above); confirm it's a real image file under the size limit and retry |
| Product shape, printed text, or logo looks distorted or inaccurate in the result | Pure text-to-video was used for a real SKU instead of a real reference photo | Switch to image-to-video with `--frame-first-image` pointing at the real product photo — for a real SKU the photo is required, not preferred (see the photo section); for a category prototype, tighten the PRODUCT block instead |
| Background isn't plain, or shows props/shadows from the original photo | The prompt didn't state the background explicitly, or the source photo's busy background carried through | Add the SCENE line verbatim ("pure white surface and backdrop, no props, no shadows on the backdrop"); a reference photo with a cluttered background can still bleed through in image-to-video since the model anchors on that image |
| The output is the photo's shape, not the platform's ratio | The photo was attached without being cropped or padded first; `adaptive` follows the image | Crop or pad the photo to the brief's ratio and generate again — a new job, billed again, which is why `Aspect` is asked before generating |
| The ORBIT segment renders as a near-static front view — no new angle at all | The segment named the camera's move (`the camera orbits the product a full 360 degrees ...`) instead of picturing the frame at each angle. Measured on job `1cf5ac46-058f-4615-a47b-067743f76f8c`, where 3.7 of 12 seconds delivered nothing new | Rewrite ORBIT as timestamped waypoints — what the frame contains at two interior views, written as appearance rather than as camera positions, each carrying its own framing clause. The same prompt at the same seed, written that way, moved (job `50f623b2-c54a-4d9d-9646-31dd06e2a926`; how far it travelled is unmeasurable there, and that is stated in §3), and an independent clip written the same way moved through about half a turn (job `8efeb556-bf38-45ec-940b-a792ef74bfcf`). Do not add a closing return to the opening view inside the move — neither clip's camera came home. New prompt, so a new cost table — see "3. Camera motion: waypoint pictures, not a camera verb" |
| The orbit travels, but the product's base or top is out of frame the whole way | No shot size was written on the waypoints, so the segment inherited the framing of the macro DETAIL segment before it. Observed on job `50f623b2-c54a-4d9d-9646-31dd06e2a926`. ⚠️ It also happens **with** the shot size written — job `cb6b7870-22f7-4a15-9168-8a013805775f` stated it on all three waypoints and inherited a macro anyway | Give every waypoint its own shot size ("the whole product in frame, top to base, with margin") and close the paragraph with "at every one of those views the entire product is inside the frame, nothing cropped" — **once held (`8efeb556`), once failed (`cb6b7870`)**, so necessary and not sufficient. Then read a 480p draft's frames. If the framing must open up, put the wider view in its own shot after a cut, where three clips have delivered it. New prompt, new cost table |
| A countable feature comes back with the wrong count — four knuckles for three, five spokes for four | Expected: the description renders and the number does not. Measured on `8efeb556` (an interleaved barrel hinge, correct in material, side and geometry, with four knuckle blocks against three written) and, in `seedance-ad-creative`, on `60fbea52`, where a limb limit written twice was ignored | Nothing in the prompt reliably fixes it — check the count on a 480p draft and re-roll, or frame the feature so the count is not readable. A spatial description in the same sentence (`the whole product in frame, top to base, with margin`) *is* honoured, so keep those. See `A description is honoured; a number attached to it is not` in the shared file |
| A turntable turns, but nowhere near a full circuit — the user asked for a 360 and sees one face of the product | Expected, and the same grammar as the count row above: the rotation renders and the quantity does not. Measured on `dc02f604` (5s, 480p, 1:1, t2v) — "most of one turn" was written and a quarter to a third arrived, while the axis rotation, the fixed camera and the unchanged framing all landed exactly as asked | Not fixable in the prompt, so fix it in the brief: tell the user before the cost table that a full 360 does not fit in 5 seconds, and let them choose more seconds or accept part of the surface. Do not quote a seconds-per-turn figure — one run cannot support one. And leave the degree count out of the motion sentence; it buys nothing and sets the expectation that gets missed. See "The turntable alternative" in §3 |
| A turntable was asked for and the product is sitting still while the camera moves, or vice versa | Not something observed here — the one run did exactly what it was told on this axis. Worth checking anyway, because the two options look alike in a thumbnail and differ completely in a listing | Read three frames: if the product's contact shadow, scale and position in frame are unchanged while its surface features travel across it, the turntable happened. If the background parallaxes, the camera moved instead. `dc02f604`'s frames are the reference for what the correct one looks like |
| The orbit travels but stops half way round, never reaching the opening view it was told to end on | Expected. Both measured clips covered about half a turn and stopped: `50f623b2` happened to end on the named front view because its move began at the rear, and `8efeb556` — whose azimuth is readable frame by frame — began at the front and finished at the rear | Nothing to fix in the move. Choose two interior views that make half a turn worth watching, and if the clip has to end on the opening view, write that view as the next segment after the cut, where the timestamps hold. See "The closing return is not honoured" in §3 |
| An accessory sits forward of or behind the line it was written on | The left/right axis is controllable and depth is not, measured on `8efeb556`: `to the right of the glasses and only to the right ... nothing lies to the left` held, while `both on the same line` did not — the cloth sits forward of and below the case | Name the side (that part works, and it repairs `beside`, which was read as "on either side of" on both grinder clips), then check the depth on the draft and accept it or re-roll. One run each way, on two accessories |
| The orbit moves, but one written angle never shows up, or the views are bunched instead of evenly spaced | Expected: the pictures are honoured, their spacing is not. On job `50f623b2-c54a-4d9d-9646-31dd06e2a926` three interior views were written and two rendered, and the move held one of them for roughly 2 of its 4 seconds; on `8efeb556-bf38-45ec-940b-a792ef74bfcf` two were written and two rendered, one on time and one about 0.6s late | Nothing to fix in a delivered clip — plan for it instead: two interior pictures for a four-second orbit, no angle required to land on a given second, and read the frames rather than assuming the stamps. See "4. A timestamp orders the pictures; it does not schedule them" |
| The clip did not cut where the timestamps said, or ran the four segments as fewer | Four segments are inside the measured envelope, so the usual cause is not the count — a timeline weighted toward named continuous transitions can soften a written `HARD CUT` too | Keep the boundaries as hard cuts (this scenario has no reason to write in-camera transitions), then re-check the draft by reading frames rather than a scene detector's count — see `Checking the cuts` in the shared file |
| A scene detector reports fewer cuts than were written, and the clip looks right | Not a defect: detection cannot see a cut between two shots of the same subject under unchanging light, which is every cut in a studio product clip. This scenario's own clips are the fifth, sixth and seventh confirmations in this repo — **all three** hid their third boundary at threshold 0.25 while the earlier boundaries were found in the same pass, and the thresholds that did show them were only discovered afterwards (0.05 at 9.750s in clip A, 0.10 at 10.041667s in clip B, 0.10 at 9.71s in clip C), so lowering the default is not the fix. A fourth clip hit it **outdoors** (0.15 at 20.958s), so it is not a studio artefact — it is any cut that does not change the location | Read the frames either side of every written stamp instead of trusting the count — `Checking the cuts: read frames, never a detector count alone` in the shared file |
| A label, tag or care panel appears on the product's **inside** — lining, inner collar, inside of a pocket — despite an AVOID list that forbade tags | The no-text construction covers the surfaces it names, and a per-part list written for a static product names only outer surfaces. Measured on `e378f058-f224-4450-94b4-798840ad139b`, where a garment held open to the lens showed a neck brand label, a small tab and a care/spec panel; none resolved into readable letters at 12x, but all three are carriers `AVOID` had named | Extend the PRODUCT block's no-text declaration to the lining, the inner collar and the inside of the pockets, and name the interior carriers in AVOID one by one (neck label, care label, composition label, size tag, hang tag). **Inferred from the defect, not yet run** — check the draft. New prompt, new cost table |
| A prohibition of the form "nothing of X before second N" is broken by about a second | Expected: the cut that X sits behind carries the usual timestamp tolerance, so the prohibition's window moves with it. Measured on `e378f058`, where `no person before 8s` was broken at 6.708s because the 8s cut landed 1.29s early | Do not write the prohibition harder — move X into a later segment so the tolerance has somewhere to absorb |
| Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; tell the user to check `https://app.ofox.ai` for a job that may already be running, per `ofox-video-core`'s no-resubmit rule |
| Exit `6`, `--out-dir` could not be created or entered | Local filesystem problem (bad path, permissions), not an API problem | The job itself is unaffected — do not re-run `generate`; fix `--out-dir` and re-run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID --out-dir <a writable directory>` |

## When NOT to use

- **The deliverable is a still, not a clip.** "Four main images in different
  styles", "some listing photos", "put this product on a white background" are
  [`product-image`](../product-image/SKILL.md) — a set of stills, each an edit
  of the same product photo, priced as a set — and a single change to a single
  picture is [`image-edit`](../image-edit/SKILL.md). Both cost cents where this
  skill costs dollars, so reaching for a video generation because the request
  merely *mentioned* a product photo is an expensive misread. **The two are
  complementary, not exclusive**: producing the listing stills first and the
  clip here is a normal sequence — just two jobs with two cost tables. If a
  still is being made as this skill's own first frame, that stays here, because
  an attached image forces the clip's ratio to follow it and that decision
  belongs where the video is priced.
- Cinematic brand/mood advertising — dramatic lighting, camera language like
  dolly-ins or rim light, a brand-tone background — use `seedance-ad-creative`
  instead. This skill's prompts are deliberately plain (plain background,
  a simple orbiting camera or turntable) for literal catalog accuracy, not
  brand storytelling. The border case is a clean studio showcase with a
  lid-opening reveal (gallery case 17): the test is whether there is a brand
  narrative or an emotional tone to carry. A listing that just needs to show
  the item is this skill; a reveal that sells a feeling is the other one.
- Anything involving people, characters, or dialogue — use
  `seedance-short-drama` instead; this skill is for inanimate product objects
  only.

  **This exclusion still stands, and one clip has been run against it anyway.**
  A 30-second presenter-led commerce clip with four spoken Chinese lines was
  produced on this skill's execution layer and accepted — see "One clip
  outside this skill's own boundary: a presenter on camera". It is recorded
  because its findings bear on the templates here, not because the rule has
  moved. What it shows is that the execution layer copes; what it does not
  show is that this skill's brief, defaults and motion vocabulary fit that
  job, and four of them had to be overridden. Presenter-led commerce video is
  a gap between the four scenario skills rather than a corner of this one, and
  **whether it deserves a scenario of its own is undecided** — no new skill
  has been created and none should be inferred from that clip.
