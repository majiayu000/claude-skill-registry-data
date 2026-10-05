---
name: product-demo
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai, plus two real screenshots of one interface in two states. Animates the transition between them as one video — both go into a single Ofox video job, and the model cross-fades the values that changed while the rest of the layout holds. Use when a user wants a short software demo animation out of captures they already have, e.g. "turn these two screenshots into a demo clip", "show the dashboard going from the free plan to the paid one", "animate this settings change for the docs", or "make a clip of the counter going from 3 to 25". Do not use for a pair that is not a user interface (see keyframe-animation), for a screen recording (record it instead), or when only one screenshot exists.
license: MIT
version: "2.0.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/product-demo
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
    emoji: "🖥️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/product-demo
---

# product-demo: one UI state to another, as a video

Two screenshots of the same interface — before and after a state change — go
into one Ofox video job as the first and last frame, and the model animates
the change between them.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns how to capture a
usable pair, the prompt for a UI transition, and the pre-generation cost
estimate; `ofox-video-core` owns talking to the Ofox API correctly and safely
(the `OFOX_API_KEY` handling, the no-resubmit rule, error-code mapping,
download/verification, and reporting the downloaded file's absolute
`VIDEO_PATH`). **Read that skill's safety contract before using this one** —
it is not restated here.

The shared prompt craft is in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md),
the pre-prompt question rules in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md),
and the spend rule in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
This file carries only what is specific to a UI pair.

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
the two captures read, the prompt written and the job priced, and only needs
the key at the moment they say yes to the cost table. Do that work first
rather than opening with a signup link; see "Pricing a job with no API key".

## Why this skill exists, and what it is built on

This scenario was expected to fail. Generative video models fabricate text —
every other scenario skill in this repo carries an `AVOID: subtitles,
on-screen text` line for exactly that reason — and a user interface is almost
entirely text. The prediction was that the interpolated middle would turn the
UI's strings to mush and a demo built this way would be worthless.

**It was tested, and the prediction was wrong.** Job `5e59baa2`,
`bytedance/seedance-2.5`, 4 seconds, 480p, **billed 44 cents**. The inputs
were two genuine Chrome-rendered screenshots of one pricing/usage panel,
differing in four places:

| | First frame | Last frame |
|---|---|---|
| plan name | `Starter` | `Business` |
| price | `$29.00` | `$99.00` |
| seat count | `3` | `25` |
| button label | `Upgrade plan` | `Manage seats` |

What the delivered clip's own frames show:

- at **t=1.3s** the four changed values are **mid-fade** — and already
  **correctly spelled and correctly positioned**;
- the labels that did *not* change stay **solid** through that moment. The
  model cross-faded only the values that differed;
- by **t=2.0s** every string is crisp and correct;
- **no garbling, no invented text, no layout drift.**

**Why the pessimistic reasoning failed, and this is the load-bearing part:**
the repo's `AVOID: on-screen text` lines exist for text the model has to
**invent**. With both endpoints supplied, it is **interpolating between two
given renderings** instead — a different task with a different failure
profile. Copying that AVOID line into this skill would be cargo-culting a rule
whose premise does not hold here, so **this skill does not carry one**; see
"The prompt" below.

### It happened twice

Job `427278b4` (2026-09-15), same model, duration, tier and input pair, again
**44 cents**, with the prompt filled in from this file's own template by an
agent working from this skill and nothing else — so what that run tested was
the skill rather than the API. Read off the delivered clip's final frame: all
four changed values render **correctly and legibly** — `Business`, `$99.00`,
`25`, `Manage seats` — the layout is identical to the input capture, nothing
drifted, and no text was invented.

Same pair, so it widens nothing about the inputs. What it adds is that the
template in this file, not a hand-written prompt, produces the result, and
that the result replicated rather than being one lucky roll — which matters
more here than in most scenarios, because a seed does not reproduce a take on
this API, so a second run really is a second sample.

### What those jobs do not establish

- One pair, one app, one panel, four changed values, at 480p and 4 seconds,
  twice. It is two clips on the same input, not a guarantee, and the second is
  a replication rather than a broadening. Read the draft's frames before
  anyone ships the output.
- Nothing about a pair that differs in **many** places, or in layout rather
  than in values. Every difference has to be resolved in the middle, and this
  run only bounded the easy case.
- Nothing about a model other than `bytedance/seedance-2.5`. The catalog lists
  `i2v` for the current video models, but `i2v` says nothing about locking
  **both** ends at once — that granularity is not in the catalog and has not
  been tested here.
- Nothing about a **pointer or cursor** moving to the control that changed. A
  cursor that is in neither screenshot is an element the model would have to
  invent, which is the class the AVOID lines were written for. Untested, and
  not recommended without a paid run to settle it.
- Nothing about screen recording. If the user can record their real app, that
  is free, exact, and better than any of this.

### The timing, from the sibling scenario — and it is no longer a pattern

⚠️ **This section used to say "it settles early and then holds" was the
pattern to plan for. A second measurement withdrew that**, and the withdrawal
matters more here than the original claim did, because this file borrowed it
from a sibling rather than measuring it.

What the sibling scenario (`keyframe-animation`) has now measured, on the same
two-frame mechanism, sampling the subject's position each second as a fraction
of total travel:

| Elapsed | `259c3ce2` (4s, moving object) | `1b7a3fab` (5s, moving object) |
|---|---|---|
| 1s | ~53% | 20% |
| 2s | ~90% | 51% |
| 3s | arrived | 80% |
| 4.5s | — | arrived |

One clip front-loads and holds for a quarter of its length; the other is
near-linear and holds for about half a second. They differ in duration,
subject, distance and seed all at once, so **neither is the mechanism's
behaviour** — and there is no curve to plan against.

**This scenario's own UI clip is still consistent with an early settle**
(crisp and settled by t=2.0s of a 4-second clip), and that observation is
unchanged. But it was read for legibility rather than sampled for an easing
curve, so it was never evidence for a curve — it was compatible with one, and
"compatible with" is what made borrowing the claim feel safe.

Practical consequence, restated honestly: **plan for the final state to be
reached and to be legible, not for a particular amount of tail.** For a docs
GIF that is usually enough, since the thing being demonstrated is the end
state rather than its timing. If the length of the hold actually matters to
the deliverable, generate a cheap draft and look — there is no clause for it
and no default to quote.

## Before writing the prompt: the brief

The shared rules — the three tiers, one round of at most four questions, the
"Let the AI decide" discipline, the order with the approval gate — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
This section adds only this scenario's question set.

Almost every axis is settled by the two screenshots: the subject, the layout,
the colours, the framing and the output's shape are all in the pair. **Zero
questions is the common case** when both files arrive with names that say
which is which.

| Tier | Product-demo axes |
|---|---|
| **must-ask** | does the second screenshot exist? and, when the input leaves it ambiguous, which state comes **first**. Neither can be guessed: a capture that does not exist cannot be invented, and the wrong order produces a clip that runs backwards and bills the same |
| **ask-if-open** | whether anything should be emphasised during the change, when the request hints at one — and the honest answer is usually "a plain cross-fade", because that is the only behaviour with a run behind it |
| **never-ask** | duration, resolution, model, provider, audio (off by default here). Aspect ratio is not a question at all: with frames attached the clip follows the screenshots. Two durations or two resolutions are **two rows in the cost table** |

### The question set

| # | Tier | `header` | Question | Options (1 = recommended) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Screens` | I need both ends: a capture of the interface before the change and one after it. Do you have the second one? | **Yes — I'll give a local path (recommended)**: both go into one job and the clip lands on both exactly. / **No, I can capture it**: take it now, same window size and same scroll position as the first. / **No, and I can't**: then there is nothing to interpolate towards — a screen recording, or a single-frame clip from another skill, is the honest alternative. **No AI option** — a screenshot of software that was never captured cannot be invented, and a made-up interface is not a demo of yours. | Only one capture is attached and the user did not name a second. |
| 2 | must-ask | `Order` | Which capture is the **starting** state? | the two filenames as the two options. **No AI option.** | Two images arrived and nothing in the names, the paths or the message says which comes first. Skip it whenever the names themselves state an order — `before`/`after`, `a`/`b`, `1`/`2`, `01`/`02`, `old`/`new`, `free`/`paid`, `off`/`on`, `light`/`dark`, two version numbers or two capture timestamps — or the message says so. The list is illustrative: any pair that reads as a sequence to you will read that way to the user. |
| 3 | ask-if-open | `Emphasis` | Should the clip do anything beyond changing the values? | **No — a plain cross-fade of what differs (recommended)**: the only behaviour measured here, and it kept every string legible. / **Yes, describe it**: it goes in the prompt as a beat — **untested**, and anything the model has to add that is in neither capture is exactly the kind of invention this mechanism avoids. I will say so in the cost table. / **Let the AI decide** — which in practice means the first option. | The request hints at a highlight, a pointer, a zoom or a callout. Skip it otherwise. |

Not asked: duration and resolution (rows in the cost table), the model, the
provider, the audio flag, the aspect ratio.

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| filenames that state an order — `before`/`after`, `a`/`b`, `1`/`2`, `01`/`02`, `old`/`new`, `light`/`dark`, `free`/`pro`, `off`/`on`, version numbers, capture timestamps | Order | as named; don't ask. Treat these as examples of the pattern, not as the whole list |
| "from this state to that one", in attachment order | Order | attachment order |
| "for the docs", "for the changelog", "a GIF" | duration | the model's minimum — `ofox-video.sh models` prints each model's range |
| "no music", "silent" | audio | off, which is already the default here |

### From answers to prompt — traceability

| Answer | Lands in |
|---|---|
| Screens: two paths | `--frame-first-image A` and `--frame-last-image B` |
| Order | which path goes on which of those two flags |
| The four (or however many) differences you read off the pair | the CHANGE line, quoted verbatim |
| Emphasis | an extra beat in the prompt, or nothing |
| Duration | `--duration`, and a row in the cost table |

### The recap for this scenario

```
Brief:
- Start state: /Users/me/caps/plan-starter.png (given)
- End state:   /Users/me/caps/plan-business.png (given)
- What differs: plan name, price, seat count, button label — 4 changes
- Emphasis: none, plain cross-fade (the measured behaviour)
- Duration / resolution / audio: 4s / 480p / off — one row below; 720p as a second row
- Frame shape: 1440x900 on both files, so the clip comes out in that shape
```

Then the full prompt, then the cost table, all in one message.

## Capturing the pair

The pair is the whole job. Everything the model is asked to do lives in the
difference between the two files, so a bounded difference is the entire craft
here.

- **Capture both from the real application.** A mockup, a Figma frame or an
  AI-generated "UI" already contains invented text, and then the demo is a
  demo of something that does not exist. The measured job used two genuine
  Chrome-rendered screenshots.
- **Change one thing, or a small bounded set.** The measured pair differed in
  four places, all of them *values* in place. Every difference is resolved in
  the middle of the clip, and you pay for all of them in one job.
- **Same window size, same scroll position, same zoom, same theme.** Resize
  the window once and capture both without touching it. A different scroll
  offset turns "one value changed" into "the whole page moved", which is a
  different and unmeasured problem.
- **Same pixel dimensions on both files.** The measured pair matched. A
  mismatched pair has not been run here; matching them first costs nothing.
  Read the real pixels (`sips -g pixelWidth -g pixelHeight <file>`,
  `identify <file>`) rather than trusting a filename or an export dialog —
  this repo has more than one record of a reported size disagreeing with the
  file actually on disk.
- **Crop to the shape you want the clip in, before generating.** With frames
  attached the output follows the frames — see "The frames decide the shape".
  Crop, never pad: a padded frame makes the bars part of the video.
- **Hide anything you don't want animated for four seconds.** Real customer
  names, real email addresses, a live token in a URL bar. The clip is a
  shareable artifact and the middle frames are generated, so anything private
  in the capture is private in the output too.
- **Crop out a real person's face** if the UI happens to show one — a profile
  picture, a customer photo, a testimonial block.
  `bytedance/seedance-2.5` refuses a photoreal-person reference at submission
  (`input_moderation_failed`, nothing billed) — a documented `ofox-video-core`
  behaviour. Cropping is the right answer nearly every time here, because a
  face is almost never the subject of a UI demo. There is now a measured
  alternative: `--real-person true`, Ofox's privacy-preserving preprocessing
  path for real-person references the user is **authorised** to use, lifted
  that refusal on 2.5 on 2026-09-16. It is an authorisation route for a
  likeness someone holds the right to use, **never a way past the check**, and
  for a headshot sitting in the corner of a screenshot it is a heavier answer
  than a crop. Evidence and limits:
  [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)
  → "`--real-person true` lifts that refusal on 2.5". An avatar illustration is a different case and has
  not been tested here either way.
- **A local file beats a remote URL** when one is available.
  `ofox-video-core` base64-encodes a local readable file into the request; a
  publicly reachable URL has been rejected upstream at least once in this repo.

## The prompt

The prompt's job here is smaller than in any other Seedance scenario: both
endpoints are supplied and the model can see them. It has to name what changed
so the cross-fade lands on the right elements, and say that everything else
holds still.

Vocabulary and the general formula are not repeated here — see
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).
Two things from that file bear on this template: negative clauses are honoured
more reliably than positive ones, and a camera verb on its own tends not to
produce a camera move — which is why the VIEW line below asks the frame to
stay put rather than asking it to travel.

```
SCREEN: the first frame and the last frame are two screenshots of the same <app or page name>, captured at the same window size and the same scroll position. Every element keeps the position, size, typeface, weight and colour it has in those two images.
CHANGE: between them, <element> reads "<value in the first frame>" and becomes "<value in the last frame>"[; <element 2> goes from "<A>" to "<B>"; …]. Those are the only things that change; every other label, number, icon and control stays exactly as it is.
VIEW: the view is locked — the screen is shown flat and straight on, framed exactly as it is in the two screenshots, at the same scale and in the same position. The framing does not move, scale, rotate or tilt at any point, and the page does not scroll.
ENDING: the clip settles on the second screenshot and holds it.
AVOID: a cut, a fade to black, a dissolve of the whole screen, a wipe or a slide transition; camera shake, zoom, pan or reframing; new panels, menus, dialogs, tooltips, toasts or badges appearing; a mouse pointer or cursor appearing; the layout shifting, reflowing or resizing; letters or digits becoming blurred, doubled or malformed.
```

**The VIEW line says "framed exactly as it is in the two screenshots", not
"the interface fills the frame".** Whatever the pair shows — a full window, a
panel with room around it, a cropped detail — is already the framing, and it
is the two attached images that decide it. Telling the model the interface
fills the frame is a description only when it happens to be true; on a capture
with page around the panel it reads as an instruction to re-frame, which means
inventing what sits outside the images it was given. Say what the pair is
framed like, or say nothing about it. If a tighter crop is wanted, crop both
captures before generating, exactly as with the aspect ratio.

**There is deliberately no blanket "no on-screen text" item in that AVOID
list**, and it is the one line not to copy in from the other scenario skills.
Those lines exist for text the model has to invent. Here both endpoints are
supplied, so it is interpolating between two given renderings — the measured
run kept every string correctly spelled and correctly positioned throughout —
and a blanket prohibition on text would be pointed at the user's own
interface. What this list does forbid is text-shaped things that are in
**neither** capture (a tooltip, a toast, a badge) and text that stops being
text (blurred, doubled, malformed glyphs), which are the real failure modes.

### Worked example

The measured pair: one pricing panel, four values changed.

```
SCREEN: the first frame and the last frame are two screenshots of the same pricing and usage panel, captured at the same window size and the same scroll position. Every element keeps the position, size, typeface, weight and colour it has in those two images.
CHANGE: between them, the plan name reads "Starter" and becomes "Business"; the price reads "$29.00" and becomes "$99.00"; the seat count reads "3" and becomes "25"; the button label reads "Upgrade plan" and becomes "Manage seats". Those are the only things that change; every other label, number, icon and control stays exactly as it is.
VIEW: the view is locked — the screen is shown flat and straight on, framed exactly as it is in the two screenshots, at the same scale and in the same position. The framing does not move, scale, rotate or tilt at any point, and the page does not scroll.
ENDING: the clip settles on the second screenshot and holds it.
AVOID: a cut, a fade to black, a dissolve of the whole screen, a wipe or a slide transition; camera shake, zoom, pan or reframing; new panels, menus, dialogs, tooltips, toasts or badges appearing; a mouse pointer or cursor appearing; the layout shifting, reflowing or resizing; letters or digits becoming blurred, doubled or malformed.
```

**Quote the values verbatim, in quotes, exactly as they appear** — including
the currency symbol and the decimals. They are strings that exist in both
captures; retyping them approximately in the prompt is the one way to
introduce a discrepancy into a job that otherwise has none.

### Checking the draft

Read the artifact, not the status. `STATUS completed` says nothing about
legibility. The check that produced the evidence above — run on both jobs — and the one to repeat:

```bash
# the delivered clip's own first and last frames, against the two inputs
ffmpeg -i out.mp4 -frames:v 1 first.png
ffmpeg -sseof -0.1 -i out.mp4 -frames:v 1 last.png
# and the middle, where the cross-fade lives
ffmpeg -ss 1.3 -i out.mp4 -frames:v 1 mid.png
```

Look at three things: are the **changed** values spelled correctly and in the
right place at the mid-point; do the **unchanged** labels stay solid; has
anything moved. If ffmpeg isn't installed, open the file and scrub — the
point is that a human or an agent looks at frames, not that a particular tool
is used.

## The frames decide the shape

With a frame attached, the output's aspect ratio follows the frame, and how it
gets there depends on the model:

- on `bytedance/seedance-2.5`, `ofox-video-core` **forces**
  `aspect_ratio=adaptive` and prints a `NOTE:` saying so, because the API
  requires it for image-to-video on that model. Anything you passed is
  overridden;
- on a model whose catalog entry lists `adaptive`, the script **defaults** to
  it when you pass no `--aspect-ratio`, and keeps your value if you pass one;
- on a model that does not offer `adaptive`, the script sends no ratio and
  says so — the frames' shape may not survive.

So: **don't pass `--aspect-ratio` on this route**, on any model. Crop both
screenshots to the shape you want before generating; that crop is what decides
the output. A browser window is rarely 16:9, and a padded frame bakes the bars
into the video — crop instead. Relay the `NOTE:` the script prints; it names
which branch applied.

This needs `ofox-video-core` 1.22.0 or newer. On an older core, a non-Seedance
model with frames attached sent no ratio at all, with nothing printed to say
so.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--frame-first-image` / `--frame-last-image` | both, in one `generate` call | the mechanism this skill is built on; both measured jobs honoured both ends |
| `--model` | not passed — the script's own default applies, **unless the user named a model**, which always wins | both measured jobs ran on `bytedance/seedance-2.5`; whether both ends can be locked on another model is untested here. `models` lists the models but does **not** mark which one the script defaults to — the `MODEL` line a `generate --dry-run` prints is what names the id that will really be sent, which is also the id the cost table has to carry |
| `--duration` | the model's minimum for a single bounded state change | this scenario's own clip was crisp and settled by t=2.0s of 4 seconds, and every extra second bills. ⚠️ Do **not** justify it as "extra seconds buy hold" — measured on the sibling mechanism, how much tail you get is not predictable (see "The timing, from the sibling scenario"). The reason to stay at the minimum is the bill, not a known curve. `ofox-video.sh models` prints each model's range |
| `--resolution` | the cheapest tier for the draft, then re-render the chosen seed higher. **When the user named neither** — the common case — draft at the model's cheapest tier and put the next tier up as a *second row* of the same cost table, so the upgrade is priced rather than asked about | both measured jobs ran at 480p, the cheapest tier their model lists, and the text stayed legible both times **at that resolution, on that pair** — fine lettering at a small tier is the first thing to check on a draft, and the second row is what the user reaches for when it fails that check. `models` prints the tiers; dry-running both rows costs nothing |
| `--aspect-ratio` | not passed | the attached screenshots decide it — see "The frames decide the shape" |
| `--generate-audio` | `false` | a docs clip has nothing to sync to, and the server's default is `true`. Omit the flag only when the clip genuinely wants a track |
| `--seed` | let the script roll one, and keep it | it prints `SEED` and writes it to the clip's `.json` sidecar, which is what lets "that take, at a higher resolution" be re-submitted at all. It does **not** reproduce it: measured, an identical request on a fixed seed came back a visibly different clip. A byte-identical prompt is necessary and not sufficient — tell the user a re-render is another roll aimed at the same shot before they pay for it |
| `--real-person` | leave unset — crop the face out instead | a photoreal face in a capture is refused at submission on `bytedance/seedance-2.5`, nothing billed. `true` is Ofox's privacy-preserving preprocessing path for **authorised** real-person references and was measured lifting that refusal on 2.5 (2026-09-16), but it is an authorisation route rather than a way past the check, and in a UI capture the face is almost never the point. See [`api-params.md`](../ofox-video-core/references/api-params.md) → "`--real-person true` lifts that refusal on 2.5" |

## Choosing a model

The model stays **never-ask** — the agent doesn't raise it. But never-ask is
not "never listen": if the user names a model, use it.

**Model ids, prices, resolutions, durations and aspect ratios are not written
down in this file on purpose.** They are catalog facts, they change, and this
repo has five recorded defects that trace to a hardcoded copy of somebody
else's value table. Read them live instead, free and with no API key:

```bash
bash ../ofox-video-core/references/ofox-video.sh models      # models, tiers, ranges
bash ../ofox-video-core/references/ofox-video.sh providers   # the price matrix
```

Worth telling the user before they switch: the text-preserving cross-fade was
measured on `bytedance/seedance-2.5` only. The catalog says the current models
do `i2v`, but `i2v` does not distinguish "one end locked" from "both", and it
says nothing at all about what happens to lettering — so another model is an
untested route for the one property this whole scenario depends on.

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the table's required columns and where the numbers come from are
written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

Get the numbers from `--dry-run`, which validates everything and prints the
estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." \
  --frame-first-image /path/to/before.png \
  --frame-last-image  /path/to/after.png \
  --duration 4 --resolution 480p --generate-audio false \
  --out-dir /absolute/path/to/out
```

Relay the `Estimated cost:` line it prints — never a number of your own — then
wait for a yes, then re-run the identical command with `--dry-run` swapped for
`--approved`. The estimate a *real* run prints comes microseconds before the
request goes out, too late to relay.

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
billed** — twice, on jobs `5e59baa2` and `427278b4`, at the same figure. It is
not a quote for any other combination — an image-to-video job bills at the
text-to-video tier, so a longer or higher clip scales from the dry run, never
from this number.

Afterwards the **actual** bill is `VIDEO_COST` from the finished job. Report
it as money, not as the raw ten-decimal string.

Worth saying out loud when the user is deciding: **a screen recording of the
real app costs nothing and is exact.** This skill earns its keep when there is
no running app to record — a design that isn't built, a state that is hard to
reach, a before/after across two releases — or when a clean animated
transition is wanted from captures that already exist.

### Confirm both captures are attached, before the money moves

The dry run's own output names the model, the duration and the resolution and
says **nothing about the frames** — so a mistyped flag, or a path that quietly
matched only one file, reads as a perfectly healthy quote and shows up in the
delivered clip instead. `--print-payload` closes that: it dumps the request
body on stderr *before* the dry run stops (the API key travels in a header,
never in the body), and the two `frame_type` entries are the part to read:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run --print-payload \
  --prompt "..." \
  --frame-first-image /path/to/before.png \
  --frame-last-image  /path/to/after.png \
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
flags didn't take; a different order means the before/after captures are on
the wrong flags, which is the backwards-clip failure below and is free to fix
at this point. Grep the payload rather than printing it whole: each capture is
base64-inlined into that JSON, so the body runs to megabytes.

`--out-dir` is worth passing to the dry run for the same reason — the script
creates and enters it here, and a path it can't use fails as exit `6` with
nothing submitted. Pass the **same** directory to the real run; a different
one afterwards re-opens the question the dry run just settled (an exit `6`
after a create costs the job's price, and is recovered with
`poll JOB_ID --out-dir <writable dir>`, never with a second `generate`).

## Several takes to choose from

The middle is generated, so it is a roll — and legibility is the thing being
rolled for. When the user wants options, `batch` prices the whole set up
front, waits on the takes concurrently, and builds a contact sheet:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 3 \
  --frame-first-image /path/to/before.png --frame-last-image /path/to/after.png \
  --duration 4 --resolution 480p --out-dir /absolute/path/to/out
```

Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`, and give the takes a row
each. If one take in three is usable, that clip cost the whole total. At
`--dry-run` the total is the `Estimated cost: ~$… for N takes` line; the two
`BATCH_COST_*` keys are what the real run prints afterwards.

The contact sheet is three frames per take at thumbnail size, so it is good
for "did the layout hold" and **not** good enough for "is the text correct" —
open the individual takes for that. Hand the user the `CONTACT_SHEET` path on
its own line, then the take paths beneath it. Each `TAKE` line carries
`seed=N`, which is how a take is named and re-submitted higher — an aim at
that take, not a promise of it (see the `--seed` row above).

Submission is sequential and only the waiting runs in parallel, so the whole
total is committed within seconds of the yes — the cost table is the only
place a batch can be stopped.

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
question set and the defaults are written out here.

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

Pass `--name` too — name the file after the state change rather than leaving
the script to guess from the prompt's opening words, which here describe a
window size. The clip lands as `<name>-<short job id>.mp4` with a `.json`
sidecar holding the full job id, the prompt, the seed and the real cost.

## Generating

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the UI-transition prompt built above>" \
  --name "<short description, e.g. plan upgrade starter to business>" \
  --frame-first-image "/absolute/path/to/before.png" \
  --frame-last-image  "/absolute/path/to/after.png" \
  --duration 4 \
  --resolution 480p \
  --generate-audio false \
  --out-dir /absolute/path/to/out
```

No `--aspect-ratio` on purpose, on any model — see "The frames decide the
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
| Exit `3`, `input_moderation_failed` | A capture contains a photoreal face. Refused at submission on `bytedance/seedance-2.5`; nothing billed | Crop or blur the face and retry — free, and almost always the right answer for a UI demo. `--real-person true` is Ofox's measured route for a likeness the user is **authorised** to use; ask before reaching for it, and don't offer it as a way past the check |
| Exit `3`, `insufficient_credits` | Ofox balance too low | No charge was made; add credits at https://app.ofox.ai and retry |
| Exit `3`, job ends `failed` with `output_moderation_failed` | The generated output failed a post-generation check — after the job ran, not at submission. Not billed | Retry as a **brand-new** `generate` with a different prompt or captures. A new request, not a resubmission |
| The clip runs backwards | The two paths were passed on the wrong flags | Swap `--frame-first-image` and `--frame-last-image`. New job, new cost table — which is why `Order` is a must-ask when the input is ambiguous |
| Text that should not have changed goes soft or doubles mid-clip | The measured runs kept unchanged labels solid on **one** pair at 480p, twice. Fine lettering, a denser layout or a lower tier are all outside that run | Re-render at the next resolution tier and compare the same mid-frame; if it persists, reduce how much differs between the two captures. New job, new cost table |
| A changed value is spelled wrong mid-fade | Outside what was measured — on job `5e59baa2` the mid-fade values were already correct, and on `427278b4` the final-frame values were | Check the prompt's CHANGE line quotes both values **verbatim** first; a typo there is the cheapest possible cause. Then re-roll, or cut the number of simultaneous changes |
| The layout drifts, reflows or scrolls | The two captures were not taken at the same window size, zoom or scroll position | Re-capture both without touching the window between them. The pair, not the prompt, is what holds the layout |
| A tooltip, toast, badge or cursor appears that is in neither capture | The model filled the middle with something plausible | Keep those items in the AVOID list (they are in the template), and re-roll. Elements that exist in neither endpoint are the one thing this mechanism is not doing for you |
| The output is the captures' shape, not the shape you wanted | Expected: with frames attached the clip follows the frames | Crop both captures to the target shape and generate again — a new job, billed again, which is why the crop happens before the first submission |
| Black bars are baked into the video | The captures were **padded** to a target ratio instead of cropped | Crop, re-run. Padding makes the bars part of the picture the model was handed |
| Exit `4`, timed out waiting | The job is still running upstream, not failed | Do **not** re-run `generate`; run `poll JOB_ID` with the id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job was created | Don't guess or retry; tell the user to check https://app.ofox.ai for a job that may already be running |
| Exit `6`, `--out-dir` unusable | Local filesystem problem, not an API problem | The job is unaffected — fix the path and `poll JOB_ID --out-dir <writable dir>` rather than regenerating |

## When NOT to use

- **The real app can be recorded.** A screen recording is free, exact, and
  shows the actual interaction. Say so before quoting a job — this skill is
  for when there is nothing to record.
- **Only one screenshot exists.** There is no destination to interpolate
  towards. Capture the second state, or record instead.
- **The pair is not a user interface.** A moving object, a product, a scene —
  that is `keyframe-animation`, the same mechanism with different prompt
  advice and its own measured behaviour.
- **The two captures are different screens entirely**, not two states of one.
  Every difference is resolved in the middle, and a whole-screen replacement
  is a cut — two clips and an editor are cheaper and more predictable.
- **The demo needs a pointer, a click, a typed input or a multi-step flow.**
  Those are elements and events that exist in neither endpoint, and none of it
  has been tested here. A screen recording, or one job per state change joined
  in an editor, is the route with a floor under it.
- **The interface is a mockup rather than the product.** Then the clip is a
  demo of something that does not exist, whatever it looks like.
