---
name: git
description: Git workflow standards, commit conventions, hooks, and pull request practices. Use this when users need guidance on Conventional Commits, Git hooks with Lefthook, pull request templates, .gitignore configuration, or Git workflow best practices for team collaboration.
license: MIT - Complete terms in LICENSE.txt
---

# Git Skills & Best Practices

Git workflow standards, commit conventions, hooks, and pull request practices.

## Table of Contents

- [Git Workflow](#git-workflow)
- [Git Hooks](#git-hooks)
- [Pull Request Templates](#pull-request-templates)
- [GitHub CLI (gh) Integration](#github-cli-gh-integration)

---

## Git Workflow

### Conventional Commits

**MUST use Conventional Commits format** - this is a strict requirement. Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/):

**Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**
```
feat(auth): add user login functionality
fix(api): resolve race condition in data fetching
docs: update README with setup instructions
```

### .gitignore

Include standard exclusions for React/React Native projects:

**Essential entries:**
```
# Environment variables
.env
.env.local
.env.*.local

# Dependencies
node_modules/
.pnp
.pnp.js

# Build outputs
dist/
build/
.next/
out/

# Testing
coverage/
.nyc_output/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
pnpm-debug.log*

# pnpm
.pnpm-store/

# Misc
.cache/
.temp/
.turbo/
```

---

## Git Hooks

### Lefthook Integration

**PREFER** using [Lefthook](https://github.com/evilmartians/lefthook) for managing git hooks (guideline). Other tools are acceptable if they meet the strict hook requirements below.

**Configuration (`lefthook.yml`):**

```yaml
pre-commit:
  parallel: true
  commands:
    lint:
      run: pnpm run lint
      stage_fixed: true
    format:
      run: pnpm run format:check
      stage_fixed: true
    test:
      run: pnpm run test:ci
      stage_fixed: true

pre-push:
  parallel: true
  commands:
    test:
      run: pnpm run test
    typecheck:
      run: pnpm run typecheck
```

**Pre-commit hooks (Strict Requirements):**
- **MUST** run linting checks
- **MUST** run formatting checks
- **MUST** run unit tests
- Auto-fix issues when possible

**Pre-push hooks (Strict Requirements):**
- **MUST** run full test suite
- **MUST** run TypeScript type checking (`tsc`)
- **MUST** prevent pushing if checks fail

---

## Pull Request Templates

Create `.github/pull_request_template.md` with the following structure:

```markdown
## Overview
<!-- Brief description of what this PR accomplishes -->

## Solution
<!-- Detailed explanation of the approach and implementation -->

## Screenshots
<!-- Add screenshots or screen recordings if applicable -->
<!-- For web: browser screenshots -->
<!-- For mobile: iOS/Android screenshots -->

## Ticket
<!-- Link to JIRA ticket or other project management tool -->
<!-- Format: [PROJECT-123](link-to-ticket) -->

## Tested On
<!-- Check all that apply -->
- [ ] Web
- [ ] Mobile
- [ ] iOS
- [ ] Android
- [ ] Other: ___________

## Additional Notes
<!-- Any additional context, breaking changes, or follow-up items -->
```

---

## GitHub CLI (gh) Integration

The GitHub CLI (`gh`) enables AI agents to interact with GitHub repositories programmatically, automating common Git and GitHub workflows.

### Authentication

**Setup:**
```bash
# Login to GitHub
gh auth login

# Check authentication status
gh auth status

# Refresh authentication token
gh auth refresh
```

**For AI Agents:**
- Use `gh auth token` to retrieve the authentication token for API calls
- Configure authentication before performing any GitHub operations
- Use `gh auth setup-git` to configure Git credentials automatically

### Pull Request Management

**Create Pull Requests:**
```bash
# Create a PR interactively
gh pr create

# Create a PR with title and body
gh pr create --title "feat: add user authentication" --body "Implements OAuth2 login flow"

# Create a PR from current branch to main
gh pr create --base main --head feature/auth --title "feat: add authentication"

# Create a draft PR
gh pr create --draft
```

**View and Manage PRs:**
```bash
# List open PRs
gh pr list

# View PR details
gh pr view <number>

# View PR diff
gh pr diff <number>

# Checkout PR locally
gh pr checkout <number>

# Review PR status and checks
gh pr checks <number>

# Comment on PR
gh pr comment <number> --body "LGTM! Great work."

# Approve PR
gh pr review <number> --approve

# Merge PR
gh pr merge <number> --squash
gh pr merge <number> --merge
gh pr merge <number> --rebase
```

**For AI Agents:**
- Automatically create PRs after completing features
- Check PR status and wait for CI checks to pass
- Add comments with analysis or suggestions
- Merge PRs after approval (when appropriate)

### Issue Management

**Create and Manage Issues:**
```bash
# Create an issue
gh issue create --title "Bug: login fails" --body "Description of the bug"

# List issues
gh issue list

# View issue details
gh issue view <number>

# Comment on issue
gh issue comment <number> --body "This is fixed in PR #123"

# Close issue
gh issue close <number>

# Reopen issue
gh issue reopen <number>
```

**For AI Agents:**
- Create issues for bugs discovered during code review
- Link issues to PRs automatically
- Update issue status based on PR status
- Create issues from TODO comments or technical debt

### Repository Operations

**Repository Management:**
```bash
# Clone a repository
gh repo clone owner/repo

# View repository details
gh repo view

# Create a new repository
gh repo create my-project --public --clone

# Fork a repository
gh repo fork owner/repo

# View repository settings
gh repo view --web
```

**For AI Agents:**
- Clone repositories for analysis or contribution
- Create new repositories with proper structure
- Fork repositories for experimentation

### Branch and Commit Operations

**Branch Management:**
```bash
# List branches
gh repo view --json defaultBranchRef

# Create branch from issue
gh issue develop <number> --branch feature/issue-123
```

**Browse GitHub Resources:**
```bash
# Open current PR in browser
gh pr view --web

# Open current issue in browser
gh issue view --web

# Open repository in browser
gh repo view --web
```

### Search and Discovery

**Search Capabilities:**
```bash
# Search code
gh search code "function authenticate"

# Search repositories
gh search repos "react typescript"

# Search issues
gh search issues "bug login"

# Search pull requests
gh search prs "is:open author:@me"
```

**For AI Agents:**
- Search for similar implementations before creating new code
- Find existing issues or PRs related to current work
- Discover patterns and best practices from other repositories

### API Access

**Direct API Calls:**
```bash
# Make authenticated API calls
gh api repos/:owner/:repo/pulls

# Get specific data
gh api repos/:owner/:repo/pulls/123 --jq '.title, .body'

# POST requests
gh api repos/:owner/:repo/issues -X POST -f title="New Issue" -f body="Description"
```

**For AI Agents:**
- Access GitHub API for advanced operations not covered by CLI commands
- Retrieve detailed data in JSON format for processing
- Perform bulk operations efficiently

### Workflow Automation Examples

**Complete Feature Workflow:**
```bash
# 1. Create and checkout feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: implement new feature"

# 3. Push branch
git push -u origin feature/new-feature

# 4. Create PR
gh pr create --title "feat: implement new feature" --body "Description" --draft

# 5. Wait for CI checks
gh pr checks --watch

# 6. After approval, merge
gh pr merge --squash --delete-branch
```

**For AI Agents:**
- Automate the complete PR workflow from branch creation to merge
- Monitor CI checks and retry failed workflows
- Update PR descriptions with analysis or documentation
- Clean up branches after merge

### Best Practices for AI Agents

1. **Always authenticate first**: Check `gh auth status` before operations
2. **Use appropriate PR flags**: Use `--draft` for work-in-progress, `--fill` to auto-populate from commits
3. **Monitor CI checks**: Use `gh pr checks --watch` to wait for checks to complete
4. **Provide context**: Always include meaningful titles and descriptions
5. **Link related items**: Reference issues in PR descriptions with `Closes #123`
6. **Handle errors gracefully**: Check command exit codes and provide helpful error messages
7. **Respect rate limits**: Implement delays for bulk operations
8. **Use JSON output**: Use `--json` flag for programmatic processing

---

## Additional Resources

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Lefthook Documentation](https://github.com/evilmartians/lefthook)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

---

## Notes

- This document should be reviewed and updated regularly as best practices evolve
- Team-specific additions and modifications are encouraged
- When in doubt, refer to official documentation and community standards

