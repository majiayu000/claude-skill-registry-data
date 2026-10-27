---
name: code-refactoring
description: "Martin Fowler refactoring catalog, cyclomatic complexity reduction, boy scout rule, and backward-compatible deprecation paths."
---

# Code Refactoring & Complexity Reduction Protocol

Systematically clean, simplify, and modularize code without altering external behavior.

---

## 1. The Boy Scout Rule & Small Steps

1. Leave the codebase cleaner than you found it.
2. Never perform massive, sweeping refactors and feature changes in the same commit.
3. Verify test coverage BEFORE refactoring. Run the test suite after every micro-step.

---

## 2. Common Refactoring Patterns

- **Extract Function**: Break 50+ line methods into small single-responsibility functions.
- **Replace Conditional with Guard Clauses**: Eliminate nested if/else pyramids by returning early.
- **Introduce Parameter Object**: Replace functions taking 5+ primitive arguments with a structured config/DTO object.
- **Decompose Conditional**: Replace complex boolean expressions with clearly named explanatory variables.
