---
name: design-child-contract
description: Compare 2-3 materially different child-level contract/interface shapes and write the chosen direction into `CONTRACT_DECISION.md` before planning when local contract shape is ambiguous.
---

# design-child-contract

Use only when the child owns an ambiguous API/config/storage/hook/module contract.

## Read first
- `../references/task-packet-contract.md`
- `../references/final-state-authoring-policy.md`
- child `INDEX.md`, `BRIEF.md`, `PLAN.md`, `AMENDMENTS.md`, `ARTIFACT_CANDIDATES.md`
- relevant parent initiative files referenced by the child brief
- `../../references/communication-mode.md`

## Workflow
1. Generate 2-3 materially different contract shapes.
2. Compare them on simplicity, coupling, flexibility, validation fit, and misuse risk.
3. Choose one direction explicitly.
4. Write `CONTRACT_DECISION.md` with the chosen direction, rejected alternatives, and rationale.
5. Update child `INDEX.md` to `Packet phase: contract_decided`.

## Writing rule
Write the chosen contract as the current local design decision.
Do not preserve competing contract vocabularies inside the canonical child packet after the decision is made.

## Do not
- write implementation code
- leave the contract decision implicit in chat only
- create contract churn when the packet already has a clear contract surface

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
