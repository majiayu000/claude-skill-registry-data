---
name: ai-audit
description: |
  Audit existing business processes to identify AI automation opportunities.
  TRIGGERS - Use when user wants to find AI opportunities, audit processes for automation, or assess AI readiness.
---

# AI Audit

## Overview
Conducts a systematic audit of business processes to identify where AI can save time, reduce costs, or improve quality. Produces a prioritized roadmap.

## Workflow

### Step 1: Business Discovery
1. **Industry**: What sector are you in?
2. **Team size**: How many people?
3. **Key processes**: What are the top 10 things your team does repeatedly?
4. **Pain points**: Where do you waste the most time?
5. **Current tools**: What software do you already use?
6. **Budget**: What can you invest in automation?

### Step 2: Process Audit

For each process, score on the AI Automation Matrix:

| Process | Volume | Repetitive? | Rule-Based? | Data Available? | Human Judgment? | AI Score |
|---------|--------|------------|-------------|-----------------|----------------|----------|
| [Process] | High/Med/Low | Yes/No | Yes/No | Yes/No | Low/Med/High | /10 |

**Scoring guide:**
- High volume + repetitive + rule-based + data available + low judgment = **Perfect for AI** (8-10)
- Medium indicators = **Good candidate with human oversight** (5-7)
- Low volume or high judgment = **Keep human, AI-assist only** (1-4)

### Step 3: Categorize Opportunities

| Category | AI Application | Examples |
|----------|---------------|---------|
| **Content generation** | LLMs create drafts | Emails, posts, reports |
| **Data extraction** | AI reads documents | Invoices, contracts, forms |
| **Classification** | AI sorts and routes | Tickets, leads, inquiries |
| **Summarization** | AI condenses info | Meetings, documents, calls |
| **Scheduling** | AI coordinates | Calendar, resources, tasks |
| **Analysis** | AI finds patterns | Data trends, anomalies |
| **Communication** | Chatbots handle inquiries | FAQ, qualification, support |

### Step 4: Prioritize & Roadmap

Use the Impact-Effort Matrix:

```
HIGH IMPACT
    │
    │  Quick Wins  │  Strategic
    │  (DO FIRST)  │  (PLAN FOR)
    │──────────────┼──────────────
    │  Fill-ins    │  Money Pits
    │  (MAYBE)     │  (AVOID)
    │
    └──────────────────────────── HIGH EFFORT
```

## Output Format

```markdown
# AI Automation Audit: [Company Name]

## Executive Summary
- **Processes audited**: [X]
- **AI opportunities identified**: [X]
- **Estimated time savings**: [X hours/month]
- **Estimated cost savings**: $[X]/month
- **Recommended first project**: [name]

## Process Audit Results

### High Priority (Score 8-10)
| Process | Current Time | AI Solution | Savings | Effort |
|---------|-------------|-------------|---------|--------|
| [Process] | [X hrs/mo] | [AI approach] | [X hrs/mo] | Low/Med |

### Medium Priority (Score 5-7)
[Same table]

### Low Priority / Keep Human (Score 1-4)
[Same table with reasoning]

## Recommended Roadmap

### Phase 1: Quick Wins (Month 1-2)
1. **[Project]**: [description, expected impact]
2. **[Project]**: [description, expected impact]

### Phase 2: Core Automation (Month 3-4)
1. **[Project]**: [description, expected impact]

### Phase 3: Advanced AI (Month 5-6)
1. **[Project]**: [description, expected impact]

## Investment Summary
| Phase | Cost | Monthly Savings | Payback |
|-------|------|----------------|---------|
| Phase 1 | $X | $X | X months |
| Phase 2 | $X | $X | X months |
| Phase 3 | $X | $X | X months |
| **Total** | **$X** | **$X** | **X months** |

## Technology Stack Recommendation
[Tools and platforms for implementation]

## Next Steps
1. [Immediate action]
2. [Short-term action]
3. [Medium-term action]
```

## Quality Checklist
- [ ] Every major process evaluated
- [ ] Scoring is objective and consistent
- [ ] Quick wins identified for early momentum
- [ ] ROI estimated for each opportunity
- [ ] Phased roadmap is realistic
- [ ] Technology recommendations included
- [ ] Next steps are clear
