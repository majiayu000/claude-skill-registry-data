---
name: writing-cold-outreach
description: Write cold email subject lines, personalized opener lines, and LinkedIn connection requests from researched lead data. Use when the user asks to write outreach, draft cold emails, personalize a lead list, or create connection requests. Uses a fixed email template with one AI-written slot — never AI-generates a whole email.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Writing Cold Outreach

## Goal
Produce a ready-to-send cold email and LinkedIn connection request for each lead, where the only AI-written words are the one line that proves this wasn't a mass send.

## The rule that matters

**Never let the model write the whole email.** The template is fixed — the user wrote it, tested it, and it works. The model fills exactly one slot: the observation about *this* company.

```
Hi {first_name},

{opener}                         <-- the ONLY AI-written line

Most companies scaling this fast hit the same bottleneck: {pain_point}.

We helped {similar_company} solve this and saw {metric} in 60 days.

Worth a 15-min chat to see if we can do the same for {company}?

{sender_name}
```

Everything except `{opener}` comes from CLI arguments or the lead record. Same words every time. If the user asks you to "make the emails more varied" or "let the AI write the whole thing", explain why that's the wrong direction: variance in the body is what makes a sequence untestable and what makes replies stop.

To change the email itself, edit `templates/email_template.md`. Not the code.

## Prerequisites
Leads must have been through `research_lead.py` and have `fact1`..`fact5` populated. Leads without facts are skipped and flagged, not given a generic opener.

## Process

### Step 1 — dry run, always
```bash
python -X utf8 scripts/04_outreach/write_outreach.py \
    --input output/researched.json --dry-run \
    --sender-name "Armin" \
    --pain "leads going cold because nobody follows up past email one" \
    --similar-company "a 12-truck HVAC company in Mobile" \
    --metric "31 extra booked jobs in 60 days"
```
Prints one complete email. Read it out loud. If the copy is wrong, fix the four arguments — those words go into every single email.

### Step 2 — the full run
```bash
python -X utf8 scripts/04_outreach/write_outreach.py \
    --input output/researched.json --out-csv output/outreach.csv \
    --sender-name "Armin" --pain "..." --similar-company "..." --metric "..."
```

## What gets enforced in code

The prompt asks for these. The script *guarantees* them, with one retry that feeds the specific failure back:

- Subject starts with `Quick question about {Company}'s`, max 11 words
- Body starts with `I noticed {Company} recently`, max 15 words
- No "Congratulations", "Congrats", "amazing", "great work", "impressive"
- No years, no month names, no quoted event names
- LinkedIn request max 200 characters, and none of "building my network" / "expanding my network" / "also working in"

Anything still failing after the retry is held back with a reason in `outreach_status`, not shipped.

## Reading the output

Check `outreach_status` before sending anything:

| Value | Meaning |
|---|---|
| `ok` | Passed every check |
| `skipped: no research facts` | Nothing true to say — go research it or drop it |
| `email failed validation: ...` | Model couldn't hit the constraint twice; read the reason |

## Anti-patterns

- Sending the whole list without reading five of them first
- Writing an opener for a lead with no facts (that's what the flag is for)
- Putting the pain point or social proof into the AI prompt — they're your copy, they're arguments
- Editing the validators to make more leads pass. If leads are failing, the research is thin.

## Follow-up
`templates/email_5_touch_sequence.md` has the cadence. The course's own number: roughly half of people stop after one message, and most deals land somewhere between touch three and five.

## Cost
About $0.005 per lead.
