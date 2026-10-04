---
name: design-award-pipeline
description: "Route and coordinate an end-to-end design-award workflow across winner research, evidence-based evaluation, award matching, entry-text preparation, and final submission checking. Use when a user asks for a complete award plan, does not know which Design Judge skill to use, wants multiple stages coordinated, or needs a resumable workflow with explicit handoffs. Do not replace the specialist skills, invent project facts, treat scores as winning probabilities, or bypass current official-rule verification."
---

# Design Award Pipeline

Coordinate the specialist Design Judge skills without duplicating their rules.

## Route the request

Choose the smallest sufficient route:

| User goal | Route |
|---|---|
| Find comparable winners | `design-award-search` |
| Diagnose or score the design | `design-evaluation` |
| Select an award, route, or category | `design-award-match` |
| Prepare entry fields and copy | `design-information-prep` |
| Audit a concrete submission package | `design-submission-check` |
| Complete journey | evaluation or match → information prep → submission check; add search only when precedents are needed |

If the user has not provided enough information to select a route, ask at most one short question. Otherwise proceed with explicit assumptions.

## Maintain the handoff

Create or update a compact handoff record using [references/handoff-schema.json](references/handoff-schema.json). Keep these concepts separate:

- user-supplied facts;
- evidence-backed findings;
- model inferences;
- missing facts and live-rule checks;
- decisions already approved by the user;
- the next recommended specialist skill.

Do not copy long specialist outputs into the handoff. Store identifiers, decisions, blockers, source links, and artifact paths.

When a handoff is written to JSON, run `python scripts/validate_handoff.py <handoff.json>` before treating it as resumable. Use [examples/handoff.example.json](examples/handoff.example.json) as a minimal valid shape, not as project evidence.

## Coordinate stages

1. State the selected route and why it is sufficient.
2. Invoke or follow the relevant specialist Skill exactly.
3. Preserve its uncertainty labels, evidence confidence, and blockers.
4. Stop for user approval when the target award, maturity track, or another consequential choice changes downstream work.
5. Hand off only facts supported by user material or cited official sources.
6. End with the completed stage, unresolved blockers, and the next optional stage.

## Boundaries

- Never merge fit score, design score, and evidence confidence into one number.
- Never claim or estimate a probability of winning.
- Never treat observed winners as official jury weights.
- Never mark a package ready when time-sensitive official rules remain unverified.
- Never invoke all specialist skills when one is enough.
