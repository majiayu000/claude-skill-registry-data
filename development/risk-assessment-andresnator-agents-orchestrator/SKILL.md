---
name: risk-assessment
description: "Trigger: risk assessment, refactor risk. Classify technical and functional legacy risk."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.1.0"
  status: testing
---

# Risk Assessment
Assess risk from technical and functional evidence.

## Signals

- Complexity and large methods/classes.
- Missing tests or low coverage.
- CRAP score when available.
- Fan-in/fan-out and number of consumers.
- External dependencies.
- Public contracts.
- Async behavior, transactions, persistence, and critical domain rules.
- Git churn when history is available.

Classify overall risk as low, medium, high, or critical and explain why.

## Churn and hot spots

When git history is available (read-only `git log` / `git blame` / `git shortlog`), rank the target's files by change frequency. High churn on a risky unit raises its priority: refactor pays off where change keeps happening. Churn ≈ 0 lowers it — untouched ugly code is zero-interest debt, and refactoring it has ROI near zero unless a planned change is about to land there.

## Business value tier

Depth of investment follows the target's value tier, not only its technical risk: core domain code (differentiating business logic) justifies deep plans; supporting code justifies moderate ones; generic/commodity code is often better replaced than refactored. Infer the tier from evidence (domain language, dependency direction, test intensity) and say explicitly when it cannot be inferred.
