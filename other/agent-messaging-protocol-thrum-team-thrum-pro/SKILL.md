---
name: agent-messaging-protocol
description: "Use when forwarding or relaying information between parties, routing an owner answer, carrying a decision or request through an intermediary, summarizing another author's message, or adding interpretation to someone else's words."
---

# Agent Messaging Protocol for Forwarding and Relaying

- Communicate directly with the intended party whenever possible.
- Treat the original message as the authoritative source.
- Forward a pointer to the original message instead of retyping or paraphrasing its body.
- Include the original author, original message ID, intended recipient, and requested action.
- Attach `message:<original-message-id>` as a message reference when supported.
- Read the original message before acting: `thrum message get <message-id> --json`.
- Reply against the original message: `thrum reply <message-id> ...`.
- Do not route the response back through the intermediary.
- Add commentary or interpretation only when requested or necessary.
- Label added reasoning as `INTERPRETATION - @agent`.
- Never present an interpretation, summary, or recommendation as words or authority from the original author.
- Label a requested summary as `SUMMARY - @agent` and retain the original message ID.
- Preserve the original scope, urgency, constraints, and requested action.
- Do not introduce new requirements, decisions, risks, or authorization while routing.
- Ask the original author directly when clarification is required.
- Continue referencing the original message rather than an intermediary's summary.
- Identify corrections by the exact message they supersede.
- Distinguish delivery, acknowledgement, execution, and verification.
- Do not reply to a message that only acknowledges or thanks; mark it read.
- Preserve the original thread audience when replying unless a deliberately narrower audience is required.

## Routing Envelope

```text
ROUTE POINTER
From: @original-author
Message: msg_...
Action: Read and reply to the original message.
```
