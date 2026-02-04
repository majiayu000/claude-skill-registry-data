---
name: component-documenter
description: Write professional documentation including README files, Storybook stories, API docs, usage examples, and migration guides for component libraries
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Component Documenter

Expert skill for creating comprehensive, user-friendly documentation for component libraries. Specializes in README files, Storybook stories, API documentation, usage guides, and migration documentation.

## Core Capabilities

### 1. README Documentation
- Professional project overview
- Installation instructions
- Quick start guides
- Feature highlights
- Usage examples
- Configuration options
- Contributing guidelines
- Troubleshooting sections

### 2. Storybook Integration
- Story creation for all components
- Controls/Args documentation
- Multiple story variants
- Interactive examples
- MDX documentation pages
- Accessibility addon integration
- Visual regression testing setup

### 3. API Documentation
- Props interface documentation
- Type definitions
- Method signatures
- Event handlers
- Return types
- Default values
- Required vs optional props

### 4. Usage Guides
- Getting started tutorials
- Common use cases
- Best practices
- Code examples
- Do's and Don'ts
- Accessibility guidelines
- Performance tips

### 5. Migration Guides
- Version upgrade guides
- Breaking changes documentation
- Migration steps
- Codemod scripts
- Before/after examples
- Deprecation notices

### 6. Component Examples
- Basic usage examples
- Advanced patterns
- Edge case handling
- Integration examples
- Real-world scenarios
- Interactive demos

## Workflow

### Phase 1: Documentation Planning
1. **Understand Audience**
   - Developers using the library
   - Contributors to the project
   - Designers implementing specs
   - Stakeholders reviewing features

2. **Identify Content Needs**
   - What needs documentation?
   - What's missing in current docs?
   - Common questions/issues
   - User pain points

3. **Choose Documentation Types**
   - README for project overview
   - Storybook for component demos
   - JSDoc for inline code docs
   - Markdown files for guides
   - TypeScript for type docs

### Phase 2: Writing Documentation
1. **Create README**
   - Clear project description
   - Installation steps
   - Quick start example
   - Links to detailed docs

2. **Write Storybook Stories**
   - Default story for each component
   - Variant stories (sizes, colors, states)
   - Interactive controls
   - Accessibility checks

3. **Document API**
   - Props with types
   - Usage examples
   - Edge cases
   - Return values

4. **Create Usage Guides**
   - Step-by-step tutorials
   - Common patterns
   - Integration examples
   - Best practices

### Phase 3: Maintenance
1. **Keep Updated**
   - Update with code changes
   - Add new examples
   - Document breaking changes
   - Fix outdated content

2. **Gather Feedback**
   - User questions
   - GitHub issues
   - Support requests
   - Usage analytics

3. **Continuous Improvement**
   - Add missing examples
   - Clarify confusing sections
   - Improve searchability
   - Update screenshots

## README Templates

### Library README
```markdown
# @myorg/ui-library

Modern React component library with TypeScript, Tailwind CSS, and full accessibility support.

[![npm version](https://badge.fury.io/js/%40myorg%2Fui-library.svg)](https://www.npmjs.com/package/@myorg/ui-library)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🎨 **50+ Components** - Buttons, inputs, modals, and more
- 🎯 **TypeScript First** - Full type safety out of the box
- ♿ **Accessible** - WCAG AA compliant, keyboard navigation
- 🌗 **Dark Mode** - Built-in theming system
- 📦 **Tree-shakeable** - Import only what you need
- 🎭 **Customizable** - Tailwind CSS and CSS variables
- 📱 **Responsive** - Mobile-first design

## Installation

```bash
npm install @myorg/ui-library
```

## Quick Start

```tsx
import { Button, Input } from '@myorg/ui-library'
import '@myorg/ui-library/styles.css'

function App() {
  return (
    <div>
      <Button variant="primary">Click me</Button>
      <Input placeholder="Enter text..." />
    </div>
  )
}
```

## Documentation

- 📚 [Full Documentation](https://ui-library.myorg.com)
- 🎨 [Storybook](https://storybook.ui-library.myorg.com)
- 📝 [API Reference](https://ui-library.myorg.com/api)
- 🚀 [Examples](https://github.com/myorg/ui-library/tree/main/examples)

## Components

### Form Components
- [Button](https://ui-library.myorg.com/button) - Buttons in various styles
- [Input](https://ui-library.myorg.com/input) - Text inputs with validation
- [Select](https://ui-library.myorg.com/select) - Dropdown selection
- [Checkbox](https://ui-library.myorg.com/checkbox) - Checkbox input

### Layout Components
- [Card](https://ui-library.myorg.com/card) - Content container
- [Stack](https://ui-library.myorg.com/stack) - Flexbox layout
- [Grid](https://ui-library.myorg.com/grid) - Grid layout

### Feedback Components
- [Alert](https://ui-library.myorg.com/alert) - Alert messages
- [Toast](https://ui-library.myorg.com/toast) - Toast notifications
- [Modal](https://ui-library.myorg.com/modal) - Modal dialogs

## Usage

### Basic Example

```tsx
import { Button } from '@myorg/ui-library'

function MyComponent() {
  return (
    <Button
      variant="primary"
      size="lg"
      onClick={() => console.log('Clicked!')}
    >
      Click me
    </Button>
  )
}
```

### With TypeScript

```tsx
import { Button, type ButtonProps } from '@myorg/ui-library'

interface MyButtonProps extends ButtonProps {
  customProp?: string
}

function MyButton({ customProp, ...props }: MyButtonProps) {
  return <Button {...props} />
}
```

### Theming

```tsx
import { ThemeProvider } from '@myorg/ui-library'

function App() {
  return (
    <ThemeProvider theme="dark">
      <YourApp />
    </ThemeProvider>
  )
}
```

## Configuration

### Tailwind CSS

Add to your `tailwind.config.js`:

```js
module.exports = {
  content: [
    './node_modules/@myorg/ui-library/dist/**/*.{js,ts,jsx,tsx}',
  ],
  presets: [
    require('@myorg/ui-library/tailwind-preset')
  ],
}
```

### CSS Variables

Customize colors in your CSS:

```css
:root {
  --color-primary: 59 130 246;
  --color-secondary: 139 92 246;
  --radius: 0.5rem;
}
```

## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © [Your Organization](https://myorg.com)

## Credits

Built with:
- [React](https://react.dev)
- [TypeScript](https://www.typescriptlang.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Radix UI](https://www.radix-ui.com)
```

### Component README
```markdown
# Button

Versatile button component with multiple variants, sizes, and states.

## Import

```tsx
import { Button } from '@myorg/ui-library'
```

## Usage

```tsx
<Button variant="primary" size="md">
  Click me
</Button>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'outline' \| 'ghost'` | `'primary'` | Visual style variant |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `disabled` | `boolean` | `false` | Disables button |
| `loading` | `boolean` | `false` | Shows loading state |
| `onClick` | `(e: MouseEvent) => void` | - | Click handler |
| `children` | `ReactNode` | - | Button content |

## Examples

### Variants

```tsx
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
```

### Sizes

```tsx
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
```

### States

```tsx
<Button disabled>Disabled</Button>
<Button loading>Loading</Button>
```

### With Icons

```tsx
<Button>
  <Icon name="plus" />
  Add Item
</Button>
```

## Accessibility

- Uses semantic `<button>` element
- Keyboard accessible (Enter, Space)
- Focus visible indicator
- Disabled state prevents interaction
- ARIA attributes when needed

## Best Practices

✅ **Do:**
- Use semantic variants (primary for main action)
- Provide clear button text
- Use loading state for async actions
- Add icons for clarity when helpful

❌ **Don't:**
- Use too many primary buttons on one page
- Make buttons too small (min 44x44px)
- Use only icons without labels for important actions
- Nest interactive elements inside buttons
```

## Storybook Stories

### Basic Component Story
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost'],
      description: 'Visual style variant',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    disabled: {
      control: 'boolean',
    },
    onClick: { action: 'clicked' },
  },
}

export default meta
type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
  },
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
}

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
}

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <PlusIcon />
        Add Item
      </>
    ),
  },
}

export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...',
  },
}

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
}
```

### MDX Documentation Story
```mdx
{/* Button.mdx */}
import { Meta, Story, Canvas, Controls } from '@storybook/blocks'
import * as ButtonStories from './Button.stories'

<Meta of={ButtonStories} />

# Button

Versatile button component for user interactions.

## Overview

The Button component provides a consistent way to trigger actions throughout your application. It supports multiple variants, sizes, and states.

<Canvas of={ButtonStories.Primary} />

## Props

<Controls />

## Variants

Buttons come in four visual styles to indicate different levels of emphasis.

### Primary

Use for the main call-to-action on a page.

<Canvas of={ButtonStories.Primary} />

### Secondary

Use for secondary actions that complement the primary action.

<Canvas of={ButtonStories.Secondary} />

### Outline

Use for tertiary actions or to reduce visual weight.

<Canvas of={ButtonStories.Outline} />

### Ghost

Use for the least visual weight, often in toolbars or menus.

<Canvas of={ButtonStories.Ghost} />

## Sizes

Three sizes are available to fit different contexts.

<Canvas of={ButtonStories.Sizes} />

## States

### Loading

Shows a spinner when an async action is in progress.

<Canvas of={ButtonStories.Loading} />

### Disabled

Prevents interaction when an action is not available.

<Canvas of={ButtonStories.Disabled} />

## With Icons

Icons can be added to provide visual clarity.

<Canvas of={ButtonStories.WithIcon} />

## Accessibility

- Keyboard accessible with Enter and Space keys
- Focus indicator visible
- Disabled state properly communicated to screen readers
- Loading state announced to screen readers

## Best Practices

### ✅ Do

- Use primary buttons for main actions
- Keep button text concise (2-4 words)
- Use loading state for async actions
- Ensure minimum touch target size (44x44px)

### ❌ Don't

- Use too many primary buttons
- Use ambiguous labels like "Click here"
- Nest interactive elements
- Make buttons too small

## Examples

### Form Submission

```tsx
function Form() {
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    await submitForm()
    setLoading(false)
  }

  return (
    <Button
      variant="primary"
      loading={loading}
      onClick={handleSubmit}
    >
      Submit
    </Button>
  )
}
```

### Button Group

```tsx
<div className="flex gap-2">
  <Button variant="primary">Save</Button>
  <Button variant="outline">Cancel</Button>
</div>
```
```

### Storybook Configuration
```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y', // Accessibility addon
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

## API Documentation

### JSDoc Comments
```typescript
/**
 * Button component for user interactions.
 *
 * @example
 * ```tsx
 * <Button variant="primary" onClick={() => alert('Clicked!')}>
 *   Click me
 * </Button>
 * ```
 */
export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Visual style variant
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'

  /**
   * Button size
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg'

  /**
   * Disables the button and prevents interaction
   * @default false
   */
  disabled?: boolean

  /**
   * Shows loading spinner and disables interaction
   * @default false
   */
  loading?: boolean

  /**
   * Button content
   */
  children: ReactNode

  /**
   * Click event handler
   */
  onClick?: (event: MouseEvent<HTMLButtonElement>) => void
}
```

### TypeDoc Generation
```json
// typedoc.json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "plugin": ["typedoc-plugin-markdown"],
  "excludePrivate": true,
  "excludeProtected": true,
  "excludeExternals": true,
  "readme": "README.md",
  "categorizeByGroup": true,
  "categoryOrder": [
    "Components",
    "Hooks",
    "Utilities",
    "Types"
  ]
}
```

## Migration Guides

### Version Upgrade Guide
```markdown
# Migration Guide: v1.x to v2.0

## Breaking Changes

### 1. Button Component

#### Removed `color` prop

The `color` prop has been replaced with `variant` for clearer semantics.

**Before (v1.x):**
```tsx
<Button color="blue">Click me</Button>
```

**After (v2.0):**
```tsx
<Button variant="primary">Click me</Button>
```

#### Renamed `isLoading` to `loading`

For consistency across components.

**Before:**
```tsx
<Button isLoading>Submit</Button>
```

**After:**
```tsx
<Button loading>Submit</Button>
```

### 2. Input Component

#### Changed validation prop structure

Validation props are now grouped in a single `validation` object.

**Before:**
```tsx
<Input required error="Required field" />
```

**After:**
```tsx
<Input validation={{ required: true, error: "Required field" }} />
```

## New Features

### ThemeProvider

v2.0 introduces a new theming system with light/dark mode support.

```tsx
import { ThemeProvider } from '@myorg/ui-library'

function App() {
  return (
    <ThemeProvider>
      <YourApp />
    </ThemeProvider>
  )
}
```

### Compound Components

Many components now support compound component patterns.

```tsx
<Select>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Content>
    <Select.Item value="1">Option 1</Select.Item>
    <Select.Item value="2">Option 2</Select.Item>
  </Select.Content>
</Select>
```

## Deprecations

### Alert Component

The `type` prop is deprecated in favor of `variant`.

```tsx
// Deprecated (still works but will warn)
<Alert type="error">Error message</Alert>

// Recommended
<Alert variant="error">Error message</Alert>
```

## Automated Migration

We provide a codemod to automate most changes:

```bash
npx @myorg/ui-library-codemod v1-to-v2 src/
```

## Step-by-Step Migration

1. **Update package version**
   ```bash
   npm install @myorg/ui-library@2.0.0
   ```

2. **Run codemod**
   ```bash
   npx @myorg/ui-library-codemod v1-to-v2 src/
   ```

3. **Review changes**
   - Check git diff
   - Test your application
   - Fix any remaining issues

4. **Update imports** (if needed)
   ```tsx
   // Some components moved
   import { Toast } from '@myorg/ui-library/feedback'
   ```

5. **Test thoroughly**
   - Run your test suite
   - Manual QA testing
   - Check for console warnings

## Need Help?

- 📖 [Full documentation](https://ui-library.myorg.com)
- 💬 [GitHub Discussions](https://github.com/myorg/ui-library/discussions)
- 🐛 [Report issues](https://github.com/myorg/ui-library/issues)
```

## Documentation Best Practices

### Writing Style
1. **Clear and Concise**: Use simple language
2. **Examples First**: Show code before explaining
3. **Progressive Disclosure**: Basic → Advanced
4. **Consistent Formatting**: Use same patterns
5. **Scannable**: Use headings, lists, tables

### Content Structure
1. **Start with Why**: Explain purpose
2. **Quick Start**: Get users running fast
3. **Common Use Cases**: Cover 80% of usage
4. **API Reference**: Complete prop documentation
5. **Troubleshooting**: Address common issues

### Code Examples
1. **Complete**: Copy-paste ready
2. **Realistic**: Real-world scenarios
3. **Commented**: Explain non-obvious parts
4. **TypeScript**: Show type usage
5. **Tested**: Ensure examples work

### Accessibility
1. **Document a11y Features**: Keyboard, screen readers
2. **Provide Guidelines**: How to use accessibly
3. **Include ARIA**: Document ARIA usage
4. **Test Instructions**: How to verify a11y

### Maintenance
1. **Keep Updated**: Update with code changes
2. **Version Docs**: Document per version
3. **Deprecation Warnings**: Clear migration paths
4. **Changelog**: Track all changes
5. **Feedback Loop**: Improve based on questions

## Tools & Resources

### Documentation Tools
- **Storybook**: Component development and docs
- **TypeDoc**: Generate API docs from TypeScript
- **Docusaurus**: Documentation website builder
- **VitePress**: Fast static site generator
- **Markdoc**: Markdown-based documentation

### Storybook Addons
- **@storybook/addon-a11y**: Accessibility testing
- **@storybook/addon-essentials**: Core addons
- **@storybook/addon-interactions**: Test interactions
- **@storybook/addon-links**: Link stories
- **storybook-dark-mode**: Dark mode toggle

### Writing Tools
- **Grammarly**: Grammar checking
- **Hemingway**: Readability improvement
- **Vale**: Prose linting
- **markdownlint**: Markdown linting

## When to Use This Skill

Activate this skill when you need to:
- Write or update README files
- Create Storybook stories
- Generate API documentation
- Write usage guides
- Create migration guides
- Document component props
- Write tutorials
- Create examples
- Set up documentation site
- Improve existing docs
- Write contributing guidelines

## Output Format

When creating documentation, provide:
1. **Complete Documentation**: README, stories, guides
2. **Code Examples**: Working, tested examples
3. **Screenshots**: Visual aids where helpful
4. **Links**: Cross-references to related docs
5. **Metadata**: Version, last updated, authors
6. **Next Steps**: What to read next

Always prioritize clarity, completeness, and accessibility in documentation.
