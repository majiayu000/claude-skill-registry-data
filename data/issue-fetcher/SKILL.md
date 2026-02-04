---
name: issue-fetcher
description: Fetch and analyze GitHub issues from the monorepo. Use when user asks about issues, what's blocking, issue status, dependencies, or wants to see issue details.
allowed-tools: Bash, Read, Grep, Glob
---

# Issue Fetcher Skill

## Purpose

Automatically fetch and summarize GitHub issues when the user asks about issue status, blockers, or dependencies. This is a read-only skill for information gathering.

## When Claude Should Use This

- User asks "show me issue #X"
- User asks "what's blocking?"
- User asks "what issues are open?"
- User asks "what depends on this?"
- User mentions issue numbers in context
- User asks about sprint/milestone progress

## Instructions

### Fetch Single Issue

```bash
gh issue view <number> --json title,body,state,labels,milestone,assignees
```

### List Issues

```bash
# All open issues
gh issue list --state open

# By milestone
gh issue list --milestone "OpenBadges Badge Generator"

# By label
gh issue list --label "type:feature"
```

### Check Dependencies

Look for "depends on", "blocks", "after #X" in issue bodies:

```bash
gh issue view <number> --json body | jq -r '.body'
```

## Output Format

Summarize findings clearly:

```markdown
## Issue #X: <title>

**Status:** Open/Closed
**Labels:** label1, label2
**Milestone:** <milestone>

**Summary:** <1-2 sentence description>

**Dependencies:**

- Depends on: #Y, #Z
- Blocks: #A, #B
```

## Repository Context

- Owner: `rollercoaster-dev`
- Repo: `monorepo`
- Project Board: #11 "Monorepo Development"
