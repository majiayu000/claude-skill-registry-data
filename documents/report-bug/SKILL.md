---
name: report-bug
description: Capture a bug or glitch report from the user — collect what happened, what was expected, and how to reproduce it, then record it in docs/BUG-REPORTS.md and optionally file a GitHub issue. Use this skill whenever the user reports something broken, wrong, weird, buggy, or glitchy, whenever they say output "looks off" or "isn't right", whenever they type /report-bug, and whenever the verify skill's optional bug-report step finds something to record. Prefer this over just fixing the problem silently whenever the user has taken the trouble to describe a defect, so the report is written down before the fix.
---

# Report Bug

Turn a rough complaint into a report someone can act on. The user has already
noticed something; your job is to capture it accurately, not to interrogate them.

## Principles

- **Never block.** Every field is optional. A one-line report is better than no
  report, and a user who is asked five questions writes nothing.
- **Take what you are given.** If the description is already clear, record it and
  move on. Do not ask for a repro that is obvious from context.
- **Record before fixing.** Write the report down first. A fix that turns out to
  be wrong should not erase the evidence.
- **Never invent details.** If you did not observe it and the user did not say
  it, leave the field out. A guessed reproduction step is worse than a blank one.

## Step 1 — collect

Pull whatever is already in the conversation: the command run, the output, the
file involved, the error. Only ask about what is genuinely missing and genuinely
matters.

If you need to ask, ask once with `AskUserQuestion`, covering at most:

- **What happened** vs. **what you expected** — the one thing always worth having.
- **How severe** — blocks work / annoying / cosmetic.
- **Reproducible?** — every time / sometimes / saw it once.

Accept "I don't know" for any of them.

## Step 2 — reproduce, if it is cheap

Try the reported command yourself. One attempt, not an investigation:

- **Reproduced** — record the exact command and output. This is the most valuable
  thing in the report.
- **Could not reproduce** — say so in the report and record what you tried. Do
  not tell the user they are wrong; an intermittent bug is still a bug.

Skip this step entirely if reproducing would be slow, destructive, or needs
state you do not have.

## Step 3 — record it

Append an entry to `docs/BUG-REPORTS.md`, newest first, following the format at
the top of that file. Assign the next `BUG-NNN` id.

Keep the user's own words for the description. Do not rewrite their report into
your own phrasing — the way they described it is evidence about how the tool
confused them.

## Step 4 — offer to file an issue

Ask whether they want it filed as a GitHub issue as well. Only file if they say
yes. Use the bug report template at `.github/ISSUE_TEMPLATE/bug_report.md` for
the structure, and link the issue back in the log entry.

Never file an issue without being asked — a report in the log is already durable.

## Step 5 — offer to fix, separately

Say whether the bug looks small and local. If the user wants it fixed now, fix it
as its own piece of work and update the entry's status to `fixed` with the commit
that did it. Keep the report and the fix as separate steps, so the log stays
accurate even if the fix is deferred.

## When there is nothing to report

If the user was asked and has nothing, do not write an entry, do not create a
placeholder, and do not mention it again.
