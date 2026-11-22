---
name: demo-builder
description: >-
  Demo Builder. Builds a demo showing how your product solves the problem, before the product exists.
  Turns a small spec into one self-contained HTML page that runs anywhere with no server: sample
  records, one button, every row moving through its statuses and a total counting up, with a banner
  that always says it is a demo with sample data. Claude can then make it look and behave more like
  the real thing for this buyer. Use when the user says "build a demo", "mock this up", "show how it
  would work", "I need something to show them", "prototype", or "make a clickable demo".
argument-hint: "[check <spec> | build <spec>]"
---

# demo-builder

Nobody buys a description. A demo that takes 2 minutes to watch does what a 20-page deck can't: it lets
someone see their problem go away. It only has to show the one moment that matters, and it has to be
honest about what it is.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/demo.py" check --spec "${CLAUDE_SKILL_DIR}/demo.example.json"
python3 "${CLAUDE_SKILL_DIR}/demo.py" build --spec "${CLAUDE_SKILL_DIR}/demo.example.json" --out whale/demo/index.html
```

## The spec

```
title        your product's name
subtitle     the one job it does here ("Late invoices")
button       the one action ("Chase all")
total_label  what the number at the bottom means ("Collected")
sample_data  must be true: a demo never shows a real customer's records
statuses     what each row moves through, in order (["Reminder sent", "Paid"])
rows         3 to 12: name, amount ($1,234.00), note ("71 days late")
accent       optional color, like #D97757
```

## Steps

1. **Find the moment.** Ask: what is the one screen where the problem goes away? For late invoices, it is a list
   of overdue invoices, one button, and the money coming in. Everything else can wait.
2. **Write the spec.** Save it as `whale/demo.json`. Use sample names and round, believable numbers from the
   buyer's world. Never use a real customer's data, and never the buyer's own records without their written okay.
3. **Build it.** `demo.py check`, then `demo.py build`. It writes one HTML file with no network calls.
4. **Open it and press the button yourself.** Then show the user. Watch for anything that looks more finished than
   it is, and say so.
5. **Make it theirs, if it helps.** Claude can restyle the page for one buyer or add a second screen. Keep the banner.
   Keep it small: a demo that takes a week to build has stopped saving time.
6. **Host it.** Any static host works (GitHub Pages, Netlify, Cloudflare Pages), or attach the file. Publishing it is
   the user's call. `/whale-hunter` puts the link in the pitch.

## Showing it

- Say first: "This is a demo with sample data. Here's how it will work for you."
- Under 2 minutes. Show the problem, press the button, show the result, stop.
- Then ask, and listen: "How close is this to how you'd want it to work?" Every answer is a requirement.

## Example from the reel

"Build a demo that chases late invoices for a freight company." Your Product, Late invoices, five rows from Granite
State Tile ($15,300.00, 71 days late) to Tern Bay Seafood ($5,240.00, 33 days late). "Chase all" moves each row to
Reminder sent, then Paid, and the total counts up to $48,210.00. This is `demo.example.json` (illustrative: every
business and amount in it is fictional).

## What it never does

- Never removes the banner. A demo that passes for a shipped product is a false promise, and it comes back as a refund.
- Never puts a real customer's records in a demo.
- Never promises a feature in a demo that the user doesn't intend to build.

## Consent and truth

- Nothing is sent, published or charged without the user's explicit yes. This skill only writes a file.
- A demo shows how it will work, not what already exists. Say so every time you show it.
- Never invent a result, a client or a review. The numbers in a demo are sample data and are labelled that way.
