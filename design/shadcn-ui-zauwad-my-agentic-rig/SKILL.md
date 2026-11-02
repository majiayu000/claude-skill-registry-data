---
name: shadcn-ui
description: Build, customize, and integrate accessible UI components and blocks using shadcn/ui patterns, Radix UI, Tailwind CSS, and class-variance-authority (CVA).
---

# shadcn/ui Component Architecture & Guidelines

Use this skill when designing, generating, auditing, or installing UI components using `shadcn/ui`.

## Core Architecture Principles

1. **Copy-Paste & Ownership**: Unlike traditional component libraries, `shadcn/ui` components live directly inside your project repository (e.g. `@/components/ui/`). You own the code and customize it directly.
2. **Accessible Primitives**: Built on top of Radix UI primitives for unstyled, accessible keyboard interactions and ARIA attributes.
3. **Tailwind CSS & CVA**: Styled with Tailwind CSS classes orchestrated via `class-variance-authority` (`cva`) for variants, sizes, and states.
4. **Utility Helper (`cn`)**: Uses `clsx` and `tailwind-merge` to safely combine classes:
   ```typescript
   import { clsx, type ClassValue } from "clsx"
   import { twMerge } from "tailwind-merge"

   export function cn(...inputs: ClassValue[]) {
     return twMerge(clsx(inputs))
   }
   ```

## Installation & CLI Workflow

When adding components to a project:
```bash
# Initialize shadcn/ui in a project (if not already initialized)
npx shadcn@latest init

# Add standard components
npx shadcn@latest add button dialog dropdown-menu card input form
```

If the project uses the `shadcn` MCP server, leverage the MCP tools to browse, search, and inspect available components and blocks.

## Component Pattern Guidelines

### 1. Variant Definition with CVA
Always expose variants and sizes through `cva`:
```typescript
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### 2. Polymorphic `asChild` with Radix Slot
Enable composition using Radix's `@radix-ui/react-slot`:
```typescript
import { Slot } from "@radix-ui/react-slot"

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"
```

### 3. Forms with React Hook Form & Zod
Always pair form controls with accessible labeling:
```typescript
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
```

## Dark Mode & Theming
- Use CSS variables (`var(--primary)`, `var(--background)`, `var(--muted)`) so theme colors adapt automatically to light and dark modes.
- Support `next-themes` or class-based dark mode toggles (`.dark`).
