---
name: vault-obsidian-format
description: Reference for the vault's markdown conventions — frontmatter shape, block-style tags, wikilinks, dates, and special-character escaping. Use when writing or fixing note markup — "format this note properly", "fix the frontmatter", "how should tags look" — or when another skill needs the house style. NOT for creating notes end-to-end (use vault-note-factory) or bulk cleanup (use vault-cleanup-studio).
---

# Obsidian Format Guidelines

All notes must follow Obsidian-compatible markdown format.

---

## 1. Frontmatter (YAML)

**MUST be at the very top** - no content before it.

```yaml
---
tags:
  - tag1
  - tag2/subtag
field_name: value
date_field: 2025-01-04
---
```

**Rules**:
- First line = `---`
- Close with `---` before content
- No blank lines before opening `---`
- Indent with 2 spaces

---

## 2. Tags

| Location | Syntax | Example |
|----------|--------|---------|
| Frontmatter (preferred) | YAML list | `tags:\n  - jobseeking` |
| Body | Hashtag | `#jobseeking` |

**Nested**: `people/friend`, `genre/fiction`

---

## 3. Links

| Type | Syntax | Use For |
|------|--------|---------|
| Wikilink | `[[Note Name]]` | Internal (preferred) |
| With alias | `[[Note\|Display]]` | Custom text |
| Markdown | `[text](URL)` | External URLs only |
| Embed | `![[Note]]` | Embed content |

---

## 4. Database Folder Fields

Match field names exactly (case-sensitive):

```yaml
---
tags:
  - jobseeking
Active: false
Application: true
Application_Date: 2024-12-01
Notes: "Text with: special chars"
---
```

---

## 5. Dates

| Context | Format |
|---------|--------|
| Frontmatter | `YYYY-MM-DD` |
| File names | `YYYY-MM-DD` |

---

## 6. Special Characters in Frontmatter

**Quote strings with special characters**:

| Character | Solution |
|-----------|----------|
| `:` colon | `"Value: with colon"` |
| `#` hash | `"Contains #hashtag"` |
| `-` at start | `"- starts with dash"` |
| Multiline | Use `\|` block |

```yaml
Notes: "Rejected 2025-01-02 - no interview"
description: |
  Multiline
  content here
```

---

## 7. Quick Checklist

Before saving any note:

- [ ] Frontmatter at top (starts with `---`)
- [ ] Tags in frontmatter or with `#` in body
- [ ] Internal links use `[[wikilinks]]`
- [ ] Dates as `YYYY-MM-DD`
- [ ] Special chars in values are quoted
- [ ] Field names match database schema

---

## 8. Common Mistakes

| Wrong | Correct |
|-------|---------|
| `#tag` before frontmatter | Frontmatter first |
| `Notes: has: colons` | `Notes: "has: colons"` |
| `[Internal](note.md)` | `[[Internal]]` |
| `2025/01/04` | `2025-01-04` |
| `Application Date:` | `Application_Date:` |

---

## Template: Minimal Note

```yaml
---
tags:
  - category
created: 2025-01-04
---

[[_Relevant MOC]]

## Content

Main content here.
```
