---
name: seedance-ad-creative
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Generate a cinematic brand/product ad clip from a product description or photo using the Ofox video API (Seedance 2.5) — runs a short creative brief (product photo, brand tone, camera move, aspect ratio) when the request leaves them open, writes a timestamped shot-craft prompt (hook, showcase, slow-motion climax, hero close), shows a cost estimate, then calls ofox-video-core to submit, poll, download, and report the real cost. Use when a user asks for a commercial-style product or brand video, e.g. "give this perfume bottle a 10-second cinematic brand ad", "make a product ad for our new sneaker", "turn this product photo into a hero video for the landing page", or "I need a 15-second brand video with a slow orbit around the bottle". Do not use for dialogue-driven scenes with people talking (see seedance-short-drama).
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-ad-creative
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
    emoji: "📺"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-ad-creative
---

# seedance-ad-creative: cinematic product/brand ad clips

Turns a product description (or a product photo) into a commercial-style
video clip: camera language, product framing, and brand tone become a
Seedance 2.5 prompt, which this skill submits, polls, downloads, and reports
the cost for.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the ad-creative
prompt craft, the creative brief, recommended defaults, and the
pre-generation cost estimate; `ofox-video-core` owns talking to the Ofox API
correctly and safely (the `OFOX_API_KEY` handling, the no-resubmit rule,
error-code mapping, download/verification). **Read that skill's safety
contract before using this one** — it is not restated here.

The prompt structure shared by every Seedance scenario skill — the vendor's
formula, timestamp formats and segment lengths, transition and camera
vocabulary, consistency locks and negative lists, the two meanings of an
attached image — lives in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
Load it before writing a prompt. This file only adds what is specific to
ads.

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
This section adds only what is specific to ads.

The brief is what turns "make an ad for this bottle" into choices the user
actually made instead of choices made for them in silence. Zero questions is
common here: "15-second vertical TikTok ad for this sneaker photo, young and
energetic, slow orbit" has settled every axis.

| Tier | Ad-creative axes |
|---|---|
| **must-ask** | is there a product photo? Ask this **first** — the answer changes the whole prompt route, and every gallery ad that had to match a real product, logo or person locked it to an image (cases 12, 13, 15, 24). |
| **ask-if-open** | brand tone, the hero camera move, aspect ratio |
| **never-ask** | resolution, model, provider, audio on/off, duration when the user gave one. 720p preview vs 1080p deliverable is **two rows in the cost table**, not a question. Never-ask means the agent doesn't raise it — not that an explicit user choice gets overridden: a model named by id or by a shorthand ("wan", "hailuo") is used instead of the `seedance-2.5` default. See "Choosing a video model" below. |

If four slots are not enough: `Photo` first, then the axis that changes the
picture most (`Tone`), then `Camera`, then `Aspect`; anything left falls to a
default and the cost table.

**The product-photo question has no "Let the AI decide" option.** A photo
that does not exist cannot be invented, and "you decide" from the user
delegates the taste axes only — it never answers this one.

### The ad-creative question set

| # | Tier | `header` | Question | Options (1 = recommended, last = delegation) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Photo` | Do you have a photo or render of the product? With one, label text and shape stay faithful. | **Yes — I'll give a local path (recommended)**: the real product is rendered from the image; the gallery's product, logo and packaging shots all lock to one (cases 12, 13, 24). / **No — describe it in text**: fine for a generic or fictional product; on a real SKU the label and logo may drift. The gallery's text-only ads all stay on generic categories — a bowl of ramen (case 14), juice bottles and produce (case 27), gym gear (case 25) — and its text-only product prompts (cases 16, 17, 19) are all fictional brands. **No AI option.** | No image attached and the user did not say "no photo". |
| 2 | ask-if-open | `Tone` | Brand tone — it sets the palette, the pace and the light. | Put the archetype that fits the product category first, marked `(recommended)`: perfume / watch / jewellery → **Luxury** — slow, dark background, warm gold highlights (cases 13, 15). snack / drink / sneaker → **Playful/consumer** — bright, saturated, cuts on the beat (cases 12, 14). headphones / gadget / app → **Minimalist-tech** — white or grey, cool light, steady precise camera. Then the other two. Then **Let the AI decide** — "I'll use the recommended archetype and mark it (AI's pick)". | No tone word in the request. |
| 3 | ask-if-open | `Camera` | The camera move for the hero segment. | **Slow 30-degree orbit (recommended)**: the whole product in one move; the orbit is the gallery's most reused rotation (cases 13, 15; official case 42 does a full 360 in 5s). The 30 degrees is this skill's convention, not a gallery figure. / **Travelling move — the camera goes somewhere and the move *is* the transition**: it plunges down through the gears, passes into a spinning brass box, spirals out to a wide (case 13, all three in one 30s piece, which never cuts); pick this when the product sits in a world worth crossing rather than on a table. / **Slow push-in, shallow depth of field**: one detail fills the frame (cases 19, 24) — with a rack focus as its variant when there is a background worth showing sharp first, then snapping off (the phrasing is in the shared file's `Camera language`; its examples, cases 7 and 26, are not ads). / **Let the AI decide**. | No camera word in the request. |
| 4 | ask-if-open | `Aspect` | Where will it run? That fixes the frame shape. | **16:9 hero (recommended)**: website, YouTube, landing page — this skill's default. / **9:16 vertical**: TikTok, Reels, Shorts. / **1:1 square**: feed placements. / **Let the AI decide**. When a product photo is attached the output ratio follows the image (`adaptive`), so each description must add "= I crop or pad the photo to this ratio before generating". | No platform or ratio in the request. |

Not asked: 720p vs 1080p (two rows in the cost table); duration — take the
user's number, and if there is none use the default and say in the recap
that every gallery ad with a stated length runs 20–30s (see Recommended
defaults);
model, provider, the audio flag.

### Skip rows specific to ad-creative

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| a product photo is attached, or a path is given | Photo | have one → image-to-video; do not ask whether there is one |
| luxury, premium, high-end, elegant, "expensive-looking" | Tone | Luxury |
| young, fun, energetic, playful, bold | Tone | Playful/consumer |
| minimal, clean, tech, precise, "no clutter" | Tone | Minimalist-tech |
| "orbit", "circle around", "move around it" | Camera | slow orbit |
| "push in", "get closer", "zoom in on the detail" | Camera | slow push-in |
| "reveal", "come into focus" | Camera | rack-focus reveal |
| "spin", "turn", "360", "white background", "for my listing" | scope | that is `seedance-product-video`'s job — see When NOT to use |

### From answers to prompt — traceability

Every answer has to be findable in the prompt or the flags.

| Answer | Lands in |
|---|---|
| Photo: yes, path | `--frame-first-image PATH`, and the anchor sentence at the top of the prompt (`Begin with the exact composition of the reference image …`) |
| Photo: no | a text-only PRODUCT block; `--aspect-ratio` becomes effective |
| Tone | the STYLE and COLOR PALETTE lines of the header, and the segment pacing (Luxury: 5s segments, slow moves; Playful: 3s segments, cut-driven pace) |
| Camera | the SHOWCASE segment's camera sentence in Template A |
| Aspect | `--aspect-ratio` on text-to-video; the crop/pad step on the photo before image-to-video |
| Duration | `--duration`, and the timestamps in the timeline |

### The recap for this scenario

```
Brief:
- Photo: /Users/me/ads/bottle.jpg (given)
- Tone: Luxury (you chose)
- Camera: slow 30-degree orbit (AI's pick)
- Aspect: 9:16 (inferred from "Reels") — I will pad the photo to 9:16 first
- Duration / resolution: 15s / 720p preview and 1080p deliverable — two rows below
```

Then the full prompt, then the cost table, all in one message — the order and
the rule for a change made at the gate are in `creative-brief.md`'s `Order,
with the approval gate`.

## Prompt template

Vocabulary is not repeated here. Timestamp formats and segment lengths:
`Segmenting the timeline`; cut and continuous-shot phrasing: `Transitions`
and `Several shots in one job`; shot sizes and moves: `Camera language`;
slow motion, speed ramps and cuts on the beat: `Pacing`; the closing
blocks: `Consistency locks and the negative list`; asset role sentences:
`Reference assets as visual anchors` — all headings in
`../ofox-video-core/references/prompt-structure.md`. What follows is the
ad-specific shape.

All nine gallery ad and UGC prompts (cases 12–15, 23–27) share one skeleton:
a style or format declaration first — or the asset anchor, when an image is
attached — then a multi-beat body and a stated closing action. Seven of the
nine end on a technical tail, and six carry a negative list (cases 14, 15,
23, 24, 25, 26). The cinematic ones pace as
**hook → showcase → physical-event climax in slow motion → hero freeze**
(cases 12, 14, 15); the UGC ones as a flat action chain that ends
"naturally, not promotionally" (cases 24–27).

### Template A — cinematic ad, 15–30s

Segments run 3–5s (cases 15, 25, 26, 27); the one official 30s piece with
10s segments (case 13) never cuts. Slots are in `<angle brackets>`; optional
lines in `[square brackets]`. Pick one header labelling style and keep it.

**The beats below are a floor, not a ceiling.** Counted per case: the
gallery's ads run 5 shots in 20s (case 15, 4s each) up to 9 `CUT`s in one
generation (case 14), and case 26 runs seven segments in 30s — so a 30s spot
written as five 6-second beats is the slowest ad in the set. Split a beat into
two shots rather than holding one for six seconds; the per-case counts are in
"Shot density, measured per case" in the shared file. The Ofox-measured
envelope now reaches **20 seconds, 7 shots and 6 hard cuts in one job, with a
first frame attached** — this scenario's own accepted jobs did it (see
"Several shots: timestamps inside one job, `chain` across jobs" below) — so Template
A's four or five beats are inside what has been run, not past it. Above 7
shots or 6 cuts is still gallery practice, and a first attempt there is an
experiment.

⚠️ **That warning was only ever about the shot *count*, and a count is half
of the problem.** It was in this file, in these words, when a 15s ad was
written as five beats at the floor — and the clip was rejected as "too
simple, too monotonous" anyway, because three of those five beats contained
no physical movement at all. A beat can be at the floor and still be dead;
"a floor, not a ceiling" says nothing about what happens *inside* a beat. The
missing half is now written down as **7. Every beat needs a physical event —
and "slow" is not "still"** below, and it is the first thing to check after
the beat count.

```
[FORMAT: <N> seconds, <16:9 | 9:16 | 1:1>, hard cuts on the timestamps.]            — optional; must match the flags
STYLE: <ad category> commercial, <capture anchor: 8K photoreal studio | 35mm film grain | glossy high-speed>, <tone: luxury — slow, dark, warm gold | playful — bright, saturated, fast | minimalist-tech — white or grey, cool, steady>.
COLOR PALETTE: <dominant>, <the product's warm or cool accent>, <contrast colour>, <metallic accent>.                        (case 14)
[CHARACTER: <one block — age range, build, hair, wardrobe item by item with colours, one signature accessory>. Referred to below as "<tag>".]   (case 14; text only — see the real-person note below)
PRODUCT: <shape> <material and finish> <colour> <product name>, <label text in quotes, verbatim>, <contents or accessories item by item>.
         [@image1 supplies the product exactly — <shape, label, cap, colour>; ignore its background.]                   (cases 12, 24)
SCENE: <backdrop>, <one or two props framing the shot>, <light: saturated studio key with a warm rim | golden hour | single hard key>.

0–<3–5>s    HOOK — <one visual focus: a macro of one ingredient | the cap | the clock face>; <one strong move: a hard cut lands as the detail completes its motion | low-angle dolly-in | a white flash freezes the frame | layers unfold>.   (cases 12, 13, 15, 14)
<TRANSITION between any two beats — name a kind; a hard cut is one of nine and an unnamed boundary becomes one: HARD CUT. | The camera plunges through <the gears / the pour / the open lid> into the next beat. (case 13) | <The product / the blade / a hand> sweeps past the lens and the camera comes out of the occlusion on <the next arrangement>. (the phrasing is cases 2, 8, 41, none of them ads) | A white flash freezes the frame, then <the next pose>. (case 15) | An extreme speed ramp carries <the event> into <the next beat>. (case 15) | Without cutting, <the array reassembles in frame>.>
<>–<>s      SHOWCASE — <arrangement: a strict geometric array of the variants | <tag> holds the product toward the lens, steam rising | the camera orbits the product 30 degrees>; cut to close-ups of <two or three details>. <one physical event in this beat — required, see slot notes>   (cases 12, 14, 24)
<>–<>s      CLIMAX — <one physical event: the biscuit snaps | the broth erupts | the blade sweeps past the lens>; drops into slow motion for one second — <micro-detail: the filling bursts, crumbs fly, droplets hang> — then back to speed.   (cases 12, 14, 15)
[<>–<>s     PAYOFF — <the event's result, as its own timed shot: the drop lands and one ring spreads and dies | the crumbs settle on the white>; full speed, and the landing named as a required visible event.]   (only when the payoff is small and fast; job 60fbea52 wrote it as CLIMAX's tail and lost it, job cb6b7870 gave it its own stamp and got it — slot notes below)
[<>–<>s     VARIATION — back at full tempo, <a second arrangement>.]                                                        (case 12)
<>–<N>s     CLOSE — product hero frame, <centered | in slow motion>; [the slogan "<text>" enters word by word, one word per cut;] [the logo per image2 in the last second;] hold the final frame.   (cases 12, 13, 14, 15)

CAMERA: handheld energy and high-speed slow motion on the <climax>; smooth static holds on the <showcase>; cinematic shallow depth of field throughout.   (case 14)
AUDIO: <room tone of the set>; <two or three recorded sounds tied to visible actions: the cap breaking its seal, the snap, fabric, a footfall in dust>; no dialogue. No music — see "4. No dialogue, no music — but a sound block" below.   (jobs 7ae7d49e, ac927785)
CONSISTENCY: the product's shape, label, colours and proportions stay identical in every shot[; <tag>'s face, hair and wardrobe do not change].   (cases 24, 15)
AVOID: dialogue, subtitles, on-screen text other than the slogan card, watermarks, jitter, identity drift, wardrobe change, warped hands, extra limbs; music, score, soundtrack, instrumental, melody, rhythm track, percussion, <named instruments: cello, strings, piano, bell, chime>, humming, singing.   (cases 15, 24, 14; the music items are jobs 1ff72400 / 7ae7d49e)
```

Notes on the slots:

- **Every beat carries one physical event, `SHOWCASE` included.** This is the
  slot where an ad goes quiet: it is the one whose job is "show the product",
  and a rejected 15s spot spent it on an orbit that never moved — six frames
  sampled across it hold the same orientation, the same cap perspective and
  the same highlight. Name something that happens — the product is set
  down, a hand enters, liquid moves, steam rises, a cloth is pulled away —
  and check the whole timeline for a beat carried only by light sliding
  across a surface. The measurement and the three repairs are in "7. Every
  beat needs a physical event — and 'slow' is not 'still'" below.
- **Anchor sentences when an image is attached** — put them first, before
  STYLE (cases 15, 24 both open on the asset):
  `Begin with the exact composition of the reference image.` (case 15, a
  `--frame-first-image` job) ·
  `Preserve the product exactly as in @image1 throughout — frame shape,
  lenses, hinges, colours, materials, proportions.` (adapted from case 24) ·
  one role line per asset, `@image1 supplies product appearance; @image2
  supplies the logo, last second only.` (cases 12, 13). Sentence patterns and
  the `@image1` caveat:
  `Reference assets as visual anchors`.
- **Several pieces or an unboxing** (case 24): name every piece and lock each
  — `Use the uploaded sunglasses, retail box and leather case as locked
  product references` — then run the showcase as a chain: box opens → case →
  product lifted → rotated to show hinges and lenses → worn, turned to
  catch the light → held beside the face → push in on the product, fade.
- **A person interacting with the product** (case 14): one CHARACTER block,
  then the tag in every segment (`the model holds the bowl toward the lens
  with both hands, steam rising`). **Describe the person in text** — and note
  that this is a full route, not a consolation prize: see "A model *and* a
  locked product: the route that works" below. Gallery cases 15 and 24
  attached real-person images on other platforms; do not read them as Ofox
  behaviour.
- **Order the framing so the risky anatomy stays small.** A person in an ad
  is where hands, faces and limb counts go wrong. Job
  `ac927785-92ef-4e28-97b9-ff8172ec5554` (20s, 7 shots, a runner and a shoe)
  came back with no deformation at all, and the thing it did differently was
  the order: **foot → hand and ankle and lower leg → lower leg and knee →
  the foot again in slow motion → full body exactly once, and that once
  distant, from behind, head turned away → the set empty again.** Focus stayed
  on the product in all seven shots and never on the person. So: escalate how
  much of the body is in frame, keep the full figure to one distant shot, and
  never make a hand or a face the focal point. Avoiding people entirely is
  not the only option.
  **What that run did not establish is that a written size limit works, and a
  later one shows it does not.** Job
  `60fbea52-b14b-4796-80bf-03afe0aa4fa0` (a hand entering a macro on a
  dropper) said twice — once in the shot and again in AVOID — `only the
  fingertips and the first knuckle ever visible and never more of the hand
  than that`, and the render shows most of the index finger and the hand to
  the knuckles. The shot was still anatomically clean, with no extra or
  warped fingers, and what kept it clean was the macro framing plus one
  simple action, not the limit. Write the framing order above; treat a "never
  more than X of a limb" clause as a wish, not a second line of defence.
- **Give the climax's payoff its own timed shot when that payoff is small and
  fast.** Measured once, on `60fbea52-b14b-4796-80bf-03afe0aa4fa0` (15s, 5
  shots, accepted): a five-second CLIMAX was written as `7-8.5s` the pipette
  lifts clear of the bottle, `8.5-10.5s` in slow motion a drop swells at the
  glass tip and falls, `10.5-12s` back at full speed `the drop lands on the
  surface of the oil in the bottle, one clean ring spreads out and dies
  against the glass`. The build-up rendered beautifully and **the landing
  never happened**: at 11.8s the drop is still hanging from the pipette, and
  at 12.25s the clip cuts to the hero frame. Five and a half seconds of
  climax bought a suspended drop and no event. A hanging, glowing droplet is
  exactly the kind of picture this model is good at, so it made that and
  skipped the fast physical beat at the end of it. The counter-measure is to
  **write the payoff as its own timestamped shot with its own share of the
  seconds**, compress the build-up to pay for it, and name the result as a
  required visible event (`the drop must be seen to leave the tip, land, and
  ring the surface`) instead of trailing it off the end of a longer shot.
  That is what the optional `PAYOFF` line in the template is for.
  ✅ **That counter-measure has now been run, and it worked** — the first
  time it was tried, on `cb6b7870`. The payoff got its own boundary at
  `11-13s`, separate from the CLIMAX before it, and its own required-event
  sentence: `A column of white steam must be seen to rise out of the open
  mouth of the bottle, climb into the warm key light where it glows, and
  drift off to the right. This is a required visible event: the steam has to
  leave the neck and travel up through the light within these two seconds,
  not merely hang above it.` The steam rises, glows and drifts, confirmed at
  t=12.5s — one of only two segments in that clip where anything physical
  happens at all, in a clip rejected for being too still. Two things to copy
  from the wording: the
  event has its **own timestamp**, and the clause naming what it must **not**
  do (`not merely hang above it`) describes the earlier failure exactly.
  One before-and-after pair on two different events, not a controlled test —
  but the fix is no longer a hypothesis.
- **A continuous state change can be one of the listed changes, if its
  direction is pinned.** A consistency lock normally reads "nothing changes
  except these things", and the things are discrete events. The same job also
  let one *continuous* drift through, and it rendered correctly: the bars of
  window light from the blinds were allowed to `only ever creep lower and
  warmer, never brighter, never higher, and never change direction` — named
  as the single permitted drift in a scene whose props were otherwise nailed
  down. Opening and closing frames confirm the bars moved, and moved the
  written way. One observation on one clip, but it means a dimming afternoon
  or a cooling set does not have to be broken into discrete steps to be
  controlled.
- **An extreme macro inside a homogeneous liquid is the weakest showcase shot
  on record here.** The same job's 2.1-second macro inside amber serum came
  back as a near-flat colour field with two soft refracted light bands:
  competent, and nothing to watch. The comparable shot into a carbonated
  drink carried itself on rising bubbles (`7ae7d49e`). One observation each
  way, so read it as a warning rather than a law — a liquid macro needs
  something inside the liquid that moves.
- **Do not ask the model for music.** The AUDIO slot above used to read
  `<upbeat | cinematic | minimal> instrumental; percussion hits synced to
  <the climax event>` — copied from cases 12 and 14, and **that is the shape
  that got refused here**. A prompt asking for "one sustained low cello note"
  and "a soft bell chime" came back `failed` with
  `error.code: output_moderation_failed` and the upstream message `the output
  audio may be related to copyright restrictions` (job
  `1ff72400-0f30-4be1-a417-f52d43955d09`, 2026-09-04). Nothing was billed.
  Keeping only recorded, diegetic sound and naming the music words in AVOID
  passed on the next run (`7ae7d49e-7eb9-4165-9d95-09cd525d53ed`); the next
  ad in the same batch wrote it that way from the start and was also clean
  (`ac927785-92ef-4e28-97b9-ff8172ec5554`). One refused sample, so the exact
  trigger is unknown — but a real ad's music is laid in afterwards anyway, so
  the cost of complying is nothing. Detail: "Asking for music can fail output
  moderation on copyright" in the shared file.
- **Slot pacing by tone**: Luxury runs 5s segments and slow moves (case 13);
  Playful runs 3s segments and cuts on the downbeat — the *cuts*, not the
  music the downbeat came from (cases 12, 14). ⚠️ Luxury's longer segments
  raise the stakes on the rule above rather than relaxing it: a 5-second beat
  with no event in it is 5 seconds of nothing, where a 3-second one is only
  3. If a Luxury beat has no physical event available, split it into two
  shorter shots instead of holding it.
- **Five beats in 15 seconds has now been run three times, and an uneven
  duration
  split is honoured closely.** `7ae7d49e`, `60fbea52` and `cb6b7870` are all
  15s, 5
  shots, 4 hard cuts, first frame attached, and all three kept every cut —
  `cb6b7870`'s four landed at 3.000 / 7.542 / 11.042 / 13.250s against
  written stamps of 3 / 8 / 11 / 13, so within half a second each way. ⚠️ And
  the third of those was **rejected**, which is the point worth carrying: the
  structural half of this template is now well verified and the structural
  half is not what decides whether an ad is watchable. See 7 in "Writing a
  good ad-creative prompt". On
  `60fbea52` the per-shot budget was planned 3 / 2 / 2 / 5 / 3 seconds and
  rendered 2.62 / 2.13 / 1.87 / 5.63 / 2.79 — every segment within 0.4s of
  its plan, including a deliberately lopsided split that gave the climax more
  than twice any other shot. So spending the seconds by function rather than
  evenly is a real instrument on this path, not a hope. (This bullet used to
  warn that four or five beats was past what had been verified; that warning
  was retired in 1.9.0, and this is what replaced it.)

### Template B — 10 seconds or less, three beats

Inferred from the 15–30s cases; **the gallery has no ad prompt of 10s or
less** (the shortest stated length is 20s, cases 15 and 27). No header
manifest — the vendor's formula order, subject and action first (shared
file, `The vendor's own formula (ByteDance first-party)`).

```
<Product> <one action or event> on <backdrop>; <tone archetype>, <capture anchor>. [@image1 supplies the product exactly; ignore its background.]
0–3s: <a macro of one detail>; a hard cut lands as it completes its motion.
3–7s: <the physical event> in slow motion — <micro-detail>; rim light along the edge.
7–10s: product hero frame, centered; [the slogan "<text>" | the logo per image2 in the last second;] hold the final frame.
<light line>. <palette line>. No music; ambient/SFX only; no dialogue. No subtitles, no watermarks, no jitter.
```

### Worked example — adapted from case 12 (translated), timestamps added

The official fruit-biscuit ad, moved from its prose-ordered original into
Template A at 20 seconds. The original reads the strawberry variant from an
attached image and takes composition, motion and impact from six reference
clips; Ofox allows one video reference, so this version keeps only the
image. Word choice is ours; the beat order, the snap-in-slow-motion climax,
the word-by-word slogan and the scatter ending are the original's.

Case 12's own audio direction is an upbeat instrumental with the cuts synced
to its downbeat. **That part is not carried over here** — this version
replaces the scored cue with recorded sound only, because asking this model
for music has failed output moderation on audio copyright here (unbilled;
see "4. No dialogue, no music — but a sound block" above, and "Asking for
music can fail output moderation on copyright" in the shared file). A score
can be laid over the delivered clip afterwards, which is where case 12's
instrumental would have to come from anyway — so, unlike the rest of this
adaptation, the AUDIO line and the beat-timed cues below are a deliberate
departure from the original, not a translation of it.

```
FORMAT: 20 seconds, 16:9, hard cuts on the timestamps.
STYLE: bright, multicoloured snack commercial; clean, premium, strongly rhythmic; glossy high-speed capture.
COLOR PALETTE: strawberry red, mango yellow, blueberry violet and kiwi green on white; gold foil accents.
PRODUCT: rectangular fruit-filled biscuits in four flavours, each beside its fruit; @image1 supplies the strawberry variant's exact packaging and filling colour; ignore its background.
SCENE: white seamless backdrop, the fruit as the only props, saturated studio key light with a warm rim.

0–3s    HOOK — a single strawberry fills the frame in macro; the cut lands as it rotates to catch the key light.
3–9s    SHOWCASE — the four biscuits and their fruits in a strict geometric array, orderly and bright; cut to a close-up of each variant.
9–13s   CLIMAX — one biscuit snaps; the instant drops into slow motion, the fruit filling bursts open and crumbs fly; back to speed.
13–16s  VARIATION — full tempo again, the biscuits in a horizontal row.
16–20s  CLOSE — the words "One bite of crispness, a heart full of delight" enter word by word, one per quick cut; product freeze frame, centered; biscuits and fruit scatter outward.

CAMERA: handheld energy on the snap, smooth static holds on the arrays, shallow depth of field throughout.
AUDIO: studio room tone; SFX: the biscuit's snap, crumbs scattering, fruit skin catching the light; no dialogue. No music.
CONSISTENCY: packaging colours, biscuit shape and filling colour identical in every shot.
AVOID: dialogue, subtitles, on-screen text other than the slogan, watermarks, jitter, music, score, instrumental, percussion.
```

### UGC variant

Five of the nine gallery ad prompts are creator-style clips (cases 23–27).

⚠️ **UGC now has its own skill — [`ugc-ads`](../ugc-ads/SKILL.md) — and it is
the better route.** The table below is a slot diff against this skill's
cinematic template; that skill inverts the polish default outright, which is
the part this file cannot do while its own archetypes are Luxury, Playful and
Minimalist-tech. Hand "make it look like a real customer filmed it" to
`ugc-ads`. Keep reading here only when the clip is fundamentally an ad that
wants a creator-ish surface — and even then, compare with that skill first.

This skill's `description` does not claim creator clips, but the request lands
here often enough that the slot differences are worth having. The boundary is
what carries the clip: a creator holding, using and describing the product
goes to `ugc-ads`; a scene carried by the performance and the exchange between
people is `seedance-short-drama`, per this skill's `description`. Same
skeleton as Template A; these slots change:

| Slot | Template A (cinematic) | UGC variant | Cases |
|---|---|---|---|
| STYLE | commercial + studio anchor | `realistic UGC-style … filmed on a smartphone`, `handheld`, `authentic, imperfect, no polished commercial look` | 24, 25, 27 |
| Capture line (new) | — | the **viewpoint**, written as a property of the shot (`selfie viewpoint` · `handheld` · `a fixed viewpoint at bench height, slightly low`) plus its flaws: `autofocus hunting, exposure shifts, compression artifacts, mild sharpening`. ⚠️ never where the phone *is* — see below | 25, 27 |
| Anchors | product image | a person image **and** each product piece, locked item by item — real-person frames are refused on Seedance 2.5 image-to-video, so on Ofox this is a text-described person | 24 |
| HOOK | macro + a hard cut on the motion | the person enters the scene, or the first line to camera | 24, 27 |
| CLIMAX | physical event in slow motion | none — a flat action chain (unbox → turn → try on → catch the light) | 24 |
| Dialogue | none | one quoted line per beat (a review), or a single closing line that is `spontaneous, slightly breathless, not scripted` | 24, 25 |
| AUDIO | room tone + SFX, no music | an ambience list (`natural gym ambience only`, eight sounds named); no music or low music | 25, 26 |
| CLOSE | hero freeze + slogan | `holds them beside her face` + push in + fade · walks out of frame while `the camera continues recording for a moment` · `not promotional` | 24, 25, 26 |
| AVOID | text, jitter, drift | adds `cinematic color grading, beauty filters, artificial skin smoothing, dramatic slow motion, music, perfect lighting` — the opposite of this skill's default look | 25 |
| Aspect | 16:9 | 9:16 appears (case 27); 16:9 also (cases 24–26) | 27 |

⚠️ **Two cells in that table are gallery quotes that render the camera into
the scene.** Case 25/27's `propped on a gym bench, slightly low angle` and
case 25's `the camera continues recording for a moment` both give the filming
device a position or a presence, and measured 2026-09-15 on job `2ecbedec`
(88 cents, `ugc-ads`' first paid run), that construction delivered **a phone
sitting in the scene, visible in every frame, with a lit screen**. The model
has no concept of an off-screen camera: a noun with a position in the room is
set dressing. Write the viewpoint instead (`a fixed viewpoint at bench height,
slightly low`, `the shot keeps running for a moment`), and add `a phone, a
camera, a tripod or a lit screen visible anywhere in the shot` to AVOID as
objects. The full note, the safe-versus-renders split and the mechanical
conversion are in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)
→ `Camera language` → `Camera movement`, under the `Phone POV` row. Nothing in
the tooling catches this: it passed `--dry-run` and `--print-payload`, and
only the extracted frames showed it.

## Writing a good ad-creative prompt

### Where the product goes

Earlier versions of this skill said: product first, then camera, then mood.
The gallery does not support that order. All nine ad and UGC prompts open
with a style or format declaration — or, when a reference image is attached,
with the asset's anchor sentence, as cases 15 and 24 do — and place the
product second or third (case 14 runs `Style:` → `Character:` → `Subject:` →
`Setting:`). There is
no A/B evidence that either order renders the product better; there is
simply no collected prompt that leads with the product. So:

- **15s and longer**: header manifest — FORMAT → STYLE / COLOR PALETTE →
  CHARACTER (if any) → PRODUCT → SCENE → timeline → CAMERA → AUDIO →
  CONSISTENCY / AVOID. Template A above; the shared file's `Prompt skeleton:
  header manifest, timeline, closing block`.
- **10s and shorter**: the vendor's formula order — subject and action first,
  then scene, style, camera, sound, in two to four sentences and no
  manifest. Template B above; the shared file's `The vendor's own formula
  (ByteDance first-party)`.

### 1. The product, described precisely

Shape, material, colour, finish, and any text on it verbatim in quotes.
Finish drives how light behaves on the surface (glass, brushed metal, matte
plastic), so name it (case 14's `Subject:` lists five ingredients; case 17
names the accent colour and every accessory).

```
A tall clear glass perfume bottle with a gold cap, "NOCTURNE" embossed on the front, centered on a reflective black surface.
```

### 2. Camera as a real shot, with a speed

Concrete cinematography terms steer the model; "make it look cool" does not.
The full vocabulary is in the shared file's `Camera language`; the moves ads
reuse most are the **30-degree orbit**, the **slow push-in with shallow
depth of field**, the **rack focus from background to product** and the
**pull-back reveal** (cases 13, 15, 19, 24, 26). Ads also carry a speed
dimension the other scenarios rarely use — **slow-motion insert**, **speed
ramp**, **freeze**, **static hold**, **cut on the beat** — in the shared
file's `Pacing` (cases 12, 14, 15).

```
The camera orbits the bottle 30 degrees; soft rim light along the glass edge; shallow depth of field, the background gently blurred. The cap turn drops into slow motion for one second.
```

### 3. Brand tone, as an archetype plus a palette line

One archetype word steers grade and pacing more reliably than a paragraph of
adjectives; a `Color palette:` line (case 14) pins the colours it implies.

- **Luxury**: slow movement, dark or moody background, warm gold highlights,
  5s segments (cases 13, 15). ⚠️ **`slow movement` is a speed, not a
  quantity — read it as "the movement is slow", never as "there is little
  movement".** This line as written above is what a rejected flask ad turned
  into three separate sentences pinning the camera and the product still; see
  7 below for the measurement and the three repairs.
- **Playful/consumer**: bright saturated colours, faster movement, cuts on
  the beat, 3s segments (cases 12, 14).
- **Minimalist/tech**: clean white or grey background, precise steady camera,
  cool light.

The negative list is where you name the tone you are *not* making — a Luxury
prompt excludes `cartoonish, oversaturated`; a UGC prompt excludes
`cinematic color grading` (case 25).

### 4. No dialogue, no music — but a sound block

Cinematic ad clips carry no speech (cases 12, 13, 15; case 14 allows one
vocal ad-lib), so say `no dialogue` to steer away from voice generation. Do
not stop there: write an AUDIO line, but write it as **room tone plus two or
three recorded sounds keyed to visible actions** — the cap breaking its seal,
the snap, a footfall in dust — and exclude music explicitly.

**The music half of case 14's AUDIO line does not transfer to Ofox.** A
prompt asking for a cello note and a bell chime failed
`output_moderation_failed` with `the output audio may be related to
copyright restrictions` (job `1ff72400-0f30-4be1-a417-f52d43955d09`, not
billed); the same ad without music passed
(`7ae7d49e-7eb9-4165-9d95-09cd525d53ed`). Score goes in afterwards, in an
editor, the way it does on a real spot. Shape and phrases: the shared file's
`Dialogue and sound`, and `Asking for music can fail output moderation on
copyright` for the measurement.

**A loudness written per shot is not honoured — write what each shot
contains, not how loud it is.** Measured on job
`60fbea52-b14b-4796-80bf-03afe0aa4fa0`, whose shot 2 read `Sound: room tone,
nothing else, very quiet` and came back as the loudest sustained passage in
the clip. Mean level per second: about -44.6 and -43.3 dB over the opening
shot, then -27.8, -24.3 and -27.0 dB across shot 2, back to roughly -37 to
-41 dB for the middle of the clip, and -47.7 then -54.4 dB in the last two
seconds. Two thirds of that AUDIO block did work: the loudest transients land
exactly where sound effects were written — peaks of -10.1 dB at 7-8s (the
pipette lifting) and -11.9 dB at 10-11s (the drop) — and the close thinned to
near silence as asked. What was ignored is the *relative* level between
shots. So **do not plan a clip whose effect depends on one shot being quieter
than its neighbours**; name each shot's sounds and leave the mix to an
editor, the same way the music goes on afterwards.

**A sound written as `faint` can be honoured as inaudible, while the
placement instruction still works.** Measured on `cb6b7870`, whose AUDIO line
named three cues: the cap thread turning, `the short pneumatic tick of the
seal parting at 9s`, and `a faint hiss of steam at 11s`. The first two
landed clearly — the level rises off a -43 to -46 dB room-tone floor to
-30.9 dB at 7.7s and to a -21.7 dB peak across 8.8-9.2s, the loudest
sustained passage in the clip and exactly where the seal was written. The
third produced nothing measurable: at 11.5s the level *drops* to -41.6 dB and
stays near the floor for the whole PAYOFF, though the steam is plainly
visible on screen. So **timing a sound to a visible action works and an
intensity adjective is not a volume control** — do not hang a beat's effect
on a sound you have described as faint. Second observation of the transient
half, first of this nuance.

### 5. Text on screen: lock it, or design it out

Two measured facts pull in opposite directions, and both are usable — plus
one refinement of the second, from the run that tested it hardest.

- **Text you want** — a brand name, a wordmark — is reliable if it exists on
  the attached first frame and the video only has to preserve it. Job
  `7ae7d49e` closed on a legible wordmark in the frame's own typeface,
  because the label was approved on the still first. Rendering the same text
  from a description is the classic failure; read the label at full size
  before spending on the clip. Confirmed a second time on `60fbea52`, where
  the label word `AURA` survived unaltered in every shot it appeared in
  **and** the same word rendered correctly as an end card in an empty patch
  of wall. What was written for it: the reference frame declared `the only
  authority on how this product looks`, the letterforms and the letter
  spacing named as invariants, and an explicit ban — `do not regenerate,
  redraw, restyle, re-letter, translate or reword the label`, and no second
  word, slogan, barcode or volume marking added to it.
- **Text you don't want** is best removed by the set, not by the negative
  list. Both ads in this batch produced **zero** invented signage, and the
  reason is that a near-black studio and an empty bright studio contain no
  surface lettering could sit on. Compare a job on a neon street whose AVOID
  list named signs, posters and characters in any language and still returned
  sign-like shapes (`41f87ac7`). Detail: `Unwanted text is designed out of
  the set, not forbidden in the list` in the shared file.
- **Where the set cannot be emptied, forbid the objects rather than the
  text.** The two studio ads are the easy case: nothing in a near-black or an
  empty bright studio can grow signage, so the rule was never really tested
  by them. Job `60fbea52` is the hard case and the strongest data point in
  this repo — a **desk**, where book spines, notebooks and loose paper are
  the classic failure mode, and a brief that wanted a real brand word legible
  in the same frame. It came back with **zero** invented text. Two things
  were written for it, both more specific than a negative list: the wall was
  specified as `entirely bare — no shelf, no book, no picture, no poster, no
  notice and no printed surface of any kind anywhere in the room`, and AVOID
  named every carrier of printed matter one by one — book, book spine,
  notebook, sticky note, paper, envelope, card, packaging box, carton,
  magazine, newspaper, phone, laptop, screen, shelf, picture frame, poster,
  signage. So the shared rule stands and gains a clause: design the text out
  of the set where the set allows it, and **in a setting that naturally
  contains printed matter, name and exclude each carrier as an object** — a
  bare "no text" has already failed once, on a neon street (`41f87ac7`),
  while an object-by-object exclusion has held once, on a desk.

### 6. What the AVOID list has held, and what it has lost

The list is worth writing and it is not a guarantee. An honest record of this
scenario's own accepted runs, so nobody plans a shot around an item that has
already failed:

| AVOID item | Record |
|---|---|
| any text other than the brand word | **no invented text in any of the four** ads, including once in a text-hostile set — see 5 above. The work was done by the set and by the object-by-object exclusion, not by the phrase "no text". The fourth (`cb6b7870`) is the easy case again — a near-black empty studio — and its real brand word also survived unaltered in every shot it appeared in |
| `no lens flare stars, no sparkle particles` | **lost once.** A small starburst glint sits on the drop at about 9.6s of `60fbea52`, in a clip whose AVOID named both. Minor, arguably attractive, and not asked for |
| `never more of the hand than the fingertips and first knuckle` | **lost once**, and it was stated twice in the same prompt — see the framing-order slot note in Template A |
| music, score, named instruments | not really tested by the list: what keeps music out is not asking for it (4 above), and the one prompt that did ask was refused before it rendered. `cb6b7870` named fourteen music words in AVOID *and* asked only for diegetic sound, and passed — which confirms the combination, not the list |
| `a faint hiss of steam` as an audible cue | **lost once**, on `cb6b7870`: no measurable level event at all where it was written, in a clip whose two other sound cues landed loudly and on time. An intensity adjective is not a volume control — 4 above |

Three of those rows are a single observation each. What they add up to so far
is a shape rather than a rule: **an item that removes a whole class of object
from the set holds better than one that asks for a fine-grained quantity, or
for the absence of a small visual flourish.**

### 7. Every beat needs a physical event — and "slow" is not "still"

**Measured on job `cb6b7870-22f7-4a15-9168-8a013805775f`** (15s, 720p, 5
shots, 4 hard cuts, generated first frame attached, Luxury tone) — **rejected,
and the only ad rejected in this scenario so far.** The verdict was that it
rotates the product once and then nothing much happens: too simple, too
monotonous. Everything this file normally checks came back clean. All four
cuts landed, the shot budget held, the etched brand word survived unaltered
in every shot it appeared in, a near-black studio produced zero invented
text, and the payoff beat worked. What failed is **how much of the 15 seconds
contained visible motion.**

**Read off the frames, per segment** — two frames per second across the whole
clip, plus six frames sampled through the SHOWCASE at 3.1 / 4.0 / 5.0 / 6.0 /
7.0 / 7.4s:

| Segment | What actually happens in it |
|---|---|
| HOOK — macro on the grain | nothing moves; a specular streak slides down the metal |
| **SHOWCASE — the orbit** | **nothing.** All six sampled frames hold the same bottle orientation, the same cap perspective and the same highlight position. The written 0° → 45° → 90° move did not happen |
| CLIMAX — the cap lifting | a real event: the cap turns, the seal parts, the thread clears the collar |
| PAYOFF — steam rising | a real event: steam leaves the neck, glows in the key, drifts right |
| **CLOSE — hero frame** | **nothing, by design** — a held hero frame to the end |

So **two of five segments contain no physical event at all** and a third
(HOOK) contains only moving light. Counting the seconds where something
visibly happens — the cap and the steam — gives roughly **5.5 seconds of
event in a 15-second spot**, a third of the runtime.

⚠️ **Do not try to establish this with a per-segment scene score. It is
measured here and it points the wrong way.** Mean inter-frame `scene` score
at native 24fps, segment boundaries at the detected cuts and each segment's
own cut frame excluded: HOOK 0.0078, SHOWCASE 0.0039, CLIMAX 0.0077, PAYOFF
0.0008, CLOSE 0.0003. That ranking puts the steam — the one beat everybody
agrees is alive — second from the bottom, and the motionless orbit in the
middle of the field. The reason is that `scene` measures **whole-frame pixel
churn, not motion**: a bright specular streak sweeping a large brushed-metal
body changes a great many pixels while nothing moves, and a thin wisp of
steam against near-black changes very few while something plainly does. On a
dark-background product clip the metric is close to anti-correlated with what
a viewer calls movement. The shared file already says not to read a camera's
angular velocity off a delta count; this is the same mistake one step further
out. **Sample frames and look at them.**

**The cause is three sentences that were written deliberately**, each
defensible alone and jointly fatal: `the camera holds still` (HOOK), `the
bottle itself never moves or rotates` (SHOWCASE) and `the camera is
completely still and the bottle does not move` (CLOSE). The middle one is the
instructive failure. It was written to stop the product self-rotating — a real
risk, and it worked — but nothing was given to the camera in exchange, so the
segment ended up with a still product **and** a still camera. A negative
clause about the subject is not a camera instruction, and pairing the two
without noticing is easy in a tone whose own definition is `slow movement`.

**The two accepted ads at the same spec are the control.** `7ae7d49e`
(sparkling tea) and `60fbea52` (serum oil) are both 15s, 5 shots, 4 hard
cuts, first frame attached — the same envelope, the same template, one
accepted verdict each. The difference is that **every segment of both
contains a physical event**: bubbles rising continuously through the tea in
one, a hand entering, a pipette lifting and a droplet falling in the other.
Neither is faster-cut than the flask ad. They are simply never empty.

Three repairs, in the order to apply them:

1. **No pure-display beat.** Every segment needs one nameable physical event
   — something enters, opens, falls, pours, rises, turns, or is set down.
   Light sliding along a surface is not an event; it is what a still shot
   looks like under a moving key. The `SHOWCASE` slot in Template A is where
   this goes wrong most easily, because "show the product well" reads as a
   licence to hold on it.
2. **In a Luxury spot, `slow` describes the speed of the movement, not
   whether there is any.** A slow orbit is still an orbit. Sentences of the
   form `the camera holds still` / `completely still` / `does not move` are a
   misreading of the archetype when they are the whole of a segment's camera
   direction — keep them for a final hero frame that has earned it, and even
   then note that this clip's held CLOSE was one of the two motionless
   segments that sank it.
3. **A low-motion product needs an external source of motion.** This is the
   one that generalises past Luxury. A sneaker can be jumped in, a carbonated
   drink carries its own bubbles — a sealed steel flask can do essentially
   nothing on its own, and no amount of prompt craft will make its body move.
   Bring the motion in from outside: pouring water, ice dropping, steam, a
   hand, moving air, a cloth pulled away. Or spend the budget on cuts
   instead — **raise the shot count from 5 to 7**, which is inside the
   measured envelope at 20s (see "Several shots" below). Deciding which
   before writing the prompt is cheaper than discovering it from a delivered
   clip.

**Two technical defects in the same clip, independent of the verdict**, both
of them about the orbit and both recorded in the shared file rather than
here, because they are about camera craft in general and not about ads:

- The SHOWCASE framing **never escaped the HOOK's macro closeness**, despite
  all three waypoints stating a shot size and the paragraph closing with `the
  bottle stays fully in frame at every moment of the move`. Six frames across
  the move are all a close shot of the upper body; the base is never in frame
  and the brand word is clipped at the right edge in the last two.
- The orbit **barely happened**: three waypoints at 0°, 45° and 90°, and the
  bottle's orientation, cap perspective and highlight position are close to
  identical across all six sampled frames.

⚠️ Together those **downgrade a conclusion this repo had marked verified** —
that a shot size on every waypoint prevents a segment from inheriting the
previous one's framing. It held on an eyeglasses clip and failed here, on the
same "macro beat, then waypoint orbit" structure. It is now **once held, once
failed**, with the differences between the two runs (i2v against t2v most of
all) unexamined. Both the record and what to do about it are in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md)
under "A camera move needs its waypoint frames, not just a verb" — read it
before writing any orbit, and read a draft's frames rather than trusting the
prompt to have widened the shot.

**One usable rule does come out of it, from the same clip.** Its `11-13s`
`medium-close shot` and its `13-15s` `medium shot dead front, the whole
bottle centred` were both written across hard cuts, and **both were
delivered** — the final one holding the whole bottle cap to base with margin,
which is precisely what the SHOWCASE waypoints asked for and never got. So
in an ad: **when a beat needs the framing to open up, put the wider shot
after a cut rather than inside a camera move.** That is also cheap here,
because Template A's boundaries are hard cuts by default.

### If the user has an actual product photo

Prefer image-to-video over describing the product purely in text. The
evidence is the gallery's split rather than a measured comparison: every
collected prompt that had to match a real product, logo or package attached
an image (cases 12, 13, 24, 29), while the text-only ones avoid readable
text instead (`all labels illegible`, case 40). Fine label detail and logos
are what text descriptions lose. Prefer a local file over a remote URL when
the user has one: `ofox-video-core` auto-base64-encodes a local file, which real
testing found more reliable than depending on the upstream provider being
able to fetch an arbitrary third-party URL (some hosts' bot/hotlink
protection can reject an otherwise valid, publicly reachable image URL).

An attached image means one of two things, and the API has a field for each
(shared file, `Reference assets as visual anchors`):

| Meaning | Flag | What it does | Status in this repo |
|---|---|---|---|
| **First frame** — the clip starts on this exact picture | `--frame-first-image PATH` | locks the opening composition (case 15's `Begin with the exact composition of the reference image`); on `bytedance/seedance-2.5` forces `aspect_ratio: adaptive`, so crop or pad the photo to the target ratio first | verified with real runs; this skill's default route |
| **Identity reference** — the model borrows the product's appearance, no frame is locked | `input_references` through `--extra-json` | use one asset for exact packaging and another for the logo, for example | Follow the shared [`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy). It owns the payload shape, canonical `@imageN` labels, array-order rule, dry-run guard, measured two-image boundary and nine-image ceiling. For this ad route, pass `--aspect-ratio` explicitly. |

**The two are mutually exclusive** in one job: the script rejects a request
that carries both (`references_conflict`). Choose the first-frame route when
the opening composition matters; choose identity references when several
product images (front, back, box, logo) should inform the whole clip.

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "Begin with the exact composition of the reference image. Camera slowly orbits 30 degrees around the product, soft rim light, cinematic color grade, no dialogue" \
  --frame-first-image "/path/to/local/product-photo.jpg" \
  --duration 10 --resolution 1080p
```

That is a real run, which is why it carries `--approved` — see "Before you
spend". To see what it would cost without sending it, run the same line with
`--dry-run` in place of `--approved`.

**Do not pass `--aspect-ratio` on this route.** With an image attached,
`ofox-video-core` forces `aspect_ratio` to `adaptive` on
`bytedance/seedance-2.5` and prints a notice, so on the default model the flag
takes effect only on the pure text-to-video path. On another model the user
named, leaving the flag off is what makes the script apply `adaptive` — pass a
ratio there and it is honoured, which fights the photo instead of following
it. Either way, omitting it is the route. That is why the brief's Aspect question, when a
photo exists, means "crop the photo to this ratio first" — cropping only,
never padding, so nothing is invented at the edges. Confirmed again on
`60fbea52`: a requested `16:9` was ignored, and the clip still came out
1280x720 — because the frame had been cropped to 16:9 before it was attached,
not because the flag did anything. On this route the crop is the only control
over the clip's shape.

**If the frame is generated rather than supplied, do not crop it by hand.**
`60fbea52`'s was, and it took two manual steps (`1792x1024` → `1792x1008` →
`1280x720`) because `ofox-image-core` had no flag for it at the time. It does
now: pass `--target-aspect 16:9` (or `--target-size 1280x720`) to
`ofox-image.sh generate` and the ratio is measured off the written file and
cropped exactly, or the run fails loudly. That matters here more than in most
places, because `adaptive` means a wrong-ratio image is charged at the price
of the clip it opened.

**That flag has now been used on a real ad frame and it does the whole job.**
On `cb6b7870` a single `--target-aspect 16:9` produced two files: the API's
own bytes at `1792x1024` on the `-uncropped` path, and an exactly-16:9
`1792x1008` on the plain path, which is the one that went to
`--frame-first-image`. **No second downscale was needed** — `adaptive` takes
the *ratio*, not the pixel count, so the clip came back 1280x720 from a
1792x1008 frame. `60fbea52`'s third manual step (`1792x1008` → `1280x720`)
was never necessary; it was a hand-crop artefact. One run, but it removes
both manual steps.

If the reference image includes an actual person (e.g. a spokesperson or
model in the shot, not just the product), Seedance 2.5 image-to-video
refuses it at submission (`input_moderation_failed`, nothing billed).
`--real-person true` **does lift that refusal on 2.5** (measured 2026-09-16).
It is Ofox's privacy-preserving preprocessing path for real-person references
the caller is **authorised** to use — an authorisation route, never a way
past the check: offer it only when the user holds the right to that person's
likeness and has said so, never as a retry after a refusal, and never set it
on their behalf. For this skill it is also rarely the answer, because the
route below gets a model *and* a locked product without it. Evidence and
every limit on it:
[`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
→ "`--real-person true` lifts that refusal on 2.5". The
`--real-person` path validates the image server-side and can fail with
`bad_data_uri`/`download_failed`/`unreachable`/`not_image`/`too_large` if
the image isn't a small, valid file the API can use — see the failure table
below.

### A model *and* a locked product: the route that works

**"The reference frame cannot contain a real person" is not "the video
cannot contain a real person."** The refusal is a check on the picture you
attach, at submission. What the model generates from your text is a separate
question, and photoreal people generated from text pass routinely — five
20–30 second text-to-video jobs built entirely around them completed in this
repo (`844c9145`, `4e5c9581`, `41f87ac7`, `036ac3a8`, `38ca8311`).

So a request for "our exact product, worn/held/used by a model" is not
blocked. It splits:

| Half | How |
|---|---|
| The product must be exactly right | attach it as `--frame-first-image` — **with no person and no part of one anywhere in that image**, hands, feet and socks included, so it clears input moderation |
| A person must appear | write them into the timeline as text, entering after the product has been established |

Measured end to end on job `ac927785-92ef-4e28-97b9-ff8172ec5554` (20s, 720p,
7 shots, 6 hard cuts): the first frame held a shoe alone, a runner entered at
4s and stayed in frame for seven or eight seconds, and a three-way comparison
of the input image, the delivered first frame and t=19.6s shows the product's
colour blocking identical in all three — **the frame lock neither expired
over 20 seconds nor drifted while a person was on screen.** Pair this with
the framing-order rule in Template A's slot notes, which is what kept that
model free of deformation.

What this route does **not** give you: consistency of the *person* across
jobs. They are generated fresh each time, so a second clip is a different
model wearing the same shoe. Only the product is locked.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | `bytedance/seedance-2.5` (script default, no flag needed) — **unless the user named a different model**, which always wins | current-generation model; see "Choosing a video model" for the other two options |
| `--duration` | `10` when the user gives no length; otherwise the user's number | 10s is a cheap, readable draft length. **Every gallery ad prompt with a stated length runs 20–30s** (cases 13, 15, 25, 26, 27; case 12 rendered at 26s), and Template A needs 15s or more for its four beats. When the user gave no duration, say in the brief recap that the collected ads run longer and offer 15–20s as a row; Seedance 2.5 accepts 4–30 |
| `--resolution` | `1080p` for a deliverable brand asset; `720p` as a cheaper draft/preview pass — `720p` is a `seedance-2.5`/`wan-3.0-prime` value, and on `minimax/hailuo-3` the draft tier is `768p` (it has no `720p`) | brand assets are usually published, so higher fidelity is worth the extra cost — show both as rows in the cost table rather than asking (see the approval gate below) |
| `--aspect-ratio` | `16:9` (landscape) unless the brief set another — **pure text-to-video only** | cinematic/hero framing for websites and YouTube; `9:16` for a vertical social cut, `1:1` for feed placements. **Once an image is attached this flag stops being yours on the default model** — `ofox-video-core` forces `adaptive` on `seedance-2.5` (see above). On another model it is honoured if you pass it, and `adaptive` is only the default when you don't |
| `--generate-audio` | `true` (server default, no flag needed) | ambient/SFX track — no music, per the AUDIO line; the prompt says "no dialogue" and carries an AUDIO line |

## Choosing a video model

`model` stays **never-ask** — the agent doesn't raise it as a question on its
own. But never-ask is not "never listen": `bytedance/seedance-2.5` is the
default only because nobody asked for something else. If the user names a
model — an id (`alibaba/wan-3.0-prime`, `minimax/hailuo-3`), or a shorthand
like "wan" or "hailuo" — use that model, not the default. Never silently
substitute `seedance-2.5` for a model the user actually asked for.

| Model | Cheapest tier (catalog) | Max resolution | Duration | Aspect ratios | Real moderation data point |
|---|---|---|---|---|---|
| `bytedance/seedance-2.5` (default) | 480p, 11 cents/s | 1080p | 4–30s | 7, incl. 21:9 | **Rejected** a photoreal-portrait i2v reference (`input_moderation_failed`) and a Re:Zero/Rem-styled anime t2v prompt after it had already generated (`output_moderation_failed`, copyright) — both free, nothing billed. See `.trellis/spec/skills/external-api-integration.md`, "Gotcha: moderation policy is per-model, not a platform-wide constant". |
| `alibaba/wan-3.0-prime` ("wan") | 480p, 6.4 cents/s | 1080p | 2–30s — the shortest minimum of the three | 6 — no 21:9/9:21 | **Accepted** both of the clips seedance-2.5 rejected above, 12.8 cents each (2s/480p, its minimum). Only these two content classes have been tested — not a general "no moderation" guarantee for this model. |
| `minimax/hailuo-3` ("hailuo") | 768p, 8 cents/s — no 480p tier | 2k, uniquely among the three, at 13 cents/s | 4–15s — the shortest **maximum** of the three, so it's out for anything past 15s | 7, incl. 21:9 | **Accepted** the same two clips, 32 cents each (4s/768p, its minimum). Same caveat: two content classes tested, not a blanket clearance. |

Price, max resolution, duration and aspect-ratio counts are catalog facts —
`GET https://api.ofox.ai/v1/models/catalog`, no API key needed, publicly
re-checkable any time — not results from a real generation. The moderation
column is the one column here that came from a real, paid API call; treat
it as evidence about exactly those two tested content classes on that date,
not as a blanket policy for either model. A product ad with a person on
screen is exactly the kind of shot that hits moderation (see "A model *and*
a locked product" above), so this is worth checking before defaulting to
`seedance-2.5` on a request that names a real person or a licensed
character. `wan-3.0-prime` runs on two upstreams (`alicloud`,
`aliyun`) and `hailuo-3` on two (`minimax`, `novita`), neither of which
`ofox-video-core` currently pins the
way Seedance's `byteplus`/`volcengine` pin works below.

### What changes when the model changes

The defaults table above was written for `seedance-2.5`. Two entries do not
carry over unchanged:

- **`--resolution 720p` does not exist on `minimax/hailuo-3`.** That model
  offers `768p` and `2k` only, so the draft row of the cost table is `768p`
  there, and the deliverable row is `2k` rather than `1080p`. Sending `720p`
  is rejected by the script locally, before submission, for free — but quote
  the right tier in the first place, or the cost table is wrong.
- **The attached product photo's shape is handled per model.** With
  `--frame-first-image`, `seedance-2.5` is *forced* to `aspect_ratio:
  adaptive`; `wan-3.0-prime` and `hailuo-3` *default* to it only when you pass
  no `--aspect-ratio`, and keep your value when you do. Either way the script
  prints a `NOTE:` naming which it did — relay it. The advice to crop or pad
  the photo to the brief's ratio before generating is unchanged and still the
  thing that actually decides the output's shape.

Both need `ofox-video-core` 1.22.0 or newer. Before that, a non-seedance model
with a photo attached sent **no `aspect_ratio` at all**, and the photo's shape
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

**Cuts inside one job are written as timestamps.** Verified on Ofox on
2026-09-03: two three-shot prompts on `bytedance/seedance-2.5`, both pinned
to `byteplus`, 8s, 480p, 16:9, `--generate-audio false`, **pure
text-to-video with no image attached**. Both rendered all three shots with
hard cuts landing within about one second of the written timestamps — one in
the bare `0-3s: … Hard cut. 3-6s: …` form, one with a header manifest and
`SHOT N (a-bs)` + `HARD CUT`.

**This scenario has since pushed that envelope out itself, on the axes ads
actually use.** Four 720p jobs — three accepted, one rejected — all
`bytedance/seedance-2.5` on `byteplus`, all with a generated product image
attached as `--frame-first-image`:

| Job | Shape | Result |
|---|---|---|
| `7ae7d49e-7eb9-4165-9d95-09cd525d53ed` | 15s, 5 shots, 4 hard cuts, hook/showcase/climax/close | all 4 cuts happened and the first frame held across them; the wordmark on the label stayed legible and in the frame's own typeface |
| `ac927785-92ef-4e28-97b9-ff8172ec5554` | 20s, 7 shots, 6 hard cuts, a model entering mid-clip | all 6 present; 5 detected within about 0.3s of their stamps, the 6th visible frame by frame |
| `60fbea52-b14b-4796-80bf-03afe0aa4fa0` | 15s, 5 shots, 4 hard cuts, hook / two showcases / climax / close, a hand entering the climax | all 4 cuts happened, detected at 2.62 / 4.75 / 6.62 / 12.25s; the per-shot split came in within 0.4s of plan; the first frame held from 0.3s to 14.9s — bottle, frosted finish, black collar and bulb, label, glass of water, eucalyptus sprig, desk grain and bare wall all unchanged |
| `cb6b7870-22f7-4a15-9168-8a013805775f` ⚠️ **rejected** | 15s, 5 shots, 4 hard cuts, hook / showcase / climax / payoff / close | all 4 cuts happened, at 3.000 / 7.542 / 11.042 / 13.250s against stamps of 3 / 8 / 11 / 13; the first frame's product held throughout and the etched brand word survived unaltered in every shot it appeared in. **Rejected on content density, not on structure** — see 7 in "Writing a good ad-creative prompt". ⚠️ Its cut scores descend through the clip — 0.395 / 0.311 / 0.216 / 0.132 — so the 0.25 default finds only two of the four and **0.10** is the first threshold that finds all of them |

All four of those wrote **every** boundary as a hard cut — 4 of 4, 6 of 6,
4 of 4 and 4 of 4 — and all four kept every cut. Repo-wide that makes seven
runs whose written hard cuts all rendered (at shares of 3 of 8, 3 of 6, 5 of
7, 4 of 4, 6 of 6, 4 of 4 and now 4 of 4) against one that lost all three of
its at a share of 3 of 9. The single list of those runs, and the reason the
threshold is still unknown, is in the shared file's `Several shots in one
job`; the rows above are entries in that record, not the start of a second
one.

**Do not read "every cut landed" as "the clip worked."** The fourth row is
the whole argument for keeping those two questions apart: it hit its cuts more
precisely than any of the three accepted rows and was rejected anyway, for
having nothing happening between them.

For the reproducibility record the third one exists to be: seed `799906248`,
billed 3.60 USD for the video (15s x 24 cents/s at 720p — image-to-video
billed at the t2v rate again, not the dearer v2v rate) plus 0.154035 USD for
the first frame on `openai/gpt-image-2` at `--quality high --size 1792x1024`,
5063 output tokens. Delivered 1280x720 h264 at 24fps with a 32kHz stereo aac
track, 15.04s; `generate_audio true`; `aspect_ratio` forced to `adaptive`.
It is in the gallery as `aura-serum-ad`. Versions in force when it ran: this
skill 1.9.0, `ofox-video-core` 1.14.0, `ofox-image-core` 1.4.0 — both
dependencies have moved on since.

The fourth one, kept as a rejected case rather than a gallery entry: seed
`226221006`, billed 3.60 USD for the video (15s x 24 cents/s at 720p, t2v
rate again — the third confirmation of that tier on this route) plus
0.153995 USD for the first frame, same model and same `--quality high`
pair. Delivered 1280x720 h264 at 24fps with a 32kHz stereo aac track,
15.072s, 13.6MB, `nb_streams=2`; `aspect_ratio` forced to `adaptive`; 538
seconds of wall clock. Total 3.753995 USD. Versions in force: this skill
1.10.1, `ofox-video-core` 1.19.1, `ofox-image-core` 1.9.1. Why it is worth a
record despite being rejected: it is the run that verified the `PAYOFF` fix
and that produced 7's motion measurements, and it is the only clip in this
scenario whose per-segment motion has been measured at all.

So four or five beats is inside the measured envelope, and so is **an
attached reference image combined with multiple cuts**, which the two 2026-09-03
runs did not cover. **Still not covered**: more than 7 shots or 6 cuts in one
job, 1080p, the `volcengine` upstream. The full record, including the reason
a written `HARD CUT` can still soften, is in the shared file's `Several shots
in one job`. The gallery's densest ads (case 14: nine `CUT`s; case 26: seven
segments) ran on unrecorded platforms — treat a count above 7 shots as
gallery practice and price a first attempt as an experiment.

**`chain` carries the last frame of one job into the first frame of the
next**, then joins the clips into one file. Use it when the sequence exceeds
one job's 30s ceiling, or when each shot needs its own approval, seed or
resolution; each shot is a separately billed job and the run estimates the
total before spending. `chain` adds one constraint: no photoreal person in
the carried frame on `bytedance/seedance-2.5` (`input_moderation_failed`), so
a sequence built around a human model cannot be chained, while product and
environment shots can. That constraint is measured with the flag unset;
`--real-person true` is an authorisation claim about a real person the user
may use, which a model-generated face in a carried frame is not, and no chain
has been run with it either way — so do not offer it as the way to chain a
human. A chain of jobs can each carry timestamped cuts.

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

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
The rule above is still the rule, and it is still yours to follow.

The brief recap (see the creative brief section) goes in the **same
message** as the prompt and the table, above them — the user approves the
choices, the prompt and the price together.

What this scenario's table usually needs a row for: the clip itself, priced
at the duration, resolution and aspect ratio you settled on. When the choice
between a 720p draft and a 1080p deliverable is still open, dry-run **both**
and show two rows — the difference is a decision, and it reads as one only
when both numbers are on screen.

**When the first frame is generated rather than supplied by the user, that is
a second row, and it is not a rounding error.** Measured on `60fbea52`'s
frame: 0.154035 USD — 15.4 cents — on `openai/gpt-image-2` at `--quality
high --size 1792x1024`, 5063 output tokens, against 3.60 USD for the 15s
720p clip it opened. **Measured a second time on `cb6b7870`'s frame:
0.153995 USD**, same model and same quality/size pair — the two agree to
within four hundredths of a cent, so at that pair the figure is stable and
15.4 cents is the number to plan with. Quote it from `ofox-image-core`'s own `--dry-run`, with
**the same `--target-aspect` the real call will use** — that flag decides
which `--size` gets requested, and the size is half of what an image estimate
is priced at. When that run was made, the estimate was anchored to a small
`low`-quality pair and quoted ~0.6 cents for a frame that billed 15.4;
`ofox-image-core` 1.7.0 made the lookup pair-aware, so the line now prices
the pair being sent, or labels itself `ROUGH UPPER BOUND` when nobody has
measured that pair. Relay the line as printed, label included — do not
substitute a figure of your own in either direction.

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

Expect the shared reference files to be out of reach for the same reason:
`prompt-structure.md`, `creative-brief.md`, `approval-gate.md` and
`api-params.md` are shipped by `ofox-video-core`, while this skill packages
only its `SKILL.md` and `CHANGELOG.md`. If the probe found a core and a link
still doesn't resolve, the link is pointing at the wrong directory name and
wants the same substitution; if it found nothing, the docs return with the
script. Nothing here becomes unusable in the meantime; the prompt templates,
the brief's question table and the defaults are all local. The part you lose
is the detail those links carry — the full transition and camera vocabulary,
the general question-flow rules, and the gate's precise wording, which is
still required before spending.

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

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the ad-creative prompt built above>" \
  --name "<short spot name, e.g. perfume bottle hero ad>" \
  --duration 10 \
  --resolution 1080p \
  --aspect-ratio 16:9
```

`--approved` is not decoration: without it the script refuses, submits
nothing, and prints the quote-first steps instead. Add it only once the cost
table has actually gone in front of the user and come back with a yes — the
flag cannot check that for you.

This one call validates the parameters, submits the job, polls to
completion, downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, and `VIDEO_COST`. Report the **actual** values from that
output to the user — never the estimate, and never a path/cost you didn't
see the script print. Do not re-implement any of the request/poll/download
logic here; always call into `ofox-video.sh`.

## Common failure modes and fixes

These are `ofox-video-core`'s documented exit codes and error codes
(full table: [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus the ad-creative-specific ones:

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, no network call made | Bad `--duration`/`--resolution`/`--aspect-ratio`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| Exit `3`, `error.code: insufficient_credits` | Ofox balance too low, especially likely at 1080p | No charge was made; suggest a cheaper 720p draft or adding credits at `https://app.ofox.ai` |
| Exit `3`, `error.code: input_moderation_failed` on an image-to-video job | The reference frame contains a photoreal person — refused at submission on Seedance 2.5, nothing billed | Describe the person in text and lock only the product to the image; or crop the person out of the reference |
| Exit `3`, job ends `failed`, or `invalid_request` on create, with no other error code hint | Likely a moderation rejection: prompts referencing a real celebrity/spokesperson likeness without consent, another brand's trademarked logo, or copyrighted characters are commonly rejected | Remove the flagged real-person/trademark/copyrighted reference from the prompt (or reference image), then call `generate` again — this is a **new** request, not a resubmission of the failed one, so it's safe to retry immediately |
| Exit `3`, job ends `failed`, `error.code: output_moderation_failed` | The generated **output** failed a post-generation content check — happens after the job ran, not at submission. Not billed (no `usage` field on the response) | Retry with a brand-new `generate` call using a different prompt or reference image — a new request, not a resubmission of the failed one, so it's safe |
| Exit `3`, job ends `failed`, `error.code: output_moderation_failed`, upstream message mentions **audio** copyright | The AUDIO block asked the model to generate music — measured on job `1ff72400-0f30-4be1-a417-f52d43955d09` with a cello note and a bell chime. Not billed | Rewrite AUDIO as room tone plus recorded sounds only, add the music words to AVOID, and re-run — a new request, safe immediately. See "4. No dialogue, no music — but a sound block" |
| A real person is needed in the ad and the attached frame is refused | The frame itself contains the person. The refusal is about the attached picture, not the clip's content | Attach a frame of the **product alone** and write the person into the timeline as text — see "A model *and* a locked product: the route that works" |
| The climax's build-up looks beautiful and the event itself never happens | The payoff was written as the tail of a longer shot. Measured once, on `60fbea52`: a drop hung from the pipette for the whole five-second climax and never landed, and the clip cut to the hero frame instead | Give the payoff its own timestamped shot with its own seconds, compress the build-up, and name the result as a required visible event — **verified on `cb6b7870`**, where steam written that way rose and drifted as asked. See the `PAYOFF` line in Template A and its slot note. This is a new prompt, so a new cost table |
| The clip is competent, every cut landed, and the user calls it monotonous or "nothing happens" | Beats that contain no physical event. Measured on `cb6b7870`, rejected: two of its five segments contain no physical event at all and a third only moving light, so only about 5.5 seconds of a 15-second spot had a visible event in it. Read this off sampled frames — a per-segment scene score gets the ranking wrong here, see 7. A Luxury brief plus a low-motion product is the setup for this | Do not just add cuts. Give every segment one nameable physical event, and for a product that cannot move on its own bring the motion in from outside — pour, steam, ice, a hand, moving air. See "7. Every beat needs a physical event — and 'slow' is not 'still'". A new prompt, so a new cost table |
| A Luxury spot comes back static rather than slow | `slow movement` in the Luxury archetype read as "little movement". On `cb6b7870` it became three separate sentences pinning the camera and the product — `the camera holds still`, `the bottle itself never moves or rotates`, `the camera is completely still and the bottle does not move` | Write the speed, not the absence: a slow orbit, a slow push-in, a slow pour. Keep "still" for a hero frame you have earned, and check that a negative clause about the *product* has not left the *camera* with nothing to do — that pairing is what produced the stillest segment in that clip. See 7 |
| The orbit segment stays at the previous beat's macro closeness even though every waypoint states a shot size | The framing was inherited and the written shot size did not release it. This is `cb6b7870`'s SHOWCASE: three waypoints all asking for the whole bottle cap to base, six frames all showing the upper body only | Keep writing the shot size — omitting it is measured to be worse — but treat it as necessary, not sufficient: it held on `8efeb556` and failed here. Read the frames of a cheap draft before paying for the final, and consider putting the wide shot after a hard cut rather than inside the move. The record is in `A camera move needs its waypoint frames, not just a verb` in the shared file |
| One shot comes back louder than the shot written to be quieter than it | A loudness written per shot is not honoured. Measured on `60fbea52`, whose "very quiet" shot 2 was the loudest sustained passage in the clip; the sound *effects* did land where they were written | Nothing to fix in the prompt — name each shot's sounds and set the relative levels in an editor. See "4. No dialogue, no music — but a sound block" |
| Invented signage or garbled lettering in the background | The negative list was relied on to remove it; on Ofox it is only partly obeyed | Change the set, not the wording: a background with no surface lettering can sit on returns zero text. See "5. Text on screen: lock it, or design it out" |
| Exit `1`, `references_conflict` | `--frame-first-image` and an `input_references` array in `--extra-json` in the same job | Pick one meaning — first frame, or identity references — and drop the other |
| `bad_data_uri` / `download_failed` / `unreachable` / `not_image` / `too_large` | `api-params.md` documents these as `real_person: true` image-validation failures, raised when Ofox fetches the reference image: it isn't a small, valid image the API can use (a remote URL that isn't publicly reachable, or a local file that failed to read/encode) | Prefer a local file (auto-base64'd, more reliable than some remote URLs — see above); confirm it's a real image file under the size limit and retry |
| Product label text or logo looks distorted/illegible in the result | Pure text-to-video can't render fine label detail reliably | Switch to image-to-video with `--frame-first-image` pointing at the real product photo instead of describing the label in text |
| The clip did not cut where the timestamps said, or cut fewer times than written | Above 7 shots / 6 hard cuts in one job is past what has been measured here. Below that, the usual cause is the transition mix: a timeline weighted toward named continuous transitions can soften a written `HARD CUT` too | Keep hard cuts the majority of the boundaries, stay within 7 shots, and read the frames of a 480p draft rather than a detector's count — see `Past that envelope` and `Checking the cuts` in the shared file |
| Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; tell the user to check `https://app.ofox.ai` for a job that may already be running, per `ofox-video-core`'s no-resubmit rule |

## When NOT to use

- Dialogue-driven scenes with characters talking — use `seedance-short-drama`
  instead.
- A clip that should look filmed by a real customer on a phone — use
  [`ugc-ads`](../ugc-ads/SKILL.md). Everything this skill defaults to
  (grading, a studio key, a slow-motion climax, a hero freeze) is a defect
  there, and that skill inverts them explicitly.
- Several cheap vertical drafts to choose from rather than one finished spot —
  use [`shorts-reels`](../shorts-reels/SKILL.md), which owns the
  draft-then-promote ladder. Write the ad prompt here and run the set there.
- Plain catalog/listing footage (white background, literal orbit or
  turntable rotation, no mood or camera language) rather than a cinematic
  brand ad — use `seedance-product-video` instead. The border case is a
  clean studio showcase with a lid-opening reveal (gallery case 17): it
  belongs here only if there is a brand narrative or an emotional tone to
  carry; a listing that just needs to show the item belongs there.
