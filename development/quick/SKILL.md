---
name: epci:quick
description: >-
  Fast implementation for TINY and SMALL tasks. Single-phase execution
  with TDD Red-Green cycle (skip Refactor). Detects native Claude Code plans
  from @plan-path to skip E-P phases. Auto-detects stack skills (Django, React,
  Spring, Symfony, Tailwind) for context. Updates index.json with summary.
  Use when: quick fix needed, small change, tiny feature, fast implementation.
  Triggers: quick fix, small change, tiny feature, bug fix, rapid code.
  Not for: STANDARD features (use /implement), debugging (use /debug).
user-invocable: true
argument-hint: "<task> | @<plan-path>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# Quick

Fast implementation for TINY and SMALL tasks with TDD Red-Green cycle.

## Quick Start

```
/quick "fix the login button alignment"
/quick "add validation to email field"
/quick @.claude/plans/fix-auth.md
```

## Input Detection

```
INPUT
├── @plan-path provided → PLAN-FIRST workflow
│   ├─ .claude/plans/*.md → Native Claude Code plan
│   ├─ docs/plans/*.md → Alternative plan location
│   └─ Skip STEP-01 and STEP-02 → Go to STEP-03 (Code)
│
└── Text description → FULL workflow
    └─ Execute STEP-01 (Mini-Explore) + STEP-02 (Mini-Plan)
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER execute on STANDARD/LARGE complexity (suggest /implement)
- 🔴 NEVER skip TDD cycle (Red-Green-Verify required)
- 🔴 NEVER skip MEMORY phase (index.json must be updated)
- 🔴 NEVER call EnterPlanMode during skill execution
- ✅ ALWAYS start with step-00-detect.md
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS detect stack skills at initialization
- ✅ ALWAYS invoke @implementer for CODE phase
- ⛔ FORBIDDEN skipping tests even for TINY tasks
- 🔵 YOU ARE A FAST BUT DISCIPLINED IMPLEMENTER

## EXECUTION PROTOCOLS:

1. **Load** step-00-detect.md
2. **Execute** current step protocols completely
3. **Proceed** to next_step or conditional_next
4. **Complete** until step-05-memory.md

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUICK WORKFLOW (TINY/SMALL)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 00: DETECT                                                 │
│  ├─ Parse input (plan vs text)                                   │
│  ├─ Auto-detect stack skills                                     │
│  └─ Validate complexity (TINY/SMALL only)                        │
│     └─ If STANDARD+ → Suggest /implement                         │
│                                                                  │
│  Step 01: MINI-EXPLORE [E] (skip if @plan)                       │
│  └─ Quick codebase scan (~5-10s)                                 │
│                                                                  │
│  Step 02: MINI-PLAN [P] (skip if @plan)                          │
│  └─ Generate minimal implementation plan                         │
│                                                                  │
│  Step 03: CODE [C]                                               │
│  ├─ Invoke @implementer (Sonnet model)                           │
│  ├─ TDD: RED → GREEN → VERIFY                                    │
│  └─ (REFACTOR: SKIP for speed)                                   │
│                                                                  │
│  Step 04: DOCUMENT [D] (conditional)                             │
│  └─ Update CHANGELOG/README if visible feature                   │
│                                                                  │
│  Step 05: MEMORY [M]                                             │
│  └─ Update index.json with summary                               │
│     └─ BREAKPOINT: Completion summary                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Steps

| Step | Name | Phase | Description | Skippable |
|------|------|-------|-------------|-----------|
| 00 | detect | - | Parse input, detect stack, validate complexity | No |
| 01 | mini-explore | [E] | Quick codebase scan | Yes (if @plan) |
| 02 | mini-plan | [P] | Minimal planning | Yes (if @plan) |
| 03 | code | [C] | TDD Red-Green via @implementer | No |
| 04 | document | [D] | Update docs if needed | Conditional |
| 05 | memory | [M] | Update index.json | No |

## Complexity Limits

| Category | Files | LOC | Duration | Action |
|----------|-------|-----|----------|--------|
| TINY | 1 | < 50 | < 30s | Execute |
| SMALL | 2-3 | < 200 | < 90s | Execute |
| STANDARD | 4+ | 200+ | - | Suggest /implement |
| LARGE | 5+ | 500+ | - | Suggest /implement |

## Comparison: /quick vs /implement

| Aspect | /quick | /implement |
|--------|--------|------------|
| **Input** | @plan-path or text | feature-slug + @spec/@plan |
| **Phases** | E-P (skippable) + C-T-D-M | E-P-C-I-M (full) |
| **Breakpoints** | 1 (completion only) | 3+ (phase transitions) |
| **Feature Doc** | No | Yes |
| **Code Review** | Skip | Full @code-reviewer |
| **Security Audit** | Skip | Conditional |
| **Subagents** | @implementer only | @implementer + reviewers |
| **Complexity** | TINY, SMALL | STANDARD, LARGE |
| **TDD Mode** | Red-Green (skip Refactor) | Full Red-Green-Refactor |

## Step Files

- [steps/step-00-detect.md](steps/step-00-detect.md) — Input detection + stack
- [steps/step-01-mini-explore.md](steps/step-01-mini-explore.md) — Mini exploration
- [steps/step-02-mini-plan.md](steps/step-02-mini-plan.md) — Mini planning
- [steps/step-03-code.md](steps/step-03-code.md) — TDD implementation
- [steps/step-04-document.md](steps/step-04-document.md) — Documentation update
- [steps/step-05-memory.md](steps/step-05-memory.md) — Memory update

## Reference Files

- [references/plan-structure.md](references/plan-structure.md) — Native plan format
- [references/stack-detection.md](references/stack-detection.md) — Stack detection algorithm
- [references/tdd-rules.md](references/tdd-rules.md) — TDD Red-Green cycle
- [references/breakpoint-formats.md](references/breakpoint-formats.md) — ASCII box templates for breakpoints

## Shared Components Used

- `epci:state-manager` — Track progress, update index.json
- `epci:complexity-calculator` — Validate scope, routing
- `epci:tdd-enforcer` — TDD cycle enforcement (Red-Green mode)
- `epci:breakpoint-system` — Interactive breakpoints (SMALL complexity only)
- `epci:project-memory` — Context persistence

## Breakpoints

This skill uses `epci:breakpoint-system` at key decision points (SMALL complexity only).

| Step | Type | Purpose | Condition |
|------|------|---------|-----------|
| step-01-mini-explore | `validation` | Complexity re-evaluation alert | If complexity appears STANDARD+ |
| step-03-code | `diagnostic` | TDD failure handling | If tests fail 2x |

TINY tasks skip breakpoints for speed. All breakpoints MUST use `@skill:epci:breakpoint-system` invocation format.

## Stack Skills (Auto-detected)

| Stack | Trigger Files | Provides |
|-------|---------------|----------|
| `python-django` | manage.py, django in deps | Django patterns, pytest |
| `javascript-react` | react in package.json | React patterns, Jest |
| `java-springboot` | spring-boot in pom/gradle | Spring patterns, JUnit |
| `php-symfony` | symfony in composer.json | Symfony patterns, PHPUnit |
| `frontend-editor` | tailwind.config.* | Tailwind patterns, a11y |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Complexity > SMALL | Task too large | Suggest /implement |
| Plan not found | @path invalid | Check file path |
| TDD fails 2x | Code won't pass tests | Escalate or investigate |
| Stack not detected | No signature match | Continue without stack skill |

## INVOCATION PROTOCOL (CRITICAL)

Les syntaxes `@skill:epci:xxx` et `@agent:xxx` dans les step files sont **DOCUMENTAIRES SEULEMENT**.
Claude interprète les blocs de code comme des exemples, pas comme des instructions d'exécution.

**Pour invoquer réellement:**

| Type | Syntaxe documentaire | Invocation réelle |
|------|---------------------|-------------------|
| Breakpoints | `@skill:epci:breakpoint-system` | Section impérative + AskUserQuestion explicite |
| Agents | `@agent:implementer` | `Task({ subagent_type: "implementer", ... })` |
| Stack skills | `@skill:python-django` | `Read("src/skills/stack/python-django/SKILL.md")` |

**Règle pour auteurs de step files:**
- Utiliser le format impératif direct (pas dans bloc de code)
- Afficher les boîtes ASCII hors bloc exécutable
- Appeler AskUserQuestion explicitement
- Ajouter `⏸️ ATTENDS la réponse` après chaque breakpoint

## Limitations

This skill does NOT:
- Handle STANDARD or LARGE features (use /implement)
- Debug existing bugs (use /debug)
- Perform code review (speed priority)
- Create Feature Documents
- Run security audits
