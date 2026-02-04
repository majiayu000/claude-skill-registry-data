---
name: qdrant-chunk-retriever
description: Retrieves and inspects chunks from specific PDF documents in Qdrant vector database. Use when user wants to view, inspect, debug, or examine chunks from a particular file, check chunk content, or investigate chunk indexing.
---

# Qdrant Chunk Retriever

This skill helps users retrieve and inspect chunks from specific PDF documents stored in the Qdrant vector database using the `UTIL/retrieve_chunks_by_filename.py` script.

## When to Use This Skill

Activate this skill automatically when the user:
- Wants to view/inspect chunks from a specific PDF file
- Needs to debug chunk content or indexing
- Asks to "show me chunks from [filename]"
- Wants to examine how a document was chunked
- Needs to verify chunk context or metadata
- Asks about chunk content, chunk indices, or chunk details
- Uses keywords like "retrieve chunks", "show chunks", "inspect document chunks"

## How to Use

### Step 1: Identify the Request

Determine what the user wants to retrieve:
- All chunks from a file
- A specific chunk by index
- Chunks saved to JSON
- Full text vs. preview

### Step 2: Build the Command

The script is located at `UTIL/retrieve_chunks_by_filename.py` and supports these options:

**Basic Usage (all chunks from a file):**
```bash
cd UTIL
python retrieve_chunks_by_filename.py --filename "document-name.pdf"
```

**Retrieve specific chunk:**
```bash
python retrieve_chunks_by_filename.py --filename "document.pdf" --chunk 5
```

**Control text preview length:**
```bash
python retrieve_chunks_by_filename.py --filename "document.pdf" --text-length 1000
# Or show full text:
python retrieve_chunks_by_filename.py --filename "document.pdf" --text-length -1
```

**Save to JSON file:**
```bash
python retrieve_chunks_by_filename.py --filename "document.pdf" --output chunks.json
```

**Quiet mode (for JSON export only):**
```bash
python retrieve_chunks_by_filename.py --filename "document.pdf" --output chunks.json --quiet
```

### Step 3: Run the Command

Execute the script with the appropriate options based on the user's request.

### Step 4: Interpret and Present Results

The script outputs:
- **Chunk index** (e.g., "Chunk 5/10")
- **Page number** from the original PDF
- **Filename** and **Point ID** (Qdrant internal)
- **Text content** (truncated or full based on --text-length)
- **Context fields** (if available):
  - `document_context`: Overall document summary
  - `chunk_context`: Previous chunk context for continuity

Present the results to the user, highlighting:
- Number of chunks found
- Chunk content preview or full text
- Any context information available
- Suggested next steps (if debugging)

## Command-Line Options Reference

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--filename` | - | PDF filename to retrieve chunks from | `bcy-26-income-eligibility-and-maximum-psoc-twc.pdf` |
| `--chunk` | `-c` | Specific chunk index (0-indexed) | All chunks |
| `--collection` | - | Qdrant collection name | From config |
| `--text-length` | - | Max characters to display (-1 for full) | 500 |
| `--output` | - | Save to JSON file | None (console only) |
| `--quiet` | - | Suppress console output | False |

## Example Workflows

### Example 1: View All Chunks from a Document

```
User: "Show me all chunks from child-care-services-guide-twc.pdf"

Claude: I'll retrieve all chunks from that document.

[Runs command]
cd UTIL
python retrieve_chunks_by_filename.py --filename "child-care-services-guide-twc.pdf"

✓ Retrieved 15 chunks from 'child-care-services-guide-twc.pdf'

The document contains 15 chunks:
- Chunk 0: Page 1 - [preview of text]
- Chunk 1: Page 2 - [preview of text]
...

Would you like to see the full text of any specific chunk?
```

### Example 2: Inspect Specific Chunk

```
User: "What's in chunk 5 of the payment rates PDF?"

Claude: Let me retrieve chunk 5 from the payment rates document.

[Identifies filename, runs command]
cd UTIL
python retrieve_chunks_by_filename.py --filename "bcy25-child-care-provider-payment-rates-twc.pdf" --chunk 5 --text-length -1

Chunk 5/12 - Page 3
Filename: bcy25-child-care-provider-payment-rates-twc.pdf

Full text:
[Complete chunk text shown]

This chunk contains information about [summary of content].
```

### Example 3: Debug Chunk Context

```
User: "I'm getting weird results for family of 5. Can you check what's in the chunks about that?"

Claude: Let me retrieve chunks from the income eligibility document to examine the context.

[Runs command]
cd UTIL
python retrieve_chunks_by_filename.py --filename "bcy-26-income-eligibility-and-maximum-psoc-twc.pdf" --text-length -1

[Reviews output and identifies relevant chunks]

I found the "family of 5" information in chunk 3. The chunk includes:
- Main text: [relevant content]
- Chunk context: [previous chunk summary for continuity]
- Document context: [overall document summary]

The issue appears to be [explanation based on chunk analysis].
```

### Example 4: Export Chunks to JSON

```
User: "Can you export all chunks from the state plan document to a JSON file?"

Claude: I'll retrieve all chunks and save them to JSON.

cd UTIL
python retrieve_chunks_by_filename.py --filename "tx-ccdf-state-plan-ffy2025-2027-approved.pdf" --output state_plan_chunks.json

✓ Saved 87 chunks to state_plan_chunks.json

The JSON file contains:
- Metadata (filename, total chunks, collection name, timestamp)
- All chunk data (text, page, index, context fields)

File saved to: UTIL/state_plan_chunks.json
```

## Understanding the Output

### Console Output Format

```
================================================================================
RETRIEVED CHUNKS: 10 total
================================================================================

Chunk 0/10 - Page 1
Filename: document.pdf
Point ID: 123e4567-e89b-12d3-a456-426614174000
--------------------------------------------------------------------------------
Text:
[Chunk text content here...]
--------------------------------------------------------------------------------
Document Context:
[Summary of the entire document]
Chunk Context:
[Summary of previous chunk for continuity]
--------------------------------------------------------------------------------

[More chunks...]
```

### JSON Output Format

```json
{
  "metadata": {
    "filename": "document.pdf",
    "total_chunks": 10,
    "retrieved_at": "2025-01-15T10:30:00",
    "collection": "tro-child-1"
  },
  "chunks": [
    {
      "id": "point-id",
      "chunk_index": 0,
      "total_chunks": 10,
      "page": 1,
      "text": "chunk content...",
      "filename": "document.pdf",
      "source_url": "https://...",
      "has_context": true,
      "master_context": "...",
      "document_context": "...",
      "chunk_context": "..."
    }
  ]
}
```

## Debugging Use Cases

### Use Case 1: Verify Chunk Splitting
Check how a document was chunked and if chunks are appropriately sized:
```bash
python retrieve_chunks_by_filename.py --filename "doc.pdf" --text-length -1
```

### Use Case 2: Investigate Missing Information
If retrieval isn't finding expected content, examine chunks to verify the text is present:
```bash
python retrieve_chunks_by_filename.py --filename "doc.pdf" | grep -i "search term"
```

### Use Case 3: Check Context Fields
Verify that contextual embeddings include proper context:
```bash
python retrieve_chunks_by_filename.py --filename "doc.pdf" --chunk 5 --text-length -1
```
Look for `document_context` and `chunk_context` fields in output.

### Use Case 4: Export for Analysis
Save chunks to JSON for external analysis or comparison:
```bash
python retrieve_chunks_by_filename.py --filename "doc.pdf" --output analysis.json
```

## Error Handling

### Filename Not Found
If no chunks are found:
- Verify the exact filename (case-sensitive, include .pdf extension)
- Suggest running `verify_qdrant.py` to list all documents
- Check if the document was loaded successfully

### Connection Errors
If Qdrant connection fails:
- Verify QDRANT_API_URL and QDRANT_API_KEY environment variables
- Check network connectivity
- Confirm collection name is correct

### Invalid Chunk Index
If requesting a chunk that doesn't exist:
- First retrieve all chunks to see the valid range
- Remind user that chunk indices are 0-indexed

## Notes

- **Default filename**: If no filename is specified, uses `bcy-26-income-eligibility-and-maximum-psoc-twc.pdf`
- **Chunk ordering**: Chunks are automatically sorted by `chunk_index` to maintain document order
- **Text truncation**: Default shows 500 characters; use --text-length -1 for full text
- **Collection**: Defaults to `QDRANT_COLLECTION_NAME_CONTEXTUAL` from config
- **Efficient retrieval**: Uses Qdrant scroll API with filtering for performance

## Related Tools

- `UTIL/delete_documents.py`: Delete documents from Qdrant
- `LOAD_DB/verify_qdrant.py`: List all documents and statistics
- `LOAD_DB/reload_single_pdf.py`: Reload a single PDF document
