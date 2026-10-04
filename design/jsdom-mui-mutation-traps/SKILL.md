---
name: jsdom-mui-mutation-traps
description: Use when mutants in MUI component styling or controlled-value handling survive despite tests that look like they cover the behaviour, when a test reads getComputedStyle on an Emotion styled element under jsdom, or when a mutation score stalls below the gate after adding coverage.
---

# jsdom and MUI mutation traps

## Profile keys consumed

- `make.test_unit_client`
- `make.test_mutation`
- `make.test_visual`
- `capabilities.mutation_testing`
- `capabilities.visual_testing`
- `quality.mutation_msi`
- `framework.ui`

Every suite runs through the profile's `make` target map. Skip the mutation
half with a recorded note when `capabilities.mutation_testing` is `false` or
`make.test_mutation` maps to `null`, and skip the "move the assertion to the
visual suite" remedy with a note when `capabilities.visual_testing` is `false`.

## Overview

Two jsdom behaviours make a test look like it kills a mutant when it cannot. Both come from the gap
between jsdom and a real browser: jsdom has no CSS cascade worth trusting, and the controlled
components of the UI library named by `framework.ui` compare stringified values, so a coerced empty
value hides the difference the mutant made.

## When to use

- A style assertion reads `getComputedStyle(element)` on a component styled through the MUI theme
  plus an `sx` prop, and mutants in either layer survive.
- A test for "the field renders its empty state" passes with the same measured value in the
  non-empty state.
- A controlled MUI input is bound as `value={state ?? ''}` and a mutant that removes the reset/clear
  call still passes the suite.
- The mutation score refuses to move against the `quality.mutation_msi` floor after adding tests
  aimed exactly at the survivors.
- Not for: mutants surviving because a module-level constant was evaluated at import time before the
  test ran — that is an isolated-module-loading problem, not a jsdom one.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — a jsdom Jest environment behind `make.test_unit_client`, MUI with Emotion 11, and
  a Stryker gate whose thresholds leave no room for an unearned kill.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — same jsdom + MUI +
  Emotion stack; the mutate scope is a curated file list, so the traps bite only when a listed file
  styles or controls a MUI input.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — a jsdom
  Jest environment and MUI components are the whole product; the Playwright visual suite mapped by
  `make.test_visual` is the natural home for the style assertions this skill moves out.

## Trap one: getComputedStyle cannot resolve MUI specificity

jsdom does not implement the cascade the way a browser does; conflicting declarations resolve by
insertion order. Emotion injects the theme's class after the component's `sx` class in some orders,
so the value `getComputedStyle` reports is whichever rule was inserted last, not the one that would
win in a browser. A test that reads the empty-state colour therefore reads the same value for a
filled field, and every mutant in either declaration survives.

Assert what the user can observe instead — rendered text, a role/state change, presence or absence
of an element. When only the pixels matter, move the assertion to the Playwright visual suite
mapped by `make.test_visual`, where real CSS applies. If a computed-style read is genuinely
unavoidable, resolve the winning declaration by selector weight yourself rather than trusting the
reported value.

## Trap two: a coerced empty value is not observable

MUI compares controlled values as strings. With `value={selected ?? ''}`, both "the state was
cleared" and "the state was never cleared" can stringify to `''`, so a mutant that deletes the reset
call produces an identical DOM.

Give the component an explicitly empty-valued option so the coercion target becomes a real,
selectable state:

```ts
<MuiRadioGroup value={selected ?? ''} onChange={onChange}>
  <MuiFormControlLabel value="" label="None" control={<MuiRadio />} />
  <MuiFormControlLabel value="option-a" label="Option A" control={<MuiRadio />} />
</MuiRadioGroup>
```

Then assert on which option is checked, which differs between the original and the mutant:

```ts
expect(screen.getByRole('radio', { name: 'None' })).toBeChecked();
```

## Common mistakes

- Treating a surviving style mutant as an equivalent mutant — it is usually an unobservable
  assertion, so re-aim it at observable output before declaring the mutant unkillable.
- Asserting the coerced value (`expect(input).toHaveValue('')`) and calling the branch covered —
  assert which explicitly-valued option is selected instead.
- Reaching for a threshold change when the score stalls — `quality.*` thresholds are raise-only, so
  fix the assertion so it observes the difference the mutant makes.
