---
name: mcp-ai-wpoos-git-ops
description: Git/GitHub workflow discipline for the mcp-ai-wpoos repo — PRs against `alpha-working` with owner-merge, commit style, staged commits (no `git add -A`), the stacked-PR rebase recipe for when a parent PR gets squash-merged, shared-worktree discipline for the multi-agent repo (check the branch before committing, never `reset --hard` over other agents' unstaged edits, `--autostash` rebases), conflict verification via `git merge-tree`, and gh CLI gotchas (`gh workflow run` 404 on non-default branches, long PHP lint checks). Use when creating/rebasing/fixing PRs, resolving PR conflicts, or dispatching workflows.
---

# mcp-ai-wpoos — Git & PR ops

## Branch & PR discipline

- **PR base is `alpha-working`.** The owner merges manually — agents never
  merge their own PRs. Clusters land as one PR per cluster (see the
  `mcp-ai-wpoos-test-suite` skill for the cluster workflow).
- Branch naming: `feat/<track>-<descriptor>`; stack dependent work on top of
  the unmerged parent branch and say so in the PR body.
- **Stage explicitly.** Never `git add -A` — the worktree often holds build
  artifacts and local state (e.g. `.lighthouseci/`, `test-results/`). Use
  explicit paths, or pathspec exclusions:
  `git add examples/nvoos-astro-velocity ":(exclude)…/test-results"`.
- Commits: imperative subject ≤ 50 chars, body only when useful (wrap at 72).
  Run commits with `GIT_EDITOR=true git commit …`; read-only git with
  `--no-pager`; prefer `git --no-optional-locks status`.

## Stacked PRs after a squash merge (the recipe that works)

When the parent PR was **squash-merged**, a stacked branch shows add/add
conflicts on every file both sides "added" — even when the squashed tree is
byte-identical to your baseline. Fix by rebasing **only your delta** onto the
updated base:

```bash
git fetch origin alpha-working
# Optional diagnosis — exits 1 when conflicts exist:
git merge-tree --write-tree origin/alpha-working HEAD
# Verify the squash tree equals your old baseline (empty diff = clean replay ahead):
git diff <squash-merge-sha> <old-baseline-sha>
# Replay only the commits after the baseline:
git rebase --onto origin/alpha-working <old-baseline-sha> <branch>
git push --force-with-lease origin <branch>
```

- Expect **zero conflicts** during the replay when the squash tree matches
  your baseline; conflicts mean something else changed — abort and
  investigate before continuing.
- After the rebase the PR shows only your delta; re-verify
  `gh pr view <n> --json mergeable,mergeStateStatus` (`MERGEABLE`).
- GitHub Docs reference: "Managing stacked pull requests" /
  "Troubleshooting stacked pull requests" (`gh stack rebase` alternative).

## Shared worktree discipline (multi-agent repo, learned 2026-10-30)

Parallel agents share the same checkout and switch branches between tasks.
Four rules, each from a session that cost a recovery:

- **Check the branch before committing.** `git branch --show-current` and
  `git log --oneline -1` before `git add`/`commit` — a commit lands on
  whatever branch is checked out, and the worktree may have been switched
  under you (a build fix once landed on another agent's
  `feat/mcp-sdk-skill-updates`).
- **Recovering a stray commit:** cherry-pick it onto your branch, then
  restore the foreign branch with `git reset --mixed <its-old-head>` +
  `git restore --worktree -- <only-the-files-you-touched>`. **Never
  `git reset --hard` in a shared worktree** — it wipes other agents'
  uncommitted tracked edits (e.g. a modified `SKILL.md`).
- **Rebasing with foreign unstaged edits present:** plain `git rebase`
  refuses ("You have unstaged changes"); use `git rebase --autostash` — it
  stashes only tracked changes and pops them back.
- **Merged PRs freeze their head.** A squash-merged (closed) PR stops
  tracking branch pushes — `gh pr view` keeps showing the stale `head_sha`.
  After the owner merges, run the stacked-PR recipe above and open a fresh
  PR for the delta (PRs #7302 → #7303).
- **Multiple linked worktrees exist — aim every git command.** Other
  agents keep `git worktree add` checkouts (see `git worktree list`). A
  `git cherry-pick` run from the wrong directory acts on the wrong
  worktree (2026-10-31: one silently no-op'd in the main worktree while
  the target was a linked one — caught by the "cherry-pick is now empty"
  message). Check `git rev-parse --show-toplevel` first, or use
  `git -C <abs-worktree-path>` for any command aimed at another worktree.
- **Dirty shared worktree + moved base → `git worktree add`, never a
  checkout.** When `origin/alpha-working` advanced and other agents'
  uncommitted files block `git checkout -b` ("would be overwritten by
  checkout"), don't stash their work: `git worktree add ../<name> -b
  <branch> origin/alpha-working`, then operate there via `git -C` (and
  `npm pack <abs-dir>` rather than `--prefix`). `git worktree remove`
  when done — the shared checkout was never touched.
- **De-stack a PR without `reset --hard`:** move the branch back with
  `git reset --mixed <parent>` (worktree untouched), restore only your own
  paths with `git restore --worktree -- <your-paths>` (a file you created
  becomes untracked again — plain `rm`), then
  `git push --force-with-lease`. Other agents' unstaged edits survive
  byte-for-byte. Verified 2026-10-31 de-stacking PR #7325.
- **Sibling PRs editing the same file (the #7348 ↔ #7349 case, 2026-11-01):**
  two open PRs touch the same docs file in overlapping hunks; the later one
  merges first and the earlier one reports merge conflicts at merge time.
  Fix: `git fetch origin` → `git checkout <branch>` →
  `GIT_EDITOR=true git rebase --autostash origin/alpha-working`, resolve by
  **keeping both PRs' intents** (the merged PR's new text usually wins for
  shared lines; your PR's unique additions stay), then
  `git push --force-with-lease`. A successful rebase replay is proof the
  conflict is gone — by construction the branch is ahead of the base.
- **Local `.git/info/exclude` can silently block deliberate files.** The
  main worktree ignores `*.png`/`*.jpg` (per-worktree media guard, not repo
  config). `git add` then fails with "ignored by one of your .gitignore
  files" — run `git check-ignore -v <path>` to find the rule and `git add -f`
  when the file is deliberate (gateway logo assets, PR #7349).

## Windows reserved-name artifacts (learned 2026-10-29)

A stray untracked file literally named `nul` (Windows reserved device name)
can appear in the repo root. Two failure modes follow:

- **`git stash push -u` aborts partway** with `failed to remove nul:
  Permission denied` — the stash IS saved, but tracked files stay modified
  and the untracked files get hidden in the stash's third parent.
  Recovery: list with `git ls-tree -r --name-only "stash@{N}^3"` and restore
  with `git checkout "stash@{N}^3" -- <paths>` (exclude `test-results/`).
  When only a few tracked files block a branch switch onto a moved base,
  the lighter tool is a pathspec stash: `git stash push -m <msg> -- <paths>`,
  switch, then `git checkout stash@{0} -- <paths>`.
- **Deleting the file itself:** normal `rm`/`del` fail (device semantics).
  Write a tiny `.ps1` using `Remove-Item -LiteralPath "\\?\<abs-path>"`
  (forward slashes OK after the prefix) and run it with
  `powershell -NoProfile -ExecutionPolicy Bypass -File` — inline `-Command`
  calls get the backslashes mangled by the sh layer. Never stage it —
  explicit staging (above) keeps it out of commits.

## Windows sh-shell gotchas (learned 2026-11-01, gateway session)

- The terminal runs **sh, not cmd**: `copy` does not exist — use `cp`;
  `del`/`ren` are `rm`/`mv`.
- **`powershell -Command` inline strings get `$var` interpolated away by the
  sh layer** (every `$i` vanished → parser errors). Write a `.ps1` file and
  run `powershell -NoProfile -ExecutionPolicy Bypass -File`, or do it in
  node instead (e.g. JPEG/PNG dimension sniffing from the file header — no
  deps needed).
- `findstr /C:"..."` quoting breaks under sh — pipe to node for filtering
  or use the terminal tool's `tail_lines`.
- `node --test <directory>` does **not** recurse on this setup (runs one
  file) — pass explicit files or the package's `npm test` script.
- Windows-reserved names: see the `nul`-artifact section above (same
  `powershell -File` pattern applies).

## gh CLI gotchas

- **`git archive` strips `package.json` and `bin/` repo-wide** — the root
  `.gitattributes` export-ignores them (meant for the plugin's release
  zips). Never `git archive <rev> packages/<pkg>` to extract package
  content (silently incomplete tar) — copy from a worktree checkout
  instead.
- `gh workflow run <name>` **404s unless the workflow file exists on the
  default branch (`main`)** — for `alpha-working`-only workflows dispatch via
  the API (`POST /actions/workflows/<id>/dispatches` with `ref=alpha-working`)
  or push a trigger.
- `gh pr checks <n>` shows queued runs; the repo-wide **PHP Linting workflow
  takes ~20–30 minutes** — don't retry or "fix" it while it's simply running.
- After a forced push, GitHub recomputes conflict status automatically;
  re-check `mergeable` before reporting done.

## PR hygiene

- PR body states: what changed, validation actually run (with counts), and —
  for stacked PRs — the parent PR number and that the diff delta is the last
  commit.
- Don't claim validation that wasn't run. Reference files by project-relative
  path.
