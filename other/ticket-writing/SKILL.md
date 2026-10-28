---
name: ticket-writing
description: >-
  Writing clear, actionable tickets in any issue tracker (Jira, Linear, GitHub Issues,
  ServiceNow, etc.). Use when: creating epics, stories, tasks, bugs, or spikes; writing
  acceptance criteria; decomposing work for a sprint; linking dependencies between
  tickets; auditing backlog items for clarity; or coaching a team on ticket quality.
  Covers title conventions, description templates, acceptance criteria, decomposition
  rules, dependency linking, and org-specific pluggable configuration.
tags:
  - developer
  - manager
  - operations
  - general
---

# Ticket Writing

## When to Use

- Writing a new epic, story, task, bug, or spike
- Reviewing a ticket before it enters sprint planning
- Auditing backlog items for clarity and actionability
- Decomposing an epic into ready-to-work stories
- Linking related tickets, dependencies, or blockers
- Coaching a team member on how to write better tickets

---

## Guiding Principles

1. **Any engineer can pick it up cold** — The ticket must be self-contained. No oral lore required.
2. **One clear outcome** — A ticket should answer: "How will I know when this is done?"
3. **Right size** — A story should take 1–5 days. Split anything larger. Combine anything smaller.
4. **Outcome over activity** — Describe the result, not the steps to get there.
5. **User language for stories, system language for tasks** — Stories frame user value; tasks frame technical work.
6. **Dependencies are explicit** — Blocks, is-blocked-by, and relates-to links are set before the ticket enters the sprint.

---

## Ticket Type Reference

| Type | Purpose | Size target |
|------|---------|-------------|
| **Epic** | A complete user-facing capability; deliverable in a quarter or less | Quarter |
| **Story** | A user-facing feature or behavior change | 1–5 days |
| **Task** | Internal technical work (infra, tooling, refactor, data migration) | 1–3 days |
| **Bug** | A defect in existing, shipped functionality | 1–2 days |
| **Spike** | Time-boxed investigation to reduce uncertainty | Fixed: 1–2 days max |
| **Sub-task** | A unit of work within a story, tracked by the same engineer or pair | Hours |

---

## Title Conventions

A good title is search-friendly, imperative, and specific — no jargon, no vagueness.

**Format**: `[Verb] [object] [qualifying context if needed]`

| Good | Bad |
|------|-----|
| `Add pagination to the activity feed API` | `Activity feed work` |
| `Fix 500 error when user submits empty search query` | `Search bug` |
| `Migrate user table to use UUID primary keys` | `Database migration` |
| `Spike: evaluate DynamoDB vs Aurora for audit log storage` | `Research DB options` |
| `Add retry logic to Stripe charge webhook handler` | `Handle webhook failures better` |

**Rules**:
- Start with a verb: Add, Fix, Refactor, Migrate, Remove, Update, Implement, Spike, Document
- Avoid acronyms unless universally known in your org
- Do not include sprint numbers or dates in the title
- Do not use "we should…" or "need to…" — write the action directly

---

## Description Templates

Pick the template for the ticket type. Fill every section. Delete none.

### Story Template

```markdown
## Context

[1–3 sentences on why this work matters. What problem does it solve for the user?
Link to the parent epic and any relevant design doc or Confluence page.]

## User Story

As a [user persona],
I want to [specific action],
So that [concrete benefit].

## Acceptance Criteria

- [ ] [Specific, testable, binary condition]
- [ ] [Specific, testable, binary condition]
- [ ] [Specific, testable, binary condition]
(Add as many as needed. Each line must be independently verifiable.)

## Out of Scope

- [Anything explicitly NOT covered by this ticket]
- [Reference a separate ticket number if that work already exists]

## Notes / Open Questions

- [Any ambiguity or decision needed before work starts]
- [Link to relevant Slack thread, doc, or prior ticket if context exists]
```

---

### Task Template

```markdown
## Context

[1–3 sentences on why this technical work is needed. What breaks or degrades without it?
Link to the driving story or epic.]

## Work to Be Done

1. [Concrete implementation step]
2. [Concrete implementation step]
3. [Add tests / validation]

## Definition of Done

- [ ] [Specific, verifiable completion condition]
- [ ] [Specific, verifiable completion condition]
- [ ] Tests written and passing
- [ ] PR reviewed and merged

## Out of Scope

- [Anything explicitly not included]

## Notes / Open Questions

- [Unknowns, design constraints, or reference links]
```

---

### Bug Template

```markdown
## Summary

[One-sentence description of the defect and its impact.]

## Environment

- **Version / Branch**: [e.g., v2.3.1 / main]
- **Affected users**: [All users / logged-out users / admin role only]
- **Frequency**: [Always / intermittent — approx. X% of the time]
- **Severity**: [P1 — user blocked / P2 — workaround exists / P3 — cosmetic]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Observe the bug]

## Expected Behavior

[What should happen.]

## Actual Behavior

[What actually happens. Include error message, screenshot, or log snippet.]

## Root Cause (if known)

[Leave blank if unknown — fill in during investigation.]

## Fix Acceptance Criteria

- [ ] Reproducer no longer triggers the defect
- [ ] Regression test added
- [ ] No new errors introduced in related flows

## Linked Items

- Parent epic / story: [link or ticket number]
- Related bug reports: [link or ticket number]
```

---

### Spike Template

```markdown
## Question to Answer

[The single, specific question this spike must answer. If you have more than one question,
split into separate spikes.]

## Why This Matters

[What decision or work is blocked until this question is answered?]

## Time Box

**Maximum**: [1 day / 2 days] — Hard stop regardless of outcome.

## Success Criteria

By the end of this spike, we will have:
- [ ] A written recommendation (with rationale) for [question]
- [ ] Identified risks or unknowns for the recommended approach
- [ ] Updated [design doc / Confluence page / ticket description] with findings

## Approaches to Investigate

- Option A: [brief description]
- Option B: [brief description]

## Out of Scope

- Actual implementation (this is research only)
```

---

## Writing Good Acceptance Criteria

Acceptance criteria (AC) define "done." Each criterion must be:

- **Binary** — Pass or fail, no judgment calls
- **Testable** — An engineer or QA can verify it without asking the author
- **Specific** — No vague words like "fast," "correct," or "appropriate"
- **Scoped** — Covers exactly this ticket, not adjacent functionality

### Bad vs. Good AC

| Bad (vague, untenable) | Good (specific, testable) |
|------------------------|---------------------------|
| `The page loads quickly` | `The activity feed loads within 2s at P95 under normal load` |
| `Errors are handled gracefully` | `A 503 from the upstream API returns a user-facing error message and logs a structured error with request ID` |
| `The form works correctly` | `Submitting the form with an empty email field shows a validation error and does not submit` |
| `Admin can manage users` | `Admin can deactivate a user; deactivated user receives an email and can no longer log in` |
| `Tests are written` | `Unit tests cover the happy path and the empty-input edge case; coverage does not decrease` |

### AC for Different Ticket Types

**Stories** — Frame in user-observable behavior:
```
- [ ] User can filter results by date range using start and end date pickers
- [ ] Selecting a date range updates results without a full page reload
- [ ] Invalid date ranges (end before start) display an inline validation error
```

**Tasks** — Frame in technical completion signals:
```
- [ ] Migration script runs idempotently (safe to run twice)
- [ ] All existing records have been backfilled with non-null `created_at` timestamp
- [ ] Rollback script documented in runbook
```

**Bugs** — Frame in "defect no longer reproducible":
```
- [ ] Steps to reproduce no longer trigger the 500 error
- [ ] New regression test added to the test suite
- [ ] Existing tests pass without modification
```

---

## Decomposition Rules

Use these rules to decide when to split a ticket.

### Split When…

| Signal | Action |
|--------|--------|
| Estimate > 5 days | Split into independent stories |
| AC list > 8–10 items | Split by user scenario or persona |
| Multiple distinct user workflows | One story per workflow |
| Frontend and backend can ship independently | Split into separate tickets |
| Ticket touches > 2 unrelated systems | Split by system boundary |
| A prerequisite task is large enough to track separately | Extract a Task or Sub-task |

### Do Not Split When…

- The front-end and back-end are tightly coupled and cannot be tested independently
- The resulting pieces would not be independently deployable or reviewable
- The sub-tasks are so small they add more overhead than value (< 2 hours)

### Decomposition Pattern

```
Epic: User can manage their notification preferences
  └─ Story: User can view their current notification settings
  └─ Story: User can enable or disable email notifications
  └─ Story: User can enable or disable push notifications
  └─ Story: User receives an in-app confirmation when preferences are saved
  └─ Task: Add notification_preferences table to DB schema
  └─ Task: Write migration to backfill defaults for existing users
```

---

## Linking Dependencies

Dependencies must be explicit **before** a ticket enters a sprint. Undiscovered dependencies mid-sprint are a leading cause of carry-over.

### Link Types

| Relationship | Use When |
|-------------|----------|
| **blocks** | This ticket must be completed before the linked ticket can start |
| **is blocked by** | This ticket cannot start until the linked ticket is complete |
| **relates to** | Related context — not a hard dependency, but useful for cross-reference |
| **duplicates** | This ticket covers the same work as the linked ticket (close one) |
| **is cloned from** | This ticket was copied from the linked ticket (for recurring work) |
| **implements** (or **child of**) | This story or task implements the linked epic |

### When to Link

- **At creation time** — If you know the dependency exists, link immediately
- **During backlog refinement** — Review parent epic links; check upstream service dependencies
- **During sprint planning** — Any ticket with an unresolved blocker link must stay in backlog
- **After discovery** — If a blocker surfaces mid-sprint, add the link immediately and surface to the team

### Dependency Red Flags

- A ticket is in the sprint but its blocker is not scheduled — **escalate immediately**
- A ticket has no parent epic link — **add it or create the epic**
- Cross-team dependencies have no linked counterpart ticket in the other team's backlog — **create a ticket there and link**

---

## Linking External Resources

Every ticket should link out to the information needed to work it. Do not make an engineer hunt.

| Resource Type | When to Link |
|--------------|-------------|
| **Design doc / RFC** | Any ticket based on a design decision |
| **Confluence page** | Runbooks, team wikis, architecture docs, meeting notes |
| **Figma / design mockup** | Any front-end story |
| **API contract / OpenAPI spec** | Any API integration ticket |
| **Relevant PR / previous commit** | Bug tickets, refactor tasks |
| **Slack thread** | Where the decision or requirement originated |
| **Monitoring dashboard** | Bug and performance tickets |
| **External documentation** | Third-party APIs, vendor SDKs |

**Rule**: If you had to open a tab to understand the scope, link that tab in the ticket.

---

## Pre-Sprint Readiness Checklist

Before a ticket can be pulled into a sprint, it must meet all of the following:

- [ ] Title is imperative, specific, and jargon-free
- [ ] Type is set (Story / Task / Bug / Spike)
- [ ] Parent epic is linked
- [ ] Description is complete (no empty sections)
- [ ] Acceptance criteria are written (binary, testable, specific)
- [ ] Estimate is set (story points or days)
- [ ] Blocking and blocked-by links are set
- [ ] External resource links added where applicable
- [ ] Org-specific fields filled: component, label/tag, assignee, priority (see below)

Any ticket that fails this checklist goes back to backlog refinement, not into the sprint.

---

## Org-Specific Configuration

The fields below are **pluggable** — substitute your org's values when using this skill. If your org
has a verified connections file or private knowledge base, load that first and populate these before
drafting tickets.

```yaml
# ticket-writing org configuration
# Populate this for your org, then reference it when writing tickets.

tracker: jira                         # jira | linear | github-issues | servicenow | other
base_url: https://jira.example.com    # Your tracker's base URL

projects:
  default: ENG                        # Default project key/identifier
  infra: INFRA
  platform: PLAT
  # Add your org's project keys here

components:
  # Map to your org's component list (service names, layers, etc.)
  - api
  - frontend
  - data-pipeline
  - infrastructure

labels_or_tags:
  # Org-standard labels. Add/remove to match your label taxonomy.
  - tech-debt
  - customer-facing
  - security
  - compliance
  - performance
  - on-call-reduction
  - dependency                        # Cross-team dependency

priority_levels:
  # Align to your org's priority definitions
  p1: "User blocked, no workaround — fix in < 24h"
  p2: "Significant impact, workaround exists — fix this sprint"
  p3: "Minor issue or improvement — schedule in backlog"
  p4: "Cosmetic or nice-to-have — icebox until prioritized"

assignee_rules:
  # Document your org's conventions for initial ticket assignment
  unassigned_on_creation: true        # true = leave unassigned until sprint planning
  auto_assign_bugs_to: oncall         # oncall | triage-rotation | reporting-engineer
  spike_owner: requesting_em          # Who owns a spike: EM or senior engineer

story_points_scale: fibonacci         # fibonacci | linear | t-shirt
default_sprint_capacity_pts: 30       # Rough per-engineer capacity per 2-week sprint

custom_fields:
  # Add org-specific custom fields here
  # team: Platform Engineering
  # cost_center: "12345"
```

### How to Use This Configuration

1. Store your completed config locally in a gitignored file, for example `ticket-writing-config.yaml`.
2. When the agent writes a ticket, reference the config to fill: `project`, `component`, `labels`, `priority`, and `assignee`.
3. If a field in the config is marked `true` for "unassigned on creation," do not set an assignee — leave it blank for sprint planning.
4. For `auto_assign_bugs_to: oncall`, look up the current on-call rotation before assigning.

---

## Common Anti-Patterns

| Anti-pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Title is a noun phrase ("Payment bug") | No action, not searchable | Use a verb: "Fix null error when payment method is missing" |
| AC is a list of implementation steps | Steps change; done-ness should not | Rewrite as observable outcomes |
| "As a user, I want a button" | Describes UI, not value | "As a user, I want to save my search so I can rerun it later" |
| Estimate is 0 | Nothing is zero effort | Minimum estimate: 1 point / half-day |
| Blockers not linked at sprint start | Surprise mid-sprint | Run dependency check during backlog refinement |
| Description is empty, all context is in comments | Comments are not durable | Move essential context into the description itself |
| Epic has 40+ stories | Scope is not a quarter, it's a year | Split into multiple focused epics |
| "Will do in follow-up ticket" with no link | Follow-up never happens | Create the ticket now and link it |

---

## Ticket Audit Workflow

When auditing a backlog for quality, apply this checklist ticket by ticket:

1. **Title** — Is it imperative, specific, and < 80 characters?
2. **Type** — Is the right type selected?
3. **Size** — Is the estimate reasonable for the type? Needs splitting?
4. **Description** — Are all template sections filled?
5. **AC** — Is every criterion binary and testable?
6. **Links** — Parent epic, blockers, related tickets, and external docs linked?
7. **Fields** — Component, labels, priority, and assignee set per org config?
8. **Staleness** — Is this ticket > 90 days old with no activity? Archive or close.

Produce a summary following this format for any backlog audit:

```markdown
## Backlog Audit — [Project] — [Date]

### Summary
- Total tickets reviewed: N
- Ready for sprint: N
- Needs refinement: N
- Recommend closing / archiving: N

### Needs Refinement (top issues)
| Ticket | Issue | Recommended Fix |
|--------|-------|----------------|
| [key] | Missing AC | Add acceptance criteria before next sprint planning |
| [key] | Estimate missing | Estimate during next refinement session |
| [key] | No parent epic | Link to [epic] or create a new epic |

### Recommend Closing
| Ticket | Reason |
|--------|--------|
| [key] | No activity in 6 months, superseded by [key] |
```
