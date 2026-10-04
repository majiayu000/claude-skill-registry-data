---
name: draft
description: Use when the user needs a written communication drafted in their voice — an email, a Slack/Teams message, a team update, an announcement, a reply to a thread, or a post. Produces a ready-to-review draft matching references/voice.md; never auto-sends external. Trigger on "/draft", "draft an email", "write a reply", "draft the update", "draft the announcement", "respond to this thread in my voice".
---

# Draft

Turn a brief (or a thread) into a ready-to-send-quality draft in the user's voice — fast, on-register, and honest.

## When to run
- The user needs to write something to a person or a group.
- After `/structure` or `/triage` flags an item that needs a reply.

## The output (always this shape)
```
**To / channel:** <who>  ·  **Type:** email | slack | update | post  ·  **Register:** internal | external
**Subject / opening line:** <if email>

<the draft — in the user's voice (references/voice.md)>

—
Send call: [internal → I can send in your voice]  /  [external → draft only, you send]
Open questions: <anything I assumed or couldn't verify>
```

## Process
1. **Get the brief.** If the ask is fuzzy, frame it first (`/structure`): audience, outcome, and the one thing they should do or know.
2. **Match the voice.** Read `references/voice.md`; mirror the register (internal vs external split). Don't fake the voice on external content.
3. **Draft tight.** Lead with the point or ask. Cut filler. One clear CTA. Length to fit the channel.
4. **Verify every claim (Verification Gate).** Any fact, number, name, date, or commitment in the draft → trace it to source (`context/`, `wiki/`, `/graph-query`, the thread). Anything you can't confirm goes under "Open questions" — never assert it.
5. **Set the send call** per guardrails.

## Autonomy
**L2** — drafts; you MAY send **internal-to-team** in the user's voice. **External is always draft-only** — the human sends.

## Guardrails (from CLAUDE.md)
- **Draft, never auto-send external** (customer / partner / investor / public). Internal team comms may go in the user's voice.
- **Cite, don't invent** — no unverified facts or figures in a draft; flag the gap instead.
- No confidential figures, PHI/PII, or secrets in the draft or the repo.
