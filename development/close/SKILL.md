---
name: close
description: Wipe all `.specwork/` artifacts to close out a feature. Run after the MR is merged, or before starting a new feature pipeline. Verifies MR status when a feature branch is detected and warns before deleting unmerged work.
allowed-tools: Bash(git branch:*), Bash(git checkout:*), Bash(git rev-parse:*), Bash(git status:*), Bash(git log:*), Bash(git remote:*), Bash(glab:*), Bash(find .specwork:*), Bash(rm:*), Bash(test:*), Bash(ls:*), Bash(command -v:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*)
---

# Close Feature

Wipe `.specwork/` clean. This is the canonical cleanup command — run it after the MR is merged, or any time you need to reset before starting a new feature.

**`/sdd:close` never deletes source code or touches remote branches.** If the working tree is dirty, it asks first: pause (stash) or discard. After that, it only deletes `.specwork/` and offers local branch cleanup.

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Deterministically resolves which pipeline (if any) governs the current branch, and whether closing here is safe, before any deletion |
| 2 | Checks working tree: dirty → offer pause or discard; clean → proceed |
| 3 | Checks MR status via `glab` for the *pipeline's own* branch and warns if not merged |
| 4 | Lists every file in `.specwork/` that will be deleted |
| 5 | Notes if spec was published to `docs/specs/` (preserved) |
| 6 | Asks for confirmation |
| 7 | Deletes every file under `.specwork/_*/` |
| 8 | On a feature branch: offers to delete the local branch and switch back to the parent |
| 9 | Prints summary |

At entry, rehydrate non-interactive mode from state when available (uses the
`slug` resolved in Step 1 below — read that step first):

```bash
if [ "${SDD_NON_INTERACTIVE:-0}" != "1" ] && [ -n "${SLUG:-}" ]; then
  SDD_MODE="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py non-interactive "$SLUG" 2>/dev/null || echo 0)"
  [ "$SDD_MODE" = "1" ] && export SDD_NON_INTERACTIVE=1
fi
```

"Safe to run from any branch" means specifically: the pipeline's own branch,
**or** the branch it was started from (`base_branch` — the normal "MR merged,
back on the base branch, now cleaning up" flow). It does **not** mean any
unrelated branch that happens to have someone else's leftover `.specwork/`
sitting on disk — Step 1 tells those apart and hard-stops on the latter.
If the working tree is dirty, you choose: pause (preserves changes) or discard.

---

## Step 1 — Resolve Pipeline & Verify It's Safe To Close Here (STRICT)

`.specwork/` is gitignored, so it does **not** move with branch changes — it
commonly still holds a *different* branch's pipeline after a `git checkout`.
Never decide "is this my pipeline?" by eyeballing branch names or trusting
`resolve-slug`'s "first file found" fallback — call the shared check, which
inspects every `state.json`'s recorded `branch` field:

```bash
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
STATUS="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-branch-status "$CURRENT_BRANCH")"
```

`STATUS` is one JSON object: `has_any_pipeline`, `owns_pipeline`, `slug`,
`recorded_branch`, `recorded_base_branch`, `is_base_branch`. Derive from it:

- `SLUG` = `.slug` — used by every later step (waiver/state lookups, Step 3's
  MR check, the non-interactive rehydration above).
- `RECORDED_BRANCH` = `.recorded_branch` — the pipeline's own branch. Step 3
  checks *this* branch's MR, not `current_branch`.
- `PARENT` = `.recorded_base_branch`, falling back to
  `git remote show origin | sed -n 's/.*HEAD branch: //p'`, then `main`, only
  when `recorded_base_branch` is empty. Capture as `parent_branch` — Step 8
  uses it.
- `branch_id`: extract a ticket id from `RECORDED_BRANCH` (e.g.
  `feature/PROJ-15535-foo` → `PROJ-15535`) — **not** from `current_branch`;
  Step 3's MR lookup must target the pipeline's own branch, not whatever
  branch you happen to be standing on. `none` if `RECORDED_BRANCH` is empty or
  has no recognizable ticket.

Then branch on safety:

- **`has_any_pipeline` is `false`** — nothing on disk. Proceed straight to
  Step 4 (it will report "already empty" and exit cleanly).
- **`owns_pipeline` is `true`, or `is_base_branch` is `true`** — this is
  either the pipeline's own branch, or the base branch you returned to after
  merging. Both are the intended "safe to run from any branch" cases —
  continue normally to Step 2.
- **Neither** — `.specwork/` belongs to a genuinely unrelated third branch
  (`recorded_branch`, slug `slug`), not to `current_branch` and not to its
  base. Deleting here would wipe out a pipeline this branch has nothing to do
  with, and Step 8's branch-cleanup prompt would be offering to delete/switch
  *this* branch based on that unrelated pipeline's `base_branch` — both wrong.
  Hard-stop instead of deleting:
  ```
  ✗ Cannot close here.

  .specwork/ belongs to '<recorded_branch>' (slug '<slug>'), not '<CURRENT_BRANCH>'
  or its base. It's gitignored and didn't move when you switched branches — it
  is still on disk, but it is not this branch's pipeline to close.

    • To close it: switch to '<recorded_branch>' and run /sdd:close there.
    • To pause it instead: switch to '<recorded_branch>' and run /sdd:pause.
    • This branch itself has no pipeline of its own — /sdd:start to begin one.
  ```

Only continue past this gate on the last two outcomes above.

---

## Step 2 — Dirty Tree Check

Check for uncommitted changes:

```bash
git status --porcelain
```

If the working tree is dirty:

```
Uncommitted changes detected.

  p) Pause — save everything (code + specwork) via pause, then close
  d) Discard all changes and continue close
  q) Quit — handle changes manually
```

| Choice | Action |
|--------|--------|
| **p** | `git add -A && git add -f .specwork/ && git stash push -m "pause: $CURRENT_BRANCH"` — stashes code + specwork, then proceeds |
| **d** | `git restore . && git clean -fd` — discards tracked + untracked changes, then proceeds |
| **q** | Abort, leave everything as-is |

If the working tree is clean, skip this step.

---

## Step 3 — Check MR Status (only if `branch_id` is set)

If `branch_id == none`, skip this step entirely.

Find the working `glab` invocation:

```bash
GLAB=""
for candidate in glab /opt/homebrew/bin/glab /usr/local/bin/glab; do
  if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
    GLAB="$candidate"
    break
  fi
done
```

If `$GLAB` is empty, skip the MR check and warn:

```
⚠  glab not found — cannot verify MR status. Proceeding anyway.
   Install glab: brew install glab (macOS) or scoop install glab (Windows)
```

If `glab` is available, fetch MR state **for the pipeline's own branch**
(`recorded_branch` from Step 1) — **not** bare `glab mr view`, which defaults
to whatever branch is currently checked out. When `is_base_branch` is true
(you're on the base branch cleaning up post-merge) that's a different branch
than `current_branch`, and the bare form would silently check the wrong one —
or find nothing and report a false "no MR yet":

```bash
PAGER=cat $GLAB mr view "$RECORDED_BRANCH" --output json 2>/dev/null
```

Strip ANSI codes and parse `state` field.

| MR State | Action |
|----------|--------|
| `merged` | Proceed normally |
| `opened` | Warn: MR is still open. Ask to confirm anyway in Step 6. |
| `closed` | Warn: MR was closed without merging. Ask to confirm anyway in Step 6. |
| Not found / parse error | Warn quietly; treat as "no MR yet". |

---

## Step 4 — List Artifacts

Find every file under `.specwork/`:

```bash
find .specwork -type f 2>/dev/null
```

If no files found:

```
.specwork/ is already empty. Nothing to clean up.
```

Then exit cleanly.

Show what will be deleted, grouped by folder:

```
About to delete all files in .specwork/:

  Spec:     .specwork/_spec/<slug>-spec.md
            .specwork/_spec/<slug>-source.md
  State:    .specwork/_state/<slug>-state.json
            .specwork/_state/<slug>-rules.json
            .specwork/_state/<slug>-implementation-cache.json
  Plan:     .specwork/_plan/<slug>-plan.md
  Progress: .specwork/_progress/<slug>-context.md
            .specwork/_progress/escalations.md
  Reviews:  .specwork/_review/<slug>-code-review.md
            .specwork/_review/<slug>-mr-address.md
  Handoff:  .specwork/_handoff/<slug>-execution-pack.md
            .specwork/_handoff/<slug>-execution-pack.json

Total: <N> files
```

Use the actual filenames found, not the placeholder names above. Optional artifacts are listed only when present.

---

## Step 5 — Note if Spec Was Published to docs/specs/

Check if `.specwork/_spec/<slug>-spec.md` has a corresponding `docs/specs/<slug>-spec.md`.

If yes, note:

```
✓ Spec published to docs/specs/<slug>-spec.md — will be preserved
```

If no published spec exists, skip silently.

---

## Step 6 — Confirm

Combine all relevant warnings (open MR, closed MR, unmoved spec, discarded changes) into a single confirmation:

```
<warnings, if any>

Delete all files in .specwork/? (y / n)
```

- **y**: proceed to Step 7
- **n**: abort silently with `Canceled.`

---

## Step 7 — Delete

Wipe `.specwork/` completely — files **and** folders:

```bash
rm -rf .specwork/
```

`/sdd:start` recreates the folders it needs (`_spec/`, `_progress/`) on the next run via `mkdir -p`. Removing the whole directory is cleaner than leaving empty folders behind, and it self-adapts to any new subfolder a future skill might introduce.

Do **not** make a git commit — `.specwork/` is gitignored.

---

## Step 8 — Branch Cleanup

Offer to delete the local feature branch. Skip this step entirely when:

- `current_branch` equals `parent_branch` (already on the parent), **or**
- `branch_id == none` (not a recognizable feature branch), **or**
- `SDD_NON_INTERACTIVE=1` — never auto-delete a branch; fall through to the summary and leave the branch in place.

Otherwise prompt:

```
Branch '<current_branch>' is not the parent ('<parent_branch>').

  d) Delete local branch and switch to <parent_branch>
  k) Keep branch, switch to <parent_branch>
  s) Stay on '<current_branch>'
  q) Quit
```

| Choice | Action |
|--------|--------|
| **d** | Switch to the parent, then delete the feature branch (see helper below). If the parent cannot be checked out, stay put and do **not** delete. |
| **k** | Switch to the parent; keep the feature branch. |
| **s** | Stay on `current_branch`; keep the branch. |
| **q** | Stop here without switching or deleting. |

To switch to the parent safely — checking it out from `origin` when it only exists remotely:

```bash
checkout_parent() {
  if git rev-parse --verify --quiet "refs/heads/$PARENT" >/dev/null; then
    git checkout "$PARENT"
  elif git rev-parse --verify --quiet "refs/remotes/origin/$PARENT" >/dev/null; then
    git checkout -b "$PARENT" "origin/$PARENT"
  else
    echo "Parent branch '$PARENT' not found locally or on origin." >&2
    return 1
  fi
}
```

For **d**: run `checkout_parent` and only on success `git branch -D "$current_branch"`. `/sdd:close` **never** touches the remote branch — `git push origin --delete` is the user's call.

`/sdd:close` is always human-driven (it is never reached by `/sdd:auto`), so branch deletion stays an explicit, interactive choice.

---

## Step 9 — Summary

```
.specwork/ cleaned — <N> files removed.

<if the branch was deleted:>
Branch '<current_branch>' deleted — now on <parent_branch>.

<if switched but kept:>
Switched to <parent_branch> — '<current_branch>' preserved.

<if kept and stayed (or non-interactive):>
Branch:             <current_branch>             (kept as-is — delete it yourself with `git branch -d <branch>` when you're done)

<if branch_id is none:>
Ready to start a new feature with /sdd:start.
```

If changes were discarded, `git status` will be clean. Published specs in `docs/specs/` are preserved for permanent documentation reference.

---

## Related Skills

- `mr` — publishes the spec to `docs/specs/` (optional) and creates the MR
- `start` — starts the next feature pipeline and recreates `.specwork/`
