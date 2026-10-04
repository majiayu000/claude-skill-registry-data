---
name: agri-research
description: "Run a comprehensive, multi-source literature and evidence-synthesis workflow for agricultural science, as a senior agricultural scientist of the relevant discipline (agronomy, soil science, horticulture, dairy and animal science, agricultural engineering, or agricultural economics). Same machinery as food-research, but the evidence base is agriculture and multidisciplinary literature ranked by journal quartile: Q1/Q2 agriculture journals plus the Nature, Science, Cell and PNAS families first, Q3 only for gaps, Q4 avoided. Use to research an agricultural topic in depth, do a literature review, build an evidence brief, or scope a systematic review. Triggers: research this agricultural topic, agronomy literature review, soil science evidence synthesis, horticulture review, animal science evidence, crop research, farming systems review, what does the agricultural evidence say."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  delegates_to: food-research
  related_skills: [agri-deep-research, agri-paper, agri-review, agri-pipeline, journal-selector, food-research]
  references:
    - references/agriculture-domain.md
---

# Agri-Research — Evidence Synthesis for Agricultural Science

**Run the `food-research` skill exactly** — its streams, subagents
(`search_strategist`, `source_scout`, `screener_appraiser`, `journal_ranker`,
`synthesis`, `writer`, `reviewer`, and the full `systematic_reviewer` PRISMA/OHAT
pipeline), gates, and output contracts — with the agriculture substitutions in
[`references/agriculture-domain.md`](references/agriculture-domain.md). Read that
file first. This skill adds no new machinery; it changes **who is working, on what
evidence, for which journal**.

## The substitutions
1. **Persona** — a **senior agricultural scientist of the specific discipline**
   (agronomy · soil science · horticulture · dairy & animal science · agricultural
   engineering · agricultural economics & policy · agriculture multidisciplinary).
   Name the discipline and apply its standards (domain §2).
2. **Evidence base** — agriculture + multidisciplinary literature, ranked by
   `journal_ranker`: **Tier 1** = Q1/Q2 of the seven agriculture categories
   ([`journals/_coverage_agriculture.md`](../journals/_coverage_agriculture.md), 230
   journals) + Nature/Science/Cell/PNAS + Q1/Q2 of adjacent disciplines; **Tier 2** =
   Q3 for gaps only; **Q4 avoided**. Authoritative non-journal sources (FAO, USDA,
   CGIAR, EFSA, extension services) count as evidence with a source and date
   (domain §3).
3. **Journal routing** — via `journal-selector`, using the agriculture coverage map
   (domain §4).

## Streams (as `food-research`)
- **quick brief** — fast orientation; Tier 1 only.
- **full review** — the default: four-layer search → two-phase screening → synthesis
  → manuscript → `reviewer` loop → Word `.docx`.
- **deep research** — calls **`agri-deep-research`** (not `food-deep-research`).
- **systematic** — full PRISMA + OHAT pipeline; **inclusion by pre-specified
  eligibility, never journal ranking**.

## Agricultural rigour
Apply domain §5 throughout — field-trial reporting (site, season/years, soil,
cultivar, design, replication), **the experimental unit** (plot/pen, not plant/animal
— pseudoreplication is the classic error), G×E and season-to-season variation, ARRIVE
for animal work, and no extrapolation from pot to field or region to region.

## Inherited unchanged (not optional)
Anti-fabrication grounding and the four-gate citation check
(`scripts/verify_citations.py`), the privacy scan, `journal-selector`'s ask-once
contract, **academic style + AI-tell removal** (`food-paper/references/writing-style.md` with `human-writing.md`), and the **mandatory AI-use
disclosure** in every written output. Also the **full-text-access first move** —
`food-research`'s highlighted, one-time request for the user's EndNote `.Data` folder
/ reference PDFs, and full-text extraction via the ladder before synthesis
(`food-research/references/full-text-access.md`).
