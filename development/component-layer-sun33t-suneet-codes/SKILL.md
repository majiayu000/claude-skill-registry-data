---
name: component-layer
description: "This skill should be used when the user asks to 'create a component', 'add a button', 'build a card', 'add UI element', or 'create a feature component'. Provides guidance for React components using shadcn/ui, Radix primitives, and CVA patterns in components/**/*.tsx."
---

# Component Layer Skill

## Scope

- `components/ui/*.tsx` - shadcn/ui base components (Radix primitives)
- `components/features/*.tsx` - Feature-specific components
- `components/shared/*.tsx` - Reusable shared components
- `components/layout/*.tsx` - Layout components
- `components/mdx/*.tsx` - MDX-specific components
- `components/providers/*.tsx` - Context providers

## Decision Tree

### Creating a new UI primitive?

1. **Check if shadcn/ui has it**: Visit ui.shadcn.com first
2. **If available**: Use `npx shadcn@latest add <component>`
3. **If custom**: Create in `components/ui/` following CVA pattern
4. **Export from component file** (no barrel exports needed)

### Creating a feature component?

1. **Create in `components/features/`**
2. **Name descriptively**: `contact-form.tsx`, `articles-list.tsx`
3. **Import UI primitives** from `@/components/ui/`
4. **Use server components** by default (no "use client" unless needed)

### Creating a shared/reusable component?

1. **Create in `components/shared/`**
2. **Keep it generic** - no feature-specific logic
3. **Props interface** with clear types
4. **Consider composition** over configuration

### Adding client interactivity?

1. **Add `"use client"` directive** at top of file
2. **Keep client boundary small** - extract client parts
3. **Prefer server components** when possible

## Quick Templates

### UI Component with CVA (shadcn/ui pattern)

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";
import { cn } from "@/lib/utils";

const componentVariants = cva(
  "base-classes-here",
  {
    variants: {
      variant: {
        default: "variant-default-classes",
        secondary: "variant-secondary-classes",
      },
      size: {
        default: "size-default-classes",
        sm: "size-sm-classes",
        lg: "size-lg-classes",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ComponentProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {}

const Component = React.forwardRef<HTMLDivElement, ComponentProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(componentVariants({ variant, size, className }))}
        {...props}
      />
    );
  }
);
Component.displayName = "Component";

export { Component, componentVariants };
```

### Feature Component (Server)

```tsx
import { ComponentName } from "@/components/ui/component-name";

interface FeatureProps {
  title: string;
  items: Array<{ id: string; name: string }>;
}

export function FeatureName({ title, items }: FeatureProps) {
  return (
    <section>
      <h2>{title}</h2>
      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </section>
  );
}
```

### Client Component

```tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

interface InteractiveProps {
  initialValue: string;
}

export function InteractiveComponent({ initialValue }: InteractiveProps) {
  const [value, setValue] = useState(initialValue);

  return (
    <div>
      <span>{value}</span>
      <Button onClick={() => setValue("clicked")}>Click me</Button>
    </div>
  );
}
```

### Layout Component

```tsx
import { cn } from "@/lib/utils";

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function Container({ className, children, ...props }: ContainerProps) {
  return (
    <div className={cn("mx-auto max-w-7xl px-4", className)} {...props}>
      {children}
    </div>
  );
}
```

## Mistakes

- ❌ `"use client"` when not needed (adds to bundle)
- ❌ Missing `cn()` utility for className merging
- ❌ Missing `displayName` on forwardRef components
- ❌ Not extending HTML element attributes for proper typing
- ❌ Wrong directory (ui vs features vs shared)
- ❌ Inline styles instead of Tailwind classes

## Validation

After changes, run:
```bash
.claude/skills/component-layer/scripts/validate-component-patterns.sh <file>
pnpm typecheck  # Verify TypeScript
pnpm check      # Biome lint/format
```

## Directory Structure

```
components/
├── ui/           # shadcn/ui primitives (button, card, etc.)
├── features/     # Feature-specific (contact-form, articles-list)
├── shared/       # Reusable across features (avatar, social-icons)
├── layout/       # Layout components (container, header, footer)
├── mdx/          # MDX rendering components (code, code-tabs)
└── providers/    # Context providers (theme, posthog)
```
