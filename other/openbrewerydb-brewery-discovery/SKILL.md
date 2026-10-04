---
name: openbrewerydb-brewery-discovery
description: Discover missing Open Brewery DB breweries and coverage gaps by comparing a regional, guild, regulator, or other licensed inventory with all source CSVs and open issues/pull requests. Use for regional list comparisons, missing breweries, additional locations, rebrands, and relocations. Do not use for one known mutation or an open-ended stale-status audit.
---

# OpenBreweryDB Brewery Discovery

Perform a read-only coverage audit of `openbrewerydb/openbrewerydb` and produce an issue-ready research report. The default outcome is a report, not dataset changes.

## Scope

Use this skill when the request concerns:

- Coverage for a city, state/province, country, or other region.
- Comparison with a guild, regulator, government, tourism, or licensed third-party list.
- Discovery of breweries or brewery locations potentially missing from Open Brewery DB.
- Batch investigation of renames/rebrands, relocations, or stale details found during an inventory comparison. Use `openbrewerydb-data-quality-auditor` for open-ended status audits.

Do **not** use it for one already-known add, delete, or update. That is a mutation task for `openbrewerydb-contributor`.

## Hard read-only boundary

- Never edit any dataset CSV or generated artifact.
- Never create a dataset branch, commit, push, pull request, or upstream implementation.
- Never run `npm install`, an npm script, another package manager's equivalent, or an npm script implementation directly in the upstream repository.
- Do not reproduce maintainer scripts or generate IDs, combined data, JSON, SQL, statistics, or contributor files.
- Read local files and public sources only. `gh` read operations for open issues/PRs are allowed; commands that create, edit, close, comment on, or otherwise mutate GitHub content are not.
- Keep temporary inventories and reports outside the dataset root. The helper emits JSON to stdout and never writes in the dataset root.

## Inputs

Obtain:

1. The dataset root. Ask once if it cannot be located.
2. The target region and intended coverage boundary.
3. One or more external inventories, including source URL, publisher, retrieval date, and licensing/reuse terms.
4. A normalized external CSV. At minimum it needs `name`; recommended columns are `website_url`, `address_1`, `address_2`, `address_3`, `city`, `state_province`, `postal_code`, and `country`. `source_url` and `source_id` are retained as evidence.

If a source cannot legally be reused, do not copy or bulk-extract it. It may be used only as a lead where permitted; independently verify every reported fact and avoid reproducing protected list content. See [source selection](references/source-selection.md).

## Workflow

### 1. Define the audit

State the geographic boundary, eligible establishment types, source snapshot dates, and known limitations. Read the live dataset's `README.md` and `CONTRIBUTING.md` for current schema and policy, but do not execute their mutation or npm instructions.

Apply [eligibility](references/eligibility.md). Do not assume that every license holder or guild member is an eligible public brewery location.

### 2. Select and normalize sources

Choose sources by authority, recency, geographic fit, and licensing. Record those factors for every source. Prefer primary official evidence for candidate details and recent evidence for volatile facts such as status or address.

Create the normalized inventory outside the dataset root. Preserve provenance in `source_url` and `source_id` where available. Never invent missing values.

### 3. Compare every source CSV in both directions

Run the helper from this skill directory or by absolute path:

```bash
python3 scripts/compare_inventory.py /path/outside/dataset/inventory.csv /path/to/openbrewerydb
```

The default reverse scope uses a single city when the inventory contains one city, otherwise exact country/state-province pairs. Override it with `--reverse-scope city|region|country|all` only when the stated audit boundary requires it.

It recursively reads every `data/**/*.csv`, normalizes names, websites, and addresses, and emits JSON to stdout. Redirect output only to a path outside the dataset root if a file is needed:

```bash
python3 scripts/compare_inventory.py /tmp/inventory.csv /path/to/openbrewerydb > /tmp/comparison.json
```

Review both `external_candidates` and `reverse_unmatched_dataset_records`. Reverse results reveal records present in Open Brewery DB but absent from the external inventory; they are leads for status verification, source-scope differences, or exclusions, never automatic deletions.

### 4. Check work already in progress

Search **all open issues and open pull requests** in `openbrewerydb/openbrewerydb` for each candidate's name, alternate name, city, website host, and street address. Use read-only commands such as:

```bash
gh issue list --repo openbrewerydb/openbrewerydb --state open --search "<name or address>" --limit 1000
gh pr list --repo openbrewerydb/openbrewerydb --state open --search "<name or address>" --limit 1000
```

Do not rely on one broad search. Search likely variants and inspect relevant issue/PR contents and diffs. Put candidates already covered by an open issue/PR in `Addressed`, with links; do not duplicate them in actionable sections.

### 5. Research and classify

Treat helper scores as triage, not decisions. Verify each candidate against official and recent evidence, resolve chains and sibling locations by full address, and follow [candidate classification](references/candidate-classification.md).

Classify findings into:

- Missing breweries
- Additional locations
- Renames/rebrands
- Relocations/updates
- Status verification
- Exclusions
- Addressed
- Approved

`Approved` must remain empty unless a human explicitly approves candidates. Agent confidence, source authority, or an existing issue/PR is not approval.

### 6. Produce the issue-ready report

Use [the issue report template](references/issue-report-template.md). Include the audit boundary, methodology, source authority/recency/licensing, comparison counts, evidence URLs, candidate rationale, possible dataset matches, confidence, and open issue/PR checks.

Report findings in the conversation or a user-requested path outside the dataset root. Do not create or mutate a GitHub issue; return Markdown ready for the user or maintainer to post.

## Quality bar

- Compare against all source CSVs, not a generated root-level export or only the expected region file.
- Compare in both directions and explain external-list scope before interpreting reverse misses.
- Require multiple attributes for identity; normalized name alone is insufficient for common names or chains.
- Distinguish a genuinely missing business from an additional location, rename, relocation, closure, duplicate, and ineligible establishment.
- Cite actual URLs and access/publication dates. Mark unresolved conflicts rather than guessing.
- Keep false positives and uncertain cases visible under `Status verification` or `Exclusions` with reasons.
