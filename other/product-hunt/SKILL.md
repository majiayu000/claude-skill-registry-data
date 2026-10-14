---
name: Product Hunt
description: "Launch, hunt, and research products on Product Hunt. API integration via web_fetch (GraphQL v2), launch strategy, engagement rules, and competitive intelligence."
---

## Setup

**API credential:** `env.PRODUCTHUNT_API_KEY` (Developer Token)

If the user doesn't have a token, guide them:
1. Go to https://api.producthunt.com/v2/oauth/applications
2. Sign in with ProductHunt account
3. Create a new application (any name + redirect URI)
4. Scroll down → click **"Generate Developer Token"**
5. Paste the token in chat → agent stores it via `config set env.PRODUCTHUNT_API_KEY <token>`

Alternatively, use client credentials (API key + secret):
```
web_fetch({
  url: "https://api.producthunt.com/v2/oauth/token",
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: '{"client_id":"API_KEY","client_secret":"API_SECRET","grant_type":"client_credentials"}'
})
```

## API Reference (GraphQL v2)

**Endpoint:** `https://api.producthunt.com/v2/api/graphql`
**Auth header:** `Authorization: Bearer <PRODUCTHUNT_API_KEY>`
**Rate limit:** 6250 complexity points per 15 minutes

### Trending products (today, featured)

```
web_fetch({
  url: "https://api.producthunt.com/v2/api/graphql",
  method: "POST",
  headers: { "Authorization": "Bearer TOKEN", "Content-Type": "application/json" },
  body: '{"query":"{ posts(first: 20, featured: true) { edges { node { name tagline votesCount commentsCount website url makers { name username } } } } }"}'
})
```

### Products by date range

```
web_fetch({
  url: "https://api.producthunt.com/v2/api/graphql",
  method: "POST",
  headers: { "Authorization": "Bearer TOKEN", "Content-Type": "application/json" },
  body: '{"query":"{ posts(first: 20, postedAfter: \"2026-03-23T00:00:00Z\", postedBefore: \"2026-03-24T00:00:00Z\", featured: true) { edges { node { name tagline votesCount url } } } }"}'
})
```

### Product detail with comments

```
web_fetch({
  url: "https://api.producthunt.com/v2/api/graphql",
  method: "POST",
  headers: { "Authorization": "Bearer TOKEN", "Content-Type": "application/json" },
  body: '{"query":"{ post(slug: \"SLUG\") { name tagline description votesCount commentsCount reviewsRating website url makers { name username } topics(first: 5) { edges { node { name } } } comments(first: 10) { edges { node { body createdAt user { name } } } } } }"}'
})
```

### Search by topic

```
web_fetch({
  url: "https://api.producthunt.com/v2/api/graphql",
  method: "POST",
  headers: { "Authorization": "Bearer TOKEN", "Content-Type": "application/json" },
  body: '{"query":"{ posts(first: 20, topic: \"artificial-intelligence\", order: VOTES) { edges { node { name tagline votesCount url } } } }"}'
})
```

### Find topics (get slug for filtering)

```
web_fetch({
  url: "https://api.producthunt.com/v2/api/graphql",
  method: "POST",
  headers: { "Authorization": "Bearer TOKEN", "Content-Type": "application/json" },
  body: '{"query":"{ topics(first: 10, query: \"AI\") { edges { node { name slug postsCount } } } }"}'
})
```

### User profile

```
web_fetch({
  url: "https://api.producthunt.com/v2/api/graphql",
  method: "POST",
  headers: { "Authorization": "Bearer TOKEN", "Content-Type": "application/json" },
  body: '{"query":"{ user(username: \"USERNAME\") { name headline followersCount madePosts(first: 5) { edges { node { name votesCount url } } } } }"}'
})
```

### API limitations

- **Cannot create posts via API** — launch submission is web-only
- Mutations limited to: goals (create/update/complete), follows
- No text search for products — filter by topic slug or date range
- Pagination: cursor-based (`after: "CURSOR"`, use `pageInfo.endCursor`)

## Quick Reference

| Topic | File | Key Trap |
|-------|------|----------|
| Launch execution | `launch.md` | Wrong launch time (not 12:01 AM PT) |
| Hunting products | `hunting.md` | Hunting without maker coordination |
| Competitive research | `research.md` | Treating upvotes as validation |
| Engagement rules | `engagement.md` | Vote manipulation detection |

## Critical Launch Traps

**Timing:**
- Launch window: **12:01 AM to 11:59 PM Pacific Time** — not your timezone
- Best days: Tuesday-Thursday. Mondays = catch-up mode, Fridays = weekend mode
- First 4-6 hours determine ranking trajectory — front-load your promotion
- Verify current specs at https://www.producthunt.com/launch before launch day

**Assets (verify specs before launch — may change):**
- Gallery images: 1270x760px — first image is EVERYTHING
- GIF/video dramatically outperforms static images (<30 seconds)
- Logo: 240x240px
- Tagline: 60 chars max, no buzzwords ("revolutionary", "AI-powered" = instant skip)

**Maker Comment:**
- Personal story, not corporate pitch — PH community is indie-friendly
- Why you built it, what problem you personally faced
- Update throughout the day with new info

## Engagement Anti-Patterns

**What Gets Detected & Penalized:**
- Multiple upvotes from same IP/device → shadowbanned votes
- Burst of upvotes from new accounts → astroturfing pattern
- Upvote circles (same 50 people always vote each other)
- External vote exchange groups (PH actively monitors Slack/Discord)
- Asking for upvotes in comment threads → public callout

## Competitive Intelligence

**Useful Signals:**
- Comment sentiment reveals real user feedback
- "I wish it had..." patterns = your opportunities
- Velocity curve > total upvotes (200 in 2h > 500 in 24h)

**Don't Trust:**
- Upvotes ≠ users ≠ paying customers (zero correlation)
- High upvotes + low comments often = gamed launch

## Scope

Covers: API queries, launching, hunting, competitive research, engagement.
Does NOT cover: building the product, growth outside PH, paid acquisition.
Posts cannot be created via API — launch submission is web-only.
