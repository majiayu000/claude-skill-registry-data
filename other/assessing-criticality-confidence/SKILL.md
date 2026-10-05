---
name: assessing-criticality-confidence
description: >-
  Guides rating a finding's criticality from its consequence and its confidence from re-validation, and avoiding the
  inflation, conflation, and shortcuts that make both scales useless.
when_to_use: >-
  Use when a checker is about to assign a level to a finding, or when whoever applies findings is rating confidence and
  choosing an order.
compatibility: Requires read access to the content each finding names.
---

# Assessing Criticality and Confidence

[Finding Criticality and Confidence][finding-criticality-and-confidence] owns the levels, the assignment order, the
fixed adjustments, the priority matrix, and the report fields. This skill covers the judgement those rules leave to the
rater: the borderline cases where a correct level is easy to miss.

## Rate the Consequence, Not the Effort

Ask what breaks, for whom, if nobody acts. Ignore how large the fix is.

A one-character mistake in an install command stops every reader who follows it, so it is `CRITICAL`, even though the
repair is trivial. A sweeping reorganization that would read better is `LOW`, even though the work is large. Rating by
effort sorts findings by how pleasant they are to fix, which is the wrong order for a gate.

## Status Is an Observation, Not a Level

Labels such as verified, error, or broken say what was observed. They do not say how much it matters. A contradicted
claim in a passing remark and a contradicted command in a setup step share a status and differ in criticality. A report
keeps both labels, and the consequence decides the level.

## Resist Inflation

Raising a finding's level to get it attention spends the scale. When most findings block, people learn to negotiate with
findings instead of fixing them, and the one that truly blocks looks like the rest. `MEDIUM` and `LOW` are not
dismissals: each still carries a disposition.

## Confidence Belongs to Whoever Applies

A checker's certainty is not confidence. Confidence is rated after re-reading the current state, one finding at a time,
under the re-validation steps the standard sets.

Two traps sit inside that rating:

- **Objective but ambiguous.** A missing field is objective, but when two different values would both satisfy the rule,
  the fix is not unambiguous. That is `MEDIUM`.
- **Nudging to clear the queue.** Moving a `MEDIUM` to `HIGH` because it is probably fine turns a person's decision into
  an unreviewed edit. Leave it flagged.

## A False Positive Needs a Disproof

`FALSE_POSITIVE` means re-validation showed the finding wrong: the problem is absent, the rule does not apply, or the
cited source is outdated. Disagreeing with the rule is not a disproof; that finding is real, and the rule question goes
to its owner. Every false positive names what would stop the checker raising it again.

## Order Protects the Run

Apply by priority, never in the order findings were discovered. A failed `P0` stops the run, because every later fix
would sit on a state still broken. Lower-priority work that needs approval waits for it, however safe it looks.

## Worked Ratings

- **a required metadata field is absent**
  - Criticality: `CRITICAL`
  - Confidence: `HIGH`
  - Why: the artifact fails validation; one correct value
- **a paragraph reads as unclear**
  - Criticality: `MEDIUM`
  - Confidence: `MEDIUM`
  - Why: minor quality issue; any rewrite is a judgement
- **a link reported broken now resolves after a rename**
  - Criticality: `HIGH`
  - Confidence: `FALSE_POSITIVE`
  - Why: re-reading disproves it; the checker's path is stale
- **a version number is reported outdated, citing a registry**
  - Criticality: `HIGH`
  - Confidence: `HIGH`
  - Why: misleading; the cited source settles the value

For writing the report itself, see [Generating Validation Reports](../generating-validation-reports/SKILL.md).

[finding-criticality-and-confidence]:
  ../../../repo-governance/development/quality/evidence/finding-criticality-and-confidence.md
