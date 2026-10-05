---
name: generate-youtube-thumbnail
metadata: {packVersion: 1.3.0}
description: >-
  Generate high-CTR YouTube thumbnails using Nano Banana Pro via the Novoads API. Handles reference image upload, character likeness alignment, proven CTR-tested prompt formulas, and bounded batch generation. Use when the user asks to create a YouTube thumbnail, video thumbnail, A/B test thumbnail variations, or refers to thumbnail design with their face, brand assets, or product photos.
---

# Generate YouTube Thumbnail

A reusable workflow for creating YouTube thumbnails via Novoads' `POST /v1/images` with
`nano-banana-pro`, with proper character likeness and proven CTR formulas.

## When to use this skill

Trigger on phrases like:
- "make me a YouTube thumbnail"
- "create a thumbnail for this video"
- "I need thumbnail variations / A/B tests"
- "remake this thumbnail with my face"
- "generate 10 thumbnail concepts"
- "thumbnail with [me / my product / my brand]"

## Read order

Paths below are **relative to this skill's own folder**, and every file they name ships inside
it. That holds wherever the folder lands: the repo, the `.claude/skills/` and `.cursor/skills/`
copies `sync-skill.sh` makes, or a standalone install of just this skill.

1. **This file** — workflow, decision tree, batch generation
2. `prompting/guide.md` — likeness alignment, expressions cheat sheet, prompt structure
3. `prompting/formulas.md` — 5 proven thumbnail formulas with templates
4. `scripts/generate-batch.sh` — the batch script (upload once → generate → download)

For the API contract itself — error codes, rate limits, the upload flow — the `novoads-api`
skill's `reference.md` is the authority.

## Prerequisites

- `.env` with `NOVOADS_API_KEY` (`novo_` + 64 hex). Verify with `./scripts/check-novoads-env.sh`.
- Optional `PRODUCT_ID`. Omit it and jobs land in your default product; `productId` is organizational only and does not influence what is generated.
- Reference images on disk (NOT pasted in chat — chat-pasted images are NOT accessible to the API):
  - `face/` — several photos of the subject (headshot + 3/4 angles + close-ups + expressions)
  - `logos/` — brand logos as files
  - `products/` — clean product shots
  - `examples/` — real ad screenshots, comparison material
  - `style/` — example thumbnails the user wants to match aesthetically

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

If references are missing or the user pastes images in chat instead of saving them, **stop and
ask the user to drop the actual files into a project folder** (e.g. `references/youtube thumbnail/`).
Chat paste ≠ file on disk.

## References — how many, and why it changed back

**`nano-banana-pro` accepts up to 14 `referenceAssetIds` per generation**, which is fal's own
published ceiling for the `/edit` arm this workflow calls, confirmed by probe on 2026-08-03. This
skill runs on `nano-banana-pro`, so the fork's original advice applies here unchanged.

For a while this pack said the cap was 4 on every image model and that "always use 5+ face
references" was void. That was our own held number, carried from a shared constant and never tested
against the transport we serve this model from. It has been corrected.

Two facts still shape how you spend them:

1. **An `assetId` is durable and reusable.** Upload once, reference forever, across runs and across
   sessions. Uploading is free and unlimited — only *generations* are charged. So keep a library of
   uploaded face angles and brand assets and pick from it.
2. **The other image models are lower.** `reve-2.1` takes 8; `gpt-image-2` takes 4, and that 4 is
   measured, not assumed — a 5-reference body was refused on the same 2026-08-04 probe run. If you
   route a likeness run to `gpt-image-2`, the 5+ advice does not survive the trip; say so rather
   than silently citing four.

**Always use 5+ face references for character work.** With 1-2 the model generalizes to a
generic face; with 5+ from different angles it locks in the specific person. Spend them: headshot,
3/4 angle, studio close-up, one smiling, one neutral, plus any brand asset that must be
pixel-accurate.

**Rolling window for a series** (ported from the character-sheet workflow): when generating
variation N, pass `[hero, N-1, N-2, N-3, N-4]` — the approved hero shot as the anchor plus the
four most recent good outputs. **Drop any variation that drifted** rather than feeding it
forward; a bad reference propagates.

If the user insists on more coverage, the answer is more *prompt* specificity, not more refs.

## Workflow

### 1. Gather requirements (in order)

Ask the user for any missing context, but only what you actually need:

1. **Concept** — what's the video about? Single concept, A/B variations, or specific recreation of an existing thumbnail style?
2. **Subject** — who is in the thumbnail (the user themselves, an AI character, no person)?
3. **Brand assets** — which logos / products / brand colors should appear?
4. **Text** — what should the title text say? Will text be baked in, or added in post (Canva/Photoshop)?
5. **Comparison material** — for "real vs AI" thumbnails, what real ad and what AI-generated ad?

### 2. Verify references exist on disk

```bash
ls "references/youtube thumbnail/"
```

If references are missing, ask the user to drop them. **Do not proceed with text-only
descriptions for brand-specific items** (logos, branded products, branded apparel) — you'll get
generic AI approximations that don't match the brand. Generic descriptions are OK for
backgrounds, expressions, and clothing.

Then pick the ones that will be cited — 5+ face angles for character work, up to 14 in all
(see the cap section above).

### 3. Price the batch and confirm (MANDATORY)

```bash
curl -sS -X POST "$NOVOADS_BASE_URL/v1/estimates" \
  -H "Authorization: Bearer $NOVOADS_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"kind":"image","model":"nano-banana-pro","prompt":"<one composed prompt>","numImages":1}'
```

It charges nothing, and it is the **only** legitimate source of a price. Multiply by the number of variations and
show the user the total against their `balance` before firing anything. Wait for an explicit
yes.

Never quote a credit figure from memory, from `logs/novoads-api.jsonl`, or from
`MASTER_CONTEXT.md` — there are no credit numbers written down anywhere in this repo, on
purpose. **Name the model in the estimate body**: the image models' schedules differ by more
than 3×, and an estimate that omits `model` prices `gpt-image-2.5-sunburst`, understating a
`nano-banana-pro` batch.

The call says nothing about the prompt — no endpoint on this API reads one for quality. Re-read
the prompt against the formula yourself before pricing: a batch runs the same shape N times, so
a flaw in it is paid for N times.

### 4. Pick a formula

See `prompting/formulas.md` for the 5 proven formulas.
Match the user's intent:

| User says... | Use formula |
|---|---|
| "Just me with my brand" / "branding thumbnail" | **Peace-sign / branding** |
| "Real vs AI" / "compare" / "before/after" | **Real vs AI comparison** |
| "Show the process" / "with the terminal" | **Terminal flow** |
| "Surprised face" / "shocked reaction" | **Reaction shock** |
| "Replace" / "alternative" / "swap out" | **Before/after split** |

### 5. Compose prompts

Follow the template in `prompting/guide.md`:

```
YouTube thumbnail, 16:9 landscape.
[SUBJECT — likeness block + clothing + framing + "no hands" if applicable]
Expression: [specific expression from expressions cheat sheet]
[LEFT visual element + reference]
[RIGHT visual element + reference]
Across the top in massive bold yellow block letters with thick black outline reads [TITLE].
Background: [color + glow]
Style: [aesthetic notes]
Avoid: distorted face, extra fingers, hands visible, blurry logos, generic face
```

**Always include the CRITICAL CHARACTER LIKENESS block** when the subject is a real person. It
and the references do different jobs: the refs fix what the face IS, the block fixes what the
prompt must not let drift. Neither substitutes for the other, so write both.

Prompts are capped per generation; the API names the limit if you exceed it. Reference the uploaded images positionally ("the face in
the first reference image") — order is preserved.

### 6. Generate (use the batch script)

Copy `scripts/generate-batch.sh` to a new versioned script (`scripts/generate-thumbnails-vN.sh`)
and modify:

1. Update `REF_BASE` and `COMMON_REFS` (max 14 — the script's `REF_CAP`) with your reference file paths
2. Replace the `PROMPTS` array entries with your composed prompts
3. Run with `bash scripts/generate-thumbnails-vN.sh > output/run.log 2>&1 &`
4. Monitor with `tail -F output/run.log | grep -E "DONE|FAILED|charged"`

The script handles:
- Image preprocessing (Lanczos to 1080px longest side, RGB JPEG)
- **Upload once, reuse the assetIds for every prompt in the batch**
- Each call blocks ~60–90s and returns the image; one still going after about 105 s answers `running` and the script polls it (API 2.39.0)
- Bounded parallelism (4 in flight, under the API's concurrency ceiling of 5)
- Per-run credit total from each response's `creditsCharged`

### 7. Review and present

After all generations complete, read each thumbnail with the Read tool and present:

- Brief verdict per thumbnail (likeness, readability, emotional impact)
- Top 3 picks ranked by CTR potential
- Specific reasons for the picks (which expression, which color contrast, which formula)
- Offer next-step refinements (different expression, background color, copy variation)
- **The total credits actually charged**, summed from the responses — not the estimate

## Quirks and pitfalls

### Reference assetIds are durable — reuse them

This is the **opposite** of how the previous backend worked, where a reused reference caused
`HTTP 500 UNKNOWN_ERROR` and every generation needed a fresh upload. On Novoads,
`POST /v1/uploads` returns an `assetId` that keeps working across calls and across sessions.
Upload once per batch — or once per campaign — and reuse. Re-uploading the same face photo
produces a *different* id and quietly loses the anchor that was holding likeness steady.

The presigned `uploadUrl` does expire (`expiresInSeconds` in the response), but that only
affects the PUT window, not the `assetId`.

### The signed upload headers must be echoed exactly

`POST /v1/uploads` returns a `headers` object. The `PUT` must send those headers byte for byte —
Content-Type and Content-Length are both part of the URL signature, so storage answers `403` if
either differs, including an added `; charset=…`. Don't let an HTTP client infer the type.

### Image preprocessing is practice, not a documented requirement

The old "images smaller than 1080px longest side return `422 — image too small`" rule was
specific to the previous backend and **has not been verified against Novoads**. The batch script
still upscales, because small references genuinely produce worse likeness — but do not report
the 422 claim to a user as an API rule. (Flagged for confirmation in the Phase 4 live smoke.)

### `referenceAssetIds` is an array of plain strings

Not objects, and not file paths — the `assetId` values returned by `POST /v1/uploads`.
Maximum 14 on `nano-banana-pro`, which is the model this skill runs on. The other image
models are lower and the number does not travel: `reve-2.1` takes 8, `gpt-image-2` takes 4.

### Chat-pasted images are NOT files

If the user pastes an image directly in chat, you cannot pass it to the API. Ask them to save
the actual file into a project folder.

### Likeness drift with too few references

With 1-2 face references the AI generalizes to "generic bearded man with glasses." With 5+ face
references from different angles it locks in the specific person. **Always use 5+ face references
for character work.** For a series, use the rolling window described above.

### Concurrency is 5, not "as many as you like"

The API allows 5 concurrent generations per organization. A 6th in flight returns `429` with
`details.reason: concurrency_limit` — and unlike the other 429 causes, **slowing your request
rate does not help**; only a finishing job frees a slot. The batch script caps itself at 4 in
flight for headroom.

### Do not blindly retry a failed generation

There are no idempotency keys on this API, so resubmitting after a timeout or a `500` can
render and charge twice. Check `GET /v1/generations` for a job that already landed before
resubmitting. The batch script deliberately does not auto-retry.

### macOS bash 3.2

Default macOS bash doesn't support `declare -A` (associative arrays). The batch script uses
indexed arrays instead.

### Brand-specific items need actual reference files

Text descriptions of brand-specific items (logos, branded apparel, custom merchandise) produce
generic approximations. For pixel-accurate brand reproduction, save the actual brand asset to
disk and cite it as one of your references.

## Cost

There is no cost table in this file, deliberately. Every price comes from a live
`POST /v1/estimates` in the current session, shown to the user and approved before anything is
generated (see step 3). Report the real total from `creditsCharged` when the run finishes.

`nano-banana-pro` costs more per image than `gpt-image-2`. If a batch is exploratory and the
concept doesn't depend on photoreal likeness, pricing both is worth the two estimates, which charge nothing.

## See also

- `prompting/guide.md` — likeness alignment, expressions, prompt structure
- `prompting/formulas.md` — 5 proven CTR formulas with prompt templates
- `scripts/generate-batch.sh` — the batch generator
- the **`novoads-api`** skill — endpoint, upload flow, error codes, rate limits
- the **`nano-banana-image-ad`** skill — the same model, pointed at Meta ad creatives
