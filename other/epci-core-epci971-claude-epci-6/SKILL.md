---
name: epci-core
description: >-
  Fundamental concepts of the EPCI workflow. Defines phases (Explore, Plan,
  Code, Inspect), complexity categories, Feature Document and breakpoints.
  Use when: any EPCI workflow, understanding the methodology.
  Not for: component creation (use /epci:create).
---

# EPCI Core

## Overview

EPCI (Explore → Plan → Code → Inspect) is a structured development methodology
with validation at each phase.

## The 4 Phases

| Phase | Objective | Output |
|-------|-----------|--------|
| **Explore** | Understand needs and existing code | Functional brief |
| **Plan** | Design the solution | Implementation plan |
| **Code** | Implement with tests | Code + tests |
| **Inspect** | Validate and finalize | PR ready |

## Complexity Categories

| Category | Files | LOC | Risk | Workflow |
|----------|-------|-----|------|----------|
| TINY | 1 | <50 | None | /quick |
| SMALL | 2-3 | <200 | Low | /quick |
| STANDARD | 4-10 | <1000 | Medium | /epci |
| LARGE | 10+ | 1000+ | High | /epci |

## Feature Document

Central traceability document for each STANDARD/LARGE feature.

### Structure (v4.0)

```markdown
# Feature Document — [ID]

## §1 — Functional Brief
[Context, acceptance criteria, constraints, Memory Summary]

## §2 — Implementation Plan
[Tasks, files, risks, @plan-validator verdict]

## §3 — Implementation & Finalization
[Progress, tests, reviews, commit, documentation, PR]
```

> **Note (v4.0):** §3 et §4 fusionnés en une seule section pour simplifier le suivi.

### Location

```
docs/features/<feature-slug>.md
```

## Breakpoints

Mandatory synchronization points:

| Breakpoint | After | Pass Condition |
|------------|-------|----------------|
| BP1 | Phase 1 | Plan validated by @plan-validator |
| BP2 | Phase 2 | Code reviewed by @code-reviewer |

### Enriched Breakpoint Format (v3.1+)

Breakpoints display a decision dashboard with:

| Section | Content | Source |
|---------|---------|--------|
| **Métriques** | Complexity, files, time, risk | Scoring algorithm |
| **Validations** | Agent verdicts, skills loaded | Subagents |
| **Preview** | Next phase tasks (3-5) | Plan §2 |
| **Liens** | Feature Document path | File system |
| **Options** | Interactive choices | Text instructions |

See `breakpoint-metrics` skill for scoring algorithm and templates.

## EPCI Subagents

| Subagent | Role | Phase |
|----------|------|-------|
| @plan-validator | Validates technical plan | Phase 1 → BP1 |
| @code-reviewer | Code quality review | Phase 2 → BP2 |
| @security-auditor | OWASP security audit | Phase 2 (conditional) |
| @qa-reviewer | Test review | Phase 2 (conditional) |
| @doc-generator | Generates documentation | Phase 3 |

## Routing

```
User brief
    │
    ▼
/brief (evaluation)
    │
    ├─► TINY/SMALL ──► /quick
    │
    ├─► STANDARD ────► /epci
    │
    └─► LARGE ───────► /epci --large
```

## EPCI Principles

1. **Traceability** — Everything is documented in the Feature Document
2. **Validation** — Each phase has an exit gate
3. **Iteration** — Phases can be revisited if needed
4. **Adaptation** — Workflow adapts to complexity
5. **Automation** — Subagents automate reviews
