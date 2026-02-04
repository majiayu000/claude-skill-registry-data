---
name: comprehensive-issue-analyzer
description: Fetches ALL open issues from any GitHub repository using pagination and generates a comprehensive analysis including category breakdown, age distribution, stale issues (30+ days), top discussed issues, prioritization, and detailed recommendations for triage. Handles large repositories (5000+ issues) efficiently.
---

# Comprehensive Issue Analyzer

## Instructions

This skill performs a complete analysis of ALL open issues in a GitHub repository, regardless of size. Unlike basic analyzers that only fetch recent issues, this skill uses pagination to retrieve the entire open issue dataset and provides in-depth statistical analysis.

### Usage

1. Import the analyzer function
2. Call it with a repository owner and name
3. The function fetches ALL pages of open issues (100 per page)
4. Generates comprehensive report with multiple analysis dimensions
5. Saves both raw data and formatted report to `./workspace/`

### Features

- **Complete Dataset Retrieval**: Fetches ALL open issues using pagination (handles 5000+ issues)
- **Multi-Dimensional Analysis**:
  - Category breakdown by labels with percentages
  - Age distribution (< 1 week, < 1 month, < 3 months, > 3 months)
  - Activity analysis (top 10 most discussed issues)
  - Temporal analysis (top 10 oldest and newest issues)
  - Stale issue detection (no activity in 30+ days)
- **Intelligent Prioritization**:
  - CRITICAL: Open bugs with >5 comments
  - HIGH: Open bugs OR issues with >3 comments
  - MEDIUM: Enhancements with recent activity (< 14 days)
  - LOW: Other active issues
  - STALE: No activity in 30+ days
- **Actionable Recommendations**: Concrete triage priorities and process improvements

### Priority Logic

The analyzer uses sophisticated multi-factor prioritization:

1. **CRITICAL** - Bugs with high community engagement (>5 comments)
   - Likely impacts multiple users
   - Requires immediate attention

2. **HIGH** - Bugs OR issues with >3 comments
   - Active discussion indicates importance
   - May include feature requests with strong support

3. **MEDIUM** - Enhancements updated in last 14 days
   - Recent feature requests with ongoing interest
   - Good candidates for roadmap planning

4. **LOW** - Other active issues
   - Less urgent but still relevant

5. **STALE** - No updates in 30+ days
   - Candidates for closure or status updates
   - May need community re-engagement

## Examples

```typescript
import { analyzeAllIssues } from './.claude/skills/comprehensive-issue-analyzer/implementation';

// Analyze all open issues in a repository
const report = await analyzeAllIssues('anthropics', 'claude-code');

// The function returns analysis results and saves:
// - ./workspace/{repo}-issues.json (raw data, may be large)
// - ./workspace/{repo}-issue-report.md (formatted markdown report)
```

## Output Files

The skill automatically saves:
- `./workspace/{repo}-issues.json` - Complete raw issue data (all pages fetched)
- `./workspace/{repo}-issue-report.md` - Formatted markdown report with:
  - Executive summary
  - Category breakdown
  - Priority summary
  - Age distribution
  - Top 10 most discussed issues
  - Top 10 oldest open issues
  - Top 10 newest issues
  - Stale issues analysis
  - Critical priority issues
  - Triage recommendations

## Performance

- Handles repositories with 5000+ open issues
- Fetches 100 issues per page
- Includes safety limit (100 pages max = 10,000 issues)
- Typical runtime: 2-5 minutes for large repositories
- Progress logging shows page fetching in real-time

## Dependencies

- MCP Tool: `list_issues` from GitHub server
- Uses GraphQL pagination with cursor-based navigation

## Changelog

- 2025-11-18: Initial version - comprehensive analysis of anthropics/claude-code (5,205 issues)
