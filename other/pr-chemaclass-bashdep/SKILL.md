---
name: pr
description: Push branch and create a GitHub PR following the bashdep PR template
user-invocable: true
argument-hint: "[#issue]"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Create Pull Request

Push the current branch and open a PR using the project's PR template.

> **IMPORTANT:** This skill MUST be used for ALL pull request creation -
> even when the user just says "create pr" without `/pr`. Never create a
> PR without following these steps.

## Current Branch Context
- Branch: !`git branch --show-current`
- Commits: !`git log main..HEAD --oneline 2>/dev/null`
- Changed files: !`git diff main..HEAD --stat 2>/dev/null`

## Arguments
- `$ARGUMENTS` - Issue reference (optional, e.g., `#42` or `42`). If
  provided, the PR Background section links to it.

## Instructions

1. **Review the branch context above** - commits and changed files are
    already loaded.

2. **MANDATORY: Update `CHANGELOG.md`** - Read it and check the
    `## Unreleased` section. If the changes from this branch aren't
    already listed there, you MUST update it before pushing. **Do NOT
    skip. Do NOT proceed without verifying.**
    - Add entries under the appropriate subsection
      (`### Added`, `### Changed`, `### Fixed`, `### Removed`)
    - Reference the issue number where applicable (e.g., `(#123)`)
    - Commit the update:
      ```bash
      git add CHANGELOG.md && git commit -m "docs: update changelog"
      ```

3. **Verify quality gate locally before pushing**:
    ```bash
    make pre_commit/run
    ```
    The pre-commit hook (if installed) runs the same checks. If it fails,
    read the output, fix the underlying issue, commit the fix, then retry.
    **Do NOT use `--no-verify` to bypass.**

4. **Push branch**:
    ```bash
    git push -u origin HEAD
    ```

5. **Generate PR title**:
    - If `$ARGUMENTS` contains an issue number, fetch the issue title:
      ```bash
      gh issue view <number> --json title -q '.title'
      ```
    - Format: `<type>(<scope>): <short description>` (conventional commit
      style, under 70 chars)
    - Derive the type from the branch prefix
      (`feat/` → feat, `fix/` → fix, `docs/` → docs)

6. **Create PR** using the structure from
    `.github/PULL_REQUEST_TEMPLATE.md`:

    ```bash
    gh pr create --title "<title>" --assignee @me --body "$(cat <<'EOF'
    ### 🔗 Ticket

    <Related #<issue-number>, or "n/a">

    ## 🤔 Background

    <1-2 sentences: motivation and context for the changes>

    ## 💡 Goal

    <One sentence: the outcome this PR delivers>

    ## 🔖 Changes

    - <bullet 1: what changed and why>
    - <bullet 2>
    - <bullet 3> (optional)

    ## 🖼️ Screenshots

    n/a
    EOF
    )"
    ```

    **MANDATORY:** Always follow the template structure
    (`🔗 Ticket` → `🤔 Background` → `💡 Goal` → `🔖 Changes` →
    `🖼️ Screenshots`). Never use a different format.

    **Assignee:** Always assign to `@me`.

    **Issue linking:** Use `Related #<n>` in the Ticket section.
    `Closes #<n>` / `Fixes #<n>` are fine in commit bodies if the user
    wants auto-close, but keep the PR template's prose form.

    **Body guidelines:**
    - Background: 1-2 sentences of context (the why)
    - Goal: a single sentence framing the outcome
    - Changes: 2-4 short bullets focused on **what + why**
    - **No file lists, no code snippets, no class names** in the body
    - Drop the `🖼️ Screenshots` section content for non-UI changes
      (replace with `n/a`)

7. **Report the PR URL** to the user.

## Example Usage

```
/pr
/pr #42
/pr 15
```
