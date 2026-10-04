---
name: cross-worktree-fix
description: Use when applying the same fix to multiple FinancialDevelopment worktrees — enumerate worktrees, apply a patch to each, and commit per-worktree instead of re-editing by hand.
---

# Cross-worktree shared-fix

Apply one fix to every active `FinancialDevelopment` worktree without hand-editing each one.

## When to use
- A bugfix, dependency note, or doc correction needs to land in multiple worktrees that share the
  same file (e.g. `dashboard` fail-fast, `vol-suite` SKILL.md sync, `var-tools` fix). These have
  recurred as the SAME fix committed 3–4× across worktrees.

## Procedure
1. **List worktrees:**
   `git worktree list` (from the repo root). Note each path + branch.
2. **Target only worktrees that contain the file** you're changing:
   `test -f <wt>/<relpath> && echo present`. Skip worktrees without the file.
3. **Prepare ONE patch file** representing the canonical change (against the shared/base content).
   Prefer a `.diff`/`.patch` you can apply identically to each.
4. **Apply + commit per worktree** (do NOT commit to master):
   ```
   for wt in <path1> <path2> ...; do
     (cd "$wt" && git apply <canonical.patch> && git add -A && \
      git commit -m "fix(scope): <same message>" )
   done
   ```
   Use `git apply` (not `git am`) so it's path-relative per worktree.
5. **Verify** each worktree's diff landed: `git -C "$wt" log --oneline -1`.
6. Do NOT use this for content that legitimately differs per worktree — that needs manual editing.

## Caveats
- Worktrees are separate branches; a commit in one does NOT appear in another.
- Skip a worktree whose file content has diverged from the shared base (patch may not apply) —
  flag it and reconcile manually.
- Never run this on `master` unless the change is intended for the main line.
- The `scripts/apply-to-worktrees.sh` helper in this skill wraps steps 3–5 for a single patch file.
