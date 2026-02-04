---
name: markdown
description: Transform AI markdown generation to be 100% markdownlint-compliant. Use this skill whenever generating messages containing markdown, generating or editing markdown files (.md) for technical documentation, README files, guides, tutorials, or any GFM content requiring clean, professional presentation.
license: MIT. See LICENSE for complete terms
---

# GitHub Flavored Markdown Generation

**Version:** 1.2.0

Generate GFM that passes markdownlint validation with zero violations.

## Core Principles

### 1. Blank Lines Are Mandatory

- Before/after ALL lists (MD032)
- Before/after ALL headings except document start (MD022)
- Before/after ALL code blocks (MD031)
- Between ALL block-level elements

### 2. Consistency Required

- Use `-` for lists
- Use `#` for headings (ATX)
- Regular spaces only—never tabs/nbsp

### 3. Structure Matters

- Heading hierarchy: 1→2→3 (not 1→3)
- ONE H1 per document
- Files end with one newline
- Lines under 80 chars

### 4. Invisible Characters Matter

- Use ONLY regular spaces (U+0020)
- Never non-breaking spaces (U+00A0, &nbsp;)
- Never tabs
- UTF-8 encoding

## Pre-Generation Checklist

- [ ] Where will lists/headings/code appear?
- [ ] Heading levels verified (1→2→3)?
- [ ] Using `-` for all lists?
- [ ] Code languages specified?
- [ ] Lines under 80 chars?
- [ ] Line breaks needed? (two trailing spaces)
- [ ] Using regular spaces only?
- [ ] URLs wrapped in `<>` or `[]`?
- [ ] Document starts with H1?
- [ ] Ordered lists use `1.` for all items?
- [ ] File ends with single newline?

## Essential Rules

### Lists (MD032, MD004)

```markdown
Text before.

- Item one
- Item two

Text after.
```

### Headings (MD001, MD022)

```markdown
Text.

## Heading

Content.
```

### Code Blocks (MD031, MD040)

````markdown
Text.

```python
code()
```

Text.
````

**Nested Fences:** When showing markdown examples that contain code blocks,
use **one more backtick** than the deepest level:

- Three backticks (` ``` `): Regular code
- Four backticks (` ```` `): Markdown examples with code
- Five backticks (` ````` `): Nested markdown examples

`````markdown
````markdown
# Example

```bash
command
```

````
`````

### Line Length (MD013)

Break long lines at natural points. Use reference-style links for long URLs.

### URLs and Email (MD034)

Wrap bare URLs and emails:

```markdown
Wrong: https://example.com
Right: <https://example.com>
Right: [link](https://example.com)

Wrong: user@example.com
Right: <user@example.com>
```

### Document Structure (MD041)

Start with H1 (or front matter then H1):

```markdown
# Document Title

First paragraph.
```

### Ordered Lists (MD029)

Use `1.` for all items:

```markdown
1. First
1. Second
1. Third
```

### File Endings (MD047)

End with single newline:

```text
Last content line.
[single newline]
[EOF]
```

### Character Encoding

**Detection:** View → Render Whitespace in VS Code

**Fix:** Find `\u00A0` → Replace with space

**Critical for AI:** Two trailing spaces = intentional line breaks. Do NOT
remove them.

## Critical Error Patterns

### 1. List Without Blank Lines

<!-- markdownlint-disable MD032 -->

**Wrong:**

```markdown
Text:
- Item
Text.
```

<!-- markdownlint-enable MD032 -->

**Right:**

```markdown
Text:

- Item

Text.
```

### 2. Heading Without Blank Lines

<!-- markdownlint-disable MD022 -->

**Wrong:**

```markdown
Text.
## Head
Text.
```

<!-- markdownlint-enable MD022 -->

**Right:**

```markdown
Text.

## Head

Text.
```

### 3. Code Without Blanks/Language

<!-- markdownlint-disable MD031 MD040 -->

**Wrong:**

````markdown
Text:
```
code
```
Text.
````

<!-- markdownlint-enable MD031 MD040 -->

**Right:**

````markdown
Text:

```python
code
```

Text.
````

### 4. Inconsistent Markers

<!-- markdownlint-disable MD004 -->

**Wrong:**

```markdown
- Item
* Item
```

<!-- markdownlint-enable MD004 -->

**Right:**

```markdown
- Item
- Item
```

### 5. Skipping Levels

<!-- markdownlint-disable MD001 -->

**Wrong:**

```markdown
# Title

### Sub (skipped H2)
```

<!-- markdownlint-enable MD001 -->

**Right:**

```markdown
# Title

## Section

### Sub
```

## Post-Generation Validation

1. Lists have blank lines before/after
2. Headings have blank lines before/after
3. Code has blank lines before/after
4. Heading progression: 1→2→3→4
5. All lists use `-`
6. All code has language
7. Lines under 80 chars
8. Document starts with H1
9. URLs wrapped properly
10. Ordered lists use `1.`
11. File ends with one newline
12. Two trailing spaces used intentionally
13. Only regular spaces (no nbsp/tabs)

## Mental Model

Markdown is **blocks with mandatory spacing:**

```text
[Text Block]
↓ BLANK LINE ↓
[Heading Block]
↓ BLANK LINE ↓
[List Block]
↓ BLANK LINE ↓
[Code Block]
↓ BLANK LINE ↓
[Text Block]
[EOF]
```

Every block transition = blank line required.

## Quick Patterns

**List:**

```markdown
text

- item

text
```

**Heading:**

```markdown
text

## Head

text
```

**Code:**

````markdown
text

```lang
code
```

text
````

**Nested:**

```markdown
- parent
  - child
- parent
```

**Ordered:**

```markdown
text

1. item
1. item

text
```

## Common Languages

**Programming:** `python` `javascript` `java` `c` `cpp` `go` `rust` `ruby`
`php` `swift` `kotlin` `typescript`

**Shell:** `bash` `sh` `powershell` `cmd` `zsh`

**Markup:** `html` `css` `xml` `json` `yaml` `toml` `markdown`

**Database:** `sql` `postgresql` `mysql`

**Other:** `text` `diff` `log`

## Validation

```bash
markdownlint filename.md
```

Goal: Zero errors/warnings.

## Additional Resources

See bundled references:

- `references/complete-rules.md` - Full rule catalog
- `references/edge-cases.md` - Platform quirks
- `references/examples.md` - Detailed examples

## Remember

Most common: Missing blank lines around lists/headings/code.

**Two trailing spaces:** Intentional line breaks. Do NOT remove.

When in doubt:

1. Add blank lines before/after blocks
2. Use `-` for lists
3. Use `#` for headings
4. Specify code language
5. Increment headings by one
6. Use regular spaces only
7. Two trailing spaces = line break
