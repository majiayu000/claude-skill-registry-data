---
name: saas-reverse
description: Reverse-engineer any SaaS into a venture-analyst-grade build blueprint. Scrapes the domain, gathers multi-source intelligence (reviews, HN, Reddit, job listings), and outputs a production-ready blueprint with moat analysis, churn vectors, upgrade gates, and a build prompt.
version: 0.2.0
---

# /saas-reverse

Reverse-engineer any SaaS product into an actionable build blueprint.

## Usage

```
/saas-reverse linear.app
/saas-reverse notion.so
/saas-reverse stripe.com
/saas-reverse cal.com - we want to build a scheduling tool for lawyers
/saas-reverse loom.com - focus on async video for customer success teams
```

The optional annotation after `-` focuses the differentiation analysis and build prompt on your specific angle.

---

## Phase 1 — Deep Scrape

Run the scraper to collect raw content from the target domain.

```
python3 skill/saas-reverse/scripts/saas_scraper.py <domain>
```

Fetches: `/`, `/pricing`, `/features`, `/product`, `/about`, `/solutions`, `/blog`, `/changelog`, `/enterprise`, `/docs`, `/team`, `/customers`

Also parses `robots.txt` to discover hidden paths and checks response headers for infrastructure signals.

Returns structured JSON:
- `pages` — path -> stripped text (up to 4000 chars per page)
- `meta` — title, og:title, og:description
- `headlines` — H1/H2/H3 text (first 20), reveals true positioning
- `cta_language` — button/link text (reveals conversion intent)
- `tech_signals` — detected from HTML patterns AND response headers
- `pricing_signals` — price patterns, tier names, trial mechanics
- `social_proof` — user count claims, award mentions, "trusted by" text
- `feature_signals` — combined feature/product/homepage text
- `discovered_paths` — paths found via robots.txt

## Phase 2 — Multi-Source Intelligence

Run the intelligence gatherer for external signals.

```
python3 skill/saas-reverse/scripts/saas_intel.py <domain>
```

Searches across 6 sources:
1. **Review sites** — G2, Capterra, Trustpilot results via DDGS
2. **Pain points** — user complaints, "wish it had", "doesn't work" discussions
3. **Alternatives** — what people compare it to (competitor map)
4. **Pricing intel** — forum/comparison site pricing data (often more accurate than landing page)
5. **Job listings** — tech stack from real job descriptions (Lever, Greenhouse, LinkedIn)
6. **HackerNews** — community discussions, launch threads, Show HN comments
7. **Reddit** — organic sentiment, use case patterns, real feature requests

Returns JSON with all sources merged.

---

## Phase 3 — Synthesis Analysis

With both data sources loaded, analyze the SaaS across these dimensions. Be specific — no vague language, no marketing phrases.

### 3.1 Product reality
- What does it actually do? (ignore taglines, look at screenshots/features/changelog)
- Who actually uses it? (role + company size + trigger moment — when does someone first need this?)
- Core value proposition in one sentence, as a user would say it, not the marketing team

### 3.2 Feature map
- List 8-20 features from scrape + headlines + feature_signals
- Classify each: **Core** (product dies without it) / **Differentiator** (why users pick this over alternatives) / **Table stakes** (expected but not special)
- Note gaps: what do competitors have that this product doesn't mention?

### 3.3 Business model dissection
- Pricing tiers with real numbers (use pricing_intel if site is vague)
- Free tier: what's included, what's the hard limit, what's the soft friction
- **Upgrade gate**: the exact moment that converts free → paid. Is it seat count? Storage? Feature lock? Reporting? API access? Be precise.
- Trial mechanics: days, card required, what gets unlocked
- Enterprise signals: custom pricing, SSO, audit logs, SLA — present or absent?
- Revenue model confidence: usage-based / seat-based / flat / hybrid

### 3.4 Real tech stack
Combine signals from:
- HTML tech_signals (from bundle patterns + tracking scripts)
- Response headers (Server, X-Powered-By, CF-Ray, X-Vercel-ID)
- Job listings (what they're hiring for = what they actually use)
- GitHub if open source (read the actual repo)

Tag each signal: [SEEN] = detected directly, [JOB] = from job listings, [INFERRED] = reasonable conclusion

### 3.5 Moat analysis
What makes this hard to copy? Score each moat type:
- **Network effects** — does value increase as more users join? (Slack: yes. Linear: no)
- **Data moat** — does the product get better with more usage data?
- **Switching costs** — how painful to migrate? (integrations, data export, habit)
- **Brand/community** — is there a cult following? (Notion, Linear — yes)
- **Integrations** — how many integrations, bidirectional or read-only?
- **Workflow lock-in** — does the product become the team's operating system?

For each: Strong / Moderate / Weak / None

### 3.6 Churn vectors
From review analysis (pain_points + reddit_sentiment + hn_discussions), identify:
- Top 3 reasons users leave (from negative reviews, not inference)
- Features users consistently request that aren't there
- Pricing complaints (too expensive? missing tier? surprise charges?)
- Support/reliability issues mentioned
- Competitor that "stole" users most often

### 3.7 User sentiment map
Classify HN + Reddit signals:
- Positive themes (what do fans keep praising?)
- Negative themes (what do critics consistently mention?)
- Neutral observations (pricing model, acquisition, direction)
- Power user patterns (how do heavy users use it differently?)

### 3.8 Competitive landscape
From alternatives_mentions + your knowledge:
- Direct competitors (same job-to-be-done, same buyer)
- Indirect competitors (different approach, same problem)
- Positioning matrix: where does this product sit vs competitors on 2 axes that matter?

### 3.9 Technical complexity score
Estimate build complexity for an indie dev or small team:

| Component | LOE | Notes |
|-----------|-----|-------|
| Core data model | X days | |
| Auth + orgs/teams | X days | |
| Main feature loop | X days | |
| Real-time features | X days | if needed |
| Integrations | X days | per integration |
| Payments/billing | X days | |
| **MVP total** | **X weeks** | without polish |

### 3.10 Differentiation angle
If building a version of this — what would you do differently to have a real chance?
- What user segment is underserved by the incumbent?
- What pricing model would win in a specific niche?
- What 1 feature would make switchers choose yours?
- What would the incumbent never build (because it would cannibalize or contradict their position)?

---

## Phase 4 — Blueprint Output

Output the complete blueprint in this exact format. Fill every section — no placeholders, no "TBD".

---

# Blueprint: [Product Name] ([domain])

> Analyzed: [date] | Confidence: [High/Medium/Low based on data richness]

## What it does
[2-3 specific sentences. No taglines. What does it actually do when you sit down and use it?]

## Who uses it
[Role + company size + trigger moment. Example: "Engineering managers at Series A-C startups (10-100 engineers) who've outgrown GitHub Issues but find Jira too heavyweight. Trigger: team grows past ~8 engineers and standup tracking breaks down."]

## Core features

| Feature | Type | Description |
|---------|------|-------------|
| [name] | Core / Diff / Table stakes | [what it does — be specific] |

## Business model

- **Free tier:** [what's included + hard limit]
- **[Tier]:** $[X]/[seat or month] — [what unlocks]
- **Enterprise:** [signals or "not detected"]
- **Upgrade gate:** [exact trigger] [SEEN/INFERRED]
- **Trial:** [days + card required?]
- **Revenue model:** [seat-based / usage-based / flat / hybrid]

## Tech stack

| Layer | Stack | Confidence |
|-------|-------|------------|
| Frontend | [tech] | [SEEN/JOB/INFERRED] |
| Backend | [tech] | [SEEN/JOB/INFERRED] |
| Database | [tech] | [SEEN/JOB/INFERRED] |
| Auth | [tech] | [SEEN/JOB/INFERRED] |
| Infrastructure | [tech] | [SEEN/JOB/INFERRED] |
| Analytics | [tech] | [SEEN/JOB/INFERRED] |

## Moat analysis

| Moat | Strength | Evidence |
|------|----------|----------|
| Network effects | Strong/Moderate/Weak/None | [why] |
| Switching costs | Strong/Moderate/Weak/None | [why] |
| Data advantage | Strong/Moderate/Weak/None | [why] |
| Brand/community | Strong/Moderate/Weak/None | [why] |
| Integrations | Strong/Moderate/Weak/None | [count + depth] |

**Overall moat:** [1-2 sentences — what keeps users, honestly]

## Churn vectors

1. **[Reason]** — [evidence from reviews/reddit/HN]
2. **[Reason]** — [evidence]
3. **[Reason]** — [evidence]

**Most requested missing feature:** [from community data]
**Competitor that wins most defectors:** [name + why]

## User sentiment

**Fans say:** [2-3 recurring positive themes]
**Critics say:** [2-3 recurring complaints]
**Power users do:** [how heavy users use it beyond the basics]

## Competitive landscape

| Product | Positioning | Vs this product |
|---------|-------------|-----------------|
| [competitor] | [one line] | [stronger/weaker on what] |

## Build complexity

| Component | LOE |
|-----------|-----|
| Data model + migrations | X days |
| Auth + team/org structure | X days |
| Core feature loop | X days |
| Real-time (if needed) | X days |
| Payments + billing | X days |
| Key integrations | X days per |
| **MVP** | **X weeks** |

## Differentiation angle

**Underserved segment:** [who the incumbent ignores or serves poorly]
**Winning move:** [1 thing you'd build differently]
**Pricing angle:** [model that would work in the niche]
**What the incumbent won't build:** [why + why that's your opening]

## Pages to build

- `/` — Landing (positioning: [angle])
- `/pricing`
- `/login`, `/signup`
- `/dashboard` — [main workspace description]
- [all app pages visible from product or scrape]

## Core user flows

**Onboarding**
1. [step — include friction points and drop-off risks]
2. [step]

**Daily core action** (the loop that creates habit)
1. [step]
2. [step]

**Upgrade moment** (what triggers the paywall)
1. [step — the exact moment]

## Data models

```typescript
// Primary entities — inferred from product behavior
type [MainEntity] = {
  id: string;
  [key fields with types];
};

type [SecondaryEntity] = {
  id: string;
  [key fields];
};
```

## Build prompt

> Paste directly into Claude Code, Cursor, or any AI coding assistant:

---

Build a [product type] SaaS called [working title or name].

**What it does:** [2-3 sentences — specific, no marketing language]

**Target user:** [role + company size + pain point + trigger]

**Tech stack:**
- Frontend: Next.js 15 (App Router) + Tailwind CSS + shadcn/ui
- Backend: Next.js API routes + tRPC (if type safety needed)
- Database: PostgreSQL with Prisma ORM — use Neon for serverless
- Auth: Clerk (handles org/team auth out of the box)
- Payments: Stripe — implement [seat-based/usage-based/flat] billing
- Email: Resend with React Email templates
- Hosting: Vercel

**Core features to build** (in priority order):
[numbered list — each with a brief description of behavior, not just name]

**Business rules:**
- Free tier limits: [exact limits]
- Upgrade gate: [exact trigger — e.g., "block creating >3 projects, show upgrade modal"]
- [any other gates, trial behavior, org/team logic]

**Data models:**
[all entities with fields and types — be complete]

**Pages:**
[all pages with brief description of content/behavior]

**Key flows:**
1. Onboarding: [steps]
2. Core loop: [steps]
3. Upgrade: [exact trigger + modal behavior]

**What to build first:** Data schema + auth + team structure. Then the core feature loop. Then billing. Landing page last.

**Differentiation from [main competitor]:** [the one thing to do differently]

---

---

## Evidence tagging

Apply these tags to any claim:
- `[SEEN]` — directly visible on the site (pricing page, feature list, tech detected)
- `[JOB]` — inferred from job listing language
- `[REVIEW]` — from user reviews, Reddit, or HN discussions
- `[INFERRED]` — reasonable technical conclusion
- `[SPEC]` — educated guess, explicitly uncertain

Do not present inferences as facts. A good blueprint is honest about its confidence level.
