---
name: triage
description: Use when the user dumps a batch of inputs at once — a pile of emails, a backlog of Slack/Teams messages, a list of asks, meeting action items, a notes brain-dump — and needs it sorted into action. Classifies each item, assigns owner + next step + priority, and flags which need a full /structure brief or a /decide call. Trigger on "/triage", "triage this", "process my inbox", "sort these asks", "clear my backlog", "what do I do with all this".
---

# Triage

Batch intake for the Chief of Staff: turn a chaotic pile into a sorted, owned, prioritized list —
the front-door `/structure` does for *one* fuzzy input, `/triage` does for *many*.

## When to run
- An inbox / backlog / message pile needs to become action.
- After a meeting, to process a batch of action items at once.
- Feeding `/daily` — fold the triaged items into today.

## The output (always this shape)
```
## Triage — <date> (<N> items)
| # | Item (1 line) | Type | Owner | Next step | Priority | Route |
|---|---------------|------|-------|-----------|----------|-------|
| 1 | … | ask/FYI/decision/task | <who> | <action> | P1/P2/P3 | /structure · /decide · /draft · done |

**Needs your decision** — the short list only the user can resolve (with the framed choice).
**Delegated** — items routed to the team (with owner + next step).
**Drop / FYI** — no action needed (so they're off the list).
```

## Process
1. **Split the batch into discrete items.** One row per real ask; merge duplicates.
2. **Classify each:** ask · FYI · decision · task. Be ruthless — most "FYIs" are drops.
3. **Assign owner + next step + priority.** Default owner to the right teammate (don't pool on the user). Priority by leverage/urgency.
4. **Route, don't solve inline:** mark complex items `/structure` (needs framing), `/decide` (needs a call), `/draft` (needs a reply). Simple ones get a one-line next step.
5. **Surface the decision shortlist.** Pull every `decision`-type item into "Needs your decision" with the choice framed for a fast yes/no.
6. **Offer next moves:** run `/structure` on the flagged items, `/draft` the replies (internal may send; external = draft), and/or feed the result into `/daily`.

## Autonomy
**L2 — sorts and routes; the human decides and sends.** Triage never auto-replies.

## Guardrails (from CLAUDE.md)
- **Eliminate first** (3Ms): if nobody would notice an item disappearing, drop it.
- No confidential data persisted to the repo; reference live sources.
- External replies are **drafts** in `references/voice.md` register; internal-to-team may send.
