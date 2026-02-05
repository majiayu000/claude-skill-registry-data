---
name: "static-site-generation"
description: "Framework evaluation criteria and deployment patterns for static site generators with GitHub Pages. Use when choosing SSG frameworks, configuring builds, or setting up GitHub Pages deployment."
---

# Static Site Generation

## Framework Evaluation Criteria

When evaluating SSG frameworks, prioritize:

1. **TypeScript support**: First-class, not bolted-on
2. **MDX integration**: Built-in or official plugin
3. **GitHub Pages compatibility**: Base path support, static output
4. **Content collections**: Type-safe content with schema validation
5. **Build performance**: Fast rebuilds for iteration
6. **DX**: Good error messages, debugging tools

## Framework Comparison for Knowledge Base

**Astro** (Recommended for content-first sites)
- Pros: Best MDX support, fast builds, content collections, multi-framework
- Cons: Newer ecosystem, fewer community plugins
- Best for: Documentation, knowledge bases, content-heavy sites

**Next.js with Static Export**
- Pros: Huge ecosystem, familiar to React devs, mature tooling
- Cons: Overkill for simple sites, larger bundles, requires explicit static config
- Best for: Apps needing both static and dynamic capabilities

**VitePress**
- Pros: Extremely fast, excellent docs focus, simple
- Cons: Vue-specific, less flexible for complex needs
- Best for: Pure documentation sites with minimal custom needs

**Avoid**: Gatsby (complex, slow builds, declining momentum)

## GitHub Pages Configuration

### Critical Settings

**Base Path for Subpath Deployment:**
```javascript
// Required if deploying to github.io/repo-name/
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name/',  // Must include trailing slash
});
```

**Output Directory:**
- Astro: `dist/` (default)
- Next.js: `out/` (with `output: 'export'`)
- VitePress: `.vitepress/dist/`

**404 Handling:**
- Create `404.html` in output directory
- For SPAs: All routes → `404.html` (GitHub Pages limitation)

### Deployment Pattern

**Using GitHub Actions (Recommended):**
```yaml
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist
      - uses: actions/deploy-pages@v4
```

**Repository Settings:**
- Pages → Source: "GitHub Actions"
- Branch deployment not needed with Actions

## Build Optimization Checklist

Before marking build complete:
- [ ] TypeScript strict mode enabled
- [ ] Base path configured correctly
- [ ] All routes generate static HTML
- [ ] Assets use correct paths (relative to base)
- [ ] 404 page exists
- [ ] Build succeeds with zero errors
- [ ] Deployment workflow tested

## Content Collections Pattern

Define schemas for type-safe content:

```typescript
import { z, defineCollection } from 'astro:content';

const docs = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { docs };
```

Benefits: Type safety, validation at build time, autocomplete in editor.

## Common Pitfalls

**Incorrect base path:**
- Symptom: Routes work locally, 404 in production
- Fix: Ensure `base` matches repo name, includes trailing slash

**Mixed path types:**
- Symptom: Some assets load, others don't
- Fix: Use framework's path helpers consistently

**Large bundle size:**
- Symptom: Slow initial load
- Fix: Enable code splitting, lazy load heavy components

**Missing TypeScript config:**
- Symptom: Type errors not caught during build
- Fix: Enable strict mode, include all source files

## Decision Template

When choosing framework, document in CLAUDE.md:

```markdown
## Framework Decision: [Name]

**Chosen:** [Framework]
**Rationale:** [Why - 2-3 key reasons]
**Alternatives considered:** [What else, why not]
**Trade-offs:** [What we gain vs. lose]
```

## Quick Start Validation

After framework initialization:
1. Run build → Should succeed with zero errors
2. Check output directory → HTML files present
3. Test locally → `npx serve dist` → All routes work
4. Deploy to GitHub Pages → All routes work with base path
5. Check console → No 404s on assets
