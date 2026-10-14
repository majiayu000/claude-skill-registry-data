---
name: feature-dev-orchestrator
description: Use when you want to describe a change, feature, or project and have it driven end-to-end through discovery, planning, approval, task breakdown, implementation, testing, and fix-until-done loops with minimal human re-intervention.
risk: safe
source: community
date_added: "2026-06-12"
---

# Feature Dev Orchestrator

## Overview

Turn a raw request (change, feature, or project) into a verified, working implementation through a structured loop:
**grill → plan → approve → decompose → implement → test → fix → repeat until done.**

Core rule: **do not move forward without alignment; do not stop without evidence.**

## When to Use

- You want to describe a feature or change in natural language and have it driven to completion autonomously.
- You need structured checkpoints (grill, plan approval, final acceptance) without manual coordination.
- You want the agent to break large work into small, testable, atomic steps and iterate until all pass.

## Required Sub-Skills

- `grill-me` — discovery and requirements hardening
- `request-refactor-plan` — structured implementation planning
- `tdd` — test-driven implementation loop
- `verification-before-completion` — acceptance gate

Optional supporting skills:
- `grill-with-docs` — when an existing domain model must be respected
- `to-issues` — export tasks as GitHub issues
- `codex-review` — automated code review before final merge
- `git-ship` — branch, commit, and PR creation
- `uv` - when managing Python projects
- `python-pro` - when writing or reviewing Python 3.12+ codebases
- `playwright-skill` - when writing or reviewing web UI tests and automations
- `handoff` - when you need to hand off work to another agent
- `security-aud` - when you need to audit the code for security vulnerabilities


## Inputs

Require these inputs before starting:
- **Request**: free-text description of the change, feature, or project
- **Scope**: file(s), module(s), or service(s) affected (or "unknown" to derive during grill)
- **Acceptance Criteria (DoD)**: explicit pass/fail conditions (or "none yet" to derive during grill)

Fixed defaults:
- max fix-loop rounds = `3`
- plan approval timeout = human gate (no auto-proceed)
- task granularity target = steps completable in ≤ 30 min each

## State Machine

```
intake → grilling → plan-draft → plan-approved → decomposed → implementing → testing → fixing → accepted
                                                                                           ↑_________↓ (loop, max 3)
                                     ↓                                                               ↓
                               plan-rejected                                                    escalated
```

States:
- `intake` — raw request received, inputs validated
- `grilling` — discovery questions asked; requirements hardened
- `plan-draft` — implementation plan written to file, awaiting approval
- `plan-approved` — human approved; task decomposition begins
- `plan-rejected` — human requested changes; return to `plan-draft`
- `decomposed` — plan split into tasks, tasks split into atomic steps
- `implementing` — steps executed sequentially
- `testing` — tests run against completed implementation
- `fixing` — failures addressed; round counter incremented
- `accepted` — all DoD criteria verified with evidence
- `escalated` — max rounds exceeded or blocker cannot be resolved

## Workflow

### 1. Intake
- Receive the free-text request.
- Validate that Scope and DoD are present (or marked "none yet").
- If any required input is missing and cannot be inferred, ask before proceeding.

### 2. Grill
- Invoke `grill-me` (or `grill-with-docs` if a domain model exists).
- Ask targeted questions until the following are unambiguous:
  - What exactly changes and what must not change.
  - Edge cases and error paths that must be handled.
  - Explicit, testable acceptance criteria (DoD).
  - Any external dependencies, secrets, or permissions needed.
- Do **not** write any code during this phase.

### 3. Plan draft
- Write a structured implementation plan to `plan.md` in the session folder covering:
  - Problem statement and constraints
  - High-level approach and alternatives considered
  - Task list (coarse-grained, ordered)
  - Risk register
- Present the plan to the user and **wait for explicit approval or change requests**.
- On rejection, revise and re-present; no iteration cap on plan revisions.

### 4. Decompose
- Once approved, break each task into atomic steps (≤ 30 min each).
- Persist steps in the session SQL database (`todos` table) with status `pending`.
- Identify and record dependencies between steps (`todo_deps` table).
- Show the full step list to the user before starting execution.

### 5. Implement
- Execute steps in dependency order, marking each `in_progress` → `done`.
- Follow `tdd` discipline: write/update tests before or alongside implementation.
- After each step, run the smallest targeted test command that covers the change.
- Do not proceed to the next step while the current step's tests are red.

### 6. Test
- After all steps are `done`, run the full test suite.
- Collect all failures into a fix list.

### 7. Fix loop
- For each failure: diagnose root cause, apply fix, re-run targeted tests.
- After all failures are addressed, re-run the full suite.
- Increment the round counter. If all tests pass, proceed to acceptance gate.
- If the round counter hits `3` and failures remain, move to `escalated`.

### 8. Acceptance gate
- Invoke `verification-before-completion`.
- Map every DoD criterion to concrete evidence (test output, logs, API response, etc.).
- Only move to `accepted` when every criterion has a matching evidence item.

## Stop Conditions

Move to `accepted` only when:
- Every DoD criterion has matching, fresh evidence.
- Full test suite passes.
- No open blockers.

Move to `escalated` when any of the following occur:
- DoD still fails after `3` full fix rounds.
- Missing secrets, permissions, or external dependencies block progress.
- A required operation is destructive or affects production without explicit approval.
- Grilling reveals conflicting constraints that cannot both be satisfied.
- Acceptance criteria are missing and the user cannot provide them.

## Human Gates

Always stop and wait for human confirmation before:
- Proceeding past `plan-draft` (explicit approval required).
- Any deploy to staging or production.
- Destructive git or data operations (force-push, migration with data loss, drop table).
- Billing, IAM, or security posture changes.
- Any action outside the agreed scope discovered during implementation.

## Output Contract

At every state transition, report:

| Field | Content |
|---|---|
| **State** | Current state machine node |
| **Completed Steps** | Checklist of done steps |
| **Next Step** | What happens next |
| **Acceptance Criteria** | Pass ✅ / Fail ❌ / Pending ⏳ per criterion |
| **Evidence** | Commands, test output, logs, or API results |
| **Open Risks** | Anything still uncertain |
| **Need Human Input** | Smallest next decision required, if blocked |

Do **not** report "done" unless state is `accepted`.

## Limitations

- Use this skill only for software changes that can be implemented, tested, and verified within the current environment.
- Do not use for tasks requiring production access, customer data, or approvals outside the agreed scope without explicit human gates.
- Stop and escalate if required inputs, permissions, safety boundaries, or success criteria cannot be established.
- This skill coordinates other skills; it does not replace environment-specific validation, security review, or expert judgment.
