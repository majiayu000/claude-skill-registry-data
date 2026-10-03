---
name: commit-message
description:
  'Draft Conventional Commit messages grounded in a real git diff. Use when the user asks to commit,
  write, draft, create, generate, prepare, build, or amend a commit message, mentions Conventional
  Commits or BREAKING CHANGE footers, or has staged or unstaged diffs available.'
license: Apache-2.0
metadata:
  author: AutanaSoft
  version: '1.0.0'
---

# Commit Message

Produce a Conventional Commit message (`type(scope): description`) anchored in the real `git diff`,
surface breaking changes, obtain explicit user approval, then run `git commit`. Six rule cards
across five categories enforce header format, safety, grounding, procedure, and style.

## When to Apply

Reference these guidelines when:

- Drafting, writing, or generating a commit message from a real `git diff`
- Amending an existing commit or converting a rough plan into a Conventional Commit
- Mentioning Conventional Commits, `BREAKING CHANGE` footers, or `type(scope)` headers
- Running `git commit` after a human review of the proposed message

## When NOT to Apply

- Auto-generated merge commits, release squash commits, or any commit where the user has not asked
  for a handcrafted message
- Documentation-only or whitespace-only commits where the user has explicitly said "no need for a
  fancy message"
- Workflows that bypass `git commit` (e.g., direct patches, PR descriptions, hand-written changelog
  files)

## Rule Categories by Priority

| Priority | Category      | Impact   | Reference                                              |
| -------- | ------------- | -------- | ------------------------------------------------------ |
| 1        | Header Format | CRITICAL | `references/header-format.md`                          |
| 2        | Safety        | CRITICAL | `references/safety.md`                                 |
| 3        | Grounding     | HIGH     | `references/grounding.md`                              |
| 4        | Procedure     | MEDIUM   | `references/commit-types.md`, `references/workflow.md` |
| 5        | Style         | LOW      | `references/style.md`                                  |

## Quick Reference

### 1. Header Format (CRITICAL)

- Header must follow `type(scope): description` with a mandatory scope - `header-format`
- Header line must stay at or under 100 characters - `header-format`
- Use a `BREAKING CHANGE:` footer when API or response shapes change - `header-format`

### 2. Safety (CRITICAL)

- No destructive Git commands without an explicit user request - `safety`
- No empty commits, no bypassed pre-commit or commit-msg hooks - `safety`
- Warn before committing files that may contain secrets - `safety`

### 3. Grounding (HIGH)

- Analyze the real `git diff`; do not guess from filenames or memory - `grounding`
- Do not invent issue IDs, ticket prefixes, or product names - `grounding`
- Honor repository-local commit conventions when visible; do not invent them - `grounding`

### 4. Procedure (MEDIUM)

- Pick a Conventional Commit type from the 11-type catalog - `commit-types`
- Infer scope from staged paths using a small heuristic set - `commit-types`
- Follow the 8-step workflow from `git status` to approved `git commit` - `workflow`

### 5. Style (LOW)

- Default to neutral professional English; honor an explicit other-language request - `style`
- No regional variants (voseo, slang, dialect grammar) unless explicitly asked - `style`

## How to Use

Each rule lives in `references/`. Read the rule file that applies to the task:

```text
references/header-format.md
references/safety.md
references/grounding.md
references/commit-types.md
references/workflow.md
references/style.md
```

Each rule file contains:

- Brief explanation of why it matters
- Incorrect code example
- Correct code example
- Reference link

## Edge Cases

- Diff spans multiple concerns: split into multiple commits or pick the dominant scope and call it
  out in the body
- Revert commit: use `revert(scope): ...` with a body that names the reverted SHA
- User supplied a pre-written message: honor it; still validate header format and footers
- Repo has strict local hooks (commitlint, husky, signed commits): read `.husky/` and any commitlint
  config before drafting; conform to it
- Possible secrets in the diff: warn the user and stop before staging or committing
- Diff is on a protected branch with no push rights: only commit locally; do not push

## Output Contract

After a successful commit, return exactly these three lines:

```text
- Message used: <header>
- Commit: <sha> <header>
- Status: committed to <branch>
```

Replace `<header>` with the actual commit header, `<sha>` with the commit hash returned by
`git commit`, and `<branch>` with the branch the commit landed on.
