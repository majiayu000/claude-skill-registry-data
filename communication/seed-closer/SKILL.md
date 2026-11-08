---
name: seed-closer
description: >-
  The Closer. Sends personalised outreach emails to investors, manages the
  conversations and keeps following up until an investor call is booked,
  and nothing leaves the user's inbox without their yes. Drafts one RFC 5322
  .eml per investor from seed/investors.json and a template (a real personal
  line, the sender's real name and an opt-out line, generic lines refused),
  shows the batch, records the user's yes word for word, enforces a daily cap
  of 20, then Claude sends through the user's own Gmail connector where the
  Allow once card is a second check. Schedules follow-ups on +3 and +7
  business days (3 touches at most, never after a reply), sorts replies into
  interested / question / not now / no / out of office, stops a thread for
  good on a no, an opt-out or a bounce, writes a valid .ics invite and shows
  the funnel. Reads seed/config.json and seed/investors.json, writes
  seed/pipeline.json, seed/outreach/ and seed/calls/. Use when the user says
  "email the investors", "send the outreach", "follow up with everyone who
  hasn't replied", "who do I follow up with today", "sort my replies", "book
  the call", "send her an invite", "how is the raise going", or after
  /seed-investors ranks the list.
argument-hint: "[draft | batch | due | inbox | book | status]"
---

# seed-closer

The Closer does the part of a raise that eats the founder's week: one
personal email per investor, the follow-ups nobody remembers to send, the
replies sorted, and the call on the calendar. It writes everything; it never
sends anything. Claude sends through the user's own Gmail, only after the
user said yes to that exact batch in the chat, and Claude's own "Allow once"
card asks again for every email. All the user has to do is say yes, show up
and pitch. Investors decide; nothing here promises a check.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/closer.py" draft --top 20          # one .eml per investor, status drafted
python3 "${CLAUDE_SKILL_DIR}/closer.py" batch                   # recipients, their personal lines, the first email in full
python3 "${CLAUDE_SKILL_DIR}/closer.py" approve --batch 3f9a1c2e --reply "yes"   # the user's reply, word for word
python3 "${CLAUDE_SKILL_DIR}/closer.py" outbox --json           # exactly what to send: to, subject, body, thread
python3 "${CLAUDE_SKILL_DIR}/closer.py" log --id maya-chen --event sent --thread-id 18c2f0a1
python3 "${CLAUDE_SKILL_DIR}/closer.py" due --today 2026-10-29  # who gets a follow-up today
python3 "${CLAUDE_SKILL_DIR}/closer.py" followup --due --extra "Here's our 60-second demo: https://..."
python3 "${CLAUDE_SKILL_DIR}/closer.py" inbox --file replies.json            # sort replies, then --write
python3 "${CLAUDE_SKILL_DIR}/closer.py" reply --id maya-chen --body-file answer.txt
python3 "${CLAUDE_SKILL_DIR}/closer.py" book --id maya-chen --start "2026-11-05 10:00" --tz America/New_York --link https://meet.google.com/abc-defg-hij
python3 "${CLAUDE_SKILL_DIR}/closer.py" status                  # the funnel
```

Every command takes `--dir` (default `./seed`) and `--today YYYY-MM-DD` (pin
the date). `--json` on batch, outbox, due, inbox and status.

## What it reads and writes

| file | what |
| --- | --- |
| `seed/config.json` | `startup` (name, one_liner, optional tagline, raise, stage), `founder` (your real name, the address you send from, company_address), `outreach` (daily_cap 20, followup_days [3, 7], max_touches 3, business_days true, optional holidays) |
| `seed/investors.json` | from /seed-investors: id, name, firm, email, sources, fit, reasons, personal_line |
| `template.txt` | the intro and the two follow-ups (this folder; copy it to `seed/template.txt` to make your own) |
| `seed/outreach/<id>-<n>.eml` | each draft: a valid RFC 5322 message (CRLF, From, To, Subject, Date, Message-ID, plain text); follow-ups carry In-Reply-To |
| `seed/pipeline.json` | one row per investor: status, touches, next_due, labels, notes, the waiting draft, the Gmail thread id, the call, the history |
| `seed/calls/<id>.ics` | the invite: RFC 5545, CRLF, folded at 75 octets, UTC times, UID, SEQUENCE, ORGANIZER, ATTENDEE, the video link |

## The rules it enforces

- **A real personal line or no email.** Each intro needs `personal_line`: one
  sentence about this investor from their public record. Refused: empty,
  under 7 words, cut off with "...", a placeholder, a stock opener ("hope this
  finds you well", "big fan", "love what you're doing", "impressive
  portfolio", "came across your profile"), the same line used for two people,
  and a line that names nothing from their row (a deal, a post, a sector, a
  number). Rows without an email or a public source URL are refused too.
- **Your real name and the opt-out line.** `founder.name` must be a real name
  ("Your Name" is refused). Every intro and follow-up carries "Not a fit?
  Reply 'no' and I won't follow up." A batch whose .eml lost it is refused.
- **The yes.** `approve` takes the user's reply word for word and the batch id
  `batch` printed. It counts only a reply that starts with "yes" and has no
  condition in it: "sure", "ok", "yes but drop Marcus", "yes tomorrow",
  "yes?" and a count that does not match the batch are not a yes. If the
  drafts changed after the batch was shown, the id no longer matches and
  nothing is recorded. `log --event sent` works only on an approved email.
- **The daily cap.** 20 cold emails a day by default (intros and follow-ups,
  counting today's sends and every approved one not sent yet), 50 at most
  whatever the config says. Replies in a live conversation do not count.
- **Three touches.** The intro on day 0, follow-up 1 on +3 business days and
  follow-up 2 on +7 (weekends and `outreach.holidays` skipped), never sooner
  than the planned gap after the touch before, and never once they replied.
- **Stops.** A no, an opt-out or a bounce ends the thread for good: the
  waiting draft is void, nothing more is recorded, and `draft` refuses that
  address forever. "Not now" is a soft pass: no more follow-ups, and
  /seed-updates can keep them posted if they asked.
- **Out of office** is not a reply: the follow-up waits until the business day
  after the return date it finds ("until Monday, November 9"), and a follow-up
  already drafted is voided and drafted again then.

Statuses: drafted, approved, sent, replied, interested, booked, and the ends
passed, bounced, optout.

## Sending: the Gmail-connector loop

The user connects their own Gmail in Claude (Customize > Connectors) and sets
the tools that send or draft to **Needs approval**, never Always allow. In
Claude Code, keep them on ask in `.claude/settings.json` and never in allow.
In the Claude Gmail connector checked on 2026-10-26 the tools are
`send_message` (send), `create_draft` (leave it in Drafts), `reply` (answer
inside a thread), `search_threads` and `get_thread` (read only); another
Gmail connector may name them differently. Nothing goes out any other way: no
mail-merge tool, no SMTP, no third-party sender.

1. `closer.py batch`. Show the user what it prints, as it prints it: every
   recipient with their personal line, the first email in full, the count
   against the daily cap. Ask: "Send these N emails from your Gmail? Reply yes
   or no." One batch per question.
2. `closer.py approve --batch <id> --reply "<their reply, word for word>"`.
   "Not recorded" means it was not a clear yes: ask again, never turn a reply
   into a yes yourself. To send fewer, show a smaller batch (`--ids`, `--limit`).
3. Only after "Recorded your yes", send each email from the JSON it printed,
   one tool call per email: `send_message` with that to, subject and body (or
   `create_draft` if the user would rather press send in Gmail). A follow-up or
   a reply goes in its thread with `reply` and the `thread_id`. Each call
   raises Claude's "Allow once / Deny" card: the second check.
4. After each send: `closer.py log --id <id> --event sent --thread-id <id from
   Gmail>`. Denied on the card: `log --id <id> --event denied` (back to
   drafted, it needs a new yes). Stop the loop if anything looks wrong.
5. Never from a scheduled or background task. A schedule may run `due`,
   `followup --due` and read replies; sending always waits for the user.

## Steps

1. Check `seed/config.json`: the user's real name, the address they send from,
   a postal address (anti-spam laws such as CAN-SPAM expect one). Read
   `seed/investors.json` from /seed-investors; ask before writing to anyone
   with a personal mailbox.
2. `closer.py draft --top 20`. Read back what it refused and why. Fix a
   refused personal line from the investor's sources, never by inventing a
   fact, then draft that id again.
3. Run the Gmail loop above for the batch: batch, the yes, send, log.
4. Every business day: `closer.py due`. For the ones due, `followup --due`
   (an optional `--extra` line for follow-up 1, `--ask` for the last one),
   then the same loop.
5. Read new replies with `search_threads` / `get_thread` (read only, for
   example `from:maya@northlight.example newer_than:14d`). Put them in a
   replies.json (`[{"from", "subject", "date", "text"}]`) and run `inbox`.
   Show the user each label and the suggested next step, then `inbox --write`.
   Labelling the threads in Gmail (Interested, Asked a question, Not now) is
   optional: ask first.
6. A question: draft the answer from `seed/plan.json` and `seed/model.json`
   only (never a number that is not in them), `reply --id ... --body-file`,
   then the loop. The .eml carries no attachment: link the deck, or the user
   attaches the PDF in Gmail.
7. Interested: find two free slots with the user's calendar (read only, for
   example `suggest_time` or `list_events`) and offer them in a reply. When
   they agree on a time, `inbox --write` that reply, then `closer.py book`.
   Show the invite, ask "Send this invite to Maya? Reply yes or no", and after
   the yes create the event in the user's own calendar with the investor as a
   guest (Google Calendar `create_event` sends the invite), or attach the .ics
   to a reply in the thread.
8. `closer.py status` for the funnel. Hand off: /seed-coach `agenda` for each
   booked call, /seed-updates `--to prospects` for the soft passes, and
   /seed-terms and /seed-dataroom when an investor asks for next steps.

## Example: the reel

Leashly is fictional, and so are the investors. `draft --top 6 --today
2026-10-26` writes six intros from the founder's own address; Maya Chen's
(Northlight Ventures, fit 96) reads:

```
To: Maya Chen <maya@northlight.example>
Subject: Leashly: dog walks without the surprise fees

Hi Maya,

Saw you led two pet-care seed rounds, so you know the 20% fee problem better than anyone.

Leashly is a dog-walking app with flat prices and a backup walker on every walk.

We're raising a $1.5M seed. Open to a 20-minute call next week?

Not a fit? Reply 'no' and I won't follow up.
```

After the user's "yes", Claude sends the six through Gmail. The reel's 40
emails would go out over two days at the daily cap of 20. With no reply, `due
--today 2026-10-29` lists follow-up 1 on Thursday, Oct 29 (+3 business days),
and follow-up 2 would come on Wednesday, Nov 4 (+7 business days; with
`business_days: false` it is Monday, Nov 2). Maya replied on Oct 30: "What's
your take rate, and how do you guarantee the backup walker?" `inbox` labels it
Asked a question and the follow-ups stop. Claude answered from the plan ("15%
flat, no owner fee. Every walk is booked with a second walker on standby
within 1 mile.") and asked "Would Thursday at 10 work for 20 minutes?". Her
"Thursday 10am works. Send an invite." is Interested, and

```
closer.py book --id maya-chen --start "2026-11-05 10:00" --tz America/New_York --link https://meet.google.com/abc-defg-hij
```

writes `seed/calls/maya-chen.ics`: "Leashly × Northlight Ventures · Intro
call", DTSTART 20261105T150000Z, DTEND 20261105T153000Z (10:00 to 10:30 AM
Eastern; the clocks went back on Nov 1, so it is UTC-05:00). The reel's
funnel, 40 sent, 12 replied, 5 interested, shows in `status` as drafted 40,
sent 40, replied 12 (30% of sent), interested 5, booked 1.

## What it never does

- Never sends, and never lets Claude send, without the user's yes for that
  batch; never "yes to everything from now on"; never from a background task.
- Never writes to anyone without a public source in their row, never guesses
  an email address, never collects a personal phone number or home address.
- Never emails a thread again after a no, an opt-out or a bounce.
- Never invents a fact in a personal line or a number in a reply.
- Never promises funding. The pack does the work; investors decide.
