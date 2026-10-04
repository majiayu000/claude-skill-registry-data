---
name: workflow-commit
description: Commit changes the way a sandboxed agent must — write Conventional Commit messages and, because commit signing fails inside the sandbox, hand the real commit off through a generated commit.sh script. Inside a git worktree, commit normally (unsigned) and emit a commit.sh that re-signs the range; in the main checkout, do not commit at all — emit a commit.sh containing the exact git add and git commit invocations for the user to run. Use when committing changes, creating a git commit, staging and committing work, writing or formatting a commit message, splitting changes into separate commits, or when an agent or sandbox cannot sign commits and must hand the commit off to the user. Not for pushing, opening or merging pull requests, rebasing or amending existing history, tagging releases, or non-git version control.
license: MIT
---

# Commit changes with a signing handoff

Sandboxed agents cannot reach the signing key (YubiKey, GPG agent, OS keychain), so a commit made
inside the sandbox either fails to sign or lands unsigned. This skill keeps history clean by **handing
the real commit off to the user through a `commit.sh` script** they run outside the sandbox. Which
path you take depends on whether you are in a git worktree.

## 1. Detect: worktree or main checkout

```sh
git rev-parse --is-inside-work-tree >/dev/null || exit 1   # bail if not in a repo
[ "$(git rev-parse --git-dir)" = "$(git rev-parse --git-common-dir)" ] && echo main || echo worktree
```

When `--git-dir` and `--git-common-dir` differ you are in a linked **worktree** (agents commonly run
on an `agent/<name>` branch); when they are equal you are in the **main checkout**. The two cases take
different paths in step 3.

## 2. Write Conventional Commit messages

Group the working-tree changes into one or more logical commits, each with a
[Conventional Commit](https://www.conventionalcommits.org/) subject:

```text
type(scope): summary
```

`type` is one of `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`, `style`.
Signal a breaking change with `!` after the type (`feat!:`) or a `BREAKING CHANGE:` footer. Keep one
cohesive concern per commit and the subject in the imperative mood.

## 3a. Inside a worktree — commit, then re-sign

Commit normally at sensible stopping points; these land **unsigned** on the worktree branch. Then
write a `commit.sh` at the worktree root whose only job is to **re-sign the range you authored this
session** using the user's signing setup:

- Pick `<base>` as the parent of your first commit this session — `HEAD~<n>` for a known count, or
  `$(git merge-base HEAD <parent-branch>)` when the count is dynamic.
- The script re-signs every commit in `<base>..HEAD`, for example by rebasing the range and amending
  each commit with the repository's configured signing command.

See [reference.md](reference.md) for a complete worktree `commit.sh`.

## 3b. Main checkout — do not commit, generate commit.sh

Do **not** run `git commit`. Instead write a `commit.sh` at the repo root containing the exact
`git add` and `git commit` invocations you would have run — one `git commit` per logical commit, with
the real messages and any trailers — for the user to run outside the sandbox where signing works.

See [reference.md](reference.md) for a complete main-checkout `commit.sh`.

## 4. The commit.sh contract (both paths)

Every `commit.sh` you write:

- starts with `#!/usr/bin/env sh` followed by `set -eu`;
- **overwrites** any prior `commit.sh` — the file is the current batch, not history;
- is created executable (`chmod +x commit.sh`) so the user runs it as `./commit.sh`;
- ends with `rm -- "$0"` so it deletes itself after a successful run. Under `set -eu` a failed
  `git commit` or re-sign aborts before the `rm`, leaving the script in place to fix and rerun.

Never add entries to the repository `.gitignore` while committing — ignore rules belong in the user's
global ignore file, not the repo. When the script is written, tell the user it is ready and that they
should run `./commit.sh` outside the sandbox.
