---
name: bioresearcher-pubmed-weekly
description: "Downloads the past week's PubMed daily update XML.gz files from ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/, streams-parses interleaved PubmedArticle and DeleteCitation records, and produces one combined Excel workbook plus a summary JSON. Use for weekly PubMed/NLM literature tracking, NCBI updatefiles retrieval, pubmedNNnNNNN.xml.gz parsing, PMID/DOI/journal/author extraction, deleted-PMID lists, or building a weekly biomedical literature table."
license: Apache-2.0
compatibility: "Unix-like shells (Linux, macOS, Git Bash) and Windows cmd.exe; requires uv + openpyxl and NCBI FTP access"
metadata:
  version: "1.0.0"
  source: "opencode-bioresearcher-plugin@1.7.2"
allowed-tools: Bash Read Glob
---

# PubMed Weekly Update Download and Parse

This skill downloads the past week's (Monday-Sunday) PubMed daily update `xml.gz` files from `ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/`, parses them with the bundled streaming scripts, and produces ONE combined Excel workbook (`combined.xlsx`) plus a summary JSON.

## Workflow Overview

1. **Python environment check**: ensure uv is available (install via the `bioresearcher-python-setup-uv` skill if needed)
2. **Date-range calculation**: compute the past week's Monday-Sunday range
3. **FTP listing + filtering**: fetch available `xml.gz` updatefiles and keep those modified within the week
4. **Download with retry + resume**: download each filtered file (3 attempts, 2s delay, `.part` resume)
5. **Parse + combine via scripts**: parse all downloaded files and produce one Excel workbook
6. **Report**: verify outputs and summarize to the user

## Prerequisites

- Internet connection and access to the NCBI FTP server
- uv package manager (if missing, load the `bioresearcher-python-setup-uv` skill and follow it EXACTLY, then return here)
- openpyxl is provided at runtime via `uv run --with openpyxl`

## Script Usage

Replace `<skill_dir>` with the full path to this skill's directory (the scripts live in `<skill_dir>/scripts/`). Run all commands from the working directory where downloads should land.

**For Unix-like shells (Git Bash / macOS / Linux):**
```bash
uv run --with openpyxl python <skill_dir>/scripts/pubmed_weekly.py <command> [args...]
```

**For Windows cmd.exe:**
```bash
uv.exe run --with openpyxl python <skill_dir>\scripts\pubmed_weekly.py <command> [args...]
```

## Steps

Follow these steps EXACTLY as described.

### Step 1: Check uv Prerequisite

```bash
if [ -f "uv" ] || [ -f "uv.exe" ]; then
  echo "uv already installed"
else
  echo "uv not found, setting up..."
fi
```

If uv is not installed, load the `bioresearcher-python-setup-uv` skill and follow all its steps EXACTLY, then continue with Step 2 below.

### Step 2: Calculate Week Date Range

Determine the date range for the past week (Monday through Sunday).

**For Unix-like shells:**
```bash
uv run --with openpyxl python <skill_dir>/scripts/pubmed_weekly.py calculate_week
```

**For Windows cmd.exe:**
```bash
uv.exe run --with openpyxl python <skill_dir>\scripts\pubmed_weekly.py calculate_week
```

This outputs the week folder name in format `YYYYMMDD-YYYYMMDD`, e.g.:

```
20250217-20250223
```

### Step 3: Fetch FTP File List

Fetch the list of daily update `xml.gz` files from the NCBI FTP server.

**For Unix-like shells:**
```bash
uv run --with openpyxl python <skill_dir>/scripts/pubmed_weekly.py fetch_files
```

**For Windows cmd.exe:**
```bash
uv.exe run --with openpyxl python <skill_dir>\scripts\pubmed_weekly.py fetch_files
```

**Expected output (space-separated filenames):**
```
pubmed24n1234.xml.gz pubmed24n1235.xml.gz pubmed24n1236.xml.gz
```

### Step 4: Filter Files for Past Week

Filter the file list to those modified within the week (PubMed filenames do not encode dates, so FTP modification times are used).

**For Unix-like shells:**
```bash
uv run --with openpyxl python <skill_dir>/scripts/pubmed_weekly.py filter_files "<WEEK>" "<FILE_LIST>"
```

**For Windows cmd.exe:**
```bash
uv.exe run --with openpyxl python <skill_dir>\scripts\pubmed_weekly.py filter_files "<WEEK>" "<FILE_LIST>"
```

Where `<WEEK>` is the week folder name (e.g., `20250217-20250223`) and `<FILE_LIST>` is the Step 3 output (quote it). Returns the space-separated filtered list.

### Step 5: Download Files with Retry and Resume

Download each filtered file into `.download/pubmed-daily/<WEEK>/`.

**For Unix-like shells:**
```bash
for file in <FILE_LIST>; do
  uv run --with openpyxl python <skill_dir>/scripts/pubmed_weekly.py download_file "<WEEK>" "$file"
done
```

**For Windows cmd.exe:**
```bash
for %f in (<FILE_LIST>) do uv.exe run --with openpyxl python <skill_dir>\scripts\pubmed_weekly.py download_file "<WEEK>" %f
```

**Download behavior:**
- Downloads one file at a time to `<filename>.part`, renamed on success
- Retries up to 3 times per file with 2-second delays
- Resumes interrupted `.part` downloads; skips already-completed files
- If a download fails after 3 retries, ask the user: "Abort remaining downloads?" ("Yes" / "No"). "Yes" stops and reports; "No" skips the failed file and continues

### Step 6: Parse and Combine into One Excel

Parse every downloaded `xml.gz` in the week directory and write ONE combined workbook `combined.xlsx` plus `summary.json` (recommended; done in a single command):

**For Unix-like shells:**
```bash
uv run --with openpyxl python <skill_dir>/scripts/pubmed_weekly.py combine "<WEEK>"
```

**For Windows cmd.exe:**
```bash
uv.exe run --with openpyxl python <skill_dir>\scripts\pubmed_weekly.py combine "<WEEK>"
```

**Output location:**
```
.download/pubmed-daily/<WEEK>/combined.xlsx
.download/pubmed-daily/<WEEK>/summary.json
```

Alternatively, invoke the parser directly (Unix; on Windows cmd.exe list files explicitly since cmd.exe does not expand `*`):
```bash
uv run --with openpyxl python <skill_dir>/scripts/parse_updatefiles.py \
  .download/pubmed-daily/<WEEK>/pubmed24n1234.xml.gz \
  .download/pubmed-daily/<WEEK>/pubmed24n1235.xml.gz \
  -o .download/pubmed-daily/<WEEK>/combined.xlsx \
  --summary-json .download/pubmed-daily/<WEEK>/summary.json
```

The parser accepts plain `.xml` as well as `.xml.gz` (gzip-transparent) and any number of input files; ordering follows the given file order, document order within each file.

### Step 7: Verify and Report

```bash
ls -lh .download/pubmed-daily/<WEEK>/
```

Report to the user: week range, files found/downloaded/failed, download location, article count and deleted-PMID count in `combined.xlsx`, and the `combined.xlsx` / `summary.json` locations.

## Frozen Output Schema

`combined.xlsx` (openpyxl workbook, write_only; schema is FROZEN — do not change):

**Sheet 1: `PubMed Articles`** — columns in EXACT order:

| # | Column | Source |
|---|--------|--------|
| 1 | `PMID` | `MedlineCitation/PMID` text |
| 2 | `DOI` | `PubmedData/ArticleIdList/ArticleId[@IdType='doi']` if present, else empty |
| 3 | `Title` | `Article/ArticleTitle` (inline markup flattened) |
| 4 | `Journal` | `Article/Journal/Title` |
| 5 | `ISSN` | first `Article/Journal/ISSN` |
| 6 | `PubDate` | `Journal/JournalIssue/PubDate` normalized: Year + Month (name or number) → `YYYY-MM`; Year only → `YYYY`; no Year → empty |
| 7 | `FirstAuthor` | first `Article/AuthorList/Author` as `LastName Initials` (e.g., `Smith J`) |
| 8 | `LastAuthor` | last `Article/AuthorList/Author` in the same format |
| 9 | `PublicationTypes` | `Article/PublicationTypeList/PublicationType` values joined with `;` |

**Sheet 2: `Deleted PMIDs`** — single column:

| # | Column | Source |
|---|--------|--------|
| 1 | `PMID` | each `DeleteCitation/PMID` text |

**`summary.json`** (written with `--summary-json` / by `combine`):

```json
{
  "source_files": ["pubmed24n1234.xml.gz"],
  "article_count": 1234,
  "deleted_pmids": ["99999999"],
  "first_rows": [{"PMID": "...", "DOI": "...", "Title": "...", "Journal": "...", "ISSN": "...", "PubDate": "...", "FirstAuthor": "...", "LastAuthor": "...", "PublicationTypes": "..."}]
}
```

`first_rows` contains up to the first 3 article rows as objects keyed by the column names above.

## Notes

- updatefiles interleave `<PubmedArticle>` and `<DeleteCitation>` records — BOTH are handled by the parser
- Parsing is memory-bounded streaming: `xml.etree.iterparse` with element clearing plus an openpyxl `write_only` workbook
- No plugin tool dependencies: stdlib `urllib` for FTP, openpyxl for Excel, nothing else
- Output ordering is deterministic: input file order (sorted within `combine`), document order within each file
- All downloads and outputs live under `.download/pubmed-daily/<WEEK>/` in the current working directory
- Only `.xml.gz` updatefiles are downloaded; downloads are sequential with retry + resume
- The FTP server path is `ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/`
- Windows with Git Bash: follow Unix-like shell instructions; Windows cmd.exe: use `uv.exe ...` variants
