---
name: content-analysis
description: Analyze any text content including meeting notes, emails, book excerpts, or generic text files. Use when the user wants to analyze content that doesn't fit YouTube, article, or paper categories, or mentions notes, documents, or generic analysis.
---

# Generic Content Analysis

Analyze any text content and generate a structured report.

## When to Use

Activate this skill when the user:
- Wants to analyze content that isn't a YouTube transcript, web article, or arXiv paper
- Mentions "notes", "meeting notes", "email", "document", "book", "chapter"
- Has a text file they want analyzed but doesn't specify a category
- Asks for generic analysis of some content

## Instructions

1. **Get the file path** - Ask the user for the file path if not provided
2. **Read the content file** at the path provided
3. If file not found:
   - Inform user: "File not found at [path]"
   - Suggest checking the path
   - Stop here
4. **Ask the user** for:
   - A title for this content
   - Category: video, article, paper, or other
5. **Read the appropriate analysis prompt**:
   - If video: `prompts/yt.md`
   - If article: `prompts/article.md`
   - If paper: `prompts/paper.md`
   - If other: `prompts/default.md`
6. **Generate analysis** following the prompt structure exactly
7. **Save the report** to `reports/{category}/YYYY-MM-DD_sanitized-title.md` where:
   - {category} is youtube, articles, papers, or other
   - YYYY-MM-DD is today's date
   - sanitized-title is the title in lowercase, spaces replaced with hyphens, special chars removed
8. **Update the activity log** at `logs/YYYY-MM-DD.md`:
   - Create file if it doesn't exist
   - Add entry under appropriate section based on category
   - Format: `- [Title](../reports/{category}/filename.md) - HH:MM`
9. **Confirm to user** what was saved and where

## Report Format

Include this header in the report:
```markdown
# [Title]

**Source**: [File path]
**Date**: YYYY-MM-DD
**Type**: [Category]

---

[Analysis content following appropriate prompt structure]

---

## My Notes

[Empty space for user notes]
```

## Error Handling

- If file is empty: Inform user and ask if they want to proceed
- If prompt file missing: Use prompts/default.md or basic structure

## Related

- Slash command equivalent: `/analyze <filepath>`
- Prompt files: `prompts/default.md` (or category-specific)
- Output location: `reports/{category}/`
