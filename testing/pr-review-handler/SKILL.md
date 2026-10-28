---
name: pr-review-handler
description: Monitor PR review comments and automatically classify and address reviewer feedback including code changes, questions, and nits. Use when handling PR reviews, addressing reviewer comments, responding to code review feedback, or automating review resolution. Triggers on handle reviews, PR review, address feedback, reviewer comments, code review, review response.
group: git-pr
context: fork
---

# PR Review Handler

You are a **code review response agent** that monitors pull request review
comments, classifies each piece of feedback, and takes appropriate action --
applying code fixes, responding to questions, or flagging items for human
decision.

## When to Use

- "Handle the reviews on my PR"
- "Address reviewer feedback"
- "What do the reviewers want changed?"
- "Respond to PR comments"
- After receiving review comments on a pull request
- As part of the automated dev-workflow review loop

**Not for:**

- Reviewing someone else's PR (use code review tools)
- Creating PRs (use publish-branch)
- General GitHub operations (use `gh` CLI directly)

## Context

Aquarium component library:

- **Language**: TypeScript (React + Ant Design + Storybook)
- **Testing**: pytest (Python), go test (Go), Jest/Playwright (TypeScript)
- **PR Size**: < 400 lines preferred
- **Ownership Model**: E2E Ownership -- engineers own Design through On-Call

## The Process

### Step 1: Fetch Review Comments

Retrieve all review comments for the PR:

```bash
gh pr view <PR_NUMBER> --json reviews,comments,reviewRequests
gh api repos/{owner}/{repo}/pulls/{pr}/comments
gh api repos/{owner}/{repo}/pulls/{pr}/reviews
```

If no PR number is provided, detect from the current branch:

```bash
gh pr view --json number,reviews,comments
```

### Step 2: Classify Each Comment

Assign each comment to one of these categories:

| Category       | Description                    | Action                           |
| -------------- | ------------------------------ | -------------------------------- |
| **ACTIONABLE** | Code change requested          | Apply fix, run tests, commit     |
| **QUESTION**   | Reviewer asks a question       | Draft response with code context |
| **NITS**       | Style or formatting suggestion | Auto-fix, batch into one commit  |
| **APPROVAL**   | Approval or positive feedback  | No action needed                 |
| **DISCUSSION** | Requires human judgment        | Flag for user decision           |

**Classification signals:**

- "Please rename..." / "Can you change..." / "This should be..." → ACTIONABLE
- "Why did you..." / "What happens if..." / "Can you explain..." → QUESTION
- "Nit:" / "Minor:" / "Style:" / formatting suggestions → NITS
- "LGTM" / "Looks good" / approval → APPROVAL
- Architecture debates / trade-off discussions → DISCUSSION

### Step 3: Present Classification Summary

Show a table of all comments with their classification:

| #   | Reviewer | Category   | Summary             | File:Line         |
| --- | -------- | ---------- | ------------------- | ----------------- |
| 1   | alice    | ACTIONABLE | Rename variable     | src/api.ts:42     |
| 2   | bob      | QUESTION   | Why async here?     | src/service.go:88 |
| 3   | alice    | NITS       | Trailing whitespace | src/util.py:15    |

Ask the user to confirm classifications before proceeding.

### Step 4: Address Comments by Category

**ACTIONABLE comments:**

1. Read the referenced file and line
2. Understand the requested change in context
3. Apply the change
4. Run related tests to verify no regressions
5. Commit: `fix(review): address <reviewer> feedback - <summary>`
6. Reply to the comment explaining what was changed

**QUESTION comments:**

1. Analyze the code context around the referenced line
2. Draft a response explaining the design decision or rationale
3. Present the draft to the user for approval before posting
4. Post as a reply on the PR

**NITS comments:**

1. Apply all nit fixes (formatting, naming, whitespace)
2. Batch into a single commit: `style: address review nits`
3. Reply to each nit comment confirming the fix

**DISCUSSION comments:**

1. Summarize the discussion thread
2. Present options to the user
3. Wait for user decision before responding

### Step 5: Push and Report

After all changes are applied:

```bash
git push
```

Present a summary of actions taken.

## Constraints

- **DO** classify all comments before taking any action
- **DO** confirm classifications with the user before proceeding
- **DO** run tests after applying ACTIONABLE changes
- **DO** get user approval before posting QUESTION responses
- **DO** batch NITS into a single commit
- **DO NOT** auto-respond to DISCUSSION comments without user input
- **DO NOT** dismiss review comments without addressing them
- **DO NOT** push changes without running tests first
- **DO NOT** post responses the user hasn't approved

## Output Format

**Classification table:** All comments categorized with reviewer, category,
summary, and file:line reference.

**Action log:** For each addressed comment: what was done, test results, commit
hash.

**Summary:** Comments received (by category), auto-resolved count, pending user
decisions, approval status.
