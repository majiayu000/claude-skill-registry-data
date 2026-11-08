---
name: git-workflow
description: Prepare branches, commits, pull requests, stacked-PR plans, authorized merges, release checklists, or safe worktree and simulator cleanup.
---

# Git and releases

Use this skill for commit or PR preparation, stacked-PR planning, an authorized merge, release preparation, or requested worktree cleanup. Follow repository templates and policies before these defaults. This skill defines conventions, not permission to commit, push, open or merge a PR, publish a release, or delete user state.

## Choose the procedure

- For an authorized PR, read [Opening a PR](references/opening-a-pr.md). For PR feedback or a request to watch CI, use [Resolve PR comments](../babysit-pr/SKILL.md); open a PR and monitor it for personal repos.
- For a large change or dependent PRs, read [Stacked PRs](references/stacked-pr.md). It owns the decision gates and native `gh stack` commands.
- For local screenshots or recordings that belong on a GitHub PR, read [Attaching media to a pull request](references/attaching-media.md). Upload only to the intended repository and PR.

## Branch & PR titles

- Use short, descriptive branch names such as `fix/issue-123` or `feat/session-cache`.
- Use `type(scope): subject` for PR titles and commit subjects. Choose `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf`; name the affected area in the scope. Write a short, imperative subject without a final period.
- Explain the problem and reason for the change before implementation details. Name concrete behavior, relevant symbols, compatibility changes, and material decisions.
- Use `Why`, `Scope`, `Tradeoffs`, `Blast Radius`, and `Verification` sections when useful, not as a required template. Omit empty sections and boilerplate.
- State relevant validation commands and results, plus material checks omitted and why. Reuse evidence under the [programming validation guidance](../programming/SKILL.md#testing--validation); preparing a commit or PR does not add a test gate.
- Include screenshots or videos for user-visible changes when they substantiate a claim or improve reviewability. Keep commit bodies focused on rationale that the subject and diff do not explain.

## Merges and releases

For authorized merges, follow the repository's merge policy. Do not infer squash, merge-commit, or rebase strategy from the target branch name. If no policy is available and the strategy affects history or a stacked change, ask before merging.

For release preparation, follow the repository's release checklist. Stop at the requested deliverable without inferring permission to publish or deploy.
