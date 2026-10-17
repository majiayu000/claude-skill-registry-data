---
name: sdd-steer
description: Use when the human defines a focused amendment at a checkpoint during partial SDD task-list implementation, especially reducing previously implemented functionality, and requests impact assessment or amendment implementation across existing development documents, code, tests, and documentation. Stop after reporting; do not resume sdd-implement.
---

# Apply a human-directed checkpoint amendment

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Steering is the lightweight checkpoint variant of the revision core workflow. Use **sdd-manage**'s **Core development workflows** model in its **Available workflows** reference for purpose and routing; this skill owns the focused amendment procedure and requires no formal campaign artifacts.

The human defines the objective at a checkpoint and decides whether to command its implementation. Distinguish an assessment request from an implementation request; discussion alone does not authorize repository changes. A command to implement the established amendment authorizes routine steps within that scope without repeated confirmation. **sdd-manage** coordinates scope and shared prerequisites. Use **sdd-manage**'s **Branch management** reference to establish or reuse an amendment branch from the paused implementation checkpoint, with that implementation branch as its target. Use a current **sdd-orient** handoff for repository instructions, Git and task state, pending-change ownership, and the implementation checkpoint.

| Work | Load |
| --- | --- |
| Establish the objective, scope, and affected work | [objective and impact](references/objective-and-impact.md) |
| Amend existing development documents and implemented behavior | [amendment execution](references/amendment-execution.md) |
| Bootstrap disclosure and usage records before the first SDD commit | **sdd-manage**: `skills/sdd-manage/references/repository-bootstrap.md` (bundled dependency) |
| Verify, commit, push, report, and stop | [verification and stop](references/verification-and-stop.md) |

1. **Establish the amendment.** Allocate or recover its shared review-campaign identity and matching revision branch; retain a minimal REVISION-REPORT with objective, scope, full baseline and paused target, adding observed verification/publication at completion. Require no fabricated review or plan. Identify the human's intended end state, affected implemented features, retained behavior, relevant existing documents and task IDs, and the checkpoint baseline. Report missing decisions or conflicts that prevent the focused amendment.
2. **Update existing development documents.** Within the commanded scope, directly amend affected SPEC, PLAN, TASKS or active FEATURE-TASKS, design, and layout so they describe the accepted end state. Preserve unaffected content and stable identities. Create no feature-document layer and invoke no feature-integration step.
3. **Align implementation.** Use **sdd-tdd** for test strategy and changes, perform focused production changes, and use **sdd-docs** for module, API, README, and guide alignment. For a reduction, remove affected functionality consistently while protecting the retained contracts and dependencies. This skill owns the production edits and repairs within the amendment.
4. **Verify and finish.** Use **sdd-verify** to assess the amendment and relevant regressions. Reassess affected completion claims, use **sdd-report** for the commit and result, commit and push the verified amendment, perform the default explicit merge into the paused implementation branch, verify and publish the target, and coordinate any warranted hosted reconciliation through **sdd-forge** when tracking is active.
5. **Stop.** Report the resulting checkpoint, implemented amendment, verification and limitations, working/target branches, amendment and merge commits and publication state, and remaining work. Do not hand off to, invoke, or resume **sdd-implement**, select further tasks, or start another amendment. The human separately decides when to resume the main task list.

**sdd-implement** owns the main task-list workflow; this skill owns the human-commanded checkpoint amendment, including its direct development-document updates, completion reassessment, commits, pushes, and issue-state coordination. A planning-only request returns findings and proposed scope, then stops. Preserve pending work and do not reset or delete unrelated implementation. Git and the current documents retain history; no separate transaction journal or recovery workflow is required.
