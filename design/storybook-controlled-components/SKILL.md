---
name: storybook-controlled-components
description: >-
  Use when a Storybook story for a controlled component is frozen — picking an option, deleting a
  chip, typing, or toggling fires onChange but nothing on screen changes. Applies to any story whose
  component takes a value prop plus an onChange callback (inputs, selects, multi-selects,
  checkboxes, radio groups, autocompletes, date pickers) and to stories wired only to an action
  logger.
---

# Storybook stories for controlled components

## Profile keys consumed

- `capabilities.storybook`
- `make.storybook_build`
- `capabilities.visual_testing`
- `make.test_visual`
- `architecture.source_root`
- `architecture.component_prefix`

Storybook work is gated by `capabilities.storybook`: skip the whole skill with a recorded
capability-absent note when it is `false`. Verify a story through the target mapped by
`make.storybook_build` (skip with a recorded note when it maps to `null`), and through the target
mapped by `make.test_visual` where the stories are the screenshot surface.

## Overview

A controlled component renders whatever `value` it is handed. A story that passes a static `value`
and only logs `onChange` can never update, so the story looks broken even though the component is
correct. The story itself has to own the state.

## When to use

- A story's control does not respond to clicks, selection, deletion, or typing.
- A story passes `value` from `args` and wires `onChange` to an action logger only.
- A new story is being written for any component that exposes a `value` / `onChange` pair.
- Not for: uncontrolled components, or components whose only props are presentational.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — Storybook 9 with stories under `<source root>/**/*.stories.@(js|jsx|ts|tsx)`; the
  repository's Storybook dev-server target runs the panel.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — Storybook 10 with the
  same story glob plus `mjs`, driven by the same Storybook dev-server target.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  Storybook 10, stories co-located in each prefixed component folder under the source root
  (`architecture.component_prefix`, e.g. `src/components/ui-*`); the select and multi-select stories
  are the shipped examples.

```bash # profile-example
# Where a shape maps a Storybook dev-server target, it is typically:
make storybook-start
```

## Core pattern

Use a CSF3 `render` that is a **named function** — hooks are only legal inside a component, and the
capitalised name is what makes lint and React treat it as one. Seed the state from `args` so the
Controls panel still supplies the initial selection, then turn off the panel control for `value` so
it cannot fight the local state.

```ts
const meta: Meta<typeof UiMultiSelect> = {
  title: 'UiComponents/UiMultiSelect',
  component: UiMultiSelect,
  argTypes: {
    options: { control: 'object' }, // editable in the panel, unlike `value`
    // Selection is driven by the story's own state; its panel control is off.
    value: { control: false },
  },
};

export const MultiSelect: StoryObj<typeof UiMultiSelect> = {
  args: { options, value: [options[0], options[2]], label: 'Role' },
  render: function Render(args): React.ReactElement {
    const [value, setValue] = React.useState<UiMultiSelectOption[]>(args.value ?? []);
    return (
      <UiMultiSelect
        options={args.options}
        label={args.label}
        value={value}
        onChange={setValue}
      />
    );
  },
};

// Sibling variants reuse the same stateful renderer rather than copying it.
export const Loading: StoryObj<typeof UiMultiSelect> = {
  args: { options, value: [options[0]], label: 'Role', loading: true },
  render: MultiSelect.render,
};
```

Everything that is _not_ selection state — `options`, `label`, `placeholder`, `disabled`, `loading`
— keeps coming from `args`, so the Controls panel stays useful for exercising the component with
different data.

## Why it matters beyond the panel

In the component-library shape the stories are the render surface for the Playwright visual suite
mapped by `make.test_visual`, which screenshots them directly: a frozen story pins a baseline of a
state the component can never actually reach, so the regression the baseline was meant to catch goes
unnoticed. In the React SPA and Next.js shapes the Playwright suites drive the app rather than
Storybook, but the stories are still the review surface and the Storybook build gate mapped by
`make.storybook_build`, so a frozen story hides the same defect from the reviewer.

## Common mistakes

- An arrow function for `render` — the hook then sits outside a component and the hooks lint fails.
- Leaving `value` as an editable control while local state also owns it; the two overwrite each
  other and the story flickers back to the arg.
- Copying the whole stateful renderer into every variant instead of reusing the first story's
  `render`, which duplicates code and drifts.
- Initialising state from a module-level constant instead of `args`, so the Controls panel's initial
  value is silently ignored.
