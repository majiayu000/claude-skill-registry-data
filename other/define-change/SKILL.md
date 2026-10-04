---
name: define-change
description: Define scope, observable acceptance, contracts and a verification plan before building. Use when a request introduces or changes behavior whose scope, acceptance or contracts are not yet agreed, or when the user asks to plan, scope or specify a change. Skip it when an existing definition already covers an implementation request.
---

# define-change

Read the request, prior decisions and `docs/content/docs/equipo/perfil-del-proyecto.md` from the
Git root. Inspect the affected implementation, callers and tests. Read PRODUCT.md
and DESIGN.md only for UI work.

## Steps

1. Establish the Definition of Ready: problem and consumer, scope/exclusions,
   observable acceptance IDs, affected contracts/capabilities, risks and the first
   vertical task with its owner and test/services plan. Files alone do not
   establish readiness.
2. Reuse existing decisions and authorization. For an unresolved idea, explore
   concrete scenarios and compare two or three approaches only when a real
   decision remains; explain the recommended interfaces, data flow and failure
   modes. Ask only for critical missing information and continue independent
   work meanwhile. Use the project's visual guidance when UI decisions remain.
3. Classify the work:
   - Functional backend, frontend or fullstack work uses one OpenSpec change.
     Use [openspec-propose](../openspec-propose/SKILL.md) for artifacts or
     [openspec-explore](../openspec-explore/SKILL.md) for uncertainty. Resolve
     paths with the repository CLI.
   - Mechanical/docs work records purpose, acceptance and proportional evidence
     in the existing task/PR/conversation, without an artificial spec or test.
     Reclassify if behavior, permissions, contracts or data start changing.
4. For an OpenSpec change, run `just change-status <id>` and `just spec-check <id>`.
5. If implementation is authorized and ready, continue with backend-change,
   frontend-change or schema-change (stored data); record a module boundary,
   contract, persistence, security or core-flow decision as an ADR first; otherwise deliver the requested definition. Use
   [the evidence contract](../validate-change/references/evidence.md) throughout
   the loop.

## Output

- Readiness verdict and remaining assumptions.
- Artifact paths (OpenSpec change or the existing task/PR record).
- A criterion → task → planned evidence mapping.

## Gotchas

- Structural validity from `spec-check` does not prove that acceptance is
  observable or that the requirement is correct.
- Do not create another PRD/spec or assume a planning home; OpenSpec is the one
  planning artifact for functional work.
- A precise implementation request with a prior definition needs no new
  interview or approval.
- OpenSpec skills and generated opsx commands are upstream-managed. Coordinate
  through project workflows and locked CLI wrappers; never patch vendor skill
  content to implement project policy.
