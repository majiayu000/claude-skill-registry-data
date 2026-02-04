---
name: julien-ref-notion-markdown
description: Complete markdown guide for Universal Notion Uploader. Covers 14 element types (headings, callouts, highlights, toggles, embeds, columns, databases), upload modes, and API constraints.
triggers:
  - importer markdown dans notion
  - upload to notion
  - mettre mon README dans Notion
  - convertir markdown en page notion
  - push markdown to notion
  - format for notion
  - notion markdown
  - notion uploader
  - notion callout
  - notion table
  - notion database
  - notion toggle
  - notion embed
  - notion columns
---

# Markdown Structuring Guide for Universal Notion Uploader

Guide for LLMs generating markdown destined to be uploaded to Notion via the Universal Notion Uploader parser.

---

## Parser Architecture

**MarkdownParser** (pages): AdmonitionParser, RichTextParser, TableParser, ImageParser
**DatabaseParser**: YAML frontmatter → Notion databases with relations

---

## Supported Elements

### 1. Headings (H1-H3 Only)

```markdown
# Heading 1
## Heading 2
### Heading 3
```

**Notion API**: `heading_1`, `heading_2`, `heading_3`

**Limitations**: Maximum 3 levels. H4+ NOT supported by Notion.

**Workaround for H4+**: Use **bold paragraph**
```markdown
**Pseudo-Heading 4**
Content of the section...
```

#### Collapsible Headings

```markdown
##+ Collapsible Section
Content under this heading.
Will collapse/expand in Notion.

## Next Section (stops collapsible)
```

**Syntax**: `#+`, `##+`, `###+` followed by title

**Notion API**: `heading_X` with `is_toggleable: true` and nested `children`

---

### 2. Rich Text (Inline Formatting)

```markdown
**bold** or __bold__
*italic* or _italic_
`code inline`
~~strikethrough~~
[links](https://example.com)
**[bold link](url)**
*[italic link](url)*
=={highlighted text}==
=={colored text}==blue
```

- Combine freely: `**bold *and italic***`
- Parser handles overlaps automatically
- Auto-chunking if text > 2000 chars (API limit)

#### Highlights (Colored Backgrounds)

```markdown
=={default yellow}==
=={blue text}==blue
=={red warning}==red
=={green success}==green
```

**Colors**: yellow (default), blue, red, green, purple, pink, gray, orange, brown

---

### 3. Callouts (4 Syntaxes Supported)

#### GitHub GFM (PREFERRED)
```markdown
> [!NOTE]
> This is an important note.
> Can contain multiple lines.
```

**Types**: NOTE, TIP, IMPORTANT, WARNING, CAUTION, DANGER, INFO, EXAMPLE

#### Python-Markdown
```markdown
!!! note "Optional Title"
    Indented content.
```

#### MyST Markdown
```markdown
:::note Optional Title
Content without indentation.
:::
```

#### Docusaurus
```markdown
:::tip
Content directly.
:::
```

**Type → Emoji Mapping**:
| Type | Emoji | Color |
|------|-------|-------|
| NOTE | 📝 | blue_background |
| TIP | 💡 | yellow_background |
| IMPORTANT | ❗ | purple_background |
| WARNING | ⚠️ | orange_background |
| CAUTION | 🚨 | red_background |
| DANGER | 🔥 | red_background |
| INFO | ℹ️ | blue_background |
| EXAMPLE | 📖 | gray_background |

**DO NOT** mix syntaxes in the same callout.

---

### 4. Lists

#### Unordered Lists
```markdown
- Item 1
- Item 2
  - Nested item (indentation)
- Item 3
```

Variants: `-`, `*`, `+`

#### Ordered Lists
```markdown
1. First item
2. Second item
   1. Nested item
3. Third item
```

#### Task Lists (To-Do)
```markdown
- [ ] Uncompleted task
- [x] Completed task
- [X] Also completed (uppercase supported)
```

**Notion API**: `to_do` block with `checked: true/false`

Rich text works in list items:
```markdown
- **Bold item** with *italic*
- [ ] Task with `inline code`
- Item with [link](url)
```

---

### 5. Code Blocks

```markdown
```python
def hello():
    print("Hello world")
```
```

- **Always specify language** after ` ``` `
- If unknown language, use `plain text`
- No rich text in code blocks (raw text only)
- Long code (>2000 chars) auto-chunked

---

### 6. Tables

```markdown
| Name | **Status** | Count |
| ---- | ---------- | ----- |
| foo  | *active*   | 42    |
| bar  | inactive   | 0     |
```

**Rich text in cells**: Bold, italic, code inline, links supported

**Recommendations**:
- Prefer ≤ 10 columns for readability (warning beyond)
- No strict technical limit
- Structure: Header row → Separator row → Data rows

---

### 7. Blockquotes

```markdown
> This is a normal quote.
> Can contain multiple lines.
```

**Distinction with callouts**:
```markdown
> Simple blockquote       → Notion quote block
> [!NOTE] Callout         → Notion callout block
```

Rich text supported in quotes.

---

### 8. Images

#### External Images (URLs)
```markdown
![Alt text](https://example.com/image.png)
```

#### Local Images
```markdown
![Alt text](./images/photo.jpg)
```

- Relative paths resolved from `base_dir` config
- Local images require upload (slower)
- Alt text recommended but not displayed in Notion (API limitation)

---

### 9. Toggle Blocks (Collapsible Sections)

```markdown
<details>
<summary>Click to expand</summary>

Hidden content here.
Can contain **any markdown**: lists, code, tables.

</details>
```

**Notion API**: `toggle` block with nested `children`

- Opening tag: `<details>` (case-insensitive)
- Summary line: `<summary>Title</summary>` (line 2)
- Closing tag: `</details>`
- Supports nested markdown including nested toggles

---

### 10. Embeds

```markdown
<!-- embed: https://www.youtube.com/watch?v=VIDEO_ID -->
<!-- embed: https://figma.com/file/xxx -->
```

**Notion API**: `embed` or `video` block

**Supported**: YouTube, Vimeo, Figma, Google Maps, Google Drive, CodePen, GitHub Gist, Miro

---

### 11. Column Layouts

```markdown
<!-- columns: 2 -->
**Left Column**

Content here.

---column---

**Right Column**

More content.
<!-- /columns -->
```

**Notion API**: `column_list` with `column` children

**Supported**: 2, 3, 4+ columns (Notion auto-sizes equally)

---

### 12. Dividers (Horizontal Rules)

```markdown
---
***
___
```

**Notion API**: `divider` block

---

### 13. Internal Links

```markdown
See [[Other Document]] for details.
Link to [[Specific Section#heading]].
```

**Feature**: `resolve_internal_links: true` in config

**Behavior**:
- `[[Page Name]]` → Resolved to Notion page link after upload
- Two-pass upload: First upload all pages, then resolve links
- Unresolved links become plain text

---

### 14. Databases from Markdown

Create Notion databases from markdown files with YAML frontmatter.

#### Database File Structure

```markdown
---
type: database
name: My Database
icon: 📊
description: Database description

properties:
  Name:
    type: title
  Status:
    type: select
    options:
      - Todo
      - In Progress
      - Done
  Date:
    type: date
  Count:
    type: number
  Active:
    type: checkbox
  Related:
    type: relation
    database: Other Database Name
---

| Name | Status | Date | Count | Active |
|------|--------|------|-------|--------|
| Item 1 | Todo | 2025-01-15 | 42 | true |
| Item 2 | Done | 2025-01-16 | 0 | false |
```

#### Supported Property Types

**Basic**: `title` (required), `rich_text`, `number`, `checkbox`, `date`
**Selection**: `select`, `multi_select`
**Links**: `url`, `email`, `phone_number`
**Relations**: `relation`, `rollup`, `formula` (computed)

#### Database Relations

Link databases together:

```yaml
properties:
  Category:
    type: relation
    database: Categories DB    # Name of target database
```

**Registry**: Parser maintains database registry for relation resolution.

---

## Upload Modes

Configure in `upload_config.yaml`:

### MIXED (Recommended for docs)
```yaml
mode: "mixed"
```
- Root page = Index with folder headings
- Each `.md` file = child page
- Navigation footers on all pages

### HIERARCHICAL (Folder preservation)
```yaml
mode: "hierarchical"
```
- Folders → Notion pages
- Files → Sub-pages
- Recreates exact folder structure

### SEQUENTIAL (Linear reading)
```yaml
mode: "sequential"
```
- All files at same level
- Prev/Next navigation between pages
- Good for tutorials

### Configuration Features
```yaml
features:
  table_of_contents: true      # Add TOC at top
  page_navigation: true        # Add prev/next footers
  image_upload: true           # Upload local images
  resolve_internal_links: true # Convert [[links]]
  flush_before_upload: false   # Delete existing content first
```

---

## Parsing Order (Priority)

1. **Tables** (multi-line, high priority)
2. **Code blocks** (multi-line)
3. **Callouts** (multi-line, 4 syntaxes)
4. **Images** (single line)
5. **Headings** (H1-H3)
6. **Task lists** (`- [ ]` / `- [x]`) - BEFORE unordered lists
7. **Unordered lists** (`-`, `*`, `+`)
8. **Ordered lists** (`1.`, `2.`)
9. **Blockquotes** (`> text`)
10. **Paragraphs** (fallback)

---

## NOT Supported

Footnotes (`[^1]`), Definition lists, HTML inline, Emoji shortcodes (`:smile:`), H4-H6 headings, Nested blockquotes (`>>`), Indented code blocks

---

## Patterns to Avoid

| Pattern | Problem | Solution |
|---------|---------|----------|
| `#### H4` | Not supported | Use `### H3` or `**Bold text**` |
| >12 columns | Hard to read | Split tables |
| Callout without `>` | Breaks parsing | Every line needs `>` prefix |
| Code without language | Suboptimal | Always specify language |

---

## LLM Pre-Upload Checklist

- [ ] Headings max H3 (no H4+)
- [ ] Callouts use valid syntax (prefer GFM)
- [ ] Tables compact (≤ 10 columns recommended)
- [ ] Code blocks have language specified
- [ ] Task lists use `- [ ]` and `- [x]`
- [ ] Images use URLs or valid paths
- [ ] Rich text in paragraphs/lists/tables/tasks
- [ ] No HTML inline
- [ ] No unsupported syntax (footnotes, definition lists)

---

## Related Skills

- **julien-ref-doc-production**: Use for documentation structure before uploading to Notion
