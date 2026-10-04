---
name: write-handover
description: Writes the non-technical note for a support ticket - symptom, cause, what changes, and numbered steps for QA - to .workflow/<KEY>/handover.md. Use for support, bug or incident tickets that a QA lead or the person who raised them has to read.
---

# write-handover

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

The audience is not engineering. A QA lead has to validate this without reading
the diff, and whoever raised the ticket has to understand what happened without
knowing the codebase exists.

## Steps

1. **Read the ticket and the plan.** `.workflow/<KEY>/triage.json` for what was
   reported and in whose words; `sdd get <KEY> --section summary` and
   `--section evidence` for what was actually wrong.

2. **Fill the `handover` block in `sdd.json`:**

   | Field | |
   |---|---|
   | `symptom_plain` | what the reporter saw, in their words |
   | `cause_plain` | why it happened, one sentence a non-engineer can repeat |
   | `fix_plain` | what changes for them |
   | `scope` | who was affected, since when, how many |
   | `workaround` | what to do until it ships, or `none` |
   | `qa_steps` | numbered steps, ending in the expected result |
   | `release_note` | one line, if the repo keeps a changelog |

3. **Write `qa_steps` as something a person can follow.** Start from a state
   they can reach, name the exact input, and end with what they should see. "Test
   the coupon flow" is not a step. "Apply coupon SUMMER24, expired yesterday →
   the order is refused with a validation message and no charge appears in
   Stripe" is.

4. **Render it.** `sdd handover <KEY>` writes `.workflow/<KEY>/handover.md` for
   pasting into the ticket.

5. **Say what is not covered.** If the fix addresses the reported symptom but not
   a related case the reporter may hit, that belongs here, not discovered later.

## Rules

- **No jargon, no paths, no function names, no commit hashes.** If it cannot be
  said without them, it is not understood well enough to hand over.
- **Do not claim a cause you could not demonstrate.** "Under investigation" is a
  legitimate handover; a confident wrong cause is not.
- **The scope is a fact, not a comfort.** If you do not know how many users were
  affected, say that rather than implying it was few.
- **Nothing beyond what is needed.** Five short answers and the steps. No
  restating the ticket back, no apology, no summary of the summary.
