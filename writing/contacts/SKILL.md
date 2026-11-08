---
name: contacts
description: "Show the user's networking board in chat (everyone in their contacts by status, with last contact, unanswered messages, and follow-ups due) and update it when they say what happened: sent a message, they replied, we talked, they referred me, set a follow-up. Use when the user says contacts, my network, who do I follow up with, or reports news about a person."
---

# Contacts (chat version)

The chat version of the Claude Contacts panel (`/contacts`). `contacts/contacts.csv` is the only source of truth: read it fresh every time, and change only the rows of the people the user is talking about. The file has no lock, so one writer at a time (the playbook's "One writer at a time" says why and what to tell the user). Columns, statuses and the rules below come from `knowledge/job-search-playbook.md` ("Tracker"); if they ever disagree, the playbook wins.

## Show the board

Read `contacts/contacts.csv` (it may come from Excel: tolerate a byte-order mark, Windows line endings, quoted commas, and dates like `10/14/2026`; write dates back as `YYYY-MM-DD`). Read dates as AGENTS.md says ("Reading dates someone else wrote": dotted dates are day first; a slash date follows the row's other unambiguous dates, then `date_order:` in preferences). A date that is still unclear shows as "date unclear", never counts as due, and is never rewritten until the user says what it means. If the file is damaged (a semicolon-separated header, or a quoted value that never closes), don't edit it: say so and offer to repair it into a copy for them to check. A blank `status` counts as `to-contact`. If it has only the header, say "No one here yet" and offer `network` (find people at a company) or `import-linkedin`.

Group people by status in this order: To contact, Contacted (waiting), Replied, Talked, Referred me. Cold people: just a count, listed only if the user asks. One line per person:

`Jane Doe, Globex, Project Manager (alum), last contact Oct 1 (5 days ago), 1 unanswered, follow up Oct 8`

- Put anyone whose `next_followup` is today or earlier first, marked "follow-up due" (no emoji), except people whose follow-up the job owns (next point). For people at `replied`, `talked` or `referred` a `next_followup` is only there because the user asked for a reminder: show it as "reminder due" rather than a nudge.
- If the person's `job` is a job folder whose row in `jobs/tracker.csv` is `applied` or later, say "follow-up handled by your application" instead of a date: the job row owns it. Don't count it as due, and offer to clear the old date.
- If `touches` is 2 and they never replied (status `contacted` or `to-contact`), say "2 messages, no reply: stop here" and suggest marking them cold.

Under the board, one line of counts (e.g. "14 people · 2 follow-ups due · 3 cold").

## Update it

Change only that person's row. Get the date right ("I messaged her yesterday" means yesterday's date).

| The user says | Change |
|---|---|
| "I sent X a message" (a date, default today) | `last_contact` = the date sent (keep the newer one if it's already later). Only if `status` is `to-contact`, `contacted` or blank (they haven't answered yet): `touches` + 1, `status` → `contacted`, and `next_followup` for pure networking (no linked job, or the linked job is not yet `applied`): 5 business days after the send date, or blank if `touches` is now 2 (stop here). A thank-you, update or referral ask to someone at `replied`, `talked` or `referred` changes `last_contact` only: no touches, no follow-up date. Never move anyone back (cold stays cold). If the linked job is `applied` or later, clear any `next_followup` on this person for that job (the job row owns it). Only if this message was an actual follow-up on the application, add 1 to the job's `followups` and set its `next_action_date` per the follow-up cadence; thank-you notes, scheduling replies and other messages don't count and don't replace an interview or offer next step. If an Outbox draft to this person matches, set it to sent and move it to `outbox/sent/`. |
| "X replied" | `status` → `replied` if it was `to-contact`, `contacted` or `cold` (never lower `talked` or `referred`); `touches` → 0; clear `next_followup`. Offer to draft a reply into the Outbox (`network`). |
| "We talked" / "I had coffee with X" | `status` → `talked` (unless already `referred`); `last_contact` = the date they talked (keep a later one); `touches` → 0; clear `next_followup`. Then follow the `network` skill's "After a conversation": offer a thank-you note within 24 hours that mentions one specific thing they said, log what the user learned in `notes`, and ask "who else should I talk to?". |
| "X referred me" | `status` → `referred`; `touches` → 0; clear `next_followup`. Put the person in the linked job row's `contact` column in `jobs/tracker.csv` and note the referral in that row's `notes` (if no job is linked, ask which job, then set the contact's `job` too). Offer a thank-you note, and remind the user to send an update when they hear back. |
| "Draft something for X" | Run `network` (first message, reply, thank-you) or `follow-up` (a nudge) for that person; drafts go to the Outbox. Don't draft another nudge after 2 unanswered messages. |
| "Follow up with X on <date>" / "in a week" | Set `next_followup`, unless the linked job is `applied` or later: then change that job's `next_action_date` (the `pipeline` skill) instead, except when the job's next step is a booked interview, a take-home or an offer deadline: never overwrite that (playbook, "Two commitments at once"); tell the user, and ask whether the follow-up can wait until after it or should go on the contact's `next_followup` as a separate reminder. |
| "Mark X cold" / "give up on X" | `status` → `cold`; clear `next_followup`. |

## Rules

- Record what actually happened. A draft is not a sent message; only count a message once the user says it went out (or the Outbox panel or `sync-inbox` reports it).
- Re-read `contacts/contacts.csv` right before each change and edit only that row with a targeted edit; never rewrite the file from an older copy (the other app may have changed it). If Excel has it open, ask the user to save and close it first.
- Follow the CSV rules in the playbook ("Tracker"; quoting, plain punctuation, and no cell starting with `=`, `+`, `-`, `@` or a tab).
- After saving: re-read the row to confirm it saved, add one line to `history/activity.md` (date and time from the computer, which app, what changed; no private details), and tell the user in one sentence what changed and when the next follow-up is.

## The Claude panel (Claude Code only; Codex: skip)

In Claude Code the board is the `/contacts` panel (by status; cold collapsed). The user records Message sent (with date), They replied, We talked, Referred me, Mark cold, or sets a follow-up date; it applies the playbook contact rules (touches, never-backwards status, job row owns the follow-up once applied), adds a line to `history/activity.md`, and leaves a `[Contacts]` note. Don't re-apply a change the note already made. "We talked" and "Referred me" also pre-fill a request for a thank-you and job update: offer to draft them.
