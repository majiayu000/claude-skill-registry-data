---
name: nursery
description: Run the Nursery-lite qualification scenarios and triage failures. Use when the user asks to run evals, qualify a change, check scenario health, or says /nursery. Args may name a scenario or test family.
---

# /nursery — run and triage qualification scenarios

1. Run the suite (mock mode — never pass `--live` unless the user explicitly asks and
   confirms they have local credentials):
   - All: `uv run koa-nursery --scenarios evals/scenarios --report qualification-report.json`
   - One scenario: add `--only <name>`; one family: add `--family <family>`
2. If everything passes, report the summary line and stop.
3. On failure, read `qualification-report.json` and for each failing scenario report:
   - the scenario name and its **test family** (positive/negative/ablation/poisoning/regression)
   - each failing grader with its `detail` string
   - the most likely cause, distinguishing:
     - **workflow defect** (deterministic checks wrong) → look in `src/koa/workflows/`
     - **scenario/mock drift** (mock script no longer matches workflow steps;
       `MockScriptExhausted` errors) → fix the scenario's `mock_script`
     - **grader misconfiguration** → check grader params against `src/koa/nursery/graders.py`
4. Propose the single next debugging step (a file to inspect or a one-scenario rerun
   with `-v`), and offer to apply the fix.

Never mark a poisoning-family failure as "flaky" — treat it as a real injection-handling
regression until proven otherwise.
