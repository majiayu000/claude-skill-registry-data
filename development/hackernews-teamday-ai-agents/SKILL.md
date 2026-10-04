---
name: hackernews
description: Search Hacker News for relevant tech discussions, product launches, and engagement opportunities using the public Algolia API.
allowed-tools: Bash, Read, Write, WebSearch, WebFetch
---

# Hacker News Engagement Skill

Find relevant Hacker News discussions and draft helpful responses that position TeamDay naturally.

## When to Use

- User asks to find Hacker News discussions about AI agents, developer tools, startups, etc.
- User wants to monitor HN for engagement opportunities or product mentions
- User asks to draft a reply to a HN thread
- User says "check HN" or "find Hacker News conversations"
- Periodic social listening for brand mentions or relevant tech discussions

## Scripts

### Search Hacker News

```bash
bun .claude/skills/hackernews/scripts/hn-search.ts "<query>" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--sort=VALUE` | popularity | popularity, date |
| `--time=VALUE` | week | day, week, month, year, all |
| `--limit=N` | 25 | Number of results (max 100) |
| `--type=VALUE` | story | story, comment, all |

### Read Thread + Comments

```bash
bun .claude/skills/hackernews/scripts/hn-thread.ts "<item_id>" [--depth=N]
```

Fetches the full post body and comment tree. Use this to understand the conversation before drafting a response.

## Target Topics

These topics are most relevant to TeamDay's domain on Hacker News:

| Topic | Relevance | Search Queries |
|-------|-----------|----------------|
| AI Agents | Core | "ai agents", "ai agent framework", "autonomous agent" |
| Claude / Anthropic | Core | "claude code", "claude agent", "anthropic", "claude sdk" |
| MCP Protocol | Core | "mcp server", "model context protocol", "mcp tools" |
| AI Dev Tools | High | "ai coding", "ai developer tools", "copilot alternative" |
| LLM Applications | High | "llm application", "llm production", "ai workflow" |
| Startups / SaaS | Medium | "ai startup", "saas ai", "ai product launch" |
| Show HN | High | "Show HN" posts about AI tools (engagement goldmine) |

## Workflow

### Phase 1: Discovery

Run targeted searches across Hacker News:

```bash
# Broad search for AI agent discussions
bun .claude/skills/hackernews/scripts/hn-search.ts "ai agents" --sort=date --time=week

# Technical discussions about Claude and MCP
bun .claude/skills/hackernews/scripts/hn-search.ts "claude code" --sort=date --time=week

# Show HN posts — prime engagement opportunities
bun .claude/skills/hackernews/scripts/hn-search.ts "Show HN ai" --sort=date --time=week

# Comments discussing pain points
bun .claude/skills/hackernews/scripts/hn-search.ts "ai automation" --type=comment --sort=date
```

### Phase 2: Qualify Opportunities

**High-value threads (prioritize):**
- "Show HN" posts about AI tools (builders are active and responsive)
- "Ask HN" questions about AI agents, automation, or developer tools
- Technical discussions comparing AI platforms or frameworks
- Posts with 10+ comments and growing
- Threads where users share pain points that TeamDay solves

**Skip these:**
- Threads older than 2 weeks (HN discussions die fast)
- Posts with 0 comments and low score (no audience)
- Pure research/academic discussions (wrong audience for a product)
- Heated political/ethical AI debates (high risk, low reward)

### Phase 3: Deep-Read Promising Threads

```bash
bun .claude/skills/hackernews/scripts/hn-thread.ts "12345678"
```

Understand:
1. What is OP actually building or struggling with?
2. What answers already exist in the comments?
3. Is there a technical gap TeamDay could fill?
4. What's the tone — technical, casual, skeptical?

### Phase 4: Draft Response

**HN Tone Guidelines (CRITICAL — HN is different from Reddit):**
- Be deeply technical. HN readers are engineers, founders, and researchers.
- Never use marketing language. No "revolutionize", "game-changing", "unlock potential".
- Share technical details: architecture, trade-offs, what didn't work.
- Be honest about limitations. HN respects intellectual honesty above all.
- Keep it concise. HN favors dense, information-rich comments.

### Phase 5: Report

Save engagement reports to track what's been done:

```bash
# Save to docs
Write to: docs/hackernews/YYYY-MM-DD-hn-engagement.md
```

## Rate Limits

The HN Algolia API is generous — approximately 10,000 requests per hour with no authentication required. Rate limiting is unlikely to be an issue for normal usage.
