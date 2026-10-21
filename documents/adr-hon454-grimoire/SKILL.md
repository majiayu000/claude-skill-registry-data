---
name: adr
description: Use when a design or architecture decision has just been made, when the user asks to record, write or supersede an ADR (architecture decision record), or when a choice is hard to reverse and a future reader would ask why. Decides whether the decision deserves a record, finds the repository's decision log, and writes one immutable MADR-style record with a one-sentence Y-statement.
license: MIT
metadata:
  plugin: book-of-engineering
  kind: documentation
  credits:
    - skill: domain-modeling (ADR-FORMAT.md)
      author: Matt Pocock
      url: https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling
      license: MIT
---

# Architecture decision records

An ADR records one decision, why it was made, what was rejected and what it costs. It is written once and never edited afterwards; a changed mind gets a new record that supersedes the old one. The value is in recording *that* a decision was made and *why*, so the next reader does not "fix" something that was deliberate.

## 1. Decide whether this deserves a record

Offer an ADR only when all three hold:

1. **Hard to reverse.** Changing your mind later costs real effort.
2. **Surprising without context.** A future reader of the code would ask "why on earth did they do it this way?"
3. **A real trade-off.** There were genuine alternatives and one was picked for specific reasons.

If any is missing, skip it. An easily reversed decision will simply be reversed; an unsurprising one raises no question; a decision with no alternative records nothing beyond "we did the obvious thing". Minor conventions (naming, formatting, defaults) go in the project's contributor guide, not in an ADR.

What qualifies: architectural shape (monorepo, event-sourced writes), integration patterns between parts, technology choices that carry lock-in (database, message bus, auth provider, deployment target), boundary and ownership decisions (the explicit "no"s are as valuable as the "yes"es), deliberate deviations from the obvious path, constraints invisible in the code (compliance, partner contracts), and rejected alternatives whose rejection is not obvious.

When the decision came out of a discussion in the current session, say so and offer to record it. Do not write one silently.

## 2. Find the decision log

Look, in this order, for an existing log: `docs/decisions/`, `docs/adr/`, `doc/adr/`, `adr/`, or any directory whose files are named `NNNN-*.md` with a status in their frontmatter. Match whatever the repository already does: its directory, its numbering, its template (a `template.md` or `README.md` in that directory wins over this skill), and its language. If the repository writes its documents in a language other than English, write the ADR in that language.

If there is no log, create `docs/decisions/` lazily when writing the first record, and put the template from this skill beside it as `template.md` so later records match. Say that you created it.

## 3. Number and name

Scan the log for the highest number and add one. Numbers are four digits, start at 0001, are consecutive and are never reused. The file is `NNNN-kebab-title.md` where the title names the problem and the chosen solution, not the topic alone (`0004-codex-manifest-location.md`, not `0004-codex.md`).

## 4. Write the record

Use [template.md](template.md) unless the repository has its own. The shape is MADR minimal plus two additions:

- Frontmatter: `status` (`proposed`, `accepted`, `deprecated`, `superseded`), `date` (`YYYY-MM-DD`), `supersedes` (a list of file names, usually empty), `superseded-by` (`null` until it happens).
- A title that states the problem and the chosen solution.
- A **Y-statement** as a one-paragraph summary right under the title: "In the context of <use case>, facing <concern>, we decided for <option> and against <alternatives>, to achieve <quality>, accepting <downside>."
- **Context and problem**: the situation and what had to be decided. Link research notes or external evidence when they exist.
- **Considered options**: a numbered list, one line each, including the one chosen.
- **Decision**: "Option N." plus one or two sentences on why it beat the others. If the discussion produced a table of options with pros and cons, carry that table over here rather than rewriting it.
- **Consequences**: good, bad, the condition under which to revisit, and how the decision is enforced or checked (a tool, a test, a CI job, a review step). A decision nothing enforces drifts.

Write it short. A record most readers finish is worth more than a complete one nobody opens. Leave out sections that would only hold filler.

## 5. Keep it immutable

- Never edit the body of an accepted record. Fix typos only in the same change that introduced them.
- To change a decision, write a new record with the old one in `supersedes`, then set the old record's `status` to `superseded` and its `superseded-by` to the new file name. Only those two frontmatter fields change in the old file.
- A record that was only partly replaced still gets `superseded`; the new record says which parts of the old one remain in force.
- To retire a decision without a replacement, set `status` to `deprecated`.

## 6. Finish

- If the log has an index (a `README.md` table or similar), add the row and update the superseded row's status.
- If the repository has an overview document or contributor rules that state the decided convention, change them in the same commit as the record. The ADR explains why; those documents state what.
- Tell the user the file path, the status, and which documents you changed alongside it.
