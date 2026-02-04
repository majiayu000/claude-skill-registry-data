---
name: create-route
description: Create React Router 7 routes with proper type imports, loaders, and actions. Use when adding new pages, API endpoints, layouts, or route files.
---

# Create Route

## When to Use

- Creating new pages or views
- Adding API endpoints
- Creating layout routes with `<Outlet />`

## Critical Rules

### 1. Route Type Imports

```tsx
// ALWAYS use this pattern:
import type { Route } from './+types/my-route';

// NEVER use relative paths:
// import type { Route } from '../+types/my-route';  // WRONG!
```

**If types are missing:** Run `npm run typecheck` - NEVER change the import path.

### 2. Destructure Directly

```tsx
// CORRECT
export async function action({ request, params }: Route.ActionArgs) {}

// WRONG
export async function action(args: Route.ActionArgs) {
    const { request } = args;  // Don't do this!
}
```

### 3. Access Data via Props

```tsx
// CORRECT
export default function MyPage({ loaderData }: Route.ComponentProps) {}

// WRONG
const data = useLoaderData();  // Don't use hooks!
```

## Quick Start

```tsx
import type { Route } from './+types/my-page';
import { data, redirect } from 'react-router';

export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireUser(request);
    return { user };
}

export async function action({ request }: Route.ActionArgs) {
    const formData = await request.formData();
    // Handle POST/PUT/DELETE
    return redirect('/success');
}

export default function MyPage({ loaderData }: Route.ComponentProps) {
    return (
        <>
            <title>Page Title | Iridium</title>
            <meta name="description" content="Description" />
            {/* Content */}
        </>
    );
}
```

## Checklist

1. [ ] Create route file in `app/routes/`
2. [ ] Register in `app/routes.ts`
3. [ ] Run `npm run typecheck` to generate types
4. [ ] Add path to `Paths` constant if reusable

## Templates

- [Page Route](./templates/page-route.tsx)
- [API Route](./templates/api-route.ts)
- [Layout Route](./templates/layout-route.tsx)

## Full Reference

See `.github/instructions/react-router.instructions.md` for:
- Nested routes & layouts
- Dynamic segments & optional segments
- Streaming with Suspense
- Error boundaries
- Navigation patterns
