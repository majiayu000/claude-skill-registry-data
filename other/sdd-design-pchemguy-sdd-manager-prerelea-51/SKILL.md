---
name: sdd-design
description: Use when exploring a software project or feature, forming architecture decisions, developing a component decomposition, or creating and revising docs/dev/PROJECT.md, ARCHITECTURE.md, DECOMPOSITION.md, and scoped architectural change documents before specification.
---

# Explore and design

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Apply the manager's [human document review](../sdd-manage/references/human-document-review.md) for PROJECT, ARCHITECTURE and DECOMPOSITION, including necessary feature design proposals, including direct calls. Newly created necessary documents pause for substantive human review before dependent progression. Reuse acceptable existing inputs after startup assessment without automatic interactive replay; requested interactive review comes first. Agent QC and repository-operation authority do not supply human acceptance.

For preimplementation project authoring, have **sdd-manage** establish the dedicated design-docs branch under its [preparation integration gate](../sdd-manage/references/branch-management.md#preparation-integration-gate). Commit project documents and required QC reports there. Before a dependent implementation branch is created, the manager explicitly merges accepted preparation into the actual default branch, verifies and publishes that baseline. Campaign plans/reports remain on revision branches; active implementation and steering amendments preserve their working-branch ownership. Read-only work creates no branch.

Choose the work requested and load only its reference. A request for a later stage can start there when its inputs are established; do not replay earlier stages as ceremony.

| Work | Load |
| --- | --- |
| Clarify the problem, compare alternatives, resolve decisions, or identify open questions | [exploration](references/exploration.md) |
| Define or revise major system blocks, dependency direction, and architectural decisions | [architecture](references/architecture.md) |
| Define or revise component responsibilities, collaboration, and provisional interfaces | [decomposition](references/decomposition.md) |

When the request crosses stages, load the next reference as that stage becomes relevant. Exploration can remain conversational. Do not create project documents solely because discussion has matured. Document creation or revision requires **sdd-manage** to coordinate the user's request and a current **sdd-orient** handoff identifying a usable Git worktree, applicable instructions, target paths, and unresolved dirty state. This skill does not perform orientation or authorize a different workflow.

Use the **sdd-conventions** modularity reference when defining or reviewing boundaries, and its design heuristics when assessing a chosen approach or comparing options. Keep these checks separate from the document-specific procedures below. Observe project instructions and existing contracts; do not overwrite unowned changes. If required project evidence conflicts, resolve the conflict before mutation.

`PROJECT.md` owns the concise project brief, `ARCHITECTURE.md` owns high-level design, and `DECOMPOSITION.md` owns detailed logical component boundaries. Both architecture and decomposition may have focused children. Scoped feature documents express a proposed architectural delta where necessary. These documents inform SPEC; they neither replace its behavioral contracts nor authorize implementation, planning, layout authoring, or task execution.

## Document boundaries

| Document | Governing concern |
| --- | --- |
| ARCHITECTURE | Major blocks, system-wide relationships and dependency direction, and consequential structural rationale. |
| DECOMPOSITION | Logical components within those blocks: responsibility, collaboration, state ownership, and design-level interface and verification seams. |
| SPEC | Observable behavior and precise success/failure contracts, required qualities, and acceptance. |
| PLAN | Practical delivery order, capability increments, dependencies, and exit/decision evidence. |
| layout.md | Physical allocation of source, tests, documentation, and artifacts. |

Support required modularity, extensibility, scalability, decoupling, and testability through the accepted design. Tie variation and load decisions to actual requirements and credible needs; these qualities do not require realizing every anticipated capability in the first increment.

Use the relevant architecture or decomposition reference for read-only design review. Incorporation of accepted feature design into main PROJECT, ARCHITECTURE, or DECOMPOSITION belongs to **sdd-integrate-feature**.

At completion, state what was explored or changed, the decisions established, unresolved material questions, and which documents were inspected or updated. Report design as design, never as implemented functionality.
