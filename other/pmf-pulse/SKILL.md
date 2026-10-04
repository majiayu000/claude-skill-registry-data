---
name: pmf-pulse
description: >
  Comprehensive product-market fit intelligence engine that aggregates signals from every source:
  customer calls (Fireflies), CRM data (HubSpot), prospect objections (Apollo), Reddit discussions,
  Indeed/LinkedIn job postings for role attrition signals, competitor benchmarking (Ahrefs + web),
  and industry forums. Surfaces pain points, unmet needs, competitive gaps, hiring signals, and
  PMF indicators. Use this skill when the user says "PMF check", "product feedback", "what are
  customers saying", "feature requests", "product insights", "churn signals", "voice of customer",
  "product pulse", "competitor analysis", "market intelligence", "what do users want", "are we at
  PMF", "run PMF", "100X founder", "market research", or any variation of wanting a synthesis of
  product and market feedback across sources. Default period: last 30 days.
---

# PMF Pulse — 100X Founder Intelligence Engine

This isn't a feedback report. It's a multi-source intelligence operation that tells you
exactly where you stand with the market, what customers actually need, what competitors
are doing, where the talent gaps are, and what to build next.

## Core Principle

PMF is measured by signal strength across multiple independent sources. When Reddit users
complain about the same thing your customers mention on calls, and competitors are hiring
for that exact problem, and Indeed shows high attrition in those roles — that's a real signal.
Single-source insights are anecdotes. Cross-source patterns are intelligence.

## The Intelligence Sources (run ALL in parallel)

Launch each source as a parallel agent. They don't depend on each other.

### Source 1: Customer Calls (Fireflies)

Pull all customer-facing calls from the analysis period:

```
fireflies_get_transcripts: mine=true, fromDate={periodStart}, toDate={periodEnd}, limit=50
```

For each call, get the summary:
```
fireflies_get_summary: transcriptId={id}
```

**Extract from each call:**
- Feature requests (explicit asks: "can Annie do X?", "we need Y")
- Pain points mentioned (what's not working, workarounds they use)
- Expansion signals ("can we add more locations?", "what about billing?")
- Churn signals ("we're evaluating alternatives", "budget is tight")
- Aha moments ("this saved us 3 hours", "we caught $40K in denials")
- Competitor mentions (who else they're looking at, what they do differently)
- Unsolicited praise (spontaneous positive, referral offers)
- Workflow descriptions (how they actually use the product day-to-day)

**Search for specific pain point keywords:**
```
fireflies_search: keyword:"frustrated" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"wish" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"manual" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"takes too long" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"denied" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"competitor" scope:sentences from:{periodStart} limit:30
```

**Classification rules:**
- KEEP: Assessment calls, FUPs, Onboarding, Touchpoints, client company names
- SKIP: Internal meetings, investor calls, recruiting

### Source 2: CRM Intelligence (HubSpot)

Pull deal activity and contact engagement:

**Won deals (what's working):**
```
search_crm_objects: objectType="deals"
  filterGroups: [{ filters: [
    { propertyName: "dealstage", operator: "EQ", value: "closedwon" },
    { propertyName: "closedate", operator: "GTE", value: "{periodStart}" }
  ]}]
  properties: ["dealname", "amount", "dealstage", "closedate",
               "hs_analytics_source", "notes_last_updated"]
```

**Lost deals (why we lose):**
```
search_crm_objects: objectType="deals"
  filterGroups: [{ filters: [
    { propertyName: "dealstage", operator: "EQ", value: "closedlost" },
    { propertyName: "closedate", operator: "GTE", value: "{periodStart}" }
  ]}]
```

**Extract:**
- Won deal patterns (ICP segment, deal size, sales cycle length, source)
- Lost deal reasons (why they said no — price, feature gap, timing, competitor)
- Stalled deal patterns (what's stuck in pipeline and why)
- Lead source quality (which channels produce buyers vs. tire-kickers)
- Time in each stage (where deals slow down)

### Source 3: Prospect Objections (Apollo)

Pull sequence performance:
```
apollo_emailer_campaigns_search: per_page=20
```

**Extract:**
- Reply rates by sequence/message (what value props resonate)
- Common objections from prospect replies
- Which ICP segments respond vs. ignore
- Which pain points get the most engagement

### Source 4: Reddit — Voice of the Market

Search Reddit for discussions matching Solum Health's ICP pain points. Run these
searches via WebSearch:

**Prior authorization pain:**
```
WebSearch: "prior authorization" site:reddit.com {current year}
WebSearch: "prior auth denied" site:reddit.com
WebSearch: "prior authorization frustrating" OR "prior auth nightmare" site:reddit.com
```

**Insurance verification pain:**
```
WebSearch: "insurance verification" "takes too long" site:reddit.com
WebSearch: "eligibility check" "manual" OR "phone call" site:reddit.com
WebSearch: "VOB" "verification of benefits" site:reddit.com
```

**Front office / admin burden:**
```
WebSearch: "medical office" "front desk" "overwhelmed" OR "burnout" site:reddit.com
WebSearch: "patient intake" "paperwork" OR "manual" site:reddit.com
WebSearch: "claims denied" OR "denial management" site:reddit.com
```

**Behavioral health specific:**
```
WebSearch: "ABA therapy" "billing" OR "insurance" OR "prior auth" site:reddit.com
WebSearch: "mental health practice" "admin" OR "billing" OR "insurance" site:reddit.com
WebSearch: "therapy practice" "burnout" OR "overhead" OR "staffing" site:reddit.com
```

**AI in healthcare operations:**
```
WebSearch: "AI prior authorization" OR "AI insurance verification" site:reddit.com
WebSearch: "healthcare AI" "front office" OR "admin" OR "billing" site:reddit.com
```

For top threads (10-15), use WebFetch to read the full discussion. Extract:
- Specific complaints and pain points (with upvote counts as signal strength)
- Workarounds people describe (these are feature opportunities)
- Tools/software mentioned (competitive landscape from user perspective)
- Sentiment toward AI solutions (excitement, skepticism, specific concerns)
- Role-specific frustrations (front desk vs. billing vs. practice owner)

### Source 5: Indeed & LinkedIn — Role Attrition Signals

Search for high-turnover roles that indicate market pain:

```
WebSearch: site:indeed.com "prior authorization specialist" posted:month
WebSearch: site:indeed.com "insurance verification specialist" posted:month
WebSearch: site:indeed.com "medical billing specialist" posted:month
WebSearch: site:indeed.com "front desk medical" posted:month
WebSearch: site:indeed.com "patient intake coordinator" posted:month
WebSearch: site:indeed.com "ABA billing specialist" posted:month
WebSearch: site:indeed.com "credentialing specialist" posted:month
```

Also search for salary and attrition signals:
```
WebSearch: "prior authorization specialist" salary turnover attrition
WebSearch: "medical billing" "high turnover" OR "hard to hire" OR "staffing shortage"
WebSearch: "front desk" "medical office" "turnover rate"
```

**Extract:**
- Number of open positions (demand indicator — more postings = more pain)
- Salary ranges (cost of manual labor you're replacing)
- Job description pain language ("fast-paced", "high volume", "must multitask")
- Employer types posting (your ICP segments)
- Geographic concentrations
- Repeat posters (companies that can't retain — hot prospects)

### Source 6: Competitor Intelligence (Ahrefs + Web)

Run competitive analysis using Ahrefs MCP and web research:

**Ahrefs organic analysis for key competitors:**
```
For each competitor domain (waystar.com, availity.com, covermymeds.com, centralreach.com,
collectly.com, tebra.com):

ahrefs_site_explorer: target={domain}, mode="subdomains"
  - Get organic traffic volume and trend
  - Get top pages (what content drives their traffic)
  - Get referring domains count
```

**Ahrefs keyword analysis:**
```
ahrefs_keywords_explorer: keywords=["prior authorization software", "insurance verification
  automation", "AI prior auth", "patient intake automation", "claims denial management",
  "ABA billing software", "healthcare front office automation"]
  - Get search volume, difficulty, CPC (willingness to pay = market validation)
  - Get SERP overview to see who's ranking
```

**Web research on competitors:**
```
WebSearch: "Waystar" "prior authorization" product launch {current year}
WebSearch: "CoverMyMeds" "prior authorization" news {current year}
WebSearch: "Availity" "insurance verification" news {current year}
WebSearch: competitor comparison "prior authorization software" {current year}
```

**Extract:**
- Competitor product updates and launches
- Pricing changes or new tiers
- Customer complaints about competitors (G2, Capterra, Reddit)
- Feature gaps where competitors are weak
- Market positioning shifts
- Funding rounds or acquisitions (signals where money is flowing)

### Source 7: Industry Forums & Communities

Search healthcare operations communities:

```
WebSearch: "prior authorization" forum community discussion {current year}
WebSearch: "MGMA" "prior authorization" OR "insurance verification"
WebSearch: "HFMA" "revenue cycle" "prior authorization" {current year}
WebSearch: "healthcare IT" forum "prior auth" automation
```

**Extract:**
- Professional association discussions about automation adoption
- Regulatory changes affecting prior auth workflows
- Industry benchmarks (denial rates, processing times, costs)
- Adoption barriers mentioned by practitioners

## Analysis Framework

### PMF Signal Scoring (1-5 per signal)

| Signal | Strong (5) | Weak (1) |
|--------|-----------|----------|
| **Pull** | Inbound interest, customers asking for more, referrals | Cold outreach only, ghosting, no expansion |
| **Retention** | Renewals easy, usage growing, "can't go back" | Churn, downgrades, "we'll revisit" |
| **Word of Mouth** | Unprompted referrals, Reddit mentions | Every deal requires cold prospecting |
| **Willingness to Pay** | Price objections rare, upsells happen | Constant discounting, "too expensive" |
| **Must-Have** | "We can't operate without this" | "Nice to have but not critical" |
| **Market Timing** | Reddit is angry, Indeed is flooded, competitors are funded | Low search volume, few complaints, no urgency |

### Cross-Source Pattern Detection

The power of this skill is connecting signals across sources. Look for:

1. **Pain + Demand convergence**: Reddit users complaining about X + Indeed flooded with X roles + customers mentioning X on calls = validated pain point
2. **Competitive gap + Customer need**: Competitor weak on Y (Ahrefs, reviews) + customers asking for Y = opportunity
3. **Hiring signal + Automation opportunity**: High-turnover role Z + high salary for Z + customers manually doing Z = strong automation case
4. **Market timing signals**: Regulatory change + industry discussion increase + competitor scramble = window of opportunity

### Customer Segmentation

Group customers by behavior:
- **Champions**: High usage, expanding, referring, quoting value on calls
- **Satisfied**: Using regularly, no complaints, not expanding yet
- **At Risk**: Usage declining, support issues, pricing pushback, competitor mentions
- **Churning**: Explicitly leaving or stopped using

### Feature Request Stack Rank

| Rank | Feature | Customer Asks | Reddit Mentions | Competitor Gap | Indeed Signal | Priority |
|------|---------|--------------|-----------------|----------------|-------------|----------|
| 1 | ... | X customers | Y threads | Z doesn't have it | W roles posted | BUILD NOW |

## Report Structure

```
# PMF Pulse — Intelligence Report
## Period: {startDate} — {endDate}

### OVERALL PMF SCORE: X.X / 5.0 (trend: up/down/flat)

---

## Signal Dashboard

| Signal | Score | Trend | Key Evidence |
|--------|-------|-------|-------------|
| Pull | X/5 | arrow | [specific] |
| Retention | X/5 | arrow | [specific] |
| Word of Mouth | X/5 | arrow | [specific] |
| Willingness to Pay | X/5 | arrow | [specific] |
| Must-Have | X/5 | arrow | [specific] |
| Market Timing | X/5 | arrow | [specific] |

---

## VOICE OF THE CUSTOMER (Fireflies + HubSpot)

### What Customers Are Saying (direct quotes)
[Top 5-7 quotes from actual calls, with customer name and date]

### Feature Requests (ranked by cross-source validation)
| # | Feature | Asks | Reddit | Competitor | Indeed | Action |
|---|---------|------|--------|-----------|--------|--------|

### Churn & Risk Signals
[Specific customers with signals, what to do]

### Expansion Signals
[Specific customers ready to grow, what to offer]

---

## VOICE OF THE MARKET (Reddit + Forums)

### Top Pain Points (ranked by thread engagement)
[What the market is frustrated about, with links to top threads]

### Sentiment Toward AI Solutions
[What people think about AI in this space — excitement, fears, objections]

### Tools Being Discussed
[What software/tools the market is talking about, positive and negative]

---

## LABOR MARKET SIGNALS (Indeed + LinkedIn)

### Role Attrition Heat Map
| Role | Open Postings | Avg Salary | Turnover Signal | Automation Opportunity |
|------|--------------|------------|----------------|----------------------|

### Hot Prospect Signal
[Companies posting repeatedly for roles you automate — these are prospects]

---

## COMPETITIVE LANDSCAPE (Ahrefs + Web)

### Competitor Moves
[Product launches, pricing changes, funding, partnerships]

### Keyword Market Size
[Search volume for key terms, CPC as willingness-to-pay proxy]

### Competitive Gaps (opportunities)
[Where competitors are weak and customers are asking]

---

## CROSS-SOURCE PATTERNS

### Validated Opportunities (pain + demand + gap converge)
1. [Pattern] — Evidence from [sources]
2. [Pattern] — Evidence from [sources]

### Emerging Threats
[Competitor moves + market shifts that could hurt]

### Timing Windows
[Regulatory, market, or competitive windows to exploit NOW]

---

## RECOMMENDED ACTIONS (ranked)

| Priority | Action | Why | Sources |
|----------|--------|-----|---------|
| FIRE | ... | ... | ... |
| THIS WEEK | ... | ... | ... |
| THIS MONTH | ... | ... | ... |
| NEXT QUARTER | ... | ... | ... |

---

## CUSTOMER SEGMENTS

| Segment | Count | Trend | Key Names | Action |
|---------|-------|-------|-----------|--------|
| Champions | X | ... | ... | Referral ask |
| Satisfied | X | ... | ... | Expansion play |
| At Risk | X | ... | ... | Save plan |
| Churning | X | ... | ... | Exit interview |
```

## Delivery

1. Save report to `~/Documents/Claude/SALES/PMF_Pulse_{YYYY-MM-DD}.md`
2. Display in terminal: PMF score, top validated opportunity, biggest risk, one actionable thing to do today
3. Ask: "Want me to drill into any segment, competitor, pain point, or specific customer?"

## Important Rules

- **Run ALL sources in parallel.** Don't wait for one to finish before starting another.
- **Quote people directly.** Every insight traces to a real customer, Reddit user, or job posting.
- **Cross-reference everything.** A single-source insight is an anecdote. Cross-source is intelligence.
- **Be brutally honest.** If PMF is weak, say so. The founder needs truth to survive.
- **Segment > average.** PMF in ABA might be 4.5 while mental health is 2.0. Say so.
- **Include the "so what."** Every finding has a recommended action.
- **Track trends.** Compare to previous reports if they exist.
- **Default period**: Last 30 days. User can specify any range.
- **Hot prospects from Indeed**: Companies repeatedly posting for roles you automate are warm leads. Flag them for outreach.
