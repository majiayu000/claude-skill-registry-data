---
name: julien-calibre
description: Complete Calibre library management - add/remove books, convert PDF to EPUB, metadata editing, library analysis, cleanup, and e-reader sync (Sony PRS-T1). Use for any ebook or Calibre operation.
license: Apache-2.0
triggers:
  # English - Core
  - calibre
  - ebook
  - epub
  - book library
  # English - Add/Import
  - add book to calibre
  - import ebook
  - add pdf to library
  - download from gutenberg
  # English - Remove
  - remove book from calibre
  - delete duplicates
  # English - Convert
  - convert pdf to epub
  - convert to epub
  - batch convert pdf
  # English - Metadata
  - update metadata
  - fix book title
  - set cover
  - edit book details
  # English - Analyze/Cleanup
  - analyze library
  - clean up library
  - find duplicates
  - library maintenance
  # English - E-reader
  - sync to e-reader
  - send to kindle
  - transfer to sony
  # French - Core
  - bibliotheque calibre
  - livre numerique
  # French - Actions
  - ajouter livre calibre
  - importer ebook
  - convertir pdf en epub
  - nettoyer bibliotheque
  - supprimer livre
  - mettre a jour metadonnees
  - synchroniser liseuse
  - envoyer sur liseuse
allowed-tools:
  - Bash
  - Read
  - Write
  - WebSearch
  - WebFetch
---

# Calibre Library Management

Complete ebook library management with Calibre.

## Configuration

| Property | Value |
|----------|-------|
| **Calibre** | C:\Program Files\Calibre2\ |
| **Library** | C:\Users\julien\OneDrive\Calibre\Calibre Library |
| **E-Reader** | Sony PRS-T1 (EPUB, PDF, TXT) |

**IMPORTANT**: Close Calibre before using CLI commands.

---

## 1. Add Books

### Add Local File

```powershell
& 'C:\Program Files\Calibre2\calibredb.exe' add 'PATH\TO\BOOK.epub' --library-path 'C:\Users\julien\OneDrive\Calibre\Calibre Library'
```

### Add with Metadata

```powershell
calibredb add "book.epub" --title "Title" --authors "Author" --library-path "..."
```

### Add Folder Recursively

```powershell
calibredb add "C:\Folder" --recurse --library-path "..."
```

### Download from Project Gutenberg

1. Search: `WebSearch: "TITLE AUTHOR site:gutenberg.org/ebooks"`
2. Extract ID from URL (`/ebooks/24850` → 24850)
3. Download: `curl -L "https://www.gutenberg.org/ebooks/24850.epub3.images" -o "book.epub"`
4. Add to Calibre

---

## 2. Remove Books

### Remove by ID

```powershell
calibredb remove 123 --permanent --library-path "..."
```

### Remove Multiple

```powershell
calibredb remove 98,99,100,101 --permanent --library-path "..."
```

### Remove Format Only (keep book)

```powershell
calibredb remove_format 123 PDF --library-path "..."
```

### Search Then Remove

```powershell
# Find IDs
calibredb search "author:Zola" --library-path "..."
# Remove
calibredb remove ID1,ID2 --permanent --library-path "..."
```

---

## 3. Convert PDF to EPUB

### Basic Conversion

```powershell
& 'C:\Program Files\Calibre2\ebook-convert.exe' 'input.pdf' 'output.epub'
```

### With Heuristics (better quality)

```powershell
ebook-convert 'input.pdf' 'output.epub' --enable-heuristics
```

### Add EPUB to Existing Book

```powershell
calibredb add_format BOOK_ID 'output.epub' --library-path "..."
```

### Find Books Without EPUB

```powershell
calibredb list --search 'formats:PDF NOT formats:EPUB' --fields id,title,formats --library-path "..."
```

### PDF Types

| Type | Quality | Notes |
|------|---------|-------|
| Text PDF | Good | Direct conversion |
| Scanned/Image | Poor | Needs OCR |
| Mixed | Variable | Use heuristics |

---

## 4. Metadata Management

### View Metadata

```powershell
calibredb show_metadata BOOK_ID --library-path "..."
```

### Set Metadata

```powershell
calibredb set_metadata BOOK_ID -f 'title:New Title' --library-path "..."
calibredb set_metadata BOOK_ID -f 'authors:Author Name' --library-path "..."
calibredb set_metadata BOOK_ID -f 'languages:fra' --library-path "..."
calibredb set_metadata BOOK_ID -f 'tags:Fiction, Classic' --library-path "..."
```

### Set Cover

```powershell
calibredb set_metadata BOOK_ID -c 'cover.jpg' --library-path "..."
```

### Extract from File

```powershell
& 'C:\Program Files\Calibre2\ebook-meta.exe' 'book.epub'
```

---

## 5. Library Analysis

### List All Books

```powershell
calibredb list --library-path "..."
```

### Search by Language

```powershell
calibredb list --search 'language:eng' --library-path "..."
```

### Find Duplicates

```powershell
calibredb list --search 'formats:PDF AND formats:EPUB' --fields id,title --library-path "..."
```

### Analysis Scripts

```bash
python scripts/analyze/find_empty_books.py      # Books with no format
python scripts/analyze/find_books_without_epub.py  # PDF-only
python scripts/analyze/find_english_books.py    # Filter by language
python scripts/analyze/analyze_library.py       # Format statistics
```

---

## 6. Library Cleanup

### Workflow

```powershell
# 1. Close Calibre + OneDrive
Stop-Process -Name calibre,OneDrive -Force -ErrorAction SilentlyContinue

# 2. Analyze
python scripts/analyze/find_empty_books.py

# 3. Remove
calibredb remove ID1,ID2 --permanent --library-path "..."

# 4. Clean orphaned folders
python scripts/force_delete_orphans.py

# 5. Reopen Calibre
```

### Remove PDF When EPUB Exists

```powershell
# Find books with both formats
calibredb list --search 'formats:PDF AND formats:EPUB' --fields id,title --library-path "..."

# Remove PDF format
calibredb remove_format BOOK_ID PDF --library-path "..."
```

---

## 7. E-Reader Sync

### Device: Sony PRS-T1

- **Formats**: EPUB (preferred), PDF, TXT

### Check Connection

```powershell
Get-PnpDevice | Where-Object { $_.FriendlyName -like "*Sony*" -or $_.FriendlyName -like "*Reader*" }
```

### Transfer Books

**Use Calibre GUI** (no CLI for device sync):
1. Connect e-reader
2. Select books in Calibre
3. Right-click → "Send to device"

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Device not detected | Unplug, wait 5s, replug |
| "No suitable format" | Convert to EPUB first |
| Transfer fails | Check device storage |

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/analyze/find_empty_books.py` | Books with no format |
| `scripts/analyze/find_books_without_epub.py` | PDF-only books |
| `scripts/analyze/find_english_books.py` | Filter by language |
| `scripts/manage/remove_books.py` | Batch removal |
| `scripts/convert/batch_convert.py` | Batch conversion |
| `scripts/force_delete_orphans.py` | Clean orphaned folders |

---

## Quick Reference

```powershell
# Add book
calibredb add "book.epub" --library-path "..."

# Remove book
calibredb remove ID --permanent --library-path "..."

# Convert PDF
ebook-convert "input.pdf" "output.epub" --enable-heuristics

# View metadata
calibredb show_metadata ID --library-path "..."

# Set metadata
calibredb set_metadata ID -f 'title:New Title' --library-path "..."

# List all
calibredb list --library-path "..."

# Search
calibredb search "author:Name" --library-path "..."
```
