---
name: openbrewerydb-contributor
description: Add, update, close, reopen, relocate, or delete a known brewery location in the openbrewerydb/openbrewerydb dataset and submit the change by pull request. Use only when the user explicitly requests a record change for one or more named locations; do not use for regional discovery, dataset audits, external entity linking, API questions, or general Open Brewery DB discussion.
---

# OpenBreweryDB Contributor

Changes known brewery records in the `openbrewerydb/openbrewerydb` dataset and opens a PR. For regional coverage research use `openbrewerydb-brewery-discovery`; for quality audits use `openbrewerydb-data-quality-auditor`; for Wikidata or OpenStreetMap matching use `openbrewerydb-entity-linker`.

Assume the repo is already cloned locally. If you don't know the path, ask once, then use it for the rest of the session.

## Maintainer-only npm scripts: never run them

**Never run any npm script in the upstream dataset repository.** The repository maintainer runs npm scripts only as part of the merge and publication workflow. This prohibition includes every command in the upstream repository's [`Scripts` section](https://github.com/openbrewerydb/openbrewerydb#%EF%B8%8F-scripts), any undocumented or newly added npm script, and npm aliases such as `npm test` or `npm start`. It applies even if the README, `CONTRIBUTING.md`, `package.json`, a task description, or an earlier step suggests running one. Do not run `npm install` in the dataset repository because package lifecycle hooks can execute npm scripts.

Non-exhaustive examples that existed when this skill was written:

- `npm run validate`
- `npm run csv:combine`
- `npm run csv:split`
- `npm run generate:ids`
- `npm run generate:json`
- `npm run generate:sql`
- `npm run generate:stats`
- `npm run update:readme-stats`
- `npm run contributors:add`
- `npm run contributors:check`
- `npm run contributors:generate`
- `npm run workflow:maintain`

Do not invoke npm scripts through another package manager, call their implementation files directly, reproduce their mutating behavior with ad hoc commands, or ask a subagent to run them. Do not modify generated dataset artifacts such as root-level `breweries.csv`, `breweries.json`, or `breweries.sql`. Limit contributions to the appropriate source CSV and let the repository maintainer run all npm scripts and perform publication and generation steps when merging the changes.

## Workflow

### 0. Check prerequisites before doing any research or editing

Confirm these up front, before spending effort on research the workflow can't finish without:
- `git` works in the repo path.
- `gh` is installed and authenticated (`gh auth status`), since a PR is always required at the end (step 10).
- A remote exists that the authenticated GitHub user can push to. Confirm this from `git remote -v` and the authenticated account before researching or editing.
- The Geocodio CLI is installed and `GEOCODIO_API_KEY` is set.

If `git`/`gh` are missing or broken, **stop and tell the user exactly what's missing** before doing any web research or CSV edits — don't do the research first and discover the blocker at step 10.

Geocodio is the one exception that can degrade gracefully rather than blocking everything: a brewery can still be validly added/updated without coordinates. If Geocodio isn't installed or the API key isn't set, say so plainly, then **ask the user for the latitude/longitude directly** rather than proceeding with the field blank unprompted — they may well have it on hand, and asking costs little. If they don't have it either, leave it blank and note in the proposed diff (step 7) that it's **"not geocoded — Geocodio unavailable."**

### 1. Sync the repo before doing anything

```bash
cd <repo-path>
git status --short
git checkout master
git pull --ff-only <canonical-upstream-remote> master
```

First use `git status --short` and stop if any tracked or untracked changes exist; do not switch branches, pull, stash, clean, or discard anything in a dirty checkout. Use `git remote -v` to identify the canonical remote; do not assume it is `origin`. Pull with `--ff-only` so synchronization cannot create a merge commit. Before opening a PR, fetch canonical `master` and verify the branch is not stale without switching away from the working branch.

After syncing, create the working branch using the required `<epoch-seconds>-<github-username>` format, where the username comes from the authenticated `gh` account. Reuse that exact branch name through push and PR creation. See `references/git-pr-workflow.md` for the commands.

### 2. Re-read the schema from the live repo — don't trust a hardcoded schema

Before building any row, check the actual current state of the dataset without running its code:
- Read `README.md` and `CONTRIBUTING.md` in the repo root for the current contribution rules.
- Read `src/config.ts` for the current `headers` and `BREWERY_TYPES` definitions. This live source configuration takes precedence over the public API documentation, which can lag the dataset.
- Read the header row of the source CSV file you're about to touch to confirm the exact current column order and names. If unsure which file, root-level `breweries.csv` is acceptable for read-only comparison, but it is generated and never a write target.

The dataset's `tags` column has been removed — do not include it even if older docs mention it. Trust the CSV header over any doc or memory of the schema.

Known-as-of-now columns (confirm live each run): `id` (never set by you; assigned by the maintainer when merging), `name`, `brewery_type`, `address_1`, `address_2`, `address_3`, `city`, `state_province`, `postal_code`, `country`, `phone`, `website_url`, `longitude`, `latitude`.

Known-as-of-now types include `alt prop`, `bar`, `beer brand`, `brewpub`, `cidery`, `closed`, `contract`, `large`, `location`, `micro`, `nano`, `office only location`, `planning`, `proprietor`, `regional`, `taproom`, and `beergarden`. Never rely on this snapshot: use the live `BREWERY_TYPES` definition for the contribution.

### 3. Research and validate the brewery

Given the name + rough location the user provided, web search to confirm:
- It is a real brewery-related entity or physical location that maps unambiguously to a live `brewery_type`.
- Its full street address
- Its official website
- Its phone number
- Signals for `brewery_type` (e.g. "brewpub" language on their own site, self-description as a taproom/large regional brand, etc.)
- Any signal it has **closed** (recent news, "permanently closed" on its own site or listings, no longer answering) — check this even on a plain "add" request, since a just-closed brewery should probably be flagged rather than added as active

**If you can't confirm the brewery with real confidence — ambiguous name, no findable official site/address, conflicting info — stop and ask the user for more detail** (exact city, street, alternate name) rather than guessing or adding a low-confidence row.

**Resolve conflicts by field and recency.** Prefer the official business site for ordinary contact details. For operating status, relocation, or ownership, weigh recent first-party statements, regulator records, property announcements, and credible dated reporting above an abandoned official page. If no primary source resolves a field, require corroboration from two genuinely independent sources; syndicated copies of one listing count as one source. Stop and ask when the evidence remains tied or ambiguous.

Note in the proposed diff (step 7) when a field was resolved this way, so the user can see it wasn't a single unverified source.

**Never fabricate a field.** If a value genuinely can't be found in any search result, leave it blank/null rather than inferring something plausible-sounding (this applies especially to phone, website, and address_2/3 — it's normal and correct for these to be empty). Every non-blank field in the diff summary should be traceable to something an actual search result stated, not something inferred from general knowledge of what breweries are usually like.

Standalone retail bottleshops do not have a dedicated dataset type. Do not force them into `bar` or another value. If the business also brews, classify the brewing operation from live evidence; otherwise stop and explain that it does not map to the current schema. Apply the same caution to kiosks, pickup points, offices, and brand-only listings.

### 4. Decide: addition, deletion, or update

Search the relevant CSV(s) for a possible existing match. **Match on normalized name, not literal string equality** — case, punctuation, whitespace, and common suffix variants ("Brewing Co" vs "Brewing Company" vs "Brewing Company, LLC") shouldn't cause a real match to be missed and create a duplicate row. Only treat it as the *same* brewery (i.e., an update) if you're highly confident based on multiple matching attributes together — e.g. name + city + state_province, or name + postal code — not name alone (brewery names repeat across regions/chains). If it's ambiguous whether this is a new entry or an existing one, stop and ask the user rather than guessing.

Search open issues and pull requests in `openbrewerydb/openbrewerydb` for the brewery name, address, and likely region. If equivalent work is already open, stop and report it rather than creating a competing contribution.

**Watch for sibling/related locations sharing a name and street** — e.g. a brewery that also runs a separate taproom, food hall, or experimental-brewing spinoff at a different address on the same street. Match on the full address, not just name + city/street, or you risk silently updating the wrong sibling location.

- **Addition** → go to step 5 and add one new row with an empty `id`; never generate, copy, or invent one.
- **Deletion** → remove only the confidently matched row. Confirm and document why deletion, rather than changing `brewery_type` to `closed`, is appropriate.
- **Update** → identify exactly which fields are actually changing (phone, website, address, type, closed status, etc.) and only touch those.

### 5. Resolve the target source CSV

**Never hand-edit root-level `breweries.csv`.** It's a generated file, rebuilt by the repository maintainer from the individual state/province/country CSVs, and is not a source file. Always make additions, deletions, and updates only in the per-region source file. Do not regenerate any root-level dataset artifact.

- Follow the live `data/<country>/<state-or-province>.csv` organization and neighboring slug conventions.
- If the required country or region partition does not exist, do not edit generated root-level files or invent a layout. Present the proposed path and ask the user or maintainer to confirm it before creating a source file.
- For every addition, leave the `id` field empty. Preserve the column and its delimiter in the CSV, but do not use a placeholder value; the repository maintainer assigns the ID when merging the change.
- Insert the new row in **alphabetical order by `name`** within the file — this is the dataset's sort convention, not something to detect per-file.
- **Match the file's existing formatting conventions** before writing your row — look at a handful of neighboring rows for how phone numbers are formatted, how addresses are abbreviated (e.g. "St" vs "Street"), and how the country name is spelled (e.g. "United States" vs "USA"). Don't introduce a new convention even if it seems more "correct" — consistency with the existing file matters more here.

### 6. Geocode the proposed address

Geocode every new or changed address before editing a CSV. Use the Geocodio CLI commands in `references/geocodio-cli.md`.

- For 1-10 addresses, geocode individually with machine-readable output.
- Above 10 addresses, get explicit user approval for the estimated lookup count and possible charges before using synchronous batch or asynchronous spreadsheet processing.
- Accept only results with accuracy at least `0.7`, and confirm the returned city, region, and country.
- Map Geocodio `lat` to CSV `latitude` and `lng` to CSV `longitude`; never swap them because the CSV stores longitude first.
- Pay-as-you-go includes 2,500 free daily lookups, not a hard daily cap. Usage beyond that can incur charges unless the account has a billing limit.

If geocoding is unavailable, unsupported by the account's country coverage, low-confidence, or geographically inconsistent, ask the user for coordinates. Leave both coordinate fields blank only when the user cannot provide them, and record the reason in the proposed diff.

### 7. Present the proposed change before writing

For every record change, show the source file, source URLs, sourcing notes, and a Markdown comparison table before editing:

| Field | Old value | New value |
|---|---|---|
| `<field>` | `<old value or (none)>` | `<new value or (blank)>` |

- **Addition**: include every field; show the new `id` as `(blank)`.
- **Deletion**: include every field and use `(none)` for new values.
- **Update**: include only changed fields.

Proceed after presenting the table unless evidence, identity, classification, file placement, or coordinates remain uncertain. In that case, wait for the user's decision.

### 8. Write and manually review one source CSV change

Write only the proposed change, then review it without running any npm script or its implementation:

- Confirm only the intended source CSV changed.
- Confirm each changed row follows the live header, column count, and CSV quoting.
- Confirm required fields satisfy the live schema. If a real country lacks a postal code but the live schema requires one, stop for maintainer guidance instead of inventing a value.
- Confirm the type exists in live `BREWERY_TYPES` and additions have an empty `id` field with no placeholder.
- Recheck duplicates, sibling locations, and alphabetical order.
- Leave generated datasets, statistics, IDs, and contributor files unchanged.

State in the PR body that npm scripts were intentionally left for the maintainer's merge and publication workflow.

### 9. Commit every change separately

A change is one addition, one deletion, or one update to one brewery record. Make exactly one commit for each change, even when several changes affect the same brewery or source CSV, so every change can be reverted independently. Never combine multiple record changes in one commit. Complete, review, stage, and commit one change before editing the next; this prevents `git add <source-file>` from accidentally staging multiple changes in the same CSV. Verify the staged diff contains exactly one change before committing. Commit only source CSV changes; do not regenerate or commit root-level dataset artifacts. See `references/git-pr-workflow.md` for branch naming and commit message conventions.

### 10. Push and open the PR

Always open a PR against the `master` branch of the canonical `openbrewerydb/openbrewerydb` repository. Never commit or push directly to `master`, even if you have access. The PR body must begin with the exact required message in `references/git-pr-workflow.md` and include a commit-by-commit change log below it.

After opening the PR, add one PR comment per change/commit. Each comment must identify the corresponding commit, explain the change, list its data sources and sourcing notes, and include the old/new Markdown table from step 7. Verify the target, comments, changed files, and GitHub Actions status before reporting completion. Upstream CI may run maintainer-configured checks; do not reproduce them locally. See `references/git-pr-workflow.md`.

## When to stop and ask instead of proceeding

- Required tooling is missing or broken — `git` or `gh` not installed/authenticated (step 0). Geocodio missing is the one exception: degrade gracefully, don't block (steps 0 and 6) — but do ask the user for lat/long directly rather than silently proceeding without it.
- Can't confirm the brewery is real / can't find a reliable address, or sources conflict with no majority (step 3)
- Ambiguous whether this is a new brewery or a match to an existing row, including sibling/related locations sharing a name and street (step 4)
- The source CSV cannot be confidently reviewed for valid columns, quoting, required fields, blank IDs on additions, or duplicates without a maintainer-only script (step 8). Ask the user or repository maintainer rather than running the script.
- Geocoding is a miss for any reason — low accuracy, wrong city/state, unavailable tool, or country not covered on the plan (step 6) — ask the user for coordinates before falling back to leaving them blank
- Uncommitted local changes are already sitting in the repo (step 1)
