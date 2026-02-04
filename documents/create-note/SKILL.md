---
name: create-note
description: Use when user wants to capture learnings, document insights, or create a draft blog post from their current project
---

# Create Note - Draft Blog Post

Create a draft blog post from learnings in any project, saved to your blog.

## When to Use

- User says `/note` or wants to document something
- User discovered something interesting while coding
- User solved a tricky problem worth sharing
- User wants to capture context for a future blog post

## Configuration

This skill requires `BLOG_CONTENT_DIR` to be set in your `CLAUDE.md`:

```markdown
## Blog Configuration
BLOG_CONTENT_DIR=/path/to/your/blog/content/directory
```

Example: `BLOG_CONTENT_DIR=/Users/you/portfolio/src/content/blog`

**If not configured**: Ask the user where their blog markdown files should be saved before proceeding.

## Workflow

### Step 0: Check Configuration

First, check if `BLOG_CONTENT_DIR` is set in the project's or user's `CLAUDE.md`.

If NOT set, ask the user:
```
Where should blog posts be saved?

Please provide the absolute path to your blog content directory
(e.g., /Users/you/site/content/blog)

You can also add this to your CLAUDE.md to skip this prompt:
BLOG_CONTENT_DIR=/your/path/here
```

Store their answer and use it for the rest of the session.

### Step 1: Gather Information

Ask the user:
1. **What did you learn or want to document?** (becomes the title)
2. **Can you give a brief description?** (1-2 sentences for the description field)
3. **Any code snippets or examples to include?** (optional)
4. **What tags apply?** (suggest based on project context)

### Step 2: Determine Project Context

Identify the current project to tag the post:
```bash
# Get project name from current directory
basename $(pwd)

# Or from git remote
git remote get-url origin 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//'
```

### Step 3: Generate Slug

Convert the title to a URL-friendly slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Keep it concise (3-5 words ideal)

Example: "How to use Astro Content Collections" -> `astro-content-collections`

### Step 4: Create Blog Post

Create the file at:
```
{BLOG_CONTENT_DIR}/{slug}.md
```

**Template:**
```markdown
---
title: "{title}"
date: {YYYY-MM-DD}
description: "{description}"
tags: ["{project-name}", ...other-tags]
draft: true
---

{User's content here}

{Any code snippets with proper language fencing}

{Context about why this is interesting/useful}
```

### Step 5: Confirm and Optionally Commit

Show the user:
```
Created draft: {slug}.md

Title: {title}
Tags: {tags}
Location: {BLOG_CONTENT_DIR}/{slug}.md

Would you like to commit this draft? (y/n)
```

If yes, commit to the blog repo:
```bash
cd {BLOG_CONTENT_DIR}
git add {slug}.md
git commit -m "draft: {title}"
```

## Frontmatter Schema

Required fields:
- `title` (string) - Post title
- `date` (date) - YYYY-MM-DD format
- `draft` (boolean) - Always `true` for new notes

Optional fields:
- `description` (string) - Brief summary
- `tags` (string[]) - Array of tags

## Example

User is working on import-magic and says `/note`:

```
> What did you learn?
"How to handle ESM vs CommonJS imports dynamically"

> Brief description?
"A technique for detecting and handling both module systems"

> Any code to include?
[user pastes code]

> Tags? (suggesting: import-magic, javascript)
"javascript, esm, commonjs"
```

Creates `{BLOG_CONTENT_DIR}/esm-commonjs-dynamic-imports.md`:

```markdown
---
title: "How to handle ESM vs CommonJS imports dynamically"
date: 2025-12-31
description: "A technique for detecting and handling both module systems"
tags: ["import-magic", "javascript", "esm", "commonjs"]
draft: true
---

[Content here...]
```

## Notes

- Always set `draft: true` - use `/blog` from portfolio to publish
- Include the source project as a tag for easy filtering
- Keep the initial draft concise - can flesh out later with `/blog`
