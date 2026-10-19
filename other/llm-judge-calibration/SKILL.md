---
name: llm-judge-calibration
description: "Calibrate LLM judges: rubrics, calibration sets, inter-annotator agreement, drift detection and judge/teacher separation. Use when an agent must build or audit an LLM-as-judge scoring pipeline; not for building a single rubric from scratch. Verified 2026-10-13."
compatibility: Python 3.10+, any LLM API; verified 2026-10-09
license: MIT
---
# LLM Judge Calibration

Trigger: building or auditing an LLM-as-judge scoring pipeline where the judge's
scores must be reliable, reproducible and free of position/order bias.

## Core invariant
A judge score is only evidence if it was produced by a judge that is separated
from the generator, scored against a rubric with per-level examples, and measured
on a calibration set that was never used to tune the rubric. Without all three,
the number is circular.

## Procedure (numbered — follow in order)
1. **Separate judge from teacher** — the judge that scores submissions must not be
   the same model (or same prompt) that generated them. If the judge can see its
   own outputs, agreement is meaningless. Record judge model, generator model and
   both prompt hashes in every report.
2. **Write a rubric before any scoring** — each score point gets a definition and
   at least one example of each level. Score points without examples are
   ambiguous and produce 20+ point spread on re-annotation.
3. **Build a calibration set** — 30-50 items spanning the score range, each with
   a human gold label. Never calibrate on the training set.
4. **Measure agreement** — Fleiss' kappa or Krippendorff's alpha >= 0.6 before
   trusting the judge. Below 0.4 the rubric is not usable.
5. **Check for position/order bias** — shuffle item order between judge runs; if
   a score moves by >0.5 on a 5-point scale when its neighbours change, the judge
   is order-sensitive and scores must be aggregated across shuffles.
6. **Detect drift** — re-run the calibration set weekly; if the mean score moves
   by >0.3 or agreement drops by >0.1, re-calibrate or retire the judge.
7. **Calibrate the pass rate** — the threshold that yields the target pass rate on
   the calibration set is the operating threshold. Never fit it to make a
   specific agent pass.

## Decision tables

### D1 — Agreement threshold
| Agreement | Verdict | Action |
|-----------|---------|--------|
| >= 0.6 | usable | ship the judge |
| 0.4-0.6 | fix the rubric | add per-level examples, re-annotate |
| < 0.4 | unusable | retire or rebuild the rubric |

### D2 — Drift
| Mean shift | Verdict | Action |
|-----------|---------|--------|
| 0-0.2 | stable | keep the judge |
| 0.2-0.3 | watch | re-check next week |
| > 0.3 | drift | re-calibrate or retire |

### D3 — Position bias
| Bias | Verdict | Action |
|------|---------|--------|
| 0-0.3 | acceptable | ship |
| > 0.5 | order-sensitive | aggregate scores across shuffles |

### D4 — Judge/teacher separation
| Setup | Verdict |
|-------|---------|
| same model + same prompt | fail - agreement is circular |
| different model or different prompt | acceptable |
| different model | preferred |

## Near-miss triggers (stop and re-check before proceeding)
- Judge and generator are the same model -> agreement is circular.
- A calibration report with no provenance fields -> the score is not
  auditable; re-run with --judge-model, --generator-model and both prompt
  hashes.
- Rubric has no per-level examples -> ambiguous, low agreement.
- Calibration set is the training set -> overfit, does not transfer.
- Agreement measured on a set the rubric was tuned on -> inflated.
- A score moves when neighbours change -> position bias present.
- Drift >0.3 or agreement drops >0.1 since last week -> re-calibrate.

## Pitfalls from research
- P1: Same-model judging of same-model outputs produces circular agreement.
- P2: Rubrics without per-level examples cause annotator spread.
- P3: Calibrating on the training set inflates agreement and does not transfer.
- P4: Position/order bias is common in LLM judges; always shuffle.
- P5: Drift is real; a judge calibrated in March may not be valid in June.
- P6: A rubric with only a definition and no examples reads as identical to a
  5-point scale and collapses onto the middle point.

## Verification checklist
- [ ] Judge and teacher are separated (different model or prompt).
- [ ] Rubric has per-level definitions and examples.
- [ ] Calibration set has 30-50 items with gold labels.
- [ ] Agreement >= 0.6 measured on a held-out set.
- [ ] Position bias < 0.5 or scores aggregated across shuffles.
- [ ] Drift check scheduled weekly with thresholds recorded.
- [ ] Pass-rate threshold derived from the calibration set, not the training set.
- [ ] Judge model, generator model and prompt hashes recorded in the report.
- [ ] The report carries all four provenance fields; a report missing any of
  them is not auditable and `scripts/calibrate_judge.py` rejects it.
- [ ] The calibration set has 30-50 items, every item has a gold label, and it
  spans at least 2 distinct scores or the script rejects it before measuring
  agreement.
- [ ] The baseline covers the same items as the current set (id alignment) or
  drift is not comparable.
- [ ] Judge and generator are not the same model with the same prompt.

## Worked examples

### Good — separated judge, calibrated threshold
Generator: `gpt-4.1` produces 100 summaries. Judge: `claude-sonnet-4` scores
them on a 4-point rubric with per-level examples. Calibration set of 40
items with human gold labels gives agreement 0.71 and a pass threshold of
>=3. The threshold is recorded with the date and the judge/generator hashes.

Result: the score is evidence, not a self-fulfilling prophecy.

### Bad — same model judges its own outputs
`gpt-4.1` generates the summaries and `gpt-4.1` scores them.

Why it fails: agreement is circular — the judge agrees with itself by
construction. The skill rule is separation: different model, or at minimum
a different prompt. Record both hashes in the report or the score is
unverifiable.

### Bad — rubric with definitions only, no examples
"1 = poor, 2 = fair, 3 = good, 4 = excellent."

Why it fails: without per-level examples annotators spread 20+ points on
re-annotation and the rubric collapses onto the middle. Every score point
needs a definition AND at least one example.
## Related skills
- [deep-research-method](../deep-research-method/SKILL.md)
- [verifiable-environments](../verifiable-environments/SKILL.md) — a judge's calibration harness is itself a verifier: the rubric is the spec, the bypass register is the audit, and the pass-rate table is the calibration.
- [skill-authoring-evals](../skill-authoring-evals/SKILL.md) — the gold labels and rubric used to score sources are evidence products: cite them, score them, state confidence.

## References
- procedures: references/procedures.md
- calibration protocol: references/calibration-protocol.md
- rubric template: references/rubric-template.md
- rubric lint: references/rubric-lint.md
- robustness: references/robustness.md
- incidents: references/incidents.md
- DESIGN: references/DESIGN.md
- EVALS: references/EVALS.md
- SOURCES: references/SOURCES.md

## Provenance gate
Every calibration report must record the judge model, the generator model and
the hash of both prompts. A score with no provenance cannot be reproduced or
audited, so `scripts/calibrate_judge.py calibrate` requires all four fields
and rejects a report where judge and generator are the same model with the
same prompt. Decision table: same model + same prompt = fail; different model
or different prompt = acceptable; different model = preferred.
