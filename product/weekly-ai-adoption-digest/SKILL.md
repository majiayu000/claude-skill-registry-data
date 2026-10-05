---
name: weekly-ai-adoption-digest
displayName: Weekly AI Adoption Digest
tagline: Auto-generate a weekly summary of AI usage trends and productivity wins for leadership.
description: |
  Sets up a recurring weekly report that summarizes AI tool adoption metrics,
  highlights new user activations, ranks top workflows, features a productivity
  win of the week, tracks costs against budget, and announces upcoming events.
  Stores historical data in Google Sheets for trend analysis and posts a
  formatted digest to Slack on a configurable schedule.
department:
  - AI Enablement Leaders
  - Data & Analytics
  - Engineering
use_cases:
  - Documentation
  - Workflow Automation
  - Cost Optimization
tools_required:
  - Slack MCP
  - Google Sheets MCP
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
  Teams: 8 engineering teams, 120 developers
  AI tools tracked: GitHub Copilot, Cursor, Claude Team
  Slack channel: #engineering-leadership
  Schedule: Every Monday at 9:00 AM EST
  Metrics sources: GitHub API, tool admin dashboards, weekly champion reports
exampleOutput: |
  AI Adoption Weekly Digest — Week of Feb 16, 2026

  USAGE SNAPSHOT
  Active Users: 94/120 (78%)  ↑ 3% from last week
  Total Sessions: 2,847       ↑ 12% from last week
  Trending: Up 📈

  NEW ADOPTIONS THIS WEEK
  - Maria G. (Data team) started using Claude Team
  - Backend team installed "ai-roi-calculator" skill
  - 4 new Copilot activations across Mobile and QA

  TOP WORKFLOWS
  1. Code completion (Copilot)   — 8,200 acceptances
  2. PR review assist (Claude)   — 127 reviews
  3. Test generation (Cursor)    — 89 test files

  PRODUCTIVITY WIN OF THE WEEK
  "Used Claude to refactor our payment service — cut 3 days of work into 4 hours.
   The AI caught 2 edge cases I would have missed."
  — Alex T., Platform Team | Impact: 20 hours saved

  COST UPDATE
  This Week: $2,400 | MTD: $7,200 | Budget Remaining: $16,800 (70%)

  COMING UP
  - Feb 25: AI Champions monthly sync (3:00 PM)
  - Mar 1: Cursor Enterprise rollout to QA team

  Generated: Google Sheet updated with Week 8 data + trend charts
  Posted: Slack #engineering-leadership with threaded details
---

# Weekly AI Adoption Digest

Auto-generate a weekly summary of AI usage trends, new skill adoptions, and productivity wins for leadership.

**Integrations:** Slack, Google Sheets

## When to Use

- The user wants to set up recurring AI adoption reports
- Leadership asks for regular updates on AI tool usage
- The user mentions "weekly digest", "adoption report", "AI summary", or "leadership update"
- Teams need to communicate AI adoption progress consistently

## Steps

### Step 1: Define Digest Content

Help the user choose which sections to include:

| Section | Description | Data Source |
|---------|-------------|-------------|
| **Usage Snapshot** | Active users this week vs last week, trend direction | Tool admin dashboards |
| **New Adoptions** | New users who started using AI tools this week | SSO/login data |
| **Top Workflows** | Most-used AI workflows ranked by frequency | Usage analytics |
| **Productivity Wins** | Concrete examples of time saved or quality improved | Team submissions, PR data |
| **Skills Installed** | New agent skills added across the organization | `skills list` output |
| **Cost Update** | Week-over-week spending and budget utilization | Billing data |
| **Champion Spotlight** | Highlight an AI champion and their team's progress | Champion reports |
| **Tips & Tricks** | One useful tip for getting more out of AI tools | Curated by AI team |
| **Upcoming** | Training sessions, new tool rollouts, policy changes | Calendar/roadmap |

### Step 2: Set Up Data Collection

For each section, configure the data source:

**Automated Data (Google Sheets):**
- Create a "Weekly Metrics" sheet with columns for each tracked metric
- Add formulas to calculate week-over-week changes
- Set up data validation for manual entries

**Manual Submissions:**
- Create a Slack workflow or Google Form for "Productivity Win" submissions
- Template: "What tool did you use? What did you accomplish? How much time did you save?"

**Skills Tracking:**
- Run `npx skills list` across projects to inventory installed skills
- Compare against previous week to identify new installations

### Step 3: Design the Digest Template

Create a consistent format:

```
AI Adoption Weekly Digest — Week of [DATE]

USAGE SNAPSHOT
  Active Users: XXX (+X% from last week)
  Total Sessions: X,XXX
  Trending: [up/down/stable]

NEW ADOPTIONS THIS WEEK
  - [Name] ([Team]) started using [Tool]
  - [Name] ([Team]) installed [Skill]
  - X new users total

TOP WORKFLOWS
  1. [Workflow] — used X times
  2. [Workflow] — used X times
  3. [Workflow] — used X times

PRODUCTIVITY WIN OF THE WEEK
  "[Quote from team member about their AI success story]"
  — [Name], [Team]
  Impact: Saved X hours on [task]

COST UPDATE
  This Week: $X,XXX
  Month to Date: $XX,XXX
  Budget Remaining: $XX,XXX (XX%)

CHAMPION SPOTLIGHT
  [Name] from [Team] helped X team members get started
  with [Tool] this week. Their team's adoption rate is now XX%.

TIP OF THE WEEK
  [Practical tip for using AI tools more effectively]

COMING UP
  - [Date]: [Event/Training]
  - [Date]: [New tool rollout]
```

### Step 4: Configure Slack Delivery

Set up automated Slack posting:

- **Channel**: #ai-adoption or #engineering-leadership
- **Schedule**: Every Monday at 9:00 AM (configurable)
- **Format**: Rich Slack message with sections, emoji indicators, and expandable details
- **Thread**: Auto-thread detailed data below the summary

Provide a Slack message template with Block Kit formatting.

### Step 5: Create the Google Sheets Backend

Build a spreadsheet with:

- **Sheet 1: Current Week** — This week's data entry (manual + automated)
- **Sheet 2: Historical Data** — Rolling 52-week history for trend analysis
- **Sheet 3: Charts** — Auto-generated charts (adoption curve, cost trend, top workflows)
- **Sheet 4: Digest Generator** — Formulas that compose the digest text from current week data
- **Sheet 5: Configuration** — Editable settings (team names, tool list, Slack channel, schedule)

### Step 6: Establish the Process

Define who does what each week:

| Day | Task | Owner |
|-----|------|-------|
| Friday | Champions submit metrics and wins | Department Champions |
| Monday AM | Review data, fill gaps, add commentary | AI Program Lead |
| Monday 9 AM | Digest auto-posts to Slack | Automated |
| Monday PM | Leadership reviews, asks questions in thread | Leadership |
| Ongoing | Collect productivity win submissions | All team members |

## Output

Deliver:
- Slack message template (Block Kit JSON)
- Google Sheets backend with formulas and charts
- Data collection form/workflow
- Process runbook for weekly maintenance
- Sample digest with realistic example data
