---
name: apex-enum-patterns
description: "Apex enum patterns — enum-based dispatch instead of string switching, ordinal stability, enum values in Custom Metadata, package-global enums, and the limitations (no methods on enum constants, no associated data). Covers `Enum.values()`, `valueOf(String)` failures, and the right way to map an enum to/from a picklist value. NOT for picklist-field design and value-set management — use admin/picklist-and-value-sets. NOT for reading picklist values at runtime via describe — use apex/apex-schema-describe."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Security
triggers:
  - "apex enum dispatch instead of string switch"
  - "enum valueOf throws system exception"
  - "apex enum custom metadata mapping"
  - "global enum managed package compatibility"
  - "apex enum ordinal stable identifier"
  - "switch on apex enum exhaustive"
tags:
  - enum
  - dispatch
  - custom-metadata
  - managed-package
  - type-safety
inputs:
  - "What the enum is modeling: state machine, dispatch type, picklist mirror, message subtype"
  - "Whether the enum is in a managed package (global vs public)"
  - "Whether the enum is persisted (string serialization to a field)"
outputs:
  - "Enum declaration with documented intent"
  - "Switch / dispatch pattern that handles all values"
  - "Safe conversion to/from string with default branch"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-05
---

# Apex Enum Patterns

Apex enums are simpler than Java enums — no constructors, no
methods on enum constants, no per-value data — but they still beat
unstructured strings for state-machine dispatch, message routing,
and any "one of N exhaustive options" code path.

The mistakes follow a predictable pattern: people serialize enum
values into Custom Metadata or a Long Text field, the picklist
gets renamed, and `Enum.valueOf(String)` starts throwing
`System.NoSuchElementException` in production. Or someone adds a
new enum value and the `switch on` doesn't have a branch — Apex
falls through silently because there's no compiler exhaustiveness
check.

This skill covers the patterns that make enums useful in Apex
without the foot-gun.

## Recommended Workflow

1. **Decide if an enum is the right shape.** If you have <2 values
   or values change at runtime, use a Boolean or a Custom
   Metadata-driven string. Enums are for closed sets.
2. **Name the enum after intent, not type.** `RenewalAction`
   beats `EnumType1`.
3. **Use `switch on <Enum>` with a `when else` branch** that throws
   a clear exception. This is the only way to surface a missed
   case at runtime when the enum gains a new value.
4. **Wrap `Enum.valueOf(String)` in a safe converter** that returns
   a default or throws a typed exception with the offending input
   in the message.
5. **Document `global` vs `public` in managed packages.** Once
   shipped, removing or renaming a `global` enum value is a
   breaking change.
6. **Write a test that asserts the enum's `values()` matches the
   expected set.** This is the cheapest exhaustiveness check Apex
   gives you.

## When To Reach For An Enum

The right places: trigger-handler dispatch keys, message-routing
discriminators, log-level enums, status machines that the app
itself owns end-to-end. Anywhere the set of values is a property
of the code, not the data, an enum is the cheaper, safer choice.

The wrong places: anything an admin should be able to add to. If
adding a new "approval reason" should not require a deployment,
do not put it in an enum. The enum becomes a maintenance ratchet
that pulls every dispatcher into the release pipeline.

## What This Skill Does Not Cover

- **Picklist-field design** — see `admin/picklist-design`.
- **Custom Metadata as configuration store** — see `apex/custom-metadata-types`.
- **State machines with side effects** — see `architect/state-machine-patterns`.
