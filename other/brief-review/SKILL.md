---
name: brief-review
description: "This skill should be used when the user shares a project brief, RFP, or Owner's Project Requirements (OPR) and wants it interrogated for unstated assumptions, gaps, contradictions, and missing constraints before design work proceeds. Trigger on 'review this brief', 'check the RFP', 'unpack this brief', 'analyze the OPR', 'is this brief complete', or pasted brief text accompanied by a request to evaluate completeness. Generates a structured brief review markdown in `docs/briefs/` and appends to the project brief index."
license: MIT
metadata:
  title: "Brief Review"
  summary: "Interrogate a brief for gaps, contradictions, and unstated assumptions"
  discipline: "design-building-types"
  tags: "Pre-Design"
---


# Brief Review


## Overview


Interrogate an architectural project brief, RFP, or Owner's Project Requirements (OPR) against eight review axes and produce a written analysis that lives in `docs/briefs/`. The output is a working document — it lists gaps, contradictions, and recommended clarifying questions to send back to the owner before design work begins.


Aligned with North American practice: AIA B101 / B201 brief expectations, ASHRAE Guideline 0 (OPR), and LEED v4.1 / WELL v2 prerequisites for documented project requirements.


## Scope and limits — read first


**What this does.** Reads a brief, RFP, or OPR against eight axes and writes a
review to `docs/briefs/` that ends in two lists: gaps to close before SD, and
questions to send back to the owner. Every gap is tagged with the axis it came
from, so a reader can see why it counts as a gap.

**What this does not do.**

- **It does not fill in what the brief left out.** A missing area, budget, code
  edition, or AHJ is reported as a gap and never supplied from a typical value.
  That is the design, not a shortfall.
- It does not design or redesign. It evaluates the brief, not the project the
  brief describes.
- It does not estimate cost or schedule. The figures in
  `references/program_benchmarks.md` are planning-grade and exist to flag an
  implausible budget, not to become one. A cost consultant estimates.
- It does not check zoning or code. Those are `zoning-summary` and
  `code-compliance-review`.
- It does not talk to the owner. The clarifying questions are drafted for you
  to send.

**What you need before starting.** The brief itself as text or a file, which
kind of document it is (RFP, OPR, program brief, design brief), and the
jurisdiction and code edition if the brief does not name them.

## When to use


Trigger on:

- Pasted brief / RFP / OPR text with a request to evaluate it.
- Project file paths to a brief document the user wants reviewed.
- Explicit asks: "review this brief", "check the RFP", "unpack the OPR", "is this brief complete", "what's missing from this brief".

Do NOT trigger for:

- Design critique of an existing project (use `design-critic`).
- Zoning code analysis (use `zoning-summary`).
- Drawing-set review (use `drawing-checklist`).
- Translating brief content into client-facing language (use `client-translator`).

## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/briefs/index.md` exists. If not:


```bash
python scripts/init_briefs_workspace.py
```


### Step 2 — Gather context

- Read `docs/project.md` if it exists for owner, site, jurisdiction, prior decisions.
- Read the brief itself (pasted text, file path, or attached PDF).
- Identify the brief type: `rfp` | `opr` | `program-brief` | `design-brief`. Some axes apply differently across types (e.g., decision rights are heavier in RFPs; performance criteria are heavier in OPRs).

### Step 3 — Apply eight-axis review


Load `references/brief_axes.md` for the full framework with sub-criteria. Quick reference:

1. **Stated vs unstated objectives** — What the owner asks for vs what the building type/market implies they actually need. Surface unstated objectives explicitly.
2. **Program completeness** — Areas (gsf/nsf), populations, adjacencies, FF&E, growth assumptions. Check against `references/program_benchmarks.md` for typical NA building-type ranges.
3. **Site & jurisdiction context** — Address, zoning district referenced, AHJ named, applicable code edition (IBC year, state amendments, local), climate zone (ASHRAE 169), fire jurisdiction, utility providers.
4. **Performance criteria** — Energy targets (EUI, ASHRAE 90.1 vintage, IECC), certifications (LEED / WELL / Living Building / Fitwel / Passive House / RELi), commissioning scope (ASHRAE Guideline 0), POE benchmarks, measurable outcomes.
5. **Schedule & budget realism** — Order-of-magnitude check against typical $/gsf for the project type and region (use `references/program_benchmarks.md`). Flag if schedule excludes AHJ review timelines or long-lead procurement.
6. **Decision rights & governance** — Who signs off at SD/DD/CD? Single point of contact? Owner's rep / project manager? Internal committees, board approvals, public hearings?
7. **Risk & exclusions** — What's explicitly out of scope? Hazardous materials assumptions, geotech responsibility, existing-conditions verification, survey scope, demolition scope, permitting fees, owner-furnished items.
8. **Sustainability & resilience** — Net-zero pathway requested? Climate hazards considered (flood, wind, heat, wildfire, seismic)? Adaptive reuse vs new build trade-off addressed? If resilience is a stated priority but no hazard is named, that gap is itself the finding.

Focus on the 3-5 axes with real signal. Do not pretend to score every axis on every brief — note the ones that are clearly fine in one line and move on.


### Step 4 — Write the review


Read `assets/brief-review-template.md`, fill placeholders. Filename:


`docs/briefs/<YYYY-MM-DD>-<slug>-review.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from project name or brief topic (`acme-hq-opr`, `westside-school-rfp`). If a review with the same date+slug already exists, suffix `-<n>`.


Use the Write tool. Match the language of the brief (this skill is English-only by design — if the brief is non-English, translate quoted excerpts into English in the review).


### Step 5 — Update the brief index


```bash
python scripts/append_to_index.py \
  --date 2026-05-07 \
  --slug acme-hq-opr \
  --brief-type opr \
  --primary-axes "objectives,performance,decision-rights"
```


The script appends a row to `docs/briefs/index.md`. Do NOT edit the index manually with the Edit tool — table alignment breaks easily.


### Step 6 — Report


Tell the user:

- Path to the review file.
- The 2-3 most pressing gaps or contradictions.
- A short list of recommended clarifying questions to send back to the owner.
- Whether `zoning-summary` should be run next.

## Output structure


The review should end with two action lists:

- **Gaps to close before SD** — items the owner must resolve before schematic design can begin in earnest.
- **Questions back to owner** — phrased as direct questions, ready to copy into an email or RFI-style response.

## Rules

- Every gap cites WHY, rooted in one of the eight axes — never "this seems vague" without an axis tag.
- Refuse to invent program areas the brief did not state. If gsf is missing, flag it; do not guess.
- If the brief references a code edition, name the edition explicitly (e.g., "IBC 2021 with 2023 California amendments"). If the edition is absent, flag it.
- Distinguish hard contradictions (two clauses that cannot both be true) from soft tensions (priorities that compete but can be balanced).
- Specifics over generalities. "Brief states LEED Gold but excludes commissioning, which is a LEED prerequisite (EAp1)" beats "sustainability section is unclear."

## Anti-patterns

- Listing every axis even when most are clearly fine — pick the 3-5 with real signal.
- Suggesting redesign of the project. Brief review evaluates the brief, not the design.
- Inventing benchmarks not in `references/program_benchmarks.md` — if the project type isn't covered, say so.
- Editing `index.md` manually instead of using `append_to_index.py`.
- Pretending the brief is in worse shape than it is to look thorough. Acknowledge what's solid.

## Resources

- `scripts/init_briefs_workspace.py` — bootstrap `docs/briefs/` and the brief index
- `scripts/append_to_index.py` — append a row to `docs/briefs/index.md`
- `references/brief_axes.md` — detailed eight-axis review framework with sub-criteria and example findings
- `references/program_benchmarks.md` — typical $/gsf, gsf/occupant, and program ratios for North American building types (sanity-check schedule and budget)
- `assets/brief-review-template.md` — review markdown template
