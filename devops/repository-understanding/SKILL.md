---
name: repository-understanding
description: "Understand repo before modifying: map language, framework, entry points, modules, contracts, configs, data, tests, CI/CD. Never redesign un-understood code."
---

# repository-understanding

Map before you modify: language, entry points, contracts, data, tests, CI — then the smallest safe change.

## Activate when

- Entering any unfamiliar codebase or module before changing it.

## Do NOT activate for

- Repos you already mapped this session (re-verify only what changed).

## Structuring pipeline (how this skill connects)

```
UNDERSTAND REPOSITORY (this skill) -> IDENTIFY LANGUAGE + FRAMEWORK (languages/*, frameworks/*)
  -> IDENTIFY EXISTING ARCHITECTURE -> PRESERVE ESTABLISHED CONVENTIONS
  -> DETERMINE MODULE BOUNDARIES (architecture/modularity, architecture/language-modularity)
  -> IMPLEMENT (core/implementation) -> REVIEW DEPENDENCY DIRECTION (architecture/modularity step 4)
  -> TEST -> REVIEW DIFF (core/code-review)
```

Never restructure an existing project merely because another architecture is theoretically cleaner. Smallest safe change; deepen, don't rewrite.

## Inspection checklist

1. README + docs + ADRs (if present) for intent and decisions.
2. Manifests/lockfiles → language, framework, versions (run `research/documentation-search` detector).
3. Entry points → routing → domain logic → data access → tests → config/env → CI/CD → deploy.
4. Conventions: naming, error handling, testing patterns, commit style (`git log` recent history).
5. Boundaries: module map, public surfaces, external services, secrets handling.

## Procedure

1. Walk the checklist top-down; write a one-paragraph mental model: what the system does, where logic lives, where change is safe.
2. Identify the established conventions you must preserve (list them explicitly).
3. Locate the change site's callers, tests, and data flow before editing.
4. Verify: you can name the entry point, the data path, the test command, and the deploy path from memory — else keep mapping.

## Failure modes

- Editing before mapping; redesigning to a "cleaner" architecture unasked; ignoring lockfiles (wrong version assumptions); missing hidden conventions (generated code, local wrappers).

## Escalation

Version facts → research/documentation-search; deep structural problems → architecture/modularity (deepen, don't rewrite).

## References

- Related: `../implementation/`, `../../architecture/modularity/`, `../../research/documentation-search/`.
