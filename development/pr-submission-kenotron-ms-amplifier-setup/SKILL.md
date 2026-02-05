---
name: pr-submission
description: Automatically submit pull requests with full autonomous workflow. Use when the user mentions creating a PR, submitting a PR, merging changes, opening a pull request, or wants to get their changes reviewed. Also use when code changes are complete and ready for review.
---

# PR Submission Skill

This skill automatically triggers the `/submit-pr` command to handle the complete pull request lifecycle autonomously.

## When to use this skill

Use this skill when the user:
- Says "create a PR" or "submit a PR"
- Says "open a pull request" or "make a pull request"
- Says "merge this" or "merge my changes"
- Says "ready for review" or "get this reviewed"
- Mentions wanting to push changes upstream
- Asks about submitting code for review
- Has completed work and wants to submit it

## What this skill does

When activated, this skill invokes the `/submit-pr` command, which:

1. **Automatically creates a feature branch** (if on main/master)
2. **Commits any uncommitted changes** with smart commit messages
3. **Ensures documentation compliance** by discovering and following repository standards
4. **Pushes changes to remote**
5. **Creates the pull request** with proper title and description
6. **Enables GitHub auto-merge** immediately
7. **Continuously monitors** CI/CD checks and review status (every 30 seconds)
8. **Autonomously fixes issues** if CI fails or changes are requested (up to 3 attempts)
9. **Waits for GitHub to auto-merge** when approved and checks pass
10. **Cleans up local branches** automatically

## Instructions

When the user requests creating or submitting a PR:

1. **Trigger the command immediately**:
   ```
   /git:submit-pr
   ```

2. **Do NOT ask for confirmation** - the command is fully autonomous and handles everything

3. **Inform the user** that the process has started:
   ```
   Starting fully autonomous PR submission workflow...
   This will handle everything from commit to merge automatically.
   ```

4. **Let the command run** - it will:
   - Show progress updates automatically
   - Handle any issues that arise
   - Merge when ready
   - Report completion

## Examples

**User**: "Create a PR for these changes"
**Action**: Immediately run `/git:submit-pr`

**User**: "Let's merge this"
**Action**: Immediately run `/git:submit-pr`

**User**: "Submit this for review"
**Action**: Immediately run `/git:submit-pr`

**User**: "I'm done, can you open a pull request?"
**Action**: Immediately run `/git:submit-pr`

**User**: "Ready to push this upstream"
**Action**: Immediately run `/git:submit-pr`

## Important notes

- **Fully autonomous**: No user interaction needed once triggered
- **Zero confirmations**: The command handles everything automatically
- **Handles failures**: Automatically fixes CI failures and addresses review feedback
- **Complete lifecycle**: From uncommitted changes to merged PR
- **Project directory aware**: Uses PROJECT_DIR environment variable if set

## What NOT to do

- ❌ Don't ask "Would you like me to create a PR?"
- ❌ Don't ask for confirmation before running the command
- ❌ Don't try to manually do the git operations yourself
- ❌ Don't suggest running git commands separately

✅ **Just trigger `/git:submit-pr` immediately**

## Fallback

If the `/git:submit-pr` command fails or is not available:
1. Inform the user about the error
2. Guide them to check that the git plugin is properly installed
3. Provide the manual steps only if the command is unavailable
