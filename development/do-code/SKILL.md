---
name: do-code
description: Implement a focused code change. Use this skill as the wrapper for any implementation work so the Maverick workflow report captures what was done and so the agent applies the project's coding standards before editing. Intended to be invoked once per task from inside a do-issue-* or do-epic phase, not standalone.
argument-hint: brief description of the task (one line)
user-invocable: true
disable-model-invocation: false
---

# Implement a Code Change

Wraps implementation work in a Maverick skill so the workflow report
records what was done and the agent applies the project's coding
standards before editing. Invoke this skill **once per task** from
inside `do-issue-solo` / `do-issue-guided` /
`do-epic` Phase 5. The argument is a one-line task
description that gets logged in the report.

This skill is a thin wrapper. The actual edits are made by the
orchestrating Claude Code session using its built-in tools (Read, Edit,
Write, Bash, Grep). The skill's job is to pin standards and scope, not
to perform the edits in a subagent.

## Project rules (mandatory)

Before doing anything else, check for repo-specific coding guidance at
`docs/maverick/skills/do-code/SKILL.md` (path relative to the repo root).

- **If the file exists**, read it fully and treat its contents as
  binding for this task. It holds project-specific rules that all
  Maverick coding in this repo must follow. Where it conflicts with
  generic guidance below, the project file wins.
- **If the file is absent**, continue without it. Do not create or
  scaffold the file as part of this task.

## Preflight (mandatory)

Run this **first**. If it exits non-zero, halt and report the stderr
output to the user verbatim. Do not proceed.

```bash
uv run maverick preflight do-code
```

Skip the preflight when invoked from inside a `do-issue-*` or
`do-epic` phase — the orchestrator already ran a stricter one this
session. Run it only when this skill is invoked standalone.

The check verifies the project is initialised and `uv` is on PATH.

## Standards to apply

Before editing, read and follow:

- `mav-scope-boundaries` — implement only what `$ARGUMENTS`
  asks for. No unrelated cleanup, no opportunistic refactors, no
  abstractions for hypothetical future requirements. Three similar
  lines is better than a premature abstraction.
- `mav-bp-error-handling` — error handling at system
  boundaries only (user input, external APIs). Don't catch what
  framework guarantees rule out. No defensive code for scenarios that
  can't happen.
- `mav-bp-operability` — log levels, structured fields, and
  the project's logging conventions.
- `mav-bp-application-security` — input validation, secret
  handling, authn/authz patterns. If the change touches any of these,
  surface the design choice in your verification.

Also read **any project-level skills** at `docs/maverick/skills/` —
topic-specific guidance for this codebase that supplements the
maverick-wide best practices.

## Implementation loop

1. **Read before writing.** Open the files you're about to change.
   Grep for existing patterns nearby — the goal is for the edit to
   look like it was written by whoever wrote the surrounding code.
2. **Make the change.** Smallest diff that satisfies the task. If you
   notice an unrelated bug or a tempting refactor, **do not fix it**
   in this skill — write it down for a follow-up.
3. **Verify** per `mav-local-verification` (lint,
   typecheck, tests). Run the project's verification commands.
4. **If verification fails**, diagnose per
   `mav-systematic-debugging` and fix. Do not paper over
   a failing test or silence a lint warning. Do not commit red.
5. **Return** when (a) the task is done and (b) verification is green.

## Rules

- **Default to no comments.** Identifiers carry the WHAT. Only add a
  comment when the WHY is non-obvious (hidden constraint, subtle
  invariant, workaround for a specific bug). No "removed X" /
  "added Y" / "used by Z" comments — those rot.
- **No half-finished implementations.** If the task can't be completed
  cleanly, halt and report rather than leaving partial state.
- **No unauthorised destructive actions.** Don't `git push --force`,
  `git reset --hard`, `rm -rf`, drop tables, or delete data. If the
  task description doesn't explicitly authorise a destructive step,
  treat it as out of scope and ask.
- **Tests are part of the change.** If the change is testable, write
  or update tests in the same task (or wrap that work in
  `do-test` as a sibling call before the commit).
- **Stay inside the task envelope.** When `$ARGUMENTS` is
  ambiguous, ask for clarification rather than guess.

## Return Protocol

`do-code` is a **subroutine of the calling workflow's
per-task loop** — not a terminal action. Returning from this skill is a
hand-back to the caller's next numbered step, not a completion event
(#106).

When you return from this skill, **do not** post a closing summary, do
not stop, do not treat verification-green as "task done." The calling
workflow's loop still owns, in order:

1. Closing the `skill-dispatch` interval that wrapped this invocation
   (`uv run maverick report end skill-dispatch … --outcome success`).
2. Optionally sibling-calling `do-test` for tests that
   weren't folded into this skill.
3. Conventional commit referencing the issue number, then push (with
   stacked-PR retarget if applicable).
4. Logging the commit row to the workflow report
   (`uv run maverick report commit …`).
5. Updating the tasks comment / closing the sub-issue.
6. Heartbeat refresh.

If you find yourself drafting a final summary after returning here,
that is the signal: scroll back to the calling workflow's per-task
loop and resume from the step immediately after the
`/do-code` invocation.

<!-- maverick-plugin-version: 4.0.2-dev -->
