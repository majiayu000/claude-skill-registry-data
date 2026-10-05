---
name: usability-heuristic-evaluation
description: >-
  Guides judging a running interface as a first-time user would, without its specifications: citing a named principle
  for every finding, walking each task step, reading labels and addresses for scent, and rating severity.
when_to_use: >-
  Use when running the spec-blind usability lens of an exploratory and usability review, or when deciding whether a
  usability observation is a finding.
compatibility: Requires a running interface in a real browser, and no access to its specifications, source, or designs.
---

# Usability Heuristic Evaluation

[Exploratory and Usability Review](../../../repo-governance/workflows/quality/exploratory-usability-review.md) owns the
sequence: the frozen tasks, the two lenses in order, structural blindness, passive conduct, and one bounded pass.
Usability Probes and Completeness owns the probes every pass runs, and Accessibility owns the full accessibility audit.
This skill covers the evaluator's judgement inside the usability lens.

## What Counts as Ground Truth

Judge only what a first-time user can perceive: rendered text, labels, layout, affordances, feedback, the address, and
behaviour seen by interacting. Measure it against published usability principles, the interface's own consistency, and
prevailing conventions, which an evaluator may look up. The product's intended behaviour is not ground truth: once
known, first-time comprehension can no longer be judged.

## No Principle, No Finding

"Confusing" is a reaction, not a finding. Every finding names what it violates: one of
[Nielsen's ten usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), a failed walkthrough
question, a recognised interaction law, an ISO 9241-110 interaction principle, or a WCAG 2.2 Understandable criterion.
When no principle is violated, record the observation as a note and move on.

## Breadth, Then Depth

Sweep the whole interface against the heuristic set for breadth. Then, for depth, walk each frozen task step by step and
ask at every step:

1. Will the user try to achieve the right result here?
2. Will the user notice that the correct action is available?
3. Will the user connect that action with the result they want?
4. After acting, will the user see that progress was made?

A "no" or an "unsure" is a finding. Keep the step transcript, so the verdict can be checked.

## Read Like Someone Scanning

Users scan and take the first plausible option. For each key task, decide whether the page makes the right first click
the most compelling target. For every link and menu item, ask whether its label alone predicts where it leads. Look past
polish: attractiveness earns undeserved tolerance, and plainness alone is not a finding.

## States a Demonstration Skips

Probe the empty or zero-result state, loading, errors, first visit against return visit, very long content, and slow or
offline conditions. Find at least one weakness, or state that a genuine attempt found none, since silence reads as
nobody trying.

## Each Size Is Its Own Experience

At each viewport class, judge usability, not only layout: whether a collapsed menu can be found, whether anything
disappears at one size, whether touch targets are reachable, whether reading order survives restacking, and whether one
value agrees across sizes. Where sizes disagree, ask which one a newcomer would trust.

The address is interface too. A usable one reads as words, mirrors the navigation, matches its page, leaks no
implementation detail, lands on a sensible parent when shortened, and follows one pattern across siblings.

## Rate Severity, Not Priority

| Severity | Meaning                                   | Criticality |
| -------- | ----------------------------------------- | ----------- |
| 4        | blocks or badly misleads most users       | `CRITICAL`  |
| 3        | many users struggle; important to fix     | `HIGH`      |
| 2        | some users are slowed or briefly confused | `MEDIUM`    |
| 1        | cosmetic; minimal impact                  | `LOW`       |
| 0        | considered and dismissed                  | no finding  |

Weigh frequency, how hard it is to overcome, and persistence across visits. Priority is the owner's decision, separate
from severity.

A finding also records the task step, viewport, browser and version, locale, date, reproducibility (always, intermittent
with a count, or once), reproduction steps, the expected behaviour its principle grounds, the actual behaviour with
exact label text, and a suggested clarification marked as a hypothesis.

## Suggesting Behaviour

When a newcomer would reasonably expect behaviour the interface lacks, propose it as a scenario only when a cited
principle grounds it, it can be written as Given, When, and Then, and the product rather than a third party owns it.
Mark it spec-blind: a spec-aware reviewer confirms it is not already specified.
[Exploratory Testing](../exploratory-testing/SKILL.md) owns the spec-aware lens and its gaps.
