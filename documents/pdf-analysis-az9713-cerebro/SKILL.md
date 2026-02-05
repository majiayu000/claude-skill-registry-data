---
name: pdf-analysis
description: Analyze PDF documents including reports, whitepapers, ebooks, and manuals. Use when the user mentions PDF, document, whitepaper, ebook, report file, or wants to analyze a .pdf file.
---

# PDF Document Analysis

Analyze PDF documents to generate structured reports with summaries, key points, data extraction, and insights.

## When to Use

Activate this skill when the user:
- Mentions "PDF", "document", "whitepaper", "ebook", "report"
- Provides a file path to a .pdf file
- Asks to summarize or analyze a PDF document
- Wants to extract insights from a document file
- References a downloaded report or paper

## Instructions

1. **Get the file path** - Ask the user for the PDF file path if not provided
2. **Verify the file exists** and is readable
3. **Read the PDF content** using the Read tool
   - The Read tool can extract text from PDF files
4. If reading fails:
   - If PDF appears to be scanned/image-based: Inform user OCR may be needed
   - Suggest alternative approaches if text extraction fails
5. **Read the analysis prompt** from `prompts/pdf.md`
6. **Extract document metadata** from content:
   - Title (from content or derive from filename)
   - Author if mentioned
   - Date if mentioned
7. **Generate analysis** following the prompt structure exactly
8. **Create output directory** `reports/pdfs/` if needed
9. **Save the report** to `reports/pdfs/YYYY-MM-DD_sanitized-title.md` where:
   - YYYY-MM-DD is today's date
   - sanitized-title is the title in lowercase, spaces replaced with hyphens, special chars removed, max 50 chars
10. **Update the activity log** at `logs/YYYY-MM-DD.md`:
    - Create file if it doesn't exist with standard sections
    - Add entry under "## PDFs Reviewed" section (create if needed)
    - Format: `- [Title](../reports/pdfs/filename.md) - HH:MM`
11. **Confirm to user** what was saved and where

## Report Format

Include this header in the report:
```markdown
# [Document Title]

**Source**: [file path]
**Date**: YYYY-MM-DD
**Type**: PDF Document

---

[Analysis content following prompts/pdf.md structure]

---

## My Notes

[Empty space for user notes]
```

## Error Handling

- If file path doesn't exist: Ask user for correct path
- If file is not a PDF: Suggest using /analyze for other file types
- If text extraction fails: Suggest OCR or manual copy
- If prompts/pdf.md missing: Use prompts/default.md

## Related

- Slash command equivalent: `/pdf <filepath>`
- Prompt file: `prompts/pdf.md`
- Output location: `reports/pdfs/`
