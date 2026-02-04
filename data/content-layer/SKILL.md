---
name: content-layer
description: "This skill should be used when the user asks to 'create an article', 'add a blog post', 'modify frontmatter', 'add a category', or 'update content schema'. Provides guidance for MDX articles, content-collections, and static content data in content/articles/*.mdx, content/data/*.ts, content-collections.ts."
---

# Content Layer Skill

## Scope

- `content/articles/*.mdx` - MDX article files
- `content/data/*.ts` - Static content data (categories, roles, projects, testimonials)
- `content-collections.ts` - Article schema configuration
- `lib/content/articles.ts` - Article fetching utilities

## Decision Tree

### Creating a new article?

1. **Choose numeric prefix**: Check existing articles in `content/articles/` and use next sequential number (e.g., `0005-`)
2. **Create file**: `content/articles/[NNNN]-[slug].mdx`
3. **Add frontmatter** with ALL required fields (see template below)
4. **Use only valid categories** from `content/data/categories.ts`
5. **Add cover image** to Cloudinary first, use public ID

### Adding a new category?

1. **Edit `content/data/categories.ts`**: Add to `CATEGORYTITLES` array
2. **Verify alphabetical sorting** is maintained in code (array auto-sorts)
3. **Update any affected articles** if needed

### Modifying article schema?

1. **Read `content-collections.ts`** first
2. **Update Zod schema** in `schema` function
3. **Update `transform`** if new computed fields needed
4. **Run build** to verify all articles pass validation

## Quick Templates

### Article Frontmatter (Required Fields)

```yaml
---
isPublished: false
title: "Article Title Here"
author: Suneet Misra
date: YYYY-MM-DD
updatedAt: YYYY-MM-DD
description: A brief description of the article (used in meta tags and previews)
coverImage: cloudinary-public-id_suffix
keywords: ["keyword1", "keyword2", "keyword3"]
categories: ["node", "typescript"]
---
```

### Article with Series Section

```mdx
---
# ... frontmatter ...
---

<SuspendedArticleImage
  src="cloudinary-public-id"
  alt="descriptive alt text"
/>

<SeriesSection
  seriesDescription="This article is part of a series..."
  seriesEntries={[
    { id: 1, title: "Part 1", slug: "article-slug-1", isCurrent: true },
    { id: 2, title: "Part 2", slug: "article-slug-2" },
  ]}
/>

## Content starts here...
```

### New Category Entry

```typescript
// In content/data/categories.ts
export const CATEGORYTITLES = [
  // ... existing categories (alphabetically sorted in output)
  "new-category",
] as const;
```

## Mistakes

- ❌ `z.string().uuid()` - articles don't have UUIDs
- ❌ Missing required frontmatter fields (build will fail)
- ❌ Categories not in `CATEGORYTITLES` array
- ❌ Skipping numeric prefix in filename (breaks slug generation)
- ❌ `isPublished: true` before article is ready
- ❌ Wrong date format (must be `YYYY-MM-DD`)

## Validation

After changes, run:
```bash
.claude/skills/content-layer/scripts/validate-content-patterns.sh <file>
pnpm build  # Full validation of all content
```

## File Naming Convention

Articles: `[NNNN]-[descriptive-slug].mdx`
- `NNNN`: 4-digit zero-padded number (0001, 0002, etc.)
- `descriptive-slug`: kebab-case title slug
- Example: `0005-building-a-nextjs-blog.mdx`
