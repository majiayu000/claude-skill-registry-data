---
name: review-pr
description: Review pull requests against the team's coding standards and best practices.
agent: review-pr
argument-hint: "[PR-number] [repo-name]"
pass-full-context: true
pass-conversation-history: true
---

# /review-pr

Review a pull request against the team's coding standards.

Review PR: $ARGUMENTS

## Usage

- `/review-pr 123` — review PR #123 in the current repository
- `/review-pr 123 repo-name` — review PR #123 in a specific repository

Produces a structured report with severity-ranked issues, positive aspects, and approve/request-changes recommendation.
