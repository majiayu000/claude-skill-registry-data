---
name: "shadcn/ui Component Integration"
description: "Install and customize shadcn/ui components with Tailwind CSS theming, variants, and styling. Use when adding UI components or customizing the design system."
tools: Read, Grep, Glob, Write, Edit, Bash
model: inherit
---

# Skill: shadcn/ui Component Integration

Complete guide for installing, customizing, and styling shadcn/ui components with Tailwind CSS theming.

## When to Use

- Adding new shadcn/ui components to your project
- Customizing component styles and variants
- Setting up or modifying theme configuration
- Troubleshooting component styling issues
- Creating custom component variants
- Integrating Tailwind CSS with shadcn/ui

## Domain Knowledge

### Critical Patterns

#### Copy-Paste, Not NPM Install (CRITICAL)

shadcn/ui is NOT an npm package - it's a collection of reusable components that you copy into your project.

**Installation method:**
```bash
npx shadcn@latest add [component-name]
```

**What this does:**
1. Downloads component source code
2. Places it in `components/ui/[component-name].tsx`
3. You own the code and can modify it directly

**Why this matters:**
- Components live in YOUR codebase
- Full control over styling and behavior
- No hidden abstractions or locked-in APIs
- Customize directly in the component file

```bash
# ❌ Wrong - no npm package exists
npm install shadcn-ui

# ✅ Correct - copy component into project
npx shadcn@latest add button
```

#### Component Installation Command

Use the shadcn CLI to add components:

```bash
# Add single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button input card

# Add all components (not recommended)
npx shadcn@latest add --all
```

Components are copied to `components/ui/` directory.

#### CSS Variables for Theming

shadcn/ui uses CSS variables defined in `app/globals.css` for theming:

```css
/* app/globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    /* ... more variables */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... more variables */
  }
}
```

**Format:** HSL values without the `hsl()` wrapper.

**Why**: Allows easy theme switching between light/dark modes by changing CSS classes.

#### Import Path Convention

Always import components from `@/components/ui/[component]`:

```typescript
// ✅ Correct
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

// ❌ Wrong - relative paths
import { Button } from "../../components/ui/button";
```

**Why:** The `@/*` alias is configured in `tsconfig.json` and provides clean imports.

### Key Files

- **components/ui/** - All shadcn/ui components live here
- **app/globals.css** - CSS variables for theming
- **tailwind.config.ts** - Tailwind configuration
- **lib/utils.ts** - Utility functions (like `cn()` for class merging)
- **components.json** - shadcn/ui configuration

### Component Anatomy

All shadcn/ui components follow similar patterns:

```typescript
// components/ui/button.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)

export { Button, buttonVariants }
```

**Key parts:**
1. `cva()` - Creates variant classes
2. `cn()` - Merges classes intelligently
3. `VariantProps` - TypeScript types for variants
4. Variants system - Predefined style combinations

### Theming System

shadcn/ui uses Tailwind CSS with custom color tokens:

**Color tokens:**
- `background` / `foreground` - Base colors
- `primary` / `primary-foreground` - Primary actions
- `secondary` / `secondary-foreground` - Secondary actions
- `muted` / `muted-foreground` - Muted content
- `accent` / `accent-foreground` - Accent highlights
- `destructive` / `destructive-foreground` - Destructive actions
- `border` - Border color
- `input` - Input border color
- `ring` - Focus ring color

Use in Tailwind classes:
```typescript
<div className="bg-primary text-primary-foreground">
  Primary colored section
</div>
```

## Workflows

### Workflow 1: Add New Component

**Step 1: Install Component**

```bash
npx shadcn@latest add button
```

This creates `components/ui/button.tsx`.

**Step 2: Import and Use**

```typescript
// app/page.tsx
import { Button } from "@/components/ui/button";

export default function Page() {
  return (
    <div>
      <Button>Click me</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="destructive">Delete</Button>
    </div>
  );
}
```

**Step 3: Verify Styling**

Check that:
- Component renders correctly
- Styles are applied
- Dark mode works (if implemented)
- Variants work as expected

### Workflow 2: Customize Component Theme

**Step 1: Identify CSS Variable**

Find the variable in `app/globals.css`:

```css
:root {
  --primary: 222.2 47.4% 11.2%; /* Current primary color */
}
```

**Step 2: Update Color Value**

Change to desired color (use HSL format):

```css
:root {
  --primary: 263 70% 50%; /* New purple primary */
}
```

**Convert colors to HSL:**
- Use online converter or browser DevTools
- Format: `hue saturation% lightness%`
- Example: Purple = `263 70% 50%`

**Step 3: Update Dark Mode (Optional)**

```css
.dark {
  --primary: 263 75% 60%; /* Lighter purple for dark mode */
}
```

**Step 4: Test Across App**

Verify all primary-colored components look correct.

### Workflow 3: Create Custom Variant

**Step 1: Locate Component File**

```typescript
// components/ui/button.tsx
const buttonVariants = cva(
  "...",
  {
    variants: {
      variant: {
        default: "...",
        destructive: "...",
        outline: "...",
        // Add custom variant here
      },
    },
  }
)
```

**Step 2: Add New Variant**

```typescript
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        // Custom success variant
        success: "bg-green-600 text-white hover:bg-green-700",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        // Custom extra-large size
        xl: "h-14 rounded-md px-12 text-lg",
      },
    },
  }
)
```

**Step 3: Use Custom Variant**

```typescript
<Button variant="success">Save Changes</Button>
<Button size="xl">Large Button</Button>
```

### Workflow 4: Combine Multiple Components

**Step 1: Install Required Components**

```bash
npx shadcn@latest add card button input label
```

**Step 2: Compose Components**

```typescript
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function LoginCard() {
  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Login</CardTitle>
      </CardHeader>
      <CardContent>
        <form className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="you@example.com" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" />
          </div>
          <Button className="w-full">Sign In</Button>
        </form>
      </CardContent>
    </Card>
  );
}
```

**Step 3: Apply Consistent Spacing**

Use Tailwind utility classes for consistent spacing:
- `space-y-4` - Vertical spacing between children
- `gap-4` - Grid/flex gap
- `p-4` - Padding
- `m-4` - Margin

### Workflow 5: Implement Dark Mode

**Step 1: Ensure Dark Mode Variables Exist**

Check `app/globals.css` has dark mode styles:

```css
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... all color variables */
}
```

**Step 2: Add Theme Provider (if using next-themes)**

```typescript
// app/layout.tsx
import { ThemeProvider } from "next-themes";

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

**Step 3: Create Theme Toggle**

```typescript
"use client";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      Toggle theme
    </Button>
  );
}
```

**Step 4: Test Both Themes**

Verify all components look good in light and dark modes.

## Troubleshooting

### Issue: Component Not Found After Installation

**Symptoms:**
- Import error: "Cannot find module '@/components/ui/button'"
- Component file exists but import fails

**Cause:** `@/*` import alias not configured

**Solution:**

Check `tsconfig.json` has the alias:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

Also check `next.config.ts` or `vite.config.ts` depending on your setup.

**Frequency:** Medium

### Issue: Styling Not Applied

**Symptoms:**
- Component renders but has no styling
- Looks like unstyled HTML

**Possible Causes & Solutions:**

**1. Tailwind not processing component paths**

Check `tailwind.config.ts`:

```typescript
export default {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}", // Must include this
  ],
  // ...
}
```

**2. CSS variables missing**

Check `app/globals.css` has all CSS variables:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    /* ... all required variables */
  }
}
```

**3. Tailwind directives missing**

Ensure `app/globals.css` has:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Frequency:** Medium

### Issue: Dark Mode Not Working

**Symptoms:**
- Theme toggle doesn't change colors
- Dark class applied but no visual change

**Cause:** Missing dark mode CSS variables

**Solution:**

Ensure `app/globals.css` has complete dark mode section:

```css
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
  /* ... all other variables */
}
```

Variables must match the light mode variables (same names).

**Frequency:** Low

### Issue: Class Names Not Merging Correctly

**Symptoms:**
- Custom classes override all styles
- Variants not working with additional classes

**Cause:** Not using `cn()` utility properly

**Solution:**

Always use `cn()` to merge classes:

```typescript
// ❌ Wrong - classes override each other
<Button className="bg-red-500">Delete</Button>

// ✅ Correct - modify component to accept custom classes properly
import { cn } from "@/lib/utils";

<Button className={cn("bg-red-500")}>Delete</Button>
```

Or modify the variant instead:

```typescript
<Button variant="destructive">Delete</Button>
```

**Frequency:** Low

## Validation Checklist

Before considering shadcn/ui integration complete:

- [ ] Component installed via `npx shadcn@latest add`
- [ ] Component renders without errors
- [ ] Styles applied correctly
- [ ] Variants work as expected
- [ ] Dark mode works (if implemented)
- [ ] Import alias (@/*) working
- [ ] Tailwind config includes component paths
- [ ] CSS variables defined in globals.css
- [ ] Component accessible and keyboard-navigable
- [ ] Responsive on mobile devices

## Best Practices

1. **Install only what you need** - Don't use `--all`, add components as needed
2. **Customize after installation** - Components are meant to be modified
3. **Use variants over custom classes** - Prefer variants for consistency
4. **Maintain the theme system** - Use CSS variables, not hardcoded colors
5. **Test dark mode early** - Don't wait until the end to implement dark mode
6. **Keep components/ui clean** - Only shadcn components in this folder
7. **Create wrapper components** - Build app-specific variants in separate folder
8. **Use consistent spacing** - Leverage Tailwind's spacing scale

## Advanced Techniques

### Creating Composite Components

Build higher-level components from shadcn primitives:

```typescript
// components/forms/SearchBox.tsx
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search } from "lucide-react";

export function SearchBox() {
  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Search..."
        className="pl-10"
      />
      <Button
        size="sm"
        className="absolute right-1 top-1/2 -translate-y-1/2"
      >
        Search
      </Button>
    </div>
  );
}
```

### Theming Multiple Projects

Extract theme to separate file:

```typescript
// lib/theme.ts
export const theme = {
  light: {
    background: "0 0% 100%",
    foreground: "222.2 84% 4.9%",
    // ...
  },
  dark: {
    background: "222.2 84% 4.9%",
    foreground: "210 40% 98%",
    // ...
  },
};
```

Generate `globals.css` from theme object for consistency across projects.

## References

- **Previous expertise**: `.claude/experts/shadcn-expert/expertise.yaml`
- **Agent integration**: `.claude/agents/agent-shadcn.md`
- **Official docs**: https://ui.shadcn.com
- **Tailwind docs**: https://tailwindcss.com
