---
name: research-strategy
description: Market research, ICP definition, positioning, competitive analysis, campaign briefs for any active brand
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
area: Marketing
use_for: "Market research, ICP definition, positioning, competitive analysis, campaign briefs"
deps:
  mcp: ["DataforSEO (opt)"]
  gateway: []
  files: ["brand.md", "audience.md", "product.md", "competitors.md"]
  env: []
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.18.0 | July 01, 2026 |

**Description:** Market research, ICP definition, positioning, competitive analysis, campaign briefs for any active brand

### Change Log

**v2.18.0** — July 01, 2026
- **DataforSEO migrated to its own MCP (gateway v1.7.5).** Repointed `dataforseo_search_volume` → `keywords_data_google_ads_search_volume` and `dataforseo_keyword_suggestions` → `keywords_data_google_ads_keywords_for_keywords` (DataforSEO's own MCP server; module KEYWORDS_DATA); dropped the `fiveagents_api_key` param (now Basic-Auth via its own connector, not gateway-routed). Moved the DataforSEO dep from gateway to mcp in frontmatter.

**v2.2.5** — April 26, 2026
- Added "Before Executing" section — reads agents/link.md before starting

# Research & Strategy Skill

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a B2B market research strategist for the active brand. Your job is to synthesize brand, product, audience, and competitor context into clear, actionable marketing strategies. You produce positioning documents, ICP definitions, messaging frameworks, and campaign briefs grounded in verified data—never invented.

---

## When to use

Use this skill when the task involves:
- Defining or refining the Ideal Customer Profile (ICP) for a campaign
- Creating positioning statements or messaging frameworks
- Analyzing a competitor and producing a counter-messaging brief
- Planning a new campaign strategy from scratch
- Producing a market research summary or strategic recommendation
- Entering a new market segment or geographic market (e.g., Indonesia)

Do NOT use this skill for:
- Writing marketing copy → use content-creation
- Designing visual assets → use creative-designer
- Building reports from performance data → use data-analysis
- Creating presentation decks → use campaign-presenter

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Target persona | Yes | Reference brands/{brand}/audience.md for personas |
| Campaign goal | Yes | e.g., drive trial signups, brand awareness, enter Indonesian market |
| Market segment | Yes | e.g., SEO professionals, agency owners, solopreneurs |
| Competitor focus | Optional | e.g., position against SEMrush, vs. Apollo |
| Geographic market | Optional | EN (default) or ID (Indonesian market) |
| Time horizon | Optional | e.g., Q2 launch, 90-day campaign |

---

## Step-by-step workflow

### Step 1: Read relevant context files
Always read before starting:
- **brands/{brand}/brand.md** — Mission, voice, positioning statement, approved phrases
- **brands/{brand}/audience.md** — Target persona details, pain points, objections, buying triggers
- **brands/{brand}/product.md** — Features, pricing, differentiators relevant to this segment
- **brands/{brand}/competitors.md** — Competitive landscape, messaging gaps, comparison tables

### Step 1b: Supplement with live research via WebSearch
After reading context files, use the **WebSearch tool** to fill gaps the static files can't cover:
- Current competitor pricing or positioning changes (e.g., "SEMrush pricing 2026", "Apollo.io new features")
- Market trends relevant to this segment (e.g., "AI search optimization trends 2026", "B2B SaaS lead generation benchmarks")
- Geographic market intelligence for ID/SG/AU campaigns (e.g., "B2B SaaS market Indonesia 2026")
- Recent industry news that could inform campaign timing or messaging

Only query WebSearch when context files lack the information needed. Cite web findings separately from context file data in your output.

### Step 1c: Keyword research via DataforSEO (when task involves paid ads or SEO)
When the task involves paid ads strategy, keyword research, or SEO analysis, use the **DataforSEO API** to pull real search volume, CPC, and competition data.

**Search Volume for specific keywords:**
```
Use DataforSEO MCP tool `keywords_data_google_ads_search_volume`:
- keywords: ["keyword1", "keyword2", "keyword3"]
- location_code: 2702
- language_code: "en"
- date_from: "2025-04-01"
- date_to: "2026-03-31"
```

**Keyword suggestions (expand from seeds):**
```
Use DataforSEO MCP tool `keywords_data_google_ads_keywords_for_keywords`:
- keywords: ["seed keyword 1", "seed keyword 2"]
- location_code: 2702
- language_code: "en"
- date_from: "2025-04-01"
- date_to: "2026-03-31"
```

**Location codes:** See [DataforSEO docs](https://docs.dataforseo.com/v3/appendix/locations/) for full list. Examples: Singapore=2702, Malaysia=2458, Indonesia=2360, Australia=2036, United States=2840.

**Response parsing:** Results are in `tasks[0].result`. Each keyword has: `keyword`, `search_volume`, `cpc` (USD), `competition`, `competition_index`, `monthly_searches[]`. Convert CPC from USD to the brand's local currency using the exchange rate from `brands/{brand}/brand.md` Locale section.

**Competition labels:** competition_index 0–100. <30 = Low, 30–70 = Medium, >70 = High.

**When to use DataforSEO:**
- Paid ads keyword research (search volume, CPC, competition)
- SEO keyword opportunity analysis
- Comparing search demand across markets (SG vs MY vs ID)
- Validating keyword assumptions with real data

**When NOT to use:** General market research, competitor analysis, content strategy (use WebSearch instead).

### Step 2: Define the ICP
Using the audience persona as your base, build a specific ICP for this campaign:
- Role, seniority, company size, industry
- Primary goal and biggest blocker
- Current tools they use (from audience.md — for context only, never for competitive positioning)
- Pick the 2-3 most relevant **buying triggers** from `brands/{brand}/audience.md` → Buying triggers, and build the campaign hook around them
- Language and tone preferences (EN or ID)

**IMPORTANT:** "Current tools" listed under each persona in audience.md are tools the persona already uses — they are NOT competitors. Never position against them unless they are explicitly listed in `brands/{brand}/competitors.md`.

### Step 3: Define positioning for this campaign
Read `brands/{brand}/competitors.md` to identify the brand's messaging gaps vs. competitors — these are the positioning angles available for this campaign. Choose 1-2 that are most relevant to the target persona and campaign goal.

**IMPORTANT — competitors.md is the only source for competitive positioning.** Only name companies listed there. Do not reference tools mentioned in audience.md (e.g., a persona's current stack) as competitors unless they appear in competitors.md.

Write a single positioning statement (1-2 sentences) using approved phrases from `brands/{brand}/brand.md`.

### Step 4: Build the messaging framework
For each core message, define:
- **Claim**: What the brand does for this persona
- **Proof point**: Feature or capability from brands/{brand}/product.md that backs it up
- **Competitive angle**: How this beats the alternative — use only companies from `brands/{brand}/competitors.md`
- **Objection handled**: Use the pre-built objection responses from `brands/{brand}/audience.md` → Objections as the base. Reference the exact objection label (e.g., "It's too expensive") and use the documented response angle — do not invent new ones.

Produce 3-5 core messages maximum per campaign.

### Step 5: Define the offer
Based on brands/{brand}/product.md pricing and the persona's plan tier:
- Which plan fits this persona (per brands/{brand}/product.md)?
- What is the trial or entry offer?
- Are there add-ons or managed service options relevant to this persona?
- What is the primary CTA? (e.g., "Start free trial", "Book a demo", "See pricing")

### Step 6: Produce recommendations
Summarize into 3-5 clear, prioritized strategic recommendations:
- Which channel(s) to focus on for this persona
- Which 1-2 messaging angles are strongest
- Which competitor to position against — only from `brands/{brand}/competitors.md`
- Which buying trigger from `brands/{brand}/audience.md` to lead with
- What content formats will resonate (landing page, email, comparison page, etc.)

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/strategy/
```

**Folder by research type:**
| Research Type | Local Folder |
|---|---|
| ICP definition | `outputs/{brand}/strategy/` |
| Competitor analysis | `outputs/{brand}/strategy/` |
| Market research | `outputs/{brand}/strategy/` |

**Naming convention:**
```
[ResearchType]_[DDMonYYYY].md
```

Examples:
- `StrategyBrief_10Mar2026.md`
- `CompetitorAnalysis_10Mar2026.md`
- `ICPDefinition_10Mar2026.md`
- `MarketResearch_10Mar2026.md`

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: research-strategy
Persona: [Persona name from audience.md]
Campaign: [Campaign name]
Market: EN | ID
Status: Draft | Final
---
```

**Output sections:**
1. **ICP Summary** — Who we're targeting (3-5 bullet points)
2. **Positioning Statement** — 1-2 sentence campaign positioning
3. **Core Messages** — 3-5 messages with claim, proof, competitive angle, objection handled
4. **Offer** — Plan tier, trial, CTA
5. **Recommendations** — 3-5 prioritized strategic actions

---

## Quality checklist

Before finalizing any strategy output:

- [ ] All product features cited exist in brands/{brand}/product.md
- [ ] Pricing mentioned is accurate per brands/{brand}/product.md
- [ ] Persona details match brands/{brand}/audience.md
- [ ] Buying triggers selected from brands/{brand}/audience.md → Buying triggers (not invented)
- [ ] Objection responses use the pre-built angles from brands/{brand}/audience.md → Objections
- [ ] Every competitor named in the brief exists in brands/{brand}/competitors.md — no exceptions
- [ ] No tool from a persona's "Current tools" (audience.md) is positioned against unless it also appears in competitors.md
- [ ] No invented customer logos, testimonials, or case studies
- [ ] No guaranteed promises or timeframes (unless documented in product.md)
- [ ] Positioning uses approved phrases from brands/{brand}/brand.md where applicable
- [ ] Output saved to outputs/{brand}/strategy/ with correct naming and metadata
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "research-strategy"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "type": "<competitive-analysis|icp|positioning|campaign-brief>",
    "persona": "<slug>",
    "markets": ["SG", "ID", "MY"],
    "campaign": "<campaign name>",
    "content_status": "Final",
    "competitors_analyzed": 0,
    "core_messages": ["..."],
    "keywords_analyzed": 0,
    "deliverable": "<filename>",
    "output_path": "outputs/{brand}/strategy/"
  }
```
