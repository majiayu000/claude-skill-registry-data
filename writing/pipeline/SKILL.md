---
name: pipeline
description: >-
  Pipeline Manager. Keeps every deal moving on one board, the CRM the other ten Closer skills
  share: contacts, deals, stages (lead, contacted, replied, call-booked, proposal, contract-sent,
  won, lost), every email and call, next steps and a do-not-contact list, all in one plain
  closer/pipeline.json in your project. Shows the board, one deal's history, moves deals between
  stages, and validates the file after every change. Use when the user says "pipeline", "board",
  "my deals", "CRM", "where are we with X", "move X to proposal", "we won X", "we lost X",
  "set up the closer skill", or wants to replace Salesforce or HubSpot.
argument-hint: "[board | show <deal> | move <deal> <stage>]"
---

# pipeline

The board every other Closer skill reads and writes. It replaces the CRM: one JSON file in the
user's project, no account, no seats, no monthly bill.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/deals.py" init --name "You" --company "Your Agency" \
    --email hello@youragency.studio --address "100 Congress Ave, Suite 400, Austin, TX 78701" \
    --offer "booking-ready websites and Google Ads" --price "\$2,500" \
    --plan_b "\$399 monthly plan instead, with no setup fee" \
    --value_line "Most practices win the cost back with 2 new patients a month."
python3 "${CLAUDE_SKILL_DIR}/deals.py" board --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/deals.py" show --deal harbor-lane-website
python3 "${CLAUDE_SKILL_DIR}/deals.py" move --deal lakeline-website --stage lost \
    --reason "timing: busy season, said ask again in the fall"
python3 "${CLAUDE_SKILL_DIR}/deals.py" validate
```

Every command takes `--file` (default `closer/pipeline.json`).

## First run

1. Ask the user for: their name, business name, the email they sell from, a postal address (the
   law needs one in cold email), their time zone, what they sell, the price, a smaller second
   option, and one true line about what it pays back. Do not guess any of these.
2. `deals.py init` with those answers.
3. If they are moving from Salesforce, HubSpot or a spreadsheet, ask them to export contacts and
   open deals as CSV, then add each with `deals.py contact` and `deals.py deal`. Map their stages
   onto the eight below and show the mapping before writing anything.

## The file

```
me          who you are and what you sell (offer, price, plan_b, value_line, proof, address)
contacts    id, name, title, company, email, phone, website, source, notes, do_not_contact
deals       id, contact_id, title, stage, value, currency, close_date, created, next_step, lost_reason
activities  id, date, contact_id, deal_id, channel, type, direction, subject, text, approval
suppression email addresses that must never be emailed again
```

Stages, in order: `lead, contacted, replied, call-booked, proposal, contract-sent, won, lost`.
Value is what the deal is worth in its first year (a $399/month plan is 4788).
Every outgoing email, LinkedIn message or SMS must carry `approval`: the user's yes, word for word.
`validate` fails without it, so nothing can be logged as sent that the user did not approve.
A lost deal needs a `lost_reason`: it is what `/win-back` reads later.

## Steps, every morning

1. `deals.py board`. Read it to the user stage by stage, biggest deals first, with each next step.
2. Point at anything marked `[quiet N days]` and say which skill moves it: `/follow-up` for no
   reply, `/scheduler` when they replied with a time, `/proposal-writer` after a call,
   `/contract-writer` when they picked an option.
3. When the user says something changed ("we lost Lakeline, bad timing"), `deals.py move` with the
   reason in their words.

## Example from the reel

On Thursday, October 29, 2026, after the call with Dana Ortiz of Harbor Lane Dental, the board says
`CONTRACT-SENT (1, $4,788)  Website + Google Ads, monthly  Harbor Lane Dental  next: Dana signs the
agreement`. `show --deal harbor-lane-website` lists the opening email on Oct 19, three follow-ups,
her reply on Oct 27, the booked call, the 24-minute call and the agreement at 2:31 PM. The whole
state is `pipeline.example.json` beside this file (illustrative: the agency, Dana and the
businesses are fictional).

## What it never does

- Never deletes a contact or an activity: history is the record. A person who asked to stop stays
  in the file as do-not-contact so no skill can email them again.
- Never marks something sent that was not, or won that was not signed.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. Claude drafts, the user says "yes", then it goes out from the user's own accounts.
  One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Never invent a number, a result, a client or a deadline. Fill in only what is true and ask when
  something is missing.
