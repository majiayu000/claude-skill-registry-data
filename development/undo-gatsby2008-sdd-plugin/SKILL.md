---
name: undo
description: Discard uncommitted code changes — from /sdd:implement in a pipeline, or from free-hand vibe coding — reversibly. Works standalone (no .specwork/ required). Reversible by default (stash), with --restore to recover and --hard to discard irreversibly. Preserves .specwork/ when a pipeline is active.
argument-hint: "[--restore | --hard]"
allowed-tools: Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/revert.py:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*), Bash(git status:*), Bash(git stash:*), Bash(git restore:*), Bash(git clean:*), Bash(git rev-parse:*)
---

# Undo Implementation

Discard **uncommitted** code changes, reversibly, before they are committed.
Works in two contexts:

- **In a pipeline** — discards what `/sdd:implement` accumulated **before
  `/sdd:commit`**, while keeping `.specwork/` (spec, plan, cache, state) intact so
  you can fix the spec and re-implement.
- **Standalone (vibe coding)** — no `.specwork/` required; it just cleans your
  working tree so you can keep coding. Pairs with `/sdd:commit` as the "undo" half
  of the vibe loop.

```bash
/sdd:undo            # reversible: stash the changes (recover with --restore)
/sdd:undo --restore  # bring back the last undone changes (redo)
/sdd:undo --hard     # irreversible: revert tracked edits + delete new files
```

When a pipeline is active, `.specwork/` is **always preserved** — it is gitignored,
so it never enters a stash and is never removed by `git clean` (this skill never
passes `-x`).

> This is not `/sdd:pause`. `/sdd:pause` stashes *everything including `.specwork/`*
> to switch branches. `/sdd:undo` stashes *only the source changes* and leaves the
> pipeline active so you can re-spec immediately. It also only applies to
> **uncommitted** work — if you already ran `/sdd:commit`, see *Already committed?*
> below.

---

## Execution

| Step | Action |
|------|--------|
| 0 | Resolve mode from `$ARGUMENTS`: none → reversible undo · `--restore` → recover · `--hard` → irreversible |
| 1 | **Preview** what will be affected (skip for `--restore`) |
| 2 | **Confirm** with the user (skip for `--restore`; required for undo and `--hard`) |
| 3 | Run the matching `revert.py` subcommand |
| 4 | Point the user back to `/sdd:spec` → `/sdd:plan` → `/sdd:implement` |

---

## Step 1 — Preview (undo / --hard)

Show exactly what will be discarded before doing anything. `.specwork/` is
gitignored so it never appears here:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/revert.py preview
```

- Exit code **1** (`(clean — nothing to undo)`): stop — there is nothing to undo.
- Otherwise: the printed paths are the tracked edits and new files that will be
  reverted. Present them to the user.

---

## Step 2 — Confirm (undo / --hard)

Always confirm before discarding work. Use a single `AskUserQuestion`:

- **Reversible undo** — "Stash these N change(s)? Recoverable with `/sdd:undo --restore`."
- **`--hard`** — make the irreversibility explicit: "Permanently revert these N
  change(s)? This cannot be undone."

In **non-interactive** mode (`gates.py non-interactive <slug>` is true), do not
prompt: proceed only for the reversible undo; **refuse `--hard`** and tell the
user to run it interactively.

---

## Step 3 — Run

Reversible undo (default). Pass the feature slug so the stash is labeled and
`/sdd:undo --restore` can find it:

```bash
SLUG="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py resolve-slug 2>/dev/null || true)"
python3 ${CLAUDE_PLUGIN_ROOT}/lib/revert.py undo --slug "$SLUG"
```

Recover the last undo (redo):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/revert.py restore
```

Irreversible discard:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/revert.py hard
```

List recoverable undo stashes:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/revert.py list
```

---

## Step 4 — Next

Branch the guidance on whether a pipeline is active:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck   # exit 0 = pipeline active
```

- **Pipeline active** — the implementation is gone but `.specwork/` is intact.
  Guide the user to correct the spec and re-implement:

  ```
  Implementation discarded; .specwork/ preserved.

    /sdd:spec <correction>   # refine the spec (resolve/append Open Questions)
    /sdd:plan                # re-run: the spec is now newer than the plan (stale gate)
    /sdd:implement
  ```

- **Standalone (vibe coding)** — the working tree is clean again. Just keep
  coding, then `/sdd:commit` when ready.

In both cases, if they undid by mistake: `/sdd:undo --restore`.

---

## Already committed?

`/sdd:undo` only handles **uncommitted** work. If the bad implementation is already
in a commit (e.g. after `/sdd:commit`), this skill does **not** rewrite history.
Tell the user that is a `git reset` operation and let them decide:

- `git reset --soft HEAD~1` — undo the commit, keep changes staged
- `git reset --hard HEAD~1` — undo the commit and discard changes (irreversible)

---

## Related Skills

- `pause` / `restore` — stash/restore the **whole** pipeline (including `.specwork/`) to switch branches
- `spec` — re-draft / refine the spec after undoing
- `close` — the opposite of `/sdd:undo`: wipes `.specwork/` and leaves the code
