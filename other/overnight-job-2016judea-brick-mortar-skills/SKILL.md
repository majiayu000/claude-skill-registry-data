---
name: overnight-job
description: Run a batch of work headless/overnight while you are away and cannot approve tool calls. Use when you say "work on this overnight", "I won't be around to approve", "headless", or hand off a multi-task list to finish unattended. Covers the pre-flight permission check, structuring work to survive without approvals, paid-API budget guards, and leaving a morning summary.
---

# Overnight Job (headless, unattended)

Running a task list while the user is asleep / away and **cannot approve tool calls**. The whole game is:
do not get blocked on an approval prompt, do not overspend, and leave everything committed + summarized
for the morning.

## #1 failure mode (learned the hard way): approval friction kills the run

If the session is in normal permission mode, **every Bash call waits for approval** — and an absent user
means it stalls or gets rejected, and nothing gets done. Before relying on autonomy:

1. **Confirm a non-blocking permission mode is set.** Ask the user to leave the session in
   **bypass-permissions** (everything runs) or at least **accept-edits** (Writes/Edits auto-run, Bash still
   prompts). If they can't, see "degraded mode" below. Say this explicitly *before* they leave — don't discover
   it mid-run when they're already gone.
2. **If mode is uncertain, assume Bash may be blocked.** Writes/Edits often pass in accept-edits mode; Bash
   often doesn't. Plan accordingly.

## Structure the work to survive (minimize tool calls)

- **No probe-run-probe loops.** Don't make 5 small Bash calls to inspect-then-act. Write **robust,
  self-contained scripts** that handle the unknowns internally (defensive parsing, fallbacks) and run **once**.
  Every incremental "let me just check X" is an approval you may not get.
- **Batch ruthlessly.** Collapse "run the thing" + "commit" into a *single* Bash invocation at the end
  (`python … && git add … && git commit …`). Aim for the fewest possible Bash calls for the whole job.
- **Front-load the no-Bash deliverables.** Anything that's pure `Write`/`Edit` (docs, skills, code, specs)
  is the safest to complete — do those first; they land even if Bash is blocked.
- **Make every artifact ready-to-run.** If a step can't execute (blocked Bash), leave the script built and
  note the exact command in the summary so it's one approved command away in the morning.

## Paid-API budget guards (don't overspend unattended)

- Get an **explicit cap** before running (e.g. "~$20 of the data-API trial").
- **Usage often isn't in response headers** (many data APIs expose none) — govern by a hard **record/operation
  count** with a conservative per-unit cost estimate. Prefer free/cheap modes (e.g. `count:true`) for sizing;
  cap the expensive record pulls.
- Bake the cap **into the script** (a `--max-records` hard stop), not just into your intentions.

## Run discipline

- Use **TodoWrite** to track the list; keep one item in progress.
- Commit in logical chunks (or one final commit) with clear messages; never leave uncommitted work that a
  context reset could lose. Branch first if working on `main` is undesirable.
- **Verify before claiming done** — render the PDF and eyeball a page, run the script and read output. No
  "should work" — show evidence (a re-rendered page, a printed count).
- Respect the project's standing rules (CLAUDE.md).

## Degraded mode (Bash is blocked and the user is gone)

Do the maximum that needs only `Write`/`Edit`: write the code/scripts, the docs, the specs, the skills.
Leave a summary listing exactly which Bash commands remain (run scripts, commit) so the morning is a few
approved commands, not a rebuild. Don't spin firing Bash calls that just get rejected.

## End every overnight run with a morning summary

A short written recap (chat message + optionally a file): what got done, what's committed, what's left and
the exact command to finish it, any budget spent, and the recommended next move. The user reads this first thing —
make it the single source of truth for where the work stands.

## Reference run (the shape, anonymised)

One overnight run built a render engine, refactored two generators, wrote a decision brief and
a county-wide record finder with a hard `--max-records` cap. The approval friction surfaced
mid-run: that is the lesson that became rule #1 above.

## Also

- Long jobs on a laptop die when it sleeps; on macOS wrap them in `caffeinate -dims <cmd>`.
- Unattended + paid API: write the spend so far into the morning summary even when it is $0.
