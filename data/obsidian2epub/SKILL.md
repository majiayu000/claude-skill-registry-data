---
name: obsidian2epub
description: Convert Obsidian vaults to EPUB ebooks. Use when the user wants to create an ebook from Obsidian notes, export a vault as EPUB, or convert markdown notes to an ebook format.
---

# Obsidian2Epub

Convert Obsidian vaults to well-structured EPUB ebooks with full support for wikilinks, attachments, and Mermaid diagrams.

## Quick Start

```bash
scripts/convert.sh /path/to/vault -o output.epub
```

## Instructions

1. Get the vault path from the user
2. Determine output EPUB path
3. Ask about optional settings (title, author, theme, filters)
4. Run the conversion using `scripts/convert.sh`
5. Report any warnings (unresolved links, mermaid failures)

## CLI Reference

```bash
# Basic conversion
scripts/convert.sh /path/to/vault -o book.epub

# With options
scripts/convert.sh /path/to/vault \
  -o book.epub \
  --title "Book Title" \
  --author "Author Name" \
  --moc "Index.md" \
  -d  # dark Flexoki theme

# Interactive TUI
scripts/convert.sh --tui
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output EPUB path (required) |
| `--title` | Book title (default: vault name) |
| `--author` | Author name |
| `--moc` | MOC file for chapter ordering |
| `-d, --dark` | Dark Flexoki theme |
| `--include` | Regex to include files |
| `--exclude` | Regex to exclude files |
| `--tui` | Launch interactive TUI |

## Features

- **Wikilinks**: `[[note]]` becomes internal EPUB links
- **Mermaid**: Rendered to SVG (requires `npm install -g @mermaid-js/mermaid-cli`)
- **Smart Ordering**: HITS algorithm for chapter order
- **Flexoki Themes**: Light (default) and dark

## Examples

Convert with custom title:
```bash
scripts/convert.sh ~/Obsidian/MyVault -o mybook.epub --title "My Knowledge Base"
```

Include only specific folders:
```bash
scripts/convert.sh ~/Obsidian/MyVault -o book.epub --include "^Projects/"
```

Exclude drafts:
```bash
scripts/convert.sh ~/Obsidian/MyVault -o book.epub --exclude "^Drafts/"
```

## Configuration

Set `OBSIDIAN2EPUB_DIR` environment variable to override the default installation path:

```bash
export OBSIDIAN2EPUB_DIR=/path/to/obsidian2epub
```

## Troubleshooting

**Mermaid not rendering**: Install mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`

**Unresolved wikilinks**: Links to notes not in vault are reported as warnings

**Missing attachments**: Ensure files exist and paths are correct in notes
