---
name: check-replies
description: Check Steve's Gmail for sent outreach and owner replies, and update each home's status. Use when Steve asks about replies, responses, follow-ups, or "who wrote back".
---

# Check replies

Use the Gmail connector to search. Only read emails to or from the owners in
this project. Do not read or summarize Steve's other emails.

1. List the homes he contacted:
   `uv run python -m sellers top --status drafted,emailed --n 100`.
2. For each home with status `drafted`, search Gmail for mail sent to that
   address (`in:sent to:<email>`). If you find it, run
   `uv run python -m sellers mark <id> emailed`.
3. For each home with status `emailed`, search for mail from that owner
   (`from:<email>`). If there is a reply, read it and pick one:
   - They ask to stop ("no thanks", "unsubscribe", "remove me"): **do this right
     away**: `uv run python -m sellers mark <id> do_not_contact --note "<their words>"`.
   - They are open to talking: `mark <id> interested --note "<short summary>"`.
   - They say no: `mark <id> not_interested --note "<short summary>"`.
   - Anything else: `mark <id> replied --note "<short summary>"`.
   Show Steve your choice for each one. He can change it.
4. Bounced emails come from "Mail Delivery Subsystem" or "postmaster". For each
   one, run `mark <id> skip --note "email bounced"`.
5. Give Steve a short summary: who replied, who is interested, and what to do
   next. You can offer to write a reply as a draft. Follow the rules in
   `.claude/skills/write-emails/SKILL.md`, and never send it.
