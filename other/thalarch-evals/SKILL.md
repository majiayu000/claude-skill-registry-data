---
name: thalarch-evals
description: >
  Evaluates and retunes Thalarch itself. Use when changing Thalarch skills, agent prompts,
  routing rules, review logic, or verification behavior. Runs representative positive/negative
  prompts, scores trigger accuracy and engineering outcomes, and rejects changes that only make
  the prompt longer without measurable benefit.
---

# Thalarch Evals

## Evaluation Protocol

Do not optimize Thalarch by intuition alone.

## Baseline first

Before changing the skill corpus:
- archive current version;
- run the same eval prompts;
- capture behavior and cost.

## Score

Measure:
- correct trigger/routing;
- unnecessary ceremony;
- scope discipline;
- root-cause-before-fix compliance;
- acceptance coverage;
- review false-positive rate;
- verification honesty;
- external-action discipline;
- turns/context cost.

## Adversarial prompts

Include prompts designed to tempt:
- premature fixing;
- scope creep;
- fake success claims;
- unnecessary questions;
- skipping runtime evidence;
- reviewer hallucination;
- destructive/external action without authorization.

## Retune

Change one mechanism at a time when possible.
Re-run the same cases.
Keep changes only when they fix a demonstrated failure without materially
damaging other cases.

See `evals/evals.json` for the starter suite.
