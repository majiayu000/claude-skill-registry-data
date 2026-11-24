---
name: root-cause-hunt
description: "Use when a first fix failed, the cause isn't obvious, a failure is intermittent, or something got slower. Skip obvious one-liners."
user-invocable: false
---
# Root cause hunt
Job: Replace guesses with evidence until the confirmed cause is fixed.
Takes: a symptom.   Gives: a fix, a regression test or a stated reason for none, and the confirmed cause.
Team moves: dispatch, isolate, race, remember

Run the six stages in order. Skip one only with a reason you state.

## Steps

1. **Signal.** Build one runnable signal before any theory, climbing the rungs in the file `signal-ladder.md` in this skill. It is ready when it:
   - has already run, as one command
   - hits the real path
   - asserts the user's exact symptom
   - gives the same answer each run
   - takes seconds and runs unattended

   Hold every theory until that command exists. If no rung works, stop, list what you tried, and ask for one of: environment access, a redacted capture, or permission for temporary production instrumentation.
2. **Confirm and shrink.** Check that the signal shows the user's failure, repeatably, and not a neighbouring one. Record the exact symptom. Then remove one input, caller, config item or step at a time, re-running after each, until all that remains is needed.
3. **Rank hypotheses.** Write three to five, ranked, before testing any. Each predicts what a specific change does: `The retry reuses a closed connection. Forcing the first attempt to fail will fail every run.` Sharpen or drop any that predicts nothing. Share the ranking and carry on, since the user can often rule some out.
4. **Probe.** One probe tests one prediction by changing one variable. Prefer a debugger. Otherwise add targeted logs where hypotheses diverge, each tagged with one unique marker such as `[hunt-7f3]` so a single search finds them all. Skip blanket logging. For a slowdown, measure a baseline and bisect, because logs usually mislead there.
5. **Test, then fix.** Add the regression test before the fix, at a seam that recreates how the failure really reaches callers. A shallower test gives false confidence. A missing seam is a finding: use the skill `module-depth`, and state the gap. Turn the minimal case into the failing test and see it fail. If you forced the failure by mutating code or data, diff against a clean copy so the mutation can't reach the fix. Fix, see it pass, and re-run the signal.
6. **Close.** Confirm the original failure is gone. Confirm the test passes or the gap is documented. Remove temporary logs and harnesses. State the confirmed hypothesis in the commit message.

## Captures

Redact everything you capture or quote. Keep credentials in environment variables and quote capture lines sparingly. If redaction blocks the diagnosis, say so.

## In a team

- Parallel work starts only after the signal exists. Put the signal command in every brief, so each entry proves itself the same way.
- Two or more independent hypotheses: dispatch isolated probes, one hypothesis each.
- A known cause with several fix approaches: race them. The user keeps one entry, and it then goes through the route `race`.
- A probe's result is `[reported]` until you re-run the signal against it yourself.
- Pin the confirmed trap at its location with the remember move.
- At solo level, probe in rank order. A race there is one attempt: say no race ran.

## Done when

- The signal command is quoted, and you saw it fail before the fix and pass after it, `[observed]`.
- The recorded symptom is the user's, and the fix addresses that symptom.
- Hypotheses were written before the first probe, and the confirmed one is named.
- A regression test at a real seam was seen failing then passing, or the report states why there is none.
- A search for the temporary marker finds nothing, and every harness is gone.
- The commit message states the confirmed hypothesis.
- Each skipped stage has its reason stated, and every quoted capture is redacted.
