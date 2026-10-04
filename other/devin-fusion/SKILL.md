---
name: devin-fusion
description: Run a Devin Fusion session — pair a frontier main agent with a cheap sidekick agent to reduce cost while keeping frontier quality. Use for complex engineering tasks with both judgment-heavy and mechanical parts.
---

# Devin Fusion — Multi-Model Sidekick Harness

## When to use

- The task mixes **judgment** (architecture, ambiguous requirements, final review) and **mechanics** (search/replace, bulk edits, slow tests).
- You want to reduce token cost without sacrificing final quality.
- The task is large enough to benefit from splitting into planned sub-tasks.

## Core pattern

Run two reasoning loops:

1. **Main loop** — frontier reasoning. Plans, interprets ambiguity, delegates, monitors, decides, reviews.
2. **Sidekick loop** — cost-effective execution. Reads/writes files, runs tests, applies repetitive edits, reports back.

Both loops keep persistent, independently cached context. The Main loop delegates via explicit sub-tasks; the Sidekick loop returns structured reports.

## Step-by-step workflow

### 1. Classify the request

Rate along two axes:

- **Judgment load** — does success depend on subtle intent, architecture, or product taste?
- **Mechanical load** — are there many files, repetitive edits, or slow verifications?

### 2. Build the plan

Produce a short, ordered plan. Tag each step:

- `[main]` — requires judgment, planning, or final review.
- `[sidekick]` — mechanical, well-scoped, executable with minimal decisions.

Example:

```markdown
1. [sidekick] List all files importing `OpenTracing`.
2. [sidekick] Remove those imports and calls, preserving behavior.
3. [main] Review the diff for missed edge cases.
4. [sidekick] Run `bun test` and report failures.
5. [main] Finalize and summarize.
```

### 3. Delegate sidekick steps

When running a `[sidekick]` step, open a clear sub-task context:

```markdown
**Context:** [2-3 sentences]
**Goal:** [concrete outcome]
**Constraints:** [what to preserve / avoid]
**Return format:** [files changed, key diffs, test results, blockers]
**Allowed decisions:** [none by default]
```

### 4. Execute sidekick steps

As the sidekick:

- Gather only local context.
- Prefer mechanical tools.
- Do not make architectural or product decisions.
- Stop if ambiguous or blocked.
- Return a structured report.

### 5. Review and route

After each sidekick report, the main loop decides:

- ✅ Accept and continue.
- 🔁 Send back for rework.
- 🚀 Escalate to main because judgment is needed.
- 🔄 Upgrade the sub-task to a stronger reasoning pass.

### 6. Final review

The main loop verifies:

- Original request satisfied.
- No regressions.
- Tests / lint / typecheck pass.
- Implementation is as simple as possible.

## State file

Maintain a shared state file at `.opencode/fusion-state.json` (or `.agents/fusion-state.json`):

```json
{
  "plan": [ ... ],
  "currentStep": 2,
  "sidekickReports": [ ... ],
  "decisions": [ ... ]
}
```

Both loops update this file to stay synchronized without losing cached context.

## Heuristics

### Delegate to sidekick

- Searching, listing, summarizing.
- Repetitive edits across files.
- Running tests, linters, type checks.
- Removing dead code or mechanical deprecations.
- Generating boilerplate from a clear spec.

### Keep on main

- Architecture decisions.
- Interpreting ambiguous requirements.
- Designing public APIs or data models.
- Final review and approval.
- Any task where "the judgment is the deliverable".

### Escalate sidekick → main

- Sidekick fails twice on the same sub-task.
- Ambiguity or product intent appears.
- The diff feels wrong.

## Cost discipline

- Main loop minimizes direct file reads and edits.
- Sidekick loop never reasons about scope or intent.
- Avoid sidekick overhead for trivial one-line tasks.
- Split large sidekick tasks into smaller, verifiable chunks.

## Verification checklist

- [ ] All delegated steps accepted or escalated.
- [ ] Tests / lint / typecheck pass.
- [ ] State file is up to date.
- [ ] Concise summary returned to user.

