---
name: mutation-testing
description: Mutation testing methodologies and frameworks (Stryker, Mutmut). Use when evaluating test suite effectiveness, identifying false-positive tests, killing surviving mutants, or auditing code coverage quality beyond raw line metrics.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: testing-unit-tdd
---

# Mutation Testing Expert

> **Test Suite Hardening, Mutant Elimination & True Semantic Coverage**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Coverage Lies, Mutants Don't** | 100% line coverage means nothing if assertions don't verify state changes. Mutation score is the true metric of test quality. |
| **Kill Surviving Mutants** | Every surviving mutant (mutated boolean, flipped comparison, stripped statement) reveals an assertion gap in your test suite. |
| **Incremental Mutation Runs** | Mutation testing is computationally expensive. Run Stryker/Mutmut on changed files or PR diffs (`--incremental`), not the entire monolith. |
| **High Mutation Score Target** | Aim for >80% mutation score on critical business logic, financial calculations, and authentication modules. |

---

## 📋 Stryker Configuration Pattern (`stryker.config.json`)

```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "reporters": ["html", "clear-text", "progress"],
  "testRunner": "vitest",
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.spec.ts",
    "!src/**/*.d.ts",
    "!src/index.ts"
  ],
  "thresholds": {
    "high": 85,
    "low": 70,
    "break": 65
  }
}
```

---

## 📋 How to Kill Common Mutants

1. **Equality Operator Mutator (`===` mutated to `!==`)**:
   - *Cause*: Missing test case checking boundary equality vs inequality.
   - *Fix*: Add dedicated assertion testing the exact equality threshold.
2. **Boolean Literal Mutator (`true` mutated to `false`)**:
   - *Cause*: Mock always returns positive or test does not verify falsy branch.
   - *Fix*: Add test case where predicate evaluates to false and verifies alternative code branch.
3. **Block Statement Mutator (Function body stripped)**:
   - *Cause*: Test calls function but makes no assertions on return value or state side effects.
   - *Fix*: Assert return payload or verify spy interactions with expected parameters.

---

## ❌ Anti-Patterns

- ❌ Relying purely on Istanbul/c8 line coverage metrics without testing assertion strength.
- ❌ Excluding tricky logic from mutation config just to artificially inflate scores.
- ❌ Running un-scoped full-suite mutation tests on every git commit.
