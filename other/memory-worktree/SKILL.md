---
name: memory-worktree
description: |
  Verify, customize, or opt out of moflo's AUTOMATIC durable-learning sharing across git worktrees /
  Conductor workspaces on one machine. As of the worktree-auto-sharing change this is on by default —
  learnings converge across a repo's worktrees with no setup. Use when the user asks "is memory shared
  across my worktrees?", "where are my worktree learnings stored?", "turn off worktree memory sharing",
  "share learnings across my separate clones", or "point my worktrees at a custom store". For a team or
  cross-machine (git-tracked) sharing, use /memory-team instead.
arguments: "[--off | --path <store>]"
---

# /memory-worktree — Durable Sharing Across Worktrees (Automatic)

Working across git worktrees is a core moflo competency, so durable-learning sharing across the
worktrees of a repo is now **automatic and on by default**. When a checkout is part of a repo with
worktrees in play, moflo derives a shared durable store at **`<git-common-dir>/moflo/durable.db`** and
converges the `learnings` + `knowledge` namespaces across every worktree at session start — no config.
A plain single checkout writes nothing and behaves exactly as before.

This skill is for the three things you might still want: **verify** it's working, **customize** where it
stores (or extend it to non-worktree clones), or **opt out**.

> Only the durable slice travels. Structural + ephemeral data stays local per checkout and rebuilds
> itself — the same safety model the auto path is built on (a dedicated `durable.db`, never a full
> `moflo.db`). See [[memory-team]] for the git-tracked, cross-machine variant.

**Arguments:** `$ARGUMENTS` — `--off` to opt out, `--path <store>` to set a custom shared store.

## When to use

- "Is memory / are learnings shared across my worktrees?" → **verify** (Step 1).
- "Where are my worktree learnings stored?" → it's `<git-common-dir>/moflo/durable.db`; verify to confirm.
- "Turn off / disable worktree memory sharing" → **opt out** (Step 2).
- "Share learnings across my separate clones / a custom location" → **customize** (Step 3).

For a team, or your own laptop+desktop over git, that's `/memory-team`, not this.

## Procedure

### Step 0 — Memory first (gate requirement)

```
mcp__moflo__memory_search { query: "durable_path worktree sharing auto git common dir learnings", namespace: "guidance" }
```

### Step 1 — Verify (default action)

Run the safety/status check and surface it verbatim:

```bash
npx flo doctor -c shared-db 2>&1
```

- **"Automatic worktree learning sharing active (<path>)"** → it's working; the path is the shared store.
- **"No shared full moflo.db detected…"** → auto sharing is NOT active here. Most likely this checkout
  has no sibling worktrees yet (auto only turns on once worktrees exist). Confirm with the user; if they
  expected sharing across *separate clones* (not worktrees), go to Step 3 — auto can't converge those.
- **A `warn`** → a full-DB misconfig is present; follow the check's `fix` line.

To see that learnings actually converged, from a second worktree:

```bash
npx flo memory list --namespace learnings 2>&1 | head
```

### Step 2 — Opt out (`--off`)

If the user wants it off, set the toggle in the project-root `moflo.yaml` (preserve other `memory:` keys):

```yaml
memory:
  worktree_sharing: false
```

Explain: this stops the auto flush/seed at session start. Anything already converged into a worktree's
local DB stays; nothing new propagates. Takes effect next session.

### Step 3 — Customize the store (`--path`, or non-worktree clones)

Setting an explicit `memory.durable_path` **overrides** the auto derivation — use it to:
- put the shared store somewhere other than `.git/moflo/` (e.g. a synced/backed-up location), or
- converge checkouts that are **separate clones**, not git worktrees (auto only covers worktrees, since
  only worktrees share a git common dir).

```yaml
memory:
  durable_path: ~/.moflo-shared/<repo-name>-learnings.db
```

The path must live outside any single checkout and must **not** be named `moflo.db`. Create the parent
dir with a Node primitive (cross-platform — never `mkdir -p`):

```bash
node -e "const p=require('path'),fs=require('fs');fs.mkdirSync(p.dirname(process.argv[1]),{recursive:true})" "<chosen-store-path>"
```

Then re-run `npx flo doctor -c shared-db` to confirm it reports the durable-only store as safe.

## Output

End with a single-block summary of what state you left it in, e.g.:

```
Worktree Memory Sharing
────────────────────────
Mode:         automatic (default)  |  custom durable_path  |  disabled
Store:        <git-common-dir>/moflo/durable.db  (or the custom/none path)
Config:       memory.worktree_sharing / memory.durable_path
Verify:       npx flo doctor -c shared-db
Scope:        learnings + knowledge only (structural stays local)
```

## Rules

- **Don't** re-implement the sync or path derivation — it's `resolveDurablePath` / `syncDurableAtSessionStart`
  in `src/cli/services/durable-sync.ts`; this skill only reads config, sets the two keys, and verifies.
- **Never** set `durable_path` to a file named `moflo.db` or the local `.moflo/moflo.db` — that's the
  HNSW-index-divergence hazard `flo doctor -c shared-db` guards against.
- **Don't** use `mkdir -p` / `rm` / `cp` in shell steps — Windows lacks them on PATH. Use Node `fs`.
- **Cross-machine or team? Wrong skill.** Redirect to `/memory-team`.

## See Also

- `/memory-team` — git-tracked JSONL sharing for teams **and** one person across machines
- `flo doctor -c shared-db` — reports auto-sharing status and catches full-DB misconfig
- `docs/blog/memory-sharing.html` — the design rationale (durable vs structural vs ephemeral)
