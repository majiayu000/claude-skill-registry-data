---
name: hig-controls
description: "Select and repair buttons, fields, selection controls, menus, sheets, dialogs, tables, and charts through explicit behavioral contracts."
---

# Repair the control’s behavior before its skin

Follow the [root contract](../../SKILL.md). Load [component-contracts.md](../../references/component-contracts.md), [state-matrix.md](../../references/state-matrix.md), and [numeric-and-web-rules.md](../../references/numeric-and-web-rules.md). HIG-010–018 and HIG-021 provide component-specific context.

## Start with the user’s intent

Classify each problematic control: navigate, execute, toggle a persistent setting, choose one, choose many, adjust a value, enter data, disclose content, or complete a bounded transaction. Match its semantic and interaction model to that intent.

Inspect the existing framework control before building a replacement. A custom visual wrapper is acceptable only when its name, role, value, keyboard behavior, pointer behavior, focus, validation, and states remain correct. Do not recreate a native control with a clickable generic container merely to achieve a different shape.

## Specify the complete contract

For each changed component record:

- Input/output value and which layer owns it.
- Immediate versus staged changes; explicit save versus autosave.
- Enabled, disabled, read-only, busy, selected, focused, invalid, and pending states.
- Activation, cancellation, dismissal, repeat activation, and interruption behavior.
- Accessible name, description, role, and state exposure.
- Failure handling, draft preservation, and return focus.

Name what “disabled” means. If a prerequisite is missing, explain the prerequisite at a useful point rather than leaving a dead control with no path forward. Never use disabled visuals as a substitute for server-side authorization.

## Forms

Inventory every field and ask whether it is needed for this task now. Identify label, purpose, data type, required/optional status, helper text, accepted format, locale handling, validation rules, privacy sensitivity, and autofill behavior.

Use persistent labels; placeholders can provide examples but should not carry the entire identity of a field. Associate errors with fields and make correction possible without losing valid input. Do not reformat partially entered values in a way that prevents the user from typing a valid final value.

Use appropriate keyboard and input hints without treating them as validation. Handle paste, password managers, multi-character input, composition input, autofill, and server rejection. Do not block copying or pasting as a cosmetic simplification.

Clarify whether an Enter/Return press submits, inserts a newline, or accepts a suggestion. Test the default action so destructive work is not accidentally committed. Preserve drafts according to the product’s privacy and expiry requirements.

## Menus, sheets, and dialogs

Use menus for a compact set of related choices; use a task surface when the interaction requires richer input or explanation. Avoid nesting transient layers merely to fit an oversized workflow into a small container.

For a modal interaction, define the initial focus, tab sequence, background availability, close paths, dismissal policy, and focus return. On the web, follow the applicable native dialog behavior and APG pattern; do not confuse adding `aria-modal` with implementing modality.

Cancel must have a clear meaning. Test outside activation, Escape, system back/dismissal, window closure, and dirty data as applicable. Do not dismiss on arbitrary pointer events if it causes accidental work loss.

## Collections and quantitative displays

Determine whether the task is scanning, comparing columns, selecting items, or reading individual narratives. Keep tables when relationships across columns matter; do not automatically replace them with large cards on every viewport.

Document sorting, selection scope, pagination, filtering, bulk actions, and detail navigation. Selection must not silently widen from visible rows to an entire account. Distinguish zero from missing, unavailable, or still loading.

For charts, specify the question answered, units, aggregation, time interval, scale, and data limitations. Maintain an accessible route to the underlying meaning or values. Visual decoration must not distort comparison or imply precision the data lacks.

## Output and gate

Deliver a component decision table and before/after contracts with tests for normal and adverse states. A pass requires correct semantics, predictable activation, recoverable failure, valid focus behavior, and preservation of domain rules—not merely matching corner radii.
