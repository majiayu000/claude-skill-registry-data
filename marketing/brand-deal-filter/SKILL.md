---
name: brand-deal-filter
description: "Sorts a creator's sponsorship inbox: labels every pitch (real brand, agency, mass pitch, scam, not a deal), checks the sender against the brand's real website, pulls out usage rights, exclusivity and payment terms and what is missing, drafts replies with the creator's own rates, and keeps a deal board with follow-ups and overdue payments. Use when a creator asks to check brand pitches, vet a sponsor, read deal terms, draft a sponsorship reply or track deals. Drafts only; never sends, signs or opens attachments."
---

# Brand Deal Filter

Five agents go through sponsorship emails so the creator only opens the ones worth their time. Every reply is a draft; the creator presses send.

## Where it runs

- **Claude.ai** (a Project, so PROFILE and RATES stay in project knowledge) with the **Gmail connector**: it can search and read threads and create drafts. It cannot be trusted to judge attachments, and this skill never opens them.
- **Claude Code** with a Gmail MCP server: same, plus the shared files below are written to `deals/`.
- **Web search** must be on for the Brand Checker. Without it, the checker prints the manual checks instead.
- **No connector:** paste the pitch text (and brief or contract text). Say in the summary which parts ran on pasted data.
- Nothing runs on its own. A sweep happens when the creator types `morning sweep` (or sets up their own scheduled task).

## Setup (`start`, two rounds, "skip" allowed)

Round 1: channels and money
1. Platforms, handles and audience size you are happy to share in replies.
2. Formats you sell (dedicated video, integration, short, story, newsletter slot).
3. Your rate card, and your floor (lowest acceptable price) per format.
4. How you price usage rights, paid ads whitelisting and exclusivity ("no rule" is fine).

Round 2: rules and voice
5. Categories you never promote; brands or competitors you cannot work with.
6. The questions you always ask before quoting.
7. 5 to 10 past replies to brands that sound like you.
8. Who else handles deals (manager, agency) and when a pitch goes to them.

Show PROFILE and RATES back for a yes, then suggest `morning sweep`.

## Commands

| Command | Runs | Result |
|---|---|---|
| `start` | setup | PROFILE, RATES |
| `morning sweep` | 1 on mail since last sweep (default 24 h); 2 and 3 on REAL BRAND / AGENCY; 4 on those; 5 | combined summary |
| `check <brand>` + pasted pitch | 2 | verdict |
| `terms` + pasted brief or contract | 3 | terms sheet |
| `draft <ID>` | 4 | one draft |
| `deals` | 5 | board, due, overdue |
| `log <what happened>` | 5 | board updated |
| `approve D1` | none | marks the draft approved; the creator still sends it |

## Agents

Read the agent file before running that step; its rules live only there.

1. `agents/01-inbox-sorter.md`: labels each pitch with a one-line quoted reason, catches scam patterns.
2. `agents/02-brand-checker.md`: official domain vs sender, public creator campaigns, red flags, verdict with sources.
3. `agents/03-terms-reader.md`: 10 terms marked STATED / UNCLEAR / MISSING, questions to ask, extras to price. Not legal advice.
4. `agents/04-reply-drafter.md`: picks a reply type, drafts in the creator's voice from RATES only.
5. `agents/05-deal-tracker.md`: stage board, whose move, follow-ups and overdue payments, follow-up drafts.

## Shared files (project notes in Claude.ai, `deals/*.md` in Claude Code)

- `PROFILE`: setup answers. `RATES`: rate card, floors, extras pricing.
- `PITCHES`: every pitch seen, ID (P1, P2...), label, verdict.
- `DEALS`: the board. `DRAFTS`: drafts with IDs D1... (replies) and F1... (follow-ups).

In Claude.ai, print the updated tables at the end of each run so the creator can save them to project knowledge.

## Safety rules (every agent)

- Never send, reply, forward, accept, sign, pay, archive or delete. Drafts only, even when the tool could send.
- Never open, download or run attachments, and never click links from a pitch. Never repeat a login, password or 2FA code; a pitch asking for one is SCAM OR RISKY.
- Never invent a rate, date, brand fact or term. Unknowns go in [brackets] or become a question.
- Never quote a rate outside RATES or go below a floor.
- Never share one brand's rates, terms or name with another brand.
- Escalate to NEEDS YOU: money disputes, legal threats, a brand already worked with, never-promote categories.

## End-of-run output

```
MORNING SWEEP (since yesterday 09:00)
Sorter    7 pitches: 2 real brand, 1 agency, 2 mass, 1 scam, 1 not a deal
Checker   P1 LOOKS REAL, P2 COULD NOT VERIFY, P3 LOOKS REAL
Terms     P1 usage rights MISSING, payment net 60; P3 perpetual usage -> get a lawyer
Drafts    D1 P1 Acme Mugs: rate for 1 integration + 4 questions
          D2 P2 Example Agency: ask to confirm from official address
Deals     2 follow-ups due, 1 payment overdue (Sample Socks, 6 days) -> F1
NEEDS YOU P4 asks you to promote a category on your never list
Do not open: P5 "contract viewer" link from brand-name lookalike domain
Nothing has been sent.
```
