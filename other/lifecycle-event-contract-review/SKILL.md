---
name: lifecycle-event-contract-review
description: Reviews a JavaScript or TypeScript plugin's lifecycle event contract against its implementation. Use when the user asks to audit custom events, EVENTS constants, emit helpers, typed event details, bubbling behavior, event ordering, addons, cleanup, tests, README, docs metadata, demos, adapters, presets, renderers, or integration examples.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: code-review
  task_type: review
  audience: javascript-and-typescript-plugin-maintainers
  tags:
    - javascript
    - typescript
    - plugins
    - events
    - custom-events
    - lifecycle
    - tests
    - documentation
  status: draft
  side_effects: none
---

# Lifecycle Event Contract Review

## Purpose

Review a JavaScript or TypeScript plugin repository for lifecycle event contract consistency. The workflow verifies that source code, event constants, emit helpers, typed event details, bubbling behavior, event ordering, addons, cleanup behavior, tests, README content, docs metadata, demos, and related extensions all describe and use the same event contract.

Confirm behavior from implementation source rather than assuming documentation is correct.

## When to use this skill

Use this skill when:

- The user asks to review plugin lifecycle events or a repository event contract.
- A plugin exposes custom events through an `EVENTS` constant, enum, map, public helper, or typed event API.
- The task involves checking event names, payload details, bubbling, cancelability, composed behavior, ordering, cleanup, or integration compatibility.
- The repository includes addons, presets, adapters, renderers, wrappers, demos, or integration examples that may consume lifecycle events.
- The user wants an implementation-ready plan before changing event names, adding events, removing events, or updating docs.

Do not use this skill when:

- The user only wants a general README rewrite without source-contract verification.
- The event behavior is unrelated to JavaScript, TypeScript, DOM events, custom events, plugin hooks, lifecycle callbacks, or integrations.
- The user asks to implement event changes immediately; use this review first, then create a separate implementation task.
- The repository cannot be inspected and the user has not provided enough implementation, test, or documentation excerpts to verify behavior.

## Inputs to inspect

Start with implementation source, not documentation:

- Package manifests and exports, such as `package.json`, workspace manifests, build entry points, and type declaration entry points.
- Core implementation files, such as `src/`, `lib/`, `packages/*/src/`, semantic component roots, initialization, render, update, destroy, cleanup, or teardown code.
- Event contract source, such as `EVENTS` constants, enums, maps, named exports, event-name factories, emit helpers, `CustomEvent`, `EventTarget`, `dispatchEvent`, callbacks, hooks, or pub/sub wrappers.
- Type sources, such as TypeScript detail types, event maps, overloads, generics, declaration files, and JSDoc.
- Related extensions, including addons, presets, adapters, renderers, wrappers, and integration examples.
- Tests, including unit, integration, DOM/event, type, snapshot, fixture, addon, adapter, and demo tests.
- Documentation, including `README.md`, `docs/`, demo pages, docs metadata, changelogs, migration notes, and examples that mention events or lifecycle behavior.

## Workflow

1. Define the review scope:
   - Identify the current plugin or package under review.
   - Detect the event prefix from implementation source, such as an `EVENTS` object, event-name factory, string literals passed to emit helpers, or exported event map.
   - Detect the primary event target from the semantic component root, not from README claims. Prefer the DOM node, plugin instance, controller, host element, or root object that represents the component boundary.
2. Build an event inventory from source:
   - List every event emitted by source code.
   - Record each event's name, prefix, emitter location, helper used, event target, timing, ordering relationship, `detail` shape, bubbling behavior, cancelability, composed behavior, and cleanup or teardown relevance.
   - Separately list constants or exported names that are not actually emitted.
   - Separately list emitted string literals that are not present in the canonical constants or event map.
3. Identify the canonical event contract:
   - Determine whether the repository uses `EVENTS`, TypeScript event maps, helper overloads, docs, generated metadata, tests, or another artifact as the intended contract.
   - Treat implementation and tests as stronger evidence than README prose.
   - Flag any mismatch between constants, emitted names, types, tests, README, generated docs, and demos.
4. Review the emit helper:
   - Check whether all lifecycle events go through a common helper or whether some bypass it.
   - Verify that the helper applies the detected prefix consistently.
   - Verify that `detail` values are stable, typed, and intentionally shaped.
   - Check whether helper defaults for `bubbles`, `cancelable`, and `composed` are appropriate and documented.
   - Identify whether overly broad helper behavior causes events to bubble or cross shadow boundaries unexpectedly.
5. Review typed event details:
   - Compare emitted `detail` objects against TypeScript definitions, exported event maps, JSDoc, declaration files, tests, and docs.
   - Flag missing, stale, optional-but-always-present, required-but-omitted, overly broad, or undocumented detail properties.
   - Check whether detail objects expose internal mutable state, DOM nodes, addon internals, or inconsistent naming.
6. Review lifecycle ordering:
   - Derive actual event order from control flow, async boundaries, initialization, render and update paths, error paths, teardown, and addon loading.
   - Confirm whether events fire before or after state mutation, DOM mutation, rendering, addon callbacks, metadata updates, and cleanup.
   - Identify misleading event names, such as `ready` events that fire before addons are ready, `change` events that fire before state is committed, or `destroy` events that fire after the target has been removed.
7. Review bubbling and event-target behavior:
   - Confirm whether events are dispatched on the semantic component root, plugin instance, document, window, child elements, or transient nodes.
   - Identify events that are too broad, duplicate native events, bubble unintentionally, fail to bubble when consumers need delegation, or cross boundaries unexpectedly.
   - Check whether demos and examples listen on the same target that implementation actually dispatches from.
8. Inspect related extensions before recommending changes:
   - Search addons, presets, adapters, renderers, wrappers, and integration examples for event consumption.
   - Record which events each extension listens to, emits, proxies, transforms, or documents.
   - Check whether changing, merging, renaming, removing, or narrowing an event would break an extension.
   - Prefer compatibility-preserving recommendations when existing extensions rely on current behavior.
9. Classify event problems:
   - Misleading event: name, timing, target, or docs imply behavior that source does not provide.
   - Duplicated event: two events fire for the same lifecycle moment without a documented distinction.
   - Missing event: source has a meaningful lifecycle transition that consumers need but no event or hook exposes it.
   - Overly broad event: event fires for unrelated causes, uses a generic name, exposes broad mutable detail, or bubbles beyond its intended audience.
   - Stale contract artifact: constants, types, README, docs metadata, tests, or demos mention events that implementation does not support.
   - Hidden contract: implementation emits events that are not exported, typed, tested, or documented.
   - Addon breakage risk: proposed event change would affect an addon, preset, adapter, renderer, or integration example.
10. Decide reuse versus new event:
    - Recommend reusing an existing event when the new behavior represents the same lifecycle moment, target, ordering, detail shape, and consumer intent.
    - Recommend introducing a new event only when there is a distinct lifecycle moment, distinct audience, distinct timing, distinct target, or incompatible detail shape.
    - If adding a new event, specify its exact name, prefix, target, timing, `detail` type, bubbling, cancelability, composed settings, docs updates, tests, and migration notes.
    - If changing an existing event, specify compatibility risks and whether a deprecation bridge is required.
11. Review tests:
    - Verify tests assert emitted event names, order, target, detail shape, bubbling, cancelability, composed behavior, and cleanup behavior.
    - Check addon and integration tests for event consumers.
    - Identify missing tests needed before implementing event changes.
    - Prefer behavior tests over snapshot-only or README-only evidence.
12. Review documentation and demos after source:
    - Compare README, docs metadata, demos, and examples against the source-derived event inventory.
    - Flag claims that are missing, duplicated, stale, misleading, or broader than implementation.
    - Identify exactly which docs or demos must change for each contract fix.
13. Produce an implementation-ready plan only:
    - Do not edit files during the review.
    - Group recommended changes by event contract area.
    - Include exact source files to edit, tests to add or update, documentation to update, and compatibility checks to run.
    - Include a migration or deprecation note when event changes affect public consumers.
    - Separate blockers from improvements.

## Output format

Return the result using this structure:

```md
## Summary

Briefly state the detected event prefix, primary event target, overall contract health, and highest-risk mismatch.

## Detected contract

- Event prefix:
- Primary event target:
- Canonical event contract source:
- Related extensions inspected:

## Event inventory

| Event | Source emitter | Target | Detail type/source | Bubbles | Cancelable | Composed | Ordering | Consumers | Status |
|---|---|---|---|---:|---:|---:|---|---|---|

## Findings

| Priority | Area | Finding | Evidence | Breakage risk | Recommendation |
|---|---|---|---|---|---|

## Reuse vs new event decisions

| Proposed behavior | Reuse existing event? | Reason | Required contract change |
|---|---:|---|---|

## Implementation plan

### Phase 1: Contract source of truth

- Files to edit:
- Changes:
- Tests:

### Phase 2: Emit behavior and types

- Files to edit:
- Changes:
- Tests:

### Phase 3: Addons and integrations

- Files to edit:
- Changes:
- Tests:

### Phase 4: Documentation and demos

- Files to edit:
- Changes:
- Tests:

## Validation checklist

- [ ] Event prefix is detected from implementation source.
- [ ] Primary event target is detected from the semantic component root.
- [ ] Every emitted event is represented in constants or documented intentionally as private.
- [ ] Every public constant is emitted or removed/deprecated.
- [ ] Typed `detail` shapes match emitted objects.
- [ ] Event ordering is covered by tests where consumers depend on it.
- [ ] Bubbling, cancelability, and composed behavior are asserted or intentionally documented.
- [ ] Addons, presets, adapters, renderers, and integration examples are checked before event changes.
- [ ] README, docs metadata, and demos match source-confirmed behavior.
- [ ] Cleanup and teardown paths do not emit misleading events from removed or stale targets.
```

## Quality bar

The task is complete only when:

- The review confirms event behavior from source before relying on documentation.
- The event prefix and primary event target are detected and reported.
- Each finding cites a specific file, symbol, test, doc claim, or missing artifact.
- Misleading, duplicated, missing, overly broad, hidden, or stale events are classified separately.
- Addons, presets, adapters, renderers, wrappers, and integration examples are inspected before recommending event changes.
- Recommendations state whether to reuse an existing event or introduce a new one.
- The implementation plan names exact files or file groups to change and exact tests to add or update.
- Compatibility, migration, and deprecation risks are called out before public event changes.
- The output is review-only and does not modify files unless the user separately asks for implementation.

## Edge cases

- If no `EVENTS` constant exists, infer the contract from emitted strings, helper calls, tests, and docs, then recommend whether a canonical constant or typed event map is needed.
- If multiple packages emit similar events, scope the inventory by package first, then identify cross-package naming or payload inconsistencies.
- If generated docs or metadata disagree with source, identify the generator or source metadata before recommending manual edits.
- If an event is intentionally private, recommend naming, export, or docs changes that make the boundary explicit.
- If a cleanup path removes the target before emission, check whether consumers can still observe the event or whether teardown should emit earlier.
- If changing event bubbling would affect delegated listeners, recommend tests and a migration note before changing defaults.
- If a new feature request appears to need an event, first test whether an existing event already represents the same lifecycle moment and consumer intent.

## Related skills

- missing-docs-spotter
- readme-change-sync
- repository-area-impact-planner
- edge-case-test-planner
