---
name: unique-cli-file-management
description: >-
  Manage files and folders on the Unique AI Platform using the unique-cli
  command-line tool. Use when the user asks to upload, download, delete,
  rename, list, find, restore versions, list versions, look for, or organize files and folders on Unique,
  or to read / view / quote the text contents of a known file (optionally by
  page or page range, e.g. "what's on page 5?", "read pages 10-12"),
  or when working with scope IDs (scope_*) or content IDs (cont_*).
  IMPORTANT: When a user says they are "looking for a file" or wants to
  "find a file", they typically mean locating it within the Unique AI
  Platform knowledge base — not on the local filesystem. Use this skill
  to browse and list folders/files on Unique to help them find it.
  This is also the preferred approach for locating Excel (.xlsx/.xls),
  CSV (.csv), and image files, as these file types are not full-text
  indexed and cannot be found via vector/full-text search.
---

# Unique CLI -- File & Folder Management

`unique-cli` is a Linux-like file explorer for the Unique AI Platform knowledge base.
It is installed via `pip install unique-sdk` and requires these environment variables:

```bash
UNIQUE_USER_ID    # User ID (required)
UNIQUE_COMPANY_ID # Company ID (required)
UNIQUE_API_KEY    # API key — optional on localhost / secured cluster
UNIQUE_APP_ID     # App ID — optional on localhost / secured cluster
```

## One-Shot Commands

Run commands directly from the shell without entering the interactive mode:

```bash
# List root folders
unique-cli ls

# List a specific folder
unique-cli ls /Reports/Q1

# List by scope ID
unique-cli ls scope_abc123

# Create a folder
unique-cli mkdir Q2

# Delete a folder (use -r for non-empty)
unique-cli rmdir /Reports/Q2
unique-cli rmdir scope_abc123 -r

# Rename a folder
unique-cli mvdir Q1 "Q1-2025"

# Upload a file with versioning enabled (to current scope -- cd first or specify destination)
unique-cli upload ./report.pdf
unique-cli upload ./report.pdf /Reports/Q1/
unique-cli upload ./data.csv scope_abc123

# List and restore file versions
unique-cli versions /Reports/Q1/report.pdf
unique-cli versions cont_abc123 --take 10
unique-cli restore-version cver_abc123

# Download a file
unique-cli download report.pdf ./local/
unique-cli download cont_abc123 ~/Desktop/

# Read a file's extracted text by content ID (whole file)
unique-cli read cont_abc123

# Read a single page or a page range
unique-cli read cont_abc123 --page 12
unique-cli read cont_abc123 --from-page 5 --to-page 9

# Declare page citations after reading a file (--read-method is mandatory)
unique-cli cite report.pdf --pages 3,5,7 --read-method text
unique-cli cite cont_abc123 --pages 1-4 --read-method vision
# Non-paginated files (Excel, CSV, txt): omit --pages to cite the whole file
unique-cli cite data.xlsx --read-method text

# Delete a file
unique-cli rm report.pdf
unique-cli rm cont_abc123

# Rename a file
unique-cli mv report.pdf "Annual Report 2025.pdf"
```

## Path & ID Formats

| Format | Example | Resolves to |
|--------|---------|-------------|
| Relative name | `Reports` | Child of current directory |
| Absolute path | `/Company/Reports/Q1` | From root |
| Scope ID | `scope_abc123` | Folder directly by ID |
| `..` | `..` | Parent directory |
| `/` | `/` | Root |
| Content ID | `cont_abc123` | File directly by ID |
| File path | `/Reports/Q1/report.pdf` | File in a folder |

## Upload Destination Resolution

The `upload` command always enables immutable content versioning. It does not expose an unversioned upload mode. Its destination works like Linux `cp`:

| Destination | Behavior |
|-------------|----------|
| *(omitted)* or `.` | Current folder, keep filename |
| `newname.pdf` | Current folder, rename |
| `subfolder/` | Into subfolder, keep filename |
| `/abs/path/` | Into absolute path folder |
| `scope_abc123` | Into that scope ID |
| `sub/new.pdf` | Into sub, renamed |

## Common Workflows

### Upload multiple files to a folder

```bash
for f in ./documents/*.pdf; do
  unique-cli upload "$f" /Reports/2025/
done
```

### List and download all files from a folder

```bash
# First list to see what's there
unique-cli ls /Reports/Q1

# Download specific files
unique-cli download "annual.pdf" ./downloads/
unique-cli download cont_abc123 ./downloads/
```

### Restore a previous file version

```bash
# List versions for a file path, file name in the current folder, or content ID.
unique-cli versions /Reports/Q1/annual.pdf
unique-cli versions "annual.pdf"
unique-cli versions cont_abc123 --take 20

# Restore using the VERSION_ID shown by `versions`.
unique-cli restore-version cver_abc123
```

### Create folder hierarchy and upload

```bash
unique-cli mkdir "2025/Q1/Financials"
unique-cli upload ./budget.xlsx /2025/Q1/Financials/
```

## Reading File Contents (by page range)

Use `read` to retrieve the **extracted text** of a single, known file — for
example to answer "what does page 5 say?", to quote an exact passage, or to
read a long document a few pages at a time. This differs from `search`:
`search` ranks chunks across many files by relevance; `read` returns the text
of one file in document order.

`read` takes a **content ID** (`cont_...`), not a file name. Get the ID first
from `ls` or `search`, then pass it to `read`.

```bash
# Whole file
unique-cli read cont_abc123

# A single page
unique-cli read cont_abc123 --page 12

# A page range (inclusive)
unique-cli read cont_abc123 --from-page 5 --to-page 9

# Cap the output size (protects your context window on huge files)
unique-cli read cont_abc123 --to-page 3 --max-chars 8000
```

| Option | Description |
|--------|-------------|
| `--page` / `-p N` | Read only page N (shorthand for `--from-page N --to-page N`) |
| `--from-page N` | First page to include (inclusive) |
| `--to-page N` | Last page to include (inclusive) |
| `--max-chars N` | Truncate the printed text to N characters |

Each chunk is prefixed with its source page(s) as `[p.N]` or `[p.N-M]`, so you
can attribute text to pages.

### How page filtering behaves (important)

- **Page numbers come from ingestion.** Each chunk carries a `startPage` and
  `endPage`; the page filter is applied to those values. Nothing in the
  ingestion pipeline needs to change.
- **Ranges overlap, they don't slice.** A chunk that spans pages 2-4 is
  returned for `--page 3` (or any range touching 2-4). The returned text is the
  whole chunk, so it may include a little from neighbouring pages. Treat the
  result as "the chunks covering these pages", not a pixel-perfect page cut.
- **Some files have no page numbers.** Plain text, markdown, and similar
  content has no page numbers; those chunks are returned only when you read
  **without** a page range. A page-filtered read of such a file returns nothing.
- **Empty / not indexed?** If `read` reports the file is still ingesting or has
  no indexed chunks, there is no extracted text to return — use `download` to
  fetch the original bytes instead.

## Citing File Pages

After reading **any** file (PDF, Office, text, etc.) and using its content in your
answer, declare citations. `cite` works on **any** file type, not just PDFs.
`--read-method` is **mandatory**: it records how you actually read the cited page(s).

```bash
unique-cli cite report.pdf --pages 3,5 --read-method text
unique-cli cite cont_abc123 --pages 1-4 --read-method vision
unique-cli cite data.xlsx --read-method text          # non-paginated: omit --pages
```

This registers `[filesourceN]` markers. Use them inline in your answer.
The platform converts `[filesourceN]` into footnotes and clickable reference chips.

**Which page number to cite.** `cite` expects **physical page positions** (1-based) — the same positions ingestion assigns and that `unique-cli read` prints as `[p.N]` / `[p.N-M]` prefixes. NEVER cite a printed page number from a header/footer; those often differ from the physical position.

**Preferred path — you read the file with `unique-cli read` (no download needed):**
The `[p.N]` markers in `read` output are already physical positions from ingestion, identical to what `cite` consumes. Cite those page numbers directly. Do **not** download the file or run `pdfinfo` / `pdftotext` just to re-derive pages you can already see in the `read` output — that duplicates work `read` already did and wastes round-trips.

**Fallback path — verify against the raw file only when you must:**
If you obtained the content some other way (you `download`ed the raw bytes and parsed them yourself, or `read` returned text with no `[p.N]` markers), confirm the physical page before citing:

1. `pdfinfo file.pdf | grep Pages` — total physical page count.
2. For **each** page you intend to cite, run `pdftotext -f N -l N file.pdf -` and confirm the referenced content is actually on that physical page.
3. Cite only the verified physical page numbers.

**`--pages` is optional.** Omit it to cite the **whole file**. Paginated formats
(PDF, PPTX) take page/slide numbers; **non-paginated formats (Excel `.xlsx`/`.xls`,
CSV, `.txt`, HTML, images) have no pages — always omit `--pages`** and cite the
whole file.

**Choosing `--read-method`** (declare the *representation* you actually read the
cited value from). Pick it by the **modality you read** — NOT by how you *located*
the page. Locating a page with `unique-cli read` does **not** force `indexed`: if you
then rendered that page and read a chart/figure with vision, the method is `vision`.

- `text` → you used **extracted text** (`pdftotext`, PyMuPDF / `fitz` `page.get_text()`, MarkItDown, or any text extraction).
- `vision` → you read a **rendered image** of the page/slide (e.g. `get_pixmap()`) with your vision capability — including when you located the page via `unique-cli read` but then rendered it to read a chart, figure, table, or scanned page.
- `indexed` → you used the **text returned by `unique-cli read`** (the platform's indexed chunks) as your answer source.

| Value | When to use |
|-------|-------------|
| `text` | You extracted the page/document text yourself and used that text. |
| `vision` | You read a rendered image of the page with your vision capability — even if you located the page via `unique-cli read`. |
| `indexed` | You used the text returned by `unique-cli read` (indexed chunks) as your source. |

**Verify page numbers before citing — unless you located them via `unique-cli read`.**
This is about the *page number* only, and is **independent of `--read-method`**. If you
located the page with `unique-cli read`, its `[p.N]` / `[p.N-M]` markers are already
physical positions — trust them and skip the checks below, even if you then rendered the
page and read it with vision (in that case still cite `--read-method vision`). Only when
you obtained the page some other way — you `download`ed the raw bytes and parsed them
yourself, or `read` returned no `[p.N]` markers — pick the row matching the file you read
and verify the cited content really is where you claim before calling `cite`:

- **PDF** — `pdfinfo file.pdf | grep Pages` for the total physical page count, then
  for **each** page run `pdftotext -f N -l N file.pdf -` and confirm the content is
  on that physical page. Page numbers are **physical PDF positions** (1-based);
  NEVER use printed page numbers from headers/footers — they often differ.
- **PPTX** — the page number is the **slide number** (1-based). Verify against the
  slide you actually read.
- **DOCX** — use the rendered page from your text extraction; if there is no
  reliable page boundary, cite the **whole file** (omit `--pages`).
- **Non-paginated (XLSX/CSV/TXT/HTML/images)** — there are no pages. Do **NOT**
  pass `--pages`; cite the whole file and verify the content exists in it.

Then determine `--read-method` by the **modality you actually read** — independent of
how you located the page. In a fallback chain (e.g. text extraction returned nothing →
render + read visually), report `text` if you used extracted text or `vision` if you read
a rendered image. If you located the page via `unique-cli read` but read the cited value
off a rendered image (a chart, figure, table, or scanned page), report `vision`, not
`indexed`. Only after confirming the page numbers, call `unique-cli cite` with the
verified page numbers (if any) and `--read-method`.

- **One method per `cite` call.** If different pages were read with different methods, issue separate `cite` calls — one per method.
- Numbers are **per-turn only**; do not reuse from prior turns.
- Do NOT use `cite` for content from `unique-cli search` or `unique-cli web-search` — those are referenced automatically.

## Error Handling

- If env vars are missing, the CLI exits with a clear error listing the missing variables.
- File-not-found and folder-not-found errors are returned as text, not exceptions.
- Successful results print to stdout -- parse output as needed.
- Scope denials (e.g. a file or folder outside the task scope) print to **stderr** and exit with a **non-zero** status, so a denial in an `&&` chain stops the chain instead of being treated as success. Read the stderr message: it names the in-scope folders/documents to redirect you, rather than retrying the same out-of-scope target.

## Interactive Mode

For multiple operations, use the interactive shell:

```bash
unique-cli
```

This opens a REPL with the same commands (without the `unique-cli` prefix). Type `help` for a list or `exit` to quit.
