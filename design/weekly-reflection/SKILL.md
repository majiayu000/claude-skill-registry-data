---
name: weekly-reflection
description: Conduct comprehensive weekly reflections by integrating time tracking (Timing app), habit tracking (Streaks), task completion (Todoist), email activity (Gmail), and notes (Obsidian) to analyze alignment with semester goals, identify trends, and provide actionable guidance. Use when the user requests a weekly reflection, weekly review, wants to analyze their week, or asks to check progress against goals.
---

# Weekly Reflection

Conduct holistic weekly analysis integrating multiple data sources to assess progress, identify patterns, and provide actionable guidance aligned with semester goals.

## Overview

This skill orchestrates a comprehensive weekly reflection process that:

1. Gathers data from five sources: Timing, Streaks, Todoist, Gmail, and Obsidian
2. Analyzes current week against previous 2-4 weeks for trends
3. Checks alignment with semester goals (focusing on research output while maintaining teaching and habits)
4. Identifies concerning patterns early
5. Provides analytical summary with limited, actionable next steps

## Core Focus Areas

**Primary:** Research output and progress  
**Secondary:** Teaching quality and effectiveness  
**Tertiary:** Habit consistency and maintenance

The analysis should balance these priorities while identifying when secondary/tertiary areas are suffering.

## Data Collection Workflow

### Vault Organization Context

The Obsidian vault follows a modified PARA system with 150+ notes:

- **10 - Projects/**: Active work (Research, Teaching subdirectories)
- **20 - Areas/**: Ongoing responsibilities (Admin, Advising, Research, Teaching, Life, etc.)
- **30 - Resources/**: Reference materials (Computing, Conference Notes, Housing, etc.)
- **40 - Archive/**: Completed or inactive items
- **Semester Notes/**: Academic semester summaries (format: "6 - 2025 Fall.md")
- **Weekly Notes/**: Weekly reflections (ISO format: "2025-W44.md")
- **@Templates/**: Note templates including "Weekly Review.md"

**Search strategy:** The vault is large (150+ notes). Always use targeted `obsidian_global_search` rather than browsing directories. Use `searchInPath` parameter to limit scope and `pageSize=10` to manage results.

Follow this sequence to gather all necessary data efficiently:

### 1. Get Timing App Data (Time Tracking)

```bash
# Get current week summary
python3 /Users/dhidalgo/Documents/personal_scripts/timing_data/llm_tools/timing_export.py --format json

# Get last 4 weeks for trend analysis
python3 /Users/dhidalgo/Documents/personal_scripts/timing_data/llm_tools/timing_export.py --compare 4
```

**What to extract:**

- Total hours worked this week vs recent weeks
- Time allocation by project type (Research, Admin, Teaching)
- Daily work patterns and consistency
- Weekend work indicators

### 2. Get Streaks Data (Habit Tracking)

```bash
# Get current week habit data (Sunday-Saturday)
# Calculate dates: current Sunday to current Saturday
shortcuts run "Get Habit Tracking Data" -i "YYYY-MM-DD,YYYY-MM-DD"

# Example for last 4 weeks:
shortcuts run "Get Habit Tracking Data" -i "2025-10-06,2025-11-02"
```

**What to extract:**

- Completion rate for each habit
- Consecutive completion streaks
- Which habits are slipping
- Patterns by day of week

**Key habits to monitor:**

- Readwise Daily Review
- Math Learning (1 hour target)
- 20 Minutes of Reading
- Exercise habits

### 3. Get Todoist Data (Task Completion)

Use Todoist MCP tools to analyze task patterns:

```
# Get completed tasks for current week
Todoist:find-completed-tasks(since="YYYY-MM-DD", until="YYYY-MM-DD")

# Get current open tasks by project
Todoist:find-tasks(projectId="...")

# Check for overdue tasks
Todoist:find-tasks-by-date(startDate="today", overdueOption="overdue-only")
```

**What to extract:**

- Tasks completed vs created
- Projects with most activity
- Overdue task accumulation
- Task completion patterns (which days/times)

### 4. Get Gmail Sent Email Analysis

Use Gmail MCP tools to analyze sent emails (proxy for communication/collaboration):

```
# Get profile info (includes email address)
read_gmail_profile()

# Search sent emails from current week
# Use Gmail operators: from:me for sent mail, after:/before: for dates
search_gmail_messages(
  q="from:me after:YYYY/MM/DD before:YYYY/MM/DD"
)

# For more specific searches, combine operators:
# Students - sent to .edu addresses or specific patterns
search_gmail_messages(
  q="from:me to:@mit.edu after:YYYY/MM/DD"
)

# Research collaborators - specific domains or people
search_gmail_messages(
  q="from:me (subject:paper OR subject:manuscript OR subject:data) after:YYYY/MM/DD"
)

# Admin - look for committee, meeting, administrative keywords
search_gmail_messages(
  q="from:me (subject:committee OR subject:meeting OR subject:admin) after:YYYY/MM/DD"
)

# Teaching - course-related emails
search_gmail_messages(
  q="from:me (subject:quant OR subject:17.800) after:YYYY/MM/DD"
)

# Read specific threads if needed for context
read_gmail_thread(thread_id="...", include_full_messages=true)
```

**Gmail search operators available:**

- `from:me` - Emails you sent
- `to:email@example.com` - Sent to specific person
- `subject:keyword` - Subject line contains keyword
- `after:YYYY/MM/DD` - After date (e.g., after:2025/10/27)
- `before:YYYY/MM/DD` - Before date
- `OR` - Match either term
- `-term` - Exclude term
- `to:@mit.edu` - Sent to MIT addresses

**What to extract:**

- Total sent email volume for the week
- Email volume by category (students, colleagues, admin)
- Response patterns (are emails clustered or spread throughout day?)
- Collaboration indicators (co-author communications, data sharing)
- Teaching-related correspondence volume (student questions, TA coordination)
- Time of day patterns (late night emails suggest boundary issues)

**Analysis approach:**

1. Get total sent count with broad `from:me` search
2. Categorize with targeted searches (students, research, admin, teaching)
3. Review thread subjects to identify major communication themes
4. Compare volume to previous weeks if possible
5. Note any unusual spikes in specific categories

**Note:** Gmail searches may return many results. Use the `max_results` parameter (default 25) to limit scope. Check for `nextPageToken` in responses if you need to paginate through more results.

### 5. Get Obsidian Vault Data

Use Obsidian MCP to read notes and track work. The vault follows a PARA organizational system with 150+ notes.

**IMPORTANT:** Always use `includeStat: true` when reading notes to get creation/modification timestamps.

```
# Read current week note (with metadata)
obsidian_read_note(
  filePath="Weekly Notes/2025-W[XX].md",
  includeStat=true
)

# Read previous weeks for comparison (2-4 weeks back)
obsidian_read_note(
  filePath="Weekly Notes/2025-W[XX-1].md",
  includeStat=true
)
obsidian_read_note(
  filePath="Weekly Notes/2025-W[XX-2].md",
  includeStat=true
)
obsidian_read_note(
  filePath="Weekly Notes/2025-W[XX-3].md",
  includeStat=true
)

# Read current semester goals
obsidian_read_note(
  filePath="Semester Notes/6 - 2025 Fall.md",
  includeStat=true
)

# Strategy 1: Search for recently modified research notes
# Use targeted searches rather than browsing - more efficient with 150+ notes
obsidian_global_search(
  query="research",
  modified_since="7 days ago",
  searchInPath="10 - Projects/Research",
  pageSize=10
)

# Strategy 2: Search for active teaching materials
obsidian_global_search(
  query="quant teaching",
  modified_since="7 days ago",
  searchInPath="20 - Areas/Teaching",
  pageSize=10
)

# Strategy 3: Check active projects broadly
obsidian_global_search(
  query="",
  modified_since="7 days ago",
  searchInPath="10 - Projects",
  pageSize=10
)

# NOTE: Check for pagination in results (totalPages field)
# If totalPages > 1, consider fetching additional pages for comprehensive view
```

**What to extract from weekly notes:**

- Progress documented in "✅ This Week's Progress"
- Challenges in "🚧 Challenges & Lessons"
- Reflections in "📝 Notes & Reflections"
- Photos/visualizations included
- Note timestamps to understand when entries were added

**What to extract from semester goals:**

- Research goals and their priority (under "## Goals / ### Research")
- Teaching goals
- Life/habit goals
- Scheduled milestones (under "## Schedule")

**What to extract from search results:**

- File paths of recently modified notes
- Modification dates to understand recency
- Brief context from search snippets
- Total pages available (for pagination decisions)

**Search result strategy:**

- Start with targeted searches in specific directories
- Use `pageSize=10` as default (avoid overwhelming context)
- Check `totalPages` in response - if >1, consider fetching more
- Prioritize files modified in last 7 days over older modifications
- Focus searches on project/research areas first, then teaching/admin

**Reading strategy for discovered files:**

- Use `obsidian_read_note` with `includeStat=true` for full context
- Read files selectively based on search result relevance
- Prioritize: Research projects > Teaching materials > Admin notes
- If approaching context limits, read only most recently modified files

**CRITICAL:** Context window management

- The vault has 150+ notes - don't try to read everything
- Use search to identify relevant notes first (not directory browsing)
- When reading recently modified files from searches, limit to top 5-10 most relevant
- Read full notes only for current week, last 2-3 weeks, and semester goals
- For other discovered files, rely on search snippets unless specifically needed

## Analysis Framework

### 1. Goal Alignment Check

Compare this week's activities against semester goals:

**Research Goals:**

- Which research goals had progress this week?
- How many hours allocated to each active research project?
- Are research goals getting sufficient attention given stated priorities?
- Are there research goals with zero progress that should be flagged?

**Teaching Goals:**

- Did teaching activities align with stated teaching goals?
- Is teaching consuming more/less time than expected?
- Are teaching materials being updated as planned?

**Life/Habit Goals:**

- Which habits were maintained consistently?
- Which habits are slipping?
- Are life goals (exercise, learning) getting attention?

### 2. Trend Analysis (Current vs Previous Weeks)

**Time Allocation Trends:**

- Is total work time increasing or decreasing?
- Is research time percentage increasing (desired) or decreasing (concern)?
- Is admin time creeping up (common red flag)?
- Are there unusual spikes in any category?

**Task Completion Trends:**

- Is task completion rate stable, improving, or declining?
- Are overdue tasks accumulating?
- Which projects have stalled (no tasks completed)?

**Habit Trends:**

- Which habits are on a positive streak?
- Which habits are on a negative streak?
- Are there weekly patterns (e.g., weekends worse than weekdays)?

**Energy and Effectiveness:**

- Based on notes, is the user expressing burnout, frustration, or flow?
- Are there mentions of feeling behind or overwhelmed?
- Are there positive momentum indicators?

### 3. Pattern Recognition & Red Flags

**Red Flags to Watch For:**

- Research time below 35% of total work time (suggests admin creep)
- Multiple consecutive days with <6 hours of work (suggests disengagement or overwhelm)
- Habit completion rate dropping below 60%
- Accumulation of overdue tasks (>10 overdue items)
- Zero progress on stated priority research goals
- Weekend work becoming regular pattern (suggests poor boundaries)
- Teaching prep consuming >15 hours/week (suggests inefficiency or scope creep)

**Patterns Meeting Targets:**

- Research time above 45% of total
- Consistent 7-8 hour work days
- Habit completion above 80%
- Clear progress notes on priority projects
- No overdue tasks or minimal overdue (<5 items)
- Good boundaries (minimal weekend work)

### 4. Intervention Strategies

When bad trends are detected, suggest specific interventions:

**For Research Time Decline:**

- Block dedicated research mornings (5-7 AM protected time)
- Defer non-urgent admin tasks
- Batch similar admin tasks to reduce context switching
- Consider saying no to new commitments

**For Habit Slippage:**

- Identify highest-value habit to focus on first
- Reduce other commitments to create habit space
- Link habit to existing strong routine
- Set implementation intention for specific habit

**For Task Overload:**

- Review overdue tasks and ruthlessly delete/defer
- Identify tasks that can be delegated
- Focus on 3 most important tasks for next week
- Set up "no new tasks" period until backlog clears

**For Teaching Time Creep:**

- Re-use previous materials more aggressively
- Identify teaching tasks that can be simplified or cut
- Set hard time limits for prep work
- Consider student feedback to validate quality vs effort

**For Overwhelm/Burnout Signals:**

- Identify one project to pause or defer
- Increase recovery time (earlier bedtime, more breaks)
- Reduce total work hour target temporarily
- Simplify scope of current projects to maintain forward momentum

## Output Format

Provide a conversational summary with this structure:

### Weekly Reflection: [Week Of Date]

**The Big Picture:**

- One paragraph summarizing the week's key theme or pattern
- Explicitly note alignment (or misalignment) with semester goals
- Call out any concerning trends immediately

**What's Working:**

- 2-3 specific patterns meeting or exceeding targets
- Include data points (percentages, hours, streaks)
- Note any goals with progress—no evaluation of whether it's "good" progress

**What Needs Attention:**

- 2-3 specific concerns or declining metrics
- Include data that shows the trend
- Connect to semester goals if relevant

**Key Insights:**

- 1-2 analytical observations about patterns across data sources
- Connections between time use, task completion, and outcomes
- Non-obvious findings from the data

**Actionable Next Steps:**

Use this exact format for action items:

**For Next Week:**

1. [Specific, concrete action with measurable outcome]
2. [Specific, concrete action with measurable outcome]
3. [Specific, concrete action with measurable outcome]

_Maximum 5 action items. Each must be:_

- Concrete (not vague like "focus more")
- Actionable (user knows exactly what to do)
- Connected to identified problems
- Realistic for one week

## Example Analysis Flow

```
1. Read all data sources (Timing, Streaks, Todoist, Obsidian)
2. Extract key metrics and patterns
3. Compare to previous weeks (2-4 weeks)
4. Read semester goals and check alignment
5. Identify red flags and positive patterns
6. Formulate 3-5 concrete action items
7. Write conversational summary with data support
```

## Conversation Style Guidelines

**Tone:** Direct and analytical. Report what the data shows without cushioning. Challenge assumptions when data contradicts goals. No praise, no encouragement—just analysis and implications.

**Data Usage:** Cite specific numbers to support observations. Don't just say "research time is down"—say "research time dropped to 35% this week from 48% last week."

**Honesty:** If multiple areas are struggling, say so plainly. State patterns that indicate problems without softening the message.

**Specificity:** Avoid generic advice. Instead of "spend more time on research," say "block 5-7 AM every day next week specifically for MBTA Communities analysis, aiming for 10 hours total research time."

**Brevity:** Keep the full reflection to 400-600 words plus the action items. Dense but readable.

**No emotional management:** Do not:

- Acknowledge the user's feelings or energy levels
- Provide encouragement or motivation
- Soften criticism with positive framing
- Celebrate wins beyond noting the data
- End with supportive statements

Focus exclusively on patterns, implications, and actionable steps.

## Important Considerations

**Context Window Management:**

- Be selective when reading recently modified files
- Truncate long files to first 200-300 words
- Prioritize recent files over older files
- If context is getting full, skip less important data sources

**Academic Calendar Awareness:**

- Week 1-4 of semester: Teaching prep is expected to be high
- Mid-semester: Research should increase, teaching stabilizes
- End of semester: Grading/admin expected to spike
- Breaks: Research should dominate, minimal teaching/admin

**Seasonal Patterns:**

- Fall: Teaching heavy, research building momentum
- Spring: Teaching continues, research manuscripts due
- Summer: Research focus, teaching minimal
- IAP (January): Variable, often research or course prep

**User Preferences:**

- Prefers technical depth, not dumbed down
- Appreciates contrary arguments and pushback
- Values frank assessment without softening or encouragement
- Wants specific, actionable advice based on data
- Comfortable with statistical and quantitative analysis
- Does not want emotional management, motivation, or self-esteem support
- Expects analytical consultant-style reports, not coaching-style feedback

## Technical Notes

**Week Numbering:** Use ISO week format (YYYY-Www) where weeks start on Sunday and end on Saturday.

**Timing Data:** The timing_export.py script returns data in minutes. Convert to hours for analysis and presentation.

**Streaks Data:** CSV format with entry_type indicating completion status. Focus on "completed_manually" and "completed_auto" vs "missed_auto" and "skipped" entries.

**Todoist Integration:** Use find-completed-tasks for historical analysis and find-tasks for current state. Pay attention to priority levels (p1-p4) when assessing task importance.

**Gmail MCP:**

- **Search operators**: `from:me` (sent), `to:address`, `subject:keyword`, `after:YYYY/MM/DD`, `before:YYYY/MM/DD`
- **Date format**: Use YYYY/MM/DD in queries (e.g., `after:2025/10/27`)
- **Boolean operators**: OR, - (exclude), AND (implicit between terms)
- **Pagination**: Check for `nextPageToken` in responses, use `page_token` parameter for next page
- **Max results**: Default 25, can adjust with `max_results` parameter
- **Thread reading**: Use `read_gmail_thread` for full context, not individual messages

**Obsidian MCP Conventions:**

- **Path format**: Always use forward slashes (e.g., "10 - Projects/Research/Project.md")
- **Case sensitivity**: Paths are case-sensitive, but case-insensitive fallback exists
- **Week notes**: "Weekly Notes/YYYY-Www.md" format (e.g., "Weekly Notes/2025-W44.md")
- **Semester notes**: "Semester Notes/N - YYYY Season.md" format (e.g., "Semester Notes/6 - 2025 Fall.md")
- **Always use includeStat**: Set `includeStat=true` when reading notes for timestamp context
- **Search parameters**: Use `pageSize=10` default, check `totalPages` for pagination needs
- **Search scope**: Use `searchInPath` to target specific folders (e.g., "10 - Projects/Research")
- **Modified dates**: Use `modified_since="7 days ago"` format for recent file searches
- **Timestamp format**: File stats show "HH:MM:SS AM | MM-DD-YYYY"

**Weekly Note Structure:**

- `## Weekly Review` header
- `### ✅ This Week's Progress` for accomplishments
- `### 🚧 Challenges & Lessons` for difficulties
- `### 📝 Notes & Reflections` for insights
- `### 📷️ Photo of the Week` for images
- `### ⌛Time Tracking` for visualizations

## Troubleshooting Common Issues

**If Timing data is unavailable:** Rely more heavily on Obsidian notes and Todoist patterns to infer time allocation.

**If Streaks data fails:** Ask user to provide approximate habit completion estimates or skip habit analysis for this week.

**If Gmail searches return too many results:**

- Use more specific search operators (combine subject:, to:, etc.)
- Reduce time range (fewer days)
- Use `max_results` parameter to limit scope
- Focus on category counts rather than reading individual threads

**If Gmail searches return too few results:**

- Verify date format is correct (YYYY/MM/DD)
- Broaden search terms (remove subject: filters)
- Check if `from:me` is returning any results at all
- Consider that low email volume might be accurate data to report

**If Obsidian searches return too many results:**

- Check `totalPages` field in search response
- If >1 page, fetch next page with pagination
- Or refine search with more specific query terms
- Use `searchInPath` to narrow scope to specific directories
- Reduce `pageSize` if context is constrained

**If Obsidian searches return too few results:**

- Broaden search terms (fewer keywords)
- Remove `searchInPath` restriction to search entire vault
- Try searching without `modified_since` filter
- Use `obsidian_list_notes` to explore directory structure

**If recently modified files overwhelm context:**

- Prioritize by modification date (most recent first)
- Read only top 5 files from search results
- Rely on search result snippets instead of full reads
- Focus on Research and Teaching directories, skip Resources/Archive

**If weekly notes are missing or incomplete:**

- Check previous week's note as fallback
- Use search to find mentions of current week work in project notes
- Explicitly note in reflection that weekly note is incomplete

**If data sources conflict:** Trust time tracking (Timing) data over subjective notes for time allocation. Trust task data (Todoist) over notes for completion patterns. Note conflicts explicitly in the reflection.

**If path not found errors:**

- Verify week number calculation (ISO format, Sunday start)
- Check semester number (sequential: 6 - 2025 Fall follows 5 - 2025 Summer)
- Use case-insensitive search to find correct path
- Verify directories exist with `obsidian_list_notes`
