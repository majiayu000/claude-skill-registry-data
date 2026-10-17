---
name: implementation-checkpoint-planner
description: Adds evidence-based review checkpoints after risky, foundational, irreversible, or cross-cutting implementation work so defects and invalid assumptions are caught before dependent tasks proceed. Use when the user asks to add review gates to an implementation plan, identify where work should pause for validation, define go/no-go criteria, protect downstream tasks from unstable foundations, or strengthen a plan that postpones review until the end.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: software-teams-technical-leads-and-coding-agents
  tags:
    - implementation-checkpoints
    - review-gates
    - risk-management
    - validation
    - dependencies
    - quality-assurance
  status: draft
  side_effects: none
---

# Implementation Checkpoint Planner

## Purpose

Insert targeted review points into an implementation sequence after work whose failure would invalidate, misdirect, or create rework for downstream tasks. Define what must be reviewed, what evidence is required, who or what performs the review, and the conditions for continuing, revising, or stopping.

This is a planning-only skill. It strengthens an existing or provisional implementation sequence; it does not implement changes or turn every task into a mandatory approval ceremony.

## When to use this skill

Use this skill when:

- An implementation plan contains foundational work that many later tasks depend on.
- Architecture, contracts, schemas, migrations, integrations, security controls, or shared UI patterns need validation before expansion.
- The user asks for review gates, pause points, go/no-go criteria, sign-offs, or staged validation.
- A long plan defers integration, accessibility, performance, security, or stakeholder review until the end.
- Multiple contributors or agents need explicit synchronization points before dependent work begins.
- A mistake would become substantially more expensive after later tasks build on it.

Example triggers:

- “Add checkpoints to this implementation plan.”
- “Where should we pause and review before continuing?”
- “Catch architectural mistakes before later tasks depend on them.”
- “Define go/no-go gates for the risky parts of this build.”
- “Which steps need human review or integration proof?”

Do not use this skill when:

- The user needs a complete implementation plan from requirements; use `implementation-plan-writer` first.
- The main decision is what to build first; use `implementation-order-planner`.
- The user wants a high-level roadmap or milestone structure; use `project-roadmap-builder` or `milestone-planner`.
- The task is implementation, code review, or test execution rather than planning review gates.
- Routine, low-risk, reversible work has no meaningful downstream dependents.

## Inputs to inspect

Start with the smallest useful evidence set:

- The implementation plan, roadmap, backlog, issue sequence, or task list to strengthen.
- Requirements, acceptance criteria, non-goals, and intended user outcomes.
- Dependency relationships and the tasks that consume each deliverable.
- Architecture decisions, API contracts, schemas, migrations, integration boundaries, and shared abstractions.
- Known risks, assumptions, irreversible choices, security or privacy concerns, and operational constraints.
- Existing validation options: tests, prototypes, builds, static analysis, manual QA, accessibility checks, performance measurements, migration rehearsals, or stakeholder review.
- Ownership and review constraints, including required subject-matter experts or external approvals.

If no implementation sequence exists, derive only the minimal provisional sequence needed to place checkpoints and label it as an assumption.

## Checkpoint selection model

Add a checkpoint when both conditions are true:

1. The preceding work has meaningful uncertainty, blast radius, irreversibility, or cross-cutting impact.
2. Later work would rely on its correctness, stability, usability, or approved direction.

Prioritize these checkpoint candidates:

| Candidate | Typical examples | Evidence to require before continuation |
|---|---|---|
| Foundation | Architecture seam, shared abstraction, design system primitive, build pipeline | Small real consumer works; assumptions and extension points are reviewed |
| Contract or boundary | API, event, schema, external service, authentication flow | Contract or integration test passes; failure behavior is demonstrated |
| Irreversible change | Data migration, destructive transform, public API, storage format | Dry run, backup and rollback proof, compatibility check, owner approval |
| Cross-cutting quality | Security, privacy, accessibility, performance, observability | Relevant focused checks pass against explicit thresholds or criteria |
| User-visible direction | Core workflow, interaction pattern, content model | Representative scenario is usable and accepted before broad replication |
| Coordination boundary | Multi-agent or multi-team handoff, shared files, shared contract | Deliverable is integrated, ownership is clear, downstream assumptions match |

Do not add a checkpoint solely because a phase ends. A useful checkpoint protects a concrete dependency or decision.

## Workflow

1. Establish the planning boundary: identify the target plan, delivery horizon, intended implementers, and fixed constraints.
2. Map dependencies. For each task or work package, identify which later items consume its outputs or assume its correctness.
3. Mark risk-bearing work. Look for high uncertainty, large blast radius, irreversibility, new boundaries, shared foundations, regulatory or safety impact, and expensive rework potential.
4. Find the last responsible review point. Place the checkpoint after enough work exists to produce meaningful evidence but before dependent expansion makes correction costly.
5. Merge overlapping checkpoints. Combine gates that review the same deliverable at the same boundary; keep separate gates when they protect different decisions or require different evidence.
6. Define the checkpoint question. State the decision the review must answer, not merely “review the work.”
7. Specify required evidence. Name observable artifacts, tests, measurements, demonstrations, diffs, approvals, or traceable acceptance criteria.
8. Assign the review mechanism. Identify automated checks, peer review, specialist review, stakeholder validation, or a combination. Name a role rather than inventing a person.
9. Define outcomes:
   - `continue`: evidence meets the exit criteria and named downstream tasks may begin.
   - `revise`: bounded problems require rework and re-review before dependents begin.
   - `replan`: evidence invalidates an assumption or architecture choice and the downstream sequence must change.
   - `waive`: only when an authorized owner explicitly accepts the residual risk and records the reason.
10. Hold downstream work explicitly. List the tasks blocked by the checkpoint and any work that can safely proceed in parallel.
11. Check proportionality. Remove gates whose review cost exceeds the plausible cost of failure, and prefer automated evidence for repeatable low-judgment checks.
12. Audit coverage. Confirm that each foundational or high-risk item has an early enough checkpoint and that the plan does not rely on one generic final review.
13. State assumptions and unresolved ownership. Do not claim a gate is enforceable if the reviewer, evidence source, or decision authority is unknown.

## Checkpoint design rules

- Make each checkpoint decision-oriented and passable; avoid vague instructions such as “verify everything looks good.”
- Require the smallest evidence set that can expose the important failure mode.
- Attach validation to the work that creates the risk, not to a distant final QA phase.
- Prefer working vertical evidence over document approval alone when runtime behavior matters.
- Separate automated checks from judgment calls so neither is mistaken for the other.
- Name downstream tasks that must wait; a gate with no controlled dependency is only a suggestion.
- Include rework and replanning paths, not only pass criteria.
- Avoid requiring human sign-off for checks that reliable automation can decide.
- Never use a checkpoint to conceal unresolved requirements; surface the decision task before implementation.

## Output format

Return the result using this structure:

```md
## Summary

- Checkpoints added: ...
- Highest-risk dependency protected: ...
- Main coverage gap in the original plan: ...

## Risk and dependency map

| Work item | Risk or assumption | Downstream dependents | Checkpoint needed? | Rationale |
|---|---|---|---|---|
| ... | ... | ... | yes / no | ... |

## Revised sequence with checkpoints

1. **Work item** — deliverable and validation performed during the work.
2. **Checkpoint: [decision question]**
   - Reviews: ...
   - Required evidence: ...
   - Review mechanism / owner role: ...
   - Continue if: ...
   - Revise if: ...
   - Replan if: ...
   - Blocks: ...
   - Safe parallel work: ...
3. **Dependent work item** — begins only after the checkpoint passes.

## Checkpoint register

| ID | After | Decision | Evidence | Owner role | Continue criteria | Blocks |
|---|---|---|---|---|---|---|
| CP-1 | ... | ... | ... | ... | ... | ... |

## Assumptions and unresolved decisions

- ...
```

For a short plan, omit the separate register if it would duplicate the revised sequence. If the user asks only for candidate checkpoint locations, provide a concise annotated list while preserving decision, evidence, and dependency details.

## Quality bar

The task is complete only when:

- Every checkpoint protects a named risk, assumption, foundation, or downstream dependency.
- Checkpoints occur after evidence can exist and before costly dependent expansion.
- Each checkpoint asks a concrete decision question.
- Required evidence is observable and proportionate to the risk.
- Continue, revise, and replan conditions are explicit where applicable.
- Blocked downstream work and safe parallel work are identified.
- Automated validation, specialist review, and stakeholder approval are distinguished.
- Duplicate, ceremonial, and low-value gates are removed.
- Foundational and cross-cutting concerns are reviewed before broad reuse or rollout.
- Assumptions, missing evidence, owner roles, and waived residual risks are visible.

## Edge cases

- If every task appears risky, rank by downstream impact and irreversibility; do not gate every small step.
- If evidence requires later work, create the smallest proof, fixture, consumer, or vertical slice needed to make the checkpoint meaningful.
- If a deadline prevents a full review, define a reduced evidence set, record residual risk, and require an explicit waiver owner.
- If no qualified reviewer is available, mark the checkpoint unresolved and avoid inventing approval authority.
- If parallel work depends on an unstable contract, allow only work behind a disposable stub or clearly versioned assumption.
- If a checkpoint fails, revise the plan and re-evaluate later checkpoints instead of blindly resuming the original sequence.
- If compliance or safety rules mandate a gate, retain it even when a simple cost-of-failure analysis would remove it.
- If the plan already includes tests, verify that they produce evidence at the correct dependency boundary rather than assuming test presence equals checkpoint coverage.

## Related skills

- `implementation-plan-writer`
- `implementation-order-planner`
- `milestone-planner`
- `project-roadmap-builder`
- `agent-workstream-planner`
