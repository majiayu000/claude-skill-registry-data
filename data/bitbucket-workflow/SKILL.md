---
name: bitbucket-workflow
description: Create PRs and debug pipeline failures in Bitbucket with Carefeed conventions. Auto-extracts Jira keys from branches, generates PR descriptions, and diagnoses CI failures. Use when user mentions PRs, pipelines, or CI/CD.
---

# Bitbucket Workflow Skill

This skill handles Bitbucket PR creation and pipeline debugging using Carefeed team conventions. It integrates with Jira for ticket linking and follows team standards for PR formatting.

## When to Use This Skill

Automatically trigger this skill when the user:

- Wants to **create a PR**: "Create a PR", "Open a pull request", "Submit for review"
- Mentions **pipeline issues**: "Pipeline failed", "CI is broken", "Build failed"
- Asks about **PR status**: "What's the status of my PR?", "Any comments on the PR?"
- Needs to **debug failures**: "Why did the build fail?", "What's wrong with the pipeline?"

## Part 1: Creating Pull Requests

### Prerequisites

- Current branch follows naming: `{type}/{JIRA-KEY}-{description}`
- Branch has commits ahead of target (usually `master`)
- All changes are committed

### Workflow

#### Step 1: Verify Branch State

```bash
# Check commits ahead of target
git log origin/master..HEAD --oneline | wc -l

# Verify branch name format
git rev-parse --abbrev-ref HEAD
```

#### Step 2: Extract Jira Ticket

Parse Jira key from branch name:
- `feature/CORE-3982-null-safety-fuzzy-matching` -> `CORE-3982`

Fetch ticket details:
```
mcp__jira__jira_get_issue(issueIdOrKey: "CORE-3982")
```

#### Step 3: Generate PR Description

**Carefeed PR Template:**

```markdown
## Jira Ticket
[CORE-3982](https://carefeed.atlassian.net/browse/CORE-3982)

## Summary
[Brief overview from Jira or custom text]

## Changes
* [List of key changes]

## Testing
* [How changes were tested]

## Related
* [Related PRs/issues if applicable]

Generated with [Claude Code](https://claude.com/claude-code)
```

#### Step 4: Create PR via MCP

```
mcp__bitbucket__bb_add_pr({
  repoSlug: "portal_dev",
  prTitle: "CORE-3982: Handle null facility names in fuzzy matching",
  sourceBranch: "feature/CORE-3982-null-safety-fuzzy-matching",
  destinationBranch: "master",
  description: "[Generated description]",
  closeSourceBranch: false
})
```

#### Step 5: Link to Jira

Add comment to Jira ticket:
```
mcp__jira__jira_add_comment(
  issueIdOrKey: "CORE-3982",
  commentBody: "Pull Request created: [PR #4067](pr_url)"
)
```

Optionally transition to "In Review":
```
mcp__jira__jira_transition_issue(
  issueIdOrKey: "CORE-3982",
  transitionId: "In Review"
)
```

### PR Title Format

Always include Jira key:
```
{JIRA-KEY}: {Jira issue summary}
```
Example: `CORE-3982: Handle null facility names in fuzzy matching`

### Team-Specific Practices

| Team | Requirements |
|------|--------------|
| **Core** | Tech lead approval, extra review for DB migrations |
| **Integration** | PCC staging test, document env vars |
| **Payments** | Security review, test with Stripe test mode |

---

## Part 2: Debugging Pipeline Failures

### Workflow

#### Step 1: Identify Failed Pipeline

List recent failed pipelines:
```
mcp__bitbucket__bb_list_pipelines({
  repoSlug: "portal_dev",
  state: "COMPLETED",
  result: "FAILED",
  limit: 10
})
```

Or get pipeline from PR:
```
mcp__bitbucket__bb_get_pr({
  repoSlug: "portal_dev",
  prId: "4067"
})
```

#### Step 2: Get Pipeline Overview

```
mcp__bitbucket__bb_get_pipeline({
  repoSlug: "portal_dev",
  pipelineId: "13906"
})
```

Returns:
- Build number and status
- Branch and commit
- Duration
- Result (SUCCESSFUL, FAILED, ERROR)

#### Step 3: List Pipeline Steps

```
mcp__bitbucket__bb_list_pipeline_steps({
  repoSlug: "portal_dev",
  pipelineId: "13906"
})
```

**Step Status Legend:**
- SUCCESSFUL - Step passed
- FAILED - Investigate this one
- IN_PROGRESS - Still running
- SKIPPED - Dependency failed

#### Step 4: Analyze Failure

**Note:** Bitbucket API doesn't expose step logs programmatically. You must view logs in the browser using the step URL.

**Common PHP Test Failures:**
- `Fatal error: Undefined method`
- `Failed asserting that null is...`
- `PDOException: SQLSTATE[23000]`

**Common Build Failures:**
- `composer install failed`
- `npm install failed`
- `Docker build failed`

**Common Lint Failures:**
- `PHPStan: Found X errors`
- `PHP_CodeSniffer: X violations`

#### Step 5: Correlate with Changes

Find last successful pipeline and compare:
```
mcp__bitbucket__bb_list_pipelines({
  repoSlug: "portal_dev",
  branch: "feature/CORE-3982",
  result: "SUCCESSFUL",
  limit: 1
})
```

Then diff the commits:
```bash
git diff --name-only [last-success-commit] [failed-commit]
```

#### Step 6: Suggest Fix

Match error patterns to common causes:

| Error Pattern | Likely Cause |
|---------------|--------------|
| `Undefined method X` | Missing/renamed method |
| `Failed asserting null` | Test expects value but got null |
| `SQLSTATE[23000]` | Database constraint violation |
| `composer install failed` | Dependency conflict |
| `Class not found` | Missing import/autoload |

### Pipeline Structure

```
Pipeline (build #13906)
  +-- Step 1: Build (docker, composer, npm)
  +-- Step 2: Test (phpunit, jest)
  +-- Step 3: Lint (phpstan, eslint)
  +-- Step 4: Deploy (if tests pass)
```

Steps run sequentially by default. If a step fails, subsequent steps are SKIPPED.

---

## Example Conversations

### Creating a PR

**User:** "Create a PR for this branch"

**Claude:**
```
I'll create a PR for your current branch.

Current branch: feature/CORE-3982-null-safety-fuzzy-matching
Jira ticket: CORE-3982 - Handle null facility names in fuzzy matching
Target: master (1 commit ahead)

PR Title: CORE-3982: Handle null facility names in fuzzy matching

Creating PR...

Created PR #4067: CORE-3982: Handle null facility names in fuzzy matching
https://bitbucket.org/Bitbucketpassword1/portal_dev/pull-requests/4067

Jira ticket CORE-3982 updated with PR link.
```

### Debugging a Pipeline

**User:** "Pipeline #13906 failed, can you help debug?"

**Claude:**
```
I'll investigate pipeline #13906.

Pipeline Overview:
  Build: 13906
  Result: FAILED
  Branch: feature/CORE-3982-null-safety
  Duration: 3m 32s

Pipeline Steps:
  SUCCESSFUL Build
  FAILED PHP Test  <-- This is where it failed
  SKIPPED Deploy

The PHP Test step failed. View logs at:
https://bitbucket.org/.../steps/{uuid}

Recent changes in this branch:
  - app/Services/MarketAnalytics/FacilityMatcher.php
  - tests/Unit/MarketAnalytics/FacilityMatcherTest.php

Likely cause: Test expects non-null value but code now returns null for edge case.

Would you like me to:
1. Show the specific changes to FacilityMatcher.php
2. Help fix the test
3. Run tests locally first
```

---

## Error Handling

### Branch doesn't contain Jira key
Ask user for the Jira ticket or suggest renaming the branch.

### No commits ahead of target
User needs to make changes and commit first.

### Bitbucket authentication failed
Check MCP server is running and credentials are configured.

### Pipeline not found
List recent pipelines to find the correct ID.

### Logs not accessible via API
Provide the step URL for browser access (API limitation).

---

## Anti-Patterns

- **Don't** create PRs without checking for existing open PRs on the branch
- **Don't** skip Jira ticket extraction - always link PRs to tickets
- **Don't** guess at failure causes without checking the changed files
- **Don't** assume logs are available via API - they require browser access
