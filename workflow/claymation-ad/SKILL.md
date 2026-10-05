---
name: claymation-ad
metadata: {packVersion: 1.3.0}
description: >-
  Builds a hand-sculpted stop-motion CLAY ad on the Novoads REST API as a
  STORYBOARD: five to eight beats, each rendered from its own key frame, a
  storyteller narration laid into the gaps, a music bed, captions burned on,
  assembled locally with ffmpeg. Carries the genre's arc (named protagonist,
  inciting moment, social beat, quiet despair, sculpted clay infographic,
  discovery, transformation, resolution card), and also recreates a found clay
  ad by reading the reference video locally with ffmpeg and Whisper. Use for
  ANY clay or stop-motion ask at ANY length: "claymation ad", "stop-motion
  ad", "clay ad", "a quick clay ad", "plasticine characters", "make an ad like
  this clay one", or a reference video with sculpted clay characters in it.
  There is no one-call tier here, so ffmpeg is required. Not for the smooth 3D
  animated look (use pixar-ad, which covers every Pixar-style length),
  talking-head UGC (novoads-api), or a static image ad.
---
<!-- AUTO-GENERATED FILE. Do not edit it: the next build overwrites you.
     Source of truth is sections/, registered in sections/manifest.json.
     Edit the section, then run: python3 scripts/build-skill-md.py -->

# Novoads Claymation Ad

One product in. A 40 to 70 second hand-sculpted clay ad out, cut from five to
eight separately rendered beats, with narration, music and captions.

This is the **sibling** of `pixar-ad` and it runs the same pipeline: the
same gates, the same calls, the same still gate, the same local assembly. Read
that skill for the pipeline. **This file owns two things it does not: the clay
look, and a narrative arc that is longer and quieter than the Pixar one.**

The two are not interchangeable, and the difference is not decoration:

| | Pixar storyboard | Claymation storyboard |
|---|---|---|
| Hook | an anthropomorphized problem with eyes, speaking | a named person in their kitchen, and a narrator |
| Arc | 4 to 6 beats, a want and a turn | 5 to 8 beats, a small life story |
| Voice | in-scene SYNC plus narration | a storyteller carrying almost all of it |
| Surface | smooth, wet-eyed, subsurface scattering | matte clay, thumbprints, tool marks |
| Runs on | want, then relief | affection for a character |

Picking the wrong one is not a style mistake, it is a story mistake. If the
product's pain is a moment, that is the Pixar skill. If it is a season of
someone's life, it is this one.

**Every clay ask lands here, including the short ones.** There is no one-call
clay tier. A five-beat short is the small end of this pipeline, not a different
door: still per-beat renders, still ffmpeg, still an assembly.

## Before anything: this runs on a Novoads account

1. A Novoads account with credits. https://novoads.ai. There is no free tier and no trial:
   every plan is a paid monthly subscription, published at novoads.ai/pricing. Never call it free.
2. **An API key in `.env` at the repo root**, as `NOVOADS_API_KEY=novo_…`. Check
   it with `./scripts/check-novoads-env.sh`; if it is missing, run
   `./scripts/setup.sh`. That is the whole setup: `curl` and `jq`, one key, no
   connector to add and no session to restart.
3. **ffmpeg on your machine.** The assembly happens here, not on the server.
   `ffmpeg -version` before you start.

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

**Every HTTP mechanic here belongs to the pack, not to this skill.** Auth, strict
bodies, status codes, the poll loop, rate limits and error envelopes are written
out once in [`skills/novoads-api/SKILL.md`](../novoads-api/SKILL.md) and its
[`reference.md`](../novoads-api/reference.md). The per-call fields this genre
needs are in `pixar-ad`'s *The calls* section, which this file shares
unchanged.

## What one run costs

Two shapes, and the choice is the operator's. What changes between them is the
COUNT of the same components, never their kind:

| Component | 5-beat short | 8-beat full |
|---|---|---|
| Cast sheet image | 1 | 1 |
| Beat stills | 5 | 8 |
| Beat clips | 5 × 6s | 8 × 7s |
| Voice-over lines | 5 | 8 |
| Music bed | 1 | 1 |
| Transcript, then one caption pass | 1 each | 1 each |

**There is no price column, on purpose.** Every credit number this run shows a
user comes from `POST /v1/estimates`, in this session, before anything is
charged: price each KIND once, multiply by the counts above, and quote what came
back. A rate written into a skill file goes on being quoted long after it moved.

**The clips are most of the bill either way**, and a still is a small fraction of
the clip it seeds. That is the whole economic argument for the board gate.

**Say the shape out loud before pricing it.** An 8-beat clay ad is the most
expensive thing in this family, and the honest question at Gate 0 is whether
beats 3, 4 and 5 are earning the three extra clips they cost. They often are; the
arc is what this genre is for. But the operator decides that, not you.

## Hard constraints

Everything in `pixar-ad`'s Hard constraints section applies unchanged:
one call per beat, 4 to 15 seconds, 9:16, `audioEnabled: true`, a narrator line
in the prompt OR the VO track and never both, one continuous voice, no
`styleFamily` field. Read them there.

Three are different here:

- **Five to eight beats**, not four to six. The arc is a story and a story needs
  its middle. Below five beats it is a Pixar-shaped ad in clay, and the Pixar
  skill will render it better and cheaper.
- **The narrator carries the ad.** This genre is third-person storytelling, and
  the narration is not filler between spoken lines the way it is in the Pixar
  skill. Most beats are VO beats and that is correct here.
- **At least one beat is still SYNC.** Usually beat 3, the social beat, where a
  second character says the thing the protagonist has been avoiding. A whole ad
  of narration over silent faces is the failure this rule exists to prevent.

## Two ways in

### A. From a product

Run `pixar-ad`'s Gate 0 and Gate 1 unchanged: is the pain emotional,
visible on a face, in a relationship, impulse-priced; then the product read. One
extra question at this length: **does this product have a before and an after
that a viewer would recognise a month apart?** The transformation beat is the
spine of the clay arc, and a product with no visible change does not have one.

### B. From a found video

The other entry, and the one this genre is usually asked for: someone shows you a
clay ad and wants theirs. Do not guess at its structure from the thumbnail.

**Read the reference locally.** Follow
[`skills/analyze-video/SKILL.md`](../analyze-video/SKILL.md):
frames out with ffmpeg, dialogue out with Whisper, then read the beats off what
you extracted. It costs nothing, needs no key, and — unlike a fixed-window
reader — it covers the whole runtime, which is what a 60-second arc needs.

**There is a hosted alternative, and it is not the default.**
`POST /v1/analyses` returns the structured hook/beat/casting breakdown in one
call (poll it if it answers `running`), priced through `POST /v1/estimates` with
`{"kind":"analysis"}`. Reach for it only when ffmpeg is missing or the local
read has already failed: the local path costs nothing, ffmpeg is a hard
dependency of the assembly anyway, and `/analyses` defaults to reading the
first 20 seconds, which is exactly the setup third a clay arc cannot afford to
lose. If you do offer it, price it first and let the user choose. See
[`reference.md`](../novoads-api/reference.md) § *Ad analysis is on this API now*.

Two things to hold on to whichever way you read it:

- **Sample the whole video, not its opening.** A clay ad spends its first third
  on setup, so a read that stops early gives you the hook, the casting and the
  palette and none of the arc. A board that claims eight beats from a partial
  read is a board with invented beats in it.
- **Write our own story.** Recreate the FORMAT, never the script: their
  protagonist, their brand and their claims are theirs. What transfers is the
  shape, the palette, the pacing and the narrator persona.

## The clay look

### Style lock — one paragraph, pasted verbatim into every prompt

<!-- eval:style-lock:start -->
```
Hand-sculpted stop-motion clay look. Plasticine characters with visible
fingerprint impressions and sculpting-tool marks, matte clay surfaces with
subtle micro-bumps, slightly asymmetric features, painted-on or sculpted
eyebrows. Real knit-fabric clothing with visible wool weave and stitch lines,
wooden and ceramic miniature-set props with hand-painted finishes. Warm tungsten
interior lighting, shallow macro depth of field, soft photographic bokeh.
Subtle imperfection in every surface. Vertical 9:16 composition.
```
<!-- eval:style-lock:end -->

**Never name a studio or a franchise.** The lineage this look comes from belongs
to two specific studios, and naming either is both an IP problem and a
worse prompt: the model reaches for their characters instead of your sculpt.
"Hand-sculpted stop-motion clay" is what the words above are doing.

### The negative block

<!-- eval:negative-block:start -->
```
no live-action footage, no photorealistic humans, no uncanny faces, no dead eyes,
no smooth 3D digital render, no glossy surfaces, no ray-traced reflections,
no subsurface scattering, no wet-eye highlights, no anime style,
no 2D illustration, no named or copyrighted animated film characters,
no extra fingers, no melted features, no morphing between frames,
no warped product labels, no on-screen text, no subtitles, no captions
```
<!-- eval:negative-block:end -->

Half of this block is doing a job the Pixar one does not: **holding the render
away from its own default.** The video models smooth clay into 3D plastic over
the length of a clip, so `no smooth 3D digital render`, `no glossy surfaces` and
`no subsurface scattering` are load-bearing, not boilerplate.

### Material detail — paste the lines that apply to what is in frame

<!-- eval:material-detail:start -->
```
Skin: matte plasticine, visible thumbprint impressions on cheeks and forehead,
small sculpting-knife creases at the corners of the eyes, slight asymmetry
between the left and right side of the face.
Hair: sculpted in distinct ribbon-strands of plasticine, individual strand
grooves carved with a tool, slightly stiff and not flowing.
Eyes: small matte clay orbs set into sculpted sockets, a single soft highlight,
no wet shine.
Knitwear: real chunky wool yarn, individual stitches visible, slight wear at the
cuffs and hems.
Wood props: hand-painted matte finish, visible grain, small dents and scratches
that suggest age.
Ceramic: hand-thrown irregular form, glaze pooling at the bottom edges, slightly
off-round.
Product packaging: a clay-shaded prop with a hand-painted label, the paint
slightly uneven and matte.
```
<!-- eval:material-detail:end -->

This block is the difference between clay and a cartoon of clay. Paste the
relevant lines into every still prompt. Drop the ones for materials that are not
in the frame; a knitwear line on a product close-up buys nothing.

### Faces here may be quirky. That is a licence, not a defect

The Pixar sibling chases APPEAL: symmetrical, soft, a moment before a smile. This
genre does the opposite and it is the single easiest thing to lose when the two
skills sit side by side. **Clay characters are allowed to be odd.** Oversized
noses, deep wrinkles where the sculptor pressed, eyes set slightly unevenly,
a jaw that is not quite level. Quirky beats appealing here, and a clay
protagonist rendered pretty reads as a 3D render wearing a clay texture.

Say it in the prompt, per character, or the model will smooth it out: "an
oversized nose, deep sculpted wrinkles at the eyes, slightly uneven eye
placement."

### Smooth motion or stop-motion judder

Real stop-motion carries a 12 to 15 fps judder. Our renders come out smooth at 24
or 30, and **smooth is the default** because it is what the genre's own reference
ads do.

If the operator wants the judder, it is a post step and never a prompt:

```bash
ffmpeg -i captioned.mp4 -filter:v "fps=12,fps=24" -c:a copy captioned-judder.mp4
```

**Run it before the music bed goes on.** `music_mix.py` stream-copies the
picture, so every pass that re-encodes the picture belongs ahead of it — and then
the file the mixer measures and verifies is the file you ship.

Asking the render for "stop-motion judder" does not control frame rate and does
break the look. Do not put it in a prompt.

## The arc

Eight beats, and the operator picks how many of them get made. The beat formulas,
the variable tables and the worked prompts are in
[`references/formulas.md`](references/formulas.md).

| # | Beat | Seconds | Track | Drop for the short? |
|---|---|---|---|---|
| 1 | Setup — the protagonist in their own world | 7 | VO | keep |
| 2 | Inciting moment — they notice the problem | 6 | VO | keep |
| 3 | Social validation — someone else says it out loud | 8 | **SYNC** | drop |
| 4 | Quiet despair — alone, at a mirror or a window | 6 | VO | drop |
| 5 | Clay infographic — the mechanism, sculpted | 7 | VO | drop |
| 6 | Discovery — they find the product | 6 | VO | keep |
| 7 | Transformation — weeks pass, the change is visible | 9 | VO | keep |
| 8 | Resolution — confident, then the end card | 6 | VO closes | keep |

**The 5-beat short is 1, 2, 6, 7, 8** and lands around 34 seconds. It is the
right call for a first run with a brand, and it is what the dry run below uses.

**Beat 3 is where the SYNC line goes** when the short is not being made. When it
is, promote the SYNC line to beat 6: the protagonist says one short thing to
themselves when they find the product. Do not ship an ad where no mouth ever
moves.

**Beat 5 is optional even in the full arc.** A sculpted clay chart sells a
mechanism; it wastes 7 seconds on a product that has none.

### Which beats earn their place, by category

| Category | Arc | What changes |
|---|---|---|
| Supplement, stress, sleep | the full 8 | Beat 5 is the one that sells it. Keep the chart |
| Beauty and skincare | 8, chart optional | Beats 2 and 4 carry it: the mirror, then the reflection alone |
| Office or B2B | the full 8 | **Beats 1 to 4 in cool fluorescent light**, warm only from the discovery on. The palette is the story |
| Food and kitchen | the 5-beat short | Beats 1, 6 and 7 dominate; if you keep beat 3, make it a family table rather than a cafe |

The office row is the one worth reading twice. Everywhere else this genre is
warm tungsten throughout; a fluorescent first half and a tungsten second half
tells the arc in light before a word is spoken.

Everything else about the board — one action per beat, its own setup, the word
budget, VO and SYNC never overlapping in the same beat, no em dashes, never
"free" — is the Pixar skill's board section, unchanged.

## The cast sheet

Same call, same single image, different contents. Clay ads usually carry **two
named characters**, and the narrator is a third presence who is never on screen.

Write the sheet text first from the template in
[`references/formulas.md`](references/formulas.md), then render it. The template's
slots that matter most here:

- **A name.** The narrator says it out loud, and a named protagonist is most of
  why this genre works. "Diane" is a person. "A woman in her 50s" is a stock
  photo.
- **Middle-aged or older.** The look flatters sculpted laugh lines and hooded
  eyelids, and the arc needs a life already in progress.
- **The terse tag**, 11 to 30 characters, anchored on wardrobe. Our renders
  re-cast on every cut, so this is what carries one face across eight beats.
- **A narrator persona**, chosen once from `GET /v1/voices` and reused for every
  line. Warm storyteller and wry observer are the two that fit; pick one and say
  which.

## The gates

Gates 2 through 8 are `pixar-ad`'s, unchanged, including:

- **Gate 2** — price every kind once with `POST /v1/estimates`, multiply,
  announce in one line, proceed.
- **Gate 3** — every still before any clip, each chained on the cast sheet and
  the previous still by the `assetId` that `POST /v1/images` returns, then
  **STOP at the board gate**. At eight beats there are eight clips waiting behind
  it. This gate is worth more here than anywhere else in the family. A still that
  answers `status: "running"` (API 2.39.0) is polled at `GET /v1/generations/{jobId}` to a
  terminal status, its `assetId` read from `images[]` there, and never resubmitted: a
  resubmit is a second charge.
- **Gate 4** — clips in waves of at most five. **Eight beats is two waves**, five
  then three, because a sixth concurrent `POST /v1/videos` comes back `429` with
  `details.reason: concurrency_limit`, and that is a real refusal, not a queue.
- **Gate 5** — one voice, chosen once from `GET /v1/voices` and passed as
  `voiceId` on every `POST /v1/voiceovers`. **Gate 6** — generate the music bed.
  **Laying** it is the last thing that happens in the run and it belongs to
  [music-mix](../../shared/skills/music-mix/SKILL.md) and its
  `scripts/music_mix.py`, run over the captioned cut, never to hand-written
  ffmpeg.
- **Gate 7** — trim each clip to its narration plus 0.5 seconds, concat, build
  ONE voice track, composite the end card from the real photograph, transcribe
  and read it back. **Read the mix out of the Pixar skill rather than from here**
  — the clip level is per beat, not one recipe, and this line used to restate it
  as a flat `VO 100% / clip 28% / music 10%`. That recipe was written when every
  beat was a VO beat. This genre has a SYNC beat (beat 3), where the clip's own
  audio IS the dialogue, and 28% buries it under a caption spelling out words the
  viewer cannot hear. One number cannot serve both cases, so this file states
  none — and the bed's level is no longer a number at all, it is whatever the
  mixer measures.
- **Gate 8** — captions, and the **BLOCKING** caption gate.
  **A garbled brand name is a failed run, not a note in the report.**

Gate 7 in particular carries four rules this genre needs verbatim and does not
restate here: trim to the VO or extend the VO to fill the shot, **never
`atempo`** a long line to fit, re-check the caption's vertical position after
trimming because the frame at the new cut is not the frame that was there, and
build the voice track with **`amix=duration=longest`** — `first` ends the mix
when its first input ends, which is how an eight-beat arc ships a silent
resolution card.

**Do the assembly in `outputs/<ad-name>/`, not in the directory you started in.** The
downloaded beats, `beats.txt`, the trimmed clips, the placed VO lines and the master are one
run's working set — a dozen of them loose in a repo root is a diff somebody else has to
explain. That includes the judder pass above: `captioned-judder.mp4` and the master live
there too.

Two caption looks fit this genre, and the preset guidance in the Pixar skill's
Gate 8 is how you choose between them. The default is the heavy white sans with
a thick dark outline. The alternative, and the one the genre's own reference ads
use, is **a solid warm-orange rounded block behind white text, sitting slightly
tilted** in the lower third. No preset renders that block, so it is the one case
where the local burn is the right call rather than the fallback.

Two clay-specific additions:

**The clay QA is its own check and it is not the Pixar one.** Both checklists are
in `references/formulas.md`. The one that matters: **the render smooths clay into
plastic over the length of a clip.** Watch the last second, not the first frame.
A still that passed and a clip that ends in glossy 3D is the single most common
failure in this genre.

**Beat 7's improvement must be localised.** "Weeks later" on a whole face
produces a different person, which reads as a lie and breaks continuity in one
shot. Name the one thing that changed and say that everything else is unchanged.

## Output format

Deliver in this order, no preamble:

1. **PRODUCT READ** — or, on entry B, the breakdown of the reference with a line
   saying how much of it was actually read.
2. **FIT** — one line confirming Gate 0, or a plain refusal naming a better
   format. If the pain is a moment rather than a season, hand off to
   `pixar-ad` and say so.
3. **ARC LENGTH** — 5-beat short or 8-beat full, and why, with both prices.
4. **CAST + STYLE LOCK** — the cast sheet text including the name and the terse
   tag, and the paragraph pasted into every prompt.
5. **BEAT BOARD** — the table. At least one SYNC beat.
6. **COST** — the `POST /v1/estimates` figures, announced in one line.
7. Then generate: cast sheet, all stills, **stop at the board gate**, clips, VO,
   music, composite the end card, assemble the voice mix, verify, caption, lay
   the bed with `music_mix.py`, and **read the captions against the script before
   calling it finished**.

## The calls

Identical to `pixar-ad`'s call list — `POST /v1/uploads`,
`/v1/estimates`, `/v1/images`, `/v1/videos`, `GET /v1/voices`,
`POST /v1/voiceovers`, `/v1/music`, `/v1/captions`, `/v1/transcripts`, and
`GET /v1/generations/{jobId}` with its `/watch` — with the fields each one takes.
Entry B adds no endpoint: the reference read is local ffmpeg and Whisper, and
spends nothing.

### Worked beat prompt

A finished **beat 3** (social validation) `POST /v1/videos` prompt: the SYNC beat,
one action, style lock and material detail included, negatives at the end.
`lib/generation/__tests__/claymation-storyboard-skill-prompts.test.ts` reads this
exact block and runs it through the same rule engine `POST /v1/estimates` lints
with.

<!-- eval:beat-prompt:start -->
```
Hand-sculpted stop-motion clay look, vertical 9:16, animating the two characters
in the reference image. A sunlit miniature clay kitchen, green-painted wooden
cabinets, a red gingham tablecloth, warm tungsten light from a window on
camera-left.

Diane, a woman in her late 50s in a cream chunky knit cardigan, matte plasticine
skin with visible thumbprint impressions and deep sculpted laugh lines, sits
across the table from her friend in a sage-green cable-knit sweater.

From zero to three seconds Diane lowers her cup and her sculpted brow furrows.
From three to eight seconds her friend leans in and says: "You have not been
sleeping, have you." Diane holds still and her eyes drop to the table.

Camera: locked medium two-shot at table height, gentle handheld breathing motion,
no dolly, no zoom. Shallow macro depth of field with the window softly out of
focus.

Skin: matte plasticine, visible thumbprint impressions on cheeks and forehead,
small sculpting-knife creases at the corners of the eyes. Knitwear: real chunky
wool yarn, individual stitches visible, slight wear at the cuffs. Ceramic:
hand-thrown irregular cups, glaze pooling at the bottom edges.

Audio: two warm, unhurried voices at a kitchen table, close and intimate, with
faint kettle and street ambience behind them.

Both characters stay visually unchanged from the reference image: same face
proportions, same hair, same wool weave, same clay texture held to the last
frame. no live-action footage, no photorealistic humans, no uncanny faces, no
dead eyes, no smooth 3D digital render, no glossy surfaces, no ray-traced
reflections, no subsurface scattering, no wet-eye highlights, no anime style, no
named or copyrighted animated film characters, no extra fingers, no melted
features, no on-screen text, no subtitles, no captions
```
<!-- eval:beat-prompt:end -->

## Failure modes

Everything in `pixar-ad`'s Failure modes list applies. Four are this
skill's own:

- **The clay turned into plastic by the end of the clip.** The most common
  failure here. The material detail block was thin or the negative block was
  missing its anti-smoothing lines. Re-render with both, and add "clay texture
  held to the last frame" to the constraints.
- **The eyes went wet.** A Pixar-style multi-catchlight eye leaked in. `no
  wet-eye highlights` in the negative block and `a single soft highlight, no wet
  shine` in the material block. Both, not either.
- **The transformation beat produced a different person.** The improvement was
  described on the whole face. Name the one thing and pin the rest.
- **Eight beats and no mouth ever moved.** Every beat went to the narrator. Beat
  3 is a SYNC beat; if you dropped it for the short, beat 6 is.

## Hard rules

- One product per run.
- Stop at the board gate. The operator approves the board before the clips fire.
- Never name a studio or a franchise, in a prompt or in ad copy.
- Never invent reviews, ratings, prices, or performance claims.
- Use the real brand and the real packaging from the photo.
- On-screen text is short words and numbers only, never sentences.
- No em dashes in ad copy. Never say free: every Novoads plan is paid.
- On entry B, recreate the format and never the script.
- The end card is composited from the real photograph. Never rendered.
- Transcribe the master before you call it finished, and read the burned captions
  against the script. A garbled brand name blocks the ship.
