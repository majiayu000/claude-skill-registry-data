---
name: agri-pipeline
description: "Master orchestrator for the whole agricultural research-to-publication workflow, run as a senior agricultural scientist. Coordinates the agri skills — journal selection, research (agri-research or agri-deep-research), writing and analysis (agri-paper), figures (food-figure), peer review (agri-review), revision and finalization — into one governed path with quality gates. Same machinery as food-pipeline, grounded in agriculture and multidisciplinary literature (Q1/Q2 preferred, Q4 avoided). Use when the user wants the entire agricultural process managed end to end. Triggers: run the full agricultural paper workflow, take my field trial from research to submission, manage my whole agronomy project, agricultural research to publication, end-to-end agriculture paper."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  delegates_to: food-pipeline
  related_skills: [agri-research, agri-deep-research, agri-paper, agri-review, food-figure, journal-selector, food-pipeline]
  references:
    - ../agri-research/references/agriculture-domain.md
---

# Agri-Pipeline — Research-to-Publication for Agricultural Science

**Run the `food-pipeline` skill exactly** — its subagents (`intake_router`,
`quality_gate`), its **stages 0–6**, its quality gates, its mode advisor, and its
review/revision authorization defaults — with the agriculture substitutions in
[`agri-research/references/agriculture-domain.md`](../agri-research/references/agriculture-domain.md).
Read that file first. No new machinery here.

## The substitutions
1. **Persona** — a **senior agricultural scientist of the specific discipline**,
   carried into every stage and every skill it dispatches (domain §2).
2. **Route to the `agri-*` skills**, not the food ones:

| Stage | Skill |
|---|---|
| 0 · ROUTE | `intake_router` + `journal-selector` (agriculture coverage map) |
| 1 · RESEARCH | **`agri-research`** (or **`agri-deep-research`**) |
| 2 · WRITE | **`agri-paper`** → figures via **`food-figure`** (domain-neutral) |
| 3 · REVIEW | **`agri-review`** |
| 4 · REVISE | **`agri-paper`** (revise) |
| 5 · RE-REVIEW | **`agri-review`** (re-review) |
| 6 · FINALIZE | **`agri-paper`** (format-convert) |

3. **Evidence base** — Tier 1 Q1/Q2 agriculture + Nature/Science/Cell/PNAS + Q1/Q2
   adjacent disciplines; Q3 for gaps; **Q4 avoided** (domain §3).

`food-figure` is used directly and deliberately — it is domain-neutral and already
renders at the journal spec.

## Inherited unchanged (not optional)
- **Journal resolved once** at ROUTE via `journal-selector` and passed to every
  downstream skill, so none re-asks.
- **Knowledge reuse:** when Stage 1 runs, its evidence base is carried into Stages
  3/5 so `agri-review` does **not** re-search the field — it reuses it and tops up
  with `agri-research` **quick brief** key reviews read in full.
- **Review/revision defaults:** **one** review→revise round; a second round **and**
  in-place Tracked Changes on the original Word file each require **explicit author
  authorization**.
- **Deliverables — exactly two files, both `.docx`:** one **manuscript**, and **one
  `Review_and_Response_Report_<slug>_<date>.docx`** carrying **both the reviewer
  feedback and the editing response** — `agri-review` writes the feedback at Stage 3,
  `agri-paper` fills each `Response (type)` into that **same file** at Stage 4, and an
  authorized round 2 appends `R2-*` items to it. **No separate reviewer report, no
  standalone response letter, never Markdown**
  (`food-review/references/report-format.md`).
- Quality gates, anti-fabrication grounding, four-gate citations, privacy scan,
  `human-writing.md`, and the **mandatory AI-use disclosure**.

## Agricultural gates (domain §5)
At the Stage-2 gate, do not pass a manuscript that omits **the experimental unit**,
field-trial reporting (site, season/years, soil, cultivar, design, replication), or
ethics/**ARRIVE** for animal work — these are the flaws that end agricultural papers
at review.
