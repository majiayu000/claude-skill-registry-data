---
name: design-principles
description: >
  Audit a codebase against well-known software design principles:
  SOLID, DRY, YAGNI, KISS, Law of Demeter, Separation of Concerns,
  Composition over Inheritance, and the code-relevant 12-Factor subset.
  Scores findings by impact and effort, runs adversarial debate on
  contested violations, and generates a prioritized DESIGN_AUDIT.md.
  Use when reviewing code quality beyond what linters catch, assessing
  design health before a refactor, or onboarding to an unfamiliar
  codebase. Can be invoked standalone or delegated from tech-debt.
compatibility: >
  Requires git. Works with any project and language. No external tools
  required — analysis is reasoning-based. Enhanced when the project has
  language-specific tooling for structural analysis.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Design Principles Audit

Audit the codebase against well-known design principles. Produce a
scored DESIGN_AUDIT.md with prioritized remediation actions.

**Core principle:** Investigate, do not pattern-match. Read the actual
code to determine whether a violation is genuine, intentional, or a
false positive. Only flag findings with specific file:line evidence.

## Prerequisite check

```bash
git --version 2>/dev/null && git rev-parse --is-inside-work-tree 2>/dev/null
```

If not in a git repository, warn but proceed — git history will be
unavailable but file analysis still works.

## Step 1: Detect context

Determine language, framework, and paradigm — this governs which
principles apply and how violations manifest:

```bash
ls go.mod package.json pyproject.toml Cargo.toml *.csproj 2>/dev/null
```

Read README.md and CONTEXT.md (if present) for architectural intent.

Determine audit scope from input:

- **Full audit** (default) — entire codebase, excluding `vendor/`,
  `node_modules/`, generated files
- **Module audit** — specific directory or package
- **Delegated mode** — called by tech-debt; focus on changed files
  and surface findings for the scorecard

For language-specific violation patterns per principle, see
`references/principles-guide.md`.

## Step 2: Scan for violations

For each applicable principle, read actual code and identify
violations. Do not grep for keywords — trace call paths and
responsibilities.

### SOLID

- **S — Single Responsibility**: Find files/classes/functions with
  multiple distinct reasons to change. Signals: files > 300 lines
  mixing concerns, functions doing I/O + business logic + formatting.
- **O — Open/Closed**: Find code that requires modification (not
  extension) to add new behavior. Signals: long `switch`/`if-else`
  chains on type tags, no interface/abstraction at extension points.
- **L — Liskov Substitution**: Find subtypes that weaken preconditions,
  strengthen postconditions, or throw unexpected errors. Signals:
  overrides that do nothing, panic on valid input, type assertions
  before use.
- **I — Interface Segregation**: Find broad interfaces forcing
  implementors to satisfy methods they do not use. Signals: interface
  with > 5 methods, stub/no-op implementations.
- **D — Dependency Inversion**: Find high-level modules importing
  concrete low-level types. Signals: direct instantiation of
  dependencies, no interfaces at package boundaries, untestable code.

### DRY

Find logic, structure, or data duplicated in two or more places where
a single abstraction would reduce maintenance risk. Distinguish genuine
duplication from coincidental similarity — two functions that look
alike but evolve independently are not DRY violations.

### YAGNI

Find abstractions, configuration options, or generality added without
a current use case. Signals: unused parameters, dead code paths,
interfaces with one implementation, config keys never read.

### KISS

Find needlessly complex solutions. Signals: indirection that adds no
value, abstractions solving problems the codebase does not have,
multi-layer delegation for simple operations.

### Law of Demeter

Find call chains that expose internal structure: `a.GetB().GetC().Do()`.
Each unit should talk only to its immediate collaborators.

### Separation of Concerns

Find mixed layers: HTTP logic in domain models, SQL in handlers,
presentation in business rules. Trace data flow from entry points.

### Composition over Inheritance

Find deep inheritance hierarchies (> 2 levels), base classes modified
to satisfy subclasses, or tight coupling through inheritance. Note:
in Go and functional languages, flag missing interface usage rather
than inheritance misuse.

### 12-Factor (code-relevant subset)

- **Config**: Hardcoded values that should come from environment
  variables (URLs, credentials, feature flags, thresholds).
- **Logs**: `fmt.Println`, `print()`, or ad-hoc string concatenation
  instead of a structured logging library.
- **Stateless processes**: In-memory state that prevents horizontal
  scaling (package-level mutable globals, local file caching of
  user-specific data).

## Step 3: Score findings

For each finding assign Impact, Effort, and Priority using the
framework in `references/report-template.md`.

- **Impact**: CRITICAL / HIGH / MEDIUM / LOW
- **Effort**: S (< 1 day) / M (1–5 days) / L (1–2 weeks) / XL
- **Priority**: P1 (high impact + low effort) through P4 (low impact,
  any effort)

Score each principle area 0–10 for the summary scorecard.

## Step 4: Adversarial debate

Identify the **top 3** findings with the highest combined Impact ×
Effort score where the violation is genuinely contested (reasonable
engineers could disagree). Skip findings that are clear-cut.

For each debated finding:

- **Red (refactor)**: argues the violation should be fixed. Must
  propose a concrete diff or refactoring approach. Challenges whether
  the current design is justified.
- **Blue (keep)**: argues the current design is correct given context.
  Must cite specific reasons beyond "it works." Points out risks of
  the proposed change.
- **White (verdict)**: evaluates on evidence. Decides: **refactor**,
  **keep**, or **add justification comment**.

### Debate rules

- Red and Blue must cite specific code, not generalities
- Red must propose a concrete change, not just identify the smell
- Blue cannot simply defend status quo without reasoning
- White's verdict is final and must be actioned in the report

## Step 5: Generate DESIGN_AUDIT.md

Write the report using the template in `references/report-template.md`.
Include executive summary, principle scorecard, detailed findings with
evidence, debate verdicts, and prioritized remediation roadmap.

Run markdownlint on the generated file:

```bash
markdownlint DESIGN_AUDIT.md 2>/dev/null || \
  npx markdownlint-cli DESIGN_AUDIT.md 2>/dev/null
```

Fix any issues before presenting.

## Step 6: Present summary

Show the user:

1. Principle scorecard (name, score 0–10, top finding)
2. Overall design health score (sum of principle scores / max)
3. Debate verdicts for contested findings
4. P1 items requiring immediate attention
5. Top 5 remediation priorities with estimated effort
6. Ask which items to address first
