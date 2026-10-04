---
name: ln-build
description: "Implement one scoped slice using TDD red-green-refactor. Use when ready to write code for a defined slice of work, or when the user wants test-driven development."
argument-hint: "[paste or reference an ln-scope card]"
---

# Ln Build

Implement **one** scope card. Beck's red-green-refactor, one cycle, no scope creep.

## Input

A full or light scope card from `ln-scope`, the next ready card in `memory/CARDS.md`, or a trivial direct-fix request: $ARGUMENTS

Extract: target behavior / objective, acceptance criteria, and verification approach.

Treat the scope card as the next implementation slice inside its containing `memory/PLAN.md` frontier item. The frontier item is the plan-level work item and Linear/branch unit; the scope-card slice is just the current execution step inside it. Unless `ln-plan` has already split the frontier into separate items, do **not** infer a new Linear issue or Graphite branch from scope-card granularity; multiple consecutive slices may land on the same branch.

If `memory/CARDS.md` exists, treat it as a derivative execution queue, not canonical planning state. Start with the next card marked `next` or the first unfinished card in that file. If that card is already satisfied on the current branch, do **not** manufacture a no-op build commit; verify the acceptance criteria, mark the card `done` or `dropped` as appropriate, reconcile the queue, and either continue to the next honest build target or route back to `ln-scope` if no build remains.

Re-enter before red.

If this is a fresh thread or an unfamiliar area, reload:

1. `memory/SPEC.md`
2. `memory/PLAN.md`
3. `HANDOFF.md` if present
4. `docs/archive/PLAN_HISTORY.md` only if the frontier or touched area is still unclear

Write a 2-4 bullet orientation note naming the containing seam, the frontier item, any manual verification debt, and the main open risk.

If the request is a direct fix and you cannot name the containing seam or whether it is settled, stop and route through `ln-scope` first.

Do not invent new planning docs, scratch histories, or alternate memory locations while building. Durable state reconciles back into `memory/SPEC.md` and `memory/PLAN.md`; temporary support artifacts stay in `HANDOFF.md`, `memory/CARDS.md`, or `memory/REFACTOR.md` only while they are still live.

## Serial execution mode

When several prepared slice cards already exist for one settled frontier item, `ln-build` may execute them in sequence instead of routing back through the user after every commit.

Loop shape:

1. take the next ready card
2. decide whether it is still a real build target or is already satisfied / stale on the current branch
3. if it is real work, run red → green → refactor
4. run the verification harness
5. reconcile canonical state and `memory/CARDS.md`
6. commit only if the card produced a real card-sized change
7. continue only if no stop condition fires

Stop the serial loop immediately when any of these becomes true:

- verification fails
- the active card needs promotion to structural work
- the containing seam no longer feels settled
- a manual outer-loop verification step is now required before proceeding
- `memory/SPEC.md` or `memory/PLAN.md` needs non-trivial revision before the next card
- the remaining queued cards are no longer obviously valid
- the user asked to pause or review between cards
- context is getting fragile enough that handoff is safer than continuing

## Red

Translate acceptance criteria into failing tests when the change benefits from them. For bugfixes or subtle seam changes, prefer one high-leverage regression test. For trivial maintenance or doc-only work, tests may be unnecessary.

Test behavior through public interfaces, not implementation details. A good test describes what capability exists and would survive internal refactoring. Avoid tests that mock internal collaborators, assert private call order, or inspect storage directly when the public interface can prove the behavior.

Do not horizontal-slice TDD. Never write a batch of imagined tests first and then a batch of implementation. Use tracer bullets: one failing behavioral test → minimum code to pass → next failing behavioral test. Each new test should respond to what the previous cycle taught you.

Run the relevant checks. Confirm failures are meaningful. If the card is already green before any code change, treat that as evidence the queue item is already satisfied or stale — not as permission to create a ceremonial red/green cycle.

## Green

Write the minimum coherent code to pass. Build inside-out: functional core first, thin I/O shell second, then end-to-end wiring.

Honor the repo's pre-release posture: if the current schema, fixture shape, dummy data, or terminology is wrong for the model, change it and regenerate dependent artifacts rather than preserving accidental compatibility. Delete obsolete paths in the same slice when they are inside the active seam.

No speculative abstractions. Only extract when two concrete cases force it. Do not anticipate later tests or build shape-only scaffolding; let the current behavioral test pull the interface into existence.

## Refactor

With tests green, improve names, boundaries, and obvious local structure. Do not widen scope.

Refactor only while green. Keep the tests pinned to the public behavior so they protect the slice while allowing internals to move. If refactoring reveals that the test is coupled to implementation, fix the test seam before trusting it.

## Verify and commit

Run the project's verification harness. All checks must pass. If the card proved already satisfied and no code or canonical-state change was needed, do not create an empty commit.

## Canonical reconciliation (mandatory)

After verification, reconcile canonical state every time. The reconciliation may end in a no-op, but skipping it is not allowed.

Traceability depth is **conditional**, not automatic.

After the build lands and verification passes, ask:

- [ ] Did this establish or change a seam / boundary?
- [ ] Did this make or reverse a non-trivial design decision?
- [ ] Did this retire or create an assumption?
- [ ] Did this establish a new seam-level invariant?

### If all answers are no

- Mark the containing frontier done in `memory/PLAN.md` **if the build completed the frontier item**, usually by updating `Sequencing` / frontier status rather than moving definition blocks
- Update `Recently Completed` if the plan uses it
- Do **not** add new SPEC/PLAN bookkeeping just because a slice happened
- If the slice was non-trivial, required manual verification, or leaves residual risk that matters beyond the current session, record it in the containing frontier definition or a terse `Recently Completed` entry only when it affects frontier-level re-entry

### If any answer is yes

Update only the touched traceability items.

#### Same-item tests

- **Same assumption** = same boundary/component + same unresolved claim
- **Same decision** = same seam/boundary + same chosen alternative
- **Same invariant** = same seam/boundary + same rule template + same proved decision(s)

#### Update rules

1. **PLAN**
   - Mark the frontier item done if this slice completed it
   - If the change closes, blocks, or unblocks a frontier item, reflect that in `Sequencing`, the affected `Frontier Definitions` entry, or `Recently Completed`
   - Do not mirror detailed slice/card history into `memory/PLAN.md`; keep active execution queues in `memory/CARDS.md`

2. **Assumptions**
   - evidence answered it → update to `validated` or `invalidated`
   - same assumption exists locally → merge/update
   - new unresolved belief that would change future work if false → add

3. **Decisions**
   - existing decision merely implemented → no-op
   - same decision, wider rationale/scope → update
   - genuinely new alternative chosen at a seam → add

4. **Invariants**
   - no new protecting oracle/test → no-op
   - same seam-level invariant gained coverage → update
   - genuinely independent seam/rule/proof → add

When uncertain between merge and add, add. When uncertain between update and no-op, update.

If uncertain whether the seam is actually settled, promote — do not silently keep the work light.

### Retire derivative artifacts

After reconciliation, garbage-collect exhausted temporary files instead of leaving breadcrumbs or tombstones:

- `HANDOFF.md` — keep only if unfinished volatile transfer state still exists; otherwise delete it
- `memory/CARDS.md` — keep only while queued scope cards still remain; otherwise delete it
- `memory/REFACTOR.md` — keep only while unfinished refactor steps still depend on it; otherwise delete it
- Do not create archive copies, numbered handoffs, or completion-pointer files

## Routing

If serial execution mode is active and no stop condition fired, continue to the next queued card instead of routing back to the user yet.

Otherwise, after verification and any necessary promotion updates, present these options to the user (use `tool-ask-question`):

| #   | Label            | Target       | Why |
| --- | ---------------- | ------------ | --- |
| 1   | Scope next item  | `ln-scope`   | More frontier work remains or no prepared queue exists |
| 2   | Review the code  | `ln-review`  | Assess quality after an implementation burst |
| 3   | Revise spec      | `ln-spec`    | The build changed durable architecture |
| 4   | Revise plan      | `ln-plan`    | The frontier or priorities changed |
| 5   | Back to triage   | `ln-consult` | Direction needs reassessment |

Recommended: **1** if more work remains and there is no active queue, **2** after multiple consecutive builds.
