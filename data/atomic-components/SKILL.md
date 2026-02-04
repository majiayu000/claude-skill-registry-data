---
name: atomic-components
description: Create atomic components (atoms) - basic, reusable UI building blocks following React/TypeScript best practices with Tailwind v4 styling. Use when creating fundamental UI elements like buttons, inputs, labels, icons, or other single-responsibility components. Triggers on requests like "create a button component", "add an input atom", "build a reusable icon wrapper", or "create atomic UI elements".
---

# Atomic Components

Create atomic components (atoms) - the fundamental building blocks of your UI with proper TypeScript interfaces and Tailwind v4 styling.

## Component Structure Template

```typescript
// ComponentName.tsx
// Brief description of component purpose

// always named imports from React
import { ReactNode, ReactElement, useState } from "react";

export interface ComponentNameProps {
  children: ReactNode;
  variant?: "primary" | "secondary"; // Variant types
  size?: "small" | "medium" | "large"; // Size types
  disabled?: boolean;
  // Additional props
}

/**
 * ComponentName component.
 * Detailed description of what it does.
 */
export const ComponentName = ({
  children,
  variant = "primary",
  size = "medium",
  disabled = false,
}: ComponentNameProps): ReactElement => {
  // 1. Local state (if needed)
  const [isActive, setIsActive] = useState(false);

  // 2. Event handlers (if needed)
  const handleClick = (): void => {
    if (!disabled) setIsActive(!isActive);
  };

  // 3. Computed variant/size classes
  const getVariantClasses = (): string => {
    switch (variant) {
      case "secondary":
        return "bg-secondary-500 text-white";
      case "primary":
      default:
        return "bg-primary-500 text-white";
    }
  };

  const getSizeClasses = (): string => {
    switch (size) {
      case "small":
        return "px-3 py-1 text-sm";
      case "large":
        return "px-6 py-3 text-lg";
      case "medium":
      default:
        return "px-4 py-2 text-base";
    }
  };

  // 4. Compose final classes
  const baseClasses = `
    rounded-lg transition-all duration-200
    ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}
    ${getVariantClasses()}
    ${getSizeClasses()}
  `;

  return (
    <div className={baseClasses} onClick={handleClick}>
      {children}
    </div>
  );
}

export default ComponentName;
```

## What Are Atoms?

Atoms are the basic building blocks of your UI - fundamental, reusable components with single responsibility.

**Characteristics:**
- Single responsibility (one thing, well)
- No dependencies on other components
- Highly reusable across the application
- Minimal props (typically 3-7)
- Pure presentational logic

**Common Examples:**
- Button with variants (primary, secondary, disabled states)
- Input field with validation states
- Typography components (Heading, Paragraph, Label)
- Icon wrapper
- Card container
- Container layout

**Not Atoms** (compose atoms instead):
- FormField (Label + Input + Error) → compose atoms into a molecule
- SearchBox (Input + Button) → compose atoms into a molecule
- NavigationBar (multiple atoms + logic) → compose atoms into an organism

## Code Style Requirements

### Import Order
1. React (named imports)
2. Third-party libraries
3. Router/navigation
4. Local API/utils
5. Components
6. Context/state

```typescript
import { ReactNode, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { formatDate } from "../utils/dates";
import { useAuth } from "../context/AuthContext";
```

### Type Definitions
- Always export interface for props
- Use explicit types (`string | null`, never `any`)
- Union types for variants/states
- Optional props with `?`

```typescript
export interface ButtonProps {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "spotify";
  size?: "small" | "medium" | "large";
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
  ariaLabel?: string;
}
```

### Naming Conventions
- **PascalCase**: Components, interfaces
- **camelCase**: Functions, variables, props
- **UPPER_SNAKE_CASE**: Constants
- **Prop naming**: `onClick`, `isActive`, `hasError` (verb prefixes for booleans)

### Component Structure Order
```typescript
// 1. Props interface
export interface ComponentProps { }

// 2. Component function with JSDoc
/**
 * ComponentName brief description.
 * Longer description if needed.
 */
export const ComponentName = (props: ComponentProps): ReactElement => {
  // 3. State declarations
  const [state, setState] = useState();
  
  // 4. Event handlers
  const handleEvent = (): void => { };
  
  // 5. Computed values/classes
  const classes = computeClasses();
  
  // 6. Return JSX
  return <div>{children}</div>;
}

// 7. Export
export default ComponentName;
```

## Styling with Tailwind v4

### Core Principles
- Use Tailwind classes, avoid inline styles
- Group related classes together
- Use template literals for conditional classes
- Extract repeated patterns into helper functions

### Pattern: Variant Classes
```typescript
const getVariantClasses = (): string => {
  switch (variant) {
    case "spotify":
      return "bg-accent-500 text-primary-900 border-accent-700";
    case "secondary":
      return "bg-secondary-200 text-primary-900 border-secondary-700";
    case "primary":
    default:
      return "bg-primary-500 text-primary-50 border-primary-700";
  }
};
```

### Pattern: Conditional Styling
```typescript
const baseClasses = `
  rounded-lg font-bold transition-all duration-200
  ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer hover:scale-105"}
  ${isActive && "bg-active-500"}
  ${getVariantClasses()}
  ${getSizeClasses()}
`;
```

### Avoid v3 Patterns
**Tailwind v4 Guidelines (vs v3):**
- Avoid v3-era abstraction patterns
- Don't use `@apply` as a component or styling system (escape hatch only)
- Don't use `theme()` — Tailwind v4 exposes design tokens via CSS variables
- Don't over-invest in `tailwind.config.js`; v4 is CSS-first, config is optional

**Preferred v4 approach:**
- Use utility classes directly in markup
- Use React components for reuse, not CSS abstraction
- Use CSS variables for theming when needed

**Rule of thumb:** If you're writing CSS to avoid utilities, you're fighting Tailwind v4.

## Error Handling & Accessibility

### Optional Chaining
```typescript
const user = data?.user?.name ?? "Guest";
```

### User-Facing Errors
```typescript
try {
  await performAction();
} catch (err: any) {
  alert(`Error: ${err.message ?? "Something went wrong"}`);
}
```

### Accessibility Props
```typescript
<button
  type={type}
  onClick={onClick}
  disabled={disabled}
  aria-label={ariaLabel}
  aria-pressed={isPressed}
>
  {children}
</button>
```

## Quick Reference

### File Naming & Organization
- `ComponentName.tsx` (PascalCase)
- Place in `components/` or `components/atoms/` directory
- One component per file

### Component Checklist
- [ ] Props interface exported
- [ ] Default prop values set
- [ ] JSDoc comment present
- [ ] Tailwind v4 classes used
- [ ] Accessibility props included
- [ ] Error boundaries where needed
- [ ] Type safety (no `any` except external data)

### Method Size Limit
Keep logic methods under 20 lines. Extract helpers if needed:

```typescript
// Bad: 30-line render method with complex logic
export const Component = () => {
  return (
    <div>
      {/* 30 lines of conditional rendering */}
    </div>
  );
}

// Good: Extracted to helper
export const Component = () => {
  return <div>{renderContent()}</div>;
}

function renderContent(): ReactElement {
  // Complex logic extracted
}
```

## Assets

Component template available at `assets/templates/AtomicComponent.tsx`
