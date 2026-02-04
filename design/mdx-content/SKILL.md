---
name: "mdx-content"
description: "Content schema design and MDX configuration patterns for knowledge bases. Use when designing content structure, configuring MDX processing, or setting up frontmatter schemas."
---

# MDX Content Management

## Content Schema Design

### Frontmatter Schema Pattern

Required fields for all content:
```yaml
---
title: string        # Page title
description: string  # Short description (for nav, search)
---
```

Common optional fields:
```yaml
date: date          # Publication/update date
tags: string[]      # Categorization
draft: boolean      # Hide from production
order: number       # Manual ordering
category: string    # Primary category
```

### Type-Safe Schema Definition

```typescript
import { z } from 'zod';

const schema = z.object({
  title: z.string(),
  description: z.string(),
  date: z.date().optional(),
  tags: z.array(z.string()).optional(),
  draft: z.boolean().default(false),
});
```

**Critical**: Validate at build time, not runtime. Catch schema errors early.

## MDX Plugin Configuration

### Essential Plugins

**Markdown processing (remark):**
- `remark-gfm`: GitHub Flavored Markdown (tables, task lists)
- `remark-frontmatter`: Parse YAML frontmatter

**HTML processing (rehype):**
- `rehype-slug`: Add IDs to headings (required for TOC)
- `rehype-autolink-headings`: Clickable heading links
- `rehype-pretty-code`: Syntax highlighting (Shiki-based)

### Minimal Config Example

```javascript
export default defineConfig({
  markdown: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [rehypeAutolinkHeadings, { behavior: 'wrap' }],
      [rehypePrettyCode, { theme: 'github-dark' }],
    ],
  },
});
```

## Content Organization Patterns

### Directory Structure

```
content/
  docs/              # Main documentation
    index.md
    getting-started.md
    api/             # Nested sections
      auth.md
  guides/            # Tutorials/guides
  changelog.md       # Special pages
```

**Routing**: Directory structure maps to URLs
- `docs/index.md` → `/docs`
- `docs/api/auth.md` → `/docs/api/auth`

### Collection Organization

Group related content into collections:

```typescript
export const collections = {
  'docs': docsCollection,
  'guides': guidesCollection,
  'blog': blogCollection,
};
```

**Benefits**: Separate schemas, different processing, type safety per collection.

## Custom Components in MDX

### Providing Components

```typescript
// Make components available in MDX
const components = {
  // Override defaults
  h1: CustomH1,
  code: CustomCode,

  // Add custom components
  Callout: CalloutComponent,
  Tabs: TabsComponent,
};
```

### Common Patterns

**Callout/Alert:**
```mdx
<Callout type="warning">
Important information here
</Callout>
```

**Code with tabs:**
```mdx
<Tabs>
  <Tab label="JavaScript">...</Tab>
  <Tab label="TypeScript">...</Tab>
</Tabs>
```

## Syntax Highlighting

### Shiki Configuration

```javascript
[rehypePrettyCode, {
  theme: 'github-dark',
  keepBackground: false,  // Use CSS custom properties
}]
```

**Theme switching**: Set `keepBackground: false`, control via CSS:
```css
pre {
  background: var(--code-background);
}
```

### Code Block Features

```markdown
```js title="example.js" {3-5}
// Line 1
// Line 2
// Lines 3-5 highlighted
// ...
```
```

Supported: Line highlighting, titles, line numbers (framework-dependent).

## Content Queries

### Basic Filtering

```typescript
import { getCollection } from 'astro:content';

// Get published docs
const docs = await getCollection('docs', ({ data }) => {
  return !data.draft;
});

// Sort by date
docs.sort((a, b) =>
  b.data.date.getTime() - a.data.date.getTime()
);
```

### Navigation Generation

```typescript
// Generate nav from content
const nav = docs
  .filter(doc => !doc.data.draft)
  .map(doc => ({
    label: doc.data.title,
    href: `/docs/${doc.slug}`,
    order: doc.data.order ?? 999,
  }))
  .sort((a, b) => a.order - b.order);
```

## Table of Contents Generation

### Extract Headings

```typescript
// From markdown AST or rendered HTML
function extractHeadings(content: string) {
  const headings = [];
  // Parse headings from content
  return headings.map(h => ({
    depth: h.depth,
    text: h.text,
    slug: h.slug,
  }));
}
```

**Display**: Show h2 and h3 only, indent by depth.

## Validation Checklist

Before committing content schema:
- [ ] Required fields defined
- [ ] TypeScript types generated
- [ ] Validation runs at build time
- [ ] Example content validates
- [ ] Frontmatter documented for authors
- [ ] Collections organized logically

## Common Issues

**Frontmatter not parsing:**
- Ensure triple dashes `---` around YAML
- Check indentation (YAML is whitespace-sensitive)
- Validate against schema

**Custom components not rendering:**
- Verify component is provided to MDX
- Check import paths
- Ensure component is exported

**Syntax highlighting broken:**
- Verify plugin is configured
- Check language identifier is valid
- Ensure theme is loaded

## Content Authoring Guidelines

Document for content authors:

```markdown
## Content Guidelines

1. **Frontmatter**: Required fields: `title`, `description`
2. **Headings**: Start with h2 (h1 is title)
3. **Links**: Use relative paths: `./other-doc.md`
4. **Images**: Place in `src/assets/`, use relative paths
5. **Code blocks**: Include language identifier
```

## Decision Points

**Schema design:**
- What content types exist?
- What metadata does each need?
- How will content be filtered/sorted?

**MDX features:**
- Which custom components are needed?
- What markdown extensions are required?
- How will code blocks be styled?

**Organization:**
- How to structure directories?
- How to handle navigation?
- How to generate TOC?

Document decisions in CLAUDE.md under "Content Structure" section.
