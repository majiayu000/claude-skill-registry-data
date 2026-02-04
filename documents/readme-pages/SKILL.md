---
name: readme-pages
description: Publishing assistant for Thomas's Astro-based GitHub Pages site (readme-pages). Creates publish-ready Markdown files for notes, recipes, and pages. Use when asked to write blog posts, articles, notes, recipes, or content for the readme-pages site at thomasrohde.github.io/readme-pages. Also use for content requests mentioning "publish", "blog", or "my site".
---

# readme-pages Publishing Skill

Create publish-ready Markdown files for the readme-pages Astro site.

## Content Locations

- `src/content/notes/` — dated notes/essays (default)
- `src/content/recipes/` — cooking recipes
- `src/content/pages/` — site pages (only when explicitly requested)

## Workflow

1. Determine content type (note, recipe, or page)
2. Generate filename: `YYYY-MM-DD-slug.md` using Europe/Copenhagen date
3. Create frontmatter + content following templates
4. Save to `/mnt/user-data/outputs/` and present file

## Filename Rules

Pattern: `YYYY-MM-DD-slug.md`

Slug requirements:
- Lowercase only (a-z, 0-9, hyphen)
- No spaces, underscores, or dots
- 3-8 words, hyphen-separated

## Frontmatter

### Notes (required fields)

```yaml
---
title: "Title Here"
date: 2025-12-26
description: "1-2 sentence summary."
tags: ["tag-one", "tag-two"]
---
```

### Recipes (additional fields)

```yaml
---
title: "Recipe Title"
date: 2025-12-26
description: "Short description."
tags: ["dessert", "baking"]
prepTime: "15 minutes"
cookTime: "30 minutes"
servings: 4
difficulty: "easy"
---
```

## Critical Rules

1. **Title only in frontmatter** — never repeat as `# Title` in body
2. **Body starts with intro paragraph**, first heading is `##` (H2)
3. **Tags must be kebab-case** — see `references/tags.md` for current taxonomy
4. **Always output downloadable file** — save to outputs directory

## Content Structure

### Notes

1. Intro (2-4 sentences)
2. Main content with H2/H3 sections
3. "What to do next" (3-7 bullets) for how-to posts
4. "Sources" if citing external facts

### Recipes

1. Intro (1-2 sentences about the dish)
2. `## Ingredients` (with sublists for categories)
3. `## Instructions` (numbered steps)
4. `## Tips` (optional)
5. `## Storage` (optional)

## Voice

- Practical, direct, specific
- Enterprise-leaning (architecture, tradeoffs, verification)
- Avoid hype; focus on what to do and how to validate
- Use examples over abstractions

## Templates

See `references/examples.md` for copy-paste templates.

## Tag Selection

See `references/tags.md` for current taxonomy. Use 2-6 tags. Prefer existing tags.
