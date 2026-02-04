---
name: vault-context
description: Understand vault organization, weekly writing pipeline (Mon-Sun stages), file conventions, and Make commands. Use when working with vault files, daily notes, blog posts, projects, or referencing vault structure and workflows.
---

# Vault Context

This skill provides comprehensive awareness of the vault's structure, workflows, and conventions.

## Directory Structure

```
vault/
├── blog/          # Published essays and blog posts (with YAML frontmatter)
├── daily/         # Daily journal (YYYY/MM/YYYY-MM-DD.md format)
├── letters/       # Formal correspondence
├── projects/      # Active work (civil-war-history, game-theory, etc.)
├── reference/     # Evergreen guides and frameworks
├── archive/       # Completed work (mirrors main structure)
├── templates/     # Scaffolding for new content
└── scripts/       # Bash automation
```

## House Rulebook Principles

1. **Everything starts in `/vault` as `.md`**
2. **Filenames are utilitarian; titles live inside files**
3. **One file per idea**
4. **When in doubt, append — don't delete**
5. **Source of truth = Markdown. Exports (PDF, HTML, blog) are derivatives**

## Weekly Writing Pipeline (Mon-Sun)

### Monday: Capture
- Dump fragments, quotes, observations (20-30 minutes)
- Use daily notes for raw capture

### Tuesday: Cluster
- Group Monday's notes into 3 thematic clusters
- Look for patterns across fragments

### Wednesday: Outline
- One-sentence thesis
- Three proof points
- Opener idea
- Closer idea

### Thursday: Draft
- Write rough draft using outline
- Mark gaps with `[TK: ...]` placeholders

### Friday: Revision
- Top-down revision:
  1. Structure (big picture)
  2. Style (sentence-level)
  3. 3-column method (problem/diagnosis/fix)

### Saturday: Outside Read
- Get feedback: where bored, unclear, unnecessary

### Sunday: Publish
- Final pass, write teaser, ship it

## Pipeline Stages Reference

| Stage   | Description              | Status Indicator |
|---------|--------------------------|------------------|
| Capture | Raw notes, fragments     | In daily notes   |
| Cluster | Group notes into themes  | Themed sections  |
| Outline | Thesis + structure       | Has outline      |
| Draft   | Fast draft               | Has `[TK:]` tags |
| Revise  | Structural + style fixes | Clean prose      |
| Review  | External feedback        | Awaiting input   |
| Publish | Final edits + ship       | In blog/         |

## Make Commands Reference

### Content Creation
- `make daily` - Create today's daily note with template
- `make new` - Interactive file creation wizard

### Export & Publishing
- `make export LETTER=path/to/letter.md` - Export letter to PDF
- `make export-blog POST=blog/post.md` - Export blog post to PDF

### Search & Organization
- `make search TERM=keyword` - Full vault search
- `make wordcount FILE=path` - Word/line count for file
- `make check-links` - Find broken internal links
- `make recent` - Show last 10 modified files with previews
- `make todo` - Find all TODO/FIXME/NOTE comments
- `make tags` - Extract and index all #tags
- `make graph` - Generate Mermaid link visualization
- `make update-index` - Auto-update index.md files

### Quality & Maintenance
- `make lint` - Check markdown formatting issues
- `make lint-fix` - Auto-fix common formatting issues
- `make stats` - Vault statistics dashboard
- `make track-words` - Track word count history
- `make backup` - Create timestamped backup archive
- `make clean` - Remove all generated PDFs

### Git Integration
- `make commit MSG="message"` - Quick commit

## File Conventions

### Blog Posts
YAML frontmatter at top:
```yaml
---
slug: post-url-slug
title: "Post Title"
date: Month Day, Year
excerpt: "Brief description for previews"
categories: ["Category1", "Category2"]
---
```

### Daily Notes
- Date as title: `# 2025-10-04`
- Structure:
  ```markdown
  ## top 3
  -
  ## log
  -
  ## gratitude
  -
  ```

### Projects
- Descriptive title
- Status section showing pipeline stage
- Can be multi-file (subdirectories OK)

### Letters
- Include date at top
- Use templates/letter.md as starting point

## Internal Linking

- **Relative paths**: `[text](../reference/guide.md)`
- **Wiki-style**: `[[filename]]` or `[[filename|display text]]`
- Run `make check-links` regularly to maintain link hygiene

## Workflow Best Practices

1. **Daily practice**: Start each day with `make daily`
2. **Weekly review**: Check `make stats` for writing progress
3. **Monthly backup**: Run `make backup` to create archive
4. **Link hygiene**: Run `make check-links` before major commits
5. **Clean exports**: Use `make clean` to remove old PDFs before backing up

## TK Placeholders

Use `[TK: description]` to mark gaps during drafting:
- `[TK: find citation]`
- `[TK: add example]`
- `[TK: verify this claim]`

Search for TK tags before publishing: `make search TERM="[TK:"`

## Template System

Templates in `templates/` use `{{PLACEHOLDER}}` syntax:
- `{{TITLE}}` - Document title
- `{{DATE}}` - Current date
- `{{SLUG}}` - URL-friendly slug

The `make new` command automatically substitutes variables.

## Archiving Process

When a project is complete:
1. Move to `archive/` preserving directory structure
2. Update any index files
3. Run `make check-links` to ensure no broken references
4. Commit with clear message about archival

## Instructions for Claude

When working with vault files:

1. **Always respect the house rulebook** - markdown is source of truth, filenames are utilitarian
2. **Track pipeline stages** - note where each piece is in the Mon-Sun flow
3. **Suggest appropriate Make commands** - don't reinvent tools that already exist
4. **Preserve YAML frontmatter** - critical for blog posts
5. **Maintain link hygiene** - check links when suggesting file moves
6. **Use templates** - reference templates/ for new file creation
7. **Mark research gaps with TK** - help user track what needs investigation

For more details, see:
- [make-commands.md](make-commands.md) - Complete command reference
