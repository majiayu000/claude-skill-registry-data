---
name: core/store-pruning
description: >-
  Use only when explicitly asked to prune unused Redux selectors, actions,
  reducers, sagas, or orphaned store logic. Requires production-usage and
  public-boundary checks before deletion.
type: sub-skill
requires:
  - core
  - core/state-integrity
  - core/actions
  - core/sagas
triggers:
  - store pruning
  - prune redux store
  - unused selector
  - unused action
  - dead saga flow
  - orphaned store logic
---
# Store Pruning Skill

Use this guide only when the user specifically asks to prune the Redux store.
Do not run store pruning automatically at the beginning or end of unrelated work.

## Agent preflight

- **MUST** confirm the request explicitly asks to prune Redux store surface area.
- **MUST** search production code separately from tests before removing anything.
- **MUST** keep items that have clear production usage or a documented
  external/public boundary that requires them.
- **MUST** include verifier-ready evidence for every pruned selector, action,
  handler, reducer case, saga flow, test, fixture, export, type, constant, or
  helper.
- **NEVER** prune during unrelated feature, bugfix, migration, or cleanup work.

## Purpose

Prune unused Redux store surface area by removing selectors, actions, handlers,
and any orphaned logic that no longer has a production path.

## Unused Selectors

A selector is unused when it has no production consumer.

Remove selectors that are referenced only by tests, because tests do not count
as production usage. Also remove selectors that are only re-exported through a
barrel or index file when there is no production consumer of that re-export.

When removing a selector, also remove selector-only tests, dead imports, dead
re-exports, and any helper logic that becomes unreachable solely because the
selector was removed.

## Unused Actions

An action is used only when it has both:

- A production trigger, such as a component dispatch, saga `put`, IPC/event
  bridge, or documented external/public entry point.
- A production handler, such as a reducer case, saga watcher, event-channel
  consumer, or documented external/public boundary.

Remove actions that lack either side. If an action is triggered but has no
production handler, remove the action and the dead trigger path. If an action is
handled but has no production trigger, remove the action and the dead handler
path. Test-only references do not keep an action alive.

## Saga-Specific Rule

If a saga handles an action that is not triggered anywhere in production code,
remove both the action and the saga logic unless a documented external/public
boundary proves the trigger exists outside the repository.

When saga pruning removes a flow, also remove orphaned request/success/failure
actions, watchers, workers, imports, tests, and any related dead code that exists
only for that flow.

## Orphaned Logic

Pruning must remove dead code made unreachable by the selector or action
removal, including:

- Saga handlers, watchers, workers, and channel bridges.
- Component dispatches and import paths.
- Reducer cases and helper functions.
- Tests and fixtures that only cover removed store surface area.
- Barrel exports, type aliases, constants, and utilities that no longer have
  production consumers.

Keep an item only when there is clear production usage or a documented
external/public boundary that requires it.

## Verification

For each pruned item, search production code separately from tests. Confirm
remaining selectors and actions have production consumers, and confirm remaining
actions have both a production trigger and a production handler.

Include in the handoff:

1. The production search terms and paths used for each removed item.
2. The separate test-only references that did not keep the item alive.
3. Any external/public boundary checked and why it does or does not preserve the
   item.
4. The relevant tests or validation commands run after pruning.

## See also

- `core/state-integrity/SKILL.md` — canonical owner and duplicate-owner rules.
- `core/actions/SKILL.md` — action creator ownership and watcher usage.
- `core/sagas/SKILL.md` — saga watcher/worker ownership and verification cues.
- `core/testing/SKILL.md` — reducer and saga test expectations.
