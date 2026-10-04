---
name: nextjs-complete-setup
description: Complete Next.js 16 project setup with standardized architecture and comprehensive TSDoc documentation, combining project structure creation with automatic documentation standards
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: project-setup
  scope: nextjs-complete
  pattern: setup-with-documentation
---

## What this workflow does

- Creates a fully standardized Next.js 16 application with shadcn, Tailwind v4, and src directory
- Establishes Tekk-prefixed component architecture with named exports
- Enables React Compiler for optimized performance
- Applies comprehensive TSDoc documentation to all generated TypeScript functions
- Ensures all components and functions follow TSDoc industry standards
- Configures TSDoc validation and linting rules
- Sets up proper TypeScript strict mode and type checking
- Implements npx zero-install experience throughout

## When to use

Use this workflow when:

- Starting a new Next.js demo application from scratch
- Need both project structure and documentation standards in one step
- Want to ensure TSDoc compliance from the beginning
- Creating maintainable, well-documented component architecture
- Setting up projects with comprehensive quality standards
- Need automated TSDoc validation in the development workflow

**Common signals:**

- New Next.js project initialization required
- Both project setup and documentation needed simultaneously
- Want to establish TSDoc standards early in project lifecycle
- Need production-ready Next.js architecture with full documentation

## Workflow Overview

This workflow combines two skills in sequence:

1. **Phase 1: Project Setup** (`nextjs-standard-setup`)
   - Initialize Next.js 16 with TypeScript and Tailwind v4
   - Configure shadcn component library
   - Create src/ directory structure with path aliases
   - Set up Tekk-prefixed component architecture
   - Enable React Compiler
   - Configure TypeScript strict mode
   - Set up ESLint and Prettier

2. **Phase 2: Documentation** (`nextjs-tsdoc-documentor`)
   - Apply TSDoc to all generated components and functions
   - Configure TSDoc validation in ESLint
   - Ensure parameter and return type documentation
   - Set up TSDoc best practices
   - Validate TSDoc completeness

## Prerequisites

- Node.js 24+ installed
- npm package manager
- Git repository initialized (optional but recommended)
- Terminal/shell access
- Internet connection for package installation
- Familiarity with Next.js and TypeScript concepts

## Workflow Steps

### Step 1: Initialize Next.js 16 Project

Create a new Next.js 16 application with TypeScript:

```bash
# Create Next.js 16 app with npx -y for zero-install experience
npx -y create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Navigate to project directory
cd my-app
```

**Project will include:**

- Next.js 16 with App Router
- TypeScript configuration
- Tailwind CSS v4
- ESLint setup
- src/ directory structure

### Step 2: Configure Tailwind v4

Update to Tailwind CSS v4 configuration:

```bash
# Install Tailwind v4 with npx -y for zero-install experience
npx -y tailwindcss@latest init -p
```

Update `tailwind.config.ts`:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
```

### Step 3: Install and Configure shadcn

Install shadcn with proper TypeScript configuration:

```bash
# Initialize shadcn with npx
npx -y shadcn@latest init

# Configuration during init:
# - TypeScript: Yes
# - Style: Default (Tailwind)
# - Base color: Slate
# - CSS variables: Yes
# - Tailwind config: tailwind.config.ts
# - Aliases: @/components, @/lib, @/utils
```

shadcn creates:

- `src/components/ui/` - Library components directory
- `src/lib/utils.ts` - Utility functions
- `components.json` - Component configuration

### Step 4: Create Standardized Directory Structure

Create src/ directory structure with proper organization:

```bash
# Create directory structure
mkdir -p src/app
mkdir -p src/components/ui
mkdir -p src/components/TekkComponents
mkdir -p src/lib
mkdir -p src/types
mkdir -p src/custom-components
mkdir -p src/page-containers
```

**Project Structure:**

```
project-root/
├── src/
│   ├── app/                      # App Router pages
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                # shadcn library components
│   │   │   ├── button.tsx
│   │   │   └── card.tsx
│   │   └── TekkComponents/    # Tekk-prefixed wrappers
│   │       ├── TekkButton.tsx
│   │       └── TekkCard.tsx
│   ├── lib/                       # Utility functions
│   │   ├── utils.ts
│   │   └── constants.ts
│   ├── types/                     # TypeScript type definitions
│   │   └── index.ts
│   ├── custom-components/        # Feature-specific components
│   └── page-containers/         # Client state containers
├── public/                     # Static assets
├── tsconfig.json               # TypeScript configuration
├── next.config.ts              # Next.js configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── .eslintrc.json            # ESLint with TSDoc validation
└── package.json
```

### Step 5: Configure TypeScript with Path Aliases

Set up `tsconfig.json` with @/ path aliases:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/app/*": ["./src/app/*"],
      "@/types/*": ["./src/types/*"]
    },
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "incremental": true,
    "jsx": "preserve",
    "plugins": [
      {
        "name": "next"
      }
    ]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### Step 6: Enable React Compiler

Configure React Compiler in `next.config.ts`:

```typescript
// next.config.ts
const nextConfig = {
  experimental: {
    reactCompiler: true,
  },
};

module.exports = nextConfig;
```

### Step 7: Generate Base Tekk Components with TSDoc

Create Tekk-prefixed components with comprehensive TSDoc:

#### TekkButton Component

````typescript
// src/components/TekkComponents/TekkButton.tsx
import React from 'react'
import { Button as ShadcnButton, ButtonProps } from "@/components/ui/button"

/**
 * Extended button component with Tekk styling and behavior.
 *
 * This component wraps shadcn Button with Tekk-specific styling
 * conventions and default behaviors. Supports all button variants
 * from the base component while adding consistent styling.
 *
 * @param variant - Button style variant (default, destructive, outline, secondary, ghost, link)
 * @param size - Button size (default, sm, lg, icon)
 * @param disabled - Whether button is in disabled state
 * @param children - Button content to render
 * @param className - Additional CSS classes to apply
 * @param props - Additional props from shadcn Button
 * @returns Enhanced button component with Tekk styling
 *
 * @example
 * ```tsx
 * <TekkButton variant="default" size="lg" disabled={false}>
 *   Submit Form
 * </TekkButton>
 * ```
 */
export const TekkButton: React.FC<ButtonProps> = ({
  variant = "default",
  size = "default",
  disabled = false,
  children,
  className,
  ...props
}) => {
  return (
    <ShadcnButton
      variant={variant}
      size={size}
      disabled={disabled}
      className={`font-semibold ${className || ''}`}
      {...props}
    >
      {children}
    </ShadcnButton>
  )
}
````

#### TekkCard Component

````typescript
// src/components/TekkComponents/TekkCard.tsx
import React from 'react'
import { Card as ShadcnCard, CardProps } from "@/components/ui/card"

/**
 * Extended card component with Tekk styling and layout.
 *
 * Provides a consistent card container for content grouping
 * with Tekk-specific styling conventions. Includes header,
 * content, and footer sections for flexible layouts.
 *
 * @param className - Additional CSS classes to apply
 * @param children - Card content components
 * @returns Enhanced card component with Tekk styling
 *
 * @example
 * ```tsx
 * <TekkCard>
 *   <TekkCardHeader>
 *     <TekkCardTitle>Card Title</TekkCardTitle>
 *   </TekkCardHeader>
 *   <TekkCardContent>
 *     <p>Card content goes here</p>
 *   </TekkCardContent>
 * </TekkCard>
 * ```
 */
export const TekkCard: React.FC<CardProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <ShadcnCard
      className={`rounded-lg border shadow-sm ${className || ''}`}
      {...props}
    >
      {children}
    </ShadcnCard>
  )
}

/**
 * Card header component with title and description.
 *
 * @param children - Header content components
 * @returns Styled card header section
 */
export const TekkCardHeader: React.FC<{ children: React.ReactNode }> = ({
  children
}) => {
  return (
    <div className="flex flex-col space-y-1.5 p-6">
      {children}
    </div>
  )
}

/**
 * Card title component for consistent heading style.
 *
 * @param children - Title text or content
 * @returns Styled card title heading
 */
export const TekkCardTitle: React.FC<{ children: React.ReactNode }> = ({
  children
}) => {
  return (
    <h3 className="text-2xl font-semibold leading-none tracking-tight">
      {children}
    </h3>
  )
}

/**
 * Card content wrapper for main content area.
 *
 * @param children - Content components
 * @returns Styled card content section
 */
export const TekkCardContent: React.FC<{ children: React.ReactNode }> = ({
  children
}) => {
  return (
    <div className="p-6 pt-0">
      {children}
    </div>
  )
}
````

#### TekkHomePageContainer Component

````typescript
// src/page-containers/TekkHomePageContainer.tsx
"use client"
import React, { useState, ReactNode } from 'react'

/**
 * Client-side container for home page with state management.
 *
 * This container wraps home page content with common
 * state management and loading states. Provides a consistent
 * structure for home page layouts.
 *
 * @param children - Page content components to render
 * @param initialLoading - Initial loading state (default: false)
 * @returns Client-side home page wrapper with state
 *
 * @example
 * ```tsx
 * <TekkHomePageContainer>
 *   <TekkHeroSection />
 *   <TekkFeaturesSection />
 * </TekkHomePageContainer>
 * ```
 */
export const TekkHomePageContainer: React.FC<{
  children: ReactNode;
  initialLoading?: boolean;
}> = ({
  children,
  initialLoading = false
}) => {
  const [isLoading, setIsLoading] = useState(initialLoading)

  /**
   * Set loading state for page transitions.
   *
   * @param loading - New loading state
   */
  const setLoading = (loading: boolean) => {
    setIsLoading(loading)
  }

  return (
    <div className="min-h-screen">
      {isLoading ? (
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-pulse">Loading...</div>
        </div>
      ) : (
        <main>{children}</main>
      )}
    </div>
  )
}
````

### Step 8: Create Index Files with TSDoc

Create index.ts files with proper re-exports and TSDoc:

````typescript
// src/components/TekkComponents/index.ts

/**
 * Central export file for all Tekk-prefixed components.
 *
 * Provides clean import paths and enables tree-shaking for
 * Tekk component library. All components are exported as
 * named exports following React best practices.
 *
 * @example
 * ```typescript
 * import { TekkButton, TekkCard, TekkHomePageContainer } from '@/components/TekkComponents'
 * ```
 */

// Core UI Components
export { TekkButton } from "./TekkButton";
export {
  TekkCard,
  TekkCardHeader,
  TekkCardTitle,
  TekkCardContent,
} from "./TekkCard";

// Page Containers
export { TekkHomePageContainer } from "@/page-containers/TekkHomePageContainer";
````

````typescript
// src/custom-components/index.ts

/**
 * Export file for custom feature-specific components.
 *
 * Groups custom components by feature area for organized imports.
 * All components use named exports for better tree-shaking.
 *
 * @example
 * ```typescript
 * import { UserProfile, NavigationBar } from '@/custom-components'
 * ```
 */

// Feature Components
export * from "./UserProfile";
export * from "./NavigationBar";
````

### Step 9: Configure TSDoc Validation

Set up ESLint with TSDoc validation rules:

```bash
# Install ESLint TSDoc packages
npm install --save-dev eslint-plugin-jsdoc @typescript-eslint/eslint-plugin @typescript-eslint/parser

# Create or update .eslintrc.json
cat > .eslintrc.json <<EOF
{
  "extends": ["next/core-web-vitals", "prettier"],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2022,
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "rules": {
    "react/react-in-jsx-scope": "off",
    "jsdoc/require-jsdoc": "error",
    "jsdoc/require-param": "error",
    "jsdoc/require-param-description": "error",
    "jsdoc/require-returns": "error",
    "jsdoc/require-returns-description": "error",
    "jsdoc/require-template": "error",
    "jsdoc/require-param-type": "off",
    "jsdoc/require-returns-type": "off"
  }
}
EOF
```

### Step 10: Configure Prettier

Set up Prettier for code formatting:

```bash
cat > .prettierrc <<EOF
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
EOF
```

### Step 11: Add Scripts to package.json

Update `package.json` with useful scripts:

```json
{
  "name": "my-nextjs-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,json,css,md}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,json,css,md}\""
  }
}
```

### Step 12: Create Utility Functions with TSDoc

Add utility functions with proper TSDoc:

````typescript
// src/lib/utils.ts

import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind CSS classes intelligently.
 *
 * Combines class names using clsx for conditional classes
 * and tailwind-merge to resolve Tailwind conflicts.
 * This is the preferred method for combining Tailwind classes.
 *
 * @param inputs - Class value inputs to merge (strings, arrays, objects)
 * @returns Merged class name string
 *
 * @example
 * ```tsx
 * const className = cn('px-4 py-2', isActive && 'bg-blue-500', customClass)
 * ```
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format a date to a localized string.
 *
 * @param date - Date object to format
 * @param locale - Locale string (default: 'en-US')
 * @returns Formatted date string
 *
 * @example
 * ```typescript
 * formatDate(new Date(), 'en-US')
 * // Returns: "January 1, 2024"
 * ```
 */
export function formatDate(date: Date, locale: string = "en-US"): string {
  return new Intl.DateTimeFormat(locale).format(date);
}

/**
 * Debounce a function call.
 *
 * Delays function execution until after a specified delay
 * has elapsed since the last call. Useful for search inputs
 * and resize handlers.
 *
 * @template T - Function type to debounce
 * @param func - Function to debounce
 * @param wait - Delay in milliseconds
 * @returns Debounced function
 *
 * @example
 * ```typescript
 * const debouncedSearch = debounce(searchItems, 300)
 * debouncedSearch(query)
 * ```
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number,
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return (...args: Parameters<T>) => {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => func(...args), wait);
  };
}
````

### Step 13: Create Type Definitions with TSDoc

Define TypeScript types with documentation:

```typescript
// src/types/index.ts

/**
 * Base interface for API response data.
 *
 * Provides consistent structure for all API responses
 * including success status and optional error information.
 *
 * @template T - Type of the response data
 */
export interface ApiResponse<T> {
  /** Indicates if the request was successful */
  success: boolean;
  /** The response data if successful */
  data?: T;
  /** Error message if request failed */
  error?: string;
}

/**
 * User profile data structure.
 *
 * Contains all essential user information for display
 * and account management purposes.
 */
export interface UserProfile {
  /** Unique identifier for the user */
  id: string;
  /** User's full display name */
  name: string;
  /** User's email address */
  email: string;
  /** User profile image URL */
  avatar?: string;
  /** Account creation timestamp */
  createdAt: Date;
}

/**
 * Navigation link configuration.
 *
 * Defines structure for navigation menu items
 * including labels, paths, and metadata.
 */
export interface NavLink {
  /** Display label for the link */
  label: string;
  /** Navigation path or URL */
  href: string;
  /** Optional icon component to display */
  icon?: React.ReactNode;
  /** Whether link is currently active */
  active?: boolean;
  /** Optional external link flag */
  external?: boolean;
}
```

## Best Practices

### Component Documentation

- **Every component** must have TSDoc with @param and @returns
- **Complex props** use dot notation for nested properties
- **Examples** provided in @example blocks
- **Type annotations** present in function signatures
- **Summary line** describes component purpose concisely

### File Organization

- **Named exports** for all custom components
- **Index files** for clean import paths
- **Organized by feature** in custom-components/
- **UI components** in components/ui/ (library)
- **Tekk wrappers** in components/TekkComponents/

### Code Quality

- **TypeScript strict mode** enabled
- **ESLint** with TSDoc validation
- **Prettier** for consistent formatting
- **React Compiler** enabled
- **No default exports** for custom components

### Documentation Standards

- **TSDoc comments** immediately before declarations
- **All parameters** documented with types
- **Return values** always documented
- **Async functions** document Promise<T> returns
- **Generic functions** use @template tags

## Verification Checklist

After setup, verify with these steps:

### Project Structure

- [ ] Next.js 16 initialized with TypeScript
- [ ] Tailwind v4 configured properly
- [ ] shadcn components installed and initialized
- [ ] src/ directory structure created
- [ ] Path aliases configured in tsconfig.json
- [ ] React Compiler enabled in next.config.ts

### TSDoc Compliance

- [ ] All components have TSDoc comments
- [ ] All parameters have @param tags
- [ ] All return values have @returns tags
- [ ] TSDoc validation enabled in ESLint
- [ ] @example blocks provided for public APIs
- [ ] Generic components have @template tags

### Code Quality

- [ ] TypeScript compilation passes (npm run type-check)
- [ ] ESLint passes without errors (npm run lint)
- [ ] Prettier formatting applied (npm run format)
- [ ] Build completes successfully (npm run build)
- [ ] Named exports used for all custom components
- [ ] Index files created for clean imports

### Runtime Verification

- [ ] Development server starts (npm run dev)
- [ ] Pages render correctly
- [ ] Components display properly
- [ ] TypeScript types resolve correctly
- [ ] TSDoc tooltips show in IDE

## Common Issues

### TSDoc Validation Errors

**Issue:** ESLint reports missing TSDoc comments

**Solution:** Add TSDoc to all functions and components

```typescript
// Before:
export const MyComponent = ({ children }) => { ... }

// After:
/**
 * Component description.
 *
 * @param children - Content to render
 * @returns Rendered component
 */
export const MyComponent = ({ children }) => { ... }
```

### Import Path Issues

**Issue:** Path aliases not resolving correctly

**Solution:** Verify tsconfig.json paths configuration

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"]
    }
  }
}
```

### Missing Named Exports

**Issue:** Import errors for custom components

**Solution:** Use named exports instead of default exports

```typescript
// ❌ Incorrect - Default export
export default function TekkButton() { ... }

// ✅ Correct - Named export
export const TekkButton = () => { ... }
```

### Tailwind Classes Not Applied

**Issue:** Tailwind styles not showing up

**Solution:** Verify Tailwind v4 configuration and content paths

```typescript
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  // ...
};
```

