---
name: architecture-planning
description: Author <feature>.overview-plan.md — the canonical Step A/B/… list and architecture approach, fitted to existing codebase patterns. Used by the architect agent at /feature:structure stage-2-overview.
---

# Architecture planning skill

## Mission
Author the overview plan: the architecture approach plus the **canonical** implementation-step list that every downstream artifact (analyzed, plan, test) references.

## Owned artifact
`docs/<feature>/<feature>.overview-plan.md`. Template: `~/.claude/templates/feature.overview-plan.md`.

## Read scope
- `docs/<feature>/<feature>.requirement.md` (BA's approved output).
- The overview-plan template.
- `docs/architecture.md` if present.
- Project `architecture-rules` + soft `docs/narrative/` / `docs/domain/` via `project-seams` (skip rule skills for pure docs/config/process features).

## Procedure
1. Read the requirement, the template, `docs/architecture.md` if present, and the project's `architecture-rules` skill if the feature touches code.
2. Write `docs/<feature>/<feature>.overview-plan.md` mirroring the template. Populate every section for this feature.
3. The Next Steps list (`Step A`, `Step B`, …) MUST be the **canonical** step list that downstream Architect-analyzed, Software Engineer, and Tester all reference. **Do not rename or renumber these steps after this point.**
4. Save via `Write`. Hand off per `pipeline-protocol`: "Stage 2-overview complete. Awaiting user APPROVE on `<feature>.overview-plan.md`."

## Design discipline (fit, don't invent)
- Study existing organization, naming, and patterns first; design the feature to fit naturally into them.
- Choose the simplest architecture that meets the requirement. Avoid speculative abstractions unless the repo already uses them.
- Order steps by dependency (types/interfaces → core logic → integration → UI → tests → docs) so each step is independently verifiable.
- Cite `architecture-rules` sections in the Architecture row where they constrain a choice.

## Boundary
Does not author `analyzed.md` (that is `risk-severity-analysis`), `plan.md`, flip `[X]`, or write `status.md`. Full contract: `pipeline-protocol`.
