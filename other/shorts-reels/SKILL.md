---
name: shorts-reels
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Generate cheap vertical 9:16 drafts in one priced batch, pick a winner off the contact sheet, then re-render only that one. The cheap tier is the point — several times cheaper per second, so a whole set can cost less than one flagship clip. Use when a user wants Shorts/Reels/TikTok raw material rather than one finished video, e.g. "give me 5 vertical clips to choose from", "a few Reels drafts for this product", "some cheap options before we commit", or "batch me some 9:16 takes". Do not use when one finished clip is wanted — go straight to the scenario skill (seedance-ad-creative, ugc-ads, seedance-short-drama, seedance-product-video), which is also where this skill gets the prompt it drafts.
license: MIT
version: "2.0.1"
homepage: https://github.com/ofoxai/skills/tree/main/skills/shorts-reels
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
    emoji: "🎥"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/shorts-reels
---

# shorts-reels: several cheap vertical drafts, then promote the winner

Short-form social wants options, not one perfect clip. This skill turns "give
me five vertical clips" into a priced batch on the catalog's cheap tier, a
contact sheet to pick from, and a single re-render of whichever one earned it.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the vertical format,
the draft-then-promote ladder and the batch economics; `ofox-video-core` owns
talking to the Ofox API correctly and safely (the `OFOX_API_KEY` handling, the
no-resubmit rule, error-code mapping, download/verification, the contact sheet,
and reporting absolute paths). **Read that skill's safety contract before using
this one** — it is not restated here.

The spend rule is in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md),
the pre-prompt question rules in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md),
and the prompt craft in
[`../ofox-video-core/references/prompt-structure.md`](../ofox-video-core/references/prompt-structure.md).

## What this skill does not own: the prompt

**Nothing here writes a prompt.** A vertical draft is still a clip of
something, and the craft for that belongs to whichever scenario fits:

| The clips are… | Write the prompt with |
|---|---|
| a handheld, phone-shot, deliberately unpolished creator clip | [`ugc-ads`](../ugc-ads/SKILL.md) |
| a polished brand or product ad | [`seedance-ad-creative`](../seedance-ad-creative/SKILL.md) |
| people talking, a scene with dialogue | [`seedance-short-drama`](../seedance-short-drama/SKILL.md) |
| plain product/catalog footage | [`seedance-product-video`](../seedance-product-video/SKILL.md) |
| anime or manga-styled | [`seedance-anime-drama`](../seedance-anime-drama/SKILL.md) |
| ambient / mood b-roll — no product, no people, no beat: rain on a window, steam off a cup, a city at dusk | **no scenario skill owns this.** Go straight to the shared craft: [`prompt-structure.md`](../ofox-video-core/references/prompt-structure.md) → `The vendor's own formula (ByteDance first-party)` for the four-sentence template, `Style anchor — the texture layer` for the look, `Camera language` for the move |

Write it there, run the set through here. The two things this skill adds on
top are **vertical** and **cheap enough to throw most of them away** — and
that second one is the whole reason it exists separately.

### When the user brings several reference images

Keep this skill's batching and vertical defaults, but build the prompt and
`input_references` payload from the shared
[`Identity-reference recipe — the authoritative copy`](../ofox-video-core/references/prompt-structure.md#identity-reference-recipe--the-authoritative-copy).
This is the route for gallery-shaped Shorts such as cases 29 and 70. Do not
copy the recipe here: its measured boundary is two images, the API ceiling is
nine, and the array order—not a creative tag spelling—binds `@image1`,
`@image2`, and later labels. Every asset needs a “supplies / ignore” role
sentence. If a source example has more than nine images, it is not directly
reproducible as one Ofox job.

⚠️ **Do not reach for the ad template just because b-roll isn't in the list
above.** An atmosphere clip borrowed from `seedance-ad-creative`'s skeleton
arrives with a hook, a showcase and a hero freeze bolted onto something that
has no product to show — the shared formula is the right starting point
precisely because it is scenario-neutral. Two things carry a subject-less clip
and they are both in that file: one continuous camera move with its waypoints
written out, and a texture line specific enough to rule out the model's
default look.

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

## First: "five clips" means two different things

Settle this before anything else, because the two routes are different
commands, different costs and different outputs.

| What the user means | Route | What they get |
|---|---|---|
| **Five takes of one idea** — same prompt, five rolls, keep the best | `batch --takes 5` | one estimate up front, one contact sheet, five takes each with its own seed, and a stop on the first rejected create |
| **Five different clips** — five ideas, one each | five `create` calls, then **one** `poll` with all five job ids | five independent clips, each with its own prompt and its own bill, waited for together rather than one after another |

"Give me 5 vertical Shorts" is genuinely ambiguous between them. **Ask.** A
batch of the wrong kind is money spent on the wrong shape of output, and no
amount of prompt quality recovers it.

The second route is `ofox-video-core`'s
`Waiting in parallel` → `Across clips: parallelise, always`. Submit each idea
with `create` (returns a job id in seconds), then poll them all at once:

```bash
bash ../ofox-video-core/references/ofox-video.sh create --approved \
  --prompt "<idea A>" \
  --duration 4 --resolution 480p --aspect-ratio 9:16 \
  --name "idea a" --out-dir /absolute/path/to/out
# ...one create per idea, each printing its own JOB_ID...

bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID_A JOB_ID_B JOB_ID_C \
  --out-dir /absolute/path/to/out
```

`create` spends, so it carries `--approved` and refuses without it; `poll` does
not and is never gated — it is how jobs you have already paid for get
collected. Price the whole set with `generate --dry-run` per idea *before* the
first `create`, because five creates commit five bills within seconds of each
other. See "Drafting" for what that flag is and is not.

Each job's output is replayed under a `=== JOB i/N <id> ===` delimiter in the
order the ids were given, and `POLL_COST_TOTAL` sums the real bills. Five
different clips still need five prompts written properly by the scenario
skill above — five variations of one sentence is a batch wearing a disguise.

A mixed case is common and fine: batch the one idea that is worth several
rolls, and `create` the others.

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

If it fails, follow `ofox-video-core`'s guidance (install `curl`/`jq`, or get
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the conversation,
and don't re-run this check on every subsequent request once it has passed.

A failing `check` is not a stop sign: `models`, `providers` and the `--dry-run`
forms all work without a key, which means the entire ladder below can be
priced and shown to a user who hasn't signed up yet.

## The cheap tier is the point

A set of drafts is only worth making if the set costs about what the clip it
is choosing between costs. On this catalog it costs less: the cheapest video
tier runs **several times cheaper per second** than the flagship, so a whole
set of short drafts can land under the price of one flagship clip of the same
length. That gap is what turns "generate five and keep one" from extravagant
into obvious, and it is the reason this skill exists separately from the
scenario skills.

**There is no price table in this file, and that is deliberate.** Prices are
catalog facts, they move, and this repo has recorded defects that trace to a
hardcoded copy of somebody else's value table. Two further reasons specific to
this skill:

- **Which model is cheapest is not a fixed answer.** It depends on the
  resolution tier, and the cheapest tier differs between models that are
  otherwise similar.
- **A model's price can differ between its own upstreams.** At least one video
  model in this catalog is priced differently on its two upstream providers,
  so even "model X costs Y" is underspecified without naming the provider.
  `providers MODEL` prints that model's full matrix, upstream by upstream.

So price it, don't quote it. Read the numbers live, free, with no API key —
in that order, because they answer different halves of the question:

```bash
# 1. shortlist: every model, its rate AT ITS OWN DEFAULT resolution, plus
#    the resolutions, durations and modes it offers
bash ../ofox-video-core/references/ofox-video.sh models

# 2. then, for each candidate, its per-resolution/per-upstream rates
bash ../ofox-video-core/references/ofox-video.sh providers MODEL
```

⚠️ **`providers` with no model argument does not print the catalog.** It
defaults to the flagship and prints that one model's matrix — the opposite of
what this skill is looking for. Always pass the candidate's id.

And the rate `models` shows is **the one at that model's own default
resolution**, which is not the same tier for every model. A model can rank
worse in that column and still be the cheapest at the tier you are actually
drafting on, so shortlist on it and settle it with `providers MODEL` — the
rate you quote has to be the one for the resolution you are about to send.

### The comparison to actually put in front of the user

Two dry runs, the draft set and the single flagship clip, side by side. This
is reproducible, current, and costs nothing:

```bash
# the draft set, on the cheap model
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 5 --model <cheap model id> \
  --duration 4 --resolution 480p --aspect-ratio 9:16 \
  --out-dir /absolute/path/to/out

# one clip on the flagship, for comparison
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 4 --resolution 480p --aspect-ratio 9:16 \
  --out-dir /absolute/path/to/out
```

Show both `Estimated cost:` lines as they print. That is the argument for
drafting, made in numbers the user can re-check, and it stays true when the
catalog changes.

**Pick the cheap model from `models`/`providers`, not from memory.** The
filters that matter: the cheapest `$/s` row, whose model also offers **9:16**
and a duration range that covers the clip. Those lists are shorter on the
budget models than on the flagship, so check rather than assume — and note
that a ratio or duration the model doesn't have is rejected locally, free,
before anything is submitted.

⚠️ **If a plan or a colleague asks for "Seedance 2.5 Fast", it does not
exist.** There is no such id in the catalog; the cheap tier is a different
model family. `models` is the authoritative list, and it takes one second to
read.

### The two measured cost anchors, with their parameters

Both on `bytedance/seedance-2.0-mini` at 480p and 4 seconds, and both billed
**8 cents a take, exactly matching the estimate**, with the contact sheet
rendered:

| Run | Takes | Billed | What it establishes |
|---|---|---|---|
| `ofox-video-core`'s batch verification | 3 | 24 cents total | the *mechanism* — the estimate matches the bill, and a batch's total is the total |
| this scenario's own run (2026-09-15) | 5 | 40 cents total, `BATCH_COST_TOTAL 0.40` | the same thing at a second take count, through this skill's own flow, plus the two checks below |

The scenario run was driven by an agent working from this file, so what it
tested was the skill rather than the API. Two things were checked on the
artifacts rather than on the job statuses:

- **all 5 takes completed, each carrying its own distinct `seed`** —
  `432922460`, `264334079`, `809870386`, `465992541`, `213135543` — and the
  contact sheet was produced;
- **the five takes are visibly different variations of one idea**, which is
  the only thing that makes a batch a selection artifact rather than five
  bills for one clip. That is what the spend buys, and it was confirmed by
  looking at the sheet.

Neither anchor is a quote for any other model, resolution, duration or take
count, and 8 cents a take is a per-second rate multiplied by 4, not a fixed
price. Every number you show a user still comes from a dry run made with the
parameters you are actually about to send.

## Before drafting: the brief

The shared rules — the three tiers, one round of at most four questions, the
"Let the AI decide" discipline, the order with the approval gate — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
This section adds only this scenario's question set.

| Tier | shorts-reels axes |
|---|---|
| **must-ask** | takes of one idea or several different ideas (see "First: 'five clips' means two different things"), and what the clips are actually of if the request doesn't say |
| **ask-if-open** | how many, and whether the winner gets re-rendered properly afterwards |
| **never-ask** | aspect ratio (9:16 is this skill's name), the draft resolution and the draft model (the cheap tier is the default — name it in the recap), the provider, the audio flag. The promotion's model and resolution are **rows in the second cost table**, not questions |

### The question set

| # | Tier | `header` | Question | Options (1 = recommended, last = delegation) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Set` | Five takes of one idea, or five different clips? | **Several takes of one idea (recommended when you're chasing one good clip)**: same prompt, different rolls, one contact sheet to pick from, one estimate. / **Different clips, one each**: separate prompts, submitted together and waited for together; each is its own bill. / **A mix**: say which ideas deserve several rolls. **No AI option** — this is what the user is buying, not a taste. | Always, unless the request already says ("five variations of this", "five different hooks"). |
| 2 | must-ask | `Content` | What are the clips of? | free text — and route the answer to the right scenario skill for the prompt itself (see "What this skill does not own"). **No AI option** when nothing at all was given. | The request names a count and a format but no subject. |
| 3 | ask-if-open | `Takes` | How many? | **3 (recommended)**: enough to see variance without paying for a crowd. / **5**: the usual ask for a social batch. / **a number up to 10**: the per-run cap. / **Let the AI decide** — 3. Every extra take is one more bill, linearly. | The user said "a few" or "some" rather than a number. |
| 4 | ask-if-open | `Promote` | After you pick one, re-render that one properly? | **Yes — a second, separately approved job (recommended)**: the drafts are for choosing; the keeper gets the better model or the higher tier. / **No — a draft is the deliverable**: legitimate for internal review or a quick test. / **Let the AI decide** — yes, priced as a second table when it happens, not now. | The user hasn't said what the drafts are for. |

Not asked: aspect ratio, the draft model and tier, the provider, the audio
flag, `--concurrency`.

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| "variations", "versions", "takes", "options of this" | Set | takes of one idea |
| "different hooks", "different angles", "one for each product" | Set | different clips — `create` + `poll` |
| a number ("5 clips", "a dozen") | Takes | that number, capped at 10 per run; say so if they asked for more |
| "for testing", "to see what it looks like", "internal" | Promote | no — a draft is the deliverable |
| "for the campaign", "we're publishing these" | Promote | yes, and say the promotion is a second approval |
| "TikTok", "Reels", "Shorts", "vertical" | Aspect | 9:16, already the default |

### The recap for this scenario

```
Brief:
- Set: 5 takes of one idea (you chose)
- Content: hands-only unboxing of the ceramic kettle — prompt written with ugc-ads
- Takes: 5, vertical 9:16, 4s, cheapest tier (this skill's default)
- Promote: yes — the keeper gets its own cost table afterwards, not now
```

Then the prompt, then the cost table, all in one message.

## Drafting

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "<the prompt written with the scenario skill>" \
  --takes 5 \
  --model <the cheap model id you read from models/providers> \
  --duration 4 --resolution 480p --aspect-ratio 9:16 \
  --max-wait 240 \
  --name "<what the clip is>" \
  --out-dir /absolute/path/to/out
```

Then, after a yes, the identical command with `--dry-run` swapped for
`--approved`.

`--approved` is where that yes gets typed out. Since `ofox-video-core` 2.0.0
the four billable subcommands — `generate`, `create`, `batch`, `chain` —
refuse to run without it, while `--dry-run` never needs it, so the quote above
is still free and still works with no API key. Be exact about what the flag
does: it records a stance, it cannot prove one. Nothing in a shell script can
observe the conversation you had, and it can be typed without showing anyone a
price. What it changes is that spending without quoting is no longer the
default — it has to be written into the command, where a transcript shows it.
A batch is where that matters most: it commits all five bills at once, so the
cost table is the only place the set can still be stopped. The rule is still
the rule, and it is still yours to follow.

What comes back, and what to do with each part:

- **`CONTACT_SHEET`** — three frames per take (first, middle, last), tiled one
  row per take. Hand this path over **on its own line**, before the individual
  clips: in this flow it is the artifact the user actually looks at first,
  because it is how they pick. It needs `ffmpeg`; without it the sheet is
  skipped with a reason and the videos are untouched.
- **`TAKE N <job-id> seed=<n> <cost> <path>`** — one per take. List the paths
  beneath the sheet. **The seed is how a take gets named and re-submitted** —
  not a guarantee of getting it back; see "Picking, and promoting the winner".
- **`BATCH_COST_TOTAL`** — the real total, built from each job's own usage.
  This is the number to report, never `BATCH_COST_PER_TAKE`.

### What a batch does that N separate runs don't

- **It stops on the first rejected create.** Takes are submitted one at a
  time, so if take 2 is rejected, takes 3..N are never sent. Whatever broke it
  would almost certainly break the rest, and each attempt is real money. Takes
  already submitted are still waited for and downloaded — they are billable
  whether or not you collect them.
- **A take that fails *after* submission doesn't stop the others.** It is
  reported as `TAKE 2 <id> seed=<n> FAILED exit=3`, keeping its number, id and
  seed. A job that ends `failed` carries no usage and is not billed.
- **`STATUS batch_partial`** replaces `batch_completed` whenever the run is not
  what was asked for, alongside `TAKES_SUBMITTED`, `TAKES_COMPLETED`,
  `TAKES_FAILED`, `TAKES_RUNNING` and `TAKES_NOT_SUBMITTED`. **Don't report a
  partial run as a complete one** — say how many landed and what happened to
  the rest.
- **It waits for the takes concurrently** (`--concurrency`, default 4), so
  five drafts take roughly one draft's wall clock rather than five.

### Duration, and why drafts should be short

Every second bills, on every take, so duration is the multiplier that hurts
most in a batch: doubling the length doubles the whole set. Draft at the
model's minimum unless the thing being judged needs longer — and read
`ofox-video.sh models` for what that minimum is, since it differs by model.

If the final clip has to be longer, the draft still answers most of the
question: framing, look, whether the idea works at all. What a short draft
can't tell you is how the back half plays.

### Timeouts

`batch` blocks while it polls. Concurrency means five takes finish in about
the time of one, but "one" is still minutes. If your tool call can't stay open
that long, lower `--max-wait` (a 4-second draft rarely needs the 540s default;
240 is generous), or `create` each take and poll them yourself. `batch` also
prints its own resume command once the takes are submitted — use that, never a
second `batch`.

## Picking, and promoting the winner

The contact sheet answers **composition, look, and whether the beat happened**.
It is three thumbnails per take, so it does **not** answer fine detail,
legibility, or anything that moves between the sampled frames — open the
individual take for that. Sampling more frames from one take costs nothing:

```bash
bash ../ofox-video-core/references/ofox-video.sh contact-sheet <take-3.mp4> \
  --out-dir /absolute/path/to/out
```

### Promoting a take is another roll, aimed at that take

Each take differs from its siblings only by seed, and the seed is printed and
written into the clip's `.json` sidecar — which is what makes "take 3" a thing
you can name and re-submit at all. It is **not** a promise that take 3 comes
back. To aim at it:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --prompt "<the identical prompt, read back from the sidecar>" \
  --seed SEED --model MODEL --resolution RES \
  --duration 4 --aspect-ratio 9:16 --name "..." \
  --out-dir /absolute/path/to/out
```

`SEED` is the winning take's own seed off its `TAKE` line or sidecar; `MODEL`
and `RES` are whatever the promotion steps up to — change one of them, not
both, if you want the result to stay recognisable.

**A promotion is a second purchase and gets its own table.** Dry-run it at the
promotion's model and resolution, show that row, and only then add
`--approved` — which is exactly what the flag is for here: the batch's yes was
a yes to five cheap drafts, not to this. The contact-sheet command above is
local ffmpeg and stays free and ungated.

Four honest boundaries on that, all of them cheap to respect:

- **A promotion can come back different even when you change nothing but the
  resolution.** Measured in this repo: three submissions of one byte-identical
  request on a fixed seed returned two visibly different clips (the subject in
  a different position, at 13x the pixel area) and one outright failure. A
  fixed seed does not make this API reproducible. **Say this before the
  promotion is paid for** — a user who was promised "the same clip, bigger"
  and got a different one has been mis-sold by the agent, not by the API.
- **The prompt must still be byte-identical.** Necessary, just not sufficient.
  Measured separately: two jobs with the same seed, model and parameters,
  differing only in the wording of one paragraph, came back with visibly
  *different subjects*. Read the prompt back out of the sidecar rather than
  retyping it — `jq -r '.request.prompt' <sidecar>.json`. A retyped prompt is
  a new prompt, and gives up the one condition that does matter.
- **So the seed is not a handle for "that one, but fix the third beat."** Edit
  the prompt and the seed preserves nothing you liked. That is a new draft
  round, not a promotion.
- **Across models it is further still from the same clip.** A different model
  is a different look by construction, and nothing in this repo has measured a
  seed carrying a take across two models. A resolution bump remains the
  closest-aimed promotion available — closest, not guaranteed.

When a user genuinely needs *this exact file* larger, the honest answer is
that this API does not offer that, and an upscale of the take you already have
is a different tool. Promote when the idea is what you are buying again.

### When to step up to a dearer model, and when not to

This is the decision the whole ladder exists to make, and the useful split is
**why the draft was rejected**, not how much the user likes it.

**Step up when the draft is right and only its fidelity is wrong:**

- the idea, framing and motion are what was wanted, and the picture is just
  soft, noisy or small;
- fine detail has to survive — a product's label, a face at distance, text
  that was locked in an attached frame;
- the clip is going to be published, where the cheap tier's ceiling is visible
  next to whatever it sits beside;
- the final clip needs to be **longer or larger than the cheap model can
  do** — budget models cap duration and resolution lower, which is a hard
  constraint rather than a quality opinion. `models` prints each one's range.

**Do not step up when the draft failed on content or structure:**

- the beat didn't happen, the camera didn't move, the product didn't appear —
  a dearer model renders the same wrong idea more expensively. Fix the prompt
  and draft again cheaply. The repo's measured failures of this kind (a camera
  move that never happened, a payoff that never landed) were prompt problems,
  not model problems;
- every take was wrong the same way — that is the prompt, and a new model
  won't read it differently;
- nobody has looked at the frames yet. `STATUS completed` is not a review.

**And one thing that is not a reason either way:** a cheaper model is not a
worse model at everything — moderation policy is per-model in this catalog,
and a prompt refused on one has been accepted on another. If the blocker is a
refusal rather than a look, changing model is a route, not a downgrade.

## Vertical: check the model has it

`--aspect-ratio 9:16` is this skill's default, on pure text-to-video.

- **Aspect-ratio lists differ per model**, and the budget models' lists are
  shorter. Read `ofox-video.sh models` before picking the draft model. A ratio
  the model doesn't offer is rejected locally, exit `1`, nothing submitted and
  nothing billed.
- **With a frame attached the flag stops being yours.** `ofox-video-core`
  forces `adaptive` on `bytedance/seedance-2.5` and defaults to it on other
  models that offer it, so the output follows the image. **Crop the image to
  9:16 before generating — crop, never pad**, since padding bakes the bars
  into the video. Relay the `NOTE:` the script prints.
- **The promotion must keep the same shape as the draft.** Passing a different
  ratio on the re-render is a different frame, which is a different clip.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--aspect-ratio` | `9:16`; **not passed** when a frame is attached | the format this skill is for; with a frame attached the crop decides |
| `--takes` | 3 when the user said "a few"; their number otherwise | enough to show variance; every take is one more bill, and the per-run cap is 10 |
| `--model` (drafts) | the cheapest tier that offers 9:16 and the duration needed, read from `models`/`providers` — **unless the user named a model**, which always wins | the whole economic case for drafting. Never silently substitute a model the user asked for |
| `--resolution` (drafts) | the draft model's cheapest tier | you are judging the idea, not the pixels. `models` prints the tiers |
| `--duration` (drafts) | the model's minimum unless the thing being judged needs longer | duration multiplies across every take |
| `--max-wait` | lower than the 540s default for short drafts — 240 is generous | keeps a batch inside a single tool call |
| `--concurrency` | leave at 4 | the default is derived from the account's measured rate limit; the ceiling is 10 and it is the whole limit |
| `--seed` | **do not pass it to a batch** | it removes the one axis a batch varies on purpose — every take then asks for the same generation, and you are billed for each. They may still come back different, because a fixed seed does not make this API reproducible (measured), but that variation is the server's rather than one you chose, so you have paid N times for nothing you can steer. The script warns. Seeds are an *output* here, not an input |
| `--name` | always | takes land as `<name>-<short job id>.mp4`, which is what makes a contact sheet legible later |
| `--generate-audio` | leave at the server default unless the scenario skill says otherwise | short-form is usually watched muted, but the track costs nothing extra |

## Before you spend: the approval gate

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule, the required columns and where the numbers must come from are
written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).
Its `Batches get an itemised table, not one total` section is the one that
governs this skill.

Three things this scenario has to get right:

1. **Quote `BATCH_COST_TOTAL`, itemised by take** — never
   `BATCH_COST_PER_TAKE`. Gacha means most takes go in the bin: if one take in
   five is usable, that clip cost the whole total. At `--dry-run` the total is
   the `Estimated cost: ~$… for N takes` line.
2. **The whole batch commits at the yes.** Submission takes seconds and the
   takes are waited for together, so the bills arrive at once. The cost table
   is the only place a batch can be stopped.
3. **A promotion is a second approval, with its own table.** Two-phase flows
   are covered in the gate's `Two-phase flows: two approvals`. Don't roll the
   promotion's price into the draft round's table as though it were decided —
   which of the takes wins isn't known yet, and neither is whether any of them
   do.

Afterwards the **actual** bill is `BATCH_COST_TOTAL` (or `VIDEO_COST` for the
promotion), read from the jobs' own usage. Report it as money, not as a raw
ten-decimal string, and state how many takes it covers.

## Pricing a job with no API key

`models`, `providers`, `generate --dry-run` and `batch --dry-run` all work
with `OFOX_API_KEY` unset. So a user who hasn't signed up can see the entire
ladder priced — the draft set, the flagship comparison, the promotion — before
deciding whether to register. **Quote it first; don't open with a signup
link.**

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

The same two causes explain a broken link to a shared reference, or to a
sibling scenario skill: this skill packages only its `SKILL.md` and
`CHANGELOG.md`. The ladder, the question set and the defaults are all written
out here, so nothing in this file becomes unusable — what is lost is the
prompt craft, which lives in the scenario skills, and the gate's precise
wording, which is still required before spending.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md).
The ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely — a ratio or duration the model doesn't offer lands here |
| `2` | Environment problem — `curl`/`jq` missing, or no `OFOX_API_KEY` | Ask the user to fix it; `check` reports the same |
| `3` | API rejected it, or a job ended failed/cancelled/expired | Read the mapped message; a rejected create was not billed |
| `4` | Timed out waiting — **the jobs are still running and billable** | Use the resume command `batch` printed, or `poll` the ids. Never re-run `batch` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after the creates, `poll` the ids into a writable directory |

⚠️ **A batch collapses several jobs' outcomes into one exit code.** Read the
`TAKES_*` counters and the per-take lines rather than the exit code alone.

## Where the files land

Always pass `--out-dir`, and **make it an absolute path**. Without it the
script writes to the current working directory — which, given that the
examples here run from this skill's own directory, would drop a user's whole
batch inside an installed skill. Relay the **absolute** paths the script
prints: the `CONTACT_SHEET` first, on its own line, then the takes.

Pass the same `--out-dir` to the dry run and the real run: the dry run creates
and enters it, so a bad path fails as exit `6` with nothing submitted.

Each take lands as `<name>-<short job id>.mp4` with a `.json` sidecar holding
the full job id, the prompt, the seed and the real cost. That sidecar is what
the promotion reads its prompt back out of.

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| The user wanted five different clips and got five near-identical ones | `batch` rolls one prompt N times | That is the `Set` question. Write one prompt per idea and use `create` + a single multi-id `poll` — see "First: 'five clips' means two different things". The spent batch is not recoverable |
| All five takes look the same | The prompt leaves almost nothing to vary. (A `--seed` passed to the batch makes every take ask for the same generation — it is not *why* they matched, since a fixed seed does not guarantee identical output, but it does mean you paid five times for one request) | Loosen the prompt, or accept that this idea has one look. And don't pass `--seed` to `batch` (the script warns) |
| `STATUS batch_partial` | A create was rejected, or a take failed after submission | Read `TAKES_*`: submitted takes were billed and downloaded, not-submitted ones were not. Fix what the rejection named and run a new, smaller batch for the remainder |
| No contact sheet | `ffmpeg` isn't installed | The videos are untouched and the sheet is skipped with a reason. Install `ffmpeg`, then `ofox-video.sh contact-sheet <files…>` to build it after the fact — no API call, no cost |
| Exit `1` on `--aspect-ratio 9:16` | The chosen model doesn't offer that ratio | `ofox-video.sh models` lists each model's ratios. Nothing was submitted, so this is free to fix — pick another cheap model that has it |
| Exit `1` on `--duration` | Below the model's minimum or above its maximum; the budget models cap lower than the flagship | `models` prints each range. Free to fix |
| The promoted clip doesn't look like the draft it came from | Nothing is guaranteed to reproduce here — a fixed seed and a byte-identical prompt have been measured returning a different clip. A changed model, or a retyped prompt, makes it likelier | Not recoverable after the fact; it is the documented behaviour, not a fault. Before the next promotion: say it up front, read the prompt from the sidecar rather than retyping it, and change resolution only — that is the closest aim available |
| The batch timed out | Wall clock exceeded `--max-wait` | Use the resume command `batch` printed, or `poll` the job ids. The jobs are running and billable; a second `batch` pays twice |
| The bill is bigger than expected | Takes x duration x rate — duration multiplies across every take | Nothing to fix after the fact. Before the next one: shorter drafts, fewer takes, and the total on screen before the yes |
| Exit `5`, ambiguous network failure on create | No HTTP response at all — can't tell whether a job exists | Don't guess or retry; tell the user to check https://app.ofox.ai for jobs that may already be running |

## When NOT to use

- **One finished clip is what's wanted.** Go straight to the scenario skill.
  A batch of drafts for a decision that has already been made is money spent
  on options nobody will look at.
- **The prompt hasn't been written yet.** This skill drafts a prompt; it
  doesn't write one. Route to the scenario skill first — a batch of five rolls
  of a vague prompt is five vague clips.
- **The output isn't vertical.** Nothing here breaks on 16:9, but then this is
  just `batch`, which the scenario skills all document themselves. Use this
  skill for the short-form format and its ladder.
- **A previous round already answered the question.** If the drafts said the
  idea works and only the fidelity was short, that is a promotion, not another
  batch.
- **The user is out of budget for iteration.** Then one clip on the cheap
  tier, looked at properly, beats five anywhere.
