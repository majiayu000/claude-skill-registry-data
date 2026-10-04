---
name: session-pr-audit
description: >
  Audit what PRs this session produced. Ask: "What work did I do this session
  that isn't in a PR yet, or isn't merged?" Forces the agent to account for
  all code changes before declaring done. Use at any point — especially at
  session end, after a manager wave, or when asked "what's left?"
usage: /session-pr-audit
io-contract:
  kind: deliverable
  produces:
    - kind: report
      description: Accounting of the session's PRs, commits, and uncommitted work with unshipped-change flags
---

# Session PR Audit

You are performing a session PR audit — a durable-accountability check over
all code work done since this session started. The goal: surface any work that
exists as commits or local changes but has not been captured in an open PR,
has not been merged, or was superseded without a durable close note.

For manager-led waves, run this immediately after parley and before launching
the next wave. Every agent-authored change in the wave must be PR-accounted:
open and ready, queued, merged, or explicitly closed/superseded with a link to
the PR that mined it.

## Steps

1. **Identify the session's worktrees and branches**
   ```bash
   git worktree list
   git log --oneline origin/main..HEAD 2>/dev/null | head -20
   ```

2. **Find all branches pushed this session** (look at recent pushes in the
   reflog or list remote branches newer than main):
   ```bash
   git for-each-ref --sort=-committerdate refs/remotes/origin \
     --format='%(refname:short) %(committerdate:relative)' | head -20
   ```

3. **List open PRs to find which branches have PRs**:
   ```bash
   gh pr list --state open --json number,headRefName,title,url | head -40
   ```

4. **Identify orphans** — branches with commits not in any PR:
   - Compare pushed branches to open PRs
   - Note any branch with work that has no PR yet

5. **Check for local-only commits** (unpushed):
   ```bash
   git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline HEAD | head -10
   ```

6. **For each open PR found**, report its CI status:
   ```bash
   gh pr checks <number> --watch=false 2>/dev/null | tail -5
   ```

7. **Account for merged or closed PRs referenced by notes**
   ```bash
   gh pr view <number> --json state,mergedAt,closed,headRefName,url
   ```
   Closed is acceptable only when the close comment names the superseding PR,
   preserved branch, or deliberate abandonment reason.

## Output format

Report a concise table:

```
SESSION PR AUDIT
================
✓  #344  feat(console): sortie pane + FleetBar launcher     [open, CI pending]
✓  #306  feat(console): pd-console to main                  [open, CI red — blocked by #344 fix]
⚠  worktree-some-branch  — has 2 commits, NO PR yet
✗  feat/old-thing — local only, never pushed
```

Verdict:
- **All clear**: every commit is in a PR or merged
- **Orphans exist**: list them with the exact branch name and how to create the PR
- **Red CI**: list the PRs with red CI and what's failing
- **Superseded but accounted**: list the closed PR and the merged/mined PR that
  replaces it

## Obligation rule

Every code change in this session must eventually land as a PR. "I'll do it
later" is not acceptable for this audit. If there are orphans, either create
the PRs now or explicitly note them as deliberate WIP with a reason.

Every manager wave must leave the same accounting trail. "Agent finished" is
not a state; the acceptable terminal states are PR open, queued, merged, or
closed with a documented supersession.

This skill enforces the principle from ADR-0045 (loud-fail invariants): work
that evaporates without a PR is a coordination failure, not a normal outcome.
