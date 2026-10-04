---
name: documenter-coauthoring
description: "Companion overlay to documenter for user-directed, multi-round coauthoring of specs, PRDs, proposals, ADRs, decision docs, and similar technical documents. Use when the user wants to shape or approve structure, set checkpoints, iterate section by section, or preserve decisions across rounds. Document size neither selects nor excludes it. Do not use alone or for autonomous one-pass drafting or review."
---

# Documenter Coauthoring

Add this to `documenter`; it changes collaboration, not documentation rules.

## Workflow

1. Establish the working state:
   - read supplied files and existing docs before asking discoverable questions
   - infer the audience, outcome, template, constraints, and output target
   - invite an unstructured context dump when useful
   - ask one batched set of questions only for unknowns that materially affect
     the next checkpoint
   - track the accepted outline and sections, decisions, general preferences,
     assumptions, open questions, delegated authority and its limits, checkpoint
     cadence, and next action
   - on resume, or before switching from chat-only draft to applied edits,
     refresh the canonical artifact, relevant evidence, repository state, and
     initial diff; mark affected accepted sections stale when material evidence
     or decisions changed
2. Agree on structure and user control:
   - confirm and reuse an established structure; when structure is unresolved,
     propose an outline with material alternatives, assumptions, and a
     recommendation
   - derive checkpoint cadence from the request; if it is unspecified, propose
     the smallest useful next checkpoint
   - let the user approve, revise, waive, or delegate checkpoints and decisions
   - treat delegation as authority to skip covered pauses, not as authority to
     hide ripple effects, weaken evidence or safety checks, or cause external
     side effects
   - pause only at an agreed checkpoint or for a material choice outside
     delegated authority; do not add gates because the document is large or
     uncertain
3. Draft the agreed section or logical tranche:
   - work in dependency order; prototype a high-uncertainty section first only
     when it could change the outline
   - write summaries after the decision and evidence are stable, then place them
     where readers need them
   - preserve accepted material and decisions
   - treat section-specific feedback as local; carry clearly general preferences
     such as tone, terminology, or audience forward, and ask only when their
     scope is materially ambiguous
   - surface ripple effects before changing an accepted decision; when delegated
     authority covers the change, disclose them without adding a checkpoint and
     mark affected accepted sections stale until reconciled
4. Reconcile at each checkpoint:
   - keep one canonical artifact rather than parallel conflicting drafts
   - show the current tranche or changed blocks during iteration while keeping
     the complete artifact coherent at milestones and completion
   - report what changed, current decisions and assumptions, unresolved material
     questions, validation state, and the next proposed action or gate
5. Finish or hand off:
   - apply the baseline validation rules
   - before declaring completion, perform a cold-read pass against the named
     audience and task without relying on conversational context; report it as
     self-review, not an independent fresh-reader test
   - declare completion only when the baseline completion criteria and cold-read
     pass are satisfied; seek approval at an agreed completion checkpoint, or
     complete autonomously within delegated authority
   - when the user pauses or requests a handoff, return the working state needed
     to resume and do not claim the document is complete
