---
name: create-pr
description: Create a feature branch, commit finished changes, push to remote, and open a high-quality pull request with a structured description. Use when implementation is complete and the work is ready for review.
allowed-tools: [Bash, git, github]
---

# Create Pull Request

Creates a reviewable branch, commits completed work, pushes it, and prepares a clear pull request.

---

## When To Use

Use this skill when:

- A feature is complete
- A bug fix is complete
- A refactor is complete
- UI changes are complete
- Database or backend changes are complete

Do not use this skill before implementation is finished.

---

## Step 1 — Review Changes

Review the diff before creating any branch, commit, or pull request.

```bash
git diff
```

Summarise:

- What changed
- Why it changed
- Files affected
- Risks
- Testing performed

---

## Step 2 — Create a Branch and Commit

Use a branch name that matches the work type:

- `feature/<short-description>` for features
- `fix/<short-description>` for bug fixes
- `refactor/<short-description>` for refactors

Run the appropriate commands:

```bash
git checkout -b feature/$ARGUMENTS
git add .
git commit -m "feat: $ARGUMENTS"
git push origin feature/$ARGUMENTS
```

Adjust the branch prefix and commit message to match the actual change.

Preferred semantic commit prefixes:

- `feat:` new feature
- `fix:` bug fix
- `refactor:` code refactor
- `ui:` UI changes
- `db:` database changes
- `test:` tests
- `docs:` documentation

Example:

```bash
git commit -m "feat: show category name instead of category id in recipe view"
```

---

## Step 3 — Prepare the Pull Request Description

Use this template:

```markdown
# Pull Request: $ARGUMENTS

## Summary
[Brief summary of changes]

## Changes Made
- [Change 1]
- [Change 2]
- [Change 3]

## Testing Done
- [Test 1]
- [Test 2]
- [Test 3]

## Screenshots / GIFs
[If applicable]

## Implementation Notes
[Any special implementation considerations]

## Breaking Changes
[List any breaking changes]

## Related Issues
Closes #[issue number]

## Reviewers
[Suggested reviewers if any]
```

---

## Step 4 — Create the Pull Request

If the GitHub MCP tool is available, use it to create the pull request with the prepared title and body.

Example implementation:

```javascript
try {
  const templateContent = `# Pull Request

## Summary
${$ARGUMENTS}

## Changes Made
- Updated relevant files
- Implemented requested feature or fix
- Adjusted logic and UI where necessary

## Testing Done
- Verified feature works
- Checked edge cases
- Confirmed no regressions

## Implementation Notes
See commits for detailed implementation.

## Breaking Changes
None

## Related Issues
Closes # [issue number]

## Checklist
- [x] Code follows project standards
- [x] Self-review completed
- [x] No new warnings
- [x] Tests pass
`;

  const pullRequest =
    await mcp__modelcontextprotocol_server_github__server_github.createPullRequest({
      owner: "jerseycheese",
      repo: "narraitor",
      title: `Fix: ${$ARGUMENTS}`,
      body: templateContent,
      head: `feature/${$ARGUMENTS}`,
      base: "develop",
    });

  console.log(`Successfully created PR: ${pullRequest.html_url}`);
} catch (error) {
  console.error("Error creating PR with MCP GitHub tool:", error);

  console.log("Please create the PR manually using this URL:");
  console.log(
    `https://github.com/jerseycheese/narraitor/compare/develop...feature/${$ARGUMENTS}`
  );
}
```

If MCP is unavailable, create the PR manually using the compare URL pattern shown above.

---

## Output Format

After creating the pull request, return:

- Branch name
- Files changed
- Commit message
- PR title
- PR description
- PR link
- Risks
- Testing summary

---

## Rules

- Do not commit directly to `main` or `develop`
- Always create a feature, fix, or refactor branch
- Always review the diff before committing
- Always write a clear PR description
- Always link related issues if available
- Prefer small PRs over large PRs
- Ensure no secrets or credentials are committed
- Document database changes when present
- Ensure permissions and visibility rules are not broken
