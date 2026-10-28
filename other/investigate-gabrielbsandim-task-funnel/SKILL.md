---
name: investigate
description: Investigation flow. Takes a question about the system (why does X happen, where does Y live, is Z feasible, what broke) and returns a verified written answer with evidence. Read-only end to end, no branch, no code change, no pull request. Use when asked to investigate, diagnose, explain behaviour or assess feasibility, or on /investigate <question>.
---

# investigate: question in, verified answer out

Read-only, end to end. If the fix becomes obvious mid-flight, the finding
becomes the spec for the task funnel; you do not edit files here. An
investigation that quietly turns into a change skips triage, tests and review,
which is every gate the funnel has.

Input: the question after the command. Empty, ask what to investigate and stop.

## Stage 1 · Sharpen the question

Restate the question and state **what evidence would settle it**. If you cannot
say what would settle it, ask and stop. Fanning out on a vague question buys file
dumps, not an answer.

## Stage 2 · Fan out, read-only, in parallel, in one message

Each subagent gets the full question, because it inherits nothing, plus one
angle:

- **code path**, where it lives, who calls it, what it returns
- **data**, schema, migrations, what the rows actually allow
- **history**, `git log` and `git blame`, the tracker, why it is the way it is
- **runtime**, config, environment, scheduled jobs, webhooks, external services

Skip the angles the question obviously does not touch. Two is a normal number,
and the concurrency ceiling is `kit config get .maxParallelAgents` (with no `kit` on
PATH, `${CLAUDE_PLUGIN_ROOT}/scripts/kit`).

Every claim a subagent returns is tagged **MEASURED**, with the command and its
output, or **INFERRED**.

## Stage 3 · Verify

An INFERRED claim that bears on the conclusion is measured before the report:
run, or dispatch, the one command that would prove it. Two angles disagreeing is
resolved by measuring, never by picking the more plausible one. An inherited
claim is not a fact.

## Stage 4 · Deliver

- The answer in short prose, conclusion first, evidence after it.
- Tied to an existing issue, post it as a comment on that issue, in the
  language the rest of the tracker uses.
- Out-of-scope findings discovered along the way become new issues, the way the
  repo's pipeline document says to open them. Never code.
- If the fix is then asked for, hand the finding to the task funnel as its spec.

## Token rules

- No worktree and no dependency install. Nothing here writes, so nothing here
  installs.
- You hold conclusions, not file dumps. Subagents read, you consolidate.
- One MEASURED claim beats a paragraph of maybes. The command's output is
  cheaper than a wrong conclusion re-litigated across the session.
