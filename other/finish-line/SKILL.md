---
name: finish-line
description: "Use before calling multi-part or risky work done, committing a multi-file change, or opening a PR, and when reviewing someone's work. Not mid-task or for one-line edits."
user-invocable: false
---
# Finish line
Job: Decide whether work is really done, by checks that can't hide each other.
Takes: a baseline, the `Asked` list or other intent source, the work.   Gives: a report with the ledger and, for code, two separate finding sets.
Team moves: check, dispatch

This check is read-only unless you started it yourself on your own work. Write the result as a report, in the shape from the file `artifacts.md` in the skill `house-rules`.

Rules and intent run as separate lenses because either can pass while the other fails: tidy but wrong, or right but messy. Blending them lets one hide the other.

## Steps

1. **Ledger, always.** List every requested item, constraint, correction and promised follow-up, from `Asked` or the conversation. Mark each met, partly or not, with labelled evidence. Prefer the real path: launch it, exercise the feature, open the file. A claim you relayed stays `[reported]`, and a mock earns `[simulated]`. State a sample or keyword scan as such under `Scope`. An item may stay open only if it is blocked, needs a gate, or is out of scope, tagged with that reason. On your own work, fix any in-scope, reversible, unblocked item, or send it to a worker, before the report; in a review someone else asked for, it is a finding.

1b. **Visible surface.** Web UI, TUI, desktop, boot or video work is not done until fresh screenshots or a recording are shared through the prefs `show:` channel, else the host's file send, linked and labelled `[observed]`. Promised media are ledger lines.

   Non-code work stops here, and so does a single-file, low-risk change.
2. **Fix the baseline.** Use what the user named, else the merge-base with the default branch, or HEAD when you're on that branch. Diff against it including uncommitted work, and list the commits. Confirm the ref resolves and the diff has content before spending more.
3. **Rules lens.** Sources: every file that documents conventions, plus the file `code-smells.md` in this skill. Smells are tentative, documented rules override them, and you skip whatever tooling already enforces. Each finding cites the rule or smell with the code, and separates breaches from judgement calls.
4. **Intent lens.** Sources, in order: the user's request if the work happened here, issues referenced in commits, a path you were passed, a matching chart. If none exists, skip this lens and say so. Findings cover missing requirements, unrequested behaviour and wrong implementation, each citing the requirement.
5. **Run the lenses apart.** Dispatch two fresh scouts in parallel, one lens each, neither seeing the other's output. For a diff under about 100 lines, or at solo level, run them inline, one after the other. Keep each under about 400 words.
6. **Present.** Show the ledger, then each lens separately and unranked. Close with counts and the worst finding per lens. Give no overall score.
7. **Act by who asked.**
   - The user asked for this review: stop at the report.
   - You started it on your own work: fix clear in-scope defects, re-check, and report those fixes plus any judgement calls left.
   - The check found the work wrong on its merits: fix the cause, not the wording.

## Checker mode

Run this after dispatched work, in the role of checker. The checker comes from the check ladder in the file `levels.md` in the skill `house-rules`. Record the rung in the report's `independent` field.

For a run-proven review, follow the file `break-lens.md` in this skill.

1. Take the worker's report as claims. Everything in it is `[reported]`.
2. Re-run its key checks yourself: the commands under `Evidence` and the card's `Accept` checks. Each one you re-run becomes `[observed]`. One you couldn't run stays `[reported]`, with the reason.
3. Run steps 1 to 6, with the worker's change as the diff. Add `## Rules findings` and `## Intent findings` to the report, kept separate and unranked, with no overall score. Each finding is one line: `R1 [blocker|should|nit] file:line claim. Fix: ...`, with `R` ids for rules and `I` ids for intent. Another path, a rare case or a small cost is a nit, whatever its label, unless it loses data, opens a security hole or skips a gate.
4. Give the verdict in the report's `status` and `Result`. You report what you find and leave the fixing to the worker.
   - Approve when there is no breach, nothing missing, and every key check was re-run.
   - If a read-only run kept you from a key check, mark the report `partial` and name the check, so the lead runs it before landing.
   - Otherwise say exactly what must change.

Round 2 sends the checker only the ledger of old ids plus `git diff <last-checked-sha>`; it marks each id resolved or open and adds new ids for new findings only. A checker that timed out or sent no report has not approved, and if `git diff --shortstat` grew since the last round, cut it back before re-checking. After two rounds of changes the work goes to the user. Judgement calls go in the report and don't hold back an approval. Check another agent's work only. If the work is your own, the most this can record is `independent: self`.

## Done when

- Every requested item, constraint, correction and promised follow-up has a ledger line with met, partly or not, and a labelled evidence line.
- Each unfinished item is named as blocked, gated or out of scope, and nothing in-scope, reversible and unblocked is left open, except as a finding in a review someone else asked for.
- Visible-surface work has fresh screenshots or a recording shared and linked.
- For code past step 1: the baseline resolved, the diff had content, and both lens results are present, or the intent lens is reported as skipped with no source found.
- Findings are separate and unranked, with counts and the worst per lens.
- A review the user asked for changed no files.
- Self-started: clear in-scope defects are fixed and re-checked.
- Checker mode: `independent` is filled, each key check is re-run or marked `[reported]` with why, and the verdict is in the report.
