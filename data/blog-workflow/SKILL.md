---
name: blog-workflow
description: Manage blog post creation, YAML frontmatter (slug, title, excerpt, categories), validate metadata, track pipeline stages, export to PDF. Use when creating blog posts, publishing, or managing blog-specific workflows.
---

# Blog Workflow

This skill provides specialized support for blog post creation, metadata management, and publishing workflows.

## Blog Post Structure

All blog posts require YAML frontmatter at the top:

```yaml
---
slug: post-url-slug
title: "Post Title"
date: Month Day, Year
excerpt: "Brief description for previews"
categories: ["Category1", "Category2"]
---
```

## YAML Frontmatter Fields

### slug
**Purpose**: URL-friendly identifier for the post

**Format**: lowercase-with-hyphens, no spaces or special characters

**Best practices**:
- Keep it short but descriptive (3-5 words)
- Use keywords from title
- Once published, don't change (breaks links)

**Examples**:
- ✅ `mcp-isnt-dead`
- ✅ `game-theory-basics`
- ✅ `weekly-writing-pipeline`
- ❌ `my-post` (too generic)
- ❌ `a-very-long-descriptive-title-for-my-post` (too long)
- ❌ `My Post!` (not URL-friendly)

### title
**Purpose**: Display title for the post

**Format**: Quoted string, Title Case or sentence case

**Best practices**:
- Compelling and specific
- 3-10 words ideal
- Matches or expands on H1 in content
- Avoid clickbait

**Examples**:
- ✅ `"MCP Isn't Dead—It's Evolving"`
- ✅ `"Game Theory for Product Decisions"`
- ✅ `"The Weekly Writing Pipeline That Works"`
- ❌ `"Post"` (too vague)
- ❌ `"You Won't Believe What I Learned About Writing!"` (clickbait)

### date
**Purpose**: Publication date

**Format**: Month Day, Year (e.g., "November 22, 2025")

**Best practices**:
- Use full month name
- Include comma after day
- Four-digit year
- Matches actual publication date

**Examples**:
- ✅ `November 22, 2025`
- ✅ `January 1, 2024`
- ❌ `11/22/2025` (wrong format)
- ❌ `Nov 22, 2025` (abbreviated month)
- ❌ `22 November 2025` (wrong order)

### excerpt
**Purpose**: Brief summary for previews, SEO, social sharing

**Format**: Quoted string, 1-2 sentences

**Best practices**:
- Compelling hook that makes reader want more
- 15-30 words ideal
- Complete sentences
- No spoilers (save the punchline for the post)
- Standalone (doesn't require reading the post)

**Examples**:
- ✅ `"Everyone thinks MCP failed. But the reports of its death are greatly exaggerated—here's why."`
- ✅ `"Game theory isn't just for economists. It's a mental model that transforms how you make product decisions."`
- ❌ `"This post is about writing."` (too vague)
- ❌ `"In this post I'll discuss..."` (boring construction)

### categories
**Purpose**: Topical tags for organization and filtering

**Format**: Array of quoted strings (JSON array syntax)

**Best practices**:
- 1-3 categories per post
- Use existing categories when possible (consistency)
- Broad enough to group posts, specific enough to be useful
- Title Case

**Examples**:
- ✅ `["Writing", "Productivity"]`
- ✅ `["AI", "Product"]`
- ✅ `["Engineering"]`
- ❌ `Writing, Productivity` (missing brackets and quotes)
- ❌ `["writing", "productivity", "tools", "techniques", "tips"]` (too many)

## Common Categories in Vault

Based on existing blog posts:
- "AI"
- "Writing"
- "Product"
- "Engineering"
- "Productivity"
- "Opinion"
- "Tutorial"

When creating new categories:
- Check existing posts first: `make search TERM="categories:"`
- Keep list manageable (10-15 categories max)
- Merge similar categories

## Blog Creation Workflow

### Method 1: Use Make Command (Recommended)
```bash
make new
# Select "blog" when prompted
# Fill in template variables
```

The `make new` command:
1. Prompts for blog metadata (title, slug, date, excerpt, categories)
2. Creates file in `blog/` directory
3. Substitutes variables in template
4. Opens file in editor

### Method 2: Manual Creation
1. Copy `templates/blog.md`
2. Save to `blog/your-slug.md`
3. Replace all `{{PLACEHOLDERS}}`
4. Start writing

## Pipeline Integration

Blog posts follow the weekly writing pipeline:

### Monday-Tuesday: Capture & Cluster
- Fragments go in daily notes, not blog drafts
- Group related ideas to identify blog-worthy topics

### Wednesday: Outline
- Create blog post file with frontmatter
- Write outline in markdown
- Don't worry about prose yet

### Thursday: Draft
- Fast draft using outline
- Mark gaps with `[TK: ...]`
- Don't edit yet

### Friday: Revise ⭐
- **Full revision**: Structure → Style → Mechanics
- Use revision-agent for systematic improvement
- Use argument-strengthener for logic
- Resolve TK placeholders (or note research needed)

### Saturday: Review
- Share with outside reader
- Get feedback: where bored, unclear, unnecessary
- Address critical issues

### Sunday: Publish
- Final polish
- Validate frontmatter
- Run checks (lint, links, export)
- Move to final state

## Publishing Checklist

Before publishing a blog post:

### Content Complete
- [ ] No `[TK: ...]` placeholders remaining
- [ ] Opening hooks reader
- [ ] Closing delivers
- [ ] All claims supported
- [ ] Examples are clear and relevant

### Frontmatter Valid
- [ ] Slug is URL-friendly and descriptive
- [ ] Title is compelling
- [ ] Date is correct format
- [ ] Excerpt is 1-2 sentences and compelling
- [ ] Categories are appropriate (1-3 tags)

### Quality Checks
- [ ] Run `make lint` - no formatting issues
- [ ] Run `make check-links` - no broken internal links
- [ ] Run `make search TERM="[TK:"` - no TK placeholders
- [ ] Read aloud once - catches awkward phrasing

### Export Test
- [ ] Run `make export-blog POST=blog/filename.md`
- [ ] Review PDF - formatting looks good
- [ ] PDF matches markdown (no export errors)

### Git Commit
- [ ] Clear commit message
- [ ] Staged only the blog post (not unrelated changes)

## Frontmatter Generation

### Auto-generating Slugs
Convert title to slug:
1. Lowercase everything
2. Replace spaces with hyphens
3. Remove special characters
4. Remove articles (a, an, the) if too long

**Examples**:
- "MCP Isn't Dead" → `mcp-isnt-dead`
- "The Weekly Writing Pipeline" → `weekly-writing-pipeline`
- "5 Game Theory Principles" → `5-game-theory-principles`

### Auto-generating Excerpts
Techniques for creating compelling excerpts:

1. **Problem-Solution**: "Everyone faces [problem]. Here's why [solution works]."
2. **Contrarian**: "Everyone thinks [common belief]. But here's why they're wrong."
3. **Curiosity Gap**: "I discovered [surprising thing] while [doing X]."
4. **Big Promise**: "Here's how [technique] changed [outcome]."

**From blog opening**:
- If opening is strong, it often works as excerpt
- If not, write dedicated excerpt (don't excerpt later content)

### Auto-generating Categories
Based on post content:

1. **Scan for keywords**: What topics appear most?
2. **Check existing categories**: Which fit best?
3. **Primary + Secondary**: Main topic + approach
   - Example: ["AI", "Product"] = AI topic, product angle
   - Example: ["Writing", "Tutorial"] = writing topic, how-to format

**Decision tree**:
- Is it about AI/technology? → "AI"
- Is it about writing craft? → "Writing"
- Is it about product decisions? → "Product"
- Is it about engineering/code? → "Engineering"
- Is it a how-to? → "Tutorial"
- Is it an opinion piece? → "Opinion"
- Is it about productivity? → "Productivity"

## Export to PDF

### Basic Export
```bash
make export-blog POST=blog/filename.md
```

This command:
1. Strips YAML frontmatter (not needed in PDF)
2. Converts markdown to PDF using Pandoc
3. Applies style.css if available
4. Outputs to `blog/filename.pdf`

### Export Requirements
- Pandoc installed
- xelatex or lualatex installed (for PDF generation)

### Export Troubleshooting

**Error: "pandoc not found"**
- Install: `brew install pandoc` (macOS)

**Error: "xelatex not found"**
- Install: `brew install --cask mactex` (macOS)

**Export works but formatting is wrong**
- Check `style.css` exists
- Verify markdown is clean (run `make lint`)

## Frontmatter Validation

### Manual Check
Review each field:
- Slug: lowercase-with-hyphens, no spaces?
- Title: quoted, compelling?
- Date: "Month Day, Year" format?
- Excerpt: quoted, 1-2 sentences?
- Categories: ["Category1", "Category2"] format?

### Common Frontmatter Errors

**Missing quotes around title/excerpt**:
```yaml
❌ title: My Post
✅ title: "My Post"
```

**Wrong date format**:
```yaml
❌ date: 11/22/2025
✅ date: November 22, 2025
```

**Categories not in array format**:
```yaml
❌ categories: Writing, AI
✅ categories: ["Writing", "AI"]
```

**Slug not URL-friendly**:
```yaml
❌ slug: My Post!
✅ slug: my-post
```

### Validation Script

Search for posts with potential frontmatter issues:
```bash
# Find posts without proper frontmatter
grep -L "^---" blog/*.md

# Find posts with malformed categories
grep -E "categories: [^[]" blog/*.md
```

## Blog Post Templates

### Standard Blog Post
Use `templates/blog.md` - works for most posts.

### Essay Format
For longer, more formal pieces:
```markdown
---
slug: slug-here
title: "Title"
date: Month Day, Year
excerpt: "Excerpt"
categories: ["Opinion", "Writing"]
---

# Title

[Opening hook - 1-2 paragraphs]

## I.

[First major section]

## II.

[Second major section]

## III.

[Third major section]

---

[Closing reflection]
```

### Tutorial Format
For how-to posts:
```markdown
---
slug: how-to-x
title: "How to X"
date: Month Day, Year
excerpt: "Learn how to X in Y steps"
categories: ["Tutorial", "Engineering"]
---

# How to X

## What You'll Learn

- Point 1
- Point 2
- Point 3

## Prerequisites

- Requirement 1
- Requirement 2

## Step 1: [Action]

[Instructions]

## Step 2: [Action]

[Instructions]

## Conclusion

[Summary and next steps]
```

## Archiving Published Posts

When a blog post is complete and published:

### Option 1: Keep in blog/
- Most blog posts stay in `blog/` directory
- They're published, not archived
- Only archive if removing from active blog

### Option 2: Archive
If post is no longer part of active blog:
```bash
# Move to archive preserving structure
mv blog/old-post.md archive/blog/old-post.md
make check-links  # Fix any broken references
```

## Multi-Part Series

For blog series (multiple related posts):

### Approach 1: Separate Files
```
blog/
  game-theory-part-1.md
  game-theory-part-2.md
  game-theory-part-3.md
```

Each has:
- Frontmatter with series indicator in categories: ["Game Theory", "Series"]
- Links to other parts at top and bottom

### Approach 2: Project Then Extract
```
projects/
  game-theory-series/
    full-manuscript.md
    outline.md
    part-1-notes.md

blog/
  [extracted posts when ready]
```

Work on full project, extract blog posts when sections are complete.

## Related Make Commands

### Content Creation
- `make new` - Create new blog post (interactive)
- `make daily` - Create daily note (for capture stage)

### Publishing
- `make export-blog POST=blog/post.md` - Export to PDF
- `make wordcount FILE=blog/post.md` - Check word count

### Quality
- `make lint` - Check formatting issues
- `make lint-fix` - Auto-fix formatting
- `make check-links` - Validate internal links
- `make search TERM="[TK:"` - Find placeholders

### Discovery
- `make search TERM="categories:"` - See all category usage
- `make recent` - See recently modified posts
- `make stats` - Vault statistics (includes blog post count)

## Instructions for Claude

When working with blog posts:

1. **Always validate frontmatter** - check format and completeness
2. **Auto-generate missing metadata** - suggest slug, excerpt, categories
3. **Respect pipeline stage** - different depth for draft vs. revision
4. **Enforce house rulebook** - clean markdown, valid links
5. **Suggest export test** - `make export-blog` before publishing
6. **Track publishing checklist** - ensure all steps complete
7. **Reference existing categories** - maintain consistency

**When creating new blog posts**:
- Suggest using `make new` for template
- Auto-generate slug from title
- Draft compelling excerpt based on opening
- Suggest appropriate categories based on content

**When revising blog posts**:
- Check frontmatter validity first
- Ensure no TK placeholders before publish
- Validate excerpt matches content
- Suggest `make check-links` and `make lint`

**When publishing**:
- Walk through publishing checklist
- Test export: `make export-blog POST=path`
- Verify frontmatter format
- Confirm ready for next stage

For more details, see:
- [frontmatter-spec.md](frontmatter-spec.md) - Complete frontmatter reference
