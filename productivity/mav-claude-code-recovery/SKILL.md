---
name: mav-claude-code-recovery
description: Patterns for Claude Code workflow resilience — state persistence, crash recovery, command failure handling, subagent failure handling, and artefact durability. Not about application-level error handling.
user-invocable: false
disable-model-invocation: true
---

# Claude Code Error Handling and Recovery

Patterns for making Claude Code workflows resilient to failures. This covers Claude Code's own recovery mechanisms, not error handling in generated application code.

## Principles

1. **Persist state early and often** — checkpoint progress after each phase so work can be resumed
2. **Post artefacts immediately** — designs, plans, and status updates go to GitHub as soon as they are ready, not at the end
3. **Diagnose before retrying** — when something fails, understand why before trying again
4. **Verify before continuing** — on resume, confirm recorded state matches reality
5. **Isolate failures** — subagent failures stay in the subagent; fix via a new subagent, not by polluting the main session

## State Persistence

The `maverick-task-progress` marker on the GitHub issue is the single
state surface for issue-driven work (see
mav-github-issue-workflow): phase, branch, and artefact
comment ids, written via `uv run maverick task-progress set` **after**
each milestone completes — never before. Writing after completion means
the marker always reflects a consistent, completed milestone: if a
failure occurs mid-phase, the marker points at the last completed phase
and the incomplete phase re-executes from scratch.

Local files (worktrees, shortlists, diffs) are derivable caches. When a
local artefact and GitHub disagree, **GitHub wins**.

## Artefact Durability

Post artefacts to GitHub immediately after they are produced, via
`uv run maverick issue comment post --kind <design|plan|tasks|completion>`.

| Artefact | When |
|---|---|
| Solution design | Immediately after design is approved/produced |
| Implementation plan | Immediately after plan is approved/produced |
| Completion summary | After all steps pass verification |
| Blocking questions | When blocked and unable to resolve |

Batching artefacts to the end means a crash loses all intermediate work,
the human has no visibility, and recovery re-does the design/planning.

## Crash Recovery (Session Resume)

When starting a session that may be resuming previous work, do not
reconstruct the position by hand:

```bash
uv run maverick coord resume-point <repo> <issue>
```

The command reads the task-progress marker, locates the PR via the
recorded branch, inspects CI and the review verdict, and returns where to
resume with evidence. Then verify the physical prerequisites for that
resume point before acting:

| Check | Command |
|---|---|
| Branch exists locally / remotely | `git branch --list $BRANCH` / `git ls-remote --heads origin $BRANCH` |
| Expected commits present | `git log --oneline -5` |
| Issue still open | `gh issue view $ISSUE --json state -q '.state'` |

Common reconciliations: branch on remote but not local → fetch and check
out; branch nowhere but marker says `branch` → re-create from the story
base; issue closed → check whether a PR already merged (work may be
complete). When resuming, briefly report what was recovered and where you
are continuing from.

For **epic** recovery — DAG, epic-state, claims, in-flight block walks,
worktree reconciliation — follow `mav-durability-on-gh`
(cold-start hydration order) and `mav-block-propagation`
(resume an interrupted walk with `uv run maverick bprop run` **before any
other epic work**).

## Command Failure Handling

When a tool or command fails: read the error output, diagnose the root
cause, then fix — applying the canonical retry budget defined in
mav-plan-execution (two attempts → systematic debugging →
escalate).

### Rules

- **Never retry blindly** — the same command will produce the same failure.
- **Never brute-force past failures** — do not add `--force`, `--no-verify`, or `|| true` to make a failing command succeed. Fix the root cause.
- **Preserve error output** — include the actual error message when reporting to the user, not just "it failed".

## Subagent Failure Handling

When a subagent fails or returns incomplete results:

- **Partial result** → dispatch a new subagent with corrective context: what the previous one did, what it got wrong, what specifically to fix.
- **Total failure, scope too large** → split the task and dispatch smaller subagents.
- **Unclear cause** → report to the user.

### Rules

- **Do not fix subagent failures in the main session** — this pollutes the main context with debugging detail. Dispatch a new subagent.
- **Reduce scope on repeated failure** — if a subagent fails twice on the same task, split the task into smaller pieces.
- **Never silently swallow failures** — if a subagent fails and you cannot recover, report the failure clearly to the user.

<!-- maverick-plugin-version: 4.0.2-dev -->
