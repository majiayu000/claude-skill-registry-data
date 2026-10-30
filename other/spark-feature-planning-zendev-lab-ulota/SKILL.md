---
name: spark-feature-planning
description: Use when designing a Spark feature or writing or materially revising a design proposal that needs repository-first research, user input on unresolved key choices, and an owner-aligned implementation plan before code changes.
---

# Spark feature planning

Turn a requested capability into an evidence-backed decision and the smallest
plan that can prove it.

## Procedure

1. Reconstruct the user problem and current behavior from the owning code, specifications, package README, nearby tests, and machine-readable inventory.
2. Separate repository facts, external facts, assumptions, constraints, and unresolved product decisions. Research questions whose answers can change the selection or acceptance boundary before drafting a direction. Verify external claims against current primary sources such as official documentation, source code, or papers; record sources and applicable versions. If necessary evidence is unavailable, identify the gap and continue only work independent of it.
3. Compare the status quo and viable options against owner fit, semantic duplication, dependency direction, compatibility cost, lifecycle and failure modes, operational burden, and validation cost.
4. Before settling a proposal or plan, obtain unresolved choices that materially change behavior, authority, or irreversible cost. Present viable options with a recommendation, evidence, and the main tradeoffs; raise root choices before dependent questions. Do not ask for facts available from the repository or manufacture options to fill a list. When the current Session has `ask`, use `ask` with those options, recommendation, and tradeoffs. When it does not, return structured `needs-decision` with the same options, recommendation, and root-question order so the caller can ask. That return completes this planning step; it does not mean a choice has been obtained.
5. Select a direction only after obtaining the key choices. Reuse explicit user choices and applicable existing decisions without asking again; cite their basis. If the user explicitly delegates a choice, decide within those constraints and record the delegation and rationale. A request to write a proposal alone is not a choice or delegation. Explain why rejected options lose without inventing future requirements.
6. Produce a dependency-ordered plan whose first slice proves the highest-risk behavior. Name the owner, affected surfaces, observable acceptance criteria, failure cases, compatibility evidence, documentation owner, and validation commands. Apply the writing checks below without changing the caller's output contract.
7. Keep adjacent cleanup and speculative extensibility out of the feature plan. Record them as rejected or out of scope rather than prebuilding them.

## Writing checks

Use the owning specification's preferred terms and distinguish current behavior,
proposed contracts, and observed results. State the actor, object, condition scope,
counting boundaries, and failure behavior when they affect a choice or acceptance
criterion. Preserve negation, ordering, exceptions, and uncertainty when revising.
Missing retry semantics, ownership, or thresholds remain evidence gaps or questions;
do not invent them to complete a sentence.

Keep reasoning in connected prose and use steps for ordered actions. Express
acceptance through observable behavior rather than unqualified claims such as
"more reliable". Follow any applicable document template without adding a proposal
numbering system, lifecycle, or mandatory document to Spark's planning workflow.

## Decision handoff

Until the key choices are obtained, mark the dependent selection and plan
`needs-decision`. Treat silence as no choice, not agreement. Do not implement
the dependent behavior while waiting. Editorial corrections and implementation
of existing decisions do not reopen settled choices or require a new proposal.

Put source citations and applicable versions in `problemEvidence`. Put the
basis of each selection, including reused decisions, explicit user choices,
and delegations, in `selection`. When verdict is `needs-decision`, `options`
holds the viable options and tradeoffs, `selection` holds the recommendation
and why, and `openQuestions` holds the root-question order for the caller.

A user choice establishes the design direction, not proposal acceptance or
implementation authority. Return `problemEvidence`,
`options`, `selection`, `plan`, `acceptanceCriteria`, `risks`, `outOfScope`,
`validationCommands`, `openQuestions`, and `verdict`.
