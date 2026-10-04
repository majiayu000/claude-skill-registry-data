---
name: reddit
description: Search Reddit for relevant discussions, monitor subreddits for engagement opportunities, read threads with comments, and draft helpful community responses. No API key required.
allowed-tools: Bash, Read, Write, WebSearch, WebFetch
---

# Reddit Engagement Skill

Search Reddit for relevant discussions, read threads with full comment trees, and draft authentic community responses.

## When to Use

- Find Reddit discussions about your product, industry, or competitors
- Monitor subreddits for engagement opportunities
- Read a specific thread and its comments before responding
- Draft helpful, non-promotional responses to community questions
- Social listening for brand mentions or relevant topics

## Scripts

### Search Reddit

```bash
bun .claude/skills/reddit/scripts/reddit-search.ts "<query>" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--subreddit=NAME` | all | Restrict to a specific subreddit |
| `--sort=VALUE` | relevance | hot, new, relevance, comments, top |
| `--time=VALUE` | week | hour, day, week, month, year, all |
| `--limit=N` | 25 | Number of results (max 100) |

**Examples:**

```bash
# Broad search
bun .claude/skills/reddit/scripts/reddit-search.ts "ai agents for business" --sort=new --time=week

# Targeted subreddit search
bun .claude/skills/reddit/scripts/reddit-search.ts "workflow automation" --subreddit=smallbusiness --time=month

# Find recent hot discussions
bun .claude/skills/reddit/scripts/reddit-search.ts "best ai tools 2026" --sort=hot --limit=10
```

### Read Thread + Comments

```bash
bun .claude/skills/reddit/scripts/reddit-thread.ts "<url_or_permalink>" [--depth=N]
```

Fetches the full post body and nested comment tree. Use before drafting a response.

**Examples:**

```bash
# Read a thread with 3 levels of comment nesting
bun .claude/skills/reddit/scripts/reddit-thread.ts "https://reddit.com/r/SaaS/comments/abc123/post_title/"

# Shallow read (top-level comments only)
bun .claude/skills/reddit/scripts/reddit-thread.ts "/r/artificial/comments/xyz789/some_post/" --depth=1
```

## Workflow

### Phase 1: Discovery

Run searches across relevant subreddits:

```bash
# Broad search across all of Reddit
bun .claude/skills/reddit/scripts/reddit-search.ts "your topic" --sort=new --time=week

# Targeted subreddit searches
bun .claude/skills/reddit/scripts/reddit-search.ts "your topic" --subreddit=relevant_sub --time=month
```

### Phase 2: Qualify Opportunities

Evaluate each result for engagement potential:

**Prioritize:**
- Questions asking for tool/product recommendations
- Pain points your product solves
- Active discussions (5+ comments, growing)
- Comparison threads

**Skip:**
- Threads older than 2 weeks (stale)
- Posts with 0 comments and low score (no audience)
- Rant/complaint threads
- Already-resolved questions

### Phase 3: Deep-Read Promising Threads

```bash
bun .claude/skills/reddit/scripts/reddit-thread.ts "<permalink>"
```

Understand: What is OP asking? What answers exist? Is there a gap you can fill? What's the tone?

### Phase 4: Draft Response

**Guidelines:**
- Be genuinely helpful first, promotional second (or not at all)
- Write like a knowledgeable community member, not a marketer
- Share specific, actionable advice
- Only mention your product if directly relevant
- Use "I've been using..." or "We built..." framing
- Match the subreddit's culture and tone

**Structure:**
1. Acknowledge the problem
2. Share useful insight (valuable regardless of your product)
3. Mention your product only if directly relevant
4. Offer to help further

### Phase 5: Report

Present findings as a structured engagement report with search queries, top opportunities, draft responses, and recommended follow-up searches.

## How It Works

Uses Reddit's public JSON API — no authentication or API keys needed. Simply appends `.json` to Reddit URLs to get structured data.

**Rate limits:** ~10 requests/minute unauthenticated. Scripts include a custom User-Agent header. If you hit 429 errors, wait 60 seconds.

## Output

- **Search**: Returns JSON array of posts with title, subreddit, score, comment count, age, and text preview. Also prints a human-readable summary.
- **Thread**: Prints formatted post body + nested comment tree. Outputs structured JSON to stderr for programmatic use.
