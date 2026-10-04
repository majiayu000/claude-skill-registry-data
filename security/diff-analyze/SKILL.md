---
name: diff-analyze
description: Analyze git diffs for risk scoring, reviewer recommendations, and change classification
argument-hint: "[--branch BRANCH] [--pr PR#]"
allowed-tools: mcp__claude-flow__analyze_diff mcp__claude-flow__analyze_diff-risk mcp__claude-flow__analyze_diff-classify mcp__claude-flow__analyze_diff-reviewers mcp__claude-flow__analyze_diff-stats mcp__claude-flow__analyze_file-risk Bash
---

# Diff Analysis

Analyze git diffs for risk, complexity, and reviewer assignment.

## When to use

Before submitting a PR or after making significant changes, analyze the diff to understand risk level, get reviewer recommendations, and classify the type of change.

## Steps

1. **Analyze diff** — call `mcp__claude-flow__analyze_diff` with the diff content for a comprehensive analysis
2. **Risk score** — call `mcp__claude-flow__analyze_diff-risk` for a quantified risk assessment
3. **Classify changes** — call `mcp__claude-flow__analyze_diff-classify` to categorize (feature, bugfix, refactor, etc.)
4. **Get reviewers** — call `mcp__claude-flow__analyze_diff-reviewers` for recommended reviewers based on code ownership
5. **Diff stats** — call `mcp__claude-flow__analyze_diff-stats` for line counts, file counts, complexity metrics
6. **File-level risk** — call `mcp__claude-flow__analyze_file-risk` for per-file risk breakdown

## Risk factors

- Files with high churn history
- Security-sensitive paths (auth, crypto, permissions)
- Large diffs (>500 lines)
- Cross-module changes
- Database migration files
