---
name: astro
description: Build content-focused websites with Astro — zero JS by default, islands architecture, multi-framework components, and Markdown/MDX support. 
category: Document Processing
source: antigravity
tags: [javascript, typescript, react, nextjs, markdown, api, claude, ai, template, design]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/astro
---


# Astro Web Framework

## Overview

Astro is a web framework designed for content-rich websites — blogs, docs, portfolios, marketing sites, and e-commerce. Its core innovation is the **Islands Architecture**: by default, Astro ships zero JavaScript to the browser. Interactive components are selectively hydrated as isolated "islands." Astro supports React, Vue, Svelte, Solid, and other UI frameworks simultaneously in the same project, letting you pick the right tool per component.

## When to Use This Skill

- Use when building a blog, documentation site, marketing page, or portfolio
- Use when performance and Core Web Vitals are the top priority
- Use when the project is content-heavy with Markdown or MDX files
- Use when you want SSG (static) output with optional SSR for dynamic routes
- Use when the user asks about `.astro` files, `Astro.props`, content collections, or `client:` directives

## How It Works

### Step 1: Project Setup

```bash
npm create astro@latest my-site
cd my-site
npm install
npm run dev
```

Add integrations as needed:

```bash
npx astro add tailwind        # Tailwind CSS
npx astro add react           # React component support
npx astro add mdx             # MDX support
npx astro add sitemap         # Auto sitemap.xml
npx astro add vercel          # Vercel SSR adapter
```

Project structure:

```
src/
  pages/          ← File-based routing (.astro, .md, .mdx)
  layouts/        ← Reusable page shells
  components/     ← UI components (.astro, .tsx, .vue, etc.)
  content/        ← Type-safe content collections (Markdown/MDX)
  styles/         ← Global CSS
public/           ← Static assets (copied as-is)
astro.config.mjs  ← Framework config
```

### Step 2: Astro Component Syntax

`.astro` files have a code fence at the top (server-only) and a template below:

```astro
---
// src/components/Card.astro
// This block runs on the server ONLY — never in the browser
interface Props {
  title: string;
  href: string;
  description: string;
}

const { title, href, description } = Astro.props;
---

<article class="card">
  <h2><a href={href}>{title}</a></h2>
  <p>{description}</p>
</article>

<style>
  /* Scoped to this component automatically */
  .card { border: 1px solid #eee; padding: 1rem; }
</style>
```

### Step 3: File-Based Pages and Routing

```
src/pages/index.astro          → /
src/pages/about.astro          → /about
src/pages/blog/[slug].astro    → /blog/:slug (dynamic)
src/pages/blog/[...path].astro → /blog/* (catch-all)
```

Dynamic route with `getStaticPaths`:

```astro
---
// src/pages/blog/[slug].astro
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<h1>{post.data.title}</h1>
<Content />
```

### Step 4: Content Collections

Content collections give you type-safe access to Markdown and MDX files:

```typescript
// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .filter(p => !p.data.draft)
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
---

<ul>
  {posts.map(post => (
    <li>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      <time>{post.data.date.toLocaleDateString()}</time>
    </li>
  ))}
</ul>
```

### Step 5: Islands — Selective Hydration

By default, UI framework components render to static HTML with no JS. Use `client:` directives to hydrate:

```astro
---
import Counter from '../components/Counter.tsx';  // React component
import VideoPlayer from '../components/VideoPlayer.svelte';
---

<!-- Static HTML — no JavaScript sent to browser -->
<Counter initialCount={0} />

<!-- Hydrate immediately on page load -->
<Counter initialCount={0} client:load />

<!-- Hydrate when the component scrolls into view -->
<VideoPlayer src="/demo.mp4" client:visible />

<!-- Hydrate only when browser is idle -->
<Analytics client:idle />

<!-- Hydrate only on a specific media query -->
<MobileMenu client:media="(max-width: 768px)" />
```

### Step 6: Layouts

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}
const { title, description = 'My Astro Site' } = Astro.props;
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="description" content={description} />
  </head>
  <body>
    <nav>...</nav>
    <main>
      <slot />  <!-- page content renders here -->
    </main>
    <footer>...</footer>
  </body>
</html>
```

```astro
---
// src
