---
name: happy-customer
description: "Works through a small business's customer support inbox with five agents: labels every email (question, order status, bug, complaint, refund, legal or risk, feedback, spam), builds one answer sheet from past replies and help docs, drafts routine replies in the owner's tone as Gmail drafts, puts refunds, angry customers and legal or data issues in a hard pile without drafting promises, and reports the top five things customers asked about each week. Use when an owner wants the support inbox cleared, replies drafted, a support FAQ built from old replies, or says \"support sweep\", \"hard pile\" or \"weekly support report\". Drafts only; never sends, refunds or promises."
---

# Happy Customer

Every support email labelled, routine ones answered in draft, hard ones set aside for you, and a weekly top five of what customers keep asking.

## Where it runs and what it connects to

| Piece | What it really does | Fallback |
|---|---|---|
| Gmail connector on the support inbox | Search and read threads, read the sent folder, create draft replies; apply labels only if the connector in your workspace exposes label tools (check its tool list on first run) | Paste emails or attach an export (CSV or .txt with date, from, subject, body) |
| Help docs and policies | Read from Google Drive, Project files or pasted text | Paste the policy text word for word |
| Order or account data | Read only, from an export or pasted details | Facts stay in [brackets] for the owner |
| Claude Code | Same agents; files in `support/`; `support sweep` can run as a scheduled task you set up | None needed |

Works in Claude.ai and Claude Code. Not for live chat that needs answers in seconds, or regulated advice (medical, legal, financial). A sweep runs when you run it.

## Setup questions (`start`)

Ask in three rounds, accept "skip", show the PROFILE back for a yes.

1. What you sell and what customers usually email about.
2. Which inbox is support, is it connected, where do help docs live.
3. Can Claude see order data, or will you paste it?
4. Refund, return, delivery and cancellation policies, word for word, and the date they took effect.
5. What must always come to you (refunds over an amount, named accounts, press, anything legal)?
6. What a reply must never say or promise.
7. Point to the sent folder or paste 10 to 20 replies you were happy with.
8. Greeting, sign-off, signing name.
9. Target reply time and what counts as urgent.

## Commands

| Command | Runs |
|---|---|
| `start` | setup, writes PROFILE |
| `build answer sheet` | agent 2 (once, then whenever a policy changes) |
| `support sweep` | agent 1, then 4, then 3 on everything not in the hard pile |
| `hard pile` | agent 4 |
| `weekly support report [week]` | agent 5 |
| `approve R3` | marks a draft approved in DRAFTS; the owner still presses send |

## Agents

Read the agent file before running that step; it is the only home for that role's detailed rules.

1. `agents/01-support-sorter.md`: one label, urgency and anger flag per email.
2. `agents/02-answer-sheet-builder.md`: approved answers from past replies and policies, conflicts sent to the owner.
3. `agents/03-reply-writer.md`: drafts for routine tickets from the answer sheet only.
4. `agents/04-hard-case-flagger.md`: refunds, angry, legal, security or data cases summarised, no promises.
5. `agents/05-weekly-report.md`: counted top five topics with one fix each.

## Shared files

Claude Code: files in `support/`. Claude.ai: print updated tables at the end of each run for the owner to save in the Project.

- `PROFILE`: setup answers.
- `ANSWER SHEET`: question, approved answer, source, last checked.
- `TICKETS`: ID, date, customer, label, urgency, status, draft ID.
- `HARD PILE`: cases waiting for the owner.
- `DRAFTS`: R1, R2... with status (draft / approved).

## Safety rules

- Never send. Replies are Gmail drafts (or pasted text); the owner presses send, even if the connector could send.
- Never issue, promise or hint at a refund, discount, credit, replacement, delivery date or fix date that is not in the approved answer sheet or written policy.
- Refunds, chargebacks, anger, legal words, security or data requests, safety issues go to the HARD PILE with no draft unless the owner asks.
- Never invent order details, policy or product facts; unknowns go in [brackets].
- Never mix one customer's data into another's reply. Never ask for a full card number or password. Never open customer attachments or links.

## End-of-run output

```
HAPPY CUSTOMER: support sweep, inbox support@example.com, last 24 h
1 Sorter     23 emails: 9 QUESTION, 6 ORDER STATUS, 3 BUG, 2 REFUND, 1 LEGAL OR RISK, 2 SPAM
4 Hard pile  4 cases (1 data deletion request, 2 refunds, 1 angry repeat chase)
3 Drafts     R1-R16 saved as Gmail drafts, 5 with [brackets] to fill
Gaps         "Do you ship to Iceland?" asked 2x, no answer-sheet entry
Nothing has been sent and nothing was promised.
```
