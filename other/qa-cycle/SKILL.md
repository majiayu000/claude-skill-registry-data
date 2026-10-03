---
name: qa-cycle
description: "QA + bugfix cycle until it passes"
user-invocable: true
workflow:
  version: 1
  steps:
    - id: gate-pre-qa
      role: system
      intent: "Run project tests and lint before QA validation."
      gate: true
      produces: [test-result, lint-result]
    - id: qa-validate
      role: qa
      intent: "Validate the implementation against acceptance criteria. Test edge cases and error scenarios. Report bugs found."
      requires: [acceptance-criteria, test-result, lint-result]
      produces: [qa-report]
      model-tier: execution
    - id: bugfix
      role: bugfix
      intent: "Diagnose and fix bugs reported by QA. Run tests after fixing."
      requires: [qa-report]
      produces: [bugfix-result]
      model-tier: execution
    - id: gate-post-qa
      role: system
      intent: "Run project tests and lint after QA cycle completes."
      gate: true
      produces: [final-test-result, final-lint-result]
---

# QA Cycle

Runs a QA validation cycle followed by bugfix until all criteria pass clean. Useful for validating implementations without the full build-feature pipeline.

## When to use

- After implementing changes that need validation
- To verify that a bug fix did not introduce regressions
- As a final cycle before creating a PR

## Usage

`/qa-cycle`

## Process

### Step 1 — Automated verification (mandatory)

Before invoking the QA agent, run the project verification commands. The specific commands are in the "CLI commands" section of CLAUDE.md:

1. Run project tests (e.g., `npm test`) — record result and output
2. Run project lint (e.g., `npm run lint`) — record result and output
3. If any fail, this becomes input for the QA report as an automatic Blocker bug

### Step 2 — QA Validation

Invoke the QA agent using Task tool with `model: "sonnet"` (execution tier):

1. Read `.claude/agents/qa.md` to assume the QA role
2. Read CLAUDE.md for context
3. Receive the test and lint results from Step 1
4. If tests or lint failed, include them as Blocker bugs in the report
5. Review the acceptance criteria for the current task (if provided)
6. Validate edge cases and error scenarios
7. Report results

### Step 3 — Bugfix (if there are bugs)

If QA reports bugs (including test/lint failures), invoke the Bugfix agent using Task tool with `model: "sonnet"` (execution tier):

1. Read `.claude/agents/bugfix.md` to assume the Bugfix role
2. Receive the QA bug report as input
3. Diagnose the root cause of each bug
4. Implement the minimal fix
5. Verify that the fix resolves the issue
6. Run tests and lint to confirm no regressions were introduced

### Step 4 — Re-validation

Return to Step 1 (automated verification) to re-validate after the bugfix.
Maximum 3 verification-QA-bugfix cycles to prevent infinite loops.

### Step 5 — Final result

Present the result:

- **Approved**: All criteria pass, no pending bugs
- **With warnings**: Passes but there are minor warnings
- **Rejected**: There are critical bugs that could not be resolved — escalate to the Tech Lead

## Example Session

```text
User: /qa-cycle

QA (sonnet) — Cycle 1: 2 of 5 criteria pass. Bug: form validation missing on email field.
Bugfix (sonnet) — Added email regex validation to UserForm component.
QA (sonnet) — Cycle 2: 5 of 5 criteria pass. 0 bugs.

Result: Approved.
```

## Subagent Configuration

When spawning QA or Bugfix agents via the Task tool, always use `subagent_type: "general-purpose"`. Guild agent role names are NOT valid Claude Code subagent_types.

Example:

```text
Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  prompt: "Read .claude/agents/qa.md and assume that role. Then: [task description]"
```

The `model` parameter is resolved from the step's `model-tier`: qa-validate and bugfix use execution→`"sonnet"`.
