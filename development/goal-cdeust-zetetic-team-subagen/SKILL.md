---
name: goal
description: 'Compile a long-running objective into a persistent, host-neutral goal contract: one measurable end state, non-goals, acceptance criteria written as external checks with an expected exit code, a budget, and an iteration ledger. Mirrors the end state into the host''s native goal command so the host''s stop check and the contract agree.'
---

# Goal

## Purpose

Native goal commands differ by host. This skill keeps the end state, acceptance checks,
non-goals and budget in a file that another session or host can read. Mirror the condition
through an available native goal capability; when none exists, report the file and the
next skill without claiming that automatic continuation was configured.

## Procedure

1. **Bind the request.** Resolve every named system, file, or concept to a concrete artifact
   with evidence (grep, git history, the memory layer's recall). When the wording is vague,
   run the refine procedure first. Do not guess a binding silently.
2. **Name the end state.** One sentence, one measurable condition: a test result, a build
   exit code, a file count, an empty queue. If two independent end states are present, write
   two goals.
3. **Name the check for each criterion.** Each acceptance criterion is a row with an id, the
   criterion in prose, the exact command that proves it, the expected result (exit code or
   output pattern), and its kind: `deterministic` when a command decides, `review` when a
   reader must judge. A criterion with no command and no reader is not a criterion.
4. **Write the non-goals.** What this goal will not change, so that a later iteration cannot
   widen the scope to make a criterion pass.
5. **Set the budget.** Maximum iterations and, when the host reports it, a token ceiling.
   Use the user's limits; otherwise write `null` and disclose that limit as unbounded.
   An iteration starts when plan writes its current verdict, including an unsound verdict.
   Initialize `iterations_used` to zero only for a new contract. Verify/refine entries use
   that same iteration number. When repairing an existing goal, preserve usage counters,
   accounting baselines and ledger history. Reactivate a blocked goal only with evidence
   that its recorded blocker is resolved and its budgets permit the next phase.
   Token accounting is cumulative for this goal across sessions, with a recorded host usage
   baseline for each session. If a requested token limit cannot be measured, leave the goal
   blocked with that reason; do not invent usage or silently remove the limit.
6. **Write the file** at `.zetetic/goals/<slug>.md` using the format below, status `active`
   only when budget accounting permits it; preserve a budget-accounting `blocked` state.
   If no check could be named in step 3, leave status `draft` and stop: the request is not
   ready to run.
7. **Mirror into the host.** Activate a native goal only when the user explicitly requested
   a goal and the host provides that capability. Hand it a condition of the form:
   `verify-goal reports every criterion of .zetetic/goals/<slug>.md met, with the command
   output in the transcript, or the file reports blocked or exhausted`. Mirror a token cap
   only when the user supplied one and the host supports it. Print the state so a host
   evaluator that reads the transcript can distinguish achievement from stopping.
8. **Record the decision** in the memory layer: the slug, the end state, and the reason for
   each non-goal.

## Goal file format

```markdown
---
slug: <slug>
status: draft | active | met | blocked | exhausted
created: YYYY-MM-DD
budget:
  iterations: <N or null>
  tokens: <N or null>
iterations_used: 0
tokens_used: <reported cumulative usage or null>
---
# Goal: <one-sentence end state>

## Non-goals
- <what stays untouched, and why>

## Acceptance criteria
| id | criterion | check | expected | kind |
|----|-----------|-------|----------|------|
| C1 | <prose> | `<command>` | exit 0 | deterministic |
| C2 | <prose> | reviewer reads <path> | <what they must find> | review |

## Plan
<written by the plan skill>

## Token accounting
<session identifier, host usage baseline and latest cumulative usage; or unavailable>

## Iterations
<appended by verify-goal and refine-goal, newest last>

## Lessons
<appended by refine-goal>
```

## Budget boundaries

Before each skill and before each new command or implementation step, refresh reported
token usage. At a reached finite token limit, set `exhausted` and stop. Missing accounting
for a finite token limit sets `blocked`. Preserve counters across resumes; only the user
may extend limits. Record any overshoot from an in-flight operation. These procedural
checks act between operations; a hard token cap requires host support.

Before starting plan, require `iterations_used < budget.iterations` when the limit is
finite; otherwise set `exhausted`. A sound plan at the last allowed iteration may still
execute its step, verify and refine. The next plan is refused. An unsound replan also
consumes an iteration, so repeated planning cannot bypass the bound.

## Zetetic Gates

| Pillar | Gate | Failure action |
|--------|------|----------------|
| Logical | every criterion has an external check or named review and an expected result | clarify the check; keep the requirement and leave the goal draft |
| Critical | the end state is decidable from the transcript alone | rephrase until a fresh reader can judge it |
| Rational | one end state per goal | split into two goal files |
| Essential | non-goals written before activation | do not set status active |

## Output Format

The goal file path, its status, the condition handed to the host, and the list of criteria
with their kind. Nothing else: planning belongs to the plan skill.

## Hand-offs

| Condition | Next skill | Reason |
|-----------|------------|--------|
| status active | plan | the contract exists; order the work |
| status draft | none | no check could be named; scope with the user |
| status blocked | none | report the accounting blocker and preserve the existing contract |

## Anti-patterns

- A criterion phrased as "works correctly" or "looks good": the transcript cannot show it.
- Setting the native goal without the file: the sentence is lost on the next host.
- Widening the end state during an iteration: that is a new goal, not a refinement.
- Inventing a budget the user did not ask for and hiding that it exists.

## Examples

Request: "make the auth tests pass without touching the fixtures".
End state: `pytest tests/auth` exits 0. Non-goal: `tests/auth/fixtures/` unchanged, checked
by `git diff --stat main -- tests/auth/fixtures` being empty. Two deterministic criteria,
budget five iterations, status active, native condition names both commands.
