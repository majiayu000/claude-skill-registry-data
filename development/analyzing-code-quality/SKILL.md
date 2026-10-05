---
name: analyzing-code-quality
description: Use when evaluating code health, finding bug hotspots, identifying anti-patterns, preparing a quality improvement plan, or assessing technical debt
---

## Announce at start: "Using codebase-analyzer to analyze code quality."

## Overview

Identify quality patterns, anti-patterns, complexity hotspots, and risk areas that make code hard to maintain.

## Process

1. Find hotspots: files changed most frequently via git log
2. Detect anti-patterns: god classes, long methods, deep nesting, feature envy (see references/anti-pattern-catalog.md)
3. Check error handling consistency
4. Assess naming conventions and readability
5. Estimate test coverage indicators (test-to-source ratio, test file presence)
6. Find complexity hotspots (deep nesting, long functions)

## Quick Reference

| Anti-Pattern | Detection | Risk |
|-------------|-----------|------|
| God class | >500 lines, >15 methods | High |
| Long method | >50 lines | Medium |
| Deep nesting | >4 levels of if/for | High |
| Feature envy | Method uses another class more than its own | Medium |
| Duplicated code | Similar blocks in 3+ files | Medium |
| Missing error handling | try/catch absent around IO | High |

## Trigger Signals

- **HIGH confidence**: Code generation artifacts (header comments, generated markers) -> `trace-codebase-provenance`
- **HIGH confidence**: Build-time code injection patterns -> `analyze-build-pipeline`
- **MEDIUM confidence**: High churn files with complex logic -> refactoring priority
- **LOW confidence**: Normal quality patterns -> no deep dive needed

## Quality-Churn Correlation

A file that changes frequently AND has high complexity is a bug factory. A file that changes frequently but is simple is just a configuration hub. The CORRELATION is the insight, not the individual metrics. Use `git log --format='%H' --name-only` to find high-churn files, then cross-reference with complexity. For churn analysis commands, see `_shared/references/git-archaeology-techniques.md`.

## Quality Gradients

Code quality degrades from edges inward. Entry points and API handlers are polished. Internal services and data access layers accumulate debt. Check the gradient to find where debt hides. A codebase that is clean at the edges but rotten in the middle has a steeper remediation curve than one with uniform moderate quality.

## SECURITY_SIGNAL

High churn in auth/security files = unstable security posture. Complexity in data handling = injection risk. Missing error handling in financial calculations = correctness risk. These correlations are not theoretical -- they predict where the next incident originates.

## Adversarial Lens

Poor code quality in specific areas may be intentional. A deliberately complex function that could be simple may be obfuscating behavior. Check: is the complexity accidental (incompetence) or deliberate (obfuscation)? Consistent patterns of poor quality in ONE area suggest intent.

## Red Flags

- Only measuring line counts without checking complexity
- Not distinguishing between intentional complexity (algorithms) and accidental
- Missing test coverage indicators
- Ignoring churn-complexity correlation (the single strongest bug predictor)

## Output Contract

Write `docs/analysis/code-quality.md` using standard contract.
Include: hotspot list, anti-pattern findings, quality score assessment, priority recommendations.
