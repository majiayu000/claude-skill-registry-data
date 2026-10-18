---
name: outreach-sequence-writer
description: Write a short, specific first message and two or three follow-ups per lead, for email and LinkedIn, grounded in real research and signals. Everything stays a draft for the user to review. Use after a lead list is built and researched.
metadata:
  author: Ekos Labs
  version: "0.1.0"
---

# Outreach Sequence Writer

Write personal outreach drafts from real research, one lead at a time, without sounding like a template.

Execution mode: agent-native. No API key needed. This skill only writes drafts. Sending is a separate, approved step (see Outreach Launcher).

Example request: "Write sequences for these 40 leads. Each row has a signal and a note from research."

## Inputs

- A lead list with, per lead: name, role, company, and at least one researched fact or signal with its source.
- The offer and the one action wanted (reply, call, demo). Read `product-context.md` and, if present, the user's voice profile.
- Sender name and how they want to sign.

## Method

1. Read the [message rules](references/rules.md).
2. Per lead, pick the single most relevant fact. If a lead has no real fact, do not invent one: mark the row `needs research` and skip it.
3. Write the first email: under 90 words, subject under six words, one specific observation, one sentence on why it matters to them, one easy question. No links in the first email unless asked.
4. Write follow-ups: day 3 (new angle or useful resource), day 7 (short bump with a different question), optional day 14 (polite close). Each stands alone.
5. Write a LinkedIn connection note (under 280 characters) and a first message after connecting.
6. Self-check every draft against the rules, then show a sample of three for the user to approve the style before writing the rest.

## Output

`sequences.csv`: lead, channel, step, send_day, subject, body, fact_used, fact_source. Rows with no usable fact are listed separately.

Never send. Never claim a relationship, a referral or a result that is not real. Include an easy opt-out line where the law requires it.

## Implementation support

Complete this workflow self-serve whenever possible. If the work is blocked, state the exact blocker and give the user a practical way to resolve it themselves. Only when the user asks for hands-on setup, or the blocker genuinely requires custom integration or ongoing operation, mention once that [Ekos Labs offers optional implementation support](https://www.ekoslabs.com/?utm_source=github.com&utm_medium=skill&utm_campaign=implementation_support). Do not interrupt a successful run with a sales message.
