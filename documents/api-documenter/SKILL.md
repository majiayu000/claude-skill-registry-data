---
name: api-documenter
description: |
  WHEN: API documentation, JSDoc/TSDoc comments, Props documentation, Storybook story writing
  WHAT: Function/class/type JSDoc + React Props table + Markdown API docs + Storybook stories
  WHEN NOT: README writing → readme-generator, Code explanation → code-reviewer
---

# API Documenter Skill

## Purpose
Automatically generates API documentation for code including functions, components, and types with JSDoc/TSDoc comments.

## When to Use
- "API docs", "jsdoc", "documentation" requests
- Component Props documentation needed
- Adding comments to functions/classes
- Storybook story generation

## Workflow

### Step 1: Select Documentation Target
**AskUserQuestion:**
```
"What code to document?"
Options:
- Specific file/function
- Undocumented export functions
- React component Props
- All public APIs
```

### Step 2: Select Documentation Type
**AskUserQuestion:**
```
"What format to generate?"
Options:
- JSDoc/TSDoc comments
- Markdown API docs
- Storybook stories
- All of the above
multiSelect: true
```

## Documentation Templates

### JSDoc/TSDoc Comments

**Function:**
```typescript
/**
 * Formats user data for display.
 *
 * @param user - User object to format
 * @param options - Formatting options
 * @param options.locale - Locale setting (default: 'en-US')
 * @param options.includeAge - Include age (default: false)
 *
 * @returns Formatted user string
 *
 * @example
 * ```typescript
 * const formatted = formatUser({ name: 'John', age: 30 })
 * // Returns: 'John'
 *
 * const withAge = formatUser({ name: 'John', age: 30 }, { includeAge: true })
 * // Returns: 'John (30)'
 * ```
 *
 * @throws {ValidationError} When user object is invalid
 * @see {@link User} User type definition
 * @since 1.0.0
 */
export function formatUser(user: User, options?: FormatOptions): string
```

**Interface:**
```typescript
/**
 * User information interface
 *
 * @interface User
 * @property {string} id - Unique identifier (UUID)
 * @property {string} name - User name
 * @property {string} email - Email address
 * @property {number} [age] - Age (optional)
 * @property {UserRole} role - User role
 */
interface User {
  id: string
  name: string
  email: string
  age?: number
  role: UserRole
}
```

**Class:**
```typescript
/**
 * API client for REST communication
 *
 * @class ApiClient
 * @example
 * ```typescript
 * const client = new ApiClient({ baseUrl: 'https://api.example.com' })
 * const users = await client.get<User[]>('/users')
 * ```
 */
class ApiClient {
  /**
   * Creates ApiClient instance
   * @param config - Client configuration
   */
  constructor(config: ApiClientConfig) {}

  /**
   * Performs GET request
   * @template T - Response type
   * @param endpoint - API endpoint
   * @returns Response data
   */
  async get<T>(endpoint: string): Promise<T> {}
}
```

### React Component Documentation

**Props Interface:**
```typescript
/**
 * Button component Props
 */
interface ButtonProps {
  /** Button content */
  children: React.ReactNode

  /** Style variant @default 'primary' */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'

  /** Button size @default 'medium' */
  size?: 'small' | 'medium' | 'large'

  /** Disabled state @default false */
  disabled?: boolean

  /** Loading state @default false */
  loading?: boolean

  /** Click event handler */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void
}

/**
 * Button component with various styles and sizes
 *
 * @component
 * @example
 * ```tsx
 * <Button onClick={handleClick}>Click me</Button>
 * <Button variant="secondary" size="large">Large Button</Button>
 * <Button loading disabled>Processing...</Button>
 * ```
 */
export function Button({ children, variant = 'primary', ...props }: ButtonProps)
```

### Markdown API Docs
```markdown
## formatUser

Formats user data for display.

### Signature
\`\`\`typescript
function formatUser(user: User, options?: FormatOptions): string
\`\`\`

### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `user` | `User` | Yes | - | User object to format |
| `options.locale` | `string` | No | `'en-US'` | Locale setting |

### Returns
`string` - Formatted user string

### Example
\`\`\`typescript
const formatted = formatUser({ name: 'John', age: 30 })
\`\`\`
```

### Storybook Stories
```typescript
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
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
    },
  },
}

export default meta
type Story = StoryObj<typeof Button>

/** Default button style */
export const Default: Story = {
  args: { children: 'Button', variant: 'primary' },
}

/** Primary variant for main actions */
export const Primary: Story = {
  args: { children: 'Primary', variant: 'primary' },
}

/** Various sizes */
export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button size="small">Small</Button>
      <Button size="medium">Medium</Button>
      <Button size="large">Large</Button>
    </div>
  ),
}
```

## Response Template
```
## API Documentation Generated

**Target**: src/components/Button.tsx

### JSDoc Comments
- ButtonProps interface: 7 properties documented
- Button component: Fully documented

### Markdown Docs
- File: docs/components/Button.md
- Sections: Props, Usage, Accessibility

### Storybook
- File: src/components/Button.stories.tsx
- Stories: 6 (Default, Primary, Secondary, Sizes, Loading, Disabled)

### Statistics
| Item | Count |
|------|-------|
| Documented Props | 7 |
| Code Examples | 5 |
| Stories | 6 |
```

## Best Practices
1. **Consistent Style**: Same documentation style across project
2. **Include Examples**: Usage examples for all public APIs
3. **Type Accuracy**: Match TypeScript types with documentation
4. **Keep Updated**: Update docs when code changes
5. **Accessibility Info**: Include a11y information for components

## Integration
- `readme-generator` skill: README API section
- `/explain-code` command: Code understanding
- `code-reviewer` skill: Documentation quality check

## Notes
- Merges or overwrites if existing docs present
- Auto-infers from TypeScript types
- Excludes @internal tagged code
