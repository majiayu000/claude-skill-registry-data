---
name: record-keeper
description: >-
  Record Keeper. Logs every email and call for you, so you never update a CRM by hand again.
  Reads your inbox through the Gmail connector, matches every message to a contact on the
  board, and logs it (opening, follow-up or reply) into closer/pipeline.json; logs calls with
  their notes saved to closer/calls/; shows the full timeline with anyone; and lists new
  addresses writing in that are not contacts yet. Use when the user says "log this",
  "log my emails", "sync my inbox", "update the CRM", "what's my history with X",
  "save the call notes", or at the end of every call and every morning.
argument-hint: "[sync | timeline <contact> | call <contact>]"
---

# record-keeper

The Record Keeper keeps the board true without anyone typing into it. Every email in and out and
every call ends up in `closer/pipeline.json` (the schema `/pipeline` owns), once.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/log.py" sync --emails closer/inbox-2026-10-27.json
python3 "${CLAUDE_SKILL_DIR}/log.py" unknown --emails closer/inbox-2026-10-27.json
python3 "${CLAUDE_SKILL_DIR}/log.py" log --contact dana-harbor-lane --channel email --direction in \
    --subject "Re: Quick idea for Harbor Lane Dental" --text "Sorry, crazy week! Thursday at 2 works." \
    --at 2026-10-27T11:48
python3 "${CLAUDE_SKILL_DIR}/log.py" call --contact dana-harbor-lane --minutes 24 \
    --notes-file /tmp/harbor-lane-notes.md --at 2026-10-29T14:00
python3 "${CLAUDE_SKILL_DIR}/log.py" timeline --contact dana-harbor-lane
```

## Syncing email

1. With the Gmail connector, search the user's mail since the last sync for messages to or from
   any contact's address (`from:dana@harborlanedental.com OR to:dana@harborlanedental.com ...`).
   Read only those threads. Never read other mail for this.
2. Write what you found to a sync file: a JSON list of
   `{"date": "YYYY-MM-DDTHH:MM", "from": "...", "to": ["..."], "subject": "...", "text": "..."}`
   with the text trimmed to the new part of each message (no quoted history).
3. `log.py sync --emails <file>`. It skips anything already logged, so running it twice is safe.
   Email the user sent from their own inbox is logged with approval "sent by you from your inbox".
4. If a reply says no or asks to stop, tell the user and run `/follow-up`'s `reply` for that person
   so every skill stops. Do not just log it.
5. `log.py unknown` lists addresses that wrote in but are not contacts. Ask the user before adding any.

No Gmail connector? The user can paste or forward the emails, and you log them with `log.py log`.

## Logging a call

After every call, write the notes in plain lines: what they need, what they said about price,
what was agreed, the next step and its date. Then `log.py call`. The notes file lands at
`closer/calls/<date>-<company>.md` and a one-line summary goes on the board. If `/sales-coach`
ran on the call, use its `review` output as part of the notes.

## Example from the reel

Dana's thread in the reel, logged with no typing: the opening on Mon Oct 19 at 9:02 AM, follow-ups
on Oct 21, 23 and 27, her reply on Tue Oct 27 at 11:48 AM ("Sorry, crazy week! Thursday at 2 works."),
then the call on Thu Oct 29: "Call, 24 min. Loved the site. Price objection on $2,500; agreed to the
$399/mo plan, no setup fee. Wants to start Monday." `timeline --contact dana-harbor-lane` prints all of
it. (Illustrative: Dana and Harbor Lane Dental are fictional.)

## What it never does

- Never logs an outgoing message the user did not send or approve.
- Never reads mail beyond the threads with known contacts, and never stores attachments.
- Never edits or deletes what is already logged: a correction is a new note.

## Consent and truth

- Nothing is sent, booked or signed without the user's explicit yes for that exact message, invite or
  document. This skill only records; it never sends anything.
- Calls: tell everyone on the call that captions or notes are on, before you start. Some places (for example
  California, Florida, Washington, and many countries) need every person's consent to record.
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Never invent what was said. Notes are what happened, in plain words.
