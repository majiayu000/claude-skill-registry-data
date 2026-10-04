---
name: meeting-prep
description: |
  Pre-meeting context gathering across all connected systems. Pulls recent interactions, open items, and suggested talking points for any person or topic. Triggers on: "meeting prep", "prep for my meeting", "meeting with X", "prep for 1:1", "before my meeting", "get ready for sync", "/meeting-prep".
---

# Meeting Prep Skill

Gathers cross-channel context before any meeting so you walk in fully prepared. Works for person-based prep (1:1s) and topic-based prep (product syncs, reviews).

## When to Activate

- User says "meeting prep", "prep for my meeting with X", "1:1 prep"
- User provides a person name or meeting topic to prepare for
- User says "what should I discuss with X?"
- Before any recurring sync where context would help

## Input

The user provides ONE of:
- **Person name**: "Daniel Carlbom", "Nina", "Marco"
- **Topic/meeting name**: "ESP review", "Big Room Planning", "Product Sync"
- **Calendar event**: A specific meeting from today's calendar

If no input, check today's Google Calendar for the next upcoming meeting and prep for that.

## Execution

### Step 0: Resolve Target

If the user gave a person name, that's the search target.
If the user gave a topic, use it as the search query across all sources.
If no input, get next meeting from Google Calendar:

```
Google Calendar MCP → list today's events → pick next upcoming → extract attendees + title
```

### Step 1: Parallel Data Gathering (Fan-Out)

Launch parallel searches across all connected sources. Use the Agent tool with subagent_type="Explore" or direct MCP calls depending on complexity.

**For person-based prep:**

| Source | Query | What to Extract |
|:-------|:------|:----------------|
| **Obsidian vault** | Search notes mentioning person name | Last 3 meeting notes, decisions, action items |
| **Granola MCP** | `query_granola_meetings` with person name | Last meeting transcript, key points |
| **Jira MCP** | `searchJiraIssuesUsingJql`: `assignee = "{person}" OR reporter = "{person}" AND updated >= -14d` | Their active issues, recent updates |
| **Slack MCP** | `slack_search_public_and_private` for recent DMs/threads with person | Recent conversations, open threads |
| **GitHub MCP** | `search_pull_requests` by author | Their recent PRs (if engineering) |
| **Confluence MCP** | `searchConfluenceUsingCql`: `contributor = "{person}" AND lastModified > now("-14d")` | Pages they've been editing |

**For topic-based prep:**

| Source | Query | What to Extract |
|:-------|:------|:----------------|
| **Obsidian vault** | Search notes mentioning topic | Meeting history, decisions, context |
| **Jira MCP** | `searchJiraIssuesUsingJql`: `text ~ "{topic}" AND updated >= -30d` | Related tickets, current status |
| **Slack MCP** | `slack_search_public_and_private` for topic | Recent discussions, decisions |
| **Confluence MCP** | `searchConfluenceUsingCql`: `text ~ "{topic}" AND lastModified > now("-30d")` | Specs, RFCs, documentation |
| **Gmail MCP** | `gmail_search_messages` for topic | Email threads about topic |

### Step 2: Synthesize Prep Doc

Merge all results into a structured prep document.

## Output Format

Output directly in the conversation (do NOT create a file unless asked):

```markdown
# Meeting Prep: {Person or Topic}
**For:** {Meeting name if known} | **When:** {Time if known}

## Last 3 Interactions
1. **{Date}** ({source}): {1-2 sentence summary}
2. **{Date}** ({source}): {1-2 sentence summary}
3. **{Date}** ({source}): {1-2 sentence summary}

## They're Waiting On You
- {Action item you owe them, with source}
- {Action item you owe them, with source}
(If none found: "Nothing outstanding found.")

## You're Waiting On Them
- {Action item they owe you, with source}
- {Action item they owe you, with source}
(If none found: "Nothing outstanding found.")

## Their Current Focus
- {What they're working on based on Jira/GitHub/Slack}
- {Recent PRs or tickets}

## Open Threads
- {Unresolved Slack threads or email chains}
- {Blocked Jira issues}

## Suggested Talking Points
1. {Based on open items and recent activity}
2. {Based on unresolved threads}
3. {Based on upcoming deadlines or decisions}
```

## Rules

- **Recency bias**: Prefer last 14 days for people, last 30 days for topics
- **No speculation**: Only include items found in actual sources. If a source returns nothing, skip that section
- **Cite sources**: Always note where information came from (Jira, Slack, Obsidian, etc.)
- **Keep it scannable**: This should be readable in 2 minutes before a meeting
- **Respect privacy**: Don't include private Slack DMs unless the user is a participant

## Fallback

If MCP tools are unavailable or return errors:
1. Search Obsidian vault directly (always available)
2. Note which sources were unreachable
3. Still produce the prep doc with whatever was found

## Examples

```
User: "meeting prep Daniel Carlbom"
→ Searches all sources for Daniel, produces person-based prep

User: "prep for ESP review"
→ Searches all sources for ESP/Explore Similar Programs, produces topic-based prep

User: "prep for my next meeting"
→ Checks Google Calendar, finds next meeting, preps based on attendees + title
```
