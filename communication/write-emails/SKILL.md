---
name: write-emails
description: Write personal emails to the owners of Steve's top homes and save them as Gmail drafts for him to review and send. Use when Steve asks to write, draft or prepare emails or outreach.
---

# Write owner emails (as Gmail drafts)

**You never send email.** You only save drafts. Steve reads, edits and sends
them himself in Gmail.

## 1. Check before you write

- Read `[me]` in `settings.toml`. If `name`, `brokerage`, `dre_number`, `phone`
  or `office_address` is empty, ask Steve and save the answer there first. The
  law requires the license number and a postal address.
- Check that you have the Gmail connector. Its tools have `Gmail` in the name,
  for example a tool that creates a draft. If you do not have it, tell Steve:
  "Open claude.ai, go to Settings, then Connectors, and connect Gmail. Then
  start a new chat here."
- Get the homes: `uv run python -m sellers top --need-email --json --n <batch_size>`.
  `batch_size` is under `[emails]` in `settings.toml`. This list already leaves
  out do-not-contact emails and homes whose status is not `new`.

## 2. Write each email

Use only facts that are in the home's record. Write like a real local agent,
not a robot.

- **Subject**: short and honest, about the home. Example: "Your home on Calle Del Mar".
- **Body**: 60-120 words, plain text.
  - Say who Steve is: a local real estate agent. This is a business email, so
    make that clear.
  - Give a true reason for writing about *this* home: the street, the
    neighborhood or the city.
  - Ask one easy question. Example: "Would you be open to a quick chat about
    what your home could sell for today?"
  - End with the signature and footer below.
- **Signature and footer**: always include these, filled in from `settings.toml`:

  ```
  <name>
  <brokerage> | DRE #<dre_number>
  <phone>
  <office_address>

  If you'd rather not hear from me, just reply "no thanks" and I won't email you again.
  ```

**Never write:**
- That Steve has a buyer, an offer or a price, unless Steve tells you it is true.
- Anything from the score: that the owner lives out of state, how long they
  have owned the home, their equity, or that it is in a trust. Owners find this creepy.
- Anything about the owner's health, family, money trouble or age.
- Fake urgency ("act now"), fake friendship, or flattery.

If you are not sure about a fact, leave it out.

## 3. Show Steve, then save

1. Show Steve every draft in the chat: the address, the recipient, the subject and the body.
2. Ask: "Shall I save these as drafts in your Gmail?" Make any changes he asks for.
3. For each approved email, create a Gmail **draft** with the Gmail connector
   (to = the owner's email, plus the subject and body). Do not send it.
4. Mark the home: `uv run python -m sellers mark <id> drafted --note "Gmail draft: <subject>"`.
5. Tell Steve: "Your drafts are in Gmail under Drafts. Read each one, edit it
   if you like, and press Send when you are happy. In a few days, ask me to
   check replies."

If an email address ends in `@example.com`, the home is demo data. Say so.
Drafts to example.com are safe practice and never reach anyone.
