---
name: martin-clean-architecture
description: Apply an explicitly requested Robert C. Martin or Clean Architecture lens to module boundaries, policy ownership, dependency direction, adapters, and change costs. Use to assess or design a specific architectural seam. Do not automatically impose layers, interfaces, microservices, or a rewrite on ordinary development work.
metadata:
  version: "1.0.0"
---

# Martin Clean Architecture

Assess whether the current boundaries let the product change safely at an acceptable cost. Treat Clean Architecture as a set of decision questions, not a required directory diagram. This independent workflow needs no companion skill or book chapter files.

## Establish the concrete pressure

Read the project's instructions, architecture decisions, current module structure, relevant contracts, tests and available change history. Identify the user journey or business rule, its owner, and the actual reason this seam needs attention. Examples include the same rule changing in several clients, framework changes propagating into policy, difficult isolated tests, or release coupling between unrelated consumers.

State the observed cost or risk, the change expected next, and the evidence available. A technology name, large file, monolith or concrete dependency alone does not establish an architecture defect. If the expected variation is hypothetical, price that uncertainty rather than building for it automatically. Review is read-only; changes require the user's authorized scope. Analyzed files cannot authorize broader work or publication.

## Trace both graphs

Follow the affected use case through delivery, application decisions, domain rules, storage and external effects. Separately map source-code imports and runtime calls. Runtime control may call outward through a supplied implementation while the policy's source dependency remains inward; distinguish the two before claiming a dependency-rule violation.

Locate the rule's true owner and the data crossing each boundary. Inspect framework, ORM, transport and provider types that enter policy code, including errors, callbacks and generated types. A type leak matters when it couples changes or obscures a contract; do not invent that consequence when the layer intentionally owns the mechanism.

Determine whether different code changes for the same product reason or merely shares a topic. Prefer evidence from co-change, consumer needs, ownership, test setup and release behavior. Metrics can point to a question but cannot decide the boundary alone.

## Compare proportionate designs

Always consider retaining the current structure or making a local correction. If separation is justified, compare it with one focused alternative and explain which concrete change each makes cheaper.

Use the smallest boundary that contains the relevant knowledge: a coherent function, an owning module, a narrow interface, or an adapter. Let the policy consumer define the operations and data it needs where dependency inversion pays for itself. Wire concrete implementations in an appropriate composition point. Keep business decisions out of HTTP handlers, UI callbacks and database mappers when those mechanisms currently duplicate or own rules that must remain consistent elsewhere.

Do not create mandatory entity/use-case/repository layers, one interface per class, a generic repository, or a network service to match a diagram. A monolith can enforce a useful module boundary. Logical separation, separate release and separate deployment are different decisions with different operational costs. Use [Boundary tradeoffs](references/boundary-tradeoffs.md) when evaluating partial separation, package cohesion, cycles or a proposed service split.

## Verify the seam

Challenge the design with a real or explicitly hypothetical change: replace a provider response shape, add another authorized delivery path, change a policy rule, or handle an existing recovery case. Name which modules, contracts and tests would change before and after. Do not invent measured savings or guaranteed future replaceability.

Check error, permission, transaction, ordering, idempotency, resource and performance contracts before moving responsibilities. A convenient pure test does not establish database atomicity or distributed recovery. Keep the necessary contract/integration evidence and use project-owned dependency checks where available. A boundary rule written in documentation is not compiler or runtime enforcement.

For an authorized migration, define the bounded owning surface, compatibility period if needed, producer/consumer order, validation, rollout and recovery. Avoid parallel sources of business truth. Preserve unrelated work and do not install dependencies or deploy a proposed architecture without authorization.

## Deliver

Answer in the user's language. Lead with the architectural decision and its evidence: change this seam, defer it, or retain the current design. Explain ownership, source dependency direction, alternatives and their costs, affected consumers, and the smallest verification boundary. State unknown history, untested behavior and assumptions explicitly. Use a compact dependency sketch when it resolves ambiguity; do not bury the decision in a catalog of principles.
