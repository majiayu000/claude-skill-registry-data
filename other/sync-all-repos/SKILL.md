---
name: sync-all-repos
description: Sync all GitHub-backed git repos on this machine with origin. Pulls behind repos, pushes ahead repos, reports dirty/non-main/conflict cases for Claude to resolve.
---

# Sync All Repos

Discover every GitHub-backed git repo on the current machine, classify each by sync state, auto-execute the obvious cases (clean repo behind/ahead/diverged from origin), and report the ambiguous cases (uncommitted changes, non-main branches, rebase conflicts) for Claude to resolve case by case.

Use this when:
- You sit down at the Mac or VPS and want to catch up with whatever the OTHER machine pushed to GitHub since last session
- You're about to walk away and want to ensure all committed-but-not-pushed work is on GitHub
- You suspect drift between machines and want a single-shot reconciliation

This skill does NOT:
- Coordinate Mac↔VPS directly (each machine syncs with GitHub independently)
- Auto-stash, auto-commit, or auto-resolve conflicts (Claude decides per case)
- Touch non-GitHub repos (gitlab, bitbucket, self-hosted git all skipped)
- Run on a timer (explicit invocation only)

## Step 1: Discover repos

Search roots:
- `~/Documents/GitHub/` (depth ≤2)
- `~/Documents/jira nbch/` (cds-dashboard, jira-nbch)
- `~/Documents/crm/`
- Any additional path in `$DOTFORGE_DIR/registry/projects.local.yml` not covered above

For each candidate directory at depth ≤2 with a `.git/` subdirectory:

```bash
REMOTE=$(git -C "$dir" config --get remote.origin.url 2>/dev/null)
case "$REMOTE" in
  *github.com*) ;;
  *) continue ;;  # non-GitHub: skip silently
esac

# Opt-out marker: project declares itself out of sync scope
if [[ -f "$dir/.dotforge-sync-ignore" ]]; then
  reason=$(head -1 "$dir/.dotforge-sync-ignore" 2>/dev/null)
  reason=${reason:-"opt-out (no reason given)"}
  echo "IGNORED|$dir|$reason"
  continue
fi

echo "$dir"
```

Skip silently:
- Directories without `.git/`
- Repos with no `origin` remote
- Repos with `origin` not pointing at GitHub

Skip with note (reported under "Ignored" in the final summary):
- Repos with a `.dotforge-sync-ignore` file at root. The first line of that file is shown as the reason. Use this for archived projects, vendored repos, or any GitHub-backed repo you deliberately don't want auto-synced. The marker is in the project's own working tree — version-controlled by that project, not by dotforge.

## Step 2: Classify each repo (with timeout + parallel)

**Critical**: wrap every git network operation (`fetch`) and tree-scanning operation (`status`) in a timeout. Without this, a single hung repo (DNS lag, large worktree, stale lock) blocks the whole sync. Process repos in parallel for speed.

Helper to detect the right timeout binary (macOS ships `gtimeout` via coreutils; Linux ships `timeout`):

```bash
if command -v gtimeout >/dev/null 2>&1; then T=gtimeout
elif command -v timeout >/dev/null 2>&1; then T=timeout
else
  # Fallback for systems without either — pure-bash timeout
  T() {
    local secs=$1; shift
    ( "$@" ) & local pid=$!
    ( sleep "$secs"; kill -TERM "$pid" 2>/dev/null ) & local watcher=$!
    wait "$pid" 2>/dev/null; local rc=$?
    kill "$watcher" 2>/dev/null
    return $rc
  }
fi
```

Use `${T} 30 git fetch ...` for every potentially-slow git call. Recommended timeouts:
- `git fetch`: 30s (network)
- `git status --porcelain`: 20s (large worktrees)
- `git rev-list --count`: 5s (cheap, just in case)

### Per-repo classification function

Run as a subshell so a single hung repo can't poison shared state, and each invocation writes its result to a unique temp file (avoids interleaved stdout from parallel runs):

```bash
classify_one() {
  local repo=$1 outdir=$2
  local out="$outdir/$(echo "$repo" | tr '/' '_').out"
  local name=$(basename "$repo")

  local branch dirty fetch_rc behind ahead last
  branch=$(git -C "$repo" branch --show-current 2>/dev/null)
  branch=${branch:-?}

  if ! ${T} 20 git -C "$repo" status --porcelain >/dev/null 2>&1; then
    printf '%s|stalled|%s|status timeout\n' "$repo" "$branch" > "$out"; return
  fi
  dirty=$(${T} 20 git -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')

  if ! ${T} 30 git -C "$repo" fetch origin --quiet 2>/dev/null; then
    printf '%s|unreachable|%s|fetch failed or timeout\n' "$repo" "$branch" > "$out"; return
  fi

  behind=$(${T} 5 git -C "$repo" rev-list --count HEAD..@{u} 2>/dev/null || echo 0)
  ahead=$(${T} 5 git -C "$repo" rev-list --count @{u}..HEAD 2>/dev/null || echo 0)
  last=$(${T} 5 git -C "$repo" log -1 --format='%h %s' 2>/dev/null)

  local state detail
  if [[ "$dirty" -gt 0 ]]; then
    state=dirty; detail="${dirty} files; ${behind}↓/${ahead}↑"
  elif [[ "$branch" != "main" && "$branch" != "master" ]]; then
    state=non-main; detail="${behind}↓/${ahead}↑"
  elif [[ "$behind" -eq 0 && "$ahead" -eq 0 ]]; then
    state=in-sync; detail="—"
  elif [[ "$behind" -gt 0 && "$ahead" -eq 0 ]]; then
    state=behind; detail="${behind} commits"
  elif [[ "$behind" -eq 0 && "$ahead" -gt 0 ]]; then
    state=ahead; detail="${ahead} commits"
  else
    state=diverged; detail="${behind}↓/${ahead}↑"
  fi
  printf '%s|%s|%s|%s|%s\n' "$repo" "$state" "$branch" "$detail" "$last" > "$out"
}
export -f classify_one
export T
```

### Parallel execution

**Critical**: paths can contain spaces (e.g., `~/Documents/jira nbch/cds-dashboard`). Always pipe **null-delimited** input to `xargs -0` — newline-delimited splits on whitespace and corrupts paths with spaces.

```bash
OUTDIR=$(mktemp -d)
# REPOS array comes from Step 1 (filtered, github-only, not ignored)
printf '%s\0' "${REPOS[@]}" | \
  xargs -0 -n 1 -P 8 -I{} bash -c 'classify_one "$1" "$2"' _ {} "$OUTDIR"

# Collect results — sort alphabetically for stable output
RESULTS=$(cat "$OUTDIR"/*.out 2>/dev/null | sort)
rm -rf "$OUTDIR"
```

The `-P 8` runs up to 8 repos concurrently. Adjust `-P` based on the machine (Mac M-series: 8; VPS Oracle ARM: 4 to leave headroom). On a 15-repo workload, parallel finishes in ~30-60s (Mac M, mixed cold/warm caches) vs 3+ min sequential.

### State table

| State | Trigger | Action in Step 3 |
|-------|---------|------------------|
| `unreachable` | fetch timeout or fail | Skip with warning. Don't fail the rest. |
| `stalled` | status timeout | Skip with warning. Repo has a huge worktree or stuck git lock. |
| `non-main` | `branch` not main/master | Report only. User may be on a feature branch deliberately. |
| `dirty` | `dirty > 0` | Report with branch + `git diff --stat` + last commit. **NO automatic action.** Defer to Claude. |
| `in-sync` | clean + main + 0/0 | No-op. |
| `behind` | clean + main + N↓/0↑ | Auto: `${T} 60 git pull --rebase` |
| `ahead` | clean + main + 0↓/M↑ | Auto: `${T} 60 git push` |
| `diverged` | clean + main + N↓/M↑ | Auto: `${T} 60 git pull --rebase` then push. If rebase fails, `git rebase --abort` and report. |
| `conflict` | rebase failed | Already aborted in `diverged` flow. Report and let Claude decide. |

## Step 3: Execute auto-actions (also parallel + timed)

For each repo classified as `behind`, `ahead`, or `diverged`, run the action with timeout. Pattern mirrors Step 2: subshell per repo, write result to a tempfile, parallelize via xargs, collect at the end.

### Push retry helper (transient failures + non-FF recovery)

Lessons from the first real run: (a) ~5% of pushes fail transiently (network blip, slow remote auth) and succeed on the next attempt; (b) between classify and action, another machine may have pushed — so an `ahead` state's push fails with non-fast-forward. Both are recoverable in-line:

```bash
_smart_push() {
  local repo=$1
  # First attempt
  if ${T} 60 git -C "$repo" push --quiet 2>/dev/null; then return 0; fi
  # Retry once (transient network failure)
  sleep 1
  if ${T} 60 git -C "$repo" push --quiet 2>/dev/null; then return 0; fi
  # Still failing — likely non-fast-forward. Try pull-rebase, push.
  if ${T} 60 git -C "$repo" pull --rebase --quiet 2>/dev/null; then
    ${T} 60 git -C "$repo" push --quiet 2>/dev/null && return 0
  else
    git -C "$repo" rebase --abort 2>/dev/null
  fi
  return 1
}
export -f _smart_push
```

### Action runner

```bash
act_one() {
  local repo=$1 state=$2 outdir=$3
  local out="$outdir/$(echo "$repo" | tr '/' '_').out"
  case "$state" in
    behind)
      if ${T} 60 git -C "$repo" pull --rebase --quiet 2>&1; then
        echo "$repo|pulled" > "$out"
      else
        git -C "$repo" rebase --abort 2>/dev/null
        echo "$repo|pull-conflict" > "$out"
      fi ;;
    ahead)
      if _smart_push "$repo"; then
        echo "$repo|pushed" > "$out"
      else
        echo "$repo|push-failed" > "$out"
      fi ;;
    diverged)
      if ${T} 60 git -C "$repo" pull --rebase --quiet 2>&1; then
        if _smart_push "$repo"; then
          echo "$repo|reconciled" > "$out"
        else
          echo "$repo|pull-ok-push-failed" > "$out"
        fi
      else
        git -C "$repo" rebase --abort 2>/dev/null
        echo "$repo|rebase-conflict" > "$out"
      fi ;;
  esac
}
export -f act_one

# Build action list from Step 2 RESULTS, filter to actionable states
ACTION_LIST=$(echo "$RESULTS" | awk -F'|' '$2 ~ /^(behind|ahead|diverged)$/ {print $1"|"$2}')
ACTOUT=$(mktemp -d)
# Null-delimited to survive paths with spaces
printf '%s\0' $ACTION_LIST | xargs -0 -n 1 -P 8 -I{} bash -c '
  IFS="|" read -r repo state <<< "$1"
  act_one "$repo" "$state" "$2"
' _ {} "$ACTOUT"

ACTIONS=$(cat "$ACTOUT"/*.out 2>/dev/null | sort)
rm -rf "$ACTOUT"
```

`_smart_push` makes up to 3 attempts total (push, push, pull-rebase+push). If all three fail, the repo lands in `push-failed` / `pull-ok-push-failed` for manual investigation. This handles the two common in-the-wild causes: transient network and concurrent push from another machine.

## Step 4: Build structured report

Two-section output: a one-line discovery summary + the per-state breakdown with aligned columns.

### Header — one-line discovery summary

```
═══ SYNC-ALL: <N> repos discovered (<M> GitHub-backed, <K> ignored, <S> skipped non-github) ═══
```

### Body — categorical breakdown

Use a fixed-width table format (40-char repo column + 14-char state + 16-char branch + rest for detail). Stable column widths across categories make it scannable.

```
STATE         REPOS                                   DETAIL
─────         ─────                                   ──────

✓ Pulled (N)
                <repo>                                was behind by N
                <repo>                                was behind by M

✓ Pushed (M)
                <repo>                                was ahead by N

✓ Reconciled (K)
                <repo>                                pulled N, pushed M

= In-sync (J)
                <repo>, <repo>, <repo>                (compact list)

⚠ Dirty — DEFERRED to Claude (X)
                <repo> [<branch>]                     <D> files; <B>↓/<A>↑
                  last: <hash> <subject>
                  diffstat:
                    <file1>: +X -Y
                    <file2>: +X -Y
                    (… N more)

⚠ Non-main — skipped (Y)
                <repo>                                on <branch>; <B>↓/<A>↑

⚠ Conflicts — manual intervention (Z)
                <repo>                                rebase aborted, diverged remained

✗ Unreachable (W)
                <repo>                                fetch timeout/failed

✗ Stalled (T)
                <repo>                                git status hung — repo may be corrupt or worktree huge

⊘ Ignored (V)
                <repo>                                <reason from .dotforge-sync-ignore>
```

### Counter line at the end

```
═══ TOTAL: pulled=N pushed=M reconciled=K in-sync=J dirty=X non-main=Y conflicts=Z unreachable=W stalled=T ignored=V ═══
```

Categories with count 0 are omitted from the body but still appear in the counter line for completeness.

## Step 5: Claude resolves dirty cases

For each repo in the `Dirty` section, Claude decides what to do based on the diff and session context:

1. Run `git -C <repo> diff` to see what's changed
2. Run `git -C <repo> log -5 --oneline` to see recent commits for context
3. Decide:
   - **Skip**: user is mid-edit on something they haven't finished. Leave it alone, note in summary.
   - **Commit WIP**: changes look like a coherent unit. Compose a descriptive commit message and stage **with worktree exclusion** (see below), then push.
   - **Stash**: changes don't fit a clean commit but need to clear the tree to pull. `git stash push -m "sync-all auto-stash <date>"`, pull, optionally `git stash pop`.
   - **Ask user**: if intent is genuinely unclear, surface via AskUserQuestion with the diff.

### CRITICAL — Staging exclusions for dotforge-managed repos

Many managed projects have `.claude/worktrees/<agent-worktree>/` directories. These are dotforge's internal agent worktrees: each is its own `.git` (a submodule reference from the outer repo's perspective). If you `git add .claude/` or `git add -A`, git silently adds them as embedded git references, polluting the commit history with submodule pointers that have no meaning.

**Always stage with explicit exclusion** when targeting `.claude/`:

```bash
# Right — pathspec exclusion preserves the intent of "everything .claude except worktrees"
git -C "$repo" add ".claude/" ":!.claude/worktrees/"

# Alternative — stage modified, then add untracked excluding worktrees
git -C "$repo" diff --name-only --diff-filter=M | xargs -d '\n' git -C "$repo" add --
git -C "$repo" ls-files --others --exclude-standard | grep '^\.claude/' | grep -v '^\.claude/worktrees/' | xargs -d '\n' git -C "$repo" add --

# Wrong — adds worktrees as embedded git refs
git -C "$repo" add .claude/        # ← causes "warning: adding embedded git repository"
git -C "$repo" add -A              # ← same
```

Verify before committing:

```bash
git -C "$repo" diff --cached --name-only | grep '\.claude/worktrees/' && {
  echo "ERROR: worktree accidentally staged — abort"
  git -C "$repo" reset --quiet
  return 1
}
```

Other paths to never auto-stage even when present in `.claude/`:
- `.claude/session/` — ephemeral session state (last-compact.md, last-startup.md, startup-history/)
- `.claude/.forge/runtime/` — v3 behavior state file (per-machine, gitignored normally but sometimes leaks)

Same pattern: pass them as `:!.claude/session/` and `:!.claude/.forge/runtime/` exclusions.

Apply the decision per repo using Bash directly. Do NOT loop back through the skill — this phase is Claude's orchestration.

## Step 6: Handle non-main branches

For each repo on a non-main branch (reported in step 4), ask one question collectively rather than per-repo:

> Found N repos on non-main branches: <repo1> on <branch1>, <repo2> on <branch2>...
> Want me to sync these branches with their tracking origin (same logic: pull/push/report)?

If yes, re-run steps 2-4 on those repos. If no, skip.

## Step 7: Final summary

After all dirty cases and non-main branches are resolved, emit the final counter:

```
═══ FINAL ═══
Total repos discovered: T
Pulled:    N
Pushed:    M
Synced:    K (in-sync, no action)
Dirty resolved: J (X committed, Y stashed, Z skipped)
Conflicts remaining: C
Unreachable: U
```

## Edge cases

- **`~/Documents/GitHub/dotforge` is included**: sync it LAST, after every other repo is done. If the pull brought new commits, surface:
  > dotforge updated to v<new-version>. The new skills/hooks are on disk but the current Claude session is still using the old version. Restart Claude to pick up the update.
  Do NOT auto-restart.
- **Repo doesn't exist on this machine**: search-roots-based discovery skips it silently. No error.
- **Repo is a submodule**: detect via `.git` being a file (not a directory). Skip submodules — they're managed by their parent.
- **Repo has a non-`origin` GitHub remote**: only `origin` is considered. If you push to multiple GitHubs, you're outside the scope of this skill.
- **Stuck Claude-managed worktrees block branch checkout**: post-v2.1.x changelog (verify exact version), Claude-managed worktrees auto-unlock on agent finish. Pre-fix, they kept the git lock and broke `git checkout main` with `'main' is already used by worktree at ...`. Detection during sync: for any repo, run `git -C "$repo" worktree list --porcelain | awk '/^worktree/ {print $2}' | grep "$repo/.claude/worktrees/"` to find Claude-managed worktrees still registered. If a worktree's branch has no unique commits vs origin AND no uncommitted work, propose cleanup: `git worktree remove <path>` + `git branch -D <branch>` + `git worktree prune`. Lived 2026-06-01 — TRADINGBOT's `claude/festive-maxwell-a70698` and `heuristic-swartz-65163d` blocked main checkout mid-sync.

## Constraints

- NEVER `git push --force` from this skill, even after a rebase. If push fails, report and stop on that repo.
- NEVER auto-commit changes to `.env`, `*.key`, `*.pem`, `**/secrets*` files. If a dirty repo's diff includes those paths, force "Skip" or "AskUserQuestion" — never WIP-commit.
- NEVER touch repos under `.claude/worktrees/` — those are dotforge's internal agent worktrees, not real project state.
- Always run `git fetch` BEFORE classifying. Without an up-to-date `@{u}`, behind/ahead counts are stale.
