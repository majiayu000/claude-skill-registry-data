---
name: sdd-specify
description: Use when creating, reviewing, or revising docs/dev/SPEC.md, focused specification children, or FEATURE-SPEC.md; defining required software behavior, interfaces, data contracts, error semantics, invariants, and objective acceptance for a new or existing system.
---

# Specify required behavior

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Apply the manager's [human document review](../sdd-manage/references/human-document-review.md) for SPEC and FEATURE-SPEC, including direct calls. Newly created necessary documents pause for substantive human review before dependent progression. Reuse acceptable existing inputs after startup assessment without automatic interactive replay; requested interactive review comes first. Agent QC and repository-operation authority do not supply human acceptance.

For preimplementation project authoring, have **sdd-manage** establish the dedicated design-docs branch under its [preparation integration gate](../sdd-manage/references/branch-management.md#preparation-integration-gate). Commit project documents and required QC reports there. Before a dependent implementation branch is created, the manager explicitly merges accepted preparation into the actual default branch, verifies and publishes that baseline. Campaign plans/reports remain on revision branches; active implementation and steering amendments preserve their working-branch ownership. Read-only work creates no branch.

Choose the requested operation and load only its reference. Enter directly when adequate decisions and project evidence exist; do not replay design exploration as ceremony.

Apply **sdd-conventions**' **Development-document QC** reference (`skills/sdd-conventions/references/development-document-qc.md`, bundled dependency). Authoring includes scoped review, correction/recheck and the adjacent report before dependent progression; pure review does not authorize corrections.

| Work | Load |
| --- | --- |
| Create or revise the complete intended system specification | [system specification](references/system-specification.md) |
| Define a scoped change to existing specified behavior | [change specification](references/change-specification.md) |
| Review SPEC quality and identify conflicts | [review](references/review.md) |

Before authoring, identify accepted decisions and the relevant PROJECT, ARCHITECTURE, DECOMPOSITION, existing SPEC, and applicable focused children. For an existing implementation, inspect only relevant code and tests to establish observed behavior; do not promote an observation into a requirement without an accepted decision. If a material architectural boundary is undecided or governing sources conflict, return that decision to design or the user rather than inventing a contract.

Read-only review can proceed without modifying files. Creating, revising, or removing project documents requires **sdd-manage** to coordinate the user's request and a current **sdd-orient** handoff establishing an eligible Git worktree, applicable instructions, affected paths, and ownership of dirty changes. This skill does not implement orientation or authorize another workflow.

SPEC is authoritative for intended observable behavior and acceptance. PROJECT owns the brief; ARCHITECTURE and DECOMPOSITION own structural design; PLAN owns delivery strategy; TASKS and an active FEATURE-TASKS own their respective executable units; layout owns physical paths. Use **sdd-conventions** when evaluating contract boundaries and necessary decomposition, without moving those shared checks into SPEC procedure. A feature specification states a scoped intended delta; it does not silently replace the complete main SPEC.

Incorporation of an accepted FEATURE-SPEC into main SPEC belongs to **sdd-integrate-feature**. Direct SPEC corrections remain in the owning system specification workflow.

Report the behavior specified or changed, affected contracts and acceptance conditions, unresolved material questions, and the precise documents inspected or updated. Document work does not authorize code changes, task selection, or continuation into implementation.
