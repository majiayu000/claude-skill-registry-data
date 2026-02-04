---
name: mindwork-progress
description: Track progress over time across therapy sessions and journal entries. Supports trend analysis, session comparisons, period summaries, and goal tracking. Reads from analysis files and generates comprehensive progress reports.
---

# Progress Tracker

Part of the **mindwork** suite. Tracks changes over time, compares sessions, and measures progress toward therapy goals.

## What It Does

1. **Reads** analysis files from the analysis/ folder
2. **Aggregates** patterns, themes, and metrics across sessions
3. **Tracks** changes and trends over time
4. **Compares** sessions to highlight growth
5. **Measures** progress toward user-defined goals
6. **Generates** comprehensive progress reports

## Key Difference from Analyze

| Skill | Focus | Input | Output |
|-------|-------|-------|--------|
| **Analyze** | Single session snapshot | 1 file | Detailed analysis |
| **Progress** | Changes over time | Multiple files | Trend reports |

---

## Modes of Operation

### 1. Trend Tracking

Track how specific patterns change over time.

**Example prompts:**
> "Track my anxiety levels over the past month"
> "How has my use of catastrophizing changed?"
> "Show me the trend of my emotional themes"
> "What patterns have decreased since I started therapy?"

**Workflow:**
1. Read all analysis files from analysis/ folder
2. Extract mentions of the specified pattern/theme
3. Count occurrences per session/week/month
4. Generate timeline showing trend

### 2. Session Comparison

Compare two or more specific sessions side-by-side.

**Example prompts:**
> "Compare my first session with my most recent one"
> "Compare sessions from January vs March"
> "What's different between session 5 and session 10?"

**Workflow:**
1. Identify the sessions to compare
2. Read both analysis files
3. Extract key metrics from each
4. Generate comparison highlighting differences

### 3. Period Summaries

Generate progress reports for time periods.

**Example prompts:**
> "Generate a weekly progress report"
> "Monthly summary of my therapy progress"
> "Quarterly review of my journal reflections"
> "Summarize my progress this year"

### 5. Journal Type Filtering

Track progress for specific journal types.

**Example prompts:**
> "Show trends in my gratitude entries"
> "Compare my dream logs from January vs March"
> "What patterns appear across my anxiety journal?"
> "Progress report for daily reflections only"

**Workflow:**
1. Determine date range from request
2. Read all analysis files in that range
3. Aggregate metrics and extract highlights
4. Generate comprehensive report

### 4. Goal Tracking

Track progress toward user-defined goals.

**Example prompts:**
> "How am I progressing on my goals?"
> "Update my goal progress"
> "Show progress on my anxiety goal"

**Workflow:**
1. Read goals.md from vault root
2. Read recent analysis files
3. Find evidence related to each goal
4. Generate goal progress report

---

## Prerequisites

- Analysis files in the analysis/ folder (created by the `analyze` skill)
- Optional: `goals.md` file in vault root for goal tracking
- Optional: `mindwork.yaml` configuration

---

## Data Sources

### Analysis Files

The progress skill reads from analysis files created by the `analyze` skill. It extracts:

**From "Cognitive Patterns Observed" section:**
- Pattern names (e.g., "Catastrophizing", "All-or-nothing")
- Frequency of each pattern

**From "Emotional Themes" section:**
- Primary emotions mentioned
- Triggers identified

**From "Key Insights" section:**
- Breakthroughs and realizations
- Growth markers

**From "Progress Notes" section:**
- Changes noted from previous sessions
- Recurring themes

### Goals File

If present, read `goals.md` from the vault root. Parse the structure:

```markdown
# My Therapy Goals

## Active Goals

### 1. Goal Title
- **Started**: YYYY-MM-DD
- **Target**: What success looks like
- **Success criteria**: Measurable indicators

## Completed Goals

### Goal Title
- **Started**: YYYY-MM-DD
- **Completed**: YYYY-MM-DD
- **Outcome**: What was achieved
```

---

## Output Formats

### Structured Timeline

For trend tracking and period summaries:

```markdown
# Progress Timeline: {Period}

## Week 1 ({Date Range})
- **Sessions**: X therapy, Y journals
- **Primary themes**: Theme1, Theme2
- **Cognitive patterns**: Pattern1 (Nx), Pattern2 (Nx)
- **Mood trend**: {start} → {end}
- **Notable**: Key event or breakthrough

## Week 2 ({Date Range})
...

## Overall Trend
{Narrative summary of changes across the period}
```

### Metrics Dashboard

For quantitative analysis:

```markdown
# Progress Metrics: {Period}

## Cognitive Pattern Frequency
| Pattern | This Period | Previous | Trend |
|---------|-------------|----------|-------|
| Pattern1 | N | N | ↓/↑ X% |
| Pattern2 | N | N | ↓/↑ X% |

## Emotional Themes
| Theme | Frequency | Intensity (1-5) |
|-------|-----------|-----------------|
| Theme1 | N mentions | X.X avg |

## Session Stats
- Total sessions analyzed: N
- Therapy sessions: N
- Journal entries: N (by type below)
  - Daily reflections: N
  - Dream logs: N
  - Gratitude entries: N
  - {Other types as configured}
- Date range: {start} to {end}
```

### Milestone Report

For highlighting progress and breakthroughs:

```markdown
# Milestones & Breakthroughs

## Recent Breakthroughs
1. **{Date}**: {Description}
2. **{Date}**: {Description}

## Growth Markers
- {Evidence of growth}
- {New skill or insight}

## Areas of Continued Focus
- {Area needing attention}
- {Ongoing challenge}
```

### Session Comparison

For comparing specific sessions:

```markdown
# Session Comparison

## Sessions Compared
- **Session A**: {name} ({date})
- **Session B**: {name} ({date})

## Key Differences

### Cognitive Patterns
| Pattern | Session A | Session B | Change |
|---------|-----------|-----------|--------|
| Pattern1 | Present/Absent | Present/Absent | Improved/Unchanged |

### Emotional Themes
**Session A**: Theme1, Theme2
**Session B**: Theme3, Theme4

### Notable Changes
- {Significant difference}
- {Growth observed}

## Summary
{Narrative comparing the two sessions}
```

### Goal Progress Report

For tracking therapy goals:

```markdown
# Goal Progress Report

## Goal: {Title}
**Status**: {In Progress / On Track / Needs Attention / Completed}
**Started**: {Date}
**Progress**: {X}% toward target

### Evidence of Progress
- {Specific evidence from sessions}
- {Metric or observation}

### Recent Examples
- {Date} session: {Example}
- {Date} journal: {Example}

### Next Steps
- {Recommended action}
- {Focus area}

---

## Goal: {Next Goal}
...
```

---

## Metric Extraction Guide

When reading analysis files, extract metrics as follows:

### Counting Cognitive Patterns

Look for the "Cognitive Patterns Observed" section. Count each pattern mentioned:
- If pattern has "Frequency: recurring" or multiple evidence items → count as 2+
- Otherwise → count as 1

### Tracking Emotional Themes

Look for the "Emotional Themes" section:
- Extract primary emotions listed
- Note any intensity indicators (words like "intense", "mild", "overwhelming")

### Identifying Breakthroughs

Look for indicators of progress:
- "First time..." statements
- "Successfully..." statements
- "Recognized..." statements
- Items in "Key Insights" that show new understanding
- Positive changes noted in "Progress Notes"

### Detecting Trends

Compare metrics across chronological sessions:
- **Improving**: Pattern count decreasing OR positive emotions increasing
- **Stable**: Minimal change (±10%)
- **Needs attention**: Pattern count increasing OR negative emotions intensifying

---

## Usage Examples

### Weekly Check-in
> "Generate my weekly progress report"

Claude will:
1. Find all analysis files from the past 7 days
2. Aggregate cognitive patterns and themes
3. Identify any breakthroughs
4. Generate a weekly summary report
5. Save to `progress/YYYY-MM-DD-weekly-report.md`

### Monthly Review
> "Monthly summary of my therapy progress"

Claude will:
1. Find all analysis files from the past 30 days
2. Generate metrics dashboard with trends
3. Compare to previous month if data exists
4. Highlight milestones and growth
5. Save to `progress/YYYY-MM-monthly-report.md`

### Specific Pattern Tracking
> "How has my catastrophizing changed over time?"

Claude will:
1. Search all analysis files for "catastrophizing"
2. Count occurrences per session
3. Generate timeline showing frequency trend
4. Note any related breakthroughs

### Session Comparison
> "Compare my first and most recent therapy sessions"

Claude will:
1. Identify oldest and newest analysis files
2. Read both completely
3. Extract comparable metrics
4. Generate side-by-side comparison
5. Highlight growth and changes

### Goal Progress
> "How am I progressing on my goals?"

Claude will:
1. Read goals.md from vault
2. For each active goal, search analysis files for evidence
3. Assess progress toward success criteria
4. Generate goal progress report with recommendations

---

## Output Location

Save progress reports to the `progress/` folder (create if needed):

**Naming conventions:**
- Weekly: `YYYY-MM-DD-weekly-report.md`
- Monthly: `YYYY-MM-monthly-report.md`
- Quarterly: `YYYY-QN-quarterly-report.md`
- Comparisons: `comparison-{session1}-vs-{session2}.md`
- Goal reports: `YYYY-MM-DD-goal-progress.md`

---

## Notes

### Handling Missing Data

If no analysis files exist:
- Suggest running the `analyze` skill first
- Offer to analyze raw transcripts/journals directly

If goals.md doesn't exist:
- Skip goal tracking section
- Suggest creating a goals file

### Privacy

Progress reports contain aggregated personal insights. Store securely alongside analysis files.

### Interpretation Guidance

When presenting progress:
- Focus on observable changes, not judgments
- Use encouraging but realistic language
- Note that progress isn't always linear
- Celebrate small wins while acknowledging ongoing challenges

### Journal Type Filtering

When the user requests progress for a specific journal type:

1. **Identify the type**: Match user's request to configured journal descriptions
2. **Filter analysis files**: Only include analyses with matching Journal Type header
3. **Generate focused report**: Show trends for just that journal type
4. **Cross-reference**: Note patterns that appear across multiple journal types

**Example query handling:**
- "Show trends in my gratitude entries" → Filter to analyses where `Journal Type` contains "gratitude"
- "Compare dream logs" → Filter to analyses from dream log folder
- "Weekly progress for anxiety journal" → Filter + aggregate for anxiety-related entries

**Report header for filtered reports:**
```markdown
# Progress Report: {Journal Type Description}
**Filtered to**: {Journal type name}
**Entries analyzed**: N
**Date range**: {start} to {end}
```
