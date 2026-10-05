---
name: plan-task
description: Plan a development task into a self-sufficient execution contract stored in `.plans/<task-slug>/` for later fresh-context implementation and review.
---

# plan-task

Turn ambiguous engineering work into a concrete execution contract. Plan for a fresh implementer, not for the current chat.

Assume the plan will be followed strictly unless a human explicitly amends it.
Assume implementation may happen in a clean context window with no access to prior conversation.

## Read first
- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/compatibility-policy.md`
- `../references/ownership-and-reuse-policy.md`
- `../references/final-state-authoring-policy.md`
- `../references/initiative-workflow-contract.md` when planning an initiative child packet
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter

## Planning workflow
1. Establish scope.
   - Clarify the exact task, desired outcome, constraints, and what is out of scope.
   - Prefer concrete deliverables over vague goals.
   - Name the real acceptance criteria early.
2. Identify the true change surface.
   - Find the owner modules, state transitions, APIs, persistence paths, tests, and tracked `AGENTS.md` constraints the task will affect.
   - Distinguish direct change points from incidental neighbors.
   - Distinguish internal boundaries from real external boundaries relative to the service.
   - If the task is lifecycle-heavy, treat restart, retry, cancellation, and recovery as first-class planning concerns.
3. Resolve ownership and reuse first.
   - Identify the current owner for each important behavior, invariant, or responsibility.
   - Prefer reusing, extending, or slightly refactoring that existing owner over introducing a parallel entity.
   - If existing code is close but awkward, plan a tidy-first refactor that makes reuse possible.
   - Only allow a new helper/service/adapter/store/module/type when the new boundary is explicitly different and non-overlapping.
   - If the plan would leave two same-purpose entities alive, treat that as a design problem and rewrite the plan.
4. Resolve compatibility policy correctly.
   - Backward compatibility is prohibited by default.
   - Do not add compatibility work to the plan unless the human explicitly asked for it.
   - If the task touches a real external boundary and compatibility requirements are unresolved, stop and ask the human explicitly whether backward compatibility is required.
   - For internal-only changes, do not ask; plan the clean internal change with no compatibility scaffolding.
5. Write the target state, not the migration story.
   - Describe the intended steady state directly: final owners, final vocabulary, final status model, final artifact layout.
   - Do not write canonical plan steps as `old + new`, `keep this for now`, `add another path`, or similar transition prose when the clean final design is already known.
   - If a real external boundary truly requires compatibility work, keep the steady-state owner and current contract obvious in the plan.
6. Bootstrap the packet.
   - Create or update `.plans/<task-slug>/INDEX.md`.
   - Create empty canonical placeholders for `AMENDMENTS.md` and `ARTIFACT_CANDIDATES.md` immediately, even if they are still empty.
   - Ensure `INDEX.md` points to those files from the first packet version.
   - `BRIEF.md` is optional. Use it only when discovery output needs to be normalized into a compact handoff artifact before writing `PLAN.md`.
   - `grill-me` may populate `BRIEF.md`; `plan-task` may normalize, complete, or create it if discovery context has not yet been captured cleanly.
7. Define success before steps.
   - State the observable behavior that must be true when the task is done.
   - Define validation early: tests, checks, smoke paths, or user-visible outcomes.
   - Call out unknowns, assumptions, and risky edges before finalizing sequencing.
8. Slice the work into low-risk increments.
   - Prefer steps that keep the system coherent after each increment.
   - Separate foundational refactors from behavior changes unless combining them is clearly safer.
   - Favor plans that are easy to review and easy to revert.
9. Plan for amendment, not improvisation.
   - State exact stop conditions.
   - Make it explicit that implementation must stop if the plan becomes unsafe, impossible, or contradicted by the codebase.
   - Require amendment flow: blocker, options, pros/cons, plan impact, human decision, packet update.
   - If a better but non-essential design appears during implementation, require a `REVIEW_NOTE` rather than silent deviation.
10. Optimize for human maintainability.
   - Minimize how much context a human must hold at once.
   - Prefer plans that centralize risky logic, reduce change amplification, and keep ownership obvious.
   - Avoid plans that require many synchronized edits unless there is no safer alternative.
11. Make the plan self-sufficient for handoff.
   - Name the concrete target models, contracts, files, artifact paths, and boundaries instead of relying on chat shorthand.
   - Include exact terminology when names affect correctness.
   - State failure behavior and unsupported-capability behavior explicitly when implementation would otherwise have to guess.
12. Produce the plan.
   - Write `PLAN.md` as the canonical execution contract.
   - Keep the steps ordered, imperative, and dependency-aware.
   - If likely durable residue is already obvious, note it in `ARTIFACT_CANDIDATES.md`; do not write tracked `AGENTS.md`.

## Planning principles
- Plan for the real dependency graph, not the order the idea was explained.
- Make the safest next step obvious.
- Keep steps independently verifiable where possible.
- Prefer plans that simplify later review, not just faster coding.
- If one safe pass is unrealistic, split the work into phases instead of pretending it is one change.
- Eliminate hidden branches: if the plan intends one design, say `do X`, not `do X or Y`.
- Prefer imperative decisions over advisory wording when implementation should not choose among alternatives.
- Prefer tidy-first reuse over greenfield parallel abstractions.
- Keep one owner and one authoritative path per important behavior whenever possible.
- Write `PLAN.md` as the target design artifact, not as a migration diary.

## Good plan qualities
A strong plan:
- defines done in observable terms
- identifies risky edges early
- keeps each step reviewable
- explains why the order matters
- includes validation strategy
- defines amendment triggers
- reduces future maintenance burden, not just present effort
- is self-sufficient enough for another agent to execute cold
- leaves no important term, rename, or target contract open to interpretation
- makes the owner and reuse path obvious instead of leaving room for parallel implementations
- reads like the current intended system, not like notes about how the old system is being patched

## Anti-ambiguity rules
- Do not present multiple design branches unless the human is explicitly being asked to choose.
- Do not use vague wording like `consider`, `might`, `could`, `recommended`, or `where possible` for core implementation decisions.
- Do not rely on a new implementer to infer final naming for important types, fields, keys, endpoints, or artifacts.
- Do not leave failure behavior implicit. Say whether the system warns, fails fast, retries, skips, or continues.
- Do not leave ownership implicit. Say which layer owns the contract, which layer adapts it, and which layer consumes it.
- Do not leave cleanup as an unspecified follow-up. Name legacy fields, shims, tests, or docs that must change.
- Do not introduce backward-compatibility branches, aliases, wrappers, or fallback behavior unless the human explicitly required compatibility for a real external boundary.
- Do not allow the plan to create a second same-purpose entity when a tidy-first refactor of the current owner would make reuse possible.
- Do not let canonical plan prose teach both an old and a new model when one final model is already chosen.

## Stateful-system planning
For queues, runners, durable workflows, async services, orchestration, or any lifecycle-heavy feature, explicitly plan for:
- state ownership
- recovery and restart
- retry and idempotency
- cancellation and partial progress
- truthfulness of status, logs, and persisted state

## Human maintainability rule
Ask:
- How many files will the implementer need open at once?
- Is there one obvious owner per step?
- Can each step be reasoned about locally?
- Will the final design lower or raise navigation cost?
- Will future changes touch one owner or require coordinated edits across same-purpose entities?

## Review alignment
Shape plans so later reviews can answer cleanly:
- what changed
- why the order mattered
- what proves the behavior
- whether maintainability improved or degraded
- whether any durable residue should later be distilled into tracked `AGENTS.md`
- whether the design kept one owner and one authoritative implementation path

## Requester-response rule

Always report the result back to the requesting side.

- If the lead/orchestrator requested the planning pass, reply back to the lead/orchestrator.
- If a human directly requested the planning pass in this pane, reply back in this pane.
- Local stdout/status text without an explicit reply to the requester does not count as completion.

## Output shape
Default output should leave the packet with:
- `INDEX.md`
- `PLAN.md`
- `AMENDMENTS.md`
- `ARTIFACT_CANDIDATES.md`
- optional `BRIEF.md`

## Do not
- depend on chat-only context
- restate the user request without turning it into an execution contract
- mix unrelated concerns in one step without justification
- treat validation as an afterthought
- leave naming, ownership, or failure behavior implicit
- write tracked `AGENTS.md` directly
- write `AGENTS.override.md`
- plan backward-compatibility work by default
- ask about backward compatibility when the change is internal-only
- propose a parallel same-purpose entity when a small tidy-first refactor would unlock reuse
- write canonical artifacts as if they were migration notes instead of the target design

## Initiative-created child packets
If the packet already exists because `hydrate-child-packet` created it:
- read `INDEX.md`, `BRIEF.md`, optional `CONTRACT_DECISION.md`, placeholder `PLAN.md`, `AMENDMENTS.md`, and `ARTIFACT_CANDIDATES.md` in that order before planning
- treat `Parent Initiative` and `Imported Context` as the frozen handoff from the parent initiative
- replace the placeholder `PLAN.md` that says `Status: not_authored`; do not bootstrap parallel packet files
- update child `INDEX.md` to `Packet phase: plan_authored`
- keep standalone-task bootstrap behavior unchanged when there is no parent initiative

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
