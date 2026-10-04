---
name: resume
description: Recover session state from git, plans, and open PRs, then continue from the last completed phase without repeating work
triggers:
  - resume
  - pick up where I left off
  - continue session
  - continue from checkpoint
  - where was I
  - restore context
---

# Resume

Recover cold from a paused or crashed session. Figure out what was in-flight, where it stopped, and what to do next — without re-running completed work.

## When to Use

- New session starting after a crash, compaction, or hand-off
- Branch has uncommitted work or WIP commits and it's unclear where you were
- `.agents/plans/*.json` or `.loop-state.json` exists from a previous run
- An open PR on the current branch needs its loop resumed

## Detection Order

1. **Explicit handoff** — read `~/.claude/handoffs/<user>/latest.md` if present; it declares the next action.
2. **Plan state** — scan `.agents/plans/` for `*.json` state files; the newest one names the current phase and step.
3. **Git state** — `git status`, `git log -3`, and current branch. Uncommitted changes or a WIP commit means work stopped mid-phase.
4. **Remote state** — `gh pr list --head <branch>` reveals whether the branch is already pushed and reviewable.

## Decision Tree

```
Handoff file present?
├── Yes → follow its NEXT ACTION; archive on completion
└── No
    ├── Plan state exists?
    │   ├── Yes → jump to last-incomplete phase; skip done phases
    │   └── No
    │       ├── Branch has WIP commits / uncommitted diff?
    │       │   ├── Yes → diagnose intent from diff, commit or continue
    │       │   └── No → branch is clean; ask user what to do
    │       └── Open PR on branch?
    │           └── Yes → resume the loop targeting that PR (see `loop` skill)
```

## Rules

- **Never re-execute a completed phase.** If a phase has a commit or the plan marks it done, skip it.
- **Never guess intent from code alone.** Read the plan, the last commit message, and the handoff before deciding next action.
- **Do not start a new feature** during resume. If no open work is found, hand control back to the user.
- **Delegate recovery.** Corrupted plan file → use `self-heal`. Uncommitted WIP that must be stashed before branching → use `checkpoint`.

## Example Invocation

```bash
# session start — automatic in Claude Code global CLAUDE.md
cat ~/.claude/handoffs/$USER/latest.md 2>/dev/null

# explicit
cat .agents/plans/*.json | head -1
git log --oneline -5 && git status --short
gh pr list --head "$(git branch --show-current)" --json number,state,title
```

## Output

```text
Resume Report
─────────────
Source:   handoff | plan | git | pr
Phase:    <name> (step <N>/<M>)
Branch:   <name> @ <sha>
PR:       <url or none>
Next:     <concrete action to take>
Skipped:  <phases already done>
```

## Related Skills

- `checkpoint` — stash uncommitted WIP before switching branches during resume
- `self-heal` — recover from errors encountered while resuming (corrupt plan, missing files)
- `loop` — the autonomous cycle that resume re-enters at the right phase
- `context-save` — write state before a planned pause so the next resume has a clean anchor

## Exit Conditions

- **Found plan + phase**: print report, hand off to `loop` at the detected phase
- **No state found**: print "nothing to resume" and exit, do not start new work
- **Ambiguous state** (multiple plans, diverged branch): print findings, ask the user to pick
- **Corrupt plan file**: delegate to `self-heal`; do not delete evidence
