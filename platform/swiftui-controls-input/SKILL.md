---
name: swiftui-controls-input
description: "Implement SwiftUI buttons, menus, pickers, forms, focus, keyboard submission, text entry, gestures, drag and drop, and validation with native semantics."
---

# Controls, forms, and input

## Inputs

Identify whether the interaction is an action, navigation, selection, edit, or continuous adjustment. Record commit/cancel semantics, input devices, validation rules, and accessibility requirements.

## Rules

- **CTRL-001 — Use the semantic control.** Prefer `Button`, `NavigationLink`, `Picker`, `Toggle`, `Slider`, and platform menus over lookalike gesture-only views.
- **CTRL-002 — Separate appearance from behavior.** Use system styles first; a custom `ButtonStyle` must preserve role, enabled, focus, pressed, keyboard, and accessibility behavior.
- **CTRL-003 — Make selection type-safe.** Use a single selection binding and unique matching tags. Distinguish choosing a value from committing a form.
- **CTRL-004 — Own focus and validation.** Model the focused field, submit action, and error presentation deliberately. Do not destroy active input to hide a layout defect.
- **CTRL-005 — Protect the command boundary.** Disable or deduplicate repeated commits as appropriate, preserve failed drafts, and provide alternatives to gesture-only actions.

## Workflow

1. Trace control → binding or command → side effect.
2. Choose a label that describes the action; retain semantic text for icon-only presentation.
3. Implement all relevant states, including disabled, busy, invalid, destructive, and unavailable.
4. Choose keyboard, focus, AutoFill, dismissal, and confirmation behavior from the actual workflow.
5. Test with touch, pointer, keyboard, and assistive interaction where applicable.

## Verify

Verify exactly one picker selection, correct commit timing, duplicate activation, keyboard navigation, input composition, validation recovery, long labels, and VoiceOver activation.

## Output

Return the chosen control semantics, state/commit contract, and interaction checks; explain custom behavior only where needed.

## References

Read the [playbook](references/control-patterns.md) for decisions, failure cases, and source links.

For focus, forms, and editable control contracts, read the [focused reference](references/focus-and-form-contracts.md).
