---
name: astro-content
description: Create Astro/Starlight MDX content pages. Use when the user says "write a new article", "add a blog post", "create content in Tech/Life category", or "add an MDX page".
---

# astro-content

Create Astro/Starlight MDX content pages.

## Trigger Examples

- "Write a new article"
- "Add an article to Tech category"
- "Create a blog post"
- "Add an MDX page"

## Directory Structure

```
app/src/content/docs/
├── about-me/          # About Me section
│   └── overview.mdx
├── tech/              # Tech articles
│   └── *.mdx
└── life/              # Life articles
    └── *.mdx
```

## Execution Flow

### 1. Confirm Category

Ask user for category:

| Category | Purpose |
|----------|---------|
| tech | Technical articles (Cloud, AI, DevOps, Architecture, etc.) |
| life | Lifestyle, hobbies, journals, etc. |

### 2. Gather Article Information

Confirm the following:

- **Title**: Article title
- **Description**: One-sentence summary
- **Slug**: URL path (e.g., `tech/genkit-intro` → `/tech/genkit-intro/`)
- **Draft**: Whether it's a draft (default: false)

### 3. Create MDX File

**File path**: `app/src/content/docs/{category}/{slug}.mdx`

**Frontmatter template**:

```yaml
---
title: <title>
description: <description>
draft: true  # Only if draft
---
```

**With hero image**:

```yaml
---
title: <title>
description: <description>
hero:
  tagline: <subtitle>
  image:
    alt: <image description>
    file: ../../../assets/<image-file>
---
```

### 4. Update sidebar.ts

Add new article to `app/src/sidebar.ts`:

```typescript
{
  label: "Tech",
  items: [
    { label: "<Article Title>", slug: "tech/<slug>" },
  ],
},
```

### 5. Assets (Optional)

If using images:

1. Place image in `app/src/assets/`
2. Import and use in MDX:

```mdx
import myImage from '../../../assets/my-image.png';

<img src={myImage.src} alt="Description" style="..." />
```

## Content Guidelines

1. **Language**: English or Japanese (follow user preference)
2. **Markdown**: Use GitHub Flavored Markdown
3. **Headings**: Start with `##` (`#` is auto-generated from title by Starlight)
4. **Lists**: Use bullet points for readability
5. **Code blocks**: Always specify language (`typescript`, `bash`, etc.)
6. **Emoji**: Use sparingly (only when user explicitly requests)

## Post-Creation Verification

After creation, suggest:

```bash
cd app && npm run build && npm run lint && npm run typecheck
```

Verify build succeeds.
