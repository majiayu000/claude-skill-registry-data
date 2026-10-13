---
name: roadmap-prioritization
description: Prioritize engineering initiatives and features for quarterly planning using RICE and ICE scoring frameworks. Map dependencies, identify quick wins vs. strategic bets, and communicate tradeoffs clearly to stakeholders. Grounded in outcome-driven roadmapping principles.
triggers:
  - "quarterly planning"
  - "roadmap prioritization"
  - "what should we work on"
  - "prioritize backlog"
  - "RICE scoring"
  - "ICE scoring"
  - "strategic planning"
  - "OKR planning"
audience:
  - manager
---

# Roadmap Prioritization

Decide what to work on next quarter using evidence, not intuition or loudest stakeholder.

---

## Before You Score Anything

Prioritization is meaningless without answering these first:

1. **What is the team's goal this quarter?** (OKR, north star metric, or strategic bet)
2. **Who are the stakeholders and what are their key asks?**
3. **What is the capacity?** (engineers × sprints × velocity factor)
4. **What is non-negotiable?** (compliance, security, contractual commitments — park these separately)

---

## RICE Scoring

RICE is best for product features and new initiatives.

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

| Factor | Scale | Definition |
|---|---|---|
| **Reach** | # users/events per quarter | How many users does this affect per quarter? |
| **Impact** | 3/2/1/0.5/0.25 | Massive/High/Medium/Low/Minimal impact on goal |
| **Confidence** | 100%/80%/50% | How confident are you in Reach and Impact estimates? |
| **Effort** | Person-weeks | Total eng effort to deliver (not just dev) |

**Example**:
```
Feature: Reduce checkout abandonment with saved addresses
Reach: 50,000 users/quarter touch checkout
Impact: 2 (high — directly reduces abandonment)
Confidence: 80% (data from A/B test in similar market)
Effort: 3 person-weeks

RICE = (50,000 × 2 × 0.8) / 3 = 26,667
```

Higher RICE = higher priority. Use relative ranking, not absolute scores.

---

## ICE Scoring

ICE is faster and works well for tech initiatives, internal tools, and engineering-led work.

```
ICE Score = Impact × Confidence × Ease
```

| Factor | Scale | Definition |
|---|---|---|
| **Impact** | 1–10 | How much does this move the needle on our goal? |
| **Confidence** | 1–10 | How sure are we it will work as expected? |
| **Ease** | 1–10 | How easy is this to implement? (10 = trivial) |

**Example**:
```
Initiative: Add distributed tracing to payment service
Impact: 7 (reduces MTTR, reduces on-call burden)
Confidence: 9 (we know this helps, team has done it before)
Ease: 5 (moderate effort, 2-week implementation)

ICE = 7 × 9 × 5 = 315
```

---

## Scoring Sheet Template

```markdown
## Q[N] Roadmap Scoring: [Team Name]

**Goal**: [OKR or strategic objective]
**Capacity**: [N] person-weeks available

### Scored Initiatives

| Initiative | Type | RICE/ICE Score | Effort (wks) | Cumulative Effort | Priority |
|---|---|---|---|---|---|
| [name] | Feature/Tech/Ops | [score] | [N] | [running total] | 1 |
| [name] | | | | | 2 |
| [name] | | | | | 3 |

**Non-negotiables** (scored separately, capacity reserved first):
| Initiative | Effort | Reason |
|---|---|---|
| [compliance item] | [N weeks] | [legal/contractual] |

**Capacity after non-negotiables**: [X weeks]

### Scope Decision
| Initiative | Decision | Rationale |
|---|---|---|
| [name] | In / Out / Stretch | [reason] |
```

---

## Dependency Mapping

Before finalizing the roadmap, map blockers:

```
Initiative A ──requires──> Initiative B (must ship B before A)
Initiative C ──blocks──>   Initiative D (C's output enables D)
Initiative E ──risks──>    Initiative F (E's outcome changes F's priority)
```

**Rules:**
- If an initiative has 2+ unresolved dependencies, it's likely a Q+1 item
- Surface cross-team dependencies in planning (not at execution time)
- Time-box dependency resolution: if it takes > 1 week to align, defer the initiative

---

## Portfolio Balance Check

A healthy quarterly roadmap balances across:

| Category | Target Mix | Examples |
|---|---|---|
| **New capability** (user value) | 40-60% | New features, integrations |
| **Tech investment** (team health) | 20-30% | Refactoring, infra, tooling |
| **Reliability** (stability) | 10-20% | Observability, on-call reduction |
| **Maintenance** (hygiene) | 5-10% | Dependency updates, security |

If tech investment drops below 20% for 2+ quarters, expect velocity to slow and incidents to increase.

---

## Communicating Tradeoffs

When a stakeholder's request doesn't make it into the roadmap:

**Template**:
```
We evaluated [initiative] using RICE/ICE scoring.
It scored [X], which placed it at priority [N] in our ranked list.
Given our capacity of [X] weeks, we can execute priorities 1-[N].

[Initiative] is planned for Q[N+1] because:
- [reason: lower impact than items above it / blocked by dependency / capacity constrained]

To move it earlier, we would need to:
- [option A: defer initiative X (here's the tradeoff)]
- [option B: add capacity (here's the cost)]
- [option C: descope it to fit in Q[N]]

Which would you prefer?
```

This positions you as decision-enabler, not gatekeeper.

---

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| HiPPO prioritization | Highest-paid person's opinion drives the roadmap | Score every initiative; surface the data |
| No capacity accounting | Roadmap assumes 100% eng time on features | Reserve 20% for unplanned work, on-call, reviews |
| Ignoring tech debt | 0 tech initiatives in the roadmap | Enforce portfolio balance; tech debt creates future capacity problems |
| Scope creep in planning | "Just add one more thing" | Capacity is finite; every addition needs a removal |
| Annual planning, quarterly ignoring | Plan once, never revisit | Monthly roadmap review; rescore when context changes |

---

## References
- Intercom: [RICE Scoring Model](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- Marty Cagan: *Inspired* (outcome-driven roadmaps)
- LeadDev: [Engineering roadmaps that make sense to stakeholders](https://leaddev.com/roadmapping)
- Will Larson: *An Elegant Puzzle* — on sequencing technical investments

## MCP Integration

**Query epics and initiatives from Jira:**
```
jira_search_issues(jql: "project = PROJ AND issuetype = Epic AND status != Done ORDER BY rank ASC")
```

**Read the current roadmap or strategy doc from Confluence:**
```
confluence_search(query: "engineering roadmap Q<N> <year>", limit: 5)
confluence_get_page(page_id: "<roadmap_page_id>")
```

**Create new planned epics from prioritization output:**
```
jira_create_issue(project: "PROJ", issue_type: "Epic", summary: "<Initiative title>", description: "<RICE score, rationale, success metrics>", labels: ["roadmap"])
```

**Write the updated roadmap to Confluence:**
```
confluence_update_page(page_id: "<roadmap_page_id>", title: "Engineering Roadmap — <Quarter>", content: "<updated roadmap with RICE scores and sequencing>")
```

**Graceful fallback:** Output the prioritized roadmap table as Markdown with RICE scores — ready to paste into Confluence and link from the relevant Jira epic.
