---
name: whale-hunter
description: >-
  Whale Hunter. Finds the decision makers and pitches them. Looks up who signs the check, who owns the
  budget and who feels the pain at a company you want as a customer, using public business sources only,
  then writes a short pitch to the right person: what they pay today, the demo, and one small ask. Every
  email waits for your yes and goes out from your own account, with the legal footer and a plain way to
  opt out. Use when the user says "who decides at X", "find the decision maker", "find the CFO", "pitch
  them", "write the pitch", "cold email the buyer", "go after this company", or "hunt whales".
argument-hint: "[who <company> | draft <deal> | record <deal>]"
---

# whale-hunter

One big customer changes everything, and big customers don't come from ads. They come from a short,
specific note to the one person who can say yes. The Hunter finds that person and writes that note.
It never sends anything itself.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/hunter.py" who --company north-pier
python3 "${CLAUDE_SKILL_DIR}/hunter.py" draft --deal north-pier --demo https://yourproduct.example/demo
python3 "${CLAUDE_SKILL_DIR}/hunter.py" record --deal north-pier --subject "You pay \$6,400 a month to chase invoices" \
    --text-file /tmp/pitch.txt --approval "yes" --at 2026-10-26T09:04
```

Add people and deals with the shared board:

```bash
python3 "${CLAUDE_SKILL_DIR}/../market-researcher/board.py" company --id north-pier --name "North Pier Logistics" --website https://northpierlogistics.com
python3 "${CLAUDE_SKILL_DIR}/../market-researcher/board.py" person --id renee-alvarez --company north-pier --name "Renee Alvarez" --title CFO \
    --decides signs --email renee@northpierlogistics.com --email_source https://northpierlogistics.com/team
python3 "${CLAUDE_SKILL_DIR}/../market-researcher/board.py" deal --id north-pier --company north-pier --person renee-alvarez --title "Founding customer"
```

## Who decides

- **`signs`** signs the check. A CFO or an owner. Pitch this person first.
- **`budget`** owns the budget. A VP. Pitch them if the signer is out of reach.
- **`pain`** feels the pain every day. A manager. They rarely buy, but they tell you what it's worth, so talk to them first.

## Steps

1. **Find the people.** Search the company's own site (team, leadership, contact pages), press releases and professional
   profiles they published for work. Save each one with `board.py person` and where you found them.
2. **Find an address they publish.** `--email_source` is required. If the company doesn't publish one, use the general
   address or call. Never guess a pattern like first.last@company.
3. **Pick one.** `hunter.py who`. One person at a company at a time: emailing three executives at once looks like spam, and
   they talk to each other.
4. **Draft.** `hunter.py draft`. If you have a real number for this company (they published it or told you), it opens with it.
   If not, it uses what the market pays, and says "often". Fill any `[fill: ...]`. Make the first line more specific if you
   can, with something true. Under 90 words.
5. **Ask.** Show the email. "Send this to Renee Alvarez at North Pier Logistics? Reply yes or no." One email per question,
   every time.
6. **Send.** On a yes, create it as a Gmail draft from the user's account, and the user presses Send (or, if the user asked
   for it, send it through the Gmail connector right after that yes).
7. **Log.** Only after it went out: `hunter.py record --approval "<their yes, word for word>"`. `/follow-up` takes over. At most
   50 pitches a day: it protects the user's inbox reputation and keeps this one to one, not bulk mail.

## Example from the reel

North Pier Logistics: Renee Alvarez, CFO (signs the check); Tom Whitlock, VP Finance (owns the budget); Priya Nair, AR Manager
(feels the pain daily). The pitch to Renee, subject "You pay $6,400 a month to chase invoices": "Hi Renee, North Pier pays about
$6,400 a month to chase late invoices. We built a demo that does it automatically. Can I show you in 2 minutes?" (Illustrative:
North Pier and everyone at it are fictional. On the example board the figure came from Priya, on a call.)

## What it never does

- Never sends, and never records an email that did not go out.
- Never guesses an email address, and never emails anyone on the suppression list or marked do-not-contact.
- Never asks for money in a cold email. The first ask is 2 minutes.
- Never invents a fact about the company, a mutual friend, a past conversation or a fake "Re:".

## Consent and truth

- Nothing is sent, booked or charged without the user's explicit yes for that exact message. Claude drafts, the user says "yes",
  then it goes out from the user's own accounts. One yes per message. Never "yes to all".
- Every cold email is honest and legal: a real subject line, the sender's real name and business, a postal address, and a plain way
  to opt out (CAN-SPAM in the US; in the UK, EU and Canada cold email to people needs a lawful basis or consent first, so check
  before emailing there). Opt-outs are honoured forever.
- Public business information only: a company's own site and what people publish for work, never a person's private life, home or
  family, and nothing behind a login. A figure about a company's spending only goes in a pitch if they published it or told you.
- Never invent a number, a result, a client or a deadline.
