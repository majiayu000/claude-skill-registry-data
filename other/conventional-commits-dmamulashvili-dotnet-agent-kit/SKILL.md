---
name: conventional-commits
description: Write, review, or fix git commit messages that follow the Conventional Commits 1.0.0 spec. Use when composing a commit message, squash/merge message, or PR title, when asked to lint or rewrite commit history, or when deciding the SemVer bump implied by a set of commits.
---

# Conventional Commits 1.0.0

Spec source: https://www.conventionalcommits.org/en/v1.0.0/ (licensed CC BY 3.0).

## Message format

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- **Header** (first line): `type`, optional `(scope)`, optional `!`, then a colon and a single space, then the description.
- **Body**: optional, starts after exactly one blank line following the header. Free-form, any number of paragraphs.
- **Footers**: optional, start after one blank line following the body (or header if no body).

## Rules (normative)

1. The header MUST start with a type (a noun like `feat`, `fix`), followed by optional scope, optional `!`, and a REQUIRED `: ` (colon + space).
2. Use `feat` when the commit adds a new feature.
3. Use `fix` when the commit fixes a bug.
4. A scope MAY follow the type, as a noun naming a part of the codebase, in parentheses: `fix(parser):`.
5. The description MUST come immediately after `: ` and briefly summarize the change.
6. The body MAY be added and MUST begin one blank line after the description.
7. The body is free-form; multiple newline-separated paragraphs are fine.
8. One or more footers MAY follow one blank line after the body. Each footer is a word token, then `: ` or ` #`, then a value (git-trailer style), e.g. `Reviewed-by: Z`, `Refs #123`.
9. Footer tokens MUST use `-` instead of spaces (`Acked-by`). Exception: `BREAKING CHANGE` may contain a space.
10. Footer values MAY contain spaces and newlines; a value ends when the next valid `token: ` / `token #` pair appears.
11. Breaking changes MUST be marked either with `!` in the header or with a footer.
12. A breaking-change footer MUST be uppercase `BREAKING CHANGE: <description>`.
13. With `!` (placed right before the `:`), the footer MAY be omitted; the header description then describes the break.
14. Other types beyond `feat`/`fix` MAY be used.
15. Parsers MUST treat all elements as case-insensitive, except `BREAKING CHANGE`, which MUST be uppercase.
16. `BREAKING-CHANGE` is equivalent to `BREAKING CHANGE` as a footer token.

## Common types

Only `feat` and `fix` are defined by the spec. The widely used set (from `@commitlint/config-conventional`, Angular convention):

| Type | Use for |
|---|---|
| `feat` | New user-facing feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace, semicolons — no behavior change |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system or external dependencies |
| `ci` | CI configuration and scripts |
| `chore` | Maintenance that doesn't touch src or tests |
| `revert` | Reverting previous commit(s) |

If the repo has its own config (`commitlint.config.*`, `.commitlintrc*`, `.czrc`, `package.json` → `commitlint`/`config.commitizen`, `release-please`, `semantic-release` config), follow its allowed types and scopes over this table. Also check `git log --oneline -20` to match existing scope names and casing.

## SemVer mapping

- `fix` → PATCH
- `feat` → MINOR
- Any commit with `!` or a `BREAKING CHANGE` footer, regardless of type → MAJOR
- Other types → no release on their own (unless breaking)

To compute a bump over a range, take the highest of these across all commits.

## How to write a message

1. Inspect the change (`git diff --staged`, or the diff provided).
2. If it mixes unrelated concerns (e.g. a feature plus an unrelated fix), recommend splitting into separate commits rather than picking one type.
3. Pick the type by intent, not by file: a bug fix in docs tooling is `fix`, a typo fix in README is `docs`.
4. Add a scope only if it adds clarity and matches the repo's existing scopes.
5. Description: imperative mood ("add", not "added"/"adds"), lowercase start, no trailing period, aim for ≤ 72 chars in the full header. (These are conventions, not spec requirements — defer to the repo's style.)
6. Body: explain *what* and *why*, not *how*; wrap at ~72 columns.
7. If any public API or behavior changes incompatibly, mark it: add `!` and/or a `BREAKING CHANGE:` footer explaining what breaks and how to migrate.
8. Reference issues in footers: `Refs: #123`, `Closes #45`.

## How to review/lint a message

Check in order and report each violation with a corrected version:

- Header matches `^[a-zA-Z]+(\([^()\r\n]+\))?!?: \S.*$`
- Exactly one blank line between header and body, and between body and footers
- Footer tokens are hyphenated (except `BREAKING CHANGE`) and use `: ` or ` #`
- `BREAKING CHANGE` is uppercase; `!` sits directly before `:`
- Type is in the repo's allowed list (or the common list above)
- Type matches the actual change (e.g. a new capability labeled `fix` should be `feat`)

## Examples

Breaking change via footer:
```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

Breaking change via `!` with scope:
```
feat(api)!: send an email to the customer when a product is shipped
```

Both `!` and footer:
```
feat!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

No body:
```
docs: correct spelling of CHANGELOG
```

Multi-paragraph body and multiple footers:
```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

Revert (spec suggests, doesn't mandate):
```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Edge cases (from the spec FAQ)

- **Early development**: write commits as if already released — someone is consuming the changes.
- **Type casing**: any case works; be consistent (lowercase is the norm).
- **Wrong type used, not yet merged/released**: fix with `git rebase -i` (reword). Never rewrite history that's already pushed to a shared branch without the user's explicit OK.
- **Non-spec type (typo like `feet`)**: not fatal, but tooling will ignore that commit.
- **Squash workflows**: only the final squash/merge message needs to conform; PR titles often become that message, so apply the same format to PR titles.
- **Reverts**: not defined by the spec; use `revert:` with a `Refs:` footer listing SHAs unless the repo's tooling says otherwise.