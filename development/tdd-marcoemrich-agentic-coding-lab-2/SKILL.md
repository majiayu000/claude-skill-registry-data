---
name: tdd
description: Strict Test-Driven Development workflow (Red-Green-Refactor) with configurable human-in-the-loop checkpoints. Invoke when the user explicitly asks to use TDD, do a TDD kata, or follow the Red-Green-Refactor discipline. Do NOT invoke for general coding tasks where the user has not asked for TDD.
---

# TDD Rules -- Hybrid (hybrid-v6, pi, exact-coding baseline)

## CRITICAL: Mandatory Output Format

This workflow runs on **pi**, where the phase skills are documents you read
rather than tools you call. Because there is no tool call per phase, the phase
boundaries are marked by **text markers** in your output instead.

### Phase-Completion Markers Are MANDATORY

Every TDD phase MUST produce a specific text marker in your output. The markers
are what make the phase structure legible — to you while you work, and to anyone
reading the session afterwards. A missing marker makes that phase invisible.

| Phase     | Mandatory Output Marker                   | What It Makes Visible                |
|-----------|-------------------------------------------|--------------------------------------|
| Test List | `## Test List` heading                    | the test list was written first      |
| Red       | `## Red` heading                          | a new cycle started                  |
| Red       | `Red Phase Complete:` + prediction lines  | both predictions were made and scored |
| Green     | `## Green` heading                        | a minimal implementation was added   |
| Refactor  | `subagent` tool call with `agent: "refactor"` | refactoring ran in an isolated context |

**Format for each Red phase output:**

```
## Red -- Test N: <test description>

<prediction and failure verification steps>

Red Phase Complete:
**Compilation Prediction**: <what you expect> Correct
**Runtime Prediction**: <what you expect> Correct

<Result summary>
```

The two prediction lines (`Compilation Prediction: ... Correct` / `Runtime Prediction: ... Correct`)
must be scored **separately** — that is what makes the Guessing Game worth
playing. You MUST output them verbatim with `Correct` or `Incorrect` at the end.
Do not abbreviate, summarize, or collapse them. Do not skip them when a test already passes --
in that case, write:

```
## Red -- Test N: <test description>

Test already passes -- no new failure to fix. Skipping green/refactor.
```

**Format for Green phase output:**

```
## Green -- <brief summary of what was added>
```

**Format for Test List phase output:**

```
## Test List

<test list details>
```

## Overview

This project follows strict Test-Driven Development practices using the Red-Green-Refactor cycle.
hybrid-v1 keeps red and green in a shared context so the predictions, error messages, and minimal
implementations stay coherent -- and isolates refactoring so the model evaluates the resulting
code on its own merits.

This baseline supports **configurable human-in-the-loop checkpoints** between
phases. See `.pi/rules/human-in-the-loop.md` for the Autonomy Level setting and
stop behavior.

## Architecture: Skills + Subagent

- **`test-list`, `red`, `green`** -- Their SKILL.md files are auto-loaded as context.
  Read each SKILL.md **before the first use** of that phase, then follow its instructions
  directly in the main context. You execute the phase yourself, following the skill content.
- **Refactor** -- Runs as a **Subagent with isolated context** via the `subagent` tool.
  The refactor agent sees only the current source/tests, not the full red/green history.
  Hypothesis: refactoring benefits most from a fresh perspective free of implementation bias.

Do NOT skip reading the skill files. Do NOT skip the mandatory output markers.

### Which Mechanism to Use:

| Phase         | Mechanism                              | How to Execute                                              |
|---------------|----------------------------------------|-------------------------------------------------------------|
| Test List     | **Skill document** (main context)      | Read `.pi/skills/test-list/SKILL.md`, follow its steps      |
| Red Phase     | **Skill document** (main context)      | Read `.pi/skills/red/SKILL.md`, follow its steps           |
| Green Phase   | **Skill document** (main context)      | Read `.pi/skills/green/SKILL.md`, follow its steps         |
| Refactor Phase| **Subagent** (isolated context)        | `subagent` tool with `agent: "refactor"`, `agentScope: "both"` |

## TDD Workflow

### 1. Test List Phase
**READ SKILL**: `.pi/skills/test-list/SKILL.md`

Provide: feature, test file path, implementation file path, requirements.

The skill creates a comprehensive test list using `it.todo()` covering every rule and example from the specification.

**DO NOT** write the test list yourself. Follow the skill instructions and produce the `## Test List` marker.


### 2. Red Phase
**READ SKILL**: `.pi/skills/red/SKILL.md`

Provide: test file path, which `it.todo()` to activate, current passing-test count, implementation file path.

The skill activates exactly ONE test, makes explicit predictions, and verifies failure.

**DO NOT** write test code yourself. Follow the skill instructions and produce the `## Red` and `Red Phase Complete:` markers with prediction lines.

### 3. Green Phase
**READ SKILL**: `.pi/skills/green/SKILL.md`

Provide: test file path, failing test name, current error, implementation file path.

The skill implements minimal code to make the test pass -- hardcoded returns are fine for early tests.

**DO NOT** write implementation code yourself. Follow the skill instructions and produce the `## Green` marker.

### 4. Refactor Phase
**INVOKE SUBAGENT**: Use the `subagent` tool with these parameters:

```json
{
  "agent": "refactor",
  "agentScope": "both",
  "task": "Test file: src/<feature>.spec.ts\nImplementation file: src/<feature>.ts\nPassing tests: <count>\nRecent Green phase: <one-line summary of what was just added>\n\nRefactor the implementation while keeping all tests green."
}
```

`agentScope: "both"` is REQUIRED because the `refactor` agent lives in `.pi/agents/` (project-local). Without this flag the subagent extension only sees user-level agents and the call fails with "Unknown agent: refactor".

The agent will improve code while keeping tests green:
- MUST attempt at least one refactoring (or document why none is possible)
- Evaluate naming FIRST
- Apply Four Rules of Simple Design (priority order)
- Calculate APP (Absolute Priority Premise) mass before/after

**DO NOT** refactor code yourself -- let the subagent do it. After it returns, read its summary, apply any test-runs needed for sanity, and proceed to the next Red phase.

### 5. Repeat
Return to step 2 (Red phase) for the next test.

### 6. End-Refactor (once, after the last green cycle)
**INVOKE SUBAGENT**: `subagent` tool with `agent: "end-refactor"`, `agentScope: "both"`

After the last per-cycle refactor returns and all tests pass, invoke the
`end-refactor` subagent exactly once. It refactors the **whole production
tree** (`src/`, excluding `*.spec.ts`) using deterministic pre/post
measurements: ESLint smells + SonarJS cognitive complexity, plus APP mass
and McCabe cyclomatic complexity. It iterates one change at a time until no
metric improves further.

```json
{
  "agent": "end-refactor",
  "agentScope": "both",
  "task": "Implementation files: src/<all non-spec *.ts>\nTest files: src/<*.spec.ts>\nPassing tests: <count>\n\nRun the final metric-driven refactoring pass over the whole src/. Iterate ONE change at a time with pre/post measurement (ESLint, cognitive, APP, McCabe). Stop when no metric improves further."
}
```

**DO NOT** refactor the whole src/ yourself — delegate to the end-refactor subagent.

## Core TDD Principles

### TDD Mindset
TDD practices will feel counterintuitive:
- **Hardcoded returns feel "too simple"** -- This is correct!
- **The urge to implement ahead is strong** -- Resist this
- **Minimal steps feel inefficient** -- They actually accelerate development
- **Predictions feel unnecessary** -- They build crucial understanding

### Common TDD Failure Modes
- **MISSING OUTPUT MARKERS** -- The most critical failure mode on pi.
  Every cycle MUST have `## Red` and `## Green` headings.
  Every Red cycle with a failing test MUST have `Red Phase Complete:` with prediction lines.
- Multiple active tests at once
- Implementing beyond what tests demand
- Skipping predictions
- Avoiding refactoring
- Refactoring in the main context instead of via the subagent

## Human-in-the-Loop

Between phases, the workflow consults `.pi/rules/human-in-the-loop.md` to
decide whether to pause for human approval. The default Autonomy Level is
`full-hitl`, which stops after Test-List, Red, and Refactor (not Green) and on
prediction failures. Switch levels by editing the setting at the top of the
HITL file — see that file for the full table.

For unattended batch runs, set the level to `autonomous` to disable all stops.

## Technical Setup: TypeScript and Vitest

### TypeScript Conventions
- Use proper type annotations
- Leverage TypeScript's type checking during development
- Name files after their content
- Import with explicit `.js` extensions for local modules

### Test File Conventions
- Use `.spec.ts` extension for test files
- Place tests near implementation files
- Import test functions: `import { describe, it, expect } from "vitest"`

### Running Tests

Run tests with `pnpm test`.

### Example Test Template

The test list comes from the kata's specification -- do not add generic "validate input types" or "edge cases" tests unless the spec calls for them.

```typescript
// some-feature.spec.ts
import { describe, it, expect } from "vitest";
import { someFeature } from "./some-feature.js";

describe("Some Feature", () => {
  it.todo("[first behaviour from the spec]");
  it.todo("[second behaviour from the spec]");
});
```

## Workflow Sequence

1. **Test List Phase** -- Read skill, produce `## Test List` marker
2. **For each test:**
   - **Red Phase** -- Read skill, produce `## Red` and `Red Phase Complete:` with predictions
   - **Green Phase** -- Read skill, produce `## Green` marker
   - **Refactor Phase** -- Invoke `subagent` tool with `agent: "refactor"`, `agentScope: "both"`
3. **Continue** until all tests are implemented and passing
4. **End-Refactor** -- invoke `subagent` with `agent: "end-refactor"`, once, over the whole `src/`

### Required Task Content for the Refactor Subagent

The refactor subagent has no memory of the red/green phases. Pass everything it needs in the `task` parameter:

```
Test file: [path]
Implementation file: [path]
Passing tests: [count]
Recent changes: [one-line summary of the Green phase]
```

After the subagent returns, read its summary and proceed directly to the next Red phase.

## Remember

- **ALWAYS PRODUCE THE MANDATORY MARKERS** -- `## Red`, `Red Phase Complete:`, `## Green`, `## Test List`
- **ALWAYS USE THE SUBAGENT** for refactor -- `subagent` tool with `agent: "refactor"`, `agentScope: "both"`
- Follow skill content (test-list/red/green SKILL.md) for the actual work
- Pass `agentScope: "both"` to the `subagent` tool so the project-local refactor agent is discovered
- Consult `.pi/rules/human-in-the-loop.md` at every phase boundary
- Trust the process -- discomfort is a signal you're doing it right

