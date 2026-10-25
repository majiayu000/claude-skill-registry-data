---
name: hunter-followup
description: >-
  Follow-up Manager. Sends polite follow-ups so no thread goes cold, and stops
  before anyone feels chased. Every morning it reads hunter/pipeline.json and
  lists what is due today: follow-ups on unanswered outreach, replies waiting
  on you, drafts waiting for your yes, applications with no news after 10 days,
  thank-you notes after interviews and coffee chats, and anyone the stop rules
  have closed (first "no", 2 follow-ups, 21 days of silence, a stop request
  honoured forever). Drafts each message from a polite template; you approve,
  it goes out from your account, and it is logged. Use when the user says
  "follow up", "who do I need to follow up with", "nudge", "they haven't
  replied", "check on my application", "thank-you note", or every morning.
argument-hint: "[--today YYYY-MM-DD]"
---

# hunter-followup

The Follow-up Manager keeps every conversation warm without pestering anyone. It
reads the pipeline, says what is due, drafts it, and waits for the user's yes. It
never sends anything by itself.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/followup.py" due --today 2026-10-15
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --contact maya-c-google --template nudge-1 \
    --hook "One new, true line." --today 2026-10-15
python3 "${CLAUDE_SKILL_DIR}/followup.py" record --contact maya-c-google --channel email \
    --text-file /tmp/sent.txt --approval "yes" --today 2026-10-15
python3 "${CLAUDE_SKILL_DIR}/followup.py" reply --contact maya-c-google --channel email \
    --text "Happy to grab a coffee, does Thursday at 10 work?" --today 2026-10-16
python3 "${CLAUDE_SKILL_DIR}/followup.py" stop --contact <id> --said "Please stop emailing me" --today 2026-10-16
python3 "${CLAUDE_SKILL_DIR}/followup.py" templates
```

Every command takes `--file` (default `hunter/pipeline.json`, the schema
`/hunter-tracker` owns) and `--today`, so a run is reproducible.

## The stop rules (the same as /hunter-connector's)

`/hunter-connector` applies them to each conversation; this skill applies them to the
PERSON, across every channel, which can only stop earlier, never later:

1. **Stop at the first "no"** or any sign of disinterest ("not interested", "no
   thanks", "please stop", "the role has been filled"...), and honour a stop
   request forever. A declined thread, a "no" in their reply or "DO NOT CONTACT" in
   the contact's notes closes every thread with them.
2. **At most 2 follow-ups** after the first message. An email and a LinkedIn request
   sent the same day count as one opening, not as a follow-up.
3. **Nothing after 21 days of silence**, counted from their last reply, or from the
   first message if they never replied.
4. **A pending LinkedIn invitation gets no follow-up** (`"invite": true` on the thread).

`record` refuses to log a follow-up that breaks a rule, and `draft` refuses to draft
one. A reply from them resets the count: it is a conversation now, and answering
them is never a "follow-up".

## The cadence

- Follow-up 1: 3 days after the opening (the reel: Day 1 email, Day 4 follow-up).
- Follow-up 2, the last: 7 days after follow-up 1, and it says it is the last note.
- A thread's own `next_followup` date (set by `/hunter-connector` or by the user)
  replaces the cadence date. The stop rules still win.
- Applications: one check-in after 10 days with no news, to a contact you already
  have at the company. No contact yet: `/hunter-connector` finds the hiring manager.
  Big companies say they cannot answer every applicant (Google's hiring page says
  so); the application status page is the right place to check there.
- Interviews and coffee chats: a thank-you within 24 hours.

## Steps, every morning

1. `followup.py due --today <date>`. Read it to the user grouped as it prints: DUE
   NOW, YOUR TURN (they replied), DRAFTS WAITING FOR YOUR YES, WAITING, STOPPED,
   APPLICATIONS AND NEXT STEPS.
2. For each item the user wants to act on, `followup.py draft --contact <id>
   --template <name> --hook "<one new, true line>"`. The hook is the whole point of
   a good follow-up: one new specific thing (a result, a relevant post of theirs,
   an answer to their question). Fill every `[fill: ...]`; nothing goes out with one.
3. Show the draft. Ask: "Send this to <name>? Reply yes or no." One message per
   question. Never "yes to all".
4. On a yes: email goes in as a Gmail draft from the user's account (the Gmail
   connector), and the user presses Send. A LinkedIn message is typed by Claude in
   Chrome with the user watching, and the user clicks Send.
5. Only after it went out: `followup.py record ... --approval "<their reply, word
   for word>"`. It logs the message and sets the next follow-up date, or none.
6. When they answer, `followup.py reply` logs it. A "no" closes every thread with
   that person for good. A request to stop: `followup.py stop`.

A scheduled morning run may list and draft. It never sends: nobody is there to say yes.

## Example: Maya C. in the reel

Jordan emailed Maya and sent a LinkedIn request on Monday 2026-10-12 (Day 1). On
Thursday the 15th (Day 4), `due` says:

```
DUE NOW
  Maya C. (Google) by email: follow-up 1 of 2: opened 2026-10-12, no reply
    draft it: followup.py draft --contact maya-c-google --template nudge-1
```

Jordan approves the nudge ("Floating this back up in case it got buried. The
payments API rebuild cut p99 latency 38%..."), sends it from Gmail, and it is
recorded; follow-up 2 would be due on the 22nd. On Friday the 16th (Day 5) Maya
replies, "does Thursday at 10 work?". `due` moves her to YOUR TURN; Jordan answers
with the confirm-time template and the thread is booked. From then on: no
follow-ups, and on the 22nd `due` says "today: Coffee chat with Maya C. Afterwards,
a thank-you within 24 hours (template after-coffee)". The full state is
`../hunter-tracker/pipeline.example.json`.

## What it never does

- Never sends, and never records a message that did not go out.
- Never follows up after a no, after 2 follow-ups or after 21 days of silence.
- Never nudges the same person on two channels at once.
- Never uses guilt, fake urgency or a made-up reason to follow up.

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
