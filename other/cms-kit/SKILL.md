---
name: cms-kit
description: "Unified CMS + content-layer toolkit — Payload CMS (collections, globals, access control, Lexical rich text), Sanity.io (GROQ, structured content, real-time), Contentlayer (type-safe content collections), MDX (@next/mdx, mdx-bundler, remark/rehype plugins), Tiptap (headless rich-text editor on ProseMirror). Single entry point for content-driven apps."
layer: domain
category: cms
triggers: [".mdx files", "@next/mdx", "@tiptap/", "EditorContent", "StarterKit", "content collections", "content source", "contentlayer", "contentlayer config", "groq", "headless cms", "lexical editor", "mdx", "mdx content", "mdx-bundler", "mdx-components", "payload", "payload admin", "payload cms", "payload collection", "payload global", "payload hook", "portable text", "prosemirror", "rehype plugin", "remark plugin", "rich text editor", "sanity", "sanity schema", "sanity studio", "sanity.io", "structured content", "tiptap", "useEditor"]
---

# cms-kit

Unified CMS + content-layer toolkit — Payload CMS (collections, globals, access control, Lexical rich text), Sanity.io (GROQ, structured content, real-time), Contentlayer (type-safe content collections), MDX (@next/mdx, mdx-bundler, remark/rehype plugins), Tiptap (headless rich-text editor on ProseMirror). Single entry point for content-driven apps.


## Absorbs

- `payload`
- `sanity`
- `contentlayer`
- `mdx`
- `tiptap`


---

## From `payload`

> Payload CMS headless content management, custom fields, access control, hooks, REST/GraphQL API, and admin panel customization

# Payload CMS

## Purpose

Build content-managed applications with Payload 3.x, a headless CMS that embeds directly into Next.js. Covers collection and global configuration, field types, access control, hooks, the Local API, REST/GraphQL endpoints, rich text with Lexical, admin panel customization, versioning/drafts, and database adapters.

## Core Patterns

### Project Structure

```
my-payload-app/
  payload.config.ts          # Main Payload configuration
  collections/
    Posts.ts
    Users.ts
    Media.ts
    Tags.ts
  globals/
    SiteSettings.ts
    Navigation.ts
  hooks/
    populateSlug.ts
    revalidateOnChange.ts
  access/
    isAdmin.ts
    isAdminOrSelf.ts
  fields/
    slug.ts                  # Reusable field configs
    hero.ts
  blocks/
    CallToAction.ts
    ContentBlock.ts
  components/
    admin/                   # Custom admin panel components
  app/
    (frontend)/              # Next.js frontend routes
    (payload)/
      admin/
        [[...segments]]/
          page.tsx           # Payload admin panel route
```

### Collection Config

```typescript
// collections/Posts.ts
import type { CollectionConfig } from "payload";
import { isAdmin } from "../access/isAdmin";
import { populateSlug } from "../hooks/populateSlug";

export const Posts: CollectionConfig = {
  slug: "posts",
  admin: {
    useAsTitle: "title",
    defaultColumns: ["title", "status", "author", "publishedAt"],
    listSearchableFields: ["title", "slug"],
    group: "Content",
  },
  access: {
    read: () => true,
    create: ({ req: { user } }) => Boolean(user),
    update: isAdmin,
    delete: isAdmin,
  },
  hooks: {
    beforeChange: [populateSlug],
    afterChange: [
      async ({ doc, req }) => {
        // Revalidate Next.js cache on content change
        if (process.env.NEXT_REVALIDATION_KEY) {
          await fetch(`${process.env.NEXT_PUBLIC_URL}/api/revalidate`, {
            method: "POST",
            headers: { "x-revalidation-key": process.env.NEXT_REVALIDATION_KEY },
            body: JSON.stringify({ collection: "posts", slug: doc.slug }),
          });
        }
      },
    ],
  },
  versions: {
    drafts: {
      autosave: { interval: 1500 },
    },
    maxPerDoc: 25,
  },
  fields: [
    { name: "title", type: "text", required: true, minLength: 5, maxLength: 120 },
    {
      name: "slug",
      type: "text",
      unique: true,
      admin: { position: "sidebar", readOnly: true },
      index: true,
    },
    { name: "content", type: "richText" }, // Lexical editor by default
    { name: "excerpt", type: "textarea", maxLength: 300 },
    { name: "author", type: "relationship", relationTo: "users", required: true },
    { name: "tags", type: "relationship", relationTo: "tags", hasMany: true },
    { name: "hero", type: "upload", relationTo: "media" },
    {
      name: "status",
      type: "select",
      options: [
        { label: "Draft", value: "draft" },
        { label: "Published", value: "published" },
      ],
      defaultValue: "draft",
      admin: { position: "sidebar" },
    },
    {
      name: "publishedAt",
      type: "date",
      admin: {
        position: "sidebar",
        date: { pickerAppearance: "dayAndTime" },
      },
    },
    {
      name: "relatedPosts",
      type: "relationship",
      relationTo: "posts",
      hasMany: true,
      maxRows: 3,
      filterOptions: ({ id }) => ({ id: { not_equals: id } }),
    },
    {
      name: "layout",
      type: "blocks",
      blocks: [
        {
          slug: "content-block",
          fields: [
            { name: "richText", type: "richText" },
          ],
        },
        {
          slug: "cta",
          fields: [
            { name: "heading", type: "text", required: true },
            { name: "description", type: "textarea" },
            { name: "link", type: "text" },
            { name: "buttonLabel", type: "text", defaultValue: "Learn More" },
          ],
        },
        {
          slug: "media-block",
          fields: [
            { name: "media", type: "upload", relationTo: "media", required: true },
            { name: "caption", type: "text" },
            { name: "size", type: "select", options: ["small", "medium", "full"], defaultValue: "medium" },
          ],
        },
      ],
    },
    {
      name: "seo",
      type: "group",
      fields: [
        { name: "metaTitle", type: "text", maxLength: 60 },
        { name: "metaDescription", type: "textarea", maxLength: 160 },
        { name: "ogImage", type: "upload", relationTo: "media" },
      ],
    },
  ],
};
```

### Global Config (Site Settings)

```typescript
// globals/SiteSettings.ts
import type { GlobalConfig } from "payload";

export const SiteSettings: GlobalConfig = {
  slug: "site-settings",
  access: { read: () => true, update: ({ req: { user } }) => user?.role === "admin" },
  fields: [
    { name: "siteName", type: "text", required: true },
    { name: "siteDescription", type: "textarea" },
    { name: "logo", type: "upload", relationTo: "media" },
    {
      name: "nav",
      type: "array",
      maxRows: 8,
      fields: [
        { name: "label", type: "text", required: true },
        { name: "url", type: "text", required: true },
        { name: "newTab", type: "checkbox", defaultValue: false },
      ],
    },
    {
      name: "footer",
      type: "group",
      fields: [
        { name: "copyright", type: "text" },
        {
          name: "socialLinks",
          type: "array",
          fields: [
            { name: "platform", type: "select", options: ["twitter", "github", "linkedin", "youtube"] },
            { name: "url", type: "text", required: true },
          ],
        },
      ],
    },
  ],
};
```

### Access Control Patterns

```typescript
// access/isAdmin.ts
import type { Access } from "payload";

export const isAdmin: Access = ({ req: { user } }) => {
  return user?.role === "admin";
};

// access/isAdminOrSelf.ts — users can edit their own content
export const isAdminOrSelf: Access = ({ req: { user } }) => {
  if (!user) return false;
  if (user.role === "admin") return true;
  // Return a query constraint — Payload applies it as a WHERE clause
  return { author: { equals: user.id } };
};

// Field-level access
const adminOnlyField = {
  name: "internalNotes",
  type: "textarea" as const,
  access: {
    read: ({ req: { user } }) => user?.role === "admin",
    update: ({ req: { user } }) => user?.role === "admin",
  },
};
```

### Hooks

```typescript
// hooks/populateSlug.ts
import type { CollectionBeforeChangeHook } from "payload";

export const populateSlug: CollectionBeforeChangeHook = ({ data, operation }) => {
  if (operation === "create" && data?.title && !data.slug) {
    data.slug = data.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");
  }
  return data;
};

// hooks/revalidateOnChange.ts
import type { CollectionAfterChangeHook } from "payload";
import { revalidatePath, revalidateTag } from "next/cache";

export const revalidateOnChange: CollectionAfterChangeHook = ({
  doc,
  collection,
  req: { payload },
}) => {
  payload.logger.info(`Revalidating ${collection.slug}: ${doc.id}`);
  revalidateTag(collection.slug);
  if (doc.slug) {
    revalidatePath(`/blog/${doc.slug}`);
  }
  return doc;
};
```

### Local API (Server-Side Data Fetching)

```typescript
// lib/payload.ts — Server-side data access
import { getPayload } from "payload";
import config from "@payload-config";

export async function getPublishedPosts(page = 1, limit = 10) {
  const payload = await getPayload({ config });
  return payload.find({
    collection: "posts",
    where: {
      status: { equals: "published" },
      publishedAt: { less_than_equal: new Date().toISOString() },
    },
    sort: "-publishedAt",
    page,
    limit,
    depth: 1, // Resolve 1 level of relationships
  });
}

export async function getPostBySlug(slug: string) {
  const payload = await getPayload({ config });
  const result = await payload.find({
    collection: "posts",
    where: { slug: { equals: slug } },
    depth: 2,
    limit: 1,
  });
  return result.docs[0] ?? null;
}

export async function getSiteSettings() {
  const payload = await getPayload({ config });
  return payload.findGlobal({ slug: "site-settings" });
}

// Creating content programmatically
export async function seedPosts() {
  const payload = await getPayload({ config });
  await payload.create({
    collection: "posts",
    data: {
      title: "Welcome",
      slug: "welcome",
      status: "published",
      content: { root: { children: [] } }, // Lexical format
      author: "admin-user-id",
      publishedAt: new Date().toISOString(),
    },
  });
}
```

### Payload Config (Main Entry)

```typescript
// payload.config.ts
import { buildConfig } from "payload";
import { postgresAdapter } from "@payloadcms/db-postgres";
import { lexicalEditor } from "@payloadcms/richtext-lexical";
import { s3Storage } from "@payloadcms/storage-s3";
import sharp from "sharp";

import { Posts } from "./collections/Posts";
import { Users } from "./collections/Users";
import { Media } from "./collections/Media";
import { Tags } from "./collections/Tags";
import { SiteSettings } from "./globals/SiteSettings";

export default buildConfig({
  admin: {
    user: Users.slug,
    meta: {
      titleSuffix: " — My CMS",
      icons: [{ url: "/favicon.ico" }],
    },
  },
  collections: [Posts, Users, Media, Tags],
  globals: [SiteSettings],
  editor: lexicalEditor(),
  secret: process.env.PAYLOAD_SECRET!,
  db: postgresAdapter({
    pool: { connectionString: process.env.DATABASE_URL! },
    push: process.env.NODE_ENV === "development", // Auto-push schema in dev
  }),
  plugins: [
    s3Storage({
      collections: { media: { prefix: "media" } },
      bucket: process.env.S3_BUCKET!,
      config: {
        credentials: {
          accessKeyId: process.env.S3_ACCESS_KEY!,
          secretAccessKey: process.env.S3_SECRET_KEY!,
        },
        region: process.env.S3_REGION!,
      },
    }),
  ],
  sharp,
  typescript: { outputFile: "payload-types.ts" },
});
```

## Best Practices

- **Use the Local API** for server-side data fetching — it's type-safe, fast, and skips HTTP overhead
- **Control `depth`** in queries — default depth resolves all relationships, which is expensive; set explicitly
- **Use field-level access control** — hide sensitive fields from non-admin users at the API level
- **Enable versions and drafts** — `versions: { drafts: true }` gives content editors a publish workflow
- **Use blocks for page builders** — the `blocks` field type lets editors compose flexible layouts
- **Revalidate Next.js cache in hooks** — use `afterChange` hooks to call `revalidateTag` or `revalidatePath`
- **Generate TypeScript types** — `payload generate:types` creates types from your collection configs
- **Use `group` fields** for organization — groups like `seo`, `metadata` keep the admin panel tidy
- **Use relationship `filterOptions`** — prevent self-referencing and enforce business rules in the admin UI
- **Set `index: true`** on fields used in queries — slug, status, publishedAt benefit from DB indexes

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|---|---|---|
| `depth: 0` or unbounded depth | Under-fetching or over-fetching related data | Set explicit depth (1-2) based on needs |
| Access control only in frontend | API is wide open, data leaks | Define access at collection and field level |
| Storing computed data in fields | Stale data, manual sync needed | Use `computedFields` or hooks |
| Hardcoding user roles as strings | Typos, no autocomplete | Define role enum and reuse across access fns |
| No slug index | Slow lookups on common queries | Add `index: true` to slug fields |
| Giant monolithic collection config | Hard to maintain, poor readability | Extract hooks, access fns, and blocks to files |
| Skipping `sharp` in config | Image resizing fails silently | Always include `sharp` for media processing |
| Using REST API for server components | Unnecessary HTTP overhead | Use the Local API (`getPayload`) in RSC |

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Content site with Next.js App Router | Payload embedded in same Next.js app |
| Need admin panel for editors | Built-in — Payload admin at `/admin` |
| User authentication needed | Add `auth: true` to Users collection — JWT/sessions included |
| Page builder / flexible layouts | Use `blocks` field type with custom block configs |
| Rich text editing | Lexical editor (default); customize features via `lexicalEditor({ features })` |
| Media uploads to S3/R2 | `@payloadcms/storage-s3` or `@payloadcms/storage-vercel-blob` |
| Need GraphQL API | Enable via `@payloadcms/graphql` plugin |
| Multi-tenant app | Use access control returning query constraints per tenant |
| Database choice | Postgres (recommended) or MongoDB via `@payloadcms/db-mongodb` |
| Content versioning | `versions: { drafts: true, maxPerDoc: 25 }` on collections |


---

## From `sanity`

> Sanity.io CMS, GROQ queries, structured content modeling, real-time collaboration, and Sanity Studio customization

# Sanity.io CMS

## Purpose

Model, manage, and deliver structured content using Sanity.io. Covers schema definition, GROQ query language, Sanity Studio customization, Portable Text rendering, real-time content collaboration, image handling with the Sanity CDN, and integration with frontend frameworks (primarily Next.js).

## Core Patterns

### Project Structure

```
sanity-project/
  sanity/
    schemaTypes/
      post.ts
      author.ts
      category.ts
      blockContent.ts
      index.ts          # Schema registry
    lib/
      client.ts         # Sanity client instance
      queries.ts        # GROQ queries
      image.ts          # Image URL builder
    sanity.config.ts    # Studio configuration
    sanity.cli.ts       # CLI configuration
  app/                  # Next.js app (if embedded)
```

### Schema Definition

```typescript
// sanity/schemaTypes/post.ts
import { defineField, defineType } from "sanity";

export const post = defineType({
  name: "post",
  title: "Post",
  type: "document",
  fields: [
    defineField({
      name: "title",
      title: "Title",
      type: "string",
      validation: (rule) => rule.required().min(5).max(120),
    }),
    defineField({
      name: "slug",
      title: "Slug",
      type: "slug",
      options: { source: "title", maxLength: 96 },
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: "author",
      title: "Author",
      type: "reference",
      to: [{ type: "author" }],
    }),
    defineField({
      name: "mainImage",
      title: "Main Image",
      type: "image",
      options: { hotspot: true }, // Enable focal point cropping
      fields: [
        defineField({
          name: "alt",
          title: "Alt Text",
          type: "string",
          validation: (rule) => rule.required(),
        }),
      ],
    }),
    defineField({
      name: "categories",
      title: "Categories",
      type: "array",
      of: [{ type: "reference", to: [{ type: "category" }] }],
    }),
    defineField({
      name: "publishedAt",
      title: "Published At",
      type: "datetime",
    }),
    defineField({
      name: "body",
      title: "Body",
      type: "blockContent", // Custom Portable Text
    }),
    defineField({
      name: "seo",
      title: "SEO",
      type: "object",
      fields: [
        defineField({ name: "metaTitle", type: "string" }),
        defineField({ name: "metaDescription", type: "text", rows: 3 }),
      ],
    }),
  ],
  preview: {
    select: {
      title: "title",
      author: "author.name",
      media: "mainImage",
    },
    prepare({ title, author, media }) {
      return {
        title,
        subtitle: author ? `by ${author}` : "No author",
        media,
      };
    },
  },
  orderings: [
    {
      title: "Publish Date, New",
      name: "publishedAtDesc",
      by: [{ field: "publishedAt", direction: "desc" }],
    },
  ],
});
```

```typescript
// sanity/schemaTypes/blockContent.ts — Custom Portable Text
import { defineType, defineArrayMember } from "sanity";

export const blockContent = defineType({
  name: "blockContent",
  title: "Block Content",
  type: "array",
  of: [
    defineArrayMember({
      type: "block",
      styles: [
        { title: "Normal", value: "normal" },
        { title: "H2", value: "h2" },
        { title: "H3", value: "h3" },
        { title: "Quote", value: "blockquote" },
      ],
      marks: {
        decorators: [
          { title: "Bold", value: "strong" },
          { title: "Italic", value: "em" },
          { title: "Code", value: "code" },
        ],
        annotations: [
          {
            name: "link",
            type: "object",
            title: "URL",
            fields: [
              { name: "href", type: "url", title: "URL" },
              { name: "blank", type: "boolean", title: "Open in new tab" },
            ],
          },
        ],
      },
    }),
    defineArrayMember({ type: "image", options: { hotspot: true } }),
    defineArrayMember({
      name: "codeBlock",
      title: "Code Block",
      type: "object",
      fields: [
        { name: "language", type: "string", options: { list: ["typescript", "javascript", "css", "bash"] } },
        { name: "code", type: "text" },
      ],
    }),
  ],
});
```

### GROQ Queries

```typescript
// sanity/lib/queries.ts
import { groq } from "next-sanity";

// Fetch all published posts
export const postsQuery = groq`
  *[_type == "post" && defined(slug.current)] | order(publishedAt desc) {
    _id,
    title,
    slug,
    publishedAt,
    "excerpt": array::join(string::split(pt::text(body), "")[0..200], "") + "...",
    mainImage {
      asset->{
        _id,
        url,
        metadata { dimensions, lqip }
      },
      alt,
      hotspot
    },
    "author": author->{name, slug, image},
    "categories": categories[]->{ _id, title, slug }
  }
`;

// Single post by slug
export const postBySlugQuery = groq`
  *[_type == "post" && slug.current == $slug][0] {
    _id,
    title,
    slug,
    publishedAt,
    body,
    mainImage { asset->{ url, metadata { dimensions, lqip } }, alt },
    "author": author->{ name, slug, image, bio },
    "categories": categories[]->{ _id, title, slug },
    "related": *[
      _type == "post"
      && _id != ^._id
      && count(categories[@._ref in ^.^.categories[]._ref]) > 0
    ] | order(publishedAt desc) [0..2] {
      title, slug, mainImage { asset->{ url }, alt }
    }
  }
`;

// Paginated list
export const paginatedPostsQuery = groq`
  *[_type == "post" && defined(slug.current)] | order(publishedAt desc) [$start..$end] {
    _id, title, slug, publishedAt,
    mainImage { asset->{ url, metadata { lqip } }, alt }
  }
`;

// Count for pagination
export const postCountQuery = groq`count(*[_type == "post" && defined(slug.current)])`;

// Full-text search
export const searchQuery = groq`
  *[_type == "post" && (
    title match $query + "*" ||
    pt::text(body) match $query + "*"
  )] | order(publishedAt desc) [0..9] {
    _id, title, slug, publishedAt
  }
`;
```

### Sanity Client Setup

```typescript
// sanity/lib/client.ts
import { createClient, type QueryParams } from "next-sanity";
import imageUrlBuilder from "@sanity/image-url";
import type { SanityImageSource } from "@sanity/image-url/lib/types/types";

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET ?? "production",
  apiVersion: "2024-12-01", // Use a fixed date, not "vX"
  useCdn: process.env.NODE_ENV === "production",
});

// Revalidation-aware fetch for Next.js App Router
export async function sanityFetch<T>({
  query,
  params = {},
  tags = [],
}: {
  query: string;
  params?: QueryParams;
  tags?: string[];
}): Promise<T> {
  return client.fetch<T>(query, params, {
    next: {
      revalidate: tags.length ? false : 60,
      tags,
    },
  });
}

// Image URL builder
const builder = imageUrlBuilder(client);

export function urlFor(source: SanityImageSource) {
  return builder.image(source);
}
```

### Next.js Integration

```tsx
// app/blog/page.tsx
import { sanityFetch } from "@/sanity/lib/client";
import { postsQuery } from "@/sanity/lib/queries";
import { PostCard } from "@/components/post-card";

export default async function BlogPage() {
  const posts = await sanityFetch<Post[]>({
    query: postsQuery,
    tags: ["post"],
  });

  return (
    <section className="py-16">
      <h1 className="text-4xl font-bold mb-8">Blog</h1>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {posts.map((post) => (
          <PostCard key={post._id} post={post} />
        ))}
      </div>
    </section>
  );
}
```

```typescript
// app/api/revalidate/route.ts — Webhook handler for on-demand revalidation
import { revalidateTag } from "next/cache";
import { type NextRequest, NextResponse } from "next/server";
import { parseBody } from "next-sanity/webhook";

export async function POST(req: NextRequest) {
  const { isValidSignature, body } = await parseBody<{
    _type: string;
    slug?: { current?: string };
  }>(req, process.env.SANITY_WEBHOOK_SECRET!);

  if (!isValidSignature) {
    return NextResponse.json({ message: "Invalid signature" }, { status: 401 });
  }

  if (body?._type) {
    revalidateTag(body._type);
  }

  return NextResponse.json({ revalidated: true, now: Date.now() });
}
```

### Sanity Studio Configuration

```typescript
// sanity.config.ts
import { defineConfig } from "sanity";
import { structureTool } from "sanity/structure";
import { visionTool } from "@sanity/vision";
import { schemaTypes } from "./sanity/schemaTypes";

export default defineConfig({
  name: "default",
  title: "My Studio",
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET ?? "production",
  plugins: [
    structureTool({
      structure: (S) =>
        S.list()
          .title("Content")
          .items([
            S.listItem()
              .title("Posts")
              .child(
                S.documentList()
                  .title("Posts")
                  .filter('_type == "post"')
                  .defaultOrdering([{ field: "publishedAt", direction: "desc" }])
              ),
            S.divider(),
            ...S.documentTypeListItems().filter(
              (item) => !["post"].includes(item.getId()!)
            ),
          ]),
    }),
    visionTool({ defaultApiVersion: "2024-12-01" }),
  ],
  schema: { types: schemaTypes },
});
```

## Best Practices

- **Fix `apiVersion` to a date** — never use `"v1"` or `"v2023-08-01"`; use `"2024-12-01"` style dates
- **Use `next-sanity`** for Next.js projects — it provides `sanityFetch`, visual editing, and webhook parsing
- **Colocate GROQ queries** — keep queries in a dedicated file near the client, not scattered across components
- **Enable `useCdn: true`** in production for fast reads; disable for previews and mutations
- **Use webhook revalidation** — set up a Sanity webhook to hit `/api/revalidate` for instant cache invalidation
- **Use `hotspot: true`** on image fields — lets editors pick focal points for responsive cropping
- **Define `preview`** on all document types — makes the Studio list views useful for editors
- **Use Portable Text** for rich content — it's structured JSON, not HTML, so it's portable across platforms
- **Type your queries** — generate TypeScript types from schemas with `sanity typegen generate`

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|---|---|---|
| Fetching all fields with `*[_type == "post"]` | Over-fetches data, slow responses | Project only the fields you need |
| Using `_updatedAt` for cache keys | Changes on every edit, defeats caching | Use webhook revalidation with tags |
| Storing HTML in text fields | Loses structured content benefits | Use Portable Text (`blockContent`) |
| Hardcoding project ID in code | Breaks across environments | Use environment variables |
| Skipping `alt` on images | Accessibility violation | Add `alt` field with required validation |
| Deep nesting references in GROQ | N+1 query explosion | Dereference with `->` in a single query |
| Using `apiVersion: "v1"` | Stuck on legacy API behavior | Pin to a recent date string |

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Content-heavy site with editors | Sanity Studio with custom structure |
| Blog with Next.js | `next-sanity` + ISR with webhook revalidation |
| E-commerce product pages | Sanity for content + Shopify/Stripe for transactions |
| Multi-language content | Use `@sanity/document-internationalization` plugin |
| Complex page builder | `blockContent` with custom block types |
| Real-time collaborative editing | Built into Sanity — no extra setup needed |
| Need GraphQL instead of GROQ | Enable GraphQL API in project settings, but prefer GROQ |
| Type-safe queries | Run `sanity typegen generate` for auto-generated types |


---

## From `contentlayer`

> Content layer and MDX content management for Next.js, including Contentlayer2, content collections, and MDX processing

# Contentlayer / MDX Content Management

## Purpose

Manage file-based content (Markdown/MDX) as type-safe data in Next.js applications. Covers Contentlayer 2 (community fork), raw MDX with `next-mdx-remote` or `@next/mdx`, content collections patterns, frontmatter handling, custom MDX components, and alternatives like Fumadocs and Velite for documentation sites.

## Core Patterns

### Contentlayer 2 Configuration

```typescript
// contentlayer.config.ts
import { defineDocumentType, makeSource } from "contentlayer2/source-files";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypePrettyCode from "rehype-pretty-code";
import remarkGfm from "remark-gfm";

export const Post = defineDocumentType(() => ({
  name: "Post",
  filePathPattern: "posts/**/*.mdx",
  contentType: "mdx",
  fields: {
    title: { type: "string", required: true },
    description: { type: "string", required: true },
    date: { type: "date", required: true },
    published: { type: "boolean", default: true },
    image: { type: "string" },
    authors: { type: "list", of: { type: "string" }, required: true },
    tags: { type: "list", of: { type: "string" }, default: [] },
  },
  computedFields: {
    slug: {
      type: "string",
      resolve: (doc) => doc._raw.flattenedPath.replace("posts/", ""),
    },
    readingTime: {
      type: "number",
      resolve: (doc) => Math.ceil(doc.body.raw.split(/\s+/).length / 200),
    },
    url: {
      type: "string",
      resolve: (doc) => `/blog/${doc._raw.flattenedPath.replace("posts/", "")}`,
    },
  },
}));

export const Doc = defineDocumentType(() => ({
  name: "Doc",
  filePathPattern: "docs/**/*.mdx",
  contentType: "mdx",
  fields: {
    title: { type: "string", required: true },
    description: { type: "string" },
    order: { type: "number", default: 999 },
    section: { type: "string" },
  },
  computedFields: {
    slug: {
      type: "string",
      resolve: (doc) => doc._raw.flattenedPath.replace("docs/", ""),
    },
  },
}));

export default makeSource({
  contentDirPath: "content",
  documentTypes: [Post, Doc],
  mdx: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [rehypePrettyCode, { theme: "github-dark-dimmed", keepBackground: false }],
      [rehypeAutolinkHeadings, { behavior: "wrap" }],
    ],
  },
});
```

### Content Directory Structure

```
content/
  posts/
    getting-started.mdx
    advanced-patterns.mdx
    2024/
      yearly-review.mdx
  docs/
    introduction.mdx
    installation.mdx
    api-reference.mdx
```

### MDX File Format

```mdx
---
title: "Building Type-Safe Content Pipelines"
description: "How to use Contentlayer with Next.js for fully typed MDX content"
date: 2024-11-15
published: true
authors: ["alice"]
tags: ["nextjs", "mdx", "typescript"]
image: "/images/content-pipeline.jpg"
---

## Introduction

This is standard markdown with **bold** and _italic_ support.

<Callout type="info">
  This is a custom MDX component rendered inline with markdown.
</Callout>

### Code Example

```tsx
export function Component() {
  return <div>Hello from MDX</div>;
}
```

<Steps>
  <Step title="Install dependencies">
    Run `pnpm add contentlayer2 next-contentlayer2`
  </Step>
  <Step title="Create config">
    Add `contentlayer.config.ts` to your project root.
  </Step>
</Steps>
```

### Next.js Integration

```typescript
// next.config.ts
import { withContentlayer } from "next-contentlayer2";

const nextConfig = {
  reactStrictMode: true,
};

export default withContentlayer(nextConfig);
```

```tsx
// app/blog/page.tsx
import { allPosts } from "contentlayer/generated";
import { compareDesc } from "date-fns";
import Link from "next/link";

export default function BlogPage() {
  const posts = allPosts
    .filter((post) => post.published)
    .sort((a, b) => compareDesc(new Date(a.date), new Date(b.date)));

  return (
    <section className="py-16 max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold mb-8">Blog</h1>
      <div className="space-y-6">
        {posts.map((post) => (
          <article key={post.slug} className="p-6 rounded-xl shadow-sm border">
            <Link href={post.url}>
              <h2 className="text-xl font-semibold hover:underline">{post.title}</h2>
            </Link>
            <p className="text-sm text-gray-500 mt-1">
              {new Date(post.date).toLocaleDateString()} · {post.readingTime} min read
            </p>
            <p className="mt-2 text-gray-700">{post.description}</p>
            <div className="flex gap-2 mt-3">
              {post.tags.map((tag) => (
                <span key={tag} className="px-2 py-1 text-xs rounded-full bg-gray-100">
                  {tag}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
```

```tsx
// app/blog/[slug]/page.tsx
import { allPosts } from "contentlayer/generated";
import { notFound } from "next/navigation";
import { useMDXComponent } from "next-contentlayer2/hooks";
import { mdxComponents } from "@/components/mdx-components";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return allPosts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const post = allPosts.find((p) => p.slug === slug);
  if (!post) return {};
  return {
    title: post.title,
    description: post.description,
    openGraph: { images: post.image ? [post.image] : [] },
  };
}

export default async function PostPage({ params }: Props) {
  const { slug } = await params;
  const post = allPosts.find((p) => p.slug === slug);
  if (!post) notFound();

  return (
    <article className="py-16 max-w-3xl mx-auto prose prose-lg dark:prose-invert">
      <h1>{post.title}</h1>
      <time className="text-sm text-gray-500">{new Date(post.date).toLocaleDateString()}</time>
      <MDXContent code={post.body.code} />
    </article>
  );
}

function MDXContent({ code }: { code: string }) {
  const Component = useMDXComponent(code);
  return <Component components={mdxComponents} />;
}
```

### Custom MDX Components

```tsx
// components/mdx-components.tsx
import type { MDXComponents } from "mdx/types";
import Image from "next/image";
import Link from "next/link";

function Callout({ type = "info", children }: { type?: "info" | "warning" | "error"; children: React.ReactNode }) {
  const styles = {
    info: "bg-blue-50 border-blue-200 text-blue-900 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-100",
    warning: "bg-amber-50 border-amber-200 text-amber-900 dark:bg-amber-950 dark:border-amber-800 dark:text-amber-100",
    error: "bg-red-50 border-red-200 text-red-900 dark:bg-red-950 dark:border-red-800 dark:text-red-100",
  };
  return (
    <div className={`p-6 rounded-xl border my-6 ${styles[type]}`}>
      {children}
    </div>
  );
}

function Steps({ children }: { children: React.ReactNode }) {
  return <div className="space-y-4 my-6 border-l-2 border-gray-200 pl-6">{children}</div>;
}

function Step({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h4 className="font-semibold text-base">{title}</h4>
      <div className="text-gray-600 mt-1">{children}</div>
    </div>
  );
}

export const mdxComponents: MDXComponents = {
  Callout,
  Steps,
  Step,
  a: ({ href, children, ...props }) => {
    if (href?.startsWith("/")) return <Link href={href} {...props}>{children}</Link>;
    return <a href={href} target="_blank" rel="noopener noreferrer" {...props}>{children}</a>;
  },
  img: ({ src, alt, ...props }) => (
    <Image src={src ?? ""} alt={alt ?? ""} width={800} height={400} className="rounded-xl" {...props} />
  ),
};
```

### Alternative: next-mdx-remote (No Contentlayer)

```tsx
// For projects that don't want a build plugin
import { compileMDX } from "next-mdx-remote/rsc";
import { readFile } from "fs/promises";
import { join } from "path";
import matter from "gray-matter";

async function getPost(slug: string) {
  const filePath = join(process.cwd(), "content/posts", `${slug}.mdx`);
  const raw = await readFile(filePath, "utf-8");
  const { content, data: frontmatter } = matter(raw);

  const { content: mdxContent } = await compileMDX({
    source: content,
    options: {
      parseFrontmatter: false,
      mdxOptions: {
        remarkPlugins: [remarkGfm],
        rehypePlugins: [rehypeSlug, rehypePrettyCode],
      },
    },
    components: mdxComponents,
  });

  return { content: mdxContent, frontmatter };
}
```

### Alternative: Velite (Contentlayer Successor)

```typescript
// velite.config.ts — Velite is a modern alternative to Contentlayer
import { defineConfig, defineCollection, s } from "velite";

const posts = defineCollection({
  name: "Post",
  pattern: "posts/**/*.mdx",
  schema: s.object({
    title: s.string().max(120),
    description: s.string().max(300),
    date: s.isodate(),
    published: s.boolean().default(true),
    tags: s.array(s.string()).default([]),
    body: s.mdx(),
    slug: s.slug("posts"),
    metadata: s.metadata(),
  }),
});

export default defineConfig({
  root: "content",
  collections: { posts },
});
```

## Best Practices

- **Type everything** — Contentlayer generates TypeScript types; use them in all components
- **Compute derived fields** — reading time, slugs, URLs belong in `computedFields`, not in frontmatter
- **Use rehype/remark plugins** — syntax highlighting, slug headings, GFM support via the plugin pipeline
- **Create reusable MDX components** — `Callout`, `Steps`, `CodeGroup`, `Tabs` for rich documentation
- **Generate static params** — use `generateStaticParams` from the generated collection for full static generation
- **Validate frontmatter** — required fields catch missing metadata at build time, not runtime
- **Keep content in `content/`** — separate content from app code; makes it easy to move to a CMS later
- **Use `prose` typography** — Tailwind's `@tailwindcss/typography` plugin handles MDX rendering beautifully

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|---|---|---|
| Storing slugs in frontmatter | Duplicates file path info, can drift | Compute from `_raw.flattenedPath` |
| Inline styles in MDX files | Hard to maintain, inconsistent | Use MDX components with Tailwind classes |
| Fetching content at request time | Unnecessary for static content | Use `generateStaticParams` for SSG |
| No syntax highlighting plugin | Raw `<code>` blocks look terrible | Add `rehype-pretty-code` or `shiki` |
| Skipping frontmatter validation | Missing fields cause runtime errors | Set `required: true` on critical fields |
| Giant MDX files (1000+ lines) | Slow to parse, hard to edit | Split into sections or use content refs |
| No `generateMetadata` for posts | Poor SEO, no social previews | Export metadata from frontmatter fields |

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Blog with Next.js App Router | Contentlayer 2 or Velite for type-safe MDX |
| Documentation site | Fumadocs (built on Contentlayer) or Nextra |
| Simple markdown, no build plugin | `next-mdx-remote/rsc` with `gray-matter` |
| Content from CMS + local MDX | Sanity for dynamic, Contentlayer for static |
| Astro project | Use Astro's built-in content collections instead |
| Need syntax highlighting | `rehype-pretty-code` with Shiki themes |
| Migration from Contentlayer v1 | Switch to `contentlayer2` (community fork) — drop-in compatible |
| Heavy interactive content | Consider a CMS; MDX is best for mostly-text content |


---

## From `mdx`

> MDX authoring, compilation, component mapping, remark/rehype plugins, and integration with Next.js App Router

# MDX Authoring & Compilation

## Purpose

Provide expert guidance on MDX -- Markdown with embedded JSX -- covering compilation toolchains, component mapping, remark/rehype plugin ecosystems, syntax highlighting, and integration with Next.js App Router (RSC-compatible approaches). This skill focuses on building production content pipelines for blogs, documentation, and knowledge bases.

## Compilation Toolchains

### Choosing a Toolchain

| Tool | Best For | RSC Support | Bundle Size | Maintained |
|------|----------|-------------|-------------|------------|
| `next-mdx-remote` | Remote/dynamic MDX, CMS content | Yes (v5+) | Small | Active |
| `@next/mdx` | Local `.mdx` files as pages/routes | Yes | Zero runtime | Active |
| `mdx-bundler` | Full bundling with imports in MDX | No (client) | Medium | Stale |
| Contentlayer2 | Type-safe content with schema validation | Yes | Medium | Fork active |
| Velite | Contentlayer alternative, Zod schemas | Yes | Small | Active |

**Recommendation:** Use `next-mdx-remote` for dynamic content or `@next/mdx` for file-based routing. For type-safe content collections, use Velite.

### next-mdx-remote (Recommended for Dynamic Content)

```bash
npm install next-mdx-remote gray-matter
```

**RSC usage (Next.js App Router):**

```tsx
// lib/mdx.ts
import fs from 'node:fs/promises';
import path from 'node:path';
import matter from 'gray-matter';

const CONTENT_DIR = path.join(process.cwd(), 'content');

export async function getPost(slug: string) {
  const filePath = path.join(CONTENT_DIR, `${slug}.mdx`);
  const source = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content } = matter(source);
  return { frontmatter, content, slug };
}

export async function getAllPosts() {
  const files = await fs.readdir(CONTENT_DIR);
  const posts = await Promise.all(
    files
      .filter(f => f.endsWith('.mdx'))
      .map(f => getPost(f.replace(/\.mdx$/, '')))
  );
  return posts.sort(
    (a, b) =>
      new Date(b.frontmatter.date).getTime() -
      new Date(a.frontmatter.date).getTime()
  );
}
```

```tsx
// app/blog/[slug]/page.tsx
import { MDXRemote } from 'next-mdx-remote/rsc';
import { getPost, getAllPosts } from '@/lib/mdx';
import { mdxComponents } from '@/components/mdx-components';
import remarkGfm from 'remark-gfm';
import rehypePrettyCode from 'rehype-pretty-code';
import rehypeSlug from 'rehype-slug';

export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map(post => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { frontmatter } = await getPost(slug);
  return {
    title: frontmatter.title,
    description: frontmatter.description,
  };
}

export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { content, frontmatter } = await getPost(slug);

  return (
    <article className="py-16 max-w-3xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight">{frontmatter.title}</h1>
        <time className="text-base text-gray-500 mt-4 block">
          {new Date(frontmatter.date).toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric',
          })}
        </time>
      </header>
      <div className="prose prose-lg dark:prose-invert max-w-none">
        <MDXRemote
          source={content}
          components={mdxComponents}
          options={{
            mdxOptions: {
              remarkPlugins: [remarkGfm],
              rehypePlugins: [
                rehypeSlug,
                [rehypePrettyCode, { theme: 'github-dark-dimmed', keepBackground: true }],
              ],
            },
          }}
        />
      </div>
    </article>
  );
}
```

**Alternative: `compileMDX` for more control:**

```tsx
// lib/mdx.ts
import { compileMDX } from 'next-mdx-remote/rsc';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypePrettyCode from 'rehype-pretty-code';

interface Frontmatter {
  title: string;
  description: string;
  date: string;
  author: string;
  tags: string[];
  image?: string;
}

export async function compileMDXContent(source: string) {
  const { content, frontmatter } = await compileMDX<Frontmatter>({
    source,
    components: mdxComponents,
    options: {
      parseFrontmatter: true,
      mdxOptions: {
        remarkPlugins: [remarkGfm],
        rehypePlugins: [
          rehypeSlug,
          [rehypePrettyCode, { theme: 'github-dark-dimmed' }],
        ],
      },
    },
  });

  return { content, frontmatter };
}
```

### @next/mdx (For File-Based MDX Pages)

```bash
npm install @next/mdx @mdx-js/loader @mdx-js/react
```

```js
// next.config.mjs
import createMDX from '@next/mdx';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypePrettyCode from 'rehype-pretty-code';

const withMDX = createMDX({
  options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [rehypePrettyCode, { theme: 'github-dark-dimmed', keepBackground: false }],
    ],
  },
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
};

export default withMDX(nextConfig);
```

```tsx
// mdx-components.tsx (project root — required by @next/mdx)
import type { MDXComponents } from 'mdx/types';
import { mdxComponents } from '@/components/mdx-components';

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return { ...components, ...mdxComponents };
}
```

Then place `.mdx` files directly in `app/` as pages:

```
app/
  docs/
    getting-started.mdx   # becomes /docs/getting-started
    api-reference.mdx      # becomes /docs/api-reference
```

### mdx-bundler (Advanced: Imports Inside MDX)

Use only when MDX files need to import local modules (images, data files). Client-only -- not RSC-compatible.

```bash
npm install mdx-bundler esbuild
```

```typescript
// lib/mdx-bundler.ts
import { bundleMDX } from 'mdx-bundler';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import path from 'path';

export async function bundleMDXContent(source: string, cwd?: string) {
  const { code, frontmatter } = await bundleMDX({
    source,
    cwd: cwd ?? path.join(process.cwd(), 'content'),
    mdxOptions(options) {
      options.remarkPlugins = [...(options.remarkPlugins ?? []), remarkGfm];
      options.rehypePlugins = [
        ...(options.rehypePlugins ?? []),
        rehypeSlug,
        [rehypeAutolinkHeadings, { behavior: 'wrap' }],
      ];
      return options;
    },
    esbuildOptions(options) {
      options.loader = { ...options.loader, '.png': 'dataurl', '.jpg': 'dataurl' };
      return options;
    },
  });

  return { code, frontmatter };
}
```

```tsx
// Client component to render bundled MDX
'use client';

import { useMemo } from 'react';
import { getMDXComponent } from 'mdx-bundler/client';

export function MDXRenderer({ code }: { code: string }) {
  const Component = useMemo(() => getMDXComponent(code), [code]);
  return <Component components={mdxComponents} />;
}
```

### Velite (Type-Safe Content Collections)

```bash
npm install velite
```

```ts
// velite.config.ts
import { defineConfig, defineCollection, s } from 'velite';

const posts = defineCollection({
  name: 'Post',
  pattern: 'posts/**/*.mdx',
  schema: s.object({
    title: s.string().max(200),
    description: s.string().max(500),
    date: s.isodate(),
    tags: s.array(s.string()).default([]),
    published: s.boolean().default(true),
    slug: s.slug('posts'),
    body: s.mdx(), // compiled MDX
  }),
});

export default defineConfig({
  root: 'content',
  output: { data: '.velite', assets: 'public/static' },
  collections: { posts },
});
```

## Component Mapping

### Building a Component Map

```tsx
// components/mdx-components.tsx
import Image from 'next/image';
import Link from 'next/link';
import type { MDXComponents } from 'mdx/types';
import { Callout } from '@/components/mdx/callout';
import { CodeTabs } from '@/components/mdx/code-tabs';

export const mdxComponents: MDXComponents = {
  // Override default HTML elements
  h1: ({ children, id }) => (
    <h1 id={id} className="text-4xl font-bold tracking-tight mt-12 mb-6 scroll-mt-24">
      {children}
    </h1>
  ),
  h2: ({ children, id }) => (
    <h2 id={id} className="text-2xl font-semibold mt-10 mb-4 scroll-mt-24 border-b border-border pb-2">
      {children}
    </h2>
  ),
  h3: ({ children, id }) => (
    <h3 id={id} className="text-xl font-semibold mt-8 mb-3 scroll-mt-24">
      {children}
    </h3>
  ),
  p: ({ children }) => (
    <p className="text-base leading-7 text-text-secondary mb-4">{children}</p>
  ),
  a: ({ href, children }) => {
    const isExternal = href?.startsWith('http');
    if (isExternal) {
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-brand-600 underline underline-offset-4 transition-colors duration-200 hover:text-brand-700"
        >
          {children}
        </a>
      );
    }
    return (
      <Link
        href={href ?? '#'}
        className="text-brand-600 underline underline-offset-4 transition-colors duration-200 hover:text-brand-700"
      >
        {children}
      </Link>
    );
  },
  img: ({ src, alt, width, height }) => (
    <Image
      src={src ?? ''}
      alt={alt ?? ''}
      width={Number(width) || 800}
      height={Number(height) || 450}
      className="rounded-xl my-6 shadow-sm"
      sizes="(max-width: 768px) 100vw, 700px"
    />
  ),
  pre: ({ children }) => (
    <pre className="rounded-xl bg-gray-950 p-6 my-6 overflow-x-auto text-sm leading-relaxed shadow-sm">
      {children}
    </pre>
  ),
  code: ({ children, className }) => {
    // Inline code (no className) vs code blocks (has className from rehype)
    if (!className) {
      return (
        <code className="rounded-md bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 text-sm font-mono text-brand-600">
          {children}
        </code>
      );
    }
    return <code className={className}>{children}</code>;
  },
  blockquote: ({ children }) => (
    <blockquote className="border-l-4 border-brand-500 pl-6 py-2 my-6 text-text-secondary italic">
      {children}
    </blockquote>
  ),
  table: ({ children }) => (
    <div className="my-6 overflow-x-auto rounded-xl border border-border shadow-sm">
      <table className="w-full text-base">{children}</table>
    </div>
  ),
  th: ({ children }) => (
    <th className="border-b-2 border-border bg-gray-50 dark:bg-gray-800 px-4 py-3 text-left font-semibold">
      {children}
    </th>
  ),
  td: ({ children }) => (
    <td className="border-b border-border px-4 py-3">{children}</td>
  ),
  ul: ({ children }) => (
    <ul className="list-disc pl-6 my-4 space-y-2 text-text-secondary">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-6 my-4 space-y-2 text-text-secondary">{children}</ol>
  ),
  hr: () => <hr className="my-8 border-border" />,

  // Custom components available in MDX files
  Callout,
  CodeTabs,
  Image: (props: React.ComponentProps<typeof Image>) => (
    <Image {...props} className="rounded-xl my-8" />
  ),
};
```

### Custom MDX Components

**Callout / Admonition:**

```tsx
// components/mdx/callout.tsx
import { cn } from '@/lib/utils';

type CalloutVariant = 'info' | 'warning' | 'error' | 'success';

const variants: Record<CalloutVariant, { bg: string; border: string; icon: string }> = {
  info: { bg: 'bg-blue-50 dark:bg-blue-950', border: 'border-blue-200 dark:border-blue-800', icon: 'i' },
  warning: { bg: 'bg-amber-50 dark:bg-amber-950', border: 'border-amber-200 dark:border-amber-800', icon: '!' },
  error: { bg: 'bg-red-50 dark:bg-red-950', border: 'border-red-200 dark:border-red-800', icon: 'x' },
  success: { bg: 'bg-green-50 dark:bg-green-950', border: 'border-green-200 dark:border-green-800', icon: '+' },
};

export function Callout({
  variant = 'info',
  title,
  children,
}: {
  variant?: CalloutVariant;
  title?: string;
  children: React.ReactNode;
}) {
  const v = variants[variant];
  return (
    <div className={cn('my-6 rounded-xl border p-6', v.bg, v.border)} role="note">
      {title && <p className="font-semibold text-base mb-2">{title}</p>}
      <div className="text-base leading-relaxed [&>p]:mb-0">{children}</div>
    </div>
  );
}
```

**Code Tabs (client component):**

```tsx
// components/mdx/code-tabs.tsx
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

export function CodeTabs({
  tabs,
}: {
  tabs: { label: string; content: React.ReactNode }[];
}) {
  const [active, setActive] = useState(0);

  return (
    <div className="my-6 rounded-xl border border-border shadow-sm overflow-hidden">
      <div className="flex border-b border-border bg-gray-50 dark:bg-gray-800">
        {tabs.map((tab, i) => (
          <button
            key={tab.label}
            onClick={() => setActive(i)}
            className={cn(
              'px-6 py-4 text-base font-medium transition-all duration-200',
              'focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-brand-500 focus-visible:outline-none',
              i === active
                ? 'text-brand-600 border-b-2 border-brand-600 bg-white dark:bg-gray-900'
                : 'text-text-secondary hover:text-text-primary'
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="[&>pre]:my-0 [&>pre]:rounded-none">{tabs[active].content}</div>
    </div>
  );
}
```

**Usage in MDX:**

```mdx
<Callout variant="warning" title="Breaking Change">
  The `getData` API has been renamed to `fetchData` in v2.0.
</Callout>
```

## Frontmatter Parsing

### gray-matter with Zod Validation

```bash
npm install gray-matter zod
```

```tsx
// lib/frontmatter.ts
import matter from 'gray-matter';
import { z } from 'zod';

const PostFrontmatterSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().min(1).max(500),
  date: z.coerce.date(),
  tags: z.array(z.string()).default([]),
  published: z.boolean().default(true),
  image: z.string().optional(),
  author: z.string().optional(),
  draft: z.boolean().default(false),
});

export type PostFrontmatter = z.infer<typeof PostFrontmatterSchema>;

export function parseFrontmatter(raw: string) {
  const { data, content } = matter(raw);
  const frontmatter = PostFrontmatterSchema.parse(data);
  return { frontmatter, content };
}
```

**Frontmatter template:**

```mdx
---
title: "Building a Blog with MDX and Next.js"
description: "A step-by-step guide to setting up MDX content in the App Router"
date: 2025-03-01
tags: ["mdx", "nextjs", "react"]
published: true
image: /images/blog/mdx-setup.png
author: "Your Name"
---

Content starts here...
```

## Remark & Rehype Plugin Ecosystem

### Essential Plugins

```bash
npm install remark-gfm rehype-slug rehype-autolink-headings rehype-pretty-code remark-math rehype-katex
```

| Plugin | Purpose | Phase |
|--------|---------|-------|
| `remark-gfm` | Tables, strikethrough, task lists, autolinks | Remark |
| `remark-math` | Math expressions (`$...$`, `$$...$$`) | Remark |
| `remark-unwrap-images` | Remove wrapping `<p>` around images | Remark |
| `rehype-slug` | Add `id` attributes to headings | Rehype |
| `rehype-autolink-headings` | Add anchor links to headings | Rehype |
| `rehype-pretty-code` | Shiki-based syntax highlighting | Rehype |
| `rehype-katex` | Render math as KaTeX | Rehype |
| `rehype-external-links` | Add `target="_blank"` to external links | Rehype |

**Plugin order matters.** Remark plugins process the Markdown AST (mdast), rehype plugins process the HTML AST (hast). Within each phase, order is sequential:

```ts
const mdxOptions = {
  remarkPlugins: [
    remarkGfm,
    remarkMath,
    remarkUnwrapImages,
  ],
  rehypePlugins: [
    rehypeSlug,                           // Must come before autolink-headings
    [rehypeAutolinkHeadings, { behavior: 'wrap' }],
    [rehypePrettyCode, {
      theme: 'github-dark-dimmed',
      keepBackground: true,
      defaultLang: 'plaintext',
    }],
    [rehypeExternalLinks, { target: '_blank', rel: ['noopener', 'noreferrer'] }],
  ],
};
```

### Writing a Custom Remark Plugin

```ts
// lib/remark-reading-time.ts
import { visit } from 'unist-util-visit';
import type { Root } from 'mdast';

const WORDS_PER_MINUTE = 200;

export function remarkReadingTime() {
  return (tree: Root, file: { data: Record<string, unknown> }) => {
    let textContent = '';
    visit(tree, ['text', 'code'], (node: any) => {
      textContent += node.value ?? '';
    });

    const words = textContent.split(/\s+/).filter(Boolean).length;
    const minutes = Math.max(1, Math.round(words / WORDS_PER_MINUTE));

    file.data.readingTime = `${minutes} min read`;
  };
}
```

## Syntax Highlighting

### rehype-pretty-code + Shiki (Recommended)

Zero client JavaScript. Highlights at compile time using Shiki.

```bash
npm install rehype-pretty-code shiki
```

```ts
// lib/mdx-options.ts
import type { Options as PrettyCodeOptions } from 'rehype-pretty-code';

export const prettyCodeOptions: PrettyCodeOptions = {
  theme: {
    dark: 'github-dark-dimmed',
    light: 'github-light',
  },
  keepBackground: true,
  defaultLang: 'plaintext',
  onVisitLine(node) {
    // Prevent empty lines from collapsing
    if (node.children.length === 0) {
      node.children = [{ type: 'text', value: ' ' }];
    }
  },
  onVisitHighlightedLine(node) {
    node.properties.className = [...(node.properties.className || []), 'highlighted'];
  },
  onVisitHighlightedChars(node) {
    node.properties.className = ['word-highlight'];
  },
};
```

**MDX syntax for line/word highlighting:**

````mdx
```js {1,3-5}
// Line 1 is highlighted
const a = 1;
const b = 2;  // Lines 3-5 highlighted
const c = 3;
const d = 4;
```

```js /useState/
// The word "useState" is highlighted inline
const [count, setCount] = useState(0);
```
````

**CSS for highlighted code blocks:**

```css
/* globals.css */
[data-rehype-pretty-code-figure] pre {
  @apply p-6 rounded-xl overflow-x-auto text-sm leading-relaxed;
}

[data-rehype-pretty-code-figure] code {
  @apply grid;
}

[data-rehype-pretty-code-figure] [data-line] {
  @apply px-6 border-l-2 border-transparent;
}

[data-rehype-pretty-code-figure] [data-highlighted-line] {
  @apply bg-white/5 border-l-blue-400;
}

[data-rehype-pretty-code-figure] [data-highlighted-chars] {
  @apply bg-white/10 rounded px-1 py-0.5;
}

/* Line numbers */
[data-rehype-pretty-code-figure] code[data-line-numbers] {
  counter-reset: line;
}

[data-rehype-pretty-code-figure] code[data-line-numbers] > [data-line]::before {
  counter-increment: line;
  content: counter(line);
  @apply inline-block w-8 mr-4 text-right text-gray-500;
}
```

### Code Block with Copy Button

```tsx
// components/mdx/copy-button.tsx
'use client';

import { useState, useRef } from 'react';

export function CopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="px-3 py-2 text-sm rounded-lg bg-white/10 text-gray-300 transition-all duration-200 hover:bg-white/20 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-gray-900"
      aria-label={copied ? 'Copied' : 'Copy code'}
    >
      {copied ? 'Copied' : 'Copy'}
    </button>
  );
}
```

## Table of Contents Generation

### Extract Headings from MDX Content

```ts
// lib/toc.ts
import { remark } from 'remark';
import { visit } from 'unist-util-visit';

export interface TocItem {
  id: string;
  title: string;
  level: number;
}

export function extractToc(markdown: string): TocItem[] {
  const toc: TocItem[] = [];
  const tree = remark().parse(markdown);

  visit(tree, 'heading', (node: any) => {
    const text = node.children
      .filter((c: any) => c.type === 'text')
      .map((c: any) => c.value)
      .join('');

    const id = text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');

    toc.push({ id, title: text, level: node.depth });
  });

  return toc;
}
```

### Table of Contents Component

```tsx
// components/table-of-contents.tsx
'use client';

import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import type { TocItem } from '@/lib/toc';

export function TableOfContents({ items }: { items: TocItem[] }) {
  const [activeId, setActiveId] = useState('');

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActiveId(entry.target.id);
        });
      },
      { rootMargin: '-80px 0px -80% 0px' }
    );

    items.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [items]);

  return (
    <nav className="sticky top-24 space-y-1" aria-label="Table of contents">
      <p className="font-semibold text-base mb-4">On this page</p>
      {items.map((item) => (
        <a
          key={item.id}
          href={`#${item.id}`}
          className={cn(
            'block text-sm py-1 transition-colors duration-200',
            item.level === 2 ? 'pl-0' : item.level === 3 ? 'pl-4' : 'pl-8',
            activeId === item.id
              ? 'text-brand-600 font-medium'
              : 'text-text-secondary hover:text-text-primary'
          )}
        >
          {item.title}
        </a>
      ))}
    </nav>
  );
}
```

**Usage in blog layout:**

```tsx
// app/blog/[slug]/page.tsx
import { TableOfContents } from '@/components/table-of-contents';
import { extractToc } from '@/lib/toc';

export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { content, frontmatter } = await getPost(slug);
  const toc = extractToc(content);

  return (
    <div className="py-16 max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-[1fr_250px] gap-12">
      <article className="prose prose-lg dark:prose-invert max-w-none">
        <MDXRemote source={content} components={mdxComponents} options={mdxOptions} />
      </article>
      <aside className="hidden lg:block">
        <TableOfContents items={toc} />
      </aside>
    </div>
  );
}
```

## MDX File Organization Patterns

### Blog / Content Site

```
content/
  posts/
    2025-03-01-building-with-mdx.mdx
    2025-02-15-react-server-components.mdx
  pages/
    about.mdx
    contact.mdx
  snippets/
    use-debounce.mdx
    use-local-storage.mdx

components/
  mdx-components.tsx      # Component map (single source of truth)
  mdx/
    callout.tsx
    code-tabs.tsx
    copy-button.tsx

lib/
  mdx.ts                  # File reading, parsing, listing
  toc.ts                  # Table of contents extraction
  frontmatter.ts          # Zod schema + gray-matter parsing
  mdx-options.ts          # Shared remark/rehype plugin config
```

### Documentation Site

```
content/
  docs/
    01-getting-started/
      01-installation.mdx
      02-quick-start.mdx
      meta.json              # { "title": "Getting Started" }
    02-guides/
      01-authentication.mdx
      02-data-fetching.mdx
      meta.json
    03-api-reference/
      components/
        button.mdx
        input.mdx
      hooks/
        use-auth.mdx
      meta.json

lib/
  docs.ts                    # Recursive directory reading, sidebar generation
```

### Sidebar Generation from File Structure

```ts
// lib/docs.ts
import fs from 'node:fs/promises';
import path from 'node:path';

interface SidebarItem {
  title: string;
  slug: string;
  children?: SidebarItem[];
}

export async function getSidebar(docsDir: string): Promise<SidebarItem[]> {
  const entries = await fs.readdir(docsDir, { withFileTypes: true });
  const dirs = entries.filter(e => e.isDirectory()).sort((a, b) => a.name.localeCompare(b.name));

  const sidebar: SidebarItem[] = [];

  for (const dir of dirs) {
    const dirPath = path.join(docsDir, dir.name);
    const metaPath = path.join(dirPath, 'meta.json');

    let title = dir.name.replace(/^\d+-/, '');
    try {
      const meta = JSON.parse(await fs.readFile(metaPath, 'utf-8'));
      title = meta.title ?? title;
    } catch {
      // No meta.json, derive title from directory name
    }

    const files = (await fs.readdir(dirPath))
      .filter(f => f.endsWith('.mdx'))
      .sort();

    const children = files.map(f => ({
      title: f.replace(/^\d+-/, '').replace(/\.mdx$/, '').replace(/-/g, ' '),
      slug: `${dir.name.replace(/^\d+-/, '')}/${f.replace(/\.mdx$/, '').replace(/^\d+-/, '')}`,
    }));

    sidebar.push({ title, slug: dir.name.replace(/^\d+-/, ''), children });
  }

  return sidebar;
}
```

## Best Practices

1. **Use `next-mdx-remote/rsc`** for server-rendered MDX in Next.js App Router -- no client bundle for content.
2. **Define `mdx-components.tsx` at project root** -- required by `@next/mdx` for component overrides.
3. **Validate frontmatter with Zod** -- catch missing or malformed metadata at build time, not runtime.
4. **Use `rehype-pretty-code`** with Shiki for syntax highlighting -- built-in language support, zero client JS.
5. **Order rehype plugins carefully** -- `rehype-slug` before `rehype-autolink-headings`, `rehype-pretty-code` after both.
6. **Scope custom components** -- only expose components that content authors actually need in the MDX component map.
7. **Use `prose` from Tailwind Typography** -- provides sensible defaults for long-form content, override specific elements in the component map.
8. **Generate static params** -- always use `generateStaticParams` for blog/docs routes to pre-render at build time.
9. **Add `scroll-mt-24` to headings** -- so anchor links do not hide behind sticky headers.
10. **Cache parsed content in production** -- avoid re-reading and re-parsing files on every request. Use `React.cache()` or Next.js data cache.
11. **Keep custom MDX components in a dedicated folder** (`components/mdx/`) separate from UI components.
12. **Extract shared plugin config** into `lib/mdx-options.ts` to avoid duplicating remark/rehype arrays.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Using `mdx-bundler` in RSC | Client-only bundler fails in Server Components | Switch to `next-mdx-remote/rsc` |
| Missing `rehype-slug` | Heading anchors and TOC links do not work | Install and add `rehype-slug` before `rehype-autolink-headings` |
| Inline `<img>` tags in MDX | No Next.js image optimization | Override `img` in component map to use `next/image` |
| No frontmatter validation | Runtime crashes from missing fields | Parse with Zod schema |
| Importing from MDX files | `mdx-bundler` supports it, `next-mdx-remote` does not | Pass data via component props or frontmatter instead |
| Giant component map | Bundle bloat from unused components | Only include components that MDX content actually uses |
| No `generateStaticParams` | Pages render dynamically on every request | Add static params for all known slugs |
| Shiki loading all themes | Large bundle at compile time | Import only the themes you need |
| Content not updating in dev | `next-mdx-remote` caching | Restart dev server or clear `.next` cache |
| Math rendering broken | Missing KaTeX CSS | Import `katex/dist/katex.min.css` in layout |
| Client-side MDX compilation | Large bundle size, slow rendering | Use `next-mdx-remote/rsc` for server-side compilation |
| Rendering raw HTML strings | XSS vulnerability risk | Use proper MDX compilation pipeline with sanitized components |
| Storing MDX in DB without cache | Recompiles on every request | Cache compiled output with `unstable_cache` or Redis |

## Decision Guide

| Scenario | Approach |
|----------|----------|
| Local MDX files in repo | `@next/mdx` with `pageExtensions` |
| CMS-sourced content | `next-mdx-remote/rsc` with `compileMDX` |
| MDX with local imports (images, data) | `mdx-bundler` (supports esbuild imports) |
| Blog with frontmatter | `next-mdx-remote/rsc` + `parseFrontmatter: true` or gray-matter |
| Type-safe content collections | Velite with Zod schemas |
| Docs site with sidebar | File-based MDX + generated nav from directory structure |
| Syntax highlighting | `rehype-pretty-code` (Shiki-based, zero client JS) |
| Table of contents | `remark` parse + `rehype-slug` + IntersectionObserver |
| Custom admonitions/callouts | Create `Callout` component, register in `mdx-components.tsx` |
| Type-safe frontmatter | Zod validation + TypeScript interfaces |


---

## From `tiptap`

> Tiptap rich-text editor — headless, extensible framework built on ProseMirror for React/Vue/vanilla

# tiptap

## Overview

Headless, extensible rich-text editor framework based on ProseMirror. Provides a modular extension system, real-time collaboration, and framework-agnostic core with first-class React bindings. Output as HTML, JSON, or Markdown.

## When to Use

- Building rich-text or block-based editors in React/Vue/vanilla
- Need collaborative real-time editing (Yjs + Hocuspocus)
- Require custom nodes, marks, or slash-command UIs
- Want headless control over editor styling and behavior

## Key Patterns

- **Editor setup**: `useEditor({ extensions, content })` hook + `<EditorContent editor={editor} />` component
- **StarterKit**: Bundle of common extensions (bold, italic, heading, lists, code, blockquote, etc.) — start here, override as needed
- **Custom extensions**: `Node.create({ name, group, content, renderHTML, parseHTML, addCommands, addKeyboardShortcuts })`
- **Marks & nodes**: Bold, italic, strike, code, link (marks); heading, image, table, codeBlock, taskList (nodes)
- **Collaborative editing**: `Collaboration` + `CollaborationCursor` extensions with `HocuspocusProvider` (Yjs backend)
- **Custom commands**: `editor.chain().focus().toggleBold().run()` — chainable command API
- **Keyboard shortcuts**: Define via `addKeyboardShortcuts()` in extensions, e.g., `'Mod-Shift-x': () => this.editor.commands.toggleStrike()`
- **BubbleMenu**: `<BubbleMenu editor={editor}>` — toolbar appears on text selection
- **FloatingMenu**: `<FloatingMenu editor={editor}>` — toolbar appears on empty lines
- **Serialization**: `editor.getHTML()`, `editor.getJSON()`, Markdown via `@tiptap/extension-markdown` or `tiptap-markdown`
- **Slash commands / suggestions**: `@tiptap/suggestion` extension — trigger on `/` char, render a popup with command list

## Anti-Patterns

- Directly mutating ProseMirror state outside tiptap's command/transaction API
- Wrapping the entire editor in uncontrolled React state (let tiptap own document state)
- Loading all extensions at once instead of tree-shaking only what you need
- Ignoring `onUpdate` debouncing — saving on every keystroke causes performance issues
- Using raw innerHTML for tiptap output — use `generateHTML()` from `@tiptap/html` or render JSON with a custom renderer, and sanitize with DOMPurify

## Related Skills

react, typescript-frontend, forms

