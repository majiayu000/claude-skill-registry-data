---
name: ticket
description: >
  Pull a Jira issue and scaffold a feature spec with test stubs.
  Use when starting work on a new Jira ticket or GitHub issue.
  Reads acceptance criteria, description, and comments. Requires
  Jira MCP server for Jira tickets. Triggers on: ticket, issue,
  PROJ-*, start work on, pick up.
---

## Ticket to Spec + Test Stubs

### Step 1: Fetch Ticket
Use the Jira MCP server to fetch ticket `$ARGUMENTS`:
- Summary and description
- Acceptance criteria (check the AC field, or custom fields)
- Comments (often contain clarifications)
- Linked issues and subtasks

If Jira MCP is not available, ask the user to paste the ticket details.

### Step 2: Analyze Requirements
Extract testable requirements from (in priority order):
1. Acceptance criteria field (if present)
2. Description (parse for behavioral statements)
3. Comments (look for clarifications from product/QA)

If requirements are too vague to write tests, STOP and output:

```
⚠️ CLARIFICATION NEEDED — Ticket lacks clear testable requirements.
What I found: [summary]
What I need: [specific questions]
```

### Step 3: Create Feature Spec
Create `docs/context/specs/<ticket-id>-<short-name>.md` with sections:
- Source (ticket URL)
- Context (from description)
- Acceptance Criteria (from AC field or synthesized)
- Technical Approach (proposed, marked DRAFT)
- Test Plan (unit + integration test cases)
- Open Questions (any ambiguity found)

### Step 4: Scaffold Test Stubs
Detect the project stack and create test file(s) with empty test
functions matching the acceptance criteria.

### Step 5: Update Sprint
Add the ticket to `docs/context/CURRENT_SPRINT.md` as "In Progress".
