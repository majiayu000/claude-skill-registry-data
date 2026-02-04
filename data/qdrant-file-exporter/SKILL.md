---
name: qdrant-file-exporter
description: Extracts all chunks with three-tier contextual embeddings from a specific PDF file in Qdrant vector database and saves to plain text. Use when user wants to extract, export, dump, or view all chunks from a PDF document, inspect file content, save chunks for analysis, or review contextual embeddings.
---

# Qdrant File Exporter

Extracts all text chunks with three-tier contextual embeddings from a specific PDF file stored in the Qdrant vector database and saves them to a plain text file.

## When to Use This Skill

Activate this skill when the user:
- Wants to extract all chunks from a specific PDF
- Asks to export, dump, or save chunks from a document
- Needs to view all chunk content for a file
- Wants to analyze chunks outside of the vector database
- Needs to review or inspect the three-tier contextual embeddings
- Wants to see how chunks were contextualized during loading
- Says things like "export chunks from [filename]" or "dump all chunks for [file]"

## How to Use

### Step 1: Get the PDF Filename

Ask the user which PDF file they want to export chunks from. The filename should match exactly what's stored in the Qdrant `doc` field (e.g., "bcy-26-income-eligibility-and-maximum-psoc-twc.pdf").

If the user doesn't know the exact filename, suggest using the `qdrant-chunk-retriever` skill first to search for files.

### Step 2: Run the Export Script

Execute the Python helper script:

```bash
python .claude/skills/qdrant-file-exporter/scripts/export_chunks.py "filename.pdf"
```

The script will:
1. Connect to Qdrant (tro-child-3-contextual collection)
2. Retrieve all chunks matching the filename
3. Save them to `UTIL/[filename]_chunks.txt`

### Step 3: Report Results

After the script completes, inform the user:
- Total number of chunks extracted
- Output file location
- File size (if available)
- Mention that contexts are included

Example:
```
✅ Extracted 47 chunks from bcy-26-income-eligibility-and-maximum-psoc-twc.pdf
📄 Saved to: UTIL/bcy-26-income-eligibility-and-maximum-psoc-twc_chunks.txt
📊 Includes master context, document context, and chunk-specific contexts
```

### Step 4: Offer Next Steps

Ask the user if they want to:
- View the exported file
- Export another PDF
- Analyze the chunk content

## Examples

### Example 1: Basic Export

```
User: "Export all chunks from the income eligibility PDF"
Assistant: "Which PDF would you like to export? Please provide the exact filename."
User: "bcy-26-income-eligibility-and-maximum-psoc-twc.pdf"
Assistant: *Runs export script*
          "✅ Extracted 47 chunks from bcy-26-income-eligibility-and-maximum-psoc-twc.pdf
           📄 Saved to: UTIL/bcy-26-income-eligibility-and-maximum-psoc-twc_chunks.txt"
```

### Example 2: Export for Analysis

```
User: "I need to see all the chunks for the PSOC chart document"
Assistant: *Runs export script with bcy-26-psoc-chart-twc.pdf*
          "✅ Extracted 12 chunks from bcy-26-psoc-chart-twc.pdf
           📄 Saved to: UTIL/bcy-26-psoc-chart-twc_chunks.txt

           Would you like me to open the file or analyze the content?"
```

## Error Handling

### File Not Found in Qdrant

If the PDF filename doesn't match any documents:
- Suggest the user check the filename spelling
- Recommend using `qdrant-chunk-retriever` to search for available files
- List similar filenames if possible

### Connection Errors

If Qdrant connection fails:
- Check QDRANT_API_URL and QDRANT_API_KEY environment variables
- Verify the collection name (tro-child-3-contextual) exists
- Suggest running `python LOAD_DB/verify_qdrant.py` to check connection

### No Chunks Found

If the file exists but has 0 chunks:
- Verify the file was loaded correctly
- Suggest running the loader script if needed

## Dependencies

- Qdrant client (`qdrant-client`)
- Environment variables: QDRANT_API_URL, QDRANT_API_KEY
- Collection: tro-child-3-contextual (must exist)

## Output Format

The exported text file contains:
- **Master Context** (once at beginning): Domain-level context for all chunks
- **Document Context** (once at beginning): Document-specific summary
- **Chunks** in original document order (sorted by chunk_index from loading pipeline)
  - Header: `--- Chunk N (Page X) ---`
  - Chunk-specific context: `[Chunk Context]: ...`
  - Plain text content
- Starts from the beginning of the document
