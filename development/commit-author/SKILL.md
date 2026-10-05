---
name: commit-author
version: 1.0.0
description: Generate concise Conventional Commits messages from a staged diff. Enforces full type set, imperative subject lines, no AI co-author attribution. Use when user wants to commit, asks for a commit message, mentions "commit", or invokes /commit.
---

# Git Commit Standards

## 1. Format
* **Structure:** `<type>(<optional scope>): <subject>`

## 2. Allowed Types

Full Conventional Commits v1.0.0 type set (Angular convention):

| Type | When to use |
|---|---|
| `feat` | New feature for the user (MINOR in SemVer) |
| `fix` | Bug fix for the user (PATCH in SemVer) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Code change that improves performance |
| `docs` | Documentation-only changes |
| `style` | Formatting, whitespace, semicolons — no code-meaning change |
| `test` | Adding or correcting tests; no production code change |
| `build` | Build system or external dependency changes (e.g. npm, go.mod, Dockerfile) |
| `ci` | CI configuration changes (GitHub Actions, pipelines) |
| `chore` | Maintenance tasks that don't fit elsewhere (no src/test changes) |
| `revert` | Reverts a previous commit; body must reference the reverted SHA |

## 3. Subject Line
* **Rules:** Use imperative mood (e.g., `add`, not `added`), maximum 50 characters, lowercase start, and no trailing period.

## 4. Body
* **Content:** Explain *why* the change was made, not *what* changed. Do not write line-by-line file summaries.
* **Formatting:** Hard wrap lines at 72 characters.

## 5. Footers
* **Breaking Changes:** Must begin with `BREAKING CHANGE:` followed by a migration path. Applies to any type and forces a MAJOR version bump.
* **References:** Append related issues at the bottom (e.g., `Resolves #12`).

## 6. Attribution
* **Do not add AI co-authorship.** Never include `Co-Authored-By: Claude` or any other AI-attribution footer. Commits belong to the human author who reviewed and approved the change.

## 7. Execution Protocol

* **User-initiated only.** This skill activates *only* when the user explicitly asks to commit — phrases like "commit this", "write the commit message", "let's commit", or invoking `/commit`. **Never volunteer to commit unprompted.** Don't propose commits at the end of a task, don't pre-emptively stage files, and don't run `git add` / `git commit` as cleanup after other work.
* **Consent to execute.** When asked to draft a commit message: ask whether the user will run the commit themselves or wants you to. **Never run `git commit` without explicit go-ahead** for the specific commit being created.
* **Scope per ask.** Permission to commit one set of changes is not blanket permission for future commits in the same session. Each commit needs its own confirmation.
* **Signing:** Delegated commits must be GPG signed if configured, unless the user explicitly opts out.