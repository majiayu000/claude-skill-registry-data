---
name: image-edit
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Change one thing in an image you already have and leave the rest of the picture alone — swap the background, recolour a part, remove or add an object, clean up a photo — from a local jpeg/png/webp file. Delegates to ofox-image-core's `edit` subcommand (POST /v1/images/edits, one synchronous request), prices the job with --dry-run before spending, and reports the real token cost including the uploaded picture, which is billed. Use when a user hands over an image and asks for a change to it, e.g. "change the background of this photo to a beach and keep the person unchanged", "make this button green", "remove the car in the background", or "put this product on a plain white background". Do not use to draw a new image from a text description with no input picture (that is ofox-image-core's `generate`), to produce a set of several images to choose between (see product-image), or to turn a photo into video (see seedance-product-video or seedance-ad-creative). Editing the content of an existing video — "change the background of my clip, keep the product" — has no route here and none in the video API either (measured; the mode field an edit would use is accepted and silently ignored, so nothing errors); this skill edits a single still, and routing such a request to a video skill generates brand-new footage instead of changing theirs.
license: MIT
version: "1.1.2"
homepage: https://github.com/ofoxai/skills/tree/main/skills/image-edit
metadata:
  author: ofoxai
  version: "1.1.2"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🖌️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/image-edit
---

# image-edit: change one thing in a picture you already have

One image in, one edited image out. The craft here is not describing a
picture — the picture already exists — it is saying **what changes and what
must not**, and then checking that the file you got back honoured the second
half.

This skill is a thin, scenario-specific layer over
[`ofox-image-core`](../ofox-image-core/SKILL.md). It owns the edit
instruction's wording, the question set, the recommended defaults and the
before-and-after check; `ofox-image-core` owns talking to the Ofox image API
correctly and safely — the `OFOX_API_KEY` handling, the model resolution, the
multipart request, the decode-and-save, the cost arithmetic, and reporting an
absolute path. **Read that skill's safety contract before using this one** —
it is not restated here.

**This skill has one run of its own, and everything else here was borrowed.**
Until 2026-09-17 every figure below came from `ofox-image-core` when its
`edit` subcommand was built, or from two probe calls made directly against
`ofox-image.sh` — none of it through this skill's own flow. That gap is now
closed by one run: a real 1792x1008 photograph, the two-sentence instruction
this file teaches, `--dry-run` first, 1.6 cents. What it settled is in "The
input image decides two things at once" and in the ⚠️ under "Say what stays,
every time" — including the correction that the protection this file promises
is **feature-level, not pixel-level**. It is one edit, of one kind (a
background swap on one product photo), on one model. Where a number appears,
the run it came from is still named.

## Where the core skill lives

Resolve once, before the first call:

```bash
for d in ../ofox-image-core \
         ../ofoxai-skills-ofox-image-core \
         ~/.agents/skills/ofox-image-core \
         ~/.agents/skills/ofoxai-skills-ofox-image-core \
         ~/.claude/skills/ofox-image-core; do
  [ -f "$d/references/ofox-image.sh" ] && echo "$d" && break
done
```

Examples below are written as `../ofox-image-core/...` (the skills.sh /
ClawHub / `npx ofox-skills` layout, where a skill's directory is named after
the skill). If the probe found a different directory — LobeHub unpacks each
skill as `ofoxai-skills-<name>`, so the sibling there is
`ofoxai-skills-ofox-image-core` — substitute it, in the `ofox-image.sh`
commands and in the `references/*.md` links alike.

**That `../` is relative to this skill's own directory**, which is also where
the probe has to run. From anywhere else nothing resolves — use the absolute
path the probe printed (candidates 3–5 are absolute already), or, in a clone
of this repo, `skills/ofox-image-core/references/ofox-image.sh` from the repo
root.

Nothing found → the core skill isn't installed; see "If the script isn't
found".

**One document this skill links to lives in a different core skill.** The
spend gate's full spec is `ofox-video-core/references/approval-gate.md`,
because that file is shared by every Ofox skill in this repo, video or not.
It needs its own probe, and it is a document rather than an execution
dependency — nothing here stops working without it, and the rule it carries
still applies:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/approval-gate.md" ] && echo "$d" && break
done
```

## Before editing: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-image-core/references/ofox-image.sh check
```

It checks `curl`, `jq` and `OFOX_API_KEY` and makes no network call. If it
fails, follow `ofox-image-core`'s guidance (install the missing tool, or get
a key at `https://app.ofox.ai`) — don't dead-end the conversation, and don't
re-run the check on every subsequent request once it has passed.

A failing `check` is not a stop sign for pricing: `models` and
`edit --dry-run` both work with `OFOX_API_KEY` unset, so the whole job can be
quoted for someone who has not signed up.

## What this skill is built on: the endpoint genuinely edits

This matters more than it sounds, because it is the one fact that makes
"leave the rest alone" a reasonable thing to write at all. An endpoint that
took your image, ignored it, and redrew the prompt from scratch would return
`STATUS completed` and look identical from the outside.

Measured by `ofox-image-core` on 2026-09-15, `openai/gpt-image-2`, an 854x480
UI screenshot in, the instruction *"Change only the blue Upgrade plan button
to green. Leave every other pixel, all text and the layout exactly as they
are"*:

- **every string in the source survived verbatim** — "Billing Settings",
  "$29.00", "Seats included 3" — which a text-to-image generation from that
  prompt could not have produced;
- against the rescaled source, mean absolute difference was **5.27/255
  overall but 84.27 inside the button**, a region that is **1.1% of the
  frame** and carried **58% of all pixels differing by more than 40**.

Replicated on a second input (a red square at 320x180 → the same square, same
position, same size, blue), and a third time in this skill's own probe work
below.

**A fourth run, 2026-09-17, moved the boundary that used to be stated here.**
The three above were all **synthetic inputs with hard edges and flat colour**,
which is exactly the easy case for "did it edit or redraw". The fourth is a
real continuous-tone photograph — a brushed-steel vacuum flask on dark slate
under dramatic side light, 1792x1008 — asked to change its background to
seamless white. Every named feature came through: the `KELVIN` wordmark's
glyph shapes, letter spacing, position and engraved relief; the copper knurl's
cross-hatch; the two polished rings and the dark seam between them; the
brushed vertical grain; the waist taper. So the endpoint edits photographs
too, not only flat graphics.

**Read the boundary as carefully as the result.** That is four runs on **one
model**. It says the endpoint is doing an edit rather than a redraw; it does
not say your particular change will be surgical, and it is not evidence about
the other ten models that serve this endpoint. ⚠️ And the fourth run is also
where "surgical" gets its limit: the **lighting moved with the background**,
and the subject shifted slightly in position and scale within the frame. See
the ⚠️ under "Say what stays, every time". The verification step below is in
the instructions rather than assumed for exactly that reason.

### The two probe calls this skill's guidance leans on

Made 2026-09-15 by running `ofox-image.sh` directly while this skill was being
written — **not through this skill's flow, and not a deliverable**. Both on
`openai/gpt-image-2`, together about 3 cents.

| Probe | What was sent | What came back |
|---|---|---|
| `edit --n 2` | a 256x256 flat blue square, *"Paint a small white circle in the centre. Leave every other pixel exactly as it is."* | two files. Both kept the blue field and added a centred white circle; the circles differ visibly in size between the two. Output 1254x1254 each |
| `generate --n 2` | no input image; a plain mug prompt at `--quality low --size 1024x1024` | two visibly different renders of the same brief — different scale, proportions and light |

The edit probe is a third independent confirmation of the paragraph above, on
a different kind of input, and the pair together are what
[`product-image`](../product-image/SKILL.md) uses to settle how a *set* is
produced. Their token counts are in that skill; what they establish for this
one is narrower: **an edit with `--n` returns that many distinct results**,
and a "leave the rest alone" clause held on both of them.

## Before writing the instruction: the brief

Two of these axes are not taste. Without the file there is nothing to edit,
and without knowing what must **not** change there is no way to tell a good
result from a redraw.

The shared rules for asking — the three tiers, one round of at most four
questions, the shape of a question, the "Let the AI decide" discipline, the
order with the approval gate, the fallback for a runtime without
`AskUserQuestion` — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
That file is written for video briefs and every rule in it about *how* to ask
carries over unchanged; its question *content* does not. This section is this
scenario's own question set.

Zero questions is common and correct: "change the background of this photo to
a beach, keep the person exactly as they are" plus an attached file has
settled every axis there is.

| Tier | image-edit axes |
|---|---|
| **must-ask** | which file, and what changes. Both decide whether there is a job at all |
| **ask-if-open** | what must survive unchanged; the shape the delivered file has to be |
| **never-ask** | the model, `--quality`, `--size`, `--output-format`, `--background`, how many results. The model comes from the chain and is named in the cost table; the rest have defaults below and are rows, not questions |

### The question set

| # | Tier | `header` | Question | Options (1 = recommended) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Image` | Which file should I edit? A local path is best — nothing has to be hosted anywhere. | free text: a local path (**recommended** — `--image`), or a public URL / `data:` URI (`--image-url`). jpeg, png or webp. **No AI option** — a file that does not exist cannot be invented. | No image attached and no path in the request. |
| 2 | must-ask | `Change` | What exactly should change? | free text. Push for one change, named concretely: "the background becomes a beach at sunset", "the jacket becomes dark green", not "make it nicer". **No AI option** — this is the job. | The request names a file but not a change. |
| 3 | ask-if-open | `Keep` | What has to come back untouched? | **The subject, exactly as it is (recommended)**: the usual answer for a person, a product or a logo. / **All text and layout**: for a screenshot or a document. / **Everything except the one thing above**: the strictest form, and the one the measured run used. / **Let the AI decide** — the last option. | The change is named but nothing says what is at risk. Skip it when the request already says "keep the person unchanged". |
| 4 | ask-if-open | `Shape` | What shape does the delivered file have to be? | **Whatever the source is (recommended)**: the output follows the input's ratio, so no crop is needed. / **Square 1:1**, / **16:9**, / **9:16** — any of these means cropping the source first, and I will say what that costs in pixels. / **Let the AI decide** — the first option. | The result is going somewhere with a fixed shape (a listing, a thumbnail, a video first frame) and the source is a different shape. |

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| a file is attached, or a path is given | Image | use it; do not ask whether there is one — but **open it first and confirm it is the picture being described**. A path is a claim about which file, and a wrong source does not fail: the edit succeeds, bills, and returns a correct edit of the wrong picture. If what you see does not match the request, say what you actually see and ask, rather than proceeding on the theory that the user knows their own folder |
| "keep the person / the product / the text the same" | Keep | exactly that, quoted back into the instruction |
| "only change the…", "just the…" | Keep | everything else — write the strict form |
| "for my listing", "main image", "thumbnail" | Shape | 1:1 — and say the source will be cropped |
| "for a video", "as the first frame" | Shape | 16:9 or 9:16 — and see "When NOT to use", because a video first frame belongs to the video scenario skill that will consume it |
| "make it look like a painting / a 3D render / a different style" | — | that is a whole-image change, which this endpoint can do, but it has no "leave the rest alone" half. Say so before spending |
| "my video", "this clip", "the footage" — the thing to be changed is a **video** | — | no skill in this repo edits the content of existing footage. Do not route it to a video skill, which generates a new clip instead. See "When NOT to use" for what to offer |

### From answers to the command

| Answer | Lands in |
|---|---|
| Image | `--image PATH` (or `--image-url URL`) |
| Change | the first sentence of `--prompt` |
| Keep | the second sentence of `--prompt`, and what you check on the result |
| Shape | a crop of the **source** before the call, and optionally `--target-aspect` as a guarantee on the output |

### The recap for this scenario

```
Brief:
- Image: /Users/me/photos/portrait.jpg (given), 1200x1600
- Change: the background becomes a beach at sunset (you said)
- Keep: the person — pose, face, clothing, edges (you said "person unchanged")
- Shape: same as the source, 3:4 — no crop (AI's pick)
```

Then the exact `--prompt` text, then the cost table, all in one message. The
user approves the instruction and the price together.

## Writing the edit instruction

An edit instruction is two sentences and they do different jobs. Neither is
optional, and the second one is the one people leave out.

```
<What changes, named concretely.> <What must not change, named concretely.>
```

Worked, from the measured run:

```
Change only the blue Upgrade plan button to green. Leave every other pixel, all text and the layout exactly as they are.
```

And the scenario this skill is named for:

```
Replace the background with a beach at sunset, with soft late light coming from the left. Keep the person exactly as they are — pose, face, hair, clothing and the edges where they meet the background.
```

Five things that follow from how the endpoint behaves:

- **Name the thing, don't gesture at it.** "The blue Upgrade plan button", not
  "the button". The instruction is the only place the region gets identified;
  there is no mask (see below), so the words are the selection.
- **Say what stays, every time.** The measured run's second sentence is the
  reason its result is checkable at all: it turns "did this work?" into a
  question about **named features** you can look for one by one. Without it
  you are comparing against your memory of the source.
  ⚠️ **What it buys is feature-level, not pixel-level, and the difference
  shows up the moment the change is a background.** Measured 2026-09-17 on a
  1792x1008 product photo asked for a seamless white background while keeping
  the body, the cap, the wordmark and the proportions: every named feature
  survived — the wordmark's glyph shapes, letter spacing and engraved relief,
  the knurl's cross-hatch, the two polished rings and the dark seam between
  them, the brushed vertical grain, the waist taper. **And the lighting
  changed with the background** (dramatic side-rim to soft even studio), and
  in the same crop the subject sat slightly lower and slightly larger.
  That is not a defect — a new background *has* to be relit — but it means
  the second sentence cannot be verified by diffing pixels outside the region
  you named. Check the features you listed, at magnification. Do not promise
  a user that everything outside the change is untouched to the pixel.
- **One change per call, and be honest that it costs more.** Two unrelated
  changes in one instruction is one bill; doing them as two calls is two. The
  reason to pay twice is that a combined instruction has not been measured
  here, and if the result gets one change right and the other wrong you cannot
  re-roll half of it — the second call is what you would have spent anyway, and
  the first result stays usable. At the cents these edits bill, that is a
  cheap kind of control. **Put the choice in the cost table** rather than
  making it silently: two rows and a total, or one row and a stated risk.
- **A whole-image restyle is a different job.** "Make this a watercolour
  painting" is legitimate and this endpoint will do it, but it has no
  leave-the-rest-alone half, so the verification step below cannot tell a good
  result from a redraw. Say that to the user before spending, rather than
  after.
- **Do not ask for text to be added or corrected and expect it to be
  reliable.** What is measured is that existing strings **survive** an edit
  aimed elsewhere. Nothing here measures the endpoint writing new text, and
  this repo's video work has repeatedly found generated lettering
  untrustworthy. If a label has to read exactly right, edit it in an image
  editor.

### There is no mask, and that is not a limitation you can route around here

`POST /v1/images/edits` may or may not accept a `mask` file — `ofox-image-core`
records it as **not established**, because finding out costs a billed edit per
attempt and this endpoint renders anything it does not reject. So the region
is selected by the words in `--prompt`, and if you want to try a mask anyway
that is `edit --extra-form` and the result belongs in
`ofox-image-core/references/api-params.md`, not in a workaround written here.

## Which models can edit: ask, never assume

**There is no model table in this file, and there must not be one.** Support
is read live from each model's `supported_endpoints` in the Ofox catalog:

```bash
bash ../ofox-image-core/references/ofox-image.sh models --endpoint edits
```

Free, keyless, and current. As of 2026-09-15 that list held 11 of the 16 image
models Ofox serves — but quote the command's output, not that count.

**Omit `--model`.** `ofox-image-core` resolves one from its cheapest-first
priority chain *against the edits endpoint*, so a chain entry that cannot edit
is skipped with a printed reason rather than failing at submission. Pass
`--model` only when the user named one. A scenario skill that pinned its own
model quietly kept paying an old price after the chain moved; that is the
failure this rule exists for, and it is `ofox-image-core`'s rule, not this
skill's invention.

Two things the script prints that must be relayed rather than swallowed:

- `MODEL_FALLBACK_FROM` / `MODEL_FALLBACK_REASON` / `MODEL_PRICE_DELTA` — the
  preferred model was unusable and something else ran, possibly dearer.
- `MODEL_SOURCE request` — the response carried no model name, so the id is
  the one that was asked for rather than one the API confirmed. Say it that
  way.

## ⚠️ This endpoint does not reject bad parameters — the dry run is the guard

On `POST /v1/images/generations` a bad `--quality` comes back as a free HTTP
400. On `POST /v1/images/edits` it does not: measured 2026-09-15 by
`ofox-image-core`, an unknown `--quality` value was **silently ignored,
rendered, and billed on six models**.

So `--dry-run` here is not a politeness before a request the API would have
refused anyway. It is the only thing standing between a typo and a bill.
**Dry-run every edit, and read the `FORM_FIELDS` line** — it names exactly
what will be sent.

The same lesson generalises past this skill, and it is worth carrying: a free
probe is only free if the thing you expect to reject it actually does.

## The input image decides two things at once

Both are measured on **one model over four runs**
(`openai/gpt-image-2`, 2026-09-15 for the first three via `ofox-image-core`,
2026-09-17 for the fourth through this skill's own documented flow), and
neither should be stated as general.

**1. The output's shape follows the input's.** Four runs, no `--size` passed:

| Input | Output |
|---|---|
| 854x480 (16:9) | 1672x941 |
| 320x180 (16:9) | 1672x941 |
| 256x256 (1:1) | 1254x1254 |
| **1792x1008 (16:9)** | **1672x941** |

Those two output sizes are 1,573,352 and 1,572,516 pixels — 0.05% apart — so
the endpoint appears to spend a near-constant ~1.57 MP on whatever shape it
was handed. **The fourth run is the useful one for that claim**: at 1792x1008
the input is already larger than the output, and the output still landed on
the same 1672x941. So the ~1.57 MP budget is a budget in both directions, not
just an upsample floor — held on the largest input measured here. Note the useful corollary: 1672x941 is 1.777, the true 16:9 that
the `generate` size enum **cannot express at all**. An edit reaches a ratio a
generation cannot request.

**Whether `--size` is honoured here is untested**, which is why the rule below
is about the input rather than a flag:

- **To change the delivered shape, crop the source before the call** — the
  output then arrives at the ratio you want, and the crop also cuts the bill.
- **To guarantee it, add `--target-aspect W:H`.** The script then measures the
  written file and centre-crops it, or fails loudly rather than handing back an
  almost-right file. It needs `ffmpeg`/`ffprobe` and fails as exit `2`
  **before** anything is spent if they are missing.
- Do both when the shape is load-bearing: the crop gets you there, the flag
  proves it.

**2. The picture you upload is billed.** On the 854x480 run, **576 of 608
input tokens were the image**. That component does not exist for a generation
at all. Measured points:

| Input | Image tokens | Billed |
|---|---|---|
| 320x180 | 240 | 0.6 cents |
| 256x256 | 256 | 0.9 cents |
| 854x480 | 576 | 1.4 cents |
| **1792x1008** | **1508** | **1.6 cents** |

⚠️ **It is not linear in pixels, so do not scale those figures.** 256x256
bills 256 image tokens and 854x480, with **6.3x the pixels**, bills 576. The
1792x1008 point is the same story at the other end: **4.4x the pixels of
854x480 for 2.6x the tokens**. The direction is reliable (a smaller source
costs less); the ratio is not, at either end. Price the actual file with
`--dry-run`, which matches the estimate on the input's own measured size.

⚠️ **Do not reason about the cost from output tokens.** They do not track the
input size at all: 129 output tokens for a 320x180 input, 229 for 256x256,
301 for 854x480, and **129 again** for 1792x1008 — the largest input ties the
smallest for the lowest count. The uploaded picture is what moves, and on a
large source it is most of the bill: `1508 * 0.000008 = 0.012064` is **74%**
of that run's 0.016249. So the lever is the **size of the file you upload**,
and `--dry-run` on the real file is the figure to relay.

**What is not measured is whether a downscaled source costs you quality.** The
output lands at ~1.57 MP either way, so the endpoint is upsampling from
whatever you give it. Shrinking a 4000px photo to save a fraction of a cent is
a trade nobody here has evaluated — do it when the source is genuinely huge
and the result is a thumbnail, not by reflex.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--image` | a **local file path** | The primary route and the one that needs no hosting. `--image-url` takes a public URL or a `data:` URI; pass exactly one of the two, and the script rejects both together |
| `--model` | **omit it** | `ofox-image-core` resolves the chain against the edits endpoint and reports any fallback. Pass one only when the user named one |
| `--quality` | **omit it** | Not required on this endpoint, unlike `generate`. Omitting it returned `"quality": "low"` on the measured runs. And since this endpoint does not validate the value, an omitted flag cannot be a typo |
| `--size` | **omit it** | Whether it is honoured here is untested. The output's shape comes from the input's — crop the source, or use `--target-aspect` |
| `--target-aspect` | only when the delivered shape is load-bearing | Turns the shape into a promise the script keeps or fails on. Needs `ffmpeg`/`ffprobe`; checked before any spend |
| `--n` | **omit it (1)** | One change, one result. `--n` is for variations to choose between, which is [`product-image`](../product-image/SKILL.md)'s job — and it is not a discount: measured at `--n 2`, both token components scaled exactly with the count |
| `--output-format` | omit unless asked | The response echoes this field on edits, so the saved file is named from what the API says it wrote |
| `--out-dir` | **always pass it, absolute** | Without it the file lands in whatever directory you happened to be in — which, given the examples run from this skill's own directory, means inside an installed skill |
| `--out-name` | pass it | Name the file after the change. A bare filename, no extension, no path separators |

## Before you spend: the approval gate

**Never send an edit until the user has seen a cost table and said yes.** The
rule, the required columns, where the numbers must come from and what to do
when no estimate is possible are written down once for every Ofox skill in
this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
(directory-name caveat and probe: "Where the core skill lives" above).

Get the number from `--dry-run`, which parses the arguments, resolves the
model, validates every parameter, creates and checks `--out-dir`, builds the
multipart form and prints the estimate — then returns, before the `POST`.
Nothing is submitted, nothing is billed, and **no `OFOX_API_KEY` is needed**:

```bash
bash ../ofox-image-core/references/ofox-image.sh edit --dry-run \
  --image /absolute/path/to/photo.jpg \
  --prompt "Replace the background with a beach at sunset. Keep the person exactly as they are — pose, face, hair, clothing and the edges where they meet the background." \
  --out-dir /absolute/path/to/out \
  --out-name beach-background
```

**Relay the `Estimated cost:` line exactly as it prints** — never a figure of
your own, and never a cents-per-image number copied out of this file. The line
carries the input size it was matched on and says how rough it is; a number
lifted out of it loses both. Three things belong in the table alongside it:
the resolved `MODEL`, the `INPUT_SIZE_ACTUAL` the script measured, and the
full `--prompt`.

Then wait for a yes, then re-run the identical command with `--dry-run`
removed. The estimate a real run prints comes microseconds before the request
goes out, too late to relay; that is what the dry run is for.

Afterwards the **actual** bill is the `EDIT_COST` line, computed from the
response's own token counts. Report it as money, not as a raw six-decimal
string, and note the script's own caveat: `EDIT_COST` is the **dearer** of two
readings of the same counts, because no invoice has settled which is right, so
it errs high by rule.

## Editing

```bash
bash ../ofox-image-core/references/ofox-image.sh edit \
  --image /absolute/path/to/photo.jpg \
  --prompt "<the two-sentence instruction built above>" \
  --out-dir /absolute/path/to/out \
  --out-name beach-background
```

What comes back, and what to do with each part:

```
STATUS completed
IMAGE_PATH <absolute path to the edited file>
INPUT_IMAGE <absolute path to the source>
INPUT_SIZE_ACTUAL <WxH measured from the source>
MODEL / MODEL_SOURCE / SIZE / SIZE_ACTUAL / QUALITY
USAGE_INPUT_TOKENS / USAGE_INPUT_IMAGE_TOKENS / USAGE_INPUT_TEXT_TOKENS
USAGE_OUTPUT_TOKENS / USAGE_TOTAL_TOKENS
EDIT_COST <dollars>
```

- **`IMAGE_PATH` goes in your reply as its own standalone line**, absolute, not
  folded into a sentence. It is the deliverable; the user should not have to
  re-derive your working directory to find it. This mirrors
  `ofox-image-core`'s `IMAGE_PATH` discipline and `ofox-video-core`'s
  `VIDEO_PATH` one exactly.
- **`SIZE_ACTUAL`, not `SIZE`.** `SIZE` is printed straight from the response
  and this API has a recorded history of that field disagreeing with the file
  on disk. `SIZE_ACTUAL` is measured from what was written.
- **`INPUT_IMAGE` is printed next to `IMAGE_PATH` on purpose** — so the check
  below is one command.

## Verify the artifact, not the exit code

`STATUS completed` means the request was accepted and a file was written. It
cannot tell you whether the endpoint edited your image or quietly redrew the
prompt from scratch, and it cannot tell you whether the thing you asked to
keep survived.

**Open the result next to `INPUT_IMAGE` and check the half of the instruction
that said "leave this alone".** The script prints a reminder on every
successful edit; treat it as a step, not a nicety.

What to look at, in order:

1. **The named change** — did the one thing you asked for happen?
2. **The thing you said must not change** — the face, the label, the layout,
   the text. Compare, do not recall.
3. **The edges between them.** A background swap is where a subject's outline
   gets softened or re-invented, and it is the part a thumbnail-sized glance
   misses.

If a difference is subtle and the decision matters, a numeric comparison is
cheap and free: rescale the source to the output's size and look at where the
differences actually are, rather than at an overall average. That is how the
measured run distinguished a real edit from a redraw — 5.27/255 overall told
nobody anything; **84.27 inside the region that was supposed to change, and
58% of substantially-changed pixels sitting in 1.1% of the frame**, is the
statement worth making.

**A failed edit is not free.** There is no job id and no poll on this API, so
a disappointing result is a spent call; the fix is a new call with a better
instruction, priced again. That is the argument for the dry run and for one
change per call, not an argument for lowering the bar on what you accept.

## Pricing a job with no API key

Both of these work with `OFOX_API_KEY` unset:

```bash
bash ../ofox-image-core/references/ofox-image.sh models --endpoint edits
bash ../ofox-image-core/references/ofox-image.sh edit --dry-run \
  --image /absolute/path/to/photo.jpg --prompt "..." --out-dir /absolute/path/to/out
```

So when a user has not signed up yet, **quote the job first and let them
decide whether it is worth registering.** Don't open with a signup link —
price it, show the number, then point at
[app.ofox.ai](https://app.ofox.ai) if they want to proceed.

## If the script isn't found

```
bash: ../ofox-image-core/references/ofox-image.sh: No such file or directory
```

Nothing is broken — this skill delegates all execution to `ofox-image-core`
and reaches it by relative path, and that path just missed. Two different
situations wear this same message, so run the probe in "Where the core skill
lives" before deciding which one it is:

- **The probe printed a directory** — the core is installed and only the
  directory *name* was wrong, which is the normal LobeHub case
  (`ofoxai-skills-ofox-image-core`). Re-run against what the probe printed.
  Nothing needs installing.
- **The probe printed nothing** — `ofox-image-core` really is absent, and
  installing it is the user's call to make, not yours: an install writes
  outside this working directory, so hand over the command and let them run
  it rather than running it for them. Which command depends on the installer
  they already have — skills.sh is
  `npx skills add ofoxai/skills --skill ofox-image-core`, which asks for that
  one skill and answers none of the agent, scope or confirmation questions on
  the user's behalf; this repo's own wrapper is
  `npx ofox-skills ofox-image-core`, the same install with all three answered
  in advance (every agent, user-level, no prompts); on LobeHub or ClawHub,
  install `ofox-image-core` from the same publisher. Ask for the one skill
  that is missing rather than the whole repo, and give all three routes —
  pointing a LobeHub user at the skills.sh line alone reads as "abandon your
  installer", which isn't the advice.

Either way, name the missing skill and where it was expected rather than
relaying the raw path error, which names neither.

A broken link to `approval-gate.md` has the same two causes and its own probe
above. This skill packages only its `SKILL.md` and `CHANGELOG.md`, so nothing
in this file becomes unusable when a link misses — the instruction shape, the
question set and the defaults are all written out here. What is lost is the
gate's exact wording, which still applies, and `ofox-image-core`'s depth on
the API itself.

## Exit codes worth knowing

Full table in [`../ofox-image-core/SKILL.md`](../ofox-image-core/SKILL.md).
The ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `0` | Success, **or** a `--dry-run` that spent nothing | Read `STATUS` to tell them apart |
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely. A file that is not jpeg/png/webp, `--image` plus `--image-url`, a `--quality` typo, `--n` on a model that refuses it, and **a `--model` that does not serve the edits endpoint** all land here — the script checks that against the same live `supported_endpoints` field the API decides on |
| `2` | Environment problem — `curl`/`jq`/`OFOX_API_KEY` missing, or `ffmpeg`/`ffprobe` missing while `--target-aspect` was passed | Ask the user to fix it; `check` reports the same. Nothing was attempted |
| `3` | The API rejected it, the response couldn't be parsed, or a `--target-aspect` target couldn't be met by the file that came back | Read the upstream message. `endpoint_not_supported` and `model_not_found` reach here only when the local catalog check was skipped or fell back to a snapshot, and are free rejections either way; a crop that couldn't be met means **the image was generated and billed** and is on disk at the `-uncropped` path |
| `4` | `--out-dir` could not be created or entered | Caught before any network call. Fix the path and retry — no money was spent finding out |
| `5` | Ambiguous network failure — no HTTP response at all | There is no job id to look up. Do **not** auto-retry; tell the user to check `https://app.ofox.ai`'s usage history first |

## Where the file lands

Always pass `--out-dir`, and **make it an absolute path**. `--out-dir` is
resolved and created **before** any network call, so a bad path fails as exit
`4` with nothing submitted — pass the same one to the dry run and the real
run.

Pass `--out-name` too. You know what the change was, so name the file after it
rather than leaving the script to fall back on a timestamp. With
`--target-aspect` the cropped file takes the plain name and the API's
untouched bytes are kept beside it as `<name>-uncropped.<ext>`, reported as
`IMAGE_PATH_UNCROPPED`.

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, "does not look like a supported format" | The endpoint enumerates exactly three: jpeg, png, webp — its own wording from a real rejection | Convert first (`ffmpeg -i in.gif out.png`) and re-run. Nothing was submitted |
| Exit `1`, both `--image` and `--image-url` | Exactly one input is allowed | Drop one. The local file is the better route when you have it |
| Exit `1` on `--n` | The chosen model refuses `n` outright — `google/gemini-3.1-flash-image` does, even at `n: 1` | Omit `--n`, or pin a model whose catalog entry advertises it. Free to fix; nothing was submitted |
| Exit `1`, "exists but does not serve /v1/images/edits" | A `--model` that cannot edit, caught locally against the catalog's `supported_endpoints`. Nothing submitted | `models --endpoint edits` lists the ones that can. This is why `--model` should usually be omitted. Reaching the API instead returns `endpoint_not_supported` — also free, fired before any parameter is looked at |
| Exit `3`, `model_not_found` | The model id does not exist and the local check didn't catch it (snapshot fallback, or validation skipped) | Check the id against `models`. Nothing billed |
| The result is a *new* picture rather than an edit of yours | Almost always the instruction: no "leave the rest alone" half, or a whole-image restyle that has no such half by nature | Rewrite as two sentences, the second naming what must survive. **The spent call is not recoverable** — this is why the instruction is approved with the price |
| The subject changed even though the instruction said not to | One run, one roll. The endpoint edits rather than redraws on the runs measured, but that is four runs on one model and says nothing about a guarantee | Re-run with the "keep" sentence made more specific (name the features, not just the noun). A new call, so a new cost table |
| The edges around a swapped background look re-invented | The commonest real defect of a background change, and not something any wording here has been measured to fix | Name the boundary in the keep sentence ("and the edges where they meet the background"). Untested wording — check the result rather than trusting it |
| A `--quality` typo rendered and billed anyway | This endpoint does not validate the value; measured on six models | Nothing to recover. Prevention only: `--dry-run` first, which rejects it locally, and omit `--quality` when you have no reason to set it |
| The delivered file is the wrong shape | The output follows the **input's** ratio, and `--size` is untested here | Crop the source to the target ratio and re-run, and pass `--target-aspect` so the script guarantees it rather than you checking. A new call, so a new cost table |
| The bill was bigger than expected on a large photo | The uploaded picture is billed, and the input-token count is not linear in pixels | Nothing to fix after the fact. Next time: dry-run the actual file — the estimate is matched on that file's own measured size — and consider a smaller source |
| Exit `5` | No HTTP response at all; unlike the video API there is no job id to check | Do not retry blindly. Check `https://app.ofox.ai`'s usage/billing history first |

## When NOT to use

- **There is no input image.** Drawing a picture from a text description is
  `generate`, not `edit` — go to
  [`ofox-image-core`](../ofox-image-core/SKILL.md) directly, which is what
  that skill's own description says to do for a plain "generate an image
  of…" request.
- **The user wants several images to choose between**, or "four main images
  in different styles", or a set at all — that is
  [`product-image`](../product-image/SKILL.md), which owns how a set is
  produced and quotes the set's total rather than one image's price. This
  skill is one in, one out.
- **The thing to be edited is a video, not a still.** "Change the background
  of my 10-second clip to a beach and keep the product exactly as it is" has
  **no route in this repo and none in the API behind it**, and this is the
  skill such a request lands on, so it is said here.
  **Measured 2026-09-16, and the shape of the answer matters**: the Ofox
  create request does carry a `mode` field, which is how the public gallery's
  `edit` cases were run — and it is **accepted and discarded**. Job
  `4686f434` sent an invented mode value in an ordinary text-to-video request,
  got `200`, and billed as an ordinary t2v clip. So there is no rejection to
  show the user and no error to wait for; the parameter simply does nothing.
  Detail: `ofox-video-core`'s `references/api-params.md` → "`mode` is accepted
  and has no effect".
  Nothing in this repo edits the content of existing footage.
  What is honestly available: a **still** can be edited (that is this skill),
  and a still can then be turned into video — but that **generates new
  footage** rather than editing theirs, and whatever real motion, lighting,
  timing and performance their clip had does not carry over. Say that before
  anyone spends.
  ⚠️ The specific wrong turn to avoid:
  [`seedance-product-video`](../seedance-product-video/SKILL.md)'s worked
  example contains *"image1 provides the product exactly as it is; take
  nothing from its background"*, which is a near-verbatim match for what this
  user asked for. It is not the same job — it keeps a **product** identical
  while generating a brand-new clip, and routing there spends money on
  footage that is not the footage they wanted changed.
  [`video-extend-edit`](../video-extend-edit/SKILL.md) continues an existing
  clip from one of its own frames and also does not edit what is inside the
  picture. For a real edit of real footage, the answer is a video editor or a
  rotoscoping tool, not this repo.
- **The deliverable is a video.** A product photo becoming catalog footage is
  [`seedance-product-video`](../seedance-product-video/SKILL.md); a photo
  becoming a cinematic ad is
  [`seedance-ad-creative`](../seedance-ad-creative/SKILL.md). Editing the
  photo first is sometimes a sensible step inside those flows — but the
  scenario skill owns the job, because an attached frame's own ratio becomes
  the finished video's ratio and that decision belongs where the video is
  priced.
- **The image is an anime or manga character being built for a video
  sequence.** [`seedance-anime-drama`](../seedance-anime-drama/SKILL.md)
  generates those itself and carries the consistency machinery that keeps one
  character the same across shots; an edit made outside that flow is not
  tracked by it.
- **The user is driving the API directly** — naming low-level parameters,
  debugging a failed request, trying a `mask` through `--extra-form`. That is
  `ofox-image-core`'s own territory; this skill adds instruction craft, not
  API surface.
- **The change has to be exact** — a specific hex colour, a pixel-accurate
  crop, a logo swapped for a supplied file, text that must read correctly. A
  generative edit is a re-render, not a compositing operation.
  [`hal-image`](../hal-image/SKILL.md) does deterministic ImageMagick work
  locally, for free, and gets those right by construction.
