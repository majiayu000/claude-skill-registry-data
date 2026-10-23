---
name: critical-journey-document
description: Create one concise evidence-linked product journey record for one actor pursuing one goal. Use when product behavior needs traceable ownership, acceptance, telemetry, or service-flow documentation for a current decision or delivery gate; not for implemented-system context under docs/context/, which belongs to repo-context-document.
---

# Critical Journey Documentation

Create one canonical record of how one actor reaches one goal, and show which steps the product implements today.

## Workflow

1. Establish what makes the journey critical, and its actor, goal, trigger, scope, owner, and risk. Find the repository's established location for product documentation. If there is none, ask the user where the record goes; do not create a new documentation tree.
2. Read the existing requirements, code, contracts, tests, telemetry, and documentation. Reuse the repository's identifiers and terms.
3. Write separate records for several actors or goals only when each record is useful alone.
4. Document the ordered steps, decisions, state changes, success, meaningful failures, recovery, and ownership. Mark each step as implemented, with a link to the code or test that shows it; specified only, with a link to the requirement; or unknown.
5. Record each unresolved fact as an unknown, with its decision owner and the condition that resolves it. Do not fill it with a guess.
6. Add acceptance, telemetry, service blueprint, or story-map sections only when a named consumer or delivery gate needs them. Acceptance sections describe product acceptance; `test-design` owns executable tests. Telemetry sections record agreed events; do not invent events.
7. Use `text-improve` on the finished record without changing agreed contracts, identifiers, or domain terms.

Use `repo-context-document` for implemented-system flows under `docs/context/`, `rollout-readiness-review` for deployment readiness, and `spec-update` for semantic decisions. Do not create a parallel canonical document, a mandatory identifier scheme, or a suite of artifacts by default.

## Result

Finish when every step has a status and an evidence link or an owner for its unknown, and the record has only sections with current consumers. Report the record's path and the gaps between specified and implemented steps.
