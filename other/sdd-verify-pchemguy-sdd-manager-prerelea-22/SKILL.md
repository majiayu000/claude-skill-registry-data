---
name: sdd-verify
description: Use when selecting and running checks for an SDD task, selected change, milestone, phase, or project; assessing acceptance and exit-condition coverage; classifying observed failures; performing read-only milestone/phase implementation code review, checking Git release-highlight ranges and drafts, release package contents, release workflows, CI outputs and hosted asset integrity; or returning verification evidence and remaining gaps before completion.
---

# Verify a selected work boundary

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Establish the requested task, change, milestone, phase, or project scope. Load the relevant references:

| Work | Load |
| --- | --- |
| Review milestone/phase implementation code and findings | [boundary review](references/boundary-review.md) |
| Derive checks from requirements, changes, and dependencies | [check selection](references/check-selection.md) |
| Assess Git highlights, package contents, release workflows, CI outputs and hosted download evidence | [package and release checks](references/release-checks.md) |
| Execute checks and assess acceptance evidence | [execution and evidence](references/execution-and-evidence.md) |
| Classify failures and return unresolved work | [failure assessment](references/failure-assessment.md) |

Use a current **sdd-orient** handoff for governing instructions, Git state, dirty-path ownership, relevant documents, and declared commands. **sdd-manage** coordinates the requested scope and execution prerequisites; the active implementation workflow, **sdd-implement** for main task work or **sdd-steer** for a checkpoint amendment, requests verification within its boundary. For standalone package/release work, use accepted source/build/package inputs without inventing TASKS; load release checks. Otherwise read the owning TASKS or FEATURE-TASKS, relevant SPEC contracts, PLAN exit conditions, design and layout, actual changes, tests, and existing evidence as needed. Read-only check planning can precede execution; commands with side effects require the established eligible Git worktree and authorized environment.

For an explicit boundary review task, load boundary review and assess implementation code separately from test execution. Neither activity substitutes for the other. Return findings and recheck evidence without repairs or task/hosted state changes.

1. Identify the acceptance and exit conditions to verify and the implementation state being checked.
2. Select sufficient direct, dependent, integration, and boundary checks. Use project commands and an existing verification map where useful; neither a map nor new scripts are required.
3. Establish representative environment capabilities for the planned checks through check selection; load its browser guidance only for relevant browser work. Run the selected checks and inspect actual outcomes, including failures, warnings, skips, and collection counts where relevant.
4. Associate each condition with evidence and any limitation. Distinguish verified, failed, blocked, and not checked conditions; passing checks do not establish acceptance they never exercised.
5. Classify observed failures where evidence permits and return remaining work to its owner. Do not silently omit an unrelated or pre-existing failure from the results.

**sdd-tdd** owns testing strategy and test design or changes; this skill assesses coverage and executes the verification campaign. **sdd-docs** owns documentation maintenance. The active implementation workflow owns repairs, completion checkboxes, commits, pushes, and issue-closure coordination. Leave source, tests, governing documents, and task status unchanged during verification; report necessary changes rather than repairing them here. Account for command-generated artifacts and preserve unrelated pending work.

Return the boundary and implementation state, conditions assessed, check selection and rationale, commands and environment, observed outcomes and evidence locations, failure classifications, omitted or blocked checks, and remaining gaps. **sdd-report** owns presentation of these facts. Existing task evidence or a project-designated record may hold durable results; no separate verification journal is required. State when the selected conditions are verified without equating that finding with task completion or whole-project correctness.
