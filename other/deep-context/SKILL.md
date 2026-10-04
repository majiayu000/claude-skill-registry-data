---
name: deep-context
description: |
  Cross-channel research on any topic. Searches Obsidian, Jira, Confluence, Slack, Gmail, and GitHub in parallel, then synthesizes a comprehensive briefing with timeline, status, stakeholders, and sources. Spans ALL connected systems including personal notes and email. Triggers on: "deep context", "tell me everything about", "research X", "what do we know about", "full context on", "brief me on", "context dump", "/deep-context".
---

# Deep Context Skill

Cross-channel research agent that searches ALL connected systems for everything known about a topic, then synthesizes a comprehensive briefing. Searches beyond Atlassian to include Obsidian, Gmail, Slack, GitHub, and Granola.

## When to Activate

- User says "deep context", "tell me everything about X", "research X"
- User says "what do we know about X?", "full context on X"
- User says "brief me on X", "context dump for X"
- Before writing a spec, RFC, or making a strategic decision
- When onboarding someone to a topic

## How It Differs from Simple Search

| | /simple-search | /deep-context |
|:--|:-------------|:--------------|
| **Sources** | Confluence, Jira, Slack, local context files | ALL of those + Obsidian vault + Gmail + GitHub + Granola |
| **Depth** | Quick answers, 1-3 sources | Comprehensive briefing, all sources |
| **Speed** | Fast (seconds) | Thorough (30-60 seconds) |
| **Output** | Direct answer with citations | Structured briefing document |
| **Use case** | "Who owns search?" | "Give me the full history of our search relevancy work" |

Use `/simple-search` for quick factual questions. Use `/deep-context` for comprehensive research.

## Input

Required:
- **Topic**: The subject to research (e.g., "ESP corridors", "MatchMaker redesign", "lead quality")

Optional:
- **Time range**: Defaults to "all time". User can specify "last 3 months", "Q1 2026", etc.
- **Focus**: "decisions", "status", "history", "people" - narrows the synthesis
- **Output**: "conversation" (default), "file", "confluence"

## Execution

### Step 0: Expand Search Terms

Use domain terminology expansion:
- Input "ESP" → also search "Explore Similar Programs", "multiplier", "loop yield"
- Input "search" → also search "Elasticsearch", "SERP", "relevancy", "RRF"
- Input "ads" → also search "Kevel", "Featured Listings", "sponsored"

For general topics, generate 2-3 synonym expansions.

### Step 1: Parallel Data Gathering (Fan-Out)

Launch ALL searches in parallel using Agent tool or direct MCP calls:

| Source | Tool | Query Pattern |
|:-------|:-----|:-------------|
| **Obsidian vault** | Obsidian vault skill or direct file search | Grep for topic + expansions across vault |
| **Granola MCP** | `query_granola_meetings` | Topic keywords in meeting transcripts |
| **Jira MCP** | `searchJiraIssuesUsingJql` | `text ~ "{topic}" ORDER BY updated DESC` (max 20) |
| **Confluence MCP** | `searchConfluenceUsingCql` | `text ~ "{topic}" ORDER BY lastModified DESC` (max 10) |
| **Slack MCP** | `slack_search_public_and_private` | Topic keywords, sorted by recency |
| **Gmail MCP** | `gmail_search_messages` | Topic keywords in email threads |
| **GitHub MCP** | `search_issues` + `search_pull_requests` + `search_code` | Topic in issues, PRs, and code |
| **Local context** | Read domain-search reference files | Check master and tech context docs |

### Step 2: Deduplicate and Rank

- Same item across sources (e.g., Jira ticket mentioned in Slack) = merge, cite both
- Rank by: recency first, then richness of content
- Group by theme/subtopic if the topic is broad

### Step 3: Synthesize Briefing

Build the structured output from merged results.

## Output Format

```markdown
# Deep Context: {Topic}

**Generated:** {timestamp}
**Sources searched:** {list of sources that returned results}
**Total items found:** {count across all sources}

---

## Executive Summary
{3-5 sentences: What is this topic, what's its current status, and what matters most right now}

## Timeline
| Date | Event | Source |
|:-----|:------|:-------|
| {date} | {What happened} | {Jira/Confluence/Slack/etc.} |
| {date} | {What happened} | {source} |
| {date} | {What happened} | {source} |

## Current Status
- **State:** {Active / Completed / Paused / Blocked}
- **Owner:** {Person or squad}
- **Last activity:** {date} in {source}
- {Key metrics or status indicators if available}

## Key Decisions
1. **{Decision}** ({date}): {What was decided and why}
   - Source: {link or reference}
2. **{Decision}** ({date}): {What was decided and why}
   - Source: {link or reference}

## Open Questions / Unresolved
- {Question or thread that hasn't been resolved}
- {Blocked item or pending decision}

## Key People
| Person | Role in This Topic | Recent Activity |
|:-------|:-------------------|:----------------|
| {name} | {their involvement} | {what they did recently} |

## All Sources
### Jira
- [{TICKET}] {title} - {status} ([link])

### Confluence
- {Page title} - last updated {date} ([link])

### Slack
- #{channel}: {thread summary} ({date})

### Obsidian
- {Note title} ({date}): {relevant excerpt}

### Gmail
- {Subject line} from {sender} ({date})

### GitHub
- {PR/Issue title} - {status} ([link])

---
*Generated by /deep-context*
```

## Rules

- **Exhaustive then concise**: Search everything, but synthesize tightly. The briefing should be readable in 3-5 minutes.
- **Source everything**: Every claim must have a source citation.
- **Conflict surfacing**: If sources disagree, call it out explicitly (same pattern as domain-search).
- **Recency weighting**: More recent items get more prominence, but don't omit history.
- **No speculation**: If something is unclear, say "unclear" not "probably".
- **Privacy**: Don't include others' private Slack DMs. Only include threads where the user is a participant or in public channels.

## Optimization

For very broad topics that return too many results:
1. Cap each source at 15-20 items
2. Prioritize last 90 days unless user specified otherwise
3. Group by subtopic and summarize groups rather than listing every item
4. Offer to "go deeper" on any subtopic

## Fallback

If MCP tools are unavailable:
1. Always search Obsidian vault (local, always available)
2. Always check domain-search local context files
3. Note which sources were unreachable
4. Produce partial briefing with available data
5. Suggest: "Re-run when {source} is available for a complete picture"

## Examples

```
User: "deep context ESP corridors"
→ Searches all sources for ESP, Explore Similar Programs, multiplier, corridor, loop yield
→ Produces full briefing with Q1 OKR data, Jira tickets, meeting decisions, Slack threads

User: "tell me everything about the MatchMaker redesign"
→ Searches all sources for MatchMaker, recommendation form, wizard, lead capture
→ Produces timeline from initial design to current implementation status

User: "deep context INS-1959"
→ Searches for the specific bug across Jira, Slack, GitHub PRs, meeting notes
→ Produces lifecycle view: reported → triaged → discussed → current state

User: "brief me on lead quality, focus on decisions, last 3 months"
→ Narrows time range, emphasizes Key Decisions section
→ Produces decision-focused briefing
```
