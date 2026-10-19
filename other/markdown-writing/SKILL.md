---
name: markdown-writing
description: >
  Author clean, semantically structured, and compliant Markdown documents
  following CommonMark and GitHub Flavored Markdown (GFM) specifications.
  Use when writing technical documentation, formatting tables, code blocks,
  relative links, task lists, and alerts, or linting with markdownlint.
compatibility: >
  Agent Skills-compatible coding agents reading or authoring Markdown files.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "markdown, gfm, commonmark, documentation, markdownlint, writing"
  topics: "documentation, devtools"
---

# Professional Markdown Authoring

Markdown is the standard format for developer documentation, READMEs, and technical specifications. Producing professional Markdown requires strict adherence to CommonMark and GitHub Flavored Markdown (GFM), consistent heading hierarchy, valid relative links, and compliance with `markdownlint` rules.

## Core Rules

1. **Maintain strict heading hierarchy**: Never skip heading levels (e.g. going directly from `# H1` to `### H3` without an intervening `## H2`). Exactly one `# H1` per document.
2. **Always specify code block language tags**: Fenced code blocks must always declare an explicit language identifier (e.g. ```` ```python ````, ```` ```bash ````, ```` ```json ````).
3. **Surround block elements with blank lines**: Blank lines must precede and follow headings, lists, tables, and fenced code blocks.
4. **Use relative links for local files**: Link to repository files using relative paths (`docs/architecture.md`) rather than absolute filesystem paths or external URLs.
5. **Format tables cleanly with alignment markers**: Keep markdown table source code readable with aligned pipes and clear delimiter rows.
6. **Prefer reference-style links for readability**: When a paragraph contains multiple long URLs, use reference-style links at the bottom of the section.

---

## 1. Structural Standards & Hierarchy

```markdown
# Document Title (Single H1)

A concise introductory paragraph explaining the purpose of the document.

## 1. Major Section (H2)

Content introducing the subsection.

### 1.1 Subsection (H3)

Detailed technical instructions or descriptions.
```

---

## 2. GitHub Flavored Markdown (GFM) Features

### GFM Alerts
Use GitHub alert callouts to emphasize critical guidance:

```markdown
> [!NOTE]
> Highlights useful information that users should take into account.

> [!TIP]
> Helpful advice for doing things more easily or with higher performance.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention to prevent failures.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
```

### Clean Tables with Alignment
```markdown
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/users` | List active user accounts | Yes |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT | No |
| `DELETE` | `/api/v1/users/{id}` | Permanently delete account | Yes |
```
- `:---` left aligns (default for text).
- `:---:` centers (useful for icons, badges, status flags).
- `---:` right aligns (recommended for numbers and currency).

### Task Lists
```markdown
- [x] Initial specification drafted
- [x] Unit test suite implemented
- [ ] Security audit completed
```

---

## 3. Link Hygiene and Media Embedding

- **Relative Links**: Always check that target files exist: `[Installation Guide](docs/install.md)`.
- **Anchors**: GitHub auto-generates heading anchors by lowercasing and replacing spaces with hyphens: `## Quick Start` -> `[Jump to Quick Start](#quick-start)`.
- **Images**: Always supply descriptive alternative text for accessibility:
  ```markdown
  ![Database schema entity relationship diagram](assets/erd-diagram.png)
  ```

---

## 4. Common Mistakes and Markdownlint Violations

| Violation Code | Description | Fix |
| :--- | :--- | :--- |
| `MD001` | Heading levels should only increment by one level at a time | Change `###` directly under `#` to `##` |
| `MD003` | Inconsistent heading styles (mixing ATX `#` and Setext `===`) | Standardize exclusively on ATX (`#`) headings |
| `MD009` | Trailing spaces at the end of lines | Trim trailing whitespace |
| `MD031` | Fenced code blocks should be surrounded by blank lines | Add a newline before and after ```` ``` ```` |
| `MD034` | Bare URLs without angle brackets or link text | Wrap URL in `<https://...>` or `[Label](url)` |
| `MD040` | Fenced code blocks should have a language specified | Add `text`, `bash`, `python`, etc. after opening backticks |

---

## 5. Verification Checklist

- [ ] Single `# H1` at top of document.
- [ ] No skipped heading levels (MD001 compliant).
- [ ] All code fences specify a language tag (MD040 compliant).
- [ ] All local markdown and image links point to valid, existing files.
- [ ] Passed `markdownlint <document.md>` with 0 errors.
