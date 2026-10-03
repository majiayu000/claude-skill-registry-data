---
name: results-writing
description: Write or revise a paper's Experimental Results section using recipes distilled from dissecting top ML researchers' papers. Use when drafting or editing a results section, its tables, figures, or captions, an ablation, or a limitations subsection, or when a results section reads as an undifferentiated scoreboard. Applies the claim-headed paragraph rule, the measurement-over-scoreboard weighting, the named-component lesion, paired-number discipline, and mechanical checklists.
---

# Results section (master method)

Follow `results-guide.md` in this folder, the complete plain-English method.
This file is the operating summary.
## Process

1. **Figures and tables first, captions that state the conclusion.** Build the
   two figures and two tables before the prose and write the section to them.
   Each caption states its finding and decodes every series, readable alone; the
   reading key and each baseline's handicap live in the caption or note, never in
   the prose.
2. **Purpose opener, number-free.** Open by naming the questions the section
   answers, no result in the opener. Each subsection then discharges exactly one
   of those questions.
3. **Bank the setup: declare fairness, disclose compute.** Bank Setup / Systems as
   action-first paragraphs, not a Metrics subsection. Name every rival inline with
   its identity and citation. Declare the comparison's fairness out loud at the
   point of comparison ("one run against one run"), and disclose the compute the
   metric ignores.
4. **Claim-headed findings that land their answer.** Organize by a stable unit
   (benchmark / claim-question), never by metric. Each subsection header is a
   declarative claim; each findings paragraph opens as a claim and lands its answer
   in the last sentence, discharged by a paired number.
5. **Tables sorted by the headline metric.** Order rows by the headline metric,
   hold column order fixed across tables, and define the metric once in prose then
   reuse it by reference.
6. **Named-component lesion for the ablation.** Remove one named component, report
   the drop from→to, and state the verdict as necessity. Isolate one variable where
   the design allows; where you remove a bundle, say so.
7. **The star measurement out-weighs the scoreboard.** The one measurement that
   carries the thesis gets the most weight; anchor it with a per-example drill-down
   narrated in domain terms. The aggregate scoreboard is the setting, not the
   point.
8. **Limitations inside results, terse; then seal.** Keep a short Limitations
   subsection inside Results, each boundary routed to "remain open." Then seal the
   section: no method re-introduction, no new component, no literature survey.
## Core rules

- Every number travels in pairs, before/after, ours/theirs, or fraction-and-
  percent; a naked or unpaired hero number never appears.
- Organize by a stable unit (benchmark / claim-question), never by a standalone
  Metrics / Baselines / Datasets subsection.
- The star measurement, the one that carries the thesis, out-weighs the
  aggregate scoreboard; anchor it with one per-example drill-down.
- The ablation is a lesion mapped to named components; the verdict is stated as
  necessity ("X is necessary for Y").
- Credit the nearest rival warmly, then contrast on exactly one axis; state losses
  plainly; no pejorative anywhere. Your closest rival is your likeliest reviewer.
- Declare fairness out loud at the point of comparison, and disclose the compute
  the metric ignores.
- Captions state the conclusion and decode every series; reading keys and baseline
  handicaps live in the caption or note, not the prose.
- Seal the section: no method re-introduction, no new component, no literature
  survey, those live in other sections.
- Prose axioms: sentences <= ~28 words, subject and verb early, zero
  "can"/"could", no bare This/These, no em dashes, numbers glued to exact objects.
## The insight layer (make it worth reading)

Before writing findings, mine the run artifacts, logs, traces, per-example
outputs, and record each candidate fact with its provenance (file, field,
computation). Then:
- Apply the quotability test: would a reviewer repeat this sentence to a
  colleague? Facts that fail stay in the ledger, not the section.
- Escalate rate -> guarantee -> exhibit: a rate ("92% of actions came from
  validated plans") beats nothing; a guarantee ("every scored action passed the
  check") beats a rate; a concrete exhibit (the one trace that shows it) beats
  both. Report the strongest form the data supports.
- Pick a story shape for the section's arc: mystery (a surprising number,
  then its explanation), objection-kill (name the reviewer's doubt, then the
  experiment that removes it), pivot (the expected story fails, the real one is
  better), honest negative (what did not work, stated plainly), or artifact
  inspection (read the system's own outputs closely).
The rules above make a Results section correct; this layer makes it worth
reading.
## Reference file

- `results-guide.md`: full guide: term translations, the claims-discharged-by-
  numbers skeleton, three results recipes with fill-in templates, the devices
  recipe (purpose opener, claim-stating captions, the lesion ablation, the
  per-example drill-down, number discipline), mechanical checklists including the
  "never in a results section" list, the assembly order, a worked example on a
  toy system, and the insight layer (Part 6).
