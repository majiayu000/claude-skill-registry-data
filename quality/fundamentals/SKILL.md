---
id: quality.fundamentals
name: Quality Fundamentals
description: >
  Coordinates quality work across ESLint, SonarQube, dead-code cleanup, and technical debt so agents can choose the right quality primitive for the codebase and the risk profile.
stack:
  - JavaScript
  - TypeScript
category: quality
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - quality fundamentals
  - quality learning path
  - code quality roadmap
  - quality primitives
  - quality capability path
  - debt and lint coordination
compatibility:
  runtime:
    browser: true
    node: true
---

# Quality Fundamentals

## Purpose

Use this skill to coordinate quality work across ESLint, SonarQube, dead-code cleanup, and technical debt.

This is a mother skill. It does not replace specialized quality skills. It tells an agent which quality primitive to use, in what order to apply it, and when the work should stay as a debt hop instead of becoming a broad refactor.

The core rule is simple:

```txt
Pick the quality primitive that matches the risk, the codebase, and the scope of the hop.
```

## When to Use

Use this skill when:

- a team needs a quality improvement path
- lint, Sonar, and debt cleanup need coordination
- a review needs to stay small and measurable
- a cleanup pass should be sequenced instead of mixed

## Do

Use a sequencing policy:

```txt
lint baseline -> disable governance -> safe autofix -> dead-code cleanup -> Sonar triage -> debt ledger
```

Keep the specialist skills separate:

```txt
eslint -> rules, disables, and safe autofix
no-dead-code -> dead exports, orphan files, dead branches
sonarqube -> gate triage, complexity, duplication, coverage
technical-debt -> hop-based debt tracking
```

Use runtime variants only when the guidance changes materially.

## Do Not

Avoid turning the mother skill into implementation guidance.

Avoid mixing lint, dead code, Sonar, and debt cleanup without a policy.

Avoid using this skill to replace the specialized skills.

## Review Checklist

- [ ] The team has a sequencing policy.
- [ ] Specialized skills remain separate.
- [ ] The cleanup hop stays bounded.
- [ ] The adoption path matches team maturity.
- [ ] The skill is used as routing and coordination, not implementation detail.

## Expected Output

1. Recommend the right quality primitive sequence.
2. Route to the specialized skills.
3. Keep the scope at architecture and cleanup-path level.
4. Preserve the debt ledger.
5. Summarize the quality improvement plan.
