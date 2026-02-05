---
name: storybook-development
description: Create component documentation and testing with Storybook using CSF3, interaction testing, and visual regression. Use when documenting components, creating UI catalog, or visual testing.
---

# Storybook Development Specialist

Specialized in creating component documentation and visual testing with Storybook.

## When to Use This Skill

- Documenting React components
- Creating component UI catalog
- Visual regression testing
- Component-driven development
- Testing component variants and states
- Sharing component library with team
- Testing interaction and accessibility

## Core Principles

- **Component Isolation**: Test components in isolation
- **Visual Documentation**: Show all component states
- **Interactive**: Allow props manipulation with controls
- **Accessible**: Document accessibility features
- **Testable**: Include interaction tests
- **Discoverable**: Organize stories logically

## Storybook Setup

```bash
# Initialize Storybook with Vite
npx storybook@latest init --builder vite

# Install additional addons
npm install -D @storybook/addon-a11y
npm install -D @storybook/test
```

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
}

export default config
```

## CSF3 Stories

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

// Meta configuration
const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
    },
  },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

// Stories
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Button',
  },
}

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large Button',
  },
}

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button',
  },
}
```

## Args and Controls

```typescript
// Card.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Card } from './Card'

const meta = {
  title: 'Components/Card',
  component: Card,
  args: {
    // Default args for all stories
    title: 'Card Title',
    description: 'Card description goes here',
  },
  argTypes: {
    title: {
      control: 'text',
      description: 'The card title',
    },
    description: {
      control: 'text',
      description: 'The card description',
    },
    variant: {
      control: 'select',
      options: ['default', 'highlighted', 'muted'],
      description: 'Visual variant of the card',
    },
    onClick: { action: 'clicked' },
  },
} satisfies Meta<typeof Card>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const Highlighted: Story = {
  args: {
    variant: 'highlighted',
    title: 'Highlighted Card',
  },
}

export const WithLongContent: Story = {
  args: {
    title: 'Long Content Card',
    description:
      'This is a very long description that demonstrates how the card handles lengthy content. ' +
      'It should wrap properly and maintain good readability.',
  },
}
```

## Decorators

```typescript
// Global decorator (.storybook/preview.tsx)
import React from 'react'
import type { Preview } from '@storybook/react'
import { ThemeProvider } from '../src/contexts/ThemeProvider'

const preview: Preview = {
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div style={{ padding: '3rem' }}>
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
  },
}

export default preview

// Story-specific decorator
export const DarkMode: Story = {
  decorators: [
    (Story) => (
      <div className="dark" style={{ background: '#1a1a1a', padding: '2rem' }}>
        <Story />
      </div>
    ),
  ],
  args: {
    children: 'Dark Mode Button',
  },
}
```

## Interaction Testing

```typescript
import { expect, userEvent, within } from '@storybook/test'
import type { Meta, StoryObj } from '@storybook/react'
import { LoginForm } from './LoginForm'

const meta = {
  title: 'Forms/LoginForm',
  component: LoginForm,
} satisfies Meta<typeof LoginForm>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const FilledForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)

    // WHY: Simulate user filling out the form
    await userEvent.type(canvas.getByLabelText('Email'), 'user@example.com')
    await userEvent.type(canvas.getByLabelText('Password'), 'password123')

    await expect(canvas.getByLabelText('Email')).toHaveValue('user@example.com')
  },
}

export const SubmitForm: Story = {
  args: {
    onSubmit: async (data) => {
      console.log('Form submitted:', data)
    },
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement)

    await userEvent.type(canvas.getByLabelText('Email'), 'user@example.com')
    await userEvent.type(canvas.getByLabelText('Password'), 'password123')
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }))

    // Verify submission was called
    await expect(args.onSubmit).toHaveBeenCalled()
  },
}

export const ValidationErrors: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)

    // Submit without filling
    await userEvent.click(canvas.getByRole('button', { name: /submit/i }))

    // Check for validation errors
    await expect(canvas.getByText(/email is required/i)).toBeInTheDocument()
    await expect(canvas.getByText(/password is required/i)).toBeInTheDocument()
  },
}
```

## Parameters

```typescript
export const Centered: Story = {
  parameters: {
    layout: 'centered', // Center in canvas
  },
}

export const FullWidth: Story = {
  parameters: {
    layout: 'fullscreen', // Full viewport
  },
}

export const CustomBackground: Story = {
  parameters: {
    backgrounds: {
      default: 'dark',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
      ],
    },
  },
}

export const WithViewport: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
}
```

## Documenting with MDX

```mdx
<!-- Button.stories.mdx -->
import { Canvas, Meta, Story } from '@storybook/blocks'
import * as ButtonStories from './Button.stories'

<Meta of={ButtonStories} />

# Button

The Button component is a versatile UI element used for user interactions.

## Usage

```tsx
import { Button } from '@/components/Button'

<Button variant="primary">Click me</Button>
```

## Variants

<Canvas of={ButtonStories.Primary} />
<Canvas of={ButtonStories.Secondary} />
<Canvas of={ButtonStories.Danger} />

## Sizes

<Canvas of={ButtonStories.Small} />
<Canvas of={ButtonStories.Medium} />
<Canvas of={ButtonStories.Large} />

## Props

<ArgTypes of={Button} />
```

## Visual Regression Testing

```typescript
// Button.stories.tsx
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="danger">Danger</Button>
      <Button variant="primary" disabled>
        Disabled
      </Button>
    </div>
  ),
  parameters: {
    // Configure for visual regression
    chromatic: {
      viewports: [320, 1200],
    },
  },
}

// Disable snapshots for interactive stories
export const Interactive: Story = {
  parameters: {
    chromatic: { disableSnapshot: true },
  },
}
```

## Accessibility Testing

```typescript
// .storybook/preview.tsx
const preview: Preview = {
  parameters: {
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
        ],
      },
    },
  },
}

// Story with specific a11y parameters
export const HighContrast: Story = {
  parameters: {
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
            options: { level: 'AAA' },
          },
        ],
      },
    },
  },
}
```

## Component Variants Pattern

```typescript
// Showing all component states
export const AllStates: Story = {
  render: () => (
    <div style={{ display: 'grid', gap: '2rem' }}>
      <div>
        <h3>Default</h3>
        <Input placeholder="Enter text" />
      </div>
      <div>
        <h3>With Value</h3>
        <Input value="Sample text" />
      </div>
      <div>
        <h3>Disabled</h3>
        <Input disabled placeholder="Disabled input" />
      </div>
      <div>
        <h3>Error</h3>
        <Input error="This field is required" placeholder="Error state" />
      </div>
      <div>
        <h3>Loading</h3>
        <Input loading placeholder="Loading..." />
      </div>
    </div>
  ),
}
```

## Mocking Data

```typescript
import { http, HttpResponse } from 'msw'

export const WithMockedData: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get('/api/users', () => {
          return HttpResponse.json([
            { id: '1', name: 'John Doe' },
            { id: '2', name: 'Jane Smith' },
          ])
        }),
      ],
    },
  },
}
```

## Addon Integration

```typescript
// .storybook/main.ts
const config: StorybookConfig = {
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials', // Essential addons
    '@storybook/addon-interactions', // Interaction testing
    '@storybook/addon-a11y', // Accessibility testing
    '@storybook/addon-coverage', // Code coverage
  ],
}
```

## Tools to Use

- `Read`: Read component code
- `Write`: Create story files
- `Edit`: Update stories
- `Bash`: Run Storybook and build

### Bash Commands

```bash
# Run Storybook
npm run storybook

# Build Storybook
npm run build-storybook

# Run interaction tests
npm run test-storybook

# Run with coverage
npm run test-storybook -- --coverage

# Build and deploy
npm run build-storybook && npx http-server storybook-static
```

## Workflow

1. **Create Component**: Build React component
2. **Write Story**: Create `.stories.tsx` file
3. **Add Variants**: Document all component states
4. **Add Controls**: Configure argTypes for interactivity
5. **Add Interactions**: Test user interactions
6. **Test Accessibility**: Use a11y addon
7. **Visual Regression**: Integrate Chromatic
8. **Document**: Add MDX documentation
9. **Share**: Build and deploy Storybook

## Related Skills

- `react-component-development`: For component implementation
- `vitest-react-testing`: For unit tests
- `react-styling`: For component styling
- `playwright-testing`: For E2E tests

## Coding Standards

See [React Coding Standards](../_shared/react-coding-standards.md)

## Key Reminders

- Use CSF3 format for stories (modern, type-safe)
- Document all component variants and states
- Use Controls for interactive props
- Implement interaction tests with `play` function
- Use decorators for global wrappers (themes, providers)
- Configure parameters for layout, backgrounds, viewports
- Enable autodocs with `tags: ['autodocs']`
- Test accessibility with a11y addon
- Use MSW for mocking API requests
- Organize stories with clear hierarchy (title)
- Keep stories focused on single component
- Show realistic usage examples
- Test dark mode and responsive variants
- Integrate visual regression testing (Chromatic)
- Write comments explaining WHY for complex story setup
