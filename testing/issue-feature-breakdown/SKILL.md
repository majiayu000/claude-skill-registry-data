---
name: issue-feature-breakdown
category: business-product
codex-short-description: "Gather Jira/Confluence context + council pass into an actionable breakdown plan"
description: >
  Analyze a Jira ticket into an actionable breakdown, following linked tickets and
  Confluence context to surface gaps and ambiguities. Read-only. Use when the user says
  "break down this feature", "analyze this ticket", "feature breakdown", or provides a
  ticket key for analysis.
related-skills:
  - clarity-council
loop-eligible: false

compatibility: claude-code codex opencode
---

# Feature Breakdown

Read-only analysis of a Jira feature ticket. Gathers context, consults the clarity-council, resolves ambiguities with the user, and produces an actionable breakdown.

**All operations are read-only. Never create, update, or transition Jira tickets.**

## Input

A Jira ticket key (e.g. `PROJ-123`). Extract from the user's message using pattern `[A-Z][A-Z0-9]+-\d+`.

## Workflow

### Phase 1 — Gather Context

1. Fetch the root ticket via `jira_get_issue` — capture summary, description, acceptance criteria, status, priority, story points, fix version, and sprint.
2. Fetch comments via `jira_get_comments`.
3. Walk **all linked tickets** (issue links from the root ticket's `issuelinks` field):
   - For each link: fetch via `jira_get_issue`, note the link type (blocks / is blocked by / relates to / etc.).
   - If the root ticket belongs to an **epic/feature**: fetch sibling stories via `jira_get_epic_issues`.
4. Check for **Confluence context**:
   - Fetch remote links via `jira_get_remote_links` — read any linked Confluence pages via `confluence_get_page`.
   - Search Confluence via `confluence_search` with CQL: `text ~ "TICKET-KEY"` to find pages that reference this ticket.
5. Compile a **Context Summary** and present it to the user. Include:
   - Root ticket details
   - Linked ticket summaries (with link types)
   - Confluence page titles and key excerpts
   - Any acceptance criteria found

**Gate:** Ask the user if any additional tickets or documents should be included before proceeding.

### Phase 2 — Council Analysis

Invoke `/clarity-council` in multi mode:

- **user_problem**: "Analyze this feature and identify what is being asked, what assumptions are being made, and what gaps or ambiguities exist."
- **context**: The full Context Summary from Phase 1.
- **desired_outcome**: "A clear understanding of the feature scope, identified gaps, risks, and open questions that need answers before implementation can begin."
- **selected_personas**: Researcher, Senior Architect, Product Owner, Tech Lead, QA Engineer, Devil's Advocate
- **depth**: standard

Persona focus:
- **Researcher** — owns evidence quality. Audits the Context Summary for missing source citations, unverified claims, and assumptions stated as facts. Surfaces the "what would we need to know to be confident?" questions that the other personas tend to skip past. Failure mode the researcher will catch: a council that confidently scopes a feature on top of an undocumented assumption.
- **Senior architect** — structural implications and integration seams.
- **Product owner** — scope, value, and acceptance criteria clarity.
- **Tech lead** — implementation risk and dependencies on other in-flight work.
- **QA engineer** — testability and edge-case enumeration.
- **Devil's advocate** — challenges the proposed scope; flags hidden assumptions.

Present the council's synthesis to the user: agreements, conflicts, risks/tradeoffs, and the questions each persona raised. **Lead with the researcher's evidence-gap list** — those questions usually need to be answered before any of the others can be productively closed.

### Phase 3 — Clarify

Collect all unresolved questions from the council output and any gaps identified in Phase 1.

Ask the user **one question at a time**. For each question:
- State which persona raised it and why it matters.
- Offer a recommended answer if the gathered context suggests one.
- Wait for the user's response before asking the next question.

Continue until:
- All questions are resolved, OR
- The user says they have enough clarity to proceed.

### Phase 4 — Breakdown Plan

Using the resolved context, produce a structured breakdown. See [BREAKDOWN-FORMAT.md](BREAKDOWN-FORMAT.md) for the output template.

Each item in the breakdown should include:
- **What**: A concrete, implementable unit of work
- **Why**: How it connects to the feature goal
- **Acceptance criteria**: Testable conditions (derived from the ticket + council analysis)
- **Dependencies**: Which other items must complete first
- **Risk/complexity**: Flag from council analysis (if any)

**Gate:** Present the breakdown and ask:
1. Does this cover the full scope?
2. Are any items too large or too small?
3. Should any items be reordered or merged?

Iterate until the user approves.

## Constraints

- **Read-only**: Never call `jira_create_issue`, `jira_update_issue`, `jira_transition_issue`, or any write operation on Jira or Confluence.
- Do not create files on disk unless the user explicitly asks to save the breakdown.
- If the Jira ticket key cannot be found, stop and ask the user to provide a valid key.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Breakdown items are vertical slices, not layers — each delivers observable value
- Gaps and ambiguities from the council pass are listed explicitly, not silently resolved
- Dependencies between items are stated
- Every claim about the ticket is grounded in gathered Jira/Confluence context, not assumed

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/issue-feature-breakdown.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
