---
name: launch-week
description: "Writes a whole product or offer launch before it starts: an offer brief and buyer questions from pasted sales call notes and DMs, the sales page, the launch email sequence on a date grid, a Reel hook and script for each launch day, and a skeptic pass that rewrites hype or promises the offer cannot keep. Use when a creator or business owner is planning a launch, course or program opening, new offer or sales week, or says \"launch week\", \"write my sales page\" or \"launch emails\". Drafts only; never sends or publishes."
---

# Launch Week

Five agents that write your launch from one OFFER BRIEF: sales page, emails, daily Reel scripts, then a skeptic rewrite of anything that sounds like hype. You load, approve and publish in your own tools.

Not for regulated claims (financial, medical, legal) without the owner's own review of every claim.

## What you need

| Input | Connector | Fallback |
|---|---|---|
| Sales call notes | Note-taker connector or Google Drive docs | Pasted transcripts or summaries |
| DMs | None (Claude cannot read Instagram or TikTok DMs) | Pasted text or screenshots |
| Pre-sale emails | Gmail | Pasted threads |
| Offer details, past pages, testimonials | Google Drive | Attached files |
| Email tool | Your email platform's connector, if your plan and admin allow and it supports drafts | Ready-to-load plan (subject, preview, body per email) |

At least 5 real buyer conversations make the question list useful; with fewer, the Offer Studier says it is thin. If a connector is missing, ask for the paste or export and carry on.

## Setup (`start`, or when OFFER BRIEF is empty)

Three rounds, accept "skip", then show OFFER BRIEF and LAUNCH CALENDAR back.

Round 1, the offer
1. What are you selling and what exactly does the buyer get?
2. Who is it for, and who is it not for?
3. What changes for the buyer, and how do you know? (real results only)

Round 2, the launch
4. Price, payment options, guarantee, refund terms, exactly as you will state them.
5. Warm-up start, doors open, doors close, time zone. Any real limit (seats, bonus deadline)?
6. Where do people buy, which email tool, which channels?

Round 3, proof and voice
7. Testimonials or results you have permission to use.
8. Sales call notes and DMs where people asked questions before buying.
9. Two emails or captions that sound like you; words you never use.
10. Claims you must avoid (income, health, guaranteed results)?

## Commands and routing

| Command | Runs |
|---|---|
| `launch week` | 1, then 2, 3, 4, then 5 on every draft; show final drafts and skeptic changes |
| `offer brief` | 1 |
| `sales page` | 2 |
| `emails` | 3 |
| `content` | 4 |
| `skeptic <ID>` | 5 on one draft |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-offer-studier.md`: OFFER BRIEF, buyer questions grouped and counted
- `agents/02-sales-page-writer.md`: page sections + claims table
- `agents/03-email-writer.md`: date grid + every email
- `agents/04-content-writer.md`: one Reel per launch day
- `agents/05-skeptic.md`: seven flag types, before/after rewrites

## Safety rules (every agent)

- Never send, schedule live, post or publish. Drafts carry IDs: P1 page, E1-E9 emails, R1-R7 Reels. An email-tool connector may only create unsent drafts, and only if the owner allows.
- Every claim traces to the OFFER BRIEF. Missing facts go in [brackets] and into OPEN QUESTIONS, never a plausible guess.
- Never invent a testimonial, result, student count, quote, bonus or deadline. No fake scarcity.
- Buyer names and words from calls and DMs stay out of public copy unless the owner confirms permission. Quote phrases, not people.
- No hype words. Short sentences, readable on a phone.

## Shared files

Claude Code: files in `launch/`. Claude.ai: print updated tables at the end so the owner can save them to Project knowledge.

- `OFFER BRIEF`: offer, buyer, promise, inclusions, price as stated, proof, terms, dates
- `BUYER QUESTIONS`: theme | example | count | sources | honest answer
- `LAUNCH CALENDAR`: date grid for emails and Reels
- `DRAFTS`: ID | type | status (draft, skeptic checked, approved)
- `OPEN QUESTIONS`: facts the owner still owes

## End of every run

1. One line per agent that ran.
2. DRAFTS with IDs and status.
3. Skeptic changes: count by flag type, lines only the owner can decide.
4. OPEN QUESTIONS to answer before launch.
5. "Nothing has been sent, scheduled or published."

Example (fake data):

```
Ran: Offer Studier (7 calls, 22 DMs), Sales Page, Emails (9), Content (7), Skeptic.
Drafts: P1 page, E1-E9 emails, R1-R7 Reels, all "skeptic checked".
Skeptic: 14 lines rewritten (6 hype, 4 vague, 2 unsupported, 1 fake urgency, 1 mismatch).
Owner decides: E6 says "only 30 seats"; is that a real cap?
Open questions: refund window (14 or 30 days?), permission for testimonial T2.
Nothing has been sent, scheduled or published.
```
