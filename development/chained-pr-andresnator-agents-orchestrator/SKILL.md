---
name: chained-pr
description: >
  Compatibility contract for splitting oversized work into chained or stacked PR review slices.
  Trigger: A workflow names chained-pr or needs a chained PR strategy for review-size risk.
license: Apache-2.0
metadata:
  author: gentleman-programming
  adapted_by: andresnator
  source: gentleman-programming/gentle-ai
  version: "1.0.0"
  status: in-progress
---

## Contract

Use this skill only when review-size evidence shows a single PR would be hard to review safely. It is a compatibility contract for workflows that name `chained-pr`; keep it aligned with the broader `work-unit-commits` review-splitting guidance when that skill is available.

## Rules

- Split by independently reviewable behavior, migration, or evidence units, not by file type.
- Keep each PR slice small enough to understand, verify, and roll back.
- Preserve test and documentation changes with the code slice they prove or explain.
- Define the base branch of each slice and the dependency order before implementation continues.
- Stop and ask for a human decision when the required ordering, ownership, or size exception is unclear.
- Do not use a chained PR strategy to hide broken tests, missing evidence, or mixed behavior fixes.

## Evidence

Record the chosen strategy, slice order, expected changed files or size, verification required per slice, rollback boundary, and any human-approved size exception.
