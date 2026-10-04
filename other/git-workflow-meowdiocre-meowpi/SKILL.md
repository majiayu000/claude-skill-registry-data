---
name: git-workflow
description: Handle Git commits, branches, merges, rebases, conflicts, pull requests, tags, and releases with inspect-first, non-destructive workflows. Use when a task changes repository history or asks for a Git or pull-request operation.
---

# Git workflow

Use Git as a record of intentional, verified changes. Repository instructions and the user's requested branching or release model take precedence.

## Start from evidence

Before changing repository state, inspect:

```sh
git status --short --branch
git diff
git diff --cached
git log --oneline --decorate -10
git remote -v
```

Identify the current branch, its upstream, the intended base branch, staged and unstaged changes, and untracked files. Preserve changes that are not part of the task. Do not assume a dirty tree is disposable.

## Choose the relevant workflow

- For staging, atomic commits, messages, amends, reverts, and history safety, read [commits and history](references/commits-and-history.md).
- For branches, merges, rebases, stashes, cleanup, and conflicts, read [branches and conflicts](references/branches-and-conflicts.md).
- For pull requests, tags, semantic versions, changelogs, and releases, read [pull requests and releases](references/prs-and-releases.md).
- When composing a commit message, load `caveman-commit` and let repository-native conventions win.

## Core workflow

1. Confirm what belongs in the change and what must remain untouched.
2. Follow the repository's branch policy. Create or switch branches only when required by the task or local rules.
3. Stage deliberately, preferably by explicit path or patch. Review the staged diff before committing.
4. Run the evidence required by the change. Do not encode known failures into history without reporting them.
5. Compose a message from the staged behavior and its reason, then commit only when the request includes committing.
6. Re-check status and the created commit. Confirm unrelated changes remain intact.
7. Push, open or update a pull request, tag, publish, or release only when the task includes that external action.

## Safety boundaries

- Treat `reset --hard`, `clean`, force-push, branch deletion, tag replacement, and public-history rebases as destructive. Do not use them without clear authorization and exact targets.
- Prefer `git restore`, `git revert`, a new corrective commit, or a backup branch when they preserve recoverability.
- Never combine unrelated working-tree changes merely to obtain a clean status.
- Never bypass hooks, required checks, signatures, or protected-branch rules unless the user explicitly requests it and the repository permits it.
- Use `--force-with-lease` rather than `--force` only when an authorized history rewrite is genuinely necessary.

Finish with the resulting branch or commit, the verification run, any remaining working-tree changes, and whether anything was pushed or published.

## Loading in Oh My Pi

Relative paths in this skill (`references/…`, `scripts/…`) resolve against the skill's own directory. Read them with `skill://git-workflow/<relative-path>`. When a shell command needs a real filesystem path, that directory is `<OMP_HOME>/skills/git-workflow/` — `~/.omp/agent/skills/git-workflow/` by default. Invoking `/skill:git-workflow` also prints the resolved location.
