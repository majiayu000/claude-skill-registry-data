---
name: technical-debt-prioritization
description: Identify, classify, and prioritize technical debt with business impact framing
triggers: [tech debt, technical debt, debt, refactoring backlog, codebase health, legacy code, cleanup]
audience: manager
---

# Technical Debt Prioritization

## Context
Technical debt is the implied cost of future rework caused by choosing a quick solution now instead of a better, longer-term approach. Not all debt is equal — some is strategic (deliberately incurred with a plan to repay), some is inadvertent (discovered after the fact), some is reckless. This skill helps you identify, classify, and prioritize debt so you can have evidence-based conversations with your team and stakeholders.

Use this skill when:
- Planning a quarter and deciding how much capacity to allocate to debt
- Advocating for tech debt work to non-technical stakeholders
- Triaging a legacy codebase before a new feature investment
- Running a "codebase health" review

## Instructions

### Step 1 — Identify the Debt
Gather evidence through:
- **Developer pain points** (ask the team: "what's the hardest part of the codebase to work in?")
- **High-churn files** (files with frequent changes and frequent bugs are debt hotspots)
- **Slow features** (areas where every change takes far longer than it should)
- **Test coverage gaps** (code with no coverage that is frequently changed)
- **Known workarounds** (places where engineers manually compensate for missing abstractions)

### Step 2 — Classify Using the Debt Quadrant
| | Deliberate | Inadvertent |
|---|-----------|------------|
| **Reckless** | "We don't have time for design" | "What's layering?" |
| **Prudent** | "We must ship now; we'll fix later" | "Now we know how we should have done it" |

Focus repayment effort on:
1. **Prudent + Inadvertent** → this is the most valuable debt to address; it's fixable and the team now knows the right design
2. **Prudent + Deliberate** → repay on schedule or the interest compounds
3. **Reckless debt** → do not add more; repay incrementally to reduce risk

### Step 3 — Score Each Debt Item
Use this scoring matrix for prioritization:

| Criterion | Score 1 (Low) | Score 2 (Medium) | Score 3 (High) |
|-----------|---------------|-----------------|----------------|
| **Business impact** | Rarely touched area | Feature area, moderate usage | Core path, high traffic |
| **Developer pain** | Minor inconvenience | Slows a team | Blocks multiple teams |
| **Risk** | No production impact | Occasional bugs | Frequent incidents |
| **Effort to fix** | High (months) | Medium (weeks) | Low (days) |

**Priority = Business Impact + Developer Pain + Risk + Effort to Fix**  
Highest total score = address first.

### Step 4 — Frame for Stakeholders
Never pitch tech debt as "cleanup" or "engineering hygiene" — stakeholders can't fund abstractions. Frame it in business terms:

| Instead of... | Say... |
|---------------|--------|
| "We need to refactor the payment module" | "The payment module causes 40% of our P1 incidents. Addressing it will halve our incident rate in that area." |
| "Our test coverage is low" | "We're shipping features in this area 3x slower than comparable areas because bugs find us in production, not in tests." |
| "This code is a mess" | "Every new hire takes 2+ weeks to become productive in this area vs. 3 days elsewhere." |

### Step 5 — Allocate Capacity
Recommended allocation models:
- **20% rule:** 1 day per sprint per engineer allocated to debt reduction
- **Boy Scout sprints:** Every sprint, leave the code a little better than you found it
- **Dedicated debt sprints:** 1 sprint per quarter focused entirely on debt (acceptable for large chunks)
- **Opportunistic:** Repay debt in the module you're already changing (low-cost, high-value)

## Principles
- Source: [Technical Debt — Martin Fowler](https://martinfowler.com/bliki/TechnicalDebt.html)
- Source: [Tech Debt Quadrant — Martin Fowler](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- Key idea: *"The real problem with technical debt is that it makes future changes more expensive. Until you can show that the cost of fixing is less than the cost of living with it, you won't get organizational support to fix it."*

## Output Format
When applying this skill, the agent should:
- Generate a scored debt inventory from team inputs or codebase signals
- Classify each item in the debt quadrant
- Sort by priority score
- Produce business-language framing for the top 3 items ready for stakeholder communication
- Suggest a capacity allocation model for the team's current situation

## MCP Integration

**Query existing tech debt tickets:**
```
jira_search_issues(jql: "project = PROJ AND labels = 'tech-debt' AND status != Done ORDER BY priority DESC")
```

**Create new tech debt tickets from the debt inventory:**
```
jira_create_issue(project: "PROJ", issue_type: "Tech Debt", summary: "<debt item title>", description: "<quadrant, priority score, business impact, effort estimate>", labels: ["tech-debt"], priority: "<High|Medium|Low>")
```

**Link debt items to the affected epics:**
```
jira_create_issue_link(inward_issue: "PROJ-debt", outward_issue: "PROJ-epic", link_type: "relates to")
```

**Document the debt decisions in Confluence:**
```
confluence_create_page(space_key: "ENG", title: "Technical Debt Register — <Quarter>", content: "<debt inventory with quadrant, scores, and capacity allocation plan>", parent_page_id: "<architecture_page_id>")
```

**Graceful fallback:** Output the scored debt register as a Markdown table — suitable for pasting into a Confluence page or converting to Jira tickets.
