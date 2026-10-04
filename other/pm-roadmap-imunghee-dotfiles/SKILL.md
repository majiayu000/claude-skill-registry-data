---
name: pm-roadmap
description: "Manage a project's per-task backlog under .agents/tasks/ and generate the next-task kickoff prompt: show what to work on next, add or close items. Reads are model-invocable; writes also fire from design and retro lifecycle gates. Skip planning a specific task (design) and closing a landed plan (retro)."
argument-hint: "list | tree | get <id> | next [id] | validate | migrate [--apply] | task ... | add ... | plan ... | note <KEY> <id> <text|-> | retitle <KEY> <id> <title|-> | reorder <KEY> <id> <order|-> | approve <KEY> <id> | persist <KEY> <id> <plan> | complete <KEY> <id> --plan P --status done|dropped | reclassify <KEY> <id> --plan P --status done|dropped [--reason T] | plan-step <check|uncheck> <plan> <N> | select --plan P | worktree adopt --plan P --base R [--base-commit OID] [--start R] [--select] | worktree <resolve|ensure|validate|prune> | expunge <KEY> <id> [--force] | triage ... | memory ... | links ... | manage"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
disable-model-invocation: false
---

Manage the per-project backlog in the **task-first model**: each task owns its backlog,
its unbounded closed history, its links and memory, under `<git-root>/.agents/tasks/<KEY>/`.

Arguments: $ARGUMENTS

## System — the pm-* loop

One of four skills. **This skill owns *backlog* + the shared task store.**

```
(pm-context · links)  ┐
(retro · memory)       ├──▶  (design · plan)
(pm-roadmap · backlog) ┘          │
        ▲__________________________│   retro closes the item, feeds memory + backlog back
```

A **task** (`<KEY>`) is a first-class record — an epic/feature with a lifecycle. Its
**items** are the workable units inside it. A task owns: `task.md` (status), `backlog.md`
(open items), `closed.md` (done/dropped history, **unbounded**), `links.md` (pm-context),
`memory.md` (retro). The cross-task roadmap is **derived at read time** by scanning
`tasks/*` — there is no single roadmap file.

## Model & storage

```
.agents/
  tasks/
    <KEY>/  task.md  backlog.md  closed.md  links.md  memory.md
    _inbox.md                   # untriaged items in the shared lock/write domain
    archive/<KEY>/              # torn-down tasks (writes refused; ids stay reserved)
    .lock/                      # transient token-owned directory lock; absent while idle
  plans/*.md                    # design plans (frontmatter `pm_loop: true|false`)
  state/  current.txt  actor.txt
```

- **task.md**: `status: active | done | archived`. `done` when all items closed; auto-reopens
  to `active` when a new item is added. `archived` = torn down (dir moved to `archive/`).
  `mode: solo | collab` (absence → solo; **always written** on create) + optional
  `collaborators:` (comma roster) — see Collaboration mode.
- **backlog item** (`backlog.md`, block grammar `- **id**` + `Key: Value`): `Priority`,
  `Status` (open|draft|active), `Order` (per-task sequence), `Plan`, `Note`, and (collab only)
  `Owner` + `OwnerNote`.
- **closed item** (`closed.md`): `Status` (done|dropped), `Plan`, `Reason` (required for
  dropped), `Closed` (date), `ClosedSource`, and (collab only) `ClosedBy`. **Unbounded — never trimmed.**
- **id**: globally unique across all tasks' backlog+closed, **never reused** (closed ids stay
  reserved, incl. archived tasks), aligned 1:1 with the plan slug. Kebab-case. **One exception:**
  `expunge` releases an id, because the invariant protects ids that named real work and an
  expunged item named none. Every other path keeps ids reserved forever.
- **Plan**: 1:1 — at most one item (backlog or closed, any task) per plan path.
- **pointers**: main `current.txt` selects the launcher plan; each managed worktree has a
  local execution `current.txt`. Every writer uses checkout-local lock+content-CAS.
  `current.txt` and `actor.txt` remain checkout-local.

## Single write path

**All mutations go through `pm-roadmap.ts` (CLI) → `ops.ts` (atomic, lock-guarded) → `store.ts`.**
Skills/design/retro/GUI never hand-edit the markdown. Run the CLI:

```bash
repo_root="$(git rev-parse --show-toplevel)" || { echo "not in a git repo"; exit 1; }
(cd ~/.config/ai/skills/pm-roadmap && [[ -d node_modules ]] || npm install)
PM_ROOT="$repo_root" ~/.config/ai/skills/pm-roadmap/node_modules/.bin/tsx ~/.config/ai/skills/pm-roadmap/pm-roadmap.ts <subcmd> [args]
```

For agent-session `persist` and `select` flows, forward the exact metadata from the
injected session-routing block on the same invocation:

```bash
PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" pm persist <KEY> <id> <plan> --title "<title>"
PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" pm select --plan <plan>
```

Do not sanitize or invent either value. `session_binding: bound` is the only successful
agent-session handoff. `session_binding: unbound (<typed reason>); do not retry persist`
means the persist transaction committed but routing did not; report it and stop without
replaying the mutation. `session_binding: unbound (<typed reason>); do not retry select`
has the same stop rule. `session_binding: not_requested` is allowed only for explicit
launcher/dashboard callers that do not claim ownership for an agent session.

(Read subcmds on a legacy repo — `tasks/` absent but old `ROADMAP.md` present — print
`⚠ legacy roadmap detected — run /pm-roadmap migrate`.)

## Subcommands

- **list** / **tree** — eligible next candidates (sorted `priority, taskKey, order, id`) + blocked + inbox count / per-task backlog. Each blocked row names its cause — `(dependency)` for an unresolved `DependsOn`, or `(earlier Order — clear it with reorder ...)` for a lower-Order sibling in the same task. The two are different problems: `depend` has no effect on an item that an Order chain is blocking. In collab tasks both show an `@owner` / `(unassigned)` badge (tree also marks `[collab]`); **list** default-filters collab items to *me + unassigned* (`--owner X` to filter by another, `--all` to show everything; solo items always shown).
- **get `<id>`** — an item's join view (plan goal + next step, task links + memory, recent done-sibling notes, note).
- **next `[id]` `[--owner X]` `[--all]`** — paste-ready kickoff prompt. Target: explicit id, else the candidate list (`Choose a candidate` — never auto-picks an eligible item; `_INBOX` excluded). The candidate-list path applies the same collab default filter as `list` (me + unassigned; `--owner`/`--all` override); an explicit id bypasses the filter. The prompt surfaces item owner + handoff note and memory/link `By` for collab tasks. After emitting, ask whether to run it **here** (no copy — a linked plan first runs session-aware `pm select --plan <plan>`, while an unplanned item proceeds into `/design <id>` and binds on persist; then resume the plan's next unchecked step) or **hand off** to a fresh session (copy to the clipboard with `pbcopy`, then stop).
- **recent** — derived recent-closed view (all `closed.md` merged by date, capped).
- **validate** — full-scan invariant check (C1–C17; see below). Exit 1 on errors. `/retro` runs it after its sink.
- **migrate `[--apply]`** — convert a legacy repo's `.agents/` to the task-first model. Default dry-run (prints the mapping). `--apply` after review. See Migration.
- **task `create|done|archive|restore|set-mode|collaborators` `<KEY>`** — task lifecycle. `archive` refuses if open items remain; `restore` re-activates an archived task. `create [--mode collab]` records mode (default solo, **always written** going forward). `set-mode <solo|collab>` switches a task either way — solo→collab assigns the switcher (resolved actor) as Owner to **every** un-owned `backlog.md` item (open|draft|active) and **requires** a resolvable actor (reports the assigned count + owner, and **warns** when that owner resolved from the `git user.email` fallback — guards against a personal email silently owning the backlog); collab→solo keeps attribution fields (lossless). `collaborators <csv>` sets the roster (empty clears).
- **add `<id> <title>` (`--task KEY` | `--inbox`) [-p] [-o] [--note]** — append a workable unit (or an untriaged inbox item). `-o` takes a positive-integer order; `--note` attaches a note.
- **assign `<KEY> <id> <owner|->` [`--note T`] [`--force`]** / **claim `<KEY> <id>` [`--note T`] [`--force`]** — set an item's `Owner` (collab tasks only; refuses solo). `assign` takes an explicit owner (`-` unassigns, dropping `Owner`+`OwnerNote`); `claim` self-assigns the resolved actor. `--note` records a handoff reason (`OwnerNote`). **Double-claim guard**: overwriting a different existing owner needs `--force`.
- **whoami `[<name>]`** — no arg prints the resolved actor + its source; `<name>` writes `state/actor.txt` (worktree-local identity).
- **mine** / **who** — collab cross-task views: `mine` = open items owned by the resolved actor; `who` = per-owner board (unassigned grouped).
- **persist / approve / complete / plan-step** — recoverable lifecycle commands. Persist
  consumes reservation-bound staged bytes; approve changes plan+item together; complete
  terminals plan+item/harvest together; plan-step serializes checkbox writes. Standalone
  variants journal only the plan.
- **reclassify `<KEY> <id> --plan P --status done|dropped [--reason T]`** — journaled
  correction for an already-closed linked plan+item. Requires exact id/plan linkage and
  `pm_loop: true`; `dropped` requires a non-empty reason, while `done` rejects a reason
  and removes any stale one. Reports `reclassified` or an idempotent `unchanged`.
- **select / worktree** — explicit launcher selection and thin wrappers around the shared
  resolve/ensure/adopt/validate/prune engine. `worktree adopt` forwards `--base-commit`
  (immutable historical diff base) and `--start` (new-branch source only). It discovers
  exact current-bearing candidates with zero/create, one/reuse, many/stop semantics,
  rejects unowned occupied topology, and preserves `adopted_selected|adopted_parked`
  JSON outcomes. Terminal cleanup is
  `worktree prune --plan <done-or-dropped-plan>`; the engine derives and revalidates its
  mapping. Main is never an execution mapping.
- **note `<KEY> <id> <text|->`** / **retitle `<KEY> <id> <title|->`** — edit an open item's
  Note or its title. These were the last two of an item's eight fields without a setter, so
  correcting either used to mean `expunge` + re-`add`, which silently reset every field the caller
  did not retype (Priority back to P2, Order dropped). `-` clears: an empty `Note` is what
  creation writes, and an empty title renders the bare `- **id**` header. Both refuse a value the
  block grammar cannot represent (newline, `U+2028/9`) before writing a byte, and both work on
  `backlog.md` only — a closed item's note is history, and an archived task is refused by name.
- **plan / reprioritize / reorder / depend / close / drop / triage** — lower-level
  item transitions and escape hatches. Design/retro use the lifecycle commands above.
  `reorder <KEY> <id> <order|->` takes a positive integer, or `-` to **remove** the Order field
  (`0` stays rejected — absent already means "no position", and storing a literal `0` would give
  the same state two encodings). Removing it is how an item leaves a per-task Order chain, since
  only the lowest Order in a task is eligible.
- **expunge `<KEY> <id>` [`--force`]** — erase a write that should never have existed. Removes
  the block outright from `backlog.md`, `closed.md`, or `_inbox.md` (use `_INBOX` as the key)
  with **no tombstone**, and **releases the id**. This is NOT a lifecycle transition: `drop`
  means "closed as dropped, with a tombstone" and is what a real abandoned item gets. Reach for
  `expunge` only when a malformed command created the record — `drop` on such a record makes it
  permanent, which is the trap it exists to undo. Three preflight guards, all before any write:
  the item must exist; its `Plan:` must not resolve to a plan that still exists (checked as the
  recorded path **or** `.agents/plans/archive/<basename>`, because the archiver rewrites that
  pointer *after* moving the file); and no other item's `DependsOn` may name it. `--force`
  relaxes **only** the plan guard — needed because `plan` cannot unlink a closed item, which
  would otherwise strand it forever. Irreversible, and `tasks/` is gitignored: copy the file
  aside first. **Archived tasks are refused**, like every other item mutator — `archive/` is a
  read-only tombstone. An id inside an archived task is still reserved, so to free it restore,
  expunge, then re-archive: `task restore <KEY>` → `expunge <KEY> <id>` → `task archive <KEY>`
  (re-archiving requires the backlog to be empty, which it is if you only expunged).
- **memory `<KEY> add <title>` [`--note T`] [`--date D`] [`--by W`]** — upsert a durable-decision note into `tasks/<KEY>/memory.md` (upsert by title; lock+CAS via ops). The non-GUI memory write path — **/retro's durable-decision sink** (the GUI `manage` is the other writer). Date defaults to today. On **collab** tasks a `By` publisher is stamped from the resolved actor (`--by` overrides; collab + unresolvable identity → stop); solo tasks get no `By`.
- **links `<KEY> add <label>` `--url U` [`--triggers C`] [`--summary S`] [`--by W`]** / **links `<KEY> remove <match>`** — upsert/remove a task's external link in `tasks/<KEY>/links.md` (case-insensitive label upsert; URL unique per task; lock+CAS via ops). The **/pm-context** write path (the GUI `manage` is the other writer); pm-context does fetch + trigger/summary extraction, then persists via this CLI. On **collab** tasks a `By` publisher is stamped (same rule as memory); the GUI PUT preserves existing `By` (it doesn't author it).
- **current-task** — read-only launcher/dashboard projection: prints the KEY linked to that checkout's selected launcher plan. Empty for no selection, standalone plans, stale plans, and terminal plans. Interactive agent consumers use `resolve-session` plus `pm get <plan-id>` instead; they never use this command as a session fallback.
- **manage** — open the dashboard GUI (see below).

## Lifecycle (automatic — implemented in /design and /retro)

| Moment | Write (via ops) |
|---|---|
| design **persist** | reservation lock → store lock; journal-create canonical plan/item, seed target, main CAS → selected or parked |
| **`승인`** | `approve` journals plan + item `draft → active` together |
| **`취소`** | `complete --status dropped` journals plan + item terminal state, then exact pointer cleanup |
| **`/retro`** done/dropped | `completePlanFromRetro` — plan→terminal + item backlog→closed + structured `## Deferred` harvest + clear pointers, all-or-nothing |
| **`/retro`** memory harvest | `addTaskMemory` (CLI `memory add`) — durable decisions → `tasks/<KEY>/memory.md`; a separate write, OUTSIDE the close transaction's lock |

## Invariants (validate)

Errors: **C1** through **C15** preserve the existing id, plan-link, status, pointer,
collaboration, and dependency contracts. **C16** rejects duplicate non-terminal worktree
ownership and main-checkout execution mappings. **C17** reports any line in
`backlog.md`/`closed.md`/`links.md`/`memory.md`/`_inbox.md` that belongs to no item block —
including a heading superseded by a later `# ` — because the parser drops it and the next
write destroys it. Never mutates — fix via ops.

## Plan archiving

`/design` persist runs `archive.ts`: terminal plans **≥30 days** old and unreferenced
move to `plans/archive/`. A match in main or any Git-managed worktree current protects
the plan; the archiver never clears pointers.

## Migration

`/pm-roadmap migrate` converts a legacy repo (old `ROADMAP.md` + `task-context/` + `memory/`)
to the task-first model: per-task dirs, taskless→`tasks/_inbox.md`, legacy `## Memory` sections split
out, `Context:`/`Parent:`→`Task`. **Default dry-run** (prints mapping, writes nothing);
`--apply` backs up `.agents/` → converts → validates → removes legacy only on a clean validate
(else rolls back). Empty tasks scaffolding does not suppress legacy migration. Inbox
relocation is an independent, journaled phase and dry-run returns `recovery_required`
without mutation when a journal is pending. **Never auto-runs.**

## manage (dashboard)

Capture the git root **before** cd; always restart the server (never reuse):

```bash
repo_root="$(git rev-parse --show-toplevel)" || { echo "not in a git repo"; exit 1; }
kill $(lsof -ti:8484 2>/dev/null) 2>/dev/null; sleep 1
cd ~/.config/ai/skills/pm-context && [[ -d node_modules ]] || npm install
TASK_CONTEXT_ROOT="$repo_root" ./node_modules/.bin/tsx server.ts   # run_in_background
```

Then open `http://localhost:8484`. The dashboard derives its view from `tasks/*`; all its
writes route through ops (planless drop, task links/memory edit, delete=archive). A
task-centric UI redesign is tracked separately (backlog `pm-dashboard-task-centric`).

## Collaboration mode

A task runs **solo** (default, single actor — zero attribution) or **collab** (multiple distinct
*people* sharing one task). Mode lives in `task.md` `mode:`; absence reads as solo so legacy
task.md keeps working, and `create` always writes it going forward. `set-mode` switches either
way (solo→collab assigns the switcher as Owner to every un-owned backlog item; collab→solo keeps
fields, lossless).

**Identity.** Attribution resolves a person, precedence most-specific first:
`--actor/--by flag > PM_ACTOR env > state/actor.txt (pm whoami) > git config user.email`. A collab
operation that *requires* identity (claim, set-mode→collab, By/ClosedBy stamping) **stops with an
error** when nothing resolves — it never writes an anonymous record. Identity is resolved by the
**CLI only**; `ops.ts` stays pure (it receives a string), and `join.ts` never sees identity. On that
stop, confirm the intended actor and re-run with `--actor <name>` (or set the identity once via the
equivalent env/whoami step for your tool).

**Attribution (collab tasks only).** `Owner`/`OwnerNote` on backlog items (via `assign`/`claim`,
double-claim-guarded); `By` on memory/links (stamped from the actor — solo tasks get none, so
retro/pm-context need no change, they get attribution for free via the CLI); `ClosedBy` on
close/drop/retro-complete. The GUI doesn't author `By` but **preserves** it on save.

**Gate asymmetry (intentional, not a bug).** `assign`/`claim` are collab-specific → they *error*
on a solo task. memory/links/close are general-purpose → on a solo task they simply *skip*
attribution (no error), since retro/pm-context call them on solo tasks too.

**Views.** `list`/`tree` badge `@owner`/`(unassigned)`; `list`/`next` default-filter collab items
to *me + unassigned* (`--owner`/`--all` override); `mine` = my open items, `who` = per-owner board.
A non-empty `collaborators` roster turns on a C13 typo-guard warning (owner ∉ roster).

**Assumption.** Each person works in their own checkout/worktree, so `state/{current,actor}.txt`
are per-person; two people sharing one checkout would collide on those worktree-local pointers.

## Worktrees

Managed worktrees symlink only `.agents/tasks` and `.agents/plans` to canonical main;
`_inbox.md` lives inside tasks. `.agents/state/` is always real and local. The shared
worktree engine is the only topology writer, while lifecycle/migration commands
canonicalize shared writes to main as required.

## Rules

- All file content English; quoted triggers may stay Korean.
- **Every field value is single-line.** The block grammar stores one line per `Key: Value`,
  so a value carrying a newline (or a Unicode line separator, or leading/trailing whitespace
  the parser would trim) is refused at write time rather than silently truncated. **Long prose
  belongs in `.agents/plans/*.md`**, which has no grammar constraint; a task-memory note keeps
  a one-line summary plus the plan reference. This applies to the dashboard's memory/summary
  textareas too — a multi-line note there returns 409 with the reason.
- **Never hand-edit `tasks/*` markdown — always go through the CLI/ops.** That is the single write path (lock + CAS + lossless serialize).
  One sanctioned exception: repairing C17 damage. A document that already carries lines outside
  any item block is refused by every writer (so the CLI cannot repair it), which makes that file
  read-only until a human folds the stranded text back into a field or moves it to a plan.
  Confirm the repair with `pm validate`. Other documents and tasks stay writable.
- Reads (`list`/`tree`/`get`/`next`/`recent`/`validate`) are safe to auto-invoke; mutations come from lifecycle gates or explicit subcommands.
- `tasks/` is gitignored (durability is the files themselves, not git).
