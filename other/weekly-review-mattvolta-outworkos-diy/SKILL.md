---
name: weekly-review
description: "Gain-based weekly reflection. Looks backward at what moved forward across all projects, written as narrative prose. Modeled on The Gap and The Gain — measures progress against where you were, not where you wish you were."
context: fork
---

# /weekly-review

Generate a reflective weekly review that measures progress backward — what you accomplished relative to where each project was 7 days ago.

## Philosophy

This skill is built on **The Gap and The Gain** framework (Dan Sullivan & Benjamin Hardy):

- **The Gap** = measuring against an ideal. Always out of reach. Breeds dissatisfaction.
- **The Gain** = measuring against your previous self. Concrete, motivating, yours.

This review measures **the Gain**. No shame lists. No blocker tables. No deadline pressure. Just an honest look backward at what moved forward and why it matters.

## Runtime Context

At the start of each review, retrieve user context:

```sql
SELECT email, timezone FROM user_profiles WHERE user_id = auth.uid()
```

Use the returned `email` for Gmail queries (replacing any hardcoded sender address) and `timezone` for date calculations.

Store these values as `USER_EMAIL` and `USER_TIMEZONE` for use throughout all steps.

## When to Use

- End-of-week reflection
- Preparing board updates or stakeholder summaries
- Reconnecting with progress after a scattered week
- Asking "what did I actually accomplish?"

## Workflow

### Step 1: Determine Date Range

Default: last 7 days from today. Accept optional user input for custom range (e.g., "last 2 weeks", "Feb 1-15").

Calculate `start_date` and `end_date` in `YYYY-MM-DD` format.

### Step 2: Gather Raw Data (in parallel)

Run all four data source queries simultaneously — they are independent.

Read `references/data-queries.md` for the exact query patterns.

1. **Log entries** — from `log_entries` table via Supabase MCP
2. **Todoist completions** — completed tasks via Sync API
3. **Gmail threads** — volume and key contacts via Google Workspace MCP
4. **Fireflies meetings** — transcribed meetings via Fireflies MCP

### Step 3: Filter to Active Projects Only

Group all data by project. **Discard any project with zero meaningful activity.** A project appears in the review only if something moved forward — a log entry was written, tasks were completed, or a meeting advanced the work.

Do not list stalled or inactive projects. They are irrelevant to a Gain-based reflection.

### Step 4: Synthesize Per-Project Narratives

For each active project, write **1-2 paragraphs of prose** that answer three questions:

1. **Where was this at the start of the week?** — Use context from log entries, prior state, or what was pending.
2. **What moved forward?** — Concrete accomplishments: things shipped, decisions made, conversations had, problems solved.
3. **Why does it matter?** — Connect the progress to the larger goal. What does this unlock? Why should the user feel good about it?

**Tone**: Warm, reflective, honest. Like a trusted advisor recapping your week over coffee. Not a status report. Not bullet points. Prose.

**Ordering**: Sort projects by significance of progress, not volume of activity. A single breakthrough matters more than 20 routine tasks.

### Step 5: Identify the Top Gains

Pull out the **3-5 most meaningful gains** across all projects. These are not "tasks completed" — they are moments of real forward progress. Ask:

- Did something go from zero to one? (new capability, new relationship, new system)
- Did something cross a finish line? (shipped, delivered, approved, signed off)
- Did something unblock a larger initiative?
- Did you learn something that changes how you'll approach the work?

Write each gain as a single sentence that captures both the what and the why.

### Step 6: Write the Looking Ahead Section

A brief paragraph (3-5 sentences) on **momentum carrying into next week**. Frame positively — what energy and progress you're building on, not what's overdue. This is not a to-do list. It's a sense of direction.

If a previous weekly review exists in `briefs/`, optionally reference it to show week-over-week momentum.

### Step 7: Format Output

Use the template in `references/output-template.md`. The final output should feel like something you'd want to read, not something you have to read.

### Step 8: Offer Follow-up Actions

Ask the user:
1. **Save to file** — Write the review to `briefs/weekly-review-YYYY-MM-DD.md`
2. **Create momentum tasks** — Add 2-3 tasks to Todoist that build on this week's gains
3. **Done** — No further action

## Key Rules

- All secrets from Vault via `$OUTWORKOS_ROOT/scripts/get-secret.sh <label>`
- Never hardcode MCP tool names — use ToolSearch to discover available tools
- Run data source queries in parallel (Step 2)
- Graceful degradation: if a data source is unavailable, note it briefly and continue
- User ID for DB queries: always use `auth.uid()` — never hardcode a user ID
- **Never include metrics tables, activity counts, or stalled project lists**
- **Never list blockers or deadlines** — that's what `/scan` is for
- **Only include projects where something moved forward**
