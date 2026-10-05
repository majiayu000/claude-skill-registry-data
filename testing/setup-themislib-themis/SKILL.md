---
name: react/migration/setup
description: >-
  Check readiness before migrating existing React state owners to ReactStore:
  installation, family choice, and app lifecycle owner. Defer bootstrap to
  setup/component-integration.
type: sub-skill
requires:
  - react
  - react/component-integration
  - react/migration
triggers:
  - ReactStore migration setup
  - prepare React state migration
  - React migration readiness
---
# React migration setup

Use this checkpoint only when adopting `ReactStore` into an existing app. For a
new app or an unresolved family choice, start with
[Store-family decision gate](../../../setup/SKILL.md#store-family-decision-gate)
and [Installation workflow](../../../setup/SKILL.md#installation-workflow).
Runtime bootstrap mechanics belong to `../../component-integration/SKILL.md`.

## Adoption checkpoint

Before migrating the first state owner, record the existing or newly configured
app runtime and the evidence for each checkpoint:

| Migration checkpoint | Canonical implementation |
| --- | --- |
| Package installed, public imports used rather than copied source | [Installation workflow](../../../setup/SKILL.md#installation-workflow) and [Correct import and class choice](../../store/SKILL.md#correct-import-and-class-choice) |
| One app-owned store and reducer map, with no package-internal registrations | [Create and configure ReactStore](../../component-integration/SKILL.md#create-and-configure-reactstore) |
| Migrated selector users cannot render before initialization | [Initialize before React renders selector users](../../component-integration/SKILL.md#initialize-before-react-renders-selector-users) |
| The same bootstrap, test, or mount adapter owns cleanup, not a child effect | [Dispose at the same owner boundary](../../component-integration/SKILL.md#dispose-at-the-same-owner-boundary) |
| Migrated sagas start explicitly after initialization and have a cancellation owner | [Start app sagas explicitly](../../component-integration/SKILL.md#start-app-sagas-explicitly) |

Reuse an existing configured store rather than introducing a second runtime. If
no slice has migrated yet, its initial app-owned reducer map can be empty; add
reducers as their owners migrate using the linked configuration procedure.

## Add slices incrementally

Migrate one inventoried owner at a time. Follow
[Setup — slice directory layout](../../../core/file-structure/SKILL.md#setup--slice-directory-layout)
for slice types, actions/reducers, selectors, sagas, and tests rather than copying
a second layout here. Register the migrated reducer and start its saga through
the same runtime owner recorded in the checkpoint above.

## Verification cues

- Record the configured store module, bootstrap/mount owner, teardown path, and
  migrated reducer/saga registrations; verify each against its canonical section above.
- Continue to `../writable-stores/SKILL.md` only after this checkpoint is satisfied.