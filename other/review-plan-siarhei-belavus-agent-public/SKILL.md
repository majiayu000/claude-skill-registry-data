---
name: review-plan
description: Review `PLAN.md` as a blind-handoff execution contract; emit `P#` findings into the task packet and block plans with ambiguity, hidden assumptions, poor artifact hygiene, or missed durable-residue calls.
---

# review-plan

Review plans as execution contracts, not brainstorming notes. Judge the written plan on its own contents, not on what the human probably meant.

Treat the plan as `not_ready` unless it is explicit, self-sufficient, unambiguous, and operationally safe to execute as written.

## Read first

- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/compatibility-policy.md`
- `../references/ownership-and-reuse-policy.md`
- `../references/final-state-authoring-policy.md`
- `../references/initiative-workflow-contract.md` when reviewing an initiative child packet
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter
- current task packet, especially `PLAN.md`

## Review standard

A plan is `ready` only when all of the following are true:

- every important term, artifact, and target outcome is explicit
- no step requires guessing intent from prior conversation
- the implementer can execute each step without hidden assumptions
- the plan does not contain choice-language where a decision should already be made
- the plan is clear enough that a competent agent can follow it in a clean context window without asking follow-up questions
- the plan keeps ownership and reuse explicit enough to avoid parallel same-purpose implementations
- the plan reads like one current target design instead of a migration diary or old/new hybrid

## Core workflow

1. Establish the real execution context.
   - Review the provided `PLAN.md` text only.
   - Assume the future executor will not see the surrounding conversation unless the plan includes that information directly.
2. Run an ambiguity pass.
   - Find wording that permits more than one reasonable interpretation.
   - Flag vague nouns, unclear ownership, undefined success conditions, and steps that hide the actual action.
3. Run a self-sufficiency pass.
   - Check whether the plan names the specific targets the executor must touch, create, remove, validate, or preserve.
   - Check whether it embeds the semantic decisions the executor would otherwise need to reconstruct.
4. Run a no-choice-language pass.
   - Flag `or`, `and/or`, `if needed`, `if appropriate`, `where possible`, `as necessary`, `consider`, `maybe`, `might`, `could`, and similar wording when used in execution instructions.
   - Allow choice-language only when the plan is explicitly presenting options to the human for a decision.
5. Run a standards pass.
   - Confirm the plan uses imperative decisions instead of advisory suggestions.
   - Confirm success criteria, validation, failure behavior, and stop conditions are explicit when they matter.
   - Confirm packet expectations are clear enough for `implement-task` and the review phases.
6. Run artifact and residue hygiene passes.
   - Flag prose that tries to become a second source of truth instead of staying in code/tests or tracked `AGENTS.md`.
   - Flag places where likely durable semantic/navigation residue is being ignored and should be called out for later capture.
7. Run an ownership-and-reuse pass.
   - Check whether the plan identifies the current owner for each important behavior or invariant.
   - Flag plans that introduce a new same-purpose helper/service/adapter/store/module/type without justifying a non-overlapping boundary.
   - Flag plans that should do a tidy-first refactor for reuse but instead jump straight to parallel implementation.
   - Flag plans that would leave future changes split across multiple same-purpose owners.
8. Run a compatibility-policy pass.
   - If the plan adds backward-compatibility work for an internal-only change, mark that as unnecessary complexity.
   - If the plan touches a real external boundary but never resolves whether backward compatibility is required, mark the plan `not_ready` and require explicit human clarification.
   - If the plan includes compatibility shims, aliases, dual support, or fallback behavior without explicit human requirement, mark that as a finding.
9. Run a final-state-authoring pass.
   - Flag plans that teach both an old and a new model when one chosen target model should be written directly.
   - Flag superseded vocabulary, owner splits, or status models that survive only as evolutionary residue.
   - Flag canonical plan prose that reads like patch notes instead of the intended steady-state contract.
10. Run a handoff-readiness pass.
   - Simulate a new agent receiving only this plan in an empty context window.
   - If that agent would need even one material follow-up question to avoid guessing, mark the plan `not_ready`.
11. Write or update `PLAN_REVIEW.md`.

- Emit compact `P#` findings.
- Include a `ready` / `not_ready` verdict.
- When residue hygiene is relevant, call it out explicitly instead of assuming later phases will infer it.

12. Update `INDEX.md` if packet status changed.

## Review heuristics

Treat these as likely findings unless the plan resolves them explicitly:

- unnamed files, modules, artifacts, systems, deliverables, or owners
- pronouns whose referent is not obvious
- steps that imply hidden prerequisites
- validation that says only `test it` or `verify it`
- steps that bundle unrelated actions without clarifying dependency
- instructions that describe intent but not the required action
- references to `standard`, `existing pattern`, or `usual approach` without naming what that means here
- acceptance criteria that depend on subjective judgment but provide no rubric
- compatibility shims, aliases, or dual-support steps with no explicit external-boundary requirement
- plans that fail to state whether backward compatibility is required when the task changes a real external contract
- plans that add a second same-purpose entity instead of reusing or tidying the existing owner
- plans that never name the authoritative owner for an important behavior or invariant
- plans that preserve old/new vocabulary or status names inside the canonical target contract

## Acceptance bar

Approve only when the plan is all of the following:

- unambiguous
- self-contained
- directive rather than suggestive
- explicit about expected output and validation
- free of hidden assumptions
- ready to hand off unchanged to another agent
- explicit about owner and reuse strategy where the task could otherwise fork into parallel implementations
- written as the target-state contract rather than as notes about how to patch the previous shape

If the plan is strong but still requires even one material guess, do not approve it.

## Requester-response rule

Always report the review result back to the requesting side.

- If the lead/orchestrator requested the review, reply back to the lead/orchestrator.
- If a human directly requested the review in this pane, reply back in this pane.
- Local pane output without an explicit reply to the requester does not count as review completion.

## Output shape

Default `PLAN_REVIEW.md` should include:

- verdict: `ready` or `not_ready`
- compact `P#` findings ordered by severity
- explicit required changes
- preserve-notes for good constraints that should survive rewrites

## Review rules

- Be strict. Do not pass a plan because the intended meaning seems obvious from conversation context.
- Quote exact ambiguous wording when possible.
- Prefer concrete rewrite instructions over generic advice.
- Evaluate the written plan, not the underlying project.
- Do not invent missing context to rescue the plan.

## Do not

- rescue the plan with remembered chat context
- rewrite tracked `AGENTS.md`
- write `AGENTS.override.md`
- treat vague validation like `test it` as acceptable
- approve a plan whose sequencing depends on intuition
- confuse `probably workable` with `ready for blind handoff`
- allow internal-only backward-compatibility work to slip through as harmless polish
- allow parallel same-purpose entities to slip through as harmless decomposition
- approve canonical plan prose that still carries obvious evolution residue when the final model is already known

## Initiative child packet checks
For initiative-created child packets also verify:
- `PLAN.md` is not still the placeholder `Status: not_authored`
- the plan is aligned with `Parent Initiative` and `Imported Context`
- repo scope, dependencies, and contract surface are explicit
- optional `CONTRACT_DECISION.md` is actually reflected when present

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
