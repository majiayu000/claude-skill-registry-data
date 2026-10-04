---
name: write-ac
description: Write acceptance criteria for a Jira story using Given/When/Then scenarios. Use this skill when the user asks to write AC, acceptance criteria, write scenarios, improve a story, add AC to a ticket, or mentions a Jira ticket and wants better requirements. Also triggers on "write better AC", "this story needs AC", "add scenarios to this ticket", or when reviewing a Jira story for completeness.
---

# Write Acceptance Criteria

Write user-focused acceptance criteria for Jira stories using numbered Given/When/Then scenarios.

The goal is to describe what the user experiences and what outcomes they observe — never how the system implements it. Good AC reads like a conversation about what "done" looks like from the user's chair.

## Process

### 1. Gather context

- Read the Jira ticket via `mcp__mcp-atlassian__jira_get_issue` (use `fields: "*all"` to get full description)
- Read any linked or parent tickets for broader context
- If a code path is mentioned or relevant, explore the codebase to understand what exists today
- Note the existing description — preserve anything useful

### 2. Draft the ticket description

Structure the updated description with three sections:

**Why** — 2-3 sentences on the business/user value. What problem does this solve? What does it unblock? This is the most important section because it aligns the team on purpose before diving into details.

**Context** — Brief background on the current state. What exists, what's broken, what changed. Preserve good context from the original ticket.

**Acceptance Criteria** — Numbered scenarios in Given/When/Then format.

### 3. Review with user

Present the AC in markdown for review BEFORE pushing to Jira. Incorporate feedback iteratively — the user knows their domain better than you do.

### 4. Push to Jira

Once approved, update the ticket via `mcp__mcp-atlassian__jira_update_issue`.

## Writing good scenarios

Each scenario follows this format:

```
Scenario N - {descriptive name}

Given {precondition from the user's perspective}
When {user action}
Then {observable outcome}
```

What makes a scenario good:

- **User and outcome focused** — describe what the user does and sees. "I can compare responses side by side" not "DualView component renders two ResponsePanels."
- **No implementation details** — no file paths, class names, API endpoints, database tables, environment variables, or port numbers. Those belong in implementation notes, not AC.
- **No prescribing HOW** — only WHAT the user experiences. The team picks the implementation.
- **Concrete examples** — use real examples to make scenarios tangible (e.g. "Haiku vs Sonnet" rather than "two different models"). This grounds abstract scenarios in something the reader can picture.
- **Independently understandable** — each scenario stands on its own without needing to read the others.
- **Cover the full picture** — happy path, key variations, edge cases, and failure modes. Think about what happens when things go wrong, not just when everything works.

Common mistakes to avoid:
- Sneaking in tech details disguised as user language ("When the API returns a 500" — the user doesn't see status codes)
- Writing scenarios that are really test scripts with exact click sequences
- Combining multiple behaviors into one scenario — split them

## Jira formatting

When pushing to Jira, use wiki markup:

```
h2. Why

{why text}

h2. Context

{context text}

h2. Acceptance Criteria

h3. Scenario 1 - {name}

*Given* {precondition}
*When* {action}
*Then* {outcome}

h3. Scenario 2 - {name}

*Given* {precondition}
*When* {action}
*Then* {outcome}
```

Use blank lines between sections for separation. Do NOT use `----` horizontal rules — Jira mangles them into heading tags.
