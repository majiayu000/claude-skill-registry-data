---
name: icaire-audience-data-collection
description: Collect immutable, timestamped ICAIRE LinkedIn and X post-level snapshots when refreshing Audience Growth Engine source data.
---

# ICAIRE Audience Data Collection

Collect reproducible post-level LinkedIn and X snapshots for ICAIRE without destroying historical observations.

## Contract Checklist

- Read the applicable project instructions before accessing `/Users/hq/projects/ICAIRE`.
- Treat public and authenticated platform state as live and verify the ICAIRE account before capture.
- Store original platform output under `/Users/hq/projects/ICAIRE/Audience Growth Engine/raw-data/` in a new timestamped run directory.
- Never overwrite, edit, deduplicate away, or silently replace a prior raw capture.
- Record posts, metric snapshots, assets, and coding fields using the normalized model in [references/post-level-schema.md](references/post-level-schema.md).
- Keep unavailable fields null and record why they are unavailable. Never infer metrics, post attributes, or missing timestamps.
- Update the existing analysis workbook only after the immutable raw capture is safely written and validated.
- Report coverage and incompleteness separately for LinkedIn and X.
- Do not publish, message, react, follow, or change any social account state.

## Workflow

1. Establish the collection run:
   - Read applicable `AGENTS.md` and `AGENTS.override.md` files.
   - Locate the Audience Growth Engine workbook and existing raw-data directories without changing them.
   - Create a UTC run identifier in `YYYY-MM-DDTHH-mm-ssZ` form and a new directory at `raw-data/runs/<run-id>/`.
   - Record the requested date range, target accounts, platform authentication state, and extraction method in a run manifest.
   - Stop if the target account cannot be verified or the new run path already exists.
   - Anti-patterns: reusing a run directory, collecting from an unverified account, treating a signed-out partial timeline as complete
2. Capture LinkedIn source data:
   - Collect each in-scope ICAIRE post, stable post identifier or URL, publication time, full visible text, format and media evidence, and all visible engagement metrics.
   - Preserve original export or rendered-source evidence before normalizing it.
   - Record inaccessible or undefined metrics as null with a limitation note.
   - Anti-patterns: estimating counts from abbreviations without recording the displayed value, dropping low-performing posts, omitting media evidence
3. Capture X source data:
   - Collect the same post-level dimensions for the verified ICAIRE X account.
   - Prefer authenticated account data when cross-platform comparison is requested.
   - If authentication is unavailable, label the result partial and do not claim full timeline coverage.
   - Preserve original export or rendered-source evidence before normalization.
   - Anti-patterns: treating pinned posts as newly published, claiming a public signed-out feed is exhaustive, combining repost and original metrics
4. Normalize without erasing history:
   - Map both platforms to [references/post-level-schema.md](references/post-level-schema.md).
   - Keep stable identity and content in `Posts`; append every observed metric state to `Metric Snapshots`; preserve media provenance in `Assets`; keep derived classifications in `Coding`.
   - Use `platform:post_id` as `post_key` and `post_key:extraction_timestamp` as `snapshot_key`. Repeated post keys across runs are expected because metrics change over time.
   - Keep numeric metric values separate from visibility or availability status so a hidden counter is never converted to zero.
   - Store normalized data inside the run directory before updating any workbook.
   - Anti-patterns: upserting on post ID alone, replacing old engagement counts, converting unknown values to zero
5. Validate and update the workbook:
   - Confirm raw source files, normalized rows, manifest, row counts, and hashes are internally consistent.
   - Append or import the new observations into the existing Audience Growth Engine workbook using its established schema.
   - Preserve prior workbook rows and formulas across `Posts`, `Metric Snapshots`, `Assets`, `Coding`, and downstream `Hypotheses / Recommendations`. Create a backup before any structural workbook change.
   - Re-open the workbook and verify row counts, identifiers, timestamps, formulas, and filters.
   - Anti-patterns: updating the workbook before raw validation, deleting duplicates across collection times, breaking formulas or existing tabs
6. Close the run:
   - Report per-platform posts captured, date coverage, metric coverage, authentication state, missing fields, and exact artifact paths.
   - Distinguish complete, partial, blocked, and not attempted states.
   - Do not begin performance interpretation in this skill.
   - Anti-patterns: hiding partial coverage, calling capture complete without artifact read-back, mixing analysis conclusions into collection

## Anti-Patterns

- Overwriting historical snapshots or raw platform evidence.
- Inferring unavailable data, converting null to zero, or silently changing metric definitions.
- Comparing LinkedIn and X when one platform has materially incomplete coverage.
- Scraping or collecting personal data beyond the ICAIRE public account and its post-level performance.
- Taking any external publishing, messaging, engagement, or account-management action.

## Output

Return the run identifier, exact raw and normalized artifact paths, workbook path, per-platform row and date coverage, validation results, missing-data inventory, and any blocker. State explicitly that no social account state was changed.
