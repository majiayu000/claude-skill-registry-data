---
name: storybook-story-authoring
description: Use when adding or changing a `*.stories.tsx` file for a React component — a new shared primitive carrying `architecture.component_prefix`, a variant or state that needs documenting, sidebar `title` placement, `argTypes` controls, a story that imports `Meta`/`StoryObj` from the wrong `@storybook/*` package, or a red run of the target mapped by `make.storybook_build`.
---

# Storybook Story Authoring

## Profile keys consumed

- `capabilities.storybook`
- `make.storybook_build`
- `make.lint`
- `make.lint_dup`
- `make.format`
- `make.test_e2e`
- `make.test_visual`
- `architecture.source_root`
- `architecture.component_prefix`

Every command resolves through the profile's `make` target map. Skip a
dependent step with a recorded note when its key maps to `null`, and record
the whole skill NOT-APPLICABLE when `capabilities.storybook` is `false`.

## Overview

Every user-visible component ships at least one story, colocated with the component source. A story
is the component's interactive documentation and, where the browser suites drive Storybook, its test
bed — so an unbuildable story is a red gate, not a cosmetic miss.

## When to use

- Building a shared UI primitive or a feature component that has variants, sizes, or states.
- Documenting disabled, loading, error, or empty states that a screenshot alone cannot explain.
- Refactoring a component whose props, defaults, or accessible name changed.
- Adding controls so a reviewer can exercise props without editing code.
- Not for: pixel-diff coverage — that is the Playwright visual suite driven by `make.test_visual`,
  and stories do not replace it.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate
  CI target): partial — a Storybook dev-server target plus the target mapped by
  `make.storybook_build`, glob `src/**/*.stories.@(js|jsx|ts|tsx)`, but types come from
  `@storybook/react-webpack5` and no browser suite reads stories.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — types come from
  `@storybook/nextjs`; the target mapped by `make.storybook_build` depends on localization
  generation because stories import the i18n stack.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — types
  come from `@storybook/react`; the targets mapped by `make.test_e2e` and `make.test_visual` boot
  Storybook through a Playwright runner, so a broken story reds both gates.

## Core pattern

Place the file in the component's own kebab-case folder under `architecture.source_root` —
`src/components/ui-chevron-button/` holds `index.tsx`, `types.ts`, `styles.ts`, and
`chevron-button.stories.tsx`. Import the story types from the framework package the repository
actually installs; the three shapes install three different ones and a wrong import fails the build.
The sample below is the component-library shape's spelling.

```ts
import type { Meta, StoryObj } from '@storybook/react';

import {
  selectControlArgType,
  textControlArgType,
} from '../../../.storybook/field-story-arg-types';

import UiChevronButton from './index';

// Icon-only, so this is the button's whole accessible name.
const CHEVRON_LABEL: string = 'Next page';

const meta: Meta<typeof UiChevronButton> = {
  title: 'UiComponents/UiChevronButton',
  component: UiChevronButton,
  tags: ['autodocs'],
  argTypes: {
    label: textControlArgType('Accessible name (aria-label) — the only name channel'),
    direction: selectControlArgType('Which way the glyph points', ['left', 'right']),
  },
};

export default meta;

type Story = StoryObj<typeof UiChevronButton>;

export const ChevronButton: Story = {
  args: { label: CHEVRON_LABEL, direction: 'right' },
};
```

`title` is a namespace path, not free text, and the prefix follows the repository's own convention:
shared primitives sit under `UiComponents/` in the component-library and Next.js shapes, under
`Components/` in the React SPA shape. Follow the prefix the neighbouring stories already use so the
sidebar groups them, and keep it consistent with `architecture.component_prefix`. Story export names
are PascalCase and name the state (`Default`, `Disabled`, `Loading`, `Error`, `Empty`,
`LongContent`) rather than the fixture that produces it.

## Quick reference

- Keep repeated `argTypes` builders in one shared module under `.storybook/` and import them; each
  story re-declaring the same control block is duplicated code the copy/paste gate mapped by
  `make.lint_dup` can flag (skip with a recorded note when it maps to `null`).
- Import `styled` components and `sx` fragments from the component's own styles module; theme
  tokens, never hardcoded hex.
- An icon-only control needs its accessible name supplied in `args` — the story is where a missing
  one becomes visible.
- Verify with the target mapped by `make.storybook_build` (it must exit clean), then the target
  mapped by `make.lint`. Where the repository exposes `make.format` run it first; the
  component-library shape instead formats through a `format-check` step inside its lint target.

```bash # profile-example
# With a profile whose storybook keys map to these targets:
make storybook-start     # local dev server, no logical key — describe by purpose
make storybook-build     # make.storybook_build → must exit clean
make lint                # make.lint
```

## Common mistakes

- Importing `Meta`/`StoryObj` from a package the repository does not install — use the framework
  package named in `.storybook/main.ts`.
- A PascalCase component folder or a `<ComponentName>.stories.tsx` name — folders and files are
  kebab-case in all three repository shapes.
- Declaring `styled()` inside the story file — import it from the component's own styles module so
  the story cannot drift from the real styling.
- Treating a story as visual-regression coverage — add a spec to the visual suite instead.
- Adding an addon whose peer range exceeds the pinned Storybook major — check the range first, or
  the preset fails to load and every build and dev start crashes.
