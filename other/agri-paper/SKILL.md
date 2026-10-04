---
name: agri-paper
description: "Multi-subagent manuscript system for agricultural science, written as a senior agricultural scientist of the relevant discipline: understand the field, frame questions, curate data, run statistics, build figures and tables, construct the discussion, draft, polish, and self-review — journal-aware throughout. Same machinery as food-paper, grounded in agriculture literature (Q1/Q2 preferred, Q4 avoided) and agricultural reporting standards for field trials, animal work and soils. Includes a format-convert mode that reformats a finished manuscript for another journal without touching the science. Triggers: write my agronomy paper, draft an agricultural manuscript, soil science paper, horticulture paper, animal science manuscript, analyze my field trial and write it up, format for an agriculture journal, reformat my manuscript for a different journal, my agricultural paper is finished I just need the formatting."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  delegates_to: food-paper
  related_skills: [agri-research, agri-review, agri-pipeline, food-figure, journal-selector, food-paper]
  references:
    - ../agri-research/references/agriculture-domain.md
---

# Agri-Paper — Manuscript System for Agricultural Science

**Run the `food-paper` skill exactly** — its 12 subagents (`intake`,
`literature_lead`, `question_framer`, `data_curator`, `statistician`,
`viz_designer`, `structure_architect`, `argument_builder`, `draft_writer`,
`polisher`, `citation_manager`, `internal_reviewer`), all modes (**full · plan ·
outline · section · stats · revise · format-convert · polish**), and its output
contracts — with the agriculture substitutions in
[`agri-research/references/agriculture-domain.md`](../agri-research/references/agriculture-domain.md).
Read that file first. No new machinery here.

## The substitutions
1. **Persona** — a **senior agricultural scientist of the specific discipline**;
   name it and write to its standards (domain §2).
2. **Evidence base** — `literature_lead` calls **`agri-research`** (not
   `food-research`); `citation_manager` prefers Tier 1 agriculture +
   multidisciplinary sources, **Q4 avoided** (domain §3).
3. **Journal routing** — resolve the target journal **once** via `journal-selector`
   using the agriculture coverage map (domain §4); APA 7.0 if 'generic'.

Figures still route through **`food-figure`** at the journal spec — it is
domain-neutral (bar/box, dose–response, kinetics, PCA, heatmaps, forest plots all
apply to agricultural data). Revision still follows
`food-paper/references/revision-response.md`; peer review calls **`agri-review`**.

## Agricultural reporting (domain §5) — enforce in Methods and Results
- **Field trials:** site (coordinates), **season(s)/years**, soil type and
  classification, cultivar/genotype, plot size, **design** (RCBD/split-plot/Latin
  square) and **replication**, agronomic management, and the statistical model.
- **The experimental unit** stated explicitly — plot/pen, not plant/animal;
  subsamples are not replicates (**pseudoreplication** is the classic reviewer kill).
- **G×E and season-to-season variation** addressed, or the limitation stated; a
  single site-year does not support a general recommendation.
- **Animal work:** ethics approval + **ARRIVE**; housing, diet composition, unit.
- **Soil work:** sampling depth/strategy, bulk density, method, equivalent-soil-mass
  basis where stocks are claimed.
- **Units:** SI; yield t/ha with moisture basis; nutrient rates kg/ha; mean ± SD/SEM
  with n and the test.

## Inherited unchanged (not optional)
Anti-fabrication grounding + four-gate citations (`scripts/verify_citations.py`),
`word-field-codes.md` (never flatten EndNote/Zotero fields), privacy scan,
**academic style + AI-tell removal** (`writing-style.md` with `human-writing.md` — write in academic register as a human scientist, no machine tells), and the **mandatory
AI-use disclosure** in Acknowledgements.
