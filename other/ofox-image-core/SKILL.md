---
name: ofox-image-core
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Shared execution layer for the Ofox image API (api.ofox.ai) — validates parameters client-side, sends one synchronous request, base64-decodes the result, saves it to a file, and reports the real usage token counts and the computed dollar cost. Does both text-to-image (generate) and editing an existing image you supply as a local file (edit — change the background, recolour an element, alter a product photo, while leaving the rest of the picture intact). This is a library skill, not a standalone user-facing one — it is meant to be invoked by scenario skills that build model/prompt/size choices for a specific use case and then call into this skill's script rather than re-implementing the API calls — image-edit owns "change this image so that...", product-image owns a set of product images to choose between, and seedance-anime-drama owns character images for a video pipeline. Load this skill directly only when a user explicitly names the Ofox image API, asks to call it with specific low-level parameters, asks to debug a failed Ofox image request, or wants a plain "generate an image of..." from text — which is the one common case no scenario skill covers.
license: MIT
version: "1.14.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-image-core
metadata:
  author: ofoxai
  version: "1.14.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🖼️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-image-core
---

# ofox-image-core: Ofox image API execution layer

Wraps the Ofox image generation API (`https://api.ofox.ai/v1/images/generations`)
behind one script: validate, request, decode, save, report real token usage.
Unlike `ofox-video-core`, this API is **synchronous** — one request either
returns the finished image(s) in the response body or fails outright. There
is no job id, no polling, and (because of that) no free "check what
happened" recovery path if a request goes wrong mid-flight.

## Safety contract (non-negotiable)

- **The script never reads a dotenv file.** `references/ofox-image.sh` resolves
  `OFOX_API_KEY` from the shell environment only, and the key is never
  hardcoded in a script or a skill file.
- **You may load the key from a dotenv file once the user has authorized it.**
  Locate it (`.env` at the repo root is the usual spot), then
  `set -a; . <path>; set +a` in the shell you'll call the script from. Sourcing
  a dotenv pulls in *every* variable in the file, not just the key —
  `OFOX_API_BASE_URL` is one this script reads, and it redirects every API call
  — so read the file before you load it. Never echo the value.
- **The key goes to exactly one host, and you are told when that host is not
  Ofox.** Since 1.14.0 `OFOX_API_BASE_URL` must be `https://` (a loopback host
  may be `http://`, for a local test server) and an override prints a `NOTE:`
  on stderr naming the host that will receive the key. Relay that line if you
  see it. Every request this script makes is built from that base — no URL out
  of a response body is ever fetched — so there is nothing else to check.
- **`edit --extra-form` will not read local files.** A value starting `@` or
  `<` is refused (curl reads those as "upload this file" / "send this file's
  contents"). Use `--image` to send an image; `--extra-form` is for extra
  *fields*.
- **Neither escape hatch can set a field that has a flag.** `--extra-json`
  (generate) and `--extra-form` (edit) are both refused for `model`, `prompt`,
  `quality`, `size`, `n`, `output_format`, `background` — and `--extra-form`
  for `image`/`image_url` too. Those are validated per model and priced
  *before* the hatch is applied, so a value arriving that way would change
  what is billed after the quote the user approved: `--extra-form "n=10"`
  printed `N 1` and asked for ten images. Pass them as flags.
- **Never print, log, or echo the raw key value** — not in chat, not in a
  file, not in a command you show the user, not in verbose curl output.
  `references/ofox-image.sh` never uses `curl -v`/`--trace` for exactly this
  reason (those would print the `Authorization` header). If you need to
  show that a key is configured, say "OFOX_API_KEY is set" — never the value.
- Never write the key into any file this skill (or a skill built on it)
  creates, including generated images' metadata, cost reports, or committed
  code.
- **Check once, then proceed.** Run the availability/key check at most once
  per session (see below). If it passes, don't re-prompt for the key on
  every subsequent call in that session.
- **Fail open on a missing key** — guide the user to get one, don't dead-end
  the conversation. A missing key means "can't call the paid API yet," not
  "stop talking to me."

## Which model: the priority chain

`bash references/ofox-image.sh models` lists every image model Ofox serves,
its per-output-token price, and the priority chain below together with the
model it resolves to **right now**. No API key needed — `GET /v1/models` is
public.

`--model` is optional. Omit it (or pass `auto`) and the script walks a
cost-per-image-ranked chain and uses the first model that is actually
available:

| | Model | Cost per image (measured — always at the pair named) | Why it is here |
|---|---|---|---|
| 1 | `openai/gpt-image-2` | **~0.6 cents** at `--quality low --size 1024x1024`; **~15.4 cents** at `--quality high --size 1792x1024` | cheapest per image at the one pair measured on both it and row 2, despite the higher per-token rate below — see the warnings |
| 2 | `microsoft/mai-image-2.5-flash` | ~2.0 cents at `--quality low --size 1024x1024` | second cheapest at that pair; was the chain's preferred model through 1.3.0 |
| 3 | `google/gemini-3.1-flash-lite-image` | not measured | tied with (1) on the per-token rate, but no per-image figure recorded yet |
| 4 | `microsoft/mai-image-2.5` | not measured | same vendor as (2), when quality matters more |

⚠️ **There is no such thing as "the" per-image price of an image model — every
figure above is only true for the `--quality`/`--size` pair beside it.**
Measured 2026-09-04: `openai/gpt-image-2` spends 196 output tokens at `low` /
`1024x1024` and **5063** at `high` / `1792x1024`, so the same model costs 0.6
cents or 15.4 cents depending on two flags — a **26x** spread. Quoting a bare
"~0.6 cents per image" for a large, high-quality frame is exactly the mistake
that produced a 15.4-cent bill against a 0.6-cent estimate. Since 1.7.0
`--dry-run` picks the measured point matching the request's own pair, and
falls back to the dearest one labelled `UPPER BOUND` when the pair has never
been measured — so the estimate no longer under-quotes, but a bare per-image
figure quoted from this table by hand still can. See "The estimate is rough,
and sometimes impossible" below.

⚠️ **This table is ranked by measured cost per image, not by the rate card's
per-output-token price** — the two rankings disagree here. At the one pair
measured on both models (`low` / `1024x1024`, 2026-09-02),
`mai-image-2.5-flash` spends 1024 output tokens against `gpt-image-2`'s 196,
so the more-expensive-per-token model is **~3.4x cheaper per image** (0.6
cents vs 2.0 cents), and that measurement is why the chain was reordered —
see "The 2026-09-04 reversal" below. The token counts are the measurement and
have not moved; the cents and the ratio are the vendor's rate card multiplied
through, and that moved on 2026-09-15 (this row read 2.67 cents and 4.5x until
Ofox cut `mai-image-2.5-flash`'s per-token rate by 25%). Two further limits on
how far the ranking reaches: rows 3–4 have no per-image measurement at all,
only the per-token rate; and **no like-for-like comparison exists at any other
pair** — the 26x within-model spread above is larger than the ~3.4x
between-model one, so "which model is cheaper" is a narrower claim than it
looks. **Do not re-derive the order from the rate card alone** — the
comparable figure is
rate x that model's own measured token count at the pair you intend to run.
Full numbers and the caveats on them: `references/pricing.md`.

**The chain is defined in exactly one place** — `MODEL_CHAIN` in
`references/ofox-image.sh` — and every skill built on this one resolves a
model by calling that script, never by keeping its own copy of the list. The
cents above are the catalog's rates as of 2026-09-15 applied to token counts
measured on 2026-09-02, quoted here to explain the ordering; the script reads
live rates, so a repricing moves the estimate without invalidating this
table's argument. It moved once already — see the note in the warning above.

It is a **priority, not a lock**. `--model <id>` still pins any image model
Ofox serves, including far more expensive ones. The chain only decides what
happens when nobody picked.

### The 2026-09-04 reversal

`MODEL_CHAIN`'s order has changed exactly once, and the change is recorded
here so it never reads as someone quietly sneaking a preference through.

On 2026-09-02, with both `mai-image-2.5-flash`'s and `gpt-image-2`'s
per-image costs already measured (the table above), the repo owner looked at
the two figures and **deliberately kept `mai-image-2.5-flash` first** —
recorded at the time in `references/token-anchors.json`'s chain-order
history note, together with the instruction that whoever next wanted to
reorder the chain should raise it first rather than doing it quietly. Cost
was one input to that choice, not the only one.

**On 2026-09-04 the repo owner raised it, and asked for `openai/gpt-image-2`
first instead.** `MODEL_CHAIN` and the table above now reflect that request.
This is the reversal it asked for, not an unreviewed reordering — and the
2026-09-02 rule is still in force for the next person who wants to change
this again: raise it before you reorder it.

**`gpt-image-2` has exactly one real run behind it in this repo, and it
carried two surprises.** Until 2026-09-04 it had none at all — its
~0.6-cent figure was a token count (2026-09-02, three calls) rather than a
look at what the model draws, while every opening-frame / concept image this
skill had actually produced came from `mai-image-2.5-flash`. On 2026-09-04 a
scenario skill generated a real frame with the new default, at `--quality
high --size 1792x1024`, and it:

- **cost 15.4 cents, not 0.6** — 5063 output tokens, ~26x the anchored
  estimate, because the anchor was measured at `low` / `1024x1024` and
  nothing recorded that (the chain table's first warning above);
- **was refused once first**, because this model does not accept `--quality
  standard` — the value every earlier image in this repo used (see "Required
  flags" below). Nothing was billed for the refusal.

It also honoured `--size` exactly, which neither model before it did (the
`SIZE` gotcha below). One run is one run: pin `--model
microsoft/mai-image-2.5-flash` explicitly if the look turns out to matter
more than the price for a given use case, and look at the result rather than
assuming it matches what `mai-image-2.5-flash` would have produced.

Both surprises are guards now rather than warnings — 1.7.0 made the estimate
pair-aware and `--quality` per-model, so that run's quote would come out at
the 15.4-cent point and its `--quality standard` would be refused at
`--dry-run` for free. Neither guard makes the model's *look* predictable,
which is the part still resting on a single run.

**Fallback is reported, never silent.** If the preferred model is missing from
the model list, doesn't serve `/v1/images/generations`, or is deprecated, the
script skips it and prints `MODEL_FALLBACK_FROM`, `MODEL_FALLBACK_REASON` and
`MODEL_PRICE_DELTA` (e.g. "1.80x the preferred rate"). Relay all three —
falling back to something more expensive is a decision the user may want to
make differently.

**The model is resolved before anything is quoted**, so the id in a `--dry-run`
quote is the id that would really run. There is deliberately no path where the
model gets chosen after the user approves a price.

### Why there is a default now, when there deliberately wasn't one before

This skill used to require `--model` and refuse to default it, reasoning that
the models differ roughly 4x in price with no obvious winner, so defaulting
would silently pick a price on the user's behalf. That reasoning was right
about the risk, and the risk is now paid for rather than avoided: `--dry-run`
plus [the approval gate](../ofox-video-core/references/approval-gate.md) put
the resolved model and its cost in front of the user **before every spend**,
default or not. The default no longer decides anything quietly, which was the
only thing wrong with having one. Weaken the gate and the default should go
back.

Three models are documented in depth in `references/api-params.md` and
`references/pricing.md` — `openai/gpt-image-2`,
`google/gemini-3.1-flash-image`, `qwen/qwen-image-3.0-pro`. The rest work
too; what isn't documented is which `--size`/`--quality` values each accepts,
because the API doesn't publish that for image models. That gap covers the
chain's models too: a `--quality` value a given model won't take surfaces as
exit `3` with the upstream message, not as a client-side rejection —
confirmed on 2026-09-04 by `gpt-image-2` refusing `--quality standard`, and
recorded per model under "Required flags" below.

## Before you spend: quote it, get a yes, then spend it

**Never send a generation request until the user has seen a cost table and
said yes.** The full spec — required columns, where the numbers must come
from, how to itemise a batch, what to do when no estimate is possible — is
shared by every Ofox skill in this repo and lives in one place:
[`ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md).

**That link, and the other two to the same file in this skill — one under
"Why there is a default now" above, one in the scenario-skill notes below —
assume the sibling directory is named `ofox-video-core`** — true for
skills.sh, ClawHub and `npx ofox-skills`, and not for LobeHub, which unpacks
each skill as `ofoxai-skills-<name>`. If it doesn't resolve, probe before
concluding the file is gone:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/approval-gate.md" ] && echo "$d" && break
done
```

Nothing found means `ofox-video-core` isn't installed at all. **The gate still
applies** — its rule is the paragraph above and the dry run below. The spec's
detail comes back with that skill, and installing it is the user's call, not
yours: hand over the command for whichever installer they already have rather
than running it. skills.sh is
`npx skills add ofoxai/skills --skill ofox-video-core`, this repo's wrapper is
`npx ofox-skills ofox-video-core`, and on LobeHub or ClawHub it is
`ofox-video-core` from the same publisher. Ask for the one missing skill
rather than the whole repo, and give all three routes — naming one installer
tells a user of the other two to abandon theirs.

What this skill contributes to that table:

```bash
bash references/ofox-image.sh generate --dry-run \
  --prompt "..." --quality high --target-aspect 16:9 --out-dir ./assets
```

(`high`, not `standard`: the chain's default model does not accept
`standard`, and since 1.7.0 this dry run refuses the combination itself
rather than letting it reach an HTTP 400 — see "Required flags" above. And
`--target-aspect 16:9` because this frame is going into a video job — the
size enum cannot express 16:9, so the crop is not optional; the dry run
reports which `--size` will be requested to serve it, **and prices the
estimate at that size** rather than at whatever pair the model's anchor
happened to be measured at.)

`--dry-run` parses the arguments, resolves the model against the chain,
validates every parameter, creates and checks `--out-dir`, builds the payload
and prints the estimate — then returns, before the `POST`. Nothing is
submitted, nothing is billed, and **no `OFOX_API_KEY` is needed**, so a job
can be priced before anyone signs up. It prints `STATUS dry_run`, `MODEL`,
`QUALITY`, `SIZE`/`N` where they apply, `TARGET_ASPECT`/`TARGET_SIZE` when a
target was set, the `MODEL_FALLBACK_*` lines when a
fallback happened, and `MODEL_CHAIN_EXHAUSTED` in the rarer case where
*nothing* in the chain is usable — the model named is then one the script
already expects the API to reject, which the user needs to hear before
approving anything.

### The estimate is rough, and sometimes impossible — say which

Video can be quoted exactly: duration is an input and the rate is per second.
Images cannot. They bill per output token, and the token count only exists in
the response. So `--dry-run` prints exactly one `Estimated cost:` line, and it
is one of two things:

- **`ROUGH ~<amount> (<N> output tokens x ..., measured <date> at --quality
  <q> --size <s>)`** — anchored to a real measured call with **that same
  model at that same pair**. Relay it as rough; it is not a quote.
- **`ROUGH UPPER BOUND ~<amount> (... measured <date> at --quality <q> --size
  <s>)`** — nothing has been measured at the pair *this* request asks for, so
  the figure is the **dearest** point that model has, quoted as a ceiling.
  Relay it as a ceiling and say so: the real bill may land well under it.
- **`cannot be predicted for '<model>' — no real call's output-token count has
  been recorded for it`** — no measurement exists yet. Relay that sentence,
  show the table anyway with "cannot be predicted" in the cost column, and
  still wait for a yes.

**An anchor is only valid for the `--quality`/`--size` pair it was measured
at, and since 1.7.0 the lookup knows that.** It used to read one number per
model and print it for every request, which cost real money on 2026-09-04: a
run at `high` / `1792x1024` was quoted from `gpt-image-2`'s `low` /
`1024x1024` anchor — approved at ~0.6 cents, billed **15.4 cents**, 26x, with
the size and the quality on screen directly above the wrong price. The rule
now:

1. a measurement at the request's own pair is quoted as-is;
2. otherwise the **dearest** measurement that model has is quoted, labelled
   `UPPER BOUND` and carrying the pair it came from, so a table built from
   the line alone still shows whether the number belongs to what was asked
   for;
3. nothing is interpolated between two measured points, and no quote comes
   out below what the request could cost;
4. `auto` for either flag — and an omitted `--size`, which is the same thing,
   the API picking — is unknowable in advance and takes the upper-bound path.

Two consequences worth carrying into the table. **A common cheap call now
over-quotes**: `--quality low` with no `--size` on `gpt-image-2` shows the
15.4-cent ceiling, not the 0.6-cent point, because an omitted size cannot be
matched — name the pair when you want the exact figure. And **the ceiling
bounds the output-token half only**; the prompt's input tokens are excluded
from every figure this script estimates, as they always were, which on
observed calls was a fraction of a cent.

**Never borrow one model's measured token count for another model.** A
borrowed number is indistinguishable from a measured one and is worth less
than no number at all. Measured anchors today: `google/gemini-3.1-flash-image`
(invoice-checked), `microsoft/mai-image-2.5-flash` and `openai/gpt-image-2`
(formula only) — each at the pair recorded beside it, and the chain's rows 3–4
at none. See `references/pricing.md`.

## Availability check

Before the first call in a session, verify the environment:

```bash
bash references/ofox-image.sh check
```

This checks `curl`, `jq`, and `OFOX_API_KEY` and exits `0` only if all three
are present — it makes no network call. Handle each failure mode plainly:

- **`curl` missing** (rare — usually preinstalled): `brew install curl`
  (macOS) or `sudo apt-get install curl` (Debian/Ubuntu), else
  https://curl.se/download.html.
- **`jq` missing**: `brew install jq` (macOS) or `sudo apt-get install jq`
  (Debian/Ubuntu), else https://jqlang.org/download/.
- **`OFOX_API_KEY` missing**: two paths, and the second one is the one
  agents forget. If the user has no key, they get one at
  `https://app.ofox.ai` (log in → Settings → API Keys → Create New Key,
  shown once) and `export OFOX_API_KEY=...` in their shell. If they say the
  key already lives in a file, don't send them back to the terminal to
  re-type it — load it yourself with `set -a; . <path>; set +a` in the shell
  you'll call the script from (see the safety contract: authorization first,
  read the file before sourcing it, never echo the value). Offer this once,
  plainly, and move on — don't repeat the pitch on every message.

`check` deliberately does **not** test for `ffmpeg`/`ffprobe`: they are only
needed by `--target-aspect`/`--target-size`, and making them a session-level
requirement would block callers who never crop. Those flags check for them
themselves, before anything is spent (exit `2`).

## Invoking the script

```bash
bash references/ofox-image.sh generate \
  --prompt "..." --quality VAL [--model MODEL] [OPTIONS]
```

There is a second subcommand, `edit`, for changing an image you already have
rather than drawing a new one — see "Editing an image you already have" below.
Everything in this section describes `generate`; `edit` shares the model
resolution, the `--dry-run` contract, the exit codes and the geometry flags,
and differs in the three ways that section lists.

`generate` resolves the model, validates every parameter client-side (model
name, size, quality, and the documented `n` + Gemini incompatibility)
**before any network call**, builds the request, sends exactly one `POST`,
and on success base64-decodes each returned image and writes it to a file. It
prints:

```
STATUS completed
IMAGE_PATH <absolute/path/to/file.ext>   (one line per generated image)
MODEL <the model the cost below is priced at>
MODEL_SOURCE response | request
MODEL_REQUESTED <id>                     (only when it differs from MODEL)
SIZE <size the response claims — not evidence of anything, see below>
SIZE_ACTUAL <WxH measured from the written file, or "unmeasured">
SIZE_FINAL <WxH of the cropped deliverable>   (only with --target-aspect/--target-size)
TARGET_ASPECT <W:H>                           (only with --target-aspect/--target-size)
IMAGE_PATH_UNCROPPED <path>                   (only when a crop happened)
QUALITY <quality actually used, from the response>
USAGE_INPUT_TOKENS <n>
USAGE_OUTPUT_TOKENS <n>
USAGE_TOTAL_TOKENS <n>
IMAGE_COST <dollars>
```

`MODEL_SOURCE` says where the `MODEL` id came from, and it matters for two
different reasons:

- `response` — the API echoed it. Normal.
- `request` — the response carried no `model` field, so the id is the one that
  was **requested**, not one the API confirmed. The cost is still computed, at
  that model's published rates. Relay it as "the API didn't echo a model name;
  priced as the model we asked for" rather than presenting it as confirmed.

⚠️ **Which of the two you get from `openai/gpt-image-2` has changed under us,
so read the line rather than predicting it.** On 2026-09-04 that model omitted
the `model` field on every call observed — first-hand, and costly enough to
be certain about: it defaulted to the literal `"unknown"`, found no rate for
it, and printed no `IMAGE_COST` at all on two paid calls, which is what
1.3.0's fallback was built to fix. This file then generalised that into
"`MODEL_SOURCE request` is now the common case for a default `generate` call".

**That generalisation no longer holds.** Re-checked 2026-09-15 on three real
paid calls against the same model — two probes run while `image-edit` and
`product-image` were written (one `generate`, one `edit`) and one further
minimal `generate --quality low --size 1024x1024` (196 output tokens, 0.59
cents, `IMAGE_COST 0.00593` against a 0.59-cent estimate) — **all three
printed `MODEL_SOURCE response`.** The field is being echoed now.

Three days of observation eleven days apart is not a schedule, and nothing
here says which way it will read tomorrow. What it does establish is the rule
worth keeping: **an upstream response shape is not a stable fact to write a
"common case" sentence about.** Both branches are handled, both are correct,
and the script prints the line unconditionally precisely so a caller never has
to guess. Relay what it printed on *this* run; do not tell a user which one to
expect.

`MODEL_REQUESTED` appears only when upstream ran a **different** model from the
one asked for (routing, aliasing, a silent downgrade). When it appears, `MODEL`
and `IMAGE_COST` describe the model that actually ran — that is what the
invoice will say — and anything you measure from that run belongs to `MODEL`,
not to `MODEL_REQUESTED`. Surface the mismatch to the user; it is the
difference between a bill that reconciles and one that does not.

Required flags: `--prompt`, and `--quality` (one of
`auto low medium high standard hd` — Ofox's docs mark this required, and not
every value applies to every model, so the script never guesses a default;
you must pass one explicitly).

**`--quality` is a per-model enum, and since 1.7.0 it is validated against
the model the request will actually use** — not just against the union of
every model's values. So an invalid combination fails at `--dry-run`, exit
`1`, no network call, instead of costing a round trip to an HTTP 400. What is
observed, and which half of it is first-hand:

| Model | Accepted set | Where that comes from |
|---|---|---|
| `openai/gpt-image-2` (the chain's head) | `auto`, `low`, `medium`, `high` — **enforced**, so `standard` and `hd` are rejected locally | **First-hand, the API's own enumeration**: HTTP 400, `Invalid value: 'standard'. Supported values are: 'low', 'medium', 'high', and 'auto'` (2026-09-04, nothing billed) |
| `microsoft/mai-image-2.5-flash` | the full union — **permissive fallback** | `standard` accepted on nine real runs. Evidence a value *works*, not an enumeration of what the model takes |
| `google/gemini-3.1-flash-image` | the full union — **permissive fallback** | `low` accepted on three real runs. Same limit |
| everything else | the full union — **permissive fallback** | no observation either way |

**Only the first row is a whitelist, and that is deliberate.** A narrower set
invented for a model that never enumerated its own would reject calls that
would have worked, and a false rejection is worse here than the 400 it
prevents: the 400 costs a round trip and no money, while a false rejection
blocks the work outright with no way around it short of editing the script.
So an absence of evidence stays permissive, and a row is added only when a
model has enumerated its own set. The table lives in `model_qualities()` in
`references/ofox-image.sh`, with the refusal quoted next to it.

The trap this closes is worth stating plainly: **`standard` used to work on
every call this repo made, and stopped working the moment the chain's head
became `gpt-image-2` on 2026-09-04** — same flag, same script, instant 400,
and `--dry-run` caught none of the five copy-pasteable commands that shipped
broken in two other skills. It now does. Any caller still passing `--quality
standard` needs `high` (or `low`/`medium`/`auto`), or `--model
microsoft/mai-image-2.5-flash` pinned to keep the value; the error names the
resolved model and both fixes, including when no `--model` was ever passed
and the id came from `MODEL_CHAIN`. `hd` has never been accepted by any model
here. Per-model detail and the captured response:
`references/api-params.md`.

Optional flags: `--model` (any image model Ofox serves; default: the priority
chain above), `--dry-run` (validate, resolve, quote, stop — no request, no
key needed), `--size` (one of the documented WxH values or `auto`),
`--target-aspect W:H` / `--target-size WxH` (the ratio or exact pixels the
delivered file must really be — see "The size enum cannot express 16:9 or
9:16" below; **this is the flag to use for a video first frame**),
`--n` (1-10, default 1 — **not supported at all by
`google/gemini-3.1-flash-image`**, rejected client-side before any network
call if combined with that model, even `--n 1`), `--output-format`
(`png`/`jpeg`/`webp`), `--background` (`transparent`/`opaque`/`auto`),
`--extra-json '<json>'` (a JSON **object** of fields not covered by a flag, e.g.
`extra_body.provider.type` for `openai/gpt-image-2` — it may not be empty and
may not set a field that has a flag; see below), `--out-dir` (default:
current directory), `--out-name` (bare filename, no extension, no path
separators — default: a timestamp-based name). Full parameter reference:
`references/api-params.md`. The cost formula and the invoice it was verified
against: `references/pricing.md`.

**Always state the full `IMAGE_PATH` as its own standalone line in your
reply to the user** — not folded into a sentence or buried mid-paragraph,
mirroring `ofox-video-core`'s `VIDEO_PATH` discipline exactly. `--out-dir`
is resolved to an absolute path (and created if missing) **before** any
network call, so relay the printed path exactly; the file's location is the
actual deliverable, and the user should be able to find it without
re-deriving your working directory.

## The size enum cannot express 16:9 or 9:16

This is the single fact that explains every size surprise in this skill, and
it is not a model bug — it is a structural gap between this image API's
`size` enum and the video API's aspect ratios. Every value `--size` accepts,
with its true ratio:

| `--size` | Ratio | What it actually is |
|---|---|---|
| `1024x1024`, `512x512`, `256x256` | 1.0000 | 1:1, exact |
| `1536x1024` | 1.5000 | 3:2, exact |
| `1024x1536` | 0.6667 | 2:3, exact |
| `1792x1024` | **1.7500** | the closest thing to 16:9 — but 16:9 is 1.7778 |
| `1024x1792` | **0.5714** | the closest thing to 9:16 — but 9:16 is 0.5625 |

**16:9 and 9:16 cannot be requested at all**, on any model, at any quality.
So every 16:9 or 9:16 frame this API produces has to be cropped. There is no
flag, no model and no prompt wording that avoids it, and looking for one is
the wrong search.

### Why that matters more than tidiness: `adaptive` propagates the error

These frames mostly exist to be attached to a video job, and attaching an
image to `bytedance/seedance-2.5` **forces `aspect_ratio: adaptive`** — the
frame's own ratio becomes the finished video's ratio, whatever the video
flags say. A 1.75 frame yields a 1.75 video. Fixing it after the fact means
paying for the video again, at video prices, so a ratio error in a
two-cent image is charged at the cost of the clip it was attached to.

### `--target-aspect` / `--target-size`: state it, and the script keeps it

```bash
# A 16:9 first frame for a video job — the common case.
bash references/ofox-image.sh generate \
  --prompt "a teenage girl at the edge of a school rooftop at sunset, ..." \
  --quality high --target-aspect 16:9 --out-dir ./assets
```

What that does, in order:

1. **Picks the request size** from the enum above — the one that survives the
   crop with the most pixels intact (`1792x1024` for 16:9, keeping 98.4%,
   against `1536x1024`'s 84.4%). An explicit `--size` is respected and never
   silently replaced; it is only warned about when it cannot cover the target.
2. **Generates as normal**, at the usual price for that size and quality.
3. **Measures the written file** with `ffprobe` — never the response's own
   `size` field, for the reasons in the next section.
4. **Centre-crops to exactly the target ratio.** Crop dimensions are integer
   multiples of the reduced ratio, not a rounded division, so the result is
   16:9 rather than 1.7773. Both crops on record fall out of that one rule:
   `1344x768 → 1344x756` and `1792x1024 → 1792x1008`.
5. **Fails loudly if the target cannot be met** — a file smaller than the
   target, or a `--target-size` no accepted size can cover without upscaling.
   It crops and scales *down*, never up. An almost-right image is the
   expensive outcome here, not the safe one.

`--target-size WxH` is the same thing with exact pixels: it requests the
cheapest size that clears the floor after cropping (since anything above it
is tokens bought and thrown away), then scales the crop to exactly `WxH`.
The two flags are mutually exclusive — `--target-size` already fixes the
ratio.

**Which file to attach.** The cropped frame takes the plain output name, so
`IMAGE_PATH` is always the file that meets the target and an existing caller
parsing that key gets the right one without changing. The API's untouched
bytes are kept alongside it as `<name>-uncropped.<ext>` and reported as
`IMAGE_PATH_UNCROPPED`, so a human who wants a different crop still has the
original. If the crop fails, the plain name is never written and the run
exits non-zero — there is no state in which a wrong-ratio frame is sitting
where the right one was promised.

**These flags need `ffmpeg`/`ffprobe`** (`brew install ffmpeg`,
`sudo apt-get install ffmpeg`) — the same dependency `ofox-video-core`
already uses for contact sheets and chain frames, not a new one. Missing,
they fail as an environment error (exit `2`) **before anything is spent**,
because the flags are a promise about the delivered file and there is no way
to keep it without measuring and cropping. Everything else in this script,
including `--dry-run` pricing, works without `ffmpeg`; drop the flag and you
own the measure-and-crop step by hand.

## Known gotcha: `SIZE` in the printed output can be wrong

Three models, three different behaviours, and the correction is needed in
all three cases:

| Model | Requested | Response said | File really was | Runs |
|---|---|---|---|---|
| `google/gemini-3.1-flash-image` | `512x512` | `512x512` | **1024x1024** | 1 (2026-08-29) |
| `microsoft/mai-image-2.5-flash` | `1792x1024` | `1354x774` | **1344x768** | 3 |
| `openai/gpt-image-2` | `1792x1024` | `1792x1024` | `1792x1024` | **1** (2026-09-04) |

`google/gemini-3.1-flash-image` appears to always generate at its native
1024x1024 and echo back whatever `size` was asked for — verified with `file`
and `sips -g pixelWidth -g pixelHeight`.

**`microsoft/mai-image-2.5-flash` is worse than a two-way mismatch — it is a
three-way one.** Request, response echo and file on disk are three
*different* numbers, on three separate paid runs. Evidence: the `refs/`
entries in `content/ofox-cases/{anime-rooftop-confession,
yunqi-sparkling-ad, sneaker-motion-ad}/case.json` in the `home-page` project
(a downstream consumer of this skill, not part of this repo).

**`openai/gpt-image-2` is the one model measured here that honours `--size`
exactly** — and it is **one run**, so read it as one observation, not a
guarantee. `qwen/qwen-image-3.0-pro` is untested.

**Honouring the request is not the same as producing a usable ratio**, which
is why that run still needed a crop: `1792x1024` is 1.75, so the frame went
to `1792x1008` before it could be attached. So the rule is the same on every
model and only the size of the correction changes — 16 pixels of height for
`gpt-image-2`, a different resolution entirely for the other two.

`SIZE` is printed straight from the response and inherits all of this;
`SIZE_ACTUAL` is measured from the file and is the one to believe. When they
disagree the script says so on stderr rather than leaving it to be noticed.
**Don't trust `SIZE`, and crop rather than pad** so nothing is invented at
the edges — or pass `--target-aspect`/`--target-size` and let the script do
both. Full detail: `references/api-params.md`.

## Editing an image you already have (`edit`)

`generate` draws a new image from text. `edit` takes a file you already have
and changes it — `POST /v1/images/edits`, added in 1.11.0.

```bash
bash references/ofox-image.sh edit \
  --image ./photo.png \
  --prompt "Replace the background with a beach at sunset. Keep the person unchanged." \
  --out-dir ./assets \
  --dry-run
```

Drop `--dry-run` to run it. Keep `--out-dir` — without it the edited file
lands in whatever directory you happened to be in.

A local file is the primary input and needs no hosting. `--image-url` takes a
public URL or a `data:` URI if you have one, but nothing requires you to put
the picture on the internet first.

Output is the same shape as `generate`, plus the input echoed back for
comparison and the token line that has no `generate` equivalent:

```
STATUS completed
IMAGE_PATH <absolute path to the edited file>
INPUT_IMAGE <absolute path to the source>
INPUT_SIZE_ACTUAL <WxH measured from the source>
MODEL / MODEL_SOURCE / SIZE / SIZE_ACTUAL / QUALITY   (as generate)
USAGE_INPUT_TOKENS <n>
USAGE_INPUT_IMAGE_TOKENS <n>    <- the uploaded picture, billed
USAGE_INPUT_TEXT_TOKENS <n>
USAGE_OUTPUT_TOKENS <n>
USAGE_TOTAL_TOKENS <n>
EDIT_COST <dollars>
```

### Three things about `edit` that differ from `generate`

**1. Not every model can edit, and the list is live.** Run
`ofox-image.sh models --endpoint edits`. Support is read from each model's
`supported_endpoints` in the catalog, never from a table in this repo —
confirmed both ways: a model without the flag is refused with
`endpoint_not_supported`, models with it ran. Omitting `--model` resolves the
priority chain against the edits endpoint, so a chain entry that could not
edit would be skipped with a reason rather than silently failing.

**2. The image you upload is billed.** On the measured run, 576 of 608 input
tokens were the picture. That component does not exist for a generation, and
it scales with the file you pass: a 320x180 input cost 0.6 cents, an 854x480
input 1.4, and a 1792x1008 input 1.6 (1508 image tokens). Pass a smaller
source when the job allows it — at the top end the uploaded picture is
**74%** of the bill (`1508*0.000008 = 0.012064` of 0.016249), so it is the
only lever that matters there.

⚠️ **Do not reason about an edit's cost from its output tokens.** They do not
track the input: 129 (320x180), 229 (256x256), 301 (854x480), **129**
(1792x1008) — the largest input ties the smallest for the lowest count. The
input **image** tokens are what move with the file (240 / 256 / 576 / 1508),
and they are the bigger half of the bill on anything large. See
`references/pricing.md` → "Measured edits".

**3. ⚠️ The API does **not** reject bad parameters here, so the dry run
matters more, not less.** `generate` gets a bad `--quality` refused upstream
for free. `edit` does not — measured 2026-09-15, an unknown `--quality` value
was silently ignored and rendered six billable images. The client-side checks
in this script are the only guard. Run `--dry-run` first and read the
`FORM_FIELDS` line to confirm what will actually be sent.

### Verify the artifact, not the exit code

`STATUS completed` cannot tell you whether the endpoint edited your image or
quietly redrew the prompt from scratch. **Open the result next to
`INPUT_IMAGE` and check that what you did not ask to change is unchanged.**
The script prints both paths side by side so this is one command, and prints a
reminder on every successful edit.

For the record, on the runs this skill is built from it genuinely edits: a UI
screenshot asked for one button colour change came back with every string
intact ("Billing Settings", "$29.00", "Seats included 3") and 58% of all
changed pixels inside the button, which is 1.1% of the frame. That is evidence
about two runs on one model, not a guarantee about yours — which is why the
check is in the instructions rather than assumed.

### What is not established

- **Whether `--size` is honoured.** All four measured runs omitted it and got
  a size derived from the input's aspect ratio at a near-constant pixel budget
  — 854x480, 320x180 and 1792x1008 (all 16:9) returned 1672x941, and 256x256
  returned 1254x1254, which is 0.05% the same pixel count. The 1792x1008 run
  is the one that shows this is a **budget** rather than an upsample floor:
  its input is larger than the output and the output did not grow. Note the
  useful side: 1.777 is the 16:9 the `generate` size enum cannot express at
  all.
- **Whether `--prompt` is required by the API.** This script requires it.
- **Whether a `mask` works.** See "Out of scope" below.
- **The other four models** that advertise the endpoint but have not been run.

Each of those costs a billed edit to answer, which is why they are written
down as open rather than guessed at.

## Out of scope for this script

- **`input_images` / image-to-image** (Qwen-only field on this same
  `/v1/images/generations` endpoint) — this script only does text-to-image.
  Passing `input_images` via `--extra-json` is rejected client-side with a
  clear message.
- **Masked / inpainting edits.** Whether `POST /v1/images/edits` accepts a
  `mask` is not established. Finding out costs a billed edit per attempt, so
  it was left alone rather than guessed at. **Nor can you try it through
  `edit --extra-form "mask=@FILE"` any more** — 1.14.0 refuses any
  `--extra-form` value starting `@` or `<`, because that spelling uploads
  whatever local file it names, which made this flag a file-exfiltration
  primitive. Stating the narrowing rather than leaving it to be discovered:
  attaching a mask now needs its own flag with its own path validation, and
  nobody has needed one enough to write it.

  (`POST /v1/images/edits` itself is **no longer out of scope** — it is the
  `edit` subcommand as of 1.11.0. It is also not "OpenAI models only", as
  this list used to claim without evidence: eleven models advertise it and
  seven have been confirmed running an edit, across three vendors.)
- **Streaming responses** (`stream: true`) — this script only parses a
  plain JSON response body. Rejected client-side if set via `--extra-json`.

## 🚨 This script writes NO sidecar — a paid run's numbers exist only on your terminal

**Save the full output of every paid `generate` or `edit` before you close the
shell.** Redirect it to a file, or copy the figures into
`references/token-anchors.json` immediately. Nothing does it for you.

`ofox-video-core` writes a `.json` sidecar next to every delivered mp4,
carrying the job id, seed, prompt, request and real cost. **This script writes
nothing of the kind** — an image lands as a `.png` and that is all. Verified:
the three edits behind this file's 1792x1008 anchor produced
`flask-white-bg.png`, `flask-set-warm-wood.png` and `flask-set-grey-sweep.png`
with no companion file, while every video job in the same session has its
sidecar on disk.

**This is not a tidiness complaint — it has already nearly cost a measurement.**
The figures `token-anchors.json`'s `_how_to_add_a_row` demands —
`USAGE_OUTPUT_TOKENS`, the input token split, `EDIT_COST` — are *exactly* the
values this path never persists. The 1792x1008 anchor was written up as
"output tokens unrecorded and unrecoverable" and a never-under-quote
disclosure was published on that premise; the numbers had simply scrolled out
of reach, and were recovered from a session transcript rather than from disk.
On the video side the same mistake is impossible, because the sidecar is
already written.

So, concretely, when you make a paid image call:

```bash
bash references/ofox-image.sh edit --image IN.png --prompt "..." \
  --out-dir /abs/out 2>&1 | tee /abs/out/edit-$(date +%Y%m%d-%H%M%S).log
```

and take the anchor figures from that log rather than from memory. A billed
run whose token counts are gone is money spent for an artifact you cannot
price the next one from.

⚠️ **Adding a sidecar to this script is a separate change and is deliberately
not made here.** It would need to decide the filename, the schema, and what
happens on the `--n > 1` path where one call writes several files — so it is a
design question, not a one-line fix. Recorded as a recommendation rather than
smuggled into a documentation pass.

## No job id, no polling — what that means for failure handling

There is nothing to resume here the way `ofox-video-core poll JOB_ID`
resumes a video job. A single `generate` call either:

- gets a real HTTP response (success or a rejected request) — the request's
  fate is decided, and it is then safe to fix parameters and try again if
  it was rejected, or
- gets **no HTTP response at all** (`curl` exits nonzero with no status
  code) — genuinely ambiguous, and unlike the video API there is no job id
  to look up afterward to find out what happened. The script exits `5` in
  this case and tells you to check your usage/billing history at
  `https://app.ofox.ai` before deciding whether to retry. Don't guess, and
  don't auto-retry a `--extra-json`-free, unmodified request on exit `5`.

**Whether a rejected (non-2xx) request is billed at all has not been
confirmed for this endpoint** — this script assumes, but has not verified
with a real call, that a request producing no image is not charged (the
common pattern for generation APIs, and the same assumption
`ofox-video-core` verified for its own create-rejection case). Treat this
as an open question pending a real, observed error case, not as a settled
fact — if you do observe billing behavior on a real error, that's worth
recording back into this skill's documentation.

## Error handling

This endpoint's error vocabulary has **not** been broadly explored, and this
skill's own earlier documentation got the error response's *shape* wrong,
not just an unconfirmed code: the original research inferred `error.code:
"provider_type_unavailable"` purely from Ofox's doc **prose** describing a
provider-mismatch scenario — it was never seen in a real response. A real
rejected call (2026-08-29, an invalid `extra_body.provider.type`, exactly
the scenario that prose was describing) showed the actual shape is
`{"error": {"message", "type", "code"}}` — an OpenAI-SDK-style shape,
different from the video API's `{code, message}` shape where `code` really
was a semantic string. Here, `error.code` was literally the HTTP status as a
**number** (`400`); the real classifier is `error.type`
(`invalid_request_error` was the only value confirmed until 2026-09-06, when
a safety-system refusal on `openai/gpt-image-2` returned a second one,
`image_generation_user_error` — see the error table in
`references/api-params.md` for the one trigger that has been isolated, and
for the two repair routes: rewrite the clause, or re-run on
`--model microsoft/mai-image-2.5-flash`. `provider_type_unavailable` still
does not appear anywhere in a real response). `print_api_error` in
`ofox-image.sh` now surfaces `error.type` as the primary classifier and shows
`error.code` for reference, but always prints the raw `error.message`
regardless — that part already worked correctly and still does. Two
message-only gotchas remain doc-prose-only, unconfirmed by a real call:
Gemini + `/v1/images/edits` ("Image editing is not supported for model") and
Gemini + `n` (this script prevents the latter client-side before any network
call, so it should never actually be observed against the real API through
`ofox-image.sh`). Don't treat an unrecognized `error.type` as this script's
bug; it means the vocabulary genuinely hasn't been seen yet — update
`references/api-params.md` and this script's `print_api_error` if/when a new
one is confirmed by a real call.

| Exit | Meaning |
|---|---|
| `0` | Success — image(s) decoded and saved, usage token counts and `IMAGE_COST` printed. Also the exit code of a `--dry-run`, which prints `STATUS dry_run` and spends nothing. |
| `1` | Usage/parameter validation error — no network call was made. Fix the flag and retry `generate` freely. Includes a `--quality` the resolved model does not accept, which since 1.7.0 lands here instead of as an exit `3` HTTP 400. |
| `2` | Environment error — `curl`/`jq`/`OFOX_API_KEY` missing, or `ffmpeg`/`ffprobe` missing while `--target-aspect`/`--target-size` was passed. Fix the environment, no request was attempted. |
| `3` | The API rejected the request, the response body couldn't be parsed into a usable image, or a `--target-aspect`/`--target-size` target could not be met by the file that came back (**the image was generated and billed** and is on disk at the `-uncropped` path; nothing wrong-ratio was written to the plain path) (see `references/api-params.md` for the one confirmed `error.type`; everything else is surfaced via the raw upstream message). |
| `4` | `--out-dir` could not be created or entered (bad path, permissions) — caught **before** any network call, so no money was spent finding this out. Fix `--out-dir` and retry. |
| `5` | Ambiguous network failure — no HTTP response received at all. No job id exists to check afterward; check `https://app.ofox.ai`'s usage/billing history before deciding whether to retry. |

## For scenario skills built on this

A scenario skill (for example, one that generates a character reference
image before handing it to `ofox-video-core` for image-to-video) should
call `references/ofox-image.sh generate` rather than duplicating any of the
request-building, validation, or decoding logic above. It owns the
scenario-specific prompt template and recommended size/quality defaults;
this skill owns the mechanics of talking to the API correctly and safely.

**Four things a scenario skill must not re-implement**, because a second copy
is a second thing to forget:

- **The model choice.** Don't hardcode a model id and don't keep a copy of
  the priority chain. Omit `--model` and let the script resolve it, or pass
  `--model` through when the user asked for a specific one. A scenario skill
  that pinned its own model quietly kept paying an old price after the chain
  moved — that is the failure this rule exists for.
- **The approval wording.** Link
  [`ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
  instead of restating the rule in your own words. Four paraphrases of "show
  the price first" become four different rules. Carry the directory-name
  caveat with the link, though — a scenario skill on LobeHub finds that file
  under `ofoxai-skills-ofox-video-core`, so a "Where the core skill lives"
  probe near the top of the skill is what keeps the link from reading as a
  missing file.
- **The measure-and-crop step.** Don't tell the caller to check the file's
  pixels and crop it by hand — pass `--target-aspect` (or `--target-size`)
  and let the script guarantee the ratio. Three agents in a row re-derived
  that arithmetic before those flags existed, and a frame that skips it
  becomes a wrong-ratio **paid video**, because attaching an image forces
  `aspect_ratio: adaptive`. A scenario skill producing a video first frame
  should treat one of the two target flags as mandatory, not optional.
- **The per-image price, and which `--quality` a model takes.** Don't write
  either into your own copy. A quoted cents-per-image figure goes stale the
  moment the chain moves or the flags change — `gpt-image-2` is 0.6 cents or
  15.4 cents depending on two of them — so relay the `Estimated cost:` line
  a `--dry-run` printed, including its `UPPER BOUND` label and the pair it
  names, rather than a number of your own. Likewise, don't hardcode a
  `--quality` value on the strength of one model accepting it: five
  copy-pasteable commands across two skills said `--quality standard` and
  broke the day the chain's head changed. Since 1.7.0 a `--dry-run` catches
  that for free, which makes dry-running your own documented command the
  cheapest way not to ship it broken.
