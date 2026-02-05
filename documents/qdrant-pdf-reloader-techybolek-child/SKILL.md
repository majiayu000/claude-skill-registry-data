---
name: qdrant-pdf-reloader
description: Surgically reloads a single PDF to Qdrant by deleting old chunks and re-uploading with fixes. Use when user wants to reload, refresh, fix, or update a specific PDF without reloading the entire collection.
---

# Qdrant PDF Reloader

This skill helps users surgically reload a single PDF document to Qdrant without reloading the entire collection, using the `LOAD_DB/reload_single_pdf.py` script.

## When to Use This Skill

Activate this skill automatically when the user:
- Wants to reload/refresh a specific PDF in Qdrant
- Needs to fix text cleaning issues in a particular document
- Wants to update a document with improved processing
- Needs to regenerate contextual embeddings for one PDF
- Asks to "reload [filename]", "refresh [filename]", or "fix [filename]"
- Uses keywords like "reload PDF", "refresh document", "update single file"

## What is Surgical Reload?

A **surgical reload** is a targeted operation that:
1. **Deletes** all existing chunks for the specified PDF from Qdrant
2. **Re-processes** the PDF with current text cleaner and chunking logic
3. **Generates** fresh contextual embeddings (document context + chunk context)
4. **Uploads** the new chunks to Qdrant

**Benefits:**
- Much faster than reloading the entire collection (seconds vs. hours)
- Only affects the target PDF - other documents remain unchanged
- Applies latest fixes (text cleaner, TOC filtering, contextual embeddings)
- No risk of losing other documents' data

## How to Use

### Step 1: Identify the PDF to Reload

Ask the user which PDF file needs to be reloaded. The filename must match exactly (e.g., `document-name.pdf`).

### Step 2: Verify PDF Exists

Check that the PDF file exists in the `scraped_content/raw/pdfs/` directory:

```bash
ls scraped_content/raw/pdfs/document-name.pdf
```

If not found, inform the user and ask them to verify the filename.

### Step 3: Run the Reload Script

Execute the surgical reload:

```bash
cd LOAD_DB
python reload_single_pdf.py document-name.pdf
```

The script takes the PDF filename as the only argument.

### Step 4: Monitor Progress

The script will output progress through these stages:
1. **Deletion**: Removing old chunks from Qdrant
2. **Processing**: Loading PDF, cleaning text, chunking
3. **Context Generation**: Creating document and chunk contexts
4. **Upload**: Uploading new chunks with embeddings

### Step 5: Report Results

After completion, summarize:
- Number of old chunks deleted
- Number of new chunks uploaded
- Any errors or warnings encountered
- Confirm successful reload

## Script Features

### Automatic Text Cleaning
The script applies the **fixed text cleaner** which:
- Normalizes whitespace
- Removes page headers/footers
- Cleans special characters
- Filters out Table of Contents (TOC) chunks

### Contextual Embeddings
The script generates **contextual metadata**:
- **Master Context**: High-level overview of the entire Texas childcare system
- **Document Context**: Summary of the specific document (purpose, key topics)
- **Chunk Context**: Summary of the previous chunk for continuity

These contexts are included in embeddings to improve retrieval accuracy.

### Special Handling

**Table-heavy PDFs** (configured in `config.TABLE_PDFS`):
- Extracted using Docling (table-aware extraction)
- Tables extracted as markdown and kept as separate chunks
- Narrative text grouped into ~1000 char chunks
- Item-level chunking (no overlap, semantic boundaries)
- Examples: income eligibility tables, evaluation reports

**Standard PDFs** (PyMuPDF extraction):
- Single-page: Loaded as one chunk to preserve structure
- Multi-page: Split using `RecursiveCharacterTextSplitter`
  - Chunk size: 1000 characters
  - Overlap: 200 characters

### Collection Target

By default, reloads to the **contextual collection** (`tro-child-1` or similar).

## Example Workflows

### Example 1: Fix Text Cleaning Issue

```
User: "The income eligibility PDF has garbled text. Can you reload it with the fixed text cleaner?"

Claude: I'll surgically reload that PDF with the updated text cleaner.

[Runs command]
cd LOAD_DB
python reload_single_pdf.py bcy-26-income-eligibility-and-maximum-psoc-twc.pdf

[Script output shows progress]
✓ Deleted 12 old chunks
✓ Loaded 8 pages
✓ Created 10 chunks after filtering (removed 2 TOC chunks)
✓ Generated contextual metadata
✓ Uploaded 10 new chunks

Reload complete! The document has been refreshed with:
- Fixed text cleaning
- TOC filtering
- Fresh contextual embeddings

Old chunks: 12 deleted
New chunks: 10 uploaded
```

### Example 2: Update After PDF Replacement

```
User: "I replaced the payment rates PDF with a corrected version. Please reload it."

Claude: I'll reload the payment rates PDF with the new version.

[Runs command]
cd LOAD_DB
python reload_single_pdf.py bcy25-child-care-provider-payment-rates-twc.pdf

✓ Surgical reload complete!
Deleted: 5 old chunks (single-page table)
Uploaded: 5 new chunks

The updated PDF is now in Qdrant with fresh contextual embeddings.
```

### Example 3: Regenerate Contextual Embeddings

```
User: "Can you regenerate the contextual embeddings for the state plan document?"

Claude: I'll reload the state plan to regenerate contextual metadata.

cd LOAD_DB
python reload_single_pdf.py tx-ccdf-state-plan-ffy2025-2027-approved.pdf

This will:
1. Delete existing chunks
2. Re-process the PDF
3. Generate new document and chunk contexts
4. Upload with fresh embeddings

[After completion]
✓ Reloaded with new contextual embeddings:
- Document context: [summary of document]
- Chunk contexts: Generated for all 87 chunks
```

### Example 4: Fix Single-Page Table

```
User: "The PSOC chart isn't being retrieved correctly. It's a single-page table PDF."

Claude: Single-page PDFs are loaded as one chunk to preserve table structure. Let me reload it.

cd LOAD_DB
python reload_single_pdf.py bcy2025-psoc-chart-twc.pdf

✓ Single-page PDF: loading as 1 chunk (3,245 characters)
✓ Uploaded 1 chunk with full table content

The table is now loaded as a single coherent chunk, which should improve retrieval.
```

## When to Use vs. Full Reload

### Use Surgical Reload When:
- ✅ Fixing a specific document
- ✅ One or a few PDFs need updating
- ✅ Quick fix needed (seconds/minutes)
- ✅ Other documents are correct and shouldn't be touched

### Use Full Reload When:
- ❌ Major changes to chunking logic or embeddings model
- ❌ Many/most documents need updating
- ❌ Collection structure changed
- ❌ Starting fresh with new documents

**Rule of thumb:** If updating < 10 PDFs, use surgical reload. If updating > 10 PDFs or making system-wide changes, use full reload.

## Technical Details

### File Location
- **Script:** `LOAD_DB/reload_single_pdf.py`
- **PDF Directory:** `scraped_content/raw/pdfs/`
- **Collection:** `QDRANT_COLLECTION_NAME_CONTEXTUAL` from config

### Architecture
The reload script uses a modular architecture:
- **Extractors** (`LOAD_DB/extractors/`): Factory pattern for PyMuPDF vs. Docling selection
- **Shared Utilities** (`LOAD_DB/shared/`): Common processing and upload logic
- **PyMuPDFExtractor**: Fast text extraction for standard PDFs
- **DoclingExtractor**: Table-aware extraction with item-level chunking for table-heavy PDFs

### Dependencies
The script requires:
- LangChain (`PyMuPDFLoader`, `RecursiveCharacterTextSplitter`)
- OpenAI embeddings (`text-embedding-3-small`)
- Qdrant client
- GROQ API (for contextual metadata generation)
- Docling (for table-aware PDFs in `config.TABLE_PDFS`)
- Local modules:
  - `extractors` - Factory pattern and extractor classes
  - `shared` - Processing utilities and upload logic
  - `contextual_processor` - Context generation
  - `text_cleaner` - Text cleaning and TOC detection
  - `prompts` - Master context template

### Process Flow

```
1. DELETE PHASE
   └─ Scroll through collection
   └─ Find chunks where filename == pdf_filename
   └─ Delete all matching chunks

2. EXTRACTION PHASE (via Factory Pattern)
   ├─ Check if PDF in config.TABLE_PDFS
   ├─ If YES: Use DoclingExtractor
   │   ├─ Convert PDF with Docling
   │   ├─ Extract tables as markdown
   │   ├─ Group items by page and sort by y-position
   │   └─ Create item-level chunks (tables + narrative)
   └─ If NO: Use PyMuPDFExtractor
       └─ Load PDF with PyMuPDFLoader (standard extraction)

3. PROCESS PHASE (via shared utilities)
   └─ Clean text on each page (clean_documents)
   └─ Enrich metadata (enrich_metadata)
   └─ Split into chunks if multi-page (text_splitter)
   └─ Filter out TOC chunks (filter_toc_chunks)
   └─ Add chunk metadata (add_chunk_metadata)

4. CONTEXT PHASE (Contextual Mode)
   └─ Generate document context from first 2000 chars
   └─ Generate chunk context for each chunk (uses previous chunk)
   └─ Add master context, document context, chunk context to metadata

5. UPLOAD PHASE (via shared uploader)
   └─ Generate OpenAI embeddings from enriched text
   └─ Create Qdrant points with embeddings + metadata
   └─ Store only original content in page_content
   └─ Upload in batches (100 per batch)
```

### Metadata Added to Chunks

Each uploaded chunk includes:
```python
{
    'text': chunk.page_content,
    'filename': pdf_filename,
    'content_type': 'pdf',
    'page': page_number,
    'total_pages': total_page_count,
    'chunk_index': chunk_number,
    'total_chunks': total_chunk_count,
    'chunk_type': 'table' | 'narrative',  # Docling only
    'extractor': 'docling' | 'pymupdf',
    'has_context': True,
    'master_context': master_context_text,
    'document_context': document_summary,
    'chunk_context': previous_chunk_summary,
    'source_url': url (if available from metadata.json)
}
```

## Error Handling

### PDF Not Found
If the PDF doesn't exist in `scraped_content/raw/pdfs/`:
- Verify the filename (exact match, case-sensitive)
- Check if the PDF was scraped/downloaded
- Suggest running the scraper if needed

### Deletion Errors
If deletion fails:
- Check Qdrant connection
- Verify API credentials
- Check if chunks actually exist (use `retrieve_chunks_by_filename.py`)

### Processing Errors
If PDF processing fails:
- Verify PDF is not corrupted
- Check if PDF is readable (try opening manually)
- Review error logs for specifics

### Upload Errors
If upload fails:
- Check OpenAI API key (for embeddings)
- Verify Qdrant connection
- Check if collection exists

## Advanced Usage

### Verify Before Reloading

Use the `qdrant-chunk-retriever` skill to check existing chunks before reloading.

### Verify After Reloading

After reloading, use the `qdrant-chunk-retriever` skill to confirm:
- Chunk count matches expectations
- Text is cleaned properly
- Context fields are populated
- Extractor type is correct (docling vs pymupdf)
- Chunk types are set (for Docling PDFs)

### Compare Before/After

1. Use `qdrant-file-exporter` skill to export chunks before reload
2. Reload the PDF:
```bash
cd LOAD_DB
python reload_single_pdf.py doc.pdf
```
3. Use `qdrant-file-exporter` skill again to export chunks after reload
4. Compare the exported files to see what changed

## Notes

- **Contextual mode is default**: All reloads use contextual embeddings
- **Chunk IDs are deterministic**: Based on hash of (filename, chunk_index, page)
- **Idempotent operation**: Running multiple times produces same result
- **No undo**: Once chunks are deleted, they're gone (reload completes the operation)
- **Collection must exist**: Script doesn't create collections, only updates existing ones

## Related Tools

- Skills:
  - `qdrant-chunk-retriever`: Verify chunks before/after reload
  - `qdrant-doc-deleter`: Delete without reloading (if you just want to remove)
  - `qdrant-file-exporter`: Export all chunks from a PDF to text file
- Scripts:
  - `LOAD_DB/load_pdf_qdrant.py`: Full collection reload (all PDFs)
  - `LOAD_DB/verify_qdrant.py`: Verify collection statistics
- Shared Modules:
  - `LOAD_DB/extractors/`: PDF extraction with factory pattern
  - `LOAD_DB/shared/`: Common processing and upload utilities
