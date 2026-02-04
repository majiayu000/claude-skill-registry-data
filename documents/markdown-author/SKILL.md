---
name: markdown-author
description: Write quality markdown content. Use when creating or editing .md files, documentation, READMEs, or any markdown-based content. Ensures proper syntax, structure, and accessibility.
allowed-tools: Read, Write, Edit
---

# Markdown Authoring Skill

This skill ensures markdown documents follow best practices for syntax, structure, accessibility, and content quality.

## Markdown Flavors

This project follows **CommonMark** with **GitHub Flavored Markdown (GFM)** extensions:

| Feature | CommonMark | GFM Extension |
|---------|------------|---------------|
| Headings | ✓ | |
| Emphasis | ✓ | |
| Links | ✓ | Autolinks |
| Images | ✓ | |
| Code blocks | ✓ | Syntax highlighting |
| Blockquotes | ✓ | |
| Lists | ✓ | Task lists |
| Tables | | ✓ |
| Strikethrough | | ✓ |

## Document Structure

### Single H1 Rule

Every document should have exactly one H1 heading as the title:

```markdown
# Document Title

Content begins here...

## First Section

## Second Section
```

### Heading Hierarchy

Follow logical heading levels - never skip levels:

```markdown
# Title (H1)

## Major Section (H2)

### Subsection (H3)

#### Detail (H4)

## Another Major Section (H2)
```

**Avoid:**
```markdown
# Title

### Skipped H2!  <!-- BAD: Jumped from H1 to H3 -->
```

### Document Template

```markdown
# Document Title

Brief description or introduction paragraph.

## Table of Contents

- [Section One](#section-one)
- [Section Two](#section-two)
- [Section Three](#section-three)

## Section One

Content here.

## Section Two

Content here.

## Section Three

Content here.

## Related

- [Link to related doc](./related.md)
```

## YAML Frontmatter

### Basic Frontmatter

Add metadata at the top of documents:

```markdown
---
title: Document Title
description: Brief description for SEO and previews
author: Author Name
date: 2024-01-15
tags:
  - documentation
  - guide
---

# Document Title

Content begins after frontmatter.
```

### Common Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `title` | Document title | `"Getting Started Guide"` |
| `description` | SEO/preview text | `"Learn how to..."` |
| `author` | Content author | `"Jane Doe"` |
| `date` | Publication date | `2024-01-15` |
| `updated` | Last modified | `2024-03-20` |
| `tags` | Categorization | `[guide, tutorial]` |
| `draft` | Publication status | `true` or `false` |
| `order` | Sort position | `1`, `2`, `3` |

### Blog Post Frontmatter

```markdown
---
title: How to Build Web Components
description: A comprehensive guide to creating custom elements
author: Jane Doe
date: 2024-01-15
tags:
  - javascript
  - web-components
  - tutorial
image: /images/blog/web-components.jpg
---
```

### Documentation Frontmatter

```markdown
---
title: API Reference
description: Complete API documentation
sidebar_position: 3
---
```

## Text Formatting

### Emphasis

```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___
~~strikethrough~~
```

**Prefer asterisks** (`*`) over underscores (`_`) for consistency.

### Inline Code

Use backticks for code, commands, filenames, and technical terms:

```markdown
Run `npm install` to install dependencies.
Edit the `package.json` file.
The `useState` hook manages state.
```

## Links

### Inline Links

```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title text")
```

### Reference Links

For repeated URLs or cleaner text:

```markdown
Read the [documentation][docs] for more details.
See the [API reference][api] for endpoints.

[docs]: https://example.com/docs
[api]: https://example.com/api
```

### Internal Links

Use relative paths for internal links:

```markdown
See [Getting Started](./getting-started.md)
Read the [API docs](../api/reference.md)
Jump to [Installation](#installation)
```

### Anchor Links

Link to headings using lowercase, hyphenated IDs:

```markdown
## Installation Steps

...

See [Installation Steps](#installation-steps) above.
```

### Accessible Link Text

Use descriptive link text:

```markdown
<!-- BAD -->
[Click here](./guide.md) for the guide.
For more info, [read this](./docs.md).

<!-- GOOD -->
Read the [installation guide](./guide.md).
See the [API documentation](./docs.md) for details.
```

## Images

### Basic Syntax

```markdown
![Alt text describing the image](./images/screenshot.png)
```

### Images with Titles

```markdown
![Dashboard screenshot](./images/dashboard.png "The main dashboard view")
```

### Reference Images

```markdown
![Application logo][logo]

[logo]: ./images/logo.png "Application Logo"
```

### Alt Text Guidelines

Write meaningful alt text:

```markdown
<!-- BAD -->
![](./chart.png)
![image](./chart.png)
![chart](./chart.png)

<!-- GOOD -->
![Monthly revenue chart showing 25% growth](./chart.png)
![Error dialog with retry and cancel buttons](./error-dialog.png)
```

### When to Use Empty Alt

For decorative images only:

```markdown
![](./decorative-divider.png)
```

## Code Blocks

### Fenced Code Blocks

Always specify the language for syntax highlighting:

````markdown
```javascript
function greet(name) {
  return `Hello, ${name}!`;
}
```
````

### Common Language Identifiers

| Language | Identifier |
|----------|------------|
| JavaScript | `javascript` or `js` |
| TypeScript | `typescript` or `ts` |
| HTML | `html` |
| CSS | `css` |
| JSON | `json` |
| YAML | `yaml` |
| Bash/Shell | `bash` or `shell` |
| Python | `python` or `py` |
| Markdown | `markdown` or `md` |
| Plain text | `text` or `plaintext` |

### Code Block with Filename

Use a comment or heading to indicate the file:

````markdown
**`src/utils.js`**
```javascript
export function formatDate(date) {
  return date.toISOString();
}
```
````

### Diff Syntax

Show changes with diff highlighting:

````markdown
```diff
- const old = "value";
+ const updated = "new value";
```
````

## Lists

### Unordered Lists

Use hyphens consistently:

```markdown
- First item
- Second item
- Third item
```

### Ordered Lists

```markdown
1. First step
2. Second step
3. Third step
```

### Nested Lists

Indent with 2 or 4 spaces (be consistent):

```markdown
- Parent item
  - Child item
  - Another child
    - Grandchild
- Another parent
```

### Task Lists (GFM)

```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another todo
```

### List Content

For multi-paragraph list items:

```markdown
1. First step

   Additional details about the first step.
   Can span multiple lines.

2. Second step

   More information here.
```

## Tables

### Basic Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Column Alignment

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| L    | C      | R     |
| L    | C      | R     |
```

### Table Best Practices

- Keep tables simple - complex data may need different format
- Use alignment for numeric data (right-align numbers)
- Keep cell content concise
- Consider using lists for very long content

## Blockquotes

### Basic Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
```

### Nested Blockquotes

```markdown
> Outer quote
>
> > Nested quote
```

### Callouts/Admonitions

Use blockquotes with emphasis for callouts:

```markdown
> **Note:** Important information here.

> **Warning:** Be careful about this.

> **Tip:** Helpful suggestion here.
```

Or with emoji for visual distinction:

```markdown
> 📝 **Note:** Information to highlight.

> ⚠️ **Warning:** Proceed with caution.

> 💡 **Tip:** Helpful suggestion.

> 🚨 **Danger:** Critical warning.
```

## Horizontal Rules

Use three hyphens with blank lines:

```markdown
Content above.

---

Content below.
```

## Escaping

Escape special characters with backslash:

```markdown
\*not italic\*
\# not a heading
\[not a link\]
```

## Line Breaks

### Paragraphs

Separate paragraphs with blank lines:

```markdown
First paragraph.

Second paragraph.
```

### Hard Line Breaks

Use two trailing spaces or `<br>` for line breaks within a paragraph:

```markdown
Line one
Line two (note two spaces above)

Or use:
Line one<br>
Line two
```

## Accessibility

### Heading Structure

Screen readers use headings for navigation:

- Use one H1 per document
- Don't skip heading levels
- Use headings for structure, not styling

### Descriptive Links

```markdown
<!-- Screen reader announces: "link, click here" - unhelpful -->
[Click here](./guide.md)

<!-- Screen reader announces: "link, installation guide" - clear -->
[Installation guide](./guide.md)
```

### Image Alt Text

- Describe the content and function
- Keep it concise but meaningful
- Use empty alt for decorative images

### Tables

- Use header rows
- Keep structure simple
- Provide context before complex tables

### Code Blocks

- Specify language for syntax highlighting
- Provide context before code examples
- Explain what code does, not just show it

## Content Quality

### Integration with Content Skills

The `content-writer` skill applies to markdown:

- Run spell check: `npm run lint:spelling`
- Run grammar check: `npm run lint:grammar`
- Check reading level for technical vs general content

### Consistency

- Use consistent heading capitalization (Title Case or Sentence case)
- Use consistent list markers (hyphens, not mixed)
- Use consistent code fence style (backticks, not indentation)
- Use consistent emphasis style (asterisks, not underscores)

### File Naming

```
README.md           # Repository root
CHANGELOG.md        # Version history
CONTRIBUTING.md     # Contribution guide
docs/               # Documentation folder
  getting-started.md
  api-reference.md
  troubleshooting.md
```

## Markdown Checklist

Before finalizing markdown documents:

### Structure
- [ ] Single H1 as document title
- [ ] Logical heading hierarchy (no skipped levels)
- [ ] Table of contents for long documents
- [ ] Frontmatter with appropriate metadata

### Content
- [ ] Descriptive link text (not "click here")
- [ ] Alt text for all images (except decorative)
- [ ] Language specified for code blocks
- [ ] Spell check passed

### Formatting
- [ ] Consistent list markers
- [ ] Consistent emphasis style
- [ ] Proper table alignment
- [ ] Blank lines around blocks (headings, code, lists)

### Links
- [ ] Internal links use relative paths
- [ ] External links work
- [ ] Anchor links match heading IDs

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Skipped heading levels | Poor accessibility | Use sequential levels |
| No code language | No syntax highlighting | Add language identifier |
| "Click here" links | Poor accessibility | Use descriptive text |
| Missing alt text | Screen readers can't describe | Add meaningful alt |
| Inconsistent lists | Visual inconsistency | Pick one marker style |
| No frontmatter | Missing metadata | Add YAML frontmatter |
| Broken internal links | 404 errors | Use relative paths, verify |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `content-writer` | Spelling, grammar, reading level |
| `i18n` | Multilingual documentation |
| `git-workflow` | Commit messages, changelogs |
