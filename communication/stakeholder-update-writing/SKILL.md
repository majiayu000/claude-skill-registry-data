---
name: stakeholder-update-writing
description: Style rules for outward-facing deliverables — client/team chat messages, status reports, results write-ups, meeting follow-ups. Use whenever drafting an update, delivery message, or report that people outside this chat will read.
---

# Stakeholder update writing

Every outward-facing deliverable must read like the user wrote it themselves.
Apply these rules on top of the vendored `humanizer` skill.

## The rules

1. **Humanizer pass.** Run the `humanizer` skill (vendored at
   `.claude/skills/humanizer`) over the final text. Hard constraints from it:
   no em dashes, straight quotes, sentence-case headings, no bold-colon bullet
   lists, active voice.
2. **First person singular.** The user writes as "I" unless they tell you the
   update speaks for a team.
3. **Quote literal system values** when they appear inline in prose: error
   strings, button labels, status names ("Not Found", "Begin Validation").
   Table and field names used descriptively stay unquoted.
4. **Tables over walls of text.** Per-record results, change lists, and field
   references go in tables. Prose is for explanation only.
5. **Keep the identifiers.** Record ids, amounts, file names stay in — readers
   navigate by them. Code internals (function names, branches, diffs) stay out
   unless the audience is engineers.
6. **Questions live in the message, not the report.** Anything needing the
   audience's call goes in the chat/email message only; an attached report
   states facts and never poses questions, so nothing is asked in two places.
7. **Match the user's voice.** Before drafting, check `Wiki/` entity notes or
   past updates for their register (openers, contractions, sign-offs) and
   mirror it. Ask if you have no sample.
8. **ETAs are the user's to promise.** Draft dates as proposals they can edit,
   and say in chat that a date is a commitment they'd be making.

## Order of work

Draft the content first (facts, tables, numbers verified against the vault),
apply rules 2–8, then run the humanizer loop last and fix what it catches.
