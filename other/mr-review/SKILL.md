---
name: mr-review
description: Stack-aware quality/security review of a peer's MR/PR or branch — resolves the input to a diff and reviews it without ever touching your working tree.
argument-hint: "<branch | mr-url | pr-url | iid>"
allowed-tools: Read, Write, Bash(gh pr view:*), Bash(gh pr diff:*), Bash(glab mr view:*), Bash(glab mr diff:*), Bash(git fetch:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git ls-remote:*), Bash(git remote:*), Bash(mkdir:*), Bash(find .:*), Bash(grep:*), Bash(command -v:*), Bash(cat .specwork/_review/*)
---

# Peer Review

Review someone else's work — a whole branch or a merge/pull request — and produce
a compact, prioritized report. Unlike `/sdd:code-review`, which reviews *your own*
uncommitted working tree, `/sdd:mr-review` reviews **committed** changes that belong
to someone else, resolved from a branch name or an MR/PR link.

---

## Core Rule

**Never mutate the repo.** No checkout, no branch switch, no `reset`, no fetch of
your own work, no commit, no push, no comment posted to the MR/PR. This skill only
*reads* a diff and *writes* a local report. The user's current branch and working
tree must be exactly as they were when the skill started.

---

## Use Cases

```bash
/sdd:mr-review feature/PROJ-15518                                  # a peer's branch
/sdd:mr-review https://gitlab.com/grp/proj/-/merge_requests/123     # a GitLab MR link
/sdd:mr-review https://github.com/owner/repo/pull/123              # a GitHub PR link
/sdd:mr-review 123                                                  # bare IID (provider auto-detected from the remote)
```

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Classify the argument: GitHub PR / GitLab MR / bare IID / branch name |
| 2 | Resolve it to a unified diff (via `gh`/`glab` for PRs/MRs, `git diff` for branches) |
| 3 | Abort if the diff is empty |
| 4 | Hand the diff to the shared review engine (see *Delegation*) |
| 5 | Write the report outside the reviewed repo's history and print it |

---

## Step 1 — Classify the Argument

Exactly one argument is required. If none is given, abort with usage:

```
Usage: /sdd:mr-review <branch | mr-url | pr-url | iid>

  /sdd:mr-review feature/PROJ-15518
  /sdd:mr-review https://gitlab.com/grp/proj/-/merge_requests/123
  /sdd:mr-review https://github.com/owner/repo/pull/123
  /sdd:mr-review 123
```

Classify:

- Contains `/-/merge_requests/` → **GitLab MR** (use `glab`)
- Contains `/pull/` (a `github.com` URL) → **GitHub PR** (use `gh`)
- Matches `^!?#?[0-9]+$` → **bare IID** — detect the provider from the origin
  remote: `git remote get-url origin`; `github.com` → `gh`, else → `glab`.
- Anything else → **branch name**

---

## Step 2 — Resolve to a Diff

### GitHub PR (link or IID)

`gh` is required. If it is missing or unauthenticated, abort and tell the user to
run `gh auth login` (or pass the branch name instead).

```bash
command -v gh >/dev/null || { echo "gh not installed — pass a branch name instead, or install gh."; exit 1; }
gh pr diff "<PR-or-URL>" > /tmp/mr-review.diff
```

Label the report from `gh pr view "<PR-or-URL>" --json number,title,headRefName,baseRefName`.

### GitLab MR (link or IID)

`glab` is required (else abort with `glab auth login` guidance).

```bash
command -v glab >/dev/null || { echo "glab not installed — pass a branch name instead, or install glab."; exit 1; }
glab mr diff "<IID-or-URL>" --color never > /tmp/mr-review.diff
```

Label the report from `glab mr view "<IID-or-URL>" -F json` (`iid`,
`source_branch`, `target_branch`, `title`, `web_url`).

Both `gh pr diff` and `glab mr diff` return the merge-base diff — the same set of
changes a reviewer sees in the PR/MR. If the PR/MR diff fails (private fork,
deleted source branch), fall back to branch mode against the source/target
branches from the JSON.

### Branch name

```bash
git fetch origin "<BRANCH>" --quiet
```

Pick the comparison base. Default to `main`. Confirm the base ref resolves on the remote
(`git ls-remote --exit-code --heads origin <base>`); if it does not, try the
other common default (`main`↔`development`) before aborting.

```bash
git fetch origin "<BASE>" --quiet
git diff "origin/<BASE>...origin/<BRANCH>" > /tmp/mr-review.diff
```

The **three-dot** range (`A...B`) diffs from the merge-base — the same set of
changes a reviewer sees in the MR/PR, not the noise of unrelated commits that
landed on the base meanwhile.

### Empty diff

If the resolved diff has no content, abort:

```
Nothing to review — the diff between <base> and <branch/MR/PR> is empty.
```

---

## Step 3 — Delegation to the Review Engine

`/sdd:mr-review` does **not** re-implement review logic. It reuses every rule from
`code-review`'s SKILL.md, applied to the resolved diff instead of the working
tree:

- **Stack routing** — Java (`sdd:java:quality-reviewer` + `sdd:java:security-reviewer`)
  vs frontend (`sdd:ui:quality-reviewer` + `sdd:ui:a11y-reviewer`), chosen from the files
  in the diff. If a required reviewer agent is missing, stop and tell the user
  to install/enable the sdd plugin (`/plugin install sdd@gatsby`) — the
  reviewers ship with it.
- **Test Coverage Check** — same stack-specific gap detection, advisory only.
- **Reviewers in parallel** — each gets only the diff, a short context note, and
  evidence-based instructions; no code outside the diff.
- **Merge / dedupe / IDs**, then **Pack Hints** (`/sdd:jpa-patterns`,
  `/sdd:concurrency-review`, `/sdd:api-contract-review`, `/sdd:logging-patterns`) appended as
  advisory `## Suggested Follow-ups`.
- **Report Format** — identical sections (Verdict, Summary, Test Coverage,
  Security Findings, Quality Findings, Action Plan, Questions, Suggested
  Follow-ups).

Detect the stack from the **file paths and extensions in the diff** (there is no
working tree to scan): `*.java` + `build.gradle`/`pom.xml` → Java; `*.ts`/`*.tsx`
+ `package.json` → frontend.

---

## Step 4 — Write the Report

Peer reviews must not pollute the reviewed repo's history. Choose the output path
in this order:

1. If `.specwork/_review/` exists in the current repo → write there as
   `<slug>-peer-review.md` (it is already gitignored by the pipeline).
2. Otherwise → write to `~/.claude/peer-reviews/<slug>-<date>.md` and tell the
   user the absolute path.

`<slug>` = the MR/PR IID (PR/MR mode) or a sanitized branch name (branch mode).

Then print the full report to stdout. This is a read-only review: **do not** offer
to apply fixes, and never post the report as an MR/PR comment.

---

## Rules

- Read-only: never checkout, switch, reset, commit, push, or comment on the MR/PR.
- Leave the user's branch and working tree untouched on every exit path.
- Review only the resolved diff — no code outside it.
- One required argument; fail cleanly with usage when it is missing.
- PR/MR mode needs an authenticated `gh`/`glab`; degrade to branch mode when possible.
- Keep findings specific, severity-ranked, and minimal (inherits code-review).

---

## Requirements

- For GitHub PR mode: `gh` installed and authenticated (`gh auth status`).
- For GitLab MR mode: `glab` installed and authenticated (`glab auth status`).
- For branch mode: the branch must exist on `origin` (only `git` needed).
- Reviewer agents installed for the detected stack.

---

## Related Skills

- `code-review` — reviews your *own* working-tree diff (this skill borrows its engine)
- `mr-address` — for the author, to handle review comments after an MR opens
- `jpa-patterns` / `concurrency-review` / `api-contract-review` / `logging-patterns` — opt-in deep packs the report may suggest
