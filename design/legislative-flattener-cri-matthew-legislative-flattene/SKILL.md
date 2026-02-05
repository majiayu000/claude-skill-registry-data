---
name: legislative-flattener
description: Converts hierarchical legislative text from Word documents into a flat list of requirements. Use when processing regulatory documents, compliance frameworks, or legal text that needs to be extracted into individual, numbered requirements for analysis or mapping.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Legislative Text Flattener

This skill processes Word documents (DOCX) containing legislative or regulatory text and converts hierarchical structures into a flat, numbered list of discrete requirements or provisions.

## When to Use This Skill

Activate this skill when the user wants to:
- Flatten hierarchical legislative or regulatory text
- Extract requirements from compliance frameworks
- Convert nested sections/subsections into a linear list
- Prepare legislative text for requirement mapping
- Process Word documents containing legal or regulatory content

## Quick Start

Install required dependencies:
```bash
pip install python-docx openpyxl
```

Basic usage (outputs formatted XLSX by default):
```bash
python flattener_utility.py input.docx output.xlsx
```

Or specify format explicitly:
```bash
python flattener_utility.py input.docx output.xlsx --format xlsx
python flattener_utility.py input.docx output.csv --format csv
python flattener_utility.py input.docx output.json --format json
```

## Processing Instructions

### 1. Input Analysis

First, understand the input document structure:
- Read the DOCX file (use python-docx library or convert to text)
- Identify the hierarchical structure (sections, subsections, paragraphs, sub-paragraphs)
- Detect numbering schemes (1.2.3, (a)(b)(c), Article-Section-Paragraph, etc.)
- Note any special formatting or emphasis (bold, italics, SHALL/MUST keywords)

### 2. Extraction Process

Extract content while preserving context:
- Each discrete requirement or provision becomes a separate item
- Maintain parent context for nested items
- Preserve the original numbering/reference system
- Extract complete sentences or logical requirement units
- Identify normative language (shall, must, should, may)

### 3. Flattening Strategy

Convert hierarchy to flat structure:
- Assign sequential flat numbering (1, 2, 3...)
- Include original reference in metadata (e.g., "Section 500.02(b)(3)")
- Preserve full context path for each item
- Handle multi-level lists and nested requirements
- Maintain logical groupings where appropriate

### 4. Output Format

Generate a structured flat list with these fields for each requirement:

```
Flat ID: [Sequential number]
Original Reference: [Original section/subsection identifier]
Context Path: [Full hierarchical path, e.g., "Article 5 > Section 2 > Paragraph b"]
Requirement Type: [Mandate/Prohibition/Permission/Definition]
Normative Level: [SHALL/MUST/SHOULD/MAY/INFORMATIVE]
Text: [Full requirement text]
Keywords: [Extracted key concepts or compliance areas]
---
```

### 5. Implementation Approach

Use this workflow:

```python
# Install required library if needed
# pip install python-docx

from docx import Document
import re

def flatten_legislative_text(docx_path):
    """
    Flattens hierarchical legislative text from DOCX.
    Returns a list of flattened requirements.
    """
    doc = Document(docx_path)
    flattened = []
    flat_id = 1
    context_stack = []

    for paragraph in doc.paragraphs:
        # Skip empty paragraphs
        if not paragraph.text.strip():
            continue

        # Detect hierarchy level (by style or numbering)
        level = detect_level(paragraph)
        original_ref = extract_reference(paragraph)

        # Update context stack
        update_context(context_stack, level, paragraph.text)

        # Extract if it's a requirement (not just a heading)
        if is_requirement(paragraph):
            item = {
                'flat_id': flat_id,
                'original_ref': original_ref,
                'context_path': ' > '.join(context_stack),
                'requirement_type': classify_requirement(paragraph.text),
                'normative_level': extract_normative_level(paragraph.text),
                'text': clean_text(paragraph.text),
                'keywords': extract_keywords(paragraph.text)
            }
            flattened.append(item)
            flat_id += 1

    return flattened
```

### 6. Output Options

Provide results in user's preferred format:
- **XLSX (Excel)**: Formatted Excel workbook with styled headers, auto-filter, frozen panes, and optimized column widths (default and recommended)
- **CSV**: Simple tabular format with all fields as columns
- **JSON**: Structured data for programmatic use
- **Markdown**: Human-readable with clear section breaks
- **Database insert**: SQL statements or database-ready format

### 7. Quality Checks

Validate the flattening:
- Ensure no requirements are lost or duplicated
- Verify context paths are complete and accurate
- Check that normative language is correctly identified
- Confirm original references are preserved
- Review that similar requirements are consistently formatted

## Example Output (Markdown Format)

```markdown
## Flattened Requirements

### Requirement 1
- **Flat ID**: 1
- **Original Reference**: Section 500.02(a)
- **Context Path**: Part 500 > Section 500.02 > Paragraph (a)
- **Requirement Type**: Mandate
- **Normative Level**: SHALL
- **Text**: Each Covered Entity shall maintain a cybersecurity program designed to protect the confidentiality, integrity and availability of the Covered Entity's Information Systems.
- **Keywords**: cybersecurity program, confidentiality, integrity, availability, Information Systems

---

### Requirement 2
- **Flat ID**: 2
- **Original Reference**: Section 500.02(b)
- **Context Path**: Part 500 > Section 500.02 > Paragraph (b)
- **Requirement Type**: Mandate
- **Normative Level**: SHALL
- **Text**: The cybersecurity program shall be based on the Covered Entity's Risk Assessment and designed to perform the following core cybersecurity functions...
- **Keywords**: Risk Assessment, core cybersecurity functions

---
```

## Notes

- **XLSX output is recommended** for most use cases as it provides:
  - Professional formatting with styled headers
  - Auto-filter for easy data exploration
  - Frozen header row for scrolling large datasets
  - Optimized column widths for readability
  - Text wrapping for long requirement text
- Handle tables within documents by processing each cell as potential requirement text
- Preserve cross-references between sections where they exist
- Flag ambiguous or incomplete requirements for manual review
- Support batch processing of multiple documents
- Maintain a processing log of any items that couldn't be automatically classified

## XLSX Features

The XLSX export includes:
- **Header styling**: Bold white text on blue background
- **Auto-filter**: Filter requirements by any column
- **Frozen panes**: Header row stays visible when scrolling
- **Column widths**: Optimized for each field type (10-60 characters)
- **Text wrapping**: Long text automatically wraps for readability
- **Borders**: Clean grid lines for professional appearance

## Supporting Files

See `examples.md` for sample input/output pairs and `template.md` for customizable output templates.
