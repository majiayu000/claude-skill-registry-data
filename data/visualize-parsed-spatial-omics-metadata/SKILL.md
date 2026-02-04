---
name: visualize-parsed-spatial-omics-metadata
description: Create an interactive HTML viewer to visualize and verify parsed metadata against source documents.
---

# spatialdata-db metadata visualizer

This skill creates a static, self-contained HTML file that allows visual verification of parsed metadata against the original source documents.

## Input-output
- **Input**:
  - A JSON file containing parsed metadata (output from spatialdata-db-parser skill)
  - One or more cached HTML files (source documents used during parsing)
  - A mapping file (JSON) that links each metadata field to excerpts in the source documents
- **Output**: A single self-contained HTML file that provides an interactive interface for verification

## Purpose

When parsing spatial omics metadata, it's critical to verify that the extracted values are accurate. This tool creates a visual interface that:
1. Shows all parsed metadata fields and their values in a sidebar
2. Displays the source HTML documents in tabs
3. Highlights the relevant excerpts when clicking on a metadata field
4. Provides visual feedback (orange highlighting) to quickly identify which documents contain relevant information

## HTML Interface Structure

The generated HTML file has three main components:

### 1. Left Sidebar (Metadata Panel)
- Displays all schema fields organized by category (Sample Level, Xenium Specific, Visium Specific)
- Shows the parsed value for each field
- Each field is clickable to trigger highlighting

### 2. Top Tab Bar
- One tab for each source HTML document
- Tabs are highlighted in orange when they contain excerpts related to the currently selected field
- Click to switch between different source documents

### 3. Center Panel (Document Viewer)
- Displays the content of the selected HTML document
- When a metadata field is clicked, relevant excerpts are highlighted in orange
- Supports scrolling to navigate the document

## Technical Requirements

**CRITICAL**: The output HTML file must be completely self-contained and offline-capable:
- All HTML content from source documents must be embedded (as escaped strings or data URIs)
- All JavaScript must be inline (no external dependencies)
- All CSS must be inline (no external stylesheets)
- NO network requests of any kind
- NO external CDN links (no jQuery, no Bootstrap, no Google Fonts, etc.)
- Must work by simply opening the file in a browser (file:// protocol)

## Input File Format

### 1. Parsed Metadata (JSON)
The output from the spatialdata-db-parser skill, e.g.:
```json
{
  "Product": "In Situ Gene Expression",
  "Assay": "spatial transcriptomics",
  "Organism": "Homo sapiens",
  ...
}
```

### 2. Source HTML Files
The cached HTML pages used during parsing, stored locally.

### 3. Mapping File (JSON)
A JSON file that maps each metadata field to the text excerpts and source files where the value was found:
```json
{
  "Product": {
    "value": "In Situ Gene Expression",
    "excerpts": [
      {
        "file": "source_page_1.html",
        "text": "In Situ Gene Expression",
        "context": "...surrounding text for better matching..."
      }
    ]
  },
  "Organism": {
    "value": "Homo sapiens",
    "excerpts": [
      {
        "file": "source_page_1.html",
        "text": "Homo sapiens",
        "context": "Species: Homo sapiens (human)"
      }
    ]
  }
}
```

## Instructions

1. Read the parsed metadata JSON file
2. Read all cached HTML source files
3. Read or create the mapping file that links metadata fields to excerpts
4. Generate a single, self-contained HTML file with:
   - Embedded source HTML content (as JavaScript strings or data URIs)
   - Inline JavaScript for the interactive functionality
   - Inline CSS for styling
   - Sidebar showing all metadata fields and values
   - Tab interface for switching between source documents
   - Click handlers that highlight excerpts in orange
   - Logic to highlight tabs containing relevant excerpts
5. Save the output as a single .html file that can be opened in any browser

## Implementation Notes

- Use vanilla JavaScript only (no frameworks or libraries)
- Escape HTML content properly when embedding
- Use `mark` or `span` tags with orange background for highlighting
- Consider using `scrollIntoView()` to auto-scroll to highlighted excerpts
- Use CSS for the three-panel layout (flexbox or grid recommended)
- Make the interface responsive if possible
- Add a "Clear highlights" button to reset the view

## Example Usage Flow

1. User runs spatialdata-db-parser skill on a dataset
2. User creates a mapping file (or the parser creates it automatically)
3. User runs this visualizer skill with the JSON, HTML files, and mapping
4. Visualizer generates viewer.html
5. User opens viewer.html in a browser
6. User clicks on "Organism" in the sidebar
7. The relevant HTML tab is highlighted in orange and switched to
8. The text "Homo sapiens" is highlighted in orange in the document
9. User can verify the extraction was correct

## Additional Information

This tool is designed for quality control and verification purposes. It helps curators:
- Quickly verify that metadata extraction was accurate
- Identify potential errors or mismatches
- Trace back each field to its original source
- Build confidence in the automated parsing process
