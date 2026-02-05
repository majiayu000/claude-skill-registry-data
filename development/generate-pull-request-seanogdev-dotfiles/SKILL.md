---
name: generate-pull-request
description: Generate a pull request using GitHub CLI following the project's pull request template.
---

# Rule: Generating a Pull Request

## Goal

To guide an AI assistant in creating a pull request using the GitHub CLI (`gh pr create`) that follows the project's pull request template and conventions.

## Process

1.  **Verify branch is pushed:**
    - Check that the current branch exists on remote: `git ls-remote --heads origin $(git branch --show-current)`
    - If not pushed, push the branch first: `git push origin HEAD`
    - This is required before creating a PR

2.  **Check for PR templates:** Look for pull request templates in common locations:
    - `.github/pull_request_template.md`
    - `.github/PULL_REQUEST_TEMPLATE.md`
    - `.github/PULL_REQUEST_TEMPLATE/*.md` (multiple templates)
    - `docs/pull_request_template.md`

3.  **Analyze the template:** If a template exists, read it to understand:
    - Required sections and format
    - What information is expected
    - Any checklists or specific requirements

4.  **Gather PR information:**
    - **Title:** Generate a clear, concise title summarizing the changes
    - **Description:** Analyze git changes to create a comprehensive description
    - **Changes summary:** List key changes, files modified, and functionality added/updated
    - **Related issues:** Check commit messages and branch name for issue references
    - **Testing:** Document what was tested
    - **Checklist items:** Complete any checklist items from the template

5.  **Analyze git state:**
    - Run `git status` to confirm there are changes to include
    - Run `git log origin/[base-branch]..HEAD` to see commits that will be in the PR
    - Run `git diff origin/[base-branch]...HEAD --stat` to get an overview of changes

6.  **Generate PR content:**
    - Fill in the template (if it exists) or create a well-structured description
    - Use markdown formatting for readability
    - Include code examples if relevant
    - Link to related issues, PRs, or documentation

7.  **Create the PR:**
    - Use `gh pr create --title "..." --body "..."`
    - For multi-line body content, use a heredoc for proper formatting:
      ```bash
      gh pr create --title "..." --body "$(cat <<'EOF'
      PR description here
      EOF
      )"
      ```
    - Default base branch is usually `main` or `master` unless specified otherwise

## PR Description Structure

If no template exists, use this default structure:

```markdown
## Summary

Brief overview of what this PR does and why.

## Changes

- List of key changes
- Organized by component or feature
- Include file paths when relevant

## Testing

- How this was tested
- Test cases covered
- Manual testing performed

## Related Issues

Closes #123
Relates to #456

## Screenshots (if applicable)

[Include screenshots for UI changes]

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changeset added (if applicable)
- [ ] No breaking changes (or documented if present)
```

## Rules

1. **Always check for templates first** - Use the project's template if it exists
2. **Be thorough** - Include all relevant information about the changes
3. **Use present tense** - Write descriptions in present tense (e.g., "Adds feature" not "Added feature")
4. **Reference issues** - Link to related issues using GitHub's syntax (`Closes #123`, `Fixes #456`)
5. **Include testing info** - Always document what testing was performed
6. **Use heredoc for body** - For proper formatting of multi-line PR descriptions

## Example Command

```bash
gh pr create --title "Fix: Resolve button hover state in dark mode" --body "$(cat <<'EOF'
## Summary

Fixes the button hover state when the application is in dark mode.

## Changes

- Updated `Button.tsx` to use theme-aware hover colors
- Added dark mode test cases in `Button.test.tsx`

## Testing

- ✅ Manual testing in dark mode
- ✅ Unit tests pass
- ✅ Visual regression tests updated

## Related Issues

Closes #789

## Checklist

- [x] Tests added
- [x] Changeset added
- [x] No breaking changes
EOF
)"
```

## Final Instructions

1. Verify the branch is pushed to remote before creating PR
2. Check for PR templates in the repository
3. Analyze git changes and commits to understand the scope
4. Generate a comprehensive PR title and description
5. Use heredoc format for the `--body` parameter
6. Create the PR using `gh pr create`
7. Output the PR URL to the user after creation
8. Remind user to request reviews if needed
