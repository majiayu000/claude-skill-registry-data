---
name: decision
description: Make a product decision with full context from the vault and available sources
argument-hint: "[decision topic]"
---

# Make a Product Decision

You help make a well-informed product decision by gathering context from all available sources and producing structured documentation, follow-up tasks, and a communication draft.

## Input

The user provides a decision topic via `$ARGUMENTS`. Examples:
- "should we support feature X in the next release"
- "prioritize feature A vs feature B"
- "should we adopt GraphQL for the new API"

## Workflow

1. **Search the vault**:
   - Recent meetings in `Meetings/` that touched this topic
   - Daily notes in `journals/` (last 2 weeks) for related context
   - `Loose Notes/Work/` for related decisions or drafts
   - `Dashboard/Weekly P-Tasks.md` for related priorities

2. **Use GitHub MCP** (if configured):
   - Search repositories for related issues/PRs
   - Read engineering comments and discussions
   - Identify any blockers or concerns raised

3. **Ask for additional context** (before options):
   - "Do you have a Slack thread, document, or discussion about this decision? If yes, paste it now."
   - If provided: extract opinions, concerns, constraints.
   - If skipped: proceed without.

4. **Present context summary**:
   - Relevant notes and prior discussions
   - Strategy alignment (if strategy docs exist)
   - Customer data or validation (if any)
   - Engineering discussions and feasibility (from GitHub)

5. **Draft options with trade-offs**:
   - 2-3 viable options
   - For each: pros (benefits, alignment, customer value), cons (costs, risks, complexity, timeline)
   - Do not recommend yet - present objectively

6. **Create decision note**:
   - Location: `Loose Notes/Work/YYYY-MM-DD - Decision - [Topic].md`
   - Structure:

```markdown
---
tags: LooseNotes
date: YYYY-MM-DD
---
# Decision: [Topic]

**Date**: YYYY-MM-DD

## Context
[Why this decision is needed - background from notes, meetings, strategy]

## Options Considered
1. **Option 1**: [Description]
   - Pros: ...
   - Cons: ...
2. **Option 2**: [Description]
   - Pros: ...
   - Cons: ...

## Decision
[To be filled after review, or suggest recommendation if clear]

## Rationale
[Why this option, trade-offs accepted]

## Impact
[What changes, who is affected, timeline]

## Communication
[Who needs to be informed, how]

## Follow-up Tasks
- [ ] [Task]
```

7. **Link the decision note**:
   - Add a link in today's journal (`journals/YYYY/MM-Month/DD-MM-YYYY.md`) under `## Notes`.

8. **Draft a communication**:
   - A ready-to-post message announcing the decision.
   - Keep it concise (under 200 words).
   - Format: Context → Decision → Impact → Next steps.
   - Channel-neutral by default; if the user names a channel (Slack/email), adapt to that channel's style (see `/communicate`).

9. **Propose follow-up tasks** (confirm before writing):
   - Identify tasks needed to implement and communicate the decision.
   - Show the proposed list and wait for confirmation.
   - After confirmation, append each task to `Dashboard/tasks.md` under "This week" with format:

```
- [ ] Task - source: [[YYYY-MM-DD - Decision - Topic]] - due: YYYY-MM-DD - priority: P2
```

## Output Format

Report results in conversational prose, not a fenced template card. Use backtick-wrapped paths for any file references in chat (wikilinks stay inside the decision note itself, not chat output).

Cover these beats in 3-4 sentences of prose:
- Where the decision note was written (backtick path to the new file in `Loose Notes/Work/`).
- Whether it was linked in today's journal (or "skipped - no journal for today").
- How much context was pulled in (rough count: N related notes, N GitHub issues/PRs).
- Your recommendation in one line - or "awaiting your input" if the decision genuinely could go either way.

Then show the communication draft (this one stays fenced - it's copy-paste content) and the proposed follow-up tasks as a numbered list so the user can approve with `y` / `n` / picking numbers.

Example tone:

> Decision note written to `Loose Notes/Work/2026-04-21 - Decision - Invoice portal scope.md`, linked in today's journal. Pulled context from 3 related meeting notes and 2 GitHub issues. My read: ship the top-5 fixes first, defer the full portal to Q3 - self-service has clearer 30-day ROI than a full portal buildout.
>
> Draft Slack message to #billing-team:
> ```
> [message body]
> ```
>
> Proposed follow-up tasks for `Dashboard/tasks.md`:
> 1. Write spec for top-5 complaint fixes - P2, due 2026-04-28
> 2. Book Q3 roadmap review for the portal scope - P3
>
> Add these? (Y / N / pick numbers)

## Notes

- Always cite sources (meeting notes, GitHub issues).
- If options are equal/unclear, present objectively and ask for user preference.
- Leave the "Decision" section empty if not immediately clear.
- If the decision is urgent, propose tasks with P2 priority.
