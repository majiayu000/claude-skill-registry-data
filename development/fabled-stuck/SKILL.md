---
name: fabled-stuck
description: >-
  Escape a failure loop — when two or more attempts to fix the same problem have failed, stop
  patching and re-derive the diagnosis from raw evidence. Use this skill the moment a second fix
  attempt fails for the same symptom, when the user says "still broken", "still failing", "didn't
  work", "same error", "you're going in circles", "we've tried this already", or "I've tried
  everything", or when you notice yourself about to retry a variation of an approach that already
  failed — in debugging, failing builds or CI, config that won't take effect, or any
  repeated-failure loop. Not for the first attempt at a bug (that is ordinary hypothesis-driven
  debugging) and not for tasks that are hard but not looping.
effort: xhigh
---

# Fabled Stuck — Escape the Failure Loop

Two failed attempts at the same symptom is not bad luck — it is evidence about your diagnosis. The defining error of a failure loop is that every attempt shares an unexamined assumption, usually the diagnosis itself, and each new fix mutates the last one instead of questioning what they all have in common. This skill replaces "try harder" with a forced strategy change.

The rule that governs everything below: **your next action must be designed to learn, not to fix.** You earn the right to attempt another fix only after the diagnosis has been re-derived from evidence.

## The Protocol

Run the steps in order. Do the reasoning explicitly — in extended thinking if available, otherwise in an externalized scratchpad (a temporary file, or notes between tool calls). A failure loop is precisely the state in which unwritten reasoning re-treads itself.

### 1. Freeze

Stop editing. Do not try the fix you were about to try. If you have changes from failed attempts still in the working tree, decide now whether they stay or revert — a workspace layered with half-fixes makes every later observation ambiguous.

### 2. Inventory the failed attempts

Write down, one line per attempt: what it changed, what it assumed the problem was, and what actually happened (the exact observed result, not "it didn't work"). Recalling attempts loosely is how the same one gets retried with cosmetic variation.

### 3. Attack the shared assumption

Ask: what did every failed attempt assume in common? That shared assumption is the prime suspect — and it is usually the diagnosis, not the fixes. If all three attempts assumed the bug is in function X, the productive hypothesis is that it is not in function X.

### 4. Re-derive the diagnosis from raw evidence

Quarantine every prior theory and rebuild from observed facts only: the exact error text, the actual log lines, the real state of the system (read the file, print the value, check the running config — do not recall what it "should" be). Mark each item as _observed_ or _inferred_; the bug lives disproportionately in the inferred column. Re-reading evidence you have already read rarely helps — collect at least one observation you did not have before.

### 5. Widen the hypothesis space

Generate at least two hypotheses that are _not_ refinements of the dead theory. Force variety across these axes:

- **Different layer** — not the code but the environment, config, dependency version, cached artifact, or data.
- **Different location** — the caller, not the callee; the test or repro itself, not the code under test.
- **Different count** — two interacting bugs, so every single-bug fix "mysteriously" half-works.
- **Different signal** — the error message is misleading or downstream of the real failure.
- **Different premise** — the thing you are treating as verified ("the fix is deployed", "this code path runs") never happened. Verify the premise directly.

For the full toolkit — decomposition changes, inversion, minimal instances, representation changes — load `../fabled/references/reasoning-moves.md` (this skill's sibling in the plugin); its "Managing the search" section is the general form of this protocol.

### 6. Probe, then fix

Design the cheapest experiment that _discriminates between hypotheses_ — a minimal repro, a bisect, a print of the disputed state — and run it before any fix. Change one thing at a time; a shotgun fix that works teaches nothing and one that fails misleads. Only when a hypothesis survives a probe do you attempt the fix it implies.

### 7. Exit or escalate

**Exit criteria — both required:**

- The fix is verified against the original failing case (rerun the exact command / repro that defined "broken", not a proxy).
- You can explain why the failed attempts failed. A fix you cannot reconcile with the earlier failures may be masking the symptom, not resolving the cause.

**Escalate honestly:** if two full passes of this protocol produce no surviving hypothesis, stop burning the user's budget. Report what is ruled out (with the evidence), what remains plausible, and the single best next probe — that is a deliverable, not a failure. If the `ceh-advisor` plugin is loaded, this is exactly its consultation moment.

## Anti-patterns in failure loops (spot these in yourself)

1. **Thrash loop** — retrying the last fix with cosmetic variation and no new evidence.
2. **Theory lock-in** — treating the original diagnosis as fact and only ever varying the fix.
3. **Shotgun fixing** — changing several things at once, so neither success nor failure is informative.
4. **Evidence recycling** — re-reading the same error output expecting new information instead of collecting a new observation.
5. **Fix-first probing** — every action attempts a repair; none is designed to discriminate between hypotheses.
6. **Success by silence** — declaring victory because the error changed or stopped appearing, without rerunning the original failing case.
7. **Sunk-cost depth** — investing harder in the current theory because of what it already cost.
8. **Silent restart** — throwing everything away and starting over without recording why each dead end died; untracked dead ends get re-entered.

## Relationship to `fabled`

This skill is the `fabled` discipline applied at the one moment the core loop cannot rescue itself: mid-loop, the model that most needs to change strategy is the least likely to stop and load a toolkit. The trigger does the work — once engaged, steps 4–6 are `fabled`'s "do the work at full depth" and "verify" stages pointed at your own failed attempts. For a hard debugging session beyond the loop itself, also invoke `ceh-fabled:fabled` and its technical-rigor reference (`../fabled/references/technical-rigor.md`).
