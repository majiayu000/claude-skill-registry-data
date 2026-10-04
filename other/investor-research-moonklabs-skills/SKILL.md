---
name: investor-research
description: >
  Research VC funds/partners to provide thesis matching, portfolio analysis, and approach strategy.
  Works standalone with web search; enhanced by data tools.
  Triggers on "[VC Name] research", "[VC] research", "[Partner Name] background", "investor info",
  "[VC명] 리서치", "[VC] 조사", "[파트너명] 배경", "투자자 정보".
---

# Investor Research

Deliver complete picture of any VC fund or partner before outreach. Works standalone with web search alone; scales dramatically with data enrichment (THE VC, Innovation Forest, OpenDART).

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                   INVESTOR RESEARCH                              │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (works standalone via web search)                │
│  ✓ Fund overview: Thesis, fund size, investment stage           │
│  ✓ Portfolio analysis: key companies, sector patterns           │
│  ✓ Key partners: background, investment track record, LinkedIn  │
│  ✓ Latest news: new funds, recent investments, announcements    │
│  ✓ Thesis fit: 4-dimension rating (sector·stage·check·geo)     │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                          │
│  + ~~data enrichment: accurate fund data, full portfolio,        │
│    complete investment history                                   │
│  + ~~CRM: auto-discover intro paths from existing network,      │
│    shared portfolio mapping                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

Tell us which investor to research:

- "Research Sequoia Capital"
- "Research Marc Andreessen at Andreessen Horowitz"
- "Analyze Y Combinator thesis"
- "Check Bluepoint Partners portfolio"

Executes web search immediately. If ~~data enrichment connected, pulls from those sources as well.

---

## Connectors (Optional)

Enhance this skill by connecting tools:

| Connector | Additional Features |
|-----------|-------------------|
| **Data Enrichment** | THE VC (investment rounds, portfolio), Innovation Forest (growth metrics), OpenDART (public company filings) — web search-based, OpenDART supports MCP |
| **CRM** | Auto-discover intro paths from existing investor network |
| **Knowledge Base** | Notion, Google Drive — search team connections and intro history |

> **No connectors?** No problem. Web search alone provides thorough research on any VC.

---

## Output Format

```markdown
# Investor Research: [VC Fund Name]

**Date Generated:** [Date]
**Sources:** Web search [+ THE VC] [+ Innovation Forest] [+ CRM]

---

## Executive Summary

[2-3 sentences: who this VC is, why we're a good/bad fit, approach strategy]

---

## Thesis Fit: [HIGH / MEDIUM / LOW]

| Dimension | Rating | Details |
|-----------|--------|---------|
| **Sector** | 🟢/🟡/🔴 | [thesis, portfolio patterns] |
| **Stage** | 🟢/🟡/🔴 | [investment stage range] |
| **Check Size** | 🟢/🟡/🔴 | [typical investment amount] |
| **Geography** | 🟢/🟡/🔴 | [investment regions] |

**Overall Assessment:** [⭐⭐⭐ HIGH / ⭐⭐ MEDIUM / ⭐ LOW]

**Recommended Action:**
- [HIGH] → Prioritize outreach, secure warm intro
- [MEDIUM] → Attempt if warm intro available
- [LOW] → Lower priority or exclude

---

## Fund Profile

| Item | Value |
|------|-------|
| **Fund Name** | [Name] |
| **Website** | [URL] |
| **Founded** | [Year] |
| **HQ** | [Location] |
| **AUM** | $[X]B (estimated) |
| **Latest Fund** | [Fund X, $XM, Year] |
| **Investment Stage** | [Seed / Series A / Series B / Multi-stage] |
| **Typical Check** | $[X]M - $[X]M |
| **Portfolio** | [X] companies |

### Investment Thesis

[Summary of thesis extracted from fund website, presentations, interviews]

**Sector Focus:**
- [Sector 1] — [X portfolio companies]
- [Sector 2] — [X portfolio companies]
- [Sector 3] — [X portfolio companies]

**Stage Focus:**
- [Seed/A/B] — [X]%

**Geographic Focus:**
- [Region] — [X]%

---

## Portfolio Analysis

### Representative Companies (Top 10)

| Company | Sector | Stage | Investment Date | Similarity to Us |
|---------|--------|-------|-----------------|-----------------|
| [Company Name] | [Sector] | Series [X] | [Date] | [HIGH/MEDIUM/LOW] |

### Sector Distribution

| Sector | Portfolio Share | Representative Companies |
|--------|-----------------|--------------------------|
| [Sector 1] | [X]% | [3 companies] |
| [Sector 2] | [X]% | [3 companies] |

### Investment Patterns

**Lead vs Follow:**
- Lead investments: [X]% — [prefers lead/avoids lead]
- Follow-on: [X]%

**Portfolio Support Style:**
- [Hands-on / Hands-off]
- [Board participation rate]
- [Follow-on investment aggressiveness]

---

## Recent Activity

### Recent Investments (Last 90 Days)

| Company | Sector | Amount | Date | Why Now Signal |
|---------|--------|--------|------|----------------|
| [Company Name] | [Sector] | $[X]M | [Date] | [New fund / thesis expansion] |

### News & Announcements

- **[Headline]** — [Date] — [Why important for our outreach]
- **[Headline]** — [Date] — [Why important]

**Why Now:**
[Recent fund close, new partner hire, thesis shift, etc. → why reaching out now is good timing]

---

## Key Partners

### [Partner Name 1] — [Title]

| Item | Details |
|------|---------|
| **LinkedIn** | [URL] |
| **Background** | [Previous career, founder experience, education] |
| **Investment Focus** | [Sectors, stages] |
| **Representative Investments** | [3 companies] |
| **Tenure** | [X years] |

**Conversation Hooks:**
- [Personal hook based on background]
- [Professional hook based on investment track record]

**Approach Strategy:**
- [Warm intro path or cold angle]

---

### [Partner Name 2] — [Title]

[Same format as above]

---

## Approach Path Mapping

### 🔥 Warm Intro (Top Priority)

**Path 1: Portfolio CEO**
```
[Portfolio CEO] (similar to us) → [Partner Name]
- Contact method: [LinkedIn / Email / Existing relationship]
- Connection strength: [Strong / Moderate]
```

**Path 2: Existing Investor**
```
[Our Investor] → [Target VC]
- Co-investment history: [Company Name]
- Relationship: [Strong / Moderate]
```

**Path 3: Network**
```
LinkedIn 2nd degree: [X people]
- [Name] — [Shared background: school/company]
- [Name] — [Relationship]
```

### Cold Outreach

**Partner Email Patterns:**
- firstname@fund.com
- firstname.lastname@fund.com

**Website Submission Form:** [URL]

---

## ~~CRM Connection — Additional Information

[Our CRM history with this investor]

| Item | Details |
|------|---------|
| **Status** | [New / Previous contact / Rejected] |
| **Last Contact** | [Date and type] |
| **Past Feedback** | [If any] |
| **Owner** | [Who in team has relationship] |

---

## Competitive Investment Check

Verify if this VC has invested in our competitors:

| Competitor | Invested? | Investment Stage | Implication |
|------------|-----------|------------------|-------------|
| [Competitor A] | ✅ Yes | Series A | ⚠️ Unlikely to reinvest in same category |
| [Competitor B] | ❌ No | — | ✅ Opportunity open |

**Recommendation:**
- If invested in competitor → Partnership angle or exclude
- If not invested → "Not yet in this category" angle

---

## Recommended Outreach Angles

### Angle 1: Portfolio Similarity

"I saw you invested in [similar portfolio company]. We're also addressing [common point]..."

**Advantage:** Immediately proves thesis fit
**Disadvantage:** Could appear competitive

---

### Angle 2: Thesis Alignment

"Your thesis on '[thesis quote]' aligns perfectly with what we're doing..."

**Advantage:** Uses partner's own language
**Disadvantage:** May be too generic

---

### Angle 3: Recent Activity

"I saw [recent investment/fund close/announcement] and wanted to reach out..."

**Advantage:** Timing relevance
**Disadvantage:** Many people use same angle

---

### Angle 4: Partner Background

"I saw [Partner Name]'s [previous career/founder experience] and wanted to reach out..."

**Advantage:** Personalization, relatability
**Disadvantage:** Only applies to specific partner

---

## Next Steps

1. [ ] Is thesis fit HIGH? → Add to priority list
2. [ ] Any warm intro paths? → Write intro request message
3. [ ] No competitive investments? → Select outreach angle
4. [ ] Run `/investor-outreach [VC name]` → Create customized email
5. [ ] Update `/lead-dashboard` → Add to pipeline

---

## Sources

- [VC Website](URL)
- [THE VC: [Fund Name]](URL)
- [Next Unicorn: [Fund Name]](URL)
- [LinkedIn: [Partner Name]](URL)
- [Recent News: [Headline]](URL)
```

---

## Execution Flow

### Step 1: Analyze Request

```
Identify research target:
- "Research Sequoia Capital" → entire fund
- "Marc Andreessen at a16z" → specific partner
- "fintech seed investors in Korea" → category (route to deal-sourcing)
```

### Step 2: Web Search (Always Executed)

```
Run these searches in parallel:
1. "[VC Fund Name]" → official website, About page
2. "[VC Fund Name] thesis investment strategy"
3. "[VC Fund Name] portfolio companies"
4. "[VC Fund Name] recent investments 2024 2025"
5. "[VC Fund Name] partners team"
6. "[Partner Name] [VC] LinkedIn"
7. "[VC Fund Name] fund size AUM"
8. "[VC Fund Name] news announcements"
```

**Extract:**
- Thesis, investment focus
- Representative portfolio companies (5-10)
- Key partners (name, title, LinkedIn)
- Fund size, recent fund closes
- Recent investment announcements (last 90 days)
- Typical check size, investment stage

### Step 3: Thesis Match (4-Dimension Rating)

```
Compare our startup with VC thesis:

Dimension 1: Sector
   - Sectors explicit in VC thesis
   - Portfolio sector distribution
   - Alignment with our sector
   → 🟢 MATCH / 🟡 PARTIAL / 🔴 MISMATCH

Dimension 2: Stage
   - VC investment stage range
   - Portfolio stage distribution
   - Alignment with our current stage
   → 🟢 MATCH / 🟡 PARTIAL / 🔴 MISMATCH

Dimension 3: Check Size
   - Typical investment amount
   - Alignment with our target
   → 🟢 MATCH / 🟡 PARTIAL / 🔴 MISMATCH

Dimension 4: Geography
   - VC geographic focus
   - Alignment with our location
   → 🟢 MATCH / 🟡 PARTIAL / 🔴 MISMATCH

Overall Fit:
   - 3+ GREEN, no RED → HIGH
   - 2 GREEN, or 1 RED → MEDIUM
   - 2+ RED → LOW
```

### Step 4: Portfolio Analysis

```
Analyze portfolio companies to:
1. Identify similar companies (sector, business model)
2. Calculate sector distribution
3. Understand investment patterns (lead/follow, frequency)
4. Check for competitive investments

If similar companies found → warm intro path priority
```

### Step 5: When ~~data enrichment connected

```
From THE VC/Innovation Forest/OpenDART (web search-based, OpenDART supports MCP):
1. Investment round history, valuation (THE VC)
2. Portfolio status and investment history (THE VC)
3. Startup traffic, hiring, revenue growth metrics (Innovation Forest)
4. Public company financials, cap structure (OpenDART)
5. Exit history — IPO, M&A (OpenDART + web search)
```

### Step 6: Approach Path Mapping

```
Discover warm intro paths:
1. Portfolio connection
   - Similar company CEO → VC partner
   - LinkedIn search, email verification

2. Existing investor connection
   - Our investor → target VC
   - Co-investment history check

3. Network connection
   - LinkedIn 2nd-degree analysis
   - Shared background (school, company)

When ~~CRM or ~~knowledge base connected:
   - Auto-scan team connections
   - Search past email history
```

### Step 7: Generate Output

```
Generate research report:
1. Executive Summary
2. Thesis fit (4-dimension rating)
3. Fund profile
4. Portfolio analysis
5. Recent activity & Why Now
6. Key partner profiles
7. Approach paths
8. Recommended outreach angles
9. Next steps
```

---

## Research by Partner

When researching a specific partner:

### Information to Extract

```
1. Background
   - Previous career (founder, operator, investor)
   - Education
   - Areas of expertise

2. Investment Focus
   - Sectors they typically invest in
   - Preferred stages
   - Representative investments (3-5)

3. Investment Style
   - Hands-on / Hands-off
   - Board participation level
   - Portfolio support approach

4. Recent Activity
   - Twitter/LinkedIn posts
   - Blog, podcasts
   - Conference talks

5. Conversation Hooks
   - Shared background
   - Shared interests
   - Investment philosophy
```

### Personalization Angles

```
Angle 1: Shared Background
"I saw you were at [school/company] in [year]..."

Angle 2: Investment Philosophy
"I deeply resonate with your point in [interview/post] where you said '[quote]'..."

Angle 3: Representative Investment
"Saw you invested in [company], and we're also..."

Angle 4: Recent Activity
"[Recent tweet/post] caught my eye..."
```

---

## Korea VC Research Specialization

Additional focus when researching Korean VCs:

### Additional Data Sources

```
1. thevc.kr — Korean VC database
2. KVCA member list
3. Investment news: Platum, VentureSquare
4. LinkedIn Korea VC groups
```

### Korean VC Characteristics

```
1. Network-driven
   - Warm intro essential (cold response rate very low)
   - Personal connections, alumni networks critical

2. Government-backed funds
   - Fund-of-funds structure
   - Investment restrictions (sector, geography)

3. High CVC proportion
   - Naver, Kakao, Samsung, others
   - Strategic investment priority

4. Investment culture
   - Longer DD period (3-6 months)
   - Conditional investment (milestone-based)
   - Active follow-on investing
```

---

## Tips

1. **Portfolio reverse sourcing** — VCs investing in similar companies most relevant
2. **Use VC's thesis language** — Write outreach in language VC uses on website
3. **Find "Why Now"** — Recent fund close, new partner, similar investment = good timing
4. **Check competitive investments** — Same category re-investment rare, but partnership angle possible
5. **Tailor by partner** — Multiple partners in fund → target most relevant one
6. **Prioritize warm intros** — Portfolio CEO intro = most effective

---

## Related Skills and Commands

- **deal-sourcing** — Discover multiple investors (this skill = deep research on 1)
- **fundraise-comms** — Warm intro, cold email templates
- `/investor-outreach` — Write customized outreach based on this research
- `/deal-sourcing` — Discover multiple investors by sector/stage
- `/lead-dashboard` — Add researched investor to pipeline
