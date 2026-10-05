---
name: pixar-ad
metadata: {packVersion: 1.3.0}
description: >-
  Builds a stylized 3D animated ad on the Novoads REST API as a STORYBOARD:
  four to six beats, each rendered from its own key frame, narration laid into
  the gaps, a music bed, captions burned on, assembled locally with ffmpeg.
  Carries the genre's beat formulas (anthropomorphized problem character,
  protagonist reveal, mascot mechanism scene, composited end card).
  Use for ANY Pixar-style, Disney-style, 3D animated or
  animated-film-look ad at ANY length: "Pixar style ad", "3D animated ad",
  "animated movie look", "cute 3D character ad", "a quick animated ad", "15
  second animated ad", "30 second animated ad", "storyboard ad", "several
  scenes", "animated ad with a voice-over", "little mascots", or a product URL
  or photo for an emotional animated spot. No one-call tier, so ffmpeg is
  required. Not for stop-motion clay (use claymation-ad), talking-head
  UGC (novoads-api), video cloning, or static image ads.
---
<!-- AUTO-GENERATED FILE. Do not edit it: the next build overwrites you.
     Source of truth is sections/, registered in sections/manifest.json.
     Edit the section, then run: python3 scripts/build-skill-md.py -->

# Novoads Pixar Ad

One product in. A 30 to 60 second stylized 3D animated ad out, cut from four to
six separately rendered beats, with narration, music and captions.

**Every animated ask lands here, including the short ones.** There is no
one-call 15-second tier in this repo. A request for "a quick animated ad" is a
request for a four-beat board rendered beat by beat and assembled locally:
longer to make, more calls, more credits, and it needs ffmpeg. Say that in one
clause before you start, then start. If the story genuinely fits in a single
shot, make it a four-beat board with short beats rather than pretending there is
a cheaper door.

**The beat formulas live in [`references/formulas.md`](references/formulas.md).**
That file is the craft: the four genre roles, the variable tables, and a worked
still prompt and a worked clip prompt for each. This file is the pipeline. Read
the formulas before you write the board, because the board is where the roles
are assigned and it is the last cheap place to get them wrong.

**Every HTTP mechanic here belongs to the pack, not to this skill.** Auth,
strict bodies, status codes, the poll loop, rate limits and error envelopes are
written out once in [`skills/novoads-api/SKILL.md`](../novoads-api/SKILL.md) and
its [`reference.md`](../novoads-api/reference.md). Read those for mechanics; this
file names the endpoint and the fields that matter to a beat.

## Before anything: this runs on a Novoads account

1. A Novoads account with credits. https://novoads.ai. There is no free tier and no trial:
   every plan is a paid monthly subscription, published at novoads.ai/pricing. Never call it free.
2. **An API key in `.env` at the repo root**, as `NOVOADS_API_KEY=novo_…`. Check
   it with `./scripts/check-novoads-env.sh`; if it is missing, run
   `./scripts/setup.sh`. That is the whole setup: `curl` and `jq`, one key, no
   connector to add and no session to restart.
3. **ffmpeg on your machine.** This is the one hard local dependency: the
   assembly happens here, not on the server. `ffmpeg -version` before you start.

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

A `401` is a bad or revoked key. A `403` carrying `error.details.reason` of
`plan_required` or `subscription_inactive` is a good key on an account with no
live subscription. Say which one it is rather than "auth failed".

## What one run costs

**There is no rate table here, on purpose.** Every credit number this run shows a
user comes from `POST /v1/estimates`, in this session, before anything is
charged: a price written into a skill file goes on being quoted long after it has
moved.

What Gate 2 prices, for a five-beat board: **1 cast sheet image · 1 still per
beat · 1 clip per beat · 1 voice-over line per VO beat · 1 music bed · 1
transcript of the master · 1 caption pass.** Four calls cover all of it, because
the arms repeat — price each KIND once (`image`, `video`, `voiceover`, `music`),
multiply by those counts, and quote what came back. The one shape worth holding
is an ordering rather than a number: **the clips are most of the bill, and a
still is a small fraction of the clip it seeds.** That is the whole economic
argument for the still gate, and for never re-rendering a beat you have not first
tried to fix in its still.

## Hard constraints

- **Four to six beats.** Fewer than four and there is no arc to assemble; more
  than six and the seams outnumber the story. A 15-second ask is four short
  beats, not one long call.
- **Each beat is its own `POST /v1/videos` call from its own start frame.** Never
  ask one call for multiple scenes.
- **4 to 15 seconds per beat**, and in practice 4 to 6. A beat is one action.
- **9:16** unless the operator says otherwise.
- **`audioEnabled: true` on every beat.** The clip's own audio is the SFX bed
  and the in-scene voices; there is no SFX endpoint and none is needed.
- **A narrator line goes in the PROMPT or in the VO track. Never both.** Getting
  this wrong is silent: Seedance renders any `NARRATOR: "…"` line in the prompt
  into the clip's own audio, so laying a `POST /v1/voiceovers` take of the same
  words on top plays every line twice. Measured — a raw beat clip transcribed on
  its own came back saying the narrator's line, and the finished mix said it
  twice. Decide per beat:
  - **Narration from the VO track** (the default here, because it is the only way
    to get ONE voice across five separate renders): the prompt carries in-scene
    dialogue only, or states that the shot has no speech. Keep `audioEnabled:
    true` for ambience.
  - **Narration native to the clip**: put `NARRATOR: "…"` in the prompt and
    generate NO voice-over for that beat. Its voice will not match the others.
- **At least one beat must be SYNC.** The rule above is a warning against
  doubling a line, and it is easy to over-obey: make every beat a VO beat and the
  ad becomes a slideshow with a voice talking over it. Measured — T12 shipped
  three beats, all VO, no character ever spoke, and it lost to the reference ad
  on exactly that. The genre's opening move is a problem character saying its own
  complaint out loud, and it only lands when the voice comes out of the face.
- **The product appears in its own beats and on the end card. Nowhere else.** A
  product held in every shot reads as a catalogue. Roles B and D show it; the
  hook and the mechanism scene do not. See `references/formulas.md`.
- **One continuous voice.** Pick the narrator voice ONCE, from `GET /v1/voices`,
  and use that same `voiceId` for every line. A voice that changes between beats
  reads as a different ad — which is also why native per-beat narration does not
  work across a storyboard: each render casts its own.
- **There is no `styleFamily` field.** It was deleted from the whole API, and the
  `/v1` request bodies are strict, so sending it is a `400 Unrecognized key`.
  Nothing on the generation path refuses a prompt on style grounds any more; the
  only prompt refusal left is content moderation.

## The gates run in order. Do not skip to the render.

### Gate 0 — is this product right for this style?

Stylized 3D animation is good at exactly one thing, and it is not explaining
features.

**What it can do:** interiority (large expressive eyes playing a private state —
shame, worry, relief); anthropomorphised objects that hold intent without a
face; warm aspirational realism that reads premium rather than novelty;
caricatured physics (squash, stretch, anticipation).

**What it is bad at:** technical explanation, spec comparison, cutaway logic, and
any pitch whose core is a number.

**The filter. All four must pass:**

- Is the pain **emotional or relational** rather than technical? A styled
  character can act "I can't read to my grandson." It cannot act "the field of
  view is 110 degrees."
- Is the pain **visible on a face** (or on a mechanism, under Doctrine D)?
- Is there a **relationship**? Two characters beat one. The strongest ads here
  are about someone else, not about the buyer alone.
- Is it **impulse-priced**? Warm animation converts at 15 dollars. At 900 it
  creates trust dissonance.

If the product fails, say so plainly and name what would suit it instead. Do not
build a charming ad for a product that needs a demo.

One addition at this length: **an arc needs a turn.** If the product read
produces one feeling and one feature, say so — the honest answer is four short
beats and a tight script, not a padded 60 seconds.

### Gate 1 — product read, then summarise in under 200 words

**A product photo alone is not a sufficient input.** Price, specs, rating,
rating count and buyer language are what this gate asks for, and a photograph
carries none of them. If you have only an image, **ask once** for a URL or the
listing text and say why in one clause. That is the single question this skill
opens with, and it costs nothing. If the operator says there is no listing,
proceed on the photo and state plainly that price and reviews were unavailable
rather than implying they were checked.

Source from the product URL or listing text, with the photo as corroboration.
Then state:

1. **Verified facts:** name, price, key specs, rating and rating count. Quote
   only what the source says.
2. **Buyer language:** recurring phrases from real reviews, in the buyer's words.
3. **Who actually buys.** Reviews often reveal the purchaser is not the user — an
   adult child buying for a parent, a spouse for a partner. If so, put the
   product into the purchaser's hand on screen. This is usually worth more than
   any feature beat.
4. **What you will NOT claim, and why.** Check negative reviews and the fine
   print. If reviews contradict durability, the ad does not say "built to last."
5. **Anything unbuyable.** No buy box, out of stock, region-locked, or a newer
   model at the same price. A perfect ad pointed at a dead listing converts at
   zero.

### Gate 2 — price the whole board, then announce it

Price each KIND once and multiply. `POST /v1/estimates` is discriminated on
`kind` and takes one at a time, so four calls describe the whole run:

```bash
E=https://api.novoads.ai/v1/estimates
H="Authorization: Bearer $NOVOADS_API_KEY"
J='Content-Type: application/json'

curl -sS -X POST $E -H "$H" -H "$J" \
  -d '{"kind":"image","model":"gpt-image-2","prompt":"<a beat still prompt>"}'
curl -sS -X POST $E -H "$H" -H "$J" \
  -d '{"kind":"video","model":"seedance-2.0","durationSeconds":5,"prompt":"<a beat prompt>"}'
curl -sS -X POST $E -H "$H" -H "$J" \
  -d '{"kind":"voiceover","script":"<the longest VO line>"}'
curl -sS -X POST $E -H "$H" -H "$J" \
  -d '{"kind":"music"}'
```

**Each arm is strict and takes only what moves the price.** The `music` arm takes
`kind` and nothing else — sending it a `prompt` is a `400`. The video arm never
sees `aspectRatio`, `startImageAssetId`, `referenceAssetIds` or `audioEnabled`,
and rejects all four. Send the `model` you will actually render, or you are
pricing a different ad.

Then announce in one line and proceed:

> Cast sheet + 5 stills + 5 clips + 5 VO lines + music + captions ≈ <the total
> the estimates returned> credits (balance: <what they reported>). Starting.

This is an announcement, not a question. Two cases change it:

- **`sufficient: false` on any kind** — stop. Name what is short and give the
  `topUpUrl`. That is a blocker.
- **The balance covers the run and no retry.** Say so in one clause before
  firing: "this covers one pass, not a re-render." At this length a re-render is
  a beat, not the whole ad — which is worth saying too, because it is the good
  news: a bad beat is one still and one clip to redo, not the whole board.

**The `warnings` array is advice.** `POST /v1/estimates` is the only call that
lints a prompt — `POST /v1/videos` and `POST /v1/images` return no such field —
and it lints against the UGC talking-head rules; nothing here refuses anything. A
prompt written the way this file says comes back clean; a warning usually means
you drifted, not that the lint is confused.

Two clauses are what make it come back clean, and both are in the style lock and
the worked prompt for this reason. Measured on a beat prompt without them: the
VOICE STYLE casting line answers `missing_actor_descriptor` (the rule looks for
an age or gender token anywhere in the prompt), and the labelHold clause answers
`label_without_hold`, which fires on the word "bottle" alone. Drop either and the
same beat comes back with a warning that is telling you the truth.

**The one warning to ignore: `missing_actor_descriptor` on a beat with no human
in it.** The lint reads prompts as talking-head UGC, where a shot without an age
or gender token gets a randomly cast person. A role-A beat is a hair clump with
eyes, or a blob of congestion, and it has no age and no gender to state. The rule
is answering a question the beat does not ask. This is the only lint output this
skill tells you to overrule, and only on a beat whose subject is genuinely not a
person — a beat that merely FORGOT to describe its human is the case the rule
exists for, and it looks identical from here. Check which one you wrote.

## Product treatment — pick one and say why

**Doctrine C: in-world product, real hero card.** The default. The product is
recreated exactly in design but rendered in the animated look, so the character
can physically use it. The real photograph appears only in the final beat as a
hero card, outside the styled world. Recognition comes from design fidelity, not
from material.

Always include the lock line, and name specific identifying details — a rivet, a
hinge, a lens shape. Generic descriptions produce generic props.

> The product is exactly as shown in the reference: same shape, same colour, same
> proportions, same finish. Do not redesign or restyle it.

**Doctrine D: product as character.** Available only when the product's real
articulation is expressive — a pan-tilt head, a hinged lid, a swivelling arm. The
product performs using **only movements the real product makes**. No eyes, no
mouth, no eyebrows, no limbs, no hopping. Head angle and existing mechanisms
only.

That constraint is the whole point: every expressive beat doubles as a real
feature demo. State the negatives explicitly, because the model will happily bolt
on eyes and turn the product into a mascot.

**A real product, always.** Use the actual brand and the actual packaging from
the photo. Never invent a brand, and never blank-label the product to avoid the
question.

## The board

Before a single call, write the board. It is the artifact the operator approves,
and it is cheaper to argue with than any render.

### Cast sheet — one image, referenced by every still

`POST /v1/images` on `gpt-image-2`, `aspectRatio: "1:1"`, the product photo in
`referenceAssetIds`. On one canvas: the lead in three emotional states readable
in the eyes, any secondary character, the product in 2 to 3 views, and a scale
line-up at true relative size. The call usually answers with the board; one still going after about 105 seconds answers `status: "running"` with no images (API 2.39.0): poll `GET /v1/generations/{jobId}` to a terminal status and read `images[]` there, never resubmit, because a resubmit is a second charge.

This single image is what makes five separately-rendered beats look like one
film. Every beat still references it. Skipping it is the most expensive shortcut
available here — five beats with five differently-imagined characters is not an
ad, and no amount of prompt discipline recovers it afterwards.

Write the cast sheet TEXT first, from the template in
[`references/formulas.md`](references/formulas.md), and render the image from it.
The template has the slots that matter — including the **terse tag**, the 11 to
30 character wardrobe-anchored phrase repeated verbatim in every later beat. Our
renders re-cast on every cut, so "the same woman" names nobody; one measured run
came back with three visibly different women across five beats.

If the ad has a mascot scene, the cast sheet carries the mascots too: one canvas
with the lead, the problem character and the mascot trio settles all three
designs for the price of one image.

### Style lock — one paragraph, pasted verbatim into every prompt

Write it once. Location palette, one named practical light source, lens and
camera height, the finish of the world. Paste it into every still prompt and
every beat prompt, unchanged, character for character. Rewording it between
beats is how the grade drifts.

Never name a studio or a franchise. Write "stylized 3D animated feature film
look." The trademark risk is higher for this aesthetic than for any other,
because it belongs to specific studios and the models will hand you near-copies
of their characters if invited.

This is the genre default. Change the palette and the light source to the
product's world; keep the structure and the render vocabulary.

<!-- eval:style-lock:start -->
```
Stylized 3D animated feature film look. Soft volumetric golden-hour lighting from
a large window, warm cosy palette of cream, butter yellow, dusty pink and soft
sage. Subsurface scattering on skin, painterly background, shallow depth of field
with creamy bokeh. Characters have large expressive eyes with multiple specular
catchlights, stylized but believable proportions, smooth simplified hands, soft
hair strands with subsurface glow. Rich material detail: waffle-knit fabric
weave, ceramic glaze, glass refraction. Slightly desaturated colour grade.
Every character reads mid-emotion, caught a moment before a smile or a sigh,
never blank-staring. Vertical 9:16 composition.
```
<!-- eval:style-lock:end -->

**The mid-emotion line is the genre's oldest craft rule and the easiest to
lose.** A character rendered at rest reads as a mannequin however good the
lighting is; the whole look depends on faces caught between expressions. It sits
in the style lock rather than in prose because that is the block that actually
reaches every prompt.

And the negative block, pasted at the end of every prompt, still and clip alike:

<!-- eval:negative-block:start -->
```
no live-action footage, no photorealistic humans, no uncanny faces, no dead eyes,
no anime style, no 2D cel-shaded look, no flat illustration,
no named or copyrighted animated film characters, no harsh fluorescent lighting,
no extra fingers, no melted features, no morphing between frames,
no warped product labels, no on-screen text, no subtitles, no captions
```
<!-- eval:negative-block:end -->

`no named or copyrighted animated film characters` is the IP line and it is not
optional. `no on-screen text, no subtitles, no captions` is what stops the render
inventing its own captions, which it does unprompted and which then collide with
the ones burned on in Gate 8.

### VOICE STYLE block — required in every prompt that carries a voice

Cast the narrator as concretely as the style lock casts the look: age, gender,
register, pace, and what it must NOT sound like.

> The NARRATOR is a warm, low, unhurried woman in her forties, close and
> confessional, the tone of someone telling you something true rather than
> selling. Never bright, never announcer-like. The IN-SCENE voices are ordinary
> and unperformed.

Always include the negative **`no upbeat announcer voice`**. Models drift toward
radio-ad delivery, and that single drift kills the emotional register. On a beat
whose narration comes from the VO track rather than from the render, this block
describes the in-scene voices only — the narrator is cast once, at Gate 5.

### Beat board — the table you get approved

Two things are decided here: what happens (the skeleton) and how the genre says
to shoot it (the role). The roles are in
[`references/formulas.md`](references/formulas.md); this is where they are
assigned.

| # | Beat | Genre role | Seconds | Track | Visual |
|---|---|---|---|---|---|
| 1 | Hook — the want, stated out loud | A. anthropomorphized problem | 5 | SYNC | … |
| 2 | Problem — the attempt fails | A. second problem character, or the human low | 5 | VO | … |
| 3 | Low point — the private defeat | B. protagonist reveal | 4 | SYNC | … |
| 4 | Turn — the product arrives and is used | C. mascot mechanism | 6 | VO | … |
| 5 | Payoff — warmth, then the hero card | D. CTA and end card | 5 | VO closes | … |

That mapping is the default, not the only one. Role A can hold two beats as a
montage; role B can take the SYNC beat as a first-person testimonial. What does
not move: **role A opens** and **role D closes**, and at least one of them is
SYNC.

Rules for the board:

1. **One action per beat.** Two actions in one prompt is the single most reliable
   way to get glitched physics. Splitting them is what a storyboard is FOR.
2. **Give each beat its own setup.** Five beats in one location at one shot size
   reads as boring no matter how clean the arc is. Change location at least once;
   vary shot size (medium → close → wide). Measured against the reference ad this
   skill was rebuilt to match: its beats each had their own world — a macro
   problem shot, a lit interior, a stylized interior cross-section, a card — and
   T12's three all shared one. That is the difference a viewer names first.
3. **The low point is the shortest beat and the most important one.** Everything
   rides on that face.
4. **Word budget is per beat, not per ad.** Two spoken lines per 5-second beat is
   the ceiling: at the measured 2.0 words/sec that is ~10 words a beat, so five
   beats make a **45–50 word** script for 25s (60 needs 30s). Count before you write.
5. **VO and SYNC never overlap in the same beat.** Write the SYNC lines first;
   fit the narration into beats that have none. And keep the narrator's words out
   of the prompt for any beat you are giving a VO line — see the hard constraint
   above. The board's Track column is what records that decision per beat.
6. **The two tracks own different things.** VO owns the problem, the mechanism,
   the offer and the brand: that track carries the selling. SYNC owns proof that
   the feeling is real. Never give SYNC the offer. Sign-off under 6 words (~3s at
   the measured rate — read it against its gap), hero card at least 2 seconds.
7. **Prefer escalating specifics over comparisons.** "Four times. Four and a
   half. Five. All the way to six" argues the same point as "most stop at three"
   without asserting a competitor fact you cannot verify.
8. No em dashes in ad copy. Never say free: every Novoads plan is paid.

## Gate 3 — stills first, all of them, then STOP

Render every beat still BEFORE any clip. Sequentially, each referencing the cast
sheet and the previous still:

```
POST /v1/uploads (product photo) → PUT the bytes with the returned `headers` VERBATIM
      │
      ▼
POST /v1/images  cast sheet   1:1   ref [product]
      │  ← images[].assetId (a `running` answer: poll it first). Pass it straight to the next call.
      ▼
POST /v1/images  beat 1       9:16  ref [castSheet, product]
POST /v1/images  beat 2       9:16  ref [castSheet, beat1]
POST /v1/images  beat 3       9:16  ref [castSheet, beat2]        ← sequential,
POST /v1/images  beat 4       9:16  ref [castSheet, beat3]          each on the
POST /v1/images  beat 5       9:16  ref [castSheet, beat4]          one before
      │  ← each one's assetId feeds the next, no upload in between
      ▼
╔═══════════════════════════════════════════════════════════════════════╗
║  BOARD GATE — show all six images in order. Wait for the operator.    ║
║  Six images spent, every clip still unspent — and the clips are       ║
║  most of the run. A wrong character, a wrong palette or a wrong       ║
║  location caught here is the cheapest fix this pipeline has.          ║
╚═══════════════════════════════════════════════════════════════════════╝
```

One still call in full. Every other call in this file is the same shape:

```bash
curl -sS -X POST https://api.novoads.ai/v1/images \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"gpt-image-2","prompt":"<style lock + beat 1 + negatives>",
       "aspectRatio":"9:16","referenceAssetIds":["<castSheet>","<product>"]}'
```

**`POST /v1/images` usually answers with the finished image.** One still going after about 105 seconds answers `status: "running"` with no images (API 2.39.0): poll `GET /v1/generations/{jobId}` to a terminal status (`succeeded`, `failed`, `blocked`, `canceled`) and read `images[]` there, never resubmit. Otherwise the finished image is in the response,
and the call blocks for 60 to 90 seconds while it
renders. **Write each image to disk as you read the response** — on a
`numImages > 1` call only the first image is recoverable afterwards, and the rest
exist nowhere but that response body.

**A generated image IS an assetId — chain it directly.** The response carries
`images[].assetId` alongside `images[].url`, and that id is what
`referenceAssetIds`, `startImageAssetId` and `sourceAssetId` take. No download,
no re-upload, nothing in between:

```
POST /v1/images → images[0].assetId  ← pass this to the next call, as-is
```

**Chain from `assetId`, not from `url`.** The URL is a one-hour presign for
fetching the bytes; the assetId does not expire that way. Still download each
still as it lands if you want the files locally — a slow board review will
outlive the URLs.

**Chain each still on the previous one, not just on the cast sheet.** That is
what carries the location, the light and the wardrobe forward. `gpt-image-2`
takes up to 4 reference images, so cast sheet plus previous still plus the
product leaves room for one more; use it for the product when the product is in
frame. That cap is per model and the bodies are strict, so a fifth reference is
`400 Too big` rather than a silently dropped image.

**This gate is one stop, not five.** Do not ask after each still. A board is
approved as a board — the operator is judging whether beat 3 follows beat 2,
which they cannot do one image at a time.

## Gate 4 — the clips, in waves of five

```bash
curl -sS -X POST https://api.novoads.ai/v1/videos \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"seedance-2.0","prompt":"<beat N>","durationSeconds":5,
       "aspectRatio":"9:16","startImageAssetId":"<beat N still>","audioEnabled":true}'
```

Returns `202` with `jobId`, `status`, `creditsCharged` and `model`.

**Submit in waves of at most five.** Five video generations may be in flight per
organization; a sixth comes back `429` with `error.details.reason` of
`concurrency_limit`, which is a real refusal and not a queue. Five beats is
exactly one wave. Six beats is one wave of five, then one. The stills are not
part of that budget — images have their own ceiling of 12 — but they are chained
sequentially anyway, so it never comes up.

**Write every jobId down the moment it comes back**, before you start waiting —
id, which beat, and `creditsCharged` from this `202`. **The charge is on the
submit response and nowhere else**; the poll payload does not carry it, so a line
written without it can never be completed. A job whose id you recorded is a
lookup when something goes wrong. A job whose id you did not is an investigation.

**Poll `GET /v1/generations/{jobId}` every 15 seconds, until TERMINAL.**
`succeeded`, `failed`, `blocked` and `canceled` are all terminal; a loop that
waits only for `succeeded` spins forever on a render that is already dead. Not
every 3 seconds: five jobs on a 3-second interval spends the whole per-key rate
budget on polling. `queued` means charged and submitted but not yet rendering,
which is normal and not a stall. Expect 3 to 8 minutes per Seedance beat.

Download the finished clip through `GET /v1/generations/{jobId}/watch`, which
`302`s to a URL signed at request time, so it never hands you an expired link:

```bash
mkdir -p outputs/<ad-name>
curl -sSL -o outputs/<ad-name>/beat1.mp4 \
  https://api.novoads.ai/v1/generations/$JOB_ID/watch \
  -H "Authorization: Bearer $NOVOADS_API_KEY"
```

The `mkdir -p` is not boilerplate: `outputs/` is gitignored and absent in a fresh
clone, and curl's failure on a missing directory reads like a broken download of
a render that already succeeded and was already billed.

**If a call times out, do NOT generate again.** The work usually completed and
was charged; what timed out was the response carrying its id. Call
`GET /v1/generations?limit=10&kind=video`, find the job by `createdAt` and its
prompt, and take it from there. There are no idempotency keys, so a blind retry
renders and charges a second time.

### Per-clip QA, before you spend a voice-over on it

Check each clip as it lands. A beat that fails here is one still and one clip to
redo; a beat that fails after the mix has cost the mix too.

1. The character is the same character as the cast sheet.
2. The action in the prompt is the action on screen, and it is ONE action.
3. Nothing grew eyes, limbs or a mouth that the design does not have.
4. The product's identifying details survived, and any printed label is legible.
5. The clip's own audio is usable — ambience and in-scene voices, not a music bed
   competing with the narration you are about to lay over it.

**The repair depends on the failure, and the two repairs are opposites.** A beat
that did two things, smeared its action or glitched its physics gets a SHORTER
prompt: fewer clauses, one action, the actor named in it. A beat that grew a
sixth finger, melted a feature or drifted a label gets ONE added negative naming
that artefact exactly. Getting it backwards is why a beat gets re-rolled three
times. The table in `references/formulas.md` has both cases.

## Gate 5 — the voice-over

One line per beat that needs narration. Pick the voice once:

```bash
# read the catalog once and filter in your own code — do not print it
curl -sS https://api.novoads.ai/v1/voices -H "Authorization: Bearer $NOVOADS_API_KEY" \
  | jq -r '.voices[] | select(.source=="platform") | "\(.id)  \(.name)"'

curl -sS -X POST https://api.novoads.ai/v1/voiceovers \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"script":"<beat 2 VO line>","voiceId":"<the one>"}'
```

**This call returns the finished mp3, not a job.** `200`, with `url`, `assetId`,
`characters` and `creditsCharged` in the response. There is nothing to poll —
download the `url` immediately, because it is time-limited and minted per
response. If a call times out, do NOT retry it: the audio was probably rendered
and charged, and `GET /v1/generations` will show it with its cost.

**`voiceId` is required and has no default** — a default would be a performance
you are charged for without having heard it. `GET /v1/voices` returns the
platform voices plus your own organization's clones; an id belonging to another
organization is a `404`.

**Write the lines to the gaps, not to the beats.** A beat with a SYNC line has no
room for narration. Read each line aloud against the beat's length before
generating it: **13 characters per second** of speech — so a 5-second beat holds
~**65 characters**, and the hard 1,000-character ceiling is ~**75 seconds**,
refused with a `400` before anything is charged. (Measured 13.2 = the 2.0
words/sec rate written out: 29 words/188 chars over a 14.2s span, 2026-08-11, one
render, spaces counted. This read 15/sec yet called 1,000 chars 40s, implying 25.)

**The script is read VERBATIM**, including anything in square brackets — the
model interprets those as performance tags rather than skipping them. Keep stage
directions out.

**Language**, if the ad is not in English: pass `language` and pick a voice whose
`languages` include it. A mismatch is refused before anything is charged, which
is the good outcome; picking a voice that does not speak the language and getting
a charged take in the wrong accent is the bad one. Voices with no recorded
languages — typically your own clones — accept any value.

Voice-overs have their own concurrency budget of **10**, counted separately from
the five video slots, so a batch of lines can never refuse a render. A `429` here
carries `details.reason: voiceover_concurrency_limit` and clears in seconds.

## Gate 6 — the music bed

```bash
curl -sS -X POST https://api.novoads.ai/v1/music \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"<what it sits under>","instrumental":true}'
# → 202 { jobId } — poll GET /v1/generations/{jobId}, then read audio[]
```

**Generating the bed is this gate. LAYING it is the LAST thing that happens**, and
never as hand-written ffmpeg — it goes through
[music-mix](../../shared/skills/music-mix/SKILL.md) *after* Gate 8's burn, because
the script stream-copies the picture and the burn's own transcription of the voice
should never have music under it:

```bash
python3 shared/skills/music-mix/scripts/music_mix.py \
  captioned.mp4 music.mp3 master-lofi-warm.mp4
```

Read that skill first. What it does that a hand-written chain did not: it
**measures** the bed rather than multiplying it — `volume=0.10` is -20 dB on a
level nobody checked, measured on a real run at -33 to -40 dB, a bed paid for and
never heard — refuses a silent track or an inaudible gain before rendering, ducks
under the voice, masters, and verifies. Report its verification line verbatim.

One request returns TWO takes for one charge. Listen to both and use the one that
sits better under the voice; they differ in length and arrangement, not price.
Two takes is also what makes 2 or 3 named variants free — another `music_mix.py`
pass each, no second generation. Expect one to two minutes of audio whatever you
ask for; the script trims it. `audio[]` on the polled job is the only place the
second take is published.

`prompt` is capped at 500 characters, and the cap applies to the **composed**
prompt: `style` and the instrumental sentence are concatenated into it before
submission. A music job spends one of the five shared video slots.

**If `/v1/music` is absent from `GET /v1/openapi.json`, skip this step.** It sits
behind a deployment flag; where music is off the path answers `400 invalid_input`
rather than a `404`, and the `music` estimate arm is gone too. Say one sentence —
"no music bed on this account, mixing without one" — and carry on. The ad works
without it; clip audio plus narration is a complete mix. No bed means no script
pass either, so master the captioned cut by hand, to the target the mixer uses:

```bash
ffmpeg -i captioned.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy master.mp4
ffmpeg -i master.mp4 -af ebur128=framelog=quiet -f null -    # read Integrated
```

## Gate 7 — local assembly

This is where the seams either disappear or announce themselves.

**Do the assembly in `outputs/<ad-name>/`, not in the directory you started in.** The
downloaded beats, `beats.txt`, the trimmed clips, the placed VO lines and the master are one
run's working set — a dozen of them loose in a repo root is a diff somebody else has to
explain. Make the directory before the first download and stay in it; every path below is
relative to it.

### Trim to the narration, not to the clip

For each beat: the clip is as long as you asked for, and the line inside it is
whatever length it is. **Trim the clip to the voice-over plus 0.5 seconds**, not
the other way round. Dead air at the end of a beat is the single most common tell
that an ad was assembled rather than shot.

```bash
# VO duration, to two decimals
ffprobe -v error -show_entries format=duration -of csv=p=0 beat2-vo.mp3
# trim the clip to it, +0.5s of air
ffmpeg -i beat2.mp4 -t <vo+0.5> -c:v libx264 -c:a aac beat2-trimmed.mp4
```

**Trimming is the default, not the only option.** A beat with no narration keeps
its own length; otherwise measure both and pick per beat. **A**, most beats: the
VO is shorter, so re-encode the clip to `vo + 0.5s` — 0.25s of lead, 0.25s of
tail, and anything past that is dead air. **B**, when the visual needs its full
length for a long camera move, the mascot mechanism or a CTA hold: extend the VO
instead, a word or two or a second short line, re-rendered and re-measured.

**If the VO is LONGER than the clip, never speed it up.** No `atempo`. Split the
line across two beats, or re-render the beat at a longer duration. A voice at
1.1x is audible as a voice at 1.1x, and it costs the ad its calm.

**Re-check the caption's vertical position after trimming.** The frame at the new
cut is not the frame that was there before, so a caption band that sat over clean
floor can land on a face or a label. This is why captions are burned AFTER the
trim and the mix, never before: the timings and the safe area both move.

### Concatenate, then build ONE voice track

The picture and the voice are assembled here. **The bed is not** — Gate 6 says why.

```bash
FMT="aformat=sample_rates=48000:channel_layouts=stereo"   # one shape for all

# 1. concat the trimmed beats
printf "file '%s'\n" beat*-trimmed.mp4 > beats.txt
ffmpeg -f concat -safe 0 -i beats.txt -c copy stitched.mp4

# 2. place each VO line at its beat's start. adelay is MILLISECONDS and takes one
#    delay PER CHANNEL: `adelay=5000|5000` on a MONO take delays the single
#    channel it has and drops the second value. `all=1` delays whatever it finds.
ffmpeg -i beat2-vo.mp3 -af "adelay=5000:all=1,$FMT" vo2-placed.wav

# 3. the beats' own audio, placed the same way, split by track type
ffmpeg -i beat1-sync.mp4 -vn -af "adelay=0:all=1,$FMT" sync1.wav
ffmpeg -i beat2-vo.mp4   -vn -af "volume=0.28,adelay=5000:all=1,$FMT" amb2.wav

# 4. one voice track. duration=longest, NEVER `first` — `first` ends the mix when
#    input 0 ends: measured, the audio stopped 2.4s before the picture and the
#    hero card played silent. normalize=0 stops amix dividing by the input count.
ffmpeg -i vo2-placed.wav -i sync1.wav -i amb2.wav -filter_complex \
  "[0:a][1:a][2:a]amix=inputs=3:duration=longest:normalize=0:dropout_transition=0[a]" \
  -map "[a]" voice.wav

# 5. the voice onto the picture. Read its duration back against stitched.mp4.
ffmpeg -i stitched.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac voiced.mp4
```

**The clip track is TWO different things and one level cannot serve both.** On a
VO beat the clip audio is ambience and belongs at about 28%, which is what step 3
does to it. **On a SYNC beat the clip audio IS the dialogue and belongs at 100%**,
because attenuating it is attenuating the only line in the shot. Measured, and
the reason this is a rule: a run mixed at a flat 28% buried its SYNC beat so far
down that an independent judge measured the line at -36 dB, under a caption
spelling out words the viewer could not hear. That is worse than no line.

If the narration is fighting something, lower the AMBIENCE track before you raise
the voice. Never lower a SYNC beat's own track to make room. **The order from
here is fixed:** end card → concat → voice mix → transcribe → captions (Gate 8) →
the bed, laid by `music_mix.py`.

**If you hear a line twice, the mix is not the problem.** That beat's prompt
carried the narrator's words and Seedance rendered them, and no level will fix
it — re-render the beat with the narration removed from the prompt. The
transcribe-verify step below is what catches this, and it is why that step is not
optional.

### The end card is composited, never rendered

The last beat ends on the real product photograph, dropped over the render. Do
not ask the model to draw the card: asking it to draw a card is asking it to
regenerate a wordmark from scratch, and it will get it wrong. Measured on this
family of runs — `Novoads.ai` came back as `Novads.ai` in every frame with the
label-hold clause present and the key frame spelled correctly, and `Owala` came
back as `ovola`. The model carries a MARK, which is a shape, and destroys TYPE.

```bash
# 1. find the cut to the card (expect a dissolve, not the hard cut you asked for)
ffmpeg -i beat5-trimmed.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep pts_time
# 2. measure the product's bounding box in BOTH the rendered card and the real
#    photo, then scale and position the real one to match. Matching by eye jumps.
# 3. fade the real card in on the render's own dissolve curve, at full opacity
#    BEFORE the wordmark becomes legible, or the misspelling ghosts through.
#    `-loop 1` is an INFINITE input and overlay runs to its LONGEST one, so
#    without `shortest=1` and `-shortest` this repeats the last frame forever:
#    measured, a 155 MB end card on a 5-second beat.
ffmpeg -i beat5-trimmed.mp4 -loop 1 -i endcard.png -filter_complex \
  "[1:v]scale=<w>:-1,format=rgba,fade=t=in:st=<t0>:d=0.4:alpha=1[card];\
   [0:v][card]overlay=<x>:<y>:shortest=1:enable='gte(t,<t0>)'" \
  -shortest -c:a copy beat5-carded.mp4
# 4. card BEFORE the concat, and add this to beats.txt: that glob wants -trimmed
```

**Match the card's background to the render before you composite it.** A retail
photo shot on near-white dropped onto a warm cream field leaves a visible
rectangle seam, and the seam is the first thing a viewer sees on the last frame.
Sample the render's own background colour and pad the card to it, or key the
photo's white out entirely.

**Do not let the card be a frozen frame in silence.** Hold the beat's own room
tone under it and let the music resolve rather than cut. A warm animated film
that ends on a still, silent packshot ends on the worst-made object in the ad.

**Then read the wordmark at full crop.** Pull the frame, crop the label, look at
it at full size. A contact sheet at thumbnail size is too small to catch a single
missing letter, which is exactly how the first one shipped.

**And review the CLIPS at full size, not on the contact sheet.** Measured on a
run that used this file: a payoff beat rendered TWO cots and TWO babies, and it
survived a contact-sheet review because at thumbnail width the second cot reads
as furniture. The contact sheet is for judging whether beat 3 follows beat 2. It
is not for judging whether beat 3 is correct.

### Verify what it actually says, before it ships

> Doctrine: [shared/references/craft.md](../../shared/references/craft.md) § 1.
> The call below is this surface's; the rule is not this skill's.

The render can gain or lose a word, and a script that survived in your head is
not evidence. Upload the master and transcribe it, then read it back against the
script:

```bash
curl -sS -X POST https://api.novoads.ai/v1/transcripts \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"assetId":"<the uploaded master>"}' | jq -r '.text'
```

**`POST /v1/transcripts` is synchronous and charged** — the words are in the
response, billed per minute of source with a one-minute minimum, so an ad this
length bills the minimum. It returns `text`, `words[]` with per-word timings
**in seconds**, `segments[]` and an `srt`. **Transcribing the same source twice
is free**, so a retry after a timeout is not a second charge. It sits behind the
`TRANSCRIPT_API` flag: where it is off the path answers `400` naming what the
deployment does render, and you transcribe locally instead.

Read the transcript against the board. A dropped word in the offer line is worth
a re-render of that beat.

## Gate 8 — captions

Captions are burned SERVER-side, and the source has to be an asset the API can
reach. A local file is not a caption source until it is uploaded.

```bash
# 1. mint a presigned PUT for the master
curl -sS -X POST https://api.novoads.ai/v1/uploads \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"contentType":"video/mp4","sizeBytes":<n>}'
# → { assetId, uploadUrl, method, headers } — then PUT the bytes to uploadUrl,
#   sending `headers` VERBATIM. Content-Type and Content-Length are signed into
#   the URL, so an omitted or library-inferred Content-Type is a 403, not an
#   upload.

# 2. burn
curl -sS -X POST https://api.novoads.ai/v1/captions \
  -H "Authorization: Bearer $NOVOADS_API_KEY" -H 'Content-Type: application/json' \
  -d '{"assetId":"<the master>","preset":"<a style>"}'
# → 202 { jobId } — poll GET /v1/generations/{jobId}
```

`GET /v1/caption-presets` lists the styles with their tier and rate, and an ad
this length bills the one-minute minimum on either tier. **Read the list rather
than trusting the names below** — presets are added, and the rate is the list's
to state, not this file's.

Two things worth knowing before you iterate: **re-captioning the same video in
the same preset is free and idempotent**, and the second call returns the first
job's id — but **a different preset is a new job and a new charge**. And a source
rendered with `audioEnabled: false` comes back `409`, because there is no speech
to transcribe.

### Which preset, and why it is not a free choice

The genre's caption look is a specific thing: heavy sans-serif, white fill, a
thick dark outline, roughly 7% of frame height, sitting in the lower third but
clear of the platform UI, changing per phrase rather than per word. That is what
a hand-burned caption track was built to produce, and it is what to match when
picking from the list.

| You want | Reach for | Note |
|---|---|---|
| The default heavy-outline social look | a basic-tier preset such as `hustle`, `slay` or `flex` | Fixed styling, which is the point: it will not surprise you |
| Per-phrase emphasis, a punchline that pops | a dynamic-tier preset such as `glide` or `fusion` | Context-aware animation, worth it on a hook beat. Read its rate off the list |
| A quiet, typographic register | `simple`, `plain` or `lowkey` | Basic tier. Right when the ad is doing the work and the captions should not |

Two things the preset cannot do for you, and both are yours:

- **Placement against the frame.** The preset picks a band; your role D still is
  what leaves the lower third clean for it. Ask for the negative space in the
  still prompt, not in the caption call.
- **The words.** Presets style a transcript; they do not correct one. See the
  gate below.

**Burning locally is the fallback, not the default.** Take it when the transcript
keeps mangling a name you cannot move to the card, or when a brand's caption
styling is contractual. `shared/skills/caption-video/SKILL.md` is that path: free,
any style you can write, and you own the timing, the font licence and the safe
area. At this length that is five phrases of timing to get right by hand, which
is why it is the fallback.

```
╔═══════════════════════════════════════════════════════════════════════╗
║  CAPTION GATE — BLOCKING. Read every caption against the script.      ║
║  A garbled brand name is a FAILED RUN, not a note in the report.      ║
╚═══════════════════════════════════════════════════════════════════════╝
```

**Captions are TRANSCRIBED, not taken from your script**, so they inherit every
mishearing the transcript does — and brand names are what they mishear. Measured
on real runs: a voice-over saying "Owala FreeSip" was captioned **"Olaf. Free sip
water"**; "bottles" came back "bootles"; and a run whose own transcript read
`NoseFrida 1499` shipped captions reading **"Nos Frida 1499."** — the brand split
in half and the price read as a number nobody says out loud.

**The check is the burned frames, not the transcript you already have.** The
captions endpoint returns a new MP4 and nothing else: no caption text, no SRT,
and `GET /v1/generations/{jobId}` on a caption job carries neither. A clean
transcript of the audio is not evidence the burn is clean, because the burn ran
its own transcription. So you look at the video.

**That class of defect blocks the ship.** Do not deliver a master with it and
mention it in the notes; that is what happened to T12 and the caption was the
first thing a viewer read. Compare the burned captions word by word against the
board's script. If a brand name, a product name or a number is wrong in even one
frame, the run is not finished.

Three fixes, in order of preference:

1. **Keep the brand name out of the NARRATION entirely** and put it on screen as
   the composited end card, which is where a wordmark belongs anyway. This is the
   only fix that removes the failure mode rather than catching it.
2. **Keep numbers out of the narration too.** A price spoken aloud is a price the
   transcript writes as digits. Put it on the card.
3. **Burn the captions locally from your own script**, where you own every
   character. The server pass is the cheap default, not the safe one.

## Output format

Deliver in this order, no preamble:

1. **PRODUCT READ** — verified facts, buyer language, who actually buys, what you
   will not claim, anything unbuyable.
2. **FIT** — one line confirming Gate 0, or a plain refusal naming a better
   format.
3. **ANGLE** — the enemy this ad attacks.
4. **DOCTRINE** — C or D, and why.
5. **CAST + STYLE LOCK** — the cast sheet text, including the terse tag, and the
   paragraph that will be pasted into every prompt.
6. **BEAT BOARD** — the table, with the genre role assigned per beat. Word count
   per beat against the two-line ceiling. At least one SYNC beat.
7. **COST** — the `POST /v1/estimates` figures, announced in one line.
8. Then generate: cast sheet, all stills, **stop at the board gate**, clips, VO,
   music, composite the end card, assemble the voice mix, verify, caption, lay
   the bed with `music_mix.py`, and **read the captions against the script before
   calling it finished**.

## The calls

The fields that matter to a beat. Auth, strict-body rules, status codes and error
envelopes are in [`skills/novoads-api/reference.md`](../novoads-api/reference.md).

```
POST /v1/uploads      { contentType: "image/jpeg" | "video/mp4", sizeBytes: <n> }
                      → 201 { assetId, uploadUrl, method, headers } — PUT the
                        bytes with `headers` VERBATIM. Free. The upload URL
                        expires in 900s; the assetId does not expire at all.

POST /v1/estimates    { kind: "image" | "video" | "voiceover" | "music" | "caption", … }
                      → { credits, balance, sufficient, shortBy?, topUpUrl?,
                          warnings? }   Strict per arm. `warnings` is advice and
                        refuses nothing; this is the ONLY endpoint that returns it.

POST /v1/images       { model: "gpt-image-2", prompt, aspectRatio: "1:1" | "9:16",
                        referenceAssetIds: [castSheet, previousStill, product?] }
                      → 200 { jobId, images: [{ url, expiresInSeconds, assetId }] }
                        the finished image is in the response (or `running`: poll the job), and
                        the call blocks ~60-90s. `assetId` chains straight into
                        the next call. Max 4 references on gpt-image-2. Its own
                        concurrency budget of 12.

POST /v1/videos       { model: "seedance-2.0", prompt, durationSeconds: 4-15,
                        aspectRatio: "9:16", startImageAssetId: <this beat's still>,
                        audioEnabled: true }
                      → 202 { jobId, status, creditsCharged, model } — not ready
                        yet. `creditsCharged` is HERE and nowhere else.

GET  /v1/voices       → { voices: [{ id, name, source, languages?, category?, labels? }] }
                        Read once. Pick one. Reuse it for every line. Unpaginated
                        and LARGE — filter it in your own code, do not print it.

POST /v1/voiceovers   { script: <=1000 chars, voiceId (REQUIRED), language? }
                      → 200 { url, assetId, characters, creditsCharged, voiceId }
                        ALREADY DONE — no jobId to poll. Download `url` now.

POST /v1/music        { prompt: <=500 chars, instrumental: true }
                      → 202 { jobId } — poll, then read audio[] (two takes, one
                        charge). Flag-gated: absent from openapi.json when off.

POST /v1/captions     { assetId | jobId, preset }
                      → 202 { jobId } — poll. Same video + same preset is free.

GET  /v1/caption-presets → { presets: [{ id, tier, credits }] }

POST /v1/transcripts  { assetId | jobId }
                      → 200 { text, words[], segments[], srt, creditsCharged }
                        SYNCHRONOUS and charged. Timings in SECONDS. The same
                        source twice is free. Flag-gated.

GET  /v1/generations/{jobId}        → { status, kind, outputUrl?, audio? }
GET  /v1/generations/{jobId}/watch  → 302 to a freshly signed download URL
GET  /v1/generations?limit=&kind=   → the recovery path when a call times out and
                        you never received the jobId. Reads only, spends nothing.
```

### Worked beat prompt

A finished **beat 4** (the turn) `POST /v1/videos` prompt — one action, style lock
included, negatives at the end.
`lib/generation/__tests__/pixar-storyboard-skill-prompts.test.ts` reads this exact
block and runs it through the same rule engine `POST /v1/estimates` lints with, so
the worked example cannot drift into one the lint has real complaints about.

<!-- eval:beat-prompt:start -->
```
Stylized 3D animated feature film look, 9:16. A warm kitchen in late afternoon,
one window low and to the left as the only light source, honey and clay palette,
35mm at chest height, shallow focus band on the counter.

The grandmother sits at the table with the copper kettle in front of her. She
lifts the lid in a single frame and the steam catches the window light across her
face. She says, half to herself: "There you are."

No other speech in this shot. This beat's narration is laid in afterwards from
the voice-over track, so nobody here speaks it.

The kettle is exactly as shown in the reference: same shape, same colour, same
proportions, same finish. Do not redesign or restyle it. Hold the printed markings
on the base sharp and legible. The woman is a warm, unhurried grandmother in her
seventies in a grey cardigan.

no named or copyrighted animated film characters, no photorealistic humans, no
uncanny faces, no dead eyes
```
<!-- eval:beat-prompt:end -->

## IP rules

The trademark risk here is higher than for any material-based style, because this
aesthetic belongs to specific studios and the models will hand you near-copies of
their characters.

- **Never name a studio or a franchise in a prompt.** Write "stylized 3D animated
  feature film look."
- Never depict named or recognisable characters. Original designs only.
- Do not reproduce a studio's mascot or signature motifs, even by allusion.
- The negative block above carries the four negatives that enforce this, and it
  is pasted into every prompt, still and clip alike.

## Failure modes

- **The prompt is rejected.** Only content moderation can refuse a render, and it
  answers `422`. There is no rule-id rejection any more, so a refusal is not a
  wording problem to lint your way out of — read what it says. Nothing is
  charged.
- **`429` with `details.reason: concurrency_limit` on the sixth clip.** Not an
  error in your request: five video generations are already in flight. Wait for
  one, then submit. This is why the waves are five. Branch on `details.reason` —
  `image_concurrency_limit`, `voiceover_concurrency_limit`,
  `caption_concurrency_limit` and `transcript_concurrency_limit` are four
  separate budgets, and none of them means "stop rendering".
- **A `403` carrying Cloudflare's `error code: 1010`.** Not your key. The edge
  refuses Python's stdlib `urllib` User-Agent outright, and the body is an edge
  page rather than the API's `{"error":{…}}` envelope. Use `curl`. Do not
  regenerate the key or tell the user their plan lapsed.
- **The character changed between beats.** The cast sheet was not referenced, or
  a still was chained on the cast sheet alone rather than on the previous still.
  Re-render the stills, not the clips.
- **The grade drifted across beats.** The style lock was reworded. Paste it
  verbatim and re-render the affected stills.
- **Two props in one clause glitch physics.** "Swallows capsules with water"
  rendered capsules on the counter and an empty palm. Split into sequential
  single-action sentences, name the actor in each, and add explicit negatives.
- **A stray reference became a shot.** Every reference passed to a render is a
  shot the model may spend time on; an unneeded product still produced a 0.13s
  flash insert. Pass only what the beat needs.
- **The render gained or lost a word.** Measured: "And wake up, we're rested" for
  a scripted "And wake up rested". Transcribe before shipping; never assume the
  script survived.
- **The wordmark on the rendered product is garbled.** Expected, and the
  labelHold clause does not fully fix it — measured on a run carrying the
  canonical clause verbatim that still rendered "Owala" as "ovola". The model
  carries a MARK (a shape) and destroys TYPE. Do not re-roll hoping for a clean
  one: keep the label small and out of focus in the beats, and composite the real
  product photo over the final beat, which is what Doctrine C does and why.
- **The product grew eyes under Doctrine D.** State the negatives explicitly and
  re-render. If it happens twice, switch to Doctrine C.
- **The captions renamed the product.** They are transcribed from the audio, not
  from your script. Blocking, not a note. See Gate 8.
- **Every beat is a VO beat and the ad feels flat.** The doubling rule was
  over-obeyed. At least one beat must be SYNC, and role A is the one that wants
  it: a problem character speaking its own complaint is the genre's opening move.
- **The beats all look like the same shot.** No role was assigned, so every beat
  became a setup shot. Each beat gets its own world and its own shot size, and
  the roles in `references/formulas.md` are what produce that variety for free.
- **The product is in every frame.** It belongs in roles B and D and on the end
  card. In the hook and the mechanism scene it is a distraction from the only
  thing carrying the ad, which is a face.
- **Dead air between beats.** The clips were not trimmed to their narration. Go
  back to Gate 7.
- **A caption for a line nobody can hear.** The SYNC beat's own audio was mixed
  at the ambience level. Its track goes at 100%, not 28%. See Gate 7.
- **The music bed cannot be heard at all**, or **the whole ad plays quiet.** The
  bed was laid by hand: a multiplier instead of a measurement, and no mastering
  pass. Lay it with `music_mix.py`, which refuses an inaudible bed before it
  renders and masters and verifies afterwards.
- **The audio ends before the picture.** `amix=duration=first`. Use `longest`.
- **The render duplicated a prop or a character.** Measured: one cot and one baby
  came back as two. Name the count in the prompt ("exactly one cot, exactly one
  baby") and negate the clone, and review the clip at full size.
- **`402`.** Not enough credits. `error.details` carries `required` and
  `available` — report both and the top-up path. Do not retry.

## Hard rules

- One product per run.
- Stop at the board gate. The operator approves the board before any clip fires.
- Never invent reviews, ratings, prices, or performance claims.
- Never claim what the reviews contradict.
- Use the real brand and the real packaging from the photo. Never invent a brand
  and never blank-label the product.
- On-screen text is short words and numbers only, never sentences.
- No em dashes in ad copy. Never say free: every Novoads plan is paid.
- The end card is composited from the real photograph. Never rendered.
- If a fact cannot be verified from the source given, leave it out and say so.
- Transcribe the master before you call it finished.
- Read the burned captions against the script. A garbled brand name blocks the
  ship.
