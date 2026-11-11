---
name: whatnext
description: Show where you are in the feature pipeline and what to do next
allowed-tools: Bash(git branch:*), Bash(git rev-parse:*), Bash(git rev-list:*), Bash(git status:*), Bash(find .specwork:*), Bash(cat .specwork/_state/*), Bash(cat .specwork/_spec/*), Bash(cat .specwork/_progress/*), Bash(grep:*), Bash(test:*), Bash(python3:*)
---

# What Next

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/whatnext/SKILL.md`

---

## Description

Inspects the current branch and `.specwork/` artifacts to determine exactly where
the developer is in the feature pipeline, then prints a focused "what to do next"
message with a one-line explanation of why.

This skill gives guidance, not a status dump. The output is always short.

---

## States

The pipeline reports one focused state at a time:

- **setup**: no SDD state detected yet
- **ready**: spec exists, Open Questions are resolved, no implementation commits yet
- **in-progress**: working tree has active implementation changes
- **review-ready**: branch is clean and has commits ahead of the feature base branch
- **blocked**: the current branch/setup is incompatible with the next pipeline step

Use Cases:

- `/sdd:whatnext` — contextual next step for the current branch (shows state + next action)
- `/sdd:whatnext overview` — full pipeline reference card, all commands explained

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Detects current branch and checks whether `.specwork/_state/*-state.json` exists |
| 2 | Reads the active state file to get the feature slug and base branch |
| 3 | Evaluates branch compatibility, spec state, open questions, worktree state, and commits ahead of base |
| 3.5 | On a branch mismatch, classifies it with `pipeline-inventory` — merged leftovers take different advice than live work elsewhere (see **Blocked States**) |
| 4 | Prints the pipeline with checkmarks showing progress (optional steps tagged `(optional)`) |
| 5 | Prints a "Next step" block with the command and a one-line explanation |

---

## Detection Logic

Handle `/sdd:whatnext overview` first: print the static reference card and stop.

For contextual mode, evaluate in this order:

| Condition | Next step if NOT met |
|-----------|---------------------|
| `.specwork/_state/<slug>-state.json` exists | `/sdd:start <ticket-or-text>` |
| Current branch matches the `branch` value in `.specwork/_state/<slug>-state.json` | Blocked — classify the mismatch first (see **Branch mismatch** below); merged leftovers → `/sdd:close`, live work elsewhere → switch back |
| `.specwork/_spec/<slug>-spec.md` exists | `/sdd:spec` (draft the spec — `/sdd:start` bootstraps state but does not write the spec) |
| Spec `## Open Questions` has no `- [ ]` items | Resolve open questions in the spec (or `/sdd:spec` with the answers as context) |
| Pending-stage file contains real paths | `/sdd:commit` |
| No uncommitted or unstaged changes (`git status` clean) | `/sdd:implement` |
| Branch has commits ahead of its recorded `base_branch` | `/sdd:mr` |

Use the state file's `base_branch` when checking whether the branch is ahead. If it
is missing, fall back to `development`, then `main`.

**Optional steps** — not part of the core detection chain. Suggest them only when
they are clearly relevant:
- `/sdd:test-design` + `/sdd:test-impl` — if you want gap-focused test coverage designed and implemented
- `/sdd:code-review` — quality + security review before MR
- `/sdd:handoff` — when another agent or model should take over execution

If the branch is clean and ahead of base, print `/sdd:mr` as the next step. Mention
`/sdd:mr-address` only as a follow-up after review comments arrive.

### Default next-step recommendation

After `/sdd:start` finishes, the spec does not exist yet — suggest `/sdd:spec` to draft it (and run triage). Once the spec is drafted, suggest `/sdd:plan` as the default checkpoint for medium-to-large features. For small/obvious changes the developer can skip planning and run `/sdd:implement` directly — the optional steps in the pipeline checklist (`/sdd:plan`, `/sdd:test-design`, `/sdd:test-impl`, `/sdd:code-review`) are always tagged `(optional)` so the developer can decide.

```
Next step:
  /sdd:mr

  Your branch is clean and contains committed work ahead of the base branch.
  Open or update the MR next. Use /sdd:mr-address after teammates leave comments.
```

---

## Output Format

When **ready** (initialized and ready to implement):

```
Pipeline: feature/PROJ-15535  [ready]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted, all questions resolved
→  /sdd:plan          (optional, recommended for medium-to-large features)
○  /sdd:implement     implement and test inline
○  /sdd:test-design   (optional)
○  /sdd:test-impl     (optional)
○  /sdd:code-review   (optional)
○  /sdd:mr
○  /sdd:mr-address

Next step:
  /sdd:plan (or /sdd:implement directly for small/obvious changes)

  Discover target files and draft an implementation plan, then implement.
```

When **blocked** (has unresolved questions):

```
Pipeline: feature/PROJ-15535  [blocked]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted
✗  /sdd:implement     blocked — 2 unresolved Open Questions

Next step:
  Resolve open questions in `/abs/path/repo/.specwork/_spec/proj-15535-spec.md:42`

  Unresolved:
    - [ ] #1 Should lookup use personUuid only, or personUuid + collateral?
    - [ ] #2 If multiple existing leads match, should we update latest or fail?

  Then run /sdd:implement.
```

**Path requirements:**

1. **Absolute** — relative paths are not clickable in Claude Code's CLI, VSCode/Cursor terminals, iTerm2, or Warp. Build it with `ABS="$(cd "$(dirname "$SPEC")" && pwd)/$(basename "$SPEC")"`.
2. **Wrapped in single backticks** — forces Claude Code's renderer to color the path so it stands out from the surrounding label.

The `:42` suffix is the line number of the `## Open Questions` heading: `grep -n "^## Open Questions" "$SPEC" | head -1 | cut -d: -f1`. Apply the same pattern to the second blocked output below.

Do **not** wrap the whole blocked-state block in a fenced code block when emitting it — fenced blocks suppress inline-code coloring on the path.

Legend:
- `✓` — completed
- `→` — current / in progress
- `○` — not started (may be `(optional)`)
- `✗` — blocked (unresolved Open Questions)

### Stale leftovers footnote

When the current branch **does** own its pipeline but `pipeline-inventory`
reports a non-empty `closable`, the leftovers are not this branch's problem —
they change nothing about the next step. This skill gives guidance, not a status
dump, so do not grow a section for them: append exactly one line after the
`Next step:` block, and only when there is something to report.

```
Note: 1 merged pipeline still in .specwork/ (PROJ-15500) — /sdd:close clears it.
```

Pluralize and name up to two slugs; beyond that use a count (`3 merged pipelines
still in .specwork/`). This never becomes a `✗` line, never changes `Next step:`,
and is omitted entirely when `closable` is empty — which is the normal case. For
the full list, `/sdd:state` prints its `Stale:` block.

---

## Blocked States

### Branch mismatch — classify before advising

`.specwork/` is gitignored, so it survives `git checkout` and outlives the branch
it belongs to. When the current branch does not own the pipeline on disk, there
are two very different reasons, and they take opposite advice: work still in
flight on another branch (go back to it) versus a merged feature whose
`/sdd:close` was never run (clear it). Telling someone to "resume" a pipeline
that already shipped sends them to look for work that no longer exists.

Resolve which one it is before printing anything:

```bash
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-inventory "$CURRENT_BRANCH"
```

Branch on the JSON — never on how the branch names look. `closable` holds the
orphans whose work already landed (`merge_status` of `merged` or `branch-gone`);
`orphans` holds every pipeline this branch does not own.

### Leftovers from a merged pipeline (blocked)

No entry is `is_current` and `closable` is non-empty:

```
Pipeline: feature/newwork  [blocked]
──────────────────────────────────────
✗  /sdd:start         blocked — .specwork/ still holds a finished pipeline

Next step:
  /sdd:close

  PROJ-15500 (feature/PROJ-15500) already merged into development, but its
  .specwork/ state was never cleared — so it blocks starting anything new here.
  Clear it from its own branch, or from its base, then run /sdd:start.
```

Render the reason from `merge_status`: `merged` → "already merged into
`<base_branch>`"; `branch-gone` → "its branch no longer exists locally". For a
`branch-gone` entry, add one line — a rename that skipped `/sdd:resync` is
indistinguishable from a merged-and-deleted branch, and `/sdd:close` would throw
away live work:

```
  If feature/PROJ-15500 was renamed rather than merged, run /sdd:resync instead.
```

Say "already merged" as the *reason reported by git*, never as verified fact:
`merge_status` only asks whether the branch is an ancestor of its base.
`/sdd:close` re-checks the real MR state via `glab` before deleting anything.
Never run `/sdd:close` here — this skill is read-only.

### Not on the recorded pipeline branch (blocked)

No entry is `is_current` and `closable` is **empty** — the pipeline belongs to
another branch and has not landed (`open`, or `unknown` when git could not tell).
Closing it would destroy unmerged work, so send the user back to it. Name the
branch from the first orphan's `branch` rather than pointing at the state file:

```
Pipeline: feature/PROJ-15535  [blocked]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted
✗  /sdd:implement     blocked — current branch does not match recorded pipeline branch

Next step:
  Switch back to feature/PROJ-15535

  The active .specwork state belongs to a different branch and has not been
  merged. Resume work on that branch before continuing the pipeline.
```

---

### Unresolved Open Questions in spec (blocked)

```
Pipeline: feature/PROJ-15535  [blocked]
──────────────────────────────────────
✓  /sdd:start         state + source written
✓  /sdd:spec          spec drafted
✗  /sdd:implement     blocked — 2 unresolved Open Questions

Next step:
  Resolve open questions in `/abs/path/repo/.specwork/_spec/proj-15535-spec.md:42`

  Unresolved:
    - [ ] #1 Should lookup use personUuid only, or personUuid + collateral?
    - [ ] #2 If multiple existing leads match, should we update latest or fail?

  Mark each resolved:
    - [x] #1 Should lookup use personUuid only, or personUuid + collateral? — resolved: personUuid + collateral
    - [x] #2 If multiple existing leads match, should we update latest or fail? — resolved: fail
  
  Then run /sdd:implement.
```

---

## Overview Mode

`/sdd:whatnext overview` prints the static pipeline reference card from
`${CLAUDE_PLUGIN_ROOT}/skills/whatnext/REFERENCE.md` § Overview Mode verbatim,
regardless of branch state, and stops. Contextual mode never reads that file.

---

## Requirements

- Run from any branch; best results when you are on the branch recorded in `.specwork/_state/*-state.json`
- Read-only — makes no changes

---

## Related Skills

- `start` — initializes the pipeline and writes `state.json` (the spec is drafted by `/sdd:spec`)
- `spec` — drafts and refines the spec
- `state` — detailed state dump (commits, plan steps, open questions counts)
- `implement` — implements the next step
- `commit` — commits and marks step complete
- `close` — clears `.specwork/`; the fix when the blocker is a merged leftover
