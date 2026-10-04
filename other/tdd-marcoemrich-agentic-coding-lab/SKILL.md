---
name: tdd
description: Strict Test-Driven Development workflow (Red-Green-Refactor) with configurable human-in-the-loop checkpoints. Invoke when the user explicitly asks to use TDD, do a TDD kata, or follow the Red-Green-Refactor discipline. Do NOT invoke for general coding tasks where the user has not asked for TDD.
---

# TDD Rules — Hybrid (hybrid-v1, exact-coding baseline)

## ⚠️ CRITICAL: Skill + Subagent Usage is MANDATORY

This workflow is a **hybrid** of two architectures:

- **`/test-list`, `/red`, `/green`** run as **Skills in the main context** — they share state, so the model keeps test list, last error, and current implementation in working memory.
- **Refactor** runs as a **Task subagent with isolated context** — the refactor agent sees only the current source/tests, not the full red/green history. Hypothesis: refactoring benefits most from a fresh perspective free of implementation bias.

The skill and subagent invocations are not just stylistic. If you write test code, implementation code, or refactorings directly in the main context instead of delegating, the workflow loses the architectural separation that makes the hybrid work.

Do NOT perform TDD phases without invoking the appropriate skill or agent.

### Before Starting Any TDD Work — Complete This Checklist:

- [ ] Have I been asked to implement something using TDD?
- [ ] Am I about to write tests or implementation code?
- [ ] **STOP** — Use the Skill tool (test-list/red/green) or the Task tool (refactor)
- [ ] NEVER write tests, code, or refactorings directly — ALWAYS delegate

### Which Tool to Use:

| Phase | Mechanism | Invoke With |
|-------|-----------|-------------|
| Test List | **Skill** (main context) | `Skill({ skill: "test-list" })` |
| Red Phase | **Skill** (main context) | `Skill({ skill: "red" })` |
| Green Phase | **Skill** (main context) | `Skill({ skill: "green" })` |
| Refactor Phase (per cycle) | **Task subagent** (isolated context) | `Task({ subagent_type: "refactor", prompt: ... })` |
| End-Refactor (once, after last cycle) | **Task subagent** (isolated context) | `Task({ subagent_type: "end-refactor", prompt: ... })` |

**If you find yourself writing test code, implementation code, or a refactoring without invoking the right tool first, you are doing it WRONG.**

## Overview

This project follows strict Test-Driven Development practices using the Red-Green-Refactor cycle. hybrid-v1 keeps red and green in a shared context so the predictions, error messages, and minimal implementations stay coherent — and isolates refactoring so the model evaluates the resulting code on its own merits.

This baseline supports **configurable human-in-the-loop checkpoints** between phases. See `@.claude/rules/human-in-the-loop.md` for the Autonomy Level setting and stop behavior.

## TDD Workflow

### 1. Test List Phase
**🚨 INVOKE SKILL**: `Skill({ skill: "test-list" })`

Provide: feature, test file path, implementation file path, requirements.

The skill creates a comprehensive test list using `it.todo()` covering every rule and example from the specification.

**DO NOT** write the test list yourself.

### 2. Red Phase
**🚨 INVOKE SKILL**: `Skill({ skill: "red" })`

Provide: test file path, which `it.todo()` to activate, current passing-test count, implementation file path.

The skill activates exactly ONE test, makes explicit predictions, and verifies failure.

**DO NOT** write test code yourself.

### 3. Green Phase
**🚨 INVOKE SKILL**: `Skill({ skill: "green" })`

Provide: test file path, failing test name, current error, implementation file path.

The skill implements minimal code to make the test pass — hardcoded returns are fine for early tests.

**DO NOT** write implementation code yourself.

### 4. Refactor Phase
**🚨 LAUNCH AGENT**: `Task({ subagent_type: "refactor", prompt: ... })`

**Required prompt context** (the subagent has no memory of red/green — give it everything it needs):

```
Task({
  subagent_type: "refactor",
  prompt: `
    Test file: src/<feature>.spec.ts
    Implementation file: src/<feature>.ts
    Passing tests: <count>
    Recent Green phase: <one-line summary of what was just added>

    Refactor the implementation while keeping all tests green.
  `
})
```

The agent will improve code while keeping tests green:
- MUST attempt at least one refactoring (or document why none is possible)
- Evaluate naming FIRST
- Apply Four Rules of Simple Design (priority order)
- Calculate APP (Absolute Priority Premise) mass before/after

**DO NOT** refactor code yourself — let the agent do it. After it returns, read its summary, apply any test-runs needed for sanity, and proceed to the next Red phase.

### 5. Repeat
Return to step 2 (Red phase) for the next test. **Invoke the `red` skill again.**

### 6. End-Refactor (once, after the last green cycle)
**🚨 LAUNCH AGENT**: `Task({ subagent_type: "end-refactor", prompt: ... })`

After the last per-cycle refactor returns and all tests pass, launch the `end-refactor` subagent exactly once. It refactors the **whole production tree** (`src/`, excluding `*.spec.ts`) using deterministic pre/post measurements: ESLint smells + SonarJS cognitive complexity, plus APP mass and McCabe cyclomatic complexity. It iterates one change at a time until no metric improves further.

**Required prompt context**:

```
Task({
  subagent_type: "end-refactor",
  prompt: `
    Implementation files: src/<all non-spec *.ts>
    Test files: src/<*.spec.ts>
    Passing tests: <count>

    Run the final metric-driven refactoring pass over the whole src/.
    Iterate ONE change at a time with pre/post measurement (ESLint, cognitive,
    APP, McCabe). Stop when no metric improves further or no improvement is
    possible.
  `
})
```

After the end-refactor subagent returns, read its summary and proceed to the Done Marker.

**DO NOT** refactor the whole src/ yourself — delegate to the end-refactor subagent.

## Core TDD Principles

### TDD Mindset
TDD practices will feel counterintuitive:
- **Hardcoded returns feel "too simple"** — This is correct!
- **The urge to implement ahead is strong** — Resist this
- **Minimal steps feel inefficient** — They actually accelerate development
- **Predictions feel unnecessary** — They build crucial understanding

### Common TDD Failure Modes
- **🚨 NOT USING SKILLS / SUBAGENT** — The most critical failure mode
- Multiple active tests at once
- Implementing beyond what tests demand
- Skipping predictions
- Avoiding refactoring
- Refactoring in the main context instead of via the subagent

## Human-in-the-Loop

Between phases, the workflow consults `@.claude/rules/human-in-the-loop.md`
to decide whether to pause for human approval. The default Autonomy Level
is `full-hitl`, which stops after Test-List, Red, and Refactor (not Green)
and on prediction failures. Switch levels by editing the setting at the
top of the HITL file — see that file for the full table.

For unattended batch runs, set the level to `autonomous` to disable all
stops.

## Technical Setup

See `@.claude/rules/tdd-with-ts-and-vitest.md` for TypeScript and Vitest configuration.

## Rule Files

| File | Contains |
|------|----------|
| `skills/tdd/SKILL.md` (this file) | The TDD workflow itself |
| `@.claude/rules/human-in-the-loop.md` | When to pause for human approval (Autonomy Level) |
| `@.claude/rules/tdd-execution-mode.md` | Phase sequence; interactive-by-default execution |
| `@.claude/rules/subagent-prompts.md` | What to pass the isolated refactor / end-refactor subagents |
| `@.claude/rules/tdd-with-ts-and-vitest.md` | TypeScript + Vitest setup |

## Running Tests

Run tests with `pnpm test`.

## Remember

- **🚨 ALWAYS USE SKILLS** for test-list/red/green; **ALWAYS USE THE SUBAGENT** for refactor
- Never write tests, implementation, or refactorings directly
- Refactor subagent runs in an isolated context — give it everything it needs in the prompt
- Consult `@.claude/rules/human-in-the-loop.md` at every phase boundary
- Trust the process — discomfort is a signal you're doing it right
