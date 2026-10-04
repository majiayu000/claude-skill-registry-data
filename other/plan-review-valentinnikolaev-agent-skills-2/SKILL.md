---
name: plan-review
description: Review an implementation plan for feasibility and gaps without edits. Use review-spec for designs and code-review for diffs.
---

# Plan Review

Review an implementation plan against requirements, repository evidence, architecture, risks, and verification expectations. Do not edit files or rewrite the plan.

## Route exclusively

- Use this skill when the primary artifact is an implementation plan, including a plan revised during ongoing work.
- Use `code-review` when the primary request is to inspect changed code or a diff.
- Use `review-spec` when the primary artifact is a specification or design proposal rather than an ordered plan.
- Use `review-arch` for system architecture without an implementation plan, and `verify-impl` for completed code against a spec.
- Use `fix-pr` when the user asks to triage or apply GitHub pull-request feedback.
- If no plan can be identified in the request, conversation, or supplied file, ask for it instead of inventing one.

## Choose one mode

Default to `deep` unless the user requests another mode.

- `quick`: verify the goal, explicit requirements, referenced artifacts, and blockers. Emit only Validation, Verdict, Blockers, Questions, and Requirements Traceability.
- `deep`: also inspect applicable architecture, data flow, security, failure handling, tests, scope, and up to three useful local comparables. Emit every report section.
- `final`: assume the plan is nearly ready and try to break it with production edge cases, migration and rollback failures, concurrency, observability, and recovery gaps. Emit every report section and a Release Risks section.

For `quick`, inspect only the plan, explicit requirements/instructions, and directly referenced files. For `deep` or `final`, inspect only enough repository context to verify material claims. Do not fill a comparison quota with irrelevant files.

## Load evidence

1. Identify the plan source and give each step a stable label if it lacks one.
2. Read applicable repository and path-scoped instructions.
3. Read explicit acceptance criteria, PRDs, issue text, or requirements supplied by the user or repository.
4. Verify referenced files, symbols, dependencies, commands, and directories.
5. Read comparable implementations only when the plan relies on a local pattern.
6. Record missing, inaccessible, or conflicting sources as limits; do not silently choose between conflicting authoritative sources.

Do not manufacture requirements or repository facts. When no explicit requirements exist, state that requirements traceability is limited to the stated goal and plan.

## Validate the plan

Check applicable concerns:

- each acceptance criterion maps to a plan step;
- steps do not add unrequested functionality;
- assumptions about current code and behavior match repository evidence;
- dependencies, interfaces, data ownership, and operation ordering are viable;
- security, privacy, authentication, and authorization boundaries are explicit;
- destructive changes include migration, rollback, and recovery;
- partial failures, retries, idempotency, concurrency, and edge cases are handled;
- tests and verification cover changed behavior and likely failure modes;
- safe parallel work is identified without obscuring dependencies;
- existing infrastructure is reused when it is the established fit.

Report only issues that improve correctness, safety, completeness, or maintainability. Omit preferences and speculative alternatives.

## Evidence and finding contract

Use stable IDs `PLAN-001`, `PLAN-002`, and so on. For every finding include:

- `Priority`: `P0`, `P1`, `P2`, or `P3`;
- `Disposition`: `open`, `question`, `accepted-risk`, or `not-applicable`;
- exact plan step and a short verbatim excerpt;
- requirement or repository evidence with `file:line` when available;
- concrete implementation risk;
- smallest plan-level remediation or a precise question.

Priority meanings:

- `P0`: the plan enables an immediate safety, security, or irreversible-loss hazard.
- `P1`: a blocker likely to make implementation incorrect, unsafe, or unrecoverable.
- `P2`: a material risk or missing behavior to resolve before executing the affected plan steps.
- `P3`: a small evidence-backed improvement.

Map report sections consistently: `P0` and `P1` open findings are Blockers; `P2` findings are Warnings; `P3` findings are Suggestions. Questions retain the priority of the risk they could reveal.

## Decide the verdict

- `APPROVE`: no open `P0` or `P1` findings, no unanswered question required to implement safely, and verification limits are acceptable.
- `REVISE`: the plan is identifiable and reviewable but needs correctable changes before implementation.
- `BLOCKED`: the plan or authoritative evidence is missing, irreconcilably conflicting, or inaccessible enough that a responsible verdict cannot be reached. A dangerous plan with confirmed defects is `REVISE` with blockers, not `BLOCKED` merely because it is poor.

Never use `APPROVE` to mean that implementation itself has been verified.

## Report

Use only the sections required by the selected mode:

```text
## Plan Review: <summary>

### Validation
- Mode: quick | deep | final
- Plan source: <source>
- Requirements: <sources or limits>
- Repository instructions: <sources>
- Referenced artifacts: <verified or missing>
- Comparables: <deep/final only; useful files or none>

### Verdict
APPROVE | REVISE | BLOCKED — <one-sentence basis>

### Blockers
ID: PLAN-001
Priority: P1
Disposition: open
Plan evidence: Step <id>, "<short excerpt>"
Repository/requirement evidence: <file:line or supplied criterion>
Risk: <concrete failure>
Remediation: <specific plan-level correction>

### Warnings
<deep/final only; same fields>

### Suggestions
<deep/final only; same fields>

### Questions
- PLAN-00N | Priority: P1 | Disposition: question | <question and missing evidence>

### Requirements Traceability
| Criterion | Plan step | Status | Evidence |
|---|---|---|---|
| <criterion> | <step> | Covered / Partial / Missing | <excerpt or source> |

### Release Risks
<final only; production, migration, rollback, and recovery residuals>

### Verification Limits
<deep/final only; sources or checks unavailable>
```

Omit empty issue sections. If no issues remain, say so and preserve the verdict basis and verification limits. Do not edit, reorder, or replace the plan; checkout branches; install dependencies; or run state-changing commands.
