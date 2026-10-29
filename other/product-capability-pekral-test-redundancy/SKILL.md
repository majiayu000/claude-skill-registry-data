---
name: product-capability
description: "Use when a PRD or product intent is clear but the implementation constraints are not — turns a vague capability ask into an engineering-ready plan that exposes invariants, interfaces, and unresolved decisions before any code is written."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/laravel/architecture.md` — actors, surfaces, states, and data model must fit the existing layers (Action → ModelService → Repository / ModelManager), not invent new abstractions.
- Apply `@rules/compound-engineering/general.md` — the plan is a durable artifact the next agent reuses, not throwaway prose.
- Do not invent product truth. Every unknown is an explicit open question, never a silent assumption.
- Separate user-visible promises from implementation detail. Keep them in distinct sections.
- Mark each constraint as **fixed policy**, **architectural preference**, or **open question** — never blur the three.
- Do not write code. The output is a plan, not an implementation.
- Use one language only. English here.

## Use when
- A PRD exists but the implementation constraints stay implicit.
- The capability spans multiple surfaces or services and needs one contract.
- The product vision is clear yet its architectural implications are not.
- Engineering reviews keep surfacing the same hidden assumptions.

The gap is not "what should we build?" but "what exactly must be true before implementation starts?".

## Execution

Walk these four steps in order. Each feeds the next.

1. **Restate the capability precisely.** Compress the ask into one statement covering the **user** (who gains the ability), the **new ability** (what they can now do), and the **outcome change** (what is true after that was not before). If you cannot fill all three, that is the first open question.

2. **Extract the constraints.** Surface what must hold regardless of design:
   - business rules the capability must obey,
   - scope boundaries (in scope vs explicitly out),
   - invariants that must never break,
   - trust boundaries and data ownership (who owns and may read/write the data; account scoping per `@rules/laravel/architecture.md`),
   - lifecycle and state transitions,
   - rollout / migration requirements.
   Tag every item as fixed policy, architectural preference, or open question.

3. **Define the implementation contract.** Make the capability concrete enough to hand off:
   - **actors** — users, roles, systems that act,
   - **surfaces** — entry points (HTTP, Livewire, command, job, listener),
   - **states** — the state machine and allowed transitions,
   - **interfaces** — Action inputs/outputs and the boundary contract,
   - **data model** — entities, ownership, and account scoping implications.
   Keep the contract aligned with the existing architecture; flag any place where it would force a new layer.

4. **Translate into execution readiness + handoff.** Decide the readiness level and route the work:
   - **Ready to implement** → hand to `@skills/create-issues-from-text/SKILL.md` to break it into tracker issues.
   - **Needs architecture review** → route the data-model / layering questions through `@rules/laravel/architecture.md` before planning.
   - **Needs product clarification** → list the open questions that block a contract; stop until they are answered.

## Output

Write the plan to a durable file (`PRODUCT.md` at the repo root, or a `docs/` capability doc) so the next agent picks it up — per `@rules/compound-engineering/general.md`. State the file path in your reply. Use exactly these sections:

1. **Capability restatement** — user, new ability, outcome change (one paragraph).
2. **User-visible promises** — what the user is guaranteed to experience. No implementation here.
3. **Constraints** — the step-2 list, each tagged fixed policy / architectural preference / open question.
4. **Implementation contract** — actors, surfaces, states, interfaces, data model (step 3).
5. **Non-goals** — what this capability explicitly does not cover.
6. **Open questions** — every unresolved decision that blocks or shapes implementation, with who must answer it.
7. **Handoff** — the readiness level and the named next step (`create-issues-from-text` or architecture review).

Fill every section. If a section has nothing, write an explicit note (e.g. `No non-goals identified.`) rather than leaving it blank.

## Done when
- The capability is restated with all three of user, ability, and outcome change.
- Every constraint is tagged fixed policy, architectural preference, or open question.
- User-visible promises are separated from implementation detail.
- The implementation contract fits the existing architecture, or each deviation is flagged.
- All open questions are listed, none disguised as assumptions.
- The plan is written to a durable file and the handoff names a real next step.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
