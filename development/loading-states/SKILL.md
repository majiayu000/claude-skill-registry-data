---
name: loading-states
description: Handle loading states in the portal app using Flask loaders. Use when adding loading indicators to buttons, cards, pages, or any async operations.
---

# Loading States in Portal

The portal uses custom Flask loader components for all loading states. Never use `Loader2` from lucide-react or CSS `animate-spin`.

## Components

Import from `@/components/ui/flask-loader`:

| Component           | Use Case                                     |
| ------------------- | -------------------------------------------- |
| `FlaskLoader`       | Centered loading for cards, panels, overlays |
| `FlaskInlineLoader` | Inline loading in buttons, text, badges      |
| `FlaskButton`       | Button with built-in loading state           |
| `CardLoader`        | Full card loading with optional message      |
| `PageLoader`        | Full page loading (rarely needed)            |

## Variants

Both `FlaskLoader` and `FlaskInlineLoader` support variants:

| Variant             | Use When                                 |
| ------------------- | ---------------------------------------- |
| `loading` (default) | Fetching data, waiting for response      |
| `processing`        | Running computations, simulations, tests |
| `idle`              | Ready state with subtle animation        |

## Button Loading States

### Simple Button with Loading

```tsx
import { FlaskInlineLoader } from "@/components/ui/flask-loader";
import { Button } from "@/components/ui/button";
import { Save } from "lucide-react";

<Button disabled={isLoading}>
  {isLoading ? (
    <FlaskInlineLoader className="mr-2 h-4 w-4" />
  ) : (
    <Save className="mr-2 h-4 w-4" />
  )}
  Save
</Button>;
```

### Processing Button (simulations, tests)

```tsx
<Button disabled={isRunning}>
  {isRunning ? (
    <FlaskInlineLoader className="mr-2 h-4 w-4" variant="processing" />
  ) : (
    <Play className="mr-2 h-4 w-4" />
  )}
  Run Simulation
</Button>
```

### FlaskButton (shorthand)

```tsx
import { FlaskButton } from "@/components/ui/flask-loader";

<FlaskButton loading={isLoading} onClick={handleSave}>
  Save Changes
</FlaskButton>;
```

## Card/Panel Loading

### Inside a Card

```tsx
import { FlaskLoader } from "@/components/ui/flask-loader";

{
  loading ? (
    <div className="flex items-center justify-center py-8">
      <FlaskLoader size="sm" />
    </div>
  ) : (
    <CardContent>...</CardContent>
  );
}
```

### CardLoader with Message

```tsx
import { CardLoader } from "@/components/ui/flask-loader";

{
  loading && <CardLoader message="Loading data ..." />;
}
```

### Inline with Text

```tsx
<div className="flex items-center justify-center py-8">
  <FlaskInlineLoader className="h-6 w-6 text-muted-foreground" />
  <span className="ml-2 text-sm text-muted-foreground">
    Loading coverage data...
  </span>
</div>
```

## Status Indicators

### Active Job/Process

```tsx
{
  job.status === "running" ? (
    <FlaskInlineLoader className="h-4 w-4" variant="processing" />
  ) : (
    <CheckIcon className="h-4 w-4" />
  );
}
```

### In Links (name resolution)

```tsx
{
  isLoading && <FlaskInlineLoader className="h-3 w-3 opacity-50" />;
}
```

## Sizes

`FlaskLoader` sizes: `sm` (32px), `md` (48px), `lg` (64px), `xl` (96px)

`FlaskInlineLoader` uses className for sizing (default 16px):

- `h-3 w-3` - tiny (12px)
- `h-4 w-4` - small (16px, default)
- `h-5 w-5` - medium (20px)
- `h-6 w-6` - large (24px)

## Page Loading (loading.tsx)

For route-level loading, keep using Skeleton components in `loading.tsx` files - they provide structural hints. Don't use FlaskLoader for page-level loading.

```tsx
// app/feature/loading.tsx
import { FeatureSkeleton } from "@/components/feature";

export default function FeatureLoading() {
  return <FeatureSkeleton />;
}
```

## Decision Guide

1. **Button loading** → `FlaskInlineLoader` or `FlaskButton`
2. **Running simulation/test** → `FlaskInlineLoader variant="processing"`
3. **Card/panel data loading** → `FlaskLoader size="sm"` or `CardLoader`
4. **Active job indicator** → `FlaskInlineLoader variant="processing"`
5. **Inline status** → `FlaskInlineLoader` with appropriate size
6. **Page loading** → Skeleton components (not Flask)
