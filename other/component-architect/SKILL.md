---
name: component-architect
description: Design a reusable component's API before its looks - what is fixed, what is configurable, which variants exist - and keep its live preview, generated prompt and source code in agreement. Use when adding a configurable component to a library, or when a component has grown props that fight each other.
---

# /component-architect

A configurable component makes three promises: the **preview** shows it, the **code** implements it, and the **description or prompt** explains it. Most library bugs come from those three disagreeing.

## 1. Split fixed from configurable

Write two lists.

- **Fixed:** purpose, structure, core interaction, motion model, accessibility contract, responsive behaviour, dependencies. These are always true, and they belong in the base description.
- **Configurable:** each axis that changes, such as colour, theme, layout, density, interaction mode or content. For each axis, list its values and exactly what each one changes.

If a "variant" changes structure or behaviour rather than appearance, it is a different component or a mode prop, not a palette.

## 2. Props follow axes

- One prop per axis (`palette`, `theme`, `mode`), each taking a small union of named values, plus an escape hatch for custom values (e.g. `colors={[...]}`).
- Defaults give the most common case. Props never contradict each other; if two do, merge them into one axis.
- **Accessibility props** (labels, `motion="reduced"`) are first-class and documented, not afterthoughts.

## 3. Describe the selection, not the catalogue

Keep a base description of what's fixed. Each variant gets its own short description of what it alone looks like and which props produce it. The text a user copies is *base + the selected variant*, never a list of every option.

Add a check in the build that fails when:

- a variant has no description;
- the base description names a specific variant;
- one variant's description names a sibling.

## 4. One source of selection

The preview, the prompt and any code snippet read the same selection state. Put it in the URL (`?variant=`) so it survives a reload and can be shared. Copy buttons read the state at click time, so the copied text is never stale.

## 5. Test every state

For each variant:

- render it;
- read the generated description;
- assert that it contains this variant and no sibling;
- assert that the props it names exist in the source.

Also test reload, rapid switching, mobile width and reduced motion.

## Output

The fixed/configurable table, the props signature, the per-variant descriptions, and the test results.
