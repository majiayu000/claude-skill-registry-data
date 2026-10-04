---
name: research-to-build
description: Convert completed research into build-ready product and engineering work for ChefFlow without starting implementation. Use when the user provides research, a research report, market/UX findings, competitive analysis, customer evidence, or says to extract build work from research.
---

# Research To Build

## Purpose

Turn completed research into concrete, queue-ready ChefFlow product and engineering work.

Extract the maximum implementation value before asking for more research. Preserve the original research intent and evidence quality; do not flatten findings into generic feature ideas.

## Hard Stops

- Do not code unless the user explicitly authorizes implementation with ChefFlow firing language or a direct hotfix instruction.
- Do not add vague ideas to the build queue. Produce queue-ready item drafts first.
- If the user explicitly asks to queue ready items, use the repo build-queue flow after the items are specific enough.
- Follow ChefFlow auth, tenant scoping, admin guard, privacy, and dirty workspace rules when evaluating implementation implications.
- Separate verified facts from inference and speculation.

## Inputs

Use any provided research artifacts, reports, notes, screenshots, transcripts, competitor examples, customer feedback, analytics, support themes, or prior conversation context.

When research references code behavior, inspect the codebase before trusting the claim.

## First Pass

Before producing the pack, classify the research:

- **Product-shaped**: clear persona, workflow, or app surface.
- **Codebase-shaped**: explicit files, routes, data, APIs, or system behavior.
- **Conceptual**: philosophy, metaphor, domain model, brand thesis, or raw thinking.
- **Evidence-shaped**: interviews, analytics, support logs, competitive findings, or citations.
- **Mixed or duplicated**: repeated excerpts or merged threads.

If the research is conceptual, first extract reusable product primitives: nouns, verbs, loops, states, handoffs, trust rules, data objects, user promises, metaphors, and constraints. Do not force a fake implementation map until a target product surface is clear.

## Decision Gate

Choose the smallest useful deliverable:

- **Full pack** when research is product-shaped and codebase mapping is useful.
- **Concept extraction** when research is broad, philosophical, or not yet tied to a feature.
- **Queue-ready draft** when the build surface and acceptance criteria are clear.
- **Spec questions** when the idea cannot be made build-ready without decisions.
- **No-op for build** when the research is not relevant to this codebase.

## Workflow

Follow the detailed extraction checklist in [REFERENCE.md](REFERENCE.md).

1. Normalize the input: identify duplicates, merged threads, contradictions, and the research's main intent.
2. Ingest the research and separate strong evidence from weak speculation.
3. Map to the codebase only where the research implies a real app surface or system.
4. Identify gaps across product, UX, data, workflow, integration, security, reliability, tests, documentation, architecture, and research.
5. Infer grounded and speculative opportunities.
6. Convert findings into candidates with scope, acceptance criteria, risks, dependencies, likely files touched, and verification.
7. Strictly classify what is built, partially built, missing, blocked, or not worth building yet.
8. Recommend sequencing around vertical slices, dependencies, parallelization limits, and queue readiness.
9. Draft queue-ready items only when they have enough specificity.
10. Extract follow-up research tasks only after build value has been exhausted.

## Codebase Mapping

Inspect only relevant surfaces: routes, components, server actions, API routes, database tables/migrations, auth gates, route policies, tests, docs, configs, and domain modules.

For every important claim, state whether it is verified in code, inferred from nearby code, based only on research, or still unverified.

If no relevant codebase surface is identifiable, say that directly and output the product/spec decisions needed before mapping.

## Output

Return a **Research-to-Build Extraction Pack** using the output structure in [REFERENCE.md](REFERENCE.md).

Be concrete. Use codebase file references. Separate fact from inference. Do not code unless explicitly told to.

For conceptual or duplicated research, use a shorter output: distilled themes, product primitives, likely app implications, spec questions, and what would make it build-ready.
