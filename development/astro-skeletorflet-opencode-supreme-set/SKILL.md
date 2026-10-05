---
name: astro
description: Astro content islands, multi-framework support, SSG/SSR modes, and content collections. Use when building static sites, content sites, or hybrid web apps.
---

## astro

### Core Concepts
- Astro Islands: client:* directives (load, idle, visible, media, interact)
- Content collections with type-safe frontmatter and schema validation
- Multi-framework: use React, Vue, Svelte, Solid components in one project
- File-based routing in src/pages/ with dynamic params and layouts
- Three output modes: static (SSG), server (SSR), hybrid per-route

### Common Patterns
- Content collections with Zod schema for blog/docs type safety
- View Transitions API for SPA-like page navigation
- Image optimization with <Image> and <Picture> components
- Server islands for dynamic content with zero client JS
- Astro DB for SQLite-backed relational data queries

### Best Practices
- Prefer static generation for content, islands only for interactivity
- Use content collections over manual markdown parsing
- Keep framework islands isolated to minimize JS payload
- Use Astro.build adapter for deployment targets
- Leverage view transitions for smooth multi-page experiences

### Common Code Patterns
- Blog post listing from content collection with sorted entries
- Interactive React counter island with client:load directive
- Hybrid page with static content and server-rendered component
