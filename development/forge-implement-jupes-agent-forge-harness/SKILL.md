---
name: forge-implement
description: Phase 3 of the Forge pipeline. Execute the plan's Beads tasks with red-green-refactor TDD, committing per checkpoint and pausing at each natural stopping point so the user can run a live demo or test and see the work themselves. Use when starting /forge-implement or the implement step of /forgemaster.
---

# forge-implement

Phase 3 of 4 in the Forge pipeline (research → plan → **implement** → ship). Input is the plan and
Beads graph from [[forge-plan]]; output is working, tested, committed code — built in observable
increments.

The defining rule of this phase: **stop at every checkpoint and let the user see it run.** Do not
silently barrel through the whole plan.

## When to Use

- The user runs `/forge-implement <slug>` or `/forgemaster` enters its implement phase.
- A `plans/drafts/<slug>.md` with checkpoints and a Beads issue map exists.

## Prerequisites

```bash
bun run forge:phase-gate implement --slug <slug>    # verifies the plan artifact exists
cat plans/drafts/<slug>.md                          # the build sequence + checkpoints
bd ready                                             # the tasks created in the plan phase
```

Beads must be reachable. If `bd` errors (e.g. Dolt server down), **stop** and fix it
(`bd dolt start`) — do not proceed without issue tracking.

## Process

### 1. Claim the first task

```bash
bd update <task-id> --claim     # sets assignee + status=in_progress (atomic, idempotent)
bd comments add <task-id> "worklog: starting implement (forge)"
```

Work tasks in dependency order. One task in progress at a time.

**Keep Beads current as you work** (do not batch all updates to the end):
- `--claim` moves the task `open → in_progress` — claim it *before* writing code, not after.
- Add a `worklog:` comment at each checkpoint and at any notable decision or pivot, so the issue
  reflects real progress: `bd comments add <task-id> "worklog: checkpoint A green — <demo cmd>"`.
- If a task gets stuck on something external, set `bd update <task-id> --status blocked` and add a
  `deps:` comment naming the blocker; file a new Beads issue for the blocker rather than going quiet.

### 2. Red-green-refactor per the TDD skill

For each behavior in the plan's TDD Strategy, follow `.claude/skills/tdd/SKILL.md` **vertically**:

```
RED:   write ONE test for the next behavior → it fails
GREEN: write the minimal code to pass → it passes
```

- One test at a time. Only enough code to pass the current test. No speculative features.
- Start with the tracer-bullet behavior to prove the path end-to-end.
- After the checkpoint's tests are green, **refactor** (extract duplication, deepen modules) and
  re-run tests. Never refactor while red.

Run `bun run typecheck` after each step and fix immediately.

### 3. Stop at the checkpoint — show the user

When a checkpoint's tests are green and typecheck passes, **pause** and give the user something to
run. This is the heart of the phase:

```
✅ Checkpoint <A> complete: <what now works>

See it yourself:
  <exact command> — e.g. `bun test <path>` or `bun run dev` → http://localhost:5173/<route>
Expected: <what they should observe>

Commit: <sha> — <message>
```

- If the checkpoint has a runnable surface, give the **exact** command/URL and the expected result.
- If the plan marked the checkpoint `(no live demo)`, say so and point to the passing tests as the
  evidence instead.
- Then ask whether to continue to the next checkpoint. Do not start the next checkpoint until the
  user has had the chance to look (under `/forgemaster` this gate is explicit).

### 4. Commit and close per checkpoint

```bash
git add <specific files for this checkpoint>
git commit -m "feat(<scope>): <checkpoint summary>

Refs: <task-id>"

# Close the task only with test evidence
bd comments add <task-id> "worklog: <behaviors> green; demo: <command>; tested: yes"
bd close <task-id>
```

Each closed task should map to something the user saw run. Commit tests alongside code (the quality
gate requires test files in recent commits).

### 5. Loop

Repeat steps 1–4 for each task/checkpoint until `bd ready` shows no remaining plan tasks.

### 6. Phase quality gate + hand off

```bash
bun run typecheck
bun run lint
bun test
git status --porcelain          # should be empty
bun run forge:phase-gate implement --slug <slug> --write    # records implement complete
```

Report the checkpoints completed and the tasks closed, then point to `/forge-ship <slug>`
(or `/forgemaster` continues).

## Hard Stops

- A checkpoint balloons past its planned scope (>8 files or >~200 lines): pause and report; consider
  splitting the Beads task before continuing.
- A behavior cannot be tested through the public interface: revisit the interface design with the
  user (see `.claude/skills/tdd/interface-design.md`) rather than testing implementation details.
- Quality gate fails twice after fixes: stop, file a Beads bug, escalate.

## Exit Criteria

- [ ] Every plan checkpoint reached green and was demoed (or marked `(no live demo)` with tests).
- [ ] Every plan Beads task closed with test evidence.
- [ ] typecheck + lint + tests pass; working tree clean.
- [ ] Forge state advanced to `implement` complete.
