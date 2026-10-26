---
name: discovery
description: Use when a product request has unclear users, outcomes, constraints, or scope.
---

# Discovery

Shape the smallest worthwhile increment before specifications or code. ai-dlc
supplies guidance; the harness applies judgment using the project's chosen tools.
Read repository product context, architecture and relevant provider instructions.

## Entry path

- Greenfield: identify audience, task/problem, available evidence and the smallest
  useful outcome. A requested feature or layout is a candidate solution, not
  validated value. Missing evidence can make the next outcome a learning goal.
- Brownfield: inspect implementation, tests, public contracts and consumers.
  Record current behavior and sources, affected users/integrations, compatibility,
  migration and recovery. Explicit conflicting requirements remain unresolved
  until their owner decides; an opt-in alternative is a proposal, not approval.

## Brief contract

Use `docs/templates/product-brief.md` when present. Worked examples:
`docs/examples/product-shaping/greenfield.md` and
`docs/examples/product-shaping/brownfield.md`. In the ai-dlc source repository,
these assets live under `agents/templates/` and `agents/examples/`. In older
projects without them, use these sections directly; do not require adoption.

Begin each brief with **Canonical brief:** its path or unique chat label,
**Owner:** the known decision owner or unknown, and **Status:** draft/reviewed
with its source. IDs are scoped to that named brief. Use these exact sections:

1. **Audience and problem** — separate the underlying task from the requested feature.
2. **Evidence and assumptions** — label observed evidence with sources/limits,
   actual user decisions with their scope/source, and unverified hypotheses.
3. **Current behavior (brownfield)** — inspected contracts and consumers, explicit
   **Compatibility** and **Migration/recovery** fields. Mark unknowns or explain
   not applicable; for greenfield record external constraints.
4. **Options and trade-offs** — compare at least two feasible approaches and
   doing nothing when meaningful. Explain impact, evidence confidence, effort
   and dependencies qualitatively; include investigation when value is unknown.
5. **Selected outcome** — bounded OUT-001 and selection reason.
6. **Scope and exclusions** — boundaries and what must remain compatible.
7. **Success evidence** — RQ-001-style criteria mapped to outcome IDs, each with
   evidence or a planned check. Keep missing facts explicitly unresolved.
8. **Next slice** — smallest action, evidence goal, dependencies and exit condition.
9. **Unresolved decisions** — unknowns, contradictions, owner and resolution method.

Reuse existing IDs and name their canonical owner; downstream PRDs/specifications
reference them rather than renumbering or duplicating authority. Separate proposed
criteria from confirmed facts: do not turn an unspecified format, interview,
user preference, business baseline or live result into an approved requirement.

End with `Decision: proceed|investigate|stop — <reason>`:

- **Proceed** when evidence supports a bounded outcome and material constraints
  are resolved within existing authorization. Next use needs-spec and the
  configured formal specification provider where required before implementation.
- **Investigate** when evidence is insufficient or requirements contradict;
  name a bounded evidence goal instead of committing to implementation.
- **Stop** for declined, duplicate, out-of-scope or infeasible work; record why.

A recommendation is not approval. Reuse existing authorization without inventing
it. Small work may keep the brief alone; expand with prd-draft only when useful.
UI/UX exploration is optional for interaction changes; non-UI work uses suitable
contract, architecture or operational evidence. Discovery does not authorize
tracker publication or external messages.

Resolve provider-specific commands from the configured role provider’s instructions.
The agent supplies judgment; services store, validate, and link artifacts.
