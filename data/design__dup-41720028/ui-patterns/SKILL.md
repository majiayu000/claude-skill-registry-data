---
name: ui-patterns
description: Apply consistent UI component patterns for the project Next.js template. Use when building forms, dialogs, notifications, loading states, or any UI components. Ensures proper dark mode support, responsive behavior, animations, and adherence to the project's component library hierarchy.
---

# UI Patterns

Apply consistent, accessible UI patterns following project's established conventions for component libraries, colors, animations, and responsive behavior.

## Overview

This skill provides guidance on UI implementation patterns for the project Next.js starter template. It ensures consistency across:

- Component library selection and usage priority
- Dark mode color patterns with proper contrast
- Responsive dialog/drawer implementations
- Loading states and skeleton loaders
- Animation standards using BlurFade
- Error handling with toast notifications

## Component Library Priority

Follow this hierarchy when selecting components:

1. **shadcn/ui** - Primary choice for standard components (<https://ui.shadcn.com/>)
2. **Kibo UI** - Specialized components not in shadcn/ui (<https://www.kibo-ui.com/>)
3. **Magic UI** - Enhanced animations and effects (<https://magicui.design/>)
4. **React Bits** - Creative backgrounds (<https://reactbits.dev/>)
5. **Custom components** - Only when existing libraries don't meet needs

### Installation Commands

```bash
# shadcn/ui components
bunx --bun shadcn@latest add <component>

# Example: Install Button and Card
bunx --bun shadcn@latest add button card
```

## Dark Mode Color Patterns

Always implement both light and dark mode variants for colored elements. Use the standard color pattern:

```tsx
// Background + Border + Text pattern
className =
  "bg-{color}-50 dark:bg-{color}-950/30 border-{color}-200 dark:border-{color}-800 text-{color}-800 dark:text-{color}-200";
```

### Critical Rules

1. **Always use `/30` opacity** for dark backgrounds: `dark:bg-{color}-950/30`
2. **Never omit dark mode when using Tailwind colors not defined as CSS variables in `app/globals.css`** - Every Tailwind color _not_ in the theme needs a dark variant, e.g. `bg-red-50 dark:bg-red-950/30`
3. **Use consistent color families** - Don't mix green background with blue text

### Common Use Cases

**Success Message:**

```tsx
<div className="bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 rounded-lg p-4">
  <p className="text-green-800 dark:text-green-200">Operation successful</p>
</div>
```

**Error Message:**

```tsx
<div className="bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800 rounded-lg p-4">
  <p className="text-red-800 dark:text-red-200">An error occurred</p>
</div>
```

**Info/Warning:**

```tsx
// Info (blue)
<div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800">
  <p className="text-blue-800 dark:text-blue-200">Information</p>
</div>

// Warning (amber)
<div className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800">
  <p className="text-amber-900 dark:text-amber-100">Warning</p>
</div>
```

## Responsive Dialog/Drawer Pattern

Implement dialogs that transform into drawers on mobile for better UX:

- **Desktop (≥768px)**: Render as `Dialog`
- **Mobile (<768px)**: Render as `Drawer`

### Core Implementation

```tsx
import { useMediaQuery } from "@/hooks/use-media-query";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Drawer, DrawerContent } from "@/components/ui/drawer";

export function MyDialog({ open, onOpenChange }) {
  const isDesktop = useMediaQuery("(min-width: 768px)");

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-[500px] overflow-y-scroll max-h-screen">
          {/* Content */}
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent className="h-[95vh]">
        <div className="flex-1 min-h-0 px-4 pb-4">{/* Content */}</div>
      </DrawerContent>
    </Drawer>
  );
}
```

### Key Classes

- **Dialog**: `sm:max-w-[500px] overflow-y-scroll max-h-screen`
- **Drawer**: `h-[95vh]` for near full-screen height
- **Drawer content wrapper**: `flex-1 min-h-0 px-4 pb-4`

### Handling Different Layouts

When content needs different layouts for dialog vs drawer (e.g., fixed bottom buttons in drawer), pass an `isInDrawer` prop:

```tsx
const renderContent = ({ isInDrawer = false }) => (
  <MyForm isInDrawer={isInDrawer} />
);

// In form component
if (isInDrawer) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-4 pr-4 pb-4">
        {/* Form fields */}
      </div>
      <div className="flex-shrink-0 pt-4 border-t bg-background">
        {/* Fixed bottom buttons */}
      </div>
    </div>
  );
}
```

## Dialog Overflow Handling

For dialogs with potentially long content (forms with many fields, dynamic content):

```tsx
<DialogContent className="sm:max-w-[500px] overflow-y-scroll max-h-screen">
  {/* Content that might exceed viewport height */}
</DialogContent>
```

**Key Classes:**

- `overflow-y-scroll` - Enables vertical scrolling
- `max-h-screen` - Limits height to viewport
- `sm:max-w-[500px]` - Responsive width control

**When to use:**

- Dialogs with dynamic or user-generated content
- Mobile-responsive dialogs
- Any unpredictable content height

## Loading States

### Spinner Component

Use `Spinner` from `components/ui/spinner.tsx` for inline loading indicators:

```tsx
import { Spinner } from "@/components/ui/spinner";

// Button loading
<Button disabled={isLoading}>
  {isLoading && <Spinner className="mr-2 h-4 w-4" />}
  {isLoading ? "Submitting..." : "Submit"}
</Button>;
```

### Skeleton Loaders

For list items and cards, use `Skeleton` from `components/ui/skeleton.tsx`. **Always match the skeleton layout to the actual page layout:**

```tsx
import { Skeleton } from "@/components/ui/skeleton";
import BlurFade from "@/components/magicui/blur-fade";

// Match the structure of your actual TodoCard component
export function TodoListSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 5 }).map((_, index) => (
        <BlurFade key={index} delay={index * 0.1} duration={0.5} inView>
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-3/4" /> {/* Title */}
            </CardHeader>
            <CardContent>
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-2/3" />
            </CardContent>
          </Card>
        </BlurFade>
      ))}
    </div>
  );
}
```

### React Suspense

Use React Suspense for server-side data fetching in React Server Components:

```tsx
import { Suspense } from "react";

export default function Page() {
  return (
    <Suspense fallback={<TodoListSkeleton />}>
      <TodoList />
    </Suspense>
  );
}
```

## Animation Standards

Sometimes, `BlurFade` from `@/components/magicui/blur-fade` may be used to up the finish of the animations. **Ask the developer if BlurFade is appropriate** for the use case before implementing.

### Preferred Settings

- **Duration**: `0.2` seconds (balance between smooth and snappy)
- **Single elements**: `0.05` - `0.1` second delays
- **List items**: Use `index * 0.05` pattern (encouraged)
- **Sequential sections**: `0.1`, `0.12`, `0.15`, `0.17`, `0.2` second delays

### Usage Patterns

**Single Element:**

```tsx
<BlurFade duration={0.2} inView>
  <Card>Content</Card>
</BlurFade>
```

**List Items (Preferred Pattern):**

```tsx
{
  items.map((item, index) => (
    <BlurFade key={item.id} delay={index * 0.05} duration={0.2} inView>
      <ItemCard item={item} />
    </BlurFade>
  ));
}
```

**Sequential Sections:**

```tsx
<BlurFade delay={0.1} duration={0.2} inView>
  <Section1 />
</BlurFade>
<BlurFade delay={0.12} duration={0.2} inView>
  <Section2 />
</BlurFade>
```

**Loading States:**

```tsx
<BlurFade duration={0.2} inView>
  <Skeleton className="h-20 w-full" />
</BlurFade>
```

### Guidelines

- Always use `inView` prop for performance
- Keep duration consistent at 0.2s
- Avoid delays longer than 0.25s for individual elements
- Apply to both content and loading states

## Error Handling

### Toast Notifications

Use Sonner for user feedback in forms and mutations:

```tsx
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";

const mutation = useMutation({
  mutationFn: serverAction,
  onSuccess: () => {
    toast.success("Item created successfully");
  },
  onError: (error) => {
    toast.error("Failed to create item", {
      description: error.message,
    });
  },
});
```

### Error Boundaries

For component-level errors, use error boundaries. See `components/error-boundary.tsx` for the implementation.

## Styling Conventions

### Semantic Colors

Use semantic color classes instead of literal colors:

```tsx
// ✅ CORRECT
className = "text-primary bg-secondary border-accent";

// ❌ AVOID
className = "text-blue-600 bg-gray-100 border-green-500";
```

### Conditional Classes

Use the `cn()` utility from `lib/utils.ts` for conditional classes:

```tsx
import { cn } from "@/lib/utils";

<div
  className={cn(
    "base-classes",
    isActive && "active-classes",
    variant === "primary" && "primary-classes"
  )}
/>;
```

### Component Variants

Prefer composition over customization for component variants:

```tsx
// ✅ CORRECT - Composition
<Card className="border-blue-200 bg-blue-50">
  <CardHeader>...</CardHeader>
</Card>

// ❌ AVOID - Over-customization
<Card variant="blue" theme="light" bordered={true}>
```

## Related Files

- Component utilities: `/lib/utils.ts`
- Spinner component: `/components/ui/spinner.tsx`
- Skeleton component: `/components/ui/skeleton.tsx`
- BlurFade component: `/components/magicui/blur-fade.tsx`
- Error boundary: `/components/error-boundary.tsx`
- Media query hook: `/hooks/use-media-query.ts`
