---
name: ai-adoption-dashboard-builder
displayName: AI Adoption Dashboard Builder
tagline: Generate a dashboard tracking AI tool usage, active users, top workflows, and productivity metrics.
description: |
  Creates a multi-tab analytics dashboard for tracking AI tool adoption across
  your engineering organization. Includes executive KPIs, team-level adoption
  curves, per-tool usage breakdowns, productivity impact comparisons, and cost
  tracking. Optionally generates a Grafana dashboard JSON for real-time monitoring.
department:
  - Engineering
  - AI Enablement Leaders
  - Data & Analytics
use_cases:
  - Documentation
  - Cost Optimization
  - Workflow Automation
tools_required:
  - Google Sheets MCP
  - Grafana MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  Organization: 150 engineers across 8 teams
  AI tools in use: GitHub Copilot, Cursor, Claude
  Metrics to track: Adoption rate, usage frequency, productivity impact, cost
  Data sources: GitHub API, SSO logs, billing invoices
exampleOutput: |
  AI Adoption Dashboard — February 2026

  EXECUTIVE SUMMARY
  Active Users:     112/150 (75%)  ↑ 8% from last month
  Monthly Cost:     $6,200         Budget: 78% utilized
  Time Saved:       1,840 hrs      ≈ $159,160 value
  Top Tool:         GitHub Copilot  (98 active users)

  ADOPTION BY TEAM
  Platform:     92% | Frontend:   81% | Backend:   78% | Data:   65%
  Mobile:       62% | DevOps:     58% | QA:        45% | Security: 38%

  TOP WORKFLOWS
  1. Code completion (Copilot)    — 12,400 acceptances/week
  2. Code review assist (Claude)  — 340 reviews/week
  3. Test generation (Cursor)     — 180 test files/week

  Generated: Google Sheet (6 tabs) with charts and sparklines
  Generated: Grafana dashboard JSON (4 rows, 12 panels)
---

# AI Adoption Dashboard Builder

Generate a dashboard tracking AI tool usage, active users, top workflows, and productivity metrics.

**Integrations:** Google Sheets, Grafana

## When to Use

- The user wants to track AI tool adoption across their organization
- Leadership needs a dashboard for AI usage visibility
- The user mentions "adoption dashboard", "AI metrics", or "usage tracking"
- Teams want to measure which AI tools and workflows have the most impact

## Steps

### Step 1: Define Metrics to Track

Help the user select from these metric categories:

| Category | Metrics |
|----------|---------|
| **Adoption** | Total users, active users (daily/weekly/monthly), adoption rate by team, new activations per week |
| **Usage** | Sessions per user, prompts per day, tokens consumed, tool-specific usage (Copilot completions, Claude conversations) |
| **Workflows** | Top workflows by usage, time saved per workflow, most popular skills installed |
| **Productivity** | PRs merged per developer, cycle time change, bug fix time change, code review turnaround |
| **Cost** | Cost per user, cost per team, cost trend, budget utilization percentage |

### Step 2: Identify Data Sources

Map metrics to data sources:

| Data Source | Metrics Available |
|-------------|------------------|
| GitHub/GitLab API | PRs, commits, review time, Copilot usage stats |
| AI tool admin dashboards | Seat usage, active users, token consumption |
| Jira/Linear | Ticket cycle time, story points velocity |
| SSO/IdP logs | Login frequency, tool access patterns |
| Billing data | Cost per tool, cost trends |

### Step 3: Build Google Sheets Dashboard

Create a spreadsheet with:

- **Sheet 1: Executive Summary** — High-level KPIs with sparkline charts (adoption rate, ROI, active users)
- **Sheet 2: Adoption Trends** — Weekly/monthly adoption curves by team and tool
- **Sheet 3: Usage Details** — Per-tool usage breakdown, top users, least-used tools
- **Sheet 4: Productivity Impact** — Before/after comparisons of engineering metrics
- **Sheet 5: Cost Tracking** — Budget vs actual, per-tool cost, cost per developer
- **Sheet 6: Raw Data** — Data import template with sample data format

### Step 4: Build Grafana Dashboard (Optional)

If the user has Grafana, provide dashboard JSON with:

- **Row 1: Overview** — Stat panels for total users, active today, weekly growth rate
- **Row 2: Adoption** — Time series of adoption by team, bar chart of tool popularity
- **Row 3: Productivity** — Before/after gauge panels, cycle time trend
- **Row 4: Cost** — Budget burn-down, cost per developer trend

Provide the Grafana dashboard JSON configuration and data source setup instructions.

### Step 5: Set Up Data Collection

Recommend a lightweight data collection approach:

1. **Weekly manual update** — For small teams, a simple form that team leads fill out
2. **API integration** — Scripts to pull from GitHub API, AI tool APIs
3. **Survey-based** — Monthly developer survey for qualitative metrics

Provide a sample data collection script or form template based on the user's preference.

## Output

Deliver:
- A ready-to-use Google Sheets dashboard with sample data
- Grafana dashboard JSON (if requested)
- Data collection templates or scripts
- A guide for updating the dashboard weekly/monthly
