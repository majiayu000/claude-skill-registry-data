---
name: design-award-search
description: "Find and verify award-winning designs in the same or adjacent functional category through eight explicit relevance dimensions: problem and user, core function, sensing technology, intervention mechanism, physical form, use context and workflow, system architecture, and visual language. Use when a user asks for same-category winners, comparable precedents, design benchmarks, appearance-related award winners, or examples from iF Design, Red Dot, IDEA, or iF Design Student Award. Do not use this skill to score, judge, optimize, or match the user's design to an award."
---

# Design Award Search

## Purpose

Retrieve a small, high-precision set of verified award-winning designs. Keep the functional design category as a mandatory boundary, then search separately across eight relevance dimensions. Search public official sources at request time. Do not connect to, package, or depend on a private award database.

## Scope Boundary

- Identify the user's canonical design category.
- Search selected relevance dimensions independently.
- Verify award identity, year, category, relation evidence, and official URL.
- Explain exactly which dimension makes each result relevant.
- Stop after retrieval. Do not score the design, predict winning probability, recommend changes, or select an award to enter.

## User Interaction Contract

Accept a project description, image set, PDF, project page, or brief. Accept optional dimensions, award sources, years, and result count.

Require enough information to identify the object or service and its primary function. If the primary function remains ambiguous, ask exactly one short question: `What is the design's primary function and who uses it?` Otherwise state reasonable assumptions and continue.

When the user does not select dimensions, use balanced mode across every dimension supported by the supplied evidence. Use user images to infer physical-form and visual-language terms. If no image is supplied, do not activate visual-language relevance unless the user supplies explicit visual descriptors.

Offer this template when the user asks how to use the skill:

```text
Project: {name or object}
Primary function: {problem solved or job performed}
Target user: {optional}
Use context: {optional}
Relevance dimensions: {all or selected dimensions}
Preferences: {optional award sources, years, and result count}
```

## Retrieval Workflow

### 1. Build the profile

Read [../design-judge-shared/category-taxonomy.md](../design-judge-shared/category-taxonomy.md) and [references/relevance-dimensions.md](references/relevance-dimensions.md). Extract:

- canonical and adjacent categories;
- designed object or service;
- problem and target user;
- primary function;
- sensing technology;
- intervention mechanism;
- physical form and wear mode;
- use context and workflow;
- system components and information flow;
- visible form and CMF descriptors;
- source, year, dimension, and result-count constraints.

Classify by primary function before appearance. Keep physical form and visual language separate.

### 2. Select dimensions

Use these eight dimension keys:

1. `problem-user`
2. `core-function`
3. `sensing-technology`
4. `intervention-mechanism`
5. `physical-form`
6. `use-context`
7. `system-architecture`
8. `visual-language`

Search only user-selected dimensions. Otherwise activate every dimension supported by the input and use balanced mode.

### 3. Generate official-source queries

Read [../design-judge-shared/source-registry.md](../design-judge-shared/source-registry.md). Use `scripts/build_search_queries.py` when a shell is available. Translate profile terms into concise English first.

Example:

```powershell
python scripts/build_search_queries.py `
  --category "Medical and Health" `
  --function "detect stress and prevent relapse" `
  --object "wearable health monitor" `
  --problem "alcohol use disorder relapse" `
  --user "people in addiction recovery" `
  --sensing "ECG HRV stress detection" `
  --intervention "haptic paced breathing biofeedback" `
  --form "adhesive chest patch" `
  --context "daily out-of-clinic high-risk moments" `
  --system "wearable sensor app personalized feedback" `
  --visual "discreet soft white blue medical wearable"
```

Execute dimension queries progressively. Stop searching a dimension after its target quota has enough verified candidates. Use official gallery search when available; otherwise use site-restricted discovery queries.

For visual-language retrieval, first build a visual-review pool of up to five same-category candidates found through every active dimension. Use visual-specific queries only when that pool is too small. Keep visual queries short: combine the designed object, physical form, and two or three unquoted visual descriptors. A domain-restricted image search may discover candidates, but only official project-page images can verify them. Do not use visual similarity outside the canonical or declared adjacent category.

### 4. Verify candidates

Open every official project page. Use `scripts/verify_official_urls.py` to reject unsupported domains and paths.

Verify:

- winner or officially recognized status;
- award organization and year;
- project identity and stable URL;
- same or declared adjacent canonical category;
- explicit evidence for the assigned primary relation.

Treat search snippets as discovery evidence only. For visual-language matches, inspect accessible official images directly; never infer visual similarity from text alone.

Before opening a full browser page, probe the visual-review pool with `scripts/verify_visual_evidence.py`. The script validates the project URL, extracts hero, thumbnail, lazy-load, and `srcset` image URLs from the official page, restricts assets to allowlisted official hosts, and fetches each image with the project page as `Referer`. It never prints image payloads. Its default mode keeps pixels in memory; use `--review-dir` only when the available visual tool requires a local path.

Example:

```powershell
python scripts/verify_visual_evidence.py `
  --request-timeout 5 `
  --candidate-timeout 12 `
  --total-timeout 60 `
  --max-images 3 `
  --progress text `
  "https://www.red-dot.org/project/example-123" `
  "https://ifdesign.com/en/winner-ranking/project/example/456"
```

Treat `Official image accessible` as an acquisition result only. It remains `Pending visual inspection` until a visual-capable tool directly inspects the official pixels. Never turn accessibility, metadata, alt text, or official prose into `Verified` visual evidence.

When the visual tool accepts only local paths, create a new session-scoped handoff directory:

```powershell
python scripts/verify_visual_evidence.py `
  --review-dir "{new non-existent temporary directory}" `
  --request-timeout 5 `
  --candidate-timeout 12 `
  --total-timeout 60 `
  --max-images 3 `
  "https://www.red-dot.org/project/example-123"
```

Call the local-image inspection tool on every returned `visual_handoff.review_path` needed for comparison. Inspect the user image pixels and official image pixels in the same task. Then clean the returned handoff directory, including after an inspection error:

```powershell
python scripts/cleanup_visual_review.py "{review_handoff.directory}"
```

Do not create the handoff inside a repository-tracked directory. Do not reuse it in another task. If cleanup is refused, report the exact reason and resolve it before creating another handoff.

Verify visual candidates in this order:

1. Run the probe and use its returned official image URL with a visual-capable tool that can inspect remote images directly.
2. If the visual tool accepts only local paths, rerun with `--review-dir`, inspect the returned `visual_handoff.review_path`, and clean the directory in the same task.
3. If neither asset path works, open the official project page after `DOMContentLoaded` and inspect its visible hero or gallery image; do not wait for `networkidle`.
4. Try at most one official page-hosted thumbnail and one official image link.
5. If image acquisition fails, record `Candidate - image inaccessible` with the probe reason code. If acquisition succeeds but no visual tool observes the pixels, keep `Pending visual inspection - visual_tool_unavailable`; never call it image inaccessible.

Emit progress when each visual candidate starts, when an asset attempt begins, and when the candidate completes. Use a five-second request timeout, a twelve-second candidate budget, and a sixty-second visual-stage budget unless the user asks otherwise. Do not let one inaccessible image block the remaining candidates or the other seven dimensions.

Compare only observable silhouette, proportion, color and material, surface treatment, and medical or low-stigma expression. Record at least two paired attributes that state what is visible in the user image and what is visible in the official image. A generic statement such as `both look minimal` does not qualify. Follow the states and comparison record in [references/retrieval-policy.md](references/retrieval-policy.md).

### 5. Rank, label, and deduplicate

Read [references/retrieval-policy.md](references/retrieval-policy.md). Assign exactly one primary relation, no more than two secondary relations, and `High`, `Medium`, or `Broad` within the primary dimension.

Keep each project once even when it matches several dimensions. Prefer dimension coverage before source or year diversity, without weakening evidence quality.

### 6. Present results

Lead with the inferred category, active dimensions, and one-sentence search scope. Group results by primary relation. Use this table within each group:

| Award-winning project | Award / year | Official category | Secondary relations | Relation evidence | Match | Official source |
|---|---|---|---|---|---|---|

Link directly to official project pages. Keep relation evidence to one sentence.

After all result groups, include only:

- `Search coverage`: sources, dimensions, filters, and verified counts per dimension.
- `Limitations`: unavailable evidence, empty dimensions, broadened categories, or visual comparisons that could not be verified.

## Fallback Rules

- If fewer than three same-category results are verified overall, broaden exactly one taxonomy level and label every added result `Broad`.
- If a selected dimension yields no verified result, report it; do not fill it with a result from another dimension.
- If visual candidates are found but their official images remain inaccessible, list up to three under `Limitations` as unverified candidates; do not count them toward the result total or visual-language coverage.
- If live web access is unavailable, return the generated official-site queries. Do not fabricate projects.
- If an official page is unavailable, omit the candidate unless another official page from the same award organization verifies it.
- If sources conflict, use the official award project page as controlling evidence and state the conflict briefly.

## Compliance Guardrails

- Access only public pages that require no login.
- Never bypass access controls, CAPTCHAs, rate limits, robots restrictions, or technical protections.
- Do not crawl entire sites or build a persistent corpus.
- Do not persist or redistribute official text, raw payloads, images, thumbnails, or content-derived embeddings. A marked session-scoped file is permitted only as a short-lived bridge to a local-path visual tool and must be removed in the same task with `scripts/cleanup_visual_review.py`.
- Return minimal factual metadata and official links.
- Respect source terms and stop automated access when disallowed.
- Prefer official APIs or licensed feeds when suitable.

## Example Invocations

- `Use $design-award-search to find ten verified winners, balanced across all eight relevance dimensions, for this project PDF.`
- `使用 $design-award-search，分别从感知技术、干预机制、产品形态和视觉语言四个方面查找同类别获奖作品。`
- `Use $design-award-search to find six same-category winners related specifically to the physical form and visual language of this project image.`
