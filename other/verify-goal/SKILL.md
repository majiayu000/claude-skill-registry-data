---
name: verify-goal
description: 'Run every acceptance criterion of a goal file as an external check, record the command, its exit code and an output excerpt per criterion, and write a per-criterion verdict into the goal''s iteration ledger. Distinct from claim verification: this judges a deliverable against its contract, never a statement against its sources.'
---

# Verify Goal

## Purpose

The builder must not grade its own work by re-reading it. This skill runs the checks the goal
file names, as processes with exit codes, and puts their output where a fresh evaluator can
read it. On a host whose native goal evaluator reads only the transcript, this output is the
only evidence that evaluator will ever see.

## Procedure

1. **Read the goal file.** Refuse when status is not `active`. Refuse when a criterion row
   lacks a check or an expected result: send it back to the goal skill. Enforce the goal's
   token budget before every check, setting `exhausted` at the limit or `blocked` when a
   finite token limit cannot be measured. Do not start another check after either state.
   Use `iterations_used` for this entry; verification does not allocate another iteration,
   including when the current iteration is the last allowed one.
2. **Run every deterministic check**, one at a time, exactly as written in the `check`
   column. Capture exit code, stdout and stderr. Never edit the command to make it pass;
   never substitute a similar command.
3. **Compare** each result with the `expected` column. `met` when it matches, `unmet` when
   the command ran and did not match, `error` when the command could not run (missing tool,
   syntax error, timeout). An error is not an unmet criterion.
4. **Run review checks** only when every deterministic check is met. Name the artifact read
   and quote the passage that decides. A review verdict without a quoted passage is unmet.
5. **Write the ledger entry** in the Iterations section (format below), newest last. Quote at
   most twenty lines of output per criterion; keep the full output in the transcript.
6. **Update status**: `met` when every row is met; `active` when at least one row is unmet
   and none is error; `blocked` when any row is error. Preserve `exhausted` or a budget
   accounting block from step 1; unchecked rows are unmet, not evidence of completion.
7. **Print the summary** to the transcript verbatim: goal slug, iteration number, per-row
   verdicts, status. This line is what a native evaluator matches against the condition.

## Zetetic Gates

| Pillar | Gate | Failure action |
|--------|------|----------------|
| Logical | verdict derives from this run's result, not a previous one | rerun the check |
| Critical | output quoted, not paraphrased | quote it or mark unmet |
| Rational | review only after deterministic checks pass | skip reviews, report unmet |
| Essential | status updated from the verdicts, never by hand | recompute from the rows |

## Output Format

```markdown
### Iteration <n> (<date>) by verify-goal
| id | verdict | command | exit | evidence |
|----|---------|---------|------|----------|
| C1 | met | `pytest tests/auth` | 0 | `42 passed in 3.1s` |
| C2 | unmet | `git diff --stat main -- tests/auth/fixtures` | 0 | `1 file changed` |
status: active
```

## Hand-offs

| Condition | Next skill | Reason |
|-----------|------------|--------|
| every row met | none; status met | the contract is fulfilled |
| a row unmet | refine-goal | the next iteration needs a backlog |
| a row error | none; status blocked | the check itself must be fixed first |

## Anti-patterns

- Reading the diff and declaring a criterion met without running its command.
- Rewriting a failing command into one that passes.
- Reporting "tests pass" without the count and the exit code.
- Treating a timeout as unmet and iterating on code that was never measured.

## Examples

Iteration 2: C1 met (`pytest tests/auth`, exit 0, `42 passed`), C2 unmet (fixture diff shows
one file). Status stays active; the unmet row goes to refine-goal, which will add a step to
restore the fixture rather than relax C2.
