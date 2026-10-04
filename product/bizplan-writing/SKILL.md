---
name: bizplan-writing
description: 'Provides domain knowledge for writing Korean government funding program business plans (사업계획서). Auto-activates in contexts like "Korean funding application", "business plan writing", "bizplan", "plan evaluation", "writing strategy", "apply-write", etc. Triggers on Korean terms: "사업계획서", "지원사업 작성", "사업계획서 평가", "작성 전략", "공고 작성".'
---

# Business Plan Writing Guide

A guide to writing Korean government funding program business plans (사업계획서) from an evaluator's perspective.

## Standard 13-Section Structure for Business Plans (사업계획서)

| Section | Description | Knowledge Base Source |
|---------|-------------|----------------------|
| 1. Company Overview | Company name, founding date, industry, location | company-profile |
| 2. Leadership & Team | Key personnel education, experience, roles | company-profile.team |
| 3. Business Item Introduction | Product/service overview, problem definition | product |
| 4. Technology Development | Core technology, development plan, TRL | product.tech + product.ip |
| 5. Market Analysis | TAM/SAM/SOM, growth rate | market |
| 6. Competitive Analysis & Differentiation | Competitive landscape, positioning | market.competitors + product |
| 7. Commercialization Strategy | Revenue model, business model | business-model |
| 8. Marketing & Sales Strategy | GTM, channels, customer acquisition | business-model.gtm |
| 9. Financial Plan | Revenue forecast, break-even point | financials |
| 10. Capital Requirements & Use Plan | Itemized expense plan | financials.funding |
| 11. Implementation Timeline | Milestones, Gantt chart | (generated per program) |
| 12. Expected Impact | Social/economic ripple effects | market + business-model |
| 13. Track Record | Past government funding achievements, awards | track-record |

---

## Program-Type Emphasis Points

### TIPS (Technology Startup Investment Program — 기술창업투자프로그램)

**Core Scoring:** Technology Innovation 40% > Market Potential 30% > Team Capability 20% > Other 10%

- **Priority 1:** Core technology originality and protection mechanisms (patents, trade secrets)
- **Priority 2:** Size of market problem the technology solves
- **Priority 3:** Founder/team's ability to implement the technology
- **Key phrases:** "world's first", "Korea's only", "X times better than existing", "TRL X achieved"
- **Operator selection strategy:** Choosing the right operator by industry is 50% of success — always review operator portfolio

### Early-Stage Startup Package (예비창업패키지)

**Core Scoring:** Commercialization Potential 40% > Item Innovation 30% > Founder Capability 30%

- **Priority 1:** Fast market validation plan (MVP → customers → revenue)
- **Priority 2:** Customer interview / pre-demand research results
- **Priority 3:** Founder's stake in solving the problem
- **Key phrases:** "○○ customer interviews conducted", "pre-MOU signed", "pilot running"

### Initial Startup Package (초기창업패키지)

**Core Scoring:** Growth Potential 35% > Item Innovation 35% > Team Capability 30%

- **Priority 1:** Quantitative achievements within 3 years of startup (revenue, customers, growth rate)
- **Priority 2:** Market validation evidence for the item
- **Critical:** Current revenue/customer count must be stated

### Startup Growth Technology Development (창업성장기술개발 — R&D Project)

**Core Scoring:** Technology Development Capability 35% > Market Potential/Commercialization Feasibility 35% > Execution Ability 30%

- **Priority 1:** Technology roadmap concreteness (annual development targets + performance metrics)
- **Priority 2:** Clear commercialization pathway after technology development
- **Priority 3:** Past R&D execution track record (government project experience)
- **Caution:** R&D expense execution plan must be detailed

### AI Voucher (AI Adoption Support — AI 바우처)

**Core Scoring:** AI Technology Application Specificity 40% > Expected Impact 35% > Execution Capability 25%

- **Priority 1:** Clear scenario: where and how AI will be applied
- **Priority 2:** Pre/post-adoption comparable KPI setting
- **Key phrases:** "AI adoption reduces processing time by X%", "target accuracy improvement of X%"

### Seoul-Type R&D / Local Government Projects (서울형 R&D / 지자체 과제)

- **Priority 1:** Regional economic contribution (job creation, regional revenue)
- **Priority 2:** Seoul/local location must be confirmed
- **Caution:** Check local government-specific criteria (e.g., Seoul prefers Seoul-based companies)

---

## Writing Principles

### Quantitative Data Presentation

```
❌ Avoid                           ✅ Recommended
"will be accomplished"            "verified as of [date]"
"market is expected to be large"  "TAM ₩X trillion per [Research Institute] 2025"
"many customers"                  "123 paying customers, MRR ₩28M"
"growing rapidly"                 "15% MoM growth (2025.01~06, 6-month avg)"
"unique technology"               "3x faster than competitors, 2 patents held"
```

### Killer Phrases by Section

**Technology Differentiation:**
- "Applied ○○ technology for the first time globally to ~~"
- "X% accuracy improvement, Y% cost reduction vs. existing methods"
- "TRL 7 achieved — prototype validation complete, production-ready stage"

**Market Analysis:**
- "Korea's ○○ market is ₩X trillion per [Research Institute] 2025"
- "X% annual growth (CAGR 2024~2029, source: ○○)"

**Team Capability:**
- "Founder graduated from ○○ University, ○○ major, X years of ○○ experience at ○○"
- "Lead developer ○○ holds X patents in ○○"

---

## Score-Based Page Allocation

When total pages are fixed, allocate space proportionally to scoring weights:

Example — 20-page business plan, TIPS program:
- Technology Development (40%): 8 pages
- Market Analysis + Commercialization Strategy (30%): 6 pages
- Team Capability + Company Overview (20%): 4 pages
- Financial Plan + Other (10%): 2 pages

---

## Page/Character Limit Management

- **Exceeding page limit:** Compress lowest-scoring sections first (expected impact, timeline)
- **Character limit:** Tables/bullets can convey same information in 20-30% less space
- **Table usage:** Competitive comparison, financial plan, and timeline are best presented as tables for evaluator readability

---

## Evaluator Checklist

Before submitting your business plan (사업계획서):

- [ ] All figures include source or measurement period
- [ ] Minimize "will be" statements; focus on verified facts
- [ ] Competitive differentiation expressed quantitatively
- [ ] TAM/SAM/SOM sources and calculation rationale included
- [ ] Team member education/experience linked to business item
- [ ] Timeline achievable within program period
- [ ] Capital use plan broken down into specific line items
