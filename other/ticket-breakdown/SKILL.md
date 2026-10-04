---
name: ticket-breakdown
description: >
  Produces an actionable, well-ordered ticket breakdown document from a macro-scoping and/or
  technical-scoping document. Use this skill whenever a user wants to structure and plan tickets,
  break down a feature into stories, estimate work, build a backlog, or says things like
  "on découpe en tickets", "écris les tickets", "on fait le backlog", "je veux les US".
  Always trigger after a technical-scoping document has been produced, or when the user explicitly
  asks for a ticket breakdown even without a full spec.
  Does NOT create tickets in any tool — use the `create-ticket` skill to push the output to Jira.
---

## Purpose

Transform a macro + technical specification into a clean, ordered, actionable ticket breakdown document.
No spec debates here — execute the spec.

## Inputs to collect

Before producing the tickets, make sure you have:

- The macro-scoping document (or a clear feature description)
- The technical-scoping document (if available)
- Team conventions: tags (e.g. [CRM], [PERF]), DoD expectations, review process
- The CIDF ticket number (`CIDF-XXXX`) — the tracking ticket on the **CIDF board** (board de cadrage).  
  It should be present in the macro or technical scoping document. If not, ask the user.

## How to reason about the breakdown

Before writing any ticket, answer these 5 questions internally:

1. **Who triggers?** — what initiates the flow?
2. **Who detects?** — what identifies eligible entities?
3. **Who executes?** — what applies the change?
4. **Who informs?** — what notifies users or systems?
5. **Who observes?** — what lets agents or operators monitor?

Each answer is a candidate ticket. Never mix two responsibilities into one ticket.

**Core rules:**

- Break down by business responsibility, not by technical layer.
  "Ticket backend" or "ticket frontend" are bad tickets. "ETQ système, je peux planifier…" is good.
- Separate User Stories (observable capability) from Technical Tasks (infrastructure support).
  A User Story produces something observable. A Technical Task only supports a User Story.
- Always separate feature implementation from data migration.
  A migration is never the feature.
- Create spike/exploration tickets for anything that involves external dependencies,
  strong hypotheses, significant technical uncertainty, or high volume.
  Never mix exploration with final implementation.

**A ticket must be:**

- Estimable (developers can size it without a 1-hour debate)
- Testable (there are clear acceptance criteria)
- Deliverable independently (no implicit unlisted dependencies)
- Understandable in 5 minutes

**Signs a ticket is too big:**

- More than 3 days of estimated work
- More than one clear "who benefits"
- Developers would debate its scope for 30+ minutes
- It mixes exploration with final implementation

**Anti-patterns to avoid:**

- Ticket mixing refactor + feature + migration + infra → split it
- Ticket named "improve authentication" or "update security" → too vague
- Ticket without acceptance criteria → always add them
- Ticket with a DoD that depends on another unwritten ticket → make the dependency explicit

## Output format

Read `assets/template.md` and produce between 10 and 30 tickets maximum, in French.
Order them by recommended implementation sequence.
Separate User Stories and Technical Tasks clearly.
Include a recommended delivery order at the end with a brief rationale for each step.

## Bridge to Jira

Once the breakdown document has been validated, the user can push each ticket to Jira
one by one using the `create-ticket` skill.
The `create-ticket` skill will use this document as its source of truth for pre-filling
summary, description, acceptance criteria and identified tasks.

**Boards :**

- Implementation tickets (User Stories, Technical Tasks) → **IDF board** (`IDF-XXXX`)
- The overall cadrage / epic tracking → **CIDF board** (`CIDF-XXXX`)  
  The CIDF ticket is the reference for TL, CTO, and client to follow the scoping progress.  
  Include the CIDF ticket number in the breakdown document header if available.

## Golden rules

- One ticket = one clear responsibility.
- Break down by business responsibility, not by technical layer.
- A good breakdown lets developers estimate without debating scope.
- Migration ≠ feature. Always separate them.
- US = observable capability. Technical task = support for a US.
- The spec is not debated here — it is executed.
