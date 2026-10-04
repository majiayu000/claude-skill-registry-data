---
name: draft-pr
description: Writes a PR title and description to .workflow/<KEY>/pr.md from the branch's commits, the plan and the recorded verification. Use when opening a PR or asked for a PR description.
---

# draft-pr

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

This skill writes the description. Opening the PR is the user's call.

## Steps

1. **Assemble the inputs.** `pr context <KEY>`. One call returns the branch and
   base, the commits on it, the changed files, the critical zones, the plan's
   summary and open questions, the verification verdict with each command's exit
   code, and a `shape` telling you how much description this change earns.
   For a PR onto a validation branch: `pr context <KEY> --target homolog`.

2. **Check `_missing`.** If it lists `plan` or `verification`, that artifact does
   not exist. Say so in the description — do not write around the gap and do not
   claim a check that was never run.

3. **Write the title** in the repo's commit style (`commit convention` if you
   have not already). One line, imperative, specific enough that a reviewer
   scanning a list knows what this is.

4. **Write only the shape you were given.** `trivial` is a title and one
   sentence, no headings at all. `small` is What and Verification. Only `large`
   earns the full template, and even then a section with nothing to say is
   deleted rather than left as an empty heading.

   ```markdown
   ## What
   One or two sentences. What changes, and why now.

   ## Why
   The problem, with the ticket link. Skip if the title says it.

   ## How
   Only the decisions a reviewer cannot infer from the diff — a trade-off, an
   approach considered and dropped, a constraint that forced the shape.

   ## Verification
   The actual commands and their results, from `pr context`.

   ## Risk and rollback
   Critical zones touched, and how to undo this.

   ## Open questions
   From the plan. An empty section is better deleted than left blank.
   ```

5. **Check and save.** `pr check --file <path> --shape <shape> --key <KEY>`
   rejects empty sections, placeholders, unticked boxes and filler, and a PR
   whose plan still owes its handover. Then save to
   `.workflow/<KEY>/pr.md` and show it.

6. **Close the ticket** if the backlog is local: `task done <KEY>`. A real
   tracker owns its own state, and `wb` refuses there rather than recording a
   status only this checkout believes. Say the PR is open, not that it merged.

## Rules

- **Only claim what was verified.** `pr context` gives the real verdict and exit
  codes. If verification failed or was refused, the description says that. A PR
  claiming green tests that never ran is worse than one admitting they did not.
- **Reviewers read the diff, not a retelling of it.** Do not list every file.
  Explain the decisions, point at the risk.
- **Name the critical zones.** If the change touches billing, auth, user data or
  a migration, that belongs in the description, not discovered in review.
- **Name the amendments.** `amended` in `pr context` lists files added after the
  plan passed its audit. List each one with its reason under Risk, because a
  reviewer has to know that the plan widened mid-flight.
- **Carry the open questions across.** A question the plan could not answer does
  not disappear because the code is written.
- **Nothing beyond what is needed.** No restating the diff, no attribution
  footer, no "as requested", no unticked template box.
