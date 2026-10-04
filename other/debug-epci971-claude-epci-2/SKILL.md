---
name: epci:debug
description: >-
  Structured debugging workflow with hypothesis-driven investigation using
  Tree of Thought (ToT) methodology. Generates ranked hypotheses with testable
  predictions, applies scientific method to root cause analysis.
  Routes to Trivial (direct fix), Quick (TDD cycle), or Complex (full investigation).
  Multi-source research via Context7 MCP, WebSearch, Perplexity suggestions.
  Auto-detects stack skills (Django, React, Spring, Symfony, Tailwind) for patterns.
  Use when: debugging errors, fixing bugs, investigating issues, troubleshooting.
  Triggers: debug, fix bug, investigate error, troubleshoot, find root cause.
  Not for: performance optimization (use /improve), refactoring (use /refactor).
user-invocable: true
argument-hint: "<bug description or error message>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# Debug

Structured debugging with Tree of Thought (ToT) hypothesis-driven investigation.

## Quick Start

```
/debug "users can't login after password reset"
/debug "TypeError: Cannot read property 'map' of undefined in checkout"
/debug "500 error on /api/orders endpoint"
/debug --full "intermittent session timeout issue"
/debug --turbo "missing import in utils.ts"
```

## MANDATORY EXECUTION RULES (READ FIRST):

- 🔴 NEVER guess root cause without evidence
- 🔴 NEVER skip hypothesis generation (min 2 hypotheses)
- 🔴 NEVER apply fix without regression test (Quick/Complex routes)
- ✅ ALWAYS start with step-00-clarify.md (unless --no-clarify)
- ✅ ALWAYS follow next_step from each step
- ✅ ALWAYS use scientific method: Observe → Hypothesize → Test → Verify
- ✅ ALWAYS store bug pattern in project-memory after fix
- ✅ ALWAYS detect stack skills at initialization
- ⛔ FORBIDDEN applying untested fixes in production code
- 🔵 YOU ARE A METHODICAL INVESTIGATOR following scientific method

## EXECUTION PROTOCOLS:

1. **Load** step-00-clarify.md (or step-01-evidence.md if --no-clarify)
2. **Execute** current step protocols completely
3. **Present** breakpoint if specified in step
4. **Evaluate** routing decision at step-04
5. **Proceed** via appropriate route (Trivial/Quick/Complex)
6. **Complete** post-debug memory storage

## Workflow Overview

```
+---------------------------------------------------------------------+
|                    DEBUG WORKFLOW (ToT)                              |
+---------------------------------------------------------------------+
|                                                                      |
|  Step 00: CLARIFY (conditional)                                      |
|  +- Skip if: --no-clarify OR clarity >= 0.6                          |
|  +- clarification-engine for input cleanup                           |
|                                                                      |
|  Step 01: EVIDENCE                                                   |
|  +- Gather: error message, stack trace, reproduction steps           |
|  +- project-memory.recall_bugs(pattern)                              |
|  +- git log --since="1 week" for recent changes                      |
|                                                                      |
|  Step 02: RESEARCH                                                   |
|  +- Context7 MCP -> WebSearch -> Perplexity (cascade)                |
|  +- Stack skill patterns loaded                                      |
|                                                                      |
|  Step 03: THOUGHT TREE                                               |
|  +- Generate 3-4 hypotheses with schema                              |
|  +- Rank by confidence (pairwise comparison)                         |
|  +- Each with testable_prediction + quick_check                      |
|                                                                      |
|  Step 04: ROUTING                                                    |
|  +- complexity-calculator evaluation                                 |
|  +- Route: TRIVIAL / QUICK / COMPLEX                                 |
|                                                                      |
|  +--> Route A: TRIVIAL (step-05)                                     |
|  |    +- Direct fix, no breakpoint                                   |
|  |    +- Inline summary                                              |
|  |                                                                   |
|  +--> Route B: QUICK (step-06)                                       |
|  |    +- TDD cycle via tdd-enforcer                                  |
|  |    +- @implementer for fix                                        |
|  |                                                                   |
|  +--> Route C: COMPLEX (step-07)                                     |
|       +- Solution scoring matrix                                     |
|       +- BREAKPOINT: diagnostic type                                 |
|       +- @code-reviewer (always)                                     |
|       +- @security-auditor (if auth patterns)                        |
|       +- @qa-reviewer (if >= 3 tests)                                |
|       +- Debug Report generated                                      |
|                                                                      |
|  Step 08: POST-DEBUG                                                 |
|  +- project-memory.store_bug(pattern)                                |
|  +- Execute post-debug hook                                          |
|  +- Suggest /commit if --commit flag                                 |
|                                                                      |
+---------------------------------------------------------------------+
```

## Steps

| Step | Name | Description | Skippable |
|------|------|-------------|-----------|
| 00 | clarify | Input clarification | Yes (--no-clarify or high clarity) |
| 01 | evidence | Gather diagnostic evidence | No |
| 02 | research | Multi-source research | No |
| 03 | thought-tree | Build ToT hypotheses | No |
| 04 | routing | Evaluate complexity, route | No |
| 05 | trivial | Route A: Direct fix | Route-specific |
| 06 | quick | Route B: TDD cycle | Route-specific |
| 07 | complex | Route C: Full investigation | Route-specific |
| 08 | post | Post-debug memory + hooks | No |

## Routing Matrix

| Route | Criteria | LOC | Files | Uncertainty | Example |
|-------|----------|-----|-------|-------------|---------|
| TRIVIAL | 1 obvious cause | <10 | 1 | <5% | Typo, missing import |
| QUICK | 1 cause | <50 | 1-2 | <20% | Single component bug |
| COMPLEX | 2+ causes | >=50 | 3+ | >=20% | Multi-component, unclear |

**Rule**: >= 2 COMPLEX criteria → Route COMPLEX

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--full` | off | Force COMPLEX mode (skip routing) |
| `--turbo` | off | @clarifier Haiku, auto-apply best solution, skip breakpoint |
| `--no-report` | off | COMPLEX mode without Debug Report |
| `--no-clarify` | off | Skip input clarification |
| `--commit` | off | Prepare commit context after fix |
| `--context <path>` | - | Link to existing Feature Document |

### --turbo Mode

| Aspect | Standard | Turbo |
|--------|----------|-------|
| Diagnostic model | Sonnet | @clarifier (Haiku) |
| Thought tree | Full (3-4 H) | Simplified (top 2) |
| Solution selection | Multiple + scoring | Best only (auto-apply) |
| Breakpoint | Required (Complex) | Skipped |
| Confidence threshold | N/A | 70% (fallback if lower) |
| Report | Full Debug Report | Summary only |

## Step Files

- [steps/step-00-clarify.md](steps/step-00-clarify.md) — Input clarification
- [steps/step-01-evidence.md](steps/step-01-evidence.md) — Gather evidence
- [steps/step-02-research.md](steps/step-02-research.md) — Multi-source research
- [steps/step-03-thought-tree.md](steps/step-03-thought-tree.md) — Build ToT hypotheses
- [steps/step-04-routing.md](steps/step-04-routing.md) — Evaluate & route
- [steps/step-05-trivial.md](steps/step-05-trivial.md) — Route A: Trivial
- [steps/step-06-quick.md](steps/step-06-quick.md) — Route B: Quick
- [steps/step-07-complex.md](steps/step-07-complex.md) — Route C: Complex
- [steps/step-08-post.md](steps/step-08-post.md) — Post-debug

## Reference Files

- [references/hypothesis-schema.md](references/hypothesis-schema.md) — ToT JSON schema
- [references/routing-matrix.md](references/routing-matrix.md) — Criteria matrix
- [references/research-workflow.md](references/research-workflow.md) — Context7 → Web → Perplexity
- [references/solution-scoring.md](references/solution-scoring.md) — Scoring formula
- [references/debug-report-template.md](references/debug-report-template.md) — Output template
- [references/examples.md](references/examples.md) — Examples per route

## Shared Components Used

- `epci:clarification-engine` — Input cleanup (Step 0)
- `epci:complexity-calculator` — Routing evaluation (Step 4)
- `epci:breakpoint-system` — Type "diagnostic" for solution choice (Step 7)
- `epci:tdd-enforcer` — RED-GREEN-VERIFY cycle (Step 6, 7)
- `epci:project-memory` — Bug history recall and storage (Step 1, 8)

## Subagents

| Agent | Model | Trigger |
|-------|-------|---------|
| `@clarifier` | Haiku | --turbo mode, rapid diagnostic |
| `@code-reviewer` | Opus | COMPLEX mode, always invoked |
| `@security-auditor` | Opus | Files match `**/auth/**`, `**/security/**` |
| `@qa-reviewer` | Sonnet | >= 3 tests added |

## Stack Skills (Auto-detected)

| Stack | Trigger Files | Debug Patterns |
|-------|---------------|----------------|
| `python-django` | manage.py, django | Django debug toolbar, pytest markers |
| `javascript-react` | react in package.json | React DevTools, Jest debugging |
| `java-springboot` | spring-boot in pom/gradle | Actuator endpoints, JUnit |
| `php-symfony` | symfony in composer.json | Profiler, PHPUnit |
| `frontend-editor` | tailwind.config.* | Browser DevTools, CSS debugging |

## MCP Integration

| Server | Usage | Fallback |
|--------|-------|----------|
| Context7 | Documentation lookup for framework errors | WebSearch |
| Sequential | Multi-step reasoning (optional) | Native Claude thinking |

## Fallback Loop

```
IF prediction REJECTED during investigation:
  -> Mark hypothesis as "infirmed"
  -> Adjust confidence of remaining hypotheses
  -> Select next best hypothesis
  -> LOOP

IF all hypotheses exhausted:
  -> Generate new hypotheses based on findings
  -> OR escalate to user with missing info questions
  -> OR suggest targeted Perplexity research
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No stack trace | Incomplete input | Ask for reproduction steps |
| Context7 unavailable | MCP down | Fallback to WebSearch |
| All hypotheses infirmed | Wrong direction | Generate new hypotheses |
| TDD fails 2x | Complex root cause | Escalate to COMPLEX route |
| Fix introduces regression | Incomplete testing | Rollback, add more tests |

## Limitations

This skill does NOT:
- Debug CSS/layout frontend-only issues (use browser DevTools)
- Perform performance profiling (use /improve)
- Handle pure refactoring (use /refactor)
- Auto-commit Debug Reports
- Integrate with IDE breakpoints
