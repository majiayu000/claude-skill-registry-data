---
name: epcp-workflow
description: Apply the Explore → Plan → Code → Commit workflow for tasks like implementing features, fixing bugs, refactors, or adding integrations. Use this when the user wants changes in a repo and wants higher reliability (read first, plan then commit/PR). Emphasize subagents for investigation during Explore, and use "think / think hard / think harder / ultrathink" during Plan when alternatives exist.
---

# EPCP Workflow (Explore → Plan → Code → Commit)

This Skill enforces a high-signal workflow to avoid jumping straight into coding.

## Core rules

### 1) Explore (no code changes)
- Read relevant files first (configs, key modules, docs).
- If unclear, ask to inspect additional files rather than guessing.
- Prefer using subagents for parallel investigation when the task is complex.

### 2) Plan (before coding)
- Propose a concrete plan with steps + acceptance criteria.
- Call out risks, edge cases, and what you will *not* do.
- If multiple approaches exist, explicitly "think hard" and compare tradeoffs.

### 3) Code (implement + verify)
- Implement incrementally.
- Run tests/lint/build where applicable.
- Self-check that the result matches the plan and doesn't introduce unnecessary complexity.

### 4) Commit (clean history)
- Summarize changes.
- Stage only relevant files.
- Write a conventional commit message.
- If GitHub CLI is available, propose opening a PR.

## Anti-patterns to avoid
- Writing code before reading files.
- Making architectural leaps without checking existing patterns.
- Large refactors when a minimal patch solves the issue.
- Committing without running at least a minimal verification step.

## Templates
- Use this plan template: [templates/plan.md](templates/plan.md)
- Use this PR template: [templates/pr.md](templates/pr.md)

## Verification script
Run before committing: [scripts/precommit-check.sh](scripts/precommit-check.sh)

## Quick checklist (use every time)
- [ ] I read the key files first
- [ ] I wrote a plan with acceptance criteria
- [ ] I implemented in small steps
- [ ] I ran verification (tests/lint/build)
- [ ] I committed with a clear message (and PR if relevant)
