---
name: find-data
description: "Find a dataset for a Data2Story blog. Accepts a topic, a URL, or a DIP-style category. Downloads + validates against 4 completeness gates before handing off to /data2story-pro. Local-first: searches Economist/Pudding/TidyTuesday clones before going online. Supports --validate-only to audit a folder you already have."
argument-hint: "<topic | URL | category | folder-path> [--mode single|theme] [--source Economist|Pudding|tidytuesday] [--out ./datasets/<name>] [--validate-only]"
allowed-tools: Bash(python:*), Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
---

# find-data

Turn an idea, URL, or category into a `phase2/datasets/<name>/` folder
that the `/data2story-pro` pipeline can run on without crashing.

You are the **gatekeeper before the 7-agent newsroom**. Detective, Analyst,
Editor, Designer, Programmer, Auditor, Inspector all assume the data is
already there, parseable, and provenanced. Your job is to make sure that's
true before they start.

Refuse to mark a folder ready until it passes 4 gates. See
`references/completeness_gates.md` for the criteria. The gates are codified
in `tools/audit.py`, not in this prose.

## Prerequisites

Python deps for the `tools/`:

- **`pandas`** — required (`audit.py` reads/inspects CSV/JSON).
- **`openpyxl`** — required **only** when a source is `.xlsx` (`audit.py`'s
  `pd.ExcelFile`); a mid-run missing-`openpyxl` is the usual cause of an XLSX
  audit error.
- **`urllib`** — stdlib, no install (`fetch.py` downloads, `audit.py` HEAD-checks).

One install line:

```bash
pip install pandas openpyxl
```

After editing anything under `tools/`, run the no-network regression suite:
`py tools/selftest.py` (exit 0 = pass).

## Resolve paths first

- `SKILL_DIR` = directory containing this `SKILL.md`
- `WORKSPACE` = ancestor that contains `phase2/datasets/` (the parent repo root), if one exists
- `DATASETS_ROOT` = `WORKSPACE/phase2/datasets` when `WORKSPACE` exists; otherwise `./datasets`
  (clone-relative, under the current working dir) — the open-source clone has no `phase2/datasets`
- `BLOGS_ROOT`    = `WORKSPACE/phase2/blogs` when `WORKSPACE` exists
- `OUT_DIR` default = `DATASETS_ROOT/<name>` (so `./datasets/<name>` on an OSS clone). Callers may
  override with an explicit `--out`, which always wins.
- `INPUT` = first positional argument from `$ARGUMENTS`
- Parse flags from `$ARGUMENTS`: `--mode`, `--source`, `--out`, `--validate-only`

Never hard-code machine paths. Resolve at runtime by walking up from `SKILL_DIR`.

## Step 0 — Classify the input

Decision tree (the FIRST condition that matches wins):

1. **`--validate-only` flag present** → MODE = `validate-only`. `INPUT` must be an existing folder path.
2. **`INPUT` is an existing folder path** (and `--validate-only` absent) → still ask the user before re-fetching; default to `validate-only` behaviour with a confirmation.
3. **`INPUT` starts with `http://` or `https://`** → MODE = `url`.
4. **`INPUT` (case-insensitive) exactly matches a DIP category** from `phase2/datasets/data_is_plural/dip_category_summary.md` → MODE = `category`.
5. **Otherwise** → MODE = `topic`.

State your classification out loud in one line before doing anything else.

**No local corpora (open-source clone):** on a machine without the `Economist/`, `Pudding/`,
`tidytuesday/` clones and without the Data-is-Plural CSV under `phase2/datasets/`, `browse_local.py`
and `dip_query.py` both return empty (no crash). In that case there is nothing to match locally, so
`topic`/`category` discovery degrades straight to WebSearch (Step 1). No flag is needed — detect it
from the empty `browse_local.py` + `dip_query.py` results. Keep the local-first path intact for
machines that DO have the corpora.

## Step 1 — Branch on mode

### validate-only mode

Just audit. Skip discovery, skip fetch.

```bash
python "SKILL_DIR/tools/audit.py" "<folder>"
```

This writes `<folder>/validate.json` and prints the gate summary. Read it back
with `Read`, surface the verdict, and stop.

If `overall.ready_for_data2story` is true → print the `/data2story-pro <folder>`
command for the user to copy.

If it's false → list the specific gate failures and recommend remediations.

### url mode

Determine OUT_DIR (use `--out` if given, else derive a slug from the URL path's
last meaningful segment, store under `DATASETS_ROOT/<slug>/` — i.e. `./datasets/<slug>/`
on an open-source clone with no `phase2/datasets`).

Branch on URL shape:

| URL pattern | Tool |
|---|---|
| `github.com/{owner}/{repo}/tree/{branch}/{path}` | `python fetch.py github-folder <url> <out_dir>` |
| `github.com/{owner}/{repo}/blob/{branch}/{path}` | Same (fetch.py auto-detects blob) |
| `github.com/{owner}/{repo}` with no path | Refuse — tell user to narrow to a folder |
| Anything else | `python fetch.py url <url> <out_dir>` |

`fetch.py` is source-aware: if the URL points to `TheEconomist/graphic-detail-data`,
`the-pudding/data`, or `rfordatascience/tidytuesday` AND the local clone already
contains that path, it copies from the local clone (no network). Otherwise it
fetches via the GitHub API. This happens automatically — do not handle it yourself.

#### URL normalization (share-page vs direct-download)

Several hosts serve a human-facing **page** at the obvious URL, not the raw bytes,
so a naive download returns HTML instead of a `.csv`/`.json`/`.xlsx`. `fetch.py`
auto-rewrites GitHub `/blob/` URLs to `raw.githubusercontent.com` and, as a
backstop, **warns on stderr** if a data-extension download comes back as an HTML
page (`<!doctype html>` / `<html`). The other common share-hosts are **not**
auto-rewritten — pass the **direct-download** form yourself:

| Host | Page URL (returns HTML) | Direct-download form to use |
|---|---|---|
| GitHub | `github.com/<o>/<r>/blob/<branch>/<path>` | auto-handled → `raw.githubusercontent.com/<o>/<r>/<branch>/<path>` |
| Google Drive | `drive.google.com/file/d/<id>/view` | `drive.google.com/uc?export=download&id=<id>` |
| Dropbox | `...?dl=0` | swap to `...?dl=1` (or `dl.dropboxusercontent.com`) |
| OneDrive | share link (`1drv.ms/...`) | append `&download=1` to the direct link |
| Kaggle | dataset page (`kaggle.com/datasets/...`) | the file API / CLI download — the page is not a file |

If a download trips the HTML warning, you almost certainly handed `fetch.py` a
share/page URL — fix the URL to its direct-download form and re-fetch.

After fetch: check whether the folder has a README.md.
- If yes → leave it alone, jump to Step 2.
- If no → generate one from `tools/README_template.md`. Auto-fill what you can
  (title from folder name, column headers from the first CSV, source URL from
  the manifest). Leave the codebook `definition` cells as `{TODO}` for the user
  to fill in. Tell the user explicitly that README is a stub.

### category mode

`INPUT` is one of the 14 DIP categories. Run both browse and DIP query in parallel:

```bash
python tools/browse_local.py "<INPUT>" --top 10
python tools/dip_query.py --category "<INPUT>" --top 10
```

Both emit JSON. Merge:
- Local candidates (already-cloned folders) score higher than DIP leads
  (which still need fetching).
- For each local candidate, run a cheap pre-score (does Gate 1 trivially pass —
  is there ≥ 1 CSV in the folder?).

Present top 5 to the user as a numbered list via `AskUserQuestion`:
- For each candidate, show: source · title · date · top-3 files · 1-line readme excerpt
- Options: pick 1–5, or "all" (theme mode), or "skip" (abort)

Then route the pick:
- Local candidate → copy folder into OUT_DIR (or in-place audit if user accepts).
- DIP lead → extract URL from the candidate's `links` array. If multiple URLs,
  pick the one with a data-file extension (csv/xlsx/json) or the GitHub one.
  Route to url mode for that URL.

### topic mode

Same as category mode but use full-text query:

```bash
python tools/browse_local.py "<INPUT>"
python tools/dip_query.py "<INPUT>" --top 10
```

If BOTH return empty (no local hits, no DIP hits), only THEN do WebSearch:
`<INPUT> open dataset CSV site:ourworldindata.org OR site:github.com OR site:data.gov`.
Cap web results at 5. Surface them with a "no local matches found, querying web" disclaimer.

From the WebSearch results, pick the one whose URL ends in a data-file extension
(`.csv` / `.xlsx` / `.json` / `.tsv`) or is a `github.com/{owner}/{repo}/tree/{branch}/{path}`
folder. Route that URL through url mode: `python tools/fetch.py url <url> <OUT_DIR>` for a direct
data file, or `python tools/fetch.py github-folder <url> <OUT_DIR>` for a GitHub folder. Then
continue to the README step (Step 2) and the audit step (Step 3) exactly as in url mode — this
closes the topic → web → fetch → audit loop. If no result has a usable data URL, report that
honestly and do not fabricate one.

## Step 2 — Optional: generate / repair the README

After fetch, the OUT_DIR may or may not have a README. Decide:

- README present + has codebook table + has source mention → leave alone
- README missing → generate from `tools/README_template.md`
- README present but no codebook table → ADD a codebook section, do not
  overwrite the existing prose

When generating, fill in:
- `{TITLE}`: human-readable from folder slug (snake_case → "snake case", title-cased)
- `{PRIMARY SOURCE URL}`: from `manifest.json` items' urls
- `{filename.csv}` rows: scan each CSV's columns
- `{Codebook}`: list each column with `{TODO: definition}` for unknown ones; you
  may guess from column names (`launch_year` → "year of launch (integer)") but
  flag guesses with a `{?}` prefix so the user can correct.

## Step 3 — Audit (the 4 gates)

```bash
python "SKILL_DIR/tools/audit.py" "<OUT_DIR>"
```

This writes `<OUT_DIR>/validate.json`. Read it back.

For Gate 4 (multimodal — advisory only), `audit.py` cannot judge by itself.
Do your own quick check after reading `validate.json`:

- From the CSV columns and entity samples, classify subjects:
  - **Concrete** (people / places / species / events / specific objects) — e.g.,
    "launches.csv has agency names like SpaceX, NASA, Roscosmos → concrete"
  - **Abstract** (rates, indices, generic counts) — e.g.,
    "GDP per capita time series → abstract"

- For concrete subjects, do ONE WebSearch with `site:commons.wikimedia.org`
  to verify at least 1 reference photo exists for a representative subject.
  Do NOT download photos — just verify they exist. That's Detective's job.

- Write your Gate 4 finding back into `validate.json` under
  `gates.multimodal.info`.

## Step 4 — Verdict

Read the final `validate.json`. Print a concise summary:

```
=== find-data verdict ===
folder: <OUT_DIR>
files: <N>
[OK ] Technical
[WARN] Story material
       - <filename.csv>: only 47 rows (< 50)
[OK ] Provenance
[INFO] Multimodal: concrete subjects (agencies, rocket types)

overall: READY
next:    /data2story-pro <OUT_DIR>
```

If overall is BLOCKED, do NOT print the `/data2story-pro` command. Instead print:

```
overall: BLOCKED
to fix: <specific remediations from the fails list>
```

Suggest concrete fixes:
- "README missing → run /find-data --validate-only <folder> after adding README"
- "Primary URL dead → find an alternate source via /find-data --source-finder"
- (or open-ended: "drop a corrected file into <path> and re-run")

## Step 5 — Save a digest

Append a one-line entry to `DATASETS_ROOT/_find-data-log.md` (create if not
present) so the user has a running history:

```
- 2026-05-25T14:00Z · single · datasets/<name> · READY · invoked via URL
```

## Constraints

- **Never overwrite an existing README.md without asking.** Generate-from-template
  only fires when README is absent. If README exists but is thin, ADD sections, don't replace.
- **Never modify the skill repo itself.** Your only writes are inside the dataset output
  directory (`DATASETS_ROOT/<OUT_DIR>/`) and the digest log.
- **Never fabricate a source URL or license.** If you can't find a real source for a
  generated README, leave the `{PRIMARY SOURCE URL}` placeholder and warn the user.
- **Cap WebSearch at 5 results, cap WebFetch at 3 calls per invocation.** This is a
  gating skill, not a research tool — depth is Detective's job.
- **Do not run /data2story-pro yourself.** Your last word is the verdict + the command for
  the user to copy. Hand-off is manual.

## Reference files

- `references/completeness_gates.md` — exact pass/warn/fail criteria for each gate
- `references/input_mode_dispatch.md` — full URL classification table
- `references/examples/good_economist.md` — what `single` mode output should look like
- `references/examples/good_theme.md` — what `theme` mode output should look like
- `tools/audit.py` — deterministic gate evaluator
- `tools/fetch.py` — source-aware downloader (manifest / github-folder / single-url modes)
- `tools/browse_local.py` — index Economist/Pudding/TidyTuesday for candidate matching
- `tools/dip_query.py` — filter dip_categorized.csv by category or topic
- `tools/README_template.md` — graphic-detail-style skeleton for auto-generation
