---
name: storybook
description: |
  Storybook CSF3 story authoring methodology for UI component catalogs.
  Prioritizes visual showcase patterns over exhaustive argTypes enumeration.
  Reference for creating scannable, maintainable component documentation.
---

# Storybook Skill

## Philosophy: Catalog over Controls

**Problem with argTypes exhaustion:**
- Dozens of stories for every prop combination
- Hard to scan and find what you need
- Maintenance burden grows exponentially
- Controls panel becomes primary interaction

**Solution: Visual Showcase Pattern**
- One story shows multiple variants in a grid
- Immediate visual comparison
- Self-documenting code
- Controls for interactive exploration only

## CSF3 Story Patterns

### 1. Showcase Story (Primary Pattern)

Display all variants of a prop in a single story:

```tsx
/**
 * All button variants displayed together for visual comparison.
 */
export const Variants: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-4 items-center">
      <span className="text-sm text-muted-foreground">Primary</span>
      <Button variant="primary">Primary</Button>

      <span className="text-sm text-muted-foreground">Secondary</span>
      <Button variant="secondary">Secondary</Button>

      <span className="text-sm text-muted-foreground">Ghost</span>
      <Button variant="ghost">Ghost</Button>

      <span className="text-sm text-muted-foreground">Destructive</span>
      <Button variant="destructive">Delete</Button>
    </div>
  ),
}
```

### 2. State Matrix Story

Show component states in a grid:

```tsx
/**
 * Button states: normal, disabled, and loading.
 */
export const States: Story = {
  render: () => (
    <div className="grid grid-cols-3 gap-4 items-center">
      {/* Header row */}
      <span className="text-sm text-muted-foreground">Normal</span>
      <span className="text-sm text-muted-foreground">Disabled</span>
      <span className="text-sm text-muted-foreground">Loading</span>

      {/* Primary row */}
      <Button>Save</Button>
      <Button disabled>Save</Button>
      <Button loading>Saving...</Button>

      {/* Secondary row */}
      <Button variant="secondary">Cancel</Button>
      <Button variant="secondary" disabled>Cancel</Button>
      <Button variant="secondary" loading>Loading...</Button>
    </div>
  ),
}
```

### 3. Use Case Story

Show real-world usage patterns:

```tsx
/**
 * Common button patterns in real UI contexts.
 */
export const UseCases: Story = {
  render: () => (
    <div className="flex flex-col gap-6">
      {/* Form Actions */}
      <div className="flex gap-2 justify-end p-4 border border-border rounded-md">
        <Button variant="ghost">Cancel</Button>
        <Button variant="primary" iconBefore={<Save />}>
          Save Changes
        </Button>
      </div>

      {/* Destructive Action */}
      <div className="flex gap-2 p-4 border border-border rounded-md">
        <Button variant="destructive" iconBefore={<Trash2 />}>
          Delete Item
        </Button>
      </div>
    </div>
  ),
}
```

### 4. A11y Test Story (with play function)

Verify accessibility requirements:

```tsx
/**
 * Accessibility test: Verifies aria-label is properly set.
 */
export const A11yAriaLabel: Story = {
  args: {
    icon: <X />,
    "aria-label": "Close panel",
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const button = canvas.getByRole("button", { name: "Close panel" })
    await expect(button).toBeInTheDocument()
    await expect(button).toHaveAccessibleName("Close panel")
  },
}
```

## Story Organization

### Naming Convention

```
Components/
├── Button           # Component name
│   ├── Variants     # Visual showcase
│   ├── Sizes        # Size showcase
│   ├── States       # State matrix
│   ├── WithIcons    # Feature showcase
│   ├── UseCases     # Real-world examples
│   ├── A11yBasic    # A11y verification
│   └── A11yFocus    # A11y verification
```

### Story Order Priority

1. **Showcase stories first** - Visual comparison grids
2. **Feature stories** - Icons, loading, etc.
3. **Use case stories** - Real-world patterns
4. **A11y test stories** - Verification with play functions

## Meta Configuration

### Minimal argTypes

```tsx
const meta: Meta<typeof IconButton> = {
  title: "Components/IconButton",
  component: IconButton,
  parameters: {
    layout: "centered",
    docs: {
      description: {
        component: `Brief component description with key features.`,
      },
    },
  },
  argTypes: {
    // Only disable complex/function props
    icon: { control: false },
    onClick: { control: false },
    // Let simple props auto-generate controls
    variant: {
      control: "select",
      options: ["default", "ghost", "destructive"],
    },
  },
}
```

### Layout Parameters

| Layout | Use Case |
|--------|----------|
| `centered` | Single components, buttons, inputs |
| `padded` | Containers, cards, panels |
| `fullscreen` | Page layouts, full-width components |

## Play Function Patterns

### Role-Based Queries (Preferred)

```tsx
play: async ({ canvasElement }) => {
  const canvas = within(canvasElement)

  // ✅ Query by role
  const button = canvas.getByRole("button", { name: "Submit" })
  const input = canvas.getByRole("textbox", { name: "Email" })
  const menu = canvas.getByRole("menu")

  // ✅ Verify accessibility
  await expect(button).toHaveAccessibleName("Submit")
  await expect(button).not.toBeDisabled()
}
```

### User Interaction

```tsx
play: async ({ canvasElement }) => {
  const canvas = within(canvasElement)
  const user = userEvent.setup()

  const button = canvas.getByRole("button", { name: "Open menu" })
  await user.click(button)

  // Verify state change
  await expect(button).toHaveAttribute("aria-expanded", "true")

  const menu = canvas.getByRole("menu")
  await expect(menu).toBeInTheDocument()
}
```

### Focus Verification

```tsx
play: async ({ canvasElement }) => {
  const canvas = within(canvasElement)
  const button = canvas.getByRole("button")

  button.focus()
  await expect(button).toHaveFocus()
}
```

### Step Function for Complex Flows

Organize multi-step interactions for better debugging:

```tsx
import { step } from "@storybook/test"

play: async ({ canvasElement }) => {
  const canvas = within(canvasElement)
  const user = userEvent.setup()

  await step("Open the dialog", async () => {
    await user.click(canvas.getByRole("button", { name: "Settings" }))
    await expect(canvas.getByRole("dialog")).toBeInTheDocument()
  })

  await step("Fill in the form", async () => {
    await user.type(canvas.getByLabelText("Name"), "Test User")
    await user.selectOptions(canvas.getByLabelText("Theme"), "dark")
  })

  await step("Submit and verify", async () => {
    await user.click(canvas.getByRole("button", { name: "Save" }))
    await expect(canvas.getByText("Settings saved")).toBeInTheDocument()
  })
}
```

## A11y Testing Checklist

Each component should have stories verifying:

- [ ] `aria-label` / `aria-labelledby` for unlabeled elements
- [ ] `aria-expanded` for expandable elements
- [ ] `aria-pressed` for toggle buttons
- [ ] `aria-selected` for selectable items
- [ ] Focus visibility and keyboard navigation
- [ ] Role attributes (`button`, `menu`, `tab`, `tablist`, etc.)

---

## Form Component Story Patterns

### BorderRadiusCheck Story

Add a story using descender-heavy text (`"gggjjjyyyqqqppp"`) to verify text doesn't clip at rounded corners. Test all size variants.

### Recommended Stories for Form Components

`Sizes`, `States`, `WithLabel`, `BorderRadiusCheck`, `A11yWithLabel`, `A11yDisabled`, `A11yError`

## File Structure

```
packages/ui/
├── .storybook/
│   ├── main.ts          # Storybook config
│   ├── preview.ts       # Global decorators, a11y config
│   └── storybook.css    # Theme import + @source
├── src/
│   └── components/
│       ├── Button.tsx
│       ├── Button.stories.tsx
│       ├── IconButton.tsx
│       └── IconButton.stories.tsx
```

## Configuration

### main.ts

```ts
import type { StorybookConfig } from "@storybook/react-vite"
import tailwindcss from "@tailwindcss/vite"

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-vitest",  // Component testing
    "@storybook/addon-a11y",    // Accessibility panel
    "@storybook/addon-docs",    // Documentation
  ],
  framework: "@storybook/react-vite",
  async viteFinal(config) {
    config.plugins = config.plugins
      ? [...config.plugins, tailwindcss()]
      : [tailwindcss()]
    return config
  },
}
```

### preview.ts

```ts
import type { Preview } from "@storybook/react-vite"
import "./storybook.css"

const preview: Preview = {
  parameters: {
    a11y: {
      config: {
        rules: [
          { id: "color-contrast", enabled: true },
          { id: "aria-required-attr", enabled: true },
          { id: "button-name", enabled: true },
          { id: "label", enabled: true },
        ],
      },
    },
    docs: {
      toc: true,  // Table of contents in docs
    },
  },
}
```

### storybook.css

```css
@import "@internal/theme/index.css";

@source "../src/**/*.tsx";
```

## Anti-Patterns

### ❌ One story per variant

```tsx
// DON'T: Creates too many sidebar entries
export const Primary: Story = { args: { variant: "primary" } }
export const Secondary: Story = { args: { variant: "secondary" } }
export const Ghost: Story = { args: { variant: "ghost" } }
export const Destructive: Story = { args: { variant: "destructive" } }
```

### ✅ Single showcase story

```tsx
// DO: One story showing all variants
export const Variants: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-4">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="destructive">Destructive</Button>
    </div>
  ),
}
```

### ❌ Relying on Controls for documentation

```tsx
// DON'T: Users must interact with controls to see variants
export const Default: Story = {
  args: {
    variant: "primary",
    size: "md",
  },
}
```

### ✅ Visual documentation

```tsx
// DO: All variants visible at once
export const Sizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
}
```

## Portable Stories (Storybook 8+)

Use stories in external test runners:

```tsx
// Button.test.tsx
import { composeStories } from "@storybook/react"
import { render, screen } from "@testing-library/react"
import * as stories from "./Button.stories"

const { Primary, Disabled } = composeStories(stories)

test("renders primary button", () => {
  render(<Primary />)
  expect(screen.getByRole("button")).toBeInTheDocument()
})

test("disabled button is not interactive", () => {
  render(<Disabled />)
  expect(screen.getByRole("button")).toBeDisabled()
})
```

**Benefits:**
- Reuse stories in Vitest/Jest
- Single source of truth for component states
- Decorators and args automatically applied

## References

- [Storybook Documentation](https://storybook.js.org/docs)
- [Storybook Test Runner](https://storybook.js.org/docs/writing-tests/test-runner)
- [Portable Stories](https://storybook.js.org/docs/api/portable-stories)
