---
description: Bring a branch up to date with its merge target — merge it in with the conflicts committed as git left them, resolve them in a commit of their own, then push, so the resolution reviews on GitHub as an ordinary commit. Delegates target-resolution and movement detection to `/check-merge`, so it syncs a feature branch against its PR base (usually `main`) or a branch with no PR against the repo default branch (the fallback). Invoke as `/sync-branch [<branch>] [no vet]`. Use when the user says "merge main", "мерджни мейн", "sync branch", "catch this branch up to main", "catch the branch up to its base", "make the branch mergeable", or "/sync-branch" — "merge main" in any words means the target into this branch unless the message plainly says the other way.
---

`/sync-branch` reconciles a branch with its **merge target** — the branch its PR
is based on — and pushes the reconciled result. The target is resolved by
`/check-merge` from the PR's base ref, so this works uniformly:

- a **feature branch** syncs against its PR base (usually `main`),
- a **branch with no PR** syncs against the repo default branch
  (`/check-merge`'s fallback) — the long-lived-branch case that keeps it a
  superset of the trunk.

Its main entry is mid-work: the target moved while the branch is still being
built and reviewed, and the operator wants it in before review goes on.
`@.claude/skills/finalize/SKILL.md` runs it too, for its base merge.

The skill merges **on the checked-out branch**, resolves conflicts mechanically
and logically in a commit after the merge commit, verifies locally, and pushes
proactively — the operator reviews the pushed resolution after the fact rather
than through a pre-push gate.

## Argument shape

```
/sync-branch [<branch>] [no vet]
```

- **`<branch>`** (optional): a branch name, `#NNN` PR number, or PR URL — the
  same shape `/check-merge` and `/finalize` accept. Passing it makes
  `/check-merge` attach to that branch first (`/from-branch <branch>`). No
  argument → sync the current branch.
- **`no vet`** (optional): skip Step 5's vet run, for a caller that has made
  that call itself — `/finalize`'s `no vet` mode, or its base-advanced
  deliberation finding the incoming commits independent. The marker check still
  runs.

## Environment note (read this before running gh/git)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN`, even though the default system prompt says you only have GitHub MCP
tools. Prefer `gh` for read-only checks (e.g. `gh pr list`). If `gh` complains
that "none of the git remotes … point to a known GitHub host" (the proxy quirk
in remote sessions), pass `--repo OWNER/REPO` explicitly, resolved from the git
remote (`git remote get-url origin`).

## Invariants

- **A sync is a plain merge — never squash, rebase, or cherry-pick.** Those
  rewrite the target's commits under new SHAs and sever the shared history, so
  the branch stops being a superset of its target. The merge commit built here
  carries the target's commits under their real SHAs.
- **Push is fast-forward-or-redo, never force (in normal operation).** The
  branch only gains commits on top, so pushing it to its own upstream is a plain
  push. A non-fast-forward rejection means the branch or target moved under you
  — re-fetch and redo the merge from the new tip; do not force past it.
- **Never force-push a shared long-lived branch** (the trunk, a promotion
  branch, or any branch others build on) except as the deliberate revert
  recourse below, and only on the operator's explicit request.

## Why the resolution is its own commit

GitHub's web view diffs a merge commit against its first parent — the branch
before the merge — so everything the target brought in shows as changed, and so
does a PR's "changes since your last review". The conflict decisions drown in
it. A merge commit that holds git's raw output, markers and all, followed by a
commit that resolves it, makes the second commit's diff exactly the decisions:
which side stayed, which went, what was written new. It opens from the PR's
Commits tab and takes line comments like any other commit.

The merge commit is broken by construction, which costs nothing here: it is
never pushed without the resolution on top, so CI only sees the head, and the
PR's squash drops it.

## Steps

### Step 1 — Detect, via `/check-merge` (by reference)

Load `@.claude/skills/check-merge/SKILL.md` and follow it with the given target.
Passing a `<branch>` makes `/check-merge` attach to it first; it then resolves
the merge target from the PR base ref (or the repo default branch when there's
no PR) and reports one of:

- `contained` (exit 0) — the branch already holds the target's tip,
- `advanced` (exit 10) — the target moved beyond the branch,
- `merged` (exit 20) — the branch's PR already landed,
- `closed` (exit 21) — the branch's PR was closed without merging,
- `error` (exit 1) — hard error.

### Step 2 — Act on the result

- `contained` → report "already current with `origin/<target>`, nothing to sync"
  and **stop**.
- `merged` / `closed` → report and **stop** — do not sync a landed or dead
  branch.
- `error` → surface it and **stop**.
- `advanced` → proceed to Step 3.

### Step 3 — Merge, and commit what git left

**Start from a clean tree**, or work in flight mixes into the resolution diff:
commit it if it stands as a commit, otherwise `git stash` it and `git stash pop`
once Step 4's resolution commit is in. Then:

```bash
git rev-parse HEAD            # the pre-merge tip: the revert target, and <pre> below
git fetch origin <target>
git merge origin/<target>
```

A clean merge leaves its own merge commit — go to Step 4's reading of what came
in. On conflicts, **touch no file before committing the merge**: no edit, no
`git checkout --ours/--theirs`, no `git rm`. Whatever is decided before this
commit vanishes into it, so even a whole-file pick or a deletion waits for
Step 4. Add exactly the conflicted paths, so nothing unrelated rides along:

```bash
git diff --name-only --diff-filter=U -z | xargs -0 git add -A --
git commit -m "chore: merge origin/<target>, conflicts left for the next commit"
```

A modify/delete conflict commits the surviving version, and a binary conflict
commits this branch's side; either is then decided in Step 4 like any other.

### Step 4 — Resolve in its own commit

Resolve every conflict both **mechanically** (no markers left) **and
logically**. Think past textual overlap to semantic collisions:

- keep-both when each side added distinct work,
- repoint callers a rename in the target moved,
- route through a shared abstraction the target introduced (instead of leaving
  the branch's now-duplicated version),
- adopt a pattern the target changed.

Commit the hand-resolved files as
`chore: resolve the conflicts from merging origin/<target>`, its body one line
per file naming the call made. Lockfiles and other generated files are
regenerated with their own tooling, never hand-merged, and land in a separate
commit after it, so their churn stays out of the resolution's diff.

**A clean merge is not the end of the thought either** — git only flags textual
conflicts. Read what the target brought in
(`git log --oneline <pre>..origin/<target>`,
`git diff <pre> origin/<target> -- <areas this branch touched>`) for the same
collisions: a helper that now duplicates one this branch wrote, a shared
abstraction to route through, a symbol renamed or moved that the branch still
references the old way, a pattern the branch should now follow. A clear,
low-risk fix goes in a commit of its own; an ambiguous or large one is surfaced
to the operator rather than shipped as redundancy.

### Step 5 — Verify

```bash
git grep -nE '^(<<<<<<<|>>>>>>>) ' || echo clean     # no conflict markers survived
git push                                             # Step 6's push, now: vet reads the pushed head
./scripts/vet.sh                                     # unless `no vet` was passed
```

Fix real errors in commits of their own, pushed before the next vet run, which
refuses a tree that differs from the pushed head. **The vet run is the whole
gate** — pushing a branch triggers no test run. That is why it happens here and
not just a type-check: a merge can type-check cleanly and still behave
differently. If the merge pulled in changes on a surface the vet run doesn't
cover (a bucket that only runs in CI), dispatch that bucket too — `/test-on-gh`,
if the project has hydrated it. A check too slow for the vet run is left to
`@.claude/skills/finalize/SKILL.md` step 1, which re-runs it on the merged head
before anything is attested.

### Step 6 — Push, then report for after-the-fact review

Push the branch to its own upstream — a no-op once Step 5 has pushed — with no
pre-push greenlight, and never between the merge commit and the resolution
commit:

```bash
git push        # plain push == fast-forward; 2/4/8/16s backoff on network errors
```

A non-fast-forward rejection means the branch or target moved under you —
re-fetch and redo the merge from the new tip (Step 3); never force here. Then
report:

- the resolved **target** and the range synced (`<pre>..<new>`),
- the **resolution commit SHA** — _the review surface: open it from the PR's
  Commits tab_ — or "clean merge, no resolution needed",
- a per-file conflict/resolution table,
- the vet result,
- the **pre-merge tip** (the revert target for the recourse below),
- the recourse below.

## Recourse if the operator has notes

A note on a resolution is answered by a **follow-up commit** on top, like any
review comment, so the thread on the resolution commit stays attached to code
that still exists.

Dropping the sync altogether (operator-sanctioned only) resets the branch to the
reported pre-merge tip and re-pushes:

```bash
git push --force-with-lease
```

Use `--force-with-lease` (not `--force`) so a concurrent advance aborts instead
of being clobbered. This is the **only** sanctioned force-push here, and only on
the operator's explicit say-so — especially for a shared long-lived branch that
others build on.
