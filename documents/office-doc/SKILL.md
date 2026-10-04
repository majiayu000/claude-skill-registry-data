---
name: office-doc
description: Office document processing - PDF, Excel, CSV, Word, YAML, JSON, INI, TOML, XML
activation_keywords: [pdf, excel, csv, word, docx, yaml, json, ini, toml, xml, document, file, parse, spreadsheet]
execution_mode: client
---

# Office Doc Skill

All-in-one office document processing tool. Use `builtin_office_doc` tool with the following operations:

## Supported Formats

### 1. PDF
- `extract`: Extract text from PDF pages
- `metadata`: Get PDF info (pages, size, author)
- `search`: Search text in PDF

### 2. Excel / CSV
- `parse`: Parse spreadsheet data
- `info`: Show columns and types
- `stats`: Calculate statistics
- `head`/`tail`: Show rows
- `filter`: Filter by column value

### 3. Word (.docx)
- `extract`: Extract text from Word document

### 4. Config Files
- `yaml`/`yml`: Parse YAML to JSON
- `json`: Parse JSON, get keys
- `ini`: Parse INI sections
- `toml`: Parse TOML config
- `xml`: Parse XML elements

## Parameters

- `format`: File type (pdf, excel, csv, docx, yaml, json, ini, toml, xml)
- `operation`: Operation (parse, extract, info, stats, head, tail, filter, search, metadata)
- `content`: File content or data
- `file_path`: Path to file (for PDF)
- `page`: Page number (for PDF)
- `query`: Search query
- `column`: Column name
- `value`: Filter value
- `key`: Key path (dot notation)

## Examples

```
# Parse CSV
format: csv, content: "name,age\nAlice,30\nBob,25", operation: stats

# Extract from PDF
format: pdf, file_path: "/path/to/file.pdf", operation: extract, page: 1

# Parse YAML
format: yaml, content: "name: test\nvalue: 123", operation: to_json

# Filter CSV
format: csv, content: "name,age\nAlice,30\nBob,25", operation: filter, column: name, value: Alice
```