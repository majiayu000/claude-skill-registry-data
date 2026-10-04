---
name: triage-issue
description: Investigate a reported problem, diagnose root cause, and file a Beads issue with a behavior-level TDD fix plan.
---

# triage-issue

Investigate a bug report or broken behavior, find the root cause, and create follow-up work in Beads with a durable RED/GREEN fix plan. Keep the workflow mostly hands-off: ask only for the minimum problem statement, then investigate.

## When to use

- The user reports a bug, regression, confusing behavior, failing workflow, or production symptom.
- The user asks to triage, investigate, diagnose, or file an issue for a problem.
- You need a fix plan but should not implement the fix yet.

Do not use this skill for broad product planning, feature decomposition, or already-approved implementation work. Use `to-prd`, `to-issues`, or `tdd` instead when those are the actual request.

## Process

### 1. Capture the problem

Get one brief description of the issue from the user. If they have not provided one, ask exactly one clarifying question first:

> What's the problem you're seeing?

Do not start with a long questionnaire. Preserve any reported symptoms, expected behavior, reproduction hints, logs, affected environment, and impact, then begin diagnosis.

### 2. Load harness context first

Before source exploration, read relevant knowledge and repo guidance:

- `knowledge/_shared.yaml`
- `knowledge/repos/<repo>.yaml` for the affected repo, when present
- `repos/<repo>/AGENTS.md` and `repos/<repo>/CONTRIBUTING.md` when investigating a sub-repo
- Existing Beads context with `bd show <id>` when the report is attached to an issue

If a knowledge file is missing, note that briefly and continue. Do not let missing documentation block investigation.

### 3. Explore and diagnose

Trace the behavior far enough to identify root cause, not just the symptom. Investigate:

- Where the problem manifests: UI behavior, command output, API response, data mutation, or user-visible effect
- What public flow or contract is involved
- Why the current behavior fails
- Similar working patterns elsewhere in the codebase
- Existing tests and the behavioral coverage gap
- Recent relevant changes when history can explain a regression

Use a focused Explore subagent only when the codebase area is broad or unfamiliar. For small, local bugs, direct reading and targeted search are enough. Do not delegate merely to add ceremony.

Keep private diagnostic notes as needed, but keep the final issue durable. The issue should describe behaviors, contracts, and outcomes rather than fragile file paths, line numbers, or implementation details that could become stale after a refactor.

### 4. Identify the minimal fix approach

Before filing, decide:

- The smallest behavior change that addresses the root cause
- Whether this is a regression, missing validation, missing feature, data migration need, or design flaw
- Which public interfaces or user-visible workflows need verification
- What existing tests should remain green
- What risk remains if the diagnosis is uncertain

If root cause is not known, file an investigation task rather than pretending to know the fix. State the leading hypothesis and the evidence needed to confirm it.

### 5. Design the TDD fix plan

Write an ordered list of RED/GREEN cycles. Each cycle is one vertical slice:

```text
RED: Add one failing test that captures an observable broken behavior.
GREEN: Make the smallest code change that passes that test.
```

Rules:

- Test through public interfaces and observable outcomes.
- Prefer behavior assertions: API responses, command results, persisted data, rendered UI state, user-visible messages, emitted events.
- Avoid tests that assert private helper calls, internal state shape, line numbers, or current file layout.
- Add one failing test at a time; do not write all tests first and implementation afterward.
- Include a final REFACTOR step only after the planned tests are green.
- Make the plan resilient to radical internal refactors. A good plan reads like a spec, not a diff.

### 6. Choose Beads priority

Before creating a new Beads issue or changing an existing issue's priority, read and apply:

```text
.claude/skills/beads-priority-assignment/SKILL.md
```

Set an explicit priority on every created issue when the local `bd` CLI supports priority. If no urgency, impact, or deferral-risk signal exists, use the harness default `P2` / `2` / `medium`.

### 7. Create or update the Beads issue

Use Beads by default. Do not create a GitHub issue unless the user explicitly asks for GitHub or the repository's documented workflow requires it.

For a new issue:

```bash
bd create --type task --title "<durable behavior title>" --description "<issue body markdown>" --priority <value> --repo .
bd comments add <new-id> "worklog: triaged root cause; TDD fix plan added."
```

For an existing issue:

```bash
bd comments add <id> "worklog: triage result - <one-line root cause and TDD plan summary>."
bd update <id> --priority <value>
```

Use this issue body shape:

<issue-template>

## Problem

Describe the durable behavior:

- Actual behavior: what happens now
- Expected behavior: what should happen instead
- Reproduction: the shortest known path, if known
- Impact: who or what is affected

## Root Cause Analysis

Summarize the diagnosis:

- Public flow or contract involved
- Why the behavior fails
- Contributing factors
- Confidence level and remaining uncertainty, if any

Avoid file paths, line numbers, and implementation-specific diffs in this section. Mention modules only at the level a maintainer would still understand after a refactor.

## TDD Fix Plan

1. RED: Write a behavior test proving `<expected observable outcome>`.
   GREEN: Implement the smallest change that makes that behavior pass.

2. RED: Write a behavior test proving `<next important edge case or regression guard>`.
   GREEN: Extend the implementation only as needed for that behavior.

REFACTOR: Clean up duplication or naming after all planned tests pass, then rerun the relevant quality gates.

## Acceptance Criteria

- The reported behavior is reproduced by at least one failing test before the fix.
- The expected behavior is verified through public interfaces or user-visible output.
- The root cause is fixed without relying on brittle implementation details.
- New tests and existing relevant tests pass.

</issue-template>

After creating or updating the issue, report the Beads ID, chosen priority, and a one-line root-cause summary to the user.
