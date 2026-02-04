---
name: bookstrap-ingest
description: Load research corpus into the database by processing files, directories, or URLs through semantic chunking, embedding generation, entity extraction, and relationship building
argument-hint: [file-paths | directories | URLs]
disable-model-invocation: true
allowed-tools: Bash, Read, WebFetch
---

# /bookstrap-ingest - Load Research Corpus

Load initial research materials into the Bookstrap database for use during writing.

## Purpose

Ingest source documents into the database to build the research corpus. This command processes multiple file types (PDF, markdown, HTML, plain text), generates embeddings for semantic search, extracts entities (characters, locations, events, concepts), builds relationships between entities, and constructs the knowledge timeline.

## Input Arguments

Accept one or more of the following:
- **File paths**: Individual files to ingest (e.g., `./research/soe-training.pdf`)
- **Directories**: Recursively process all files in a directory (e.g., `./research/`)
- **URLs**: Web pages to fetch and ingest (e.g., `https://example.com/article.html`)

Multiple sources can be provided in a single invocation:
```
/bookstrap-ingest ./research/documents/ https://example.com/article.html ./notes.md
```

## Supported File Types

| File Type | Extension | Processing Method |
|-----------|-----------|-------------------|
| PDF | `.pdf` | Extract text via `ingest-file.py` |
| Markdown | `.md`, `.markdown` | Read directly |
| HTML | `.html`, `.htm` | Parse and extract text content |
| Plain Text | `.txt` | Read directly |

## Processing Workflow

For each source provided:

### 1. Source Collection
- Parse arguments to identify file paths, directories, and URLs
- If directory: recursively find all supported files
- If URL: fetch content using WebFetch
- Track all sources for batch processing

### 2. File Ingestion
For each file, execute the ingestion pipeline:

```bash
python scripts/ingest-file.py <file-path>
```

The `ingest-file.py` script handles:
- **File reading**: Load content from supported formats
- **Semantic chunking**: Use LLM to identify natural breakpoints (paragraph boundaries, topic shifts, scene changes) rather than fixed token windows
- **Embedding generation**: Call configured embedding provider (Gemini, OpenAI, Ollama, LM Studio) via `scripts/generate-embedding.py`
- **Entity extraction**: Use LLM to extract characters, locations, events, concepts with context via `scripts/extract-entities.py`
- **Database storage**: Store source, chunks, embeddings, and entities in SurrealDB

### 3. Relationship Building
After entity extraction, automatically create graph relationships:
- Link sources to extracted concepts (`source->supports->concept`)
- Link events in chronological order (`event->precedes->event`, `event->follows->event`)
- Link entities mentioned together (`character->knows->character`, `concept->related_to->concept`)

### 4. Timeline Construction
Order events by:
- Extracted dates (if available)
- Sequence numbers from document structure
- Contextual ordering from content analysis

### 5. Metadata Recording
Store ingestion metadata for each source:
```surql
CREATE source SET
  title = $title,
  content = $content,
  embedding = $embedding_vector,
  url = $url,
  source_type = $source_type,  -- 'primary', 'secondary', 'web'
  reliability = $reliability,   -- 'high', 'medium', 'low'
  ingested_at = time::now(),
  ingested_during = 'bootstrap'
;
```

## Statistics Reporting

After ingestion completes, report:

```
INGESTION COMPLETE
==================

SOURCES PROCESSED: 15 files, 3 URLs
  - PDF: 8 files
  - Markdown: 5 files
  - HTML (web): 3 URLs
  - Plain Text: 2 files

ENTITIES EXTRACTED: 247 total
  - Characters: 34
  - Locations: 52
  - Events: 123
  - Concepts: 38

RELATIONSHIPS CREATED: 412 edges
  - source->supports->concept: 156
  - event->precedes->event: 98
  - event->follows->event: 98
  - character->knows->character: 24
  - concept->related_to->concept: 36

EMBEDDINGS GENERATED: 347 vectors
  - Sources: 15
  - Chunks: 285
  - Entities: 47

TIMELINE ENTRIES: 123 events ordered chronologically

STORAGE
-------
Database: bookstrap.my_book
Namespace: bookstrap
Total size: 12.4 MB
```

## Error Handling

Handle common ingestion errors gracefully:

| Error | Recovery |
|-------|----------|
| File not found | Skip and report, continue with remaining files |
| Unsupported format | Warn user, skip file |
| URL fetch timeout | Retry once, then skip if still fails |
| Embedding API error | Retry with exponential backoff, fail if persistent |
| Database connection error | Abort ingestion, report last successful file |

## Configuration

Ingestion behavior is controlled by `bookstrap.config.json`:

```json
{
  "embeddings": {
    "provider": "gemini",
    "model": "text-embedding-004",
    "dimensions": 768
  },
  "extraction": {
    "provider": "llm",
    "chunking": {
      "strategy": "semantic",
      "max_tokens": 1024,
      "overlap": 128
    }
  },
  "surrealdb": {
    "host": "localhost",
    "port": 2665,
    "namespace": "bookstrap",
    "database": "my_book"
  }
}
```

## Implementation Notes

- **Batch processing**: Process files sequentially to avoid overwhelming the embedding API
- **Rate limiting**: Respect embedding provider rate limits (configured in `bookstrap.config.json`)
- **Idempotency**: Re-ingesting the same file updates existing records rather than creating duplicates (match on title + content hash)
- **Progress tracking**: Log each file as it's processed for visibility during long ingestions
- **Database connection**: Verify SurrealDB is running before starting ingestion

## Example Usage

```bash
# Ingest a single file
/bookstrap-ingest ./research/soe-training-manual.pdf

# Ingest an entire directory
/bookstrap-ingest ./research/primary-sources/

# Ingest multiple sources at once
/bookstrap-ingest ./research/ https://en.wikipedia.org/wiki/SOE https://example.com/lyon-resistance.html

# Ingest web content only
/bookstrap-ingest https://archive.org/details/soe-field-manual
```

## Pre-requisites

Before running `/bookstrap-ingest`:

1. **BRD created**: `/bookstrap-init` must have been run to create the Book Requirements Document
2. **SurrealDB running**: Database must be accessible (started via `docker-compose up -d` or `./scripts/start-surreal.sh`)
3. **Schema initialized**: Database schema must be loaded via `./scripts/init-schema.sh`
4. **API keys configured**: Embedding provider API key must be set in environment variables (e.g., `GEMINI_API_KEY`)

## Related Commands

- `/bookstrap-init` - Create BRD and initialize database
- `/bookstrap-plan-research` - Identify knowledge gaps after ingestion
- `/bookstrap-research` - Fill gaps with targeted web research
- `/bookstrap-status` - View corpus statistics and coverage

## Supporting Scripts

| Script | Purpose |
|--------|---------|
| `scripts/ingest-file.py` | Main ingestion pipeline for file processing |
| `scripts/generate-embedding.py` | Multi-provider embedding generation |
| `scripts/extract-entities.py` | LLM-based entity extraction with context |
| `scripts/chunk.py` | Semantic chunking using LLM |

See individual script documentation for configuration options and advanced usage.
