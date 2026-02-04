---
name: pr-address-feedback
description: "Workflow for addressing review feedback on your pull requests. Use when YOUR PR has been reviewed and you need to respond to comments with fixup commits."
---

# Handling Pull Request Review Feedback

When the user asks you to address review feedback on a PR, follow these systematic steps:

## 0. Prerequisites Check

Before starting, verify the environment is ready:

```bash
# Check git status is clean (or only has expected changes)
git status

# Ensure you're on the correct branch
git branch --show-current

# Check if branch is up to date with remote
git fetch && git status

# Verify gh CLI is authenticated
gh auth status
```

## 1. Reading Review Comments

Use the GitHub CLI to fetch ALL review comments and feedback:

```bash
# List PRs for current branch (repo name = folder name, usually)
gh pr list --head <branch-name>

# Get comprehensive PR details including all comments and reviews
gh pr view <PR-number> --json title,body,comments,reviews,reviewRequests,commits

# Get PR review comments (line-specific comments)
gh api repos/Lundalogik/<repo-name>/pulls/<PR-number>/comments

# Get formatted PR view
gh pr view <PR-number>
```

**Important:** All repos are in the `Lundalogik` organization. The repo name is generally the same as the folder name, with exceptions like `limeclient.js` repo cloned into `lime-client` folder. When in doubt, ASK the user.

## 2. Address Feedback Systematically

**One Issue Per Commit:**
- Address review feedback ONE item at a time
- Create separate fixup commits for each distinct issue
- This makes the review process clear and traceable

**Important:** Before making any changes, consider if the feedback is correct! If you disagree with the feedback, explain why and ask the user what to do.

**Use Fixup Commits:**
```bash
# Make your changes to address the feedback
git add <files>

# Create fixup commit targeting the relevant original commit
git commit -m "fixup! <original-commit-subject>

<description of what was fixed>

Addresses review feedback from @<reviewer>"
```

**Fixup Commit Format:**
- Subject: `fixup! <original-commit-subject>`
- Body: Clear description of what was changed (always include this)
- Footer: `Addresses review feedback from @<reviewer>`

**CRITICAL - NEVER AUTO-SQUASH:**
- ❌ DO NOT use `git rebase -i --autosquash`
- ❌ DO NOT squash fixup commits automatically
- ❌ DO NOT use `git commit --amend` to add changes to existing commits
- ✅ Fixup commits MUST remain as separate commits during review
- ✅ You MAY use `git rebase -i --no-autosquash` to reorder commits if needed
- ✅ Only squash commits if the user EXPLICITLY requests it

**Why:** Keeping fixup commits separate preserves the review trail, allowing reviewers to see exactly what changed in response to their feedback.

## 3. Responding to Review Comments

**ALWAYS ASK PERMISSION FIRST:**
Before posting any replies to review comments, ASK the user:
- "Should I post replies to the review comments?"
- "Do you want me to respond to @reviewer's feedback?"
- "I've addressed N comments. Should I post replies to all of them?"

**Response Format:**
When given permission, post threaded replies using the GitHub API.

**IMPORTANT - Correct API Endpoint:**
- ✅ **CORRECT:** Use the PR comments collection endpoint with `in_reply_to` parameter
- ❌ **WRONG:** Do NOT try to POST to the individual comment endpoint

**Correct command format:**
```bash
# Get repo owner and name from PR URL or assume Lundalogik/<repo-name>
gh api repos/<owner>/<repo-name>/pulls/<PR-number>/comments -X POST \
  -f body="⚡️ <commit-hash>" \
  -F in_reply_to=<comment-id>
```

**Example:**
```bash
# For PR #153 on jgroth/kompendium, replying to comment 2568687596
gh api repos/jgroth/kompendium/pulls/153/comments -X POST \
  -f body="⚡️ 59a0220" \
  -F in_reply_to=2568687596
```

**Common mistake to avoid:**
```bash
# ❌ WRONG - This will fail with "in_reply_to is not a permitted key"
gh api repos/owner/repo/pulls/comments/2568687596 -X POST \
  -f body="⚡️ 59a0220" \
  -F in_reply_to=2568687596
```

**Notes:**
- Use the ⚡️ (zap) emoji to indicate feedback has been addressed, followed by the relevant fixup commit hash
- The `-f` flag is shorthand for `--field` (both work)
- The `-F` flag is for integer/number fields like `in_reply_to`
- For non-Lundalogik repos, extract owner and repo name from the PR URL

**Track which comments need replies:**
```bash
# List all review comments with their IDs
gh api repos/<owner>/<repo-name>/pulls/<PR-number>/comments | \
  jq '.[] | {id, body, path, line}'
```

## 4. Verify and Push

After creating all fixup commits:

```bash
# Run linting with auto-fix
# For TypeScript projects or frontend/ folders:
lintf

# For Python projects using black/isort/flake8:
lintpy

# For Python projects using ruff:
lintruff

# Run tests locally
npm test  # or pytest, or appropriate test command

# If tests and linting pass, push changes to remote
git push
```

**Note:** Always run linting and tests BEFORE pushing to catch issues early.

## 5. Complete Workflow Example

1. **Check prerequisites:** Verify git status, branch, and gh auth
2. **Read feedback:** `gh pr view 63 --json comments,reviews`
3. **Address issues one by one:** Create SEPARATE fixup commits for each item
4. **Verify changes:** Run linting and tests
5. **Push to remote:** `git push`
6. **Ask permission:** "Should I post replies to indicate the feedback has been addressed?"
7. **Post responses:** Use the format `⚡️ commit-hash` where `commit-hash` is the hash of the fixup commit that addresses the feedback in the specific comment.
8. **Summarize:** Provide overview of all changes made

## 6. Best Practices

- **Be systematic:** Don't batch unrelated fixes into one commit
- **Be specific:** Reference exact reviewer suggestions in commit messages
- **Be communicative:** Clear commit messages help reviewers understand changes
- **Be respectful:** Always ask before posting comments on behalf of the user
- **Be thorough:** Address ALL feedback items, don't miss any
- **Never auto-squash:** Keep fixup commits separate during review
- **Verify before pushing:** Run linting and tests to catch issues early

## 7. Troubleshooting

**Branch diverged from remote:**
```bash
# Rebase to sync with remote (preserves fixup commits)
git pull --rebase origin <branch-name>
```

**Need to modify the last fixup commit:**
```bash
# Only if explicitly requested by user
git add <files>
git commit --amend --no-edit
git push --force-with-lease
```

**Linting or tests fail:**
- Fix the issues before pushing
- Create additional fixup commits if needed
- Never push broken code

**Check if comment is outdated:**
- Review comments may be on old line numbers after changes
- Verify the comment still applies to current code
- Ask user if unclear whether feedback is still relevant

## 8. Repository Information

**For Lundalogik Organization:**
- **Organization:** `Lundalogik`
- **Repo naming:** Usually matches folder name (e.g., `aws-bedrock-gateway`)
- **Exception:** `limeclient.js` repo is in `lime-client` folder
- **When uncertain:** Ask the user for clarification

**For Non-Lundalogik Repos:**
When working with PRs on repos outside the Lundalogik organization:
1. Extract the owner and repo name from the PR URL
   - Example: `https://github.com/jgroth/kompendium/pull/153` → owner: `jgroth`, repo: `kompendium`
2. Use these in your `gh api` commands
3. The workflow remains the same, just substitute the correct owner/repo in API calls
