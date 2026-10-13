---
name: difficult-message-drafter
description: Use when you need to say something hard to someone. Asks one clarifying question, then drafts the message in three versions — direct, diplomatic, and firm — for your choice.
version: 1.0.0
author: Pete Swain / Hermes Agent
output_mode: push
destination: email draft / Slack message
---

⚠️ OUTPUT NOTE: The goal of this skill is NOT to display results in chat.
The outcome is pushing output to a meaningful destination — Slack, Google Doc,
email draft, Notion, or web. If you're reading this in chat, the skill hasn't
finished its job.

## Overview

Difficult messages — the ones where something true needs to be said, a boundary needs to be set, or a hard conversation needs to happen — are almost always delayed because they're hard to start. This skill takes the situation out of your head and puts it on the page in three distinct versions: direct (no softening), diplomatic (clear but kind), and firm (sets a boundary or escalates). You choose the version that fits, blend as needed, and send. The message is pushed to an email draft or Slack, depending on where the conversation lives.

## When to Use

- You say "draft a difficult message"
- You say "I need to say something hard to [person]"
- You say "help me write this"
- A conversation has been avoided and it's time to have it
- Someone has crossed a boundary and you need to name it
- A working relationship is deteriorating and needs a direct reset
- You need to deliver feedback, bad news, or a "no" clearly and professionally
- You're ending a relationship — client, supplier, or team member — and need the right words

## How It Works

1. **Get the situation.** Ask the user: *"Tell me what needs to be said, who it needs to be said to, and what's happened. Give me as much context as you're comfortable sharing."*

   Accept whatever level of detail they offer. The agent does not need the full history — just enough to understand: who, what, and what outcome is needed from this message.

2. **Ask one clarifying question if needed.** If a critical piece of information is missing, ask exactly one question — not a list. Typically the most important clarification is: *"What outcome do you want from this message — do you want to repair the relationship, set a clear expectation going forward, deliver information without expecting a response, or escalate?"*

   If the situation is clear enough, skip the clarifying question entirely and proceed to drafting.

3. **Write three versions of the message.**

   ---

   **Version 1 — Direct**
   No softening. No "I hope this finds you well." No excessive qualifiers. Just the truth, stated plainly and professionally. This version respects the recipient enough to say exactly what needs to be said without hedging. It may feel blunt — that's intentional. Use it when clarity matters more than comfort.

   Structure: State the issue → state the impact → state what needs to change or happen → close with clarity on next steps.

   **Version 2 — Diplomatic**
   Clear, but kind. This version says the same thing as Version 1 but builds in empathy, acknowledgement of the other person's perspective, and an opening for dialogue. It does not sacrifice honesty for comfort — it uses tone and structure to deliver the message in a way that's easier to receive. Use this when you want to preserve the relationship while still being clear.

   Structure: Acknowledge context or relationship → name the issue carefully → express the impact → invite response or collaboration → close warmly but with clarity.

   **Version 3 — Firm**
   For situations where a boundary has been crossed, a previous conversation hasn't landed, or an escalation is needed. This version is professional but unmistakably serious. It does not ask — it states. It may include consequences or a defined deadline. Use when the diplomatic version hasn't worked, or when the situation requires unambiguous seriousness.

   Structure: Reference the history briefly if relevant → state the position clearly → name the consequence or required action → close without ambiguity.

   ---

4. **Add a usage note for each version.** One sentence below each version explaining when it's the right choice and what impression it will leave on the recipient.

5. **Ask for destination.** After presenting the three versions: *"Which version would you like to send, or would you like to blend elements? And should I push this to an email draft, a Slack message, or save it to a Google Doc?"*

6. **Push to the chosen destination.** Send to email draft (with subject line) or Slack message as specified. Confirm when delivered.

## What the Agent Needs From You

- **The situation** — who, what happened, and what needs to be said
- **The relationship context** — client, colleague, supplier, team member, partner?
- **The desired outcome** — repair, reset, inform, escalate, or end?
- **The channel** — is this an email or a Slack message?

## Output

In chat first:
- Three complete message drafts: Direct, Diplomatic, Firm
- A usage note for each version

On approval:
- Selected version pushed to email draft (with subject line) or Slack message
- Confirmation of delivery in chat
