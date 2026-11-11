---
name: dm-closer
description: "Designs an Instagram DM funnel from the user's own past conversations: finds the questions people ask before they buy, writes a reply bank in their voice, writes two or three qualifying questions, sets the rule for who gets the booking link, and writes a click-by-click ManyChat build for the user to set up. Use when someone wants a DM funnel, DM reply templates, lead qualifying in DMs, a booking-link rule, or a ManyChat flow. Claude designs it; ManyChat sends. This skill never sends a DM."
---

# DM Closer

Five agents that turn your best past DMs into a reply bank, qualifying questions, a booking-link rule and a ManyChat build. Claude writes it, you click it into ManyChat, ManyChat sends it.

Not for sending DMs, mass messaging, or messaging anyone who has not written first.

## What you need

| Input | How Claude gets it |
|---|---|
| 10 to 30 past DM conversations (ideally some that ended in a sale or booking) | Pasted text, screenshots, or files from Instagram's "Download your information" (messages) export. Claude cannot read your Instagram inbox directly. |
| Booking link, what the call is for, length | Typed in setup, or `<your booking link>` for now |
| ManyChat account connected to an Instagram professional account | You build in ManyChat yourself; Claude never logs in |

Under 10 conversations: the agents still run, and the DM Reader says the counts are rough.

## Setup (`start`, or when PROFILE is empty)

Two rounds, accept "skip", then show PROFILE back and ask for the conversations.

Round 1, the offer
1. What do you sell in DMs and what does it cost? (only what replies may say)
2. Booking link, what the call is for, how long?
3. Who is a great fit? Who is not, and what should they get instead (free resource, cheaper product, waitlist, kind no)?
4. The keyword people comment or DM (e.g. GUIDE)?

Round 2, voice and limits
5. Paste 5 to 10 DMs you wrote. Words you never use?
6. What must always come to you personally?
7. Do you already use ManyChat?

## Commands and routing

| Command | Runs |
|---|---|
| `read DMs` | 1 |
| `replies` / `qualify` / `link rule` / `build` | 2 / 3 / 4 / 5 |
| `full build` | 1 to 5, one combined summary |
| `test` | Walk three sample leads (serious, curious, wrong fit) through the finished flow on paper; show where each ends |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-dm-reader.md`: anonymise, group, count, mark buying signals
- `agents/02-reply-writer.md`: one phone-length reply per top question
- `agents/03-question-writer.md`: 2 or 3 button questions, FIT / MAYBE / NOT A FIT
- `agents/04-link-gate.md`: link only on the FIT path, messages for every other path
- `agents/05-flow-builder.md`: numbered ManyChat build + test plan

## Safety rules (every agent)

- Never send a DM or comment, never log in to Instagram or ManyChat. Everything is a draft with an ID (R1, Q1, L1, F1). The user builds and switches it on.
- Only people who DM first or comment the keyword enter the flow. No cold broadcasts.
- Never promise prices, results, discounts or guarantees the user has not written down. Unknowns go in [brackets].
- Strip names, handles, phone numbers and emails from pasted DMs. Quote patterns, not people. Keep no personal details in shared files.
- Complaints, refunds, legal, medical, money trouble, anyone upset, anyone asking for a human: always routed to the user, never auto-answered.
- Meta limits automated replies (e.g. a 24-hour window after the person's last message). Tell the user to confirm current rules in ManyChat's help docs; do not promise follow-ups outside them.

## Shared files

Claude Code: files in `dms/`. Claude.ai: print updated tables at the end so the user can save them to Project knowledge.

- `PROFILE`: setup answers
- `QUESTION BANK`: ranked questions from agent 1
- `REPLY BANK`: approved replies
- `QUALIFIERS`: questions, buttons, scoring rule, field names
- `LINK RULE`: rule and path messages
- `FLOW`: the ManyChat build, with a version number

## End of every run

1. One line per agent that ran.
2. Drafts awaiting approval: ID | what | one line.
3. NEEDS YOU items.
4. Missing data and how to fix it.
5. "Nothing has been sent. ManyChat sends only after you build and switch on the flow."

Example (fake data):

```
Ran: DM Reader (18 conversations), Replies (8), Qualify (3 questions), Link rule, Build (v1, 10 steps).
Drafts: R1-R8 replies, Q1-Q3, L1-L4 path messages, F1-F10 build steps.
NEEDS YOU: refund question seen in 2 DMs; routed to handoff, you answer those.
Missing: no price confirmed; R2 says "[price]".
Nothing has been sent. ManyChat sends only after you build and switch on the flow.
```
