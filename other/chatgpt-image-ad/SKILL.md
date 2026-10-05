---
name: chatgpt-image-ad
metadata: {packVersion: 1.3.0}
description: >-
  Generate one or more standalone Meta image-ad creatives via ChatGPT Image 2 (gpt-image-2) through the Novoads API. Locks the model, auto-strips platform chrome, enforces edge-safe layouts and glyph-safety inside body text. Use when the user asks for a "gpt-image-2 ad", "ChatGPT Image ad", "Image 2 ad creative", "make a static image ad with GPT", or anchors on a need for typography-heavy / dense-text / UI-mimicry ad creatives (chat threads, comparison tables, fake search results, iOS dialogs, Slack snapshots, ChatGPT-conversation ads, Apple Notes lists). Does NOT trigger on Nano Banana cues — use nano-banana-image-ad for those.
---

# chatgpt-image-ad

Generate one or more **standalone Meta ad image creatives** via Novoads' `POST /v1/images`
with `model: "gpt-image-2"`. Hands the image paths off to your Meta-ad-builder skill — this
skill does not upload to Meta itself.

## If the `shared/` files are not on disk

Then this skill was installed on its own from skills.sh and the rest of the pack stayed behind.
Fetch each missing file from `https://raw.githubusercontent.com/novoads/agent-skills/main/<path>`,
where `<path>` is one of `shared/skills/image-ad-prompting/OVERVIEW.md`,
`shared/skills/image-ad-prompting/prompting/prompt-library.md`,
`shared/skills/image-ad-prompting/prompting/safety-suffixes.md`,
`shared/skills/image-ad-prompting/prompting/template-format.md` and
`shared/skills/chatgpt-image-ad/prompting/guide.md`. Or take everything at once with
`git clone https://github.com/novoads/agent-skills.git`. That install has no
`scripts/check-novoads-env.sh` either, so set `NOVOADS_API_KEY` in the environment yourself and
let the first call report the key.

## Read order

Paths below are **from the repo root**. This skill is copied into `.claude/skills/` and
`.cursor/skills/` by `sync-skill.sh`, so a relative link out of it would break in those
copies — read these from the repo you are working in.

1. **This file** — endpoint, auth, upload flow, workflow phases.
2. `shared/skills/image-ad-prompting/OVERVIEW.md` — the ecosystem hub: which skill, which model, what the family does and doesn't do.
3. `shared/skills/chatgpt-image-ad/prompting/guide.md` — model-specific prompting (what gpt-image-2 is good/bad at, when to switch to nano-banana-pro).
4. `shared/skills/image-ad-prompting/prompting/prompt-library.md` — 40 validated templates with per-model notes.
5. `shared/skills/image-ad-prompting/prompting/safety-suffixes.md` — the 3 always-on guards.
6. `skills/chatgpt-image-ad/scripts/generate_image.py` — the helper script (Python stdlib only).

For anything about the API itself that this file does not answer — error codes, rate limits,
concurrency, the upload contract — the `novoads-api` skill's `reference.md` is the authority.

## Hard rules — never relax

1. **Model is `gpt-image-2`.** The script refuses any other value. If the user asks for Nano Banana, point them at `nano-banana-image-ad`.
2. **No platform/screenshot chrome in output.** `NO_CHROME_SUFFIX` is always on (override with `--allow-chrome` only when the ad's concept *requires* chrome — rare).
3. **Edge-safe + glyph-safety suffixes always on** unless `--no-safe-zone` is explicit. They fix real failures; don't remove silently.
4. **Max 4 reference images.** `referenceAssetIds` caps at 4 on `gpt-image-2` (`nano-banana-pro` takes up to 14, `reve-2.1` 8 — spec 2.7.0). The script enforces it.
5. **Every brand mark that appears in the frame is passed as a reference asset.** Not a tip — a rule. This model invents brand-shaped content on any surface the prompt leaves unspecified, and it states it as fact. Measured over a 34-template run on one real product (2026-08-04): the label was faithful in **all 34** because a reference pinned it, while unpinned marks failed three ways — a billboard invented a *back-of-can view* carrying "OUR WATER IS SOURCED FROM THE AUSTRIAN ALPS…" with an icon row and a barcode, a prop thermos rendered a **Hydro Flask logo**, and a publication wordmark drifted. So: pin the product, pin the logo, pin any third-party mark the concept needs; and for product surfaces the ad does **not** show, say so — *"front label only; do NOT render the back of the can, no invented label copy, no ingredient text, no sourcing statement, no barcode."* One retry with that wording cured the fabricated claim completely. Unpinned means invented. **Pass it as `--pin-block "<one-line product description>"`** rather than writing the clause by hand: the script wraps the shared library's standard 346-character guard around your description, counts it against this model's prompt cap (32,000 characters, deployed spec 2.16.0, verified 2026-08-08), and refuses pre-network naming the pin block's share if it does not fit. Hand-written pin blocks ran ~700 characters and used to be the single largest cause of a refused prompt, back when the cap was 4,000 on every model. At 32,000 a hand-written block no longer overflows anything, and the reason to pass `--pin-block` is that the standard guard is the wording that was measured to work.
6. **No Meta upload from this skill.** Image generation only. Hand off via filesystem paths.
7. **Always show a live cost estimate before generating, and get an explicit yes.** The price comes from `POST /v1/estimates` in this session — never from memory, never from `logs/novoads-api.jsonl`, never from `MASTER_CONTEXT.md`. There are no credit numbers written down anywhere in this repo, on purpose.

## Prerequisites

- `.env` containing `NOVOADS_API_KEY` (`novo_` + 64 hex, created at <https://novoads.ai/dashboard/settings?tab=api>). Verify with `./scripts/check-novoads-env.sh`.
- Optional: `PRODUCT_ID` in `.env` so generated assets are filed under a specific product. Omit it and the job lands in your default product. `productId` is **organizational only** — it does not influence what is generated.
- Reference images on local disk (PNG/JPG/JPEG/WEBP). The script handles the upload flow internally — you pass local paths.

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

## Configuration

- **Base URL:** `https://api.novoads.ai` (or `NOVOADS_BASE_URL`). That is the **host only** — callers append `/v1/...`.
- **Auth:** `Authorization: Bearer $NOVOADS_API_KEY`.
- **Endpoint:** `POST /v1/images`: the call blocks for the render (typically 60–90 seconds) and returns the finished images. A render still going after about 105 seconds answers `status: "running"` with no images instead (API 2.39.0): poll `GET /v1/generations/{jobId}` to a terminal status and read `images[]` there. Never resubmit it; that job is already paid.
- **Reference uploads:** `POST /v1/uploads` with `{contentType, sizeBytes}` returns `{assetId, uploadUrl, method, headers, expiresInSeconds, maxBytes}`. `PUT` the raw bytes to `uploadUrl` **echoing the returned `headers` byte for byte** — Content-Type and Content-Length are both part of the signature, so storage returns 403 if either differs. The resulting `assetId` is **durable and reusable**: upload a product shot once and pass the same id on every later call.

## What this model takes

| Field | Value |
|---|---|
| `model` | `gpt-image-2`, locked by the script. No longer the API default; see the note under the table. |
| `prompt` | the image prompt — the always-on suffixes count against the model's cap |
| `aspectRatio` | `1:1` `4:5` `2:3` `9:16` `16:9` `21:9` — **defaults to `1:1`**, so always set it |
| `referenceAssetIds` | up to **4**, order preserved, addressable positionally from the prompt |
| `numImages` | `1`–`4`, **one call**, charged per image |
| `productId` | optional, organizational only |

`3:2`, `3:4`, `4:3` and `5:4` are **not** on this model — they exist on `nano-banana-pro` and
`reve-2.1`. The request schema is strict, so sending one is a `400` before anything is charged.
No template in the shared library needs them.

**Two newer GPT models now sit beside this one, and one of them is worth naming by hand.**
Deployed spec 2.25.0 added `gpt-image-2.5-flare` and `gpt-image-2.5-sunburst`, and the API's
default when `model` is omitted moved from `gpt-image-2` to Sunburst. This skill still locks
`gpt-image-2`, which is unchanged and still offered. **When the brief turns on label text,
small legal copy, a wordmark or a spec table coming back exact, render it on
`gpt-image-2.5-sunburst` instead.** It is the slower of the two 2.5 models and the one built to
hold fine detail. Everything in this skill carries over unaltered: the same six aspect ratios,
the same **cap of 4 `referenceAssetIds`**, the same 32,000-character prompt ceiling, the same
`sourceAssetId` edit arm, and the same price per image, so the change is the `model` value and
nothing else. `generate_image.py` refuses any value but `gpt-image-2`, so a Sunburst render is a
direct `POST /v1/images` call. Price it with the `image` arm of `POST /v1/estimates` first, the
same as any other call here.

**N variants is one call, not N calls.** Send `numImages: 4` and four images come back in
`images[]`. Do not fan out four parallel requests — that burns four of your five concurrency
slots to get the same result at the same price.

**There IS an edit mode, on the GPT models only.** `sourceAssetId` edits an existing image
instead of drawing a new one — "remove the logo on the bottle", "make the background a
kitchen counter". `POST /v1/images` since spec **2.10.0**, and since 2.25.0 on all three GPT
models; `nano-banana-pro` and `reve-2.1` do not publish the field, so an edit is a reason to
stay in this family rather than switch out of it.

Two rules the API enforces with a `400`, not a shrug:

- **`aspectRatio` cannot be sent with `sourceAssetId`.** An edit's output tracks the
  source's shape — the service measures the source and renders at the closest cell of this
  model's grid — so an `aspectRatio` alongside it would reframe the thing you asked to
  preserve. *Closest*, not exact: this grid has nothing between `1:1` and `16:9`, so a 4:3
  landscape source renders `1:1`. Portrait is never rendered landscape, or the reverse.
- **The source spends a reference slot.** Source + `referenceAssetIds` must total ≤ 4.

There is still no mask and no inpainting: you describe the change in words. If the field is
missing from `GET /v1/openapi.json`, this deployment has the arm switched off — say so
rather than retrying.

## Inputs the user must provide

| Input | Notes |
|---|---|
| Seed prompt | The creative direction in their words. You will rewrite it (see Phase 3). |
| Aspect ratio | One of the six above. Reject anything else. |
| Reference image(s) | Optional but strongly recommended when the ad features a specific product. Up to 4. |
| Variant count `N` | Default 1. Cap at 4. Each one is charged. |

## Workflow

### Phase 1: Preflight

1. `.env` exists with `NOVOADS_API_KEY`.
2. Health check: `./scripts/check-novoads-env.sh` prints OK (a 401 is a bad key; a 403 with `details.reason: plan_required` is a good key on an account without API access — different fixes).

### Phase 2: Gather inputs

Collect: seed prompt, reference paths, variant count, aspect ratio.

Present choices per `shared/skills/image-ad-prompting/OVERVIEW.md` § Presenting choices to
the user, which is one decision at a time and never this four-item brief up front.

### Phase 3: Prompt rewrite

Read `shared/skills/image-ad-prompting/prompting/prompt-library.md`. If the user's brief maps
onto a template, **check the Model notes block** — only proceed if `gpt-image-2` is marked
clean or preferred. If nano-banana-pro is preferred, suggest switching skills before generating.

Fill the `{placeholders}` and show the user the rewritten prompt. Ask "Use this, edit it, or
start over?" Loop until approved.

For fresh prompts (no template match), follow the structure in
`shared/skills/chatgpt-image-ad/prompting/guide.md` § Phase 3b.

### Phase 4: Cost confirmation (MANDATORY)

```bash
curl -sS -X POST "$NOVOADS_BASE_URL/v1/estimates" \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"kind":"image","model":"gpt-image-2","prompt":"<final prompt>","numImages":<N>}'
```

It charges nothing, and it is the only legitimate source of a price. Show the user `credits`, and whether
`sufficient` is true against their `balance`. If it is false, say so and stop — the response
carries `shortBy` and `topUpUrl`. Wait for an explicit yes before Phase 5.

Three things to know about this call:

- **It reads the image prompt too, and says so in `warnings`.** `POST /v1/estimates` returns the same advisory `warnings` array of craft notes on a `kind: "image"` call as it does on video, with rules of its own — `banned_polish` and `blank_label` both observed live on deployed spec 2.19.0 (verified live 2026-08-12). The older note here, that an image estimate came back with no `warnings` key at all, described the 2026-08-04 deployment and is retired. They are still **advisory**: none refuses the call, none changes `credits`, and they match substrings, so read each one, judge it against what your prompt actually says, and state your reasoning if you override it — never paste a suggested fix into a prompt it does not fit, and never drop one silently. The rewrite rules in Phase 3 remain the real check; this is a second opinion that costs nothing on a call you were making anyway.
- **The body is strict.** Only `kind`, `prompt`, `model`, `numImages`, `language` are accepted. Sending `aspectRatio` or `referenceAssetIds` is a `400 Unrecognized key` — the estimate never sees them, and neither affects the price.
- **Its length check is looser than this model's.** The estimate's own request schema caps `prompt` at 50,000 characters for every image model, while `POST /v1/images` caps this one at 32,000 (deployed spec 2.16.0, verified 2026-08-08). A prompt between those two numbers prices cleanly and is then refused by the generation, so a clean estimate is not proof the prompt is sendable. `generate_image.py` measures against 32,000 before either call, which is the check that decides. The estimate does **not** run moderation either, so a prompt it blessed can still come back `422 content_policy`.

Estimate the **final** prompt, the one the script will send with the safety suffixes
appended, or the quote will be short by roughly 1,500 characters' worth of prompt.

### Phase 5: Generate

```bash
./skills/chatgpt-image-ad/scripts/generate_image.py \
  --prompt "<rewritten>" \
  --aspect-ratio <ratio> \
  --n <N> \
  --image-ref <product.png> \
  [--image-ref <style-board.png>] \
  --out ./generated \
  --env-file .env
```

`--image-ref` uploads the file on every invocation. For a batch that reuses one product
photo across many prompts, upload it once and pass `--ref-asset-id <assetId>` instead —
same reference, no repeat upload. The two are interchangeable and share the 4-reference cap.

Each line on stdout is one JSON image (`variant`, `path`, `job_id`, `width`, `height`,
`prompt`, `aspect_ratio`, `model`, `credits_charged`).

Log the call to `logs/novoads-api.jsonl` per `logs/README.md` — images are written **once,
complete** (sync endpoint, no `jobId` to poll back). Record `creditsCharged` from the response,
never an estimate. Observability only, never a pricing source.

### Phase 5b: For an edit run

Same seven phases; four differences, all of them consequences of editing rather than drawing.

```bash
./skills/chatgpt-image-ad/scripts/generate_image.py \
  --prompt "Remove the sticker on the bottle. Change nothing else." \
  --source-image ./generated/T36-....png \
  --out ./generated \
  --env-file .env
```

1. **No `--aspect-ratio`.** The script refuses the pair locally, before spending, for the
   same reason the API does. Use `--source-asset-id` instead of `--source-image` when the
   image is already uploaded — re-uploading the same bytes mints a second asset.
2. **The prompt names the CHANGE and pins everything else.** "Remove the sticker" leaves the
   rest of the frame unspecified, and unspecified is what this model reinvents. Say what
   must not move: *"Change nothing else. Keep the label, the wordmark, the lighting and the
   framing exactly as they are."*
3. **The wordmark rule applies harder here, not less.** You are handing the model a picture
   that already contains brand marks — the failure mode is it re-renders them slightly
   wrong. Pass the brand's own wordmark as `--image-ref` alongside the source when the
   edit touches anything near it, and read the result for drift.
4. **Phase 6 QA is unchanged and still mandatory.** An edit is a fresh render, not a patch:
   nothing carries over pixel-for-pixel, so the whole frame is in scope for QA, not only
   the region you asked about. Compare against the source side by side.

Cost is a normal image: an edit is one image, charged once, priced by `POST /v1/estimates`
like any other. Confirm it in Phase 4 the same way.

### Phase 6: Visual QA (MANDATORY)

For each image, **read it** and inspect for:
- Garbled small text (most common gpt-image-2 failure on dense body text)
- Wordmark drift (if a brand wordmark wasn't passed as `--image-ref`)
- Wrong text count (e.g. 4 Slack messages instead of 3)
- iOS dialog / UI proportion drift

If defective: regenerate with a revised prompt explicitly correcting the issue (see
`shared/skills/chatgpt-image-ad/prompting/guide.md` § Retry mode). **Cap at 2 retries.**
Each retry is a fresh charge — there is no free re-roll — so no re-confirmation is needed
within the cap, but report the extra credits at the end of the run. After the cap, stop and
show the best attempt.

### Phase 7: Confirm and hand off

Show all paths to the user. Ask "Use all / use these specific ones / regenerate / cancel."

Open the output folder (`open` on macOS, `xdg-open` on Linux) so the user sees the results
without hunting for them.

Selected images are ready for the **`meta-ad-builder` skill**. Print the paths so the user can
pipe them. Optionally write them to `./generated/run-<ts>.jsonl` for downstream consumption.

## Full-library run

One product photo, the whole template library, one folder of finished ads. This is the
batch shape of the seven phases above — not a replacement for them. Every phase still
applies per image; what follows is the choreography around them.

**1. Inputs.** One product photo — a real product, with its real brand on it. Upload it
**once** with `POST /v1/uploads` and reuse that `assetId` on every template
(`--ref-asset-id <id>`); an `assetId` is durable, and re-uploading the same bytes per
template just mints redundant assets. Also collect the offer and brand facts the templates
interpolate (product name, claim, price, CTA). Output goes to **one flat folder** — one
folder for the whole run, not a folder per template.

**2. Estimate before anything renders.** One `POST /v1/estimates` for the run's image count
(Phase 4's rules apply unchanged: the estimate is the only price source, and it charges nothing).
Show the total against `balance` and get an explicit yes before the pilot. Decide a
**hard credit ceiling for the run at the same time**, and check it before *every* request,
retries included — if the next call would cross it, stop and report what is left rather
than finishing the set. Worst case is not the happy path: every template retried twice is
three times the quoted number. If you drive this from a script, have it read prior spend
back off its own ledger, so a second process inherits the budget instead of restarting at
zero.

**3. Pilot five, then check them yourself.** Run `T12` (fake ChatGPT), `T14` (fake Slack), `T33`
(typography hero), `T34` (iMessage), `T38` (stat hero + chart) — five templates that
exercise dense UI text, conversation layout, pure type, and chart rendering, which is where
this model fails if it is going to. **At most 4 requests in flight** (the org concurrency
cap is 5, it is org-wide, and anything else the account is running shares it). Then Phase 6
QA on all five. **This is the agent's checkpoint, not the user's**
(`shared/skills/image-ad-prompting/OVERVIEW.md` § Presenting choices to the user): when the
five read right, continue into the remainder in the same run. Stop and show the images only
when the problem is systematic (a brand wordmark drifting, the product rendered from the
wrong angle), because that flaw is worth catching before 30 more images carry it.

**4. The remainder.** When this run was entered through OVERVIEW's option 1, this
engine's set is one half of one plan: the templates the library routes to the other
generator ride the same total and render in the same run
(`shared/skills/image-ad-prompting/OVERVIEW.md` § Presenting choices to the user).
Every other template whose `Model notes` block marks `gpt-image-2`
clean or preferred. **Count them from `prompt-library.md` at run time; do not carry a number
from a previous run or from another product's library** — entries get added, and Model notes
get corrected by exactly the kind of run you are doing now. Templates marked `acceptable`,
or whose note leads with a caveat rather than "clean", are not in the set; name them in the
report as skipped rather than silently dropping them. Same 4-in-flight cap. On `429`, branch
on `details.reason`: `concurrency_limit` clears only by waiting, so honor `Retry-After`
instead of retrying tighter.

**5. One image per call.** Omit `numImages` (or send `1`). A library run wants one render
per template, and a multi-image response is the **only copy** of images 2–N — a lost
response loses them while the credits stay charged (see the `novoads-api` skill's
`reference.md`). **Write every image to disk the moment it arrives**, before starting the
next template.

**6. Report.** Per-template credits summed from each response's `creditsCharged` (never the
estimate), the defect list from QA, what retries cost, and which templates were skipped or
left unrun and why. The QA defects are the useful output: they are what corrects the Model
notes in `prompt-library.md`. File those as follow-ups — do not edit the library mid-run,
that is `clone-image-ad`'s job.

## Out of scope — fail clearly

- **Meta upload** — the `meta-ad-builder` skill.
- **Nano Banana image generation** — use `nano-banana-image-ad`.
- **Masked / inpainted editing** — `sourceAssetId` edits from a prompt; there is no mask, no region selection, no img2img strength dial. Describe the change in words.
- **Video, carousel, DCO ads** — image only. Video lives in the `novoads-api` skill.
- **Ad copy writing** — different skill.
- **Editing the shared prompt library** — use `clone-image-ad`.

## Common errors

| What you see | What it means |
|---|---|
| `400 invalid_input` with `details.issues` | A malformed field. Most often an `aspectRatio` this model doesn't take, more than 4 `referenceAssetIds`, or a prompt over the model's cap. Nothing was charged. |
| `401 unauthorized` | Missing, malformed or revoked key. Send the user to <https://novoads.ai/dashboard/settings?tab=api>. |
| `402 insufficient_credits` | `details` carries `required` and `available`. Tell the user the gap; do not retry. |
| `403 forbidden` | `details.reason` says which: `plan_required`, `subscription_inactive`, or API access off for the account. |
| `422 content_policy` | Moderation blocked it. The estimate does not run moderation, so this can land on a prompt the estimate priced cleanly. Nothing was charged. Rewrite or stop. |
| `429 rate_limited` | **Branch on `details.reason`.** `key_limit` / `organization_limit` / `client_limit` are paced by slowing down; `concurrency_limit` is not — only waiting frees a slot. Honor `Retry-After`. |
| `403` on the presigned PUT | The signed headers weren't echoed byte for byte. Send the `headers` object from `POST /v1/uploads` exactly as returned. |
| `500 internal_error` | **Do not blindly retry** — there are no idempotency keys, so a retry can double-charge. Check `GET /v1/generations` for a job that already landed. |
| `502 provider_failed` | The model provider failed. Credits are refunded automatically. |

## Files this skill owns

- `skills/chatgpt-image-ad/SKILL.md` — this file
- `skills/chatgpt-image-ad/scripts/generate_image.py` — the gpt-image-2 caller (upload + generate + download)

## See also

- `shared/skills/image-ad-prompting/OVERVIEW.md` — ecosystem hub, read first
- `shared/skills/chatgpt-image-ad/prompting/guide.md` — gpt-image-2 strengths/limits, retry playbook
- `shared/skills/image-ad-prompting/prompting/prompt-library.md` — 40 validated templates
- `shared/skills/image-ad-prompting/prompting/template-format.md` — entry skeleton for new templates
- `shared/skills/image-ad-prompting/prompting/safety-suffixes.md` — the 3 always-on guards
- the **`clone-image-ad`** skill — reverse-engineers an existing ad into a reusable library entry
- the **`nano-banana-image-ad`** skill — sibling for photoreal / lifestyle / multi-ref templates
- the **`novoads-api`** skill — the API contract underneath all of this
