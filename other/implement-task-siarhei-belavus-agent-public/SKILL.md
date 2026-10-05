---
name: implement-task
description: Implement a planned task from `.plans/<task-slug>/` with strict plan adherence, explicit amendments, and no direct writes to tracked `AGENTS.md`.
---

# implement-task

Implement changes so they are correct, reviewable, and maintainable. Optimize for small safe increments, clear ownership, explicit validation, and low future change cost.

Treat `PLAN.md` as a contract. Do not improvise around it silently.

## Read first

- `../references/task-packet-contract.md`
- `../references/persistent-artifacts-contract.md`
- `../references/review-phases-contract.md`
- `../references/compatibility-policy.md`
- `../references/ownership-and-reuse-policy.md`
- `../references/final-state-authoring-policy.md`
- `../references/initiative-workflow-contract.md` when implementing an initiative child packet
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain
- applicable `AGENTS.override.md` only if local execution constraints matter
- current task packet: `INDEX.md`, `PLAN.md`, `AMENDMENTS.md`, `ARTIFACT_CANDIDATES.md`

## Implementation workflow

1. Establish scope before coding.
   - Confirm the task, desired behavior, constraints, and nearby boundaries.
   - Refuse to start without `PLAN.md`.
   - Prefer root-cause fixes over surface patches when the cause is clear and local.
2. Repair packet drift before coding.
   - If `AMENDMENTS.md` or `ARTIFACT_CANDIDATES.md` is missing, create the missing placeholder before continuing.
   - Note the packet repair in `INDEX.md`.
3. Identify the true change surface.
   - Find the owner modules, contracts, state transitions, persistence paths, tests, and tracked `AGENTS.md` constraints that define the behavior.
   - Distinguish direct edits from incidental neighbors.
   - Distinguish internal boundaries from real external contracts relative to the service.
   - Avoid changing unrelated code unless it is a tiny blocker in the same area.
4. Apply ownership-and-reuse policy.
   - Identify the existing owner for each important behavior or invariant before adding code.
   - Prefer reusing, extending, or slightly refactoring that owner over creating a parallel helper/service/adapter/store/module/type.
   - If existing code is close but awkward, do a small tidy-first refactor that makes reuse possible.
   - Do not keep old and new same-purpose implementations alive together.
   - If a genuinely new boundary is required, make the non-overlapping responsibility explicit in code and packet notes.
5. Apply the compatibility policy.
   - Backward compatibility is prohibited by default.
   - Do not add aliases, shims, dual support, fallback behavior, or compatibility wrappers unless the human explicitly required compatibility.
   - If the change touches a real external boundary and compatibility requirements are unresolved, stop and ask the human explicitly before proceeding.
   - For internal-only changes, do not ask and do not preserve compatibility.
6. Implement the chosen target state directly.
   - Move canonical code/docs/contracts toward the steady-state design described in the plan.
   - Remove superseded vocabulary and same-purpose residue inside owner artifacts instead of layering new semantics on top of old names.
   - If a real external boundary requires temporary compatibility behavior, keep the steady-state owner and current contract obvious.
7. Implement in reviewable increments.
   - Follow the plan strictly.
   - Keep the system coherent after each step where possible.
   - Prefer centralizing risky logic rather than spreading coordinated edits across helpers.
   - Separate structural refactors from behavior changes unless combining them is clearly safer.
8. Preserve maintainability while coding.
   - Keep ownership obvious.
   - Minimize new sources of truth.
   - Avoid hidden cross-file contracts when a local explicit contract will do.
   - Write code so a human can find, understand, and change it later without reconstructing half the project.
   - Keep canonical owner artifacts in one vocabulary and one state model.
9. Validate deliberately.
   - Start with the smallest test or check that proves the changed behavior.
   - Expand validation as confidence grows.
   - If the risky path is retry/restart/cancel/recovery, validate that path directly rather than relying on happy-path tests.
10. Hand off cleanly.
   - Keep `AMENDMENTS.md`, `ARTIFACT_CANDIDATES.md`, and `INDEX.md` current enough that both review phases can start cold.
   - Record durable residue candidates when they appear.
   - Commit the implementation pass before reporting back to the lead.
   - Never write tracked `AGENTS.md` or `AGENTS.override.md` directly.

## Plan adherence rule

- Never silently deviate from the agreed plan.
- Unauthorized backward-compatibility work counts as plan drift unless the plan or later human amendment required it explicitly.
- A new same-purpose entity that the plan did not explicitly justify also counts as plan drift.
- Leaving canonical code/docs/contracts in a visible old-plus-new hybrid shape also counts as plan drift when the target design is already known.
- If implementation reveals a blocker, contradiction, or new fact that makes the plan unsafe or impossible, stop execution.
- Report:
  - the exact reason the plan can no longer be followed
  - the available options
  - pros and cons of each option
  - how each option changes the plan
- Let the human choose.
- After the human decides, update `AMENDMENTS.md` before continuing implementation.

## Suboptimal plan rule

- If the plan seems workable but suboptimal, do not silently improve it during implementation.
- Stay on plan.
- Leave a `REVIEW_NOTE:` at the relevant implementation point describing the better option and why it may be preferable.
- Treat `REVIEW_NOTE` as advisory only; it does not authorize changing scope or design.

## Implementation principles

- Make the safest next edit obvious.
- Prefer local reasoning over clever indirection.
- Keep risky logic centralized.
- Leave the code easier to review than before.
- Make canonical owner artifacts read like the current system, not like notes about an in-progress migration.
- Avoid plans-in-code that only make sense if someone already knows the backstory.
- Prefer tidy-first reuse over greenfield duplication.
- Keep one authoritative implementation path per important behavior whenever possible.

## When to slow down

Pause and think harder when:

- the task changes persistence or state ownership
- restart, retry, cancellation, or recovery semantics are involved
- the change introduces a second source of truth
- the easy fix requires scattered coordinated edits
- a test passes, but does not actually prove the risky behavior
- the real code shape disagrees with the plan
- a better design appears mid-implementation but was not approved in the plan
- you are about to add a new same-purpose entity because the current owner is inconvenient to reuse

## Initiative child packets
For initiative-created child packets:
- stop immediately if `PLAN.md` still says `Status: not_authored`
- mutate code plus child packet artifacts only
- route parent initiative truth changes through `sync-initiative`, not ad hoc edits during coding
- keep `Parent Initiative`, `Imported Context`, dependencies, and optional `CONTRACT_DECISION.md` visible while implementing

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.

## Stateful implementation

For queues, workers, orchestration, durable tasks, async services, or other lifecycle-heavy code, explicitly preserve:

- valid state transitions
- consistent writer/reader behavior
- idempotent or intentionally controlled side effects
- truthful status and recovery behavior

## Human maintainability rule

Implement so a human can later:

- find the owner logic quickly
- understand the contract without archaeological digging
- make a safe change with low context load
- know which tests prove the behavior
- change one owner instead of coordinating multiple same-purpose implementations

## Review-fix loop

Treat routed review findings as executable work, not FYI.

When the lead routes `P#`, `PS#`, or `M#` findings back to you:

- start the fix pass immediately in the same turn unless a human decision is required
- do **not** stop after acknowledgement, status restatement, or repeating the findings back
- do **not** wait for an extra `proceed` if the requested fixes are within the approved plan or recorded amendments
- only pause before editing when the finding exposes true plan contradiction, missing decision authority, or unresolved external-compatibility requirements
- after the fix pass, rerun the smallest validation that proves the finding is resolved, update packet artifacts, commit that fix pass, then report results

If a finding is unclear, sharpen it fast and then keep moving. Do not normalize a review loop into `ack -> wait`.

## Commit-before-report rule

For implementation work that changed the workspace:

- make a focused git commit before reporting back to the requester
- do this for the initial implementation pass and after every review-fix cycle
- use a Conventional Commit message that matches the actual change
- include the commit hash and subject in the handoff
- if no files changed because you are blocked or only asking a question, do not make a dummy commit; report the blocker instead

## Requester-response rule

Always report the result back to the requesting side.

- If the lead/orchestrator requested the implementation or review-fix pass, reply back to the lead/orchestrator.
- If a human directly requested the implementation or steering in this pane, reply back in this pane.
- Local pane output, scratch notes, or status text without an explicit reply to the requester does not count as completion.

## Review alignment

Code so the eventual reviews can cleanly answer:

- what changed
- why it changed here
- what proves it works
- whether maintainability improved or degraded
- whether any durable residue should be distilled later into tracked `AGENTS.md`
- whether ownership stayed single and obvious

## Output shape

Default implementation handoff should leave behind:

- updated code
- actual validation run
- packet updates needed for review
- key remaining risks or limits

## Avoid

- broad opportunistic refactors during a focused task
- scattering one behavior across many files without strong reason
- introducing hidden contracts when explicit ones are possible
- relying on tests that do not cover the risky path
- `works for now` fixes that obviously raise future maintenance cost
- silent plan drift
- self-approving design changes during implementation
- adding backward-compatibility scaffolding by default
- asking about backward compatibility for internal-only changes
- introducing a parallel same-purpose helper/service/adapter/store/module/type instead of tidying and reusing the current owner
- writing tracked `AGENTS.md` directly
- writing `AGENTS.override.md`
