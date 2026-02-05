---
name: pdf-reader
description: Extract text, tables, and images from PDF files using pdfplumber and PyMuPDF. Use when analyzing PDF documents, brand materials, reports, or any content that requires structured extraction from PDF format. Supports table detection, layout preservation, and high-quality image extraction.
---

# PDF Reader

Extract comprehensive content from PDF files including text, tables, images, and metadata using industry-standard Python libraries.

## When to Use This Skill

Use this skill when:
- Analyzing brand documents, design briefs, or company materials in PDF format
- Extracting structured data from reports, invoices, or forms with tables
- Retrieving images, logos, or graphics embedded in PDFs
- Converting PDF content into markdown or structured formats for further processing
- Investigating PDF metadata, page layouts, or document structure

## How It Works

This skill combines two powerful libraries:
1. **pdfplumber** - Excels at text extraction with layout preservation and table detection
2. **PyMuPDF** - Provides fast image extraction and comprehensive metadata access

## Quick Start

### Install Dependencies

```bash
pip install pdfplumber pymupdf pillow
```

### Extract from PDF

```bash
python scripts/extract_pdf.py <path/to/document.pdf> --output-dir ./output
```

## Output Structure

The script creates the following output:

```
output/
├── extracted_text.md       # All text content with page numbers
├── extracted_tables.json   # Structured table data
├── metadata.json           # PDF metadata and page info
└── images/                 # Extracted images
    ├── page_1_image_1.png
    ├── page_2_image_1.jpeg
    └── ...
```

## Usage in Claude Code

When a user provides a PDF file for analysis:

1. **Check dependencies**: Verify pdfplumber and PyMuPDF are installed
2. **Run extraction script**: Execute `scripts/extract_pdf.py` with the PDF path
3. **Analyze output**: Read the generated markdown and JSON files
4. **Present findings**: Summarize key content, tables, and images found

Example workflow:

```bash
# Step 1: Extract PDF content
python scripts/extract_pdf.py "brand_document.pdf" --output-dir ./brand_analysis

# Step 2: Read extracted text
cat ./brand_analysis/extracted_text.md

# Step 3: Analyze tables
cat ./brand_analysis/extracted_tables.json

# Step 4: Check images
ls ./brand_analysis/images/
```

## Advanced Features

### Text Extraction Options

The script uses `layout=True` to preserve formatting and spacing, which is crucial for:
- Maintaining column layouts
- Preserving visual hierarchy
- Keeping address and contact information structured

### Table Detection

pdfplumber automatically detects tables using:
- Line-based strategies for ruled tables
- Text alignment strategies for borderless tables
- Configurable tolerance settings for complex layouts

### Image Quality

PyMuPDF extracts images in their original format (JPEG, PNG) without re-encoding, preserving:
- Original resolution and quality
- Color profiles and metadata
- Transparency and alpha channels

## Troubleshooting

### Missing Dependencies

If the script fails with import errors:
```bash
pip install --upgrade pdfplumber pymupdf pillow
```

### Encrypted PDFs

For password-protected PDFs, use PyMuPDF's authentication:
```python
import pymupdf
doc = pymupdf.open("encrypted.pdf")
doc.authenticate("password")
```

### Large Files

For very large PDFs (>100MB), process pages in batches to manage memory usage.

## Technical Details

### Library Comparison

| Feature | pdfplumber | PyMuPDF |
|---------|-----------|---------|
| Text extraction | ⭐⭐⭐ (Best layout preservation) | ⭐⭐ (Fast, good quality) |
| Table detection | ⭐⭐⭐ (Excellent) | ⭐ (Basic) |
| Image extraction | ⭐ (Basic) | ⭐⭐⭐ (Best performance) |
| Speed | ⭐⭐ (Moderate) | ⭐⭐⭐ (Very fast) |
| Memory usage | ⭐⭐ (Higher) | ⭐⭐⭐ (Lower) |

### Why Both Libraries?

Using both libraries provides optimal results:
- **pdfplumber** for text and tables (superior accuracy)
- **PyMuPDF** for images and metadata (superior performance)

This combination ensures comprehensive extraction without compromise.

## Examples

### Brand Document Analysis

```bash
python scripts/extract_pdf.py "company_brand_guidelines.pdf" --output-dir ./brand_analysis
```

Expected output:
- Brand values and mission statements (text)
- Color palette tables (tables)
- Logo variations (images)
- Document metadata (metadata)

### Design Brief Extraction

```bash
python scripts/extract_pdf.py "design_brief.pdf" --output-dir ./brief_analysis
```

Expected output:
- Project requirements (text)
- Timeline and milestones (tables)
- Reference images (images)
- Client information (metadata)

## Integration Tips

### With Logo Design Workflows

After extracting brand guidelines:
1. Review extracted text for brand keywords and values
2. Analyze color palette tables for official brand colors
3. Examine logo images for existing design elements
4. Use findings to inform new logo design strategy

### With Research Workflows

After extracting research documents:
1. Convert extracted tables to structured data
2. Process images for visual analysis
3. Generate summary reports from text content
4. Cross-reference metadata for document versioning
