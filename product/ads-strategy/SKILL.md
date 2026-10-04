---
name: ads-strategy
description: Full Ad Strategy Orchestrator. Launches 5 parallel subagents to build a complete advertising strategy from a single URL — audience personas, creative concepts, funnel architecture, competitive intelligence, and budget allocation. Produces a composite Ad Readiness Score (0-100) with a unified, client-ready strategy report.
---

# Full Ad Strategy Orchestrator

## Skill Purpose

Perform a comprehensive, end-to-end advertising strategy build for any business from a single URL. This is the flagship command of the AI Ads Strategist — it launches 5 parallel subagents simultaneously to analyze every dimension of ad readiness, then synthesizes all findings into a unified strategy document with a composite Ad Readiness Score (0-100).

The output is a client-ready deliverable that covers audience research, creative strategy, funnel architecture, competitive positioning, and budget allocation — the kind of document an agency would charge $3,000-$10,000 to produce.

## When to Use

- User runs `/ads strategy <url>`
- User asks for a "full ad strategy", "complete advertising plan", or "ad audit"
- User wants everything in one command without running individual ad skills separately
- User needs a single deliverable covering all advertising dimensions
- User is preparing to launch paid ads and wants a complete roadmap

## Input Requirements

- **Required:** A business URL to analyze
- **Optional:** Monthly budget, target geography, industry context, specific platforms of interest

---

## How to Execute

This skill runs 3 phases. Phase 1 gathers intelligence. Phase 2 launches 5 parallel subagents. Phase 3 synthesizes all results into the final report.

Display progress to the user:

```
================================================================
  ADS STRATEGY BUILD: [Company Name]
================================================================

  Phase 1: Discovery & Business Intelligence ......... [running]
  Phase 2: Parallel Agent Analysis ................... [pending]
    - Audience Research Agent (25%) .................. [pending]
    - Creative Strategy Agent (20%) .................. [pending]
    - Funnel Architecture Agent (20%) ................ [pending]
    - Competitive Intelligence Agent (15%) ........... [pending]
    - Budget & ROI Agent (20%) ...................... [pending]
  Phase 3: Synthesis & Report Generation ............. [pending]

================================================================
```

Update each status as work progresses:
- `[running]` -- Currently executing
- `[complete]` -- Finished successfully
- `[limited]` -- Completed with limited data
- `[pending]` -- Not yet started

---

## Phase 1: Discovery & Business Intelligence

**Objective:** Fetch the target URL, extract all available business intelligence, detect business type, and prepare the context package that all 5 subagents will receive.

### Step 1: Fetch and Analyze the Homepage

Use `WebFetch` to retrieve the homepage at the provided URL. Extract:

| Data Point | Where to Find |
|---|---|
| Company name | Page title, logo, footer, about page |
| Tagline / Value proposition | Hero section, H1, meta description |
| Products or services | Navigation menu, service pages, pricing page |
| Pricing model | Pricing page, CTAs ("free trial", "get quote", "add to cart") |
| Target market signals | Copy language, imagery, testimonials, case studies |
| Trust signals | Client logos, certifications, review counts, media mentions |
| Current CTAs | Buttons, forms, phone numbers, chat widgets |
| Contact info | Phone, email, address, social links |
| Tech stack signals | Meta tags, scripts, platform indicators |
| Content assets | Blog, resources, videos, podcasts, lead magnets |

### Step 2: Detect Business Type

Classify the business into one of these categories based on homepage signals:

| Business Type | Detection Signals | Ad Strategy Implications |
|---|---|---|
| **SaaS / Software** | Pricing page, "Sign up" / "Free trial" / "Book demo" CTAs, feature lists, integration pages, app subdomain | Focus on demo/trial conversions, long sales cycles, retargeting heavy |
| **E-commerce** | Product listings, shopping cart, "Add to cart" buttons, product categories, price displays | Focus on ROAS, product catalog ads, shopping campaigns, impulse triggers |
| **Local Business** | Physical address, Google Maps embed, service area mentions, phone number prominent, "Near me" language | Focus on call extensions, local targeting, Google LSAs, radius targeting |
| **Agency / Services** | Case studies, portfolio, "Our Work", client logos, consultation CTAs, team page | Focus on lead gen, authority building, LinkedIn, long nurture sequences |
| **Creator / Course** | Course listings, "Enroll now", instructor bio, curriculum, testimonials from students, community mentions | Focus on webinar funnels, transformation messaging, urgency/scarcity |
| **Restaurant / Hospitality** | Menu, reservations, location hours, food imagery, delivery links | Focus on Instagram/TikTok visuals, local targeting, seasonal promotions |

### Step 3: Identify Industry and Competitive Context

Use `WebSearch` to gather additional intelligence:

```
"[Company Name]" competitors
"[Company Name]" reviews
"[Company Name]" pricing
[industry] + [location] market size
[industry] advertising benchmarks [current year]
```

### Step 4: Detect Recommended Platforms

Based on business type, determine the optimal platform mix:

| Business Type | Primary Platforms | Secondary Platforms | Avoid |
|---|---|---|---|
| SaaS / Software | Google Ads (Search), LinkedIn | Facebook/Instagram (retargeting), YouTube (demos) | TikTok (unless B2C SaaS) |
| E-commerce | Meta (FB/IG), Google Shopping | TikTok, Pinterest, YouTube | LinkedIn |
| Local Business | Google Ads (Search + LSA), Facebook/IG | Nextdoor, Yelp Ads | LinkedIn, Pinterest |
| Agency / Services | LinkedIn, Google Ads (Search) | Facebook (retargeting), YouTube | TikTok, Pinterest |
| Creator / Course | YouTube Ads, Instagram, Facebook | TikTok, Google (search) | LinkedIn (unless B2B) |
| Restaurant / Hospitality | Instagram, Facebook, Google (local) | TikTok, Yelp | LinkedIn |

### Step 5: Build the Context Package

Compile all Phase 1 findings into a structured context package. This exact package is passed to every subagent so they all operate from the same intelligence:

```
CONTEXT PACKAGE:
- Company: [Name]
- URL: [URL]
- Business Type: [Type]
- Industry: [Industry]
- Products/Services: [List]
- Pricing Model: [Model]
- Value Proposition: [Tagline]
- Target Geography: [Location or "National/Global"]
- Current CTAs: [List]
- Trust Signals: [List]
- Recommended Platforms: [Platform list]
- Monthly Budget: [If provided, else "Not specified"]
- Key Competitors: [List from search]
```

---

## Phase 2: Parallel Agent Launch

**Objective:** Launch 5 specialized subagents simultaneously using the `Agent` tool. Each agent receives the full context package from Phase 1 and produces a category score (0-100) plus detailed findings.

**CRITICAL:** All 5 agents MUST be launched in parallel (not sequentially) to minimize execution time. Use 5 separate `Agent` tool calls in the same response.

---

### Agent 1: Audience Research Agent

**Weight in composite score: 25%**
**Corresponding skill:** `ads-audience`

Launch this agent with the following prompt:

```
You are the Audience Research Agent for an ad strategy build. Using the context below, build a complete audience analysis.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Build 5-7 detailed audience personas for this business. For each persona include:
   - Persona name and archetype (e.g., "Budget-Conscious Buyer", "Overwhelmed Executive")
   - Demographics: age range, gender split, income level, education, job title, location
   - Psychographics: values, lifestyle, aspirations, fears, daily frustrations
   - Pain points: top 3 problems this business solves for them
   - Buying triggers: what specific events or moments push them to buy
   - Objections: top 3 reasons they hesitate or say no
   - Content consumption: platforms they use, content formats they prefer, influencers they follow
   - Platform-specific targeting parameters:
     - Meta (Facebook/Instagram): interests, behaviors, lookalike seed suggestions
     - Google Ads: search intent keywords, in-market audiences, affinity audiences
     - LinkedIn: job titles, industries, company sizes, skills
     - TikTok: interest categories, creator affinities, hashtag communities
   - Persona relevance score (1-5): how valuable is this persona relative to others

2. Define negative audiences (who NOT to target):
   - Demographic exclusions
   - Interest-based exclusions
   - Behavioral exclusions
   - Why each exclusion matters (wasted spend reasons)

3. Identify the #1 highest-value persona and explain why they should receive the largest budget allocation.

4. Map personas to funnel stages — which personas are TOFU (cold), MOFU (warm), BOFU (hot)?

5. Provide an Audience Clarity Score (0-100) based on:
   - How well-defined the ICP is from the website (0-25)
   - How many distinct personas the business can viably target (0-25)
   - How precise the targeting parameters are on each platform (0-25)
   - How clearly the website speaks to specific audience segments (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers for each persona and section. End with:
- AUDIENCE_CLARITY_SCORE: [0-100]
- TOP_PERSONA: [Name]
- TOTAL_PERSONAS: [Count]
- KEY_INSIGHT: [One-sentence biggest finding about the audience]
```

---

### Agent 2: Creative Strategy Agent

**Weight in composite score: 20%**
**Corresponding skill:** `ads-creative`

Launch this agent with the following prompt:

```
You are the Creative Strategy Agent for an ad strategy build. Using the context below, develop a complete creative strategy.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Develop 3 core messaging angles for this business:
   - Pain-point angle: Lead with the problem the audience faces
   - Aspiration angle: Lead with the outcome/transformation
   - Social proof angle: Lead with results, reviews, or authority

2. Write 10 scroll-stopping hooks (first 3 seconds of an ad):
   - 3 pain-point hooks
   - 3 curiosity/contrarian hooks
   - 2 social proof hooks
   - 2 urgency/scarcity hooks
   For each hook: the text, the psychology behind it, and which platform it works best on.

3. Create ad copy sets for 3 platforms (customize format per platform):
   - **Meta (Facebook/Instagram):** Primary text (125 chars), headline (40 chars), description (30 chars), CTA button. Provide 3 variations using PAS, AIDA, and BAB frameworks.
   - **Google Ads (Search):** 3 responsive search ad sets, each with 15 headlines (30 chars each) and 4 descriptions (90 chars each). Include keyword insertion templates.
   - **LinkedIn:** Introductory text (150 words max), headline, CTA. 2 variations — one thought-leader style, one direct-response style.

4. Develop 3 creative concept briefs:
   - Static image ad concept (with visual description, text overlay, color direction)
   - Short video ad concept (15-second script with shot-by-shot breakdown)
   - UGC-style ad concept (script template for a creator to film)

5. Provide a Creative Quality Score (0-100) based on:
   - Hook strength and attention-grabbing potential (0-30)
   - Copy clarity and persuasion quality (0-30)
   - Visual concept variety and platform fit (0-20)
   - A/B test readiness (multiple variations provided) (0-20)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers. End with:
- CREATIVE_QUALITY_SCORE: [0-100]
- STRONGEST_HOOK: [The single best hook you wrote]
- RECOMMENDED_FIRST_AD: [Which ad concept to test first and why]
- KEY_INSIGHT: [One-sentence biggest creative opportunity]
```

---

### Agent 3: Funnel Architecture Agent

**Weight in composite score: 20%**
**Corresponding skill:** `ads-funnel`

Launch this agent with the following prompt:

```
You are the Funnel Architecture Agent for an ad strategy build. Using the context below, design a complete advertising funnel.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Design a complete 4-stage advertising funnel:

   **TOFU (Top of Funnel) — Awareness:**
   - Objective: brand awareness, video views, engagement
   - Audience: cold traffic, broad interests, lookalikes
   - Ad formats: video ads, carousel, boosted content
   - Platforms and campaign types per platform
   - KPIs: CPM, video view rate, engagement rate
   - Budget allocation: percentage of total spend

   **MOFU (Middle of Funnel) — Consideration:**
   - Objective: traffic, lead generation, content consumption
   - Audience: warm traffic (engaged with TOFU), website visitors, email subscribers
   - Ad formats: lead ads, content downloads, case studies, webinar registrations
   - Platforms and campaign types per platform
   - KPIs: CPC, CTR, cost per lead, landing page conversion rate
   - Budget allocation: percentage of total spend

   **BOFU (Bottom of Funnel) — Conversion:**
   - Objective: purchases, demos, consultations, sign-ups
   - Audience: hot traffic (MOFU engagers), cart abandoners, pricing page visitors
   - Ad formats: offer ads, testimonial ads, urgency/scarcity ads, dynamic product ads
   - Platforms and campaign types per platform
   - KPIs: CPA, ROAS, conversion rate
   - Budget allocation: percentage of total spend

   **Retargeting — Recovery & Loyalty:**
   - Retargeting windows (1-3 days, 3-7 days, 7-14 days, 14-30 days, 30-60 days)
   - Audience segmentation by engagement depth
   - Creative rotation strategy (avoid ad fatigue)
   - Frequency caps per platform
   - Cross-sell / upsell sequences for existing customers
   - Budget allocation: percentage of total spend

2. Map the conversion path:
   - Ad click -> Landing page -> [Micro-conversion] -> [Primary conversion]
   - Identify the primary conversion action (purchase, demo, call, form)
   - Define landing page requirements for each funnel stage

3. Define the retargeting pixel strategy:
   - What events to track (page views, add to cart, initiate checkout, form start, video watch %)
   - Custom audience definitions for each retargeting segment
   - Lookalike audience recommendations from each segment

4. Provide a Funnel Architecture Score (0-100) based on:
   - Funnel completeness (all 4 stages defined) (0-25)
   - Stage-to-stage flow logic and audience progression (0-25)
   - Retargeting sophistication and timing (0-25)
   - Platform-specific campaign structure quality (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers for each funnel stage. End with:
- FUNNEL_ARCHITECTURE_SCORE: [0-100]
- RECOMMENDED_FUNNEL_TYPE: [e.g., "Lead Gen Funnel", "Direct Purchase Funnel", "Webinar Funnel"]
- BUDGET_SPLIT: [TOFU: X% | MOFU: X% | BOFU: X% | Retargeting: X%]
- KEY_INSIGHT: [One-sentence biggest funnel opportunity]
```

---

### Agent 4: Competitive Intelligence Agent

**Weight in composite score: 15%**
**Corresponding skill:** `ads-competitors`

Launch this agent with the following prompt:

```
You are the Competitive Intelligence Agent for an ad strategy build. Using the context below, analyze the competitive advertising landscape.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Identify 3-5 direct competitors using web search:
   - Search: "[Company Name] competitors", "[Company Name] alternatives", "[Company Name] vs"
   - Search: "best [industry] [location]" or "top [product category] companies"
   - Fetch each competitor's homepage to analyze their positioning

2. For each competitor, analyze:
   - **Positioning:** How do they position themselves? What is their main value proposition?
   - **Offer structure:** What are they selling and at what price points? Free trials, discounts, bundles?
   - **Landing page quality:** CTA clarity, trust signals, page speed, mobile optimization
   - **Ad presence indicators:** Do they appear to run ads? (look for UTM parameters, retargeting pixels, ad library presence)
   - **Content strategy:** Blog, YouTube, podcast, social media activity
   - **Unique angles:** What messaging do they use that the target business does NOT?

3. Search for competitor ads:
   - Reference Meta Ad Library: "facebook.com/ads/library" searches for competitor names
   - Reference Google Ads Transparency Center mentions
   - Look for competitor ad copy patterns in search results (sponsored listings)

4. Build a competitive gap analysis:
   - What are competitors saying that this business should also say?
   - What are competitors NOT saying that this business could own?
   - What platforms are competitors absent from (opportunity for first-mover advantage)?
   - What audience segments are competitors ignoring?

5. Create a "Beat the Competition" strategy:
   - 3 specific positioning angles that differentiate from competitors
   - Ad copy hooks that directly counter competitor messaging
   - Platform opportunities where competitors are weak or absent
   - Pricing/offer strategies that create competitive advantage

6. Provide a Competitive Position Score (0-100) based on:
   - Market differentiation (how unique is the business positioning) (0-25)
   - Competitor ad sophistication (how hard is the competition) (0-25)
   - Gap opportunities identified (exploitable weaknesses) (0-25)
   - First-mover potential on underserved platforms/audiences (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers. End with:
- COMPETITIVE_POSITION_SCORE: [0-100]
- TOP_COMPETITOR: [Name of strongest competitor]
- BIGGEST_GAP: [Single most exploitable competitive gap]
- KEY_INSIGHT: [One-sentence competitive advantage summary]
```

---

### Agent 5: Budget & ROI Agent

**Weight in composite score: 20%**
**Corresponding skill:** `ads-budget`

Launch this agent with the following prompt:

```
You are the Budget & ROI Agent for an ad strategy build. Using the context below, build a complete budget allocation and ROI projection.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Determine estimated pricing benchmarks for this industry and business type:
   - Average CPM (cost per 1,000 impressions) by platform
   - Average CPC (cost per click) by platform
   - Average CPA (cost per acquisition/conversion) by platform
   - Average ROAS (return on ad spend) benchmarks
   - Average conversion rates by platform and funnel stage
   Use web search if needed: "[industry] advertising benchmarks [current year]"

2. Build 3 budget scenarios:

   **Starter Budget ($1,000-$2,000/month):**
   - Platform allocation (percentages and dollar amounts)
   - Campaign types to run at this budget
   - Expected impressions, clicks, and conversions
   - What to prioritize and what to skip
   - Timeline to meaningful data (statistical significance)

   **Growth Budget ($3,000-$5,000/month):**
   - Platform allocation with multi-platform strategy
   - Full funnel activation (TOFU through retargeting)
   - Expected metrics and projected ROAS
   - A/B testing budget allocation
   - Scaling triggers (when to increase spend)

   **Scale Budget ($7,000-$10,000+/month):**
   - Advanced platform mix with full optimization
   - Multi-channel attribution considerations
   - Creative testing velocity requirements
   - Team/agency resource requirements
   - Expected ROAS at scale and diminishing returns thresholds

3. Calculate break-even analysis:
   - Average order value (AOV) or customer lifetime value (CLV) — estimate from pricing page
   - Break-even CPA calculation
   - Break-even ROAS calculation
   - Months to profitability at each budget tier

4. Build a 90-day scaling roadmap:
   - Month 1: Testing phase — budget, platforms, campaigns, KPIs
   - Month 2: Optimization phase — what to cut, what to scale, new tests
   - Month 3: Scaling phase — budget increases, new platforms, automation

5. Provide a Budget Efficiency Score (0-100) based on:
   - Pricing clarity (can we estimate AOV/CLV from the website) (0-25)
   - Platform-market fit (are the recommended platforms right for this business) (0-25)
   - Scalability potential (room to grow ad spend profitably) (0-25)
   - ROI achievability (realistic conversion path and economics) (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers. End with:
- BUDGET_EFFICIENCY_SCORE: [0-100]
- RECOMMENDED_STARTING_BUDGET: [$X/month]
- PROJECTED_ROAS: [X.Xx at growth budget]
- BREAK_EVEN_CPA: [$X]
- KEY_INSIGHT: [One-sentence budget/ROI finding]
```

---

## Phase 3: Synthesis & Report Generation

**Objective:** Collect all 5 agent results, calculate the composite Ad Readiness Score, assign a grade, and generate the unified strategy report.

### Step 1: Extract Scores from Agent Results

Parse the closing metrics from each agent's output:

| Agent | Score Variable | Weight |
|---|---|---|
| Audience Research | AUDIENCE_CLARITY_SCORE | 25% |
| Creative Strategy | CREATIVE_QUALITY_SCORE | 20% |
| Funnel Architecture | FUNNEL_ARCHITECTURE_SCORE | 20% |
| Competitive Intelligence | COMPETITIVE_POSITION_SCORE | 15% |
| Budget & ROI | BUDGET_EFFICIENCY_SCORE | 20% |

### Step 2: Calculate Composite Ad Readiness Score

```
Ad_Readiness_Score = (Audience * 0.25) + (Creative * 0.20) + (Funnel * 0.20) + (Competitive * 0.15) + (Budget * 0.20)
```

### Step 3: Assign Grade

| Score Range | Grade | Interpretation |
|---|---|---|
| 95-100 | A+ | Exceptional ad readiness -- this business is primed to scale paid ads immediately |
| 90-94 | A | Excellent foundation -- minor refinements needed before aggressive scaling |
| 85-89 | A- | Strong position -- address 1-2 gaps before full budget deployment |
| 80-84 | B+ | Good readiness -- some strategic gaps to close before scaling |
| 75-79 | B | Solid base -- needs focused work on weaker categories before launch |
| 70-74 | B- | Above average -- several areas need improvement for consistent ROI |
| 65-69 | C+ | Moderate readiness -- significant work needed in 2-3 categories |
| 60-64 | C | Fair -- fundamental gaps exist that will limit ad performance |
| 55-59 | C- | Below average -- most categories need substantial improvement |
| 50-54 | D+ | Weak -- major strategic overhaul needed before spending on ads |
| 45-49 | D | Poor -- advertising spend will likely be wasted without foundational fixes |
| 40-44 | D- | Very poor -- critical issues across most categories |
| 0-39 | F | Not ad-ready -- business fundamentals must be addressed before paid advertising |

### Grade Interpretation and Recommendation

| Grade | Recommendation |
|---|---|
| A+ to A- | Start running ads immediately. Focus on testing and scaling. Use the Growth or Scale budget scenario. |
| B+ to B- | Address the 1-2 lowest-scoring categories first. Start with the Starter budget to test while improving. |
| C+ to C- | Significant prep work needed. Fix fundamentals (landing pages, offer clarity, tracking) before spending. Start with Starter budget on one platform only. |
| D+ to F | Do NOT run ads yet. Invest in website improvements, offer development, and brand positioning first. Revisit ads in 30-60 days after foundational work. |

---

## Output Report

Generate a file called `ADS-STRATEGY-[CompanyName].md` where `[CompanyName]` is the cleaned company name (spaces replaced with hyphens, lowercase):

```markdown
# Ad Strategy Report
## [Company Name]
### Strategy Date: [Date]
### URL: [URL]

---

## Executive Summary

**Ad Readiness Score: [X]/100 ([Grade])**

[3-5 sentence executive summary covering: current ad readiness state, business type classification, biggest strength, biggest vulnerability, and the single most important action to take before launching ads. This paragraph should give a busy executive everything they need in 30 seconds.]

**Business Type:** [Detected Type]
**Industry:** [Industry]
**Recommended Platforms:** [Platform list]
**Recommended Starting Budget:** [$X/month]
**Projected ROAS:** [X.Xx]

---

## Score Dashboard

| Category | Score | Weight | Weighted | Status |
|---|---|---|---|---|
| Audience Clarity | [X]/100 | 25% | [X] | [Excellent/Strong/Adequate/Weak/Critical] |
| Creative Quality | [X]/100 | 20% | [X] | [Excellent/Strong/Adequate/Weak/Critical] |
| Funnel Architecture | [X]/100 | 20% | [X] | [Excellent/Strong/Adequate/Weak/Critical] |
| Competitive Position | [X]/100 | 15% | [X] | [Excellent/Strong/Adequate/Weak/Critical] |
| Budget Efficiency | [X]/100 | 20% | [X] | [Excellent/Strong/Adequate/Weak/Critical] |
| **Ad Readiness Score** | | **100%** | **[X]/100** | **[Grade]** |

### Status Key
- **Excellent (90-100):** Best-in-class, no immediate action needed
- **Strong (75-89):** Above average, minor optimizations available
- **Adequate (60-74):** Functional but clear room for improvement
- **Weak (40-59):** Below average, needs focused attention
- **Critical (0-39):** Major issues that will undermine ad performance

---

## Company Profile

| Field | Detail |
|---|---|
| Company | [Name] |
| URL | [URL] |
| Business Type | [Type] |
| Industry | [Industry] |
| Products/Services | [List] |
| Pricing Model | [Model] |
| Value Proposition | [Tagline] |
| Target Geography | [Location] |
| Primary Conversion Action | [Purchase/Demo/Call/Form/Sign-up] |

---

## Audience Personas

[Full output from the Audience Research Agent]

### Persona Overview

| # | Persona | Age | Income | Platform | Relevance | Funnel Stage |
|---|---|---|---|---|---|---|
| 1 | [Name] | [Range] | [Range] | [Primary] | [1-5] | [TOFU/MOFU/BOFU] |
| 2 | [Name] | [Range] | [Range] | [Primary] | [1-5] | [TOFU/MOFU/BOFU] |
| 3 | [Name] | [Range] | [Range] | [Primary] | [1-5] | [TOFU/MOFU/BOFU] |
| 4 | [Name] | [Range] | [Range] | [Primary] | [1-5] | [TOFU/MOFU/BOFU] |
| 5 | [Name] | [Range] | [Range] | [Primary] | [1-5] | [TOFU/MOFU/BOFU] |

### Detailed Personas

[Each persona with full demographics, psychographics, pain points, buying triggers, objections, targeting parameters per platform]

### Negative Audiences (Who NOT to Target)

[Exclusion list with rationale]

### Audience Key Insight
> [One-sentence biggest finding from the Audience agent]

---

## Campaign Architecture

[Full output from the Funnel Architecture Agent]

### Funnel Overview

```
TOFU (Awareness) ──> MOFU (Consideration) ──> BOFU (Conversion) ──> Retargeting (Recovery)
     [X]%                  [X]%                    [X]%                   [X]%
```

### TOFU -- Awareness Stage
[Objectives, audiences, ad formats, platforms, KPIs, budget %]

### MOFU -- Consideration Stage
[Objectives, audiences, ad formats, platforms, KPIs, budget %]

### BOFU -- Conversion Stage
[Objectives, audiences, ad formats, platforms, KPIs, budget %]

### Retargeting -- Recovery & Loyalty
[Windows, segmentation, creative rotation, frequency caps, cross-sell sequences]

### Conversion Path Map
```
[Ad Click] -> [Landing Page] -> [Micro-Conversion] -> [Primary Conversion]
```

### Pixel & Tracking Strategy
[Events to track, custom audiences, lookalike recommendations]

### Funnel Key Insight
> [One-sentence biggest finding from the Funnel agent]

---

## Creative Strategy

[Full output from the Creative Strategy Agent]

### Core Messaging Angles

| # | Angle | Description | Best For |
|---|---|---|---|
| 1 | Pain-Point | [Description] | [Platform/Stage] |
| 2 | Aspiration | [Description] | [Platform/Stage] |
| 3 | Social Proof | [Description] | [Platform/Stage] |

### Top 10 Scroll-Stopping Hooks

| # | Hook | Type | Platform | Psychology |
|---|---|---|---|---|
| 1 | [Hook text] | [Pain/Curiosity/Proof/Urgency] | [Platform] | [Why it works] |
| 2 | [Hook text] | [Type] | [Platform] | [Why it works] |
| ... | ... | ... | ... | ... |

### Platform-Specific Ad Copy

#### Meta (Facebook / Instagram)
[3 ad copy variations with primary text, headline, description, CTA]

#### Google Ads (Search)
[3 responsive search ad sets with headlines and descriptions]

#### LinkedIn
[2 ad copy variations]

### Creative Concepts

#### Concept 1: Static Image Ad
[Visual description, text overlay, color direction, platform specs]

#### Concept 2: Short Video Ad (15s)
[Shot-by-shot script, voiceover, on-screen text, music direction]

#### Concept 3: UGC-Style Ad
[Creator script template, talking points, B-roll suggestions]

### Creative Key Insight
> [One-sentence biggest finding from the Creative agent]

---

## Competitive Landscape

[Full output from the Competitive Intelligence Agent]

### Competitor Overview

| Competitor | Positioning | Ad Presence | Strongest Platform | Key Weakness |
|---|---|---|---|---|
| [Name] | [Value prop] | [Active/Moderate/None] | [Platform] | [Gap] |
| [Name] | [Value prop] | [Active/Moderate/None] | [Platform] | [Gap] |
| [Name] | [Value prop] | [Active/Moderate/None] | [Platform] | [Gap] |

### Competitive Gap Analysis

| Gap | Opportunity | How to Exploit |
|---|---|---|
| [Gap] | [What it means] | [Specific ad strategy] |
| [Gap] | [What it means] | [Specific ad strategy] |
| [Gap] | [What it means] | [Specific ad strategy] |

### "Beat the Competition" Strategy
[3 positioning angles, counter-messaging hooks, platform opportunities, offer strategies]

### Competitive Key Insight
> [One-sentence biggest finding from the Competitive agent]

---

## Budget Allocation & ROI Projections

[Full output from the Budget & ROI Agent]

### Industry Benchmarks

| Metric | [Platform 1] | [Platform 2] | [Platform 3] | Industry Avg |
|---|---|---|---|---|
| CPM | $[X] | $[X] | $[X] | $[X] |
| CPC | $[X] | $[X] | $[X] | $[X] |
| CPA | $[X] | $[X] | $[X] | $[X] |
| Conv. Rate | [X]% | [X]% | [X]% | [X]% |
| Avg. ROAS | [X.Xx] | [X.Xx] | [X.Xx] | [X.Xx] |

### Budget Scenarios

#### Starter ($1,000-$2,000/mo)
| Platform | Allocation | Monthly Spend | Est. Clicks | Est. Conversions |
|---|---|---|---|---|
| [Platform] | [X]% | $[X] | [X] | [X] |
| **Total** | **100%** | **$[X]** | **[X]** | **[X]** |

#### Growth ($3,000-$5,000/mo)
[Same table format with expanded platform mix]

#### Scale ($7,000-$10,000+/mo)
[Same table format with full platform activation]

### Break-Even Analysis

| Metric | Value |
|---|---|
| Estimated AOV / Deal Size | $[X] |
| Break-Even CPA | $[X] |
| Break-Even ROAS | [X.Xx] |
| Months to Profitability (Starter) | [X] |
| Months to Profitability (Growth) | [X] |

### Budget Key Insight
> [One-sentence biggest finding from the Budget agent]

---

## 90-Day Implementation Plan

### Month 1: Foundation & Testing (Days 1-30)

**Week 1: Setup**
- [ ] Install tracking pixels on all platforms (Meta, Google, LinkedIn)
- [ ] Set up conversion events and custom audiences
- [ ] Create landing pages for each funnel stage
- [ ] Build initial ad creative (3-5 variations per platform)

**Week 2: Launch**
- [ ] Launch TOFU campaigns on primary platform
- [ ] Launch BOFU retargeting campaigns
- [ ] Begin A/B testing ad copy and creative
- [ ] Set up daily performance monitoring

**Week 3: Optimize**
- [ ] Review first week data -- pause underperforming ads
- [ ] Adjust audience targeting based on early signals
- [ ] Launch second platform if budget allows
- [ ] Test new hooks and creative angles

**Week 4: Analyze**
- [ ] Full performance review of Month 1
- [ ] Calculate actual CPC, CPA, ROAS vs projections
- [ ] Identify winning ads, audiences, and platforms
- [ ] Plan Month 2 optimizations

### Month 2: Optimization & Expansion (Days 31-60)

- [ ] Scale winning campaigns by 20-30% budget increase
- [ ] Kill losing campaigns and reallocate budget
- [ ] Launch MOFU campaigns for warm audience nurturing
- [ ] Expand to secondary platform
- [ ] Create new creative based on Month 1 learnings
- [ ] Build lookalike audiences from converters
- [ ] Implement advanced retargeting sequences
- [ ] Test landing page variations

### Month 3: Scaling & Automation (Days 61-90)

- [ ] Increase budget to Growth tier if ROAS targets are met
- [ ] Activate full funnel across 2-3 platforms
- [ ] Implement automated rules for bid/budget management
- [ ] Launch dynamic creative optimization (DCO) campaigns
- [ ] Build customer LTV analysis from early cohorts
- [ ] Create cross-sell/upsell retargeting campaigns
- [ ] Document winning formulas for repeatable scaling
- [ ] Set 90-day review meeting to plan next quarter

---

## Quick Wins (Start This Week)

These 5 actions require minimal effort but will significantly improve ad readiness:

1. **[Specific action]** -- [Why it matters and expected impact]
2. **[Specific action]** -- [Why it matters and expected impact]
3. **[Specific action]** -- [Why it matters and expected impact]
4. **[Specific action]** -- [Why it matters and expected impact]
5. **[Specific action]** -- [Why it matters and expected impact]

---

## Next Steps

| What to Do Next | Skill | Command |
|---|---|---|
| Deep-dive audience research | Audience Persona Builder | `/ads audience [url]` |
| Generate full ad copy sets | Ad Copy Generator | `/ads copy [platform]` |
| Get 20+ scroll-stopping hooks | Hook Generator | `/ads hooks` |
| Build complete funnel blueprint | Funnel Architect | `/ads funnel [url]` |
| Full competitor ad analysis | Competitive Intelligence | `/ads competitors [url]` |
| Detailed budget projections | Budget Allocator | `/ads budget [amount]` |
| Video ad scripts | Video Script Generator | `/ads video [product]` |
| Landing page audit | Landing Page Auditor | `/ads landing [url]` |
| A/B testing plan | Testing Plan Builder | `/ads testing [campaign]` |
| Generate PDF report | PDF Report Generator | `/ads report-pdf` |
```

---

## Terminal Output

After the report is saved, display a comprehensive summary in the terminal:

```
================================================================
  AD STRATEGY COMPLETE: [Company Name]
================================================================

  Ad Readiness Score:  [XX]/100  ([Grade])

  Agent Results:
    1. Audience Research ........ COMPLETE  [XX]/100
    2. Creative Strategy ........ COMPLETE  [XX]/100
    3. Funnel Architecture ...... COMPLETE  [XX]/100
    4. Competitive Intelligence . COMPLETE  [XX]/100
    5. Budget & ROI ............. COMPLETE  [XX]/100

  Company Profile:
    Business Type:     [Type]
    Industry:          [Industry]
    Platforms:         [Platform list]
    Starting Budget:   $[X]/month
    Projected ROAS:    [X.Xx]

  Key Metrics:
    Total Personas:    [N] built
    Ad Copy Sets:      [N] variations across [N] platforms
    Hooks Written:     10 scroll-stopping hooks
    Competitors:       [N] analyzed
    Budget Scenarios:  3 (Starter / Growth / Scale)
    Break-Even CPA:    $[X]

  Top Finding:    [Most critical finding across all agents]
  Top Action:     [Single most impactful recommended action]

  Full report saved to: ADS-STRATEGY-[CompanyName].md

  Next steps:
    /ads copy [platform]    -- Generate full ad copy sets
    /ads hooks              -- Get 20+ hooks for testing
    /ads landing [url]      -- Audit the landing page
    /ads report-pdf         -- Generate client-ready PDF
================================================================
```

---

## Key Principles

- **This is the flagship skill.** The report should be thorough enough to justify a $5,000+ consulting engagement if presented as a client deliverable.
- **Parallel execution is mandatory.** All 5 agents MUST launch simultaneously to minimize total execution time. Never run them sequentially.
- **Context consistency matters.** All 5 agents receive the identical context package from Phase 1. This ensures consistency across all sections of the final report.
- **WebSearch is the data source.** Be transparent about what was found and what was estimated. Never fabricate metrics, but do provide industry benchmark ranges when exact data is unavailable.
- **Copy-paste ready.** All ad copy in the report should be ready to paste directly into the ad platform without editing. Character counts must comply with platform limits.
- **Actionable over theoretical.** Every section must end with specific actions, not vague advice. "Create a Meta campaign targeting HR managers at 500+ employee companies using lead gen objective" beats "Consider targeting your ideal audience on social media."
- **The 90-day plan must be specific.** Dates, platforms, budgets, and metrics should be concrete. The reader should know exactly what to do on Day 1, Day 7, Day 14, etc.
- **Grade honestly.** A business with a mediocre website, no tracking, and unclear pricing is NOT an A. The score must reflect reality so the action plan is credible.
- **Always end with next steps.** Guide the user to the specific individual skills that will help them execute on the strategy. The flagship report identifies what to do; the individual skills help them do it.
- **If data is limited, say so.** Mark sections as `[estimated from industry benchmarks]` or `[limited data -- verify before launch]` rather than guessing. Honest limitations build trust.
