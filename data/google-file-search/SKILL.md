---
name: google-file-search
description: Google File Search API templates, configuration patterns, and usage examples for managed RAG with Gemini. Use when building File Search integrations, implementing RAG with Google AI, chunking documents, configuring grounding citations, or when user mentions Google File Search, Gemini RAG, document indexing, or semantic search.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebFetch
---

# Google File Search

Comprehensive skill for implementing Google File Search API with Gemini models for Retrieval-Augmented Generation (RAG).

## Overview

Google File Search provides managed RAG capabilities through:
- Automatic document chunking and embedding generation
- Semantic search across multiple document types
- Metadata-based filtering for targeted retrieval
- Grounding citations showing source documents
- Persistent storage with file search stores
- Integration with Gemini 2.5 models

This skill provides templates, scripts, and examples for implementing File Search in Python applications using the `google-generativeai` package.

## Use When

This skill is automatically invoked when:
- Building RAG systems with Google Gemini
- Implementing document search and retrieval
- Configuring chunking strategies
- Setting up grounding citations
- Managing file search stores
- Uploading and indexing documents
- Filtering search results by metadata
- Testing semantic search capabilities

## Key Capabilities

### 1. Store Management
- Create persistent file search stores
- List and retrieve existing stores
- Delete stores with force option
- Monitor storage quotas (1GB-1TB by tier)

### 2. Document Upload & Indexing
- Direct upload and indexing in single operation
- Separate upload via Files API then import
- Batch file processing
- Support for 100+ file types (PDF, DOCX, code, etc.)
- Maximum file size: 100 MB per document

### 3. Chunking Configuration
- White space-based chunking strategies
- Configurable tokens per chunk
- Overlap token settings for context preservation
- Custom chunking for domain-specific needs

### 4. Metadata & Filtering
- Custom key-value metadata during import
- String and numeric metadata values
- AIP-160 compliant filter syntax
- Multi-condition metadata queries

### 5. Grounding & Citations
- Access to source document references
- Citation extraction from responses
- Fact-checking and verification support
- Transparent sourcing for AI responses

## Security: API Key Handling

**CRITICAL:** All templates and examples use placeholder values:

❌ NEVER hardcode actual API keys
✅ ALWAYS use: `GOOGLE_API_KEY=your_google_api_key_here`
✅ ALWAYS use: `GOOGLE_GENAI_API_KEY=your_google_genai_api_key_here`
✅ ALWAYS read from environment variables in code
✅ ALWAYS add `.env*` to `.gitignore` (except `.env.example`)

Obtain API keys from: https://aistudio.google.com/apikey

## Usage Instructions

### Phase 1: Load Required Documentation

Before implementing File Search, fetch the latest documentation:

```markdown
WebFetch: https://ai.google.dev/gemini-api/docs/file-search
WebFetch: https://ai.google.dev/gemini-api/docs/embeddings
```

### Phase 2: Initialize File Search Store

Use the Python setup script to create a new store:

```bash
python scripts/setup_file_search.py --name "My RAG Store"
```

This Python script:
- Creates a new file search store
- Saves store ID to environment
- Validates creation
- Returns store details

### Phase 3: Configure Chunking Strategy

Customize chunking for your document domain:

```bash
python scripts/configure_chunking.py --max-tokens 200 --overlap 20
```

Generates configuration file with:
- Maximum tokens per chunk
- Overlap tokens for context
- White space chunking strategy

### Phase 4: Upload and Index Documents

Upload files to the store:

```bash
python scripts/upload_documents.py --path /path/to/documents
```

This script:
- Validates file types and sizes
- Uploads and indexes simultaneously
- Applies chunking configuration
- Adds optional metadata
- Tracks upload progress

### Phase 5: Test Semantic Search

Verify search functionality:

```bash
python scripts/search_query.py --query "your search query"
```

Tests:
- Semantic search capabilities
- Citation extraction
- Metadata filtering
- Response grounding

### Phase 6: Validate Setup

Run comprehensive validation:

```bash
python scripts/validate_setup.py
```

Checks:
- Store existence and accessibility
- Indexed document count
- Chunking configuration
- API key configuration
- Storage quota usage

## Available Scripts

### `scripts/setup_file_search.py`
Initialize a new file search store with display name.

**Usage:**
```bash
python scripts/setup_file_search.py --name "Store Name"
```

### `scripts/upload_documents.py`
Upload and index documents to a file search store.

**Usage:**
```bash
python scripts/upload_documents.py --path /path/to/documents
python scripts/upload_documents.py --file /path/to/file.pdf --metadata author="John Doe"
```

### `scripts/configure_chunking.py`
Generate chunking configuration file.

**Usage:**
```bash
python scripts/configure_chunking.py --max-tokens 200 --overlap 20
python scripts/configure_chunking.py --preset small  # 100 tokens, 10 overlap
python scripts/configure_chunking.py --preset large  # 500 tokens, 50 overlap
```

### `scripts/search_query.py`
Test semantic search with sample queries.

**Usage:**
```bash
python scripts/search_query.py --query "explain quantum computing"
python scripts/search_query.py --query "author=Einstein" --metadata-filter
```

### `scripts/validate_setup.py`
Comprehensive validation of File Search configuration.

**Usage:**
```bash
python scripts/validate_setup.py
python scripts/validate_setup.py --verbose
```

## Available Templates

### Configuration Templates

**`templates/store-config.json`**
- File search store creation configuration
- Display name and description
- Storage tier settings

**`templates/chunking-config.json`**
- White space chunking configuration
- Token limits and overlap settings
- Strategy presets

**`templates/metadata-schema.json`**
- Metadata field definitions
- String and numeric value types
- Filtering examples

**`templates/env.example`**
- Environment variable template
- API key placeholders
- Store ID configuration

### Code Templates

**`templates/python-setup.py`**
Complete Python implementation template:
- Store creation and management
- Document upload with chunking
- Search with metadata filtering
- Citation extraction
- Error handling

**`templates/typescript-setup.ts`**
Complete TypeScript implementation template:
- Store initialization
- File upload and indexing
- Semantic search queries
- Grounding metadata parsing
- Type-safe interfaces

## Available Examples

### `examples/basic-setup.md`
Simple File Search implementation for getting started:
- Create first store
- Upload single document
- Perform basic search
- Extract citations

### `examples/advanced-chunking.md`
Custom chunking strategies for different document types:
- Technical documentation (larger chunks)
- Legal documents (precise boundaries)
- Code repositories (function-level chunks)
- Scientific papers (section-based chunks)

### `examples/metadata-filtering.md`
Using metadata for targeted search:
- Add custom metadata during upload
- Filter by author, date, category
- Multi-condition metadata queries
- Combining metadata with semantic search

### `examples/grounding-citations.md`
Extract and display source citations:
- Parse grounding metadata
- Extract document references
- Display citation information
- Build source attribution UI

### `examples/multi-store.md`
Manage multiple file search stores:
- Separate stores by domain
- Cross-store search patterns
- Store migration strategies
- Quota management across stores

## Supported Models

- **gemini-2.5-pro**: Production model for complex reasoning
- **gemini-2.5-flash**: Fast model for quick responses

## Supported File Types

**Documents:** PDF, DOCX, ODT, PPTX, XLSX, CSV, TXT, MD
**Code:** Python, JavaScript, Java, TypeScript, Go, Rust, SQL
**Data:** JSON, XML, YAML, HTML
**Archives:** ZIP (automatically extracted)

Over 100 MIME types supported.

## Storage Limits

**Per-Document:**
- Maximum file size: 100 MB
- Recommended store size: Under 20 GB

**Total Storage by Tier:**
- Free: 1 GB
- Tier 1: 10 GB
- Tier 2: 100 GB
- Tier 3: 1 TB

Storage calculation: Input size × ~3 (includes embeddings)

## Pricing Considerations

- **Indexing:** $0.15 per 1M tokens (one-time per document)
- **Storage:** Free
- **Query embeddings:** Free
- **Retrieved tokens:** Standard context pricing

**Optimization tip:** Index documents once, query multiple times for cost efficiency.

## Best Practices

1. **Chunk Size Optimization**
   - Technical docs: 300-500 tokens
   - General content: 200-300 tokens
   - Code: 100-200 tokens
   - Use overlap for context preservation

2. **Metadata Strategy**
   - Add author, date, category during upload
   - Use consistent naming conventions
   - Plan filtering needs upfront
   - Leverage numeric values for date ranges

3. **Store Organization**
   - Separate stores by domain/project
   - Keep stores under 20 GB for optimal retrieval
   - Name stores descriptively
   - Monitor quota usage

4. **Citation Handling**
   - Always extract grounding metadata
   - Display sources to users
   - Enable fact-checking workflows
   - Track citation coverage

5. **Error Handling**
   - Validate file types before upload
   - Check file size limits
   - Handle quota exceeded errors
   - Retry failed uploads with backoff

## Integration Patterns

### With FastAPI Backend
```python
from google import genai
from fastapi import FastAPI, HTTPException

app = FastAPI()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@app.post("/search")
async def search(query: str, store_id: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={
            "tools": [{"file_search": {"store_id": store_id}}]
        }
    )
    return {
        "answer": response.text,
        "citations": response.candidates[0].grounding_metadata
    }
```

### With Next.js Frontend
```typescript
// app/api/search/route.ts
import { GoogleGenAI } from '@google/generative-ai';

export async function POST(request: Request) {
  const { query, storeId } = await request.json();

  const genai = new GoogleGenAI(process.env.GOOGLE_API_KEY!);
  const model = genai.getGenerativeModel({ model: 'gemini-2.5-flash' });

  const result = await model.generateContent({
    contents: [{ role: 'user', parts: [{ text: query }] }],
    tools: [{ fileSearch: { storeId } }]
  });

  return Response.json({
    answer: result.response.text(),
    citations: result.response.candidates[0].groundingMetadata
  });
}
```

## Troubleshooting

**Issue: Files not uploading**
- Check file size (max 100 MB)
- Verify file type is supported
- Ensure API key has correct permissions
- Check storage quota availability

**Issue: Poor search results**
- Adjust chunking configuration
- Add relevant metadata for filtering
- Try different chunk sizes
- Verify documents indexed successfully

**Issue: Missing citations**
- Enable grounding in API request
- Check response for grounding_metadata
- Ensure store has indexed documents
- Verify model supports grounding

**Issue: Quota exceeded**
- Check current storage usage
- Delete unused stores
- Upgrade to higher tier
- Archive old documents

## Related Skills

- **embedding-specialist**: For custom embedding strategies
- **vector-db-engineer**: For alternative vector storage
- **langchain-specialist**: For LangChain integration
- **llamaindex-specialist**: For LlamaIndex integration

## References

- **Official Docs**: https://ai.google.dev/gemini-api/docs/file-search
- **Embeddings Guide**: https://ai.google.dev/gemini-api/docs/embeddings
- **API Keys**: https://aistudio.google.com/apikey
- **Filter Syntax**: https://google.aip.dev/160

## Version

**Skill Version:** 1.0.0
**Last Updated:** 2025-11-11
**Compatible With:** Gemini 2.5 Pro/Flash, Google GenAI SDK
