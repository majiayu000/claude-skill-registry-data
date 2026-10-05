---
name: keyframe-animation
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai, plus two images you already have, a start frame and an end frame. Animates the motion between them as one video — both frames go into a single Ofox video job, the clip opens on A, closes on B, and the model fills the middle. Use when a user has two stills and wants the in-between animated, e.g. "here is the before and the after, animate the transition", "make a video that starts on this image and ends on that one", "tween these two frames", or "move the object from where it sits in the first picture to where it sits in the second". Do not use when only one image exists (animating a single frame is seedance-ad-creative or seedance-product-video), or when the pair is two states of a user interface (see product-demo).
license: MIT
version: "2.0.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/keyframe-animation
metadata:
  author: ofoxai
  version: "2.0.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🎞️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/keyframe-animation
---

# keyframe-animation: start on image A, end on image B, fill in the middle

Two stills you already have become one clip: image A is attached as the first
frame, image B as the last frame, in the **same** job, and the model generates
the motion between them.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns what makes a usable
A/B pair, the prompt for the middle, the duration advice, and the
pre-generation cost estimate; `ofox-video-core` owns talking to the Ofox API
correctly and safely (the `OFOX_API_KEY` handling, the no-resubmit rule,
error-code mapping, download/verification, and reporting the downloaded file's
absolute `VIDEO_PATH`). **Read that skill's safety contract before using this
one** — it is not restated here.

The shared prompt craft — the vendor's formula, timestamp rules, camera
vocabulary, consistency locks, negative lists, and what a frame lock has been
measured to hold — lives in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
The rules for the questions that come **before** a prompt exists are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md),
and the spend rule is in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
This file carries only what is specific to a two-ended interpolation.

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
the probe has to run: every example below assumes the working directory is the
one this `SKILL.md` sits in. From anywhere else nothing resolves — use the
absolute path the probe printed (candidates 3–5 are absolute already), or, in
a clone of this repo, `skills/ofox-video-core/references/ofox-video.sh` from
the repo root.

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

`check` reports whether the key is **present**, not whether it is valid; it
makes no network call. The key is an ordinary environment variable in the
shell that runs the script — the script reads nothing from a `.env` file on
its own, so if a project keeps it in one it has to be sourced into the same
shell before the command runs.

**A failing `check` is not a stop sign for this conversation.** It exits `2`
when `OFOX_API_KEY` is unset, but `models`, `providers` and
`generate --dry-run` all run without a key — so a keyless user can still get
the pair of frames read, the prompt written and the job priced, and only needs
the key at the moment they say yes to the cost table. Do that work first
rather than opening with a signup link; see "Pricing a job with no API key".

## What this skill rests on: three measured jobs on two pairs

Everything below traces to real runs, or it says it doesn't. All three ran
`bytedance/seedance-2.5` at 480p with a first frame and a last frame attached
in one job, **44 to 55 cents each**.

The first two ran 4 seconds on the same inputs: a red square on a flat
background with no text, drawn at x=120–240 in the first frame and at
x=614–734 in the last.

| Job | What it tested |
|---|---|
| `259c3ce2` | the **mechanism** — can both ends be locked in one job at all, and how does the middle behave |
| `2514540e` (2026-09-15) | the **prompt template in this file**, filled in by an agent working from this skill and nothing else. Same pair, so it widens nothing about the inputs; what it adds is that the template — not a hand-written prompt — produces the same result, and that the result replicated |
| `1b7a3fab` (2026-09-17, 5s, 55 cents) | the **inputs** — the first pair that is not the red square. A real photograph of a product carrying a readable wordmark and a brushed-metal texture, left third to right third, cropped for free out of an image this repo already had. It overturned this file's duration claim; see "Duration: the easing curve is not a property of the tool" |

**The third run is the one that changes how to read this file.** Two of the
three clips share a pair, so until it there was **one** input class behind
every claim here, and the file said so. What `1b7a3fab` adds:

- **A real subject with lettering survives the interpolation.** The wordmark
  is intact and legible at every sampled point — 0, 1, 2, 3 and 4.5 seconds —
  not just at the two supplied ends. That is the question a pair of plain red
  squares could not ask, and the answer is positive. It is also the measured
  backing for the AVOID-list advice below, which until now was reasoning.
- **Both ends honoured again**, on a pair the earlier runs say nothing about:
  first frame matches A, last matches B, the camera does not move, the
  background does not change, no second copy of the subject appears.
- ❌ **And the duration claim this file carried did not survive it.** The
  detail is in the duration section; the short version is that the two clips'
  easing curves differ so much that neither can be quoted as the model's
  behaviour.

The measurements below are from `259c3ce2` unless noted. The endpoint result
is the one that has now happened three times:

**Endpoint replication, job `2514540e`.** Scanning the delivered video's own
first and last frames for red gives x=120–239 and x=614–733 — the same
figures, to the pixel, as the first run. **And again on a different pair**
(`1b7a3fab`, a photographed product): first frame matches A, last matches B.
Three runs across two input classes is not a guarantee, but "both ends are
honoured" is by some distance the best-supported claim in this file — and
note that it is the only one that survived the third run unchanged.

| What was measured | The measurement |
|---|---|
| **Both ends are honoured, to the pixel** | scanning the *delivered video's own frames* for red: its first frame has the square at x=120–239, its last frame at x=614–733. Not "the job reported completed" — the artifact was read |
| **This clip's motion was front-loaded** ⚠️ | the same scan at t=1/2/3s gives x≈384, 564, 614. Against a total travel of 494 px that is roughly **53% of the distance in the first quarter, 90% by halfway, and arrival at 3 seconds of 4**. ⚠️ **Do not carry this over to your clip** — `1b7a3fab` measured a near-linear curve on the same mechanism. See the duration section |
| **This clip's last beat was a hold, not travel** ⚠️ | having arrived at ~3s, it stays; the final second delivers no movement. Same caveat — `1b7a3fab`'s hold was about half a second of five |

What those jobs do **not** establish, and this skill does not claim:

- **any easing curve at all.** This used to read "whether the front-loaded
  easing scales with duration is untested", which assumed the front-loading
  and questioned only its scaling. The second duration was measured and came
  back a different shape, so what is untested is the curve itself, on any
  duration;
- anything wider about the **inputs than two pairs**. The first two runs share
  one pair; `1b7a3fab` adds a real photographic subject with lettering. A UI,
  a person, a scene change, or ends that differ in more than one bounded way
  are all still untested here;
- whether first+last in one job works on any model other than
  `bytedance/seedance-2.5`. The catalog lists `i2v` for the current video
  models, but `i2v` says nothing about locking *both* ends at once — that
  granularity is not in the catalog and has not been tested here;
- whether a mismatched pair (two images of different pixel dimensions) works.
  The measured pair were two renderings of one canvas;
- anything about how a pair that differs wildly is interpolated. See "When the
  two frames differ too much", which is reasoning, and labelled as such.

## Before writing the prompt: the brief

The shared rules — the three tiers, one round of at most four questions, the
"Let the AI decide" discipline, the order with the approval gate, the fallback
for a runtime without `AskUserQuestion` — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
This section adds only this scenario's question set.

Most of the axes other Seedance scenarios ask about are settled here by the
two images themselves: the subject, the setting, the framing, the lighting and
the output's shape are all in the pair. **Zero questions is the common case**
when both files arrive with names that say which is which.

| Tier | Keyframe axes |
|---|---|
| **must-ask** | does the second image exist? and, when the input leaves it ambiguous, which of the two is the **start**. Neither can be guessed: a frame that does not exist cannot be invented, and getting the order backwards produces a clip that runs the wrong way and costs the same |
| **ask-if-open** | the path — what happens between the two frames, when the pair leaves more than one reading |
| **never-ask** | duration, resolution, model, provider, audio (off by default here). Aspect ratio is not a question at all: with frames attached the clip follows the frames. Two durations or two resolutions are **two rows in the cost table**, which tells the user more than a question with two labels and no prices. Never-ask means the agent doesn't raise it — a model the user names by id or by shorthand is used instead of the default |

### The question set

| # | Tier | `header` | Question | Options (1 = recommended) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Frames` | I need both ends of this: the picture the clip starts on and the picture it finishes on. Do you have the second one? | **Yes — I'll give a local path (recommended)**: both frames go into one job and the clip lands on both exactly. / **No, only one**: then this is not a two-ended job — animating a single frame is `seedance-ad-creative` or `seedance-product-video`, and I can hand it over. **No AI option** — a frame that does not exist cannot be invented. | Only one image is attached and the user did not name a second. |
| 2 | must-ask | `Order` | Which of the two is where the clip **starts**? | the two filenames as the two options. **No AI option.** | Two images arrived and nothing in the names, the paths or the message says which comes first. Skip it whenever the names themselves state an order — `before`/`after`, `start`/`end`, `first`/`last`, `a`/`b`, `1`/`2`, `01`/`02`, `open`/`closed`, `old`/`new`, a timestamp or a frame number — or the message says so. The list is illustrative: any pair that reads as a sequence to you will read that way to the user. |
| 3 | ask-if-open | `Path` | How should the subject get from the first picture to the second? | **Straight there (recommended)**: the plain reading of the pair, and the only one with a measured run behind it. / **Along an arc**: name the arc in the prompt (over, under, around the object between them). / **Something happens on the way**: describe it and it goes in the prompt as a beat — untested here, and the middle is the part the model invents. / **Let the AI decide**. | The two frames leave more than one plausible route between them. Skip it when the pair is a plain displacement. |

Not asked: duration and resolution (rows in the cost table), the model, the
provider, the audio flag, the aspect ratio.

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| filenames that state an order — `before`/`after`, `start`/`end`, `first`/`last`, `a`/`b`, `1`/`2`, `01`/`02`, `open`/`closed`, `old`/`new`, timestamps, frame numbers | Order | as named; don't ask. Treat these as examples of the pattern, not as the whole list |
| "from this one to that one", in the order the files were attached | Order | attachment order |
| "it should slide / travel / move across" | Path | straight |
| "it should arc / swing / hop over" | Path | arc, described in the prompt |
| "a quick transition", "short", "for a GIF" | duration | the model's minimum — `ofox-video.sh models` prints each model's range |

### From answers to prompt — traceability

| Answer | Lands in |
|---|---|
| Frames: two paths | `--frame-first-image A` and `--frame-last-image B` |
| Order | which path goes on which of those two flags |
| Path | the MOTION line of the prompt |
| Duration | `--duration`, and a row in the cost table |

### The recap for this scenario

```
Brief:
- Start frame: /Users/me/shots/ball-left.png (given)
- End frame:   /Users/me/shots/ball-right.png (given)
- Path: straight across the table (inferred from "slide it over")
- Duration / resolution / audio: 4s / 480p / off — one row below; 720p as a second row
- Frame shape: 1024x576 on both files, so the clip comes out in that shape
```

Then the full prompt, then the cost table, all in one message — the order and
the rule for a change made at the gate are in `creative-brief.md`'s "Order,
with the approval gate".

## What makes a good A/B pair

The two frames are the only thing the job is anchored to, so the pair carries
more weight here than a reference photo does anywhere else in this repo.

- **Two states of one scene, not two pictures.** Same subject, same set, same
  lighting, same camera position and the same distance from it. The measured
  pair differed in exactly one thing — where the square sat — and the model
  had one job to do. The further the pair drifts from that, the more of the
  clip is the model's invention rather than your material.
- **One change, or a small bounded set of them.** Every difference between A
  and B has to be resolved somewhere in the middle, and you are paying for all
  of them at once.
- **Same pixel dimensions on both files.** The measured pair were two
  renderings of one canvas. A mismatched pair has not been run here; matching
  them first costs nothing and removes the question. `hal-image` or any
  ImageMagick/`sips` call will do it, and reading the real pixels
  (`sips -g pixelWidth -g pixelHeight <file>`, `identify <file>`) rather than
  trusting a filename or an export dialog is this repo's standing habit.
- **Crop to the shape you want the clip in, before generating.** With frames
  attached the output follows the frames — see "The frame decides the shape"
  below — so the aspect ratio is a crop you make first, not a flag you pass
  afterwards.
- **A local file beats a remote URL** when one is available.
  `ofox-video-core` base64-encodes a local readable file into the request; a
  publicly reachable URL has been rejected upstream at least once in this repo
  (likely host-side hotlink protection). A URL works, it is just the
  less-reliable of the two.
- **A photoreal person in either frame stops the job by default — and the one
  exception is an authorisation, not a trick.** `bytedance/seedance-2.5`
  refuses a photoreal-person reference at submission
  (`input_moderation_failed`, nothing billed) — a documented `ofox-video-core`
  behaviour, and the refusal happens before any money moves. `--real-person
  true` routes such a reference through Ofox's privacy-preserving preprocessing
  for real-person material the user is **authorised** to use, and as of
  2026-09-16 it is measured lifting that refusal on 2.5. **It is an
  authorisation route, never a way past the check**: reach for it only when the
  user holds the right to use that likeness and has said so, and never as a fix
  for a rejection. What was measured is a synthetic portrait on a single first
  frame at one tier — a two-ended pair with the flag set is outside it, and so
  is a real photograph of a real person. Evidence and limits:
  [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
  → "`--real-person true` lifts that refusal on 2.5".

## Duration: the easing curve is not a property of the tool

**This section used to be headed "the motion arrives early and then holds"
and that was overturned by the second measurement.** It is kept as a heading
rather than quietly deleted because the old version told callers to budget for
a hold, and anyone who read it should know why not to.

Two clips, each read the same way — the subject's horizontal position sampled
per second and expressed as a fraction of the total travel:

| Fraction of the clip elapsed | `259c3ce2` (4s, red square) | `1b7a3fab` (5s, real product) |
|---|---|---|
| 0.25 | ~53% of the distance | — |
| 0.20 | — | 20% |
| 0.40 | — | 51% |
| 0.50 | ~90% | — |
| 0.60 | — | 80% |
| 0.75 | **arrived** | — |
| 0.90 | — | **arrived** |

The first is strongly front-loaded with a quarter of the clip left over as a
hold. The second is **close to linear with a slight ease-out**, and its hold
is the last half second — about 10% of the clip, not 25%.

**So there is no easing curve to plan against.** The two runs differ in
duration (4s vs 5s), subject, travel distance and seed, and one measurement
each cannot attribute the difference to any of them. What used to be written
here as a property of the model is a property of *those two clips*.

What to do with that:

- **Do not promise a hold, and do not promise arrival on the final frame.**
  The old text said flatly that an arrival on the last frame "won't" happen.
  One of two clips arrives at 90% of the way through, which is close enough to
  the end that the claim cannot stand. Tell the user the clip lands on frame B —
  that part is measured, twice, to the pixel — and that **when** it gets there
  is not something this skill can predict.
- **If the timing of the arrival matters, it is a draft question.** Generate
  the cheapest tier first and look, rather than writing a clause. There is no
  known clause.
- **Short is still the honest default**, for a different reason than before:
  not "a longer clip buys more hold" (unsupported) but simply that it bills
  per second and the arrival is unpredictable either way. Start at the model's
  minimum duration (`ofox-video.sh models` prints each model's range) and show
  a longer option as a second row in the cost table.
- **Don't write "at an even speed" into the prompt.** Both clips eased to some
  degree regardless, and an instruction the tool measurably does not follow is
  a liability rather than a rule — this repo has the scar to prove it. If even
  pacing genuinely matters, that is a question for a real run, not a clause.
- **Two points are not a curve.** Do not read the table above as "longer clips
  are more linear". It is two observations that disagree, which is exactly
  enough to retire the old claim and not nearly enough to replace it.

## When the two frames differ too much

**This section is reasoning, not measurement.** The one run behind this skill
used a pair that differed in one thing. Nothing here has been paid for.

The middle of the clip is the part nobody supplied, and the further apart the
endpoints, the more of it the model is inventing. Signals that a pair is
asking for too much: a different set, a different camera position, a different
subject, a different time of day, or several unrelated changes at once.

Three routes, in the order worth trying:

1. **Make the pair closer.** Re-shoot, re-render or re-crop B so it differs
   from A in one bounded way. Cheapest by a wide margin — it costs no API
   call at all.
2. **Split it into two jobs and let the middle be a cut.** Two shorter A→B
   clips joined in an editor beat one clip asked to invent a transition it was
   never shown. Two jobs are two rows in the cost table.
3. **Use `chain` instead** when what you actually have is a *sequence* rather
   than two ends: `ofox-video.sh chain` carries the last frame of one job into
   the first frame of the next and joins the clips. It is a different tool —
   you give it prompts, not a destination frame — but for "keep going from
   here" it is the one that fits.

If the user wants the wide pair anyway, price it, say plainly that the middle
is unmeasured territory, and suggest the cheapest resolution for the first
attempt.

## The prompt

With both ends supplied, the prompt has a smaller job than in any other
Seedance scenario: it is not describing a shot, it is describing **what
happens between two pictures the model can already see**. Keep it to the
subject, the single change, and what holds still.

Vocabulary and the general formula are not repeated here — see
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
Two things from that file bear directly on this template: negative clauses are
honoured more reliably than positive ones, and a camera verb on its own tends
not to produce a camera move. The second is why this template asks the camera
to stay put rather than asking it to travel.

```
SUBJECT: <the subject, in physical words — material, colour, shape, size relative to the frame>. It keeps the same shape, colour, proportions and markings from the first frame to the last.
SCENE: <the setting, described once — it is the same setting in both frames>. The background, the lighting and the framing stay as they are; the camera does not move.
MOTION: the <subject> travels from <where it is in the first frame — "the left third of the frame, on the table"> to <where it is in the last frame — "the right third, on the same table">, <along a straight line | in a shallow arc over the <object>>, staying <in contact with the surface | at the same height> the whole way. Nothing else in the frame moves.
ENDING: it comes to rest in the position of the last frame and stays there.
AVOID: a cut, a fade to black, a dissolve, a wipe; camera shake, zoom, pan or reframing; the <subject> changing shape, colour or size; a second <subject> appearing; motion blur smearing the <subject>; subtitles, captions, on-screen text, watermarks.
```

**About that last AVOID item.** It is here because the *first* measured pair
carried no lettering, so any text in the middle would be text the model
invented — which is the failure mode every `AVOID: on-screen text` line in
this repo exists for. **If your own two frames contain lettering** — a label,
a sign, a readable screen — the premise flips: the model is then interpolating
between two supplied renderings rather than inventing glyphs, and forbidding
text fights your own material. Drop the item.

**That flip is now measured here rather than only reasoned.** Job `1b7a3fab`
(2026-09-17) ran this template on a pair whose subject carries a printed
wordmark, with the no-text item removed for exactly this reason, and **the
wordmark is intact and legible at every sampled point through the clip**, not
only at the two supplied ends. One pair, one wordmark, 5 seconds — but it is
the first direct evidence for an instruction this file had been giving on
inference. `product-demo` is still the skill to read when the pair is two
states of an interface.

### Worked example

Two renderings of one 1024x576 canvas: a red ceramic mug on a light wooden
table, at the left in A and at the right in B, nothing else different.

```
SUBJECT: a red ceramic mug with a rounded handle, matte glaze, about one sixth of the frame's width. It keeps the same shape, colour, proportions and handle angle from the first frame to the last.
SCENE: a light wooden table under even, soft, overhead light, a plain pale wall behind it. The background, the lighting and the framing stay as they are; the camera does not move.
MOTION: the mug travels from the left third of the frame to the right third, along a straight line across the table, its base staying in contact with the tabletop the whole way and the handle keeping the same angle. Nothing else in the frame moves.
ENDING: the mug comes to rest in the position of the last frame and stays there.
AVOID: a cut, a fade to black, a dissolve, a wipe; camera shake, zoom, pan or reframing; the mug changing shape, colour or size; a second mug appearing; motion blur smearing the mug; subtitles, captions, on-screen text, watermarks.
```

Check the draft the same way the evidence jobs were checked: read the
delivered clip's own first and last frames against the two inputs, and sample
the middle — never take `STATUS completed` as proof the interpolation is the
one you asked for. **This template has been run twice, on two different
subjects**: job `2514540e` filled this shape in for a red square, and job
`1b7a3fab` for a real photographed product with a readable wordmark. Both came
back with the ends honoured, which is what the check above is looking for.
What the two disagreed on is *when* the subject arrives — see the duration
section — so check the ends, and look at the middle rather than predicting it.

## The frame decides the shape

With a frame attached, the output's aspect ratio follows the frame, and how it
gets there depends on the model:

- on `bytedance/seedance-2.5`, `ofox-video-core` **forces**
  `aspect_ratio=adaptive` and prints a `NOTE:` saying so, because the API
  requires it for image-to-video on that model. Anything you passed is
  overridden;
- on a model whose catalog entry lists `adaptive`, the script **defaults** to
  it when you pass no `--aspect-ratio`, and keeps your value if you pass one;
- on a model that does not offer `adaptive`, the script sends no ratio and
  says so — the frame's shape may not survive.

So: **don't pass `--aspect-ratio` on this route**, on any model. Crop both
frames to the shape you want before generating; that crop is what actually
decides the output. Relay the `NOTE:` the script prints — it names which of
the three branches applied.

This needs `ofox-video-core` 1.22.0 or newer. On an older core, a non-Seedance
model with frames attached sent no ratio at all, with nothing printed to say
so.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--frame-first-image` / `--frame-last-image` | both, in one `generate` call | the whole point of this skill; both ends were honoured to the pixel on both measured jobs |
| `--model` | not passed — the script's own default applies, **unless the user named a model**, which always wins | both measured jobs ran on `bytedance/seedance-2.5`; whether both ends can be locked on another model is untested here, so say so before switching rather than after. `models` lists the models but does **not** mark which one the script defaults to — the `MODEL` line a `generate --dry-run` prints is what names the id that will really be sent, which is also the id the cost table has to carry |
| `--duration` | the model's minimum for a plain A→B move | the motion arrives at about three quarters of the clip and holds; extra seconds buy hold and bill per second. `ofox-video.sh models` prints each model's range — don't quote a range from memory |
| `--resolution` | the cheapest tier for the draft, the deliverable's tier for the final. **When the user named neither** — the common case — draft at the model's cheapest tier and put the next tier up as a *second row* of the same cost table, so the upgrade is priced rather than asked about | both measured jobs ran at 480p, the cheapest tier their model lists. Which tiers a model has is a catalog fact; `models` prints them, and dry-running both rows costs nothing |
| `--aspect-ratio` | not passed | the attached frames decide it — see "The frame decides the shape" |
| `--generate-audio` | `false` | a tween of two stills has nothing to sync to, and the server's default is `true`. Omit the flag only when the clip genuinely wants a track |
| `--seed` | let the script roll one, and keep it | it prints `SEED` and writes it to the clip's `.json` sidecar, which is what lets "that take, at a higher resolution" be re-submitted at all. It does **not** reproduce it: measured, an identical request on a fixed seed came back a visibly different clip. A byte-identical prompt is necessary and not sufficient — tell the user a re-render is another roll aimed at the same shot before they pay for it |
| `--real-person` | leave unset — **unless the user holds the right to use the likeness in the pair and has said so** | a photoreal person in a frame is refused at submission on `bytedance/seedance-2.5`, nothing billed. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person references, and it was measured lifting that refusal on 2.5 (2026-09-16) — an authorisation route, never a way past the check. Measured on a synthetic portrait as a single first frame; a two-ended pair with the flag, and a real photograph of a real person, are both outside it. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

## Choosing a model

The model stays **never-ask** — the agent doesn't raise it. But never-ask is
not "never listen": if the user names a model, use it.

**Model ids, prices, resolutions, durations and aspect ratios are not written
down in this file on purpose.** They are catalog facts, they change, and this
repo has five recorded defects that trace to a hardcoded copy of somebody
else's value table — the most recent created by refreshing the data next to
it. Read them live instead, free and with no API key:

```bash
bash ../ofox-video-core/references/ofox-video.sh models      # models, tiers, ranges
bash ../ofox-video-core/references/ofox-video.sh providers   # the price matrix
```

One thing worth telling the user before they switch: the first+last-frame
combination has only been run here on `bytedance/seedance-2.5`. The catalog
says the current models do `i2v`, but `i2v` does not distinguish "one end
locked" from "both", so another model is an untested route, not a known-good
one.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the table's required columns, where the numbers must come from, and
what to do when no estimate is possible are written down once for every Ofox
skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
Follow it rather than improvising.

Get the numbers from `--dry-run`, which validates everything and prints the
estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." \
  --frame-first-image /path/to/A.png \
  --frame-last-image  /path/to/B.png \
  --duration 4 --resolution 480p --generate-audio false \
  --out-dir /absolute/path/to/out
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

The brief recap goes in the **same message** as the prompt and the table,
above them.

**The cost anchor this skill has**, with the parameters it was measured at
attached, because a figure without them is not a measurement:
`bytedance/seedance-2.5`, 4 seconds, 480p, first+last frames, **44 cents
billed** — twice, on jobs `259c3ce2` and `2514540e`, at the same figure. It is
not a quote for any other combination — an image-to-video job bills at the
text-to-video tier, so a longer or higher clip scales from the dry run, never
from this number.

Afterwards the **actual** bill is `VIDEO_COST` from the finished job. Report
it as money, not as the raw ten-decimal string. An estimate is never a bill.

### Confirm both frames are attached, before the money moves

The dry run's own output names the model, the duration and the resolution and
says **nothing about the frames** — so a mistyped flag, or a path that quietly
matched only one file, reads as a perfectly healthy quote and shows up in the
delivered clip instead. `--print-payload` closes that: it dumps the request
body on stderr *before* the dry run stops (the API key travels in a header,
never in the body), and the two `frame_type` entries are the part to read:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run --print-payload \
  --prompt "..." \
  --frame-first-image /path/to/A.png \
  --frame-last-image  /path/to/B.png \
  --duration 4 --resolution 480p --generate-audio false \
  --out-dir /absolute/path/to/out \
  2>&1 >/dev/null | grep -o '"frame_type":"[a-z_]*"'
```

Measured output on a two-frame job:

```
"frame_type":"first_frame"
"frame_type":"last_frame"
```

Two lines, in that order, is the confirmation. One line means one of the two
flags didn't take; a different order means `--frame-first-image` and
`--frame-last-image` are carrying the wrong paths, which is the same defect as
a backwards clip and is free to fix at this point. Grep the payload rather
than printing it whole: each local frame is base64-inlined into that JSON, so
the body runs to megabytes.

`--out-dir` is worth passing to the dry run for the same reason — the script
creates and enters it here, and a path it can't use fails as exit `6` with
nothing submitted. Pass the **same** directory to the real run; a different
one afterwards re-opens the question the dry run just settled (an exit `6`
after a create costs the job's price, and is recovered with
`poll JOB_ID --out-dir <writable dir>`, never with a second `generate`).

## Several takes to choose from

The middle is generated, so it is a roll. When the user wants options rather
than one clip, `batch` prices the whole set up front, waits on the takes
concurrently, and builds a contact sheet:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 3 \
  --frame-first-image /path/to/A.png --frame-last-image /path/to/B.png \
  --duration 4 --resolution 480p --out-dir /absolute/path/to/out
```

Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`, and give the takes a row
each — the gate wants the itemised shape. If one take in three is usable, that
clip cost the whole total. At `--dry-run` the total is the
`Estimated cost: ~$… for N takes` line; the two `BATCH_COST_*` keys are what
the real run prints afterwards.

Hand the user the `CONTACT_SHEET` path on its own line; in this flow it is the
artifact they look at first. Each `TAKE` line carries `seed=N`, which is how a
take is named and re-submitted at a higher resolution — an aim at that take,
not a promise of it (see the `--seed` row above).

Submission is sequential and only the waiting runs in parallel, so a
submission failure stops the remaining takes — but the whole total is
committed within seconds of the yes. That is a real reduction in
recoverability compared with running takes one at a time, and the cost table
is the only place a batch can be stopped.

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
  (`ofoxai-skills-ofox-video-core`). Re-run the command against what the probe
  printed. Nothing needs installing.
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

Either way, say which skill is missing and where it was expected rather than
relaying the raw path error, which names neither.

A broken link to a shared reference has the same two causes: this skill
packages only its `SKILL.md` and `CHANGELOG.md`, so `prompt-structure.md`,
`creative-brief.md`, `approval-gate.md` and `api-params.md` are out of reach
whenever the script is. The skill still works without them — the template, the
question set and the defaults are written out here; what is unavailable is the
depth behind the rules they reference.

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
low-resolution clip is usually one to three minutes. Say so before starting,
so the wait isn't silent.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) followed by `poll`, instead of `generate`. That way a
timeout can never strand a job whose id you never saw.

## Where the file lands

Always pass `--out-dir`, and **make it an absolute path**. Without it the
script writes to the current working directory — which, given that the
examples here run from this skill's own directory, would drop the user's video
inside an installed skill. Relay the **absolute** `VIDEO_PATH` the script
prints, on its own line.

The dry run is where a bad directory gets caught: `generate --dry-run` (and
`batch --dry-run`) creates and enters `--out-dir` before it quotes, and exits
`6` without submitting anything if it can't. That only covers the directory
you actually passed it, so give the real run the same one — swapping it
afterwards puts you back to discovering the problem after the job is paid for.

Pass `--name` too — you know what the clip is, so name the file after it
rather than leaving the script to guess from the prompt's opening words. The
clip lands as `<name>-<short job id>.mp4` with a `.json` sidecar holding the
full job id, the prompt, the seed and the real cost.

## Generating

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the A-to-B prompt built above>" \
  --name "<short description, e.g. mug slides right>" \
  --frame-first-image "/absolute/path/to/A.png" \
  --frame-last-image  "/absolute/path/to/B.png" \
  --duration 4 \
  --resolution 480p \
  --generate-audio false \
  --out-dir /absolute/path/to/out
```

No `--aspect-ratio` on purpose, on any model — see "The frame decides the
shape".

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
| Exit `1`, no network call made | A flag the model doesn't accept — a duration outside its range, a resolution it doesn't have | Read the error, which names the model's real values, and re-run. Nothing was submitted, so retrying is free |
| Exit `1`, `references_conflict` | `--frame-first-image`/`--frame-last-image` together with an `input_references` array in `--extra-json` | Pick one meaning — locked frames, or identity references — and drop the other. They cannot be combined in one job |
| Exit `3`, `input_moderation_failed` | One of the two frames contains a photoreal person. Refused at submission on `bytedance/seedance-2.5`; nothing billed | Use frames without a photoreal person, or crop them out. If the user is **authorised** to use that likeness, `--real-person true` is the route Ofox provides for it and is measured lifting this refusal on 2.5 — ask first, price it as an experiment (it was measured on a single first frame, not on a two-ended pair), and do not offer it as a way past the check |
| Exit `3`, `insufficient_credits` | Ofox balance too low | No charge was made; add credits at https://app.ofox.ai and retry |
| Exit `3`, job ends `failed` with `output_moderation_failed` | The generated output failed a post-generation check — after the job ran, not at submission. Not billed | Retry as a **brand-new** `generate` with a different prompt or frames. A new request, not a resubmission |
| The clip runs backwards | The two paths were passed on the wrong flags | Swap `--frame-first-image` and `--frame-last-image`. New job, new cost table — which is why `Order` is a must-ask when the input is ambiguous |
| The subject reaches its destination early and then sits there | **Possible, not expected.** Job `259c3ce2` did exactly that (~53% of the distance in the first quarter, arrival at 3 of 4 seconds); job `1b7a3fab` did not (20% at 1s of 5, arrival at 4.5s). Two clips, two different curves | Nothing in the prompt is known to change it, and **nothing predicts which you will get** — so treat the arrival time as a draft question rather than a plannable parameter. Don't write "constant speed"; both clips eased to some degree anyway |
| The output is the frames' shape, not the shape you wanted | Expected: with frames attached the clip follows the frames | Crop both frames to the target shape and generate again — a new job, billed again, which is why the crop happens before the first submission |
| The middle invents something that is in neither frame | The pair was too far apart, so the middle was the model's to fill | Bring the pair closer, or split it into two shorter jobs. See "When the two frames differ too much" — reasoning, not measurement |
| Readable lettering appears mid-clip that is in neither frame | The AVOID list's text items were dropped, or the pair has lettering in only one end | Keep the text items when your frames are text-free. When both frames genuinely carry the same lettering, `product-demo` is the skill with a measured run behind that case |
| Exit `4`, timed out waiting | The job is still running upstream, not failed | Do **not** re-run `generate`; run `poll JOB_ID` with the id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job was created | Don't guess or retry; tell the user to check https://app.ofox.ai for a job that may already be running |
| Exit `6`, `--out-dir` unusable | Local filesystem problem, not an API problem | The job is unaffected — fix the path and `poll JOB_ID --out-dir <writable dir>` rather than regenerating |

## When NOT to use

- **Only one image exists.** Animating a single still is `seedance-ad-creative`
  (cinematic) or `seedance-product-video` (catalog-literal). This skill's whole
  premise is that the destination is supplied.
- **The pair is two states of a user interface** — a settings panel before and
  after a toggle, a dashboard at two values. Use `product-demo`: it is the same
  mechanism, but its measured behaviour and its prompt advice differ, and it
  deliberately does not carry the anti-text line above.
- **The two pictures are unrelated scenes.** Two ends with nothing in common
  is a cut, not an interpolation, and this skill has nothing measured to say
  about it. Two jobs and an editor are cheaper and more predictable.
- **What you have is a sequence, not two ends** — "and then this happens, and
  then this". That is `ofox-video-core`'s `chain`, which carries each clip's
  last frame into the next job's first frame.
