---
name: repoprompt-apply-edits-silent-format
description: |
  Diagnostic for `mcp__RepoPrompt__apply_edits` silently running a
  Prettier-style formatter across the entire file it touches, even when the
  project has NO formatter configured (no `.prettierrc`, no lefthook, no
  husky, no editorconfig). Use when: (1) you just made a small surgical
  edit with `apply_edits` and `git diff --shortstat` reports far more
  changed lines than you touched (e.g., your edit was ~50 lines but the
  diff is +742 -202), (2) the diff for that file contains suspicious
  unrelated reformatting hunks like split imports, wrapped long ternaries,
  added parens around `??` expressions, or string literals split across
  lines, (3) a code reviewer / Oracle flags "large unrelated reformat" in
  a PR that you intended to be a focused change. Covers the detection
  heuristic, the cleanup path (revert + re-apply minimal edits), and the
  prevention rule (always check `git diff --shortstat` after each
  `apply_edits` call, especially in projects without a formatter).
author: Claude Code
version: 1.0.0
date: 2026-05-15
---

# RepoPrompt apply_edits Silent Formatter

## Problem

`mcp__RepoPrompt__apply_edits` runs an internal Prettier-style formatter
across the entire file as part of its write step. This happens **even when
the project has no formatter configured** — there is no `.prettierrc`, no
lefthook hook, no husky pre-commit, nothing in `package.json` that would
explain the reformat. The tool's success message reports only the number
of lines it *intentionally* changed (e.g., `Lines changed: 27`), so the
hidden formatting churn is invisible until you inspect the actual diff.

In a recent session, ~50 lines of intentional edits to a 2,300-line `.tsx`
file produced a `+742 / -202` diff. The semantic change was a handful of
hunks; the rest was the formatter splitting long imports, wrapping
ternaries, parenthesizing `??` expressions, and breaking long string
literals across lines.

## Context / Trigger Conditions

You're seeing this bug if **any** of these hold after `apply_edits`:

1. `git diff --shortstat <file>` reports an insertions+deletions count
   dramatically larger than the lines you actually touched.
2. The `apply_edits` tool's response said "Lines changed: N" where N is
   small, but `git diff` shows hundreds of lines moving.
3. The diff contains hunks that look like cosmetic-only changes:
   - One-line `import { … } from "x"` becoming a multi-line import block
   - `condition ? a : b ? c : d` being broken into nested multi-line ternaries
   - `x ?? y` becoming `(x ?? y)` (added parens)
   - Long string literals being wrapped onto a new line
   - Function arg lists being split one-arg-per-line
4. The project has **no Prettier / oxfmt / dprint config** in the repo
   root (so this can't be blamed on a save-hook running locally).
5. A reviewer (human or Oracle) flags "large unrelated reformat" in a PR
   you intended to keep focused.

## Solution

### Detection (always do this after `apply_edits`)

Run this immediately after every `apply_edits` call where you care about
diff hygiene:

```bash
git diff --shortstat <file>
```

Compare the number against the `Lines changed: N` figure from the
`apply_edits` response (sum across all `Apply Edits` results in the
session for that file). If the git number is more than ~2× your reported
edits, the formatter has run.

### Cleanup (when you've already been bitten)

The cleanest recovery is to discard the file and re-apply only the
intended edits:

```bash
# 1. Discard the entire reformatted version (keeps other working changes)
git checkout -- <file>

# 2. Re-apply your targeted edits — but do it via `Edit` from the
#    standard Claude Code toolset, OR craft `apply_edits` calls whose
#    `replace` text already matches the formatter's output style for
#    that file's surrounding context. Surgical search/replace blocks
#    that don't span ternaries / long strings rarely trigger the
#    reformat of unrelated code.
```

Verify the cleanup worked:

```bash
git diff --shortstat <file>   # should now match your intended edit size
```

### Prevention

- **Always inspect `git diff --shortstat` after each `apply_edits`** in a
  project without a configured formatter. Treat large unexpected churn as
  a signal to back up and re-do.
- **Prefer many small `search`/`replace` edits over `rewrite`** of a
  whole file — the rewrite path is the most reliable way to trigger
  whole-file reformatting.
- **Keep `search` blocks short and structurally local** (don't span huge
  multi-line constructs) — the formatter is more likely to leave the
  surrounding code alone.
- **For purely surgical changes in formatter-sensitive files**, fall
  back to the standard Claude Code `Edit` tool, which does not run a
  formatter.

## Verification

After applying the cleanup pattern above:

```bash
git diff --shortstat <file>
```

Should report a count close to the lines you actually intended to
change. If it still shows large churn, your re-applied edit is also
triggering the formatter — split the edit into smaller, more local
search/replace blocks and try again.

You can also visually confirm by running:

```bash
git diff -U0 <file> | grep -E "^@@" | wc -l
```

A clean targeted edit usually has 1-5 hunks. Whole-file reformat-on-save
behavior produces dozens.

## Example

**Symptom:** I made these `apply_edits` calls on `app/routes/foo.tsx`:

```
Apply Edits ✅ Lines changed: 27
Apply Edits ✅ Lines changed: 1
Apply Edits ✅ Lines changed: 1
Apply Edits ✅ Lines changed: 1
Apply Edits ✅ Lines changed: 4
Apply Edits ✅ Lines changed: 10
```

Total intended change: **~44 lines**. But:

```
$ git diff --shortstat app/routes/foo.tsx
 1 file changed, 742 insertions(+), 202 deletions(-)
```

**Diagnosis:** The formatter ran. Inspecting hunks confirms it:

```
$ git diff -U0 app/routes/foo.tsx | grep -E "^@@" | wc -l
47
```

47 hunks for a logically-cohesive 6-edit change is wildly disproportionate.

**Cleanup:** `git checkout -- app/routes/foo.tsx`, then re-apply the 6 edits
using the standard `Edit` tool. After re-applying:

```
$ git diff --shortstat app/routes/foo.tsx
 1 file changed, 50 insertions(+), 6 deletions(-)
```

That matches the intended scope.

## Notes

- **Why this matters beyond aesthetics:** noisy diffs hurt code review,
  break `git blame` history (every reformatted line now points at *your*
  commit instead of the original author), and are conflict-prone in
  long-running branches.
- The formatter behavior appears consistent with Prettier defaults
  (printWidth ~80, trailing commas, parens around `??`). It's not
  configurable from the `apply_edits` MCP call.
- This is **not** the same problem as a project's lefthook/husky
  pre-commit hook running prettier — that one is visible (you can find
  the hook config) and intentional. The `apply_edits` reformat happens
  with no such config present.
- If your project *does* have a formatter configured and matching the
  RepoPrompt formatter's output, you won't notice this bug. The pain
  is concentrated in projects that have made an explicit choice to skip
  Prettier (common in early-stage React Router / Vite projects).
- Don't try to "fix" this by adding a Prettier config to the project just
  to silence the churn — that's tail wagging the dog. Address it at the
  edit-tool layer instead.

## See also

- `oxc-toolchain-setup` — for projects that *want* a formatter, this
  documents adding oxfmt + lefthook so the reformatting becomes
  intentional and consistent.
