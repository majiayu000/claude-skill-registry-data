---
name: leed-tracker
description: "This skill should be used when the user wants to build, update, or score a LEED v4.1 BD+C New Construction scorecard for an architectural project — by walking the credit list, declaring pursuit status (Yes / Maybe / No / N/A) for each credit, and summing points to predict certification level (Certified / Silver / Gold / Platinum). Trigger on \"LEED scorecard\", \"LEED v4.1 score\", \"score this project for LEED\", \"LEED tracker\", or pasted project program with sustainability goals. Reads bundled credit-by-credit point matrix from USGBC LEED v4.1 BD+C and outputs a CSV scorecard plus a markdown summary in `docs/leed/`. Does NOT make LEED eligibility judgments — the user declares what they intend to pursue; this skill organizes and scores."
license: MIT
metadata:
  title: "LEED Tracker"
  summary: "Score a project scorecard and predict its certification level"
  discipline: "envelope-performance"
  tags: "Compliance"
---


# LEED Tracker


## Overview


Build a LEED v4.1 BD+C: New Construction scorecard for a project. The user declares pursuit status for each credit; this skill computes the running point total and the predicted certification level. Output is a CSV (one row per credit) plus a markdown summary in `docs/leed/`. This replaces the manual spreadsheet pass at every project's pre-design phase, kept evergreen through CD.


This skill **does not** decide whether a credit is _achievable_ for a project — that is a strategy call by the LEED-AP and the design team. The skill organizes the structure, performs the arithmetic, cites the point matrix verbatim from `references/`, and flags which credits the user has not yet committed on.


## Scope and limits — read first


This skill covers:

- **LEED v4.1 BD+C: New Construction (NC)** — 110 points, certification thresholds 40/50/60/80.
- LEED **categories** (LT, SS, WE, EA, MR, EQ, IN, RP) and **credit structure** at the level published in the USGBC LEED v4.1 BD+C scorecard / Reference Guide table of contents.

This skill does **NOT** cover:

- Other LEED v4.1 rating systems: Core & Shell, Schools, Retail, Data Centers, Warehouses, Hospitality, Healthcare. (Different point allocations.)
- LEED v4.1 ID+C, O+M, ND, Cities & Communities. (Out of scope.)
- LEED v4 (the predecessor). v4 projects use a different (but related) credit list.
- LEED v5 (when published). Update `references/` and the **Last verified** date in `references/_provenance.md` when v5 ships.
- **Eligibility judgments.** The skill does not decide whether your project earns a credit; it reflects what you declare.
- The full prerequisite + credit _technical content_ (model documentation, calc methodology). The point matrix and credit names are bundled; the _how to earn_ lives in the LEED Reference Guide (paywalled from USGBC) which this skill does not redistribute.

For credit substantive content, the user must consult the official USGBC LEED v4.1 BD+C Reference Guide.


## When to use


Trigger on:

- "Make a LEED scorecard for this project."
- "Score this project for LEED v4.1."
- "Update the LEED tracker — we just confirmed EA Cr 2 is in."
- Pasted sustainability targets ("project targets LEED Silver — track progress").

Do NOT trigger on:

- "What credits can my project earn?" — that's a strategy question, not a tracker request.
- LEED v4 (older) or v5 (newer) — out of scope.
- Other rating systems (WELL, Living Building Challenge, Passive House) — those have separate trackers in the catalog.

## Workflow


### Step 1 — Bootstrap if needed


Check whether `docs/leed/index.md` exists. If not, run:


```bash
python scripts/init_workspace.py
```


The script creates `docs/leed/` and an empty tracker log. No external Python dependencies. Confirm with the user before bootstrapping if `docs/` does not already exist.


### Step 2 — Confirm rating system


State explicitly to the user:

> "This skill scores against LEED v4.1 BD+C: New Construction (110 points; Cert 40 / Silver 50 / Gold 60 / Platinum 80). If your project is on a different rating system or version, this skill is the wrong tool. Continue?"

Do not proceed silently if the user has not confirmed the rating system.


### Step 3 — Gather project context


Read `docs/project.md` if present. Otherwise ask the user for:

- `project_name`
- `target_certification_level` ("Certified" / "Silver" / "Gold" / "Platinum" / "TBD")
- `phase` ("pre-design" / "SD" / "DD" / "CD" / "construction" / "operation")

### Step 4 — Initialize a fresh scorecard, or update an existing one


If a scorecard CSV exists at `docs/leed/<project-slug>-leed-scorecard.csv`, load it and present current totals before editing. Otherwise initialize from `assets/leed-v41-bdc-nc-scorecard-template.csv`, which is pre-seeded with every credit's name, category, max-points, and prereq flag — sourced verbatim from `references/leed_v41_bdc_nc_points.md`.


### Step 5 — Walk the credit list with the user


For each credit, the user declares one of:

- `Yes` — committed to pursuit; counts toward score.
- `Maybe` — under consideration; counted only in the optimistic total.
- `No` — not pursuing; zero contribution.
- `N/A` — not applicable to this project type.

For credits with point options (e.g. EA Credit 2 has multiple paths each yielding 1–18 points), the user states the points-attempted; the skill verifies that against the max published in `references/`.


For prerequisites (P), they must be `Yes` or `N/A`. If marked `N/A`, the user must justify; if `No`, the project is non-compliant — flag.


### Step 6 — Compute scores


Run:


```bash
python scripts/compute_score.py \
  --scorecard docs/leed/<project-slug>-leed-scorecard.csv \
  --out docs/leed/.cache/<project-slug>-score.json
```


The script computes:

- Committed points (Yes only).
- Optimistic points (Yes + Maybe).
- Predicted certification level for both totals using the v4.1 BD+C thresholds (40 / 50 / 60 / 80).
- Per-category subtotals.
- Prerequisite status (all met / failures listed).

The script reads thresholds and max points from `references/leed_v41_bdc_nc_points.md` — never hard-coded into the script.


### Step 7 — Write the markdown summary


Beside the CSV, write `docs/leed/<project-slug>-leed-summary.md`:

- Header with project name + target + phase + last-updated date.
- Committed total, optimistic total, predicted cert level for each.
- Per-category subtotal table.
- List of credits marked `Maybe` (next-decision queue).
- Prereq compliance status.
- Citation footer: standard version (LEED v4.1 BD+C: NC), reference file path, USGBC Reference Guide pointer.

### Step 8 — Update the project LEED index


Run:


```bash
python scripts/append_to_index.py \
  --date 2026-05-08 \
  --project "<project-slug>" \
  --target "<Silver|Gold|Platinum|Certified>" \
  --phase "<phase>" \
  --committed <committed-points> \
  --optimistic <optimistic-points> \
  --cert-predicted "<level>" \
  --csv "<project-slug>-leed-scorecard.csv" \
  --summary "<project-slug>-leed-summary.md"
```


Appends a row to `docs/leed/index.md`. Do NOT edit `index.md` with Edit.


### Step 9 — Report


Tell the user:

- Path to scorecard CSV + summary.
- Committed / Optimistic point totals + predicted cert level for each.
- Top 5 credits marked `Maybe` (highest-leverage decisions).
- Any prereq concerns.
- Reminder: this is structural tracking, not eligibility judgment — verify each `Yes` against USGBC LEED v4.1 BD+C Reference Guide credit requirements.

## Rules

- Every row in the scorecard CSV must reference a credit that exists in `references/leed_v41_bdc_nc_points.md`. No invented credits.
- Max points per credit are quoted from the references file; the skill never increases a credit's max (e.g. EA Credit 2 max = 18 — do not let the user enter 20).
- Certification thresholds come from `references/leed_v41_bdc_nc_points.md`, never from training data.
- Score arithmetic runs through `compute_score.py`, never inline math by Claude.
- Output files live in `docs/leed/` of the user's project.
- Standard version (LEED v4.1 BD+C: New Construction) and last-verified date are reported in every summary.

## Anti-patterns

- Adding a credit not in `references/`. If the user asks about a credit by a name not in the references, treat as user typo and propose the closest match — do not invent.
- Letting the user record more points than the credit's max.
- Predicting a higher cert level than the thresholds support.
- Recommending which credits to pursue. This skill is structural — strategic credit selection belongs to the LEED-AP.
- Editing `docs/leed/index.md` directly with Edit.
- Treating LEED v4 / v5 / different rating systems as scoreable here.

## Resources

- `scripts/init_workspace.py` — bootstrap `docs/leed/`
- `scripts/compute_score.py` — sum points, evaluate cert level, validate against references
- `scripts/append_to_index.py` — append a row to `docs/leed/index.md`
- `references/_provenance.md` — source, version, last-verified
- `references/leed_v41_bdc_nc_points.md` — full credit list with point values, prereqs, thresholds
- `references/leed_categories.md` — category structure, point allocation per category
- `assets/leed-v41-bdc-nc-scorecard-template.csv` — pre-seeded scorecard (one row per credit)
- `assets/leed-index-template.md` — header table for `docs/leed/index.md`
