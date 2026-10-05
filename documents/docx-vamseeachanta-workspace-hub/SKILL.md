---
name: docx
description: Comprehensive Word document toolkit for reading, creating, and editing
  .docx files. Supports text extraction, document creation with python-docx, and tracked
  changes via redlining workflow. Use for legal, academic, or professional document
  manipulation.
type: reference
version: 1.1.0
last_updated: 2026-01-02
category: data
related_skills:
- pdf
- pptx
- document-inventory
capabilities: []
requires: []
tags: []
---

# Docx

## Overview

This skill enables comprehensive Word document operations through multiple specialized workflows for reading, creating, and editing documents.

## Quick Start

```python
from docx import Document

# Read existing document
doc = Document("document.docx")
for para in doc.paragraphs:
    print(para.text)

# Create new document
doc = Document()
doc.add_heading("My Title", level=0)
doc.add_paragraph("Hello, World!")
doc.save("output.docx")
```

## When to Use

- Extracting text and tables from Word documents
- Creating professional documents programmatically
- Generating reports from templates
- Bulk document processing and modification
- Legal document redlining with tracked changes
- Converting Word documents to other formats
- Adding headers, footers, and page numbers
- Inserting images and tables into documents

## Version History

- **1.1.0** (2026-01-02): Added Quick Start, When to Use, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with python-docx, pandoc integration, redlining workflow

## Sub-Skills

- [Execution Checklist](execution-checklist/SKILL.md)
- [Error Handling](error-handling/SKILL.md)
- [Metrics](metrics/SKILL.md)
- [Dependencies](dependencies/SKILL.md)

## Sub-Skills

- [Core Capabilities](core-capabilities/SKILL.md)
- [Extract Text with Pandoc (+2)](extract-text-with-pandoc/SKILL.md)
- [Basic Document Creation (+3)](basic-document-creation/SKILL.md)
- [Modify Existing Document (+1)](modify-existing-document/SKILL.md)
- [Step 1: Convert to Markdown (+4)](step-1-convert-to-markdown/SKILL.md)
- [Extract Metadata](extract-metadata/SKILL.md)
- [Working with Headers/Footers](working-with-headersfooters/SKILL.md)
