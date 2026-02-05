---
name: squash-commits
description: Squash all commits in a feature branch into a single commit with an AI-generated summary message. Use when the user wants to clean up their git history before merging, combine multiple commits, or create a single commit from a feature branch.
allowed-tools: Bash, AskUserQuestion
---

# Squash Git Commits

Squash all commits in a feature branch into a single commit with a well-structured, AI-generated commit message.

## Instructions

### Step 1 - Safety Checks

First, perform these safety checks:

1. **Check for uncommitted changes:**
   ```bash
   git status
   ```
   - If there are uncommitted changes, inform the user and STOP
   - Suggest they commit or stash changes before proceeding

2. **Get current branch name:**
   ```bash
   git branch --show-current
   ```
   - Store this for later use

3. **Create backup branch:**
   ```bash
   git branch backup/<current-branch-name>-$(date +%Y%m%d-%H%M%S)
   ```
   - Inform the user that a backup branch has been created for safety

### Step 2 - Detect Base Branch

Auto-detect the base branch by checking which exists (in priority order):
1. `main`
2. `master`
3. `develop`

Check each with:
```bash
git rev-parse --verify <branch-name> 2>/dev/null
```

If none exist, ask the user to specify the base branch.

### Step 3 - Determine Commit Type from Branch Name

Parse the current branch name to determine the commit type prefix:

**Priority 1: JIRA Ticket Pattern**
- Pattern: `<prefix>/<TICKET-NUMBER>` or `<prefix>/<TICKET-NUMBER>-description`
- Examples: `feature/TVFUS-12345`, `fix/JIRA-999-bug-fix`
- Regex pattern: `^(feature|chore|fix)/([A-Z]+-\d+)`
- **Commit type:** Use the ticket number (e.g., `TVFUS-12345:`)

**Priority 2: Branch Prefix Mapping**
- `feature/` → `feat:`
- `chore/` → `chore:`
- `fix/` → `fix:`

**Fallback:**
- If no pattern matches, ask the user what commit type to use

### Step 4 - Analyze Changes

Gather comprehensive information about all changes:

1. **Get commit history:**
   ```bash
   git log <base-branch>..HEAD --oneline
   git log <base-branch>..HEAD --format="%B"
   ```

2. **Get code changes:**
   ```bash
   git diff <base-branch>...HEAD --stat
   git diff <base-branch>...HEAD
   ```

3. **Analyze the changes:**
   - Review both commit messages AND the actual code diff
   - Identify **functional changes** (what the code does differently)
   - Focus on:
     - User-facing changes
     - New features or capabilities
     - Bug fixes and their impact
     - Refactoring and improvements
     - Configuration or dependency changes
   - **DO NOT** just list commit messages - synthesize the actual functional impact

### Step 5 - Generate Commit Message

Create a commit message in this **exact format**:

```
<commit-type>: A brief summary line of the change

- functional change 1
- functional change 2
- functional change 3
```

**Guidelines:**

- **First line (summary):**
  - Concise summary (ideally under 72 characters)
  - Captures the overall purpose of the changes
  - Use imperative mood (e.g., "Add feature" not "Added feature")

- **Blank line:** Required separator between summary and body

- **Body (bullet points):**
  - Each bullet describes ONE functional change
  - Describe WHAT changed functionally, not implementation details
  - Focus on user-visible or behavioral changes
  - Be concise but descriptive
  - Use imperative mood and present tense

**Example:**
```
feat: Add user profile management

- Add user profile page with editable fields
- Implement avatar upload functionality
- Add email verification workflow
- Include profile deletion with confirmation dialog
```

**Example with JIRA ticket:**
```
TVFUS-12345: Implement shopping cart feature

- Add cart UI with item list and quantity controls
- Implement cart persistence across sessions
- Add checkout button with price calculation
- Include empty cart state with call-to-action
```

### Step 6 - Present for Approval by User

Show the user:
- The generated commit message (in a code block for easy review)
- Number of commits that will be squashed
- The base branch being used
- Reminder that a backup branch was created

Use the AskUserQuestion tool to present choices to proceed:

Question: Proceed with this commit message?

1. Yes
3. Edit the message? (if yes, ask for the edited version)
2. No, cancel

**DO NOT** proceed without the confirmation by the user.

### Step 7 - Execute Squash (Only After Approval by User)

Once the user approves the commit message:

1. **Perform the squash:**
   ```bash
   git reset --soft <base-branch>
   git commit -m "<approved-message>"
   ```

   Note: Use a heredoc for multi-line messages:
   ```bash
   git commit -m "$(cat <<'EOF'
   <approved-message>
   EOF
   )"
   ```

2. **Verify success:**
   ```bash
   git log --oneline -5
   ```

3. **Inform the user:**
   - Squash completed successfully
   - Show the new commit hash and message
   - Ask the user if the backup branch should be deleted now

## Important Rules

- **DO NOT** push to remote automatically - let the user decide
- **DO NOT** proceed if there are uncommitted changes
- **ALWAYS** create a backup branch before squashing
- **ALWAYS** wait for user approval before executing the squash
- **ALWAYS** use heredoc format for multi-line commit messages
- Focus on **functional changes** in the commit body, not implementation details

## Error Handling

If any command fails:
- Show the error message to the user
- Explain what went wrong in plain language
- Suggest recovery steps
- **DO NOT** proceed with the squash if there are errors
- Remind them that the backup branch exists if they need to recover

## Examples

### Example 1: Feature branch with JIRA ticket
```
Branch: feature/TVFUS-12345-user-auth
Base: main
Commits: 8

Generated message:
TVFUS-12345: Add user authentication system

- Add login and registration forms
- Implement JWT-based authentication
- Add password reset functionality
- Include session management with auto-refresh
```

### Example 2: Simple fix branch
```
Branch: fix/navbar-mobile
Base: main
Commits: 3

Generated message:
fix: Resolve navigation menu issues on mobile

- Fix hamburger menu not closing after selection
- Correct menu positioning on small screens
- Add smooth scroll behavior to anchor links
```
