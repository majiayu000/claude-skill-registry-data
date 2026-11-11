---
name: bias-analysis
description: "Use when comparing options with field reports, reviews, forum threads, surveys, reliability statistics, benchmarks, or user feedback, when writing a comparative study, or when asked whether X is more reliable, faster, or better than Y. Also use when a study needs a bias analysis section, or when the user questions whether the evidence is biased."
---

# Bias Analysis

## When to use
- User compares options (products, tools, vendors, engines, libraries) from field evidence
- A study cites forums, reviews, surveys, breakdown statistics, or benchmarks
- User asks "is X more reliable than Y" or "why does everyone say X is better"
- A comparative document needs a bias section, or an existing one looks ad hoc

## Overview

Field evidence carries systematic distortions. Name them, test them, and correct
the conclusion; never just list them. Every verdict on a bias needs evidence, like
any other claim: the [`evidence-based-analysis`](../evidence-based-analysis/SKILL.md)
skill owns citation rules.

Reference: [biases.md](biases.md). Sweep the full checklist; never pick biases
from memory.

## Workflow

1. Inventory the sources. Tag each one: fleet statistic, survey, forum anecdote,
   vendor claim, professional test. The tag sets its weight.
2. Sweep the checklist in [biases.md](biases.md) against **every** option, not only
   the favourite. A bias analysis that only weakens one side is itself biased.
3. For each candidate bias, record four fields: mechanism, direction (which option
   it inflates), evidence for or against, magnitude (weak, moderate, strong).
4. Give a verdict per bias: confirmed, plausible, or rejected. Confirmed requires
   cited evidence, not a plausible mechanism. A mechanism alone caps at plausible.
5. Separate genuine causal advantages from perception effects. List them per
   option under "real advantages, not biases". This prevents over-correction.
6. Re-state the comparison after correction. Say which claims survive, which
   flip, and which stay undecidable. A closing line must follow from the table,
   never from hand-waving.

## Verdict table

One row per bias, all four fields filled:

| Bias | Mechanism | Direction | Evidence | Magnitude | Verdict |
|---|---|---|---|---|---|
| Survivorship | High-mileage survivors visible, failures scrapped | Inflates X | Forum failure at 124k cited | Moderate | Confirmed |
| Volume | Bigger fleet, more absolute reports | Deflates Y | No fleet-size data found | — | Plausible |

Not: "Volume bias: X has a bigger fleet, so more reported failures. **Confirmed.**"
Yes: "Volume bias: plausible — the mechanism holds but no fleet-size figures found; failure counts stay uncorrected."

## Symmetry check

Before closing, ask once per option: which biases inflate **this** one? Common
misses: cheaper repairs get fixed instead of reported; the study language
over-represents a local brand; enthusiast forums self-select complainers on
every side; the newer option has less time to fail.

## Boundaries

This skill weighs external evidence: reviews, statistics, reports. Claims about
code stay with [`evidence-based-analysis`](../evidence-based-analysis/SKILL.md).
It never rejects evidence because a bias exists; it grades how much the bias
moves the conclusion.
