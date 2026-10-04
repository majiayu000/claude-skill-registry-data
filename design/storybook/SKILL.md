---
name: storybook
description: Designs, configures, audits Storybook 8+ workspaces in Component Story Format 3 (CSF3). Writes meta/StoryObj-typed stories — args, argTypes, parameters, decorators, loaders — and play functions with `@storybook/test`. Covers default, variant-matrix, per-state, and interaction stories. Configures `.storybook/main.ts`, `.storybook/preview.tsx`, addons (a11y, controls, docs, interactions, themes, viewport, msw, vitest, chromatic), autodocs/MDX, theming decorators, and MSW network mocking. Sets up the test runner, the Vitest addon, and Chromatic visual regression. Audits for missing variants/states, real network calls, brittle mocks, assertion-free play functions, and stories duplicating snapshots. Triggers on "storybook", "csf3", ".stories.tsx", "storyobj", "argtypes", "play function", "interaction test", "storybook addon", ".storybook/main", ".storybook/preview", "autodocs", "mdx", "storybook test runner", "storybook vitest", "msw storybook", "chromatic", "visual regression", "story composition".
---

# Storybook

Storybook is a workshop for UI in isolation. Every story is a named, reproducible state of a component. The skill covers authoring stories, configuring the workspace, wiring addons, and auditing existing story files.

## Mode router

| Mode | Use when | Output |
|------|----------|--------|
| **Author** | A component lacks story coverage | Story file with CSF3 `meta` + default + variants + per-state + interaction stories |
| **Configure** | A workspace is being set up or extended | `.storybook/main.ts`, `.storybook/preview.tsx`, addon wiring, MSW/Chromatic/test-runner setup |
| **Audit** | An existing story file or workspace needs review | Severity-ranked findings with `file:line` |

If the mode is ambiguous, ask.

## This project's workspace

The rest of this skill is general Storybook reference. These are the facts for
**react-basics-ui** — prefer them over the generic examples below when they differ.

| | Actual |
|---|---|
| Version | Storybook **10**, `@storybook/react-vite` |
| Config | `.storybook/main.ts` and `.storybook/preview.ts` — **`.ts`, not `.tsx`** |
| Stories glob | `../src/**/*.stories.@(js\|jsx\|mjs\|ts\|tsx)` — depth-agnostic, so nested component folders are picked up automatically. No `*.mdx` glob: there are no MDX files, and the glob logged "No story files found" on every run |
| Addons registered | `@storybook/addon-docs`, `@storybook/addon-a11y`, `@storybook/addon-vitest` |
| Global CSS | `preview.ts` imports `../src/global.css` — the token system. Without it every story renders unstyled |
| Alias | `viteFinal` maps `@` → `src/` |
| Commands | `npm run storybook` (dev, :6006) · `npm run build-storybook` · `npm run test:stories` |

**Stories are tests here.** `@storybook/addon-vitest` is wired as a `storybook`
project in `vitest.config.ts`, so every `play()` function executes in headless
Chromium under `npx vitest run`. A story with a broken `play()` fails the
suite. Don't write one you don't intend to hold. See [`test`](../test/SKILL.md).

Story discovery for that project comes from the `stories` globs above, not from
`test.include` — setting `test.include` on the storybook project is ignored and
warns on every run.

Not wired up here — don't assume they exist: MSW, Chromatic, `@storybook/test-runner`,
and `addon-themes`. None of those packages are installed.

`preview.ts` has no JSX today. Adding a decorator that returns JSX means renaming it
to `preview.tsx` — do that deliberately, and update this table.

Dark mode is driven by the `data-theme` attribute on the root element, not by a
Storybook theme addon. See the `ThemeProvider` component and [`design-systems`](../design-systems/SKILL.md).

## Story format (CSF3)

One story file per component, co-located beside the component as `<Name>.stories.tsx`.

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta = {
  title: "Primitives/Button",
  component: Button,
  tags: ["autodocs"],
  args: { children: "Click me", tone: "neutral", size: "md" },
  argTypes: {
    tone: { control: "inline-radio", options: ["neutral", "success", "danger"] },
    size: { control: "inline-radio", options: ["sm", "md", "lg"] },
    onClick: { action: "clicked" },
  },
  parameters: { layout: "centered" },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
export const Danger: Story = { args: { tone: "danger" } };
export const Disabled: Story = { args: { disabled: true } };
```

Rules:

- `satisfies Meta<typeof Component>` — preserves the component's prop types so `args` and controls are correctly typed.
- `StoryObj<typeof meta>` — inherits meta-level `args` types into every story.
- Default export must be the meta object. Named exports become stories.
- Story names follow PascalCase. They render as labels in the sidebar.
- Disable controls for props that should not be tweaked (`argTypes: { ref: { table: { disable: true } } }`).

## What to write per component

| Story | When | Notes |
|-------|------|-------|
| Default | Always | Canonical use with realistic args |
| Variants | Per variant axis (size, tone, density) | One story per axis, or a matrix story rendering all combinations |
| State | One per applicable interaction state | Story name = state name (Hover, Focus, Disabled, Loading, Error, Empty, ReadOnly, Indeterminate, Selected) |
| Interaction | One per behavior | Play function asserts the behavior |
| Edge content | Long strings, RTL, narrow viewport, dense data | Catches layout fragility |

Force a hover/focus state by parameter, not by writing a separate component:

```tsx
export const Hover: Story = { parameters: { pseudo: { hover: true } } };
```

(Requires `storybook-addon-pseudo-states` registered in `main.ts`.)

## Play functions

Play functions run inside the story canvas after render. Use them to drive a behavior and assert the result.

```tsx
import { expect, userEvent, within } from "@storybook/test";

export const SubmitsOnEnter: Story = {
  args: { onSubmit: fn() },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByRole("textbox"), "hello{Enter}");
    await expect(args.onSubmit).toHaveBeenCalledWith("hello");
  },
};
```

Rules:

- Import `expect`, `fn`, `userEvent`, `waitFor`, `within` from `@storybook/test` — not from `@storybook/jest` or `@testing-library/*`. The Storybook re-export is the supported surface.
- Use `fn()` to create spies in `args`. Wire to `argTypes: { onX: { action: "x" } }` only when an action log is enough.
- Query by accessible role first (`getByRole`), text second, test-id last.
- Await every `userEvent.*` and every `expect` to keep the timeline deterministic.
- Keep play functions under ~50 lines. Past that, the story is testing too many things — split into two stories.
- Do not assert internal implementation (state, context). Assert what a user observes: rendered text, role, value, focus, spy calls.

## Configuration

### `.storybook/main.ts`

```ts
import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  framework: "@storybook/react-vite",
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-a11y",
    "@storybook/addon-interactions",
    "@storybook/addon-themes",
    "@storybook/experimental-addon-test",
  ],
  docs: { autodocs: "tag" },
  typescript: { reactDocgen: "react-docgen-typescript" },
};

export default config;
```

- Glob both `*.mdx` and `*.stories.@(ts|tsx)` so docs pages and stories live beside components.
- `autodocs: "tag"` opts components in via `tags: ["autodocs"]` in meta. Avoid `"true"` (everything gets a docs page whether it deserves one or not).

### `.storybook/preview.tsx`

```tsx
import type { Preview } from "@storybook/react";
import { withThemeByClassName } from "@storybook/addon-themes";
import "../src/styles/globals.css";

const preview: Preview = {
  parameters: {
    controls: { matchers: { color: /(background|color)$/i, date: /Date$/ } },
    a11y: { config: { rules: [] } },
    layout: "padded",
  },
  decorators: [
    withThemeByClassName({ themes: { light: "", dark: "dark" }, defaultTheme: "light" }),
  ],
};

export default preview;
```

- Global decorators belong here — never inside individual story files.
- Register the theme toggle in `preview.tsx` once; stories must render correctly in every registered theme.
- Import global CSS here, not from individual stories.

## Decorators

A decorator wraps every story below it. Order matters: outermost first in the array, innermost closest to the story.

```tsx
const meta = {
  component: Form,
  decorators: [
    (Story) => <div style={{ maxWidth: 480 }}><Story /></div>,
    (Story) => <QueryClientProvider client={qc}><Story /></QueryClientProvider>,
  ],
} satisfies Meta<typeof Form>;
```

Use decorators for environment a component would have in production (theme, query client, i18n provider, router). Do not use them to inject mock data — that belongs in `args` or `parameters.mockData`.

## Mocking

### Network — MSW

Install `msw-storybook-addon`, initialize in `preview.tsx`:

```ts
import { initialize, mswLoader } from "msw-storybook-addon";
initialize({ onUnhandledRequest: "warn" });
preview.loaders = [mswLoader];
```

Per-story handlers via `parameters.msw.handlers`:

```tsx
export const Loaded: Story = {
  parameters: {
    msw: {
      handlers: [http.get("/api/users", () => HttpResponse.json([{ id: 1, name: "Ada" }]))],
    },
  },
};
```

### Modules

Storybook 8 supports module-level mocks via `vi.mock` only inside Vitest addon runs. For the canvas, prefer dependency injection through props or a context decorator.

## Documentation (autodocs + MDX)

`tags: ["autodocs"]` on meta auto-generates a Docs page from prop types and JSDoc.

For richer docs, add a sibling `<Name>.mdx` file:

```mdx
import { Meta, Canvas, Controls } from "@storybook/blocks";
import * as Stories from "./Button.stories";

<Meta of={Stories} />

# Button

When to reach for it, when not to.

<Canvas of={Stories.Default} />
<Controls of={Stories.Default} />
```

JSDoc on props becomes prop-table descriptions — keep them one sentence.

## Test runner & Vitest addon

Two test surfaces, pick by what you want:

| Surface | Runs | Use for |
|---------|------|---------|
| `@storybook/experimental-addon-test` (Vitest) | Story files as Vitest tests in the browser (Playwright) | Fast local feedback, CI-blocking play-function assertions, coverage |
| `@storybook/test-runner` (Playwright + Jest) | Built Storybook in a real browser | Smoke run that catches render errors, a11y violations, broken stories |

The Vitest addon is the default for new workspaces. The test runner is the right tool only when stories must be run against the deployed/published Storybook.

Add to `vitest.config.ts`:

```ts
import { storybookTest } from "@storybook/experimental-addon-test/vitest-plugin";

export default defineConfig({
  plugins: [storybookTest({ configDir: ".storybook" })],
  test: { browser: { enabled: true, name: "chromium", provider: "playwright" } },
});
```

A story without an explicit `play` is still run — render alone must succeed.

## Visual regression (Chromatic)

Chromatic captures a screenshot per story per viewport per theme. Wire it in CI on PRs.

```yaml
- uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    onlyChanged: true
```

`onlyChanged: true` uses TurboSnap to skip unchanged stories. Snapshot stability rules:

- No `Date.now()`, `Math.random()`, or animation frames in render — they cause false diffs. Inject deterministic substitutes via args or decorators.
- Pin font loading: use `<link rel="preload">` in `preview-head.html` and wait for `document.fonts.ready` in `preview.tsx`.
- Disable diff on a story that is intentionally non-deterministic: `parameters: { chromatic: { disableSnapshot: true } }`.

## Composition

Embed another Storybook into the sidebar of this one:

```ts
const config: StorybookConfig = {
  refs: { tokens: { title: "Design Tokens", url: "https://tokens.example.com" } },
};
```

Use composition to surface a design-system Storybook from an app Storybook. Do not mirror stories across repos.

## Audit dimensions

Run in order. Each finding: location, observation, impact, suggestion.

### 1. Story shape

```bash
grep -rnE "as Meta<|: Story = \{" --include="*.stories.tsx"
```

Findings:

- `as Meta<...>` instead of `satisfies Meta<...>` — types narrow incorrectly.
- Story without an explicit return type assigned to `Story` — controls lose autocomplete.
- Meta-level `args` omitted while every story re-declares the same defaults.

### 2. Play-function smells

| Smell | Fix |
|-------|-----|
| No `await` on `userEvent` calls | Add `await` — race conditions appear on slow CI |
| Asserts on internal state via `screen.debug()` or refs | Assert on rendered output |
| `setTimeout` waiting for async | Use `waitFor(() => expect(...))` |
| Imports from `@testing-library/react` directly | Import from `@storybook/test` |
| Play function over ~50 lines | Split into multiple stories |
| No assertion at all | Either add `expect(...)` or remove `play` |

### 3. Real-world leaks

```bash
grep -nE "fetch\(|axios|/api/" <story-file>
```

Every hit: replace with MSW handler in `parameters.msw.handlers`.

### 4. Coverage gaps

For each component story file, confirm:

- Default story exists.
- One story per applicable interaction state (Hover, Focus, Disabled, Loading, Error, Empty).
- One story per variant axis or a matrix story.
- At least one interaction story if the component has any behavior beyond rendering.

### 5. Configuration

- `.storybook/main.ts` uses framework presets, not hand-rolled Webpack/Vite config.
- `.storybook/preview.tsx` registers global CSS and global decorators — story files do not.
- A11y addon present and not silenced globally.
- Autodocs opt-in via `tag`, not blanket-enabled.

### Severity

- **Critical** — story renders against production network, breaks build, or fails to type-check.
- **High** — missing state/variant coverage that hides a real bug class; play function with no assertion; flaky snapshot source.
- **Medium** — outdated import surface (`@storybook/jest`), inconsistent naming, no autodocs tag on a public component.
- **Low** — taste call.

## Definition of Done

```
- meta uses `satisfies Meta<typeof Component>` and stories are `StoryObj<typeof meta>`
- Default + one story per applicable state + one per variant axis + ≥1 interaction story
- Every `userEvent` and `expect` awaited
- No real network calls; MSW handlers cover async stories
- A11y addon clean on every story (or violation explicitly waived with rationale)
- Component documented via autodocs tag or MDX
- Story file renders in light and dark themes without manual intervention
```

If any item fails, label **Iterate** and list the gap.

## Output templates

### Story plan

```
# Stories: <Component>

## Default
args: <realistic prop values>

## Variants
- <axis>: <values> → matrix story or one per value

## States
<one row per applicable state with story name + how it is forced (args, parameters.pseudo, MSW handler)>

## Interactions
- <behavior> → play asserts <observable outcome>

## Edge content
- <case>: <why>

## Open questions
1. [blocker] ...
2. [clarify] ...

## Status
**[Ready / Iterate / Blocked]**
```

### Audit report

```
# Storybook Audit: <path>
> Files examined: <clickable paths>

## Findings

### <Dimension>
**[Severity] — <title>**
- Location: file:line
- Observation: <what is there>
- Impact: <what a consumer or contributor notices>
- Suggestion: <concrete change>

[repeat per finding, grouped by dimension]

## Summary
| Severity | Count |
|----------|-------|
| Critical | N |
| High     | N |
| Medium   | N |
| Low      | N |

## Status
**[Ready / Iterate / Blocked]**
```
