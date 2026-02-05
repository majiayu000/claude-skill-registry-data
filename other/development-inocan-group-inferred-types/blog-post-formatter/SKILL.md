---
name: blog-post-formatter
description: "Format blog content into properly structured markdown files for Next.js portfolio blog. Use when user wants to: (1) Format raw blog content into markdown with frontmatter, (2) Create new blog posts from topics or titles, (3) Generate blog post files with proper metadata (title, excerpt, date, author) and save to _posts/ directory. Automatically generates excerpts, converts titles to kebab-case filenames, and ensures proper frontmatter format."
---

Format blog content into properly structured markdown files for the Next.js portfolio website. All blog posts are stored in `_posts/` directory and automatically processed by the site's MDX system.

## Quick Reference

- **File location**: `_posts/{slug}.md` (slug is kebab-case of title)
- **Frontmatter format**: See [references/post-structure.md](references/post-structure.md)
- **Template**: See [assets/template.md](assets/template.md)

## Workflow

### 1. Format Existing Content

When user provides raw blog content:

1. **Extract or generate title**:
   - If first line is a heading (H1), use it as title
   - If content starts with text, extract first sentence or generate from content
   - Ensure title is clear and descriptive

2. **Generate excerpt**:
   - Extract first meaningful paragraph (150-200 characters)
   - Remove markdown formatting from excerpt
   - If no suitable paragraph, generate summary from first few sentences
   - Keep excerpt concise and engaging

3. **Set metadata**:
   - **Date**: Use current date in `YYYY-MM-DD` format if not provided
   - **Author**: Default to `'Santosh Rai'` (wrapped in single quotes)
   - **Title**: Wrap in single quotes in frontmatter

4. **Format content**:
   - Do NOT include an H1 heading in the content (the page component already displays the title from frontmatter)
   - Start content directly with paragraphs or H2 headings
   - Preserve user's original markdown formatting
   - Validate markdown syntax (code blocks, lists, links)

5. **Generate filename**:
   - Convert title to kebab-case (lowercase, hyphens for spaces)
   - Remove special characters, keep only alphanumeric and hyphens
   - Example: "Understanding JavaScript" → `understanding-javascript.md`

6. **Save file**: Write to `_posts/{slug}.md`

### 2. Create New Post

When user provides topic/title:

1. **Generate frontmatter**:
   - Use provided title or generate from topic
   - Create excerpt placeholder or generate from topic description
   - Set date to current date
   - Set author to `'Santosh Rai'`

2. **Create structure**:
   - Do NOT add an H1 heading (the page component already displays the title from frontmatter)
   - Start content directly with paragraphs or H2 headings
   - Add placeholder sections or basic outline
   - Use template from `assets/template.md` as starting point

3. **Save file**: Write to `_posts/{slug}.md`

### 3. Auto-Generation Rules

**Excerpt generation**:
- Extract first paragraph (up to 200 characters)
- Remove markdown syntax (links, bold, code)
- If paragraph is too short, include next sentence
- Ensure excerpt is complete and grammatically correct

**Title to slug conversion**:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters (keep only alphanumeric and hyphens)
- Remove leading/trailing hyphens
- Examples:
  - "What is JavaScript?" → `what-is-javascript`
  - "Design Patterns With VBA" → `design-patterns-with-vba`
  - "Simple calculator in javascript using MVC pattern" → `simple-calculator-in-javascript-using-mvc-pattern`

**Date format**: Always use `YYYY-MM-DD` (e.g., `'2024-01-20'`)

## Frontmatter Format

All posts must include this exact frontmatter structure:

```yaml
---
title: 'Post Title'
excerpt: 'Brief description'
date: 'YYYY-MM-DD'
author: 'Santosh Rai'
---
```

**Important**: All values must be wrapped in single quotes.

## Validation

Before saving, verify:
- Frontmatter has all required fields (title, excerpt, date, author)
- Date is in YYYY-MM-DD format
- All frontmatter values are wrapped in single quotes
- Content does NOT start with an H1 heading (title is displayed from frontmatter)
- Filename is valid kebab-case slug
- File will be saved in `_posts/` directory

## Examples

**Example 1: Format existing content**
```
User: "Here's my blog post about JavaScript closures..."

Output: Creates _posts/javascript-closures.md with:
- Title extracted/generated from content
- Excerpt from first paragraph
- Current date
- Properly formatted markdown
```

**Example 2: Create new post**
```
User: "Create a blog post about React hooks"

Output: Creates _posts/react-hooks.md with:
- Title: "React Hooks"
- Generated excerpt about React hooks
- Current date
- Basic structure starting with content (no H1 heading)
```

## Reference Files

- **Post structure details**: See [references/post-structure.md](references/post-structure.md) for complete format specification and examples
- **Template**: See [assets/template.md](assets/template.md) for reusable blog post template

## Integration

The formatted files integrate automatically with the existing blog system:
- `lib/mdx.ts` reads all `.md` files from `_posts/`
- Posts are sorted by date (newest first)
- Individual posts accessible at `/blog/[slug]`
- Blog listing at `/blog` displays all posts
