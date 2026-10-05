---
name: clone-image-ad
metadata: {packVersion: 1.3.0}
description: >-
  Clones a STATIC IMAGE ad into finished ads for your own product, into a reusable prompt
  TEMPLATE, or both — the template is what makes the ads and the ads are what prove the
  template. Round-trips the frame through gpt-image-2, nano-banana-pro or reve-2.1 until
  it reproduces, replaces every brand-specific with a {placeholder}, then fills it with
  your product pinned to a real photo. Use for "clone this ad for my product", "rebuild
  this competitor's ad for us", "make me ads like this", "reverse engineer this ad",
  "make this ad reusable", "add this to my prompt library", or "clone my competitors'
  ads" with NO file attached — it sources one via spy-competitor-ads rather than asking
  which. **Among cloners the source's medium decides**: a still, or nothing attached, lands
  here; "clone this ad" plus a VIDEO is clone-video-ad. NOT for generating an ad from a brief
  (chatgpt-image-ad, nano-banana-image-ad), nor animating a still as-is
  (image-to-motion). Refuses to render your product without a real photo of it.
---

# clone-image-ad

Take an existing image ad and turn it into a reusable, parameterizable prompt template that
gets appended to the shared **40-template image-ad library**. The template is validated by
round-tripping it through a Novoads image model and comparing against the original.

## If the `shared/` files are not on disk

Then this skill was installed on its own from skills.sh, and the library it is supposed to append
to came with nothing. Fetch each missing file from
`https://raw.githubusercontent.com/novoads/agent-skills/main/<path>`, where `<path>` is one of
`shared/skills/clone-image-ad/prompting/guide.md`,
`shared/skills/image-ad-prompting/prompting/template-format.md`,
`shared/skills/image-ad-prompting/prompting/prompt-library.md` and
`shared/skills/image-ad-prompting/OVERVIEW.md`. Cloning the whole pack with
`git clone https://github.com/novoads/agent-skills.git` is the better move here, because the
deliverable is an entry written back into `prompt-library.md` and a raw fetch gives you nowhere to
save it. That install has no `scripts/check-novoads-env.sh` either, so set `NOVOADS_API_KEY` in the
environment yourself and let the first call report the key.

## Read order

Paths below are **from the repo root**. This skill is copied into `.claude/skills/` and
`.cursor/skills/` by `sync-skill.sh`, so a relative link out of it would break in those copies.

1. **This file** — model choice, the validator, what's fixed at the repo layer.
2. `shared/skills/clone-image-ad/prompting/guide.md` — the full 10-phase workflow (visual analysis → draft prompt → generate-with-reference → iterate → generalize → test → cross-model validate → document → save).
3. `shared/skills/image-ad-prompting/prompting/template-format.md` — entry skeleton.
4. `shared/skills/image-ad-prompting/prompting/prompt-library.md` — destination for the new entry. 40 validated templates already there; new entries go at T40+.
5. `shared/skills/image-ad-prompting/OVERVIEW.md` — ecosystem context.

## Hard rules

Inherits all 8 hard rules from the shared guide (strip platform chrome, validate by generating,
test the generalized version, no brand-specific text in the final template, a v1 clone is never
publishable, never silently overwrite, document model notes, price the whole run up front). Plus:

8. **Model is one of `gpt-image-2`, `nano-banana-pro`, `reve-2.1`.** Those are the three image models on this API. The choice happens in Phase 1 once the user picks (or the agent auto-detects).
9. **Never write a `Model notes` claim for a model you didn't actually run.** Mark it `untested`. An invented note is worse than a missing one.

10. **A v1 faithful clone never leaves this workflow.** Phase 4 reproduces the source *including* its wordmark, registered marks and any real customer testimonial — that is what makes it a structural check, and it makes it unpublishable. It is evidence, never creative: not into an ad account, a deck, a post or a case study. **Phase 6 is where brand-specifics and real testimonials die.** Invent the test fill; never inherit a real person's quoted review.

## Phase 0 — the deliverable, the reference, and the product

Three questions, answered before anything else. Two of them you answer yourself.

### 0a. Ads or a template?

The same ten phases produce both. What changes is which one is the point.

| They said | Mode | Phase 7 fills with | You hand back |
|---|---|---|---|
| "clone this ad **for my product**", "make me ads like this", "rebuild this for us" | **ads** | **their own product**, three variants | 3 ready-to-run ads **and** the library entry |
| "turn this into a **template**", "make this reusable", "add it to my library" | **template** | a different brand, one render | the library entry (the test render is evidence) |

**Ads is the default when the ask names their product or says nothing about reuse.**
Someone who asks to clone an ad wants an ad; the template is what we keep.

The extra ads cost two more renders than the template run needs — quote them in the
Phase 4 estimate, not after. Everything else is shared, which is the point: the
faithful v1 is the structural check either way, and **the three filled variants are
themselves the proof the template generalises**, so ads mode does not pay for Phase 7
separately.

**In both modes the library entry gets written.** It is not an optional extra in ads
mode: Phase 4 reproduces the source *including* its wordmark, registered marks and any
real customer testimonial, and Phase 6 is where those die. Skipping the write-out does
not skip a nice-to-have, it leaves the competitor's marks alive in the only artifact
anyone keeps.

### 0b. Is there a reference?

**Handed one** — a path, an attached image, a still already in `outputs/` — clone it.
Do not sweep. Someone who handed over an image has already answered the question a
sweep would ask.

**Not handed one — do NOT stop and ask "which ad?".** That puts the work back on the
user at the moment they asked us to do it. Run `spy-competitor-ads` in image mode, and
say what you are about to do in one line with a price and a way out:

> No ad attached. I'll sweep Arcads, Creatify and Icon for their **static** ads and clone
> the strongest. N credits for the sweeps; I'll price the renders before they run. Say
> "stop", say "video" for their video ads instead, or drop your own image.

- **Statics are the default, and the line says so.** A bare "clone my competitors' ads"
  lands here rather than on `clone-video-ad` for two reasons that point the same way. The
  render is the expensive half and a static costs a fraction of a video. And the sweep's
  `count` maxes at **20 whatever mode you ask for**, so a mixed sweep spends those 20 on a
  split the user did not choose — measured 2026-08-10, `"all"` came back **20 video, 0 static**
  for one brand. Asking for one kind gets you 20 of that kind. Naming the video escape in the
  same breath is what keeps the default honest — the user picks in one word instead of being
  asked a question.
- **"video" means a SECOND sweep, and say so before firing it.** There is nothing to hand
  over: the first sweep ran in image mode, so it holds stills `clone-video-ad` cannot open.
  Switching media means sweeping again with `mediaType: "video"`, which costs what a sweep
  costs. Quote it from a live estimate, get a yes, then hand the new files to
  `clone-video-ad` and stop. Passing the statics along as if they answered the question is
  the failure this clause exists to prevent.
- **Quote the sweeps as sweeps.** The renders are priced at their own gate in Phase 4. A
  line that reads as the run's total while covering only the search is wrong even when every
  number in it came from a real estimate.
- **Name the competitors**, so a wrong guess is corrected before it is paid for.
- **The total comes from a live `POST /v1/estimates` in this session** — never a number
  from memory or from this file. N competitors is N charges and that multiplication is
  the whole quote.
- **One word stops it**, and the escape hatch is naming their own image instead.
- Default to **three** competitors when you picked them yourself; honor any list they name.

Then act. It is a proposal with a veto, **not a question and not a menu** — a menu makes
the user classify their own situation, which is the friction this branch exists to remove.
`spy-competitor-ads` hands back file paths and a ranked top three; take the top one unless
the user picked otherwise.

### 0c. Do we have the brand?

**First look at the source ad and answer two questions about the FRAME**, not about the business.

1. **Does it show a product?** A skincare bottle does. A price comparison in type, a testimonial
   card, a screenshot of somebody's dashboard: those do not.
2. **Does it carry a claim?** A number, a statistic, a named person's quote. Measured on four
   real Arcads statics, **every one did**: "300 Natural AI Actors", "6,000+ teams", "99%
   reduction in cost", a CMO quoted by name.

```bash
./scripts/brand-context.py check clone-image-ad --mode ads --product-in-ad yes|no --claims-in-ad yes|no
./scripts/brand-context.py check clone-image-ad --mode template          # asks for nothing
```

**A claim does not stop the clone — it gets labelled.** A number on a rendered ad is something
a person catches at a glance, and a gate that stops the work also stops the person who would
have caught it from ever seeing the ad. So the claims cross, and the hand-off **lists every one:
what the source said, what the clone says.** A figure that crossed silently is the one nobody
checks; a listed one is a decision.

Use `brand.claims` where we have a true equivalent — it makes the substitution real rather than
a rhythm-preserving guess. Its absence never blocks.

> Three claims carried into this clone — check them before it runs anywhere:
> • "300 Natural AI Actors" → "1,000+ AI actors"
> • "35 languages" → "5 languages"
> • "30% off first month" → "$49/month, cancel anytime"

**Never carry a real named person through.** "Ashvin Melwani, CMO at Obvi" in a Novoads ad puts
words in an identifiable person's mouth about a company he never mentioned. Replace him —
invented name, invented company, invented quote, in the same register and roughly the same
length as the source. What you must not do is keep his.

### Every zone ships finished

**A render never contains scaffolding.** No "Placeholder Name", no empty card, no grey skeleton
bars, no `{brand.name}`, no lorem, no `example.com`. If a zone needs a name, invent a plausible
one. If it needs a testimonial, write a plausible one. If it needs a domain, invent a plausible
domain.

This is not a style preference. A finished ad reading "Placeholder Name" is useful to nobody:
the person reviewing it cannot judge the layout past the word, and the person who ships it ships
the word. Blanking a zone is the same failure wearing a nicer coat — an empty white card is not
a decision, it is an unfinished ad.

The distinction that keeps this coherent: **a TEMPLATE carries `{slots}`; a RENDER never does.**
Template mode writes the slots into the library entry, and the image it validates with is still
filled in with plausible content.

`validate_image.py` refuses a prompt carrying scaffolding **before it charges**, so this cannot
reach a paid call. It was added after a render shipped reading "Placeholder Name" over
"agency.com · partner", beside a blank card and two grey bars.

**Then read the render back — the lint cannot do this part.** It matches the PROMPT, and the
two failures it cannot see are the ones that shipped: a slot-shaped *value* the pattern list has
not met yet, and a zone the prompt never named at all, which the model then fills however it
likes. Open every PNG and check three things: each zone carries real content, the wordmark is
spelled right letter by letter, and no text from the source brand survived. A blank or
slot-shaped zone means the **prompt** under-specified it — name that zone's content and re-run.
Never hand over an image you have not looked at.

**A product in the frame makes a real photo mandatory** — an image model will otherwise render
a plausible bottle with invented label text, which is the failure a viewer catches instantly.
**No product in the frame and it is never asked for**, because there is nothing to pin and
nothing to fabricate. The gate is derived from the ad, not declared from the business, which is
the whole reason a SaaS or an agency can use this at all.

The logo is the one thing required either way: every ad carries a mark, and that mark must
never be the competitor's.

### Getting the mark right — three rules, and the first one is why this exists

**1. Pass the files, do not describe them.** The render call takes them as reference images, in
this order, and the order is load-bearing — reference 1 is the strongest identity signal at the
provider:

```bash
REFS=()
while IFS= read -r r; do REFS+=(--image-ref "$r"); done \
  < <(./scripts/brand-context.py refs clone-image-ad)
# then pass "${REFS[@]}" to validate_image.py
```

**Build the array, do not interpolate a string.** `refs` prints one path per line for two
reasons, both found by getting them wrong: zsh does not word-split an unquoted `$(...)`, so a
joined flag string arrives as ONE argument and argparse rejects the lot; and a path containing
a space cannot survive being space-joined at all, which user folders routinely contain. The first real clone this pack produced came back with a **generic
white square** where the mark should be: `brand.logo` was stored, it *blocked* the run, and no
renderer ever received it. A gate on an asset nothing passes is worse than no gate — it charges
the user for a promise it does not keep.

**2. Spell the wordmark letter by letter in the prompt.** Image models mangle brand text more
reliably than anything else in a frame. Write it out: *the wordmark reads N-O-V-O-A-D-S,
"novoads", seven letters, lowercase*. Then check the render against the spelling, not against
your memory of it.

**Count the letters before you write the number.** This sentence shipped saying "eight" for a
seven-letter word — a miscount inside the one instruction whose whole job is to stop the model
miscounting. Spell the word out, count the spelled letters, then write the total.

**3. When it still comes back wrong, composite — do not re-roll.** Two bad wordmarks in a row
means the third will probably be bad too, and each one costs. Burn a clean logo PNG onto the
zone instead. **That is the reliable path to pixel-perfect brand text, not a fallback**, and it
is the one part of this workflow with a guaranteed outcome.

**No logo stored?** Omit the zone and say a logo overlay is available afterwards. Never invent a
mark and never leave the competitor's.

Exit 2 means blocked, and the output names exactly what is missing. **Ask for those and
nothing else**, then write each answer back so no later run asks again:

```bash
./scripts/brand-context.py set product.photo references/products/hero.png
./scripts/brand-context.py set product.description 'A 500ml insulated water bottle'
```

What blocks depends on the ad. In **ads** mode with a product in frame: `product.photo` and
`product.description`, hard. With no product in frame: the logo alone. In **template** mode:
nothing. Everything else — brand name, colors, fonts, tone — is used when stored and never
demanded.

**On a first run with nothing stored, offer the shortcut before the interview:**

> Drop your website and I'll draft the brand block from it — no credits, and you correct
> anything I get wrong. Or just give me a product photo and one line about it.

```bash
./scripts/brand-context.py from-url https://theirbrand.com
```

It writes nothing. Confirm each drafted line with the user, then `set` them. Its image
candidates are **candidates**: a site hero is usually a lifestyle shot with text burned
in, and this skill still needs a clean packshot.

Template mode does not need any of it — a template is filled with a stand-in brand by
design. Do not ask.

## Picking the model in Phase 1

Pick by what the reference ad is showing — most templates fall into one clear bucket.

**Use `gpt-image-2` when the reference is:**
- Typography-heavy / UI mimicry (Apple Notes lists, fake Google search, fake Slack threads, ChatGPT-conversation ads, iMessage screenshots, comparison tables, fake AirDrop dialogs, Hinge-style cards, calendar UI, weather forecast UI, magazine masthead)
- Brutalist / editorial typography heros (huge type makes the joke)
- Dense small text inside UI elements

**Use `nano-banana-pro` when the reference is:**
- Photoreal handheld objects (whiteboards, napkins, sticky notes, letter boards, scratch-off tickets)
- Aspirational lifestyle photography (sunset, kitchen at golden hour, OOH / transit)
- Multi-image reference blending (logo + product + style + character in one composition)
- Clay / claymation / Pixar-adjacent textures
- Anything at `3:2`, `3:4`, `4:3` or `5:4` — those ratios do not exist on `gpt-image-2`

**Use `reve-2.1` when:**
- The template rendered wrong on both of the above and you want a genuinely different interpretation rather than another tweak
- The user asks for it, or wants a third look before committing a template to the library

It is a deliberate choice, not a fallback tier, and it is the most expensive of the three per
image — so name it in the estimate when you use it.

**If the reference straddles buckets** (e.g. a UGC-style photo with rendered text overlays),
clone once and cross-validate in Phase 8, then ship the template with `Model notes` saying
which renders cleaner.

If the user explicitly names a model, honor that.

## The validator

This skill has its own caller: `skills/clone-image-ad/scripts/validate_image.py`.

```bash
./skills/clone-image-ad/scripts/validate_image.py \
  --model <gpt-image-2|nano-banana-pro|reve-2.1> \
  --prompt "$(cat prompts/<tag>-v1.txt)" \
  --aspect-ratio <ratio> \
  --image-ref <reference.png> \
  --pin-block "<one-line product description>" \
  --out iterations/clone-tmp \
  --env-file .env
```

**`--pin-block` is how the brand pin gets counted.** It wraps your description in the shared
library's standard 346-character guard — front face only, no invented label copy, no
fabricated claims — and measures the result against **the cap of the `--model` you named**
*before* the network, naming the pin block's share if it overflows. Those caps are 32,000 on
`gpt-image-2`, 50,000 on `nano-banana-pro` and 4,000 on `reve-2.1` (deployed spec 2.16.0,
verified 2026-08-08), so an overflow here is almost always a `reve-2.1` run. When it happens,
the script also names the roomier models: switching `--model` is usually the better repair,
because trimming loses clone fidelity the cross-check was meant to test. A clone run
that skips it inherits the failure it exists to prevent: unpinned marks come back invented.

Why a separate script rather than the generators': the two generator skills are **model-locked
by brand contract**, so a production run can't drift models by accident. Cloning has the
opposite requirement — Phase 8 exists to run the same template on a second model. This script
takes `--model`, applies that model's own aspect-ratio grid, and is the only path to
`reve-2.1`, which has no generator skill.

It shares everything else with the generators: the same three always-on safety suffixes, the
same upload flow, each model's own reference cap (`gpt-image-2` 4, `nano-banana-pro` 14,
`reve-2.1` 8), the same local prompt-length check before spending.

### Editing a source (Phase 7's second instrument)

`POST /v1/images` accepts `sourceAssetId` — **`gpt-image-2` only** — which repaints the zones a
prompt names and leaves the rest of the frame alone:

```bash
./skills/clone-image-ad/scripts/validate_image.py \
  --model gpt-image-2 \
  --prompt "$(cat prompts/<tag>-swap.txt)" \
  --source-image original-ad.jpg \
  --out iterations/clone-<date>/T40/test-fill \
  --env-file .env
```

`--source-asset-id` takes an id already uploaded, including one this API generated.

**Use it in Phase 7, not Phase 4.** Measured 2026-08-06 on one source, three renders: given the
full faithful-reproduction prompt an edit came back *worse* than the reference-image arm at the
same price, and given a short brand-swap prompt it held texture, grid, barcode, fine print and
lighting through a wordmark transplant in a single call. It also restyled a headline typeface
nobody asked it to change — pin the type in the swap prompt. Full write-up in the guide's Phase 7.

Two refusals happen locally, before any spend: `--aspect-ratio` alongside a source (an edit's
output tracks the source's shape, and the API 400s the pair), and a source on any model but
`gpt-image-2`. The source also spends one slot of the reference cap, because that is what it
becomes at the provider.

## Dependencies

- `.env` with `NOVOADS_API_KEY` (`novo_` + 64 hex). Verify with `./scripts/check-novoads-env.sh`.
- Optional: `PRODUCT_ID` in `.env`. Omit it and jobs land in your default product; `productId` is organizational only and does not influence what is generated.
- Python 3.12+.

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

The generator skills are **not** required to run a clone. They're where the finished template
gets used afterwards.

## Cost — read this before Phase 4

A clone is **six or more charged generations**: Phase 4, up to four Phase 5 iterations, the
Phase 7 test fill, and an optional Phase 8 cross-model run. Every one is billed and there are
no free re-rolls.

Price the run once, up front, with `POST /v1/estimates` (it charges nothing), and present a **range** — floor
is two calls, ceiling is the full iteration cap. Get one explicit yes covering the run. Do not
ask six separate times, and do not surface the cost only at the end.

The schedules differ by more than 3× across the three models, so **name the model** in the
estimate body — a Phase 8 cross-check on `reve-2.1` is not priced by a `gpt-image-2` estimate.

A **batch** (several references cloned in one conversation) prices the same way, once: one free
estimate per distinct final prompt, presented as one combined range, one yes covering the whole
batch — not a consent per reference.

Report the **actual total** from each response's `creditsCharged` when the run finishes.

**On a batch, that tally is not the ledger — reconcile against the balance.** Summing
`creditsCharged` by hand across many calls is right per call and wrong in aggregate the moment
one response goes missing (a retry that printed to stdout instead of the log is enough). Read
the `balance` that `POST /v1/estimates` returns **before the first charged call and again after
the last** — the estimate charges nothing, so this adds no cost — and report both numbers: the summed
`creditsCharged` and the balance delta. When they disagree, **the delta is the truth** and your
sum is missing a call; say so rather than reporting the smaller number.

## Aspect ratio mapping

| Ratio | `gpt-image-2` | `nano-banana-pro` / `reve-2.1` |
|---|---|---|
| `1:1` `2:3` `4:5` `9:16` `16:9` `21:9` | ✅ | ✅ |
| `3:2` `3:4` `4:3` `5:4` | ❌ | ✅ |

When measuring the original ad's aspect in Phase 2, map to the nearest ratio **the chosen model
accepts**. A `1.91:1` ad maps to `16:9` and post-crops downstream. A `4:3` ad is native on two
of the three and needs a mapping on `gpt-image-2` — which is on its own a reason to route that
template to `nano-banana-pro`.

Document any fallback in the template's `Aspect ratio:` field so future users know they're
rendering at a mapped ratio, not the original.

## Workflow phases (see the shared guide for full detail)

Phase 0 above runs first in both modes. Phases 7 and 10 are where the two diverge.

0. **Phase 0: Deliverable, reference, brand.** Ads or template; clone what was handed
   over or sweep for one; `brand-context.py check` and ask only for what blocks.
1. **Phase 1: Preflight + model choice.** Reference image resolves; `.env` has `NOVOADS_API_KEY`; validator located. **Ask which model to validate against** (or auto-detect).
2. **Phase 2: Visual analysis.** Describe the reference structurally — aspect ratio, format type, layout, typography, color palette, photography style, every text string verbatim, decorative elements, chrome to strip, and `[BRAND]` vs `[STRUCTURE]` for each.
3. **Phase 3: Draft v1 prompt** (brand-specifics intact). The three always-on safety suffixes take 1,575 characters off whatever the chosen model's cap is, leaving **30,425 on `gpt-image-2`, 48,425 on `nano-banana-pro`, 2,425 on `reve-2.1`**. On the first two, write the prompt the clone needs and stop thinking about length. On `reve-2.1`, 2,425 is the whole budget on default flags, and a faithful six-panel clone wants more than that. The validator prints the exact number when you overflow.
4. **Phase 4: Generate with reference.** Price the run and get a yes first. Pass `--image-ref <reference>` and the matched ratio. Blocks 60–90s; a render that answers `running` is polled by the script, never resubmitted.
5. **Phase 5: Compare and iterate.** Refine on the deltas. Cap 4 iterations. Track running credits.
6. **Phase 6: Generalize into placeholders** (`{brand.name}`, `{brand.color_primary}`, etc.).
7. **Phase 7: Fill the template and render.** **Ads mode:** fill with the user's own
   brand from `MASTER_CONTEXT.md`, pin the product to `product.photo` as a reference
   image, and render **three** variants at the source's ratio — image failure modes are
   independent enough that a roll nailing the product often misses the text. Those three
   are the deliverable *and* the proof the template generalises. **Template mode:** one
   render against a DIFFERENT, invented brand. Either way, if structure breaks, refine
   the placeholder set. Optionally cross-check by *editing* the original with
   `--source-image` and a brand-swap prompt — see the validator section.
8. **Phase 8: Cross-model validation (recommended).** Run the same template on another model. Document real deltas only.
9. **Phase 9: Document the template** per `template-format.md`.
10. **Phase 10: Save and confirm.** Append to the library, print the path, move PNGs to a permanent iteration dir, report total credits charged. **Ads mode also hands back the three variants** — which one you would run, what was preserved, what was swapped, and any copy still standing in. Say the library entry number in the same breath: two artifacts, one run.

## Iteration directory layout

```
<cwd>/iterations/clone-2026-08-01/
  T40-lifestyle-hero/
    prompt.txt
    v1.png, v2.png, …                # against the source ref (chosen model)
    test-fill-v1.png, …              # Phase 7 generalization test against a different brand
    cross-<other-model>/v1.png       # Phase 8 cross-model validation (optional)
    notes.md
```

## Common `Model notes` patterns to write in Phase 9

```markdown
**Model notes:**
- **gpt-image-2:** {e.g. "clean — strong on UI mimicry and table text"; "tends to add a 4th Slack message — keep the prompt explicit about exactly N"; "small chart axis labels blur — bump font size feel"}
- **nano-banana-pro:** {e.g. "strong — preferred for handheld board photos"; "weak on dense table text — keep rows to 4 max"}
- **reve-2.1:** {e.g. "untested"; "different composition read — wider crop, warmer grade"}
```

If you validated against only one model, say so explicitly:

```markdown
**Model notes:**
- **gpt-image-2:** validated clean (see iteration path)
- **nano-banana-pro:** untested — validate before using on that model
- **reve-2.1:** untested
```

This block is the difference between a portable template and one nobody knows how to use.
Don't skip it, and don't fill it in with guesses.

## Files this skill owns

- `skills/clone-image-ad/SKILL.md` — this file
- `skills/clone-image-ad/scripts/validate_image.py` — the model-aware clone validator

## See also

- `shared/skills/clone-image-ad/prompting/guide.md` — full 10-phase workflow
- `shared/skills/image-ad-prompting/OVERVIEW.md` — ecosystem context
- the **`chatgpt-image-ad`** skill — where a gpt-image-2 template gets used in production
- the **`nano-banana-image-ad`** skill — where a nano-banana-pro template gets used in production
- the **`novoads-api`** skill — the API contract underneath all of this
