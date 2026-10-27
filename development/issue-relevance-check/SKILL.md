---
name: issue-relevance-check
description: "Slash command to evaluate whether an issue or pull request is still relevant, actionable, and worth keeping open"
metadata:
  author: arisng
  version: 0.1.0
---

# Issue Relevance Check

A slash command (`/issue-relevance-check`) that evaluates whether an issue or pull request is still relevant to the project's current codebase, state, and priorities.

## Usage

Trigger the skill by commenting `/issue-relevance-check` on any issue or pull request in a repository where this skill is installed.

## Workflow

1. **Gather context** — reads the full issue/PR, checks current codebase state, reviews recent commits/PRs, and searches for duplicates.
2. **Evaluate relevance** — assesses applicability, resolution status, superseding items, staleness, and actionability.
3. **Post analysis** — returns a structured comment with verdict, evidence, and recommendation.

See [`references/evaluation-guide.md`](references/evaluation-guide.md) for the complete evaluation framework and criteria.
