---
name: Storybook Patterns
description: Component documentation, visual testing, interaction testing
---

# Storybook Development Patterns

Component development and documentation with Storybook 7+.

## Story Basics

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  title: 'UI/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    backgroundColor: { control: 'color' },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// Primary story
export const Primary: Story = {
  args: {
    primary: true,
    label: 'Button',
  },
};

// Secondary story
export const Secondary: Story = {
  args: {
    label: 'Button',
  },
};

// Large button
export const Large: Story = {
  args: {
    size: 'large',
    label: 'Button',
  },
};
```

## Args and Controls

```typescript
const meta = {
  component: Button,
  args: {
    // Default args for all stories
    label: 'Click me',
    variant: 'primary'
  },
  argTypes: {
    // Control types
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'tertiary'],
    },
    size: {
      control: { type: 'radio' },
      options: ['small', 'medium', 'large'],
    },
    disabled: {
      control: 'boolean',
    },
    onClick: { action: 'clicked' },
  },
} satisfies Meta<typeof Button>;
```

## Decorators

```typescript
// Global decorator
export const decorators = [
  (Story) => (
    <div style={{ margin: '3em' }}>
      <Story />
    </div>
  ),
];

// Component-level decorator
const meta = {
  component: Button,
  decorators: [
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
  ],
};
```

## Play Functions (Interaction Testing)

```typescript
import { within, userEvent, expect } from '@storybook/test';

export const FillForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Find form elements
    const emailInput = canvas.getByLabelText('Email');
    const passwordInput = canvas.getByLabelText('Password');
    const submitButton = canvas.getByRole('button');

    // Interact
    await userEvent.type(emailInput, 'user@example.com');
    await userEvent.type(passwordInput, 'password123');
    await userEvent.click(submitButton);

    // Assert
    await expect(canvas.getByText('Success')).toBeInTheDocument();
  },
};
```

## Visual Testing

### Snapshot Tests

```typescript
export const AllStates: Story = {
  render: () => (
    <div>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button disabled>Disabled</Button>
    </div>
  ),
};
```

### Responsive Testing

```typescript
export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};

export const Tablet: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'tablet',
    },
  },
};
```

## Documentation

### MDX Stories

```mdx
import { Meta, Story, Canvas } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

Buttons allow users to take actions.

<Canvas of={ButtonStories.Primary} />

## Usage

```tsx
import { Button } from './Button';

<Button variant="primary">Click me</Button>
```

## Variants

<Canvas of={ButtonStories.Secondary} />
<Canvas of={ButtonStories.Tertiary} />
```

### Auto-generated Docs

```typescript
const meta = {
  component: Button,
  tags: ['autodocs'], // Auto-generate docs page
  parameters: {
    docs: {
      description: {
        component: 'A versatile button component',
      },
    },
  },
};
```

## Loaders

```typescript
export const WithData: Story = {
  loaders: [
    async () => ({
      user: await fetchUser(),
    }),
  ],
  render: (args, { loaded: { user } }) => (
    <UserProfile user={user} />
  ),
};
```

## Best Practices

✅ **Do**:
- Write stories for all component states
- Use args for interactive controls
- Document usage with MDX
- Test interactions with play functions
- Use decorators for common wrappers
- Keep stories focused and simple

❌ **Don't**:
- Put business logic in stories
- Duplicate setup across stories
- Skip edge cases and error states
- Forget responsive variants
- Ignore accessibility testing
