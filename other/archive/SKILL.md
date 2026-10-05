---
name: archive
description: 'Auto-archive mail like a message the user shows or names (a screenshot, or its sender and subject): keys a filters.js archive rule on sender and subject together and hands it to the filter skill to dedupe, write and sync. Shorthand for "/filter auto-archive based on sender + subject". Use when asked to archive, auto-archive or keep out of the inbox mail like a given message ("archive this", "auto-archive these").'
---

# Archive (message → mail like it skips the inbox)

Shorthand for `/filter auto-archive based on sender + subject`. Input is one message: a screenshot,
its sender and subject typed out, or both. Output is a `filters.js` rule that archives mail from
that sender whose subject marks it as the same kind, written and synced by the `filter` skill.

This skill settles what a bare "archive this" leaves open — the action, the scope, the key — so the
usual run asks nothing. Everything else belongs to `filter`: the session-title prefixes, where the
spec lives, the dedupe, the sync and the report.

Examples in this file are invented; the privacy rule in `AGENTS.md` applies to it.

## Procedure

### 1. Hand off to filter

Invoke the `filter` skill (Skill tool) with the args `auto-archive based on sender + subject`,
followed by anything the user typed, and follow it end to end. The steps below amend the `filter`
steps they name; where they are silent, `filter` stands.

### 2. Settle the open choices (filter steps 2–3)

Unless the user's words say otherwise:

- **Archive only.** The mail skips the inbox; no label is added and nothing is trashed.
- **Mail like this one.** "These" means the message's own kind, not everything its sender sends.
- **Sender and subject together**, even when the sender sends nothing else today: the subject keeps
  a later security alert from the same address in the inbox.

### 3. Find the message's kind (filter steps 1–2)

If the screenshot shows several messages and nothing singles one out — an open message, a selected
row, a typed sender — ask which, with 🚙 set first.

Survey the sender with `search_threads` on `from:<address>` (the domain, when the local part
rotates), `pageSize` 50, paging back until a full page adds no new kind — kinds the sender has
stopped sending do not matter. The message's own kind is the family; the other kinds are the
"sender's other mail" that filter step 2's fragment must not match, and they keep going where they
go today.

| Family vs. the sender's other kinds                    | Rule                                          |
| ------------------------------------------------------ | --------------------------------------------- |
| A fragment the whole family has and no other kind does | sender + that fragment — the usual case       |
| No such fragment, but a List-Id only the family has    | sender + List-Id                              |
| No such fragment, and the sender sends no other kind   | sender alone — say so in the report           |
| No such fragment, and other kinds exist                | not expressible — say so and ask, with 🚙 set |

Reuse the `from` the spec already has for this sender, if it has one (filter step 4's grep finds
it), so the sender's conditions differ only by subject.

### 4. Keep every label (filter step 4)

Archiving adds to what the mail gets today; it never swaps a label out. An entry that already
labels this mail keeps doing so:

- **A broader condition** (`*@acme.com` → Newsletters) stays as it is, and the archive condition
  goes in an archive-only entry. Gmail stacks the two filters, and in Proton a label never
  conflicts with a folder.
- **The same condition** moves to an entry with that label plus `archive` — never to an
  archive-only entry, which would drop the label.

An entry that already archives this mail makes the request a `duplicate`. If the screenshot shows
the message in the inbox anyway, that is the `match` skill's step 4 — mail older than the filter,
an unsynced filter, or a `gmail` NO MATCH — not a reason for a second rule.

### 5. Repeat the account test on the rendered rule (filter step 5)

After the edit, repeat filter step 2's account test on the `gmail` term the matcher prints for the
new condition, back to the oldest date step 3 surveyed (`after:`). Every thread it returns must be
the family; anything else is mail the filter would archive by mistake — lengthen the fragment and
check again before syncing. The rendered term is what the filter will actually run: the glob as the
renderer translated it, and every address a widened `from` reaches.

### 6. Report (filter step 7)

Add one line naming the sender's other kinds — the mail this rule leaves where it was. The message
itself stays where it is too: the rule is for mail still to come.
