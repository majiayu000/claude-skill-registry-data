---
name: git-conventional-commits
description: Guide branch creation, commit messages, and titles so the repo’s semantic workflow is enforced
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: documentation
  since: "2026-02-25"
---

# When to use

- When the user authors commits 
- When the user asks about conventional commits

## Use Instead [if available]

- Use `pr-create` for end-to-end PR title/body drafting and Jira-linking workflow.
- Use `github-pull-request-handling` for resolving and replying to existing PR review conversations.

## Standard

Apply the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages and PR titles.

## Allowed types

Use exactly one of these types in PR titles and commits:

| Type          | Purpose                                     |
|---------------|---------------------------------------------|
| `chore`       | Maintenance, tooling, config changes        |
| `ci`          | CI/CD pipeline changes                      |
| `deploy`      | Deployment-related changes                  |
| `docs`        | Documentation only                          |
| `feat`        | New feature                                 |
| `fix`         | Bug fix                                     |
| `improvement` | General improvement (non-feature, non-fix)  |
| `perf`        | Performance improvement                     |
| `build`       | Build system/dependency changes             |
| `refactor`    | Code refactoring, no behavior change        |
| `style`       | Formatting only, no behavior change         |
| `test`        | Adding or updating tests                    |

## Format

```
<type>[(scope)]: <description>

[optional body]

[optional footer(s)]
```

- **Scope** (optional): Must match `[a-z:_-]+` (lowercase letters, digits, underscores, colons, hyphens). Examples: `sdk`, `api`, `my_component`.
- **Description**: Short, imperative summary. No period at the end.

## Breaking changes

For breaking changes, append `!` after type/scope and include a `BREAKING CHANGE:` footer when relevant.

Example:

```
feat(api)!: switch auth token format

BREAKING CHANGE: clients must re-authenticate with the new token format
```

## Body and footers

- Body is optional and should explain motivation ("why"), not only implementation details.
- Separate body from subject with one blank line.
- Use explicit footers for traceability, such as:
  - `BREAKING CHANGE: <description>`
  - `Refs: UN-12345` or `Refs: #123`
  - `Reviewed-by: <name>`

## Commit Summary 

- `feat(toolkit): add streaming support`
- `feat(sdk): update message endpoint`
- `ci: add semantic PR validation`

## Branch & commit workflow

1. **Check current branch**
   - Run `git branch --show-current`; do not commit directly to `master`/`main`
   - If you are still on the base branch, create a feature branch following this pattern: `fix/<scope>/<short-slug>` or `feat/<scope>/<short-slug>`
   - Keep branch names short but descriptive (e.g., `fix/payment/null-check`)

2. **Review & stage**
   - Inspect your diff (`git diff` for unstaged, `git diff --cached` for staged)
   - Stage with `git add -A` once you understand all changes
   - Optionally include `Refs: <ticket>` block in the commit body to link Jira/Ticket numbers (the repo tooling can pick this up)

3. **Write the commit**
   - Use the `<type>(<scope>): <description>` format
   - Keep the subject ≤ 72 characters without trailing period
   - Add a blank line and optional body for context, explaining why the change is necessary

4. **Examples**
   - `fix(api): handle missing authorization header`
   - `feat(payments): add refund webhook handler`
   - `chore(deps): upgrade pytest to 9.0`

## Branch/commit rules
- Always branch before committing (avoid `master`/`main`)
- Use imperative language and don’t end with punctuation
- Keep commits focused on a single concern
- Reference tickets/issue IDs in the `Refs:` section when relevant

## Quick checklist

Before finalizing a commit message or PR title:

- [ ] Starts with a valid type
- [ ] Scope is specific and relevant
- [ ] Description is imperative and has no trailing period
- [ ] First line is under 72 characters
- [ ] Breaking changes use `!` and/or a `BREAKING CHANGE:` footer
- [ ] Body explains motivation for non-trivial changes