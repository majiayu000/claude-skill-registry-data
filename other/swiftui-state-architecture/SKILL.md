---
name: swiftui-state-architecture
description: "Fix SwiftUI state ownership, Observation, bindings, environment injection, view identity, scene scope, and testable feature boundaries without imposing an architecture."
---

# State, identity, and architecture

## Inputs

Identify deployment minimums, existing observation system, view identity, creation site, mutation sites, and required lifetime: render, view, scene, app, or persistent store.

## Rules

- **STATE-001 — Choose lifetime first.** Give mutable state one owner at the narrowest sufficient lifetime; pass values, bindings, or explicit services to readers.
- **STATE-002 — Match the observation system.** Use `@State` for owned Observation models on supported targets; retain `@StateObject`/`@ObservedObject` for compatible legacy models. Migrate incrementally.
- **STATE-003 — Preserve identity.** Use stable domain IDs for mutable collections. View position, a newly generated UUID, and object identity are not interchangeable with record identity.
- **STATE-004 — Keep rendering pure.** Do not start services, write persistence, or perform expensive work from `body` or repeatedly evaluated initializers.
- **STATE-005 — Separate draft from durable state.** Cancel must not persist edits that the UI promises to discard. Observation and actor isolation solve different problems.

## Workflow

1. Draw owner → readers → writers for the changed feature.
2. Select wrappers from the playbook; avoid mirrored booleans and unnecessary view models.
3. Model mutually exclusive states as an enum when independent flags admit impossible combinations.
4. Extract services or reducers only where side effects, reuse, or deterministic tests justify them.
5. Check lifetime across navigation, sheets, list changes, multiple windows, and relaunch.

## Verify

Test parent recomputation, record reorder/deletion, two scenes, cancel/save, restoration, and model replacement. Verify mutations update only the intended UI and do not recreate resource owners.

## Output

Provide the ownership map, chosen wrappers, compatibility boundary, and focused behavior tests.

## References

Read the [playbook](references/state-patterns.md) for decisions, failure cases, and source links.

For observation, bindings, and dependency seams, read the [focused reference](references/observation-and-bindings.md).
