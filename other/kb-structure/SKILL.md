---
name: kb-structure
description: Performs knowledge base structuring, schema definition, and completeness validation. Auto-activates in contexts like "knowledge base", "KB", "organize company info", "business plan data", "knowledge base", "kb-init", "kb-update", and Korean terms "지식베이스", "KB", "회사 정보 정리", "사업계획서 데이터".
---

# Knowledge Base Structure

All business plan (사업계획서) automation in the startup-apply plugin is built on this knowledge base. Once established, it enables reusable business plan generation across all funding programs without repetition.

## 7-Category Schema

### 1. company-profile (Company Basic Information)

**Required:**
- Legal company name (+ English name)
- Establishment date
- Representative name
- Address (location)
- Business registration number
- Industry code (KSIC)
- Company type (주식회사, 유한회사, etc.)
- Mission / Vision (one sentence)

**Optional:**
- Website / SNS
- Company history (major milestones by year)
- Awards / certifications

**Team Composition (key personnel):**
- Name / Title
- Final education (university, major)
- Main experience (3 lines max)
- Role/responsibility

---

### 2. product (Product / Service)

**Required:**
- One-line product/service description
- Problem being solved
- Core features list
- Technology differentiation (vs competitors)

**Optional:**
- Technology stack
- Development stage (idea / MVP / beta / full launch)
- Service URL / demo

**Technology / IP:**
- Patents (application / registered, number, name)
- Software copyright
- Certifications (ISO, KC, GS, etc.)
- TRL stage (1~9)

---

### 3. market (Market Analysis)

**Required:**
- TAM (total addressable market, source, calculation basis)
- SAM (serviceable addressable market, source, calculation basis)
- SOM (serviceable obtainable market, calculation basis)
- Target customers (1-3 personas)

**Optional:**
- Market growth rate (CAGR, source)
- Competitor analysis (name, strengths, weaknesses, differentiation vs us)
- Market trends (3-5 keywords)

> Note: TAM/SAM/SOM must include sources (report name, issuing agency, year) and calculation basis to be recognized in evaluations.

---

### 4. business-model (Business Model)

**Required:**
- Revenue model (subscription/transaction/licensing/advertising, etc.)
- Key customer segments
- Pricing policy (price per plan)
- Customer acquisition channels

**Optional:**
- GTM strategy summary
- Key partners
- Major customers/references

---

### 5. financials (Financials / KPIs)

**Required:**
- Revenue trend (by year, unit: 만원)
- Current MRR / ARR
- Break-even point (BEP) achievement status / estimated timing

**Optional:**
- Key KPIs:
  - MAU / DAU
  - Conversion rate (CVR)
  - LTV / CAC ratio
  - NPS
- Financial statement summary (revenue, operating profit, net income)
- Fundraising history (round, amount, investors)
- Current runway (months)
- Fund use plan (by item %)

---

### 6. track-record (Track Record)

**Required:**
- Past government funding program execution history:
  - Program name, administering agency, year, funding amount, results
- Awards / selections

**Optional:**
- Fundraising history
- Major customer / partner logos
- Press coverage

---

### 7. past-plans (Past Document Patterns)

Auto-generated — populated when `/kb-init` is executed by analyzing past business plans.

- Frequently used writing style / tone characteristics
- Section-specific expression patterns (e.g., "~을 통해 ~를 실현합니다")
- Emphasized differentiation keywords
- Writing patterns by program type

---

## Completeness Score Criteria

| Category | Weight | Criteria |
|----------|--------|----------|
| company-profile | 15% | All required items + 2+ team members |
| product | 20% | All required items + 1+ technology/IP entry |
| market | 20% | TAM/SAM/SOM with sources |
| business-model | 15% | Revenue model + pricing policy |
| financials | 20% | Revenue trend + 3+ KPIs |
| track-record | 10% | 1+ track record |

**Completeness Interpretation:**
- 90%+ → Ready to apply to all funding programs immediately
- 70~89% → Can apply to most, minor supplements needed
- 50~69% → Supplements needed before applying to major programs
- Below 50% → Use `/kb-update` to fill critical items first

---

## Storage Structure

### With Notion Connection (Recommended)

```
[Company Name] Knowledge Base (Notion page)
├── 📄 company-profile
├── 📄 product
├── 📄 market
├── 📄 business-model
├── 📄 financials
├── 📄 track-record
└── 📄 past-plans
```

### Without Notion Connection (Local Markdown)

```
.kb/
├── company-profile.md
├── product.md
├── market.md
├── business-model.md
├── financials.md
├── track-record.md
└── past-plans.md
```

---

## Category-Specific Writing Guide

**market — TAM/SAM/SOM Writing Principles**
- Always cite sources: "○○연구원, 2025년 국내 AI 시장 전망 보고서"
- Provide calculation basis: "Number of domestic SMEs 800K × Average SaaS spending 2M KRW/year = TAM 1.6T KRW"
- Use most conservative figures

**financials — Numeric Presentation Principles**
- Verified numbers preferred over projections: "Achieved MRR 12M KRW in April 2025"
- When citing growth, specify period: "MoM 15% growth vs. prior year (Jan~Jun 2025)"

**product — Technology Differentiation Writing Principles**
- Provide quantitative differences vs competitors: "3x processing speed, 40% cost reduction"
- Clarify TRL stage: "TRL 7 (시제품 검증 완료)"
