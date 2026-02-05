---
name: web-frontend
description: Guidelines for building minimal, professional, and concise frontend components in the /web project using TypeScript, React Router v7, Tailwind CSS, and the CVA pattern.
---

# Web Frontend Development Skill

This skill provides guidance for developing frontend components in the `/web` project for CRAN/E, a PWA that searches CRAN packages and authors.

## Tech Stack

- **TypeScript** for type safety
- **React Router v7** (Vite build) with Remix-style file-based routes
- **Tailwind CSS** with Radix Colors for styling
- **CVA (Class Variance Authority)** for component variants
- **Remix Icons** (`@remixicon/react`) for icons
- **Supabase** for data fetching via typed client

## Design Principles

### Minimal & Professional

The design follows a clean, minimal aesthetic with:
- Gradient accents (iris, ruby, jade, bronze, sand, amethyst, opal)
- Subtle hover effects with slow transitions (duration-700)
- Rounded corners (rounded-full for pills, rounded-xl for cards)
- Consistent spacing using Tailwind's gap utilities
- Dark mode support via Radix Colors

### Component Structure

All UI components follow these patterns:

1. **Props Definition**: Use `PropsWithChildren` when accepting children, combine with `VariantProps<typeof twBase>` from CVA
2. **CVA Styling**: Define variants using `cva()` for reusable, type-safe class composition
3. **Display Name**: Always set `Component.displayName` for debugging
4. **Type Safety**: Leverage TypeScript for props, Zod schemas for validation

### Core Component Patterns

#### Layout Components

**Header** (`app/modules/header.tsx`):
- Gradient backgrounds with variants
- Headline + optional subline structure
- Optional ornament slot for additional content

**PageContent** (`app/modules/page-content.tsx`):
- Full-width wrapper with consistent padding
- `full-width` class for spanning viewport width
- Inner flex column with gap-16 for section spacing

**PageContentSection** (`app/modules/page-content-section.tsx`):
- Headline, subline, and fragment ID for anchor navigation
- Prose variant for long-form text styling
- Gap-16 for consistent vertical rhythm

#### Interactive Components

**InfoPill** (`app/modules/info-pill.tsx`):
- Rounded-full border with gradient hover effects
- Optional label slot (left-aligned, gray-dim)
- Size variants: xs, sm, md, lg
- Gradient variants matching design system
- Hover opacity transition on gradient overlay

**InfoCard** (`app/modules/info-card.tsx`):
- Rounded-xl border with gradient hover effects
- Min height for consistent card sizing
- Icon indicators (external/internal) with wiggle animation on hover
- Group hover states for coordinated animations

**Tag** (`app/modules/tag.tsx`):
- Small, uppercase, rounded-full labels
- Border gradients (iris, jade) for semantic meaning
- Size variants: xs, sm

#### Utility Components

**Separator** (`app/modules/separator.tsx`):
- Simple `<hr>` with opacity-20 for subtle dividers

**Prose** (`app/modules/prose.tsx`):
- Typography component for long-form content
- Supports dangerouslySetInnerHTML for rendered HTML
- Text-xl, font-light, leading-normal baseline

**Anchors & AnchorLink** (`app/modules/anchors.tsx`):
- Navigation for in-page sections
- Fragment-based routing

### Color System

Use Radix Colors with semantic variants:
- **iris**: Primary/action color
- **ruby**: Error/destructive actions
- **jade**: Success/positive states
- **bronze**: Neutral/informational
- **sand/gold**: Warm highlights
- **amethyst**: Secondary accent (plum + iris mix)
- **opal**: Cool accent (iris + sky mix)

Text colors:
- `text-gray-normal`: Body text
- `text-gray-dim`: Secondary/muted text
- `text-gray-12/text-gray-4`: Prose (dark/light mode)

### Page Structure Pattern

Reference pages follow this structure:

1. **Header** with gradient and title
2. **Anchors** navigation (if multiple sections)
3. **PageContent** wrapper
4. **PageContentSection** for each major section
5. **Separator** between sections

Example from `_page.privacy._index.tsx`:
```tsx
<Header gradient="sand" headline="Privacy" subline="..." />
<Anchors anchorIds={...}>...</Anchors>
<PageContent>
  <PageContentSection headline="General" fragment="general">
    <p>...</p>
  </PageContentSection>
  <Separator />
  <PageContentSection headline="..." fragment="...">
    ...
  </PageContentSection>
</PageContent>
```

### Route Patterns

- `_page.*` files: Public pages with layout wrapper
- `_page.package.$packageName.tsx`: Package detail pages
- `_page.author.$authorName.tsx`: Author profile pages
- `_page.privacy._index.tsx`: Static content pages
- `api.*`: API endpoints (search, MCP)
- `*.og.*`: Open Graph image generation

### Data Loading

Use React Router's `loader` pattern:
```tsx
export const loader: LoaderFunction = async ({ params }) => {
  const data = await Service.fetchData(params.id);
  if (!data) throw data(null, { status: 404 });
  return data(data);
};
```

Access via `useLoaderData<LoaderData>()`.

### Meta Tags

Use `mergeMeta()` helper for combining meta tags:
```tsx
export const meta = mergeMeta(({ data }) => {
  const title = `${data.name} | CRAN/E`;
  return [
    { title },
    { name: "description", content: data.description },
    { property: "og:title", content: title },
    { property: "og:image", content: `${url}/og` },
  ];
});
```

### Styling Best Practices

1. **Use CVA for variants**: Don't hardcode conditional classes
2. **Prefer Tailwind utilities**: Avoid custom CSS when possible
3. **Dark mode**: Use Radix Colors with `dark:` variants
4. **Transitions**: Use duration-700 for smooth, professional animations
5. **Responsive**: Use `md:` breakpoint for desktop adjustments
6. **Spacing**: Use gap utilities for flex/grid spacing instead of margins

### Accessibility

- Use semantic HTML elements
- Provide meaningful alt text for images
- Ensure keyboard navigation works
- Test with screen readers when adding interactive elements

### Icon Usage

Import from `@remixicon/react`:
```tsx
import { RiArrowRightSLine, RiExternalLinkLine } from "@remixicon/react";
```

Size prop for consistency (typically 16 or 20).

### Component File Structure

```tsx
import { cva, VariantProps } from "cva";
import { PropsWithChildren, ReactNode } from "react";

type Props = PropsWithChildren<
  VariantProps<typeof twBase> & {
    // Custom props
  }
>;

const twBase = cva({
  base: "...",
  variants: {
    size: { ... },
  },
  defaultVariants: { ... },
});

export function Component(props: Props) {
  const { children, ...rest } = props;
  return <div className={twBase(rest)}>{children}</div>;
}

Component.displayName = "Component";
```

## Testing Strategy

- **Lint**: `npm run lint` from `/web`
- **Typecheck**: `npm run typecheck` from `/web`
- **Build**: `npm run build` from `/web`
- No unit tests; validation relies on lint/typecheck/build

## Common Patterns to Follow

### Example: Package Detail Page (_page.package.$packageName.tsx)

- Header with package name and gradient
- Anchors for section navigation (Synopsis, Documentation, Team, Insights, Binaries, Dependencies)
- Multiple PageContentSection components
- InfoPill for metadata (version, license, etc.)
- InfoCard for related packages/authors
- ExternalLink components for CRAN URLs
- Lazy-loaded components for performance (e.g., PackageDependencySearch)

### Example: Author Page (_page.author.$authorName.tsx)

- Header with author name
- List of packages by author using InfoCard grid
- Team section showing collaborators
- Similar structure to package page

## File Organization

- Routes: `/web/app/routes/*.tsx`
- Components: `/web/app/modules/*.tsx`
- Data services: `/web/app/data/*.ts`
- Types: `/web/app/data/*.shape.ts` (Zod schemas), `*.types.generated.ts` (Supabase)

## Environment

- Node >= 20 (v23.3.0 recommended via `.nvmrc`)
- npm (with `legacy-peer-deps = true` in `.npmrc`)
- Required env vars: See `.env.example`
