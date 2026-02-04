---
name: create-content
description: Create new pages or notes in the readme-pages project. Use when the user asks to create, add, or write a new page, note, article, or blog post. This skill handles file creation with proper frontmatter, filename conventions, and placement in the correct content collection.
---

# Create Content Skill

This skill creates new markdown content files for the readme-pages Astro site.

## Content Types

### Notes (`src/content/notes/`)
Dated entries like blog posts, updates, or time-sensitive content.

**Filename convention**: `YYYY-MM-DD-slug.md` (date prefix optional but recommended)
- Example: `2025-12-25-my-new-note.md`
- Date extracted automatically from filename prefix

**Frontmatter**:
```yaml
---
title: "Note Title"           # Required (auto-generated from filename if omitted)
date: 2025-12-25              # Required (auto-extracted from filename or defaults to today)
description: "Summary"        # Optional, max 500 chars
tags:                         # Optional, lowercase alphanumeric with hyphens
  - javascript
  - tutorial
draft: false                  # Optional, set true to hide from publication
---
```

### Pages (`src/content/pages/`)
Evergreen documentation pages without dates.

**Filename convention**: `slug.md`
- Example: `getting-started.md`

**Frontmatter**:
```yaml
---
title: "Page Title"           # Required (auto-generated from filename if omitted)
description: "Description"    # Optional, max 500 chars
order: 1                      # Optional, controls sidebar ordering
---
```

## Workflow

### To create a new note:

1. Determine the slug from the user's topic (kebab-case)
2. Use today's date or a specified date
3. Create the file at `src/content/notes/YYYY-MM-DD-slug.md`
4. Include frontmatter with title, date, and optional tags/description
5. Add the markdown content

### To create a new page:

1. Determine the slug from the user's topic (kebab-case)
2. Create the file at `src/content/pages/slug.md`
3. Include frontmatter with title and optional description/order
4. Add the markdown content

## Validation Rules

- **Title**: 1-200 characters, required
- **Date** (notes only): Must be between 2000-01-01 and today (no future dates)
- **Tags**: Lowercase alphanumeric with hyphens only, 1-50 chars each
- **Description**: Max 500 characters

## Auto-Generation

The site automatically handles:
- Missing title: Generated from filename (converted to Title Case)
- Missing date (notes): Extracted from `YYYY-MM-DD-` prefix, or defaults to today
- Table of contents from headings
- Reading time estimates
- Last modified dates from git history
- Related notes based on tag overlap

## Examples

### Minimal Note
```markdown
---
title: "Getting Started with TypeScript"
date: 2025-12-25
tags:
  - typescript
  - tutorial
---

Your content here...
```

### Minimal Page
```markdown
---
title: "Installation Guide"
order: 1
---

Your content here...
```

## Ask User For

When creating content, gather:
1. **Type**: Note or Page?
2. **Title**: What should it be called?
3. **Content**: What should it contain? (or ask if they want to provide it)
4. **Tags** (notes only): Any tags to categorize it?
5. **Draft**: Should it be published immediately or saved as draft?
