---
name: rule-frontend-storybook
description: MANDATORY when editing files matching ["frontend/**/*.stories.tsx", "frontend/**/*.stories.ts", "frontend/**/*.stories.jsx", "frontend/.storybook/**/*"]. Storybook story writing patterns, args/controls configuration, accessibility (a11y) stories, and visual regression story setup
---

# Frontend Storybook Rules

## CSF3 Format

ALWAYS use Component Story Format 3 (CSF3) with `Meta` and `StoryObj` types from `@storybook/react`. NEVER use CSF2 function-based stories. PREFER `args` over custom `render` functions.

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Forms/Button",
  component: Button,
  args: { children: "Click me", variant: "primary" },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Default: Story = {};
export const Disabled: Story = { args: { disabled: true } };
```

## File Conventions

ALWAYS co-locate `Component.stories.tsx` next to `Component.tsx`. ALWAYS mirror folder structure in the `title` (e.g., `Components/Forms/Button`). ALWAYS export a `Default` story and add named variants for key states: `Loading`, `Error`, `Disabled`, `Empty`, `Filled`. NEVER duplicate `Default` under another name.

## Args & Controls

ALWAYS define `argTypes` for interactive controls with explicit control kinds (`select`, `radio`, `boolean`, `text`, `color`). ALWAYS set shared defaults via `meta.args` and override per-story. ALWAYS document props via `argTypes[prop].description` and `table.type`.

```tsx
const meta: Meta<typeof Alert> = {
  title: "Components/Feedback/Alert",
  component: Alert,
  args: { tone: "info" },
  argTypes: {
    tone: {
      control: { type: "select" },
      options: ["info", "success", "warning", "error"],
      description: "Visual tone of the alert.",
      table: { type: { summary: "AlertTone" } },
    },
  },
};
```

## Accessibility Stories

ALWAYS rely on `@storybook/addon-a11y` — every component's `Default` story MUST pass a11y checks. ALWAYS add explicit stories demonstrating keyboard navigation, focus states, and screen-reader labels. For form components, ALWAYS include stories with associated labels and error messages. When intentionally disabling an a11y rule, ALWAYS document it in `parameters.a11y.config.rules` with a comment explaining why.

```tsx
export const WithError: Story = {
  args: {
    label: "Email",
    error: "Email is required",
    "aria-describedby": "email-error",
  },
};

export const DecorativeIcon: Story = {
  args: { icon: "star", "aria-hidden": true },
  parameters: {
    a11y: {
      config: {
        // Decorative-only icon; label provided by sibling text.
        rules: [{ id: "svg-img-alt", enabled: false }],
      },
    },
  },
};
```

## Visual Regression Stories

ALWAYS create dedicated stories for visual states: `Hover`, `Focus`, `Active`, `Disabled`, `RTL`, and dark mode (if supported). ALWAYS use `parameters.chromatic` (or the project's VR tool) to control viewports, delay, and disable flaky stories. NEVER use randomness, animations, live data, or `Date.now()` in VR stories — mock everything for deterministic snapshots.

```tsx
export const Hover: Story = {
  args: { children: "Hover me" },
  parameters: { pseudo: { hover: true }, chromatic: { delay: 200 } },
};

export const Animated: Story = {
  parameters: { chromatic: { disableSnapshot: true } },
};
```

## Decorators & Providers

ALWAYS wrap stories that need context (theme, i18n, router, query client) via decorators in `.storybook/preview.tsx` for global providers, or via per-story `decorators` for opt-in cases. KEEP decorators minimal and reusable — extract shared wrappers into `.storybook/decorators/`.

```tsx
export const Localized: Story = {
  decorators: [(StoryFn) => <IntlProvider locale="es"><StoryFn /></IntlProvider>],
};
```

## Mocking

ALWAYS mock network calls with MSW via `msw-storybook-addon` — NEVER make real API calls from stories. ALWAYS mock Next.js router/navigation through the official `@storybook/nextjs` framework helpers. Use `parameters.nextjs.appDirectory` and `parameters.nextjs.navigation` for App Router segment params.

```tsx
export const Loaded: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("/api/opportunities", () => HttpResponse.json(opportunityFixture)),
      ],
    },
    nextjs: { appDirectory: true, navigation: { pathname: "/opportunities" } },
  },
};
```

For story-specific mock data, PREFER reusing fixtures from `src/utils/testing/fixtures.ts`. Per-story JSON mocks (e.g., `stories/components/.../*.mock.json`) are only acceptable when the fixture is genuinely story-only.

## Play Functions & Interaction Tests

ALWAYS use `play` with `@storybook/test` (`userEvent`, `expect`, `within`) to script interactions. KEEP `play` functions focused — assert observable behavior, NEVER implementation details.

```tsx
import { userEvent, within, expect } from "@storybook/test";

export const SubmitsForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText("Email"), "user@example.com");
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));
    await expect(canvas.getByText(/thanks/i)).toBeInTheDocument();
  },
};
```

## Storybook Config (`.storybook/`)

`main.ts` MUST declare `framework`, `addons`, and a `stories` glob. `preview.tsx` MUST set global decorators, `parameters` (backgrounds, viewport, a11y), and `globalTypes` (theme, locale). KEEP config DRY — extract shared decorators into `.storybook/decorators/` helpers.

## Anti-Patterns

NEVER branch on `process.env` inside stories. NEVER make real network or database calls. NEVER export untyped stories (`export const Foo = {}` without `StoryObj`). NEVER duplicate the `Default` story under a different name. NEVER rely on the user's system clock or `Math.random()` — snapshots must be deterministic.

---

## Related Rules

When working on Storybook stories, also consult:
- **`frontend-components.mdc`** — component patterns being storied
- **`frontend-tests.mdc`** — overlap with interaction tests and fixtures
- **`frontend-i18n.mdc`** — locale decorator and translation setup
- **`accessibility.mdc`** — WCAG 2.1 AA compliance validated by a11y addon

## Specialist Validation

**Simple changes (new variant, args tweak):** No specialist needed.

**Moderate changes (new component story file, new decorator):** Invoke `codebase-conventions-reviewer`.

**Complex changes (Storybook config, framework upgrade, new global decorator/addon):** Invoke in parallel:
- `architecture-strategist` — validate config structure
- `accessibility-auditor` — verify a11y addon coverage
- `kieran-typescript-reviewer` — story typing review
