---
name: pair-capability-verify-quality
description: "Checks quality gates against the current codebase. Reads project-specific quality gate command from way-of-working adoption and universal standards from quality-standards guidelines. Gates already passing are skipped. Invocable independently or composed by /pair-process-implement and /pair-process-review."
version: 0.4.1
author: Foomakers
---

# /pair-capability-verify-quality — Quality Gate Checker

Validate the current codebase against quality gates. Two sources of truth:

- **[way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)** — project-specific quality gate command and process (e.g., `pnpm quality-gate`). This is "what command we run."
- **[quality-standards](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/README.md)** — universal quality standards (gates, DoD, checklists). This is "what we check."

Only check gates that are not already passing.

## Arguments

| Argument | Required | Description                                                                                                    |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| `$scope` | No       | Limit checking: `code-quality`, `tests`, `lint`, `all`, or any custom scope key from adoption (default: `all`) |

## Algorithm

Execute each gate in order. For every gate, follow the **check → skip → act → verify** pattern.

### Step 1: Read Adoption Quality Gate Configuration

1. **Check**: Read [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) and look for a **Quality Gates** section declaring the project-specific quality gate command (e.g., `pnpm quality-gate`).
2. **Skip**: If `way-of-working.md` has no Quality Gates section, fall back to `package.json` scripts for detectable gate commands (e.g., `test`, `lint`, `ts:check`).
3. **Act**: If found, record the command for use in Step 5. Also note any sub-checks listed (e.g., type checking, testing, linting, formatting).

### Step 2: Lint Gate

1. **Check**: Run the project linter (e.g., `pnpm lint` or `turbo lint`). Capture output.
2. **Skip**: If zero violations, report "Lint: PASS" and move to Step 3.
3. **Act**: If violations found, report each violation with file and line.
4. **Verify**: After developer fixes, re-run linter to confirm zero violations.

### Step 3: Type Check Gate

1. **Check**: Run the type checker (e.g., `pnpm tsc --noEmit` or `turbo build`). Capture output.
2. **Skip**: If zero errors, report "Type Check: PASS" and move to Step 4.
3. **Act**: If errors found, report each error with file and line.
4. **Verify**: After developer fixes, re-run type checker to confirm zero errors.

### Step 4: Test Gate

1. **Check**: Run the test suite (e.g., `pnpm test` or `turbo test`). Capture output including coverage.
2. **Skip**: If all tests pass, report "Tests: PASS (N tests, X% coverage)" and move to Step 5.
3. **Act**: If tests fail, report each failure with test name, file, and assertion message.
4. **Verify**: After developer fixes, re-run tests to confirm all pass.

### Step 5: Custom Gates (from adoption)

1. **Check**: Read [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) → look for a `### Custom Gate Registry` section.
2. **Branch** based on what is found:

   **A) Custom Gate Registry table found** → execute custom gates (Step 5.A).

   **B) Explicit opt-out found** (section contains "No custom quality gates") → skip to Step 6 silently.

   **C) No Custom Gate Registry section at all** → first-time setup (Step 5.C).

#### Step 5.A: Execute Custom Gates

1. **Act**: For each row in the table, ordered by `Order`, filtered by `$scope`:
   - `$scope = all` → run all custom gates.
   - `$scope = <scope-key>` → run only gate(s) matching that scope key.
   - For each gate, apply check → skip → act → verify:
     - **Check**: Has this gate already run in this session?
     - **Skip**: If cached result exists, reuse it.
     - **Act**: Run the gate command. Capture output and exit code.
     - **Verify**: Record result based on `Required` column:
       - `Required = Yes` → exit code 0 = PASS, non-zero = FAIL (contributes to overall FAIL).
       - `Required = No` (Advisory) → exit code 0 = PASS, non-zero = WARNING (does not block).
2. **Verify**: All custom gates executed and results recorded. Move to Step 6.

#### Step 5.C: First-Time Custom Gate Setup

1. **Act**: Ask the developer:

   > No custom quality gates configured. Would you like to add custom gate steps (e.g., formatting, security scan, markdown lint)?
   > If not, I'll record the opt-out so this question won't be asked again.

2. **Branch**:
   - **Developer says yes** → help define gates and write the Custom Gate Registry table to [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md). Then execute them (Step 5.A).
   - **Developer says no** → write the opt-out marker to [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md):

     ```markdown
     ### Custom Gate Registry

     No custom quality gates configured. To add custom gates, replace this line with the gate table (see quality-gates.md).
     ```

3. **Verify**: way-of-working.md updated. Move to Step 6.

See [quality-gates.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/quality-gates.md) for Custom Gate Registry table schema and enforcement level semantics.

### Step 6: Aggregate Quality Gate

If a project-level quality gate command exists (from Step 1):

1. **Check**: Run the aggregate command (e.g., `pnpm quality-gate`).
2. **Skip**: If exit code 0, report "Quality Gate: PASS" and move to output.
3. **Act**: If non-zero exit, report the failing sub-gates.
4. **Verify**: After developer fixes, re-run to confirm pass.

## Output Format

Present results as:

```text
QUALITY GATE REPORT:
├── Lint:       [PASS | FAIL — N violations]
├── Type Check: [PASS | FAIL — N errors]
├── Tests:      [PASS — N tests, X% coverage | FAIL — N failures]
├── Custom:     [N gates — N PASS, N FAIL, N WARNING | No custom gates]
└── Aggregate:  [PASS | FAIL | N/A]

RESULT: [ALL GATES PASS | BLOCKED — N gates failing]
```

## Composition Interface

When composed by `/pair-process-implement` or `/pair-process-review`:

- **Input**: The composing skill invokes `/pair-capability-verify-quality` after implementation or before commit.
- **Output**: Returns PASS or FAIL with details. The composing skill decides what to do:
  - `/pair-process-implement`: HALT on FAIL — developer must fix before commit.
  - `/pair-process-review`: Report FAIL as review finding — does not block review completion.

When invoked **independently**:

- Run all gates (or scoped gates if `$scope` is provided).
- Report results. No side effects — this skill only reads and reports.

## Graceful Degradation

- If a standard gate command is not available (e.g., no test script in package.json), skip that gate and report: "Tests: SKIPPED — no test command found."
- If [quality-standards](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/README.md) directory is not found, warn and run only detectable gates (lint, type check, tests from package.json scripts).
- If no quality-related scripts are found at all, report: "No quality gates detected. Configure quality gate commands in package.json or way-of-working.md."
- If a custom gate command fails to execute (command not found), report as WARNING: "Gate `[name]`: SKIPPED — command not found."
- If [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) is not found, skip custom gates entirely (standard gates still run).

## Notes

- This skill is **read-only** except for Step 5.C (first-time setup writes opt-out or Custom Gate Registry to way-of-working.md). All other steps only run existing commands.
- Two sources: [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) for the project-specific quality gate command and custom gates (adoption-driven), [quality-standards](../../../.pair/knowledge/guidelines/quality-assurance/quality-standards/README.md) for universal quality standards.
- Standard gates (Lint, Type Check, Test) are universal and language/platform-independent. Custom gates are project-specific and defined in adoption.
- Each gate is independent — a failure in one gate does not prevent checking subsequent gates.
- Re-invoke after fixes to confirm resolution. Already-passing gates are re-verified but complete instantly.
- First-time setup (Step 5.C) only triggers once — after the developer responds, way-of-working.md is updated and subsequent invocations follow branch A or B.
