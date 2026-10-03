---
name: pkg-ship
description: Implement a roadmap package end-to-end — read spec, branch in a worktree, implement with tests, sweep for stale call sites, open PR, fix CI, resolve conflicts.
invocation: /pkg-ship <pkg-name>
---

# /pkg-ship \<pkg-name\>

End-to-end package implementation skill. Codifies the spec → branch → implement → test → PR sequence that has shipped pkg42, pkg43, pkg54a-d, pkg55-A.0/A.1, pkg63, pkg67, pkg70, pkg72, pkg74, pkg82, pkg83, pkg84, pkg85-B, pkg85-C this project.

## When to use

When the owner says "implement pkg88" or "start on pkg43" or hands you a spec to land. NOT for: research-only sessions (use `/architect` instead), spec-filing without implementation (use `/file-followup`), or hardware-verification of an already-merged PR (use `/verify`).

## Step 0 — Worktree & pyd hygiene preamble (MANDATORY)

Before any code:

1. `cd <repo-root>` (or the active repo path the owner referenced — never silently switch worktrees per CLAUDE.md §Build & Verification).
2. `pwd && git rev-parse --show-toplevel` to confirm location.
3. Scan for shadow `.pyd` files that could mask fresh builds:
   ```powershell
   Get-ChildItem -Path . -Filter "astroray*.pyd" -Recurse -Force |
     Where-Object { $_.FullName -notmatch "(\\build_cuda\\|\\build_tcnn\\|\\\.claude\\worktrees\\)" } |
     ForEach-Object { $_.FullName }
   ```
   Should produce no output. If shadows exist, DELETE them before proceeding. See memory `stale_pyd_locations` for the failure mode.
4. Confirm main is current: `git fetch origin && git log -1 --oneline origin/main`.

## Step 1 — Read the spec

Read `.astroray_plan/packages/<pkg-name>*.md` end-to-end. Specifically capture:
- Frontmatter: `Track`, `Status`, `Depends on`, `Estimated effort`
- Goal section (before/after)
- Specification phases — your scope is the first non-done phase
- Acceptance criteria — write them down; each must trace to a measured number in the final PR body
- Non-goals — they bound what NOT to widen into
- Open design questions — STOP and ask the owner if any are blocking; do not silently pick

If the spec frontmatter says `Status: research signed off — not yet ready to implement` or similar, abort the skill and surface that the spec needs promotion or owner answers first.

## Step 2 — Create worktree

```powershell
git worktree add "<repo-root>\.claude\worktrees\<pkg-name>" -b <pkg-name> main
```

Then enter it:
```
EnterWorktree path="C:\\Users\\hgcom\\OneDrive\\Astroray\\Astroray_repo\\Astroray\\.claude\\worktrees\\<pkg-name>"
```

Verify with `pwd` + `git rev-parse --show-toplevel` per CLAUDE.md §Build & Verification. ABORT if either is wrong.

## Step 3 — Implement with tests

Standard implementation discipline:
- Follow the spec's "Files to create" + "Files to modify" lists literally; don't widen scope.
- Cite every non-trivial algorithm per CLAUDE.md §6 (paper + permissively-licensed reference).
- Match existing code style (CLAUDE.md §3 — surgical changes).
- For multi-week packages, the spec defines phases. Implement only the phase(s) you were dispatched for. Don't try to land all phases in one session.
- Write tests alongside implementation (per the spec's acceptance criteria). Don't defer tests "for later".

## Step 4 — Pre-push call-site sweep (CRITICAL — captures pkg63 / motion-vectors / OptiX-denoiser CI failure pattern)

Before opening a PR, audit for stale call sites of every signature you changed:

```powershell
# List every public function/class signature you changed
git diff origin/main --name-only -- '*.h' '*.hpp' '*.py' | ForEach-Object {
    git diff origin/main -- $_ | Select-String "^[-+].*\b(class|struct|def|void|int|float|auto)\b" | Out-Host
}
```

Then for each changed signature, Grep the entire repo to find call sites. Treat tests, mocks, stubs, and Python bindings as first-class call sites. If any call site uses the old signature, update it in the same commit as the signature change — NOT in a follow-up CI fix.

This is the cheapest 30-second check that has caught a recurring failure mode (per `/insights` analysis: 25+ buggy first-pass implementations across the project history).

## Step 5 — Run the full local test suite

```powershell
cmake --build build_cuda --config Release -j 8
pytest tests/ --ignore=tests/test_wavefront_parity.py -v --tb=short -x
```

The `--ignore=tests/test_wavefront_parity.py` is current (pkg55-B Phase B' is mid-flight); drop it once Phase B' lands. The `-x` halts at the first failure so you can fix it before continuing.

Address any failures BEFORE pushing. CI will run the same tests; a green local run usually means green CI.

Note: the chronic `test_disney_clearcoat_adds_gloss` flake (issue #276) and the ReSTIR `test_spatial_reduces_mse` flake (pkg79 territory) are known-flaky; don't block on them but DO note them in the PR body so reviewers know.

## Step 6 — Commit, push, open PR

```powershell
git add <files-changed>
git commit -m "feat(<pkg-name>): <one-line headline>"
git push -u origin <pkg-name>
gh pr create --base main --head <pkg-name> --title "feat(<pkg-name>): <headline>" --body "<body>"
```

PR body must include:
- Each acceptance criterion from the spec marked ✓ with measured number
- A "Verification" section listing the tests run + their results
- Citations of the references used per CLAUDE.md §6
- Any known flakes encountered (with a note that they're pre-existing per issue #N)

## Step 7 — Wait for CI, fix failures

```powershell
gh pr checks <pr-number> --watch
```

If CI fails:
1. Identify the failure (build error, test failure, lint error)
2. Re-run the call-site sweep from Step 4 — most CI fails are stale callers
3. Fix in a follow-up commit with message `fix(<pkg-name>): <what failed>`
4. Push; repeat until green.

## Step 8 — Resolve merge conflicts if any

If `gh pr view <pr-number>` shows "Behind" or there are merge conflicts:
1. Rebase against current main: `git fetch origin && git rebase origin/main`
2. **State the conflict resolution explicitly** before committing (per CLAUDE.md §PR & Git Workflow): "Conflict in `<file>` between my change (X) and the new main change (Y). Resolution: <one-line>."
3. Resolve, `git add -p` to confirm only the intended change is staged, `git rebase --continue`, `git push --force-with-lease`.

## Step 9 — Hand off for owner review

When CI is green:
1. Mark the PR ready for review.
2. Surface the PR number + headline numbers in your final response.
3. Do NOT auto-merge unless the owner explicitly authorized it. Implementation packages with C++/CUDA changes go through owner review.

## Out of scope for this skill

- Hardware-verification gates on RTX (use `/verify` afterward)
- Multi-package coordination (use `/dispatch-next` or `/close-round`)
- Spec-filing without code (use `/file-followup`)
- Cross-package architecture review (use `/architect`)

## Failure modes / when to STOP

- Spec has unresolved owner-preference questions → STOP, surface them, wait
- Acceptance criterion requires hardware you don't have (RTX) → STOP, hand off to `/verify` instead
- Implementation would require a non-trivial algorithm with no cited reference → STOP, file research note per CLAUDE.md §6, hand back
- A 5th+ ambiguity surfaces mid-implementation → STOP, surface it; CLAUDE.md §1 over silent decisions
