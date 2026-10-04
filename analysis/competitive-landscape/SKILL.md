---
name: competitive-landscape
description: >
  Competitive landscape analysis, positioning strategy, and battlecard development.
  Triggers on "competitive analysis", "competitors", "positioning", "differentiation", "competitive advantage", "battlecard",
  "경쟁 분석", "경쟁사", "포지셔닝", "차별화", "경쟁 우위", "배틀카드".
---

# Competitive Landscape

> For unfamiliar placeholders or connected tools, see [CONNECTORS.md](../../CONNECTORS.md).

Strategic competitive analysis and positioning framework. Uses Porter's 5 Forces, Blue Ocean 4-Actions, and positioning matrices to secure a unique market position and arm sales teams with battlecards.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                 COMPETITIVE LANDSCAPE ANALYSIS                   │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (Standalone)                                      │
│  ✓ Web search to discover competitors and collect intel          │
│  ✓ Porter's 5 Forces industry structure analysis                │
│  ✓ Positioning matrix (4 strategic patterns)                     │
│  ✓ Auto-generate battlecards (strengths/weaknesses/tactics)     │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                           │
│  + ~~data enrichment: Auto-collect competitor funding, revenue, │
│                       team size                                   │
│  + ~~knowledge base: Extract insights from Win/Loss interviews  │
│  + ~~CRM: Analyze competitor frequency and win rates in deals   │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

1. **Industry Structure**: "Analyze competitive intensity in Korea's SaaS CRM market"
2. **Competitor Mapping**: "Find and compare our top 5 competitors"
3. **Positioning**: "Suggest a differentiated positioning strategy for us"
4. **Battlecards**: "Build a battlecard against Salesforce"

## Competitive Analysis Framework

### 1. Competitor Discovery & Tier Classification

#### 4-Tier Framework

```
Tier 1: Primary Competitors (Direct competition)
 - Same ICP, same problem, same solution
 - Example: We = SMB CRM → Pipedrive, Zoho

Tier 2: Secondary Competitors (Indirect competition)
 - Different approach, same problem solved
 - Example: Spreadsheets, general SaaS

Tier 3: Emerging Competitors (New entrants)
 - Rapid growth, new market entry
 - Example: Recent Y-Combinator cohort

Tier 4: Alternatives (Substitutes)
 - Different category, partial feature overlap
 - Example: Email, manual workarounds, outsourcing
```

#### Competitor Discovery Web Search Patterns

**10-Query Research**:
1. "[Category] top competitors"
2. "[Our product] alternatives"
3. "best [category] for [ICP]"
4. "[Problem] solutions"
5. "[Competitor A] vs [Competitor B]" (comparison articles)
6. "THE VC [category] startups"
7. "[Region] [category] companies"
8. "G2 [category] reviews"
9. "[VC firm] portfolio [category]"
10. "Product Hunt [category] launches"

#### Tier Classification Criteria

| Factor | Primary (Tier 1) | Secondary (Tier 2) | Emerging (Tier 3) | Alternatives (Tier 4) |
|--------|------------------|--------------------|--------------------|------------------------|
| **ICP Overlap** | >70% | 30-70% | >70% (future) | <30% |
| **Feature Overlap** | >80% | 50-80% | >80% | <50% |
| **Deal Overlap** | >50% | 20-50% | <20% | <10% |
| **Market Share** | Top 5 | Top 10-20 | New (<1%) | Different category |
| **Monitoring Frequency** | Weekly | Monthly | Quarterly | Annually |

### 2. Porter's 5 Forces Analysis

#### Framework

```
┌──────────────────────────────────────────────────┐
│         Threat of New Entrants (Barriers)        │
│              ↓ (High/Medium/Low)                 │
│                                                  │
│  Bargaining Power ←─→ [Market Competition] ←─→ Bargaining│
│  of Suppliers                               of Buyers│
│  (Supplier Power)                           (Buyer Power)│
│                                                  │
│              ↑ (High/Medium/Low)                 │
│       Threat of Substitutes (Alternatives)       │
│                                                  │
│         Competitive Rivalry (Intensity)          │
│         ↓ Overall Score: High/Medium/Low        │
└──────────────────────────────────────────────────┘
```

#### Each Force Evaluation

**1. Competitive Rivalry (Market Intensity)**

| Factor | High (Unfavorable) | Medium | Low (Favorable) |
|--------|-------------------|--------|-----------------|
| Market growth | <5%/year | 5-15% | >15% |
| Number of competitors | >20 | 5-20 | <5 |
| Differentiation | Low (Commodity) | Medium | High (Unique) |
| Switching costs | Low | Medium | High |
| Customer concentration | Distributed | Medium | Concentrated |

**Point Example** (Korea CRM market):
- Market growth: 12%/year → Medium
- Competitors: 15 → Medium
- Differentiation: Unique AI → Medium-High
- Switching costs: Medium → Medium
- **Overall**: Medium-High Rivalry

**2. Threat of New Entrants (Entry Barriers)**

| Factor | High Barrier (Favorable) | Medium | Low Barrier (Unfavorable) |
|--------|--------------------------|--------|---------------------------|
| Capital required | >$10M | $1-10M | <$1M |
| Regulation | Strong (licensing) | Medium | Weak |
| Brand power | Strong market leader | Medium | New market |
| Network effects | Strong | Medium | None |
| Switching costs | High (Lock-in) | Medium | Low |

**Point Example**:
- Capital: SaaS <$1M possible → Low
- Regulation: None → Low
- Brand: Salesforce dominance → High
- Network: CRM is weak → Low
- **Overall**: Low-Medium Barrier (high threat)

**3. Bargaining Power of Buyers (Customer Power)**

| Factor | High Power (Unfavorable) | Medium | Low Power (Favorable) |
|--------|--------------------------|--------|----------------------|
| Buyer concentration | Top 3 = 50%+ | Medium | Distributed |
| Switching costs | Low | Medium | High |
| Information transparency | High (easy to compare) | Medium | Low |
| Price sensitivity | High | Medium | Low (value-focused) |
| Backward integration | Possible (in-house) | Difficult | Impossible |

**4. Bargaining Power of Suppliers (Vendor Power)**

SaaS/Software typically **Low** (labor and cloud infrastructure are replaceable)

**5. Threat of Substitutes (Alternatives)**

| Factor | High Threat (Unfavorable) | Medium | Low Threat (Favorable) |
|--------|---------------------------|--------|----------------------|
| Alternative performance | Similar or superior | Slightly inferior | Much inferior |
| Price | Cheaper | Similar | More expensive |
| Ease of switching | Easy | Medium | Difficult |

**Example** (CRM):
- Alternatives: Excel, Google Sheets, email
- Performance: CRM superior → Low
- Price: Free vs paid → High
- **Overall**: Medium Threat

#### Porter's 5 Forces Summary Output

```markdown
# Porter's 5 Forces: Korea CRM Market

## Overall Score
**Market Attractiveness**: Medium (⚠️ Caution)

| Force | Score | Status | Key Reason |
|-------|------|--------|-------------|
| Competitive Rivalry | High | 🔴 | 15 competitors, low differentiation |
| Threat of New Entrants | Medium | 🟡 | Low capital, brand barriers |
| Buyer Power | High | 🔴 | Low switching costs, price-sensitive |
| Supplier Power | Low | 🟢 | Replaceable infrastructure |
| Threat of Substitutes | Medium | 🟡 | Free alternatives (Sheets) available |

## Strategic Implications
1. **Differentiation Required**: Feature parity insufficient; create 10x value via AI/automation
2. **Strengthen Lock-in**: Data integration, workflow automation to increase switching costs
3. **Niche Focus**: Target specific vertical (e.g., manufacturing) rather than general market
```

### 3. Positioning Strategy: 5 Patterns

#### Positioning Matrix

```
         High Feature Overlap
                │
      ────────────────────────
      │         │             │
      │ Head-   │   Niche     │
      │ to-Head │             │
Broad ├─────────┼─────────────┤ Focused
ICP   │ Reframe │  Leapfrog   │  ICP
      │         │             │
      └─────────┴─────────────┘
                │
          Low Feature Overlap
```

#### Pattern 1: Head-to-Head (Direct Competition)

**When to choose**:
- Market leader has weaknesses (legacy, slow innovation)
- We have capital/brand competitive advantage
- Feature parity + price advantage

**Examples**:
- Zoom vs Skype (better UX, cheaper)
- Notion vs Confluence (simpler, faster)

**Risks**:
- Price competition → margin pressure
- Brand battle is uphill

**Strategy**:
- "Better, Faster, Cheaper" — pick 2+ attributes
- Switching Program (free legacy data migration)

#### Pattern 2: Niche (Specialization)

**When to choose**:
- Unique domain expertise in vertical/ICP
- General solutions miss specific needs

**Examples**:
- Veeva (pharmaceutical CRM) vs Salesforce
- Toast (restaurant POS) vs Square

**Advantages**:
- High win rates (acknowledged expertise)
- Premium pricing
- Strong word-of-mouth

**Strategy**:
- "Salesforce for [Vertical]"
- Industry-specific workflow templates
- Sponsor vertical conferences

#### Pattern 3: Reframe (Category Redefinition)

**When to choose**:
- Define same problem differently
- Different value proposition vs competitors

**Examples**:
- Slack: "Email killer" → "Team communication hub"
- Airbnb: "Hotel replacement" → "Local experiences"

**Strategy**:
- Create new category ("We're not CRM, we're Revenue Operations Platform")
- Target different buying center (IT → Sales Ops)

#### Pattern 4: Leapfrog (Leap Forward)

**When to choose**:
- 10x innovation tech (AI, Automation)
- Incumbent is legacy

**Examples**:
- Tesla vs internal combustion (electric cars)
- ChatGPT vs Google Search (AI-powered answers)

**Risks**:
- Market education costs high
- Adoption curve slow

**Strategy**:
- "Next Generation [Category]"
- Thought leadership (blogs, conferences)

#### Pattern 5: Coexist (Complement)

**When to choose**:
- Not replacement, but complement
- Integration/add-on strategy

**Examples**:
- Gong (revenue intelligence on Salesforce)
- Zapier (connects all SaaS)

**Strategy**:
- Emphasize "Works with [Leader]"
- Marketplace/App Store strategy

### 4. Battlecard (Sales Enablement)

#### Battlecard Structure

```markdown
# [Competitor Name] Battlecard

## 📊 Basic Info
- **Company**: [Name]
- **Founded**: [Year]
- **Funding**: $[Amount] ([Round])
- **Customer Base**: [Number]
- **Target ICP**: [Segment]
- **Pricing**: $[ARPA]/month

## 🎯 When We Meet Them
- Deal Type: [SMB/Mid/Ent]
- Frequency: [%] of deals
- Win Rate vs Them: [%]

## 💪 Competitor Strengths
1. **[Strength 1]**: [Details]
   - Our Response: [Tactic]
2. **[Strength 2]**: [Details]
   - Our Response: [Tactic]

## ⚠️ Competitor Weaknesses
1. **[Weakness 1]**: [Details]
   - Attack Point: [Question/Demo]
2. **[Weakness 2]**: [Details]
   - Attack Point: [Question/Demo]

## 🏆 Our Differentiation
1. **[Differentiator 1]**: [Evidence/Data]
2. **[Differentiator 2]**: [Evidence/Data]
3. **[Differentiator 3]**: [Evidence/Data]

## 🗣️ Customer Objections & Responses
**"[Competitor] is more famous?"**
→ [Response]

**"[Competitor] is cheaper?"**
→ [Response]

## 📚 Resources
- Case Study: [Link]
- Head-to-Head Comparison: [Link]
- Win Story: [Customer]
```

#### Battlecard Example

```markdown
# Salesforce Battlecard

## 📊 Basic Info
- **Company**: Salesforce
- **Founded**: 1999
- **Funding**: Public company (Market Cap $200B+)
- **Customer Base**: 150,000+
- **Target ICP**: Enterprise (1,000+ employees)
- **Pricing**: $150-300/user/month

## 🎯 When We Meet Them
- Deal Type: Mid-Market, Enterprise
- Frequency: 60% of deals (market leader)
- Win Rate vs Salesforce: 35%

## 💪 Salesforce Strengths
1. **Brand**: "CRM = Salesforce" perception
   - Our Response: "Enterprise overkill for SMB; we're right-sized"
2. **AppExchange**: 3,000+ integrations
   - Our Response: "Top 20 integrations covered; 2,980 are unused"
3. **Enterprise Features**: Complex workflows
   - Our Response: "Complexity is poison for SMB; 5-minute setup vs their 45-minute video"

## ⚠️ Salesforce Weaknesses
1. **Price**: $150+/user (SMB burden)
   - Attack: "₩3.6M annually (20 users) vs us ₩1.2M. 3x difference"
2. **Complexity**: Admin required (training cost)
   - Attack: "Can you run without dedicated admin?" (demo 30-second setup)
3. **Implementation**: 3-6 months (consulting needed)
   - Attack: "When do you actually start using it? We're 1 week"

## 🏆 Our Differentiation
1. **SMB Optimized**: $50/user (1/3 price)
2. **Instant Deployment**: 5-minute onboarding, no consulting
3. **Korean Support**: 100% Korean UI, customer support

## 🗣️ Customer Objections & Responses
**"Salesforce is more famous?"**
→ "True. But Ferrari isn't right for everyone. For 20-person teams, we're the 'national car' — 70% of our customers switched from Salesforce and never looked back."

**"Won't we need Salesforce later as we grow?"**
→ "No. We have 200-person clients. We support custom workflows and APIs when needed, but keep complexity low. You won't outgrow us."

## 📚 Resources
- Case Study: [Company] Salesforce → Us (60% cost savings)
- Comparison: Salesforce vs Us
- Demo: 5-minute onboarding vs Salesforce 45-minute video
```

### 5. Blue Ocean 4-Actions Framework

#### Framework

```
┌────────────────────┬────────────────────┐
│   Eliminate        │   Raise            │
│ (Remove Standards) │ (Raise Above)      │
│                    │                    │
│ - [Element 1]      │ - [Element 1]      │
│ - [Element 2]      │ - [Element 2]      │
├────────────────────┼────────────────────┤
│   Reduce           │   Create           │
│ (Below Industry)   │ (New Elements)      │
│                    │                    │
│ - [Element 1]      │ - [Element 1]      │
│ - [Element 2]      │ - [Element 2]      │
└────────────────────┴────────────────────┘
```

#### Example (SMB CRM)

| Eliminate | Raise |
|-----------|-------|
| • Admin console (complexity) | • Mobile UX |
| • Consulting service requirement | • Korean support quality |
| • Minimum user count enforcements | • AI automation |

| Reduce | Create |
|--------|--------|
| • Implementation time (6 months → 1 week) | • KakaoTalk integration alerts |
| • Price ($150 → $50) | • Free tier (5 users) |
| • Onboarding training (3 days → 30 mins) | • SMB-specific templates |

### 6. Win/Loss Analysis

#### Win Analysis (Why We Won)

```markdown
## Win: [Customer Name]
**Deal Size**: $[Amount]
**Competed Against**: [Competitor]
**Win Reasons**:
1. [Key Reason 1] (40%)
2. [Key Reason 2] (35%)
3. [Key Reason 3] (25%)

**Customer Quote**:
"[Actual feedback]"
```

#### Loss Analysis (Why We Lost)

```markdown
## Loss: [Project Name]
**Deal Size**: $[Amount]
**Won By**: [Competitor]
**Loss Reasons**:
1. [Key Reason 1] (50%) → Improvement Plan: [Action]
2. [Key Reason 2] (30%) → Improvement Plan: [Action]
3. [Key Reason 3] (20%)

**Lesson Learned**:
[Team insight]
```

#### Pattern Analysis

**Quarterly Win/Loss Review**:
```
Total Deals: 50
Won: 20 (40%)
Lost: 15 (30%)
No Decision: 15 (30%)

Top 3 Win Reasons:
1. Price (60%)
2. Ease of use (45%)
3. Korean support (30%)

Top 3 Loss Reasons:
1. Brand awareness (50%)
2. Feature gaps (40%)
3. Integration limits (25%)

→ Action: Increase brand marketing, prioritize [Feature X], expand integrations
```

## Output Format

### Competitive Environment Summary

```markdown
# [Market Name] Competitive Landscape

## Market Structure
- **Market Attractiveness**: Medium (Porter's 5 Forces)
- **Competitive Intensity**: High (15 competitors, low differentiation)
- **Entry Barriers**: Low (new entrant threat)

## Key Competitors (Tier 1)

| Competitor | Target ICP | Strength | Weakness | Win Rate vs Us |
|------------|-----------|----------|----------|-----------------|
| Vendor A | Enterprise | Brand | Price | 35% |
| Vendor B | SMB | Price | Features | 60% |
| Vendor C | Mid-Market | Integration | UX | 50% |

## Our Positioning
**Strategy**: Niche (manufacturing SMB specialization)

**Differentiation**:
1. AI inventory forecasting (unique)
2. Korean ERP integration (Dasan, Yeourim)
3. ₩50/user (half market average)

**Target**: 50-200 employee manufacturers (4,000 TAM)

## Battlecards
- [Vendor A Battlecard](link)
- [Vendor B Battlecard](link)
- [Vendor C Battlecard](link)

## Win/Loss Insights
- Wins: Price (60%), UX (45%)
- Losses: Brand (50%), Features (40%)
- **Action**: Increase brand marketing, prioritize [Feature X]
```

## Execution Flow

1. **Discover Competitors**: 10-query web search pattern
2. **Tier Classification**: Primary/Secondary/Emerging/Alternatives
3. **Porter's 5 Forces**: Market attractiveness evaluation
4. **Positioning Choice**: Select from 5 strategic patterns
5. **Generate Battlecards**: Tier 1 competitors each
6. **Win/Loss Analysis**: Quarterly pattern tracking
7. **Update**: Monthly competitive monitoring

## Connected Tools

| Tool Category | Placeholder | Use Case | Example Tools |
|---------------|-------------|----------|----------------|
| Data Enrichment | `~~data enrichment` | Competitor funding, growth metrics | THE VC, Innovation Forest, OpenDART |
| Knowledge Base | `~~knowledge base` | Store Win/Loss interviews | Notion, Confluence |
| CRM | `~~CRM` | Deal-level competitor frequency & win rate | Relate, HubSpot |
| Sales Tools | (~~knowledge base) | Distribute battlecards | Klue, Crayon |

## Related Skills

- **market-sizing**: Set our point-of-share target vs competitors
- **gtm-strategy**: Choose GTM motions that align with positioning
- **sales-playbook**: Integrate battlecards into sales process
- **pitch-craft**: Reflect competitive advantage in pitch deck

## Tips

- **Focus on Tier 1**: Can't track all competitors; concentrate on top 3-5
- **Keep Battlecards Alive**: Quarterly updates, real deal feedback
- **Win/Loss Is Sacred**: Most honest feedback; track patterns and adjust
- **Monitor Continuously**: G2 reviews, blogs, job postings (strategy hints)
- **Messaging Consistency**: Website, pitch, sales talk — all same story
- **Avoid Competition**: Sometimes "we're not a [competitor] replacement, we're a new [category]" is stronger
- **Sustainable Advantage**: Short-term feature advantage weak; network effects, data, brand are durable
- **Customer Lens**: Focus on "solving customer problem better" not "we're better than them"
