---
name: codebase-fix-and-pr
description: Apply code changes to a GitHub repository and automatically create a pull request. Takes user feedback or fix requirements, clones the repo, makes localized changes, commits to a new branch, and opens a PR via GitHub MCP.
compatibility: Requires git, GitHub authentication via PAT environment variable, and network access to GitHub
license: MIT
---

# Codebase Fix and Pull Request

## When to use this skill

Use this skill when you need to apply code fixes or improvements to a GitHub repository and automatically create a pull request. Specifically, use it when you need to:
- Fix bugs reported by users or found through code review
- Implement feature improvements
- Apply refactoring changes
- Fix documentation or configuration
- Apply automated code corrections
- Update dependencies or package versions

## Overview

This skill guides an agent through the complete workflow of analyzing user feedback, making targeted code changes, and creating a pull request. The agent uses GitHub authentication via environment variables and the GitHub MCP tools to complete the entire flow.

## Prerequisites

Before using this skill:

1. **Configure Git CLI**: Use the `configure-git-cli` skill to set up git user identity and GitHub authentication with your PAT
2. **Required environment variables**:
   - `GITHUB_EMAIL`: Your git email
   - `GITHUB_NAME`: Your git name
   - `GITHUB_PAT`: GitHub Personal Access Token with repo and workflow scopes

## Workflow

### Step 0: Configure Git (Prerequisite)

Before performing any git operations, ensure git is configured by invoking the `configure-git-cli` skill. This will:
- Set your git user email and name
- Configure GitHub authentication with your PAT
- Verify git credentials work correctly

Once configured, you can proceed with the following steps.

### Step 1: Parse Requirements

**Input required:**
- GitHub repository URL or `owner/repo` format
- User feedback, issue description, or fix requirement
- Specific files or areas to modify (optional)
- PR description and title (optional - will auto-generate if not provided)

**Actions:**
1. Parse the user feedback to understand:
   - What needs to be fixed
   - Why it needs to be fixed
   - Which files are likely affected
   - Success criteria for the fix
2. Break down complex requests into discrete changes
3. Plan the implementation approach

### Step 2: Repository Setup

**Actions:**
1. Git is already configured from Step 0, so authentication is ready
2. Clone the repository:
   ```bash
   git clone https://github.com/owner/repo.git
   cd repo
   ```
3. Verify repository structure and identify relevant files
4. Document the current state before making changes

### Step 3: Create Feature Branch

**Actions:**
1. Create a new branch with a descriptive name:
   ```bash
   git checkout -b fix/description-of-change
   # or
   git checkout -b feature/description-of-change
   ```
2. Branch naming conventions:
   - Use `fix/` prefix for bug fixes
   - Use `feature/` prefix for new features or improvements
   - Use `refactor/` prefix for refactoring work
   - Use `docs/` prefix for documentation updates
   - Use kebab-case for the description

3. Verify the branch was created successfully

### Step 4: Analyze and Make Changes

**For each required change:**

1. **Locate the relevant file(s)**
   - Read the file(s) that need modification
   - Understand the current code structure
   - Identify dependencies and imports

2. **Make targeted changes**
   - Modify only what's necessary to fix the issue
   - Maintain code style consistency
   - Keep changes focused and atomic
   - Update related tests if applicable

3. **Verify changes**
   - Check for syntax errors
   - Verify the change achieves the stated goal
   - Ensure no unrelated code was modified

**Common change patterns:**
- Bug fixes (modify logic)
- Configuration updates (modify config files)
- Documentation (update README, comments, docs)
- Dependency updates (modify package.json, requirements.txt)
- Test additions (new test files)
- Code refactoring (improve structure)

### Step 5: Commit Changes

**Actions:**
1. Stage the changes:
   ```bash
   git add .
   # or for specific files:
   git add path/to/file1 path/to/file2
   ```

2. Create a meaningful commit message:
   - Use conventional commit format (recommended)
   - First line: summary (50 characters max)
   - Blank line
   - Body: detailed explanation (optional)
   - Reference issue numbers if applicable

**Commit message examples:**

```
fix: resolve authentication timeout in user service

When a user login attempt exceeded 30 seconds, the timeout
handler was not properly cleaning up resources. This caused
the subsequent requests to fail. 

Now using a WeakMap to track in-flight requests and properly
clean up on timeout.

Fixes #123
```

```
feat: add retry logic to API client calls

Adds exponential backoff retry strategy for transient
API failures. Configurable retry count and backoff
multiplier.
```

```
docs: update installation instructions for macOS
```

### Step 6: Push to Remote Branch

**Actions:**
1. Push the branch to the remote repository:
   ```bash
   git push origin fix/description-of-change
   ```
2. Verify the push was successful
3. Note the branch name for PR creation

### Step 7: Create Pull Request via GitHub MCP

**Using the GitHub MCP authenticated tools:**

1. Call the GitHub MCP to create a pull request with:
   - **Title**: Clear, descriptive title (auto-generated or provided)
   - **Description**: What was changed and why
   - **Head**: The feature branch name
   - **Base**: The target branch (usually `main` or `develop`)

2. **PR Description template:**
   ```
   ## What changed
   Brief summary of the changes

   ## Why
   Explanation of the motivation for these changes

   ## How to test
   Steps to verify the fix works correctly

   ## Related issues
   Fixes #123
   Closes #456
   ```

3. **PR creation example:**
   - Title: "Fix authentication timeout in user service"
   - Base branch: "main"
   - Head branch: "fix/auth-timeout"
   - Description: Includes what changed, why, testing steps

### Step 8: Verify PR Creation

**Actions:**
1. Confirm the PR was created successfully
2. Verify:
   - All changes are visible in the PR diff
   - Commit history is clean
   - No unrelated files were modified
   - PR description is clear
3. Provide the PR URL and summary to the user

## Common Patterns

### Bug Fix Pattern
```
1. Identify the bug in the code
2. Understand the root cause
3. Fix the specific issue (usually 1-2 files)
4. Create test case if not present
5. Commit with "fix:" prefix
6. Create PR with issue reference
```

### Feature Addition Pattern
```
1. Identify where to add the feature
2. Implement the feature
3. Add tests for the feature
4. Update documentation if needed
5. Commit with "feat:" prefix
6. Create PR with feature description
```

### Documentation Update Pattern
```
1. Identify documentation that needs updating
2. Update markdown or comment documentation
3. Fix any broken links
4. Commit with "docs:" prefix
5. Create PR with summary of changes
```

### Dependency Update Pattern
```
1. Update version in package.json or requirements.txt
2. Run dependency installation/update
3. Test that the code works with new version
4. Commit with "chore:" or "deps:" prefix
5. Create PR documenting version changes
```

## Error Handling

**If repository clone fails:**
- Verify the PAT has repo access permissions
- Check that the repository URL is correct
- Ensure network connectivity

**If branch creation fails:**
- Check if the branch already exists
- Verify you're in the correct repository directory
- Ensure git is properly configured

**If commit fails:**
- Verify files exist and have correct changes
- Check for merge conflicts (if pulling latest)
- Ensure file permissions are correct

**If PR creation fails:**
- Verify the branch has been pushed successfully
- Check that the base branch exists
- Ensure the GitHub PAT has PR creation permissions
- Verify no branch protection rules are blocking

## GitHub MCP Integration

The skill uses the GitHub MCP tools which are pre-authenticated with the GitHub PAT:

**Available operations:**
- `create_pull_request`: Create a new PR
- Git operations via command line using configured credentials
- Repository metadata access

**Environment variables required:**
- `GITHUB_PAT`: GitHub Personal Access Token with repo and pull-request scopes
- (Git is configured via the `configure-git-cli` skill)

## Best Practices

1. **Make atomic commits**: Each commit should represent one logical change
2. **Keep PRs focused**: Fix one issue or implement one feature per PR
3. **Write clear messages**: Future developers will read your commits
4. **Test locally first**: Verify changes work before pushing
5. **Reference issues**: Link to related issues in commit and PR descriptions
6. **Describe the "why"**: Explain motivation, not just what changed
7. **Keep changes minimal**: Don't refactor unrelated code

## Example Use Cases

### Bug Fix Example
**User feedback:** "The login button doesn't work on mobile devices"

**Agent process:**
1. Parse the issue: Mobile login failure
2. Clone repository
3. Create branch: `fix/mobile-login-button`
4. Locate login component
5. Debug and fix responsive design issue
6. Test the fix
7. Commit: "fix: correct mobile login button styling"
8. Push branch
9. Create PR: "Fix login button on mobile devices"

### Feature Addition Example
**User feedback:** "Add dark mode support to the application"

**Agent process:**
1. Parse the requirement: Implement dark mode
2. Clone repository
3. Create branch: `feature/dark-mode-support`
4. Implement theme switching logic
5. Update components to support theme
6. Add configuration option
7. Create tests for theme switching
8. Commit: "feat: add dark mode theme support"
9. Push branch
10. Create PR: "Add dark mode support with theme switcher"

### Documentation Update Example
**User feedback:** "The API documentation is outdated"

**Agent process:**
1. Parse the requirement: Update API docs
2. Clone repository
3. Create branch: `docs/update-api-documentation`
4. Locate and update README or docs folder
5. Fix outdated examples
6. Update endpoint descriptions
7. Commit: "docs: update API documentation examples"
8. Push branch
9. Create PR: "Update API documentation with current endpoints"

## Success Criteria

The workflow is complete when:
- ✅ Repository successfully cloned
- ✅ Feature branch created with descriptive name
- ✅ All required changes made to files
- ✅ Changes are focused and atomic
- ✅ Commit message is clear and follows conventions
- ✅ Changes pushed to remote
- ✅ Pull request created successfully
- ✅ PR includes clear description and issue references
- ✅ User provided with PR link and summary
