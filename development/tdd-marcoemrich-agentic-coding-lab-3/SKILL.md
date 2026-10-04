---
name: tdd
description: Strict Test-Driven Development workflow (Red-Green-Refactor) with configurable human-in-the-loop checkpoints. Apply when the user explicitly asks to use TDD, do a TDD kata, or follow the Red-Green-Refactor discipline. Do NOT apply for general coding tasks where the user has not asked for TDD.
---

# TDD Rules -- Hybrid (exact-hybrid-v2-testlist-fix, cursor, exact-coding baseline)

## CRITICAL: Mandatory Output Format

This workflow runs on **cursor-agent**. The `test-list`, `red` and `green`
phases are skill documents you read rather than tools you call — read each
SKILL.md once and then follow its instructions directly. Because those phases
produce no tool call of their own, their boundaries are marked by **text
markers** in the assistant output. Refactor is different: it runs as an
**isolated subagent** via the Task tool, so the tool call itself marks the
phase.

### Phase-Completion Markers Are MANDATORY

Every TDD phase MUST produce its marker. The skill phases emit a text heading;
the refactor phase is recognised by its subagent call. The markers are what
make the phase structure legible — to you while you work, and to anyone reading
the session afterwards. A missing marker makes that phase invisible.

| Phase     | Mandatory Marker                          | What It Makes Visible                |
|-----------|-------------------------------------------|--------------------------------------|
| Test List | `Test List Created` (or `Test List Phase Complete`) | the test list was written first |
| Red       | `## Red` heading                          | a new cycle started                  |
| Red       | `Red Phase Complete:` + prediction lines  | both predictions were made and scored |
| Green     | `## Green` heading                        | a minimal implementation was added   |
| Refactor  | Task call to the `refactor` subagent      | refactoring ran in an isolated context |

**IMPORTANT**: emit every text marker as **assistant output text**, not only
inside private reasoning. A marker that appears only in a thinking/reasoning
block is not visible. State the `## Red` / `## Green` headings in your visible
response.

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

**Refactor phase output** is produced by the `refactor` subagent, not by you.
After it returns, read its report and continue with the next Red phase.

**Format for Test List phase output:**

```
Test List Created:

<test list details>
```

## Overview

This project follows strict Test-Driven Development practices using the Red-Green-Refactor cycle.
The hybrid keeps red and green in a shared context so the predictions, error messages, and minimal
implementations stay coherent -- and isolates refactoring so the model evaluates the resulting
code on its own merits.

This baseline supports **configurable human-in-the-loop checkpoints** between
phases. See `.cursor/rules/human-in-the-loop.mdc` for the Autonomy Level setting
and stop behavior.

## Architecture: Auto-loaded Skills + Isolated Subagent

This workflow is a **hybrid**, exactly like the cc and pi variants:

- **`test-list`, `red`, `green`** -- Their SKILL.md files are auto-loaded as context.
  Read each SKILL.md **before the first use** of that phase, then follow its instructions
  directly in the main context. These three share state, so the test list, last error,
  and current implementation stay in working memory.
- **`refactor`** -- Runs as a **Task subagent with isolated context**. It lives in
  `.cursor/agents/` and sees only the current source and tests, not the red/green
  history. Hypothesis: refactoring benefits most from a fresh perspective
  free of implementation bias.

**Delegate the refactor phase — do not perform it yourself.** If you refactor
in the main context instead of calling the subagent, the workflow loses the
architectural separation that makes the hybrid work.

Do NOT skip reading the skill files. Do NOT skip the mandatory markers.

### Which Mechanism to Use:

| Phase         | Mechanism                              | How to Execute                                              |
|---------------|----------------------------------------|-------------------------------------------------------------|
| Test List     | **Skill document** (main context)      | Read `.cursor/skills/test-list/SKILL.md`, follow its steps  |
| Red Phase     | **Skill document** (main context)      | Read `.cursor/skills/red/SKILL.md`, follow its steps        |
| Green Phase   | **Skill document** (main context)      | Read `.cursor/skills/green/SKILL.md`, follow its steps      |
| Refactor Phase| **Task subagent** (isolated context)   | Launch the `refactor` agent from `.cursor/agents/`           |

## TDD Workflow

### 1. Test List Phase
**READ SKILL**: `.cursor/skills/test-list/SKILL.md`

Provide: feature, test file path, implementation file path, requirements.

The skill creates a comprehensive test list using `it.todo()` covering every rule and example from the specification.

**DO NOT** write the test list yourself. Follow the skill instructions and produce the `Test List Created:` marker.


### 2. Red Phase
**READ SKILL**: `.cursor/skills/red/SKILL.md`

Provide: test file path, which `it.todo()` to activate, current passing-test count, implementation file path.

The skill activates exactly ONE test, makes explicit predictions, and verifies failure.

**DO NOT** write test code yourself. Follow the skill instructions and produce the `## Red` and `Red Phase Complete:` markers with prediction lines.

### 3. Green Phase
**READ SKILL**: `.cursor/skills/green/SKILL.md`

Provide: test file path, failing test name, current error, implementation file path.

The skill implements minimal code to make the test pass -- hardcoded returns are fine for early tests.

**DO NOT** write implementation code yourself. Follow the skill instructions and produce the `## Green` marker.

### 4. Refactor Phase
**LAUNCH SUBAGENT**: the `refactor` agent from `.cursor/agents/refactor.md`

The subagent runs in an isolated context and has **no memory of red/green** —
everything it needs must be in the prompt you pass it:

```
Test file: src/<feature>.spec.ts
Implementation file: src/<feature>.ts
Passing tests: <count>
Recent Green phase: <one-line summary of what was just added>

Refactor the implementation while keeping all tests green.
```

The agent improves the implementation while keeping all tests green:
- MUST attempt at least one refactoring (or document why none is possible)
- Evaluate naming FIRST
- Apply the Four Rules of Simple Design (priority order)
- Calculate APP (Absolute Priority Premise) mass before/after

**DO NOT** refactor code yourself -- let the agent do it. After it returns,
read its report and proceed directly to the next Red phase.

### 5. Repeat
Return to step 2 (Red phase) for the next test.

## Core TDD Principles

### TDD Mindset
TDD practices will feel counterintuitive:
- **Hardcoded returns feel "too simple"** -- This is correct!
- **The urge to implement ahead is strong** -- Resist this
- **Minimal steps feel inefficient** -- They actually accelerate development
- **Predictions feel unnecessary** -- They build crucial understanding

### Common TDD Failure Modes
- **MISSING OUTPUT MARKERS** -- The most critical failure mode.
  Every cycle MUST have `## Red` and `## Green` headings in visible output.
  Every Red cycle with a failing test MUST have `Red Phase Complete:` with prediction lines.
- **NOT DELEGATING THE REFACTOR PHASE** -- equally critical. Refactoring in the
  main context loses the isolated-context architecture.
- Multiple active tests at once
- Implementing beyond what tests demand
- Skipping predictions
- Avoiding refactoring

## Human-in-the-Loop

Between phases, the workflow consults `.cursor/rules/human-in-the-loop.mdc` to
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

1. **Test List Phase** -- Read skill, produce `Test List Created:` marker
2. **For each test:**
   - **Red Phase** -- Read skill, produce `## Red` and `Red Phase Complete:` with predictions
   - **Green Phase** -- Read skill, produce `## Green` marker
   - **Refactor Phase** -- Launch the `refactor` subagent, read its report
3. **Continue** until all tests are implemented and passing

## Remember

- **ALWAYS PRODUCE THE MANDATORY MARKERS** -- `Test List Created:`, `## Red`, `Red Phase Complete:`, `## Green` -- in visible assistant output, not only in reasoning. Refactor is recognised by its subagent call, not by a heading.
- **ALWAYS DELEGATE THE REFACTOR PHASE** -- launch the `refactor` agent from `.cursor/agents/`; never refactor in the main context.
- **The refactor subagent has no memory of red/green** -- pass it everything it needs in the prompt.
- Follow skill content (test-list/red/green SKILL.md) for the actual work
- Consult `.cursor/rules/human-in-the-loop.mdc` at every phase boundary
- Trust the process -- discomfort is a signal you're doing it right

