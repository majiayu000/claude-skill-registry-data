---
name: Adding to your knowledgebase
description: How to fetch webpages and convert them to markdown to add to your knowledge base
allowed-tools: Bash, Read, WebFetch, Write
---

# Adding to your knowledge base

## Instructions
1. Convert any webpage to markdown and add it to your knowledge base using the helper script:
```bash
sh scripts/helper.sh URL FILENAME.md
```

The script will:
- Convert the URL to markdown and save to `~/.claude/resources/FILENAME.md`
- Prompt you for a category (e.g., Music, Programming, Documentation)
- Prompt you for a brief description
- Automatically update `~/.claude/resources/INDEX.md` with the new entry

## Example
```bash
sh scripts/helper.sh https://example.com/docs my_doc.md
# Category: Documentation
# Description: API reference for example service
```

The INDEX.md follows llms.txt-style formatting with markdown links and descriptions.
