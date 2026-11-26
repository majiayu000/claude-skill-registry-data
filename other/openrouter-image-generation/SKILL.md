---
name: openrouter-image-generation
description: "Generate or edit images via OpenRouter."
license: MIT
allowed-tools: Read Bash
metadata:
  author: project
  version: "1.0"
  category: Creative
  tags:
    - creative
    - image-generation
    - openrouter
---

# OpenRouter Image Generation & Editing

## When to use

- User asks to generate an image with AI (OpenRouter models).
- User asks to edit an image (change region, object, style).

## Hard rules

1. **Every generated image goes to `~/Documents/studio/output/images`**, named `<YYYYMMDD-HHMMSS>_<model>_<what>.<ext>`, with `_index.md` listing them. **The timestamp goes first** so a directory listing sorts by time; a model-first name groups renders by model and loses the order they were made. The studio renderer defaults there. Never a scratch or temp dir for a render that matters.
2. **No model judges an image — not vision, not me, not another agent.** No scoring, ranking, pass/fail or "checking" of generated output, and never report what an image looks like as a finding. **The user judges quality.** Report parameters and cost, hand over the files.
3. **A claim may rest only on parameters, cost, spec text, or the user's own verdict.** Every historical scoring claim in these skills was produced by a model reading pixels; the two that were checked by eye were both wrong.
4. Depth on mechanics, model facts and pitfalls: the `image-model-craft` skill.

## Model selection (speed, reference capacity, cost — never a quality ranking)

**There is no valid quality ranking between these models, and no model may produce one.**
An earlier three-model comparison ranked them on a fixed binary rubric; every check was
produced by a model reading the images, at least one check was invented (it scored a
spec-mandated prop as a violation), and the ranking was withdrawn. What remains factual
is selection criteria: latency, reference-plate ceiling, supported resolutions and
aspects, and cost. Choose on those, and let the user judge the output.

1. `qwen/qwen-image-2.1-turbo` or `bytedance-seed/seedream-5-0-flash` — the defaults. flash is fastest (~18-29s); qwen is ~36-49s and takes `n` up to 6, so it can return several samples in one call. They cap at 4 and 14 reference images respectively.
2. `bytedance-seed/seedream-5-0-pro` — only when a long multi-character brief needs its extra detail. Expect ~109-178s and occasional transient failures (retry once; it succeeded on retry here both times).
3. `openai/gpt-image-*` — premium tier, 16 references. **Read the parameter enum before calling it:** `openai/gpt-image-2.5-sunburst` has NO `resolution` parameter (size follows `aspect_ratio` + `quality`, which runs up to `max`) and NO 4:5 aspect (`1:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16, 21:9, auto`) — 3:4 at `xhigh` returned 1152x1536. An unsupported pair costs you a failed call.
4. `meta/muse-image` — only when explicitly asked for it, and only after checking the brief won't trip Meta's filter (see Pitfalls). ~35s, ~$0.01 at 1K.

**NEVER use `google/gemini-3-pro-image` (Nano Banana Pro) unless Charles asks for it by name.** He has ruled it out — it _sucks and is expensive_: ~$0.14/image, roughly 8x the Seedream render he kept, with worse results on long briefs (it floated a phantom into a cinema screen instead of staging it on the stage, and drew hand tattoos the brief forbade). Cost with no quality edge is a hard no.

**Match the model's reference capacity to the cast before choosing.** `supported_parameters.input_references` caps how many reference images a model accepts, and it varies by nearly an order of magnitude: `qwen/qwen-image-2.1-turbo` accepts **0-4**, while `bytedance-seed/seedream-5-0-flash`, `-pro` and the Gemini image models accept **0-14**. Ask a model for more references than it supports and the surplus is silently dropped — which looks exactly like a model that cannot hold identity. Read the cap from `GET /api/v1/images/models` for the chosen model and compare it against the number of characters that need a plate. Same endpoint also reports supported `resolution` and `aspect_ratio` enums, so an unsupported pair is caught before the request rather than at it.

## Key facts

- Image models live on a SEPARATE endpoint from chat models: list with `GET /api/v1/images/models`, generate with `POST /api/v1/images/generations` (`{model, prompt, aspect_ratio, resolution, n}`). A model absent from `/api/v1/models` may still exist here (e.g. `meta/muse-image`).
- `meta/muse-image`: Meta's agentic image model; reasons before rendering, ~35s, ~$0.01 at 1K. Same request shape as the others.
- `resolution` enum is 1K/2K/4K for the Google and Qwen families; passing it does not guarantee the pixel size you expect (a 2K 4:5 Gemini request returned 928x1152) — check with `sips -g pixelWidth -g pixelHeight`.
- API: chat completions with `modalities: ["image"]`. Response has `choices[0].message.images[0].image_url.url` (data URL).
- The images endpoint returns `data[0].b64_json` (plus a `usage` block carrying `cost`) — not `choices`.
- Alternate request shape, and the one that supports **reference images**: `POST /api/v1/images` with `{model, prompt, input_references: [{type: 'image_url', image_url: {url: <dataURL>}}], aspect_ratio, resolution, output_format}`. Returns `data[0].b64_json` and puts the generation id in an `X-Generation-Id` response header.
- **Read the price off the response.** Every image response carries a `usage` block; `usage.cost` is that render's actual price and `completion_tokens_details.image_tokens` is the image share. Do not fetch `/api/v1/generation` with an image id — it 404s, which is how a pipeline can look correct and report every render as unpriced. **Measured**: `qwen/qwen-image-2.1-turbo` is **$0.0184 flat at 1K and 2K with three reference plates attached**, i.e. the plate count and resolution did not move the price on this model. An earlier claim that plates cost ~100× a bare render came from bracketing a coarse daily counter and is withdrawn: the response is authoritative, the counter is not.
- Attached references do change what a render costs on models that bill them (`seedream-5-0-pro`: $0.045 base + $0.002 per reference), so read the number per model instead of carrying an assumption across models. They also fight the scene prompt when the reference is a character study rather than the subject — a design lock appended to every clip or frame prompt will contradict scenes that do not feature that character.
- For editing: pass original image as `image_url` in user message content array + text prompt.
- Speed: 18-29s per image on the fast models (`seedream-5-0-flash`), 36-49s on the default (`qwen-image-2.1-turbo`). Cost: **$0.0184** per render on `qwen-image-2.1-turbo`, flat across 1K/2K and across 0-3 attached plates — measured from `usage.cost` in the response, not bracketed from a counter.

## Logging convention

- Scripts are bundled in this skill under `scripts/`. Read them from the skill dir; run them from anywhere.
- `scripts/or_image_gen.py <out.png> "<prompt>" [model] [aspect] [resolution]` — or `@file.txt` as the prompt arg. Use it instead of hand-rolling a script; pass `resolution`/`aspect_ratio` only for models that support them.
- `scripts/gen_and_log.py <out.png> "<prompt>" [model]` — older chat-completions variant, same logging.
- `scripts/image_edit_server.py` — click-to-edit server (port 8811).
- `scripts/render_sweep.sh` — resume-safe model x spec x N-sample sweep. Every image lands in the inbox with the required naming, one log line per attempt, and a rendered/skipped/failed summary. Output names are stable per sweep, so re-running the SAME command after a kill renders only what is missing. Run it as a tracked background job; override `RENDERER=` / `INBOX=` if you are not using the studio renderer.
- Logs one `<usage dir>/<timestamp>.json` per attempt (model, prompt size, elapsed, status, cost, output path). Every attempt is billed whether or not it returns an image, so the filtered ones must be logged too — an unlogged session makes its own spend unaccountable.
- The usage dir is `$OPENROUTER_IMAGE_USAGE_DIR` if set, else `${HOMINEM_HOME:-~/.hominem}/ai_usage`.

## Prompt voice: state what IS, never what to exclude

**Write every prompt in positive voice. Do not name a thing you want absent, in any grammatical form.** Image conditioning does not represent negation: the tokens carry the noun regardless of the "no" or "never" in front of them, so mentioning a thing raises the odds of it appearing. Charles's standing rule, from his own research: _anything that gets mentioned pushes models to include it._

- Express absence by **omission**, not prohibition. "No dog in this frame" names the dog; leave it out. Gaze, count and content constraints belong in the _positive_ clause that already exists ("every gaze is fixed on the costume") — a parallel negative adds nothing and invites the failure.
- Convert prohibitions to the positive state of the thing: _"never transparent"_ → _"the robe is dense opaque cloth"_; _"no tattoos on his hands"_ → _"his hands are clean bare skin"_; _"no readable text"_ → _"every surface is plain and unlettered"_; _"two round holes… no ventilation dots, no perforations, no other holes"_ → _"one smooth black surface with two round holes at the eyes"_.
- **The exception is text/watermark suppression** ("no readable text, no logos, no watermark"), where the training signal is strong enough that the negative earns its place. That is one clause, not fifty.
- **Audit a compiled or templated prompt by counting**, don't eyeball it: `grep -oiE '\b(no|never|not|none|without|nothing|nobody)\b' prompt.txt | wc -l`. A frame-sized prompt over ~30 negation words is mostly prohibition and is fighting itself.
- **An assembled prompt has more sources than the prose you can see — count per SOURCE, not per file.** Rewriting the obvious text (character blocks, the constraints list) left 45 negation words in _every_ frame, because the same voice also arrived from prop `description`/`state` fields, structured outfit descriptions held in a registry, per-object data records, and the generator's own emitted clauses — one of which the generator was inserting itself, in violation of the rule it documents. Bucket the hits by the clause they land in (`CONTENT`, `STAGING`, `PROP`, `STATE`, the verbatim block, `RENDER GRADE`), re-measure after every pass, and treat a bucket you believed was clean as a source you have not looked at yet: a source-level tally ("the canon is at zero") says nothing about the compiled output. Applies to any pipeline that assembles a prompt from canon + spec + generator.
- **Rewrite the generator, not the generated text.** When an emitted prompt violates the voice rule, patching the output fixes one render and leaves the generator producing the same anti-pattern for every other frame and item — including when the offending clause sits in a shared block appended to every prompt rather than in any per-frame source.
- **Before paying for a voice A/B, prove the two arms actually differ.** A flag that selects a variant is worthless if the code path resolves to an older build that ignores it: both arms then render the identical prompt and the experiment "proves" the change made no difference. Diff the two compiled prompts — length plus the clauses that differ — before spending on a single render.
- **Confirm a quoted source is version-controlled before a bulk rewrite of it.** Hand-authored canon, specs and prompt text are frequently untracked (`??` in `git status`) while looking like part of the repo, so they have no history to fall back on. Capture the current text to a dated file first, then commit it so the rewrite is reviewable.
- Full rationale, the anti-pattern to recognise, and the measured before/after: `references/prompt-voice.md`.

## Procedure: generate

1. Source `~/.localrc` for `OPENROUTER_API_KEY` (usually not in `${HOMINEM_HOME:-~/.hominem}/.env`).
2. Prefer `scripts/or_image_gen.py` — it builds the payload, saves the image and logs usage in one step.
3. Extract the image from `data[0].b64_json`; save to a file.
4. Confirm the log line landed in the usage dir.
5. **Never judge the render — file it and hand it over.** No vision inspection, no scoring, no "does it match the brief" verdict on generated output. Report model, prompt sha256, aspect, resolution, real pixel size, cost and file path, then let Charles judge. This is absolute, and it is not a shortcut: model reads of small objects and downscaled panels are unreliable and a leading question is answered affirmatively — two fabricated findings came out of one image that way and were caught only by the user's eye.
6. **Deliver into the inbox and read the path back off disk before quoting it.** `~/Documents/studio/output/images/<YYYYMMDD-HHMMSS>_<model>_<what>.<ext>` (the studio renderer's default; timestamp first so the folder sorts), keep `_index.md` current. A path written from memory rather than from the filesystem is a dead link; if you use a `MEDIA:` line, the path in it must already exist.
7. **Let the user set the sample count, and ask before a sweep.** Run the smallest experiment that answers the question — usually one render. A multi-arm sweep is a separate, explicit request even at ~$0.09. When a sweep is warranted, skip outputs that already exist so an interrupted run resumes instead of re-billing, and run it as a tracked background job rather than a shell you sit and poll.
8. **Check the spec before concluding a render is wrong — and only in terms of parameters.** Quote the sentence that is violated. A flag that selects a prompt variant is worthless if the code path resolves to a build that ignores it, so diff the two compiled prompts (length plus the clauses that differ) before spending on an A/B: identical arms "prove" nothing.

## Procedure: edit (localized)

1. Load original image; let user click to add pins with comments.
2. Annotate image with red numbered markers at pin positions.
3. Build prompt listing each edit by number with (x,y) coordinates + global instruction.
4. Send annotated image + prompt to model.
5. Composite diff back onto original to preserve untouched regions (recommended).

## Localization strategies (deep research)

- Masks are the most reliable spatial constraint; Seedream/OpenRouter ignores hard masks in practice.
- Use annotated images + explicit spatial prompts as fallback.
- For true mask enforcement, use local inpainting (SDXL/FLUX.1 Fill) behind the same UI.
- SAM segmentation from click → mask → inpaint is the gold standard (Inpaint Anything pattern).
- Prompt engineering: explicit spatial descriptors, "only modify X, keep everything else".
- Two-stage refine: generate with generous mask, then composite diff back to original.
- Attention regularization (LIME) for diffusion editors without user masks.

## Cost discipline

- **Cost units differ by modality — read the unit before assuming a batch is cheap.** Images bill per render (~$0.01-0.14). Video bills per SECOND: `kwaivgi/kling-v3.0-std` is $0.084/s silent ($0.126/s with audio), so one default 8-second clip is ~$0.67 — a 3-scene set is ~$1.60, roughly 1,000x a text draft. Speech bills per token. Read the rate from the provider's own metadata rather than estimating: video models expose it under `pricing_skus` via `GET /api/v1/videos/models`, and the `usage.cost` block on a real response is authoritative. Quote the published rate, and label a figure derived from arithmetic as derived.
- **A paid stage gets a free preflight and a dry run.** Resolve config, model and inputs with a `--dry-run` that spends nothing; make the expensive stage dry-run by default and require an explicit go-ahead flag (`--yes`) to spend; print per-item and total cost before committing; and offer a single-item path (`--only <id>`) so iterating a prompt costs one item, not a batch.
- **The price tier buys resolution and plate capacity, not rule-following.** There is no valid adherence measurement to justify paying premium prices: the one attempt was scored by a model reading images, one of its checks was invented, and it was withdrawn. Facts that stand: one `openai/gpt-image-2.5-sunburst` render at `xhigh`, 3:4, with 3 plates cost **$0.1174** and returned 1152x1536 in 67s, against **$0.0184** for a 1K qwen render with the same plates. Pay premium for pixels or plate ceiling (16 refs), not for obedience. Method and measured costs: the `image-model-craft` skill.
- **Prefer the single decisive test, and ask before a sweep.** State the question, then run the smallest experiment that answers it — usually one render. A multi-arm sweep is a separate request even at ~$0.09, so never launch one to settle something a single render can settle. When a sweep is genuinely warranted, skip outputs that already exist so an interrupted run resumes instead of re-billing.
- Check the remaining budget BEFORE any batch or probe series: `curl -H "Authorization: Bearer $K" https://openrouter.ai/api/v1/key` returns `limit_remaining` / `usage_daily`, and `/api/v1/credits` returns account totals. **Read `effective_budget`, not the budget that looks largest:** a key carries both a lifetime limit and workspace _daily_ budgets, and only `effective_budget` binds. Reading the daily workspace figure ($9 left) while the lifetime key limit sat at $0.10 lets a sweep die halfway — which leaves the arms with unequal sample counts and voids the comparison. A key limit with `limit_reset: null` never resets; a top-up is the only way to continue.
- One full-brief render, then a model switch, is cheaper than any diagnosis loop. A probe that only re-confirms what you already concluded is pure spend.
- State the run's image count and cost when it ends, and label derived figures as derived. Auditing recipe: `references/cost-audit.md`.

## Pitfalls

- **A generated prompt is not innocent just because a template produced it.** Fix the template when its output violates the voice rule above — patching the emitted text by hand fixes one render and leaves the generator producing the same anti-pattern for every other frame. Two consequences of fixing it at the source: a consumer that quotes that text by **exact string** (per-frame overrides that delete or replace a sentence) breaks the moment the source prose is reflowed — match whitespace-tolerantly and re-run the fixture suite after every source edit, because a wrapped paragraph changes the whitespace, not the words, and the failure surfaces as a missing-sentence error rather than a wrong render. And confirm the source text is version-controlled before a bulk rewrite; if it is not, dump the current text to a dated file first, since hand-authored prose is not recoverable from anywhere else.
- A provider content filter rejects the RESPONSE, not your request, so the error reads `400 The response was filtered... metadata.provider_name`. Meta's filter rejects scenes whose aggregate density trips it even when every element passes alone: bisecting a long briefs into sub-blocks returns OK for all of them while the whole brief still 400s. **Do not bisect**: after ONE confirming probe, stop and switch model (`bytedance-seed/seedream-5-0-pro`, falling back to `-flash`). Each probe is a billed API call, and the answer — 'switch provider' — is already known. Never reach for Gemini as the fallback; it is the one model ruled out on cost.
- Filtered attempts take ~30s and cost money; a 'quick' bisect is 20-30 paid calls. Prefer one model switch over diagnosis.
- Do not expose API key in browser; proxy through a local server.
- Model ignores masks; use visual markers + spatial prompts.
- Composite back to original to guarantee preservation of untouched regions.
- Log every request for cost/speed tracking.
- Source `~/.localrc` for `OPENROUTER_API_KEY` if it is not set in `${HOMINEM_HOME:-~/.hominem}/.env` (the key often lives there).
- Pick a free port for the click-to-edit server (check with `lsof -nP -iTCP:<port>`); 8765 is commonly occupied by Switchyard.
- Image edits that change pose/outfit often drift identity; constrain with "keep face, hair, body identical" and composite the diff back onto the original.
- **Ask what holds a prop up before rewriting its description.** A prop whose shape is fixed by its own support — a net on ceiling pulleys, a rope pulled taut between two handlers — renders as a flat backdrop in the picture plane and will not deform to a figure, however explicitly the relation is worded. Slackening that support is not enough, because a supported object keeps its own shape: remove the support and make the figure the only thing holding it up (anchor the prop to the body, let its free ends trail on the ground, and negate every other support). Wide-mesh props over an opaque figure are the hard case for per-cord occlusion, so give them a silhouette that depends on the body — tenting, sagging, bunching — and say what shows through the gaps. Full recipe: `references/prompt-geometry.md`.
- **When a feature renders wrong on every model, suspect a conflict between the prompt text and the reference image before blaming the models.** A model given a name in prose that contradicts the plate it can see (text says "hockey mask", the plate shows a smooth oval shield) resolves the conflict arbitrarily and produces something matching neither — and because the failure is a compromise, it looks model-specific even when it is not. Two independent models making the same 'mistake' on the same clause is the signal: check the plate against the prompt text as a **fact** (does it show the mask the text names?) and show the finding to the user before changing anything. Inspecting a reference asset is not the same as judging a render — the verdict on the output is always theirs. The plate is what the model actually conditions on, so text that contradicts it loses; fix the text when the plate is authoritative, and fix the plate when the text is.
- **Change the field that drives the geometry, not the trailer.** A clarifying paragraph appended to a long compiled prompt does not override earlier dominant clauses: the same failure returned with the physics spelled out verbatim, because the geometry was set by the staging and prop blocks near the top. Alter one variable per render and keep every variant — a change that produces no visible difference is evidence the cause lies elsewhere, so stop refining that lever instead of restating it harder. Camera-relative phrasing ("near edge at his waist, far edge at his knees") is unrenderable when the camera looks along that axis and collapses to a band across the torso; describe geometry relative to the body.
