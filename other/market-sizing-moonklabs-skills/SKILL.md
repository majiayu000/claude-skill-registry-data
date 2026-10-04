---
name: market-sizing
description: >
  TAM/SAM/SOM market size analysis and 3 methodologies (Top-down, Bottom-up, Value Theory).
  Triggers on "market size", "TAM", "SAM", "SOM", "market analysis", "total market",
  "시장 규모", "TAM", "SAM", "SOM", "시장 분석", "전체 시장".
---

# Market Sizing

> For unfamiliar placeholders or connected tools, see [CONNECTORS.md](../../CONNECTORS.md).

TAM (Total Addressable Market), SAM (Serviceable Available Market), SOM (Serviceable Obtainable Market) analysis framework. Cross-validates using 3 methodologies (Top-down, Bottom-up, Value Theory) to present compelling market opportunity to investors.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    MARKET SIZING FRAMEWORK                      │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (Standalone)                                      │
│  ✓ Calculate TAM/SAM/SOM using 3 methodologies                  │
│  ✓ Web search for industry reports and market data              │
│  ✓ Cross-validate with triangulation for confidence             │
│  ✓ Create investor-ready visual summary & assumptions doc       │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                           │
│  + ~~knowledge base: Refine Bottom-up with internal customer     │
│                      data                                        │
│  + ~~spreadsheet: Model market size scenarios                    │
│  + ~~data enrichment: Validate against competitor data           │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

1. **Basic Analysis**: "Analyze TAM/SAM/SOM for Korea B2B SaaS CRM"
2. **Specific Segment**: "What's the market size for SMB accounting SaaS?"
3. **Investor Pitch**: "Create a market sizing slide for Series A pitch"
4. **Validate**: "Verify our $5B TAM estimate"

## TAM / SAM / SOM Definition

### 3-Tier Framework

```
┌──────────────────────────────────────────────────────┐
│                   TAM (Total)                        │
│  "Everyone with this problem"                        │
│  Example: Global CRM market $50B                     │
│  ┌───────────────────────────────────────────┐       │
│  │          SAM (Serviceable)                │       │
│  │  "People we can reach"                    │       │
│  │  Example: Korea SMB CRM $500M             │       │
│  │  ┌─────────────────────────────────┐      │       │
│  │  │    SOM (Obtainable)             │      │       │
│  │  │  "Realistic capture target"     │      │       │
│  │  │  Example: 3-year goal $15M (3%) │      │       │
│  │  └─────────────────────────────────┘      │       │
│  └───────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────┘
```

### Each Tier Defined

| Tier | Definition | Key Question | Investor Focus |
|------|-----------|--------------|-----------------|
| **TAM** | Total addressable market | "If all potential customers used us?" | Is market big enough? ($1B+ preferred) |
| **SAM** | Serviceable available market | "Who can our business model reach?" | Is target realistic? |
| **SOM** | Serviceable obtainable market | "How much can we realistically capture?" | Is execution feasible? |

### Typical Ratios
- **SAM**: 10-50% of TAM (geography, segment, channel constraints)
- **SOM**: 2-10% of SAM (3-5 year goal, competition considered)

**Example** (Global SaaS CRM):
- TAM: $50B (all enterprises worldwide)
- SAM: $5B (Korea + SMB + cloud-based)
- SOM: $150M (5-year 3% market share goal)

---

## 3 Methodologies

### Methodology Comparison

| Methodology | Approach | Advantages | Disadvantages | Best For |
|------------|----------|-----------|----------------|----------|
| **Top-down** | Market → Segment | Fast, uses reports | Many assumptions, over-estimates | Mature market, initial estimates |
| **Bottom-up** | Unit economics → Aggregate | Accurate, realistic | Data-heavy, time-consuming | Validated Unit Economics |
| **Value Theory** | Customer value creation | Fits new markets, differentiates | Subjective, hard to prove | New categories, 10x products |

**Recommendation**: Execute all 3, then cross-validate (Triangulation)

### 1. Top-down (Top to Bottom)

#### Process

```
Entire market size
    ↓ Region filter (example: Korea = 2% of global)
Korea market size
    ↓ Segment filter (example: SMB = 60%)
Target segment
    ↓ Adoption rate (example: cloud conversion = 40%)
SAM
    ↓ Market share target (example: 5% in 5 years)
SOM
```

#### Calculation Example (CRM SaaS)

1. **TAM**: Global CRM market = $50B (Gartner 2024)
2. **Region Filter**: Korea = 2% of global = $1B
3. **Segment**: SMB (10-500 employees) = 60% = $600M
4. **Channel**: Cloud-based = 70% = **$420M (SAM)**
5. **Market Share**: 5-year goal 5% = **$21M (SOM)**

#### Data Sources
- **Global**: Gartner, IDC, Forrester, Statista, Grand View Research
- **Korea**: Korean IT Industry Association (KAIT), KISA, Statistics Korea
- **Free Alternative**: Public company IR, industry association reports, CB Insights

#### Cautions
- **Avoid Over-estimation**: Conservative filter at each step
- **Use Current Data**: 2-3 year old reports, adjust for growth
- **Confirm Definitions**: "CRM" scope varies by report

### 2. Bottom-up (Bottom to Top)

#### Process

```
Unit economics
 (Revenue per customer)
    ↓ × Target customer count
Potential revenue
    ↓ × Realistic reach rate
SAM
    ↓ × Conversion rate
SOM
```

#### Calculation Example (Accounting SaaS for SMB)

**Step 1: Target Customer Count**
- Korea SMB (10-100 employees): 150,000 (Statistics Korea)
- Current accounting software users: 80% = 120,000
- Cloud conversion intent: 50% = **60,000 (TAM customers)**

**Step 2: Customer Revenue**
- ARPA (Average Revenue Per Account): ₩300K/month
- Annual: ₩3.6M per customer

**Step 3: TAM Calculation**
- 60,000 × ₩3.6M = **₩216B (~$180M)**

**Step 4: SAM (Reachable)**
- Sales team can cover: 30% = 18,000 customers
- SAM = 18,000 × ₩3.6M = **₩64.8B ($54M)**

**Step 5: SOM (5-year target)**
- Target share: 5% = 900 customers
- SOM = 900 × ₩3.6M = **₩3.24B ($2.7M ARR)**

#### Data Sources
- **Customer Count**: Statistics Korea, SME Office, industry associations
- **ARPA**: Competitor disclosures, beta customer data, pricing pages
- **Conversion**: Own funnel data, benchmarks (Seed: 1-3%, Series A: 5-10%)

#### Advantages
- **Verifiable**: Each step backed by data
- **Connects to Execution**: SOM reverse-calculates needed customers
- **Investor Trust**: Specific, credible narrative

### 3. Value Theory (Value-Based)

#### Process

```
Current solution cost
    ↓ - Our product cost
Savings (or added value)
    ↓ × Total customer count
TAM
    ↓ × Adoption target %
SOM
```

#### Calculation Example (AI Recruiting Platform)

**Step 1: Current Cost**
- Avg SMB recruiting cost: ₩5M per hire (20% agency fee)
- Avg hires/year: 5
- Annual recruiting cost: ₩25M/business

**Step 2: Our Value**
- Reduce agency fee 80%: -₩4M
- Save HR time 50%: -₩1.2M
- Reduce bad hires 30%: -₩1.5M
- Total savings: ₩7.5M/year

**Our subscription**: ₩1.2M/year
- **Net savings**: ₩6.3M/year
- **ROI**: 525%

**Step 3: Willingness to Pay**
- Customers pay 10-30% of savings: 30% = ₩1.9M
- Our price ₩1.2M is 63% of willingness → attractive

**Step 4: TAM**
- Target: 50,000 SMBs
- TAM = 50,000 × ₩1.2M = **₩600B (~$50M)**

**Step 5: SOM**
- 5-year adoption: 10% (existing solution replacement)
- SOM = 5,000 customers × ₩1.2M = **₩300B ($25M ARR)**

#### When to Use
- **New Categories**: No existing market data
- **10x Innovation**: Revolutionary product
- **B2B ROI**: Clear cost savings narrative

#### Cautions
- **Validate Assumptions**: "80% savings" proven with beta customer data
- **Consider Alternatives**: Free/low-cost competing options
- **Behavior Change**: Value exists, but conversion may be slow

---

## Cross-Validation (Triangulation)

### Why It's Needed

- **Top-down**: Tends to over-estimate
- **Bottom-up**: Tends to under-estimate (conservative)
- **Value Theory**: Subjective, hard to prove

→ **3 results in similar range = high confidence**

### Validation Process

1. **Run 3 Methodologies Independently**
   - Don't let one result influence another

2. **Compare Results**
   ```
   | Methodology | TAM | SAM | SOM (5-year) |
   |--------|-----|-----|-----------|
   | Top-down | $200M | $50M | $5M |
   | Bottom-up | $180M | $45M | $3M |
   | Value Theory | $250M | $60M | $6M |
   | **Average** | **$210M** | **$52M** | **$4.7M** |
   | **Range** | ±15% | ±14% | ±29% |
   ```

3. **Assess Consistency**
   - **±20% or less**: Confident → use average
   - **±20-50%**: Medium confidence → review assumptions
   - **±50%+**: Low confidence → re-run methodology

4. **Choose Conservative Value**
   - **Investor**: Mid-range or lower 25%
   - **Internal Plan**: Upper range as stretch goal

### Example: Analysis Difference

**Bottom-up ($45M SAM) vs Top-down ($50M SAM) – Why?**:
- Top-down: "SMB" in report includes up to 500 employees
- Bottom-up: We target only 10-100 employees
- **Conclusion**: Bottom-up is more accurate; adjust Top-down assumptions

---

## Investor Presentation

### Slide Structure (1 Page)

```markdown
# Market Opportunity

## TAM / SAM / SOM

┌──────────────────────────────────────────┐
│  TAM   $200M   Korea SMB Accounting SaaS │
│    ↓                                      │
│  SAM    $50M   10-100 employees, cloud   │
│    ↓                                      │
│  SOM     $5M   5-year 10% market share   │
└──────────────────────────────────────────┘

### Methodology (Cross-Validated)
✓ Top-down: Gartner market report basis
✓ Bottom-up: 60,000 targets × ₩3.6M ARPA
✓ Value Theory: ₩6.3M/year savings basis

### Growth Drivers
• Cloud migration acceleration (15% annual)
• Digital tax invoice mandate (2025)
• SMB automation demand increase
```

### Investor Red Flags vs Green Lights

| Check | RED FLAG 🔴 | GREEN LIGHT 🟢 |
|-------|------------|-----------------|
| **TAM Size** | <$500M | >$1B |
| **SAM Logic** | "Everyone" | Clear segment definition |
| **SOM Basis** | "We'll take 10%" | Unit economics reverse-calc |
| **Growth Rate** | Flat market | 10%+ annual growth |
| **Competition** | Saturated | Fragmented or new |
| **Methodology** | 1 only | 2-3 cross-validated |

### Common Mistakes

❌ **Over-estimation**
- "Global $500B market, we'll take 1% = $5B"
- → Why 1%? How? Plan not shown

❌ **TAM = SAM**
- Ignores geography, segment, channel constraints
- → "Only Seoul, 3 districts" coverage missed

❌ **Static Market**
- Current size only, no growth rate
- → What about market in 5 years?

❌ **Single Methodology**
- Top-down only → unverified
- → Use minimum 2, ideally 3

✅ **Good Example**
```
TAM: $2B (2024) → $4B (2029, 15% CAGR)
SAM: $500M (Korea + SMB + SaaS 40% adoption)
SOM: $25M (5-year 5% market share)

Evidence:
• Top-down: Gartner report
• Bottom-up: 60K accounts × ₩5M ARPA
• Beta customer validation: ₩4.8M actual ARPA (±4%)
```

---

## By Business Model

### SaaS

**TAM Calculation Basis**:
- Total target customers (companies or people)
- ARPA × customer count
- Existing legacy solution market size

**Key Assumptions**:
- Cloud migration rate (on-premise → SaaS)
- Adoption rate (manual/Excel → software)
- ARPA (price per tier × mix)

**Example**:
- TAM = 100K companies × $500/month × 12 = $600M

### Marketplace

**TAM Calculation Basis**:
- Total transaction value (GMV) × Take Rate
- OR: Offline market online conversion

**Key Assumptions**:
- Online penetration rate (e.g., 20% of used car sales)
- Take rate (10-30%, category-specific)
- Transaction frequency

**Example**:
- Korea used car sales: ₩45 trillion
- Online conversion: 20% = ₩9 trillion GMV
- Take rate: 3% → TAM = ₩270B

### Consumer

**TAM Calculation Basis**:
- Total target users × ARPU
- OR: Replace offline spending

**Key Assumptions**:
- Target demographic size
- Smartphone adoption (mobile apps)
- Monetization willingness (subscription, IAP, ads)

**Example** (Fitness app):
- Korea 20-50 age exercise population: 10M
- App usage intent: 10% = 1M
- ARPU: ₩5,000/month → TAM = ₩600B/year

### B2B Enterprise

**TAM Calculation Basis**:
- Account count (enterprises) × ACV
- OR: IT budget category share

**Key Assumptions**:
- ICP filters (industry, employee count, revenue)
- ACV (SMB <$50K, Mid $50-250K, Ent >$250K)
- Buying committee existence

**Example**:
- Korea manufacturing (500+ employees): 2,000
- IT budget ₩1B × 5% (our category) = ₩50M
- TAM = 2,000 × ₩50M = ₩100B

---

## Execution Flow

1. **Collect Input**
   - Product description
   - Target customer (region, segment)
   - Pricing model (ARPA or ACV)
   - Competitors (if known)

2. **Web Research** (10-15 queries)
   - "Korea [industry] market size 2024"
   - "[category] global market size forecast"
   - "Number of [target customers] in [region]"
   - "[competitor] revenue ARR"
   - "ARPA benchmark [industry]"

3. **Top-down Calculation**
   - Find global/Korea market size
   - Apply filters (geography → segment → channel)
   - TAM → SAM → SOM

4. **Bottom-up Calculation**
   - Define target customer count
   - Set ARPA
   - Apply reach and conversion rates

5. **Value Theory** (optional)
   - Current solution cost vs our price
   - Savings or value addition
   - Willingness to pay validation

6. **Cross-Validate**
   - Compare 3 results
   - If ±20% range: use average
   - If wider: recheck assumptions

7. **Create Output**
   - Investor slide (1 page)
   - Assumptions doc (detailed calculation)
   - Data sources cited

---

## Connected Tools

| Tool Category | Placeholder | Use Case | Example Tools |
|---------------|-------------|----------|----------------|
| Knowledge Base | `~~knowledge base` | Validate ARPA with internal customer data | Notion, Confluence |
| Spreadsheet | `~~spreadsheet` | Model market scenarios | Google Sheets, Excel |
| Data Enrichment | `~~data enrichment` | Verify against competitor data | THE VC, Innovation Forest, OpenDART |
| CRM | `~~CRM` | Extract actual conversion data | Relate, HubSpot |

---

## Related Skills

- **startup-metrics**: Set metrics to achieve SOM
- **financial-modeling**: Embed market sizing into revenue forecast
- **competitive-landscape**: Analyze competition within market
- **gtm-strategy**: Select GTM motion for SAM reach

---

## Tips

- **Conservative Assumptions**: Investors always suspect over-optimism; downside estimates build credibility
- **Growth Markets Preferred**: Stagnant market < 10%+ growth
- **Do All 3 Methods**: 1 method = "not validated" impression; minimum 2, ideally 3
- **Cite Data Sources**: "Gartner 2024", "Statistics Korea 2023" — specifics matter
- **Document Definitions**: "SMB = 10-100 employees" — be explicit
- **Reverse-Check SOM**: $5M SOM ÷ $50K ACV = 100 customers needed. Realistic? Check.
- **Market vs Us**: TAM is market; SOM is us. Don't confuse.
- **Korea Adjustments**: Korea market smaller, lower ACV, slower adoption than US → calibrate

**Detailed Methodology**: See [references/methodology-guide.md](references/methodology-guide.md)
