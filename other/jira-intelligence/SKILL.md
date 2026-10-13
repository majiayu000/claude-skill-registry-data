---
name: jira-intelligence
description: "Agent-native equivalents of Jira Intelligence (Atlassian AI) — no Premium license required. Seven commands: work breakdown (epic → child stories), story enhancement (rewrite vague tickets), comment thread summary (decisions + action items), edge case generator, dependency detector (sprint sequencing), story point estimator (codebase-grounded Fibonacci), and natural language to JQL translation. Works with or without Jira MCP."
triggers:
  - "improve this ticket"
  - "rewrite this story"
  - "summarize this ticket"
  - "tldr this jira"
  - "what are the edge cases"
  - "find dependencies"
  - "estimate this story"
  - "story point estimate"
  - "turn this into JQL"
  - "generate JQL"
  - "break down this epic"
  - "child stories from epic"
  - "what's blocking what"
  - "dependency map"
  - "sprint sequencing"
audience: manager, engineer, qa
---

# Jira Intelligence (Agent-Native)

## Context

Atlassian Intelligence is a Jira Premium/Enterprise feature. This skill replicates its core capabilities using the AI agent directly — paste any ticket, epic, comment thread, or natural language query and get the same output. Works with plain text input or Jira MCP when configured.

**Seven commands — invoke any independently:**

| Command | Trigger phrase |
|---------|---------------|
| [Work Breakdown](#1-work-breakdown) | *"Break this epic into stories"* |
| [Story Enhancement](#2-story-enhancement) | *"Improve this ticket"* |
| [Comment Summary](#3-comment-thread-summary) | *"Summarize this ticket"* |
| [Edge Case Generator](#4-edge-case-generator) | *"What are the edge cases?"* |
| [Dependency Detector](#5-dependency-detector) | *"Find dependencies in these stories"* |
| [Story Point Estimator](#6-story-point-estimator) | *"Estimate this story"* |
| [NL → JQL](#7-natural-language--jql) | *"Turn this into JQL"* |

---

## 1. Work Breakdown

> *"Break this epic into stories"* / *"Generate child issues from this epic"*

**Input:** Paste the epic title + description — or fetch via MCP:
```
jira_get_issue(issue_key: "PROJ-epic")
```

**What the agent does:**
1. Identifies core user journeys and outcomes in the epic
2. Applies vertical slicing patterns (workflow steps, happy/unhappy paths, CRUD, roles)
3. Checks each candidate against INVEST (Independent, Valuable, Estimable, Small, Testable)
4. Returns child stories with title, acceptance criteria, size signal, and splitting rationale

**Output:**
```
Epic: <title>
Split strategy: <pattern used — e.g. Workflow Steps + Happy/Unhappy Path>

Child Stories:
1. [S] <title>
   Value: <one-line user benefit>
   AC:
   - Given <ctx>, When <action>, Then <outcome>
   Splitting rationale: <why this is its own story>
   INVEST: I✅ N✅ V✅ E✅ S✅ T✅

2. [M] <title>
   ...
```

**Create in Jira (MCP):**
```
jira_create_issue(project: "PROJ", issue_type: "Story", summary: "<title>",
  description: "<AC + rationale>", parent: "PROJ-epic", labels: ["vertical-slice"])
```

> **Tip:** Combine with the `story-slicing` skill for codebase-grounded sizing.

---

## 2. Story Enhancement

> *"Improve this ticket"* / *"Rewrite this story"* / *"This description is vague"*

**Input:** Paste the raw ticket title + description in any format.

**What the agent does:**
- Rewrites using `As a / I want / So that` template
- Fills in or completes acceptance criteria as Given/When/Then
- Flags INVEST violations with specific fixes
- Adjusts tone for the right audience (engineering, product, or stakeholder)
- Ensures scope is bounded (not over-specified, not under-specified)

**Example:**
```
Before: "Add search to the app"

After:
Title: User can search products by keyword

As a shopper
I want to search for products by entering a keyword
So that I can find what I need without browsing every category

Acceptance Criteria:
- Given I type 3+ characters, When I submit search, Then results matching name or
  description appear ranked by relevance
- Given no results match, Then "No results for X" message shown with a reset link
- Given I clear the search field, Then the full product list is restored

INVEST fixes applied:
  ❌ Not Estimable — scope was unbounded → ✅ Scoped: keyword match on name + description only, no fuzzy
  ❌ Not Testable — no AC → ✅ 3 Given/When/Then criteria added
```

**Update in Jira (MCP):**
```
jira_update_issue(issue_key: "PROJ-123", fields: {
  summary: "<enhanced title>",
  description: "<enhanced description with AC>"
})
```

---

## 3. Comment Thread Summary

> *"Summarize this ticket"* / *"TLDR this thread"* / *"What's the current status?"*

**Input:** Paste the comment thread — or fetch via MCP:
```
jira_get_issue(issue_key: "PROJ-123")   # includes description + all comments
```

**Output:**
```
## Summary: PROJ-123 — <issue title>

Status: <current status>   Last updated: <date>

### What's been decided
- <decision 1 with date/author>
- <decision 2>

### Key context
- <important constraint or background>

### Open questions
- <unresolved item> — needs input from <person/team>

### Action items
- [ ] <action> — owner: <name>
- [ ] <action> — owner: <name>

### What needs to happen next
<one-paragraph recommendation>
```

---

## 4. Edge Case Generator

> *"What are the edge cases for this story?"* / *"What am I missing in the AC?"*

**Input:** Paste the story title + acceptance criteria.

**Output:**
```
Story: <title>
Happy path covered: ✅

Edge cases by category:

🔴 Error / failure states
  - Empty input submitted
  - Input exceeds max length (what's the limit?)
  - Upstream service returns 500

🟡 Boundary conditions
  - Exactly 0 items vs. 1 vs. the maximum
  - Date is today / yesterday / tomorrow / far future

🟠 Authorization
  - Non-owner attempts access
  - Session expires mid-flow
  - Role lacks required permission

⚪ Empty / null states
  - No results match the query
  - Required field is null in the database
  - First-time user with no history

Suggested additional AC (ranked by risk):
1. [HIGH]   Given empty input submitted, Then inline validation error shown
2. [MEDIUM] Given session expires during the flow, Then redirect to login with state preserved
3. [LOW]    Given 0 results match, Then "No results" message with reset action shown
```

---

## 5. Dependency Detector

> *"Find dependencies in these stories"* / *"Which stories are blocking each other?"*

**Input:** Paste a list of stories, or fetch the sprint via MCP:
```
jira_search_issues(jql: "sprint in openSprints() AND project = PROJ ORDER BY rank ASC")
```

**What the agent does:**
- Identifies shared data entities, API endpoints, auth preconditions, and sequential user flows
- Classifies as hard dependency (blocked) or soft dependency (integration risk)
- Suggests a delivery sequencing order

**Output:**
```
Dependency Analysis — <Sprint or Epic>

⛔ Hard dependencies (cannot start until blocker is done):
  PROJ-12 → BLOCKED BY → PROJ-8   (shares Order entity)
  PROJ-15 → BLOCKED BY → PROJ-12  (admin view requires checkout to exist)

⚠️  Soft dependencies (can start in parallel; integration needed):
  PROJ-10 and PROJ-12 — both write to the Order table
  PROJ-11 and PROJ-9  — both use the same Stripe credentials

✅ Fully independent:
  PROJ-13  PROJ-14

Suggested sequencing:
  Week 1: PROJ-8 → PROJ-9
  Week 2: PROJ-10, PROJ-11, PROJ-12 (parallel)
  Week 3: PROJ-13, PROJ-14, PROJ-15
```

**Create dependency links in Jira (MCP):**
```
jira_create_issue_link(inward_issue: "PROJ-12", outward_issue: "PROJ-8", link_type: "is blocked by")
```

---

## 6. Story Point Estimator

> *"Estimate this story"* / *"How complex is this?"* / *"Give me a point estimate with reasoning"*

**Input:** Story title + description. Optionally, paste codebase scan output for higher accuracy.

**Estimation model (Fibonacci: 1, 2, 3, 5, 8, 13):**

| Complexity signal | Points |
|-------------------|--------|
| Base (any story) | 1 |
| Each additional service touched | +1 |
| New DB table or migration | +2 |
| New external integration / third-party API | +3 |
| Auth / permission change | +2 |
| > 5 acceptance criteria | +1 |
| Team unfamiliar with this area of codebase | +2 |
| Cross-platform (web + mobile) | +2 |
| Performance or scalability NFR | +2 |

**Output:**
```
Story: <title>
Estimate: 5 points

Reasoning:
  Base                              → 1
  1 new endpoint (POST /sessions)   → +1
  JWT auth token generation         → +2
  Team hasn't touched auth in 6mo   → +2 (unfamiliarity)
  Total: 6 → rounded to 5 (Fibonacci)

Confidence: Medium
If confidence is low: consider a 1-point spike first.
Spike focus: <specific unknown to investigate>
```

---

## 7. Natural Language → JQL

> *"Find all stories stuck in progress for more than 5 days"*
> *"Show me unresolved bugs assigned to me this sprint"*

**What the agent does:** Translates plain English into valid JQL, then optionally executes it via MCP.

**Examples:**

| Plain English | JQL |
|--------------|-----|
| Stories in progress for more than 5 days | `project = PROJ AND status = "In Progress" AND status changed to "In Progress" before -5d` |
| Unresolved bugs assigned to me this sprint | `project = PROJ AND issuetype = Bug AND status != Done AND assignee = currentUser() AND sprint in openSprints()` |
| Epics with no child stories | `project = PROJ AND issuetype = Epic AND issueFunction not in subtasksOf("issuetype = Story")` |
| Stories completed last sprint | `project = PROJ AND sprint in closedSprints() AND status = Done AND issuetype = Story` |
| High-priority blockers from last 2 weeks | `project = PROJ AND labels = blocked AND priority in (High, Highest) AND created >= -14d ORDER BY created DESC` |
| Stories without an assignee in this sprint | `project = PROJ AND sprint in openSprints() AND assignee is EMPTY` |
| All stories that changed status today | `project = PROJ AND status changed after startOfDay()` |

**Execute via MCP:**
```
jira_search_issues(jql: "<generated JQL>", max_results: 25)
```

**Graceful fallback:** Output the JQL as a copyable string — paste directly into Jira's issue navigator.

---

## Agent Instructions

When applying this skill, the agent should:

1. Identify which command the user is invoking from their trigger phrase
2. Ask for the input (ticket text, epic, comment thread) if not provided — or fetch via MCP
3. Apply the relevant command and produce the structured output
4. If Jira MCP is available, offer to execute the result (create tickets, update fields, run JQL)
5. If multiple commands are useful (e.g., enhance a story *and* generate edge cases), chain them automatically

---

## MCP Quickref

```
jira_get_issue(issue_key: "PROJ-123")
jira_search_issues(jql: "<jql>", max_results: 25)
jira_create_issue(project: "PROJ", issue_type: "Story", summary: "...", description: "...", parent: "PROJ-epic")
jira_update_issue(issue_key: "PROJ-123", fields: { summary: "...", description: "..." })
jira_create_issue_link(inward_issue: "PROJ-A", outward_issue: "PROJ-B", link_type: "is blocked by")
jira_transition_issue(issue_key: "PROJ-123", transition: "In Progress")
```

---

## References

- Atlassian: [AI Features in Jira](https://www.atlassian.com/blog/artificial-intelligence/ai-jira-issues)
- Bill Wake: [INVEST in Good Stories](https://xp123.com/invest-in-good-stories-and-smart-tasks/)
- Richard Lawrence: [Story Splitting Flowchart](https://agileforall.com/resources/how-to-split-a-user-story/)
- LeadDev: [Making refinement less painful](https://leaddev.com/agile-other-ways-working)
