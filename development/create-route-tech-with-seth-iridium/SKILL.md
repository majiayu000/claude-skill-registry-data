---
name: create-route
description: Create React Router 7 routes with proper type imports, loaders, and actions. Use when adding new pages, API endpoints, layouts, or route files.
---

# Create Route

Creates React Router 7 routes following Iridium's config-based routing patterns with proper type safety.

## When to Use

- Creating new pages or views
- Adding API endpoints
- Creating layout routes with `<Outlet />`
- User asks to "add a route", "create a page", or "add an endpoint"

## Critical Rule #1: Route Type Imports

**THE MOST IMPORTANT RULE - NEVER BREAK THIS:**

```tsx
// ✅ ALWAYS use this exact pattern:
import type { Route } from './+types/my-route';

// ❌ NEVER use relative paths:
import type { Route } from '../+types/my-route';   // WRONG!
import type { Route } from '../../+types/my-route'; // WRONG!
```

**If you see TypeScript errors about missing `./+types/[routeName]` modules:**

1. Run `npm run typecheck` to generate types
2. **NEVER try to "fix" it by changing the import path**

## Critical Rule #2: Destructure Directly

```tsx
// ✅ CORRECT - destructure in function signature
export async function action({ request, params }: Route.ActionArgs) {
    const formData = await request.formData();
}

// ❌ WRONG - intermediate variable
export async function action(args: Route.ActionArgs) {
    const { request } = args;  // Don't do this!
}
```

## Critical Rule #3: Access Data via Props

```tsx
// ✅ CORRECT - use loaderData prop
export default function MyPage({ loaderData }: Route.ComponentProps) {
    return <div>{loaderData.user.name}</div>;
}

// ❌ WRONG - old hook pattern
export default function MyPage() {
    const data = useLoaderData();  // DON'T USE THIS!
}
```

## Route Module Pattern

### Page Route (with UI)

```tsx
import type { Route } from './+types/my-page';
import { data, redirect } from 'react-router';

// Server data loading (GET requests)
export async function loader({ request, params }: Route.LoaderArgs) {
    const user = await requireUser(request);
    const items = await getItems(user.id);
    return { items };
}

// Form handling (POST/PUT/DELETE)
export async function action({ request, params }: Route.ActionArgs) {
    const user = await requireUser(request);
    const formData = await request.formData();

    if (request.method === 'POST') {
        await createItem(formData);
        return redirect('/items');
    }

    if (request.method === 'DELETE') {
        await deleteItem(formData.get('id') as string);
        return data({ success: true });
    }

    return null;
}

// Component - access data via props
export default function MyPage({ loaderData }: Route.ComponentProps) {
    return (
        <>
            <title>Page Title | Iridium</title>
            <meta name="description" content="Page description" />
            {/* Page content */}
        </>
    );
}
```

### API Route (no UI)

```tsx
import type { Route } from './+types/my-api';
import { data } from 'react-router';

// GET requests
export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireUser(request);
    const items = await getItems(user.id);
    return data({ items });
}

// POST/PUT/DELETE requests
export async function action({ request }: Route.ActionArgs) {
    const user = await requireUser(request);

    if (request.method === 'POST') {
        const body = await request.json();
        const result = await createItem(body);
        return data({ result });
    }

    if (request.method === 'PUT') {
        const body = await request.json();
        const result = await updateItem(body);
        return data({ result });
    }

    if (request.method === 'DELETE') {
        const body = await request.json();
        await deleteItem(body.id);
        return data({ success: true });
    }

    return data({ error: 'Method not allowed' }, { status: 405 });
}
```

### Layout Route (with Outlet)

```tsx
import type { Route } from './+types/my-layout';
import { Outlet } from 'react-router';

export default function MyLayout({ loaderData }: Route.ComponentProps) {
    return (
        <div className="layout">
            <nav>{/* Navigation */}</nav>
            <main>
                <Outlet />  {/* ✅ Child routes render here */}
            </main>
        </div>
    );
}

// ❌ NEVER use children prop - it doesn't exist
// export default function MyLayout({ children }: Route.ComponentProps)
```

## Register in routes.ts

After creating a route file, add it to `app/routes.ts`:

```tsx
import { type RouteConfig, index, route, layout, prefix } from '@react-router/dev/routes';
import { Paths } from './constants';

export default [
    // Page routes
    route(Paths.MY_PAGE, 'routes/my-page.tsx'),

    // Layout with children
    layout('routes/my-layout.tsx', [
        index('routes/my-layout-index.tsx'),
        route('child', 'routes/my-layout-child.tsx'),
    ]),

    // API routes
    ...prefix(Paths.API, [
        route('my-endpoint', 'routes/api/my-endpoint.ts'),
    ]),
] satisfies RouteConfig;
```

## Type-Safe URLs with href()

```tsx
import { Link, href, redirect } from 'react-router';

// Static routes
<Link to={href('/products')}>Products</Link>

// Dynamic routes - TYPE SAFE
<Link to={href('/products/:id', { id: product.id })}>View</Link>

// In redirects
return redirect(href('/products/:id', { id: newId }));

// ❌ NEVER manually construct URLs
<Link to={`/products/${id}`}>View</Link>  // No type safety!
```

## File Naming

```text
✅ GOOD - kebab-case, directories:
routes/my-page.tsx
routes/api/my-endpoint.ts
routes/dashboard/settings.tsx

❌ BAD - flat routing with $ or periods:
routes/dashboard.$id.tsx
routes/dashboard.settings.tsx
```

## Meta Tags (React 19 Pattern)

```tsx
export default function MyPage({ loaderData }: Route.ComponentProps) {
    return (
        <>
            <title>Page Title | Iridium</title>
            <meta name="description" content="Description" />
            {/* Page content */}
        </>
    );
}

// ❌ NEVER use meta() export - it's the old pattern
```

## After Creating a Route

1. **Register in routes.ts** - Add the route configuration
2. **Run `npm run typecheck`** - Generate route types
3. **Add to Paths constant** if reusable (in `app/constants.ts`)

## Anti-Patterns

- ❌ Using `../+types/` relative imports (always `./+types/`)
- ❌ Using `useLoaderData()` hook (use `loaderData` prop)
- ❌ Creating intermediate variables for destructuring
- ❌ Using `meta()` export (use React 19 JSX tags)
- ❌ Using `children` in layout routes (use `<Outlet />`)
- ❌ Manual URL construction (use `href()`)
- ❌ Using file-based routing conventions with `$`
- ❌ Calling Prisma directly (use model layer)

## Templates

- [Page Route Template](./templates/page-route.tsx)
- [API Route Template](./templates/api-route.ts)
- [Layout Route Template](./templates/layout-route.tsx)

## Full Reference

See `.github/instructions/react-router.instructions.md` for comprehensive documentation including streaming, error boundaries, and advanced patterns.
