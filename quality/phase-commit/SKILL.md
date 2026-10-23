---
name: phase-commit
description: Create one local commit for a completed, validated, and reviewed unit of work. Use only when the user explicitly requests a commit without pushing or other delivery actions.
---

# Phase Commit

Create one isolated local commit without changing history or external state.

## Workflow

1. Confirm required repository checks and applicable validation and review cover the exact intended content.
2. Inspect status, staged and unstaged changes, and relevant untracked files; preserve all unrelated user work.
3. Stop when scope is ambiguous or includes sensitive, unexpectedly generated, or otherwise unsafe paths.
4. Stage only explicit paths with `git add -- <paths>`; never use broad staging commands or globs.
5. Review the staged path list and diff against the requested unit. If the unit mixes a behavior-preserving restructuring with a behavior change, say so and offer two commits; commit them together only if the user keeps one.
6. Draft the commit subject and body using repository conventions. Without a convention, write a short imperative subject and a body that states the problem, the change, and why. Then use `text-improve` without changing technical meaning.
7. Commit without bypassing hooks or changing signing policy.
8. Verify the created commit with `git show --stat HEAD` and the remaining worktree with `git status --short`.

Do not amend, rewrite history, push, create branches or pull requests, manage CI, tag, release, or include unrelated changes.

When a hook only reformats the staged paths, review its changes, stage those same paths, and commit once more. On any other hook or commit failure, stop and report the blocker without claiming completion.

Finish only after verifying the created commit, then report its hash and concise summary.
