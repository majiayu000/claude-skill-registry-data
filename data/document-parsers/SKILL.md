---
name: document-parsers
description: Multi-format document parsing tools for PDF, DOCX, HTML, and Markdown with support for LlamaParse, Unstructured.io, PyPDF2, PDFPlumber, and python-docx. Use when parsing documents, extracting text from PDFs, processing Word documents, converting HTML to text, extracting tables from documents, building RAG pipelines, chunking documents, or when user mentions document parsing, PDF extraction, DOCX processing, table extraction, OCR, LlamaParse, Unstructured.io, or document ingestion.
allowed-tools: Read, Write, Bash, Grep, Glob, Edit
---

# Document Parsers

**Purpose:** Autonomously parse and extract content from multiple document formats (PDF, DOCX, HTML, Markdown) using industry-standard libraries and AI-powered parsing tools.

**Activation Triggers:**
- Building RAG (Retrieval-Augmented Generation) pipelines
- Extracting text, tables, or metadata from documents
- Processing large document collections
- Converting documents to structured formats
- Handling complex PDFs with tables and layouts
- OCR for scanned documents
- Chunking documents for vector embeddings
- Building document search systems

**Key Resources:**
- `scripts/setup-llamaparse.sh` - Install and configure LlamaParse (AI-powered parsing)
- `scripts/setup-unstructured.sh` - Install Unstructured.io library
- `scripts/parse-pdf.py` - Functional PDF parser with multiple backend options
- `scripts/parse-docx.py` - DOCX document parser
- `scripts/parse-html.py` - HTML to structured text parser
- `templates/multi-format-parser.py` - Universal document parser template
- `templates/table-extraction.py` - Specialized table extraction template
- `examples/parse-research-paper.py` - Research paper parsing with citations
- `examples/parse-legal-document.py` - Legal document parsing with sections

## Parser Comparison & Selection Guide

### 1. LlamaParse (AI-Powered Premium)

**Best For:**
- Complex PDFs with tables, charts, and mixed layouts
- Scanned documents requiring OCR
- Documents where accuracy is critical
- Multi-column layouts and scientific papers
- Financial reports and invoices

**Pros:**
- AI-powered layout understanding
- Excellent table extraction accuracy
- Built-in OCR support
- Handles complex formatting
- Structured output (Markdown/JSON)

**Cons:**
- Requires API key (paid service)
- API rate limits
- Network dependency
- Slower than local parsers

**Documentation:** https://docs.cloud.llamaindex.ai/llamaparse

**Setup:**
```bash
./scripts/setup-llamaparse.sh
```

**Usage Pattern:**
```python
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-...",
    result_type="markdown",  # or "text"
    language="en",
    verbose=True
)

documents = parser.load_data("document.pdf")
for doc in documents:
    print(doc.text)
```

### 2. Unstructured.io (Local Processing)

**Best For:**
- Batch processing many documents
- Multiple format support (PDF, DOCX, HTML, PPTX, Images)
- Local processing without API dependencies
- Structured element extraction
- Production RAG pipelines

**Pros:**
- Open-source and free
- Multi-format support
- Runs locally (no API keys)
- Good table detection
- Element-based chunking

**Cons:**
- Requires system dependencies (poppler, tesseract)
- Complex installation
- Less accurate than LlamaParse for complex layouts

**Documentation:** https://unstructured-io.github.io/unstructured/

**Setup:**
```bash
./scripts/setup-unstructured.sh
```

**Usage Pattern:**
```python
from unstructured.partition.auto import partition

elements = partition("document.pdf")
for element in elements:
    print(f"{element.category}: {element.text}")
```

### 3. PyPDF2 (Simple PDF Text Extraction)

**Best For:**
- Simple text-based PDFs
- Quick prototyping
- Metadata extraction
- PDF manipulation (merge, split)

**Pros:**
- Pure Python (no dependencies)
- Fast and lightweight
- Good for simple PDFs
- Active maintenance

**Cons:**
- Poor table extraction
- Struggles with complex layouts
- No OCR support
- Limited formatting preservation

**Documentation:** https://github.com/py-pdf/pypdf2

**Setup:**
```bash
pip install pypdf2
```

**Usage Pattern:**
```python
from PyPDF2 import PdfReader

reader = PdfReader("document.pdf")
for page in reader.pages:
    print(page.extract_text())
```

### 4. PDFPlumber (Advanced PDF Analysis)

**Best For:**
- Table extraction from PDFs
- PDF with tabular data
- Financial statements and reports
- Coordinate-based extraction

**Pros:**
- Excellent table extraction
- Visual debugging tools
- Coordinate-level control
- Metadata and layout info

**Cons:**
- Slower than PyPDF2
- Requires pdfminer.six dependency
- No OCR support

**Documentation:** https://github.com/jsvine/pdfplumber

**Setup:**
```bash
pip install pdfplumber
```

**Usage Pattern:**
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        text = page.extract_text()
```

### 5. python-docx (Word Documents)

**Best For:**
- Microsoft Word (.docx) documents
- Extracting paragraphs, tables, headers
- Document metadata
- Template-based document generation

**Pros:**
- Native DOCX support
- Preserves structure (paragraphs, tables, sections)
- Access to styles and formatting
- Can also write/modify DOCX

**Cons:**
- Only works with .docx (not .doc)
- Limited image extraction

**Documentation:** https://github.com/python-openxml/python-docx

**Setup:**
```bash
pip install python-docx
```

**Usage Pattern:**
```python
from docx import Document

doc = Document("document.docx")
for para in doc.paragraphs:
    print(para.text)
for table in doc.tables:
    for row in table.rows:
        print([cell.text for cell in row.cells])
```

## Decision Matrix

| Use Case | Recommended Parser | Alternative |
|----------|-------------------|-------------|
| Simple PDF text extraction | PyPDF2 | Unstructured |
| Complex PDFs with tables | LlamaParse | PDFPlumber |
| Scanned documents (OCR) | LlamaParse | Unstructured + Tesseract |
| Word documents (.docx) | python-docx | Unstructured |
| HTML to text | parse-html.py | Unstructured |
| Multi-format batch processing | Unstructured | Multi-format-parser |
| Table extraction | PDFPlumber | LlamaParse |
| Research papers | LlamaParse | Unstructured |
| Legal documents | LlamaParse | PDFPlumber |
| Production RAG pipeline | Unstructured | LlamaParse |

## Functional Scripts

### 1. Parse PDF (`scripts/parse-pdf.py`)

Command-line PDF parser supporting multiple backends:

```bash
# Using PyPDF2 (default)
python scripts/parse-pdf.py document.pdf

# Using PDFPlumber (better for tables)
python scripts/parse-pdf.py document.pdf --backend pdfplumber

# Using LlamaParse (AI-powered)
python scripts/parse-pdf.py document.pdf --backend llamaparse --api-key llx-...

# Output to file
python scripts/parse-pdf.py document.pdf --output output.txt

# Extract tables as JSON
python scripts/parse-pdf.py document.pdf --backend pdfplumber --tables-only --output tables.json
```

**Features:**
- Multiple backend support (PyPDF2, PDFPlumber, LlamaParse)
- Table extraction
- Metadata extraction
- Page range selection
- JSON/Text output formats

### 2. Parse DOCX (`scripts/parse-docx.py`)

Word document parser with structure preservation:

```bash
# Basic extraction
python scripts/parse-docx.py document.docx

# Extract with structure
python scripts/parse-docx.py document.docx --preserve-structure

# Extract tables only
python scripts/parse-docx.py document.docx --tables-only

# Output as JSON
python scripts/parse-docx.py document.docx --output output.json --format json
```

**Features:**
- Paragraph extraction with styles
- Table extraction
- Header/footer extraction
- Metadata (author, created date, etc.)
- Structured JSON output

### 3. Parse HTML (`scripts/parse-html.py`)

HTML to clean text converter:

```bash
# Basic HTML parsing
python scripts/parse-html.py document.html

# From URL
python scripts/parse-html.py https://example.com/article

# Preserve links
python scripts/parse-html.py document.html --preserve-links

# Extract specific selector
python scripts/parse-html.py document.html --selector "article.content"
```

**Features:**
- Clean text extraction (removes scripts, styles)
- Link preservation
- CSS selector support
- URL fetching
- Markdown output option

## Templates

### Multi-Format Parser (`templates/multi-format-parser.py`)

Universal parser handling multiple formats with automatic format detection:

```python
from multi_format_parser import MultiFormatParser

parser = MultiFormatParser(
    llamaparse_api_key="llx-...",  # Optional
    use_ocr=True,
    chunk_size=1000
)

# Automatic format detection
result = parser.parse_file("document.pdf")
print(result.text)
print(result.metadata)
print(result.tables)

# Batch processing
results = parser.parse_directory("./documents/")
for filename, result in results.items():
    print(f"{filename}: {len(result.text)} characters")
```

**Supports:**
- PDF, DOCX, HTML, Markdown, TXT
- Automatic chunking for RAG
- Metadata extraction
- Table extraction across all formats
- Error handling and fallbacks

### Table Extraction (`templates/table-extraction.py`)

Specialized table extraction with multiple strategies:

```python
from table_extraction import TableExtractor

extractor = TableExtractor(
    prefer_llamaparse=True,
    fallback_to_pdfplumber=True
)

# Extract all tables from document
tables = extractor.extract_tables("financial_report.pdf")

for i, table in enumerate(tables):
    print(f"Table {i + 1}:")
    print(table.to_markdown())  # or .to_csv(), .to_json()
    print(f"Confidence: {table.confidence}")
```

**Features:**
- Multiple extraction strategies
- Automatic fallback
- Table validation
- Format conversion (CSV, JSON, Markdown, DataFrame)
- Confidence scoring

## Examples

### Research Paper Parsing (`examples/parse-research-paper.py`)

Complete example for parsing academic papers:

```python
# Extracts title, abstract, sections, citations, tables, figures
python examples/parse-research-paper.py paper.pdf --output paper.json
```

**Extracts:**
- Title and authors
- Abstract
- Section structure (Introduction, Methods, Results, etc.)
- Citations and references
- Tables and figures with captions
- Metadata (DOI, publication date, journal)

### Legal Document Parsing (`examples/parse-legal-document.py`)

Specialized parser for legal documents:

```python
# Extracts clauses, sections, definitions, parties
python examples/parse-legal-document.py contract.pdf --output contract.json
```

**Extracts:**
- Document type (contract, agreement, etc.)
- Parties involved
- Definitions section
- Numbered clauses and sections
- Signature blocks
- Dates and deadlines

## RAG Pipeline Integration

### Document Chunking for Embeddings

```python
from multi_format_parser import MultiFormatParser

parser = MultiFormatParser(chunk_size=512, chunk_overlap=50)
result = parser.parse_file("document.pdf")

# Chunks ready for embedding
for chunk in result.chunks:
    print(f"Chunk {chunk.id}: {chunk.text[:100]}...")
    print(f"Metadata: {chunk.metadata}")
    # Send to embedding model
```

### Batch Processing Pipeline

```python
import glob
from multi_format_parser import MultiFormatParser

parser = MultiFormatParser()

# Process all documents in directory
for filepath in glob.glob("./documents/**/*", recursive=True):
    try:
        result = parser.parse_file(filepath)
        # Store in vector database
        store_embeddings(result.chunks)
        print(f"✓ Processed {filepath}")
    except Exception as e:
        print(f"✗ Failed {filepath}: {e}")
```

## Best Practices

**Parser Selection:**
- Start with PyPDF2 for simple PDFs, upgrade if needed
- Use LlamaParse for complex layouts (budget permitting)
- Use Unstructured for multi-format production systems
- Use PDFPlumber specifically for table extraction

**Performance:**
- Cache parsed results to avoid re-processing
- Use batch processing for multiple documents
- Consider async processing for large collections
- Monitor API rate limits for LlamaParse

**Accuracy:**
- Validate table extraction results
- Implement fallback strategies
- Log parsing errors for debugging
- Use confidence scores when available

**RAG Optimization:**
- Chunk size: 512-1024 tokens for embeddings
- Overlap: 10-20% for context preservation
- Preserve metadata (page numbers, sections) for retrieval
- Clean extracted text (remove headers/footers)

## Troubleshooting

**PyPDF2 returns garbled text:**
- Try PDFPlumber or LlamaParse
- PDF may have non-standard encoding
- Check if PDF is scanned (needs OCR)

**Unstructured installation fails:**
- Install system dependencies: `sudo apt-get install poppler-utils tesseract-ocr`
- On macOS: `brew install poppler tesseract`

**LlamaParse API errors:**
- Verify API key is correct
- Check rate limits in dashboard
- Ensure document size is within limits

**Table extraction misses columns:**
- Try different parser (PDFPlumber vs LlamaParse)
- Adjust table detection settings
- Validate table structure manually

**DOCX parsing fails:**
- Ensure file is .docx not .doc
- Check file is not corrupted
- Try converting to .docx with LibreOffice

## Dependencies

**Core:**
```bash
pip install pypdf2 pdfplumber python-docx beautifulsoup4 lxml markdown
```

**Optional (Unstructured):**
```bash
pip install unstructured[local-inference]
sudo apt-get install poppler-utils tesseract-ocr  # Linux
brew install poppler tesseract  # macOS
```

**Optional (LlamaParse):**
```bash
pip install llama-parse
# Requires API key from https://cloud.llamaindex.ai
```

---

**Supported Formats:** PDF, DOCX, HTML, Markdown, TXT
**Parsers:** LlamaParse, Unstructured.io, PyPDF2, PDFPlumber, python-docx
**Version:** 1.0.0
