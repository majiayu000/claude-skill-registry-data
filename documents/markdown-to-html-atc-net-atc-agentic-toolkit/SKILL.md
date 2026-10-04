---
name: markdown-to-html
description: 'Convert Markdown files to HTML similar to `marked.js`, `pandoc`, `gomarkdown/markdown`, or similar tools; or writing custom script to convert markdown to html and/or working on web template systems like `jekyll/jekyll`, `gohugoio/hugo`, or similar web templating systems that utilize markdown documents, converting them to html. Use when asked to "convert markdown to html", "transform md to html", "render markdown", "generate html from markdown", or when working with .md files and/or web a templating system that converts markdown to HTML output. Supports CLI and Node.js workflows with GFM, CommonMark, and standard Markdown flavors.'
---

# Markdown to HTML Conversion

Expert skill for converting Markdown documents to HTML using the marked.js library, or writing data conversion scripts; in this case scripts similar to [markedJS/marked](https://github.com/markedjs/marked) repository. For custom scripts knowledge is not confined to `marked.js`, but data conversion methods are utilized from tools like [pandoc](https://github.com/jgm/pandoc) and [gomarkdown/markdown](https://github.com/gomarkdown/markdown) for data conversion; [jekyll/jekyll](https://github.com/jekyll/jekyll) and [gohugoio/hugo](https://github.com/gohugoio/hugo) for templating systems.

The conversion script or tool should handle single files, batch conversions, and advanced configurations.

## Core Workflow

1. **Identify the conversion need** - Single file, batch, or template system
2. **Select the right tool** - See Tool Selection Guide below
3. **Load the appropriate reference** - Read the tool-specific reference file
4. **Apply conversion patterns** - Use the conversion examples from references
5. **Handle security** - Sanitize output when processing untrusted input

## Tool Selection Guide

Choose the tool based on the user's environment and requirements:

| Tool | Best For | Language | Install |
|------|----------|----------|---------|
| [marked](references/marked.md) | Node.js projects, browser usage, CLI quick conversions | JavaScript | `npm install -g marked` |
| [pandoc](references/pandoc.md) | Multi-format conversion (MD, HTML, PDF, DOCX, LaTeX) | Haskell | [pandoc.org/installing](https://pandoc.org/installing.html) |
| [gomarkdown](references/gomarkdown.md) | Go projects, custom parsers, AST manipulation | Go | `go get github.com/gomarkdown/markdown` |
| [jekyll](references/jekyll.md) | Blog-aware static sites, GitHub Pages | Ruby | `gem install jekyll bundler` |
| [hugo](references/hugo.md) | Fast static sites, complex content management | Go | [gohugo.io/installation](https://gohugo.io/installation/) |

### Decision Logic

- **Just need quick MD-to-HTML?** Use `marked` (CLI) or `pandoc`
- **Node.js project?** Use `marked`
- **Need PDF/DOCX/LaTeX output?** Use `pandoc`
- **Go project?** Use `gomarkdown`
- **Building a blog/static site?** Use `jekyll` (Ruby) or `hugo` (Go)
- **Need GitHub Pages compatibility?** Use `jekyll`
- **Need fast build times?** Use `hugo`

## Conversion Reference Files

### Markdown Element Conversion Examples

Load these when working on conversion logic to understand how specific Markdown elements map to HTML.

| Reference | When to Load |
|-----------|-------------|
| [basic-markdown-to-html.md](references/basic-markdown-to-html.md) | Headings, paragraphs, inline formatting, links, images, lists, blockquotes, footnotes |
| [code-blocks-to-html.md](references/code-blocks-to-html.md) | Fenced code blocks, syntax highlighting, showing backticks, diagrams |
| [collapsed-sections-to-html.md](references/collapsed-sections-to-html.md) | `<details>`/`<summary>` elements, open-by-default sections |
| [tables-to-html.md](references/tables-to-html.md) | Tables with alignment, formatted content in cells, escaped characters |
| [writing-mathematical-expressions-to-html.md](references/writing-mathematical-expressions-to-html.md) | Inline math (`$...$`), block math (`$$...$$`), MathML output |

### Markdown Syntax References

Load these when users need help writing Markdown (not converting it).

| Reference | When to Load |
|-----------|-------------|
| [basic-markdown.md](references/basic-markdown.md) | Full Markdown writing syntax reference |
| [code-blocks.md](references/code-blocks.md) | Code block syntax and language identifiers |
| [collapsed-sections.md](references/collapsed-sections.md) | Collapsible section syntax |
| [tables.md](references/tables.md) | Table formatting syntax |
| [writing-mathematical-expressions.md](references/writing-mathematical-expressions.md) | LaTeX math expression syntax |

### Tool-Specific References

Load the appropriate reference based on the tool selected.

| Reference | When to Load |
|-----------|-------------|
| [marked.md](references/marked.md) | Using marked.js: CLI usage, Node.js API, config files, batch conversion, security (DOMPurify) |
| [pandoc.md](references/pandoc.md) | Using pandoc: multi-format conversion, extensions, templates, Lua filters, batch scripts |
| [gomarkdown.md](references/gomarkdown.md) | Using gomarkdown: Go API, parser/renderer config, AST manipulation, security (Bluemonday) |
| [jekyll.md](references/jekyll.md) | Using Jekyll: site creation, Liquid templates, Kramdown config, plugins, front matter |
| [hugo.md](references/hugo.md) | Using Hugo: site creation, Go templates, Goldmark config, shortcodes, Hugo Pipes |
