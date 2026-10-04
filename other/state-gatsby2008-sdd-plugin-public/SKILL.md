---
name: state
description: Show a concise snapshot of the active pipeline branch
allowed-tools: Bash(git rev-parse:*), Bash(git branch:*), Bash(git log:*), Bash(git status:*), Bash(git diff:*), Bash(find .specwork:*), Bash(find docs:*), Bash(cat .specwork/_review/*), Bash(grep -n:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*)
---

# State

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/state/SKILL.md`

---

## Description

Show a short snapshot of the current pipeline branch: what exists, what is blocked,
and the next best step. Keep the default output compact.

---

## Use Cases

- `/sdd:state` — auto-detect current branch
- `/sdd:state PROJ-15535` — explicit ticket ID

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Detect branch and ticket/slug |
| 2 | Read `.specwork/` artifacts; count open questions with code (see below) |
| 3 | Read review files if present |
| 4 | Check `git status` and recent commits |
| 5 | Inventory `.specwork/` for orphan pipelines that already landed (see **Stale Leftovers** below) |
| 6 | Print a compact status plus one next step |

---

## Output Format

The `N open / M resolved` counts come from code, not by eyeballing the section:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py count-oqs <slug>   # prints "<open> <resolved>"
```

Default output should stay short:

```text
Branch: feature/PROJ-15535
Spec:   ✓ PROJ-15535-spec.md (2 open / 1 resolved OQs)
        `/abs/path/repo/.specwork/_spec/PROJ-15535-spec.md:42`  ← Open Questions
Plan:   ✓ PROJ-15535-plan.md (1 open OQ)
        `/abs/path/repo/.specwork/_plan/PROJ-15535-plan.md:88`  ← Open Questions
Tree:   clean
Next:   /sdd:plan (recommended, can skip)
        /sdd:implement
```

Use full detail only when the user asks for it or when a blocker needs explanation.

### Stale Leftovers

`.specwork/` is gitignored, so it survives `git checkout` and outlives the branch
it belongs to — a merged feature whose `/sdd:close` was never run keeps sitting
there, and later blocks `/sdd:start`. `/sdd:state` is where the user looks to
orient, so surface those leftovers here instead of letting them be discovered as
a refusal later:

```bash
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-inventory "$CURRENT_BRANCH"
```

Read the `closable` array — orphan pipelines (not owned by this branch) whose
`merge_status` says the work already landed. **Omit the `Stale:` block entirely
when `closable` is empty**; this is an exception report, not a standing section,
and the default output stays compact. Never derive this by eyeballing branch
names — branch on the JSON.

When it is non-empty, print one block between `Tree:` and `Next:` (`Next:` stays
last — it is the action):

```text
Stale:  2 orphan pipelines in .specwork/ — their work already landed
        • PROJ-15500 (feature/PROJ-15500) — merged into development
        • PROJ-15490 (feature/PROJ-15490) — branch no longer exists locally
        Clear each from its own branch, or from its base, with /sdd:close.
```

One bullet per `closable` entry, rendering its reason from `merge_status`:
`merged` → "merged into `<base_branch>`"; `branch-gone` → "branch no longer
exists locally". The trailing line names both branches because `/sdd:close`
hard-stops on an unrelated third branch: it runs from the pipeline's own branch
**or** its `base_branch` — and for a `branch-gone` entry the base is the only
option left.

Two things this block must not do:

- **Never present it as a blocker.** These leftovers do not affect the current
  branch's pipeline; `Next:` is computed exactly as it would be without them.
- **Never run `/sdd:close`**, and never state the work *is* merged as fact.
  `merge_status` is derived from git alone (is the branch an ancestor of its
  base?), and a branch renamed without `/sdd:resync` looks identical to one
  merged and deleted. `/sdd:close` re-verifies the real MR state via `glab`
  before deleting anything.

If the current branch has **no pipeline of its own** (no entry with
`is_current: true`), say so plainly rather than reporting on someone else's
pipeline — this is the case where the leftovers are the whole answer:

```text
Branch: feature/newwork
Spec:   × no pipeline on this branch
Stale:  1 orphan pipeline in .specwork/ — its work already landed
        • PROJ-15500 (feature/PROJ-15500) — merged into development
        Clear it from its own branch, or from its base, with /sdd:close.
Next:   /sdd:start <ticket|description>
```

### Linking to Open Questions

Whenever the line for `Spec:` or `Plan:` reports **one or more open** questions (`N open`, N ≥ 1), print a follow-up indented line with the **absolute path** and the line number of the `## Open Questions` heading, **wrapped in single backticks** (same approach as `/sdd:whatnext`'s blocked outputs):

1. **Absolute** — relative paths are not clickable in Claude Code's CLI, VSCode/Cursor terminals, iTerm2, or Warp.
2. **Wrapped in single backticks** — Claude Code's renderer colors the path token so it stands out from the surrounding label.

Do **not** wrap the whole status block in a fenced code block (` ``` `) when emitting it — fenced blocks suppress inline-code coloring.

Compute the absolute path, line number, and backticked output with:

```bash
for artifact in ".specwork/_spec/<slug>-spec.md" ".specwork/_plan/<slug>-plan.md"; do
  [ -f "$artifact" ] || continue
  ABS="$(cd "$(dirname "$artifact")" && pwd)/$(basename "$artifact")"
  LINE="$(grep -n "^## Open Questions" "$artifact" | head -1 | cut -d: -f1)"
  [ -n "$LINE" ] && echo "        \`${ABS}:${LINE}\`  ← Open Questions"
done
```

Format: `` `<absolute-path>:<line>` ``  ← Open Questions (two spaces before the arrow).

Omit the follow-up line entirely when:
- The artifact has no `## Open Questions` section, or
- All items in the section are resolved (`0 open`), or
- The artifact itself doesn't exist (e.g., `Plan: ×`).

### Rendering `Next:`

**Spec gate first.** If `.specwork/_spec/<slug>-spec.md` does not exist, the only next step is `/sdd:spec` (draft the spec) — `/sdd:start` bootstraps state but does not write the spec. Render:

```text
Next: /sdd:spec (draft the spec)
```

Once the spec exists, use the generic pipeline chain to pick `Next:` — `/sdd:plan → /sdd:implement → /sdd:commit → /sdd:mr` (with `/sdd:test-design` and `/sdd:test-impl` available between `/sdd:implement` and `/sdd:commit` for high-risk changes). Pick the first step that has no artifact yet.

Render `Next:` in one of two forms:

- **Single, required** — the next step is non-skippable (`/sdd:implement`, `/sdd:commit`, `/sdd:mr`):
  ```text
  Next: /sdd:implement
  ```
- **Dual, recommended-but-skippable** — the next step is optional (`/sdd:plan`, `/sdd:test-design`, `/sdd:test-impl`) AND the following non-optional step is a distinct alternative the user can jump to directly:
  ```text
  Next: /sdd:plan (recommended, can skip)
        /sdd:implement
  ```

Use the dual form when an optional step still has no artifact and the developer might reasonably skip it. Use the single form when only a required step remains.

If `.specwork/_state/<slug>-path.json` exists (written by triage during `/sdd:spec` draft), read it as the authoritative source for `Next:`. The triage path determines the first pending step.

---

## Rules

- Prefer counts and status symbols over long tables
- Skip step-by-step detail if no plan exists
- Show review verdicts only as PASS / WARNINGS / FAIL
- Show ADR warnings only if uncommitted files exist in `docs/adr/`
- Show the `Stale:` block only when `pipeline-inventory` reports a non-empty `closable` — see "Stale Leftovers" above
- For `Next:`, use the dual form (recommended + skip target) only when the recommended step is optional and a distinct fallback exists — see "Rendering `Next:`" above

---

## Requirements

- Run from any point in the pipeline

---

## Related Skills

- `start` — bootstraps pipeline state (source + state files)
- `spec` — drafts and refines the spec
- `implement` — writes changes
- `commit` — records step completion
- `code-review` — code quality/security review
- `mr` — open the MR
- `close` — clears `.specwork/`; the fix for anything reported under `Stale:`
- `whatnext` — contextual next step guidance
