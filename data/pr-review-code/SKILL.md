---
name: pr-review-code
description: "**ALWAYS USE THIS SKILL** when asked to review a PR or given a PR URL. Provides systematic workflow for code review."
---

# Reviewing Pull Requests

When the user asks you to review someone else's PR, follow these systematic steps:

## 0. Prerequisites Check

Before starting, verify the environment is ready:

```bash
# Check git status is clean (or only has expected changes)
git status

# Ensure you're on a safe branch (not their PR branch yet)
git branch --show-current

# Verify gh CLI is authenticated
gh auth status
```

## 1. Finding the PR

Use the GitHub CLI to find and view PR details:

```bash
# List open PRs in the repository
gh pr list

# Get detailed PR information
gh pr view <PR-number>

# Get PR metadata including commits and files
gh pr view <PR-number> --json title,body,author,commits,files

# View the diff
gh pr diff <PR-number>
```

**Important:** All repos are in the `Lundalogik` organization. The repo name is generally the same as the folder name, with exceptions like `limeclient.js` repo cloned into `lime-client` folder. When in doubt, ASK the user.

## 2. Checking Out the PR Locally

Check out the PR branch to review and test it locally:

```bash
# Check out the PR branch
gh pr checkout <PR-number>

# Ensure it's up to date with the remote
git pull
```

This allows you to examine the code directly, run it, and verify behavior.

## 3. Local Verification

Review the code thoroughly, focusing on quality and security:

### Code Quality Review

- **Logic and implementation patterns**: Is the approach sound?
- **Code smells and anti-patterns**: Are there obvious issues?
- **Error handling and edge cases**: Are errors handled properly?
- **Readability and maintainability**: Is the code clear and well-structured?
- **Abstractions and separation of concerns**: Is the code properly organized?

### Security Review

- **Common vulnerabilities**: Check for SQL injection, XSS, command injection, etc.
- **Input validation and sanitization**: Is user input properly validated?
- **Authentication/authorization**: Are permissions checked correctly?
- **Secrets and credentials**: Are there any exposed secrets?
- **Data handling**: Is sensitive data handled securely?

### Nitpicks and Polish

- **Spelling mistakes**: Check variable names, comments, and strings
- **Code style**: Minor formatting or naming improvements
- **Minor optimizations**: Small improvements that aren't critical

### Optional Testing (if desired)

- You can run tests to verify functionality
- You can run linting to check style compliance
- Not required, but available for additional verification

## 4. Preparing Review Comments

### IMPORTANT - Do NOT Post Comments to GitHub

- ❌ **NEVER** use `gh pr review` to post comments directly to GitHub
- ✅ **ALWAYS** output review comments in your response to the user
- The user will manually post comments after reviewing and editing them

### Comment Format

Format your review comments as markdown in your response, organized by:

1. **Major Issues** - Blocking problems that must be addressed
2. **Minor Issues** - Important but not critical
3. **Nitpicks** - Small improvements (spelling, style, comments)
4. **Positive Aspects** - What was done well

For line-specific feedback, use this format:
- `file.ts:42` - Description of the issue with code examples

### Comment Best Practices

- **Be constructive and specific**: Explain what and why
- **Explain the "why"**: Help the author understand the reasoning
- **Offer solutions**: Don't just point out problems, suggest fixes
- **Use code examples**: Show what you mean when helpful
- **Distinguish severity**: Make it clear what's blocking vs. nice-to-have
- **Mark nitpicks**: Prefix with "Nitpick:" when the comment is minor
- **Include nitpicks**: Don't skip spelling mistakes, minor style issues, etc.
- **Be concise**: Keep feedback clear and to the point
- **Acknowledge good work**: Recognize improvements briefly when appropriate

## 5. Providing Your Recommendation

**CRITICAL - Agent's Role:**

- ❌ NEVER submit the review (approve/request changes/comment)
- ❌ NEVER post comments directly to GitHub
- ✅ Output review comments in your response for the user to review
- ✅ Provide a recommendation to the user on what action to take

**Workflow:**

1. Output all review comments as formatted markdown in your response
2. Summarize your findings
3. Provide a clear recommendation to the user
4. User will manually post the review to GitHub after reviewing/editing

**Recommendation Format:**

After outputting your review comments, provide a clear recommendation:

- "Based on the review, I recommend **requesting changes** due to [security concerns/major issues that must be addressed]"
- "Based on the review, I recommend **commenting** with suggestions that are nice-to-have but not blocking"
- "Based on the review, I recommend **approving** - the code looks good with only minor nitpicks"

**Note:** The user always has full control to edit your feedback and choose when/how to post it to GitHub.

## 6. Complete Workflow Example

Here's a complete example of the review process:

1. **Prerequisites check**: `git status` and `gh auth status`
2. **Find the PR**: `gh pr list` and `gh pr view 42`
3. **Check it out**: `gh pr checkout 42`
4. **Review locally**:
   - Examine code quality (logic, patterns, readability)
   - Check for security issues (input validation, auth, secrets)
   - Note nitpicks (spelling, minor style issues)
5. **Output review**: Format your findings as markdown and output to the user
6. **Provide recommendation**: "I recommend requesting changes due to the input validation issue in line 123"
7. **User takes over**: User manually posts the review to GitHub after reviewing/editing your feedback

**Note:** Do NOT include cleanup steps after review. Leave the PR branch checked out as-is.

## 7. Risk Assessment (Optional)

For significant changes, consider performing a formal risk assessment using the **pull-request-risk-assessment** skill. This is especially relevant for:

- Infrastructure changes (Docker, Consul, Terraform, etc.)
- Database migrations
- Changes affecting many customers
- Changes that are hard to test or verify in staging

To invoke: Use the Skill tool with `pull-request-risk-assessment`

The risk assessment helps determine if special rollout/verification/rollback plans are needed per Lime's Change Management policy.

## 8. Best Practices

- **Focus on important issues first**, but nitpicking is expected too
- **Mark nitpicks clearly**: Prefix with "Nitpick:" when appropriate
- **Spelling matters**: Do point out spelling mistakes in code (variable names, comments, etc.)
- **Be respectful and constructive**: Explain the "why" behind feedback
- **Consider context**: Understand the constraints the author was working with
- **Ask questions**: If something is unclear, ask rather than assume
- **Recognize good work**: Acknowledge improvements and good patterns, but keep it concise
- **Distinguish severity**: Make it clear what's blocking vs. nice-to-have
- **Be concise and to the point**: Clear, direct feedback is most useful

## 9. Troubleshooting

**PR has merge conflicts:**

- Note the conflicts in your review
- Suggest the author rebase on main/master
- May need to wait for conflicts to be resolved before completing review

**Can't check out PR:**

```bash
# Verify gh CLI is authenticated
gh auth status

# Check if you have uncommitted changes blocking checkout
git status

# If needed, stash changes temporarily
git stash
gh pr checkout <PR-number>
```

**Serious security issues found:**

- Flag them immediately and clearly in comments
- Mark as high-severity/blocker
- Recommend requesting changes
- Consider notifying the user directly if extremely critical

**Unsure about something:**

- Ask questions in the review comments
- Don't assume - clarify with the author
- It's better to ask than make wrong assumptions

## 10. Repository Information

- **Organization:** `Lundalogik`
- **Repo naming:** Usually matches folder name (e.g., `aws-bedrock-gateway`)
- **Exception:** `limeclient.js` repo is in `lime-client` folder
- **When uncertain:** Ask the user for clarification
