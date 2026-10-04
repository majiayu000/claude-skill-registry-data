---
name: thalarch-git
description: >
  Safe Git and GitHub delivery workflow for any repository. Use when the user asks
  to branch, commit, push, prepare/open a pull request, update an existing PR, or
  otherwise publish code changes. Preserves unrelated work, verifies the exact diff,
  keeps commits intentional, and never merges/releases/force-pushes unless explicitly
  authorized.
---

# Thalarch Git

Git operations are part of the deliverable, not cleanup after the fact.

## Preflight

Before mutation:

1. inspect current branch and upstream;
2. inspect `git status` and the full intended diff;
3. preserve unrelated dirty work;
4. discover repository contribution/branch conventions;
5. establish the exact external actions authorized by the user.

Never stage the whole worktree when unrelated changes are present.

## Branching

Prefer a focused branch when starting from the default branch unless the user has
explicitly requested a direct update.

Do not rewrite shared history or force-push without explicit authorization.

## Commit quality

A commit should represent one coherent change and contain only intended files.

Before committing:

- run the relevant verification gate;
- inspect staged diff;
- confirm no generated secrets, local paths, caches, or unrelated files are staged.

Use a concise professional message that describes the change, not the process.

## Push / Pull request

Push only when authorized.

For a PR, report:

- what changed;
- why;
- user/developer impact;
- verification evidence;
- residual risk or UNVERIFIED items.

Do not merge, publish a release, deploy, or enable auto-merge unless the user asked
for that specific class of action.

## Final verification

After publishing, independently verify the remote branch/PR points at the expected
commit and that the intended files are present.
