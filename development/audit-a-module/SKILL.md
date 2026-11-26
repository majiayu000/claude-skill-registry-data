---
name: audit-a-module
description: "Health check one module or service and recommend what to do with it: leave it, clean it up, refactor it with care, or don't touch it without a senior. Covers what it does, who depends on it, risk, test coverage, churn and rule breaks. Use when the user says \"audit this module\", \"is it safe to refactor X\", \"how healthy is this service\" or \"should we rewrite X\"."
---

# Audit a module

## 1. Gather, in parallel where you can
- **Purpose:** what it does in two sentences, from its code, README and callers.
- **Shape:** size, public surface, what it imports, what imports it (use `blast-radius` for the full list and score).
- **Tests:** which tests cover it, whether they test behaviour, and roughly what share of its public surface is covered.
- **History:** churn over 90 days, bug-fix commits (`git log --grep -i fix`), how many people touch it.
- **Rules:** any architecture rule it breaks (`stay-in-the-lines`), and any danger zone in `CODEBASE.md`.
- **Smells:** cycles, dead exports, copy-pasted logic, files over 500 lines, functions with deep nesting.

## 2. Report on one screen
| | |
|---|---|
| What it does | … |
| Risk | score and band from `blast-radius` |
| Dependents | count, and which cross a boundary |
| Tests | covered / thin / none |
| Churn | commits and fixes in 90 days |
| Breaks rules | … |

Then a **recommendation**: leave it / clean up / refactor with care / senior sign-off first. Give the three changes that would help most, in order, each with its risk.

## 3. If tests are thin and risk is high
Offer `tests-for-old-code` before any refactor. Show the plan first; don't write tests unasked.

Never recommend a rewrite without the dependent count and a path that keeps it working the whole way.
