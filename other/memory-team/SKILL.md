---
name: memory-team
description: |
  Guided setup for sharing moflo's durable learnings through a git-tracked JSONL artifact — for a whole
  TEAM on one repo, OR for one person across several MACHINES (a team of one). Use when the user says
  "share learnings with my team", "commit our moflo memory", "sync memory across my laptop and desktop",
  "set up memory.team_artifact", or "auto-export learnings on every PR". Installs a pre-commit hook so the
  artifact rides along in every commit. For many worktrees on ONE machine, use /memory-worktree instead.
arguments: "[--solo]"
---

# /memory-team — Share Learnings via a Git-Tracked Artifact

Wires up **`memory.team_artifact`**: a diffable JSONL file (`.moflo/shared/learnings.jsonl`) that lives
**in the repo**, reviewed like any other change. Teammates `git pull` it and their next session
auto-imports the merged learnings; each entry is stamped with its git author. This skill also installs a
**pre-commit hook** so the artifact is re-exported and staged on every commit — the learnings ride along
in each PR with zero effort.

> **One mechanism, two audiences.** A *team* and *one person across machines* are the same problem — push
> the durable slice through git. This skill covers both; the only difference is whether anyone else is on
> the other end. (Prefer a private, non-git file for your own machines? See "Advanced" at the bottom —
> `flo memory sync` moves a binary artifact that keeps embeddings verbatim.)

**Arguments:** `$ARGUMENTS` — pass `--solo` to skip team-oriented wording (still identical setup).

## When to use

- "share learnings / memory with my team"
- "commit our moflo knowledge to the repo"
- "sync memory between my laptop and desktop"
- "auto-export the learnings on every PR / commit"
- "set up `team_artifact`"

For **many worktrees on one machine**, that's a shared local store, not git — use `/memory-worktree`.

## Procedure

### Step 0 — Memory first (gate requirement)

```
mcp__moflo__memory_search { query: "team_artifact learnings jsonl git share import session-start", namespace: "guidance" }
```

### Step 1 — Confirm this is the git path

- Team on one repo, or one person across machines who both push to the same repo? → correct skill.
- Many worktrees on **one** machine, no cross-machine need? → redirect to `/memory-worktree`.
- A private synced file (Dropbox/USB), no git? → point at the Advanced section (`flo memory sync`).

### Step 2 — Set the config

Read the project-root `moflo.yaml` and add/merge under `memory:` — **preserve existing keys**:

```yaml
memory:
  team_artifact: .moflo/shared/learnings.jsonl
```

`.moflo/shared/learnings.jsonl` is the default; only override if the user wants a different tracked path.

### Step 3 — First export (creates + tracks the artifact)

```bash
npx flo memory team-export 2>&1
```

This writes the JSONL, and **rewrites `.gitignore`** from a blanket `.moflo/` to `.moflo/*` +
`!/.moflo/shared/` so the shared artifact is tracked while the machine-local DB stays ignored. Surface
what it reports (entries added, `.gitignore` change). If there are no durable learnings yet, that's fine —
the artifact is created empty and fills in as learnings accrue.

### Step 4 — Install the pre-commit hook

The hook re-exports and stages the artifact on every commit, so it's never stale in a PR. Handle three
cases; **do not clobber** an existing hook.

Define the managed block (POSIX `sh` — git runs hooks via `sh` on Linux, macOS, **and** Windows):

```sh
# >>> moflo team-export (managed by /memory-team) >>>
# Refresh the shared learnings artifact so it rides along in this commit.
npx --no-install flo memory team-export >/dev/null 2>&1 || true
if [ -n "$(git status --porcelain -- .moflo/shared/learnings.jsonl 2>/dev/null)" ]; then
  git add .moflo/shared/learnings.jsonl
fi
# <<< moflo team-export (managed by /memory-team) <<<
```

Install it:

1. **Husky present** (`.husky/pre-commit` exists) → append the block to that file.
2. **Existing `.git/hooks/pre-commit`** → if it already contains the `moflo team-export` markers, leave it
   (idempotent); otherwise append the block after the shebang.
3. **No hook** → create `.git/hooks/pre-commit` with `#!/bin/sh` as the first line, then the block.

On POSIX, make it executable:

```bash
node -e "require('fs').chmodSync('.git/hooks/pre-commit', 0o755)"
```

(Use the Node `fs.chmodSync` primitive, not `chmod` — it's a harmless no-op on Windows. Never shell out
to `chmod` in a cross-platform step.)

- The `|| true` keeps a failed export from ever blocking a commit.
- The `git status --porcelain` guard means the artifact is only re-staged when it actually changed — no
  empty-diff churn on unrelated commits.

### Step 5 — Commit and share

```bash
git add .moflo/shared/learnings.jsonl .gitignore
git commit -m "chore: share moflo learnings"
git push
```

Teammates (or your other machine) run `git pull`; their **next session auto-imports** the merged file —
no manual import command. To pull learnings without waiting for a restart:

```bash
npx flo memory team-import 2>&1
```

## Output

End with a single-block summary:

```
Team Memory Sharing — configured
─────────────────────────────────
Artifact:    .moflo/shared/learnings.jsonl  (git-tracked, JSONL, author-stamped)
Config key:  memory.team_artifact
PR hook:     .git/hooks/pre-commit  → re-exports + stages on every commit
Import:      automatic at session start (after git pull)  |  npx flo memory team-import
Scope:       learnings + knowledge only (embeddings regenerated on import)
```

## Advanced — one person, a private file (no git)

If you're solo and would rather not commit learnings, carry a binary artifact instead. It keeps the
embeddings verbatim (no recompute on the far side) and merges idempotently:

```bash
npx flo memory sync --to   ~/Dropbox/moflo-learnings.db   # machine A
npx flo memory sync --from ~/Dropbox/moflo-learnings.db   # machine B
```

Same durable slice, no repo footprint, no review — the trade-off is it's not diffable and not shared.

## Rules

- **Don't** reimplement export/import or the `.gitignore` rewrite — `flo memory team-export/team-import`
  own all of it (`team-artifact-sync.ts`). This skill sets config, runs them, and installs the hook.
- **Don't** overwrite an existing pre-commit hook or husky config — append the marked block only.
- **Don't** use `chmod` / `mkdir` / `rm` in shell steps — Windows lacks them on PATH; use Node `fs`.
- Embeddings are intentionally **omitted** from the JSONL (384 floats/row would wreck diffs) — they're
  regenerated on import. Don't try to add them.

## See Also

- `/memory-worktree` — same-machine sharing across worktrees / Conductor (a shared local store, not git)
- `flo memory team-export --help` / `flo memory sync --help`
- `docs/blog/memory-sharing.html` — the design rationale (durable slice, why not share the whole DB)
