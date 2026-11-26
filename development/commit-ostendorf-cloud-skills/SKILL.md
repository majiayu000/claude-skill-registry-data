---
name: commit
description: "Turns the current working tree into one or more atomic Conventional Commits, split by intent, without asking for confirmation first. Use when changes are ready to commit, or the working tree holds several unrelated changes that need splitting."
---

# Commit

Turn the working tree into atomic, well described commits.

## When to use

- Work is finished, or at a reviewable intermediate state.
- The working tree holds several unrelated changes.

## Steps

1. Read the state: current branch, `git status`, `git diff` and `git diff --cached`. Never
   commit blind.
2. If the current branch is the default branch, create a feature branch first. A commit never
   lands on the default branch directly.
3. Group the changes by intent. Formatting, refactoring and a behaviour change are separate
   commits. Stage per group with `git add -p` or per path. Split a file at the hunk level when
   one file mixes concerns.
4. Order the commits by dependency, so each one still builds on its own where that is possible.
5. Check the diff for what must never land: a secret, a credential, a state file, debug output,
   commented out code, unrelated formatting, a generated file.
6. Write the message: `type(scope): subject`, imperative, lowercase, no trailing period, a body
   only when the why is not obvious, `Refs #123` in an issue context, `Closes #123` when this
   commit alone resolves it. No attribution or co-author line for an assistant.
7. Commit. Never pass `--no-verify`. A hook that blocks a commit names a real problem, fix it.
8. Report what was committed, one line per commit, and what is left unstaged and why.

## Guardrails

- No confirmation is needed before committing. Splitting and ordering are this skill's job.
- Never commit on the default branch. Branch first.
- Never commit a secret, a state file or a credential shaped value. Scan the staged diff for one.
- Never commit, amend or rebase with `GIT_CONFIG_GLOBAL=/dev/null` set unless the same command
  sets `GIT_COMMITTER_EMAIL`, and `GIT_AUTHOR_EMAIL` for a new commit. The switch is for test
  runs. See `git-conventions`.
- Signing stays whatever the repository already has configured. Never disable it.
- An unfixed security vulnerability in a public repository gets no exploit detail in a commit
  message: see the baseline's security vulnerability rule.

## References

- `git-conventions` for the full commit and branch convention.
- `secrets-handling` for what a staged diff must never carry.
