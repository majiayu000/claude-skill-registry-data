---
name: git-conventions
description: "Use when the user asks to commit, stage, branch, diff, write a commit message, or perform any git operation, and when the user asks to describe or summarise a change for review, such as a merge request or pull request description (MR, PR). Also use when discussing version control workflows or git safety."
---
# Git Conventions

## When to use
- User asks to commit, stage, diff, or perform any git operation
- User asks to create a branch or write a commit message
- User asks to check differences with a previous version
- User asks to describe or summarise a change for review (merge request, pull request)
- User mentions "git", "commit", "branch", "diff", "MR", "PR", or "version control"
- A task is green and ready to commit, in any context, headless included

## Overview

Rules for safe and consistent git usage, from the commit to the change description.

Reviewing code or answering review feedback is the
[`code-review`](../code-review/SKILL.md) skill. Forge commands live in its
[gitlab.md](../code-review/gitlab.md) (`glab`) and [github.md](../code-review/github.md)
(`gh`) reference files.

## Forge routing

Pick the forge CLI (`gh` or `glab`) in this order. Never guess.

1. An explicit argument or user statement wins. A project path or URL names the forge.
2. Otherwise read `git remote get-url origin`. Host `github.com` routes to `gh`;
   host containing `gitlab` routes to `glab`.
3. Unknown host: check `gh auth status` and `glab auth status` for a matching
   configured host. Still ambiguous: ask the user.

Missing origin remote: ask the user.

## Git versus forge

`git` owns local state. The forge CLI owns everything on the server.

| Operation | Tool |
|---|---|
| stage, commit, branch, local diff, log, worktree | `git` only |
| push | `git push` — command rules below unchanged |
| MR/PR create, description, edit | forge CLI — never a clipboard; assign me, pick the reviewer from the change (rule in the forge file) |
| MR/PR diff for review | forge CLI — local `git diff` only for uncommitted work |
| threads, approvals, merge, CI status | forge CLI only |
| rebase / branch update of a pushed MR/PR branch | forge CLI only — never local rebase plus force-push |

Concrete lifecycle commands per forge: [gitlab.md](gitlab.md) (GitLab, `glab`) and
[github.md](github.md) (GitHub, `gh`).

## Rules

Before committing, the code must compile and tests must pass, none failing or ignored.

1. Push only when the user asks for it in the current turn. Never push on your own after a commit. Push the current branch to its upstream, never to `master` or `main` directly.
2. Never use `--force`.
3. Never amend to modify files: add a fix commit and explain the reason.
4. Use git freely when checking differences with the previous version.
5. Commit each task as soon as its tests pass with assertions and coverage is checked. A headless or delegated run commits on its own: the commit is the user's ask, not a question for them ([`plan`](../plan/SKILL.md#rules-for-both-routes)).
6. Stage by path: `git add <file> <file>`, never `git add -A` or `git add .`. Run `git status` first; status, add, and commit fit one shell call (`git status --short && git add <files> && git commit -m "<subject>"`). Generated files (`__pycache__`, build output, caches) are never staged; add a `.gitignore` entry when the project lacks one.

## Commit message

Short and exact. Why over what: the diff already says what changed.

### Subject

`<type>(<scope>): <imperative summary>`, scope optional.

Types:

- `feat:` for feature
- `fix:` when fixing the codebase
- `refac:` for refactoring, mostly to prepare or finish a feat
- `chore:` to cleanup the codebase, removing dead code
- `docs:` when touching .md files or documentation
- `test:` when touching test only
- `perf:` for a measured performance change
- `build:` or `ci:` for build tooling or pipeline changes
- `revert:` when reverting a prior commit

Rules: imperative mood ("add", "fix", "remove", never "added" or "adds"), 50 characters
when possible and 72 at most, no trailing period, no restating the file name when the
scope already says it. Match the project convention for capitalisation after the colon.
One commit per slice: the subject names the behaviour that now works, never the layer
touched ([`plan`](../plan/SKILL.md#rules-for-both-routes)).

### Body

Skip it when the subject is self-explanatory. Add one only for a non-obvious why, a
breaking change, migration notes, or linked issues. Wrap at 72 characters, bullets with
`-`, issue references last (`Closes #42`, `Refs #17`).

Always add a body for: breaking changes, security fixes, data migrations, and reverts.
Future debuggers need the context.

Never in a commit message: "this commit does", "I", "we", "now", "currently", "as
requested by" (use a `Co-authored-by` trailer), AI attribution, emoji unless the project
convention requires it.

Examples:

- Not: `feat: added a new option so that users can export their invoices as CSV files`
- Yes:
  ```
  feat(export): add --format csv to invoice export

  Finance imports invoices into a spreadsheet each month and
  currently retypes them from the PDF export.

  Closes #214
  ```
- Breaking change:
  ```
  refac(config)!: read settings from ni.toml instead of ni.json

  BREAKING CHANGE: ni.json is no longer read. Rename it to ni.toml
  and convert the keys; startup fails with a pointer to the new file.
  ```

## Change description

When asked to describe a change for review, whatever the forge calls it (merge
request, pull request):

1. Write the description to a file. The body carries four parts, in this order:
   1. Summary, led by the smallest visual that shows the change. A diff hunk, a
      file tree, a call list, or a Mermaid diagram; one sentence when nothing
      visual exists.
   2. Evidence that it works, before and after: test output, a command and its
      result, a screenshot.
   3. Reversibility: one-way door (hard to undo: schema change, public contract,
      data deletion, a release users pin) or two-way door. Then the blast radius
      in one line: what breaks if it is wrong, who sees it.
   4. A link to the review checklist in [`code-review`](../code-review/SKILL.md).
2. Route per [Forge routing](#forge-routing). Create or update the MR/PR from that
   file with the forge CLI: commands in [gitlab.md](gitlab.md) or
   [github.md](github.md).

- Not: "Refactored the export module and fixed some tests."
- Yes: the changed signature's hunk, the test red then green, "two-way door: one
  caller, Finance sees nothing", the checklist link.

## Boundaries

This skill owns git usage, commit messages, forge routing, the git-versus-forge
boundary, and the MR/PR lifecycle files. Review flows, threads, and suggestions
belong to [`code-review`](../code-review/SKILL.md). Never create, read, or store
forge tokens.
