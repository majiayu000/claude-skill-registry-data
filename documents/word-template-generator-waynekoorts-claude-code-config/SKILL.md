---
name: word-template-generator
description: Generate Word documents (.docx) using direct OOXML manipulation. Use when the user asks to create Word documents, templates, resumes, invoices, letters, reports, proposals, or any .docx file with full control over formatting and structure.
---

# Word Document Generator

Generate Word documents (.docx) by directly creating the XML files that comprise the DOCX package. This skill provides complete knowledge of the Office Open XML (OOXML) format for generating any type of Word document.

## DOCX File Format

A DOCX file is a ZIP archive containing XML files following the Open Packaging Conventions (OPC) and WordprocessingML schema. The format is defined by ISO/IEC 29500 (ECMA-376).

### Package Structure

```
document.docx (ZIP archive)
├── [Content_Types].xml          # Content type definitions for all parts
├── _rels/
│   └── .rels                    # Package relationships (entry point)
├── word/
│   ├── document.xml             # Main document content
│   ├── styles.xml               # Style definitions
│   ├── numbering.xml            # List/numbering definitions (if needed)
│   ├── settings.xml             # Document settings
│   ├── fontTable.xml            # Font declarations
│   ├── header1.xml              # Header content (optional)
│   ├── footer1.xml              # Footer content (optional)
│   └── _rels/
│       └── document.xml.rels    # Document part relationships
└── docProps/
    ├── app.xml                  # Application properties
    └── core.xml                 # Core document properties (metadata)
```

### Core Namespaces

| Prefix | Namespace URI | Purpose |
|--------|--------------|---------|
| `w` | `http://schemas.openxmlformats.org/wordprocessingml/2006/main` | Main WordprocessingML |
| `r` | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` | Relationships |
| `wp` | `http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing` | Drawing positioning |
| `a` | `http://schemas.openxmlformats.org/drawingml/2006/main` | DrawingML |
| `pic` | `http://schemas.openxmlformats.org/drawingml/2006/picture` | Pictures |

### Measurement Units

- **Twips**: 1/20 of a point, 1/1440 of an inch (primary unit for margins, spacing)
- **Half-points**: Font sizes (24 = 12pt)
- **EMUs**: 914400 EMUs = 1 inch (for drawings)
- **Percentages**: Some widths use fiftieths of a percent (5000 = 100%)

Common conversions:
- 1 inch = 1440 twips = 914400 EMUs
- 1 cm = 567 twips
- 1 point = 20 twips

## Instructions

When asked to create a Word document:

1. **Create the folder structure** for the raw XML files in `templates/{docname}/`
2. **Generate each required XML file** with proper content (no extra whitespace/indentation)
3. **Package into a DOCX** using Python's zipfile module (see Packaging section below)
4. **Clean up** the temporary folder after packaging

### CRITICAL: Packaging Requirements

**DO NOT use PowerShell's Compress-Archive** - it creates invalid DOCX files that Word cannot open.

**ALWAYS use Python's zipfile module** with these requirements:
- Use `zipfile.ZIP_DEFLATED` compression
- Archive paths must use **forward slashes** (`/`), not backslashes
- Paths must be relative to the source folder (no leading `./` or folder prefix)

Use this packaging script (saved at `templates/package_docx.py`):

```bash
cd templates && python package_docx.py {source_folder} {output_file.docx}
```

### XML Formatting Rules

- **No indentation/pretty-printing** in XML files - Word is sensitive to whitespace
- Use single-line elements where possible
- Always include `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` declaration
- All XML must be valid and well-formed

### Required Files (Minimum)

Every DOCX needs these files:
- `[Content_Types].xml`
- `_rels/.rels`
- `word/document.xml`
- `word/_rels/document.xml.rels`

### Recommended Additional Files

For proper rendering:
- `word/styles.xml` - Defines styles (Normal, Heading1, etc.)
- `word/settings.xml` - Document settings
- `word/fontTable.xml` - Font declarations
- `docProps/core.xml` - Document metadata
- `docProps/app.xml` - Application properties

### Output Location

Save generated documents to: `templates/`

Naming convention: `{document_type}_template.docx`

## XML File Templates

### [Content_Types].xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
    <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
    <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
    <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
    <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
```

### _rels/.rels

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
```

### word/_rels/document.xml.rels

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
</Relationships>
```

### word/document.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <w:body>
        <!-- Document content goes here -->
        <w:p>
            <w:r>
                <w:t>Hello World</w:t>
            </w:r>
        </w:p>
        <w:sectPr>
            <w:pgSz w:w="12240" w:h="15840"/>
            <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
        </w:sectPr>
    </w:body>
</w:document>
```

### word/styles.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:docDefaults>
        <w:rPrDefault>
            <w:rPr>
                <w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Times New Roman"/>
                <w:sz w:val="22"/>
                <w:szCs w:val="22"/>
                <w:lang w:val="en-US"/>
            </w:rPr>
        </w:rPrDefault>
        <w:pPrDefault>
            <w:pPr>
                <w:spacing w:after="160" w:line="259" w:lineRule="auto"/>
            </w:pPr>
        </w:pPrDefault>
    </w:docDefaults>
    <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
        <w:name w:val="Normal"/>
        <w:qFormat/>
    </w:style>
    <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="heading 1"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="240" w:after="0"/>
            <w:outlineLvl w:val="0"/>
        </w:pPr>
        <w:rPr>
            <w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/>
            <w:color w:val="2E74B5"/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:style>
    <w:style w:type="paragraph" w:styleId="Heading2">
        <w:name w:val="heading 2"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:qFormat/>
        <w:pPr>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="200" w:after="0"/>
            <w:outlineLvl w:val="1"/>
        </w:pPr>
        <w:rPr>
            <w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/>
            <w:color w:val="2E74B5"/>
            <w:sz w:val="26"/>
            <w:szCs w:val="26"/>
        </w:rPr>
    </w:style>
</w:styles>
```

### word/settings.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:zoom w:percent="100"/>
    <w:defaultTabStop w:val="720"/>
    <w:characterSpacingControl w:val="doNotCompress"/>
    <w:compat>
        <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
    </w:compat>
</w:settings>
```

### word/fontTable.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:font w:name="Calibri">
        <w:panose1 w:val="020F0502020204030204"/>
        <w:charset w:val="00"/>
        <w:family w:val="swiss"/>
        <w:pitch w:val="variable"/>
    </w:font>
    <w:font w:name="Calibri Light">
        <w:panose1 w:val="020F0302020204030204"/>
        <w:charset w:val="00"/>
        <w:family w:val="swiss"/>
        <w:pitch w:val="variable"/>
    </w:font>
    <w:font w:name="Times New Roman">
        <w:panose1 w:val="02020603050405020304"/>
        <w:charset w:val="00"/>
        <w:family w:val="roman"/>
        <w:pitch w:val="variable"/>
    </w:font>
</w:fonts>
```

### docProps/core.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <dc:title>Document Title</dc:title>
    <dc:creator>Author Name</dc:creator>
    <dcterms:created xsi:type="dcterms:W3CDTF">2025-01-01T00:00:00Z</dcterms:created>
    <dcterms:modified xsi:type="dcterms:W3CDTF">2025-01-01T00:00:00Z</dcterms:modified>
</cp:coreProperties>
```

### docProps/app.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
    <Application>OOXML Generator</Application>
    <AppVersion>1.0</AppVersion>
</Properties>
```

## WordprocessingML Elements

See `REFERENCE.md` for complete documentation of all XML elements for paragraphs, runs, tables, styles, numbering, headers/footers, and more.

## Common Document Types

- **Resume/CV**: Contact info, summary, skills, experience, education
- **Cover Letter**: Header, date, recipient, body paragraphs, signature
- **Invoice**: Company info, client info, line items table, totals
- **Proposal**: Title, executive summary, scope, timeline, pricing
- **Meeting Minutes**: Header, attendees, agenda items, action items
- **Business Letter**: Letterhead, date, recipient, body, signature block
- **Report**: Title page, table of contents, sections, appendices

## Style Guidelines

### Fonts
- Headings: Calibri Light, 14-18pt
- Body: Calibri, 10-11pt
- Use bold for emphasis, avoid underlines except for links

### Spacing
- Section spacing: 12pt (240 twips) before major sections
- Line spacing: 1.0 to 1.15 for compact layouts
- Margins: 0.5" to 1" (720-1440 twips)

### Colors
- Professional: black text, subtle accent colors
- Use color sparingly for headers or key elements
- Common accent: #2E74B5 (blue)
