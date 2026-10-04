---
name: documentation
description: "Updates technical docs for verified behavior, public contracts, commands, configuration, and operations."
---

# Skill: documentation

## Purpose

Keep technical documentation accurate, minimal, and tied to implemented behavior.

## Rules

Update documentation when changes affect:

- public API;
- configuration;
- deployment;
- commands;
- behavior;
- integration contracts;
- hardware wiring/safety expectations;
- migration or operational procedures.

Do not document behavior that is not implemented.

Do not write marketing prose inside technical docs.

## Good Documentation

Good documentation is:

- precise;
- minimal;
- verifiable;
- consistent with code;
- easy to update;
- explicit about assumptions and constraints.

## Document These When Relevant

- how to run tests;
- how to run the service/tool;
- configuration keys;
- environment variables without secret values;
- safety caveats;
- migration steps;
- rollback notes;
- operational failure modes;
- known limitations.

## Avoid

- stale examples;
- fake placeholders;
- undocumented behavior changes;
- copy-pasted README inflation;
- screenshots as the only source of truth;
- secret values in examples.
## Extended References


For deeper work, read:

- `../../engineering/19_documentation_style.md`
- `../../engineering/24_task_todo_style.md`
