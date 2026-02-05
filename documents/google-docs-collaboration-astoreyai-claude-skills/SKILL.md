---
name: google-docs-collaboration
description: Manages Google Docs, Sheets, and Slides through the Docs, Sheets, and Slides APIs. Create, read, and edit documents, spreadsheets, and presentations programmatically. Format content, manage collaboration, extract data, and automate document workflows. Use when working with Google Workspace documents, editing content, extracting data, or automating document creation.
---

# Google Docs Collaboration

Comprehensive Google Workspace document integration enabling programmatic creation, editing, and management of Docs, Sheets, and Slides through their respective APIs.

## Quick Start

When asked to work with Google Docs, Sheets, or Slides:

1. **Authenticate**: Set up OAuth2 credentials (one-time setup)
2. **Create documents**: Generate Docs, Sheets, or Slides
3. **Read content**: Extract text, data, or presentation content
4. **Edit documents**: Update content programmatically
5. **Format**: Apply styling and formatting
6. **Collaborate**: Manage sharing and comments

## Prerequisites

### One-Time Setup

**1. Enable APIs:**
```bash
# Visit Google Cloud Console
# https://console.cloud.google.com/

# Enable these APIs:
# - Google Docs API
# - Google Sheets API
# - Google Slides API
# - Google Drive API (for file operations)
```

**2. Create OAuth2 Credentials:**
```bash
# In Google Cloud Console:
# APIs & Services > Credentials > Create Credentials > OAuth client ID
# Application type: Desktop app
# Download credentials as credentials.json
```

**3. Install Dependencies:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client --break-system-packages
```

**4. Initial Authentication:**
```bash
python scripts/authenticate.py
# Opens browser for Google sign-in
# Saves token.json for future use
```

See [reference/setup-guide.md](reference/setup-guide.md) for detailed setup.

## Google Docs Operations

### Create Documents

**Create blank Doc:**
```bash
# New document
python scripts/create_doc.py --title "Project Proposal"

# With initial content
python scripts/create_doc.py \
  --title "Meeting Notes" \
  --content-file template.txt
```

**Create from template:**
```bash
# Copy template and customize
python scripts/create_from_template.py \
  --template-id TEMPLATE_DOC_ID \
  --title "Q4 Report" \
  --replacements "{{date}}:2025-01-20,{{author}}:John Smith"
```

### Read Documents

**Get document content:**
```bash
# Read as text
python scripts/read_doc.py --doc-id DOC_ID

# Get structured content
python scripts/get_doc_structure.py --doc-id DOC_ID --output doc.json

# Export as different format
python scripts/export_doc.py --doc-id DOC_ID --format pdf --output report.pdf
python scripts/export_doc.py --doc-id DOC_ID --format docx --output report.docx
```

**Extract specific elements:**
```bash
# Get headings only
python scripts/extract_headings.py --doc-id DOC_ID

# Get tables
python scripts/extract_tables.py --doc-id DOC_ID

# Get images
python scripts/extract_images.py --doc-id DOC_ID --output ./images/
```

### Edit Documents

**Append content:**
```bash
# Add text to end
python scripts/append_doc.py \
  --doc-id DOC_ID \
  --text "New paragraph content"

# Add formatted content
python scripts/append_doc.py \
  --doc-id DOC_ID \
  --content-file content.json
```

**Insert content:**
```bash
# Insert at specific position
python scripts/insert_text.py \
  --doc-id DOC_ID \
  --index 100 \
  --text "Inserted text"

# Insert before/after heading
python scripts/insert_after_heading.py \
  --doc-id DOC_ID \
  --heading "Introduction" \
  --text "New content"
```

**Replace content:**
```bash
# Find and replace
python scripts/replace_text.py \
  --doc-id DOC_ID \
  --find "old text" \
  --replace "new text"

# Replace with regex
python scripts/replace_text.py \
  --doc-id DOC_ID \
  --pattern "\d{4}-\d{2}-\d{2}" \
  --replace "2025-01-20"
```

**Delete content:**
```bash
# Delete range
python scripts/delete_range.py \
  --doc-id DOC_ID \
  --start-index 100 \
  --end-index 200
```

### Format Documents

**Apply text formatting:**
```bash
# Bold text
python scripts/format_text.py \
  --doc-id DOC_ID \
  --range 10:50 \
  --bold

# Multiple formats
python scripts/format_text.py \
  --doc-id DOC_ID \
  --range 10:50 \
  --bold --italic --underline \
  --font-size 14 \
  --font-family "Arial"
```

**Apply paragraph formatting:**
```bash
# Set heading style
python scripts/set_paragraph_style.py \
  --doc-id DOC_ID \
  --range 0:20 \
  --style "HEADING_1"

# Adjust alignment and spacing
python scripts/format_paragraph.py \
  --doc-id DOC_ID \
  --range 50:100 \
  --alignment "CENTER" \
  --line-spacing 1.5
```

**Insert elements:**
```bash
# Insert image
python scripts/insert_image.py \
  --doc-id DOC_ID \
  --index 100 \
  --image-url "https://example.com/image.jpg"

# Insert table
python scripts/insert_table.py \
  --doc-id DOC_ID \
  --index 100 \
  --rows 3 \
  --columns 4

# Insert page break
python scripts/insert_page_break.py \
  --doc-id DOC_ID \
  --index 500
```

## Google Sheets Operations

### Create Sheets

**Create blank Sheet:**
```bash
# New spreadsheet
python scripts/create_sheet.py --title "Budget 2025"

# With initial data
python scripts/create_sheet.py \
  --title "Sales Data" \
  --data data.csv
```

**Create with structure:**
```bash
# Multiple sheets with headers
python scripts/create_sheet.py \
  --title "Project Tracker" \
  --sheets "Tasks,Timeline,Budget" \
  --headers "Task,Owner,Status,Due Date"
```

### Read Sheets

**Get data:**
```bash
# Read range
python scripts/read_sheet.py \
  --sheet-id SHEET_ID \
  --range "Sheet1!A1:D10"

# Read entire sheet
python scripts/read_sheet.py \
  --sheet-id SHEET_ID \
  --sheet "Sheet1"

# Export as CSV
python scripts/export_sheet.py \
  --sheet-id SHEET_ID \
  --format csv \
  --output data.csv
```

**Get sheet properties:**
```bash
# Get sheet metadata
python scripts/get_sheet_info.py --sheet-id SHEET_ID

# List all sheets
python scripts/list_sheets.py --sheet-id SHEET_ID
```

### Edit Sheets

**Update cells:**
```bash
# Update single cell
python scripts/update_cell.py \
  --sheet-id SHEET_ID \
  --cell "A1" \
  --value "New Value"

# Update range
python scripts/update_range.py \
  --sheet-id SHEET_ID \
  --range "A1:B10" \
  --values data.csv

# Append rows
python scripts/append_rows.py \
  --sheet-id SHEET_ID \
  --sheet "Sheet1" \
  --values new_data.csv
```

**Formulas:**
```bash
# Add formula
python scripts/set_formula.py \
  --sheet-id SHEET_ID \
  --cell "D2" \
  --formula "=SUM(A2:C2)"

# Copy formula down column
python scripts/fill_formula.py \
  --sheet-id SHEET_ID \
  --range "D2:D100" \
  --formula "=SUM(A2:C2)"
```

**Formatting:**
```bash
# Format cells
python scripts/format_cells.py \
  --sheet-id SHEET_ID \
  --range "A1:D1" \
  --bold \
  --background-color "blue" \
  --text-color "white"

# Number format
python scripts/set_number_format.py \
  --sheet-id SHEET_ID \
  --range "B2:B100" \
  --format "CURRENCY"
```

**Sheet structure:**
```bash
# Add sheet
python scripts/add_sheet.py \
  --sheet-id SHEET_ID \
  --title "New Sheet"

# Delete sheet
python scripts/delete_sheet.py \
  --sheet-id SHEET_ID \
  --sheet-name "Old Sheet"

# Rename sheet
python scripts/rename_sheet.py \
  --sheet-id SHEET_ID \
  --old-name "Sheet1" \
  --new-name "Data"
```

**Sort and filter:**
```bash
# Sort range
python scripts/sort_range.py \
  --sheet-id SHEET_ID \
  --range "A1:D100" \
  --sort-by-column 1 \
  --ascending

# Create filter
python scripts/create_filter.py \
  --sheet-id SHEET_ID \
  --range "A1:D100"
```

## Google Slides Operations

### Create Presentations

**Create blank presentation:**
```bash
# New presentation
python scripts/create_slides.py --title "Q4 Review"

# From template
python scripts/create_from_template.py \
  --template-id TEMPLATE_ID \
  --title "Sales Presentation"
```

### Read Presentations

**Get presentation content:**
```bash
# Read all slides
python scripts/read_slides.py --presentation-id PRES_ID

# Get specific slide
python scripts/get_slide.py \
  --presentation-id PRES_ID \
  --slide-index 0

# Export as PDF
python scripts/export_slides.py \
  --presentation-id PRES_ID \
  --format pdf \
  --output presentation.pdf
```

### Edit Presentations

**Add slides:**
```bash
# Add blank slide
python scripts/add_slide.py \
  --presentation-id PRES_ID \
  --layout "TITLE_AND_BODY" \
  --index 1

# Add slide with content
python scripts/add_slide.py \
  --presentation-id PRES_ID \
  --layout "TITLE_AND_BODY" \
  --title "Key Points" \
  --body "Point 1\nPoint 2\nPoint 3"
```

**Update slides:**
```bash
# Update text
python scripts/update_slide_text.py \
  --presentation-id PRES_ID \
  --slide-index 0 \
  --find "{{title}}" \
  --replace "Q4 Results"

# Replace image
python scripts/replace_image.py \
  --presentation-id PRES_ID \
  --slide-index 1 \
  --image-url "https://example.com/chart.png"
```

**Delete slides:**
```bash
# Delete slide
python scripts/delete_slide.py \
  --presentation-id PRES_ID \
  --slide-index 2
```

## Batch Operations

### Batch Requests

**Multiple operations in one API call:**
```python
# Example: Create doc with multiple sections
requests = [
    {'insertText': {'location': {'index': 1}, 'text': 'Title\n'}},
    {'updateParagraphStyle': {'range': {'startIndex': 1, 'endIndex': 6}, 
     'paragraphStyle': {'namedStyleType': 'HEADING_1'}}},
    {'insertText': {'location': {'index': 7}, 'text': 'Content here\n'}}
]

python scripts/batch_update_doc.py \
  --doc-id DOC_ID \
  --requests requests.json
```

## Common Workflows

### Workflow 1: Report Generation

**Scenario:** Generate monthly report from data

```bash
# 1. Create doc from template
python scripts/create_from_template.py \
  --template-id TEMPLATE_ID \
  --title "Monthly Report - Jan 2025"

# 2. Fetch data from Sheet
python scripts/read_sheet.py \
  --sheet-id DATA_SHEET_ID \
  --range "Summary!A1:B10" \
  --output data.json

# 3. Insert data into doc
python scripts/populate_doc.py \
  --doc-id NEW_DOC_ID \
  --data data.json \
  --template-mapping mappings.json

# 4. Export as PDF
python scripts/export_doc.py \
  --doc-id NEW_DOC_ID \
  --format pdf \
  --output "Report-Jan-2025.pdf"
```

### Workflow 2: Data Collection to Sheets

**Scenario:** Append form responses to Sheet

```bash
# Append new row with timestamp
python scripts/append_with_timestamp.py \
  --sheet-id SHEET_ID \
  --values "name,email,response" \
  --add-timestamp
```

### Workflow 3: Presentation Automation

**Scenario:** Generate presentation from data

```bash
# Create presentation with data-driven slides
python scripts/generate_presentation.py \
  --template-id TEMPLATE_ID \
  --data-source SHEET_ID \
  --output-title "Weekly Dashboard"
```

### Workflow 4: Document Translation

**Scenario:** Create multi-language versions

```bash
# Extract text and translate
python scripts/translate_doc.py \
  --source-doc-id DOC_ID \
  --target-languages "es,fr,de" \
  --create-copies
```

### Workflow 5: Collaborative Editing

**Scenario:** Track and manage document changes

```bash
# Get revision history
python scripts/get_revisions.py --doc-id DOC_ID

# Accept/reject suggestions
python scripts/manage_suggestions.py \
  --doc-id DOC_ID \
  --suggestion-id SUGG_ID \
  --action accept
```

## Document Structure

### Google Docs Structure

```json
{
  "title": "Document Title",
  "body": {
    "content": [
      {
        "paragraph": {
          "elements": [
            {
              "startIndex": 1,
              "endIndex": 10,
              "textRun": {
                "content": "Text here",
                "textStyle": {
                  "bold": true,
                  "fontSize": {"magnitude": 12, "unit": "PT"}
                }
              }
            }
          ],
          "paragraphStyle": {
            "namedStyleType": "HEADING_1"
          }
        }
      }
    ]
  }
}
```

### Google Sheets Structure

```json
{
  "properties": {
    "title": "Spreadsheet Title"
  },
  "sheets": [
    {
      "properties": {
        "title": "Sheet1",
        "sheetId": 0
      },
      "data": [
        {
          "rowData": [
            {
              "values": [
                {"userEnteredValue": {"stringValue": "Cell A1"}}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## API Rate Limits

**Docs API:**
- Read requests: 300/min per user
- Write requests: 60/min per user

**Sheets API:**
- Read requests: 500/min per project
- Write requests: 100/min per user

**Slides API:**
- Requests: 300/min per user

**Best practices:**
- Batch operations when possible
- Use exponential backoff
- Cache document structure
- Minimize read requests

## OAuth Scopes

### Docs Scopes
```python
'https://www.googleapis.com/auth/documents'  # Read/write
'https://www.googleapis.com/auth/documents.readonly'  # Read-only
```

### Sheets Scopes
```python
'https://www.googleapis.com/auth/spreadsheets'  # Read/write
'https://www.googleapis.com/auth/spreadsheets.readonly'  # Read-only
```

### Slides Scopes
```python
'https://www.googleapis.com/auth/presentations'  # Read/write
'https://www.googleapis.com/auth/presentations.readonly'  # Read-only
```

## Scripts Reference

**Docs:**
- `create_doc.py` - Create document
- `read_doc.py` - Read content
- `append_doc.py` - Append text
- `insert_text.py` - Insert at position
- `replace_text.py` - Find and replace
- `format_text.py` - Apply formatting
- `export_doc.py` - Export to format

**Sheets:**
- `create_sheet.py` - Create spreadsheet
- `read_sheet.py` - Read data
- `update_cell.py` - Update cell
- `update_range.py` - Update range
- `append_rows.py` - Append data
- `set_formula.py` - Add formula
- `format_cells.py` - Format cells
- `sort_range.py` - Sort data

**Slides:**
- `create_slides.py` - Create presentation
- `read_slides.py` - Read slides
- `add_slide.py` - Add new slide
- `update_slide_text.py` - Update text
- `replace_image.py` - Replace image
- `export_slides.py` - Export format

**Common:**
- `authenticate.py` - OAuth setup
- `batch_update.py` - Batch operations
- `create_from_template.py` - Template operations

## Best Practices

1. **Use batch requests:** Multiple operations in single API call
2. **Cache document structure:** Avoid repeated reads
3. **Validate indices:** Check ranges before operations
4. **Handle concurrent edits:** Implement conflict resolution
5. **Use named ranges:** (Sheets) Reference data by name
6. **Template everything:** Reusable document structures
7. **Export regularly:** Backup as different formats
8. **Monitor quotas:** Stay within rate limits

## Integration Examples

See [examples/](examples/) for complete workflows:
- [examples/report-automation.md](examples/report-automation.md) - Automated report generation
- [examples/data-pipeline.md](examples/data-pipeline.md) - Data collection and analysis
- [examples/presentation-builder.md](examples/presentation-builder.md) - Dynamic presentations
- [examples/collaboration-workflow.md](examples/collaboration-workflow.md) - Team workflows

## Troubleshooting

**"Invalid index"**
- Verify index is within document bounds
- Remember indices are 1-based for content

**"Permission denied"**
- Check document sharing settings
- Verify OAuth scopes

**"Rate limit exceeded"**
- Implement exponential backoff
- Use batch operations
- Reduce request frequency

**"Invalid range"**
- Check A1 notation syntax
- Verify sheet name
- Ensure range exists

## Reference Documentation

- [reference/setup-guide.md](reference/setup-guide.md) - Complete setup
- [reference/docs-api-reference.md](reference/docs-api-reference.md) - Docs API
- [reference/sheets-api-reference.md](reference/sheets-api-reference.md) - Sheets API
- [reference/slides-api-reference.md](reference/slides-api-reference.md) - Slides API
- [reference/formatting-guide.md](reference/formatting-guide.md) - Formatting options
