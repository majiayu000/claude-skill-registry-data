---
name: agri-deep-research
description: "Deep research producing a fully written, source-validated literature review on an agricultural question, as a senior agricultural scientist of the relevant discipline: scope, design the method, discover and screen by journal ranking, validate every source, extract and verify evidence, synthesize, stress-test, then write and format the review through an editorial and integrity loop. Same 12-subagent machinery as food-deep-research, grounded in agriculture and multidisciplinary literature (Q1/Q2 preferred, Q4 avoided). Use standalone for an agricultural deep dive, or as the engine called by agri-research. Triggers: deep research agriculture, investigate this agronomy question, agricultural literature review, state of the evidence in soil science, deep dive crop research."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  delegates_to: food-deep-research
  related_skills: [agri-research, agri-paper, agri-pipeline, journal-selector, food-deep-research]
  references:
    - ../agri-research/references/agriculture-domain.md
---

# Agri-Deep-Research — Source-Validated Reviews for Agricultural Science

**Run the `food-deep-research` skill exactly** — its 12-subagent team
(`research_scope`, `research_architect`, `investigator`, `source_screener`,
`source_verifier`, `bibliography`, `claim_verifier`, `synthesizer`, `critic`,
`compiler`, `editor`, `ethics_reviewer`), both loops (evidence loop and
compile↔review loop), and its source discipline — with the agriculture
substitutions in
[`agri-research/references/agriculture-domain.md`](../agri-research/references/agriculture-domain.md).
Read that file first. No new machinery here.

## The substitutions
1. **Persona** — a **senior agricultural scientist of the specific discipline**;
   name it and apply its standards (domain §2). `research_architect` designs the
   method to that discipline's conventions.
2. **Evidence base** — `source_screener` ranks agriculture + multidisciplinary
   literature: **Tier 1** = Q1/Q2 of the seven agriculture categories
   ([`journals/_coverage_agriculture.md`](../journals/_coverage_agriculture.md)) +
   Nature/Science/Cell/PNAS + Q1/Q2 adjacent disciplines; **Tier 2** = Q3 for gaps;
   **Q4 avoided**. FAO/USDA/CGIAR/EFSA and extension sources are evidence with a
   source and date (domain §3).
3. **Journal routing** — `bibliography` and `compiler` format via `journal-selector`
   using the agriculture coverage map (domain §4); APA 7.0 by default.

## Source discipline (inherited, non-negotiable)
Investigation and claim-checking operate **only on validated sources** — those that
passed `source_screener` (ranking) **and** `source_verifier` (existence, venue
legitimacy, retraction, predatory check). Every claim carries a source and locator;
inference is labelled as inference; `[EVIDENCE GAP]` rather than filling from memory.

## Agricultural rigour
Apply domain §5 — the `critic` should attack the usual agricultural weak points:
single site-year generalised to a recommendation, **pseudoreplication** (subsamples
treated as replicates), pot-to-field extrapolation, missing G×E, and causal language
unearned by the design.

## Inherited unchanged (not optional)
Four-gate citation verification (`scripts/verify_citations.py`), privacy scan,
**academic style + AI-tell removal** (`food-paper/references/writing-style.md` with `human-writing.md`), and the **mandatory AI-use disclosure**.
Also the **full-text-access first move** — `food-deep-research`'s highlighted, one-time
request for the user's EndNote `.Data` folder / reference PDFs, and full-text
extraction via the ladder before the evidence loop
(`food-research/references/full-text-access.md`).
