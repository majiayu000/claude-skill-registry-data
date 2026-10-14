---
name: java-api-design
description: "Trigger: Java API design, public API, encapsulation, modules, visibility, contracts, binary compatibility. Design Java APIs with clear boundaries."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.0.4"
---

# Skill: java-api-design

## Activation Contract

Use this skill when designing or reviewing Java APIs, public classes, interfaces, modules, package boundaries, visibility, method contracts, and compatibility risks.

Do **not** use this skill for private implementation cleanup, general Clean Code review, REST API product design, or non-Java API design.

## Responsibility

This skill teaches Java API boundary design. It does not call other skills, generate full libraries, or decide product behavior.

## Required Context

- API consumers and expected usage.
- Public vs internal surface.
- Java version and module usage when known.
- Compatibility expectations.
- Error and validation contract expectations.

## Context Budget

- Keep this `SKILL.md` focused on API decisions.
- Use `references/java-api-boundaries.md` for detailed boundary guidance.

## Hard Rules

- Minimize public surface; public means support burden.
- Make invalid states hard to represent where practical.
- Document preconditions, postconditions, exceptions, and thread-safety when relevant.
- Prefer package-private/internal implementation until a stable consumer need exists.
- Avoid leaking mutable internals.
- Avoid breaking compatibility unless the user explicitly accepts it.

## Decision Gates

| Condition | Action |
|---|---|
| Member need not be public | Reduce visibility. |
| API exposes mutable collection/object | Return defensive copy, immutable view, or documented ownership transfer. |
| Constructor has many parameters | Consider named factory, parameter object, or builder based on complexity. |
| Module boundary exists | Export only published API packages; keep implementation unexported. |
| Reflection access is requested | Prefer narrow `opens`/qualified access and document the reason. |

## Execution Steps

1. Identify consumers and stability expectations.
2. Separate API surface from implementation.
3. Review visibility, mutability, construction, errors, and documentation.
4. Check Java module/package implications.
5. Recommend API shape and compatibility notes.

## Output Contract

Return:

- API boundary verdict.
- Public surface changes recommended.
- Contract documentation needed.
- Compatibility risks.
- Minimal API design proposal.

## References

- `references/java-api-boundaries.md` — Visibility, modules, mutability, and compatibility guidance.

## Assets

- None.
