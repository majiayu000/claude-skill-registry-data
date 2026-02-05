---
name: session-summary
description: End-of-session summary that logs work completed to Obsidian. Run this at the end of any Claude Code session to capture what you accomplished. Creates or appends to the daily session log.
---

# Session Summary Skill

Generate a summary of the current Claude Code session and save it to Obsidian, including estimated time savings.

## Instructions

When the user runs `/session-summary`, do the following:

### 1. Analyze the Current Session

Review the conversation history and identify:
- **Project worked on**: The directory/project name
- **Key accomplishments**: What was built, fixed, or completed
- **Files created or modified**: Important code changes
- **Decisions made**: Any architectural or design choices
- **Problems solved**: Bugs fixed, issues resolved
- **Next steps**: Any pending work mentioned

### 2. Estimate Time Investment

**Track these metrics from the session:**
- Session duration (estimate from conversation timestamps or ask user)
- Number of queries/SQL statements written
- Number of files created or modified
- Number of bugs/errors debugged
- Lines of code or boilerplate generated
- Explanations or learning moments provided

**Apply these conservative multipliers for manual equivalent:**

| Task Type | Multiplier | Notes |
|-----------|------------|-------|
| Boilerplate/scaffolding | 5-10x | Templates, repetitive code |
| SQL query generation | 3-5x | Complex joins, aggregations |
| Data cleaning/transformation | 3-5x | Pandas operations, ETL logic |
| Debugging/error fixing | 2-4x | Investigating, Stack Overflow, trial-and-error |
| Documentation/comments | 2-3x | Writing clear explanations |
| Code explanation/learning | 2-3x | Research time avoided |
| Simple edits/tweaks | 1.5-2x | Minor changes |

**Calculate the estimate:**
1. Estimate actual session duration (ask if unclear)
2. Identify the primary task types from the session
3. Apply a weighted multiplier based on what was done
4. Provide a **range** (low and high estimate)

### 3. Generate the Summary

Create a markdown summary in this format:

```markdown
### [HH:MM] - Project Name
*Directory: `~/path/to/project`*

**Time Investment:**
- Session duration: XX min
- Estimated manual equivalent: X.X - X.X hours
- Primary savings: [Brief note on what drove the savings]

**Accomplishments:**
- [Bullet points of what was done]

**Key Changes:**
- [Files modified or created, if notable]

**Notes:**
- [Any important context, decisions, or next steps]
```

### 4. Save to Obsidian

The daily log file is located at:
```
~/playground/obsidian-notes/austin-os/claude-code-sessions/YYYY-MM-DD-claude-session.md
```

#### Hourly Rate for Value Calculation

Use this hourly rate to calculate the dollar value of time saved:
- **Annual salary:** $164,103
- **Hourly rate:** $78.90 (based on 2,080 hours/year)

#### Token Usage and Cost Tracking

Read the stats cache file to get today's token usage:
```
~/.claude/stats-cache.json
```

**Look for today's date in these sections:**
- `dailyActivity` - for message count, session count, tool call count
- `dailyModelTokens` - for tokens by model

**Pricing rates for cost calculation:**
| Model | Output Tokens (per 1M) |
|-------|------------------------|
| claude-opus-4-5 | $75 |
| claude-sonnet-4-5 | $15 |

*Note: The dailyModelTokens tracks output tokens. Input tokens are harder to track per-day, so we use output tokens as the primary metric. This gives a conservative cost estimate.*

**Calculate daily cost:**
```
cost = (opus_tokens / 1,000,000 × $75) + (sonnet_tokens / 1,000,000 × $15)
```

#### If the file doesn't exist (first session of the day):

Create it with this header and aggregate callout:

```markdown
# Claude Code Session Log: YYYY-MM-DD

**Date**: [Full date like "Monday, December 30, 2024"]

> [!tip] Daily Time Savings
> **Total session time:** XX min
> **Estimated time saved:** X.X - X.X hours
> **Value of time saved:** $XXX - $XXX

> [!info] Daily Token Usage
> **Sessions:** X · **Messages:** XXX · **Tool calls:** XXX
> **Tokens:** XXX,XXX · **Cost:** $X.XX

---

[Session summary here]
```

#### If the file exists (subsequent sessions):

1. **Read the existing file** to find the current aggregate values in the callout
2. **Add the new session's time** to the running totals:
   - Add new session duration to total session time
   - Add new low estimate to total low estimate
   - Add new high estimate to total high estimate
3. **Update the callout** at the top with new aggregates
4. **Append** the new session summary to the end of the file

**Example of updated callouts after 3 sessions:**
```markdown
> [!tip] Daily Time Savings
> **Total session time:** 2 hr 15 min
> **Estimated time saved:** 5.5 - 9.0 hours
> **Value of time saved:** $434 - $710

> [!info] Daily Token Usage
> **Sessions:** 3 · **Messages:** 89 · **Tool calls:** 42
> **Tokens:** 125,430 · **Cost:** $9.41
```

*Note: The token usage callout pulls from `~/.claude/stats-cache.json` and updates each time a session is logged. The data reflects the entire day's usage, not just individual sessions.*

**If today's date is not in the stats cache:** The cache updates periodically, not in real-time. If today's data isn't available yet, add the callout with placeholder text:
```markdown
> [!info] Daily Token Usage
> **Stats pending** — will update when cache refreshes
```

### 5. Backfill Previous Day's Token Stats

Before confirming, check if yesterday's session log has pending token stats that can now be filled in.

**Steps:**
1. Calculate yesterday's date (YYYY-MM-DD format)
2. Check if the file exists: `YYYY-MM-DD-claude-session.md`
3. If it exists, read it and look for `**Stats pending**` in the token usage callout
4. If pending, check `~/.claude/stats-cache.json` for yesterday's date in `dailyActivity` and `dailyModelTokens`
5. If stats are now available, update the callout with the actual values

**Example replacement:**
```markdown
# Before (pending):
> [!info] Daily Token Usage
> **Stats pending** — will update when cache refreshes

# After (backfilled):
> [!info] Daily Token Usage
> **Sessions:** 11 · **Messages:** 1,587 · **Tool calls:** 467
> **Tokens:** 184,010 · **Cost:** $13.80
```

**If backfill occurs**, mention it to the user:
- "Also updated yesterday's log (YYYY-MM-DD) with token stats: X tokens, $X.XX cost"

### 6. Confirm to User

After saving, tell the user:
- The summary was saved
- The file path
- The session's time investment (duration + estimated savings)
- Today's aggregate time savings so far
- A brief recap of the key accomplishments logged

## Example Output

If the user worked on a BigQuery HR data project for ~45 minutes:

```markdown
### 14:30 - BigQuery HR Data
*Directory: `~/analysis/bigquery-hr-data`*

**Time Investment:**
- Session duration: 45 min
- Estimated manual equivalent: 2.0 - 3.5 hours
- Primary savings: Query generation (8 queries), debugging join issues

**Accomplishments:**
- Fixed employee ID join between timesheet and worker tables
- Added job code validation query
- Created diagnostic script for ID column analysis

**Key Changes:**
- Modified `queries/timesheet_analysis.sql`
- Created `scripts/validate_joins.py`

**Notes:**
- Need to verify labor level mappings with HR team
```

## Time Estimation Guidelines

**Be conservative** - it's better to underestimate savings than overstate them.

**Consider the user's context:**
- They're learning Python, so some tasks take them longer manually
- They're experienced with SQL, so SQL-only work has lower multiplier
- Complex debugging or unfamiliar territory = higher multiplier

**When in doubt, ask:**
- "How long do you think this would have taken you manually?"
- Use their answer to calibrate future estimates

**Round sensibly:**
- Use 15-minute increments for session duration
- Use 0.5-hour increments for estimates under 4 hours
- Use 1-hour increments for longer estimates

## Important

- Keep summaries concise but meaningful
- Focus on outcomes, not process
- Use the user's actual project context from the conversation
- Include specific file names when relevant
- Capture any "next steps" mentioned so nothing is lost
- **Always show time as a range** to acknowledge uncertainty
- **Update the daily aggregate** every time you append a new session
