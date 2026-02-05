---
name: styling-guidelines
description: Tailwind CSS styling patterns with mandatory eb- prefix for embedded components. Use when applying styles, creating UI, or working with design tokens. Keywords - Tailwind, CSS, styling, eb- prefix, responsive design, design tokens.
compatibility: Designed for Tailwind CSS 3.x with custom prefix configuration
metadata:
  version: "2.0.0"
  author: jpmorgan-payments
  lastUpdated: "2025-12-24"
  priority: critical
---

# Styling Guidelines

## ⚠️ CRITICAL: eb- Prefix Requirement

**ALL Tailwind CSS classes MUST be prefixed with `eb-`.** This is mandatory for the embedded components library to avoid style conflicts when embedded in other applications.

## Correct Usage Examples

```typescript
// ✅ CORRECT - All classes prefixed with eb-
<div className="eb-flex eb-items-center eb-gap-4 eb-p-6">
  <Button className="eb-bg-primary eb-text-white eb-rounded-lg">
    Click me
  </Button>
</div>

// ❌ INCORRECT - Missing eb- prefix
<div className="flex items-center gap-4 p-6">
  <Button className="bg-primary text-white rounded-lg">
    Click me
  </Button>
</div>
```

## Common Class Patterns

### Layout

```typescript
className = "eb-flex eb-flex-col eb-items-center eb-justify-between";
className = "eb-grid eb-grid-cols-2 eb-gap-4";
className = "eb-w-full eb-h-full eb-max-w-md";
```

### Spacing

```typescript
className = "eb-p-4 eb-px-6 eb-py-2 eb-m-4 eb-mx-auto";
className = "eb-space-y-4 eb-space-x-2";
```

### Typography

```typescript
className = "eb-text-lg eb-font-semibold eb-text-gray-900";
className = "eb-text-sm eb-text-center eb-leading-relaxed";
```

### Colors and Backgrounds

```typescript
className = "eb-bg-white eb-text-black eb-border-gray-200";
className = "eb-bg-primary eb-text-primary-foreground";
```

### Interactive States

```typescript
className = "hover:eb-bg-gray-100 focus:eb-ring-2 active:eb-scale-95";
className = "disabled:eb-opacity-50 disabled:eb-cursor-not-allowed";
```

### Borders and Shadows

```typescript
className = "eb-border eb-border-gray-300 eb-rounded-lg";
className = "eb-shadow-md eb-shadow-lg eb-ring-1";
```

## Responsive Design

```typescript
// Mobile-first approach
className = "eb-text-sm md:eb-text-base lg:eb-text-lg";
className = "eb-grid eb-grid-cols-1 md:eb-grid-cols-2 lg:eb-grid-cols-3";
className = "eb-p-4 md:eb-p-6 lg:eb-p-8";
```

## Component Composition

```typescript
<Card className="eb-bg-white eb-shadow-sm eb-rounded-lg">
  <CardHeader className="eb-border-b eb-p-4">
    <CardTitle className="eb-text-lg eb-font-semibold">Title</CardTitle>
  </CardHeader>
  <CardContent className="eb-p-4 eb-space-y-4">
    {/* Content */}
  </CardContent>
</Card>
```

## Design Tokens

Use semantic color tokens from the theme:

```typescript
// Semantic colors
className = "eb-bg-primary eb-text-primary-foreground";
className = "eb-bg-secondary eb-text-secondary-foreground";
className = "eb-bg-destructive eb-text-destructive-foreground";
className = "eb-bg-muted eb-text-muted-foreground";
```

## Loading States

Always use skeleton components, never "Loading..." text:

```typescript
import { Skeleton } from '@/components/ui/skeleton';

{isLoading && (
  <div className="eb-space-y-3">
    {Array.from({ length: 5 }).map((_, i) => (
      <Skeleton key={i} className="eb-h-12 eb-w-full" />
    ))}
  </div>
)}

// For headers
<Skeleton className="eb-h-6 eb-w-32" />
<Skeleton className="eb-h-10 eb-w-28" />
```

## Status Messages

Centralize status messages in a single object:

```typescript
const STATUS_MESSAGES: Record<Status, string> = {
  ACTIVE: "Your account is active.",
  PENDING: "We are processing your request.",
  INACTIVE: "The account is currently inactive.",
  REJECTED: "We could not process this request.",
};

// Usage
{STATUS_MESSAGES[status] ?? "Unknown status"}
```

## Dialog and Popover Patterns

When using popovers inside dialogs, use explicit portals:

```typescript
<Dialog>
  <DialogContent>
    <Popover>
      <PopoverTrigger>...</PopoverTrigger>
      <PopoverContent portal={true}>
        {/* Content - won't be clipped by dialog */}
      </PopoverContent>
    </Popover>
  </DialogContent>
</Dialog>
```

## Accessibility Classes

```typescript
// Screen reader only
className = "eb-sr-only";

// Focus visible
className = "focus-visible:eb-ring-2 focus-visible:eb-ring-offset-2";

// ARIA states
className = "aria-disabled:eb-opacity-50";
className = "aria-selected:eb-bg-accent";
```

## Animation Classes

```typescript
className = "eb-transition-all eb-duration-200 eb-ease-in-out";
className = "hover:eb-scale-105 eb-transform";
className = "eb-animate-fade-in eb-animate-slide-up";
```

## Grid and Flex Patterns

```typescript
// Centered content
className = "eb-flex eb-items-center eb-justify-center eb-min-h-screen";

// Card grid
className = "eb-grid eb-grid-cols-1 md:eb-grid-cols-2 lg:eb-grid-cols-3 eb-gap-6";

// Form layout
className = "eb-flex eb-flex-col eb-gap-4";
```

## Best Practices

1. **Always use eb- prefix** - No exceptions
2. **Mobile-first** - Start with mobile, add breakpoints
3. **Use semantic colors** - Prefer `eb-bg-primary` over `eb-bg-blue-500`
4. **Composition** - Build complex UI from simple utility classes
5. **Consistency** - Follow existing patterns in codebase
6. **Accessibility** - Include focus states, ARIA support
7. **Performance** - Use `eb-transition` wisely

## Common Mistakes to Avoid

❌ Missing eb- prefix  
❌ Using "Loading..." text instead of Skeleton  
❌ Hardcoding colors instead of design tokens  
❌ Missing responsive breakpoints  
❌ Missing focus/hover states  
❌ Inconsistent spacing values  
❌ Not using semantic color names  

## Custom Configuration

The eb- prefix is configured in `tailwind.config.js`:

```javascript
module.exports = {
  prefix: 'eb-',
  // ... other config
}
```

## References

- See `embedded-components/DESIGN_TOKENS.md` for design system
- See `embedded-components/tailwind.config.js` for configuration
- See `embedded-components/ARCHITECTURE.md` for complete styling patterns
