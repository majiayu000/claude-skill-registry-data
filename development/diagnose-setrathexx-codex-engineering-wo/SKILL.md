---
name: diagnose
description: Runs a systematic debugging workflow for bugs, regressions, flaky behavior, and performance surprises. Use when something is broken, failing, throwing, slow, flaky, or when the user asks to debug or diagnose a specific problem.
---

# Diagnose

Diagnose bugs by building a reliable feedback loop, proving the symptom, narrowing the cause, fixing the smallest responsible behavior, and leaving a regression check behind.

Do not jump straight to a fix. A plausible fix without a reproduced symptom is guesswork.

## Read First

Before changing code, inspect project setup:

- `docs/agents/test-commands.md`
- `docs/agents/domain.md`
- `CONTEXT.md`
- relevant ADRs under `docs/adr/`
- package scripts or equivalent task definitions

If setup docs are missing, infer commands from the repo. If commands remain unclear, ask the user one focused question.

Use the repo's domain language when describing the failure and suspected modules.

## Workflow

### 1. State The Symptom

Restate the user-visible failure in one or two sentences.

Capture:

- What is expected.
- What actually happens.
- Where it happens.
- Whether it is deterministic, flaky, or performance-related.

If the symptom is ambiguous, ask for the missing observation before changing code.

### 2. Build A Pass/Fail Feedback Loop

Create or identify the fastest command or action that can prove the bug exists.

Prefer this order:

1. Focused failing test.
2. Existing test command that already fails for the right reason.
3. CLI command with fixture input.
4. HTTP request against local dev server.
5. Browser automation for UI bugs.
6. Small throwaway harness near the relevant code.
7. Replayed payload, log, trace, or fixture.
8. Repeated stress loop for flaky behavior.

The loop must be:

- Runnable by Codex.
- Specific to the user's symptom.
- Deterministic when possible.
- Fast enough to repeat.

If no loop can be built, stop and explain what was tried. Ask for a log, fixture, repro steps, recording, environment access, or permission to add temporary instrumentation.

See `references/feedback-loop-patterns.md` for options.

### 3. Reproduce

Run the loop and verify it fails for the same reason the user reported.

Record:

- Command or action used.
- Exact failure text, wrong output, timing, or visible behavior.
- Whether the failure repeated.

Do not continue if the loop fails for an unrelated reason.

### 4. Minimize

Reduce the failing case while preserving the same symptom.

Options:

- Narrow to one test.
- Reduce fixture size.
- Remove unrelated setup.
- Isolate one function through public entry points.
- Pin time, random seed, filesystem path, or network dependency.
- Increase reproduction rate for flaky cases.

Keep the minimized loop connected to the real bug path. Do not create a tiny test that proves a different problem.

### 5. Hypothesize

Write 3 to 5 ranked hypotheses before editing the fix.

Each hypothesis must include:

- Suspected cause.
- Prediction.
- Probe that can confirm or falsify it.

Format:

```txt
1. Cause: ...
   Prediction: If this is true, then ...
   Probe: ...
```

Share the ranked list when useful. If the user is unavailable, proceed with the strongest falsifiable hypothesis.

### 6. Instrument

Add the smallest temporary probe that tests one hypothesis.

Allowed probes:

- Debugger or REPL inspection.
- Targeted logs at key module boundaries.
- Timing measurement for performance regressions.
- Query plan or profiler output when relevant.
- Assertion in a throwaway harness.

Tag temporary logs with a unique marker such as `[DIAG-1234]`.

Avoid broad logging. Change one variable at a time.

### 7. Fix

After a hypothesis is confirmed, make the smallest fix that addresses the real cause.

Prefer fixing the module that owns the behavior rather than patching each caller.

Do not broaden scope into unrelated cleanup.

### 8. Add Regression Coverage

Before or alongside the fix, add a regression test at the best available public interface.

A good regression test:

- Fails before the fix.
- Exercises the real bug pattern.
- Uses public behavior, not private implementation.
- Would catch the bug if it returns.

If no correct test location exists, document that as an architecture/testability finding and leave the strongest verification command available.

### 9. Clean Up

Remove temporary instrumentation:

- Search for the unique debug marker.
- Delete throwaway harnesses unless the user approved keeping them.
- Remove temporary files or mark them clearly if kept.

Do not remove user files unrelated to the diagnosis.

## Performance Regressions

For slow behavior, measure first.

Record:

- Baseline timing.
- Command or scenario measured.
- Change after the fix.
- Variance if repeated.

Avoid log-heavy instrumentation that changes timing.

## Flaky Behavior

For flaky behavior, improve reproduction rate.

Use:

- repeated runs,
- isolated environment,
- pinned seed,
- controlled time,
- narrowed concurrency,
- stress loop.

Report failure rate before and after.

## Verification

Before declaring done:

- Re-run the original repro loop.
- Run the minimized regression test or closest focused command.
- Run relevant broader verification if affordable.
- Confirm temporary instrumentation is removed.
- Summarize root cause, fix, regression coverage, and remaining risk.

See `references/diagnosis-loop.md` for the compact checklist.
