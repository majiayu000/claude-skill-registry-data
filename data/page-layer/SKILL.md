---
name: page-layer
description: "This skill should be used when the user asks to 'create a page', 'add a route', 'create a layout', 'add metadata', or 'set up a dynamic route'. Provides guidance for Next.js 15 App Router pages, layouts, and route handlers in app/**/*.tsx."
---

# Page Layer Skill

## Scope

- `app/**/page.tsx` - Next.js page components
- `app/**/layout.tsx` - Layout components
- `app/**/not-found.tsx` - Not found pages
- `app/**/loading.tsx` - Loading states
- `app/**/error.tsx` - Error boundaries

## Decision Tree

### Creating a new page?

1. **Determine route**: Map URL to folder structure in `app/`
2. **Create folder**: `app/[route-name]/`
3. **Create `page.tsx`**: Export default async function
4. **Add metadata**: Export `metadata` object or `generateMetadata` function
5. **Use layout components**: Container, PageIntro, etc.

### Creating a dynamic route?

1. **Create folder with brackets**: `app/[param]/` or `app/[...slug]/`
2. **Type params as Promise**: `params: Promise<{ param: string }>`
3. **Await params**: `const { param } = await params;`
4. **Add `generateStaticParams`**: For static generation
5. **Add `generateMetadata`**: For dynamic meta tags

### Adding page metadata?

1. **Static metadata**: Export `metadata` object
2. **Dynamic metadata**: Export async `generateMetadata` function
3. **Include OpenGraph**: title, description, images, type
4. **Use env variables**: `env.PROJECT_BASE_TITLE`, etc.

### Adding a layout?

1. **Create `layout.tsx`** in route folder
2. **Accept `children` prop**
3. **Wrap with structural components**
4. **Export metadata if needed** (inherited by child pages)

## Quick Templates

### Basic Page

```tsx
import type { Metadata } from "next";
import { Container } from "@/components/layout/container";
import { PageIntro } from "@/components/layout/page-intro";

export const metadata: Metadata = {
  title: "Page Title",
  description: "Page description for SEO",
};

export default function PageName() {
  return (
    <Container className="mt-16">
      <PageIntro title="Page Title">
        <p>Page content description</p>
      </PageIntro>
      {/* Page content */}
    </Container>
  );
}
```

### Dynamic Route Page (Next.js 15)

```tsx
import type { Metadata } from "next";
import { notFound } from "next/navigation";

type Props = {
  params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
  // Return array of param objects for static generation
  return [{ slug: "example-1" }, { slug: "example-2" }];
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  // Fetch data and return metadata
  return {
    title: `Dynamic Title for ${slug}`,
    description: "Dynamic description",
  };
}

export default async function Page({ params }: Props) {
  const { slug } = await params;

  // Fetch data
  const data = getData(slug);
  if (!data) {
    notFound();
  }

  return (
    <div>
      <h1>{data.title}</h1>
    </div>
  );
}
```

### Layout

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    template: "%s | Section Name",
    default: "Section Name",
  },
};

export default function SectionLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="section-wrapper">
      {children}
    </div>
  );
}
```

### Not Found Page

```tsx
import { NotFound } from "@/components/shared/not-found";

export default function NotFoundPage() {
  return <NotFound message="Page not found" />;
}
```

### Metadata with OpenGraph

```tsx
import type { Metadata } from "next";
import { getCldImageUrl } from "next-cloudinary";
import { env } from "@/lib/config/env";
import { withCloudinaryCloudName } from "@/lib/utils/withCloudinaryCloudName";

const ogImageUrl = getCldImageUrl({
  width: 1200,
  height: 630,
  src: withCloudinaryCloudName("path/to/image"),
});

export const metadata: Metadata = {
  title: "Page Title",
  description: "Page description",
  openGraph: {
    title: "Page Title",
    description: "Page description",
    url: "/page-path",
    images: [ogImageUrl],
    type: "website",
    locale: "en_GB",
    siteName: env.PROJECT_BASE_TITLE,
  },
};
```

## Mistakes

- ❌ Missing `await params` in Next.js 15 (params is now a Promise)
- ❌ `"use client"` on pages (should be server components)
- ❌ Missing `generateStaticParams` for dynamic routes (breaks static export)
- ❌ Not calling `notFound()` for missing data
- ❌ Hardcoding URLs instead of using route config
- ❌ Missing metadata/OpenGraph tags

## Validation

After changes, run:
```bash
.claude/skills/page-layer/scripts/validate-page-patterns.sh <file>
pnpm build      # Full build validates routes
pnpm typecheck  # TypeScript validation
```

## Route Structure

```
app/
├── layout.tsx              # Root layout (required)
├── page.tsx                # Home page (/)
├── not-found.tsx           # Global 404
├── about/
│   └── page.tsx            # /about
├── articles/
│   ├── page.tsx            # /articles
│   └── [slug]/
│       ├── page.tsx        # /articles/[slug]
│       └── not-found.tsx   # Article 404
├── contact/
│   └── page.tsx            # /contact
└── projects/
    └── page.tsx            # /projects
```

## Next.js 15 Breaking Changes

**Params are now Promises**:
```tsx
// Next.js 14 (old)
export default function Page({ params }: { params: { slug: string } }) {
  const { slug } = params;
}

// Next.js 15 (current)
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
}
```
