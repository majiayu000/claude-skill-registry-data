---
name: prepare-next-slice
description: Prepare and risk-check the next rolling-wave slice for implementation. Use when the user wants to continue a rolling-wave project, draft one bounded slice in the main context by default, use a fresh planning author only when context or discovery cost warrants it, use a fresh preparation reviewer when semantic risk or uncertainty warrants independent pressure-testing, decompose parallel implementation chunks where appropriate, identify agent, human, either, or hybrid execution fit, write or update docs/rolling-wave/{project}/slices/NNN-slug.md, and mark that slice ready even when other slices are active.
---

# Prepare Next Slice

## Core Invariants

- Work under `docs/rolling-wave/{project}/`.
- Store project-level state in `project.md`; store slices in `slices/NNN-slug.md`.
- Use slice statuses: `pending`, `ready`, `in progress`, `ready for review`, `in review`, `done`.
- Multiple slices may be `ready`, `in progress`, `ready for review`, or `in review` concurrently. Each workflow invocation operates on one explicitly resolved slice and must not change other slices merely to enforce uniqueness.
- Accept user preferences by default, but push back when strong evidence conflicts with the workflow, prior decisions, terminology, or constraints.
- Pushback format: "I disagree because... The likely consequence is... Continue anyway?"
- Do not modify product code. This skill stops after marking a slice `ready`.
- Slice artifacts are agent state, not human-facing documentation. Prefer stable headings, terse `key: value` bullets, IDs, and tables over explanatory prose.
- Prepare the slice until it is ready enough to implement, not until every optional planning field is polished.
- Keep an optional section only when it prevents a distinct plausible implementation failure, resolves non-default routing, or records material uncertainty. Do not restate one fact across contract, risks, decisions, minimum implementation, and readiness notes.
- Do not mark an executable slice `ready` unless it fits one bounded human review decision. Independently executable, useful, or revertible chunks may stay together when one architectural intent or transformation recipe, risk class, and verification strategy cover them.
- Draft in the main context by default. Use subagents only when fresh context, independent risk review, or genuine parallel work outweighs coordination and repository-reload cost.
- Keep standard preparation bounded. Prefer targeted evidence and early structured returns over exhaustive repository inventory.
- Require an exact inventory only when implementation needs a finite complete list. Otherwise record the discovery method and representative risky consumers; defer completeness proof to the final testing/validation slice.

## Workflow

### Orchestration

1. Choose the author.
   - Keep authorship in the main context for small or cohesive slices, familiar repository areas, and work where active conversation or prior project shaping already contains useful context.
   - Spawn one fresh planning author only when the main context is long or compacted, repository discovery is broad or unfamiliar, multiple plausible slice shapes need isolated investigation, or preserving main-context capacity materially helps later delivery.
   - When using a planning author, spawn with no conversation history, `model="gpt-5.6-terra"`, and `reasoning_effort="medium"`.
   - Give it the repository root, any user-named project or slice, and a terse brief containing only user-stated constraints that are not already recorded in project artifacts.
   - Do not pass exploratory chat, parent reasoning, recommendations, or raw repository findings.
   - Instruct it to use `$prepare-next-slice` in `author-only` mode, execute Author Phase steps 1-5, keep the selected slice `pending`, make no product-code changes, and return only:
     - `drafted`: selected slice path, material assumptions or safe deferrals, and a neutral evidence index
     - `question`: one highest-leverage user question with evidence and a recommended answer
     - `blocked`: exact missing dependency or evidence
   - Keep the evidence index factual: paths, commands, observed symbols, dependency edges, and artifact references. Exclude rationale, confidence, recommendations, and suspected reviewer conclusions.
   - Use a soft standard budget of about three minutes and twelve repository queries. Batch related reads and searches. On budget exhaustion, return `drafted`, `question`, or `blocked` instead of continuing broad exploration.
   - If it returns `question`, relay that single question to the user, send the answer back to the same author, and continue until `drafted` or `blocked`.
   - When keeping authorship local, execute Author Phase steps 1-5 directly and produce the same `drafted`, `question`, or `blocked` result.
2. After `drafted`, apply the preparation-review gate.
   - Spawn one fresh independent reviewer when any of these apply: behavior changes; public API, exported type, compatibility, security, authorization, data, migration, or irreversible risk; mixed or cross-domain semantics; conflicting repository evidence; unclear scope; unresolved contract choice; or no deterministic bounded proof.
   - Skip the reviewer only when behavior is unchanged, work is a low-semantic mechanical transformation, scope is explicit, no material question remains, and one deterministic shared proof can judge every acceptance row.
   - Record `preparation_review: skipped, reason: ...` in `Readiness Notes` when skipping.
   - When review is required and a planning author drafted the slice, use a different fresh-context reviewer.
3. If the reviewer returns `redirect`, reuse existing contexts:
   - The reviewer drafts the prerequisite or replacement slice, updates material roadmap/dependency state, preserves `status: pending`, and returns its path plus a neutral evidence index.
   - Send that redirected slice to the context that did not author it for independent review in `$grill-me` `prepare-review` mode.
   - Do not spawn a second author/reviewer pair. If redirected review finds another redirect, return `blocked` or `question` instead of starting an unbounded preparation chain.
4. After required independent review returns `ready`, or after a justified skip, run Final Readiness in the main context.
5. While agents run, wait in intervals up to 60 seconds and provide at most one useful status update per interval. Do not busy-poll or call `list_agents` unless an agent stays silent beyond its soft budget.
6. If a required fresh-context reviewer is unavailable, run Independent Review inline. Disclose missing context separation.

### Author Phase

When invoked in `author-only` mode, execute only steps 1-5. Do not spawn another author, run Independent Review, or mark the slice `ready`.

1. Resolve the project.
   - If the user names a project, use it.
   - If exactly one rolling-wave project exists, use it.
   - If multiple projects exist and none was named, ask which one to use.
   - If none exist, tell the user to run `shape-project` first.

2. Read project and slice state.
   - Read `project.md`.
   - Scan frontmatter or status lines across all slice files; do not read every slice body.
   - Read the full selected slice, its direct dependencies, active slices that materially affect it, and completed-slice learnings explicitly referenced by the project or dependency chain.
   - Search `docs/solutions/`, ADRs, tests, configs, and product code by targeted term or path. Do not bulk-read whole documentation trees.
   - Note existing `ready`, `in progress`, `ready for review`, and `in review` slices for dependency and learning context.
   - Do not block, ask permission, or change another slice merely because active slices already exist.

3. Select the next slice.
   - Prefer the next `pending` implementation slice that best advances the finish line.
   - Apply learnings from completed slices.
   - If learnings contradict the roadmap, explain the proposed reorder before changing it.
   - Check whether the selected slice depends on unresolved behavior or learnings from an unfinished predecessor. Existing active work is not itself a blocker; only a concrete missing dependency is.
   - If missing predecessor knowledge prevents an honest implementation contract, explain the dependency and leave the selected slice `pending`. Otherwise prepare it using stable current evidence and record any safe deferred uncertainty.
   - If the next pending item is only a broad phase or validation/planning activity, rewrite it into a concrete implementation step before grilling it. If it cannot be made implementation-shaped, move it to project open questions, risks, verification notes, or cross-slice decisions instead of preparing it as a slice.

4. Draft only the selected slice.
   Resolve evidence-backed choices and write a provisional contract. Required:
   - behavior is clear
   - scope boundaries are explicit enough to prevent obvious overreach
   - scope forms one bounded human review decision
   - expected intermediate state is clear, including whether compile/run/test failures are acceptable for this slice
   - likely approach is clear enough
   - any user-facing, public API, migration, data-loss, security, or irreversible decision that affects this slice is resolved

   Infer by default instead of asking:
   - verification intent may be a one-line note about what the final testing/validation slice should eventually prove
   - child rolling-wave project is `none` unless the slice clearly has its own finish line or internal roadmap
   - owner fit is `agent` or `either` unless the main risk is taste, naming, API/type shape, or human product judgment
   - parallel work is `serial/local-only` unless there are obvious disjoint ownership areas
   - temporary green shims are `no`
   - risks, decisions, and minimum-implementation notes may be omitted when no meaningful non-default item exists
   - bundled or static assets with one observed runtime consumer live beside that consumer unless repository convention, reuse, generation, or deployment constraints justify a shared asset location

   Avoid file/function-level grilling unless it affects behavior, scope, risk, correctness, data shape, migration concerns, testability, or downstream ordering.
   Do not require a detailed test plan, exact test files, or final validation commands at slice-preparation time unless they are already obvious and materially affect the slice shape. Broad tests are locked down in the final testing/validation slice after implementation slices settle.
   Do not build an exhaustive consumer, import, generated-registration, or dependency manifest during preparation unless implementation requires that exact finite list. Record the reproducible query and known high-risk examples; put completeness proof in the final testing/validation slice.
   Do not require every slice to compile, run, or pass tests. Ask whether an intermediate broken state is acceptable only when the slice is likely to leave the repo broken or partially wired. If accepted, record what may be broken and which later slice, roadmap item, or project risk will resolve it before the finish line.
   If compile/typecheck/lint/test/runtime failures are acceptable for this slice, record them explicitly in `Expected Intermediate State` and default `temporary_green_shims_allowed` to `no`.
   Do not plan temporary code, compatibility shims, fake fallbacks, broad validation, placeholder adapters, or throwaway wiring just to make intermediate validation pass. Prefer recording the accepted failure and the later restoration target.
   Do not prepare a slice whose only output is "decide", "research", "validate", or "design" unless the slice also has a concrete reviewable artifact or code/docs change required for implementation.

   Decide whether the slice should become a child rolling-wave project only when it contains multiple review decisions or needs its own internal roadmap:
   - First try batching chunks that share one reviewer question, transformation recipe, risk class, and verification method.
   - Split into sibling slices when chunks need separate product or architecture approval decisions, unrelated mental models, distinct risk classes, incompatible intermediate states, or materially different verification strategies.
   - Recommend a child project when the selected slice has its own finish line, multiple internal implementation steps, separate review cycles, or enough uncertainty that preparing it as one slice would be fake precision.
   - Keep it as a normal slice when changes can be judged through one bounded review decision, even across multiple domains, files, concerns, commits, or chunks.
   - If using a child project, create or reference `docs/rolling-wave/{child-project}/project.md`, define what child-project completion means for the parent slice, and record which child scope counts toward the parent slice versus what remains outside it.
   - Do not duplicate the child project's internal roadmap inside the parent slice. Link to the child project and keep only the parent-level contract and completion condition.
   - If the child project does not exist yet, route to `shape-project` for the child project before pretending the parent slice is ready.

   Define the minimum implementation only as much as needed to prevent likely overbuilding:
   - Ask what code or behavior does not need to exist yet when the slice is likely to invite extra safeguards, knobs, compatibility paths, abstractions, or dependencies.
   - Prefer stdlib, native platform features, existing project helpers, and already-installed dependencies before planning custom logic or new dependencies.
   - Record the simplest acceptable path, things explicitly not being built, intentional shortcuts or ceilings, and the trigger that would justify upgrading the shortcut later.
   - Do not remove necessary input validation at trust boundaries, security controls, data-loss prevention, accessibility basics, migration safety, or behavior the user explicitly requested.
   - If the slice intentionally chooses a shortcut with a known ceiling, make the ceiling and upgrade trigger explicit so "later" does not become silent debt.
   - Record any useful test ideas as backlog for the final testing/validation slice, not as mandatory work for this slice unless this slice itself is the final testing/validation slice.

   Decompose implementation work where appropriate, but do not force chunk planning for small coherent slices:
   - Chunks may parallelize one review-sized slice and guide review navigation. Independently useful, executable, or revertible chunks do not require separate slices when one review decision covers them.
   - Create `Parallel Work Chunks` in the slice contract when the slice can be split into independent ownership areas.
   - Prefer one to three chunks. Do not invent more chunks than `implement-slice` can usefully delegate.
   - A good chunk has a concrete output, owned files/modules/responsibilities, dependencies, suggested owner, reason, human handoff, agent fallback, timebox, final-test backlog focus, and review focus.
   - Chunks should be disjoint enough that one subagent can own each chunk without frequent merge conflicts.
   - If chunks must run in order, record dependencies clearly; do not call sequential phases "parallel".
   - If the slice is tiny, tightly coupled, or has one obvious critical path, record `Parallel Work Chunks: serial/local-only` with the reason instead of forcing fake chunks.
   - Avoid grilling every individual file or validation command. Ask only about chunk boundaries when they affect behavior, risk, ownership, or parallel execution.

   Set the review budget:
   - Group by reviewer question and verification method, not product domain alone.
   - Use roughly 500 non-move changed lines as a soft default. Lower it for semantic, stateful, public-contract, security, data, or irreversible work; allow a larger raw diff for repetitive mechanical changes when one proof covers the batch.
   - For mechanical relocation batches, require one transformation recipe, unchanged behavior, vertically complete moved units with consumers and existing tests, rename-aware review, stale-reference scans, and few explicit non-mechanical exceptions.
   - Move behavioral exceptions or different-risk work into another slice unless they remain minor, explicit, and reviewable under the same decision.
   - Add `Review Shape` to cross-domain, multi-chunk, mechanical-batch, mixed, or near-budget contracts.

   Identify execution fit only to the level needed for implementation routing:
   - Use `agent` for broad search, repetitive edits, cross-file wiring, mechanical consistency, test scaffolding, and "find all places" work.
   - Use `human` for narrow changes that depend on taste, naming, API/type shape, product judgment, or cases where explaining the desired result is likely slower than editing it.
   - Use `either` when the chunk is small and well specified enough that either the user or an agent can do it efficiently.
   - Use `hybrid` when an agent should gather context or do the broad/mechanical work, but the user should make the final taste/API/type-shape decision.
   - Prefer `human` when the user could likely finish the chunk in under 10-15 minutes, the target files are obvious, and the main risk is clarification churn.
   - For human or hybrid chunks, include a concrete `Human handoff` and `Agent fallback` so `implement-slice` knows whether to pause or continue.

5. Write the slice artifact.
   - Use `../rolling-wave-common/references/artifacts.md` for the slice template.
   - Use `../rolling-wave-common/references/lifecycle.md` for status rules.
   - Use `../rolling-wave-common/references/pushback.md` when a decision needs evidence-based pushback.
   - Optimize the slice for future agent retrieval: compact tables, canonical statuses, stable IDs, paths, and one fact per canonical section.
   - Avoid narrative summaries, duplicated context, and polished prose. Human-facing explanations belong in chat or `exec-summary`, not in the slice file.
   - Preserve an immutable `Original Slice Contract` section once the slice is marked `ready`.
   - Do not write skill workflow instructions into the slice artifact. Rules like "do not rewrite this section after ready", "filled by implement-slice", or "mark ready only when..." belong in the skill workflow, not the slice plan.
   - Use the sparse slice template. Include optional sections only when they add information beyond the defaults.
   - If omitting optional sections, rely on these defaults: `child_project: none`, `owner_fit: agent|either`, `temporary_green_shims_allowed: no`, `parallel_work: serial/local-only`, `risks: none known`, `decisions: none`.
   - Include `Execution Fit` only when the slice is human, hybrid, unusually suitable for agents, or has non-obvious routing.
   - Include `Minimum Implementation` only when the slice is likely to attract speculative safeguards, abstractions, dependencies, compatibility paths, or future-proofing.
   - Include `Child Rolling-Wave Project` only when non-`none` or when the parent/child relationship could be ambiguous.
   - Include `Parallel Work Chunks` only when implementation can actually be split into useful independent ownership areas; otherwise omit it or record one terse `serial_reason`.
   - Include suggested owner, reason, human handoff, agent fallback, and timebox only for chunks where ownership is non-obvious or human/hybrid.
   - Name new slices `NNN-slug.md`.
   - Keep the selected slice `pending` during drafting and independent grilling.
   - Leave all other slice statuses unchanged. More than one `ready`, `in progress`, `ready for review`, or `in review` slice is valid.
   - Update `project.md` only for material roadmap pressure, cross-slice decisions, risks, or change history. Do not add routine rows for ordinary slice preparation.
   - Before saving, convert long prose into table rows or `key: value` bullets and remove duplicate facts that already live in the parent project or child project.
   - Keep `Readiness Notes` to reviewer deltas, resolved questions, redirects, and explicit deferrals. Do not summarize the original contract there.

### Independent Review

6. When the preparation-review gate requires it, delegate the grill to one fresh-context subagent.
   - Use `model="gpt-5.6-terra"` and `reasoning_effort="medium"` by default. Use `gpt-5.6-sol` only for security, data-loss, irreversible migration, or unresolved public-contract conflicts.
   - Spawn with no conversation history, such as `fork_turns="none"`. Give it the repository root, project path, selected slice path, immutable constraints, and the author's neutral evidence index.
   - Do not pass the draft author's rationale, recommendations, confidence, or a suspected answer. Objectivity depends on reconstructing conclusions from the artifact and repository.
   - Instruct it to use `$grill-me` in `prepare-review` mode on the selected slice contract, validate the highest-risk claims, edit the same slice artifact directly, avoid product-code changes, preserve `status: pending`, and return one of:
     - `ready`: material branches resolved or safely deferred
     - `question`: one highest-leverage user question with evidence and a recommended answer
     - `blocked`: exact missing dependency or evidence
     - `redirect`: prerequisite or replacement slice path plus neutral evidence index
   - Use a soft standard budget of about three minutes and twelve repository queries. Verify representative high-risk evidence instead of recreating every inventory. Inspect beyond the evidence index only when a material risk requires it.
   - Keep the same reviewer for follow-up turns. If it returns `question`, relay that single question to the user, then send the answer back to the reviewer. Continue until `ready`, `blocked`, or `redirect`.
   - Challenge reviewer findings when stronger repository evidence conflicts. Send the evidence back for reconciliation instead of silently overriding or blindly accepting the finding.
   - Do not add more reviewers by default. One independent pass provides the context separation without turning preparation into review theater.
   - If fresh-context subagents are unavailable, run `$grill-me` `prepare-review` inline and disclose that context separation was unavailable.

### Final Readiness

7. Finalize readiness in the main context.
   - Confirm any required independent review left no unresolved material branch or unsafe deferral. When review was skipped, confirm the recorded reason still satisfies the preparation-review gate.
   - Run the review-budget check: one reviewer question, one bounded verification strategy, compatible risk class and intermediate state, and a plausible focused human pass.
   - Treat this as a metadata and consistency gate. Do not repeat repository discovery, consumer scans, or evidence validation already completed during authorship or review unless outputs conflict or leave a concrete gap.
   - Do not split merely because a chunk is independently useful, executable, revertible, or separately committable.
   - Split the roadmap item or route it to a child project if that check fails.
   - Mark only the selected slice `ready`.
   - Preserve its `Original Slice Contract` from this point onward.

## Completion

Stop after the slice is `ready`. Do not implement. Keep the final response very short and include:
- slice path
- `Implementation preview:` one or two short sentences naming the concrete behavior or code changes the prepared slice will implement; describe the intended result, not the preparation process
- unresolved items, only when explicitly deferred

Omit routine caveats for planning-only work. Do not say that no code tests were run or that `docs/rolling-wave/` is gitignored unless the user asked about verification, persistence, or file visibility, or unless an attempted validation step failed.
