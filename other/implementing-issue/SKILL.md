---
name: implementing-issue
description: Implements a single issue with TDD, code review, and fix loop. Use when a specific issue needs implementation -- either standalone or as part of orchestrated spec execution.
---

# Implementing Issue

## Overview

Implements a single MCP issue with TDD and automated code review. Designed for two use cases:

1. **Standalone** -- user invokes directly for a specific issue
2. **Dispatched** -- called as the unit of work from implementing-specs

**Entry point:** `/wrangler:implementing-issue ISS-XXXXXX`

## When to Use

- Implementing a specific issue (ISS-XXXXXX)
- Invoked directly for standalone work
- Dispatched as a subagent from implementing-specs

## When NOT to Use

- Implementing a full specification (use implementing-specs)
- Exploring code (use locating-code)
- Answering questions (just answer directly)

## Input

- **Issue ID** (required): e.g., `ISS-000042`
- **Working directory context** (optional): defaults to current directory

## Core Workflow

### 1. Setup

1. Read issue via `issues_get` MCP tool
2. Capture working directory and branch (see `references/working-directory-protocol.md`)
3. Understand requirements and acceptance criteria from the issue description

### 2. Implementation (TDD)

Follow the `practicing-tdd` skill strictly:

1. **RED** -- Write a failing test that captures the requirement
2. **GREEN** -- Implement the minimum code to make the test pass
3. **REFACTOR** -- Clean up implementation and tests
4. Commit work with a descriptive message

Repeat for each distinct requirement in the issue.

### 3. Code Review

1. Request code review using `requesting-code-review` skill
2. Parse feedback into severity categories:
   - **Critical** -- Must fix. Auto-fix with up to 2 attempts, escalate if both fail.
   - **Important** -- Must fix. Same 2-attempt process as Critical.
   - **Minor** -- Document only, do not fix.
3. Verify all Critical/Important issues resolved before proceeding

See `references/code-review-automation.md` for the detailed process.

### 4. Completion

1. Verify all tests pass
2. Provide TDD Compliance Certification (from practicing-tdd)
3. Verify git status (working tree clean, changes committed)
4. Report results:
   - Implementation summary (what was done)
   - Test results (pass count, coverage if available)
   - TDD Compliance Certification table
   - Commit hash
   - Any Minor issues noted for future cleanup

See `references/verification-checklist.md` for the full checklist.

## Blocker Detection

Only stop for genuine blockers. See `references/blocker-detection.md` for the full decision flowchart.

**Immediate escalation:**
- Unclear requirements (do not guess)
- Git conflicts (do not auto-resolve)

**Escalation after 2 attempts:**
- Persistent test failures
- Fix subagent cannot resolve the issue
- Missing dependencies that cannot be auto-installed

**Non-blockers (continue autonomously):**
- First test failure -- auto-fix
- Code review feedback -- auto-fix (2 attempts)
- Warnings -- document and continue

## Anti-Patterns

- Stopping to ask "should I continue?" when not blocked
- Guessing about unclear requirements instead of escalating
- Proceeding with failing tests
- Skipping code review
- Fixing Minor issues instead of documenting them

## Integration with Other Skills

- `practicing-tdd` -- TDD workflow (RED-GREEN-REFACTOR)
- `verifying-before-completion` -- Final verification checks
- `requesting-code-review` -- Code review dispatch and feedback parsing

## References

Detailed documentation in `references/` subdirectory:

- `working-directory-protocol.md` -- Location verification and command patterns
- `subagent-prompts.md` -- Subagent prompt templates (reviewer, fix agent)
- `code-review-automation.md` -- Review handling and fix loop process
- `verification-checklist.md` -- Completion verification steps
- `blocker-detection.md` -- Decision flowchart and escalation criteria
- `examples.md` -- Workflow examples

For workflow checklists, see `assets/workflow-checklist.md`.
