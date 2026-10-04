---
name: tool-pdf-reader
description: Extract and read PDF files two ways — chunked stdout (read-as-you-go, costs context per page; for triaging a few pages) or full-dump to a markdown file (token-cheap, re-readable later via Read/Grep). Supports info, TOC, page-range extract, keyword search, and full dump. Use when the user says "read this PDF", "extract pages X-Y", "PDF table of contents", or "search this PDF for <term>". NOT for digesting an engineering standard/textbook into the EmptyOS KB (use vault-source-digest).
---

# PDF Reader Skill

Extract and read PDF files. Two modes: **chunked stdout** (read-as-you-go, costs context per page) and **full-dump to a markdown file** (token-cheap, re-readable later via Read/Grep).

## Setup (One-time)

```bash
pip install pymupdf
```

`SKILL_DIR` below = `{home}/.claude/skills/tool-pdf-reader/` on the user's machine. Reference the script with that absolute path.

## Usage

### 1. Get PDF Info

```bash
python "<SKILL_DIR>/pdf_tool.py" info "path/to/file.pdf"
```

Returns: total pages, title, author, file size.

### 2. Extract Text (Page Range, stdout)

```bash
python "<SKILL_DIR>/pdf_tool.py" extract "path/to/file.pdf" --start 1 --end 10
```

- `--start`: Starting page (1-indexed, default: 1)
- `--end`: Ending page (inclusive, default: 10)
- Recommended: Read 10-20 pages at a time
- **Use when:** you only need a few pages, or you're triaging which sections to dump.

### 3. Extract Table of Contents

```bash
python "<SKILL_DIR>/pdf_tool.py" toc "path/to/file.pdf"
```

### 4. Search Text

```bash
python "<SKILL_DIR>/pdf_tool.py" search "path/to/file.pdf" "keyword"
```

Returns pages containing the keyword.

### 5. Dump Full PDF to Markdown File (token-saver)

```bash
python "<SKILL_DIR>/pdf_tool.py" dump "path/to/file.pdf" "path/to/output.md"
```

Writes the entire PDF to a flat markdown file with `## Page N` headers, faithful to the source. Blank pages are noted but not skipped (so page numbers stay aligned).

- **Use when:** you (or future-you in a new session) will want to reference the PDF more than once. Dump once, then `Read` / `Grep` the .md instead of re-parsing the PDF.
- **Use when:** the PDF is long (>30 pages) and you need most of it but not in stdout — saves context vs. iterated `extract` calls.
- Skip when: the PDF is mostly figures/scans (no extractable text), or you only need 1–2 pages.

For a vault PDF, dump beside it under a parallel directory:
```
{vault}/99_Attachments/cdegs/Foo.pdf
{vault}/30_Resources/Electrical-Engineering/cdegs-extracted/Foo.md       # dump output
{vault}/30_Resources/Electrical-Engineering/cdegs-extracted/Foo-digest.md  # your hand-written digest
```

---

## Workflow for Reading a Book

1. **Get info first** to know total pages:
   ```bash
   python pdf_tool.py info "book.pdf"
   ```

2. **Extract TOC** to understand structure:
   ```bash
   python pdf_tool.py toc "book.pdf"
   ```

3. **Read in chunks** (10-20 pages per request):
   ```bash
   python pdf_tool.py extract "book.pdf" --start 1 --end 15
   python pdf_tool.py extract "book.pdf" --start 16 --end 30
   # ... continue as needed
   ```

4. **Search for specific topics**:
   ```bash
   python pdf_tool.py search "book.pdf" "emotion"
   ```

---

## Common PDF Locations

| Type | Path |
|------|------|
| Books | `99_Attachments/books/` |
| Papers | `99_Attachments/papers/` |
| Downloads | `{home}/Downloads/` |

---

## Trigger Phrases

| User Says | Action |
|-----------|--------|
| "读这个 PDF" / "read this PDF" | Get info → TOC → Extract chunks |
| "PDF 有多少页" / "how many pages" | Run `info` command |
| "提取第 X-Y 页" / "extract pages X-Y" | Run `extract --start X --end Y` |
| "搜索 PDF 中的 X" / "search PDF for X" | Run `search` command |
| "save the PDF as md" / "dump to markdown" / "extract whole PDF to file" / "save it programatically" | Run `dump` command, write `.md` next to source under a `*-extracted/` parallel dir |

---

## Notes

- Text extraction quality depends on PDF type (scanned vs. native text)
- For scanned PDFs, consider OCR tools (not included in this skill)
- Large PDFs should always be read in chunks to preserve context window
