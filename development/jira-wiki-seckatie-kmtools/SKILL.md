---
name: jira-wiki
description: Jira Wiki Markup (Text Formatting Notation) for formatting issue descriptions, comments, and custom fields. NOT Markdown—Jira uses different syntax. Use when formatting Jira text, creating tables/panels/code blocks in Jira, linking users/issues/attachments, writing Jira templates, or when any Jira formatting question arises. Triggers include "Jira markup", "Jira formatting", "Jira table", "Jira code block", "Jira panel", "link in Jira", "format Jira comment/description", "Jira wiki syntax".
---

# Jira Wiki Markup

Jira uses Wiki-style markup, **not Markdown**. Key differences from Markdown:

| Element | Markdown | Jira Wiki |
|---------|----------|-----------|
| Bold | `**text**` | `*text*` |
| Italic | `*text*` | `_text_` |
| Headings | `# ## ###` | `h1. h2. h3.` |
| Code inline | `` `code` `` | `{{code}}` |
| Links | `[text](url)` | `[text\|url]` |
| Images | `![alt](url)` | `!url!` |
| Tables | `\|` separators | `\|\|` headers, `\|` cells |

## Quick Reference

### Text Effects
```
*bold*  _italic_  -strikethrough-  +underline+
^superscript^  ~subscript~  {{monospace}}
??citation??  {color:red}colored{color}
```

### Headings
```
h1. Largest
h2. Large
h3. Medium (most common for sections)
```

### Links
```
[http://example.com]                    Plain URL
[Link Text|http://example.com]          URL with text
[~username]                             User mention (notifies them)
[^attachment.ext]                       Link to attachment
[PROJ-123]                              Issue link (auto-detected)
```

### Lists
```
* Bullet item              # Numbered item
** Nested bullet           ## Nested number
- Alternative bullet       #* Mixed: number then bullet
```

### Tables
```
||Header 1||Header 2||Header 3||
|Cell 1|Cell 2|Cell 3|
|Cell 4|Cell 5|Cell 6|
```

### Code and Preformatted Text

**Code block with syntax highlighting:**
```
{code:python}
def hello():
    return "world"
{code}
```

**Plain preformatted (no highlighting):**
```
{noformat}
Preserves whitespace, no *formatting* applied
{noformat}
```

### Panels and Quotes

**Quote (for citations):**
```
bq. Single paragraph quote

{quote}
Multi-paragraph
quoted content
{quote}
```

**Panel (for callouts/notices):**
```
{panel:title=Warning|bgColor=#FFFFCE}
Important message here
{panel}
```

### Breaks
```
\\              Force line break
----            Horizontal rule
---             Em dash (—)
--              En dash (–)
```

## When to Use What

| Need | Use |
|------|-----|
| Highlight important info | `{panel:title=Note}` |
| Quote someone/something | `bq.` or `{quote}` |
| Show code/logs/errors | `{code:language}` |
| Preserve spacing without highlighting | `{noformat}` |
| Notify a team member | `[~username]` |
| Reference an issue | Just type `PROJ-123` |
| Structured data | Tables with `\|\|` and `\|` |

## Common Patterns

### Status Update
```
h3. Status
*Current:* In progress
*Blockers:* None
*Next steps:* Complete testing

h3. Details
Description here...
```

### Bug Description
```
h3. Steps to Reproduce
# Step one
# Step two
# Step three

h3. Expected vs Actual
||Expected||Actual||
|Should show X|Shows Y|

{code:title=Stack Trace}
Error details here
{code}
```

### Decision Record
```
h3. Decision
We chose option B.

{panel:title=Rationale}
Explanation of why...
{panel}

h3. Alternatives Considered
* Option A - rejected because...
* Option C - rejected because...
```

## Escaping

Use backslash to show literal characters: `\*not bold\*` → \*not bold\*

## Additional References

- **Complete syntax reference**: See [references/complete-syntax.md](references/complete-syntax.md)
- **Templates**: See [references/templates.md](references/templates.md) for meeting notes, feature requests, etc.
- **Emoticons**: See [references/emoticons.md](references/emoticons.md) for the full emoticon list
