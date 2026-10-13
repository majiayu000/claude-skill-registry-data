---
name: backlog-refinement
description: Run effective backlog refinement sessions to keep work well-defined, sized, and ready
triggers: [backlog, refinement, grooming, backlog grooming, backlog refinement, story points, sprint planning, ready for sprint, ticket, user story]
audience: manager, engineer
---

# Backlog Refinement

## Context
Backlog refinement (formerly "grooming") is the ongoing process of reviewing, clarifying, estimating, and ordering backlog items so the team always has a queue of well-understood work ready for the next sprint. Done well, it dramatically reduces sprint planning time and prevents mid-sprint blockers. Done poorly, it becomes a ceremony that wastes time without improving clarity.

The distinction:
- **Grooming** — the older term, now replaced
- **Refinement** — the current Scrum term; an ongoing activity, not just a meeting

Use this skill when:
- Preparing for a refinement session
- Writing or improving a user story or ticket
- Assessing whether a backlog item is "ready" for sprint
- Running a refinement meeting with your team

---

## Instructions

### What Makes a Backlog Item "Ready"?
Use the **INVEST criteria** to assess readiness:
| Letter | Criterion | Check |
|--------|-----------|-------|
| **I** | Independent | Can be built and deployed without depending on another in-progress item? |
| **N** | Negotiable | Is it a statement of need, not a prescribed solution? |
| **V** | Valuable | Does it deliver clear value to a user or the business? |
| **E** | Estimable | Does the team have enough information to size it? |
| **S** | Small | Can it be completed within one sprint? |
| **T** | Testable | Is the acceptance criteria clear enough to write tests against? |

If any criterion fails, the item is **not ready** and needs more work before entering a sprint.

---

### User Story Template
```
As a [type of user],
I want [to do something],
so that [I get some value / outcome].

**Acceptance Criteria:**
- Given [precondition], when [action], then [expected result]
- Given [precondition], when [action], then [expected result]
- ...

**Out of scope:**
- [Explicitly list what this story does NOT cover]

**Dependencies:**
- [List any blockers or related items]

**Notes / Context:**
- [Links to designs, ADRs, API contracts, relevant discussions]
```

---

### Running a Refinement Session

**Before the meeting:**
1. Pull the top 10–15 items from the backlog that are candidates for the next 2 sprints.
2. Pre-read each item. Flag any that are obviously incomplete — fix or reject them before the meeting.
3. Share the agenda with the team in advance so they can think ahead.

**During the meeting (timebox: 60–90 min max, twice per sprint):**

1. **Present the item** — Product Owner or EM reads the story aloud (2 min).
2. **Clarify** — Engineers ask questions until the "what" and "why" are clear. The facilitator documents answers in the ticket (5–10 min).
3. **Check acceptance criteria** — Are they testable? Complete? Missing edge cases?
4. **Size the item** — Use relative estimation (story points or t-shirt sizes). Surface disagreement as a signal, not a problem (see below).
5. **Mark ready or defer** — Either the item passes INVEST and is marked "Ready", or it is sent back for more definition.

**When estimates diverge:**
Divergence in sizing is information. When engineers give very different estimates:
- Ask the high estimator: "What complexity are you seeing that others might have missed?"
- Ask the low estimator: "What assumption are you making that would change if it were wrong?"
- Converge on a shared understanding, then re-estimate. Do not average.

---

### Sizing Guidance

**Story points (Fibonacci: 1, 2, 3, 5, 8, 13):**
| Points | Complexity | Rule of thumb |
|--------|-----------|---------------|
| 1–2 | Trivial | Config change, copy update, single isolated function |
| 3 | Small | Well-understood change in a familiar area, clear tests |
| 5 | Medium | Multiple components involved, some unknowns |
| 8 | Large | Significant scope, multiple touch points — consider splitting |
| 13 | Too big | Must be split before it enters a sprint |

**When to split a story:**
- It spans multiple layers (frontend + backend + DB) with independent deployable value at each layer
- It has multiple user types (admin flow vs. customer flow)
- It contains a "happy path" that could ship before edge cases
- It has a "spike" (research) component that should be separated from implementation

---

### Backlog Health Indicators
| Signal | Healthy | Warning |
|--------|---------|---------|
| Items ready for next sprint | 2+ sprints worth | < 1 sprint worth |
| Average story age (days unrefined) | < 14 days | > 30 days |
| % stories meeting INVEST at session start | > 70% | < 40% |
| Stories split during refinement | Occasional | Every session (stories entering too large) |
| Stories returned for more info | Occasional | Frequent (PO not preparing adequately) |

---

### Common Anti-Patterns to Avoid
- **Refinement as design session:** If the team is designing the solution during refinement, the item wasn't ready to refine. Send it back for discovery/design first.
- **Estimating without understanding:** Rushing to a point value without first aligning on acceptance criteria produces meaningless estimates.
- **Tickets with no "why":** If the story doesn't explain the user value, engineers can't make good trade-off decisions during implementation.
- **Over-specification:** Describing the implementation rather than the requirement removes engineers' autonomy and produces worse solutions.
- **Infinite backlog:** If items are never deleted, the backlog becomes noise. Age out anything untouched for 90+ days that has no near-term plan.

---

## Principles
- Source: [Scrum Guide — Product Backlog Refinement](https://scrumguides.org)
- Source: [User Stories — Ron Jeffries / Mike Cohn](https://www.mountaingoatsoftware.com/agile/user-stories)
- Source: [LeadDev — Effective Engineering Teams](https://leaddev.com)
- Source: [Making Work Visible — Dominica DeGrandis]
- Key idea: *"The goal of refinement is not to produce estimates — it is to produce shared understanding. The estimate is a byproduct. The conversation is the product."*

---

## Output Format
When applying this skill, the agent should:
- Assess a given backlog item against the INVEST criteria and flag any gaps
- Rewrite vague stories into the user story template with clear acceptance criteria
- Recommend a story point estimate and explain the reasoning
- Flag stories that are too large and suggest how to split them
- Generate a refined, sprint-ready version of the item

## MCP Integration

When Jira MCP and Confluence MCP are configured, use them to ground refinement in real data.

**Fetch stories from Jira for refinement:**
```
jira_search_issues(jql: "project = PROJ AND sprint in openSprints() AND status = 'Backlog' ORDER BY rank ASC", max_results: 10)
```

**Read the linked spec or requirements from Confluence:**
```
confluence_get_page(page_id: "<linked_page_id>")
```
Or search by title:
```
confluence_search(query: "feature spec <story_summary>", limit: 3)
```

**Update the Jira story with refined acceptance criteria:**
```
jira_update_issue(issue_key: "PROJ-123", fields: { description: "<refined_description>", story_points: 5 })
```

**Split a large story by creating child issues:**
```
jira_create_issue(project: "PROJ", issue_type: "Story", summary: "<sub-story title>", description: "<AC>", parent: "PROJ-123")
```

**Graceful fallback:** If MCP is not configured, output the refined story as structured Markdown — ready to paste into Jira or Confluence manually.
