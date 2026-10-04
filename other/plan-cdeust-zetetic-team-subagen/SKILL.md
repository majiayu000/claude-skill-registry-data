---
name: plan
description: 'Turn an active goal contract into an ordered plan where every step carries its own check, then verify the plan against the goal before any code is written: each criterion is covered by at least one step, no step touches a non-goal, and the first step is the one that retires the most uncertainty.'
---

# Plan

## Purpose

A plan written from memory of the request drifts from the contract. This skill writes the
plan from the goal file and checks it against the same file, so the work that follows is
judged by criteria that existed before the plan did. The host's native plan mode, when one
exists, is a fine place to draft; the goal file is where the plan is kept.

## Procedure

1. **Read the goal file.** Refuse to plan a goal whose status is not `active`, or whose
   criteria table is empty. Enforce its token budget before further work; unavailable
   accounting for a finite token limit blocks. Refuse a new plan when `iterations_used`
   has reached the finite iteration limit: set `exhausted`, retain evidence and stop.
2. **Read the code the criteria touch.** Open every existing file a criterion reads or a
   step will change. For a new file, record its absence and inspect its parent directory
   and neighboring conventions before planning its creation.
3. **Draft the steps.** Each step states: what changes, in which files, which criteria it
   serves, and the check that proves the step is done (a command, or a reviewer reading a
   named artifact). A step with no check is split until each part has one.
4. **Order by uncertainty.** Put first the step most likely to show the goal is impossible or
   mis-specified. A cheap step that could invalidate the whole plan runs before an expensive
   step that assumes the plan holds.
5. **Verify the plan** against the goal file:
   - coverage: every criterion id appears in at least one step; list any orphan criterion;
   - scope: no step writes inside a non-goal; list any violation;
   - order: explain why the first step retires the most uncertainty; for a one-step plan,
     record that comparison with a second step is not applicable;
   - budget: a sound plan executes one step before verification; estimate whether remaining
     iterations cover the steps, and state any uncertainty without increasing the limit.
   Record the verdict `sound` or `unsound` with the findings.
6. **Write the Plan section** of the goal file: the steps, the mapping, the verdict. Replace
   the previous Plan section. Increment `iterations_used` and use that number as the plan
   revision. Append the CURRENT verdict and revision as the newest entry `by plan` in the
   Iterations ledger; earlier entries remain history. The Plan and latest plan entry must
   agree before execution. Recheck token usage before each implementation step or command.
7. **Stop** when the verdict is unsound. Rewrite with the findings as input. Do not execute
   an unsound plan to "see what happens".

## Zetetic Gates

| Pillar | Gate | Failure action |
|--------|------|----------------|
| Logical | criteria and steps map both ways | add the missing step or delete the orphan |
| Critical | plan judged against the file, not the memory of the request | re-read the file, re-verify |
| Rational | riskiest step first | reorder and state the reason |
| Essential | every step changes a criterion's outcome | delete the step |

## Output Format

```markdown
## Plan
revision: <iterations_used>
verify-plan: sound | unsound (<date>)
| step | change | files | serves | check |
|------|--------|-------|--------|-------|
| S1 | <what> | <paths> | C1, C3 | `<command>` exits 0 |
findings: <coverage / scope / order / budget notes, or "none">

### Iteration <iterations_used> (<date>) by plan
plan revision: <iterations_used>
verify-plan: sound | unsound
findings: <current findings>
```

## Hand-offs

| Condition | Next skill | Reason |
|-----------|------------|--------|
| verdict sound | execute S1, then verify-goal | the plan is covered and in scope |
| verdict unsound | plan (again) | findings become the input |
| a criterion cannot be served by any step | goal | the contract, not the plan, is wrong |

## Anti-patterns

- Planning from the chat history instead of the goal file.
- A step called "implement the feature" with no files and no check.
- Ordering by convenience so the hard step is discovered last.
- Silently dropping a criterion the plan cannot serve.

## Examples

Goal with C1 `pytest tests/auth` exits 0 and C2 fixtures unchanged. Plan: S1 run the suite
and record the failing tests (serves C1, check: the failure list is in the transcript); S2
fix the token expiry path in `auth/session.py` (serves C1, check: the two named tests pass);
S3 `git diff --stat main -- tests/auth/fixtures` is empty (serves C2). Verdict sound; S1 first
because it may show the failures are in fixtures, which would make the goal impossible.
