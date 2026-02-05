---
name: github-issue-analyzer
description: Fetches issues from any GitHub repository with recent activity and generates a prioritized report by analyzing issue state, labels, and comment counts to identify high-priority bugs, enhancements, and good first issues for contributors.
---

# GitHub Issue Analyzer

## Instructions

This skill fetches GitHub issues from any repository and generates a comprehensive prioritized report. It's useful for understanding project health, identifying what needs attention, and helping new contributors find good starting issues.

### Usage

1. Import the analyzer function
2. Call it with a repository owner and name
3. Optionally specify the number of days for "recent activity" (default: 30)
4. The function returns a structured report and saves raw data to `./workspace/`

### Features

- **Automatic Categorization**: Issues are categorized into HIGH, MEDIUM, LOW priority and "Good First Issues"
- **Smart Filtering**: Identifies bugs vs enhancements, counts active discussions
- **Activity-Based Ranking**: Sorts by comment count and recency
- **Comprehensive Report**: Includes summary statistics, top 10 recommended issues, and full issue listings

### Priority Logic

- **HIGH PRIORITY**: Open bugs OR open issues with >3 comments
- **MEDIUM PRIORITY**: Open enhancements/feature requests
- **LOW PRIORITY**: Closed issues or less active items
- **GOOD FIRST ISSUES**: Issues explicitly labeled as beginner-friendly

## Examples

```typescript
import { analyzeGitHubIssues } from './.claude/skills/github-issue-analyzer/implementation';

// Basic usage - analyze last 30 days
const report = await analyzeGitHubIssues('modelcontextprotocol', 'inspector');

// Custom timeframe - analyze last 60 days
const report = await analyzeGitHubIssues('modelcontextprotocol', 'inspector', 60);

// Report includes:
// - summary statistics
// - top 10 recommended issues with explanations
// - categorized issues by priority
// - actionable insights and next steps
```

## Output Files

The skill automatically saves:
- `./workspace/all-issues.json` - Raw issue data (100 issues per page)
- `./workspace/issue-report.md` - Formatted markdown report

## Dependencies

- MCP Tool: `list_issues` from GitHub server
