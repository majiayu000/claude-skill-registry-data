---
name: optimize
description: Score an existing Lexsis page against the same page-type, design, proof, offer, asset and copy rules used to build pages, propose improvements as a strict optimization plan with real replacement copy and asset decisions, wait for approval, then apply the approved changes with version protection and hosted QA.
---

# Optimize a Page

`/plan-page` and `/design-page` for a page that already exists. Read the live
page, score it against the rules a new page is built to, write the same plan
blocks a new page gets (final copy, an asset decision per section, a claim
gate, a work queue), wait for approval, then apply the approved changes to the
persisted source and review the hosted draft. Never publish.

## References

| Reference | Read when |
|---|---|
| `references/plan-page.md` | always; the shared block vocabulary (Asset slots decisions, Claim gate, Work queue owners, status labels) this skill reuses |
| `references/evidence-led-cro.md`, `references/consumer-behavior-cro.md` | ordering evidence and forming one behavioural hypothesis |
| `references/offers/offer-strategy.md`, `references/offers/offer-stacking.md` | diagnosing positioning, offer value, composition, or pricing |
| `/audit` report | when one exists for this page version, start from its findings instead of rescoring |
| the matching section of `references/industry-cro.md` | when the vertical is known |
| `references/page-types/_index.md`, then the type file | scoring the page against its type contract (Above the fold, Proof, Offer and CTA, Imagery, Copy, Never, Checklist) |
| `references/design-rules.md` | scoring N1 to N14 and A1 to A12 |
| `references/proof/proof-ledger.md`, `references/offers/offer-ledger.md` | reconstructing the ledgers from what the page shows |
| `references/workflows/section-asset-workflow.md` section 2 | the fit review of every image on the page |
| `references/copy/headline-and-cta-rules.md`, `references/anti-patterns/copy-anti-patterns.md` | scoring copy |
| `references/anti-patterns/mobile-anti-patterns.md`, `references/anti-patterns/cro-anti-patterns.md` | scoring mobile and CRO tells |
| `references/assets/generation-policy.md` | before proposing any generated or composited asset |
| `references/page-editing.md`, `references/qa-recipe.md`, `references/source-artifact-workflow.md` | applying approved changes and reviewing the hosted draft |
| `references/authoring/css-and-styling.md`, `references/animation-system.md` | before any CSS, class or motion change |
| `references/lexsis-design-capabilities.md` | optional deeper design guidance |

Use `lexsis_pages.edit_context`, `lexsis_pages.get`, `lexsis_pages.inspect`,
`lexsis_pages.source`, `lexsis_pages.section_source`, `lexsis_pages.compile`,
`lexsis_pages.integrity`, `lexsis_pages.diff`, `lexsis_pages.qa`,
`lexsis_analytics.page`, `lexsis_analytics.timeseries`,
`lexsis_analytics.attribution`, `lexsis_catalog.get`, `lexsis_catalog.reviews`,
`lexsis_assets.view`, `lexsis_asset_library.search`,
`lexsis_asset_select.select`,
`lexsis_asset_import.import`, `lexsis_asset_upload.upload`,
`lexsis_workspace.credits`, `lexsis_drafts.asset_generate`,
`lexsis_template_library.search_page_kits`,
`lexsis_template_library.search_sections`,
`lexsis_build.push_token` with `npx @lexsis/cli pull`/`diff`/`push` (CLI
mode, the default) or `lexsis_build.get`, `lexsis_build.patch`,
`lexsis_build.commit`, `lexsis_build.diff` (inline mode, no shell), and `lexsis_drafts.page_record_qa`. Resolve only unfamiliar schemas through exact
router/action discovery. A zero-result directory lookup does not make page or
analytics data unavailable. If the actual live read fails, state that
limitation; generic CRO guidance is not a substitute for live evidence.

## Confirm the Objective

Start by confirming:

1. Target outcome: conversion, add-to-cart, AOV, bounce, trust, mobile UX,
   speed, or SEO.
2. Target page, audience, and traffic source.
3. Diagnosis only, or permission to edit after approval.
4. Copy, sections, SEO fields, or offers that must remain unchanged.

Do not edit until the objective and scope are clear. Confirm the page's
workspace, store and theme binding from saved setup or current MCP context;
if it is missing, stop with `Run /setup for this store and theme first.` Never
run setup automatically.

## Read the Live Page

1. `lexsis_pages.edit_context`, then `lexsis_pages.get`, `lexsis_pages.inspect`
   and `lexsis_pages.source`: current version, section order, islands, copy,
   media, head.
2. `lexsis_analytics.page`, `.timeseries`, `.attribution` for the outcome
   window: conversion, bounce, device split, drop-off by section, traffic
   source. Analytics and observed behaviour outrank generic patterns.
3. The host browser at 390, 768 and 1280: screenshots, first screen, sticky
   elements, hydration, console.
4. `lexsis_assets.view` on every image the page shows: identity, job, crop,
   baked-in text or watermark, set consistency. A filename is never evidence.
5. `lexsis_catalog.get` and `lexsis_catalog.reviews` for the products and
   proof the page claims.
6. Identify the page type from the live structure and the brief with
   `references/page-types/_index.md`; load only that type file.

## Score

Write the scorecard first. Every row cites the rule source and the finding.

```markdown
## Scorecard

| Area | Rule source | Result | Blocking findings | Notes |
|---|---|---|---|---|
| Page type contract | <type>.md checklist, Above the fold | 7/10 | price below 1.5 screens at 390 (A8) | |
| House rules | design-rules N1-N14, A1-A12 | 11/14 | N2 band in benefits, N1 emoji in trust strip | |
| Proof | proof-ledger per-kind table | 2 verified / 3 unledgered | "50,000 customers" has no source | |
| Offer | offer-ledger rules 1-6 | ... | compare-at without basis (O2) | |
| Assets | section-asset-workflow section 2 | 5 pass / 2 fail | hero carries a baked-in ad headline -> reference-only | |
| Copy | copy-frameworks CF5, headline HC rules, copy blacklist | ... | h1 14 words; "seamless" x3 | |
| Mobile | mobile-anti-patterns | ... | sticky bars 22% of viewport | |
| CRO anti-patterns | cro-anti-patterns | ... | | |
| Analytics | evidence-led-cro | CVR, bounce, device split, drop-off section | | |
```

Proof and offer findings block; type deviations and copy findings are review
notes unless the page's own plan recorded them. Use
`references/consumer-behavior-cro.md` to name the visitor mode, the top
unanswered decision question, and the smallest behavioural hypothesis.

### Offer Value Findings

When positioning, offer value, composition, or pricing is in scope, use
`references/offers/offer-strategy.md`. Distinguish a weak value argument from
missing evidence, confusing terms, or purchase friction; each needs a different
response. Record the relevant rationale and, when substantively replanning the
offer, complete the seven value-strategy fields in Page strategy.

Preserve fixed offers and campaign promises. Keep unconfirmed commercial
alternatives separate from final replacement copy. Unknown margins limit
profitability conclusions, not valid existing offers. Check traffic mix, stock,
seasonality, and tracking before diagnosing offer fatigue.

Do not require a strategy rewrite for unrelated copy, layout, speed, or metadata
fixes. Previously approved plans remain usable; carry their argument forward
unless the approved scope changes it.

## Findings by Section

One entry per section, in page order, with the same copy fields
`/plan-page` uses so the replacement text is final, not a brief.

```markdown
## Findings by section

### S3. benefits - keep | improve | replace | remove | test

**Finding.** three icon tiles on a tinted band; no image of the product in use
**Evidence.** screenshot 390 and 1280; N2, N3; drop-off 38% at this section (analytics)
**Rule.** design-rules N2, N3; <type>.md Imagery
**Proposed change.** rebuild around one in-use image per benefit
**Copy.** (only when copy changes)
- Eyebrow: <text or none>
- Headline: <text, at most 10 words, sentence case>
- Subhead: <text, at most 20 words, or none>
- Body: <paragraph(s), at most 45 words each>
- Labels / bullets: <exact strings, or none>
- CTA: "<verb + object>" -> <destination>
**Claims in this section.** <C# ids> or none
**Layout.** 1280: ... | 390: ...
**Interaction.** none | <behaviour and decision inputs>; no island names or props
**Asset.** <slot id: decision state> | none-required: <why>
```

Protect the primary-product decision and any element the user listed as
unchanged. Do not force template comparison for copy-only, offer-only,
metadata or minor visual changes; for a structural redesign, compare the
current structure with relevant page kits and sections
(`lexsis_template_library.search_page_kits`, `search_sections`).

## Asset Plan

Write the `## Asset slots` table exactly as `/plan-page` defines it
(`references/plan-page.md`): one row per media slot on the proposed page with
a decision from `reuse-selected`, `shopify-product-media`,
`user-selection-required`, `user-upload-required`, `generate-required`,
`composite-required`; `none-required` on a section's `Asset` line; a current
image that fails the fit review or carries baked-in copy is `reference-only`
with its replacement slot named.

```markdown
## Asset slots

| Slot | Section | Role/purpose | Aspect | Decision | Source decision | Id / URL | Status |
```

An existing image that passes the fit review is `reuse-selected` with its
current id. Add `## User selection` when a role has more than one fit
candidate and `## Generation briefs` for every generate-required or
composite-required slot, in the shapes `/plan-page` defines. Generation obeys
`references/assets/generation-policy.md`; this skill spends no credits before
approval.

## Claim Gate

Write the `## Claim gate` table exactly as `/plan-page` defines it: one row per
claim currently on the page and per proposed claim, gated
`approved evidence available`, `merchant evidence required` or
`remove from V1`, with the ledger row or the V1 copy that ships without it.

```markdown
## Claim gate

| # | Claim (verbatim) | Where | Gate | Evidence | V1 copy if not approved |
```

A claim on the live page with no evidence is a blocking finding: it is
gated `remove from V1` or `merchant evidence required`, never left as is.

## Work Queue

Write the `## Work queue` table with the owners `/plan-page` defines (`user`,
`agent`, `merchant`, `blocked-by-evidence`). Tasks include every approved
change, every pending asset, every open claim, the apply step, the hosted
review, and any `/ab-test` hand-off.

```markdown
## Work queue

| # | Task | Owner | Section / slot | Unblocks | Status |
```

## Approval

Present the Scorecard, Findings by section, Asset slots, Claim gate, Work
queue, the protected elements, and the measurement:

```text
Outcome:
Evidence:
Main friction:
Visitor mode:
Behavioral hypothesis:
Scorecard: <blocking findings n / notes m>
Changes: <keep k / improve i / replace r / remove d / test t>
Asset slots: <n verified / m planned> ; decisions: <counts per state>
Claim gate: <n approved / m merchant evidence required / k removed>
Work queue: <n open: u user / a agent / m merchant / b blocked>
Protected elements:
Expected measurement:
Experiment recommended: yes/no
Status: OPTIMIZATION_PLAN_READY | BLOCKED - evidence required
```

Return `OPTIMIZATION_PLAN_READY`, or `BLOCKED - evidence required` when any
open task is `blocked-by-evidence`. Wait for explicit approval; record
`PLAN_APPROVED <who> <date>` when granted. Nothing is edited before that.

## Apply Approved Changes

Run `/design-page`'s Existing Page Edits and Hosted Design Review procedures:

1. Pick the write mode with the probe in `lexsis-mcp-contract.md` (Write
   Path). CLI mode: `push_token` with `page_id`, then `npx @lexsis/cli pull`.
   Inline: `lexsis_build.get` for the version and file tree, reading only the
   files the approved changes touch. Stop on unexpected version drift.
2. Resolve the approved asset decisions first: `lexsis_asset_library.search`
   and `lexsis_assets.view` for reuse, `lexsis_asset_select.select` when the
   user must choose among reviewed candidates, `lexsis_asset_upload.upload` or
   `lexsis_asset_import.import` for supplied files, `lexsis_workspace.credits`
   then `lexsis_drafts.asset_generate` per brief after the user confirms the
   batch. View every asset before it enters the source.
3. Place the approved copy verbatim. CLI mode: edit the files in the pulled
   folder, then `push --dry-run` and `push`. Inline: copy, price and
   single-rule CSS changes go through `lexsis_build.patch`; new or rebuilt
   sections through `lexsis_build.commit` with only those files and
   `base_version` (the build router's `expected_version` guard), `dry_run: true` first for large changes. Fix every returned
   diagnostic in one pass.
4. Check the diff (`npx @lexsis/cli diff` or `lexsis_build.diff`) and run
   `lexsis_pages.integrity`; update recorded version
   only after success.
5. Hosted review at 390, 768 and 1280 with the commerce checks in
   `references/qa-recipe.md`; save evidence with `lexsis_drafts.page_record_qa`.
   Fix in place with another versioned patch; never a replacement page.

Preserve the URL and SEO fields unless the user approved changing them. Never
edit compiled output in place of source. Return `DESIGN_APPROVED` for the new
version once the hosted review passes and the user approves it; `/publish`
gates on that version.

## Experiment Handoff

When the value of a change is uncertain and traffic supports measurement,
return a focused hypothesis for `/ab-test` instead of presenting the change
as proven.

## Return

Return the approved objective, the scorecard totals, changed sections, page
version, verification results, MCP evidence, whether an experiment is
recommended, and the state: `OPTIMIZATION_PLAN_READY` or `DESIGN_APPROVED`.
