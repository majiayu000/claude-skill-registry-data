---
name: sdd-plan
description: Use when planning delivery phases, milestones, dependencies, or exit gates, or when designing or reviewing a software project's repository layout, directory and package structure, and physical ownership of code, tests, and documentation. Produces or revises PLAN.md, FEATURE-PLAN.md, layout.md, and focused children before executable TASKS or FEATURE-TASKS are derived.
---

# Plan delivery and physical layout

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Apply the manager's [human document review](../sdd-manage/references/human-document-review.md) for PLAN and layout, including necessary feature strategy/placement proposals, including direct calls. Newly created necessary documents pause for substantive human review before dependent progression. Reuse acceptable existing inputs after startup assessment without automatic interactive replay; requested interactive review comes first. Agent QC and repository-operation authority do not supply human acceptance.

For preimplementation project authoring, have **sdd-manage** establish the dedicated design-docs branch under its [preparation integration gate](../sdd-manage/references/branch-management.md#preparation-integration-gate). Commit project documents and required QC reports there. Before a dependent implementation branch is created, the manager explicitly merges accepted preparation into the actual default branch, verifies and publishes that baseline. Campaign plans/reports remain on revision branches; active implementation and steering amendments preserve their working-branch ownership. Read-only work creates no branch.

Default to an early meaningful end-to-end MVP followed by small, testable capability increments; preserve the complete intended design and SPEC. Use the delivery reference for scope, prerequisite exceptions, and exit evidence.

Choose the requested work and load only its references. A request for complete delivery planning develops both PLAN and layout when physical ownership needs to be established; a focused request to review or revise one document does not automatically authorize rewriting the other.

Apply **sdd-conventions**' **Development-document QC** reference (`skills/sdd-conventions/references/development-document-qc.md`, bundled dependency). Authoring includes scoped review, correction/recheck and the adjacent report before dependent progression; pure review does not authorize corrections.

| Work | Load |
| --- | --- |
| Prepare both delivery strategy and physical placement for task derivation | [delivery plan](references/delivery-plan.md) and [physical layout](references/physical-layout.md) |
| Define or revise delivery strategy, phases, milestones, dependencies, or a scoped feature plan | [delivery plan](references/delivery-plan.md) |
| Define or revise physical ownership of implementation, tests, and documentation | [physical layout](references/physical-layout.md) |
| Review PLAN and layout consistency | [review](references/review.md) |

Before authoring, read the relevant PROJECT, ARCHITECTURE, DECOMPOSITION, SPEC, their focused children, and any existing PLAN and layout. Inspect relevant code, tests, and packaging for existing projects; distinguish observed placement from intended placement. If inputs conflict or a required behavioral or architectural decision is unresolved, identify its owner instead of silently settling it in PLAN or layout. Start at the requested operation when its inputs are established.

Read-only review can proceed without changing files. Creating, revising, or removing project documents requires **sdd-manage** to coordinate the user's request and a current **sdd-orient** handoff establishing an eligible Git worktree, applicable instructions, target paths, and ownership of dirty changes. This skill does not perform orientation or authorize another workflow.

PLAN owns delivery strategy and boundary verification; layout owns physical placement and ownership. SPEC owns behavior and acceptance; design owns logical structure; TASKS and an active FEATURE-TASKS own their respective stable, ordered execution units and progress. Use **sdd-conventions** when assessing component or task boundaries, without incorporating its shared rules here. Neither PLAN nor layout is a task checklist, a progress journal, or permission to implement. The downstream task workflow consumes the accepted design, SPEC, PLAN, and layout together.

Incorporation of an accepted FEATURE-PLAN into main PLAN or layout belongs to **sdd-integrate-feature**. Direct plan or layout corrections remain in their owning authoring workflows.

At completion, report the strategy or placement established, affected phases or ownership boundaries, unresolved material decisions, and documents inspected or updated. Describe proposed work as planned, not implemented.
