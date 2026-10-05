---
name: measurement-critic
description: Review measurement instruments and results — LLM-as-instrument content scoring AND hand-tuned composite/weighted scoring functions — for validity, reliability, bias, Goodhart exposure, and calibration adequacy
triggers:
  - review measurement
  - measurement quality
  - validate scores
  - measurement validity
  - inter-rater reliability
  - composite score
  - weighted scorer
  - scoring function
  - ranking function
  - is this score a valid proxy
version: 1.1.0
---

# Measurement Critic

## When to Use
Use when you need an evidence-backed validity review of a measurement. Two modes (the critic auto-selects in Phase 0):

- **LLM-instrument mode** — a measurement instrument design (from content-measurement-planner), measurement results (from content-measurement-executor), or both. Best for catching construct validity gaps, reliability issues, and bias before acting on LLM-scored results.
- **Composite-scorer mode** — a hand-tuned weighted/composite scoring function used to rank or filter candidates in a search space (rules, designs, configs). Best for catching invalid component proxies, arbitrary weighting, and **Goodhart exposure when a search process optimizes against the score**.

## What It Does
First selects the measurement mode (Phase 0), then runs only the phases that apply:

**LLM-instrument mode:**
- **Instrument validity** — construct, face, content, discriminant validity
- **Reliability** — inter-rater, internal consistency, test-retest, precision
- **Bias detection** — position, length, anchoring, style, demographic
- **Calibration verification** — adequacy, drift, representativeness

**Composite-scorer mode:**
- **Instrument validity** — does the formula's output track the stated goal?
- **Composite scorer review** — component proxy validity, weighting justification + sensitivity, Goodhart-under-search (with a concrete adversarial candidate), falsifiability + a specific validation experiment, weight-tuning provenance

## Invocation
```
/measurement-critic
```

## Input
Provide any of:
1. Measurement instrument design (content-measurement-planner output) — *LLM-instrument mode*
2. Measurement execution results (content-measurement-executor output) — *LLM-instrument mode*
3. A composite/weighted scoring function plus its stated goal — the formula, its component terms and weights, and how it is used (e.g., to rank candidates in a search space) — *composite-scorer mode*

## Output
- Measurement mode line (which family was reviewed)
- Validity assessment table (both modes)
- *LLM-instrument mode:* reliability metrics with thresholds, bias detection results, calibration verification
- *Composite-scorer mode:* component proxy validity, weighting justification + sensitivity, a concrete Goodhart-under-search adversarial candidate, a specific falsifying validation experiment, weight-tuning provenance
- Multi-perspective findings (methodologist, statistician, domain expert, skeptic)
- Severity-rated findings with evidence
- Verdict: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT

## Companion Skills
- **content-measurement-planner** — when REVISE/REJECT in LLM-instrument mode, route back for instrument redesign
- **content-measurement-executor** — produces the measurement results this critic reviews
- *Composite-scorer mode has no companion planner — it reviews hand-authored scoring functions directly. For redesign, the findings hand back to whoever owns the formula.*
