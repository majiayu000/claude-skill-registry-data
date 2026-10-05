---
name: astro-expert
description: Deep Astro expertise for island architecture, content collections, multi-framework integration, and hybrid rendering. Use when building Astro sites.
---

# Astro Expert

Specialized expertise in Astro development, providing deep guidance on the island architecture, content collections with type-safe schemas, file-based routing with static/SSR/hybrid rendering, multi-framework component integration (React, Vue, Svelte, Solid), client hydration directives, data fetching patterns, API endpoints, middleware, image optimization with `astro:assets`, View Transitions, and production deployment across multiple adapters.

## When to Use This Skill

Use this skill for:

- Scaffolding new Astro projects with proper directory structure
- Building content-driven sites with type-safe content collections
- Designing island architecture strategies with selective hydration
- Integrating React, Vue, Svelte, or Solid components in Astro pages
- Implementing file-based routing with dynamic segments and pagination
- Configuring static, SSR, or hybrid rendering modes
- Creating API endpoints and server-side middleware
- Optimizing images, fonts, and Core Web Vitals
- Adding View Transitions for SPA-like navigation
- Generating sitemaps, RSS feeds, and structured data
- Deploying to Vercel, Netlify, Cloudflare Workers, or Node.js

**Trigger phrases**: "astro", "astro.build", "content collections", "island architecture", "partial hydration", "client:load", "client:idle", "client:visible", "astro components", "astro routing", "astro deployment", "astro adapter", "view transitions", "astro:assets", "MDX astro"

## What This Skill Does

Provides Astro expertise including:

- **Project Structure**: Directory conventions, `.astro` component syntax, frontmatter scripts, expressions, and slots
- **Content Collections**: Zod schema definitions, querying and rendering collections, MDX integration, reference relations
- **Routing**: File-based routing, dynamic routes, rest parameters, pagination, i18n routing
- **Island Architecture**: `client:load`, `client:idle`, `client:visible`, `client:media`, `client:only` directives and hydration strategies
- **Multi-Framework**: React, Vue, Svelte, Solid components coexisting in a single Astro project with shared state
- **Data Fetching**: Frontmatter fetch, API endpoints, SSR middleware, authentication patterns
- **Performance**: Image optimization with `astro:assets`, View Transitions, prefetching, fonts, Core Web Vitals
- **Deployment**: Node.js, Vercel, Netlify, Cloudflare adapters, static output, environment variable configuration

## Instructions

### Step 1: Astro Fundamentals

**Standard Astro project structure**:

```
src/
  components/        # Reusable .astro and framework components
    Header.astro
    Footer.astro
    Button.tsx       # React component (island)
  content/           # Content collections (Markdown, MDX, JSON)
    blog/
      first-post.md
      second-post.mdx
    authors/
      alice.json
    config.ts        # Collection schema definitions
  layouts/           # Page layouts
    BaseLayout.astro
    BlogPost.astro
  pages/             # File-based routing
    index.astro      # /
    about.astro      # /about
    blog/
      index.astro    # /blog
      [slug].astro   # /blog/:slug
    api/
      search.ts      # /api/search (API endpoint)
  styles/            # Global styles
    global.css
  middleware.ts      # Request middleware (SSR mode)
public/              # Static assets (served as-is)
  favicon.svg
  robots.txt
astro.config.mjs     # Astro configuration
tsconfig.json        # TypeScript configuration
```

**Astro component anatomy** (`.astro` files have a frontmatter script fence and an HTML template):

```astro
---
// src/components/Greeting.astro
// --- Frontmatter: runs at build time (or request time in SSR) ---
// This is server-side TypeScript. It never ships to the browser.

interface Props {
  name: string;
  greeting?: string;
}

const { name, greeting = "Hello" } = Astro.props;
const capitalizedName = name.charAt(0).toUpperCase() + name.slice(1);
const timestamp = new Date().toLocaleDateString("en-US", {
  year: "numeric",
  month: "long",
  day: "numeric",
});
---

<!-- Template: standard HTML with expressions in curly braces -->
<div class="greeting-card">
  <h2>{greeting}, {capitalizedName}!</h2>
  <p>Generated on {timestamp}</p>
  <slot />           <!-- Default slot for child content -->
  <slot name="footer" /> <!-- Named slot -->
</div>

<style>
  /* Scoped styles: only apply to this component */
  .greeting-card {
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
  }
  h2 {
    color: #1a202c;
    margin: 0 0 0.5rem;
  }
</style>
```

**Using the component with slots**:

```astro
---
// src/pages/index.astro
import Greeting from "../components/Greeting.astro";
import BaseLayout from "../layouts/BaseLayout.astro";
---

<BaseLayout title="Home">
  <Greeting name="developer" greeting="Welcome">
    <p>This content fills the default slot.</p>
    <p slot="footer">This goes into the named "footer" slot.</p>
  </Greeting>
</BaseLayout>
```

**Base layout with `<head>` management**:

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}

const { title, description = "An Astro site" } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content={description} />
    <link rel="canonical" href={canonicalURL} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
  </head>
  <body>
    <header>
      <nav>
        <a href="/">Home</a>
        <a href="/blog">Blog</a>
        <a href="/about">About</a>
      </nav>
    </header>
    <main>
      <slot />
    </main>
    <footer>
      <p>&copy; {new Date().getFullYear()} My Site</p>
    </footer>
  </body>
</html>

<style is:global>
  /* is:global escapes scoping for base styles */
  *,
  *::before,
  *::after {
    box-sizing: border-box;
    margin: 0;
  }
  body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: #1a202c;
  }
</style>
```

**Conditional rendering and list iteration**:

```astro
---
// src/components/FeatureList.astro
interface Props {
  features: { title: string; available: boolean }[];
  showUnavailable?: boolean;
}

const { features, showUnavailable = false } = Astro.props;
const visibleFeatures = showUnavailable
  ? features
  : features.filter((f) => f.available);
---

{visibleFeatures.length > 0 ? (
  <ul class="feature-list">
    {visibleFeatures.map((feature) => (
      <li class:list={["feature", { unavailable: !feature.available }]}>
        {feature.title}
        {feature.available ? <span class="badge">Available</span> : null}
      </li>
    ))}
  </ul>
) : (
  <p>No features to display.</p>
)}
```

### Step 2: Content Collections

**Define collection schemas** in `src/content/config.ts` using Zod:

```ts
// src/content/config.ts
import { defineCollection, z, reference } from "astro:content";

const blogCollection = defineCollection({
  type: "content", // Markdown/MDX files
  schema: ({ image }) =>
    z.object({
      title: z.string().max(100),
      description: z.string().max(200),
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      heroImage: image().optional(), // Validated image import
      tags: z.array(z.string()).default([]),
      draft: z.boolean().default(false),
      author: reference("authors"), // Reference to another collection
    }),
});

const authorsCollection = defineCollection({
  type: "data", // JSON or YAML files
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      email: z.string().email(),
      bio: z.string().max(500),
      avatar: image().optional(),
      social: z
        .object({
          twitter: z.string().url().optional(),
          github: z.string().url().optional(),
        })
        .optional(),
    }),
});

const changelogCollection = defineCollection({
  type: "content",
  schema: z.object({
    version: z.string().regex(/^\d+\.\d+\.\d+$/),
    date: z.coerce.date(),
    breaking: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
  authors: authorsCollection,
  changelog: changelogCollection,
};
```

**Example content files**:

```markdown
---
# src/content/blog/getting-started.md
title: "Getting Started with Astro"
description: "Learn how to build your first Astro site from scratch."
pubDate: 2025-01-15
tags: ["astro", "tutorial"]
draft: false
author: alice
heroImage: "./images/getting-started-hero.jpg"
---

## Introduction

Astro is a web framework for building content-driven websites...
```

```json
// src/content/authors/alice.json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "bio": "Full-stack developer and technical writer.",
  "social": {
    "twitter": "https://twitter.com/alice",
    "github": "https://github.com/alice"
  }
}
```

**Query and render collections**:

```astro
---
// src/pages/blog/index.astro
import { getCollection } from "astro:content";
import BaseLayout from "../../layouts/BaseLayout.astro";
import BlogCard from "../../components/BlogCard.astro";

// Filter out drafts in production
const allPosts = await getCollection("blog", ({ data }) => {
  return import.meta.env.PROD ? !data.draft : true;
});

// Sort by publication date (newest first)
const sortedPosts = allPosts.sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
---

<BaseLayout title="Blog">
  <h1>Blog</h1>
  <ul class="post-list">
    {sortedPosts.map((post) => (
      <li>
        <BlogCard
          title={post.data.title}
          description={post.data.description}
          pubDate={post.data.pubDate}
          tags={post.data.tags}
          href={`/blog/${post.slug}`}
        />
      </li>
    ))}
  </ul>
</BaseLayout>
```

**Generate pages from collection entries**:

```astro
---
// src/pages/blog/[slug].astro
import { getCollection, type CollectionEntry } from "astro:content";
import BlogPost from "../../layouts/BlogPost.astro";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

interface Props {
  post: CollectionEntry<"blog">;
}

const { post } = Astro.props;
const { Content, headings, remarkPluginFrontmatter } = await post.render();

// Resolve the author reference
const authorEntry = await getEntry(post.data.author);
---

<BlogPost
  title={post.data.title}
  pubDate={post.data.pubDate}
  author={authorEntry.data.name}
  headings={headings}
>
  <Content />
</BlogPost>
```

**MDX integration for rich content**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

export default defineConfig({
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: "github-dark",
      wrap: true,
    },
  },
});
```

### Step 3: Routing and Pages

**File-based routing rules**:

| File path                          | URL                 | Type             |
| ---------------------------------- | ------------------- | ---------------- |
| `src/pages/index.astro`           | `/`                 | Static page      |
| `src/pages/about.astro`           | `/about`            | Static page      |
| `src/pages/blog/[slug].astro`     | `/blog/:slug`       | Dynamic route    |
| `src/pages/blog/[...slug].astro`  | `/blog/*`           | Rest parameter   |
| `src/pages/[lang]/index.astro`    | `/:lang`            | i18n root        |
| `src/pages/api/search.ts`         | `/api/search`       | API endpoint     |

**Dynamic routes with `getStaticPaths`** (required for static output):

```astro
---
// src/pages/tags/[tag].astro
import { getCollection } from "astro:content";
import BaseLayout from "../../layouts/BaseLayout.astro";

export async function getStaticPaths() {
  const allPosts = await getCollection("blog", ({ data }) => !data.draft);

  // Extract unique tags
  const uniqueTags = [
    ...new Set(allPosts.flatMap((post) => post.data.tags)),
  ];

  return uniqueTags.map((tag) => ({
    params: { tag },
    props: {
      posts: allPosts.filter((post) => post.data.tags.includes(tag)),
    },
  }));
}

const { tag } = Astro.params;
const { posts } = Astro.props;
---

<BaseLayout title={`Posts tagged "${tag}"`}>
  <h1>#{tag}</h1>
  <ul>
    {posts.map((post) => (
      <li>
        <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      </li>
    ))}
  </ul>
</BaseLayout>
```

**Pagination with `paginate()`**:

```astro
---
// src/pages/blog/[page].astro
import { getCollection } from "astro:content";
import type { GetStaticPaths } from "astro";
import BaseLayout from "../../layouts/BaseLayout.astro";

export const getStaticPaths = (async ({ paginate }) => {
  const allPosts = await getCollection("blog", ({ data }) => !data.draft);
  const sorted = allPosts.sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );
  return paginate(sorted, { pageSize: 10 });
}) satisfies GetStaticPaths;

const { page } = Astro.props;
// page.data       - array of posts for this page
// page.currentPage - current page number (1-based)
// page.lastPage   - total number of pages
// page.url.prev   - URL of previous page (or undefined)
// page.url.next   - URL of next page (or undefined)
// page.total      - total number of items
---

<BaseLayout title={`Blog - Page ${page.currentPage}`}>
  <h1>Blog</h1>
  {page.data.map((post) => (
    <article>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
    </article>
  ))}

  <nav class="pagination" aria-label="Blog pagination">
    {page.url.prev && <a href={page.url.prev}>Previous</a>}
    <span>Page {page.currentPage} of {page.lastPage}</span>
    {page.url.next && <a href={page.url.next}>Next</a>}
  </nav>
</BaseLayout>
```

**Rendering modes** (configure in `astro.config.mjs`):

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import node from "@astrojs/node";

export default defineConfig({
  // Option 1: Static (default) - all pages pre-rendered at build time
  output: "static",

  // Option 2: Server - all pages rendered on demand
  // output: "server",
  // adapter: node({ mode: "standalone" }),

  // Option 3: Hybrid - static by default, opt-in to SSR per page
  // output: "hybrid",
  // adapter: node({ mode: "standalone" }),
});
```

**Per-page rendering overrides** (in hybrid or server mode):

```astro
---
// src/pages/dashboard.astro
// In hybrid mode (default static), opt this page into SSR:
export const prerender = false;

// In server mode (default SSR), opt this page into static:
// export const prerender = true;

const user = await getUser(Astro.cookies.get("session")?.value);
if (!user) {
  return Astro.redirect("/login");
}
---

<h1>Welcome, {user.name}</h1>
```

**i18n routing configuration**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";

export default defineConfig({
  i18n: {
    defaultLocale: "en",
    locales: ["en", "fr", "de", "ja"],
    routing: {
      prefixDefaultLocale: false, // / for English, /fr/ for French
    },
    fallback: {
      fr: "en",
      de: "en",
    },
  },
});
```

```astro
---
// src/pages/[lang]/about.astro
export function getStaticPaths() {
  return [
    { params: { lang: "en" }, props: { greeting: "About Us" } },
    { params: { lang: "fr" }, props: { greeting: "A Propos" } },
    { params: { lang: "de" }, props: { greeting: "Uber Uns" } },
  ];
}

const { lang } = Astro.params;
const { greeting } = Astro.props;
const currentLocale = Astro.currentLocale; // "en", "fr", or "de"
---

<h1>{greeting}</h1>
<p>Current locale: {currentLocale}</p>
```

### Step 4: Island Architecture

Astro ships zero JavaScript by default. Interactive components become "islands" only when you add a `client:*` directive. Choose the directive that matches the component's loading priority.

**Client directive reference**:

| Directive         | When it hydrates                                       | Use for                                    |
| ----------------- | ------------------------------------------------------ | ------------------------------------------ |
| `client:load`     | Immediately on page load                               | Critical interactive UI (nav, modals)      |
| `client:idle`     | After the page finishes initial load (requestIdleCallback) | Below-fold interactive widgets             |
| `client:visible`  | When the component scrolls into the viewport           | Comments, carousels, footer widgets        |
| `client:media`    | When a CSS media query matches                         | Mobile-only sidebars, responsive widgets   |
| `client:only`     | Client-only render (no SSR HTML)                       | Components that cannot SSR (canvas, WebGL) |

**Applying hydration directives**:

```astro
---
// src/pages/index.astro
import BaseLayout from "../layouts/BaseLayout.astro";
import SearchBar from "../components/SearchBar.tsx";      // React
import Newsletter from "../components/Newsletter.vue";    // Vue
import ImageCarousel from "../components/Carousel.svelte"; // Svelte
import ThreeScene from "../components/Scene.tsx";          // React (canvas)
import MobileSidebar from "../components/Sidebar.tsx";     // React
---

<BaseLayout title="Home">
  <!-- Critical: hydrate immediately -->
  <SearchBar client:load placeholder="Search articles..." />

  <!-- Non-critical: hydrate when browser is idle -->
  <Newsletter client:idle />

  <!-- Deferred: hydrate when scrolled into view -->
  <ImageCarousel client:visible images={heroImages} />

  <!-- Conditional: hydrate only on narrow viewports -->
  <MobileSidebar client:media="(max-width: 768px)" />

  <!-- Client-only: no server-rendered HTML (for WebGL, canvas) -->
  <ThreeScene client:only="react" />

  <!-- Static by default: no directive = zero JS shipped -->
  <footer>
    <p>This Astro component ships no JavaScript.</p>
  </footer>
</BaseLayout>
```

**When to hydrate (decision framework)**:

```astro
---
// DECISION: Does this component need interactivity?
//
// NO  -> Use a plain .astro component (zero JS)
// YES -> Does it need to be interactive on first paint?
//        YES -> client:load
//        NO  -> Is it above the fold?
//               YES -> client:idle
//               NO  -> client:visible
//        Does it depend on viewport size?
//               YES -> client:media="(your query)"
//        Can it render on the server?
//               NO  -> client:only="framework"

// Example: A like button that is important but not above the fold
import LikeButton from "../components/LikeButton.tsx";
---

<!-- Hydrate when the user scrolls to it -->
<LikeButton client:visible postId="abc-123" />
```

**Passing props and children to islands**:

```astro
---
import Accordion from "../components/Accordion.tsx";

const faqItems = [
  { question: "What is Astro?", answer: "A web framework for content sites." },
  { question: "Is it fast?", answer: "Yes. Zero JS by default." },
];
---

<!--
  Props are serialized to the client.
  Only serializable data (strings, numbers, arrays, plain objects) can be passed.
  Functions, classes, and DOM nodes cannot be passed as props to islands.
-->
<Accordion client:visible items={faqItems} defaultOpen={0}>
  <p slot="footer">Can't find your answer? <a href="/contact">Contact us</a>.</p>
</Accordion>
```

### Step 5: Multi-Framework Integration

Astro supports multiple UI frameworks simultaneously. Each framework is added as an integration.

**Configuration**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import vue from "@astrojs/vue";
import svelte from "@astrojs/svelte";
import solid from "@astrojs/solid-js";

export default defineConfig({
  integrations: [
    react({
      include: ["**/react/*"], // Only process files in react/ directories
    }),
    vue({
      include: ["**/vue/*"],
    }),
    svelte(),
    solid({
      include: ["**/solid/*"],
    }),
  ],
});
```

**React component as an island**:

```tsx
// src/components/react/Counter.tsx
import { useState } from "react";

interface CounterProps {
  initialCount?: number;
  label: string;
}

export default function Counter({ initialCount = 0, label }: CounterProps) {
  const [count, setCount] = useState(initialCount);

  return (
    <div className="counter">
      <span>{label}: {count}</span>
      <button onClick={() => setCount((c) => c + 1)}>+</button>
      <button onClick={() => setCount((c) => c - 1)}>-</button>
    </div>
  );
}
```

**Vue component as an island**:

```vue
<!-- src/components/vue/ToggleTheme.vue -->
<script setup lang="ts">
import { ref } from "vue";

const isDark = ref(false);

function toggle() {
  isDark.value = !isDark.value;
  document.documentElement.classList.toggle("dark", isDark.value);
}
</script>

<template>
  <button @click="toggle" class="theme-toggle">
    {{ isDark ? "Light Mode" : "Dark Mode" }}
  </button>
</template>

<style scoped>
.theme-toggle {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
}
</style>
```

**Svelte component as an island**:

```svelte
<!-- src/components/Tabs.svelte -->
<script lang="ts">
  export let tabs: { label: string; content: string }[] = [];
  let activeIndex = 0;
</script>

<div class="tabs">
  <div class="tab-headers" role="tablist">
    {#each tabs as tab, i}
      <button
        role="tab"
        aria-selected={i === activeIndex}
        on:click={() => (activeIndex = i)}
      >
        {tab.label}
      </button>
    {/each}
  </div>
  <div class="tab-content" role="tabpanel">
    {tabs[activeIndex]?.content}
  </div>
</div>
```

**Composing multiple frameworks on one page**:

```astro
---
// src/pages/showcase.astro
import BaseLayout from "../layouts/BaseLayout.astro";
import Counter from "../components/react/Counter.tsx";
import ToggleTheme from "../components/vue/ToggleTheme.vue";
import Tabs from "../components/Tabs.svelte";

const tabData = [
  { label: "React", content: "React component rendered as an island." },
  { label: "Vue", content: "Vue component alongside React on the same page." },
  { label: "Svelte", content: "Svelte too. Each framework hydrates independently." },
];
---

<BaseLayout title="Multi-Framework Showcase">
  <h1>Framework Islands</h1>

  <!-- Each island hydrates independently with its own framework runtime -->
  <Counter client:load label="Visitors" initialCount={42} />
  <ToggleTheme client:idle />
  <Tabs client:visible tabs={tabData} />

  <!-- Static Astro content between islands (zero JS) -->
  <section>
    <h2>Why Islands?</h2>
    <p>Each interactive component loads only the JS it needs.</p>
    <p>Static content between islands ships no JavaScript at all.</p>
  </section>
</BaseLayout>
```

**Sharing state between framework islands** using nano stores:

```ts
// src/stores/cartStore.ts
// Use nanostores for cross-framework state sharing
import { atom, computed } from "nanostores";

export interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

export const $cartItems = atom<CartItem[]>([]);

export const $cartTotal = computed($cartItems, (items) =>
  items.reduce((sum, item) => sum + item.price * item.quantity, 0)
);

export function addToCart(item: Omit<CartItem, "quantity">) {
  const items = $cartItems.get();
  const existing = items.find((i) => i.id === item.id);
  if (existing) {
    $cartItems.set(
      items.map((i) =>
        i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
      )
    );
  } else {
    $cartItems.set([...items, { ...item, quantity: 1 }]);
  }
}
```

```tsx
// src/components/react/CartButton.tsx
// React component reading from the shared store
import { useStore } from "@nanostores/react";
import { $cartItems, $cartTotal } from "../../stores/cartStore";

export default function CartButton() {
  const items = useStore($cartItems);
  const total = useStore($cartTotal);

  return (
    <button className="cart-button">
      Cart ({items.length}) - ${total.toFixed(2)}
    </button>
  );
}
```

```vue
<!-- src/components/vue/AddToCartButton.vue -->
<!-- Vue component writing to the same shared store -->
<script setup lang="ts">
import { addToCart } from "../../stores/cartStore";

const props = defineProps<{
  productId: string;
  productName: string;
  price: number;
}>();

function handleAdd() {
  addToCart({ id: props.productId, name: props.productName, price: props.price });
}
</script>

<template>
  <button @click="handleAdd">Add to Cart - ${{ price.toFixed(2) }}</button>
</template>
```

### Step 6: Data Fetching and API Routes

**Fetch data in frontmatter** (runs at build time for static, request time for SSR):

```astro
---
// src/pages/users.astro
import BaseLayout from "../layouts/BaseLayout.astro";

interface User {
  id: number;
  name: string;
  email: string;
}

// Top-level await is supported in Astro frontmatter
const response = await fetch("https://jsonplaceholder.typicode.com/users");
if (!response.ok) {
  throw new Error(`Failed to fetch users: ${response.status}`);
}
const users: User[] = await response.json();
---

<BaseLayout title="Users">
  <h1>Users</h1>
  <ul>
    {users.map((user) => (
      <li>
        <strong>{user.name}</strong> ({user.email})
      </li>
    ))}
  </ul>
</BaseLayout>
```

**API endpoints** (server-side route handlers):

```ts
// src/pages/api/search.ts
import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export const GET: APIRoute = async ({ url }) => {
  const query = url.searchParams.get("q")?.toLowerCase();
  if (!query || query.length < 2) {
    return new Response(JSON.stringify({ error: "Query too short" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const posts = await getCollection("blog", ({ data }) => !data.draft);
  const results = posts
    .filter(
      (post) =>
        post.data.title.toLowerCase().includes(query) ||
        post.data.description.toLowerCase().includes(query)
    )
    .map((post) => ({
      slug: post.slug,
      title: post.data.title,
      description: post.data.description,
    }));

  return new Response(JSON.stringify({ results }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();

  // Validate input
  if (!body.email || typeof body.email !== "string") {
    return new Response(JSON.stringify({ error: "Email required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Process subscription (e.g., save to database)
  // await db.subscribers.create({ email: body.email });

  return new Response(JSON.stringify({ success: true }), {
    status: 201,
    headers: { "Content-Type": "application/json" },
  });
};
```

**Middleware** (for SSR/hybrid mode):

```ts
// src/middleware.ts
import { defineMiddleware, sequence } from "astro:middleware";

const authMiddleware = defineMiddleware(async (context, next) => {
  const { cookies, redirect, url } = context;

  // Skip auth for public routes
  const publicPaths = ["/", "/login", "/api/auth"];
  if (publicPaths.some((path) => url.pathname.startsWith(path))) {
    return next();
  }

  const sessionToken = cookies.get("session")?.value;
  if (!sessionToken) {
    return redirect("/login?returnTo=" + encodeURIComponent(url.pathname));
  }

  // Validate session and attach user to locals
  try {
    const user = await validateSession(sessionToken);
    context.locals.user = user;
  } catch {
    cookies.delete("session", { path: "/" });
    return redirect("/login");
  }

  return next();
});

const loggingMiddleware = defineMiddleware(async (context, next) => {
  const start = performance.now();
  const response = await next();
  const duration = (performance.now() - start).toFixed(2);
  console.log(`${context.request.method} ${context.url.pathname} - ${duration}ms`);
  return response;
});

// Chain middleware in order
export const onRequest = sequence(loggingMiddleware, authMiddleware);
```

**Type-safe locals** (define in `env.d.ts`):

```ts
// src/env.d.ts
/// <reference types="astro/client" />

interface User {
  id: string;
  name: string;
  role: "admin" | "user";
}

declare namespace App {
  interface Locals {
    user?: User;
  }
}
```

**Authentication pattern with cookies**:

```ts
// src/pages/api/auth/login.ts
import type { APIRoute } from "astro";

export const POST: APIRoute = async ({ request, cookies, redirect }) => {
  const formData = await request.formData();
  const email = formData.get("email")?.toString();
  const password = formData.get("password")?.toString();

  if (!email || !password) {
    return new Response("Missing credentials", { status: 400 });
  }

  // Verify credentials against your auth provider
  const user = await authenticateUser(email, password);
  if (!user) {
    return new Response("Invalid credentials", { status: 401 });
  }

  // Set session cookie
  const sessionToken = await createSession(user.id);
  cookies.set("session", sessionToken, {
    path: "/",
    httpOnly: true,
    secure: import.meta.env.PROD,
    sameSite: "lax",
    maxAge: 60 * 60 * 24 * 7, // 7 days
  });

  return redirect("/dashboard");
};
```

### Step 7: Performance and SEO

**Image optimization with `astro:assets`**:

```astro
---
// src/components/OptimizedImage.astro
import { Image, Picture } from "astro:assets";
import heroImage from "../assets/hero.jpg"; // Import for static optimization

interface Props {
  src: ImageMetadata;
  alt: string;
  widths?: number[];
}

const { src, alt, widths = [400, 800, 1200] } = Astro.props;
---

<!-- Basic optimized image (auto-generates WebP, sets width/height) -->
<Image src={heroImage} alt="Hero banner" />

<!-- Responsive image with multiple sizes -->
<Image
  src={heroImage}
  alt="Hero banner"
  widths={[400, 800, 1200]}
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
/>

<!-- Picture element for art direction with multiple formats -->
<Picture
  src={heroImage}
  formats={["avif", "webp"]}
  alt="Hero banner"
  widths={[400, 800, 1200]}
  sizes="(max-width: 600px) 400px, 800px"
/>
```

**Remote image optimization**:

```astro
---
import { Image } from "astro:assets";
---

<!-- Remote images require explicit dimensions -->
<Image
  src="https://example.com/photo.jpg"
  alt="Remote photo"
  width={800}
  height={600}
  inferSize={false}
/>
```

```ts
// astro.config.mjs - authorize remote image domains
import { defineConfig } from "astro/config";

export default defineConfig({
  image: {
    domains: ["example.com", "images.unsplash.com"],
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.amazonaws.com",
      },
    ],
  },
});
```

**View Transitions for SPA-like navigation**:

```astro
---
// src/layouts/BaseLayout.astro
import { ViewTransitions } from "astro:transitions";
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>{title}</title>
    <!-- Enables client-side navigation with animated transitions -->
    <ViewTransitions />
  </head>
  <body>
    <nav>
      <a href="/">Home</a>
      <a href="/blog">Blog</a>
      <a href="/about">About</a>
    </nav>
    <main transition:animate="slide">
      <slot />
    </main>
  </body>
</html>
```

**Named transition animations**:

```astro
---
// src/components/BlogCard.astro
const { slug, title, image } = Astro.props;
---

<!-- Give elements a shared transition:name so they animate between pages -->
<article>
  <img
    src={image}
    alt={title}
    transition:name={`hero-${slug}`}
    transition:animate="morph"
  />
  <h2 transition:name={`title-${slug}`}>{title}</h2>
</article>
```

```astro
---
// src/pages/blog/[slug].astro (the target page)
const { slug } = Astro.params;
---

<!-- Same transition:name values connect elements across pages -->
<img
  src={post.data.heroImage}
  alt={post.data.title}
  transition:name={`hero-${slug}`}
/>
<h1 transition:name={`title-${slug}`}>{post.data.title}</h1>
```

**Prefetching configuration**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";

export default defineConfig({
  prefetch: {
    prefetchAll: false, // Do not prefetch every link
    defaultStrategy: "hover", // Prefetch on hover (default)
  },
});
```

```astro
<!-- Per-link prefetch control -->
<a href="/blog" data-astro-prefetch="viewport">Blog</a>   <!-- Prefetch when visible -->
<a href="/about" data-astro-prefetch="hover">About</a>    <!-- Prefetch on hover -->
<a href="/large-page" data-astro-prefetch="false">Skip</a> <!-- Never prefetch -->
```

**Sitemap and RSS integration**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://example.com",
  integrations: [
    sitemap({
      filter: (page) => !page.includes("/admin/"),
      changefreq: "weekly",
      priority: 0.7,
      lastmod: new Date(),
      i18n: {
        defaultLocale: "en",
        locales: { en: "en-US", fr: "fr-FR" },
      },
    }),
  ],
});
```

```ts
// src/pages/rss.xml.ts
import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import type { APIContext } from "astro";

export async function GET(context: APIContext) {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  const sorted = posts.sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return rss({
    title: "My Blog",
    description: "A blog about web development",
    site: context.site!,
    items: sorted.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.slug}/`,
      categories: post.data.tags,
    })),
    customData: "<language>en-us</language>",
  });
}
```

**Structured data (JSON-LD)**:

```astro
---
// src/layouts/BlogPost.astro
const { title, description, pubDate, author, image } = Astro.props;

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  headline: title,
  description: description,
  datePublished: pubDate.toISOString(),
  author: {
    "@type": "Person",
    name: author,
  },
  image: image ? new URL(image, Astro.site).href : undefined,
};
---

<head>
  <script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />
</head>
```

### Step 8: Deployment and Adapters

**Adapter selection guide**:

| Target              | Adapter               | Install command                    |
| ------------------- | --------------------- | ---------------------------------- |
| Static hosting      | (none, default)       | N/A                                |
| Node.js server      | `@astrojs/node`       | `npx astro add node`              |
| Vercel              | `@astrojs/vercel`     | `npx astro add vercel`            |
| Netlify             | `@astrojs/netlify`    | `npx astro add netlify`           |
| Cloudflare Workers  | `@astrojs/cloudflare` | `npx astro add cloudflare`        |
| Deno                | `@astrojs/deno`       | `npx astro add deno`              |

**Static deployment (default)**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://example.com",
  output: "static", // Pre-render all pages at build time
  build: {
    assets: "_assets", // Custom assets directory in output
  },
  compressHTML: true, // Minify HTML output
});
```

```bash
# Build and preview locally
npx astro build    # Outputs to dist/
npx astro preview  # Serves the built site locally
```

**Node.js adapter (standalone server)**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import node from "@astrojs/node";

export default defineConfig({
  output: "server",
  adapter: node({
    mode: "standalone", // Self-contained server (or "middleware" for Express)
  }),
  server: {
    host: "0.0.0.0",
    port: 4321,
  },
});
```

```dockerfile
# Dockerfile for Node.js standalone deployment
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./

ENV HOST=0.0.0.0
ENV PORT=4321
EXPOSE 4321

CMD ["node", "./dist/server/entry.mjs"]
```

**Vercel adapter**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import vercel from "@astrojs/vercel";

export default defineConfig({
  output: "server", // or "hybrid" for mostly static + some SSR
  adapter: vercel({
    webAnalytics: { enabled: true },
    imageService: true, // Use Vercel image optimization
    isr: {
      expiration: 60, // ISR: revalidate every 60 seconds
    },
  }),
});
```

**Netlify adapter**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import netlify from "@astrojs/netlify";

export default defineConfig({
  output: "server",
  adapter: netlify({
    edgeMiddleware: true, // Run middleware at the edge
    imageCDN: true,       // Use Netlify Image CDN
  }),
});
```

**Cloudflare adapter**:

```ts
// astro.config.mjs
import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  output: "server",
  adapter: cloudflare({
    platformProxy: {
      enabled: true, // Access KV, D1, R2 bindings via platform.env
    },
  }),
});
```

```ts
// src/pages/api/kv-example.ts
// Accessing Cloudflare bindings in API routes
import type { APIRoute } from "astro";

export const GET: APIRoute = async ({ locals }) => {
  const runtime = locals.runtime;
  const value = await runtime.env.MY_KV_NAMESPACE.get("key");
  return new Response(JSON.stringify({ value }), {
    headers: { "Content-Type": "application/json" },
  });
};
```

**Environment variables**:

```ts
// astro.config.mjs - define expected environment variables
import { defineConfig, envField } from "astro/config";

export default defineConfig({
  env: {
    schema: {
      // Server-only (never exposed to client)
      DATABASE_URL: envField.string({
        context: "server",
        access: "secret",
      }),
      API_KEY: envField.string({
        context: "server",
        access: "secret",
      }),
      // Public (available in client JS)
      PUBLIC_SITE_URL: envField.string({
        context: "client",
        access: "public",
        default: "http://localhost:4321",
      }),
    },
  },
});
```

```astro
---
// Accessing environment variables in Astro components
// Server-side (frontmatter): use import.meta.env
const apiKey = import.meta.env.API_KEY;           // Server secret
const siteUrl = import.meta.env.PUBLIC_SITE_URL;  // Public variable

// Convention: PUBLIC_ prefix exposes to client bundles
// Variables without PUBLIC_ prefix are server-only
---

<p>Site: {siteUrl}</p>

<script>
  // Client-side: only PUBLIC_ variables are available
  const url = import.meta.env.PUBLIC_SITE_URL;
  console.log(url);
  // import.meta.env.API_KEY would be undefined here
</script>
```

**Production configuration checklist**:

```ts
// astro.config.mjs - production-ready configuration
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import react from "@astrojs/react";
import node from "@astrojs/node";

export default defineConfig({
  site: "https://example.com",
  output: "hybrid",
  adapter: node({ mode: "standalone" }),

  integrations: [
    react(),
    mdx(),
    sitemap({
      filter: (page) => !page.includes("/admin/"),
    }),
  ],

  image: {
    domains: ["images.unsplash.com"],
  },

  prefetch: {
    defaultStrategy: "hover",
  },

  compressHTML: true,

  vite: {
    build: {
      cssMinify: true,
      rollupOptions: {
        output: {
          manualChunks: {
            react: ["react", "react-dom"],
          },
        },
      },
    },
    ssr: {
      noExternal: [], // Add packages that need to be bundled for SSR
    },
  },

  security: {
    checkOrigin: true, // CSRF protection for form submissions
  },
});
```
