---
name: frontrange-cli
description: Expert guidance for using the FrontRange CLI (fr command) to manage YAML front matter in text documents. Use when working with front-mattered files, YAML metadata, blog posts, markdown with front matter, or when the user mentions 'fr' commands. Supports reading/writing front matter keys, JMESPath-based searching, bulk operations via piping, directory recursion, and multiple format output (JSON/YAML/plist/CSV).
---

# FrontRange CLI Expert

Comprehensive guidance for using the **FrontRange CLI (`fr`)** to manage YAML front matter in text documents.

## Core Concepts

### What is Front Matter?

Front matter is YAML metadata at the beginning of a text file, enclosed by `---` delimiters:

```markdown
---
title: My Blog Post
draft: true
tags: ["swift", "tutorial"]
date: 2025-01-15
---

# Blog Post Content

This is the body of the document...
```

### How to Invoke the CLI

**Recommended (installed globally):**
```bash
fr <command>
```

**During development (from FrontRange project directory):**
```bash
swift run fr <command>
```

DO NOT USE `swift run fr` unless developing or testing FrontRange itself.

---

## Quick Start: Essential Commands

### Read a Value
```bash
# Single file
fr get --key title post.md

# All files in directory recursively
fr get --key title posts/ -r
```

### Write a Value
```bash
# Single file
fr set --key draft --value false post.md

# All files recursively
fr set --key published --value true posts/ -r
```

### Search for Files
```bash
# Find all drafts (ALWAYS recursive)
fr search 'draft == `true`' ./posts

# Complex query
fr search 'draft == `false` && contains(tags, `"swift"`)' ./posts
```

### Bulk Operations (Piping)
```bash
# Update all matching files
fr search 'draft == `true`' ./posts | while read -r file; do
  fr set "$file" --key draft --value false
  fr set "$file" --key publishDate --value "$(date +%Y-%m-%d)"
done
```

---

## Critical Non-Obvious Behaviors

### 1. Search is ALWAYS Recursive

Unlike other commands, `search` **always** searches recursively - no `-r` flag needed:

```bash
# Other commands: explicit recursive flag required
fr get --key title posts/         # Only direct children
fr get --key title posts/ -r      # Includes subdirectories ✓

# Search: ALWAYS recursive automatically
fr search 'draft == `true`' posts/ # Searches ALL subdirectories ✓
```

### 2. JMESPath Literal Syntax - THE ONE TRUE WAY

**ALWAYS** use this exact syntax for search queries:

1. **Wrap entire expression in SINGLE QUOTES**
2. **Use BACKTICKS around ALL literals**

```bash
# CORRECT ✓
fr search 'draft == `true`' .
fr search 'status == `"published"`' .
fr search 'count > `100`' .
fr search 'contains(tags, `"swift"`)' .

# WRONG ✗
fr search draft == `true` .           # Missing quotes
fr search "draft == `true`" .         # Wrong quotes (shell interprets backticks)
fr search 'draft == true' .           # Missing backticks around literal
```

**Common JMESPath patterns:**
```bash
# Equality
'draft == `true`'
'status == `"published"`'

# Arrays
'contains(tags, `"tutorial"`)'

# Boolean logic
'draft == `false` && featured == `true`'
'status == `"draft"` || status == `"review"`'

# Comparisons
'views > `1000`'
'rating >= `4.5`'
```

### 3. Directory Processing Modes

**Default:** Most commands only process files in the specified directory (non-recursive).

**Recursive:** Use `--recursive` / `-r` flag to include subdirectories.

**Exception:** `search` is ALWAYS recursive.

```bash
# Process only posts/ directory (direct children)
fr get --key title posts/

# Process posts/ and all subdirectories
fr get --key title posts/ --recursive

# Short form
fr get --key title posts/ -r
```

### 4. Extension Filtering

Default extensions: `md`, `markdown`, `yml`, `yaml`

**Override with `--extensions` / `-e`:**

```bash
# Only markdown files
fr get --key title docs/ -r --extensions md

# Multiple extensions
fr list content/ --extensions txt,md,rst

# All files (empty string)
fr search 'title' . --extensions ""
```

---

## Common Commands Overview

For complete command reference, see [references/commands.md](references/commands.md).

| Command | Purpose | Example |
|---------|---------|---------|
| `get` | Retrieve value | `fr get --key title post.md` |
| `set` | Set/update value | `fr set --key draft --value false post.md` |
| `has` | Check key exists | `fr has --key author post.md` |
| `list` | List all keys | `fr list post.md` |
| `remove` | Delete key | `fr remove --key temp post.md` |
| `rename` | Rename key | `fr rename --old-key tag --new-key tags post.md` |
| `sort-keys` | Alphabetize keys | `fr sort-keys post.md` |
| `lines` | Show line numbers | `fr lines post.md` |
| `dump` | Export front matter | `fr dump post.md --format json` |
| `search` | Query files (JMESPath) | `fr search 'draft == \`true\`' ./posts` |
| `replace` | Replace entire front matter | `fr replace post.md --data '{}' --format json` |

---

## Bulk Operations

The `search` command outputs file paths (one per line), enabling powerful piping:

### Using while loops (Recommended)

Handles spaces, special characters, and large file sets:

```bash
# Publish and date-stamp matching posts
fr search 'draft == `true`' ./posts | while read -r file; do
  fr set "$file" --key published --value true
  fr set "$file" --key date --value "$(date +%Y-%m-%d)"
done
```

### Using xargs (Simple cases only)

Works for small file sets without spaces in paths:

```bash
# Simple bulk update
fr search 'draft == `true`' ./posts | xargs fr set --key draft --value false

# With spaces: use -I flag
fr search 'tags' . | xargs -I {} fr get --key tags "{}"
```

**When to use each:**
- `while read`: Paths with spaces, 100+ files, multi-step operations
- `xargs`: <100 files, no spaces, simple one-liners

For detailed piping patterns, see [references/examples.md](references/examples.md).

---

## Output Formats

Most commands support `--format` / `-f` for output formatting:

```bash
# YAML (default for most commands)
fr get --key tags post.md --format yaml

# JSON
fr get --key tags post.md --format json

# Plain string (no formatting)
fr get --key title post.md --format plainString

# Dump supports additional formats
fr dump post.md --format plist      # Apple PropertyList XML
fr dump post.md --format yaml --include-delimiters
```

---

## Handling Missing Keys

Not all files have all keys. Commands error when keys are missing:

```bash
$ fr get --key tags post.md
Error: Key 'tags' not found in frontmatter.
```

**Strategies:**

1. **Filter with search first:**
   ```bash
   fr search 'tags' . | while read -r file; do
     fr get --key tags "$file"
   done
   ```

2. **Suppress expected errors:**
   ```bash
   fr get --key tags posts/ -r 2>/dev/null
   ```

3. **Check for errors in scripts:**
   ```bash
   if fr has --key tags "$file" 2>/dev/null; then
     fr get --key tags "$file"
   fi
   ```

---

## Common Workflows

### Publishing Workflow

```bash
# Find drafts ready to publish
fr search 'draft == `true` && ready == `true`' ./posts

# Publish them
fr search 'draft == `true` && ready == `true`' ./posts | while read -r file; do
  fr set "$file" --key draft --value false
  fr set "$file" --key published --value true
  fr set "$file" --key publishDate --value "$(date +%Y-%m-%d)"
done
```

### Content Auditing

```bash
# Get all authors
fr get --key author content/ -r --format json

# Count by status
fr search 'status == `"draft"`' posts | wc -l
fr search 'status == `"published"`' posts | wc -l

# List unique tags
fr get --key tags posts/ -r --format json | jq -r '.[]' | sort -u
```

### Batch Updates

```bash
# Add key to all files
fr set --key version --value "2.0" content/ -r

# Rename keys across project
fr rename --old-key category --new-key categories . -r

# Remove deprecated keys
fr search 'oldField' . | xargs fr remove --key oldField
```

For more patterns and recipes, see [references/examples.md](references/examples.md).

---

## Global Options

Available across most commands:

- Path arguments: File(s) and/or directory(ies) to process
- `--recursive` / `-r`: Process subdirectories (default: false, except `search` which is always recursive)
- `--extensions` / `-e`: File extensions to process (default: `md,markdown,yml,yaml`)
- `--format` / `-f`: Output format (`yaml`, `json`, `plainString`)
- `--debug` / `-d`: Enable debug output

---

## Quick Reference: When to Use Each Approach

### Single File Operations
```bash
fr get --key title post.md
fr set --key draft --value false post.md
```

### Directory Operations (Non-Recursive)
```bash
fr get --key title posts/              # Only direct children
fr set --key reviewed --value true posts/
```

### Directory Operations (Recursive)
```bash
fr get --key title posts/ -r           # All subdirectories
fr set --key category --value "blog" content/ -r
```

### Query-Based Operations
```bash
# Search (always recursive) + pipe to other commands
fr search 'draft == `true`' . | xargs fr set --key draft --value false

# With while loop for safety
fr search 'ready == `true`' . | while read -r file; do
  fr set "$file" --key published --value true
done
```

---

## Additional Documentation

- **[references/commands.md](references/commands.md)** - Complete command reference with all options and flags
- **[references/examples.md](references/examples.md)** - Detailed patterns, recipes, and workflows
- **[references/troubleshooting.md](references/troubleshooting.md)** - Troubleshooting guide and advanced usage

---

## Summary

**Key Principles:**
1. **Search is always recursive** - no `-r` flag needed
2. **JMESPath requires backticks** - `'draft == \`true\`'` not `'draft == true'`
3. **Most commands need `-r` for subdirectories** - except search
4. **Pipe search results for bulk operations** - `fr search ... | xargs fr set ...`

The FrontRange CLI provides a complete toolkit for managing YAML front matter with powerful directory processing, flexible querying, and seamless bulk operations.
