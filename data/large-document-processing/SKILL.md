---
name: large-document-processing
description: Process large documents (200+ pages) with structure preservation, intelligent parsing, and memory-efficient handling. Use when working with complex formatted documents, multi-level hierarchies, or when you need to extract structured data from large files like PDFs, DOCX, or text files.
---

# Large Document Processing

## Overview

A comprehensive skill for processing large documents (200+ pages) with structure preservation, intelligent parsing, and memory-efficient handling. Designed for documents with complex formatting, hierarchical structures, and multi-level indentation.

## Capabilities

- **Multi-format Support**: DOCX, PDF, and text files
- **Structure Preservation**: Maintains document hierarchy, indentation, and formatting
- **Memory Efficiency**: Chunked processing to handle very large documents
- **Intelligent Parsing**: Recognizes headings, lists, dictionary entries, and semantic boundaries
- **Progress Tracking**: Real-time processing status and error recovery
- **Metadata Extraction**: Comprehensive document analysis and statistics

## Core Components

### 1. Advanced Document Parser

Parse complex document structures while preserving formatting and hierarchy.

**Key Features**:

- Hierarchical structure detection (levels 1-10)
- Formatting preservation (bold, italic, fonts, sizes)
- Page-by-page processing for memory efficiency
- Intelligent content classification
- Multi-language support with accent character handling

### 2. Implementation Pattern

```python
from .large_document_processor import LargeDocumentProcessor, ProcessingConfig

# Configure processing
config = ProcessingConfig(
    chunk_size_pages=50,
    parallel_workers=4,
    preserve_formatting=True
)

# Initialize processor
processor = LargeDocumentProcessor(config)

# Process document
results = processor.process_large_document(
    input_file="large_document.docx",
    output_dir="output/processed"
)
```

### 3. Intelligent Text Chunking

```python
from .intelligent_chunker import IntelligentTextChunker, ChunkType

chunker = IntelligentTextChunker(
    max_chunk_size=1024,
    overlap_ratio=0.15,
    preserve_sentences=True
)

chunks = chunker.chunk_document(text, ChunkType.SEMANTIC)
```

## Output Formats

- **Structured JSON**: Complete document hierarchy and metadata
- **Plain text**: Clean extracted text with optional formatting markers
- **Chunked data**: AI-ready text segments with overlap and metadata
- **Statistics report**: Processing metrics and quality analysis

## Best Practices

1. **Memory Management**: Use chunked processing for documents >100MB
2. **Parallel Processing**: Leverage multiple workers for batch operations
3. **Structure Validation**: Verify hierarchy detection accuracy
4. **Progress Tracking**: Provide user feedback for long-running operations

## Dependencies

- `python-docx`: DOCX file processing
- `PyMuPDF`: Advanced PDF processing
- `Pillow`: Image processing for embedded content
- `pathlib`: Cross-platform path handling
