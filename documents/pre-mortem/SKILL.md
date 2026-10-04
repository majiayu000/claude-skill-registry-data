---
name: pre-mortem
category: strategy
description: >
  Assumes a project has already failed, works backward to identify the top causes,
  scores them by likelihood and impact, and outputs a mitigation plan. Use when starting
  a new project, before a major launch, evaluating risky decisions, or when the user says
  "pre-mortem", "what could go wrong", "risk analysis", "failure modes", "red team this plan".
---

# Pre-Mortem

Assume the project has already failed. Work backward to find out why.

## Workflow

1. **Gather context** — Read the project description, plan, or doc the user provides. If a vault path is given, read it. If the user describes the project verbally, capture the key facts.

2. **Generate failure scenarios** — Imagine it is 6 months from now and the project has failed catastrophically. Generate 8-12 distinct failure causes across these categories:
   - **Technical** — architecture gaps, scaling limits, dependency risks, security holes
   - **Execution** — timeline, staffing, skill gaps, coordination failures
   - **Market/External** — competition, regulation, user adoption, economic shifts
   - **Organizational** — stakeholder alignment, funding, priority shifts, team morale

3. **Score each cause** — For each failure cause, assign:
   - **Likelihood** (1-5): How probable is this failure mode?
   - **Impact** (1-5): If it happens, how severe is the damage?
   - **Risk Score** = Likelihood × Impact (1-25)

4. **Rank and filter** — Sort by risk score descending. Present the top 5-8.

5. **Mitigation plan** — For each top risk, provide:
   - **Early warning signal** — What would you see first if this is happening?
   - **Mitigation action** — Concrete step to reduce likelihood or impact
   - **Owner suggestion** — Who should own this mitigation?
   - **Deadline heuristic** — When should this be addressed relative to project timeline?

## Output Format

```markdown
## Pre-Mortem: [Project Name]

**Scenario**: It is [date + 6 months]. The project has failed.

### Top Risks

| # | Cause | Category | Likelihood | Impact | Risk | Early Warning |
|---|-------|----------|-----------|--------|------|---------------|
| 1 | ... | Technical | 4 | 5 | 20 | ... |

### Mitigation Plan

#### Risk 1: [Cause]
- **Signal**: ...
- **Action**: ...
- **Owner**: ...
- **By**: ...
```

## Vault Integration

If the user has an Obsidian vault, save the output to:
`vault/decisions/pre-mortem-[project]-[YYYY-MM-DD].md`

Add frontmatter:
```yaml
---
type: pre-mortem
project: [name]
date: [YYYY-MM-DD]
top_risk_score: [highest score]
tags: [pre-mortem, risk, project-name]
---
```
