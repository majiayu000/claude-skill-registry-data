---
name: verify-change
description: Verify an implemented change by mapping intended behavior to executable checks, running those checks, and handing off concrete evidence and gaps. Use when asked to verify agent-generated code, prove a change works, or prepare a verification handoff when code volume exceeds human reading capacity. This is implementation verification; use codex-review for an adversarial Codex review of Opus-generated code.
---

# Verify Change

Give the implementation agent a way to check its work and give the human
evidence they can evaluate. The output is a verification handoff for a
specific code state, not a code-review verdict or permission to merge.

## Establish intent and scope

Read the request, the changed code, and the project's guidance and existing
checks. Identify the intended behavior and the boundaries it must preserve.
Use the user's PR, commit range, or paths when supplied; otherwise identify
the active change and state its scope. Resolve an ambiguous scope before
claiming coverage.

Record the baseline and head commit where available, plus relevant staged,
unstaged, and untracked files. For a dirty checkout, preserve enough local
diff or content identity to distinguish the tested state from a later edit.
Do not commit, reset, or clean the checkout to make verification easier.

This skill can be used by the agent that wrote the code. It does not run
Codex, dispatch adversarial reviewers, or invoke codex-review. If independent
review is also requested, hand off the verification record separately;
that review remains a distinct activity.

## Map behavior to evidence

Build a compact map of the changed behavior, its important failure modes,
and the checks that could detect them. Use a short paragraph for a tiny
change or a table for several behaviors:

| Intended behavior or invariant | Failure to catch | Check and observable result | Gap |
|--------------------------------|------------------|-----------------------------|-----|
| Specific user action or system contract | Concrete regression or boundary error | Existing test, command, experiment, or inspection and what success means | What this check cannot establish |

Derive expectations from the requirements, established contracts, or a
known-good reference. Do not derive the expected answer solely from the new
implementation. In a bug fix, prefer a check that demonstrates the original
failure and passes with the fix when that comparison is practical and safe.

Size the verification to the consequences of failure. Consider affected
users, sensitive data, shared state, cross-platform behavior, and how easily
the change can be undone. Diff size and the author's confidence are poor
substitutes for risk. Read existing project requirements before choosing
additional checks.

## Choose useful feedback loops

Use the cheapest check that can detect each consequential failure, then
cross the relevant integration boundary where a local check is insufficient.
Examples include a reproducer, targeted tests, type checks, a build, a
browser interaction, or a device run. Reuse existing checks where they
already establish the behavior; avoid adding tests that merely mirror the
implementation or add little confidence to a trivial reversible edit.

For user flows, exercise the actual interaction and assert its result.
For transformations or state machines, consider invariants and property
tests. For UI work, inspect rendered states and interactions; a successful
build cannot establish layout or usability. For permissions, test the
denied path as well as the allowed path. Passing static checks alone does
not establish runtime behavior.

Read [references/verification-patterns.md](references/verification-patterns.md)
when choosing checks for an unfamiliar change or explaining the method's
origin. The examples are options, not a mandatory test suite.

## Run checks and keep their evidence

Run the relevant available checks in the authorized environment. Inspect
scripts before running unfamiliar commands whose effects could reach live
systems. Prefer isolated fixtures or a test environment for mutating flows;
do not substitute production data or change deployment settings to obtain
a green result.

For each material check, record the command or procedure, tested code state,
environment, actual outcome, and enough output or artifact location to
support it. A zero exit code with no tests discovered is not evidence that
the feature passed. A screenshot supports what is visible in that state;
it does not prove a backend action completed.

Distinguish passed, failed, not run, and blocked checks. Explain a failed
check before dismissing it as unrelated; compare against the baseline if
needed and feasible. Do not replace an expected outcome with the observed
output just to pass a test.

If a repair is already authorized, fix the cause and rerun affected checks.
After a change to tested code or a dependency it relies on, invalidate the
affected evidence and refresh it. Do not apply results from an earlier
commit to a later one without checking what changed.

Track failed repair-and-check attempts for each behavior. After three
failed attempts on the same behavior, complete a checkpoint before trying
again: summarize what changed and what the checks showed, then either
diagnose the failing assumption from that evidence or choose a materially
different repair strategy. State what the next check will establish;
cosmetic edits or an unchanged rerun do not satisfy the checkpoint.

Resume authorized repair after the checkpoint and start a new attempt
count. Three attempts trigger diagnosis or a strategy change, not a stop
or a request for renewed permission. Diagnose earlier when retries are
already uninformative. The task's time, cost, and risk limits still apply;
report a blocker when progress actually needs missing input or access.
Do not create a reviewer/fixer loop here or relax assertions to finish.

## Hand off evidence and residual risk

Report concisely:

- **Scope and intent:** what changed and which code state was checked.
- **Evidence:** the meaningful checks and actual outcomes, with commands
  and local artifact or CI links where useful.
- **Gaps:** important behavior not exercised, what passing checks miss,
  and the next check or person needed to resolve the uncertainty.
- **Recovery and ownership:** how to disable or revert a consequential
  change, and the responsible person if the context identifies one. State
  when a recovery path is proposed rather than tested; do not invent an owner.
- **Required human decisions:** the project's ownership rules, required
  checks and approval policy as far as they can be read. If they cannot be
  read, say the policy is unknown, not that none applies. Name any change to
  CI workflows, or to paths the project marks as owner-reviewed or sensitive,
  as needing a human decision; passing checks do not stand in for it.

Say plainly when verification is incomplete. Avoid a blanket claim that
the change is safe or bug-free. A missing environment or credential belongs
in the handoff as a gap, not an inferred pass.

This handoff does not approve a PR, resolve review threads, change required
reviewers, publish, or deploy. Follow the project's existing review process;
automated evidence does not stand in for a required human decision.

If a recurring failure reveals a stable invariant, suggest a targeted
regression check or a short project instruction. Make that follow-up
concrete rather than accumulating generic rules. Broader pipeline changes
and reviewer evaluations are separate work when requested.

## Attribution

Adapted from [Addy Osmani's X post, 18 October 2026](https://x.com/addyosmani/status/2111604705340326393)
and [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/)
by Addy Osmani, Morgan Westlee Lunt, and Qing Wang (15 October 2026).
This skill implements the verification and evidence-handoff part of their
approach; Inkstone's codex-review remains the separate adversarial reviewer.
