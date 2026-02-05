---
name: react-styling
description: Implement styling with Tailwind CSS, CSS Modules, and CSS-in-JS. Use when styling React components, implementing responsive design, dark mode, or managing dynamic styles.
---

# React Styling Specialist

Specialized in styling React applications using Tailwind CSS, CSS Modules, and CSS-in-JS libraries.

## When to Use This Skill

- Styling React components with Tailwind CSS
- Using CSS Modules for component-scoped styles
- Implementing CSS-in-JS with styled-components or Emotion
- Creating responsive designs
- Implementing dark mode and theming
- Managing dynamic className composition
- Building reusable style utilities

## Core Principles

- **Consistency**: Use design tokens and spacing scales
- **Responsive**: Mobile-first responsive design
- **Maintainable**: Component-scoped styles to avoid conflicts
- **Performance**: Optimize for production (purge unused CSS)
- **Accessible**: Ensure sufficient color contrast and focus states
- **Type-Safe**: Use TypeScript for theme and variant types

## Tailwind CSS

### Setup

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [],
}

export default config
```

### Basic Usage

```typescript
export const Button: FC<ButtonProps> = ({ children, variant = 'primary' }) => {
  return (
    <button
      className="px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
    >
      {children}
    </button>
  )
}
```

### Conditional Styling with clsx/cn

```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

// Utility to merge Tailwind classes
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  className?: string
  children: React.ReactNode
}

export const Button: FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  className,
  children,
}) => {
  return (
    <button
      disabled={disabled}
      className={cn(
        // Base styles
        'rounded-lg font-medium transition-colors focus:outline-none focus:ring-2',
        // Variant styles
        {
          'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500':
            variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500':
            variant === 'secondary',
          'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500':
            variant === 'danger',
        },
        // Size styles
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        // Disabled styles
        disabled && 'opacity-50 cursor-not-allowed',
        // Allow className override
        className
      )}
    >
      {children}
    </button>
  )
}

// Usage
<Button variant="primary" size="lg" className="w-full">
  Submit
</Button>
```

### Responsive Design

```typescript
export const Card: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div
      className={cn(
        // Mobile-first approach
        'p-4',
        // sm: 640px
        'sm:p-6',
        // md: 768px
        'md:p-8',
        // lg: 1024px
        'lg:p-10',
        // Grid layout
        'grid grid-cols-1 gap-4',
        'md:grid-cols-2',
        'lg:grid-cols-3'
      )}
    >
      {children}
    </div>
  )
}
```

### Dark Mode

```typescript
// tailwind.config.ts
const config: Config = {
  darkMode: 'class', // or 'media'
  // ...
}

// Component with dark mode
export const Card: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div
      className={cn(
        'p-6 rounded-lg border',
        // Light mode
        'bg-white border-gray-200 text-gray-900',
        // Dark mode
        'dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100'
      )}
    >
      {children}
    </div>
  )
}

// Dark mode toggle
'use client'

import { useTheme } from 'next-themes'

export const ThemeToggle: FC = () => {
  const { theme, setTheme } = useTheme()

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700"
    >
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>
  )
}
```

## CSS Modules

### Setup

CSS Modules work out of the box with Next.js. File naming: `Component.module.css`

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.primary:hover {
  background-color: #2563eb;
}

.secondary {
  background-color: #e5e7eb;
  color: #1f2937;
}

.secondary:hover {
  background-color: #d1d5db;
}

.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

```typescript
// Button.tsx
import styles from './Button.module.css'

interface ButtonProps {
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  children: React.ReactNode
}

export const Button: FC<ButtonProps> = ({
  variant = 'primary',
  disabled = false,
  children,
}) => {
  return (
    <button
      disabled={disabled}
      className={cn(
        styles.button,
        styles[variant],
        disabled && styles.disabled
      )}
    >
      {children}
    </button>
  )
}
```

### Composing Classes

```css
/* Card.module.css */
.card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.cardHeader {
  composes: card;
  background-color: #f9fafb;
}
```

## CSS-in-JS (styled-components / Emotion)

### styled-components

```typescript
import styled from 'styled-components'

// Styled component
const StyledButton = styled.button<{ variant: 'primary' | 'secondary' }>`
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
  border: none;
  cursor: pointer;

  ${props => props.variant === 'primary' && `
    background-color: #3b82f6;
    color: white;

    &:hover {
      background-color: #2563eb;
    }
  `}

  ${props => props.variant === 'secondary' && `
    background-color: #e5e7eb;
    color: #1f2937;

    &:hover {
      background-color: #d1d5db;
    }
  `}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`

interface ButtonProps {
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  children: React.ReactNode
}

export const Button: FC<ButtonProps> = ({
  variant = 'primary',
  disabled = false,
  children,
}) => {
  return (
    <StyledButton variant={variant} disabled={disabled}>
      {children}
    </StyledButton>
  )
}
```

### Theming with styled-components

```typescript
// theme.ts
export const lightTheme = {
  colors: {
    primary: '#3b82f6',
    background: '#ffffff',
    text: '#1f2937',
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
  },
}

export const darkTheme = {
  colors: {
    primary: '#60a5fa',
    background: '#1f2937',
    text: '#f9fafb',
  },
  spacing: lightTheme.spacing,
}

export type Theme = typeof lightTheme

// App.tsx
import { ThemeProvider } from 'styled-components'

export const App = () => {
  const [theme, setTheme] = useState(lightTheme)

  return (
    <ThemeProvider theme={theme}>
      <Dashboard />
    </ThemeProvider>
  )
}

// Component using theme
const Card = styled.div`
  background-color: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  padding: ${props => props.theme.spacing.lg};
  border-radius: 0.5rem;
`
```

## Design Patterns

### Variant-based Styling

```typescript
// Using cva (class-variance-authority) with Tailwind
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
        ghost: 'bg-transparent hover:bg-gray-100 text-gray-900',
      },
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-10 px-4 py-2',
        lg: 'h-11 px-8',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button: FC<ButtonProps> = ({
  className,
  variant,
  size,
  ...props
}) => {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}
```

### Layout Components

```typescript
// Stack (vertical layout)
export const Stack: FC<{
  gap?: 'sm' | 'md' | 'lg'
  children: ReactNode
}> = ({ gap = 'md', children }) => {
  return (
    <div
      className={cn('flex flex-col', {
        'gap-2': gap === 'sm',
        'gap-4': gap === 'md',
        'gap-6': gap === 'lg',
      })}
    >
      {children}
    </div>
  )
}

// Flex (horizontal layout)
export const Flex: FC<{
  gap?: 'sm' | 'md' | 'lg'
  justify?: 'start' | 'center' | 'end' | 'between'
  align?: 'start' | 'center' | 'end'
  children: ReactNode
}> = ({ gap = 'md', justify = 'start', align = 'start', children }) => {
  return (
    <div
      className={cn(
        'flex',
        {
          'gap-2': gap === 'sm',
          'gap-4': gap === 'md',
          'gap-6': gap === 'lg',
        },
        {
          'justify-start': justify === 'start',
          'justify-center': justify === 'center',
          'justify-end': justify === 'end',
          'justify-between': justify === 'between',
        },
        {
          'items-start': align === 'start',
          'items-center': align === 'center',
          'items-end': align === 'end',
        }
      )}
    >
      {children}
    </div>
  )
}
```

## Tools to Use

- `Read`: Read existing styled components
- `Write`: Create new styled components
- `Edit`: Modify styles
- `Bash`: Run dev server and build

### Bash Commands

```bash
# Development
npm run dev

# Build (purges unused CSS)
npm run build

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install clsx and tailwind-merge
npm install clsx tailwind-merge

# Install styled-components
npm install styled-components
npm install -D @types/styled-components
```

## Workflow

1. **Design System**: Define color palette, spacing, typography
2. **Choose Approach**: Select Tailwind, CSS Modules, or CSS-in-JS
3. **Write Tests**: Test component appearance and variants
4. **Implement Styles**: Create styled components
5. **Ensure Accessibility**: Check contrast, focus states
6. **Test Responsive**: Verify on different screen sizes
7. **Optimize**: Purge unused CSS in production
8. **Commit**: Create atomic commit

## Related Skills

- `react-component-development`: For component implementation
- `nextjs-optimization`: For CSS optimization
- `vitest-react-testing`: For testing styled components

## Coding Standards

See [React Coding Standards](../_shared/react-coding-standards.md)

## Key Reminders

- Use design tokens for consistency (colors, spacing, typography)
- Implement mobile-first responsive design
- Ensure color contrast meets WCAG standards
- Provide focus states for keyboard navigation
- Use Tailwind's purge in production to remove unused CSS
- Prefer composition over duplication
- Use TypeScript for variant and theme types
- Test dark mode implementation
- Optimize for performance (minimize CSS bundle size)
- Keep styles close to components (co-location)
- Use semantic class names with CSS Modules
- Document design system tokens
- Write comments explaining WHY for complex styles
