---
name: zotero-paper-reader
description: Read and analyze academic papers from Zotero library. Use when the user requests to read, access, or analyze a paper by title, author, or topic from their Zotero library. Automatically searches Zotero, converts PDFs to markdown, saves to Notes/PaperInMarkdown, and provides analysis.
---

# Zotero Paper Reader

## Overview

Read and analyze academic papers directly from the Zotero library. This skill handles the complete workflow from searching Zotero to converting PDFs to readable markdown format.

## When to Use

Use this skill when the user requests to:
- "Read this paper from Zotero"
- "Find and read [paper title]"
- "Access [author name] paper"
- "Get the paper about [topic]"
- "Convert [paper] from Zotero to markdown"

## Workflow

### Step 1: Search Zotero Library

Use the Zotero MCP tools to search for the paper:

```python
# Search by title, author, or keywords
mcp__zotero__zotero_search_items(query="paper title or author", limit=5)
```

Present the search results to the user if multiple papers are found. Get the `item_key` from the selected paper.

### Step 2: Get PDF Attachment

Retrieve the PDF attachment information:

```python
# Get child items (attachments) for the paper
mcp__zotero__zotero_get_item_children(item_key="ITEM_KEY")
```

Look for the attachment with `type: application/pdf` and note its `Key` (attachment key) and `Filename`.

### Step 3: Get PDF File (Local or Download)

Use the bundled script to get the PDF - it automatically tries local storage first, then downloads if needed:

```bash
uv run python .claude/skills/zotero-paper-reader/scripts/get_zotero_pdf.py ATTACHMENT_KEY
```

The script workflow:
1. First searches local Zotero storage (`~/Zotero/storage/ATTACHMENT_KEY/`)
2. If found locally, returns that path
3. If not found locally, downloads from Zotero web library using API
4. Retrieves original filename from Zotero metadata and downloads to `/tmp/[original_filename]`

**Security note:** The Zotero API key and library configuration are read directly from `Notes/.env` by the Python script and never exposed to the LLM. Required environment variables: `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_TYPE`, `ZOTERO_LIBRARY_ID`.

### Step 4: Convert to Markdown

Use the `mistral-pdf-to-markdown` skill to convert the PDF:

```bash
uv run python .claude/skills/mistral-pdf-to-markdown/scripts/convert_pdf_to_markdown.py \
  "PATH_TO_PDF" \
  "Notes/PaperInMarkdown/CLEAN_FILENAME.md"
```

**Filename convention:** Create a clean filename from the paper metadata:
- Format: `Author_Year_Title.md`
- Example: `Du_et_al_2023_Are_Intermediary_Constraints_Priced.md`
- Replace spaces with underscores, remove special characters

### Step 5: Read and Analyze

Read the converted markdown file:

```python
# For large papers, read in sections
Read(file_path="Notes/PaperInMarkdown/FILENAME.md", offset=1, limit=500)
```

Since academic papers are often large (>25k tokens), read strategically:
- Start with abstract and introduction (first 300-500 lines)
- Use Grep to search for specific sections if needed
- Read specific sections based on user interest

Provide the user with:
1. Paper metadata (title, authors, publication year)
2. Brief summary of the abstract
3. Main findings or sections of interest
4. Offer to read specific sections or search for particular content

## Example Usage

**User request:** "Read the paper 'Are Intermediary Constraints Priced' from my Zotero library"

**Workflow:**
1. Search: `mcp__zotero__zotero_search_items(query="Are Intermediary Constraints Priced")`
2. Get attachment: `mcp__zotero__zotero_get_item_children(item_key="KPRQ2DLZ")`
3. Get PDF: `uv run python .claude/skills/zotero-paper-reader/scripts/get_zotero_pdf.py 2HSELEHX`
   - Returns local path if available, or downloads and returns temp path
4. Convert: `uv run python .claude/skills/mistral-pdf-to-markdown/scripts/convert_pdf_to_markdown.py [PDF_PATH] Notes/PaperInMarkdown/Du_et_al_2023_Are_Intermediary_Constraints_Priced.md`
5. Read: `Read(file_path="Notes/PaperInMarkdown/Du_et_al_2023_Are_Intermediary_Constraints_Priced.md", limit=500)`
6. Summarize and offer to dive deeper into specific sections

## Notes

- The skill works with both local and web Zotero libraries
- For web libraries, requires `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_TYPE`, and `ZOTERO_LIBRARY_ID` in `Notes/.env`
- For local libraries, Zotero local API must be enabled in Zotero preferences
- Requires Mistral API key in `Notes/.env` for PDF conversion
- Converted markdown files include extracted images in `images/` subfolder
- Large papers (>40k tokens) should be read in sections to avoid context limits

## Resources

### scripts/

- `get_zotero_pdf.py` - Unified script that tries local storage first, then downloads from web API if needed
