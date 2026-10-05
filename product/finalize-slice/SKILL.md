---
name: finalize-slice
description: Finalize an implemented rolling-wave slice for user review. Use when the user wants Codex to review the current branch state against a ready-for-review or in-review slice contract, confirm and fix required findings, repeat review and verification until no required findings remain, ask before accepting findings that materially change project shape or contradict project assumptions, record review state, and leave the clean slice in review for complete-slice.
---

# Finalize Slice

## Core Invariants

- Work under `docs/rolling-wave/{project}/`.
- Store project-level state in `project.md`; store slices in `slices/NNN-slug.md`.
- Use slice statuses: `pending`, `ready`, `in progress`, `ready for review`, `in review`, `done`.
- Multiple slices may be `ready`, `in progress`, `ready for review`, or `in review` concurrently. Each workflow invocation operates on one explicitly resolved slice.
- Accept user preferences by default, but push back when strong evidence conflicts with the workflow, prior decisions, terminology, or constraints.
- Pushback format: "I disagree because... The likely consequence is... Continue anyway?"
- Treat invocation as permission to review, edit product code, run relevant verification, use zero to three focused subagents when useful, and repeat until clean.
- Confirm reviewer findings against code, contract, and repository evidence before fixing them. Do not implement raw reviewer suggestions blindly.
- Fix confirmed findings automatically when they are required by the existing slice contract and do not materially change project shape.
- Ask the user before resolving or accepting a finding that materially changes the finish line, success criteria, roadmap order, project scope, public behavior, compatibility policy, irreversible migration behavior, or a recorded project assumption or decision.
- Preserve the immutable `Original Slice Contract`. Record approved deviations in review notes, completion learnings, and project decisions instead of rewriting history.
- Review against the slice's expected intermediate state. Do not require an ordinary slice to be production-ready, compiling, runnable, or fully tested when accepted breakage is recorded and tracked.
- Do not add temporary shims, fake fallbacks, placeholder adapters, broad validation, or speculative safeguards merely to make an accepted intermediate state green.
- Keep fixes inside the slice's prepared review decision. Independent usefulness or revertibility alone does not make work out of scope. Record changes needing a separate approval decision, risk class, or verification strategy as roadmap pressure instead of silently expanding the slice.
- Never mark the slice `done`. Leave it `in review`; `complete-slice` owns user-approved completion.
- Keep going until no confirmed required finding remains, a material project-shape decision requires user input, or a genuine external blocker prevents progress.
- When running inside a Codex goal, mark the goal complete only after the slice is clean and remains `in review`. A project-shape question pauses work for user input; it does not complete the goal or become a blocker on its first occurrence.

## Workflow

1. Resolve the project and slice.
   - Prefer the single slice with status `ready for review`; otherwise use the single slice with status `in review`.
   - If multiple candidates exist, ask which one to finalize.
   - If only `in progress` implementation exists, stop and route back to `implement-slice`; active implementation is not ready for finalization.
   - If no implemented candidate exists, stop and route to `implement-slice`.
   - Read the slice file first, especially `Original Slice Contract`, expected intermediate state, implementation notes, test backlog, prior review notes, and child-project completion condition.
   - Read only relevant `project.md` sections for finish line, scope, assumptions, decisions, risks, roadmap, and prior learnings.
   - Treat absent optional slice sections as defaults from `../rolling-wave-common/references/artifacts.md`.
   - Use `../rolling-wave-common/references/lifecycle.md` for status rules and `../rolling-wave-common/references/pushback.md` for evidence-based pushback.

2. Resolve the review surface.
   - Use the target branch named by the user.
   - Otherwise use the Git Town parent branch, then branch upstream if Git Town cannot resolve a parent.
   - Ask for the target branch only when neither source resolves one.
   - When invoked by `deliver-slice`, use its immutable handoff for project, slice, base, `HEAD`, and prior verification only.
   - Build the mutable review surface once in one batched snapshot: live `HEAD`, changed paths, diff stat, staged changes, unstaged changes, untracked paths, and worktree status.
   - Review the current branch state as a whole against the target branch. Include committed branch changes plus local staged, unstaged, and untracked files.
   - Do not assume one branch equals one slice. Previous slices or unrelated branch work matter only when they break the current contract, obscure review, introduce project risk, or contradict expected intermediate state.
   - Reuse prior verification results and a recent `code-review` or finalization pass only when current `HEAD`, changed paths, and worktree state still match their recorded review surface. Re-review changed or unresolved areas instead of repeating identical broad passes.

3. Mark or keep the slice `in review`.
   - Set slice status and matching `project.md` roadmap row to `in review` before review work.
   - Append dated passes; never overwrite prior review history.

4. Run one focused review pass.
   - Use `references/finalization-checklist.md`.
   - Start with a local contract and complexity pass before waiting on reviewers.
   - Compare current branch state to original contract, expected intermediate state, accepted breakage, implementation notes, and project decisions.
   - The fresh finalizer's local pass is the primary independent review. Default to zero additional reviewers.
   - Use zero reviewers for high-confidence local review, including mechanical moves, renames, generated updates, obvious follow-up fixes, and low-semantic-risk changes even when they touch many files.
   - For mechanical batches, review rename-detected moves separately from non-move edits, confirm declared invariants and exceptions, and use shared stale-reference or boundary checks across all chunks.
   - Use the mechanical fast path when `review_method` is `mechanical-batch`, implementation notes contain exact completion-gate results, and the live `HEAD` plus changed surface match the recorded verification fingerprint:
     1. inspect rename-detected moves for declared invariants
     2. review every non-move edit and declared mechanical exception
     3. independently rerun the contract's shared stale-reference, import-boundary, or equivalent mechanical proof
     4. compare results to every applicable behavior and acceptance row
   - Keep the mechanical fast path to a soft budget of about one minute and six repository queries. Do not rediscover already inventoried consumers or rerun unrelated broad checks when the fingerprint matches and the focused proof passes.
   - Fall back to the normal focused review when the fingerprint differs, proof fails, behavior changed, or concrete uncertainty remains.
   - Use one reviewer only when the local pass leaves concrete uncertainty, one dominant specialist risk needs independent attention, or a prior finding remains unresolved.
   - Use two or three only for high semantic complexity, multiple independent high-risk areas, unresolved conflicting evidence, or explicit adversarial review.
   - File count, diff size, or language match alone do not justify an additional reviewer.
   - Select reviewer focus by risk: correctness, testing, security, API contract, reliability, maintainability, adversarial, or available language/framework reviewer.
   - Spawn direct reviewer agent types for the selected focus; do not ask a generic subagent to invoke the full `code-review` skill.
   - Spawn reviewers together when independent. Give each target branch, changed files, relevant contract rows, implementation notes, and one narrow focus.
   - Close every reviewer after capturing output.
   - Do not report a reviewer claim as confirmed until local evidence shows the behavior, contract mismatch, regression, or meaningful risk is real.

5. Classify each confirmed finding.
   - `required fix`: existing contract, accepted intermediate state, or existing project decision requires the change. Fix automatically.
   - `project-shape decision`: resolving it changes project finish line, success criteria, scope, roadmap order, public behavior, compatibility policy, irreversible behavior, or contradicts a recorded assumption or decision. Ask the user.
   - `accepted intermediate gap`: contract explicitly allows it and later work or project risk already tracks it. Keep it open only as recorded future work, not as a blocker.
   - `future slice`: useful but independently reviewable work outside this slice. Record roadmap pressure; do not implement it here.
   - `not a finding`: unsupported, speculative, duplicate, preference-only, or already resolved. Discard it.

6. Ask only for material project-shape decisions.
   - Present specific evidence, affected project state, likely consequence, and recommendation.
   - Ask one decision at a time and wait. Do not choose silently, bury it in `Open Questions`, or keep fixing around it.
   - After the user answers, record the decision in `project.md` and the current review pass. Resume finalization using that decision.
   - Do not ask for ordinary implementation choices or straightforward in-contract fixes.

7. Resolve required findings.
   - Fix every confirmed `required fix` before another broad pass.
   - Use the smallest change that satisfies the contract. Prefer existing patterns, direct wiring, deletion, and current dependencies.
   - Use zero to three implementation subagents only when fixes have disjoint ownership or specialist value. Keep tightly coupled fixes local.
   - Tell fix subagents their exact finding, owned files or responsibility, contract evidence, verification focus, and scope boundary. Close them after results are integrated.
   - Do not add broad test coverage unless the current slice is the final testing/validation slice. Run relevant existing checks and add only tests required by this slice's contract or needed to prevent a confirmed regression.
   - Record changed files, verification, accepted failures, discarded reviewer claims, and final-test backlog in the dated review pass.
   - Update `project.md` only for material risks, approved shape changes, cross-slice decisions, review notes useful outside the slice, or roadmap pressure.

8. Repeat until clean.
   - After fixes, rebuild the branch and local-change review surface.
   - Re-run targeted checks for resolved findings, then perform another local contract pass.
   - Spawn follow-up reviewers only when changes or remaining risk justify them. Do not repeat unchanged reviewer work.
   - If the same finding survives two attempted fixes, switch to root-cause investigation before editing again. Ask the user only when blocked or when resolution becomes a project-shape decision.
   - Continue while any confirmed required finding remains.

9. Finish finalization.
   - Require no unresolved `required fix` and no unanswered `project-shape decision`.
   - Confirm child-project completion condition when the slice references a child project.
   - Record final review findings, resolved findings, accepted gaps, verification, and project-shape decisions in `Review Notes`.
   - Keep accepted intermediate gaps tracked to a later slice, roadmap item, or project risk.
   - Leave slice status and matching roadmap row `in review`; leave active-slice slot unchanged.
   - Do not capture completion learnings or output roadmap completion progress; `complete-slice` owns that transition.

## Completion

Report only resolved findings and unresolved accepted gaps or risks. Do not include a good-news summary or successful-check summary.

If no fixes were needed, respond exactly:

```text
No findings.
```

Leave marking `done`, completion learnings, next-slice selection, and roadmap checklist to `complete-slice`.
