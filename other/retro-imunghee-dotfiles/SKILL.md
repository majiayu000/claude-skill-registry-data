---
name: retro
description: "Post-work retrospective that closes the landed plan in the pm loop and harvests follow-ups and durable per-task decisions. Use at end of session after significant work, never mid-task."
argument-hint: "[commit range, e.g. HEAD~3, or blank for HEAD~5]"
allowed-tools: Bash, Read, Write, Glob, Grep, Edit
disable-model-invocation: false
---

Analyze the recent work and close the loop — consolidate learnings into the task store, not accumulate.

Range: $ARGUMENTS (if empty, default to HEAD~5)

## System — role in the pm-* loop

`retro` is the **memory** owner + loop-closer of the project-management system:

```
(pm-context · context | retro · memory | pm-roadmap · backlog)  ──▶  design · plan
        ▲___________________________________________________________________│
        retro: on a landed plan → close the pm-roadmap item, harvest follow-up workable units → backlog, harvest durable decisions → that task's MEMORY
```

So retro feeds **memory** and **backlog** back into the loop. The close is **one atomic transaction** — the `pm-roadmap.ts complete` CLI (→ `completePlanFromRetro`): plan → terminal status, the backlog item → `closed.md`, the plan's structured `## Deferred` block harvested into the task backlog, and the `current.txt`/`focus` pointers cleared, all-or-nothing. Memory (durable per-task decisions/learnings) is **retro's domain — retro is its primary writer** — distinct from `pm-context`'s links and from a plan's Post-Impl Notes. Stored per-task at `.agents/tasks/<KEY>/memory.md`, written through the `pm-roadmap.ts memory add` CLI (lock+CAS via ops) — **never hand-edited**; the `pm-context` manage GUI is the other writer.

## Current Context
- Branch: !`git branch --show-current 2>/dev/null || echo "N/A"`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "N/A"`

## Core Principle

**Hygiene over growth.** Capture only durable decisions worth recalling next session — not a transcript. Fewer, sharper memory notes beat many vague ones.

## Phases

### 1. Collect

Gather what happened in this session:

```bash
git log --oneline <range>
git diff --stat <range>
```

Resolve the active plan through the originating session. An explicit plan argument uses
`resolve-plan`; otherwise use the exact injected metadata:
```bash
root="$(git rev-parse --show-toplevel)" || exit 1
PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" node "$HOME/.config/ai/lib/worktree.mjs" resolve-session --root "$root" --tool "<injected session tool>"
```

If `resolve-session` returns `ok`, re-root all collection to `execution_root` and compare
from immutable `base_commit`. Capture whether `pm_loop` is true. A routing or mapping
error blocks retro; never collect or close from the caller checkout. Linked and
standalone plans both close through the CLI transaction; neither uses a direct status edit.
An unbound main session has no implicit plan: require an explicit plan rather than
consulting launcher state.
If the plan is already terminal (`done`/`dropped`), skip the close.

If `/verify` ran in this session, reference its truth-condition verdict — a failed or partial verdict means the plan's goal was not fully met, which the close should account for.

### 2. Analyze

Answer these questions based on the collected data:

- What diverged from the plan (if one existed)?
- Did follow-up work emerge that should become its own backlog item? (→ `## Deferred` harvest)
- Were there decisions or gotchas worth recalling next session? (→ task memory harvest)
- Were there false starts or wasted iterations? What would have prevented them?

Do NOT force insights. If the session was routine, say so (propose nothing beyond the close).

### 3. Propose

Present proposed changes in a single table for approval:

```
| # | Action            | Target                   | Summary                         |
|---|-------------------|--------------------------|---------------------------------|
| 1 | Plan post-impl    | plans/2026-..-auth.md    | Add post-implementation notes   |
| 2 | Deferred harvest  | <new-id> → task backlog  | Follow-up: rate-limit the API   |
| 3 | Task memory       | tasks/<KEY>/memory.md    | Decision: chose CAS over mutex  |
| 4 | Close             | plan + item → done       | Atomic complete transaction     |
```

Wait for the user to approve by number (e.g., "1,2,3" or "all" or "none").

### 4. Apply

Only apply approved items.

**Update plan body**: Fill `## Post-Implementation Notes` with key outcomes, design pivots, and findings. A plan under `{{PLAN_DIR}}/` is a design artifact, **not** a task-store file, so edit it directly with `Edit`. If follow-up workable units emerged, add a structured `## Deferred` block to the same plan so the close transaction harvests them into the task backlog (grammar below). Do **not** hand-edit the plan's `status:` here — the close step owns it.

CLI setup (one block; `<id>` = the plan's frontmatter `id`):
```bash
repo_root="$(git rev-parse --show-toplevel)" || { echo "not in a git repo"; exit 1; }
(cd $HOME/.config/ai/skills/pm-roadmap && [[ -d node_modules ]] || npm install)
pm() { PM_ROOT="$repo_root" $HOME/.config/ai/skills/pm-roadmap/node_modules/.bin/tsx $HOME/.config/ai/skills/pm-roadmap/pm-roadmap.ts "$@"; }
pm get <id>   # resolves the owning task KEY + confirms the item is still open (linked path)
```

`## Deferred` block grammar (harvested by `complete`; ids must be fresh kebab-case — a collision aborts the whole close):
```markdown
## Deferred

- **<new-kebab-id>** — <title>
  - Priority: P2
  - Note: <one-line follow-up description>
```

**Close the loop** — pick one path:
- **Linked to a backlog item** (the pm loop — `pm get <id>` finds the item **still open** in a task backlog; `<id>` = the plan's frontmatter `id`, aligned 1:1 with the plan slug):
  ```bash
  pm complete <KEY> <id> --plan <plan-path> --status done       # done path
  pm complete <KEY> <id> --plan <plan-path> --status dropped --reason "<why abandoned>"   # dropped path
  ```
  `complete` journals plan status, item close, and Deferred harvest together, then
  clears exact matching pointers best-effort. **Do NOT hand-edit plan status or
  current.** Preconditions fail before the journal is prepared.
- **Standalone (`pm_loop:false`)**:
  ```bash
  pm complete --standalone --plan <plan-path> --status done
  pm complete --standalone --plan <plan-path> --status dropped --reason "<why abandoned>"
  ```
  This journals the plan-only transition and performs the same exact all-worktree
  pointer cleanup. Never edit status or current directly.

**Harvest durable decisions → task memory**: for each decision/gotcha worth recalling next session, write it to the task's memory store via the CLI (a separate write, outside the close transaction):
```bash
pm memory <KEY> add "<note title>" --note "<one-line decision>" --date <YYYY-MM-DD>
```
This upserts (by title) `.agents/tasks/<KEY>/memory.md` through ops (lock+CAS) — **never hand-edit it**. Surfaced in `pm next` prompts and item context.

**Harvest review lessons → repo lessons file**: task memory is scoped to one task, but a critique about *how code is written* outlives it. Hand those to the `review-lessons` skill, which owns `.agents/review-lessons.md`:

- **LOCAL entries** — anything the user critiqued about the code this session that would change how future code is written (a naming rule, a missed guard, a util that should have been reused). Record the reasoning they gave, not just the instruction. Skip one-off corrections tied to a line that will never recur.
- **Collection refresh** — if the file is missing, or its `Collected` date is over 30 days old, run a full collection: PRs from this work have since been reviewed, and the skill re-evaluates existing entries in the same pass.

Skip entirely when the session produced neither code nor critique.

After applying, if either close transaction ran, run the invariant checker once (`pm validate`) and report its output — a read-only self-check of the just-written plan/task state.

## Rules

- Never force insights from a routine session — "nothing to change, just close the loop" is a valid outcome
- Durable decisions go to **task memory** (`pm memory <KEY> add`) — never hand-edit `tasks/<KEY>/memory.md`
- The close transaction owns plan `status` and exact current-pointer cleanup for linked and standalone paths — never hand-edit them
- `## Deferred` block ids must be fresh kebab-case (a collision aborts the whole close)
- All file content in English
