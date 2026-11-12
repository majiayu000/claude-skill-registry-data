---
name: ak-watzup
description: "Write short handoff reports from Git branches, remote refs, worktrees, unfinished plans and roadmap docs with ranked next steps."
when_to_use: "Invoke for what's in flight, detached worktrees or end-of-session status."
category: workflow
keywords: [session, wrap-up, changes, review, worktree, branches, plans, roadmap, priority, next-steps]
argument-hint: "[branch|worktree|status]"
metadata:
  author: agentkit
  version: "1.2.1"
---

# Wrap Up

Create a short, evidence-backed handoff report for the active project, with priority-ranked next steps grounded in plan progress and roadmap state.

This skill handles status and handoff reporting only. It does not implement, edit, commit, checkout, merge, push, or fetch unless the user explicitly requests fresh remote refs.

For conversation-state compaction that preserves decisions, rationale, and session
context for a fresh agent, use ak-handoff instead.

## Required Scan

Run the scanner first from the project root:

```bash
node scripts/watzup-scan.cjs --json
```

Use `--fetch` only when the user asks to refresh remotes before the report:

```bash
node scripts/watzup-scan.cjs --json --fetch
```

When developing from this source repository before install, run the same command from the source skill directory.

Default behavior:
- Scan local branches and remote branch refs.
- Scan registered worktrees.
- Scan unfinished plans from visible worktrees and tracked branch refs.
- Count `- [ ]` / `- [x]` checkboxes in each plan directory (plan.md + phase-*.md) for progress %.
- Scan `docs/*roadmap*.md` and `docs/*milestones*.md` for active milestones.
- Build priority-ranked next steps via composite scoring (see below).
- Do not run network operations.
- Do not change branches or mutate the checkout.

## Priority Ranking

The scanner now emits `nextSteps[]` as objects with `{priority, action, rationale, planId?}`. Ordering reflects a composite score per plan:

- **Status**: `in-progress` (+400) > `in-review` (+300) > `pending` (+150).
- **Workspace alignment**: current worktree (+600), current branch (+400).
- **Provenance**: filesystem source (+80), local ref (+40).
- **Momentum**: plans between 40-90% complete get bumped (close to done). Brand-new plans (<10%) get a small starter bump.

The scanner places hygiene steps (dirty working tree, detached HEAD) first and fills remaining slots with roadmap milestones. This is a heuristic, not a mandate: in the human report rank the user's current goal, release blockers, and demonstrated risk first. Explain any reranking and retain the raw scanner evidence. Dirty work alone is not a blocker or permission to discard it.

## Report Format

Keep output brief. Prefer this structure:

1. **Current State** - branch or detached HEAD, dirty/clean, active worktree.
2. **Recent Work** - only the highest-signal branches/worktrees.
3. **In-Flight Plans** - unfinished plans with `X/Y todos · NN% done` annotation.
4. **Roadmaps** - active milestones from `docs/*roadmap*.md`, if any.
5. **Next Steps** - 5 to 6 priority-ranked actions, each with one-line rationale.
6. **Warnings** - scanner failures, stale remote-ref caveat, detached HEAD.

If the scanner fails, say it failed and include the error. Then use minimal read-only fallback commands:

```bash
git status --short --branch
git worktree list --porcelain
git for-each-ref --format='%(refname:short) %(committerdate:iso8601) %(objectname:short) %(subject)' refs/heads refs/remotes
find plans -maxdepth 2 -name plan.md -print
find docs -maxdepth 2 -iname '*roadmap*.md' -print
```

Do not pretend the full scan completed when fallback was used.
