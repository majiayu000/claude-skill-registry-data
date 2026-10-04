---
name: bring-your-data
description: The on-ramp for any Built GTM analyst skill when your tools are not connected yet. Tells you exactly what to paste or upload to run a given analysis today, in plain language, then hands the data to the right skill. Trigger on "I haven't connected my tools", "how do I run this without connecting", "what do I paste", "run this on my data", "I have a CSV", "bring my own data", or any moment a connector-dependent skill needs data and nothing is connected.
---

# Bring Your Data

## What this does
Every Built GTM analyst skill runs on the data you give it. You do not have to connect a tool to start. This helper tells you exactly what to hand over for the analysis you want, accepts it in whatever shape you have, and passes it to the right skill. Connect your tools later and the same skills pull the data automatically.

## How to use it
Tell it which analysis you want, or just describe your question. It returns the shortest possible input list for that skill, the formats it accepts, and a paste-ready template. Then paste your data and it runs.

## Accepted formats
- Paste a table straight from a spreadsheet or a CRM report view.
- Upload a CSV or an export file.
- Paste plain text, a list of accounts or a set of numbers. The skill structures it.
- Point to a doc, for an ICP definition or a criteria list.

It never needs everything. It names what is required, what is optional, and what each optional field would add. A missing field is a prompt, never a guessed value.

## What to bring, by analysis
| If you want to run | Paste or upload |
|---|---|
| Deal health / deal-risk audit | Open deals: name, stage, amount, close date, last activity date, contacts per deal |
| Pipeline coverage | Open pipeline by channel and owner, plus the period target |
| Rep coaching | Per-rep open deals and activity counts, and your qualification fields |
| Win / loss / churn patterns | Closed-won, closed-lost, and churned accounts with size, industry, loss reason, competitor |
| Funnel / strike-zone diagnosis | Funnel counts by stage and channel, with a cohort entry date per channel |
| Renewal health | Upcoming renewals: account, date, value, terms, champion, usage notes |
| Book of business | Accounts with owner, ARR or contract value, renewal date |
| Conversation / relationship pulse | Timeline of meetings and email replies, contacts, last-response dates |
| Contact / list enrichment | Names and companies, or domains |
| Sequence performance | Sequence stages with subjects, timing, recipients, and open/click/reply/bounce rates |
| ICP interview slate | Your customer list plus your ICP definition, criteria or a doc |

## The rule
The skill you run never fabricates. If you cannot provide a field, it says what that costs and runs the rest. It closes by naming the one connection that would let the analysis pull this automatically next time.

Voice: plain declaratives, no em dashes, no emojis, receipts over theory.
