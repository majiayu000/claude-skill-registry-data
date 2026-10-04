---
name: verify
description: Run an explicit user-requested criteria-driven verification loop. Use when the user asks to define success criteria, close the loop against criteria, or rigorously verify non-code outputs. Do not use for a plain live-software check owned by end-to-end, routine coding completion, or narrower audit/debug checks.
user-invocable: true
argument-hint: <task description>
---

# Criteria-driven verification

Translate the user's actual requirements into checks, evaluate the intended
artifact or outcome, and report what the evidence establishes. A verification
request alone does not authorize implementing fixes or changing the target.

## Scope and authority

- For one direct check or a narrower coding, debugging, PR or audit workflow,
  use its verification path instead of adding this outer loop.
- For plain live-software acceptance, use `end-to-end` alone. Combine it with
  this skill when the user explicitly requested generated criteria or a
  criteria-driven loop: this skill owns the requirements and `end-to-end`
  owns decisive live observations.
- Use available workflow checks; do not assume a named plugin is installed or
  that it overrides the active runtime's completion rules.
- Separate verifying existing work, proposing criteria, and executing or
  repairing work. Only carry out the modes the user authorized. Evidence
  collection must respect access, privacy, cost and external-write boundaries.
  A criterion is not permission to send a message, publish, delete, or obtain
  credentials. Use isolated fixtures where appropriate and label their limits.

## 1. Establish the target

Read the request and relevant source material. Identify the exact artifact,
version, environment and outcome to verify. Preserve user-supplied acceptance
criteria and distinguish requirements from examples or optional preferences.
For a changed or live target, record enough identity and observation time to
avoid attributing one version's result to another.

Read-only inspection needed to define criteria may precede execution. Do not
claim that criteria were fixed in advance if work or evaluation already began.
If the task is only to propose a verification plan, deliver that plan without
running the underlying workflow.

## 2. Define criteria and evidence

Map each material requirement to an observable check and its evidence source.
Keep this proportional to the task; a small task may need only a few sentences.
For each criterion, establish:

- What would count as success and failure, including relevant edge cases.
- Where the expectation comes from: user requirements, a source record,
  authoritative specification or a clearly identified assumption.
- How to observe the result directly, with scope, tolerances and sampling
  limits stated when they matter.
- Whether the check is available, safe and within authority. Keep required
  human judgment, external approval or inaccessible evidence visible as a gap;
  do not remove the requirement or replace it with an unapproved proxy just
  because the agent cannot evaluate it.

Criteria should cover the important dimensions without imposing unrelated
standards. A five-year source cutoff, empty-list output or exact tone rubric
is appropriate only when the task warrants it. For historical or stable facts,
source relevance and reliability matter more than an arbitrary recency window.

Separate mechanical checks from qualitative judgment. Word counts are directly
measurable; audience fit may need a rubric and a qualified assessment. Passing
the former does not prove the latter. An agent's confidence is not evidence of
quality, user approval or domain authority.

State proposed criteria before substantial execution when useful. Ask only
when a missing decision materially changes scope or success and no reasonable
default exists, or when the user requested approval of the criteria. Otherwise
use explicit, reversible assumptions and proceed within scope.

## 3. Check whether the criteria are adequate

Before applying the checks, look for missing requirements, circular tests and
weak proxies. Expected values must not simply copy the current output under
test. Ask whether a plausible wrong result would fail the checks; use known
positive and negative cases or independent references when useful.

If a criterion remains vague, consult the relevant authoritative rubric or
source and refine its observable meaning. Keep this investigation bounded.
There is no guarantee that recursively evaluating the criteria will converge.
When safe avenues are exhausted, preserve the unresolved requirement and
explain the evidence or judgment needed, instead of declaring it testable by
approximation. Continue independent checks that remain meaningful.

Do not relax acceptance thresholds, drop a failing requirement or alter source
evidence to get a pass. Correct a demonstrably mistaken check with an explicit
reason, preserve the original requirement, and re-evaluate affected results.
Material changes to user-approved criteria require renewed agreement.

## 4. Execute only authorized work and evaluate

If the user requested implementation as well as verification, do that work and
check relevant criteria along the way. For verification-only requests, inspect
the target and report defects without silently repairing it. Subagents may
provide independent evaluation when available and authorized; give them the
requirements and raw evidence, not a demanded verdict.

Evaluate every applicable criterion using the bound target:

- **Pass:** the required observation supports it; cite or retain that evidence.
- **Fail:** evidence contradicts it; identify the concrete discrepancy.
- **Uncertain:** evidence is missing, stale, conflicting, sampled too narrowly,
  or requires judgment the agent cannot supply. State the limitation.
- **Not applicable:** justify why it does not apply; never use this to discard
  an inconvenient required check.

If using a curated case set, run every declared case and report the denominator,
failures and exclusions. Accuracy on those cases is not population accuracy.
For qualitative reviews, distinguish source-backed findings from assessments.
Mocked results, static checks and fixture runs cannot silently stand in for a
required live outcome.

## 5. Recheck or report

When repairs are authorized, fix supported failures, then rerun failed checks
and all checks affected by the change. Rebind evidence if the target changed.
Stop repeating an approach when it is not yielding new evidence or progress;
surface the unresolved issue without broadening authority.

For verification-only work, a report of failures can complete the requested
review while the target remains incorrect. Do not describe the target as fixed.
For execution work, call it complete only when the material requirements are
covered and their required checks pass. An all-green table over an incomplete
or self-selected subset does not establish completion.

Deliver the result or artifact with concise pass/fail/uncertain findings and
material evidence gaps. Put a detailed criterion-to-evidence record in an
appropriate audit artifact when useful, not an unsolicited session log.
State exactly what was verified; preserve unresolved uncertainty instead of
asking the user to waive it as the default path to a success claim.
