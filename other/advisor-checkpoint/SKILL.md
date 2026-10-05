---
name: advisor-checkpoint
description: >
  Consult a stronger model mid-task for a second opinion before committing to
  an approach, when stuck, or before declaring a non-trivial task done — the
  fast-executor + strong-advisor pattern, implemented with the Agent and
  Workflow tools (Claude Code does not expose Anthropic's raw API advisor
  tool). Use when running on a cheaper/faster model for mechanical work and a
  hard design/architecture/risk decision needs a stronger check, or when
  authoring a Workflow script that should get expert review partway through
  instead of only at the end.
---

# Advisor Checkpoint

Spend the expensive model only at a task's few load-bearing moments; let a
cheaper/faster model handle the rest.

## When to consult

- **Before committing to a non-obvious approach.** Orientation (reading files,
  finding the shape of the problem) doesn't need it; the moment you're about
  to write code, edit a plan, or declare an interpretation does.
- **When stuck** — an error is recurring, an approach isn't converging,
  results don't fit what you expected.
- **Before declaring a non-trivial task done.** Make the deliverable durable
  first (commit, save, write the file) — the consult adds latency, and a
  durable result survives an interruption where an unwritten one doesn't.

Skip it on short, reactive steps where the next action is dictated by what you
just read — the value is highest on the first consult, before an approach
crystallizes, not on every turn.

## In an interactive session

Dispatch an `Agent` call at a checkpoint above, with `model` set to a stronger
tier than the one currently running (`opus` or `fable`), given the plan or
diff so far and a specific question — not "review everything," but "does this
approach have a flaw" or "which constraint breaks the tie between X and Y."

Treat the response as advice, not a verdict:

- If you act on it and it fails empirically, or you have primary-source
  evidence it's wrong (the file says X, the test says Y), adapt — don't
  re-litigate an empirical result against advice.
- If you already have evidence pointing one way and the advice points
  another, don't silently switch. Surface the conflict in one more consult —
  "I found X, you suggest Y, which constraint wins?" — rather than picking a
  side alone.
- A passing self-check is not evidence the advice was wrong; it's evidence
  your check doesn't test what the advice was about.

This is the same posture as the security-review skill's verify-before-report
principle — a second opinion is only useful if you actually weigh it, not
just collect it.

## In a Workflow script

`agent()` calls accept a per-call `model` override, so a workflow can run its
bulk stages on a cheap/fast model and insert a stronger-model checkpoint at
the same moments — after the fast stage has produced something concrete (a
plan, a diff, a set of findings), not before. Workflow agents don't share a
live transcript automatically, so pass the advisor exactly what it needs to
judge:

```js
// Fast stage: does the exploration/legwork on the default (cheaper) model.
const draft = await agent('Draft an approach for <task>.', { label: 'draft' })

// Advisor checkpoint: a stronger model reviews the CONCRETE output.
const advice = await agent(
  `Review this approach for <task>. Flag any flaw or missed constraint:\n\n${draft}`,
  { label: 'advisor-checkpoint', model: 'opus' }
)

// Fast stage resumes, informed by the advice.
const result = await agent(
  `Implement this approach, taking the following review into account:\n\nApproach:\n${draft}\n\nReview:\n${advice}`,
  { label: 'implement' }
)
```

The same shape applies before a final "done" verdict: run the cheap stage,
then one `agent()` call on a stronger model asked specifically "is this
actually complete, or is something missing" before the workflow returns.

This is a named instance of the Workflow tool's existing judge-panel/pipeline
patterns — nothing new is being invented, just this specific shape (propose →
advise → refine) is worth reaching for whenever a workflow's early stages are
cheap and mechanical but a later stage is a real decision.
