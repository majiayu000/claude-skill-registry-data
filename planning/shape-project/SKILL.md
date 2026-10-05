---
name: shape-project
description: Shape or update a rolling-wave engineering project before slice preparation. Use when the user wants to start a rolling-wave project, define the finish line, clarify success criteria, create or update docs/rolling-wave/{project}/project.md, sketch a broad roadmap, or interrogate project-level direction without implementation details.
---

# Shape Project

## Core Invariants

- Work under `docs/rolling-wave/{project}/`.
- Store project-level state in `project.md`; store slices in `slices/NNN-slug.md`.
- Use slice statuses: `pending`, `ready`, `in progress`, `ready for review`, `in review`, `done`.
- Multiple slices may be `ready`, `in progress`, `ready for review`, or `in review` concurrently. Each workflow invocation operates on one explicitly resolved slice.
- Accept user preferences by default, but push back when strong evidence conflicts with the workflow, prior decisions, terminology, or constraints.
- Pushback format: "I disagree because... The likely consequence is... Continue anyway?"
- Do not modify product code. This skill only creates or updates rolling-wave planning artifacts.
- Shape the whole project, not the first slice. `shape-project` defines the global finish line, success criteria, non-goals, constraints, risks, and broad roadmap across all slices.
- Slices are concrete implementation steps, not general project phases. Each slice should produce a reviewable change toward the finish line.
- Slices are delivery sequence and implementation-detail containers. Do not use "later slice" as a way to avoid deciding whether something belongs in the project finish line.
- Keep executable slices within one bounded human review decision. A slice may contain multiple independently executable or revertible chunks when one architectural intent or transformation recipe, risk class, and verification strategy cover them. Commit count, file count, domain count, and raw diff size are signals, not limits.
- A slice may be backed by another rolling-wave project when that slice is large enough to need its own finish line, roadmap, and review loop. Treat that as a parent/child planning relationship, not as de-scoping from the parent project.
- Project and slice artifacts are agent state, not human-facing documentation. Prefer stable headings, terse `key: value` bullets, IDs, and tables over explanatory prose.
- Keep skill mechanics out of project artifacts. Rules like "planning only in this phase", "do not modify product code", "ask one question at a time", or "write under docs/rolling-wave" are workflow instructions for the agent, not project constraints, non-goals, assumptions, risks, or decisions.
- Optimize for enough shared direction to prepare the next slice, not for a perfect project document.

## Interaction Rules

- Ask one question at a time only when user input is required to avoid a material planning mistake.
- Prefer bounded choices when selecting among clear alternatives.
- Use open prose questions when the answer should reveal context, evidence, or uncertainty.
- Do not ask questions already answered by existing artifacts.
- When you ask the user a shaping question, stop and wait for the answer. Do not answer it yourself and continue in the same turn unless the user explicitly asked you to make the call.
- When proposing low-risk assumptions, label them and proceed; do not force a confirmation turn just to make the artifact cleaner.
- Do not one-shot risky broad roadmaps. For straightforward projects, recommend one sequence and record uncertainty instead of presenting multiple options.
- Do not use `Open Questions` as a substitute for decisions that affect the finish line, first slice, public behavior, irreversible migration, or major cost/risk. Safe deferrals may be recorded without asking first.
- If exactly one high-impact project-shape blocker remains, ask it before finalizing. If it is low or medium impact, record it as an assumption or deferred question.
- Create or update `project.md` once the project is ready enough, unless the user explicitly asks to discuss before writing or the remaining uncertainty is high impact.

## Workflow

0. Assess shaping depth and subject clarity.
   - If the requested project subject is too vague for another agent to identify, ask what project to shape before doing anything else.
   - Classify the shaping need as `lightweight`, `standard`, or `deep`.
   - Lightweight shaping may produce a compact provisional `project.md` with minimal questioning.
   - Standard shaping should ask only for high-impact blockers and otherwise proceed on labeled assumptions.
   - Deep shaping should pressure-test direction before creating roadmap slices.
   - Shape at full ambition within the named project, but do not widen into adjacent projects unless the current project cannot be coherent without them.

1. Resolve the project.
   - If the user names a project, use that slug or create it if missing.
   - If exactly one project exists under `docs/rolling-wave/`, use it.
   - If multiple projects exist and none was named, ask which one to use.
   - Before creating a new project, normalize the requested slug and compare it with existing project folders. Push back if it strongly overlaps.

2. Inspect existing context.
   - Read existing `project.md`, slice files, nearby planning docs, and any user-provided requirements.
   - Auto-resolve answers from artifacts before asking the user.
   - Treat explicit user requirements, named docs, and existing `project.md` decisions as constraints.
   - Treat nearby docs, old slice notes, and inferred repo context as background unless the user names them as constraints.
   - Do not treat this skill's own workflow rules as project context. They govern the current shaping session only.
   - If `project.md` already exists, shape as an update: preserve prior decisions unless the user explicitly changes them, keep completed slice history intact, and move stale assumptions only when artifact evidence supports the change.
   - If context is thin, do not ask unlimited questions, but still meet the ready-enough shaping gate before writing: finish line, observable success criteria, scope boundaries, likely first implementation slices, and any product/API/policy decision that would materially change the first slice or final outcome.
   - Label remaining assumptions clearly only when they are low-impact, evidence-backed, or explicitly safe to defer to slice preparation.

3. Grill project-level direction until the project is ready enough.
   Ask one high-leverage question at a time. Cover:
   - finish line
   - success criteria
   - non-goals
   - constraints
   - assumptions
   - broad implementation slice sequence
   - dependencies
   - project-level risks
   - expected learnings

   Keep scope and sequencing separate:
   - First decide whether a requirement, behavior, risk, or non-goal belongs in the overall project shape.
   - Only after project scope is clear should the roadmap decide which slice handles it.
   - Do not ask whether a project-level requirement should be "deferred to a later slice." Ask whether it is in scope for the project at all, then record likely sequencing separately.
   - If something is too risky for the first slice but still part of the desired outcome, keep it in the project finish line or roadmap and sequence it later. Do not turn sequencing into accidental de-scoping.

   Keep slices implementation-shaped:
   - A slice is a concrete step that `prepare-next-slice` can turn into an implementation contract and `implement-slice` can build.
   - Prefer the largest batch that still fits one bounded review decision and moves the project forward without mixing risk classes.
   - Keep code, types, config, migration, docs, and other tightly coupled changes together when a reviewer needs their combined context to judge the outcome.
   - Group chunks by reviewer question and verification method. A mechanical relocation batch may cross domains when one transformation recipe applies, behavior stays unchanged, each moved unit includes consumers and existing tests, and rename-aware review separates moves from edits.
   - Split a proposed slice when chunks need separate product or architecture approval decisions, unrelated mental models, distinct risk classes, incompatible intermediate states, or materially different verification strategies.
   - Do not split merely because chunks are independently useful, executable, revertible, or could be accepted as separate commits.
   - Do not split merely to satisfy commit, file-count, or diff-size targets. Avoid temporary glue, fake sequencing, and review fragmentation.
   - Use roughly 500 non-move changed lines as a soft default review budget. Lower it for high-semantic or high-risk work; allow larger repetitive mechanical diffs when one proof covers the batch.
   - Parallel chunks divide execution ownership and review navigation inside one review decision. Prefer one to three chunks.
   - Plan broad test coverage as a final testing/validation slice after the implementation slices have settled. Earlier slices may record test backlog, probes, or verification intent, but should not require full test implementation.
   - If a concrete slice grows large enough to have its own global finish line, success criteria, and internal sequence, keep it as one parent slice and create or reference a child rolling-wave project under `docs/rolling-wave/{child-project}/`.
   - Do not expand a child project's internal slices into the parent roadmap unless the parent genuinely needs to track those steps separately.
   - Record the parent slice's completion condition in parent terms, for example "child project reaches its finish line and exports the migration notes needed by the parent project."
   - Do not create slices that are only project phases, research phases, planning phases, validation phases, or vague lifecycle stages.
   - Avoid slice names like "Design the approach", "Validate compatibility", "Phase 1", or "Future hardening" unless they are rewritten as concrete implementation deliverables.
   - Good slice framing names the product/code behavior that will change, for example "Add entitlement-aware catalog inputs" or "Filter list_items from the builtin catalog when item read is unavailable".
   - Research, design, validation, and compatibility checks belong inside the relevant implementation slice as readiness, verification, risks, or acceptance criteria unless they produce a standalone reviewable artifact needed by implementation.

   Scan for these gaps and probe only the gaps that are actually present:
   - Finish-line gap: completion is described as activity rather than an observable end state.
   - Success gap: success criteria are vague, subjective, or generic.
   - Scope-boundary gap: likely adjacent work is not explicitly included or excluded.
   - Dependency gap: the roadmap assumes unresolved inputs, tools, access, or decisions.
   - Sequencing gap: early slices do not reduce uncertainty or do not produce reviewable implementation progress.
   - Risk gap: cross-slice risks are likely but not recorded.
   - Learning gap: early slices do not identify what they should teach later slices.
   - Open-question gap: the artifact would contain a project-level question that has not actually been asked.

   If useful, derive 3-5 project axes such as user workflow, data shape, migration risk, rollout, docs, or reliability. Use them only to check question coverage, not to create a detailed upfront plan.

   Classify unresolved questions before writing:
   - Ask-now questions materially affect the finish line, success criteria, scope, non-goals, first slice, public/user-facing behavior, compatibility policy, rollout policy, irreversible migration, or major project-level risk.
   - Safe deferrals are implementation details for a future slice, low-impact unknowns, facts that slice preparation can verify from code, or items the user explicitly chooses to defer.
   - Ask-now questions cannot be silently moved into `Open Questions`. Ask them one at a time, or record an explicit user deferral.

4. Shape and grill the broad implementation slices.
   This is not `prepare-next-slice`; do not fully specify each slice. The goal is shared understanding of the broad delivery sequence.

   Before writing roadmap rows:
   - Recommend one broad slice sequence by default.
   - Propose 2-3 plausible slice sequences only when ordering materially changes risk, cost, reversibility, or what the first slice can teach.
   - For each option, summarize the sequencing tradeoff in one sentence: what it learns early, what it delays, and what risk it carries.
   - Recommend one sequence when evidence favors it, and push back if the user's preferred sequence has strong evidence against it.
   - Ask the user to choose, combine, or correct the broad sequence only when the choice is high impact. Otherwise write the recommended order as an assumption.

   Grill the chosen or likely sequence enough to catch bad slices:
   - Are the slices implementation steps rather than phases?
   - Does each slice produce a reviewable change or artifact needed by implementation?
   - Does each slice present one reviewer question with a bounded verification strategy?
   - Should any broad slice split because it requires separate approval decisions or risk conversations?
   - Could small roadmap items sharing one mechanical recipe or verification method be batched even across domains?
   - Does the first slice reduce a meaningful uncertainty or create the smallest useful foundation?
   - Are later slices broad enough to stay flexible, but concrete enough that `prepare-next-slice` can refine them?
   - Is there a final testing/validation slice that can lock down the settled project behavior after implementation churn?
   - Are dependencies and learnings flowing forward between slices?
   - Are any important requirements accidentally missing because they were treated as "later" rather than in-scope?
   - Are any slices too large for one slice contract and better represented as a child rolling-wave project?

   Ask only the highest-leverage roadmap questions. Stop once the user and agent share a rough slice map, not when every slice has a full contract.

5. Avoid implementation detail.
   - Keep file/function decisions out unless they materially change scope, risk, sequencing, or feasibility.
   - Record tempting implementation details as notes only when they affect project shape.

6. Present or write the project-shape synthesis.
   - Summarize `Stated`, `Inferred`, and `Out of scope`.
   - Include the proposed broad slice sequence and call out any remaining roadmap uncertainty.
   - Include any remaining ask-now questions separately from safe deferrals.
   - Exclude skill mechanics from the synthesis unless the user explicitly wants to document the planning process.
   - Ask unresolved ask-now questions before asking the user to confirm the synthesis.
   - For lightweight or standard shaping, write the artifact in the same turn when the remaining uncertainty is safe to defer.
   - Ask the user to confirm or correct the synthesis before writing only for deep shaping, high-impact uncertainty, or a material change to existing project direction.
   - After asking for confirmation, stop and wait. Do not write the artifact in the same response as the confirmation request.
   - If the user corrects it, revise the synthesis before updating artifacts.

7. Write or update `docs/rolling-wave/{project}/project.md`.
   - Use `../rolling-wave-common/references/artifacts.md` for the project template.
   - Use `../rolling-wave-common/references/lifecycle.md` for slice status rules.
   - Optimize the artifact for future agent retrieval, not human readability: compact tables, stable IDs, canonical statuses, paths, and one fact per canonical section.
   - Avoid narrative summaries, intro paragraphs, duplicated rationale, or polished prose. Put human-facing explanations in chat or `exec-summary`, not in `project.md`.
   - Create `slices/` if missing.
   - Add broad future implementation slices as `pending` when useful.
   - Update change history only for material direction changes, not routine artifact cleanup.
   - For each major project-level decision, include a basis when it is not obvious: `direct`, `prior`, or `reasoned`.
   - Before saving, remove skill-leak text from project sections. Examples: "planning only in this phase", "this skill does not modify product code", "use shape-project first", "ask one question at a time", or any statement that describes the agent workflow rather than the project.
   - Before saving, audit `Open Questions`: each item must be either explicitly asked and left unanswered/deferred by the user, or clearly safe to defer to a later slice-preparation conversation.

   Roadmap slices should describe implementation-step outcomes and learning order, without over-planning file/function details. A good pending slice has:
   - a clear reviewable implementation outcome
   - one bounded review decision with review-sized scope
   - a reason it belongs before or after nearby slices
   - enough scope signal for later `prepare-next-slice`
   - an implied product/code/docs change that can be implemented and reviewed
   - no detailed file/function/API design unless it changes sequencing or risk
   - a child-project reference when the slice is intentionally managed by another rolling-wave project

   Before saving, normalize artifact style:
   - convert long prose to short table rows or `key: value` bullets
   - assign IDs to success criteria, constraints, assumptions, decisions, open questions, risks, and review notes
   - remove duplicate facts from secondary sections and replace them with paths or IDs
   - keep only decision-relevant `why` or `basis` text

   Before saving, rewrite phase-like roadmap items into implementation slices. If an item cannot be expressed as a concrete implementation step, record it as a risk, open question, verification concern, or cross-slice decision instead of a slice.

8. Run a ready-enough coverage check.
   - Every required shaping area has an answer, explicit deferral, or recorded unknown/risk.
   - Every high-impact project-shape question was asked, auto-resolved from evidence, or explicitly deferred by the user before writing.
   - Generic success criteria are sharpened into observable outcomes.
   - Cross-slice decisions and risks are recorded at project level.
   - Requirements are either in the project finish line, explicitly out of scope, or recorded as project-level unknowns; they are not hidden inside "later slice" language.
   - `Open Questions` does not contain unasked high-impact blockers.
   - No section contains skill mechanics presented as project facts.
   - Each roadmap slice is an implementation step, not just a general project phase.
   - The broad slice sequence is either confirmed or recorded as a low-risk assumption.
   - The next planned slice is clear enough for `prepare-next-slice`.
   - Every executable roadmap slice fits one bounded human review decision. Independently useful chunks may remain batched when one intent or transformation recipe, risk class, and verification strategy cover them; separate approval decisions are split.

## Completion

Stop when the project has enough global direction to define the desired end state and broad slice sequence without pretending later slices are fully specified.

Report:
- the shaped project path
- the finish line in one sentence
- the next planned slice and why it should come next
- assumptions or risks that should carry into `prepare-next-slice`

Omit routine caveats for planning-only work. Do not say that no code tests were run or that `docs/rolling-wave/` is gitignored unless the user asked about verification, persistence, or file visibility, or unless an attempted validation step failed.

Do not start slice preparation unless the user explicitly asks.
