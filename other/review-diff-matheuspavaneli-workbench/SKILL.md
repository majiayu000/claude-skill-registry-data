---
name: review-diff
description: Reviews the current diff against the repo's quality preset, reporting findings as file:line with a severity. Use to self-review before a PR, or to review uncommitted or staged changes.
---

# review-diff

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

## Steps

1. **Get the computed facts.** `review context` (add `--staged` for the staged
   diff). It reports the preset, every changed file, the critical zones touched,
   the sources that changed with no test alongside, and the gates that apply.

2. **Read the diff itself**, then read the surrounding code. A diff shows what
   changed, not what it broke. For anything that changes a shared contract, ask
   the index who calls it:
   `../../shared/code-search.md`.

3. **Settle the mechanical gates first.** `review gates` (add `--key <KEY>` so
   the bug-fix regression rule knows the ticket type). It reads the added lines
   and reports secrets, swallowed errors and added dependencies as `file:line`
   findings. Exit 7 means it found some; report them, do not re-derive them.
   A dependency finding is a question to answer, not a defect: say who owns it
   and why nothing already in the repo does the job.

4. **Check the rest of the gates yourself.** Every gate `review context` printed
   that `review gates` did not settle is a question with a yes or no answer for
   this diff. The floor is not negotiable at any preset: unit test for changed
   logic, regression test with a bug fix, no swallowed error, no secret, a
   stated rollback.

   `review context` also lists files the plan gained after its audit
   (`plan amended after its audit`). The first audit never saw those files, so
   read them as closely as a critical zone.

5. **Go deeper in critical zones.** Billing, auth, user data, migrations and
   secrets are held to a higher standard than the preset otherwise sets. In
   those files, read every changed line and its error path.

6. **Write the findings**, most severe first, to `.workflow/<KEY>/review.md`:

   ```
   - high  `src/checkout.py:42` — `charge = create_charge(total)`
     Coupon is validated after the charge. An expired coupon charges, then errors.
   ```

   Severity: **high** — wrong behaviour, data loss, or a security hole.
   **medium** — will break under a plausible input or state. **low** — real but
   contained. Skip formatting and taste unless it changes meaning.
   Then `cite check .workflow/<KEY>/review.md --worktree`, and report only once
   it passes: a finding whose line is not there is withdrawn, not reworded.

7. **Say when it is clean.** "No findings" is a result. Do not manufacture a
   finding to look thorough.

## Rules

- **Every finding cites `file:line` and quotes the line.** Read the line to
  quote it; do not quote from an index or from memory.
- **State the failure, not the preference.** A finding needs concrete inputs or
  state that produce a wrong outcome. "Consider extracting this" is not a
  finding.
- **The missing-test list is a heuristic**, not a verdict. Check each one: a
  test may cover it under another name.
- **Do not fix while reviewing.** Report; let the author decide.
