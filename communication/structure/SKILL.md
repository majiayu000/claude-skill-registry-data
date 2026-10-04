---
name: structure
description: Use when the user brings any fuzzy, half-formed, or interrupt-driven input — an order from a boss, a forwarded email thread, a ticket, a chat message, a "can you look into X", a raw idea — and it needs framing before work starts. Turns the input into a structured brief (Context · Desired outcome · Goal · Owner · Next step · Decision needed). This is the AIOS's front door; run most things through it first. Trigger on "/structure", "frame this", "what's the actual ask here", "structure this", or any vague task that lacks a defined outcome.
---

# Structuring Engine

A common leverage point: inputs arrive **without structured context, defined outcomes, or clear goals.** This skill fixes that before any work begins. Frame first, then act (or delegate).

## When to run
- A new task lands fuzzy ("the boss wants the draft checked", "look into the X thing").
- A long email/chat thread needs to become an action.
- The user is about to do something the old way → apply the **Default Shift** ("to what extent could AI be leveraged here?").

## The output (always this shape)
```
## <short title>
**Context** — what's going on, in 2-4 plain sentences. The why behind the ask.
**Desired outcome** — the end state. What does "done" look like, concretely?
**Goal** — the measurable/observable target (a date, a number, a deliverable). One line.
**Owner** — who should own this (route to the team; don't pool on the user by default).
**Next step** — the single next physical action, and by when.
**Decision needed** — the specific call the user must make, framed as a fast choice.
```
When a decision is involved, present it as a **fast checklist** they can answer in seconds:
```
- Send to the client now (yes/no)?
- Loop in <reviewer> first (yes/no)?
- Target date: <propose one>
```

## Process
1. **Read everything given.** If it references a ticket, doc, or thread and a connection exists, pull it rather than guessing.
2. **Strip to the real ask.** Separate noise from the actual decision/outcome. Name what's missing.
3. **Fill the template.** Be concrete. If a field is genuinely unknown, write `❓ <the open question> → <who can answer>` instead of inventing.
4. **Route the owner.** Default to delegating to the right teammate; only put the user as owner when it's truly theirs (a decision, an external sign-off).
5. **Offer the next move.** After the brief, offer to: create the artifact (ticket / note / plan — allowed without approval), draft the reply in the user's voice (internal may send to team; never external without approval), and/or log a decision to `decisions/log.md`.

## Guardrails (from CLAUDE.md)
- No confidential figures or sensitive/regulated data persisted to the repo. Pull live, don't store.
- **Cite, don't invent** — any regulatory/financial/legal claim cites a source or is flagged as a gap.
- **Draft, never send external.** Internal to the team may be OK; external needs approval.
- Match `references/voice.md`.
