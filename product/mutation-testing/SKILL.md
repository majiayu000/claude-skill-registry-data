---
name: mutation-testing
description: "Mutation testing protocols, evaluating test suite effectiveness, mutant survival analysis, and killing false-positive tests."
---

# Mutation Testing & Test Quality Protocol

Measure the actual defect-detection capability of your test suite beyond simple code coverage metrics.

---

## 1. The Mutation Testing Principle

1. High code coverage can be misleading if assertions are weak or missing.
2. Mutation testing intentionally injects mutants (faults) into production code:
   - Replaces comparison operators
   - Replaces arithmetic operators
   - Inverts boolean conditions
   - Removes function calls or return values
3. If tests still pass when code is mutated, the mutant survives (identifies an untested boundary).
4. If a test fails, the mutant is killed (confirms real assertion coverage).

---

## 2. Surviving Mutant Remediation

1. When a mutant survives, identify the missing edge-case test.
2. Add a targeted test case asserting the specific boundary condition until the mutant is killed.
3. Aim for a Mutation Score Indicator > 80% on mission-critical business logic.
