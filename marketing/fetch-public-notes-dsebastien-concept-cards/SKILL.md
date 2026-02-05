---
name: fetch-public-notes
description: Extract content from the public notes website at notes.dsebastien.net. Use when fetching MoCs, notes, or any content from the Obsidian Publish site.
allowed-tools: WebFetch, Bash, Read, Grep, Glob
---

# Fetching Content from Public Notes

This skill provides instructions for extracting information from the public notes website hosted at `https://notes.dsebastien.net/`.

## Important: The Site Uses Dynamic Loading

The notes website is an **Obsidian Publish** site. Content is loaded dynamically via JavaScript, which means:

- **Direct WebFetch on page URLs will NOT work** - You'll only get HTML boilerplate and JavaScript loaders
- **You must use the Obsidian Publish API** to get the raw markdown content

## Step-by-Step Process

### Step 1: Identify the Note Path

Determine the full path to the note you want to fetch. Notes are organized in folders like:

| Folder | Description |
|--------|-------------|
| `30 Areas/32 Literature notes/32.02 Content/` | Literature/reference notes |
| `30 Areas/32 Literature notes/32.04 Expressions/` | Expressions and sayings |
| `30 Areas/32 Literature notes/32.05 Quotes/` | Quotes |
| `30 Areas/33 Permanent notes/33.02 Content/` | Permanent/evergreen notes |
| `30 Areas/34 Maps/34.01 MoCs/` | Maps of Content |

### Step 2: Construct the API URL

Use this URL pattern to fetch raw markdown:

```
https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/[URL-encoded-path].md
```

**URL Encoding Rules:**
- Spaces become `%20`
- Parentheses: `(` becomes `%28`, `)` becomes `%29`
- The path starts from `30 Areas/...`

### Step 3: Fetch the Content

Use WebFetch with the constructed API URL:

```
WebFetch:
  url: https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/30%20Areas/34%20Maps/34.01%20MoCs/Positivity%20(MoC).md
  prompt: List all the note links/concepts mentioned. Extract the note names.
```

## Examples

### Fetching a MoC (Map of Content)

**Goal:** Get content from "Positivity (MoC)"

**Public URL (won't work for fetching):**
```
https://notes.dsebastien.net/30+Areas/34+Maps/34.01+MoCs/Positivity+(MoC)
```

**API URL (use this):**
```
https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/30%20Areas/34%20Maps/34.01%20MoCs/Positivity%20(MoC).md
```

### Fetching a Permanent Note

**Goal:** Get content from "Positive psychology"

**API URL:**
```
https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/30%20Areas/33%20Permanent%20notes/33.02%20Content/Positive%20psychology.md
```

### Fetching a Literature Note

**Goal:** Get content from "Atomic Thinking"

**API URL:**
```
https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/30%20Areas/32%20Literature%20notes/32.02%20Content/Atomic%20Thinking.md
```

## Alternative: Read from Local Repository

If you have access to the local notes repository, you can read files directly:

**Repository Location:** `/home/dsebastien/notesSeb/`

```bash
# Find a note by name
find /home/dsebastien/notesSeb/30\ Areas -type f -name "*Note Name*" 2>/dev/null | grep -v ".smart-env"

# Read the note directly
Read: /home/dsebastien/notesSeb/30 Areas/33 Permanent notes/33.02 Content/Note Name.md
```

## Constructing Related Notes URLs

When adding `relatedNotes` to concept cards, use the public website URL format:

- Base URL: `https://notes.dsebastien.net/`
- Spaces become `+`
- Remove the `.md` extension
- Path starts from `30+Areas/...`

**Example:**
- File: `/home/dsebastien/notesSeb/30 Areas/33 Permanent notes/33.02 Content/Positive psychology.md`
- URL: `https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Positive+psychology`

## Common Pitfalls

1. **Don't use the public URL for WebFetch** - It returns JavaScript loaders, not content
2. **Always URL-encode the path** - Spaces must be `%20` in the API URL
3. **Include the `.md` extension** in the API URL
4. **The site ID is fixed**: `91ab140857992a6480c9352ca75acb70`

## Quick Reference

| Task | Method |
|------|--------|
| Fetch note content online | WebFetch with `publish-01.obsidian.md` API URL |
| Read note locally | Read tool with `/home/dsebastien/notesSeb/` path |
| Find note location | `find` command in local repository |
| Construct public URL | Replace spaces with `+`, remove `.md` |
