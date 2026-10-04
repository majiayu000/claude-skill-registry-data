---
name: pr-breakdown
description: Split a large, multi-concern branch or PR into several focused, independently reviewable PRs. Use this whenever a working tree or branch mixes more than one logical change (a model/schema rework tangled with frontend work, plugin updates, and an unrelated bugfix), when the user says things like "split this PR", "break this branch into smaller PRs", "this diff is too big to review", or when you're about to open one PR covering clearly unrelated concerns. Also covers auditing existing open PRs before splitting, so the split minimizes PR churn — force-pushing a rewrite into an existing PR the same author already opened for that slice of work, rather than closing it and opening a new one, and skipping a slice entirely if another open PR already covers it.
---

# PR breakdown

A branch that grew organically often ends up mixing several concerns: a data-model
change, the call sites that consume it, a UI layer, incidental tooling updates, and a
stray unrelated fix. Reviewing all of that as one PR forces every reviewer to context-switch
between domains and makes it hard to revert one slice without reverting all of them. This
skill walks through splitting that branch into PRs that each read as one coherent change.

The goal is not "more PRs" — it's each PR being reviewable on its own terms, by the person
who actually owns that domain, without waiting on or being blocked by the others.

## Step 1: categorize the changes

Read every changed/added/removed file and group them by **what would break if this slice
shipped alone**. A useful sorting test: for each file, ask "does removing this file change
whether the core feature compiles or works?" Files that answer "yes" together form one
atomic slice; files that answer "no" are either their own slice or don't need to move at all.

Common categories, roughly in dependency order:

1. **Model / schema / retiring an old shape.** A new data model, its migration, and the
   deletion of whatever it replaces belong in one PR. Retiring an old shape and introducing
   its replacement must land atomically — if you split them, there's a commit in between
   where `main` references a shape that no longer exists (or vice versa).
2. **Wiring that depended on the old shape.** Call sites that already consumed the shape
   being retired have to move with slice 1, for the same atomicity reason — you can't retire
   a model while a caller still expects its old fields. Wiring that's genuinely new and
   doesn't touch the retired shape can be its own slice, but check this carefully; it's easy
   to assume something is independent when it's actually load-bearing on slice 1.
3. **Frontend / UI.** Keep UI separate from backend even when it depends on the backend
   slice — UI review needs a different reviewer and a different lens (visual correctness,
   wording, interaction) than model or schema review, and gating one on the other slows both
   down. If the UI slice depends on new backend shapes, base its branch on the backend PR's
   branch (see Step 4) rather than on `main`.
4. **Unrelated infrastructure / tooling.** Internal scripts, skill docs, CI config, or an
   incidental new endpoint that doesn't touch the feature's core files. Use the same removal
   test: if deleting it doesn't change whether the main feature works, it doesn't belong
   bundled with the feature.
5. **Standalone bugfixes.** A fix with no dependency on the rest of the branch. Before
   opening this as its own PR, do the open-PR audit in Step 2 — a fix this small is exactly
   the kind of thing that may already be sitting in another open PR.

Not every branch has all five categories, and the boundaries between 1/2/3 can shift
depending on how tightly the feature's layers are coupled. Treat this as a starting
taxonomy, not a checklist to force-fit.

**Worked example** *(from a real `groot` split)*: a branch reworking a batch-scoped
`BatchLesson` model into a top-level polymorphic `Lesson` model had 39 uncommitted files.
Category 1 was the new `Lesson` model, its migration, and deletion of the old
`BatchLesson` model/fixture/test. Category 2 was every call site that already read
`BatchLesson` (a batch model, a work-unit model, a retrospecting phase, two serializers) —
these had to move with category 1, since leaving them behind would mean `main` referencing
a deleted model. Category 3 was a Runs-page React panel rendering the new lesson data —
it depended on the new model's shape but was kept as its own PR, rebased onto the model
PR's branch. Category 4 was a Kubernetes-log-fetching endpoint plus unrelated internal
plugin/CLI scripts — verified independent by confirming none of those files referenced the
`Lesson` model at all. Category 5 was a one-line diff-parsing fix that, per Step 2's audit,
turned out to already be covered (plus more) by an existing open PR — so no fifth PR was
opened.

## Step 2: audit existing open PRs before opening anything new

Before creating a single new PR, check what's already open. Two situations to look for:

- **An existing open PR already covers one of your slices**, either because the same
  author started it earlier and this branch supersedes it, or because someone else already
  landed the same fix. List open PRs (`gh pr list`) and skim ones that look topically close
  to each slice; read their diffs (`gh pr diff <n>`), not just their titles.
- **An existing PR is an earlier, incomplete iteration of a slice you're about to open.**
  If it's authored by the same person as the branch being split, prefer rewriting that PR's
  branch in place over opening a new PR and closing the old one — this keeps the PR number,
  review comments, and CI history attached to the final version, and avoids inflating the
  open-PR count with a close/reopen pair that says nothing useful in the log. Only open a
  brand-new PR when no open PR covers that slice at all.

If a slice turns out to be a strict subset of what an existing open PR already contains
(same fix, or the same fix plus more), drop that slice entirely rather than opening a
duplicate. Confirm this with a real diff comparison, not a guess from the PR title — file
names or one-line summaries can look unrelated while the actual patches overlap, or look
similar while actually solving different problems.

## Step 3: build each slice without disturbing the others

The branch being split usually has all the changes sitting uncommitted, or committed
together, in one working tree. Splitting it without corrupting any one slice mid-edit is
easier with `git worktree` than by juggling branches in a single working directory:

1. Snapshot the current state into a scratch commit on a throwaway branch, so nothing is
   lost while you work:
   ```bash
   git checkout -b tmp/split-source
   git add -A && git commit --no-verify -m "wip: snapshot before splitting into PRs"
   ```
2. For each target PR, create an isolated worktree off the right base (usually `main`, or
   another slice's branch — see Step 4 for that case):
   ```bash
   git worktree add /path/to/worktree -b <slice-branch-name> <base-ref>
   ```
3. Pull only that slice's files into the worktree:
   ```bash
   git -C /path/to/worktree checkout tmp/split-source -- <path1> <path2> ...
   ```
4. Verify the slice builds/tests on its own — the narrowest check you can actually run
   locally (typecheck plus unit tests for the touched files, at minimum). If a fuller check
   (full test suite, linter) can't run locally, don't skip it silently — note in the PR body
   that it's deferred to CI, and say why (e.g., an environment-specific dependency that
   isn't available locally).
5. Commit and push. Remove the worktree once its branch is pushed and no longer needed
   locally (`git worktree remove --force /path/to/worktree`); the branch ref itself survives
   independently of the worktree.

The original branch is never touched by this process — it's fine to leave it exactly as it
was until every slice is confirmed pushed, in case you need to re-cut a slice.

## Step 4: rewrite existing PRs safely when reusing their branch

When Step 2 says to reuse an existing PR's branch instead of opening a new one, force-push
the new content over its current tip rather than closing and reopening:

1. Fetch the branch's actual current remote tip immediately before pushing — not a tip you
   fetched earlier in the session. If the PR has been open for a while, or if any
   automation (a bot, a background agent) might also be pushing to it, assume the remote has
   moved since you last looked.
   ```bash
   git fetch origin <branch-name>
   ```
2. If the fetched tip has commits you didn't expect, read their diffs before overwriting.
   Confirm each one is either fully superseded by your rewrite or doesn't carry anything
   unique — don't force-push over a commit you haven't looked at.
3. Force-push anchored to that confirmed tip, not a bare `--force`:
   ```bash
   git push --force-with-lease=<branch-name>:<confirmed-remote-sha> <slice-branch-name>:<branch-name>
   ```
   `--force-with-lease` fails loudly if the remote moved again between your fetch and your
   push, instead of silently discarding someone else's work.
4. Update the PR's title and body to describe its new scope. A PR that's been rewritten to
   cover a narrower or different slice than its original description will confuse reviewers
   who read the description before the diff — don't leave stale framing in place.

For a PR that depends on another slice (e.g. a UI PR built on a model PR that hasn't merged
yet), base its branch on the *other slice's branch*, not on `main` — otherwise its diff
includes the other slice's changes too, defeating the point of separating them. Once the
base PR merges, GitHub will typically retarget the dependent PR's base to `main`
automatically; if not, retarget it manually with `gh pr edit <n> --base main`.

## Step 5: write each PR's description around its actual final scope

Each PR should read as a self-contained change:

- **Summary**: what changed and why, scoped to just this slice.
- **Scope note**: if this slice depends on or was split from another PR, say so explicitly
  and link it — reviewers need to know a "missing" piece is intentionally elsewhere, not
  forgotten.
- **Test plan**: what you actually ran, and — just as important — what you *couldn't* run
  locally and why, if anything was deferred to CI. Don't write a test-plan checklist that
  implies a local run happened when it didn't.

If `gh pr edit`/`gh pr create` reject a multi-line `--body` string, write the body to a
scratch file first and pass `--body-file <path>` instead of fighting with heredoc escaping.
