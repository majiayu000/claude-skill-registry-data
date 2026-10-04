---
name: pricing-strategy
description: >
  Pricing strategy and packaging guidance — pricing models, value metrics, psychology, packaging.
  Triggers on "pricing", "pricing tiers", "packaging", "value metric", "price setting",
  "가격 전략", "가격 책정", "패키징", "가치 지표", "요금 결정".
---

# Pricing Strategy

> For unfamiliar placeholders or connected tools, see [CONNECTORS.md](../../CONNECTORS.md).

SaaS pricing strategy framework. Covers pricing models, value metric selection, psychology tactics, Good/Better/Best packaging, and feature fencing to optimize customer value and revenue.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRICING STRATEGY FRAMEWORK                    │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (Standalone)                                      │
│  ✓ Recommend pricing model based on business type               │
│  ✓ Evaluate value metric on 4 criteria (explain/align/predict)  │
│  ✓ Design Good/Better/Best 3-tier packaging                     │
│  ✓ Apply pricing psychology (Anchoring, Decoy, Charm)           │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (with tool connections)                           │
│  + ~~analytics: Validate metrics with customer usage data        │
│  + ~~CRM: Analyze price sensitivity and package preference       │
│  + ~~spreadsheet: Simulate revenue by pricing scenario           │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

1. **Pricing Model**: "What pricing model fits our SaaS?"
2. **Value Metric**: "Which unit should we charge by?"
3. **Packaging**: "Design our 3-tier pricing structure"
4. **Optimize**: "Validate our current pricing"

## Pricing Models

### 5 Main Models

| Model | Definition | Advantages | Disadvantages | Best For |
|-------|-----------|-----------|----------------|----------|
| **Per-Seat** | Charge per user | Predictable, simple | Growth resistance | Collaboration tools (Slack) |
| **Usage-Based** | Charge by volume | Value-aligned, scalable | Unpredictable revenue | APIs, infrastructure (Twilio) |
| **Flat-Rate** | Fixed monthly fee | Friction-free | Leaves money on table | Small SaaS |
| **Tiered** | Graduated tiers | Upsell pathway | Choice paralysis | General SaaS (HubSpot) |
| **Hybrid** | Mix (seats + usage) | Flexible, optimized | Complex | Enterprise (Salesforce) |

### 1. Per-Seat (User-Based)

**Formula**: `Price = User Count × Per-User Price`

**Examples**:
- Slack: $8/user/month
- Zoom: $15/user/month
- Asana: $10.99/user/month

**Advantages**:
- Simple (easy to understand/decide)
- Predictable MRR
- Team growth = revenue growth

**Disadvantages**:
- Growth friction (each user costs)
- Seat sharing (1 account, many users)
- Value mismatch (power user vs casual)

**Optimization**:
- **Active User Definition**: Logged in 1+ month
- **Viewer/Guest Free**: Read-only users
- **Volume Discount**: 100+ users get discount

### 2. Usage-Based (Consumption)

**Formula**: `Price = Usage Volume × Unit Rate`

**Examples**:
- Twilio: $0.0075 per SMS
- AWS: Per compute hour
- Stripe: 2.9% + $0.30 per transaction

**Advantages**:
- Value-aligned (use more, pay more)
- Low entry barrier (start small)
- Customer growth = your growth

**Disadvantages**:
- Revenue unpredictability
- Bill shock risk (surprise overages)
- Calculation complexity

**Optimization**:
- **Usage Cap**: Set maximum
- **Usage Alert**: Notify at 80% threshold
- **Commitment Discount**: Commit to minimum usage

### 3. Flat-Rate (All-You-Can-Eat)

**Formula**: `Price = Fixed Amount (unlimited usage)`

**Examples**:
- Basecamp: $99/month (unlimited users)
- Netflix: $15.99/month (unlimited viewing)

**Advantages**:
- Zero friction (worry-free usage)
- Predictable cost to customer
- Marketing simplicity ("unlimited")

**Disadvantages**:
- Value leakage (power users underpay)
- Limited upsell
- Revenue optimization ceiling

**Best For**:
- Small SaaS (simplicity)
- SMB-only (limited segments)
- Brand differentiation ("simple")

### 4. Tiered (Good/Better/Best)

**Formula**: Features/usage increase per tier

**Examples**:
- HubSpot:
  - Starter: $50/month (1K contacts)
  - Professional: $800/month (10K contacts)
  - Enterprise: $3,200/month (unlimited)

**Advantages**:
- Clear upsell path
- Segment optimization
- Anchoring effect

**Disadvantages**:
- Choice overload (too many tiers)
- Boundary frustration

**Optimization**:
- **3-Tier Rule** (research: optimal)
- **Highlight Middle**: "Most Popular" badge
- **Enterprise Custom**: Large deals separate

### 5. Hybrid (Mixed)

**Formula**: Base Fee + Usage OR Per-Seat + Feature Tier

**Examples**:
- Salesforce: Base (users) + Add-ons (features)
- Snowflake: Compute + Storage separate
- MongoDB Atlas: Cluster tier + Data transfer

**Advantages**:
- Flexibility (diverse customers)
- Revenue optimization
- Lock-in strengthened

**Disadvantages**:
- Complex to explain
- Billing system complex
- Customer confusion

**Best For**:
- Enterprise customers
- Diverse use cases
- Mature products

---

## Value Metric

### Definition

**Value Metric**: What unit you measure/charge by. "What do we count?"

**Examples**:
- Slack: Active users
- Mailchimp: Contacts
- Twilio: API calls
- Stripe: Transaction volume

### 4 Evaluation Criteria

| Criterion | Definition | Good Example | Bad Example |
|-----------|-----------|--------------|------------|
| **Understandability** | Customer grasps it in 5 secs? | "Users" | "API Request per 1K batches" |
| **Value Alignment** | Metric matches customer value? | "Revenue generated" | "Database rows" |
| **Predictability** | Customer forecasts own cost? | "Fixed 10 users" | "Daily active users" (volatile) |
| **Scalability** | Customer growth = your growth? | "Transactions" | "Login counts" (plateaus) |

### Understandability

**Bad**:
- "Compute Units" (undefined)
- "Storage Blocks in 128KB" (complex)

**Good**:
- "Users"
- "Projects"
- "Contacts"

**Test**: 5-second explanation possible? Mom would understand?

### Value Alignment

**Bad**:
- CRM → "Database Rows" (customer doesn't care)
- Marketing Tool → "Emails Sent" (encourages spam)

**Good**:
- CRM → "Revenue Generated" (outcome-focused)
- Marketing → "Leads Converted" (result-oriented)

**Test**: More use = bigger value? Clear ROI?

### Predictability

**Bad**:
- "Daily Active Users" (high volatility)
- "API Calls" (unpredictable)

**Good**:
- "Seats" (fixed)
- "Monthly Active Users" (stable)

**Test**: Can customer forecast next month's bill?

### Scalability

**Bad**:
- "Logins per Month" (hits ceiling)
- "Files Uploaded" (saturates)

**Good**:
- "Transaction Volume" (infinite scale)
- "Team Size" (company growth = revenue)

**Test**: 10x customer growth = 10x your revenue?

### Selection Process

**Step 1: Brainstorm Candidates**
- All possible metrics
- Example: Users, Projects, Storage, API Calls, Revenue

**Step 2: Score on 4 Criteria**
```
| Metric | Explain | Value | Predict | Scale | Total |
|--------|---------|-------|---------|-------|-------|
| Users | 5 | 3 | 5 | 4 | 17 |
| Projects | 4 | 4 | 4 | 3 | 15 |
| API Calls | 2 | 3 | 2 | 5 | 12 |
| Revenue % | 3 | 5 | 3 | 5 | 16 |
```

**Step 3: Select Top 2-3**
- Highest scores
- Competitive benchmarks

**Step 4: Customer Test**
- Interview 10-20 customers
- "Which feels fairest?"

---

## Pricing Psychology

### 1. Anchoring

**Definition**: First price = reference point

**Application**:
- Show high price first (sets expectation)
- Strikethrough discount: ~~$199~~ → $99
- Annual discount: $100/mo → $1,000/yr (17% off)

**Example**:
```
┌─────────────────────────────┐
│ Enterprise    Pro    Starter│
│ $499/mo      $99/mo  $29/mo │
│ (Anchor)   (Target) (Entry) │
└─────────────────────────────┘
```
Enterprise anchors perception → Pro seems "reasonable"

### 2. Decoy Effect

**Definition**: Intentionally unattractive option → guides choice

**Application**:
- Want Pro chosen
- Add Decoy: similar price, fewer features

**Example**:
```
Starter: $29 (100 contacts)
Pro: $99 (10K contacts) ← target
Decoy: $79 (1K contacts) ← intentionally bad deal
```
Customer thinks: "Decoy is waste; Pro is clear winner"

### 3. Charm Pricing

**Definition**: End in 9 → "cheaper" perception

**Application**:
- $100 → $99
- $1,000 → $997 (or $995)

**Effect**:
- Research: $99 vs $100 = 20% conversion boost
- Psychology: "90s" feels cheaper than "100s"

**Caution**:
- Enterprise: $999 vs $1,000 difference negligible
- Premium brand: $100 keeps prestige

### 4. Price Partitioning

**Definition**: Break down total → cheaper perception

**Application**:
- Annual → Monthly: $1,200/yr → $100/month
- Per-Account: $1,000 (10 users) → $100/user

**Example**:
```
Bad:  $1,440/year
Good: $120/month OR $12/user/month
```

### 5. Bundling

**Definition**: Bundle products → cross-sell

**Strategy**:
- Individual: Feature A $50, Feature B $30
- Bundle: A+B $60 (10% discount)

**Effect**:
- Cross-sell increases
- Churn decreases (more features used)

---

## Good/Better/Best Packaging

### 3-Tier Structure

```
┌──────────────┬──────────────┬──────────────┐
│   Starter    │     Pro      │  Enterprise  │
│   (Good)     │  (Better)    │    (Best)    │
├──────────────┼──────────────┼──────────────┤
│  Entry       │  Most Popular│   Custom     │
│  $29/month   │  $99/month   │  Contact Us  │
│              │              │              │
│ Basic        │ Advanced     │ All features │
│ Email support│ Priority     │ Dedicated CSM│
│ 1 project    │ 10 projects  │ Unlimited    │
└──────────────┴──────────────┴──────────────┘
```

### Starter (Good)

**Purpose**: Lower entry barrier, product experience

**Characteristics**:
- Price: $10-50/month
- Target: Individual, freelancer, tiny team
- Features: Core only (80% of use cases)
- Constraints: Usage limits (100 contacts, 1 project)

**Exclude**:
- Advanced features (AI, Automation)
- Integrations (API, Zapier)
- Support (self-serve only)

### Pro (Better)

**Goal**: Majority of customers (60-70%)

**Characteristics**:
- Price: $50-200/month
- Target: SMB, team (5-20 people)
- Features: All core + some advanced
- Constraints: Reasonable (10 projects, 10K contacts)

**Emphasis**:
- **"Most Popular" badge**
- Colored highlight (blue border)
- 10x value vs Starter

### Enterprise (Best)

**Goal**: High-value customers, upsell path

**Characteristics**:
- Price: $300+ or "Contact Us"
- Target: Enterprise (50+ employees)
- Features: Everything + custom
- Constraints: None (unlimited)

**Add-ons**:
- Dedicated CSM (customer success manager)
- SLA (Service Level Agreement)
- Custom integrations
- Onboarding support

### Tier Spacing (Pricing Ladder)

**Recommended Multiplier**: 3-5x

```
Starter: $29
Pro: $99 (3.4x)
Enterprise: $499 (5x)
```

**Too Narrow** (<2x):
- Weak upgrade motivation
- Limited revenue growth

**Too Wide** (>10x):
- Middle tier missing
- Customer abandonment

---

## Feature Fencing

### 5 Strategies

| Strategy | Description | Example | Pros | Cons |
|----------|-----------|---------|------|------|
| **Usage** | Limit volume | 100 vs 10K contacts | Clear, fair | Complex calculation |
| **Feature** | On/off features | AI unavailable | Differentiates | Development burden |
| **Support** | Tier quality | Email vs phone | Cost-aligned | Experience gap |
| **SLA** | Response time | 48h vs 1h | Justifies enterprise | Measurement needed |
| **API** | Integration limits | No API vs unlimited | Lock-in | Developer frustration |

### 1. Usage Fencing

**Examples**:
- Contacts: 100 (Starter) vs 10K (Pro)
- Projects: 1 vs 10 vs Unlimited
- Storage: 10GB vs 100GB vs 1TB

**Best Practices**:
- Soft limit (encourage upgrade)
- Hard limit (block) = bad UX

### 2. Feature Fencing

**Examples**:
- AI: Pro+ only
- Automation: Enterprise only
- Custom Branding: Enterprise

**Strategy**:
- Limit 20% features = 80% value creation
- Core available all tiers

### 3. Support Fencing

**Example**:
- Starter: Self-serve (Help Center)
- Pro: Email (48h response)
- Enterprise: Phone + Dedicated CSM (1h)

**Advantage**:
- Cost structure alignment
- Enterprise differentiation

### 4. SLA Fencing

**Example**:
| Tier | Uptime | Response Time |
|------|--------|---------------|
| Starter | Best Effort (95%) | N/A |
| Pro | 99.5% | 4h |
| Enterprise | 99.9% | 1h (P1) |

### 5. API/Integration Fencing

**Example**:
- Starter: No API
- Pro: 1K calls/day
- Enterprise: Unlimited

---

## Annual vs Monthly

### Comparison

| Factor | Monthly | Annual | Annual Advantage |
|--------|---------|--------|------------------|
| **Price** | $100/mo | $1,000/yr ($83/mo) | 17% discount |
| **Cash Flow** | Monthly | Upfront | Immediate cash |
| **Churn** | High (monthly review) | Low (committed) | Better retention |
| **Sales Friction** | Easy (low barrier) | Hard (big decision) | Higher barrier |

### Recommended Discount

**Annual Discount**: 15-20%

**Calculation**:
```
Monthly: $100/mo → $1,200/year
Annual: $1,000/year ($83/mo, 17% off)
```

**Why 17%?**
- 10%: Too weak (no motivation)
- 25%: Too high (margin loss)
- 15-20%: Sweet spot

### Strategy

**Option 1: Annual Default**
- Show Annual first → "or $100/month"
- Example: Basecamp, ConvertKit

**Option 2: Monthly Default**
- Monthly primary → "Save 17% with Annual"
- Example: Slack, Zoom

**Option 3: Annual Only** (Advanced)
- Enterprise: Annual only
- Reason: Large contract, upfront cash

### Cash Flow Impact

**Monthly**:
```
Year 1: $100 × 12 = $1,200 (distributed)
```

**Annual**:
```
Year 1: $1,000 (immediate)
→ Extended runway, marketing investment
```

**For Startups**: Annual strongly recommended
- Improves cash flow
- Reduces churn
- Increases predictability

---

## Anti-Patterns

### 1. Too Many Tiers

**Problem**: 5+ tiers → choice paralysis

**Fix**: **3-Tier Rule** (research-optimal)
- If 4+ needed: Split SMB/Enterprise

### 2. Value/Price Mismatch

**Problem**: Price doesn't match customer value

**Fix**:
- Use value-based pricing
- ROI-driven, not cost-driven

### 3. Race to Bottom

**Problem**: Continuous undercutting → margin death

**Fix**:
- **Differentiate on value** (not price)
- Niche premium positioning
- Bundle defensively

### 4. Frequent Price Changes

**Problem**: 3-month changes → customer confusion

**Fix**:
- Change 1-2× annually
- Grandfather existing customers

### 5. Hidden Costs

**Problem**: "Contact Us" or surprise fees

**Fix**:
- Transparent pricing (all tiers)
- No surprise fees
- Enterprise only "Contact Us"

---

## Testing & Optimization

### A/B Testing

**Test Items**:
1. Price point: $99 vs $129
2. Discount: 15% vs 20% annual
3. Tier name: Pro vs Business
4. Anchoring: Enterprise first vs last
5. CTA: "Start Free Trial" vs "Get Started"

**Sample Size**: 100+ conversions/variant, 95%+ confidence

### Van Westendorp Price Sensitivity Meter

**4 Questions**:
1. "What price would be **too cheap** (suspect quality)?"
2. "What price is **good bargain**?"
3. "What price is **expensive**?"
4. "What price is **too expensive** (won't buy)?"

**Analysis**:
- Optimal range: Q2-Q3 intersection
- Best price: Q1-Q4 intersection

### Price Increase Strategy

**When to Raise?**:
- NPS >40 (high satisfaction)
- Churn below industry average
- New features added

**How Much?**:
- 10-20% annually
- Gradual vs sudden

**Handle Existing Customers**:
- **Grandfather**: Maintain old price (6-12 months)
- **Gradual**: 3-month notice
- **Emphasize Value**: "New features justify increase"

---

## Related Skills

- **gtm-strategy**: Integrate pricing into GTM
- **financial-modeling**: Model pricing scenarios
- **startup-metrics**: Track ARPA, LTV
- **sales-playbook**: Pricing negotiation tactics

## Tips

- **Customer Value**: Price on ROI, not cost
- **3-Tier Rule**: Research shows 3 optimal (not 2, not 4)
- **Pro Target**: Design so 60-70% choose Pro
- **Annual Priority**: Early-stage needs cash flow
- **Don't Hesitate**: Raise if value exists. 20% premium > competitors is OK
- **Validate Metric**: 10-20 customer interviews required
- **Transparency**: No hidden fees; Enterprise only "Contact"
- **Regular Review**: Quarterly check, annual adjustment
