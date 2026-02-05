---
name: remix-static-routing
description: |
  Use when working with Remix routing in this repository as a static site generator (SSG). Covers file-based routing, dynamic segments, layout groups, and best practices.
---


This skill covers using Remix as a static site generator (SSG) in this repository, including file-based routing conventions, dynamic segments, layout groups, and best practices for creating routes.

## Key Concepts

### 1. Remix as a Static Site Generator

This repository uses Remix with Vite to generate a static site. Routes are pre-rendered at build time using the `ssg-cli.ts` script, which crawls routes and generates static HTML files.

### 2. File-Based Routing

Remix uses a flat file structure in `app/routes/` where the file path maps directly to URL routes:

- `app/routes/_landing._index/route.tsx` → `/`
- `app/routes/b._index/route.tsx` → `/b`
- `app/routes/b.$slug/route.tsx` → `/b/:slug`
- `app/routes/h.$slug/route.tsx` → `/h/:slug`

### 3. Route File Naming Conventions

- **Layout Groups** (prefixed with `_`): Group related routes without affecting the URL
  - `_landing` groups landing page routes
  - `_index` denotes the index route for a segment

- **Dynamic Segments** (prefixed with `$`): Create parameterized routes
  - `$slug` captures a URL parameter named `slug`
  - Used in `/b/$slug` for blog posts and `/h/$slug` for help pages

- **File Organization**: Each route has its own directory with:
  - `route.tsx` - The main route component
  - Optional `layout.tsx`, `error.tsx`, or other Remix files

### 4. Route Component Structure

A typical route component exports a default React component and optional loaders/actions:

```typescript
import type { LoaderFunctionArgs } from '@remix-run/node';

export async function loader(args: LoaderFunctionArgs) {
  // Load data at build time or request time
  return { data: '...' };
}

export default function RouteComponent() {
  // Render the route
  return <div>Content</div>;
}
```

### 5. Static Route Generation

For SSG, routes must be crawlable by the build system:
- Remix generates static HTML from all reachable routes
- Dynamic routes (`$slug`) need `getStaticPaths` or crawler hints
- The build system pre-fetches and renders all accessible routes

### 6. Styling and Assets

- Use Tailwind CSS for styling (see `styling-react-with-tailwind` skill)
- Import styles in route components or root layout
- Static assets go in `public/` directory

## Common Tasks

### Creating a New Route

1. Create directory: `app/routes/[segment]/`
2. Create file: `app/routes/[segment]/route.tsx`
3. Export default React component
4. Export loader if data is needed
5. The route is automatically available at `/{segment}`

### Creating a Dynamic Route

1. Use `$` prefix: `app/routes/section.$id/`
2. Access params via `useParams()` or loader args
3. Ensure all IDs are discoverable by the crawler

### Organizing Routes with Layouts

1. Use `_` prefix for layout groups (e.g., `_landing`)
2. Create shared layout component in the group
3. Child routes inherit the layout without URL changes

## Files and Configuration

- **Route files**: `app/routes/**/route.tsx`
- **SSG CLI**: `ssg-cli.ts` - Generates static site
- **Root layout**: `app/root.tsx` - Global layout and styling
- **Build config**: `vite.config.ts` - Vite + Remix build configuration

## Best Practices

1. **Keep routes simple** - One concern per route file
2. **Use loaders for data** - Fetch data server-side before rendering
3. **Name routes semantically** - Use clear, descriptive names
4. **Test with SSG** - Verify routes render correctly in static build
5. **Handle 404s** - Create catch-all or error boundary routes
6. **Optimize assets** - Use static assets from `public/` directory

## Related Skills

- `styling-react-with-tailwind` - CSS styling approach
- Core Remix documentation for advanced patterns
