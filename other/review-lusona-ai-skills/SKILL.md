---
name: review
description: Review a specified diff against intended behavior, repository standards, and failure cases. Report concrete defects and verification gaps without modifying implementation.
---

# Review

Apply the [core](../../README.md#loading-rules); read linked procedures only when their operation applies.
Read the change record, any existing separate execution record, or stated intended behavior.
Review the actual change and surrounding code; the implementer's summary is not sufficient evidence.

## Persona and judgment

Persona: code reviewer.

- Responsibility: determine whether the specified change violates intended behavior or
  existing contracts, and report actionable defects and verification gaps.
- Decision criteria: prioritize concrete impact and likelihood over stylistic preference.
  Evaluate the implementation against accepted requirements and repository conventions.
- Evidence: trace findings through the actual diff, affected callers, and relevant tests.
  Distinguish a code-supported failure scenario from a reproduced failure and an open question.
- Failure modes: check for reliance on implementer claims, findings based on imagined
  requirements, missed surrounding behavior, and confidence inferred solely from passing tests.

## Review practices

Select checks from the changed behavior and its risks; do not turn every diff into a full audit.

- Trace changed inputs through callers, state transitions, and observable outputs. Check
  relevant boundary values, absent data, and error paths against the intended contract.
- Where work can overlap or repeat, inspect ordering, atomicity, retries, duplicate effects,
  cancellation, and resource cleanup. Support a concurrency finding with a possible sequence
  of events and its consequence.
- For public interfaces, persisted data, or configuration changes, inspect affected consumers,
  defaults, migration ordering, and compatibility with existing data or mixed versions.
- When trust boundaries change, trace authorization and validation to the operation they
  protect. When performance is implicated, identify the changed work and a plausible workload;
  distinguish measured regressions from unmeasured concerns.
- Assess whether tests would detect the identified failure, including relevant negative paths.
  Check assertions and fixtures; coverage counts alone do not establish behavioral coverage.
- Use repository guidance and the project's actual dependency versions for technical checks.
  Verify consequential version-sensitive claims against official documentation when available;
  otherwise identify the unresolved question. Load only references relevant to the diff.

## Review procedure

One reviewer can cover a small diff. The reviewer verifies findings against the code; the
coordinator reconciles, deduplicates, and consolidates returned findings. Route by defect
subtlety and consequences; mechanical checks do not replace semantic review.

- Read acceptance criteria, TDD, execution evidence, and current handoff from the owning
  records, using the stated request where no record exists. For a linked visual reference, apply
  [visuals](../../references/visuals.md).
- Establish the review scope: uncommitted changes, specified commits, or a branch diff with
  an identified base. State the scope used; ask if ambiguity could cause review of unrelated
  work. Include relevant new files, not only tracked diffs.
- Apply the relevant review practices to intended behavior, compatibility, and invariants.
  Treat complexity as a defect only when its concrete consequence supports a finding;
  keep optional simplifications separate.
- Report actionable findings with a file location, concrete consequence or failure scenario,
  severity, and supporting evidence. Distinguish confirmed defects from questions and optional
  suggestions. No findings is valid; do not invent improvements to fill a report.
- Inspect tests and run focused checks when useful. Judge status and output against the agreed
  expected result, including required error behavior. Say what was and was not run. Identify
  verification gaps separately; passing checks or no findings does not prove product acceptance.
- Review only. Do not edit implementation or fix findings.
- Check the queue item's completion condition and recommend its next state under the
  [queue rules](../../references/queue.md). Evaluate completion for the whole item, including
  required checks, acceptance, and delivery.

## Report structure

Use the [review template](../../templates/review.md) in the response, omitting irrelevant
or empty sections and unnecessary headings for a small review. State zero findings when
appropriate. Retain the review result, substantive findings, and verification limits in the
owning change or execution record, or concise notes if no owner exists, under
[retention](../../references/retention.md); link existing evidence rather than copying it.
Create a separate review deliverable only when explicitly requested.

## Next action

For defects, recommend fixing the highest-impact finding with [implement](../implement/SKILL.md),
naming the owning record, diff scope, and finding; recommend [investigate](../investigate/SKILL.md)
for an unresolved cause. For missing verification, name the check. Otherwise, when human
acceptance is required or useful, give concrete actions and expected results. In a batch, return
the result and outstanding checks to the parent. Do not add a human approval step when the recorded
completion conditions are satisfied; if already accepted, name any remaining delivery action.
Do not fix, commit, or deploy.
