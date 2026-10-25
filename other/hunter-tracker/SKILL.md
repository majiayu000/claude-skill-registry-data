---
name: hunter-tracker
description: >-
  Pipeline Tracker. Tracks every role, contact and next step in one pipeline:
  hunter/pipeline.json, the single file every hunter skill reads and writes.
  Adds and updates roles and contacts, moves roles through the stages (saved,
  applied, screen, interview, onsite, offer, rejected, withdrawn), shows a
  summary by stage, what is coming up this week, what has gone stale, and
  exports CSV for a spreadsheet. Owns the pipeline schema and validates it
  after every change. Use when the user says "show my pipeline", "where am I
  with each application", "add this job", "I applied", "I got an interview",
  "I got rejected", "what's next", "what's stale", "export my applications",
  or "track this".
argument-hint: "[summary | add | move | export]"
---

# hunter-tracker

The Pipeline Tracker is the memory of the whole search. Every other hunter skill
reads `hunter/pipeline.json` and writes its part back; this skill owns the file's
shape and checks it.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" init
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" add-role --company Google --title "Software Engineer" --url <posting URL>
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" move google-software-engineer applied --today 2026-10-23
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" update-role google-software-engineer --next-step "Recruiter screen" --next-date 2026-10-30
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" add-contact --name "Maya C." --company Google --role "Engineering Manager"
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" summary --today 2026-10-16
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" next --today 2026-10-16 --days 7
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" stale --today 2026-10-16 --days 14
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" show google-software-engineer
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" export --what roles --out hunter/pipeline-roles.csv
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" validate
```

Every command takes `--file` (default `hunter/pipeline.json`) and `--today
YYYY-MM-DD` where dates matter, so results are reproducible.

## The schema (this skill owns it)

```json
{ "roles":    [ {"id", "company", "title", "url", "stage", "applied", "next_step", "next_date", "notes"} ],
  "contacts": [ {"id", "name", "role", "company", "linkedin", "email", "email_confidence", "source", "notes"} ],
  "threads":  [ {"contact_id", "role_id", "channel",
                 "messages": [ {"date", "direction": "out|in", "text"} ],
                 "status", "next_followup"} ] }
```

- **stages**: saved, applied, screen, interview, onsite, offer, rejected, withdrawn.
- **thread status**: drafted, sent, replied, booked, declined, closed.
- **dates**: `YYYY-MM-DD`. A message date may carry a time (`2026-10-12T09:30`).
- **ids**: roles `company-title` (`google-software-engineer`), contacts `name-company`
  (`maya-c-google`); a clash gets `-2`. Ids from `/hunter-scout` are kept as they are.
- **email_confidence**: a number from 0 to 1 (a pattern guess from
  `/hunter-connector`), or high, medium, low, unknown, or `published`. `published`
  (or `verified`) is only valid when `source` is the URL of the public page where the
  address appears; everything else is a guess.
- **channel**: email, linkedin, phone, in-person or other.
- **optional fields kept by `/hunter-connector`** (part of the schema):
  thread `invite` (true while a LinkedIn invitation is pending; it gets no follow-up),
  thread `draft` (`{"kind", "subject", "text", "created", "hash"}`, a message waiting
  for the user's yes), thread `approval` (`{"reply", "date", "hash"}`, that yes word for
  word), thread `booked` (`{"when", "minutes", "where"}`), and contact `do_not_contact`
  (true after a stop request: never contacted again).
- **a pending draft** is never in `messages`: `messages` holds only what really went
  out or came in. (A hand-made file may instead flag a message `"draft": true` or use
  status `drafted` with the draft as its last outgoing message; both are read the same way.)
- **notes**: free text; the tool appends dated lines (`2026-10-16: applied ->
  screen`) so the history stays readable. "DO NOT CONTACT" in a contact's notes
  closes every thread with them for good.
- Missing lists are read as empty. Top-level keys starting with `_` are comments.
  Any other extra field is kept and reported as a warning.

`validate` exits 1 on an error (unknown stage or status, bad date, a thread pointing
at a contact or role that does not exist, duplicate ids, an invalid email, a
"published" email with no source URL) and lists warnings (no applied date on an
applied role, a follow-up date on a closed thread, messages out of order).

## Who writes what

| skill | writes |
| --- | --- |
| `/hunter-scout` | new roles at stage saved, from `hunter/jobs.json` |
| `/hunter-resume`, `/hunter-cover` | a dated note on the role |
| `/hunter-apply` | a note that the application is filled and waiting for the user; `move ... applied` once the user submits |
| `/hunter-connector` | contacts and threads: drafted, sent, replied, booked |
| `/hunter-followup` | follow-ups it recorded after the user's yes, replies, stop requests |
| `/hunter-interview`, `/hunter-salary` | next steps and dates |

After any skill writes, run `validate`.

## Steps

1. First time: `init`, then add what the user already has in flight (roles they
   applied to, people they talk to). Ask for the applied dates; do not guess them.
2. Each time something happens, update it right away: `move` for a stage change,
   `update-role --next-step ... --next-date ...` for the next action.
3. When the user asks where things stand: `summary`. It shows counts by stage, the
   next 7 days (overdue first) and stale roles: active, nothing scheduled, no
   activity in 14 days.
4. For a spreadsheet: `export --what roles` (or contacts, threads) and the user
   opens the CSV in Google Sheets or Excel.

## Example: Jordan's pipeline on 2026-10-16

`pipeline.example.json` is the reel's story: five roles at the hardest companies,
Maya C. at Google, the email thread booked for coffee and the LinkedIn request.

```
Pipeline on 2026-10-16: 5 roles (5 active, 2 applied), 1 contact

By stage:
  saved      3
  applied    1
  screen     1

Conversations: 1 sent, 1 booked

Next 7 days:
  2026-10-19  Amazon, Software Development Engineer II: Online assessment
  2026-10-19  Meta, Software Engineer, Product: Tailor the resume (hunter-resume)
  2026-10-22  Google, Software Engineer: Coffee chat with Maya C. (Google Meet, 10:00)

Stale (no activity and nothing scheduled):
  netflix-senior-software-engineer (Netflix, saved): 22 days idle
  nvidia-deep-learning-software-engineer (NVIDIA, applied): 16 days idle
```

The Google role is still "saved": the application is filled but not sent, and the
coffee chat comes first. That is the point of the reel: an in at the company before
the application goes out.

## What it never does

- Never sends anything or contacts anyone: it is a record.
- Never guesses a date, a stage or a reply the user did not report.
- Never stores private information about a contact: public professional facts only.

## Consent and truth

- Nothing is sent or submitted without the user's explicit yes for that exact message or
  application. Claude drafts, the user approves, then it goes out from the user's own
  accounts: email as a Gmail draft first; LinkedIn messages through Claude in Chrome with
  the user present, one at a time, at human pace, the user clicking Send; application forms
  filled and left for the user to submit.
- No bulk or automated messaging, no scraping behind logins, no tricks around a site's
  limits. LinkedIn's terms forbid bots and automated messaging.
- Contact research uses public professional information only (the person's public profile,
  talks, posts, papers, the company site), never personal life, family, home address or
  private accounts. Email addresses are guesses from public patterns, marked with a
  confidence, never called verified unless found published.
- Stop rules: stop at the first "no" or any sign of disinterest, max 2 follow-ups, no message
  after 21 days of silence, and a request to stop is honoured forever.
- Never invent experience, titles, degrees, dates or numbers: rewrite and reorder what is
  true, and ask when something is missing.
- Salary benchmarks and interview material cite their sources. Nothing here guarantees an
  offer or an outcome.
