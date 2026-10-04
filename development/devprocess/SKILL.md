---
name: devprocess
description: |-
  Structured build workflow: branch, delegate to coding agent, test, screenshot, and commit.
  Triggers on: "$devprocess", "build this properly", "use the coding agent workflow", or any
  feature/refactor/infrastructure change that is too large for a direct edit.
  NOT for: one-line fixes, doc edits, prompt tweaks, or simple config changes — do those directly.
---

# $devprocess — How We Build

## Core Principle
You are the product partner. The coding agent is the worker for substantial code changes.
Do the framing, architecture, review, verification, and release decisions here. Delegate the heavy implementation work.

Small direct edits are fine for docs, prompts, tiny fixes, or surgical config changes. For feature work, refactors, or anything that needs exploration, use a coding agent.

## Before Every Feature

### 1. Read the Code First
- Read the repo structure and the relevant files before deciding anything.
- Reuse existing patterns before inventing new ones.
- For architecture questions, read `graphify-out/GRAPH_REPORT.md` first if it exists.

### 2. Create a Branch
```bash
git checkout -b <prefix>/<feature-name>
```
- Do not build features directly on `main`.
- One branch per logical change.

### 3. Write the Plan
Create `plans/<branch-name>/plan.md` with:
- **What** — what is being built
- **Why** — what problem it solves
- **How** — approach, touched files, constraints
- **Tests** — what must pass
- **Definition of done** — what proves completion

If the request is ambiguous or long-running, also create or update a lightweight spec first.

## During Development

### 4. Delegate the Build
- Use the coding-agent skill for substantial implementation.
- Give the coding agent the plan, target files, constraints, and definition of done.
- If the first pass is poor, tighten the brief and rerun.
- Do not accept unexplained large diffs.

### 5. Test
- Add or update tests with the change when appropriate.
- Run the smallest meaningful gate first, then the broader suite if needed.
- Do not claim success if tests are red.

### 6. Look at the Real UI
- Open the app or rendered output when there is any user-facing change.
- Take screenshots or snapshots when that is the best proof.
- Browser-visible bugs do not count as fixed until inspected visually.

### 7. Commit in Small Units
- One logical change per commit.
- Review the diff before each commit.
- Push often enough that work is safe.

## After Building

### 8. Measure
Capture before/after evidence when possible:
- tests added/passing
- load time or latency change
- bug reproduced then gone
- screenshot before/after
- error rate change

### 9. Review the Diff Yourself
- Read the patch like a reviewer.
- Check naming, duplication, edge cases, and fit with existing patterns.
- Revert sloppy code and rerun if needed.

### 10. Merge or PR
- If the change is verified and low risk: merge and ship.
- If risk or uncertainty remains: open a PR with a concise summary and ask for review.

## OpenClaw-Specific Defaults
- Prefer `sessions_spawn` with `runtime="acp"` when the owner explicitly wants Codex/Claude Code/Cursor/Gemini-style harness work.
- Prefer the bundled coding-agent workflow for substantial repo work when local execution is the right fit.
- After changing code files, run `graphify update .` when this repo uses graphify.
- Always leave the branch, plan, commits, and verification artifacts in a state another person can inspect.

## Anti-Patterns
- Writing a whole feature yourself without first deciding whether it should be delegated
- Starting on `main`
- No plan file
- One giant unreviewed commit
- Saying "tests pass" without running them
- Saying UI is good without opening it
- Shipping local-only work and calling it done
