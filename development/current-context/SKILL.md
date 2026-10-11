---
name: current-context
description: Detect branch, worktree session, and staged changes for devteam.
---

# Current Context Detection

Before executing any devteam command, identify the working context so that analysis and actions stay scoped to the right branch and files.

## Steps

Run these commands in order:

| Command | Purpose |
|---------|---------|
| `git branch --show-current` | Identify the active branch |
| `git diff --name-only HEAD` | List locally modified files |
| `git diff --name-only main...HEAD` | List all files changed in this branch vs main |
| Check `.dev-team-agents/.worktree-session` (if present) | Identify active worktree and its branch |

## Scope Rule

Restrict all analysis and actions to files and changes within the detected context. Do NOT scan or act on the full codebase unless the task explicitly requests a broader scope.

## Worktree Session

If `.dev-team-agents/.worktree-session` exists, read it before proceeding:
- `worktree=no` — operating on main working tree; no worktree isolation active
- `worktree=yes branch=<b>` — operating inside a worktree on branch `<b>`; load `skills/shared/worktree/SKILL.md` and follow its isolation protocol

If the file does not exist, assume the main working tree and proceed normally.

## Staged Changes

Use `git status --porcelain` to distinguish:
- `M ` (staged modifications) — already added to the index
- ` M` (unstaged modifications) — modified but not staged
- `??` (untracked files) — new files not yet tracked

This matters when the task involves committing or reviewing only staged work.

## Branch Freshness Check

After running the context commands, check if the branch is behind the remote main:

```bash
git fetch --quiet origin 2>/dev/null || true
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
```

If `BEHIND` is greater than 7:
- Warn the user: "This branch is N commits behind main. Consider rebasing before continuing."
- Offer three options: (a) rebase now, (b) continue anyway, (c) abort.
- If the user chooses (a), run `git rebase origin/main` and re-run the context detection.

If `git fetch` fails (no network), skip the check silently and proceed.

## Cache

Running 4 git commands on every invocation adds latency. Use a short-lived cache stored at `.dev-team-agents/user-data/.context-cache.json`:

```json
{ "ts": <unix-epoch-seconds>, "branch": "...", "changed": N, "worktree": "yes|no" }
```

**Read the cache first:**
```bash
CACHE=".dev-team-agents/user-data/.context-cache.json"
NOW=$(date +%s)
if [ -f "$CACHE" ]; then
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "")
    cached_branch=$(python3 -c "import json,sys; d=json.load(open('$CACHE')); print(d.get('branch',''))" 2>/dev/null || echo "")
    if [ -n "$CURRENT_BRANCH" ] && [ -n "$cached_branch" ] && [ "$cached_branch" != "$CURRENT_BRANCH" ]; then
        # Branch changed — invalidate cache
        rm -f "$CACHE"
    fi
fi
if [ -f "$CACHE" ]; then
    cached_ts=$(python3 -c "import json,sys; print(json.load(open('$CACHE'))['ts'])" 2>/dev/null || echo 0)
    age=$(( NOW - cached_ts ))
    [ "$age" -lt 1800 ] && echo "Context (cached): $(cat $CACHE)" && exit 0
fi
```

**Write the cache after detection:**
```bash
python3 -c "
import json, time
json.dump({'ts': int(time.time()), 'branch': '$BRANCH', 'changed': $CHANGED, 'worktree': '$WORKTREE'}, open('$CACHE','w'))
" 2>/dev/null || true
```

Cache TTL is 1800 seconds (30 minutes). On cache miss, branch change, or stale cache, run the full detection flow and write a fresh cache entry. If `python3` is unavailable, skip caching silently and always run the full detection.

---

## Summary Format

After running the commands, produce a one-line context header before any action:

```
Context: branch=<branch> | worktree=<yes|no> | changed=<N files>
```

This makes the working scope explicit to any subsequent agent or step.
