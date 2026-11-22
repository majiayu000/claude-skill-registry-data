---
name: jira-implement
description: Implement a Jira ticket end-to-end - read the ticket, clarify, plan via /plan, execute via /execute-plan, create the MR, and comment the MR link back on the ticket.
user-invocable: true
disable-model-invocation: false
argument-hint: "<ISSUE-KEY> [--plan-only]"
---

# Implement a Jira ticket end-to-end

Slimmed from the workspace `/jira-implement` (493 → this). **OPTIONAL: lives in
`.agentic/optional-skills/`; onboarding copies it into `.claude/skills/` only when
the team works from Jira. Requires the Atlassian/Jira MCP server.** Composition over
duplication: planning and execution are delegated to `/plan` and `/execute-plan` —
this skill only adds the ticket lifecycle around them.

Jira base URL: <!-- onboard:jira-url -->`TODO e.g. https://yourorg.atlassian.net`<!-- /onboard -->

## Step 1 — Fetch & parse

`jira_get_issue` for the key (epics: also `jira_get_epic_children`). Extract the
acceptance criteria verbatim — they seed the plan's AC→test mapping table.
Transition the ticket to In Progress (resolve the transition ID first; never guess IDs).

## Step 2 — Scope guardrails (stop and confirm with the user when any hit)

- Story points > 8, or the change clearly spans multiple repos.
- A bug with no reproduction path.
- Auth/security-touching work.
- Ambiguous or contradictory acceptance criteria.

## Step 3 — Clarify, then plan

Mandatory interview (3–7 questions, max 2 rounds) about intent and scope — not about
things the code answers. Then run `/plan` with the ticket content; name the spec
`plan-<issue-key>-<slug>.md`. Iterate until the user explicitly approves.
`--plan-only` stops here.

## Step 4 — Execute & deliver

- `/execute-plan` on the approved spec (branch: `feature/<issue-key>-<slug>`).
- After the MR exists: `jira_add_comment` with the MR link and a 2–3 line summary.
- Ticket transition after MR: <!-- onboard:jira-post-mr-transition -->`TODO — e.g. "none: In Review happens on staging deploy" or "transition to In Review"`<!-- /onboard -->
