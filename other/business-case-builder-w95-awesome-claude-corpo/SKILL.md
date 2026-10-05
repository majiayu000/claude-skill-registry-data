---
name: business-case-builder
description: "Build business cases with cost-benefit analysis, ROI calculations, risk assessment, implementation timeline, and stakeholder analysis"
---

# Business Case Builder

## Overview

Develop compelling business cases that justify investments, align stakeholders, and enable informed go/no-go decisions. Comprehensive business cases combine financial analysis, risk assessment, and strategic alignment to make the case for action.

## Core Components

### 1. Executive Summary
- **Investment Required**: Total cost in dollars and timeline
- **Expected Benefit**: Quantified returns (revenue, cost savings, efficiency)
- **ROI**: Payback period, IRR, NPV
- **Strategic Alignment**: How this supports company goals
- **Recommendation**: Proceed / Proceed with conditions / Do not proceed

### 2. Problem Statement
- **Current State**: What's broken or missing today
- **Impact**: Business cost of status quo (missed revenue, inefficiency, risk)
- **Why Now**: Urgency drivers and market windows
- **Success Criteria**: How we'll measure improvement

Example:
```
Problem: Manual invoice processing takes 40 hours/week, error rate 3%,
60-day payment cycle
Impact: $180K annual cost in labor + 2% revenue impact from late payments
Why Now: Volume growing 25% YoY; competitors process faster
Success: Automate 80% of invoices, reduce cycle to 10 days, <0.5% errors
```

### 3. Solution Overview
- **Proposed Approach**: High-level solution design
- **Key Features**: Core capabilities and benefits
- **Differentiation**: Why this solution over alternatives
- **Implementation Path**: Phased rollout or big-bang

### 4. Financial Analysis

**Cost Structure**:
```
Category | Year 1 | Year 2 | Year 3 | Total
---------|--------|--------|--------|-------
Software License | $50K | $60K | $70K | $180K
Implementation | $100K | $0 | $0 | $100K
Training | $20K | $5K | $5K | $30K
Support/Maintenance | $30K | $35K | $40K | $105K
Total Cost | $200K | $100K | $115K | $415K
```

**Benefit Stream**:
```
Category | Year 1 | Year 2 | Year 3 | Total | Type
---------|--------|--------|--------|-------|-------
Labor Savings | $140K | $140K | $140K | $420K | Hard
Improved Collection | $30K | $50K | $50K | $130K | Hard
Reduced Errors | $10K | $10K | $10K | $30K | Soft
Faster Reporting | $0K | $20K | $20K | $40K | Soft
Total Benefit | $180K | $220K | $220K | $620K |
```

**Financial Metrics**:
- **Net Present Value (NPV)**: Benefits - Costs (discounted at 10%)
  - Year 1: $180K - $200K = -$20K
  - Year 2: $200K / 1.1 = $182K - $100K = $82K
  - Year 3: $220K / 1.21 = $182K - $115K = $67K
  - **Total NPV**: ~$131K

- **ROI**: (Total benefit - Total cost) / Total cost
  - ($620K - $415K) / $415K = 50% total ROI
  - Payback period: ~15 months

- **Internal Rate of Return (IRR)**: Break-even discount rate = 22%

**Sensitivity Analysis**:
```
Scenario | Impact | Cost | Benefit | ROI
----------|--------|------|---------|-----
Base Case | 1.0x | $415K | $620K | 50%
Pessimistic | 0.8x | $450K | $500K | 11%
Optimistic | 1.2x | $400K | $750K | 88%
Delayed 6 Mo | Impact | $435K | $580K | 33%
```

### 5. Risk Assessment

**Risk Matrix**:
```
Risk | Probability | Impact | Mitigation | Owner
-----|------------|--------|-----------|-------
Scope Creep | High | Medium | Change control process | PM
Adoption | Medium | High | Extensive training | HR/PM
Integration | Low | High | Technical POC pre-sales | Tech
Vendor Risk | Low | High | Service level agreements | Procurement
Delayed ROI | Medium | Medium | Phased implementation | Finance
```

### 6. Implementation Timeline
```
Phase | Duration | Deliverables | Risks | Dependencies
-------|----------|-------------|-------|---------------
Discovery | 4 weeks | Requirements, design | Requirements change | Exec sponsorship
Setup | 6 weeks | System config, data migration | Data quality | IT resources
Pilot | 4 weeks | Pilot results, training | Low adoption | Vendor support
Rollout | 8 weeks | Full deployment, support | Integration issues | IT resources
Optimization | 8 weeks | Performance tuning, hypercare | User resistance | User adoption
```

**Key Milestones**:
- Week 4: Requirements approved by steering committee
- Week 10: System ready for pilot
- Week 14: Pilot results reviewed; GO/NO-GO decision
- Week 22: Full production deployment
- Week 30: Hypercare complete; production support transitions

### 7. Stakeholder Analysis

**Steering Committee**:
- CEO: Strategic alignment, investment level ✓
- CFO: ROI, payback period, budget ✓
- COO: Implementation timeline, resource impact ✓

**Key Stakeholders**:
- Finance team: Daily users, training needs, process change impact
- IT department: Infrastructure, integration, support
- Vendor/Service provider: Support, success metrics
- Process owners: Workflow changes, adoption

**Communication Plan**:
- Monthly steering committee updates
- Biweekly pilot group check-ins
- Quarterly all-hands updates
- Success stories shared company-wide

### 8. Alternatives Analysis

**Option 1: Current State (Do Nothing)**
- Cost: $0
- Benefit: $0
- ROI: 0%
- Risk: Falling behind competitors, missing growth opportunity

**Option 2: Manual Optimization (Status Quo Enhanced)**
- Cost: $50K (hiring)
- Benefit: $80K (labor savings)
- ROI: 60% over 3 years
- Risk: Still manual process; limited scalability

**Option 3: Proposed Solution (Recommended)**
- Cost: $415K
- Benefit: $620K
- ROI: 50% over 3 years
- Risk: Manageable with mitigation plan

**Recommendation**: Option 3 (Proposed) is optimal. Delivers 10x better ROI than Option 2, with payback in 15 months.

## Template Structure

**BUSINESS CASE: [Project Name]**

Prepared by: [Name]
Date: [Date]
For: [Decision forum]
Decision Needed By: [Date]

**EXECUTIVE SUMMARY**
[1-2 paragraphs overview]

Investment: $[Amount] over [Period]
Expected Benefit: $[Amount]
ROI: [Percentage] | Payback: [Months]
Recommendation: [Proceed / Proceed with conditions / Do not proceed]

**PROBLEM STATEMENT**
Current State: [Describe]
Business Impact: [Quantified]
Strategic Drivers: [Why now]

**PROPOSED SOLUTION**
Overview: [High-level description]
Key Benefits: [List]
Approach: [Phased/Big-bang with timeline]

**FINANCIAL ANALYSIS**
[Cost table] [Benefit table] [Metrics]

**RISK ASSESSMENT**
[Risk matrix with mitigations]

**IMPLEMENTATION PLAN**
[Timeline with milestones]

**ALTERNATIVES CONSIDERED**
[Option 1, 2, 3 with comparison]

**STAKEHOLDER ANALYSIS & COMMUNICATIONS**
[Governance, key contacts, communication plan]

**APPENDICES**
- Detailed cost build-up
- Sensitivity analysis
- Vendor proposals
- References/case studies
- Technical architecture (if applicable)

## Best Practices

1. **Be Conservative**: Underestimate benefits; overestimate costs
2. **Quantify Everything**: Use data, not assumptions
3. **Include All Costs**: Don't hide implementation or ongoing support costs
4. **Real Cash Flow**: Consider working capital, timing of cash flows
5. **Sensitivity Analysis**: Show what happens in downside scenarios
6. **Comparison Matrix**: Make trade-offs explicit
7. **Clear Governance**: Who decides? What's needed to move forward?
8. **Stakeholder Alignment**: Understand concerns; address objections upfront
9. **Success Metrics**: Define how you'll measure success post-implementation
10. **Decision Criteria**: Be clear what "good" looks like

## Red Flags

- ROI disappears if one assumption changes slightly (sensitivity check)
- Benefits rely on unproven technology or team adoption
- Costs missing major categories (change management, training, support)
- No risk mitigation plan for high-probability/high-impact risks
- Stakeholder misalignment on strategic value
- Timeline unrealistic or resources unavailable
- Vendor not financially stable or lacking references
- No clear DRI (Directly Responsible Individual)

## When to Use Business Cases

- Capital expenditure >$100K
- Strategic initiative affecting multiple departments
- Make-or-buy decisions
- Significant process/system changes
- Market entry or expansion
- Build vs. partner decisions
- Organizational restructuring

## Sign-Off Template

```
I have reviewed this business case and concur with the
recommendation to PROCEED.

CEO: _________________________ Date: _________
CFO: _________________________ Date: _________
Sponsor: ______________________ Date: _________

Approved for implementation.
Next step: Project initiation meeting scheduled [Date].
Budget allocated: $[Amount]
Timeline: [Start date] - [End date]
```

---

**Use this skill to**: Justify major investments, align stakeholders, get budget approval, and ensure clear go/no-go decision frameworks.
