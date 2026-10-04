---
name: deal-sourcing
description: >
  Guidance on investor sourcing methodology and data sources for VC, AC, angels, and CVC funds.
  Triggers on "find investors", "VC list", "find accelerator programs", "deal sourcing", "investor sourcing",
  "discover VCs", "[sector] investors", "[stage] VC",
  "투자자 찾기", "VC 리스트", "AC 프로그램 찾기", "딜소싱", "투자자 소싱", "VC 발굴".
---

# Deal Sourcing

Systematically discover new VC, AC, angel, and CVC investors. Evaluate thesis fit and map approach pathways. This skill works standalone with web search alone and scales dramatically when data enrichment tools (THE VC, Innovation Forest, OpenDART) are connected.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                       DEAL SOURCING                              │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (works standalone via web search)                │
│  ✓ Investor sourcing strategy by type (VC/AC/Angel/CVC)        │
│  ✓ 10-query web search pattern: thesis, portfolio, investment   │
│  ✓ Thesis matching framework: 4-dimensional evaluation          │
│    (sector·stage·check size·geography)                           │
│  ✓ Approach pathway mapping: warm intro / cold / accelerator    │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                          │
│  + ~~data enrichment: THE VC, Innovation Forest, OpenDART data  │
│  + ~~CRM: investor network analysis, intro path mapping         │
│  + ~~knowledge base: team docs for connections, intro history   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

Activates automatically when investor sourcing is needed:

- "Find fintech series A investors"
- "List of VCs investing in SaaS seed stage in Korea"
- "Are there accelerator programs like Y Combinator?"
- "Recommend other investors who've invested in our portfolio companies"

Executes web search immediately. If ~~data enrichment is connected, pulls data from those sources as well.

---

## Connectors (Optional)

Enhance this skill by connecting tools:

| Connector | Additional Features |
|-----------|-------------------|
| **Data Enrichment** | THE VC (investment rounds, portfolio), Innovation Forest (growth metrics), OpenDART (public company filings) — web search-based, OpenDART supports MCP connection |
| **CRM** | Existing investor network analysis, auto-map intro pathways |
| **Knowledge Base** | Notion, Google Drive — search team intro history and connection database |

> **No connectors?** No problem. Web search alone provides comprehensive investor lists and approach strategies.

---

## Output Format

```markdown
# Deal Sourcing Report: [Search Criteria]

**Search Criteria:**
- Sector: [sector]
- Stage: [stage]
- Geography: [geography]
- Check Size: $[X]-[X]

**Investors Discovered:** [X] funds/programs

---

## Results by Investor Type

### VC (Venture Capital) — [X] funds

| VC Fund | Thesis Fit | Check Size | Approach |
|---------|-----------|-----------|----------|
| [Fund Name] | ⭐⭐⭐ HIGH | $[X]-[X] | [Warm intro/Cold] |
| [Fund Name] | ⭐⭐ MEDIUM | $[X]-[X] | [Cold] |

### AC (Accelerator) — [X] programs

| Program | Application Deadline | Funding | Fit |
|---------|-------------------|---------|-----|
| [Program Name] | [Date] | $[X] + [Mentoring] | HIGH |

### Angel Investors — [X] investors

| Name | Background | Investment Track Record | Approach |
|------|-----------|---------------------|----------|
| [Name] | [Former CEO @ Company] | [Sector, X deals] | [LinkedIn 2nd connection] |

### CVC (Corporate VC) — [X] funds

| Parent Company | CVC Fund | Sector Focus | Approach |
|----------------|---------|-------------|----------|
| [Company] | [Fund Name] | [Sector] | [Cold/Partnership] |

---

## Top Targets in Detail (Thesis Fit: HIGH)

### [VC Fund Name]
**Thesis Fit:** ⭐⭐⭐ HIGH

| Dimension | Rating |
|-----------|--------|
| Sector | 🟢 MATCH — [explicit thesis, 3 portfolio companies] |
| Stage | 🟢 MATCH — [seed/A/B] |
| Check Size | 🟢 MATCH — $[X]-[X] |
| Geography | 🟢 MATCH — [geography] |

**Recent Investment:** [Company] ($[X], [Date])
**Portfolio:** [Company 1], [Company 2], [Company 3]
**Key Partners:** [Name — Title — LinkedIn]

**Approach Pathways:**
1. 🔥 Warm intro: [Portfolio CEO] → [Partner]
2. 🔥 Warm intro: [Existing investor] → [Partner]
3. Cold: [Email]

**Why Now:** [Recent fund close / Similar investment / Thesis announcement]

---

## Next Steps

1. [ ] `/investor-outreach [VC Name]` — Write customized outreach
2. [ ] Update `/lead-dashboard` — Add new targets
3. [ ] Secure warm intros — [X investors]
4. [ ] Submit accelerator applications — [Program Name, deadline [Date]]
```

---

## Execution Flow

### Step 1: Clarify Target Criteria

Analyze user request to establish criteria:

```
Required Criteria:
- Sector: [e.g., fintech, SaaS, healthcare, marketplace]
- Stage: [e.g., seed, series A, series B]

Optional Criteria:
- Geography: [e.g., Korea, US, SEA, Global]
- Check Size: [e.g., $500K-$2M, $2M-$10M]
- Investor Type: [VC, AC, Angel, CVC, All]
```

**If unclear:**
"What investor stage are you targeting? (seed, series A, series B)"
"Do you have geography preferences? (Korea, US, Southeast Asia, Global)"

### Step 2: Data Source Priority

```
Priority 1: Network (Most Effective)
   - Request intros from existing investors
   - Ask for recommendations from portfolio CEO/Founders
   - Advisor and mentor network

Priority 2: Databases
   - When ~~data enrichment connected: THE VC, Innovation Forest, OpenDART
     (web search-based, OpenDART supports MCP)
   - Without connection: Web search (10-query pattern below)

Priority 3: Reverse Sourcing
   - Find VCs investing in similar startups
   - Portfolio analysis → discover other investors

Priority 4: Events & Community
   - Demo Days, Pitch Competitions
   - VC conferences, industry events
   - LinkedIn, AngelList, ProductHunt

Priority 5: Accelerator Program Calendar
   - Y Combinator, Techstars, 500 Global
   - Korea: SparkLabs, Bluepoint, Primer
   - Track application deadlines
```

### Step 3: Web Search (10-Query Pattern)

When ~~data enrichment not connected, run these searches in parallel:

```
1. "[Sector] [Stage] venture capital firms"
   → e.g., "fintech seed venture capital firms"

2. "[Sector] investors [Geography]"
   → e.g., "SaaS investors Korea"

3. "[Stage] VC funds [Geography] 2024 2025"
   → e.g., "series A VC funds US 2024 2025"

4. "top [Sector] [Stage] investors"
   → e.g., "top healthcare seed investors"

5. "[Sector] accelerator programs [Geography]"
   → e.g., "fintech accelerator programs Asia"

6. "[Similar Startup] investors"
   → e.g., "Stripe investors" (comparable company)

7. "[Sector] angel investors [Geography]"
   → e.g., "SaaS angel investors Silicon Valley"

8. "[Sector] corporate venture capital"
   → e.g., "fintech corporate venture capital"

9. "new VC funds [Sector] 2024 2025"
   → New fund closings (abundant dry powder)

10. "[Geography] startup funding [Sector]"
    → e.g., "Korea startup funding fintech"
```

**Extract:**
- VC fund name, website
- Thesis, investment sector, stage
- Check size, fund size
- Representative portfolio companies (3-5)
- Key partners (name, title, LinkedIn)
- Recent announcements (last 90 days)

### Step 4: Thesis Matching Framework

Evaluate each investor across 4 dimensions:

```
Dimension 1: Sector
   🟢 GREEN (MATCH): explicit in thesis, portfolio shows [sector]
   🟡 YELLOW (PARTIAL): adjacent sector, broad thesis like "tech"
   🔴 RED (MISMATCH): completely different sector

Dimension 2: Stage
   🟢 GREEN: explicit match on seed/A/B
   🟡 YELLOW: adjacent stage (e.g., seed-A investor for series A)
   🔴 RED: completely different stage (e.g., growth VC for seed startup)

Dimension 3: Check Size
   🟢 GREEN: typical check aligns with request range
   🟡 YELLOW: partial overlap or unclear
   🔴 RED: too large or too small

Dimension 4: Geography
   🟢 GREEN: explicit regional coverage
   🟡 YELLOW: "Global" thesis or adjacent region
   🔴 RED: explicitly invests in different region only
```

**Overall Fit Assessment:**

```
HIGH (⭐⭐⭐):
   - 3+ dimensions GREEN
   - No RED
   → Warm intro = top priority; cold attempt if no intro

MEDIUM (⭐⭐):
   - 2 GREEN, or 1 RED
   → Try if warm intro exists; hold cold

LOW (⭐):
   - 2+ RED
   → Lower priority or exclude
```

### Step 5: Approach Pathway Mapping

Explore approach pathways for each HIGH/MEDIUM investor:

#### A. Warm Intro Pathways (Top Priority)

```
1. Portfolio Connection
   - Target VC's portfolio company CEO → VC partner
   - Search portfolio CEO on LinkedIn → check 2nd connections

2. Existing Investor Connection
   - Our existing investor → target VC
   - Check co-investment history, fund relationships

3. Network Connection
   - LinkedIn 2nd-degree analysis
   - Common background (school, previous company)
   - Advisors, mentors, board members

When ~~CRM or ~~knowledge base connected:
   - Auto-scan team member LinkedIn connections
   - Search Notion, Google Drive for intro email history
   - Analyze past meeting attendees, email CC patterns
```

#### B. Cold Outreach

```
When no warm intro available:
   - Only HIGH thesis fit → cold email
   - Partner email pattern: firstname@fund.com
   - Website "Contact" or "Founders" page
```

#### C. Accelerator Application

```
Accelerator programs:
   - Submit application (public process)
   - Track application deadlines
   - Prepare references
```

### Step 6: Priority Sorting and Output

```
Sort Order:
1. Thesis Fit HIGH + Warm Intro ⭐⭐⭐🔥
2. Thesis Fit HIGH + Cold ⭐⭐⭐
3. Thesis Fit MEDIUM + Warm Intro ⭐⭐🔥
4. Accelerator Programs (Fit HIGH)
5. Thesis Fit MEDIUM + Cold ⭐⭐

Output top 5-10 in detailed profiles
Summarize remainder in table format
```

---

## Sourcing Strategy by Investor Type

### VC (Venture Capital)

**Characteristics:**
- Professional investment fund, capital raised from LPs
- Explicit thesis, sector/stage focus
- Partner consensus required (slow decision)
- Check size $500K-$50M (depends on fund size)

**Sourcing Methods:**
- Portfolio reverse tracking (most effective)
- THE VC, Innovation Forest web search
- VC association member lists
- Web search: "[sector] [stage] VC"

**Approach Strategy:**
- Warm intro essential (cold response rate < 5%)
- Portfolio CEO intro = highest impact
- Confirm partner thesis variance

### AC (Accelerator)

**Characteristics:**
- Batch-based operation, cohort structure
- Small check + mentoring + network
- Public application process
- Demo Day connects additional investors

**Sourcing Methods:**
- "accelerator programs [sector] [geography]"
- F6S, AngelList, THE VC program database
- YC, Techstars, 500 Global (top-tier)
- Korea: SparkLabs, Bluepoint, Primer

**Application Strategy:**
- Maintain deadline calendar
- Batch timeline (typically 6 months)
- Prepare 2-3 references
- Gather traction documentation

### Angel Investors

**Characteristics:**
- Invest personal capital
- Fast decision (1-2 weeks)
- Small check ($25K-$250K)
- Personal interest, experience-driven

**Sourcing Methods:**
- AngelList, LinkedIn
- Sector-specific angel groups
- Successful founders, former executives
- Network events, Pitch Nights

**Approach Strategy:**
- Personal connection key (school, company)
- Direct LinkedIn messages
- Leverage intro culture

### CVC (Corporate VC)

**Characteristics:**
- Corporate strategic investment
- Financial + strategic objectives
- Synergy with parent business
- Complex decision (internal approvals)

**Sourcing Methods:**
- "[Parent Company] corporate venture capital"
- THE VC CVC filters
- Key companies' CVC teams by industry

**Approach Strategy:**
- Emphasize strategic value (beyond financial)
- Propose parent partnership
- Leverage BD, partnership channels

---

## Korea-Specific Deal Sourcing

### VC/AC

**Key VCs:**
- Early-stage: Primer, Bluepoint Partners, Bon Angels
- Mid-stage: Smilegate Investment, Kakao Ventures
- Growth: IMM Investment, Altos Ventures

**Key ACs:**
- SparkLabs (global network)
- Bluepoint Partners AC
- Primer
- FuturePlay

**Government Programs:**
- TIPS (Tech Incubator Program for Startup)
- K-Startup (Korean Startup Foundation)
- SME and Venture Business Promotion Corporation

### Data Sources

```
1. Associations/Organizations
   - KVCA (Korea Venture Capital Association) — member list
   - KVIC (Korea Venture Investment) — government-backed funds

2. Databases
   - thevc.kr — Korean VC investment database
   - innoforest.co.kr — startup growth metrics
   - VentureSquare — investment statistics

3. News/Media
   - Platum — investment news
   - VentureSquare — deal announcements
   - TechCrunch Korea

4. Community
   - Startup Alliance
   - D.CAMP
   - Google for Startups Campus
```

---

## Accelerator Program Calendar

Track key AC program application deadlines:

### Global Top-Tier

| Program | Batch Frequency | Application Periods | Funding |
|---------|----------------|-------------------|---------|
| Y Combinator | 2x/year (Winter/Summer) | September, March | $500K |
| Techstars | 4x/year | Rolling | $120K |
| 500 Global | 4x/year | Rolling | $150K |

### Korea

| Program | Batch Frequency | Application Periods | Funding |
|---------|----------------|-------------------|---------|
| SparkLabs | 2x/year | Rolling | $150K |
| Bluepoint AC | 2x/year | Rolling | $100K |

---

## Reverse Sourcing

Most effective deal sourcing method:

### Step 1: Identify Similar Startups

```
Comparable companies:
- Same sector
- Similar business model
- Same stage
- Similar traction

Example: Stripe → fintech B2B payments SaaS
Similar: Adyen, Square, PayPal
```

### Step 2: Discover Investors

```
THE VC, Innovation Forest, web search:
"[Similar Startup] investors"
"[Similar Startup] series A"

Extract:
- Investor list
- Investment stage
- Investment amount
- Investment date
```

### Step 3: Validate Thesis

```
Does this VC:
- Repeatedly invest in our sector → 🟢 Thesis confirmed
- Invest multiple times in similar companies → 🟢 Strong interest
- Check if lead investor or co-investor
```

### Step 4: Portfolio Connection

```
Similar company CEO → VC partner warm intro request
"Hi, I saw you invested in [Similar Company]..."
```

---

## When ~~data enrichment Connected

THE VC, Innovation Forest, OpenDART automatically available (web search-based, OpenDART supports MCP):

```
Precise Data:
- Fund size, AUM (Assets Under Management)
- Complete portfolio (more complete than web search)
- Investment history, average check size
- Partner investment focus, track record
- Fund closing date, Vintage (dry powder estimate)
- LP composition, fund strategy

Advanced Filtering:
- "VCs investing in [sector] in past 12 months"
- "Funds closed within 1 year (abundant dry powder)"
- "Investors active in [geography] at [stage]"
```

---

## Tips

1. **Portfolio reverse sourcing first** — Finding similar startup investors is most effective
2. **Maintain 3x coverage** — 3x target closing amount in pipeline (1-3% conversion)
3. **Focus on warm intros** — Cold response < 5% vs warm intro > 40%
4. **Strict thesis fit** — Invest time only in HIGH fit, MEDIUM only with warm intro
5. **Manage AC calendar proactively** — Don't miss application deadlines
6. **Source daily** — Continuous target discovery maintains healthy pipeline
7. **Korea VC is network-driven** — Personal connections, intros more critical than overseas

---

## Related Skills and Commands

- **investor-research** — Deep research on specific VC fund/partner
- **fundraise-comms** — Warm intro, cold email templates
- `/deal-sourcing` — Command version of this skill, structured output
- `/lead-dashboard` — Add discovered investors to pipeline, track
- `/investor-outreach` — Write customized outreach for specific investor
