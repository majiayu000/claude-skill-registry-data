---
name: platform-prd-builder
description: Build or improve professional PRDs, BRDs, requirement sections, and product decision artifacts from rough Chinese/English notes, prototypes, historical PRDs, meeting notes, or early ideas. Use when the user is ready to write, rewrite, translate, structure, enrich, or polish requirement content, especially for platform capability, workflow, configuration, governance, cross-system, or fintech product work. Invoked internally by platform-product-orchestrator, or directly when the user names this skill; for a natural-language request that does not name a skill, platform-product-orchestrator is the entry point.
---

# Platform PRD Builder

Use this skill to convert rough input into structured, implementation-ready product requirements. Do not simply translate. Understand, reorganize, enrich, and preserve precise scope.

## Operating Modes

Choose the lightest mode that satisfies the request:

- Full PRD build: create a complete PRD for a complex or cross-system requirement.
- Section build: write only requested sections such as background, scope, flow, API/data changes, or rollout.
- Rewrite / polish: improve structure, clarity, English, or bilingual wording without changing decisions.
- Input normalization: convert scattered notes into confirmed decisions, assumptions, missing decisions, and engineering-readable language before drafting.
- Template fit: choose the right artifact type when the request is not necessarily a full PRD.
- Direction alignment draft: create a lightweight concept / alignment version before expanding into a full PRD.

## First Move

Briefly identify:

- business scenario
- platform capability
- involved systems
- current phase and exclusions
- artifact type: full PRD, PRD section, one-page BRD, bilingual draft, English rewrite, table, or flow description

If the user only asks for impact or feasibility, do not draft the PRD yet; use impact analysis first.

If the artifact type is unclear, propose the smallest useful artifact and continue unless that choice would create delivery risk.

## Step 0: Stage Detection

Before drafting, classify the user's stage:

- Idea only: create a direction alignment draft first.
- Scattered notes: normalize decisions, assumptions, and missing decisions first.
- Scope unsettled: route to `platform-scope-checker` before drafting current-phase requirements.
- Ready to draft: build the requested PRD or section.
- Existing draft: improve structure or route to `platform-prd-reviewer` if the user wants feedback.
- RFC detail request: keep product semantics in the PRD and route implementation specifics to engineering follow-up.

## Build Challenge Gate

Before turning a request into a build-heavy PRD, briefly challenge whether the same business goal can be achieved by:

- existing platform capability
- configuration
- operational process or temporary manual handling
- smaller workflow change
- phased rollout
- compatibility placeholder without full current-phase behavior

If the answer is unclear or the build risk is high, recommend a scope check before writing a full PRD.

## Two-Phase Delivery

For ambiguous, 0-to-1, or large cross-system requirements, prefer two phases:

1. Direction Alignment Draft: problem, target users/ops, platform capability, scope boundary, core flow, ownership, assumptions, and open decisions.
2. Detailed PRD: requirements by system, field/API/data changes, state/edge cases, rollout/operations, acceptance criteria, and risks.

Do not jump to the detailed PRD when core product direction, MVP boundary, or source of truth is still unsettled.

## When NOT to Use

Do not use this skill as the first move when:

- the business problem or target user is still contested; first clarify direction with `platform-product-guide`
- the question is "should we do this now?"; first use `platform-scope-checker`
- the user only wants review feedback on an existing artifact; use `platform-prd-reviewer`
- the request is a pure engineering RFC, code design, or implementation plan with no product requirement work

## PM Input Normalizer

When input is vague, non-technical, or written as scattered notes, first translate it into engineering-readable product decisions before drafting. Do not require the user to use technical vocabulary.

Use this lightweight output when decisions are missing:

```md
Known Decisions
- ...

Missing Decisions
- ...

Engineering-Relevant Translation
- "Need approval record" means audit log fields, write timing, query access, and retention need decisions.
- "Notify another system" means callback timing, retry, timeout, failure handling, and status consistency need decisions.
```

Ask business-language questions instead of technical-label questions:

- Instead of "What is the idempotency key?", ask "If the same request is submitted twice, should the system create a new record, reject it, or return the existing one?"
- Instead of "What is the callback retry strategy?", ask "If the receiving system cannot be notified, what should users see, who fixes it, and how long can it remain unresolved?"
- Instead of "Who is the source of truth?", ask "If two systems show different statuses, which one should be trusted?"
- Instead of "What is the compatibility strategy?", ask "Will existing records or in-flight processes be affected after launch?"
- Instead of "Define a state machine", ask "What statuses can this request have from creation to completion, and what actions are allowed in each status?"

## Assumption and Evidence Ledger

When important decisions are inferred from rough notes, surface them before finalizing:

```md
Assumptions
- A1: ...

Evidence / Source
- E1: From user note / prototype / prior PRD / meeting note / explicit instruction

Needs Confirmation
- C1: ...
```

Do not silently turn assumptions into requirements. If the user asks to proceed, keep unresolved items in Open Questions with owner/dependency when known.

## Template Selection

Choose the template by artifact type instead of forcing one heavy structure.

Short feature PRD:

- Background
- Objective
- Scope
- Requirements
- API / Data Changes
- Edge Cases
- Attachment / Links

API / field change note:

- Background
- Changed Contract
- Field Table
- Validation / Default Behavior
- Backward Compatibility
- Downstream Consumers
- Examples

Configuration UI PRD:

- Background
- Goal
- Page Path / Entry
- List Fields
- Filter / Query Behavior
- Create / Edit Behavior
- Validation Rules
- Permission / Audit
- Attachment / Prototype

Migration PRD:

- Background
- Scope
- Source / Target Systems
- Migration Flow
- Data Mapping
- Validation / Reconciliation Checklist
- Cutover / Rollback
- Open Questions

Formula / rule logic PRD:

- Background
- Rule Format
- Field Definitions
- Processing Logic
- Examples
- Edge Cases
- Backward Compatibility

## Default PRD Structure

Use this structure unless the user gives a different template:

1. Background
2. Goal
3. Scope
4. Actors / Systems
5. Overall Flow
6. Flow Details
7. Requirements by System
8. API / Data Changes
9. Scenarios & Edge Cases
10. Rollout / Operations
11. Open Questions
12. Dependencies / Risks

For short sections, keep only the relevant headings but preserve the same thinking order.

## Use Platform Flow Modeler When

Use `platform-flow-modeler` before writing Overall Flow, Flow Details, Scenarios & Edge Cases, State Transition, or Operations sections when the requirement involves 3+ systems, lifecycle/status changes, callback/retry/timeout, rollback/cancel/resubmit, reconciliation, settlement, migration, or manual fallback.

Let it shape flow tables first, then convert those tables into PRD prose, requirements by system, scenarios, acceptance criteria, and open questions.

## Output Contract

Every PRD-style output should make these things testable:

- Problem and "why now"
- Current-phase goal
- Scope boundaries
- Main flow and key exception flows
- Product decisions still open
- Acceptance criteria or scenario matrix
- Owner/source-of-truth for cross-system behavior
- Rollout, rollback, or temporary manual handling when relevant

Default response shape:

1. Brief note on selected artifact type, when useful
2. Drafted PRD content or requested section
3. Assumptions and open decisions, if any
4. Suggested next review route: scope check, PRD review, RFC follow-up, or stakeholder confirmation

This skill should produce an artifact, not only advice. If the artifact cannot be produced safely, output the missing-decision ledger and the next action instead.

For detailed PRD templates and artifact-specific output contracts, read `references/prd-output-contract.md` when the task involves a full PRD, 0-to-1 platform PRD, migration PRD, configuration UI PRD, or API/data change note.

## Scenarios & Acceptance Criteria

For Scenarios & Edge Cases sections, use Given/When/Then acceptance criteria when it improves QA and engineering alignment:

```md
**Scenario: [name]**
- Given: [precondition: system state, actor, data, configuration]
- When: [trigger action]
- Then: [expected result: final status, user/ops-visible outcome, downstream sync, audit record]
```

Cover these scenario types when relevant:

- Happy path
- Validation failure: missing field, invalid value, duplicate submission
- Downstream system failure: callback timeout, API error, partial failure
- Concurrent or duplicate submission
- Status transition edge case: resubmission from terminal state, mid-flow cancellation
- Rollback or reversal
- Manual fallback: ops intervention or exception queue entry
- Permission boundary: actor not allowed or source-system mismatch

Make each `Then` clause testable. Name the final status, the user/ops-visible result, whether downstream systems are notified, and whether an audit/event record is created.

If the scenario matrix would be large, use a compact table:

| Scenario | Precondition | Trigger | Final Status | User/Ops Result | Downstream | Audit |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## API / Data Table Style

For API or data changes, default to tables with:

- Field
- Data Type / Type
- Mandatory
- Value / Validation
- Description
- Example
- Change Type: new / existing / removed, when relevant
- Owner / Consumer, when ownership matters

## 0-to-1 Platform PRD Additions

For new platform/infrastructure capabilities, add:

- platform direction and design principles
- configuration objects vs runtime objects
- ownership/source-of-truth table
- lifecycle/state machine
- versioning and snapshot behavior
- callback, retry, timeout, and idempotency behavior
- audit/event logging
- permission and source-system isolation
- MVP exclusions and future iteration
- UI/workspace model by role, data scope, and operational region

## Writing Rules

- Convert rough notes into professional English when English output is requested.
- Preserve Chinese/English mixed terminology when it reflects real system names or team artifacts.
- Add missing explanation needed for readers to understand and implement, but do not invent business decisions.
- If input quality is uneven, normalize it into business layer and engineering collaboration layer before writing the final PRD.
- Use numbered hierarchy for reviewability.
- Use tables for fields, APIs, ownership, scenarios, calculations, status transitions, and open questions.
- Separate requirements by system when multiple systems change.
- Keep product-readable sections product-readable; move low-level details into API/data sections or open questions.
- Follow provided prototypes or existing PRD structure when the user says to base work on them.

## Scope Discipline

Always separate:

- `In Scope`
- `Out of Scope`
- `Not Supported in This Phase`
- `Future Iteration`

Do not include future-phase features in current-phase requirements except as explicit exclusions, compatibility notes, or future iteration.

## Flow and Data Requirements

For cross-system work:

- describe creation/query/callback/update/settlement/reconciliation flows separately when relevant
- identify persistence points and status changes
- define configuration-time fields separately from runtime fields
- distinguish snapshot fields from dynamically resolved fields
- use field names carefully; singular/plural naming may encode scope, such as `portalCode` vs `portalCodes`

## Guardrails

- Treat historical PRDs as learning/reference material unless the user asks to rewrite them.
- Do not inject unrelated context from previous projects.
- Do not output code when the user asks for requirements.
- Do not over-polish into marketing language.
- Do not hide open decisions; list them clearly with owner/dependency when known.

## Common Mistakes to Flag

- Drafting detailed requirements before direction alignment is ready.
- Turning assumptions into requirements without labeling them.
- Mixing current MVP with future iteration behavior.
- Writing only page/button behavior while leaving states, ownership, and exception handling implicit.
- Over-prescribing database, queue, retry job, or service design in the PRD.
- Treating an implementation request as product-ready without checking the business goal and scope boundary.

## Routing

- Route to `platform-product-guide` when business direction, platform abstraction, or decision framing is not ready.
- Route flow-heavy sections to `platform-flow-modeler` before converting them into PRD content.
- Route to `platform-scope-checker` when current-phase inclusion, MVP size, or hidden complexity is unresolved.
- Route to `platform-prd-reviewer` after drafting when the user wants readiness, gaps, or score.
- Route RFC-level implementation questions to engineering follow-up while keeping product semantics in the PRD.

## Quality Checklist

Before finalizing, verify:

- [ ] The document explains what to build and why.
- [ ] Scope is explicit: in scope, out of scope, not supported now, future.
- [ ] Requirements are testable enough for QA or engineering review.
- [ ] Cross-system ownership and source of truth are visible.
- [ ] Assumptions are separated from confirmed decisions.
- [ ] Technical considerations are surfaced without over-prescribing implementation.
- [ ] The next route or review step is explicit.

## References

- `references/prd-output-contract.md`: load when a detailed template, artifact-specific contract, or quality checklist is needed.
