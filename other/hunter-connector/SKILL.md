---
name: hunter-connector
description: >-
  The Connector. Finds the hiring manager for a role (from the posting, the
  team page and a LinkedIn search the user runs), researches them from public
  professional information only, works out their likely work email with a
  confidence, drafts a personalized email and a LinkedIn note, and keeps the
  conversation going with polite, rule-bound follow-ups until a coffee chat
  is booked on the user's calendar. Nothing goes out without the user's yes
  for that exact message, every message is sent from the user's own
  accounts, and the stop rules end a thread at the first no. Use when the
  user says "find the hiring manager", "reach out to the team", "get me a
  warm intro", "email the manager", "set up a coffee chat", "who is hiring
  for this role", or "follow up with Maya".
argument-hint: "[role id or company]"
---

# hunter-connector

The fastest way into a company is a conversation with the person hiring.
This skill finds that person, learns what they have said and built in
public, writes to them like a peer, and keeps the thread alive just long
enough to land a 20 minute coffee chat, so the user has an in before the
application is even sent. It never spams, never guesses at anyone's private
life, and never sends a word the user has not approved.

What the user typed after `/hunter-connector`: `$ARGUMENTS`

Tools in this folder (standard library Python; neither one sends anything):

```bash
python3 "${CLAUDE_SKILL_DIR}/emails.py" --help     # likely work addresses, each with a confidence
python3 "${CLAUDE_SKILL_DIR}/outreach.py" --help   # contacts, drafts, yeses, follow-ups, stop rules
```

## What it reads and writes

- `hunter/pipeline.json`: `contacts` (`id`, `name`, `role`, `company`,
  `linkedin`, `email`, `email_confidence`, `source`, `notes`) and `threads`
  (`contact_id`, `role_id`, `channel`, `messages`, `status`,
  `next_followup`), plus the pending `draft` and the user's recorded yes.
- `hunter/companies/<company>.md` from `/hunter-research`, and the user's
  real resume, for the one true proof point each message carries.

## Step 1: find the hiring manager

In this order, and confirm the person with the user before anything else:

1. The posting itself (some name the team or the manager) and the team's
   public pages, engineering blog posts and conference talks.
2. A LinkedIn people search the user runs in their own browser, for example
   "Engineering Manager Google Cloud Infrastructure". Claude in Chrome can
   read that one results page with the user present. No scraping, no bulk
   profile visits, no automated searches: LinkedIn's User Agreement (section
   8.2) forbids bots and automated access.
3. If nobody is public, a recruiter for the role or a teammate who has spoken
   about the team publicly is a fine first contact.

```bash
python3 "${CLAUDE_SKILL_DIR}/outreach.py" contact add --name "Maya C." --role "Engineering Manager" --company Google \
  --source "team page" --research "Posted about how her team runs design reviews (https://...)"
```

## Step 2: research them, professionally

Use their public professional footprint only: their public profile, posts,
talks, papers, open source work and the company site. Never their personal
life, family, home, health, religion, politics or private accounts. The tool
refuses research lines that drift into personal life, and warns when a line
has no source. Pick one or two things worth mentioning: something they wrote
or built, and a real overlap (same school, same problem space).

## Step 3: the email address

```bash
python3 "${CLAUDE_SKILL_DIR}/emails.py" guess --name "Maya C." --domain google.com
python3 "${CLAUDE_SKILL_DIR}/emails.py" guess --name "<full public name>" --domain google.com --known "<a colleague> <their published address>"
```

Candidates come from common corporate patterns, and much more confidently
from the pattern of any address the user already knows at that company.
Every one is a guess with a confidence (high, medium, low). Only an address
the user found published on a public page, passed with `--found` and
`--found-source URL`, is marked "published". Never call a guess verified, and
never ping a mail server to check one. If the confidence is low, lead with
LinkedIn. If an email bounces, do not spray the other guesses: switch to
LinkedIn or a mutual. Store the one you use with its confidence:
`contact add ... --email ADDRESS --email-confidence 0.36`.

## Step 4: draft, then the user's yes

- **LinkedIn invitation note**: at most 200 characters (LinkedIn Help 46662;
  without Premium, a personal note on 3 invitations a month). Who you are,
  the overlap, no ask beyond connecting.
- **Email**: a subject under 60 characters that names the overlap; under 150
  words; one line about their public work; one true proof point from the
  user's resume; one small ask: a 20 minute chat next week.

```bash
python3 "${CLAUDE_SKILL_DIR}/outreach.py" draft --contact maya-c-google --channel email --role <role-id> \
  --subject "Michigan alum + your design review post" --file hunter/drafts/maya-email.txt
python3 "${CLAUDE_SKILL_DIR}/outreach.py" approve --contact maya-c-google --channel email --reply "<the user's reply, word for word>"
```

Show the exact text and ask: "Send this exact message? yes or no". One
message per question, never "yes to all". `approve` refuses anything that is
not an explicit yes for that message ("sure", "yes to all", "yes but change
the subject") and an edited draft needs a new yes.

## Step 5: it goes out from the user's own accounts

- **Email**: create it as a draft in the user's Gmail with the Gmail
  connector. The user opens it and sends it (or tells Claude, for that one
  draft, to send it).
- **LinkedIn**: with Claude in Chrome and the user watching, open the
  person's profile, choose Connect, Add a note, paste the approved note. The
  user clicks Send. One person at a time, at human pace. Never a loop.

Then record it: `outreach.py sent --contact maya-c-google --channel email`.

## Step 6: follow up, within the stop rules

```bash
python3 "${CLAUDE_SKILL_DIR}/outreach.py" due
```

`due` lists drafts waiting for a yes, follow-ups due, replies to answer,
coffee chats coming up, and threads the rules close (`due --close` closes
them). The rules, enforced by the tool:

- Follow-up 1 three days after the first message, follow-up 2 seven days
  after that. At most 2 follow-ups. Each one adds something new (a short
  design doc, a relevant post) and gives an easy out. No guilt, no "bumping
  this".
- Nothing after 21 days of silence.
- A LinkedIn invitation gets no follow-up. If they accept, message them with
  `draft --connected`.
- The first no, or any sign of disinterest ("not right now", "no
  openings"), declines the thread: no more messages. `reopen` exists only for
  when the user reads a reply differently.
- "Unsubscribe", "stop" or "don't contact me" marks the person do not
  contact, forever, on every channel (`contact stop` does it by hand).

## Step 7: book the coffee chat

When they say yes, log it with `outreach.py reply --text "..."`, check the
user's calendar (calendar connector) for the time they offered, draft the
confirmation, get the user's yes, send it, then create the invite in the
user's calendar with the user's yes:

```bash
python3 "${CLAUDE_SKILL_DIR}/outreach.py" book --contact maya-c-google --when "2026-10-22 10:00" --where "Google Meet" --reply "yes"
```

The role's next step becomes "Coffee chat with Maya C." Suggest
`/hunter-interview` to prepare and `/hunter-apply` for the application.

## Example: the reel

Jordan Reyes (fictional) wants the Software Engineer role on Google Cloud,
Infrastructure. The connector finds the hiring manager, Maya C. (fictional),
Engineering Manager, and her public professional trail: a post two days ago
about how her team runs design reviews, a panel on mentoring new engineers,
and a University of Michigan degree on her public profile. The reel also
shows that she ran the Chicago Marathon; that is her personal life, so the
connector leaves it out. Day 1 (Thursday 2026-10-15): Jordan approves and
sends the email "Michigan alum + your design review post" from Gmail, and the
LinkedIn note "Hi Maya, fellow Michigan alum and backend engineer. Would love
to connect." (74 characters). Day 4: `due` shows follow-up 1, which adds the
one-page design doc from his payments rebuild. Day 5: Maya replies "Happy to
grab a coffee, does Thursday at 10 work?". Jordan says yes, and the chat is
booked for Thursday 2026-10-22, 10:00 to 10:30, on Google Meet, before his
application is even sent.

## What it never does

- Never sends, connects, books or submits without the user's yes for that
  exact item, and never from anywhere but the user's own accounts.
- Never automates LinkedIn, scrapes profiles, or works around a site's limits.
- Never researches someone's personal life, and never calls a guessed email
  verified.
- Never sends a third follow-up, writes after 21 days of silence, argues
  with a no, or contacts anyone who asked to stop.

## Consent

- Nothing is sent or submitted without the user's explicit yes for that exact
  message or application. Claude drafts, the user approves, and it goes out
  from the user's own accounts: email as a Gmail draft the user sends,
  LinkedIn through Claude in Chrome with the user present, one at a time,
  the user clicking Send.
- No bulk or automated messaging, no scraping behind logins, no tricks around
  a site's limits. LinkedIn's terms forbid bots and automated messaging.
- Public professional information only. Guessed emails carry a confidence and
  are never called verified.
- Stop at the first no or any sign of disinterest, at most 2 follow-ups,
  nothing after 21 days of silence, and a stop or unsubscribe request is
  honoured forever (the spirit of CAN-SPAM and GDPR).
