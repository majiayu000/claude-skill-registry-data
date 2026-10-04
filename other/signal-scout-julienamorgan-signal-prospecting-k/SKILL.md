---
name: signal-scout
description: >
  Identifies the buying signal TYPES that matter for the user's market, then
  uses them to find companies showing those signals right now. Triggers:
  /signal-scout, "find signals", "what signals matter". Reads: ./gtm/icp.md,
  ./gtm/company.md. Writes: ./gtm/signals.md. Standalone: yes — asks what
  they sell if no context exists.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Agent
  - WebSearch
  - WebFetch
---

# /signal-scout — Buying Signal Discovery

You identify the specific buying signals that indicate someone needs what
the user sells, RIGHT NOW. Not generic signals like "company is growing."
Specific, observable events tied to their market.

---

## Process

### Step 1: Load Context

Read `./gtm/icp.md` and `./gtm/company.md` if they exist.

If neither exists, ask: "What do you sell and who do you sell to?" Then
proceed. Don't require /start to have been run.

**If running standalone (no icp.md exists):** After the user answers,
create a minimal `./gtm/icp.md` with their response before continuing:
```markdown
# ICP Profile
## What We Sell
{their answer}
## Target Buyer
{their answer — title, company size, industry}
```
This ensures /prospect can read the ICP when it auto-continues.

**Check for Won Deal Patterns in icp.md.** If the user provided examples
of deals they've closed, the "Won Deal Patterns" section contains the
highest-confidence signals — these are events that ACTUALLY preceded
a purchase, not theoretical indicators. Prioritize these over everything
else when building the signal list.

**Check for Lost Deal Anti-Signals in icp.md.** If the user provided
examples of deals they've lost, the "Lost Deal Anti-Signals" section
contains disqualification patterns — characteristics of companies that
looked like prospects but never closed. These are as valuable as buying
signals because they prevent wasted outreach. From actual ICP analyses:
80% of lost companies were disqualifiable using just 2-3 anti-fit signals.

**CRM field warning:** If the user provides CRM data or mentions fields
like catalyst note count, champion count, MEDDPICC scores, or any
"did the AE do X" metric — DO NOT use these as signals. They're
downstream artifacts of AE engagement, not causal properties of the
account. They correlate with wins because someone was working the deal,
not because the account was a good fit. Every scoring input must be
observable BEFORE the AE touches the account.

Show what you loaded:

```
  Loaded: {company} sells {product} to {buyer type}.
  {if won deals exist:} Found {N} won deal patterns —
  using these as primary signal source.
  {if lost deals exist:} Found {N} lost deal patterns —
  using these to build anti-signals.
  Researching signals that indicate buying intent.
```

### Step 2: Identify Signal Types

Based on ICP research, determine what observable events mean a company
needs this product. Think from the buyer's perspective: what just happened
that would make them pick up the phone?

**Start with won-deal patterns.** If icp.md has a "Won Deal Patterns"
section, extract the signals from real deals first. These go straight
to high-intent because they're proven. Then fill in the rest of the
categories with theoretical signals. Always label which signals came
from real deals vs. research.

**Signal categories to explore:**

Go deeper than "company is hiring" or "company raised funding."
Those are table-stakes signals that every sales tool surfaces.
The best signals are BEHAVIORAL (what people are saying/doing)
and NEGATIVE (things going wrong). These are harder to find but
far more actionable.

**Transactional Signals (standard — include but don't stop here)**
- Funding rounds (what stage matters for this product?)
- Revenue milestones, M&A activity
- Key hires (which titles signal need?)
- Team expansion in relevant departments
- Product launches, geographic expansion, partnerships
- Regulatory/compliance deadlines

**Behavioral Signals (what the buyer is saying/doing)**
These are the highest-value signals because they show the buyer
is ACTIVELY thinking about the problem, not just growing:
- Buyer posting on LinkedIn about challenges your product solves
- Buyer asking for tool recommendations in communities or posts
- Buyer commenting on content about the problem space
- Buyer speaking at conferences about the topic
- Buyer publishing blog posts about their process struggles
- Company employees leaving G2 reviews about related tools
- Buyer engaging with competitor content (liking, sharing, commenting)

**Negative Signals (things going wrong)**
Pain creates urgency. These are often the strongest buying triggers:
- Declining metrics publicly visible (reply rates, pipeline,
  conversion rates mentioned in earnings, posts, or interviews)
- Churned off an agency or vendor (agency removes them from
  client page, company stops mentioning the vendor)
- Employee turnover in the relevant department (SDRs leaving,
  visible on LinkedIn — signals bad tools/process)
- Same role posted multiple times (can't fill or high turnover)
- Glassdoor/Blind reviews mentioning poor tools, bad leads, or
  process frustration from the department you're selling to
- Price increases from their current vendor creating re-evaluation
- Outbound emails from the company showing up on spam databases
  or being discussed negatively in communities

**Organizational Signals (structural changes)**
- Reorganized team structure (new department, merged teams)
- Promoted someone from IC to manager (needs to build processes)
- Downsized adjacent team (marketing cut → more pressure on sales)
- New board member from a company known for strong GTM
- CRM or tool migration (job postings mentioning "Salesforce
  migration" or "implementing HubSpot")

**Competitive/Market Signals (external pressure)**
- Their direct competitor just raised funding or scaled sales
- Their category is getting crowded (more competition = harder sales)
- Industry report showing their market growing (FOMO pressure)
- Their customer segment is contracting (need better targeting)
- New entrant disrupting their space (urgency to defend position)

**Proxy Signals (indirect indicators)**
- Attending relevant conferences or events
- Evaluating related tools (G2 comparison pages, demo requests
  visible in communities)
- Their investors also invested in companies that use your product
- Following or engaging with thought leaders in your space
- Downloaded or signed up for content/tools from your competitors

**The Buyer's Customer Signals (advanced)**
What's happening to THEIR customers that would make them need this
product? Example: if you sell STR data to DSCR lenders, the signal
isn't "lender raised money" — it's "increase in STR loan applications."

**Social Signals (Reddit, X/Twitter, LinkedIn)**
The warmest signal source. People actively discussing the problem:

- **Reddit threads:** Asking about the problem, comparing solutions,
  complaining about competitors, requesting recommendations
- **X/Twitter posts:** Tweeting about pain points, asking for
  recommendations, sharing frustrations
- **LinkedIn engagement:** Commenting on posts about the topic,
  engaging with competitor content, asking questions in groups

Social signals are high-intent because the person is actively thinking
about the problem. They're also unique — competitors relying on
traditional signals (funding, hires) miss these entirely.

Use WebSearch to validate: are these signals actually findable? Search
for recent examples of each signal type. Drop any that can't be found
in public sources.

**Social signal search queries to test:**
- `site:reddit.com "{problem keyword}" OR "{product category}"`
- `site:reddit.com "{competitor name}" alternative OR vs OR review`
- `site:twitter.com "{problem keyword}" recommend OR looking for`
- `site:linkedin.com/posts "{topic}" OR "{pain point}"`

## Signal Reliability Hierarchy

Not all signals are equally trustworthy. Rank your discovered signals
using this hierarchy (highest → lowest confidence):

1. **Job listings** — Active budget + acknowledged pain. Highest-intent
   because they're spending money to solve the problem with people,
   which means they'd also spend money on tools. (Typical lift: 3.8-5.5x)
2. **Proven signals from won deals** — Validated by actual purchases.
   Higher confidence than any research-based signal.
3. **Behavioral signals** (buyer posting/asking about the problem) —
   Active awareness. The buyer is thinking about this right now.
4. **Negative signals** (churn, turnover, declining metrics) —
   Pain creates urgency. Strong triggers but harder to find.
5. **Compliance/procurement infrastructure** (SOC2, GDPR, ISO) —
   Indicates formal buying process, higher close rates. (Lift: 2.1-6.5x)
6. **Tech stack tools** (niche SaaS in their stack) — Infrastructure
   readiness. But context matters: does the tool create or solve the
   problem? (Lift: 1.5-5.5x)
7. **Website content** — Variable and the most unreliable. A company
   mentioning your product category on their site might be a BUYER
   or a COMPETITOR. Always cross-check. (See interpretation rules below)
8. **Transactional signals** (funding, hiring, M&A) — Table-stakes.
   Every sales tool surfaces these. Useful as supporting signals but
   weakest as standalone triggers.

**When website signals fail:** For B2B back-office tools (AR, billing,
compliance, HR), buyers don't publish their pain on websites. In actual
analyses: 0 of 7 verified customers had relevant website signals. For
these verticals, lean on job listings, tech stack, and firmographics.

## Signal Interpretation Rules

**CRITICAL: Same keyword means different things depending on source.**

Before adding any signal to the list, classify WHERE it appears:
- **Product/features page:** Company SELLS this → competitor signal, NOT buyer
- **Careers/jobs page:** Company NEEDS this → buyer signal (high intent)
- **Blog/case study:** Could be either — is the author writing as vendor
  (promoting their solution) or sharing operational experience?
- **Integrations page:** They connect to relevant systems → infrastructure signal

**The #1 false positive:** If a company's website mentions terms
describing what you sell, they're likely a COMPETITOR or adjacent vendor,
not a buyer. Example: for an AR automation tool, a company whose website
says "our collections automation platform" is a seller. A company whose
job listing says "seeking AR Manager to reduce DSO" is a buyer.

**Tech stack correlation matters:** Not all tech signals are equal.
- **Positive correlation:** Technologies that create MORE complexity
  you solve (ERP, CRM, payment processors for AR tools)
- **Inverse correlation:** Technologies that SOLVE the problem already
  (Shopify for AR tools — consumer payments are immediate, not invoiced)

**n=1 signals need flagging.** A signal appearing in only 1 company
produces high theoretical confidence but is statistically unreliable.
Flag single-company signals with "*(single source — verify)*" and
never use them as primary scoring criteria.

## Anti-Signals (from Lost Deals + Research)

Anti-signals are as valuable as buying signals. They identify companies
that LOOK like prospects but will never close. Catching these early
saves hours of wasted research and outreach.

**Step 2b: Build Anti-Signal List**

Start with lost-deal patterns from icp.md (if available). Then
supplement with research:

**From lost deals (highest confidence):**
Extract what the lost companies had in common. Common patterns:
- Wrong business model (B2C not B2B, consumer not enterprise)
- Competitor or adjacent vendor (they sell what you sell)
- Wrong stage (too early, no budget; too late, already solved it)
- Wrong department structure (no relevant buyer title exists)
- Cultural mismatch (no process, no tools, not ready for automation)

**From market research (supplement):**
- Consumer signals (shopper, checkout, cart, debit) → B2C company
- Retention/churn language on their product pages → consumer
  subscription model, not enterprise buying (typical lift: 0.2-0.4x)
- Selling same product category → competitor, not buyer (lift: 0.1-0.3x)
- No job listings in 12+ months → not growing, no hiring budget
- Their target customer is consumers, not businesses
- Under minimum employee count for your product's sweet spot

**Anti-signal search queries:**
- `"{product category}" competitors` → build a competitor list
- `site:g2.com "{product category}"` → find companies in the space
- WebSearch for companies that sell similar products → these are
  NOT your prospects, they're your competitors

**How anti-signals flow into /prospect:**
The anti-signal list becomes a disqualification checklist. When
/prospect finds a company, it checks against anti-signals first.
A company matching 2+ anti-signals gets dropped regardless of how
strong their buying signals look. This is the fastest way to
improve prospect quality.

### Step 3: Present Signal Types for Approval

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  SIGNAL TYPES: {product/market}
  Researched: {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PROVEN SIGNALS (from your won deals)
  ─────────────────────────────────────────────

  {If won deal patterns exist in icp.md:}
  ① {Signal from Deal 1} — proven
     From: {deal reference}
     Why it matters: {this actually led to a closed deal}

  ② {Signal from Deal 2} — proven
     From: {deal reference}
     Why it matters: {one sentence}

  {If no won deals, skip this section entirely.}

  BEHAVIORAL SIGNALS (buyer doing/saying something — highest value)
  ─────────────────────────────────────────────
  You MUST populate this section with at least 2 signals. If you
  find zero via research, explicitly note "none found via WebSearch"
  — do not silently skip the section.

  ③ {Signal type}
     Example: {recent real example found via search}
     Why it matters: {one sentence}

  NEGATIVE SIGNALS (things going wrong — strongest triggers)
  ─────────────────────────────────────────────
  Churn, turnover, bad reviews, declining metrics, vendor complaints.
  At least 1 required; note "none found" if unavailable.

  ④ {Signal type}
     Example: {recent real example}
     Why it matters: {one sentence}

  ORGANIZATIONAL SIGNALS (structural changes)
  ─────────────────────────────────────────────
  Reorgs, IC→manager promotions, adjacent team downsizing, new board,
  CRM/tool migrations.

  ⑤ {Signal type}
     Example: {recent real example}

  COMPETITIVE/MARKET SIGNALS (external pressure)
  ─────────────────────────────────────────────
  Competitor raised, category crowding, market contraction, new
  entrants, industry reports.

  ⑥ {Signal type}
     Example: {recent real example}

  TRANSACTIONAL / MODERATE-INTENT SIGNALS (worth monitoring)
  ─────────────────────────────────────────────
  Funding, hiring, M&A, expansion. Call these out separately — they
  are the weakest signal class even though they're the easiest to find.

  ⑦ {Signal type}
     Example: {recent real example}

  THEIR CUSTOMER SIGNALS (advanced)
  ─────────────────────────────────────────────

  ⑧ {What's happening to their buyer's customers}
     Example: {if findable}

  SOCIAL SIGNALS (warmest — people talking now)
  ─────────────────────────────────────────────

  ⑨ Reddit: {subreddits + thread types to monitor}
     Example: {recent thread found via search}
     Search: {working query}

  ⑩ X/Twitter: {topics + post types to watch}
     Example: {recent post found via search}
     Search: {working query}

  ⑪ LinkedIn: {post topics where commenters = prospects}
     Example: {recent post found via search}
     Search: {working query}

  ANTI-SIGNALS (disqualify fast — saves the most time)
  ─────────────────────────────────────────────
  Companies showing these patterns look like prospects
  but will never close. Drop them before researching.

  {If lost deal patterns exist in icp.md:}
  From your lost deals:
  ✗ {Anti-signal from Loss 1} — proven non-buyer
  ✗ {Anti-signal from Loss 2} — proven non-buyer

  From market research:
  ✗ {Anti-signal}: {why this disqualifies}
  ✗ {Anti-signal}: {why this disqualifies}
  ✗ {Anti-signal}: {why this disqualifies}

  {If no lost deals, skip the "From your lost deals"
  sub-section and populate from research only.}

  SIGNAL RELIABILITY (strongest → weakest)
  ─────────────────────────────────────────────
  ① Job listings (active budget)
  ② Proven signals (from your won deals)
  ③ Behavioral (buyer actively discussing problem)
  ④ Negative (pain events — churn, turnover)
  ⑤ Compliance/procurement infra (SOC2, ISO)
  ⑥ Tech stack (niche tools in their stack)
  ⑦ Website content (unreliable — check seller vs buyer)
  ⑧ Transactional (funding, hiring — table stakes)

  ──────────────────────────────────────────────

  These are the signals I'll use to find target
  companies. Anything to add or change?
```

### ✋ APPROVAL GATE

Wait for user confirmation. They may:
- Confirm → save signals.md and route
- Add signal types they know from experience
- Remove signals that aren't relevant → remove and re-present
- Reprioritize (move moderate to high, etc.)
- Ask questions ("what's a behavioral signal?", "why is this
  important?") → answer in plain language, then re-present
- Request changes to specific signals → modify, then re-present
  the FULL signal list (not just the changed part) for final
  confirmation before saving signals.md

**After ANY modification, re-present the complete signal list.**
The user must see the full picture before signals.md is written
and /prospect auto-starts.

### Step 4: Save and Route

Create `./gtm/signals.md`:

```markdown
# Buying Signals

## Proven (from won deals)
- {signal type}: {description + deal reference}

## High-Intent
- {signal type}: {description + why}
- {signal type}: {description + why}

## Moderate-Intent
- {signal type}: {description}
- {signal type}: {description}

## Customer Signals
- {signal type}: {description}

## Social Signals
- Reddit: {subreddits + thread types + working query}
- X/Twitter: {topics + post types + working query}
- LinkedIn: {post topics + working query}

## Anti-Signals (disqualifiers)
{Patterns that indicate a company is NOT a buyer. Check these
BEFORE investing time in research or outreach.}

### From Lost Deals
- {anti-signal}: {from Loss 1 — what was observable before the deal}
- {anti-signal}: {from Loss 2}

### From Research
- {anti-signal}: {why this disqualifies — e.g., "competitor, not buyer"}
- {anti-signal}: {why this disqualifies}
- {anti-signal}: {why this disqualifies}

### Competitor List (do not prospect)
- {competitor 1} — {domain}
- {competitor 2} — {domain}
- {competitor 3} — {domain}

## Signal Reliability Hierarchy
1. Job listings (active budget + acknowledged pain)
2. Proven signals (from won deals)
3. Behavioral (buyer discussing problem)
4. Negative (churn, turnover, declining metrics)
5. Compliance/procurement infra
6. Tech stack (context-dependent)
7. Website content (check seller vs buyer)
8. Transactional (funding, hiring — weakest standalone)

## Confirmed
{date} — user approved

## Search Queries — Company Signals
{EVERY WebSearch query you ran during signal research that returned
useful results. One per line. These are reused by /prospect.}

Example:
- "tech company merger acquisition rebrand 2026"
- "{product category}" competitors alternatives funding
- "{buyer title}" hired 2026 announcement

## Search Queries — Social Signals
{EVERY social search query that returned useful results.}

Example:
- site:reddit.com "{problem keyword}" OR "{product category}"
- site:linkedin.com/posts "{buyer title}" "{pain point}"
- site:twitter.com "{problem keyword}" recommend OR "looking for"
```

**CRITICAL: Include the search queries.** /prospect depends on these
to find companies showing signals. Without them, /prospect has to
guess at search queries instead of reusing validated ones. Copy every
query that returned results during your research above.

```
  ──────────────────────────────────────────────

  Signals locked. Searching for companies
  showing these signals now.
```

**After the user approves the signal list and signals.md is saved,
automatically proceed to run the /prospect process.** Do not wait
for the user to type "/prospect". The user just confirmed what to
search for — go search.

---

## Handling Questions and Tangents

If the user asks a question ("what's a behavioral signal?", "why is
job listings ranked #1?", "what does anti-signal mean?"), answer in
plain language. Then resume: "Good question. [answer]. Here's the
signal list — does it look right?"

If they want to explore something ("can you find signals for a
different buyer?", "what about industry X?"), do the research and
fold it into the signal list. Re-present for approval.

If they go off-topic, answer, then bring them back to the approval
gate.

---

## Running Signal-Scout on a Single Company

If the user names a specific company (e.g., `/signal-scout Ramp`), switch
to single-company mode:

1. Load signals.md if it exists (for relevant signal types)
2. WebSearch for that specific company across all signal categories
3. Score and present findings (same format as before)
4. Route to /outreach for that company

This mode is useful for ad-hoc research on a specific target.
