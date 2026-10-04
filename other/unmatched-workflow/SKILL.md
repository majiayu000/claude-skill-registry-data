---
name: unmatched-workflow
description: >-
  Design a rigorous, auditable playbook when no narrower skill fits: a large
  migration, multi-part change, or work a human will review after stepping away.
  Apply when no playbook matches, the work is a migration, or they will be
  gone while the work runs. Use inception when the deliverable is the plan.
  Use deep-deliberation to choose among options without implementing. Use
  kit-workflows for a known bug-fix, feature, or refactor. Use blinded-eval
  to prove a skill change.
user-invocable: true
disable-model-invocation: true
version: "1.3.0"
author: "Ali Farahat"
tags: ["playbook", "migration", "hypothesis"]
when_to_use: |
  USE WHEN:
  - No narrower BalaKit skill or kit-workflows playbook fits.
  - The work is a large migration or multi-part change with a falsifiable done-check.
  DO NOT USE WHEN:
  - The decision is "which approach" with no implementation (use deep-deliberation).
  - The deliverable is the plan, not the work (use inception).
  - The task is a known bug-fix, feature, or refactor (use kit-workflows).
---

# Unmatched workflow

> **Leading words:** falsifiable done-predicate, hypothesis loop, VERIFIED
> NOT VERIFIED INCONCLUSIVE.

When no playbook fits, the deliverable **before any code** is the workflow:
phases that scale rigor to the task. Inconclusive is not a pass.

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Frame: falsifiable done-predicate, scope, rigor level (one-way doors get more). Present before a long run.
2. Design the workflow: atomic units, riskiest-unknown first, verification harness before features. The first unit that writes code is the harness, not a product edit. Deleting the old API is out of scope unless the Phase 1 predicate names it. Write the phase list down.
3. Run the loop: each unit is an experiment — hypothesis, smallest change, measure on the real artifact, keep or revert.
4. Verify the whole against the Phase 1 predicate on the real product.

## Verdicts

Each unit: **VERIFIED**, **NOT VERIFIED**, or **INCONCLUSIVE**. Do not hide a negative.

Pair delegated work with a parent read of the artifacts. If a worker games the
gate, harden the contract. If the gate is wrong, fix the gate in its own change.

## Reply contract

The playbook you designed, the rigor level and why, what is verified against
the predicate, and what is still open.
