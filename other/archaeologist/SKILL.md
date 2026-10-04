---
name: archaeologist
description: Use when changing unusual or defensive code, mature APIs, dependencies, or architecture, or estimating a migration where Git history may reveal hidden constraints.
---

# Archaeologist

> Your codebase has a past. Read the part that matters.

Use history to answer a current decision, not to produce a chronology. Treat it as evidence about constraints and prior attempts, never as authority over current requirements.

## Frame the investigation

Before recommending a material change:

1. State the decision history could change: remove a guard, preserve compatibility, widen a migration, or revise an estimate.
2. Identify the smallest relevant surface: symbols, lines, files, tests, dependencies, and analogs.
3. Ask one or two concrete questions. Prefer “What failure caused this retry guard?” over “What is the history of this file?”
4. Check whether useful history exists. If it is shallow, missing, or inaccessible, report this and continue from current evidence without inventing a past.

Do not invoke a history review for a trivial edit whose behavior and intent are directly established.

## Follow the evidence trail

When history is available, run the narrowest query that can answer the question before making the recommendation.

1. **Find the live surface.** Search code and tests for the symbol, behavior, error text, dependency names, and analogs.
2. **Locate origin and change points.** Choose the query that matches the question:

   ```sh
   git log --oneline -- path/to/file
   git log -S'ExactToken' --oneline --all -- path/to/area
   git log -G'RelevantPattern' --oneline --all -- path/to/area
   git blame -L START,END -- path/to/file
   ```

   Add `--follow` for a likely single-file rename. Use blame only as a pointer to a commit, never as proof of intent.
3. **Read only decisive commits.** Inspect the patch, message, changed-file list, parent when needed, and tests introduced with the behavior:

   ```sh
   git show --stat COMMIT
   git show COMMIT -- path/to/code path/to/tests
   ```

   Check what invariant a regression test encodes rather than merely noting that a test exists.
4. **Check reversals and analogs when relevant.** Inspect reverts together with the commits they revert. For a migration or estimate, inspect several genuinely similar changes and note compatibility work, rollout, migrations, tests, and follow-up fixes.

Expand only while a decision-relevant question remains unresolved. Stop when another history query is unlikely to change the decision; avoid exhaustive logs, author profiles, and unrelated chronology.

Stay read-only throughout the investigation. Do not rewrite history, restore files, or discard working-tree changes.

## Calibrate the conclusion

Prefer an invariant encoded by a regression test over an unsupported commit-message claim, and a commit message over guessing from a patch or blame. Verify that a historical constraint still applies to the current environment before preserving it.

Do not infer that an approach failed merely because the code later changed. Do not treat a repeated pattern as a mandatory convention. Never claim that history proves author intent, production impact, or effort without direct support.

If history materially affects the work, use this compact handoff:

```text
Evidence: <directly observed commit, diff, test, revert, or issue>
Inference: <explanation derived from that evidence>
Decision impact: <how the current proposal changes>
Unknown: <material question history cannot answer>
```

Otherwise report only: “No material historical evidence found.” Do not pad the handoff.

For estimates, present a range and name historically observed scope drivers. Treat diff size and elapsed commit dates as weak proxies, never as a precise schedule or effort measurement.
