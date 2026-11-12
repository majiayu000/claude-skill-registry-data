---
name: inbox
description: Check the user's connected Gmail for replies to applications they sent (received, rejected, an assessment, an interview, an offer) and put them on the record. Use when the user says /inbox, "did anyone reply", "check my email for responses", or "any interviews".
argument-hint: "[days]"
model: claude-sonnet-5-5
effort: low
---

# /inbox

Run `npx jev inbox`, or `npx jev inbox --days <n>` when they gave a number.
It needs Gmail connected, read-only (`/accounts gmail`). If it says Gmail
is not connected, say that this is optional and what it does, and stop.

It reads only each email's sender, subject and the short preview Gmail
itself shows, never the body. What it is sure of goes on the application's
record: the "Reply" column in `/report` and in `applications/all.csv`. A
confirmation also settles an application that was clicked and never
confirmed.

Tell the user, in this order:

1. Interviews, assessments and offers, by company. These need them.
2. How many said no, and how many only confirmed receipt.
3. How many emails it was not sure about. Those wait under "Needs you" in
   the dashboard: `/report`.

Never read the user's mail any other way, never open or quote an email's
body, and never reply to anyone.
