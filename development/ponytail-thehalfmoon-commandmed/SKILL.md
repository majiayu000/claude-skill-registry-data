---
name: ponytail
purpose: Minimal, evidence-first implementation discipline for commandMed.
---

# Ponytail — commandMed adaptation

Use this skill whenever planning or implementing commandMed work.

## Core rule

Prefer the smallest correct mechanism that satisfies the active specification. Do not build infrastructure in anticipation of hypothetical future needs.

## Decision ladder

Before adding code, dependency, abstraction, or service, ask in order:

1. Does this need to exist for the active spec?
2. Can an existing repository mechanism satisfy it?
3. Can the standard library satisfy it?
4. Can the native platform/runtime satisfy it?
5. Can an already-approved dependency satisfy it?
6. Can a direct small implementation satisfy it?
7. Only then add a new abstraction or dependency.

## Default behavior

- Prefer explicit code over generalized frameworks.
- Prefer data files over databases when data volume/concurrency does not require a database.
- Prefer pure functions over object hierarchies.
- Prefer one bounded schema over a schema framework.
- Prefer filesystem artifacts over services when a service is not required.
- Prefer deterministic fixtures over live integrations in early specs.
- Avoid plugin systems, factories, registries, queues, caches, background workers, and distributed components until a measured requirement demands them.
- Delete unused scaffolding rather than preserving it for imagined future work.
- Keep the change surface limited to the active spec.

## Healthcare safety carve-out

Ponytail is an anti-overengineering rule, NOT a shortcut around assurance.

Never remove, defer, weaken, or bypass necessary:

- clinical safety validation;
- deterministic escalation logic;
- security checks;
- privacy boundaries;
- PHI controls;
- input validation at trust boundaries;
- source/license/provenance metadata;
- content hashing and identity binding;
- split and Gold quarantine;
- contamination checks;
- reproducibility evidence;
- calibration and abstention evaluation;
- safety-critical tests;
- audit artifacts;
- error/failure handling;
- independent review.

If a safety or evidence control looks verbose, first simplify its implementation, not its guarantee.

## Dependency rule

A new dependency must have an active-spec requirement that cannot reasonably be met with the standard library, native platform, or an already-approved dependency. Record why it is needed and what simpler alternatives were rejected.

## Research rule

Do not introduce training or inference machinery before the evaluation and provenance contracts that judge it exist.

## Completion rule

A task is complete only when its required evidence exists. More code is not evidence of greater completion.
