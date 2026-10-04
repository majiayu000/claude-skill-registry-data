---
name: agri-review
description: "Multi-reviewer peer-review system for agricultural manuscripts. Simulates an editorial panel — a coordinating editor, three domain reviewers (methodology, domain/novelty, integrity/ethics) and a devil's advocate — plus a formatting check against the target journal, all acting as senior agricultural scientists. Same machinery as food-review, including the knowledge_builder that reads the cited sources and key field literature first, grounded in agriculture literature (Q1/Q2 preferred, Q4 avoided) and agricultural standards for field trials, experimental unit and pseudoreplication, animal ethics and soils. Triggers: review my agronomy paper, peer review agricultural manuscript, referee report soil science, critique my crop paper, pre-submission review agriculture, mock review animal science."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  delegates_to: food-review
  related_skills: [agri-paper, agri-research, agri-pipeline, journal-selector, food-review]
  references:
    - ../agri-research/references/agriculture-domain.md
---

# Agri-Review — Peer-Review Panel for Agricultural Science

**Run the `food-review` skill exactly** — its panel (`review_coordinator`,
`knowledge_builder`, `reviewer_methodology`, `reviewer_domain`,
`reviewer_integrity`, `devils_advocate`, `format_checker`), its modes (**full ·
quick · methodology · re-review**), and its report format — with the agriculture
substitutions in
[`agri-research/references/agriculture-domain.md`](../agri-research/references/agriculture-domain.md).
Read that file first. No new machinery here.

## The substitutions
1. **Persona** — every reviewer is a **senior agricultural scientist of the specific
   discipline** (agronomy · soil science · horticulture · dairy & animal science ·
   agricultural engineering · agricultural economics & policy). Name the discipline;
   a soil-carbon paper gets a soil scientist's standards (domain §2).
2. **Knowledge base** — `knowledge_builder` runs first, unchanged in method:
   **Pathway A** reads the manuscript's cited sources in full and audits whether each
   supports its claim; **Pathway B** reads the field's key literature, ranked as
   **Tier 1** Q1/Q2 agriculture ([`journals/_coverage_agriculture.md`](../journals/_coverage_agriculture.md))
   + Nature/Science/Cell/PNAS + Q1/Q2 adjacent disciplines, **Q4 avoided**. Pathway B
   may use **`agri-research`'s `full review`** branch for discovery/screening —
   **knowledge extraction only, no literature-review article** (domain §3).
   Inside `agri-pipeline` with a Stage-1 evidence base: reuse it and top up with
   `agri-research` **quick brief** key reviews, exactly as `food-review` does.
3. **Journal routing** — `format_checker` audits against the journal resolved once by
   `journal-selector` from the agriculture coverage map (domain §4); APA 7.0 default.

## What an agricultural reviewer checks first (domain §5)
- **The experimental unit / pseudoreplication** — subsamples counted as replicates,
  plants scored as units within one plot, animals within one pen. The single most
  common fatal flaw; raise it as **Critical** when present.
- **Field-trial reporting** — site, **season(s)/years**, soil classification,
  cultivar, plot size, design, replication, management, statistical model.
- **Generalisation** — one site-year, one region, or a pot/glasshouse study presented
  as a general agronomic recommendation; missing **G×E**.
- **Animal work** — ethics approval and **ARRIVE**; diet composition; unit (pen vs
  animal).
- **Soil work** — sampling depth, bulk density, equivalent-soil-mass basis for stock
  claims.
- **Economics/policy** — identification strategy; causal language unearned by design.

## Inherited unchanged (not optional)
The report format (`food-review/references/report-format.md`: Parts A/B/C, stable
issue IDs, `Response (type)` taxonomy, **editorial decision — Accept · Minor
Revision · Major Revision · Reject with the decisive reasons**) and its
**Word (`.docx`) deliverable rule — never Markdown**; inside `agri-pipeline` this is
the **single Review & Response Report** that `agri-paper` later fills responses into,
so **no separate reviewer report or response letter is created**. Also inherited:
**editor-query comments placed in the manuscript** for fixes needing the author's
data (`word-review-comments.md`), the AI-writing-tell check (`human-writing.md`), the
privacy scan, and the rule that a source never retrieved is **marked, not
summarized**.
