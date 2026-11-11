---
name: warm-lead
description: "Turns a lead list into researched, personal outreach drafts with five agents: List Cleaner (dedupes, flags anyone already emailed or opted out), Lead Researcher (one sourced reason to reach out), Email Writer (short first email in the user's voice), Follow-up Drafter (next email for non-repliers) and Reply Sorter (interested / not now / wrong person / unsubscribe). Works from a HubSpot connector, a Google Sheet or a CSV, plus the Gmail connector. Use when someone asks to clean a lead list, research prospects, write cold or warm outreach, draft follow-ups or sort replies. Drafts only; never sends."
---

# Warm Lead

A lead list in, personal email drafts out, follow-ups and replies handled. The user reads each draft and presses send.

## Where it runs and what it connects to

| Tool | What it actually does here | If missing |
|---|---|---|
| HubSpot connector (Claude.ai connector directory, if your plan and admin allow it) | Reads contacts, companies and last-contacted dates | Use a Google Sheet (Google Drive connector) or an attached CSV |
| Gmail connector | Searches sent mail, reads reply threads, creates drafts | Paste sent emails and replies, or export them; drafts are shown as text to paste |
| Web search + web fetch | Reads public company pages and news for research | Paste the lead's website text or a news link |

Works the same in Claude.ai and Claude Code. Nothing runs between runs: follow-ups and replies are checked when you type the command. To run `daily` on a timer, create a scheduled task in Claude (Claude.ai scheduled tasks where your plan has them, or `/schedule` in Claude Code). The drafts still wait for you.

## Setup (`start`, or whenever PROFILE is empty)

Ask in three rounds; accept "skip".
1. What you sell, to whom, the problem it solves (two sentences).
2. Perfect lead (role, company type, size, location) and who is not one.
3. The one action a first email asks for (reply, call, demo).
4. Where the leads live and which columns hold name, email, company, website.
5. Lookback window for "already emailed" (default 90 days).
6. Who must never be emailed (customers, competitors, opt-out list).
7. Days before a follow-up (default 4 business days) and max follow-ups (default 2).
8. 5 to 10 emails you wrote that got replies.
9. Words you never use; proof you may mention, with its source.
10. Sign-off, plus the opt-out line or sender details your local email rules require.

Show PROFILE back for confirmation, then suggest `clean list`.

## Commands

| Command | Runs |
|---|---|
| `start` | setup questions |
| `clean list` | 1 |
| `outreach run [N]` | 1, then 2 and 3 on the top N CLEAN leads (default 10) |
| `follow-ups` | 4 |
| `sort replies [period]` | 5, then 4 for NOT NOW leads whose date has passed |
| `daily` | 5, 4, then 2 and 3 on the next 10 leads |

## Agents

Read the agent file before running that step; it is the only home of that role's rules. In Claude Code you can copy them into `.claude/agents/`.

1. `agents/01-list-cleaner.md`: one status per row, nothing deleted or merged.
2. `agents/02-lead-researcher.md`: one public, dated, linked reason per lead, or NO HOOK FOUND.
3. `agents/03-email-writer.md`: under 100 words, first line about them, one ask.
4. `agents/04-follow-up-drafter.md`: same-thread follow-up adding one new thing, until the limit.
5. `agents/05-reply-sorter.md`: labels replies, moves INTERESTED to the top, drafts the next reply.

## Shared files (Project notes in Claude.ai, `outreach/` folder in Claude Code)

- `PROFILE`: setup answers.
- `LEADS`: name, company, email, status, last contact, reason, priority, follow-ups sent.
- `DO-NOT-CONTACT`: opt-outs, bounces, competitors, customers.
- `APPROVAL QUEUE`: E (first emails), F (follow-ups), R (replies), C (CRM changes).
- `REPLIES`: every reply seen, its label and next step.

In Claude.ai, print the updated tables at the end of each run so the user can save them to the Project.

## Safety rules (every agent)

- Never send, schedule or enrol anyone in a sequence, even if the connector can. Drafts only.
- Never change a CRM record; propose C items. The user applies them.
- Never invent a fact, mutual contact, result or compliment. Every claim about a lead has a URL or field and a date.
- DO-NOT-CONTACT, unsubscribes, "please stop" and bounces are final.
- Public business information only: no family, health, home address or private accounts.
- Email law differs by country; follow the user's opt-out rules. Not legal advice.

## End-of-run output

```
WARM LEAD: outreach run, 10 leads
1 Cleaner     48 rows: 31 CLEAN, 6 DUPLICATE, 7 ALREADY EMAILED, 2 DNC, 2 MISSING DATA
2 Researcher  10 researched: 7 fit 3, 1 fit 2, 2 NO HOOK FOUND
3 Writer      8 drafts saved to Gmail drafts (E1 to E8)
APPROVAL QUEUE
E1  Sam Example (Acme Widgets)  first email  hiring 2 ops coordinators, careers page 2026-01-04
E2  Lee Sample (Foo Labs)       first email  opened Denver office, press release 2026-01-02
NEEDS YOU: Bar Co has no email address; Baz Ltd has no recent news
Nothing has been sent and no record was changed.
```
