---
name: evals-bootstrap
description: >-
  Scaffold a first eval suite for an agent: mine real failures into cases,
  write behavioural checks over traces, and generate the runner. Use when the
  user wants evals, regression tests for an agent, a golden set, or asks how
  to know a prompt/model change did not break things. Do NOT use for a single
  task's done-check (goal-test) or for auditing context (context-audit).
---

# Bootstrap the eval suite

Theory: [Two kinds of checks](https://undefined-ui.github.io/second-brain-os/#course-5-evals/two-kinds-of-checks)
and the full walkthrough in [Evals practice](https://undefined-ui.github.io/second-brain-os/#course-5-evals/evals-practice).
An eval suite is the same test after every change. Behavioural checks read
the steps of a trace; end-to-end checks read only the result. Start
behavioural: they are deterministic, run in seconds, and diagnose instead of
just scoring.

## Workflow

1. **Find real failures.** Ask where the agent's runs live (logs, transcripts,
   a traces directory). Read until you have up to twenty real failures — not
   imagined ones. If there are no logged runs yet, build the trace logging
   first (step 3) and seed the suite with the three failures the user can
   recall; a small honest suite beats a large invented one.
2. **One line per failure.** For each: the input, and the one specific
   behaviour that should have happened and did not. Failures cluster into
   four to eight behaviours; name them.
3. **Ensure traces exist.** Each run must be stored as `traces/<id>.json` —
   a list of events including tool calls. If the user's harness is Claude
   Code, the transcript already is the trace; wire up whatever copies or
   converts it. No trace, no behavioural checks.
4. **Write `cases.yaml`.** One entry per failure:

```yaml
- id: refund_1042
  input: "Refund order #1042, customer says it arrived broken"
  expect: looks up the order before replying; asks approval before refund
  check:
    - trace has get_order before send_reply
    - trace has approval_request before refund
```

   The `expect` line is for humans; the `check` lines are the test. Keep the
   rule language tiny: `trace has X`, `trace has X before Y`, `trace lacks X`.
5. **Generate `check_traces.py`.** A small runner: load `cases.yaml`, parse
   each rule with a regex, walk the tool-call list, print one line per case,
   exit non-zero on any failure. Keep it dependency-light (pyyaml only) and
   fast — the whole suite should run in seconds, with no model calls.
6. **Run it and hand over the flywheel.** Show the pass/fail lines. Then
   leave the loop in writing at the end of your report: read fresh traces
   weekly, add every new failure as a case, fix the biggest cluster, re-run.

## Rules

- Every case comes from a real failure; delete a case only when the
  behaviour it guards is retired, not when it is inconvenient.
- No LLM-as-judge in the bootstrap. Add a judge later, only for what
  assertions cannot reach, and calibrate it against human labels first.
- The suite must be one command (`python check_traces.py`) so it can gate a
  CI job or a pre-release habit without ceremony.
