---
name: pr-review-checker
description: Check PR review comments and feedback from CodeRabbit and human reviewers. Use when user asks about reviews, unresolved comments, CodeRabbit feedback, Claude review, or PR status.
allowed-tools: Bash, Read, Grep
---

# PR Review Checker Skill

## Purpose

Automatically fetch and summarize PR review comments when the user asks about review status, unresolved feedback, or what reviewers said. This is a read-only skill.

## When Claude Should Use This

- User asks "any review comments?"
- User asks "what did CodeRabbit say?"
- User asks "unresolved comments on PR #X"
- User asks "check PR feedback"
- User asks "is PR #X approved?"
- User mentions reviewing or addressing feedback

## Instructions

### Get PR Review Status

```bash
gh pr view <number> --json reviews,reviewDecision,state
```

### Get Review Comments (Inline)

```bash
gh api repos/rollercoaster-dev/monorepo/pulls/<number>/comments
```

### Get Issue Comments (Includes CodeRabbit/Claude)

```bash
gh api repos/rollercoaster-dev/monorepo/issues/<number>/comments
```

### Identify Reviewers

- `coderabbitai[bot]` - CodeRabbit AI review
- `claude[bot]` - Claude Code review
- Other usernames - Human reviewers

## Parsing CodeRabbit Reviews

CodeRabbit reviews typically include:

- **Walkthrough** - Summary of changes
- **Actionable Comments** - Issues to address (look for severity indicators)
- **Pre-merge Checks** - Title, description, linked issues checks

Look for these patterns:

- `_Potential issue_` or red indicators = Critical
- `_Nitpick_` = Optional/Low priority
- Checkmarks = Approvals

## Output Format

```markdown
## PR #X Review Status

**CodeRabbit:** Reviewed (Approved/Changes Requested)
**Claude:** Reviewed/Not triggered
**Human Reviews:** <count>

### Actionable Items

| #   | File            | Issue       | Severity | Status     |
| --- | --------------- | ----------- | -------- | ---------- |
| 1   | path/file.ts:42 | Description | Critical | Unresolved |

### Summary

- <n> critical issues
- <n> suggestions
- <n> approvals
```

## Repository Context

- Owner: `rollercoaster-dev`
- Repo: `monorepo`
