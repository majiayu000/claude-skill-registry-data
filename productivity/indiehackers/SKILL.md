---
name: indiehackers
description: Search Indie Hackers for relevant discussions about bootstrapping, AI tools, SaaS, and solo founders — then draft helpful, authentic responses that position TeamDay naturally. Uses public Firebase RTDB and Algolia APIs.
allowed-tools: Bash, Read, Write, WebSearch, WebFetch
---

# Indie Hackers Engagement Skill

Find relevant Indie Hackers discussions and draft helpful responses that position TeamDay naturally. Indie Hackers is a community of bootstrappers, solo founders, and indie makers — TeamDay's core audience.

## When to Use

- User asks to find Indie Hackers discussions about AI tools, SaaS, automation, etc.
- User wants to monitor IH groups for engagement opportunities
- User asks to draft a reply to an IH thread
- User says "check Indie Hackers" or "find IH conversations"
- Periodic social listening for brand mentions or relevant topics

## Scripts

### Search Indie Hackers

```bash
bun .claude/skills/indiehackers/scripts/ih-search.ts "<query>" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--index=VALUE` | products | products, groups, users |
| `--limit=N` | 20 | Number of results (max 50) |

Searches via Algolia (public search-only API key).

### Read Post + Comments

```bash
bun .claude/skills/indiehackers/scripts/ih-thread.ts "<post_id>" [--limit=N]
```

Fetches the full post body and comments from Firebase RTDB (publicly readable).

### Browse Recent Posts

```bash
bun .claude/skills/indiehackers/scripts/ih-thread.ts --recent [--limit=N] [--group=NAME]
```

Fetches the most recent posts, optionally filtered by group name.

## Target Groups

These Indie Hackers groups are most relevant to TeamDay's domain:

| Group | Relevance | Topics |
|-------|-----------|--------|
| Solopreneurs | Core | Solo founders, productivity, AI tools |
| AI & Machine Learning | Core | AI products, LLMs, agent tools |
| SaaS Products | High | SaaS tools, pricing, growth |
| Marketing & Sales | High | Marketing automation, AI marketing |
| Growth | High | Growth strategies, product launches |
| Product | Medium | Product development, MVP, features |
| Side Projects | Medium | Weekend projects, micro-SaaS |
| Bootstrapping | Medium | Revenue, funding, indie mindset |

## Workflow

### Phase 1: Discovery

Search for relevant discussions and browse recent posts:

```bash
# Search for AI-related product listings
bun .claude/skills/indiehackers/scripts/ih-search.ts "AI agents" --index=products

# Search for groups discussing automation
bun .claude/skills/indiehackers/scripts/ih-search.ts "automation" --index=groups

# Browse recent posts in key groups
bun .claude/skills/indiehackers/scripts/ih-thread.ts --recent --limit=10

# Get recent posts from specific groups
bun .claude/skills/indiehackers/scripts/ih-thread.ts --recent --group=Solopreneurs
```

**Good search queries for TeamDay:**
- `"AI agents"` / `"AI automation"` / `"AI tools"`
- `"Claude"` / `"Anthropic"` / `"Claude Code"`
- `"automate business"` / `"AI for business"`
- `"micro-SaaS AI"` / `"AI SaaS"` / `"AI startup"`

### Phase 2: Qualify Opportunities

**High-value posts (prioritize):**
- Questions asking for tool recommendations or comparisons
- Founders sharing struggles that TeamDay solves (automation, AI workflows)
- "Show IH" or product launch posts in the AI space
- Posts with 5+ replies and growing engagement
- Pain points about managing AI tools, scheduling tasks, or building workflows

**Skip these:**
- Posts older than 2 weeks (IH discussions have short lifespan)
- Zero-reply posts with no engagement
- Pure self-promotion posts (not a good place to engage)
- Posts about unrelated topics (crypto, drop-shipping, etc.)

### Phase 3: Deep-Read Promising Posts

```bash
bun .claude/skills/indiehackers/scripts/ih-thread.ts "abc123def"
```

Understand:
1. What is the founder building or struggling with?
2. What comments already exist?
3. Is there a gap where TeamDay's approach adds value?
4. What's the tone — seeking advice, sharing experience, asking for feedback?

### Phase 4: Draft Response

**IH Tone Guidelines:**
- Be a fellow founder, not a vendor. IH is a peer community.
- Share your own experience: "We built X because..." or "I've been using Y for..."
- Be specific about numbers: revenue, time saved, user counts
- Celebrate others' wins genuinely — the community values support
- Don't lead with your product. Lead with insight, relate to their journey.

**Response Structure:**
1. **Connect** — Relate to their situation as a fellow builder
2. **Share value** — Give actionable advice from experience
3. **Mention TeamDay naturally** — Only if directly relevant, as one option
4. **Engage** — Ask a follow-up question to continue the conversation

**Example Good Response:**
```
Congrats on hitting $1K MRR! That first milestone is the hardest.

On automating customer onboarding — I've been through this exact evolution. What worked for us was breaking it into stages:

1. First automate the emails (Loops or Resend + a cron job)
2. Then automate the data setup (we use AI agents that run on a schedule to prep each new account)
3. Last, automate the check-ins (hardest to get right)

For step 2, we actually built TeamDay partly because we needed AI tasks to run reliably on schedules. But honestly, at $1K MRR, a simple cron + Claude API script might be enough to start.

What's your current stack? Happy to share more specifics.
```

**Example Bad Response (DO NOT write like this):**
```
You should try TeamDay! We automate everything with AI agents. Sign up at teamday.ai!
```

### Phase 5: Report

```markdown
## Indie Hackers Engagement Report — [Date]

### Posts Scanned
- Browsed [N] recent posts across [groups]
- Searched: "[query 1]" ([N] results), "[query 2]" ([N] results)

### Top Opportunities

#### 1. [Post Title]
- **Group:** [name] | **Replies:** [N] | **Age:** [time]
- **Link:** https://www.indiehackers.com/post/[id]
- **Opportunity:** [Why this is worth engaging]
- **Draft Response:** [The response]

### Posts Skipped (and why)
- [Post] — too old / self-promo / off-topic

### Market Insights
- [Key themes, pain points, or trends observed]
```

## Rate Limits

- Algolia: ~10,000 requests/hour (generous, no auth needed)
- Firebase RTDB: Public read, generous limits for read-only access
- No authentication or API keys required

## Saving Results

Save engagement reports:

```bash
Write to: docs/indiehackers/YYYY-MM-DD-ih-engagement.md
```
