---
name: resync
description: Resync SDD pipeline artifacts with the current branch. Renames .specwork files and updates state.json after a branch rename. Two modes — sync-only when called without args (assumes git rename already happened), atomic when called with --rename-branch <new-branch-name> (runs git branch -m first, then syncs).
argument-hint: "[--rename-branch <new-branch-name>]"
allowed-tools: Read, Write, Bash(git rev-parse:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(find .specwork:*), Bash(mv:*), Bash(cat .specwork/_state/*), Bash(test:*), Bash(python3:*), Bash(ls:*)
---

# Resync

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/resync/SKILL.md`

---

## Description

Synchronize SDD pipeline artifacts under `.specwork/` with the current branch when the branch was renamed and the pipeline state still points at the old name. Renames the `.specwork/*-state.json`, spec, source, plan, cache, path, and context files, and updates `state.json` fields (`id`, `branch`, `ticket`, `input_type`, internal paths).

Two modes based on argument:

| Mode | Invocation | Behavior |
|------|-----------|----------|
| Sync-only | `/sdd:resync` | Compares current branch to `state.json::branch`. If they differ, renames artifacts to match the current branch. Does not touch git. Use after running `git branch -m` manually. |
| Atomic | `/sdd:resync --rename-branch <new-branch-name>` | Runs `git branch -m <new>` first, then syncs. One-shot for "rename branch + update pipeline" in a single step. |

---

## Use cases

- A free-text feature gets assigned a ticket: rename to `feature/IR-70-<original-slug>` and resync — `ticket` and `input_type` get filled in automatically.
- Branch name typo fixed mid-pipeline.
- Recovery: someone ran `git branch -m` and forgot to update the pipeline.

---

## Flow

| Step | Action |
|------|--------|
| 1 | Prerequisite check — pipeline must be initialized in `.specwork/` |
| 2 | Parse argument (`--rename-branch <name>` or none) |
| 3 | (Atomic mode only) Run `git branch -m <new>` |
| 4 | Derive new slug, ticket, input_type from current branch |
| 5 | Identify the active state.json, derive old slug, detect collisions |
| 6 | Rename every `.specwork/*/<old-slug>-*` file to use the new slug |
| 7 | Update state.json content (id, branch, ticket, input_type, internal paths) |
| 8 | Print a summary of what changed |

---

## Step 1 — Prerequisites

```bash
if [ ! -d .specwork/_state ]; then
  echo "No SDD pipeline found in .specwork/. Nothing to resync."
  exit 0
fi

shopt -s nullglob 2>/dev/null
STATE_FILES=(.specwork/_state/*-state.json)
if [ ${#STATE_FILES[@]} -eq 0 ]; then
  echo "No state.json found under .specwork/_state/. Nothing to resync."
  exit 0
fi
```

Exit cleanly (not error) when there's no pipeline to resync.

---

## Step 2 — Parse Argument

`/sdd:resync` accepts:

- **No args** → sync-only mode. Skip Step 3.
- **`--rename-branch <name>`** → atomic mode. Capture `<name>` as the new branch, then proceed to Step 3.
- **Anything else** (bare value without the flag, unknown flag, or `--rename-branch` with no value) → stop with a usage message.

```text
Usage:
  /sdd:resync                                  Sync pipeline with current branch (no git ops).
  /sdd:resync --rename-branch feature/IR-70-foo  Rename branch then sync (atomic).
```

```bash
NEW_BRANCH=""
case "$1" in
  "")
    : # sync-only mode
    ;;
  --rename-branch)
    if [ -z "$2" ]; then
      echo "Usage: /sdd:resync --rename-branch <new-branch-name>" >&2
      exit 1
    fi
    NEW_BRANCH="$2"
    ;;
  *)
    echo "Usage: /sdd:resync --rename-branch <new-branch-name>" >&2
    exit 1
    ;;
esac
```

---

## Step 3 — Rename Branch (atomic mode only)

`NEW_BRANCH` was captured from `--rename-branch` in Step 2.

```bash
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [ "$CURRENT_BRANCH" != "$NEW_BRANCH" ]; then
  git branch -m "$NEW_BRANCH"
fi
```

The `if` guard handles the idempotent case (already on the target branch). Surface git's exit code and stop on any failure — typically a name collision against another local branch.

After this step, `git rev-parse --abbrev-ref HEAD` returns the new branch name.

---

## Step 4 — Derive Slug, Ticket, input_type

Derivation is done in code (`lib/slug.py`), not by re-deriving the regex here. It prints JSON for
the current branch (or a branch passed as an argument):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/slug.py
# → {"branch": "...", "unprefixed": "...", "slug": "...", "ticket": "...", "input_type": "..."}
```

Capture the values into bash variables (`CURRENT_BRANCH` from `branch`, `NEW_SLUG` from `slug`,
`TICKET` from `ticket`, `INPUT_TYPE` from `input_type`), e.g. with `python3 -c`/`jq` on the output.

If `slug` is empty after derivation (e.g., branch was `feature/` with nothing after), stop and tell the user the new branch name is not slug-friendly.

---

## Step 5 — Identify Old Slug & Collision Check

Pick the active state.json. The normal case is exactly one file under `.specwork/_state/`. If multiple exist (leftover from a previous unclosed pipeline), prefer the one whose `branch` field matches the current branch (which, after Step 3 in atomic mode, is the new branch — so this only matches if we're already in sync; otherwise none match and we fall back to picking the only candidate or aborting).

```bash
OLD_STATE="$(python3 - <<'PY'
import glob, json, subprocess, sys
states = sorted(glob.glob(".specwork/_state/*-state.json"))
if not states:
    sys.exit("No state.json files found.")
current = subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD']).decode().strip()
matches = []
for s in states:
    try:
        if json.load(open(s)).get('branch') == current:
            matches.append(s)
    except Exception:
        pass
if matches:
    print(matches[0])
elif len(states) == 1:
    print(states[0])
else:
    sys.exit(f"Multiple state.json files and none matches current branch '{current}'. Manual cleanup needed — keep one of: {', '.join(states)}")
PY
)"
[ -n "$OLD_STATE" ] || exit 1

OLD_SLUG="$(basename "$OLD_STATE" | sed -E 's/-state\.json$//')"
```

Collision check: if `OLD_SLUG != NEW_SLUG` and a file already exists at `.specwork/_state/${NEW_SLUG}-state.json`, abort with a clear message — refuse to overwrite another pipeline's state.

```bash
if [ "$OLD_SLUG" != "$NEW_SLUG" ] && [ -f ".specwork/_state/${NEW_SLUG}-state.json" ]; then
  echo "Refusing to resync — a different pipeline already exists at slug '${NEW_SLUG}'."
  echo "Run /sdd:close on one of them first, or pick a different branch name."
  exit 1
fi
```

---

## Step 6 — Rename Files

Skip if `OLD_SLUG == NEW_SLUG` (branch may have been renamed to a name that produces the same slug, or atomic mode was a no-op).

For every file in `.specwork/` whose basename starts with `${OLD_SLUG}-`, rename it to swap the prefix:

```bash
if [ "$OLD_SLUG" != "$NEW_SLUG" ]; then
  find .specwork -type f -name "${OLD_SLUG}-*" -print0 | while IFS= read -r -d '' f; do
    dir="$(dirname "$f")"
    base="$(basename "$f")"
    new_base="${NEW_SLUG}${base#"$OLD_SLUG"}"
    mv "$f" "$dir/$new_base"
  done
fi
```

This catches `*-state.json`, `*-rules.json`, `*-implementation-cache.json`, `*-spec.md`, `*-source.md`, `*-plan.md`, `*-context.md` consistently.

---

## Step 7 — Update state.json

The rename is done in code (`lib/state.py rename-slug`): it rewrites every string field that
mentions the old slug (internal paths) **before** setting the authoritative
`id`/`branch`/`ticket`/`input_type`, so a new slug that contains the old one doesn't double up.

```bash
NEW_STATE=".specwork/_state/${NEW_SLUG}-state.json"
python3 ${CLAUDE_PLUGIN_ROOT}/lib/state.py rename-slug \
  "$NEW_STATE" "$NEW_SLUG" "$OLD_SLUG" "$CURRENT_BRANCH" "$TICKET" "$INPUT_TYPE"
```

Do **not** modify `source_title` — that field reflects the user's original input at `/sdd:start` time and changing it requires explicit user intent. If the rename surfaced a ticket that wasn't there before, point the user at editing `source_title` manually or rerunning `/sdd:start`.

---

## Step 8 — Print Summary

Show what changed in a compact block:

```text
Resync complete.

Branch:  feature/consent-personuuid   →  feature/IR-70-consent-personuuid
Slug:    consent-personuuid           →  ir-70-consent-personuuid
Ticket:  null                         →  IR-70
Type:    freetext                     →  jira

Files renamed: 5
  .specwork/_state/<slug>-state.json
  .specwork/_state/<slug>-rules.json
  .specwork/_state/<slug>-implementation-cache.json
  .specwork/_spec/<slug>-spec.md
  .specwork/_spec/<slug>-source.md

Next:
  - source_title in state.json still reflects the original input.
    Edit it manually or rerun /sdd:start if you want it to match the new ticket.
  - If the old branch was pushed to origin, push the new branch and delete the old:
      git push -u origin HEAD
      git push origin --delete <old-branch>
```

Omit lines that did not change. If `OLD_SLUG == NEW_SLUG`, print *"Slug unchanged — only state.json was refreshed."*. If `branch`, `slug`, `ticket`, and `input_type` are all already current, print *"Already in sync."* and exit without writes.

---

## Hard Rules

- Exit cleanly (zero) when there is no `.specwork/` to resync. This skill is a recovery tool — never an error path for fresh repos.
- Never touch the remote — no `git push`, no `git push --delete`. Print instructions for the user to run those manually.
- Never overwrite an existing state.json belonging to a different slug. Collision means abort with manual cleanup needed.
- Do not modify `source_title`. That is the user's original spec source and must not be implicitly rewritten.
- The file rename + state.json update are not atomic. If a `mv` fails mid-flight, surface the error so the user can recover manually — do not attempt automatic rollback.
- Idempotent: running `/sdd:resync` when nothing needs syncing prints "Already in sync" and exits.

---

## Related Skills

- `/sdd:start` — initializes the pipeline; can produce the state this skill resyncs
- `/sdd:whatnext` — shows pipeline status; will block when branch ≠ state.json::branch (this skill resolves that)
- `/sdd:close` — clears `.specwork/` after merge; use when both old and new slugs need to be wiped
