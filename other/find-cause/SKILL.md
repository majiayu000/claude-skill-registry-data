---
name: find-cause
description: Use when existing behavior is reported wrong (bug, error, crash, regression, broken output, slowdown) and no evidence yet shows one causal line plus a mechanism predicting the symptom. Not when a diagnostic's file, line and symbol match the source, when the stated cause checks out, or for a feature complaint.
argument-hint: <symptom, failing command or error>
---
# Find cause

a. **Locate.** Until the cause is proven this skill outranks `spec` and `build`; a read-only planning turn writes the plan per `../spec/references/task-list.md`, reproduction test as Task 1. Run `node "${CLAUDE_SKILL_DIR}/../../lib/scratch-exclude.mjs"`; no symbol: `exo:locate-code`.
b. **Investigate.** Proven needs a causal line and a mechanism predicting it or holding in the source: write `Status: proven`; else dispatch `exo:solve-hard` from `investigator-prompt.md`.
c. **Fix.** Settle where it commits per `../build/references/workspace.md`, else copy the handoff to `.exo/debug/`. Dispatch `general-purpose` on `sonnet` from `fixer-prompt.md`; resume `failed` via SendMessage.
d. **Report.** Read only status lines and Report's fields. After compaction, re-run `Repro`.

1. **Reproduce.** One command reproduces it, else evidence, no fix.
   - Send long output to `<scratch>/debug-repro.log`, `<scratch>` from `node "${CLAUDE_SKILL_DIR}/../../lib/scratch-path.mjs" debug`; read with `tail -n 40`.
   - No infrastructure: reproduce unstubbed at the first owning function below; no sign-off.
2. **Instrument.** Keep two hypotheses; observe once at their first divergence.
3. **Isolate.** Remove inputs or branches until one more clears it; two rounds standing end it.
4. **Predict, then fix.** State the causal line, changed output and why; change only that; drop old patches.
5. **Prove.** Re-run the repro, isolated case and suite per Step 1. Return to Step 1 when the repair reaches a second owner or resists one reading.
6. **Retain project knowledge.** Per the table.
7. **Fresh eyes.** No PR review: run `node "${CLAUDE_SKILL_DIR}/../../lib/size-facts.mjs"`; when it prints `changed files` above 2 or `dependency-added yes`, or the fix crosses a public signature, persisted format or security boundary, run `code-review` at `node "${CLAUDE_SKILL_DIR}/../verify/scripts/pick-reviewer.mjs" --effort`'s level (`skip`, `low` or `medium`); fix under Step 5. End on `node "${CLAUDE_SKILL_DIR}/../route-skills/scripts/next-stage.mjs" --after find-cause --artifact none`'s output when edits to build remain; else end on `ship`.
   - Past `exo: context`: keep the letters, hand on via a fresh delegate; stage- or workflow-invoked: ask nothing, return to it.

## References

| File | Read it when |
|---|---|
| `references/handoff.md` | b, c |
| `../build/references/workspace.md` | c |
| `investigator-prompt.md` | b |
| `fixer-prompt.md` | c |
| `../build/references/performance.md` | Speed |
| `references/profiling.md` | Trace |
| `../build/references/critique.md` | No review |
| `../build/references/security.md` | When its first line applies. |
| `../build/references/data-migration.md` | When its first line applies. |
| `../build/references/test-design.md` | When its first line applies. |
| `../build/references/project-knowledge.md` | 6 |

Report: the mechanism, up to ten proof lines, log path, test and fix SHAs; unproven: `Repro`, `Expected`, `Actual`, `Hypotheses`.
