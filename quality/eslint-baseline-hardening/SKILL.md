---
id: quality.eslint.eslint-baseline-hardening
name: ESLint Baseline Hardening
description: >
  Raises ESLint quality in bounded steps by reviewing current rules, warnings, TypeScript and framework-specific checks, and CI integration without turning the repo into a massive lint refactor.
stack:
  - JavaScript
  - TypeScript
category: eslint
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - eslint baseline hardening
  - lint baseline
  - eslint quality gate
  - lint warnings
  - lint config review
  - rule hardening
compatibility:
  runtime:
    browser: true
    node: true
---

# ESLint Baseline Hardening

## Purpose

Use this skill to harden ESLint in small, safe steps.

The goal is to improve the lint baseline without causing a repo-wide breakage or mixing lint cleanup with unrelated refactors.

The core rule is simple:

```txt
Raise the standard in phases.
```

## When to Use

Use this skill when:

- the repo has too many warnings ignored
- lint rules need a phased rollout
- CI should enforce a stronger baseline
- TypeScript or framework-specific linting needs review

## Do

Review:

- active rules
- disabled rules
- warnings versus errors
- TypeScript rules
- framework-specific rules
- CI integration

Change the baseline in bounded increments and validate each step.

## Do Not

Avoid broad lint churn without a plan.

Avoid changing rules and formatting and logic in the same hop.

Avoid forcing a strict baseline before the repo is ready.

## Review Checklist

- [ ] Current lint state is understood.
- [ ] Errors and warnings are classified.
- [ ] CI integration is considered.
- [ ] The change is bounded and safe.

## Expected Output

1. Inspect the lint baseline.
2. Classify rule gaps.
3. Propose phased hardening.
4. Keep the change bounded.
5. Validate with the project checks.
