---
name: follow-up
description: >-
  Follow-Up. Keeps the deal moving. Tells you who is due today after a pitch or an offer, drafts the next
  note (a bump, something useful, a last note), waits for your yes, logs it, and stops at the first "no",
  the moment a demo is booked, after 3 follow-ups or after 30 days. Logs their replies and knows when it's
  your turn. Use when the user says "follow up", "who do I need to follow up with", "they haven't replied",
  "chase", "nudge", "bump this", "they replied", "they said no", or every morning.
argument-hint: "[due | draft <deal> | reply <deal> | stop <deal>]"
---

# follow-up

Big deals are lost to silence more often than to "no". Busy people don't answer the first email. This skill makes
sure nobody is forgotten and nobody is pestered. It drafts; it never sends by itself.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/followup.py" due --today 2026-10-28
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --deal north-pier --today 2026-10-28
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --deal north-pier --today 2026-10-30 \
    --hook "here's what the demo looks like with a freight company's invoices."
python3 "${CLAUDE_SKILL_DIR}/followup.py" record --deal north-pier --text-file /tmp/f.txt --approval "yes" --at 2026-10-28T09:00
python3 "${CLAUDE_SKILL_DIR}/followup.py" reply --deal north-pier --text "Interesting. Can you show me tomorrow?" --at 2026-10-28T14:20
python3 "${CLAUDE_SKILL_DIR}/followup.py" stop --deal north-pier --said "Please remove me from your list." --at 2026-10-30
```

## The rules (per person, across every channel)

1. **Stop at the first "no"** or any sign of disinterest ("not interested", "no thanks", "we're all set", "please remove me").
   An unsubscribe goes on the suppression list, and no skill emails them again.
2. **Stop the moment a demo is booked.** That is the job.
3. **A reply is your turn.** Answering them is a conversation, never a follow-up.
4. **At most 3 follow-ups** after a pitch or an offer, and the third one says it's the last.
5. **Nothing after 30 days** without a reply.

`draft` refuses to draft and `record` refuses to log anything that breaks a rule.

## The cadence

Follow-up 1 is two days after the pitch or offer, follow-up 2 two days after that, follow-up 3 four days after that. A date on a weekend
moves to Monday.

1. **The bump.** Short: "just bumping this up in case it got buried."
2. **Give something.** One new, true, specific thing for them (`--hook`). Without a hook there is no follow-up 2.
3. **The last note.** Ask for a day, and say it's the last email. Either answer is fine.

## Steps, every morning

1. Check the inbox first, so replies are on the board: `followup.py reply` for each.
2. `followup.py due`. Read it to the user grouped as it prints: DUE NOW, YOUR TURN, WAITING, BOOKED, STOPPED.
3. For each DUE NOW, `followup.py draft`. Fill every `[fill: ...]`. Show it: "Send this follow-up to Renee? Reply yes or no." One message per question.
4. On a yes: a Gmail draft in the same thread from the user's account, which the user sends (or sent through the Gmail connector right
   after that yes). Then `followup.py record --approval "<their yes, word for word>"`.
5. For each YOUR TURN: if they want a demo, book it and `board.py move --stage demo-booked`. If they pushed back, `/objection-handler`. If they
   said no, `followup.py stop` with their words: it stops everything and marks the deal lost.

A scheduled morning run may list and draft. It never sends: nobody is there to say yes.

## Example from the reel's board

Renee Alvarez doesn't answer the pitch on Mon Oct 26. Follow-up 1 on Wed Oct 28: "Just bumping this up in case it got buried." At 2:20 PM she
replies, "Interesting. Can you show me tomorrow?" The deal moves to YOUR TURN, the demo is booked, and she gets no more follow-ups. Gwen Tate at
Harrow Line replies, "We're all set, thanks." The deal is lost, and she hears nothing else. (Illustrative: everyone here is fictional.)

## What it never does

- Never sends, and never records a message that did not go out.
- Never follows up after a no, after a booking, after 3 follow-ups or after 30 days.
- Never uses guilt, fake urgency, a fake "Re:" or a made-up reason to write.

## Consent and truth

- Nothing is sent, booked or charged without the user's explicit yes for that exact message. Claude drafts, the user says "yes", then it goes out from
  the user's own accounts. One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Every email keeps the opt-out line from the opening thread. Opt-outs are honoured forever.
- Never invent a number, a result, a client or a deadline.
