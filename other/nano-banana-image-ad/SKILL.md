---
name: nano-banana-image-ad
metadata: {packVersion: 1.3.0}
description: >-
  Generate one or more standalone Meta image-ad creatives via Nano Banana Pro through the Novoads API. Locks the model, auto-strips platform chrome, enforces edge-safe layouts. Use when the user asks for a "Nano Banana ad", "Gemini image ad", "nano-banana-pro ad creative", "make a static image ad with Gemini", or anchors on a need for photoreal / lifestyle / multi-reference / handheld-object / clay-texture ad creatives (sticky-note flatlays, held-whiteboard signs, lifestyle portraits, ingredient collages, OOH photography). Does NOT trigger on ChatGPT Image cues — use chatgpt-image-ad for those.
---

# nano-banana-image-ad

Generate one or more **standalone Meta ad image creatives** via Novoads' `POST /v1/images`
with `model: "nano-banana-pro"`. Hands the image paths off to your Meta-ad-builder skill —
this skill does not upload to Meta itself.

## If the `shared/` files are not on disk

Then this skill was installed on its own from skills.sh and the rest of the pack stayed behind.
Fetch each missing file from `https://raw.githubusercontent.com/novoads/agent-skills/main/<path>`,
where `<path>` is one of `shared/skills/image-ad-prompting/OVERVIEW.md`,
`shared/skills/image-ad-prompting/prompting/prompt-library.md`,
`shared/skills/image-ad-prompting/prompting/safety-suffixes.md` and
`shared/skills/nano-banana-image-ad/prompting/guide.md`. Or take everything at once with
`git clone https://github.com/novoads/agent-skills.git`. That install has no
`scripts/check-novoads-env.sh` either, so set `NOVOADS_API_KEY` in the environment yourself and
let the first call report the key.

## Read order

Paths below are **from the repo root**. This skill is copied into `.claude/skills/` and
`.cursor/skills/` by `sync-skill.sh`, so a relative link out of it would break in those
copies — read these from the repo you are working in.

1. **This file** — endpoint, auth, upload flow, workflow phases.
2. `shared/skills/image-ad-prompting/OVERVIEW.md` — the ecosystem hub: which skill, which model, what the family does and doesn't do.
3. `shared/skills/nano-banana-image-ad/prompting/guide.md` — model-specific prompting (what Nano Banana Pro is good/bad at, when to switch to gpt-image-2).
4. `shared/skills/image-ad-prompting/prompting/prompt-library.md` — 40 validated templates with per-model notes.
5. `shared/skills/image-ad-prompting/prompting/safety-suffixes.md` — the 3 always-on guards.
6. `skills/nano-banana-image-ad/scripts/generate_image.py` — the helper script (Python stdlib only).

For anything about the API itself that this file does not answer — error codes, rate limits,
concurrency, the upload contract — the `novoads-api` skill's `reference.md` is the authority.

## Hard rules — never relax

1. **Model is `nano-banana-pro`.** It is the only Nano Banana on this API — there is no `nano-banana-2`, no `nano-banana-edit`, no legacy `nano-banana`. The script refuses anything else. If the user asks for gpt-image-2, point them at `chatgpt-image-ad`.
2. **No platform/screenshot chrome in output.** `NO_CHROME_SUFFIX` is always on (override only with `--allow-chrome`).
3. **Edge-safe + glyph-safety suffixes always on** unless `--no-safe-zone` is explicit.
4. **Max 14 reference images.** `referenceAssetIds` caps at 14 on `nano-banana-pro` (spec 2.7.0; `gpt-image-2` takes 4, `reve-2.1` 8). The script enforces it — and 2-4 well-chosen references usually beat many.
5. **Every brand mark that appears in the frame is passed as a reference asset.** Not a tip — a rule. Image models invent brand-shaped content on any surface the prompt leaves unspecified, and state it as fact. Measured on the sibling model over a 34-template run (2026-08-04): the product label was faithful in **all 34** because a reference pinned it, while unpinned marks failed three ways — an invented back-of-can panel carrying a sourcing claim nobody wrote, a **Hydro Flask logo** on a prop thermos, and a drifted publication wordmark. This model's 14-reference headroom makes the rule cheap to follow: pin the product, the logo, and any third-party mark the concept needs. For product surfaces the ad does **not** show, say so explicitly (*"front label only; no invented label copy, no barcode"*). Unpinned means invented. **Pass it as `--pin-block "<one-line product description>"`** rather than writing the clause by hand: the script wraps the shared library's standard 346-character guard around your description, counts it against this model's prompt cap (50,000 characters, the largest on the API, deployed spec 2.16.0, verified 2026-08-08), and refuses pre-network naming the pin block's share if it does not fit. Hand-written pin blocks ran ~700 characters and used to be the single largest cause of a refused prompt, back when the cap was 4,000 on every model. At 50,000 that pressure is gone, and the reason to pass `--pin-block` is that the standard guard is the wording that was measured to work.
6. **No Meta upload from this skill.** Image generation only. Hand off via filesystem paths.
7. **Always show a live cost estimate before generating, and get an explicit yes.** The price comes from `POST /v1/estimates` in this session — never from memory, never from `logs/novoads-api.jsonl`, never from `MASTER_CONTEXT.md`. There are no credit numbers written down anywhere in this repo, on purpose. Nano Banana Pro costs more per image than gpt-image-2, so the model choice is worth surfacing when you show the quote.

## Prerequisites

- `.env` containing `NOVOADS_API_KEY` (`novo_` + 64 hex, created at <https://novoads.ai/dashboard/settings?tab=api>). Verify with `./scripts/check-novoads-env.sh`.
- Optional: `PRODUCT_ID` in `.env` so generated assets are filed under a specific product. Omit it and the job lands in your default product. `productId` is **organizational only** — it does not influence what is generated.
- Reference images on local disk (PNG/JPG/JPEG/WEBP). The script handles the upload flow internally.

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
- **Reference uploads:** `POST /v1/uploads` with `{contentType, sizeBytes}` returns `{assetId, uploadUrl, method, headers, expiresInSeconds, maxBytes}`. `PUT` the raw bytes to `uploadUrl` **echoing the returned `headers` byte for byte** — Content-Type and Content-Length are both part of the signature, so storage returns 403 if either differs. The resulting `assetId` is **durable and reusable**: upload a character or product shot once and pass the same id on every later call. That is what makes cross-run identity consistency cheap here.

## What this model takes

| Field | Value |
|---|---|
| `model` | `nano-banana-pro` |
| `prompt` | the image prompt — the always-on suffixes count against the model's cap |
| `aspectRatio` | `1:1` `2:3` `3:2` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` — **defaults to `1:1`**, so always set it |
| `referenceAssetIds` | up to **14**, order preserved, addressable positionally from the prompt |
| `numImages` | `1`–`4`, **one call**, charged per image |
| `productId` | optional, organizational only |

This model takes the **full ratio set** — including `3:2`, `3:4`, `4:3` and `5:4`, which
`gpt-image-2` does not. That is the one hard reason to route a bespoke prompt here regardless
of style.

**N variants is one call, not N calls.** Send `numImages: 4` and four images come back in
`images[]`. Do not fan out four parallel requests — that burns four of your five concurrency
slots to get the same result at the same price.

**There is no edit mode on THIS model.** The Nano Banana inpainting flows the older skill
had do not exist on this API — no `nano-banana-edit`, no mask, no img2img — and
`nano-banana-pro` does not publish `sourceAssetId`. Editing an existing image is a
`gpt-image-2` capability (spec 2.10.0): route it to `chatgpt-image-ad` rather than
approximating it here with a reference-led regeneration.

## Inputs the user must provide

| Input | Notes |
|---|---|
| Seed prompt | The creative direction in their words. You will rewrite it (see Phase 3). |
| Aspect ratio | One of the ten above. Reject anything else. |
| Reference image(s) | Optional but strongly recommended for a specific product, character or brand mark. Up to 14. |
| Variant count `N` | Default 1. Cap at 4. Each one is charged. |

## Workflow

### Phase 1: Preflight

1. `.env` exists with `NOVOADS_API_KEY`.
2. Health check: `./scripts/check-novoads-env.sh` prints OK (a 401 is a bad key; a 403 with `details.reason: plan_required` is a good key on an account without API access — different fixes).

### Phase 2: Gather inputs

Collect: seed prompt, reference paths (up to 14), variant count, aspect ratio.

Present choices per `shared/skills/image-ad-prompting/OVERVIEW.md` § Presenting choices to
the user, which is one decision at a time and never this four-item brief up front.

### Phase 3: Prompt rewrite

Read `shared/skills/image-ad-prompting/prompting/prompt-library.md`. If the user's brief
matches a template, **check the Model notes block** — only proceed if nano-banana is marked
clean, preferred, or strong. If gpt-image-2 is preferred, suggest switching skills.

Fill `{placeholders}` and show the user the rewritten prompt. Ask for approval before generating.

For fresh prompts (no template match), follow the structure in
`shared/skills/nano-banana-image-ad/prompting/guide.md` § Phase 3b — lean on Nano Banana
strengths (named reference roles, lighting specifics, material specifics).

### Phase 4: Cost confirmation (MANDATORY)

```bash
curl -sS -X POST "$NOVOADS_BASE_URL/v1/estimates" \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"kind":"image","model":"nano-banana-pro","prompt":"<final prompt>","numImages":<N>}'
```

It charges nothing, and it is the only legitimate source of a price. **Name the model in the estimate body** — the
image models' schedules differ by more than 3×, so pricing the wrong one is a quote that
disagrees with the invoice. Show the user `credits`, and whether `sufficient` is true against
their `balance`. If it is false, say so and stop — the response carries `shortBy` and
`topUpUrl`. Wait for an explicit yes before Phase 5.

Three things to know about this call:

- **It reads the image prompt too, and says so in `warnings`.** `POST /v1/estimates` returns the same advisory `warnings` array of craft notes on a `kind: "image"` call as it does on video, with rules of its own — `banned_polish` and `blank_label` both observed live on deployed spec 2.19.0 (verified live 2026-08-12). The older note here, that an image estimate came back with no `warnings` key at all, described the 2026-08-04 deployment and is retired. They are still **advisory**: none refuses the call, none changes `credits`, and they match substrings, so read each one, judge it against what your prompt actually says, and state your reasoning if you override it — never paste a suggested fix into a prompt it does not fit, and never drop one silently. The rewrite rules in Phase 3 remain the real check; this is a second opinion that costs nothing on a call you were making anyway.
- **The body is strict.** Only `kind`, `prompt`, `model`, `numImages`, `language` are accepted. Sending `aspectRatio` or `referenceAssetIds` is a `400 Unrecognized key` — the estimate never sees them, and neither affects the price.
- **Its length check happens to match this model's.** The estimate's own request schema caps `prompt` at 50,000 characters for every image model, which is exactly this model's ceiling on `POST /v1/images` (deployed spec 2.16.0, verified 2026-08-08). The agreement is a coincidence of this being the roomiest model on the API: on `gpt-image-2` (32,000) and `reve-2.1` (4,000) the estimate is the looser of the two and will price a prompt the generation then refuses. It does **not** run moderation either, so a prompt it blessed can still come back `422 content_policy`.

Estimate the **final** prompt, the one the script will send with the safety suffixes
appended, or the quote will be short by roughly 1,500 characters' worth of prompt.

### Phase 5: Generate

```bash
./skills/nano-banana-image-ad/scripts/generate_image.py \
  --prompt "<rewritten>" \
  --aspect-ratio <ratio> \
  --n <N> \
  --image-ref <product.png> \
  [--image-ref <character.png>] \
  [--image-ref <style.png>] \
  --out ./generated \
  --env-file .env
```

`--image-ref` uploads the file on every invocation. For a batch that reuses one product
photo — or the same character shot, which is what holds a face steady across runs — upload
it once and pass `--ref-asset-id <assetId>` instead: same reference, no repeat upload. The
two are interchangeable and share the 14-reference cap.

Each line on stdout is one JSON image (`variant`, `path`, `job_id`, `width`, `height`,
`prompt`, `aspect_ratio`, `model`, `credits_charged`).

Log the call to `logs/novoads-api.jsonl` per `logs/README.md` — images are written **once,
complete** (sync endpoint, no `jobId` to poll back). Record `creditsCharged` from the response,
never an estimate. Observability only, never a pricing source.

### Phase 6: Visual QA (MANDATORY)

For each image, **read it** and inspect for:
- Garbled small text (the main Nano Banana weakness — if the ad is text-led, it belongs in `chatgpt-image-ad`)
- Extra fingers / wrong limb count (common Gemini-family failure)
- Wordmark drift (always pass brand wordmarks as `--image-ref` to mitigate)
- Character identity drift across variants — reuse the **same `assetId`** for the character reference on every call, which is what keeps a face consistent across runs

If defective: regenerate with a revised prompt explicitly correcting the issue (see
`shared/skills/nano-banana-image-ad/prompting/guide.md` § Retry mode). **Cap at 2 retries.**
Each retry is a fresh charge — there is no free re-roll — so no re-confirmation is needed
within the cap, but report the extra credits at the end of the run. After the cap, stop and
show the best attempt.

### Phase 7: Confirm and hand off

Show all paths to the user. Ask "Use all / use these specific ones / regenerate / cancel."

Open the output folder (`open` on macOS, `xdg-open` on Linux) so the user sees the results
without hunting for them.

Selected images are ready for the **`meta-ad-builder` skill**. Print the paths. Optionally
write them to `./generated/run-<ts>.jsonl` for downstream consumption.

## Out of scope — fail clearly

- **Meta upload** — the `meta-ad-builder` skill.
- **ChatGPT Image 2 / gpt-image-2 generation** — use `chatgpt-image-ad`.
- **Editing an existing image** — no model on this API has an edit or inpainting path. Offer a fresh generation with the original as a reference.
- **Video, carousel, DCO ads** — image only. Video lives in the `novoads-api` skill.
- **Ad copy writing** — different skill.
- **Editing the shared prompt library** — use `clone-image-ad`.

## Common errors

| What you see | What it means |
|---|---|
| `400 invalid_input` with `details.issues` | A malformed field. Most often more than **14** `referenceAssetIds` — that is this model's cap, and 4 is `gpt-image-2`'s, so do not carry the sibling's number here — a `numImages` above 4, or a prompt over this model's 50,000 characters. The refusal reads `Too big: expected array to have <=14 items`. Nothing was charged. |
| `401 unauthorized` | Missing, malformed or revoked key. Send the user to <https://novoads.ai/dashboard/settings?tab=api>. |
| `402 insufficient_credits` | `details` carries `required` and `available`. Tell the user the gap; do not retry. |
| `403 forbidden` | `details.reason` says which: `plan_required`, `subscription_inactive`, or API access off for the account. |
| `422 content_policy` | Moderation blocked it. The estimate does not run moderation, so this can land on a prompt the estimate priced cleanly. Nothing was charged. Rewrite or stop. |
| `429 rate_limited` | **Branch on `details.reason`.** `key_limit` / `organization_limit` / `client_limit` are paced by slowing down; `concurrency_limit` is not — only waiting frees a slot. Honor `Retry-After`. |
| `403` on the presigned PUT | The signed headers weren't echoed byte for byte. Send the `headers` object from `POST /v1/uploads` exactly as returned. |
| `500 internal_error` | **Do not blindly retry** — there are no idempotency keys, so a retry can double-charge. Check `GET /v1/generations` for a job that already landed. |
| `502 provider_failed` | The model provider failed. Credits are refunded automatically. |

## Files this skill owns

- `skills/nano-banana-image-ad/SKILL.md` — this file
- `skills/nano-banana-image-ad/scripts/generate_image.py` — the nano-banana-pro caller (upload + generate + download)

## See also

- `shared/skills/image-ad-prompting/OVERVIEW.md` — ecosystem hub, read first
- `shared/skills/nano-banana-image-ad/prompting/guide.md` — model-specific prompting, retry playbook
- `shared/skills/image-ad-prompting/prompting/prompt-library.md` — 40 validated templates
- the **`clone-image-ad`** skill — reverse-engineers an existing ad into a reusable library entry
- the **`chatgpt-image-ad`** skill — sibling for typography-heavy / UI-mimicry templates
- the **`novoads-api`** skill — the API contract underneath all of this
