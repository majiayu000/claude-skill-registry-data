---
name: git-pushing-fast
description: Use when committing and pushing current changes on one branch with a Conventional Commit message. Supports diff-based type/scope/message generation, staged or requested change handling, segmented commit bodies for non-trivial changes, and safe single-branch push handling.
---

# Git Pushing Fast

## Overview

Commit and push the current repository's local changes on the current branch with a fast, safe single-branch workflow.

The default output is one focused Conventional Commit plus a push to the tracked remote branch. Analyze the actual diff, stage the requested change set, generate the commit message from the change content, and write a segmented body for non-trivial changes so reviewers can quickly see what changed by topic.

This workflow handles ordinary single-branch handoff requests such as saving current work to the remote, without branch merging, history rewriting, or PR creation.

## Conventional Commit Rules

Base format:

```text
<type>[optional scope]: <description>

[body: optional only for trivial changes; required and segmented for non-trivial changes]

[footer(s): required for breaking changes; optional for relevant issue references]
```

For this skill, the body is optional only for trivial commits. For non-trivial changes, write a segmented body and include a `Tests:` or localized equivalent section when tests, validators, hooks, or manual verification ran.

Types:

| Type | Use for |
| --- | --- |
| `feat` | New user-facing or product capability |
| `fix` | Bug fix |
| `docs` | Documentation-only change |
| `style` | Formatting/style change with no logic impact |
| `refactor` | Code restructure with no feature or bug fix |
| `perf` | Performance improvement |
| `test` | Test-only or test coverage change |
| `build` | Build system, dependency, or packaging change |
| `ci` | CI or automation config change |
| `chore` | Maintenance or miscellaneous change |
| `revert` | Revert a previous commit |

Breaking changes:
- Use `!` after the type or scope, such as `feat(api)!: remove legacy field`.
- Add a `BREAKING CHANGE:` footer when the behavioral contract changes.

Message style:
- Use the repository's existing commit language.
- Write the subject in present tense and imperative mood, such as `fix login redirect`.
- Keep the subject under 72 characters when practical.
- Reference issues in the body or footer when relevant, such as `Closes #123` or `Refs #456`.

## When to Use

Use this skill when the user asks to:
- Commit and push the current work
- Push this, save to remote, or finish a normal single-branch handoff
- Create one Conventional Commit from staged and unstaged changes
- Include a readable commit body that groups changes by feature area, UI area, tests, docs, or validation

## Do Not Use

Do not use this skill for:
- Multi-branch flows that merge a work branch into a primary branch
- Force-push, rebase, squash, amend, or history-rewrite requests
- Pull request creation unless the user explicitly asks for it after the push
- Code review, release notes, weekly reports, or changelog generation
- Destructive commands such as `git reset --hard` or `git checkout -- <file>`

## Instructions

Follow this workflow in order. Stop and report the blocker instead of guessing when the target repository, branch, or push destination is unclear.

1. Inspect the repository.
   - Run `git status --short`, `git branch --show-current`, and `git remote -v`.
   - Check the upstream with `git rev-parse --abbrev-ref --symbolic-full-name @{u}` when possible.
   - Review the staged diff with `git diff --cached --stat` and `git diff --cached`; if nothing is staged, review `git diff --stat` and `git diff`.
   - Use `git status --porcelain` when script-friendly status parsing is useful.
   - Never discard or revert user changes.

2. Stage changes.
   - If the user asked to commit everything, run `git add -A`.
   - If the user requested a narrower scope, stage only that scope.
   - Use file-specific adds, path patterns, or `git add -p` only when the requested scope requires logical grouping.
   - Re-run `git status --short` and verify the intended files are staged.
   - Never leave known secrets staged for commit, including `.env`, credential files, private keys, or tokens.

3. Build the commit message.
   - Use Conventional Commits: `type(scope): concise summary` in the repository's existing commit language.
   - Choose the type and scope from the actual diff, not from filenames alone.
   - For non-trivial changes, include a segmented body with 2-5 short sections.
   - Each section title should name the affected area, followed by bullet points.
   - Include a `Tests:` or localized equivalent section when tests, validators, hooks, or manual verification ran.

Example segmented body:

```text
fix(module): update component behavior

Behavior:
- Adjust the default state for the affected component.
- Keep existing behavior unchanged for unsupported input.

Implementation:
- Move repeated logic into a small helper.
- Update related configuration to use the new helper.

Tests:
- Add coverage for the updated behavior.
- Run the relevant validator before pushing.
```

4. Commit.
   - Use `git commit` with multiple `-m` arguments or an editor-free equivalent so the body is preserved.
   - Do not use `--no-verify`.
   - If hooks or validation fail, fix the failure and retry the commit.

5. Push.
   - If the current branch has an upstream, run `git push`.
   - If there is no upstream, run `git push -u origin <current_branch>` unless the repository or user specifies another remote.
   - If the push is rejected because the remote moved, run `git fetch` and inspect before retrying.
   - Do not force-push unless the user explicitly requested force-push and the risk has been confirmed.
   - Never force-push to `main` or `master`.

6. Report.
   - Keep the final response concise.
   - Include the commit hash, branch, remote push result, and validation that ran.
   - If the host app supports Git directives, emit them only after the matching action succeeds.

## Safety Protocol

- Never update global or system Git config.
- Never run destructive commands such as `git reset --hard` or `git checkout -- <file>` unless explicitly requested.
- Never skip hooks.
- Never commit secrets.
