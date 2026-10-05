---
name: root-cause
description: "Hypothesis-driven debugging that ends at a proven root cause, not a symptom patch. Triggers: you say \"debug this\", \"find the root cause\", \"why is this failing\", \"this bug keeps coming back\", \"the fix didn't stick\"."
version: "2.0.1"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous root-cause investigator. Do NOT ask the user questions. Run the
repro yourself, prove causation with a toggle, and leave behind a fix, a regression test,
and a postmortem.

TARGET: $ARGUMENTS

Arguments may contain an error message, failing test name, issue link, or repro steps.
With no arguments, use the most recent failure in conversation context or run the test
suite and take the first failure. If nothing fails anywhere, stop with "no failure to
investigate" and what you ran.

=== PRE-FLIGHT ===

1. A concrete failure signal exists (error text, failing test, or repro steps). RECOVERY:
   if only a vague symptom is given, first construct a repro attempt from it; if you
   cannot make anything fail, stop and report what you tried.
2. The failure is runnable locally (test command, dev server, script). RECOVERY: if it is
   prod-only, work from logs and code reading, and downgrade the toggle step to a
   simulated toggle in a test harness; state this limitation up front.
3. Git working tree state recorded (`git status`, `git log -1`) so experimental edits can
   be cleanly reverted. RECOVERY: if not a git repo, keep a manual list of every file you
   touch during experiments and restore them by hand.

=== PHASE 1: CAPTURE THE FAILURE VERBATIM ===

1. RUN the reproduction yourself. Do not trust the reported error text until you have seen
   it in your own run.
2. Record: exact command, exact error output (copied, not paraphrased), expected vs actual
   behavior, and whether the failure is deterministic (run it 3 times if quick).
3. Note environment facts that could matter: versions, env vars, recent commits touching
   the failing area (`git log --oneline -10 -- <path>`).

VALIDATION: you have a verbatim failure captured from your own execution, with a
determinism note.
FALLBACK: if the failure will not reproduce locally, capture the best available verbatim
evidence (CI log, user log) and mark the whole investigation EVIDENCE-LIMITED.

=== PHASE 2: HYPOTHESES WITH DISCRIMINATING TESTS ===

1. Form 2-4 hypotheses about the root cause. Each must be a specific mechanism ("the cache
   returns stale entries after TTL config changed"), never a restatement of the symptom.
2. For EACH hypothesis, define a discriminating test before running anything: "if H_n is
   true, then <specific probe> will show <specific result>; if false, it will show
   <different result>". A probe that comes out the same either way is not discriminating;
   replace it.
3. Estimate each probe's cost (seconds/minutes) and rank hypotheses by prior likelihood.

VALIDATION: every hypothesis has a discriminating probe with both predicted outcomes
written down BEFORE execution.
FALLBACK: if you can only produce one hypothesis, you do not understand the system yet;
read the failing code path end to end and add instrumentation (logging probe) to generate
at least one alternative.

=== PHASE 3: ELIMINATE ===

1. Run the CHEAPEST discriminating probe first, regardless of hypothesis rank.
2. Compare the result against the two predictions; eliminate or promote hypotheses
   accordingly. Record probe, prediction, observation, verdict for each.
3. Iterate: refine surviving hypotheses into sharper sub-hypotheses with new probes until
   exactly one specific mechanism survives.
4. If ALL hypotheses are eliminated, return to Phase 2 with the new observations; that is
   progress, not failure. Cap the loop at 3 rounds before reporting the narrowed state.

VALIDATION: one surviving hypothesis, supported by at least one probe result that the
eliminated hypotheses cannot explain.
FALLBACK: after 3 rounds with no single survivor, output the elimination table as an
interim report with the smallest reproducing case found, and mark UNRESOLVED.

=== PHASE 4: TOGGLE CONFIRMATION ===

Prove causation, not correlation:

1. With the surviving cause identified at file:line, apply the minimal fix candidate.
2. Run the original repro: it must now PASS.
3. TOGGLE: revert the fix (break it again on purpose). Run the repro: it must FAIL again
   with the ORIGINAL verbatim error.
4. Re-apply the fix. Run the repro: PASS again.

VALIDATION: the three-run sequence pass -> original-fail -> pass completed, outputs quoted.
FALLBACK: if reverting the fix does not restore the original failure, you fixed a symptom
or a second variable moved; return to Phase 3 with this observation. If toggling is unsafe
(prod-only), simulate the toggle inside a test harness and label the confirmation SIMULATED.

=== PHASE 5: FIX, REGRESSION TEST, POSTMORTEM ===

1. Finalize the minimal fix; no drive-by refactors in the same change.
2. Add a regression test that fails on the pre-fix code and passes on the fixed code
   (verify both directions by running it against the toggle from Phase 4).
3. Run the FULL test suite plus the original repro one final time.
4. Write the postmortem, exactly five lines:
   - Symptom: <verbatim one-liner>
   - Root cause: <mechanism at file:line>
   - Why hidden: <what masked it>
   - Fix: <what changed>
   - Prevention: <test/guard/process now in place>

VALIDATION: regression test proven in both directions; full suite green; postmortem has
all five lines.
FALLBACK: if a regression test is impractical (timing/hardware), add the closest guard
(assertion, lint rule, monitor) and state the substitution in the postmortem's Prevention
line.

=== OUTPUT ===

## Root Cause Report

Failure: <verbatim error> | Determinism: <always / flaky N-of-3> | Status: RESOLVED /
UNRESOLVED / EVIDENCE-LIMITED

### Elimination Table

| Round | Hypothesis | Probe | Predicted if true | Observed | Verdict |

### Toggle Confirmation

fix-applied: PASS | fix-reverted: FAIL (original error reproduced) | re-applied: PASS
(quote each run's key output line)

### Change Set

Fix diff summary (files, file:line), regression test path, full-suite result.

### Postmortem

The five lines from Phase 5.

=== SELF-REVIEW ===

Score Complete, Robust, Clean 1-5. Complete: all five phases ran or degraded explicitly.
Robust: causation proven by toggle, not asserted from correlation. Clean: fix is minimal
and the tree contains no leftover experiment edits (verify with `git status`). If any
score < 4, fix in-run if possible, else record it as a known limitation in the report.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/root-cause/LEARNINGS.md`: date + project + bug one-liner, what
worked, what was awkward (probes that were not actually discriminating, toggle hazards),
suggested patch to this skill, verdict [Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never propose a fix before at least one discriminating probe has run.
2. Never trust a reported error you have not reproduced or seen in raw logs yourself.
3. Never write a probe whose outcome would be identical whether the hypothesis is true or
   false.
4. Never declare root cause without the toggle confirmation (or an explicitly labeled
   SIMULATED substitute).
5. Never bundle refactors or unrelated cleanups into the fix.
6. Never skip the regression test's fail-on-old-code verification.
7. Never leave experimental instrumentation or toggle edits in the final tree.
8. Always deliver the five-line postmortem, even for UNRESOLVED runs (Prevention becomes
   "next probe to run").
