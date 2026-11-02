---
name: skill-routing-evaluation
description: "Measures whether realistic prompts select the intended skills and reveals adjacent candidates that are confused or over-triggered."
---

# Skill Routing Evaluation

## Purpose

Measures whether realistic prompts select the intended skills and reveals adjacent candidates that are confused or over-triggered.

## When to use

A candidate batch passed structural checks but still needs discoverability evidence.

## Required inputs

Canonical IDs, descriptions, representative prompts, expected routes, and any available evaluation harness.

## Workflow

1. Build a prompt set from observed user tasks with natural variants, sparse inputs, and incomplete requests.
2. Assign expected canonical IDs with written rationale; add negatives for similar existing skills and unrelated domains.
3. Run the local routing/evaluation harness if configured; capture command, version, configuration, output, and errors.
4. Report precision/recall or comparable metrics when supported; include false-positive/false-negative examples.
5. If no evaluator exists, publish the evaluation plan and mark routing as unmeasured.

## Validation checklist

Results are reproducible or explicitly unmeasured; negative routing is evaluated rather than assumed.
- [ ] Source revision, paths, and authorized scope are recorded.
- [ ] Every material claim has a source reference or explicit uncertainty label.
- [ ] At least one neighboring/negative case has been checked.
- [ ] Validation describes what actually ran and does not treat a plan as a pass.

## Required output

Evaluation dataset, label rationale, metrics/results or plan-only status, confusion pairs, and prioritized description changes.

## Boundaries and failure handling

Do not send confidential prompts to third parties without approval or manipulate metrics to make a batch appear ready.
If source access, evidence, permissions, or provenance is insufficient, stop and return blockers rather than inventing details. Preserve originals and seek human review for ambiguous licensing or semantic boundaries.

## Trigger examples

- **Positive:** Evaluate whether users can find the right skill and show false positives against neighbors.
- **Negative:** Claim perfect routing from descriptions alone without a measured test.
