---
name: branch-strategy
description: Git workflow for this project — branch naming and lifecycle, commit message conventions, what belongs in one commit, PR flow and review, merge vs rebase, keeping a branch current, tagging and releases, and handling binary/asset files. Use before starting a branch, before committing or pushing, when preparing a PR, or when resolving a conflict or a messy history.
---

# Branch strategy

How work moves from an idea to `main` in this repo.

## Project specifics

- **Default branch:** `main`
- **CI on PR:** build, typecheck, lint, unit + determinism tests, bundle-size budget.
- **Versioning:** `v0.x` until the game is playable end to end.
- **Assets:** decide Git LFS before the first large binary lands (see below).

## Push after every increment — the working tree is not storage

This container's filesystem has rolled back twice now, discarding hours of work
that existed only locally. The second time, the tree reverted three commits
while the branch on the remote was intact, so recovery was:

    git stash push -u              # save uncommitted work in progress
    git fetch origin <branch>
    git reset --hard origin/<branch>
    git stash pop

That worked only because everything finished had already been pushed. Commit and
push at every point the work is coherent, not when a feature feels done — a
push is the only durable record, and the cost of one extra commit is nothing
against the cost of redoing an afternoon.

## Branch model

Trunk-based: `main` is always releasable, and everything else is a short-lived branch
off it. Long-lived parallel branches are what produce the painful merges; the defence
is branches measured in days, not weeks.

**Naming:** `<type>/<short-kebab-description>`

| Type        | For                                                 |
| ----------- | --------------------------------------------------- |
| `feat/`     | new gameplay, systems, content                      |
| `fix/`      | bug fixes                                           |
| `perf/`     | performance work with a measured before/after       |
| `refactor/` | no behaviour change                                 |
| `chore/`    | tooling, deps, CI, build                            |
| `docs/`     | documentation only                                  |
| `spike/`    | throwaway exploration — never merged, deleted after |

Examples: `feat/drift-physics`, `fix/tunnelling-at-max-speed`, `perf/collision-broadphase`.

**Lifecycle:** branch from current `main` → commit in small steps → keep current with
`main` → PR → review → merge → delete the branch. If a branch is still open after a
few days, it is too big: split it or land the safe part behind a flag.

## Commits

One commit = one coherent change that leaves the game in a working state. If you
can't describe it in one line without "and", it's two commits.

**Format** — Conventional Commits, matching the branch types above:

```
<type>(<optional scope>): <imperative summary, <=72 chars>

Why this change exists and what approach it takes. Not a restatement of the
diff — the diff is right there. Note anything a reviewer would otherwise have
to ask about: rejected alternatives, measured numbers, follow-ups deliberately
left out.
```

- Imperative mood: "add coyote time", not "added" or "adds".
- `perf:` commits state the measurement: "17.2ms → 4.1ms tick time, 400-entity scene".
- Behaviour-changing commits reference the test that covers them.
- Never commit commented-out code, debug logging, or a `.orig`/`.rej` file.

## Keeping a branch current

Rebase your own unshared branch onto `main` to keep history linear:
`git fetch origin main && git rebase origin/main`.

Once a branch is pushed and someone else may have it — or once a PR has review
comments anchored to commits — **merge `main` in instead of rebasing**. Rewriting
shared history invalidates other people's checkouts and detaches review threads.
Never force-push a branch you don't exclusively own.

## Merging to main

Squash-merge by default: one branch becomes one commit on `main`, and the PR title
and description become that commit message — so write them as a commit message, not
as a note to the reviewer. Keep the individual commits (a true merge) only when the
branch is a genuine sequence of independently meaningful, independently revertable
steps.

A branch may merge only when: CI is green on the current head, review is approved,
it has no conflicts with `main`, and its tests actually cover the change.

## Pull requests

Small. A PR a reviewer can hold in their head gets a real review; a 2000-line one
gets an approval. If a change must be large (an engine bump, a mechanical rename),
say so up front in the description and isolate the mechanical part in its own commit.

Description covers: what changed, why, how it was verified (the actual test/run
result), and anything deliberately out of scope. Gameplay and visual changes include
a clip or screenshot — feel is not conveyable in a diff.

Do not open a PR unless it has been asked for.

## Conflicts

Resolve by understanding both sides, never by taking one wholesale. Specifically:

- **Lockfiles and generated files:** never hand-merge. Take either side, then
  regenerate with the project's own tooling and commit the result.
- **Tunables/data files:** conflicts here usually mean two people tuned the same
  value. That is a design question, not a merge question — ask, don't pick.
- **Binary assets:** they don't merge. Whoever lands second re-exports from source.
  See the asset note below.
- After any non-trivial resolution, run the suite before pushing. A resolution that
  compiles is not a resolution that works.

## Assets and binaries

Game repos accumulate binaries fast, and git handles them badly — every revision of
every asset lives in history forever. Decide the storage approach (Git LFS or an
external asset pipeline) before the first large asset lands, not after; retrofitting
means rewriting history. Keep source files (`.blend`, `.aseprite`, project files)
distinguishable from exported runtime assets, and never commit build output.

## Tags and releases

Releases are annotated tags on `main`: `v<major>.<minor>.<patch>`. Pre-1.0, minor is
for features and patch for fixes. A tag marks a commit that was actually built and
played, not merely one that compiled.

## Never

- Commit or push without being asked to.
- Push directly to `main`.
- Force-push a shared branch, or rewrite anyone else's history.
- Commit secrets, keys, or local config. If one lands, rotate it — removing the
  commit is not enough.
- Merge red CI, or disable a test to get green.
- Land a "temporary" fix without an issue tracking its removal.
