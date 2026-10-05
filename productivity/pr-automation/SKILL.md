---
name: pr-automation
displayName: PR Automation
tagline: Automate pull request workflows including reviews, labels, and merge strategies.
description: |
  Automates pull request lifecycle on GitHub. Auto-assigns reviewers based on
  code ownership, adds labels by file paths or PR size, enforces merge rules,
  and posts summary comments. Reduces review bottlenecks and ensures consistent
  PR hygiene across teams.
department:
  - Engineering
  - DevOps
use_cases:
  - Code Review
  - Workflow Automation
  - Developer Productivity
tools_required:
  - GitHub MCP
  - Slack MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Set up PR automation for our monorepo:
  - Auto-assign reviewers by CODEOWNERS
  - Label PRs by size (S/M/L/XL)
  - Post Slack notification for PRs waiting >24h
exampleOutput: |
  PR Automation Setup — Monorepo

  RULES CONFIGURED
  1. Reviewer Assignment: CODEOWNERS-based, 2 required
  2. Size Labels: S (<50 lines), M (50-200), L (200-500), XL (>500)
  3. Stale PR Alert: Slack #dev-alerts after 24h without review
  4. Auto-merge: Enabled for dependabot PRs with passing CI

  WEEKLY STATS
  Avg Review Time:    4.2h (was 12h)
  PRs Merged/Week:    47
  Stale PRs:          3 (down from 11)
---

# PR Automation

Automate pull request workflows including reviews, labels, and merge strategies.

**Integrations:** GitHub, Slack

## When to Use

- The user wants to streamline PR workflows in their repository
- Review bottlenecks are slowing down the team
- The user mentions "PR automation", "code review", or "merge strategy"

## Steps

### Step 1: Define PR Rules

Configure reviewer assignment, labeling, and merge policies.

### Step 2: Set Up Notifications

Configure Slack alerts for stale PRs, failed checks, and merge events.

### Step 3: Enable Auto-merge

Set conditions for automatic merging (e.g., dependabot, all checks pass).

## Output

Deliver:
- PR automation configuration
- Notification rules
- Weekly PR health metrics
