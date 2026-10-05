---
name: render-filter
description: "Render filters.js conditions as the repo's standard rule table — the six columns Change, Sender, Subject, List-Id, Actions, Replaces, one row per condition. Use whenever a response shows the user a filter rule: a rule about to be written, a rule that matched a message, or a rule proposed as a fix. Invoked by the filter and match skills; not a standalone task."
---

# Render filter (conditions → the rule table)

One table shape for every response that shows the user a `filters.js` rule, so a rule reads the same
whether it is about to be written, was found matching a message, or is only being proposed.

Input is one or more conditions and the actions of the entry each belongs to. Output is a markdown
table, one row per condition, followed by a one-sentence plain-language reading of it.

Examples in this file are invented. The privacy rule in `AGENTS.md` applies to anything written into
committed files; check a new example against the real spec before committing it.

## The table

Six columns — **Change, Sender, Subject, List-Id, Actions, Replaces** — in that order:

| Change | Sender         | Subject         | Actions              | Replaces        |
| ------ | -------------- | --------------- | -------------------- | --------------- |
| widen  | `*@acme.com`   | `Weekly digest` | Newsletters, archive | `news@acme.com` |
| add    | `*@*.acme.com` | `Weekly digest` | Newsletters, archive | —               |

> Mail from Acme whose subject contains "Weekly digest" gets the Newsletters label and skips the inbox.

- **Change** — what is happening to the spec: `add`, `widen`, `update`, `remove`, or `duplicate`
  (the row already exists; nothing is written).
- **Sender / Subject / List-Id** — the exact values in the spec, in backticks, `—` when the
  condition has no such criterion. A glob is shown as the glob, not paraphrased.
- **Actions** — the entry's labels, then its inbox effect: `archive`, `trash`, or nothing when the
  mail stays in the inbox.
- **Replaces** — the condition(s) this row supersedes; `—` when it supersedes none.

**Drop a column no row uses.** A column where every row would read `—` carries nothing, so it is
left out rather than rendered empty — which is why most tables show three or four columns, not six.
The order of the ones that remain never changes. Dropping is per table, not per row: one row with a
`List-Id` keeps the column for every row.

A condition's `comment` goes in the plain-language sentence, not a column.

## The sentence

One sentence under the table, reading the rule in plain language: which mail, and what happens to
it. It is what the user checks the table against, so it states the rule's effect rather than
restating its cells — "gets the Newsletters label and skips the inbox", not "Newsletters, archive".

For several rows that are one rule seen from two angles (a widen and the add beside it), one
sentence covers them both. For rows that are genuinely different rules, one sentence each.

## Which columns a caller uses

The columns are one vocabulary; a caller fills the ones its job gives it and the drop rule removes
the rest. Never invent a column outside the six — a verdict, a reason, an entry index belongs in the
prose around the table.

- **Writing a rule** (`filter`, `archive`) fills **Change** on every row, and **Replaces** on a
  `widen` or `update`.
- **Explaining a rule that already exists** (`match`) writes nothing, so **Change** and **Replaces**
  are empty on every row and drop out. What is left says what the rule matches and what it does.
  Which entry a row came from, and whether it fired in sieve, in Gmail or neither, go in the prose.
- **Proposing a fix** fills **Change** with what the edit would be, and says in the prose that
  nothing has been written yet.
