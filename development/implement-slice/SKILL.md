---
name: implement-slice
description: Implement a ready rolling-wave slice without locking it down with broad tests yet. Use when the user explicitly wants to code the current docs/rolling-wave/{project}/slices/NNN-slug.md slice, mark it in progress while working, implement small or cohesive work in the main context by default, use one to three gpt-5.6-terra workers only for genuine parallel chunks or large discovery/mechanical work where delegation pays for its handoff cost, pause or hand off chunks marked human-fit when appropriate, record implementation notes and final-test backlog, preserve the original slice contract, and mark completed implementation ready for review.
---

# Implement Slice

## Core Invariants

- Work under `docs/rolling-wave/{project}/`.
- Store project-level state in `project.md`; store slices in `slices/NNN-slug.md`.
- Use slice statuses: `pending`, `ready`, `in progress`, `ready for review`, `in review`, `done`.
- Multiple slices may be `ready`, `in progress`, `ready for review`, or `in review` concurrently. Each workflow invocation operates on one explicitly resolved slice.
- Accept user preferences by default, but push back when strong evidence conflicts with the workflow, prior decisions, terminology, or constraints.
- Pushback format: "I disagree because... The likely consequence is... Continue anyway?"
- Product code changes are allowed only because this skill is the explicit implementation entry point.
- Treat implementation as exploratory: refactoring, slice-shape discoveries, and plan adjustments are expected.
- Individual slices do not have to be fully functioning or production-ready. The final project must work; intermediate slices may intentionally fail compile, typecheck, lint, tests, runtime, or validation when that state is recorded in the slice contract.
- Do not add temporary code, compatibility shims, fake fallbacks, placeholder adapters, broad validation, or throwaway wiring just to make an intermediate slice compile or pass checks.
- Do not write new tests in ordinary implementation slices unless a tiny probe is required to understand or unblock the implementation. Broad test coverage belongs in the final testing/validation slice after implementation has settled.
- Keep implementation within one bounded review decision. Related or mechanically identical changes may span domains, files, commits, and independently executable chunks when the prepared review question and verification strategy cover them.
- Choose delegation by net operating cost. Small, cohesive, serial work stays in the main context; workers serve genuine parallelism, large mechanical batches, broad isolated discovery, or specialist ownership.
- Invoking this skill is the explicit request to implement the slice using the workflow below, including implementation subagents when the execution shape calls for them.
- Keep contract resolution, project-shape decisions, cross-chunk integration, and final status ownership in the root agent. Terra workers own implementation chunks.
- Slice/project artifacts are agent state. Record implementation notes as terse table rows or `key: value` bullets; avoid narrative handoff prose unless it captures a decision-critical reason.

## Workflow

1. Resolve the project and slice.
   - If the user names a project or slice, use it.
   - Otherwise collect slices with status `ready`.
   - If exactly one `ready` slice exists, use it.
   - If no `ready` slice exists, stop and route to `prepare-next-slice`.
   - If multiple `ready` slices exist, ask which one to implement.

2. Read the contract.
   - Read relevant `project.md` sections for project-level decisions, risks, and completed-slice learnings.
   - Read the slice file, especially `Original Slice Contract`, acceptance criteria, verification intent, child rolling-wave project relationship, minimum implementation, scope boundaries, and risks.
   - Treat absent optional sections as defaults from `../rolling-wave-common/references/artifacts.md`, not as a preparation failure.
   - If the slice uses the sparse `Contract` table, treat `behavior`, `acceptance`, `include`, and `exclude` rows as the source of behavior, acceptance criteria, and scope boundaries.
   - If the slice is backed by a child rolling-wave project, read the child `project.md` and current child slice state before choosing execution shape.
   - Read `Parallel Work Chunks` from the slice contract when present. Treat prepared chunks as the default execution plan.
   - If `Parallel Work Chunks` is absent, infer `serial/local-only` for tiny/cohesive slices or define an execution split only when obvious from the contract.
   - Read `Execution Fit` for the slice and chunk-level suggested owners when present. If absent, infer `agent` or `either` unless the work is clearly human/hybrid fit.
   - Use `../rolling-wave-common/references/lifecycle.md` when status ownership is unclear.
   - Use `../rolling-wave-common/references/pushback.md` when implementation would violate the contract or lifecycle.
   - Do not rewrite the original contract. Record discoveries elsewhere.
   - Confirm the executable slice still fits its prepared review decision and budget. Independent usefulness, executability, or revertibility alone is not a reason to split. If work now needs separate approval decisions, unrelated mental models, distinct risk classes, incompatible intermediate states, materially different verification, or has grown beyond a credible focused review, stop before changing status or product code and route it back to `prepare-next-slice`.

3. Mark the slice `in progress`.
   - Update the slice status before implementation work starts.
   - Add an implementation attempt entry with date, agent, and intended ownership.

4. Choose execution shape.
   This is mandatory. Do not start editing product code until the execution shape is chosen and recorded in the implementation attempt.

   Decide based on slice size, coupling, discovery cost, execution fit, parallel ownership, expected coordination overhead, and platform availability.

   Use the prepared `Parallel Work Chunks` first:
   - If the slice defines parallel chunks, spawn one implementation worker per `agent` or suitable `either` chunk when the platform supports subagents.
   - Do not spawn subagents for chunks marked `human` unless the user asks to use the agent fallback.
   - For chunks marked `hybrid`, do the agent-fit context gathering or mechanical work, then pause for the human decision before finalizing that chunk unless the contract says the agent fallback is acceptable.
   - If a chunk is marked `human`, pause before implementation and present the human handoff, reason, timebox, and agent fallback. Ask whether the user wants to do it by hand or have the agent continue with the fallback.
   - Dispatch independent agent-fit chunks before pausing for a human or hybrid chunk. Pause only the human-owned chunk and work that depends on its result.
   - Keep chunks as written unless a chunk has become unsafe, stale, overlapping, or impossible. If so, record the reason before adjusting execution shape.
   - Assign each subagent the chunk's concrete output, owned files/modules/responsibilities, dependencies, final-test backlog focus, and review focus.
   - Tell each subagent to skip new test coverage unless a minimal test/probe is required to unblock implementation.
   - Keep one immediate integration or critical-path task local when useful, but do not duplicate a chunk already owned by a subagent.

   If the slice has no usable chunks, keep small or cohesive serial implementation in the main context.

   Use one to three Terra implementation workers only when:
   - two or more disjoint chunks can make useful progress concurrently
   - one large mechanical batch has a finite inventory and deterministic proof, and isolating its edits materially reduces main-context load
   - broad repository discovery can run independently while the main context performs non-overlapping critical-path work
   - specialist ownership materially lowers correctness risk

   Use one worker per disjoint prepared chunk. If more than three chunks would be needed, stop and ask to re-prepare the slice or merge chunks before implementation.

   Keep agent-fit implementation local only when one of these is true:
   - the slice is small, cohesive, or serial and delegation startup, handoff, and repository reload would likely cost more than direct implementation
   - all remaining chunks are marked `human` and the user chooses to do them by hand
   - Terra workers are unavailable in the current environment
   - repository instructions explicitly prohibit subagent dispatch
   - the next action is an urgent blocker that must be done before any useful parallel work exists

   If keeping work local or pausing for human work, write the reason into `Implementation Notes` before editing product code. Main-local implementation must satisfy the same completion gate required of workers.
   If the platform rejects a Terra worker, do not silently substitute another model. Continue locally only after recording that platform blocker in the implementation notes and final response.

   When delegating:
   - Spawn with agent type `worker`, model `gpt-5.6-terra`, and `fork_turns: "none"`.
   - Pass a self-contained task packet: project and slice paths, exact chunk contract, owned files/modules/responsibilities, dependencies, scope boundaries, final-test backlog focus, and review focus.
   - Assign disjoint ownership with explicit files, modules, or responsibilities.
   - Tell each subagent it is not alone in the codebase.
   - Tell each subagent not to revert edits made by others.
   - Require each subagent to list changed files and any lightweight verification performed.
   - Require each subagent to identify any final testing/validation slice backlog created by its chunk.
   - Require each subagent to report whether its chunk contract was completed, partially completed, or blocked.
   - Require each worker to finish a completion gate before reporting `completed`:
     - map every applicable behavior and acceptance row to changed files or a concrete verification result
     - for `mechanical-batch` or `mixed` work, run the contract's declared `shared_proof`, including changed/moved-file scans for forbidden deep imports, stale paths, relays, or other declared mechanical exceptions
     - inspect all moved source files, not only primary components, against owner-public and same-owner import rules
     - fix any in-contract mismatch in the same worker turn, then rerun the failed proof
   - Require exact completion-gate commands and results in the worker return. A worker must report `partially completed` instead of leaving an obvious contract mismatch for root integration or finalization.
   - Keep root work to orchestration, integration, conflict resolution, and non-overlapping critical-path preparation. Do not duplicate worker implementation.
   - After each subagent result is captured and no further input is needed, close that subagent. `wait_agent` does not close it automatically.

   For main-local implementation, run the same completion gate before reporting completion: map applicable contract rows, execute declared mechanical proof, inspect moved sources and import boundaries, fix in-contract mismatches, and record exact commands and results.

5. Implement against the slice contract.
   - If the parent slice points to a child rolling-wave project, implement only the child slice or child-project work that is currently ready. Do not collapse the child project's remaining roadmap into this parent-slice implementation.
   - Keep parent implementation notes focused on parent-visible progress, child project path, active child slice, and child learnings that affect the parent project.
   - Before writing code for each local or delegated chunk, apply the minimum-implementation ladder:
     1. Does this code need to exist for this slice?
     2. Does the standard library or language runtime already do it?
     3. Does a native platform, browser, database, framework, or OS feature cover it?
     4. Does an already-installed dependency or existing project helper solve it?
     5. Can this be one direct path instead of a new abstraction, option, fallback, or dependency?
     6. Only then write the minimum custom code that satisfies the slice.
   - Prefer deletion, direct wiring, and existing primitives over future-proofed scaffolding.
   - Do not add config knobs, wrappers, factories, compatibility layers, broad normalization, or edge-case guards unless the slice contract, a real caller, a trust boundary, or repo evidence requires them.
   - Do not patch around incomplete future-slice work just to satisfy current validation. If the missing later work causes compile/typecheck/lint/test/runtime failure that is accepted by the contract, leave it broken, record it, and continue within scope.
   - If validation fails unexpectedly, decide whether it is a real slice bug or an acceptable intermediate gap. Fix real slice bugs narrowly; do not add temporary green-check code for accepted gaps.
   - Do not simplify away input validation at trust boundaries, security controls, data-loss prevention, accessibility basics, migration safety, or behavior the user explicitly requested.
   - When taking an intentional shortcut with a known ceiling, record the ceiling and upgrade trigger in implementation notes. Add a short code comment only when future maintainers would otherwise misread the shortcut as accidental or unsafe.
   - Prefer existing project patterns.
   - Keep edits scoped to the slice.
   - Favor getting the behavior into the right shape over prematurely locking tests around churn.
   - Do not broaden the slice just to make a future test plan cleaner.
   - Respect `Execution Fit`: use agents for broad/mechanical work, pause for human-fit taste/API/type-shape calls, and resume only after the user provides the result or authorizes the fallback.
   - If the slice contract is wrong or incomplete, pause, record the issue, and ask before expanding scope.

6. Record implementation notes.
   - Use `references/implementation-handoff.md` for the note format. Resolve this path relative to this `implement-slice` skill directory, not `rolling-wave-common`.
   - Update the slice `Implementation Notes` section with execution shape, human-fit pauses or handoffs, delegation/local-only reason, ownership, changed files, commands run, accepted validation failures, final-test backlog, known risks, deviations, and review focus.
   - Include what was deliberately skipped or simplified under the minimum-implementation decision, plus any upgrade trigger.
   - Record a compact verification fingerprint: changed paths or owned surface, exact completion-gate commands and results, and current `HEAD`. This is evidence for finalization reuse, not an implementation conclusion.
   - Preserve the artifact's compact structure. Prefer appending one dated row plus short keyed details over adding paragraphs.
   - Update `project.md` only for cross-slice decisions, new risks, or roadmap pressure.

7. Finish implementation status.
   - Before accepting a worker as complete, confirm its return includes the required completion-gate mapping and exact results. Do not repeat broad repository discovery in root when the evidence is complete; inspect only missing, conflicting, or integration-sensitive areas.
   - If slice implementation is complete, set slice status and matching `project.md` roadmap row to `ready for review`.
   - Treat implementation as complete when every required contract behavior and in-scope implementation chunk is done, implementation notes capture known deviations and accepted failures, and no required human handoff or implementation blocker remains.
   - Do not require broad tests, a clean finalization pass, or production-ready project state before marking `ready for review`; those belong to later workflow stages or recorded intermediate state.
   - If implementation is partial, blocked, waiting on a required human handoff, or missing required contract work, leave status `in progress` and record exact remaining work.

## Completion

Stop with completed implementation `ready for review`; leave incomplete implementation `in progress`. Summarize changed files, resulting status, any lightweight verification run, accepted validation failures, and final testing/validation backlog. End with `Commit message:` followed by one short bullet in imperative mood describing the changes made; omit workflow and status details. Do not create a commit. Do not route to a separate per-slice test phase.
