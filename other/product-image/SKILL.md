---
name: product-image
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Produce a set of product images to choose between — several styles, backgrounds or treatments of one product, for a listing, a store page or an ad — and quote the whole set's cost before any of it is spent. From a real product photo it edits that photo once per style, so the item stays identical across the set; for a fictional or prototype product with no photo it generates from text instead, and says what that costs in accuracy. Delegates to ofox-image-core. Use when a user asks for several product images at once, e.g. "give me 4 main images in different styles for this product", "a few background options for this photo", "some listing images for my shop", or "show this product on white, on wood, and in a lifestyle scene". Do not use for a single change to a single image (see image-edit), for video from a product photo (see seedance-product-video), or for one plain text-to-image render (that is ofox-image-core's `generate`).
license: MIT
version: "1.1.2"
homepage: https://github.com/ofoxai/skills/tree/main/skills/product-image
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
    emoji: "🛍️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/product-image
---

# product-image: a set of product images to choose between

"Four main images in different styles" is a **set**, and a set is a different
job from one picture. It has a shape nobody asked about out loud — how many,
varying what, and does the product stay the same across them — and it has a
price that is the total, not the per-image figure.

This skill is a thin, scenario-specific layer over
[`ofox-image-core`](../ofox-image-core/SKILL.md). It owns the set's
composition, the per-style prompt craft, the consistency requirement and the
set-total pricing; `ofox-image-core` owns talking to the Ofox image API
correctly and safely — the `OFOX_API_KEY` handling, model resolution,
requests, decoding, cost arithmetic and absolute paths. **Read that skill's
safety contract before using this one** — it is not restated here.

**This skill has produced one set of its own.** 2026-09-17: three background
variants of a single real product photograph, on the `edit` route this file
recommends, one axis varied, one image plainly on white, about 1.6 cents each.
It settled the claim the whole skill turns on — **the product is the same
product in all three** — and it exposed one this file had not said: **the
product's size within the frame is not held**. Both are in "Why the 'keep'
sentence is worth its length". Three images is not four and one product is not
a catalogue; the **generate** route still has no set of its own.

The other measured figures below come from `ofox-image-core`'s work building
the `edit` subcommand, and from two probe calls made directly against
`ofox-image.sh` while this file was being written. Every one of them names the
run it came from.

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

**The spend gate's spec lives in a different core skill**, because it is
shared by every Ofox skill in this repo, video or not. It is a document rather
than an execution dependency — nothing here stops working without it, and the
rule it carries still applies:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/approval-gate.md" ] && echo "$d" && break
done
```

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-image-core/references/ofox-image.sh check
```

It checks `curl`, `jq` and `OFOX_API_KEY` and makes no network call. If it
fails, follow `ofox-image-core`'s guidance (install the missing tool, or get a
key at `https://app.ofox.ai`) — don't dead-end the conversation, and don't
re-run the check on every subsequent request once it has passed.

A failing `check` never blocks the quote: `models` and both `--dry-run` forms
work with `OFOX_API_KEY` unset, so a whole set can be priced for someone who
has not signed up.

## First: is there a photo of the real product?

Settle this before anything else. It decides the command, the price and how
much of the result you can promise.

| The product is… | Route | What you get |
|---|---|---|
| a **real item the user has a photo of** — a real SKU, a logo, a printed label, particular geometry | **`edit`, once per style.** Every image in the set starts from the same source file | the product stays itself across the set, because every image is an edit of the same picture rather than an independent invention of it |
| a **fictional, prototype or purely generic product** — "a matte white ceramic mug", a brand that does not exist yet | **`generate`, once per style** | a set of plausible product images that are **not the same object** — see the measurement below. Say this before spending. This route is also the one where `--quality` becomes required and decides the set's whole cost profile (⚠️ section under the approval gate) |

### The file being there is not evidence it shows the product

**Open the source image and confirm it is the product before treating it as
one.** A path in a request is a claim, and the claim is wrong often enough to
be worth ten seconds: wrong file picked from a folder, a screenshot instead of
a photo, the packaging instead of the item, last week's SKU.

This is cheap to check and expensive to skip, because the edit route does not
fail on a wrong source — it succeeds. Four calls against the wrong picture
return four well-executed, correctly-billed images of the wrong thing, and the
mistake is only visible when someone opens them.

If the file is not the product the user described, **stop and say what you
actually see**, naming both — "this looks like a screenshot of a billing
settings page, not a thermos". Do not:

- proceed anyway on the theory that the user knows their own files;
- silently switch to the generate route, which produces a *different* wrong
  answer — four images of a plausible invented item — at the same cost;
- generate a reference image and edit that. See the prohibition below; the
  wrong-file case is exactly where it is most tempting.

The three legitimate exits are: ask for the right file, proceed on the generate
route **only if the user confirms there is no photo** and accept what that
costs in accuracy, or stop.

**The measurement that decides it.** One probe call, 2026-09-15,
`openai/gpt-image-2`, `generate --n 2` on a single mug prompt at
`--quality low --size 1024x1024`: two files came back, and they are visibly
different mugs — different proportions, different camera scale, different
light. For "give me two options", that variety is the product. **For a
listing, it is the defect**, because a shopper compares every image in a set
against the same physical item and against each other.

That is one probe on one model, not a law. But it lines up exactly with
[`seedance-product-video`](../seedance-product-video/SKILL.md)'s own rule,
arrived at independently: a real SKU needs the photo, a category prototype can
go text-only with the expectation set. This skill follows the same split, for
the same reason.

⚠️ **Do not offer to generate a reference image first and then edit that.**
`seedance-product-video` records the reasoning and it holds here identically:
a generated image can be wrong about the label, the cap and the proportions in
exactly the ways the set can — and then locks those errors into every image in
it. If the user has no photo of a real SKU, say the results may not match the
item and offer to proceed as a category prototype instead.

## How a set is actually produced — asked, not assumed

This is the question this skill exists to have already answered, so read it
before reaching for `--n`.

### The request has one `prompt` field, so a style set is N calls

Four styles means four different instructions. The request body carries
exactly **one** `prompt`, and there is no per-image prompt field on either
endpoint. So a four-style set is four calls whatever else is true — that is
not a guess about how the model behaves, it is the field list.

`--n` is a count on a single prompt. It asks for N renders of the *same*
instruction. Useful, and a different thing.

### What `--n` does buy, measured

Two probe calls, 2026-09-15, run directly against `ofox-image.sh` while this
file was being written — **not through this skill's flow, and not
deliverables**. Both on `openai/gpt-image-2`; together about 3 cents.

| Probe | Output files | Output tokens | The n=1 anchor for the same conditions | Billed vs estimated |
|---|---|---|---|---|
| `generate --n 2`, `--quality low --size 1024x1024` | 2, suffixed `_0` and `_1` | 391 | 196 (2x = 392) | 1.19 cents against a 1.18-cent estimate |
| `edit --n 2`, a 256x256 input | 2, suffixed `_0` and `_1` | 458 | 229 (2x = 458, exactly) | 1.81 cents against a 1.84-cent estimate |

Three things follow, and the third is the one that settles the route:

1. **`--n` really does return that many distinct results.** Two files each
   time, visibly different from each other, and the edit pair both honoured
   the instruction's "leave every other pixel exactly as it is" half.
2. **Output tokens scale linearly with `n`** — 391 against 2x196, and 458
   against exactly 2x229. Before these probes the script's own dry run said
   this "has never been measured on either endpoint"; now it has been, at
   n=2, on one model, on both endpoints.
3. **`--n` is not a discount.** On the edit probe the *input image* tokens
   came back as **512 = exactly 2 x 256**, so the uploaded picture is billed
   once per output image rather than once per call. On the generate probe the
   input text tokens scaled the same way. **One call at `--n 4` and four
   separate calls cost the same**, to within the measurement.

### Therefore: the default is N separate calls

Since the price is the same either way, choose on what the set needs — and a
product set needs three things `--n` cannot give:

- **different instructions per image**, which is what "different styles" means;
- **the ability to stop after the first one is wrong**, instead of paying for
  four renders of a misunderstanding;
- **independent re-rolls** — replace image 3 without touching 1, 2 and 4.

So: **one call per image, one prompt each.** Reach for `--n` only when the
user wants several rolls of **one** style to pick from — and price that as
part of the same set total.

### Which models take `n` at all: ask the catalog

**There is no support table in this file.** The Ofox catalog carries it, free
and keyless, in each model's `image_attributes.supported_params`:

```bash
curl -s https://api.ofox.ai/v1/models | jq -r '
  .data[]
  | select((.supported_endpoints // []) | index("/v1/images/generations"))
  | [.id,
     (if .image_attributes.supported_params == null then "unknown — no image_attributes"
      elif (.image_attributes.supported_params | index("n")) then "n advertised"
      else "n absent from the list" end)]
  | @tsv'
```

**Three states, not two** — which is why the query is written this long. A
model that carries the list and leaves `n` out of it is saying something; a
model with no `image_attributes` block at all is saying nothing.

Read 2026-09-15: `n` was advertised by exactly **four** of the sixteen image
models, all OpenAI ones; the four Gemini models carry the list and omit `n`;
the other eight (Microsoft, Qwen, Volcengine) have no `image_attributes` block
at all. Quote what the command prints today, not that sentence.

Two limits worth carrying:

- **`google/gemini-3.1-flash-image` refuses `n` outright**, even at `n: 1`.
  `ofox-image-core` rejects it client-side on both subcommands — exit `1`,
  free, nothing submitted.
- **`supported_params` is a generations-shaped list** and never mentions the
  edits endpoint. The edit probe above shows `n` working on the edits endpoint
  for a model that advertises it, which is one model in one direction. Do not
  read the field as an edits contract.

None of this changes the default, which is why it is safe to leave as a
lookup: N separate calls need no `n` support from anybody.

## Composing the set

A set is only worth paying for if the images differ in a way a buyer would
notice. Four renders of "a nice photo of this product" is one image billed
four times.

Name each image's job before writing any prompt. The usual axes, and a request
usually picks one of them rather than mixing:

| Axis | A four-image set looks like |
|---|---|
| **Background / setting** (the commonest reading of "different styles") | pure white catalog; a warm wooden surface; a soft grey studio sweep; a lifestyle scene where the product is in use |
| **Lighting treatment** | even softbox; hard directional with a defined shadow; backlit rim; moody low-key |
| **Framing** | full product on white; three-quarter hero; a macro of one feature; a scale shot next to something familiar |
| **Seasonal / campaign** | plain evergreen; summer; winter; gift |

Two rules for the list you settle on:

- **Keep one image plainly on white**, whatever else the set does, unless the
  user has ruled it out. Every marketplace wants one, and it is the image the
  others are judged against.
- **Vary one axis, not three.** A set that changes background *and* framing
  *and* light gives the user four unrelated pictures instead of four options.

## Writing each image's prompt

### On the edit route — the shape that keeps the product itself

Same two-sentence discipline
[`image-edit`](../image-edit/SKILL.md) is built on, and here the second
sentence is what makes the set a set:

```
<The new setting, lighting and surface, described concretely.> Keep the product itself exactly as it is — shape, proportions, colour, material, and every printed word and logo on it — and do not move or re-frame it.
```

Four prompts for a four-image set differ **only** in the first sentence. The
second is byte-identical across all four, and it is the thing standing between
a set of options and four pictures of four slightly different products.

Worked, the background axis:

```
1. Place the product on a pure white seamless background with even studio softbox light, a soft contact shadow directly beneath it and nothing else in frame. Keep the product itself exactly as it is — shape, proportions, colour, material, and every printed word and logo on it — and do not move or re-frame it.
2. Place the product on a warm oak surface against a softly blurred neutral wall, with soft late-afternoon light from the left. Keep the product itself exactly as it is — ...
3. Place the product on a light grey studio sweep with a gentle gradient behind it and a soft true reflection beneath it. Keep the product itself exactly as it is — ...
4. Place the product on a kitchen counter beside a linen cloth and a small plant, in soft daylight from a window out of frame. Keep the product itself exactly as it is — ...
```

**Why the "keep" sentence is worth its length**, and where the evidence stops:
`ofox-image-core` measured this endpoint genuinely editing rather than
redrawing — a UI screenshot asked for one button colour change returned every
string verbatim, with mean absolute difference 5.27/255 overall against 84.27
inside the button, a region that is 1.1% of the frame carrying 58% of all
substantially-changed pixels. Replicated three times, on **one model**, on
inputs with hard edges and flat colour. That is what makes "leave the product
alone" a reasonable thing to ask for. It is not a promise that your product
survives, which is why the set gets checked below rather than trusted.

**And the set claim itself has now been run — this skill's core sentence
held.** 2026-09-17, one real 1792x1008 product photograph, three edits
differing only in the first sentence (pure white; warm oak; grey sweep), the
"keep" sentence byte-identical across all three, about 1.6 cents each. Put
side by side, the wordmark's glyph shapes, letter spacing, position and
relative size; the copper knurl and the two polished rings; the brushed
vertical grain; and the waist taper are **the same in all three**. That is
the thing this file promises — every image is an edit of one photograph, not
three independent re-inventions of it — and it is a measurement now rather
than an inference from a UI screenshot.

⚠️ **What the same three images exposed, which this file had not said: the
framing is not locked.** The "keep" sentence protects the product's identity;
it does **not** hold the product's size within the frame. The oak image came
back visibly larger in frame than the white one, and the grey-sweep image
slightly narrower. Nothing was cropped or distorted — the subject simply sits
at a different scale. `--target-aspect` governs the **frame's shape** and has
nothing to say about this.

So for a marketplace set that has to line up — a grid where the product must
appear the same size in every tile — treat scale consistency as **unsolved
here**, tell the user before they pay, and plan to normalise it in an image
editor afterwards. Adding "do not move or re-frame it" to the prompt (this
file already does) did not deliver it. One run of three images, one model,
one product.

⚠️ **Printed text is the part to check hardest.** What is measured is that
existing strings *survive* an edit aimed elsewhere. Nothing measures the
endpoint preserving a label through a change to the whole scene around it, and
nothing at all measures it writing new text correctly. If the label has to
read right, that is a check on every image in the set, not a hope.

### On the generate route — the shape for a product that does not exist yet

No input image, so every image is an independent roll and the product will
drift between them. Write the product block identically in all four prompts
and vary only the scene, which narrows the drift without removing it:

```
<Product, in physical words: material, finish, colour, geometry, any structural points.> <The setting, lighting and surface.> No printed text, no logo, no engraving and no marking anywhere on it.
```

Three notes, all borrowed rather than measured here:

- **Physical words, not adjectives** — `matte off-white glazed ceramic,
  straight-sided cylinder, curved handle`, not "an elegant mug". This is
  `seedance-product-video`'s PRODUCT-block rule and it is the same problem.
- **A description is honoured; a number attached to it is not.** That skill
  measured `three interleaved knuckles` rendering as four. If a countable
  feature matters, check it rather than writing it harder.
- **The no-text declaration plus a per-carrier negative list** is what has
  actually produced text-free product renders in this repo — on video, three
  times. It is an inference here, not a measurement, and it only covers the
  surfaces you name.

## The shape of the set, and where it comes from

**On the edit route the output's shape follows the input's**, measured on one
model over four runs: 854x480, 320x180 and 1792x1008 all returned 1672x941,
and 256x256 returned 1254x1254 — a near-constant ~1.57 MP spent on whatever
shape it was handed, and **spent in both directions**, since the 1792x1008
input is larger than the output it came back as. Whether `--size` is honoured
on this endpoint is **untested**.

So for a marketplace set that has to be square:

1. **Crop the source photo to the target ratio before the first call.** Every
   image in the set then arrives at that ratio, and the crop also cuts the bill
   — the uploaded picture is billed.
2. **Pass `--target-aspect 1:1`** (or whatever the platform wants) as the
   guarantee: the script measures the written file and centre-crops it, or
   fails loudly rather than handing back an almost-right one. It needs
   `ffmpeg`/`ffprobe`, and fails as exit `2` **before** anything is spent if
   they are missing.

Do both when the shape is load-bearing — the crop gets you there, the flag
proves it, on every image in the set rather than on the one you happened to
look at.

**On the generate route the shape is `--size`**, whose enum has no 16:9 or
9:16 entry at all; `--target-aspect` covers that gap the same way. Detail:
`ofox-image-core`'s "The size enum cannot express 16:9 or 9:16".

## Before writing anything: the brief

The shared rules for asking — the three tiers, one round of at most four
questions, the "Let the AI decide" discipline, the order with the approval
gate, the fallback for a runtime without `AskUserQuestion` — are in
[`../ofox-video-core/references/creative-brief.md`](../ofox-video-core/references/creative-brief.md).
Every rule there about *how* to ask carries over; its question content does
not. This is this scenario's own set.

| Tier | product-image axes |
|---|---|
| **must-ask** | is there a photo of the real product (it decides the route and what can be promised), and what varies across the set |
| **ask-if-open** | how many images; the delivery shape |
| **never-ask** | the model, `--quality`, `--output-format`, `--background`, whether to use `--n`. The model comes from the chain and is named in the cost table; the rest are settled below. **One exception**: on the generate route `--quality` defaults to `low`, but if the user says the renders are the finished artwork rather than proposals, it stops being a default and becomes two priced rows in the cost table — see the ⚠️ section under the approval gate |

### The question set

| # | Tier | `header` | Question | Options (1 = recommended) | Ask when |
|---|---|---|---|---|---|
| 1 | must-ask | `Photo` | Do you have a photo of the actual product? With one, every image in the set is an edit of that same photo, so the item stays itself. | **Yes — a local path (recommended)**: the edit route. / **No — describe it in text**: fine for a generic or fictional product; for a real item the set will not be four pictures of the same object, and I will say so. **No AI option** — a photo that does not exist cannot be invented. | No image attached and the user did not say there is none. |
| 2 | must-ask | `Vary` | What should differ between the images? | **Background and setting (recommended)**: white, wood, studio sweep, lifestyle — the usual reading of "different styles". / **Lighting treatment**: same scene, four looks. / **Framing**: full shot, hero, macro detail, scale. / **Seasonal or campaign**. **No AI option** — this is what the set is. | The request says "different styles" or "a few options" without saying of what. |
| 3 | ask-if-open | `Count` | How many? | **4 (recommended)**: enough to choose from without paying for a crowd. / **2** — a straight comparison. / **6** — a spread. / **Let the AI decide** — 4. Every image is one more line on the bill, linearly. | The user said "a few" or "some" rather than a number. |
| 4 | ask-if-open | `Shape` | What shape do these need to be? | **Square 1:1 (recommended)**: what most marketplace grids want. / **4:5 for a social feed**. / **16:9 for a site banner**. / **Same as the source photo**. / **Let the AI decide** — 1:1. | The destination is not stated and the source is not already the right shape. |

### Skip rows specific to this scenario

On top of the generic rows in `creative-brief.md`:

| Input says… | Axis | Value |
|---|---|---|
| a photo is attached, or a path is given | Photo | edit route; do not ask whether there is one — but **open it and confirm it shows the product** before using it. The path is the answer to "is there a file"; only looking answers "is it the product" |
| "white, wood, and in a kitchen", any list of settings | Vary | background — and the list is the set |
| "different lighting", "brighter / moodier versions" | Vary | lighting |
| "close-up too", "one showing the detail" | Vary | framing |
| a number ("4 images", "a couple") | Count | that number |
| Amazon, Etsy, Shopify, eBay, "listing", "main image" | Shape | 1:1 |
| Instagram, "feed post" | Shape | 4:5 |
| "banner", "hero", "site header" | Shape | 16:9 |

### The recap for this scenario

```
Brief:
- Photo: /Users/me/shop/kettle.jpg (given), 2000x2000 — I will crop to 1:1 first (already square, no crop)
- Vary: background — white / oak / grey sweep / kitchen scene (you listed three, I added the grey sweep)
- Count: 4 (you said)
- Shape: 1:1 (inferred from "Etsy")
- Route: edit, four calls, one per background — the product stays the same photo in all four
```

Then all four prompts in full, then the cost table with its total, all in one
message. The user approves the set, the prompts and the price together.

## Before you spend: the approval gate, and the total

**Never send the first image until the user has seen a cost table for the
whole set and said yes.** The rule, the required columns and where the numbers
come from are written down once for every Ofox skill in this repo:
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
(directory-name caveat and probe: "Where the core skill lives" above). Its
**`Batches get an itemised table, not one total`** section is the one that
governs this skill.

Four things this scenario has to get right:

1. **Quote the set's total, itemised one row per image.** Never the per-image
   figure on its own. If one image in four is usable, that image cost the
   whole total; the per-image number understates it by 4x. This is the same
   rule [`shorts-reels`](../shorts-reels/SKILL.md) follows for video batches,
   for the same reason.
2. **The whole set commits at the yes.** These calls take seconds each, so all
   four bills land together. The cost table is the only place the set can be
   stopped.
3. **A re-roll of one image is a second approval**, with its own row. Don't
   fold "and we'll redo any that miss" into the first table as though it were
   priced.
4. **On the generate route, show both `--quality` rows** — see the ⚠️
   subsection that closes this one. It is the one flag in this skill that
   moves the set's total by more than an order of magnitude, and it must not
   be picked silently when the renders are the deliverable.

Get every number from `--dry-run`, which validates, resolves the model, builds
the request and prints an estimate — then returns, before anything is sent.
No key needed:

```bash
bash ../ofox-image-core/references/ofox-image.sh edit --dry-run \
  --image /absolute/path/to/kettle-square.jpg \
  --prompt "<style 1's prompt>" \
  --target-aspect 1:1 \
  --out-dir /absolute/path/to/out --out-name kettle-white
```

**Dry-run each image, not one of them.** On the edit route all four share the
same input file and near-identical prompt length, so the four estimates are
usually the same figure — but "usually" is not a basis for a price a user is
approving, and a per-image estimate is the only thing that lets the table be
itemised honestly. It costs nothing.

Then sum them into the table's total, **relaying each `Estimated cost:` line
as it prints** — never a figure of your own, never a cents-per-image number
copied out of this file. The line carries the conditions it was matched on and
how rough it is; a number lifted out of it loses both. Alongside the total,
the table needs the resolved `MODEL`, the input's measured size, and all four
prompts in full.

⚠️ **On the edit route the source photo's size is the set's cost lever, and a
set multiplies it by N.** The uploaded picture is billed per image, and on a
large source it is most of the bill: a 1792x1008 input bills 1508 image
tokens, `1508 * 0.000008 = 0.012064`, which is **74%** of that edit's
0.016249. Four images at that size is ~6.5 cents against ~2.4 for four
854x480 ones. Cropping the source to the target ratio before the first call —
which this file already tells you to do — cuts every image in the set, not
just the first. `ofox-image-core`'s `references/pricing.md` → "Measured edits"
has the four measured points.

Afterwards the **actual** bill is the sum of the `EDIT_COST` (or `IMAGE_COST`)
lines the real runs print, computed from each response's own token counts.
Report the total as money, say how many images it covers, and note the
script's own caveat that `EDIT_COST` is the **dearer** of two readings of the
same token counts, because no invoice has settled which is right.

### ⚠️ On the generate route, `--quality` decides the set's whole cost profile

`--quality` is **required** on `generate` (and only there — omit it on `edit`).
The skill cannot leave that to chance, because the two values a caller would
reach for first are not in the same price bracket. Both rows below are what
`--dry-run` printed on 2026-09-15 for a four-image set at `--size 1024x1024`,
on the chain's resolved head `openai/gpt-image-2` — free, no key, no request
sent:

| `--quality` | Per image, as the gate quotes it | A set of four | What the number is |
|---|---|---|---|
| `low` | ROUGH, ~0.59 cents | **~2.4 cents** | An **anchor measured at this request's own pair** (2026-09-02, `low` + `1024x1024`), which is the only condition under which an image estimate means much |
| `medium` or `high` | ROUGH **UPPER BOUND**, ~15.19 cents | **~61 cents** | **No anchor exists at either pair.** The gate falls back to the dearest of the model's two measured points (2026-09-04, `high` + `1792x1024`) and quotes it as a **ceiling**, deliberately erring high |

⚠️ **That table is for choosing, not for quoting.** It is a snapshot of one
model on one day, and the chain's head moves. The figures a user approves come
from `--dry-run` on the actual request, every time — the rule above ("never a
cents-per-image number copied out of this file") applies to these two numbers
as hard as to any other.

**Read the 26x honestly — it is a spread in the quote, not a measured spread
in the bill.** The model's two measured points really are about 26x apart in
output tokens (196 against 5063), and the script says so itself. But nothing
has been measured at `medium`/`1024x1024` or `high`/`1024x1024`, so the
15.19-cent figure is a bound, and the actual bill could land well under it.
Say it that way to the user: *"at `high` I can only quote you a ceiling, and
the ceiling for four is 61 cents; at `low` I have a real measurement and it is
about 2.4 cents."* Never present the ceiling as a price, and never quietly
substitute a cheaper guess for it.

**The default is `low`,** and it is a default rather than a question because
of what the generate route is *for*: this route exists only for a product that
has no photo (see the first section), so the set is a batch of style proposals
to choose between, not final listing artwork. `low` is the value with a real
measurement behind it and the one the cheap-first discipline in this repo
points at.

**Override it when the user says the renders are the deliverable** — final
artwork rather than proposals. Then the choice belongs to them, so put both
rows in the cost table rather than picking: the ceiling for the set at the
dearer value, the measured total at `low`, and the sentence that the dearer
one is a bound. That is the only place in this skill where the cost table
carries two options instead of one total.

Two things that follow and are easy to get wrong:

- **`--quality` is a per-model enum, validated by the dry run** against the
  model the request will actually use (since `ofox-image-core` 1.7.0). Do not
  hardcode a value on the strength of one model accepting it — five
  copy-pasteable commands in this repo said `--quality standard` and broke the
  day the model chain's head changed. `low` is a recommendation to pass, not a
  value to assume is accepted; let the dry run confirm it.
- **None of this applies to the edit route**, which is the common one. There
  `--quality` is not required, it is not validated by the endpoint, and a typo
  in it renders and bills anyway — so omit it entirely.

## Running the set

One call per image. Same input file, same `--out-dir`, a distinct
`--out-name` each time so the results are legible later:

```bash
IMG=/absolute/path/to/kettle-square.jpg
OUT=/absolute/path/to/out

bash ../ofox-image-core/references/ofox-image.sh edit \
  --image "$IMG" --prompt "<style 1's prompt>" \
  --target-aspect 1:1 --out-dir "$OUT" --out-name kettle-white

bash ../ofox-image-core/references/ofox-image.sh edit \
  --image "$IMG" --prompt "<style 2's prompt>" \
  --target-aspect 1:1 --out-dir "$OUT" --out-name kettle-oak
# ...one per style...
```

**Stop after the first one and look at it.** It is one image's worth of money
to find out that the instruction was misread, and three images' worth to find
out afterwards. If image 1 is right, run the rest; if it is not, fix the
prompt shape and re-price.

For the generate route the shape is the same, one call per style:

```bash
bash ../ofox-image-core/references/ofox-image.sh generate \
  --prompt "<style 1's prompt>" --quality low --target-aspect 1:1 \
  --out-dir "$OUT" --out-name mug-white
```

**`--quality low` is not decoration in that command** — it is required on
`generate`, and it is the difference between a four-image set quoted at ~2.4
cents and one quoted at a ~61-cent ceiling. The reasoning, both priced rows,
and when to hand the choice back to the user are in "⚠️ On the generate route,
`--quality` decides the set's whole cost profile" above. Pass it explicitly and
let the dry run validate it against the resolved model, which since
`ofox-image-core` 1.7.0 it does for free.

### Reporting the set

- **Every `IMAGE_PATH` on its own line**, absolute, grouped as a list with the
  style each one is. The paths are the deliverable; the user should not have
  to re-derive your working directory.
- **The total cost, and how many images it covers.**
- **Any `MODEL_FALLBACK_*` or `MODEL_SOURCE request` line**, relayed rather
  than swallowed — the first means something dearer may have run, the second
  means the API did not confirm the model the price is computed at.
- **`SIZE_ACTUAL`, not `SIZE`.** `SIZE` is printed straight from the response
  and this API has a recorded history of that field disagreeing with the file
  on disk.

## Check the set before you hand it over

`STATUS completed` means each request was accepted and a file was written. For
a set it does not answer the question that matters, which is not "did four
images arrive" but **"are these four images of the same product"**.

Check, in this order:

1. **Product identity across the set.** Put all four next to the source and
   compare the same features in each: shape and proportions, colour and
   material, every printed word and logo, any distinctive part (a handle, a
   hinge, a cap). Pick the features *before* looking, so you are comparing
   rather than being reassured.
2. **The white image, hardest.** It is the one a marketplace will actually
   reject, and a plain background makes a wrong shadow or a cut-out edge
   obvious.
3. **The labels at magnification.** Text is the first thing to go soft, and a
   listing image with a plausible-but-wrong wordmark is worse than one with
   none.
4. **The shape, on every file.** `SIZE_ACTUAL` on each, not the one you
   happened to open. With `--target-aspect` the script has already guaranteed
   it; without it, this is the check that was skipped.
5. **How big the product sits in each frame** — and expect this one to fail.
   Measured (see "Why the 'keep' sentence is worth its length"): identity held
   across three edits and **scale did not**. Nothing in the prompt or the
   flags controls it, so this is a check that ends in an editor rather than a
   re-roll. Say it at the gate, not at hand-over.

**A wrong image is a spent call.** There is no job id and no poll on this API,
so the repair is a new call with a better prompt, priced again as its own row.
That is the argument for stopping after image 1, not an argument for accepting
image 3.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| Route | `edit` when there is a real photo; `generate` only for a fictional or generic product | The only thing that keeps one product identical across a set is starting every image from the same picture |
| Calls | **one per image** | The price is the same as `--n` (measured), and separate calls buy per-image prompts, an early stop, and independent re-rolls |
| `--n` | **omit it** | Reach for it only when the user wants several rolls of one style. Not a discount; refused outright by at least one model |
| `--model` | **omit it** | `ofox-image-core` resolves its cheapest-first chain against the endpoint being used and reports any fallback. Pass one only when the user named one |
| `--quality` | **omit on `edit`**; on `generate` it is required — **`low`** | Not required on edits, and since that endpoint does not validate the value, an omitted flag cannot be a typo. On generations it is the single flag that moves the set's total by more than 10x: a four-image set quotes ~2.4 cents at `low` (a measured anchor) against a ~61-cent **ceiling** at `medium`/`high` (no anchor at that pair). See "⚠️ On the generate route, `--quality` decides the set's whole cost profile" — and let the dry run validate the value against the resolved model either way |
| `--target-aspect` | the platform's ratio, on **every** image | A set whose images are not all the same shape is not a set. The script guarantees it or fails; `--size` is untested on edits |
| `--size` | omit on `edit`; on `generate`, the enum value that survives the crop with the most pixels | The edit output's shape follows the input's. On generations `--target-aspect` picks the size for you |
| `--out-dir` | **always, absolute** | Without it the files land in whatever directory you happened to be in — which, given the examples run from this skill's own directory, means inside an installed skill |
| `--out-name` | one per image, naming the style | `kettle-white`, `kettle-oak`. A set of timestamp-named files is unusable a day later |

## Pricing a set with no API key

All of these work with `OFOX_API_KEY` unset:

```bash
bash ../ofox-image-core/references/ofox-image.sh models --endpoint edits
bash ../ofox-image-core/references/ofox-image.sh edit --dry-run --image FILE --prompt "..." --out-dir DIR
bash ../ofox-image-core/references/ofox-image.sh generate --dry-run --prompt "..." --quality low
```

So a user who has not signed up can see the whole set priced before deciding
whether to register. **Quote it first; don't open with a signup link.**

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
here becomes unusable when a link misses — the routes, the question set, the
prompt shapes and the defaults are all written out in this file. What is lost
is the gate's exact wording, which still applies, and `ofox-image-core`'s
depth on the API itself.

## Exit codes worth knowing

Full table in [`../ofox-image-core/SKILL.md`](../ofox-image-core/SKILL.md).
The ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `0` | Success, **or** a `--dry-run` that spent nothing | Read `STATUS` to tell them apart |
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely. A source file that is not jpeg/png/webp, a `--quality` typo, `--n` on a model that refuses it, and a `--model` that does not serve the endpoint all land here |
| `2` | Environment problem — `curl`/`jq`/`OFOX_API_KEY` missing, or `ffmpeg`/`ffprobe` missing while `--target-aspect` was passed | Ask the user to fix it; `check` reports the same. Nothing was attempted, so the set has not started |
| `3` | The API rejected it, the response couldn't be parsed, or a `--target-aspect` target couldn't be met | Read the upstream message. An upstream rejection (`endpoint_not_supported`, `model_not_found`) is free and only reaches here when the local catalog check was skipped or fell back to a snapshot; a crop that couldn't be met means **that image was generated and billed** and is on disk at the `-uncropped` path |
| `4` | `--out-dir` could not be created or entered | Caught before any network call. Fix the path and retry — no money spent finding out. Worth hitting on image 1 rather than image 4, which is another reason to dry-run all of them first |
| `5` | Ambiguous network failure — no HTTP response at all | There is no job id to look up. Do **not** auto-retry that image; tell the user to check `https://app.ofox.ai`'s usage history, and do not start the rest of the set until they have |

## Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| The four images are four different-looking products | The generate route was used for a real item. Measured: two renders of one mug prompt came back with different proportions, scale and light | Switch to the edit route with a photo of the real product. For a genuinely fictional product this is expected — say so before spending, not after |
| The product changed inside one image of an edited set | One roll. The endpoint edits rather than redraws on the runs measured, but that is four runs on one model and is not a guarantee | Re-run that one image with the keep sentence made more specific (name the features, not just "the product"). A new call, so a new row on a new table |
| A label or logo went soft or wrong | Text is what degrades first, and nothing here measures a label surviving a whole-scene change | Check every image at magnification before delivering. If the label has to read exactly right, composite it back in an editor — [`hal-image`](../hal-image/SKILL.md) does that locally and free |
| The images are not all the same shape | `--target-aspect` was passed on some calls and not others, or the source was not cropped and `--size` was relied on | Pass `--target-aspect` on every call in the set. `--size` is untested on the edits endpoint; the output's shape otherwise follows the input's |
| Exit `1` on `--n` | The chosen model refuses `n` outright — `google/gemini-3.1-flash-image` does, even at `n: 1` | Omit `--n`. This skill's default route doesn't use it; nothing was submitted, so it is free to fix |
| Exit `1`, "exists but does not serve /v1/images/edits" | A model that cannot edit was pinned, caught locally against the catalog's `supported_endpoints`. Nothing submitted | `models --endpoint edits` lists the ones that can, read live. Usually the fix is to stop passing `--model` at all. Reaching the API instead returns `endpoint_not_supported`, also free |
| The bill was bigger than expected | The set is N bills, and on the edit route each one includes the uploaded picture. Input tokens are **not** linear in pixels — 854x480 bills 576 image tokens where 256x256 bills 256 | Nothing to fix after the fact. Next time: dry-run every image with the real file, show the total, and crop the source smaller if the deliverable is small |
| A `--quality` typo on an edit rendered and billed anyway | The edits endpoint does not validate the value; measured on six models | Prevention only: `--dry-run` first, which rejects it locally, and omit `--quality` on edits entirely |
| Half the set is good | Expected — that is what a set is for | Re-roll only the misses, each as its own row on a second cost table. Do not re-run the whole set |
| Exit `5` partway through a set | No HTTP response at all on one image; there is no job id to check | Stop the set. Have the user check `https://app.ofox.ai`'s usage history before any further calls — the ambiguous one may or may not have billed |

## When NOT to use

- **One change to one image.** "Change this photo's background to a beach" is
  [`image-edit`](../image-edit/SKILL.md) — one in, one out, with the craft for
  what survives an edit. Come here when the answer is a set.
- **The deliverable is video.** A product photo becoming catalog footage is
  [`seedance-product-video`](../seedance-product-video/SKILL.md), which owns
  the orbit, the turntable and the literal-accuracy prompt craft, and which
  has its own documented text-only route for fictional products. A cinematic
  brand spot is [`seedance-ad-creative`](../seedance-ad-creative/SKILL.md).
  **If the user wants both a set of stills and a clip, they are two jobs with
  two cost tables** — and note that an image attached to a video job forces
  the clip's ratio to follow the image's, so the video skill owns the crop
  decision rather than inheriting one made here.
- **One plain render from text**, with no set and no product to keep
  consistent. That is `generate` and belongs to
  [`ofox-image-core`](../ofox-image-core/SKILL.md) directly, as that skill's
  own description says.
- **Character images for an anime video sequence.**
  [`seedance-anime-drama`](../seedance-anime-drama/SKILL.md) generates those
  itself and carries the machinery that keeps one character consistent across
  shots; images made outside that flow are not tracked by it.
- **The user is driving the API directly** — naming low-level parameters,
  debugging a failed request. `ofox-image-core` is the skill for that; this
  one adds set composition, not API surface.
- **The change has to be exact** — a supplied logo dropped in, a specific hex
  background, a pixel-accurate crop, text that must read correctly. A
  generative render is not a compositing operation.
  [`hal-image`](../hal-image/SKILL.md) does that locally, deterministically
  and for free.
