---
name: gh
description: GitHub operations using gh CLI for any repository. Use when the user asks to "create pr", "create pull request", "view pr", "check ci", "pr status", "list prs", "create issue", "view issue", "search code", or any other GitHub-related operations. Handles PR creation with proper base branch detection, template support, and project conventions.
user-invocable: true
model: haiku
trigger:
  - pull request
  - create pr
  - create pull request
  - make pull request
  - make a pr
  - open pull request
  - open a pr
  - github pr
  - check ci
  - pr status
  - view pr
  - list prs
  - show prs
  - my prs
  - pr checks
  - create issue
  - github issue
  - view issue
  - list issues
  - search code
  - search repo
  - repository search
---

# GitHub Operations

Manage GitHub workflows using the `gh` CLI.

## When to Use This Skill

Use this skill when the user asks to:
- Create a pull request
- View PR details or status
- Check CI/CD pipeline status
- Manage issues
- Review PR comments
- Search repository code or issues

## Commands

### Create Pull Request

When creating a PR:

1. **Verify current branch and changes:**
   ```bash
   git branch --show-current
   git status
   ```

2. **Check if branch is pushed:**
   ```bash
   git log @{u}.. 2>/dev/null || echo "Branch not pushed"
   ```

3. **Push if needed:**
   ```bash
   git push -u origin $(git branch --show-current)
   ```

4. **Detect parent branch (if base not specified):**

   Find the parent branch from which the current branch was created:
   ```bash
   PARENT_BRANCH=$(git show-branch -a 2>/dev/null | grep '\*' | grep -v "$(git rev-parse --abbrev-ref HEAD)" | head -n1 | sed 's/.*\[\(.*\)\].*/\1/' | sed 's/[\^~].*//' | sed 's/remotes\/origin\///')

   # Fall back to common default branches if detection fails
   if [ -z "$PARENT_BRANCH" ]; then
     for branch in development develop main master; do
       if git show-ref --verify --quiet refs/remotes/origin/$branch; then
         PARENT_BRANCH=$branch
         break
       fi
     done
   fi
   ```

5. **Gather change information:**

   Get commits and diff to understand the changes:
   ```bash
   # Get commit messages for this branch
   git log --oneline "$PARENT_BRANCH"..HEAD

   # Get the diff summary (files changed)
   git diff --stat "$PARENT_BRANCH"..HEAD

   # Get the full diff for detailed analysis
   git diff "$PARENT_BRANCH"..HEAD
   ```

6. **Create PR with filled template:**

   Read the template:
   ```bash
   cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || echo "No template found"
   ```

   This repo has a template, so the filled-body path below is the one that applies.
   Only if the template is genuinely missing, fall back to `--web` (see below).

  - Analyze the commits and diff from step 5
  - Fill in each section of the template with relevant information based on the actual changes
  - Keep every section label (`**Jira issue:**`, `**What was solved?**`, `**Additional info:**`, `**Screenshots:**`) and the `Additional info` checklist verbatim and in order — they are bold labels, not markdown headings; do not convert them
  - Leave checklist boxes unchecked; they are the author's to confirm
  - Create the PR using `--body` with a heredoc containing the filled template:
   ```bash
   gh pr create --title "Brief title (under 70 chars)" --base "$PARENT_BRANCH" --body "$(cat <<'EOF'
   [Filled template content here based on actual changes]
   EOF
   )"
   ```

   **If no template exists** (does not happen in this repo), open the browser for a
   manual description instead:
   ```bash
   gh pr create --title "Brief title (under 70 chars)" --base "$PARENT_BRANCH" --web
   ```
   Note what `--web` costs: it does not create the PR, only opens the compare page.
   It prints nothing in a non-TTY run, so no URL comes back, and it is rejected
   outright with `--draft`, `--reviewer`, and `--dry-run` — so it cannot open a
   draft PR.

   **Never use `--template`.** It seeds an interactive prompt only: rejected
   alongside `--body`/`--body-file`, exits 1 in a non-TTY run (`must provide
   --title and --body ... when not running interactively`), silently ignored when
   combined with `--fill`, and it matches a *remote* template filename rather than
   a local path.

   **Base branch logic**:
  - Auto-detect: Use the parent branch from which current branch was created
  - Fallback: Use common default branches if detection fails
  - Override: Use explicitly specified base branch if provided by user

7. **Display PR URL to user**

### View Pull Request

```bash
# View specific PR
gh pr view 123

# View PR in browser
gh pr view 123 --web

# List open PRs
gh pr list

# List PRs by author
gh pr list --author @me
```

### Check PR Status

```bash
# Check CI/CD status
gh pr checks 123

# View PR status
gh pr status
```

### PR Comments

```bash
# View comments on PR
gh pr view 123 --comments

# Add comment to PR
gh pr comment 123 --body "Your comment here"
```

### Issue Management

```bash
# Create issue
gh issue create --title "Issue title" --body "Issue description"

# View issue
gh issue view 456

# List open issues
gh issue list

# Search issues
gh issue list --search "keyword"
```

### Code Search

```bash
# Search code in current repository
gh search code "search term"

# Search code in specific repository
gh search code --repo owner/repo "search term"
```

### View Commits

```bash
# List recent commits on current branch
git log --oneline -10

# View specific commit
gh pr view <commit-sha>
```

## PR Best Practices

### Title Format
- Keep under 70 characters
- Use imperative mood: "Add feature" not "Added feature"
- Be specific but concise

Examples:
- ✅ "Optimize CLAUDE.md by removing general knowledge"
- ✅ "Fix memory leak in ChatController disposal"
- ✅ "Add snapshot tests for CallVisualizer UI"
- ❌ "Update files" (too vague)
- ❌ "This PR adds a new feature to handle user authentication and also fixes some bugs" (too long)

### Description Format

- Read the template at `.github/PULL_REQUEST_TEMPLATE.md`
- Analyze commits and diff to understand the changes
- Fill each template section with relevant details from the actual changes, keeping the bold section labels and the checklist verbatim
- Use `--body` with the filled template content
- If no template exists, use `--web` to open the browser for a manual description — note it does not create the PR and cannot be combined with `--draft`
- Never use `--template` - it exits 1 in a non-TTY run and is rejected alongside `--body`

### Base Branch Selection
- **Auto-detect**: Automatically use the parent branch from which the current branch was created
- **Fallback**: Use common default branches (`development`, `develop`, `main`, or `master`) if parent branch detection fails
- **Override**: Use explicitly specified base branch if the user requests it (e.g., "create PR against master")

## Error Handling

If `gh` is not authenticated:
```
Run: gh auth login
Follow browser-based OAuth flow
```

If `gh` is not installed:
```
macOS: brew install gh
Or download from: https://cli.github.com/
```

## Important Notes

- **Always use the PR template**: Read `.github/PULL_REQUEST_TEMPLATE.md`, fill its sections with change details, and pass the result via `--body`
- **Fill template with actual changes**: Analyze commits and diff, then populate each template section with relevant information
- **No template?**: Use `--web` to open the browser - it does not create the PR and rejects `--draft`
- **Never use `--template`**: It exits 1 in a non-TTY run and conflicts with `--body`
- Always verify branch is pushed before creating PR
- Check CI status before requesting review
