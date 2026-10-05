---
name: docx
description: Use this skill whenever the user wants to create or edit .docx (Microsoft Word) files. This includes creating new Word documents from scratch, editing existing Word documents, extracting content from Word files, converting between formats, adding images or other content to Word files, or manipulating Word file structure. If the user mentions .docx, Word, DOCX, or wants to produce a Word document, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX Processing Guide

## Overview

This guide covers creating, editing, and analyzing Word documents (.docx files). Use this skill when you need to programmatically create new Word documents, make targeted edits to existing files, or extract content.

## Creating Documents

Use the `docx` JavaScript library for programmatic document creation. The library provides a powerful API for building Word documents with full formatting control.

### Page Sizing

Always explicitly set page size — `docx-js` defaults to A4 (11,906 × 16,838 DXA), not US Letter. Specify dimensions using DXA units, where 1 inch = 1440 DXA.

For US Letter (8.5" × 11"):
- Width: 12,240 DXA
- Height: 15,840 DXA
- With standard 1" margins: content area is 10,240 × 13,840 DXA

For landscape orientation, pass portrait dimensions with `landscape: true` — the library handles internal conversion:
```javascript
const doc = new Document({
  sections: [{
    properties: {
      pageHeight: 15840,  // Portrait height
      pageWidth: 12240,   // Portrait width
      landscape: true,    // Library rotates internally
    }
  }]
});
```

### Tables

Tables require dual width specifications. Always specify both `columnWidths` array AND individual cell `width` properties, with all values using `WidthType.DXA` (percentage widths break in Google Docs).

Table width must equal the sum of column widths:
```javascript
const columnWidths = [3000, 4000, 3000];  // Total: 10000
const table = new Table({
  columnWidths: columnWidths,
  width: { size: 10000, type: WidthType.DXA },  // Match total
  rows: [
    new TableRow({
      cells: [
        new TableCell({
          children: [...],
          width: { size: 3000, type: WidthType.DXA }
        }),
        // ... more cells
      ]
    })
  ]
});
```

Use `ShadingType.CLEAR` for cell background colors to avoid rendering issues.

### Bullets and Lists

Never insert bullet points using manual Unicode characters. Instead, use the numbering system with `LevelFormat.BULLET`:

```javascript
new Paragraph({
  text: "Item 1",
  bullet: {
    level: 0
  }
})
```

### Smart Typography

Maintain professional typography with smart quotes and apostrophes via XML entities in the underlying document:
- `&#x201C;` — Left double quote (")
- `&#x201D;` — Right double quote (")
- `&#x2019;` — Apostrophe/Right single quote (')

These are handled automatically when using standard string methods, but when editing raw XML, use these entities explicitly.

## Editing Existing Documents

Use the three-step workflow: unpack → edit → pack.

### Step 1: Unpack

Extract the .docx archive into editable XML:
```bash
unzip -q input.docx -d unpacked/
```

### Step 2: Edit

Edit files in `unpacked/word/document.xml` directly. Prefer the Edit tool for transparent string replacement rather than writing custom Python scripts.

When applying tracked changes (revision marks), copy the original run's formatting block (`<w:rPr>`) to the new run to maintain style consistency:
```xml
<!-- Original run with formatting -->
<w:r>
  <w:rPr>
    <w:b/>
    <w:color w:val="FF0000"/>
  </w:rPr>
  <w:t>Original text</w:t>
</w:r>

<!-- New run with revision mark — copy the <w:rPr> block -->
<w:r>
  <w:ins w:id="0" w:author="Editor" w:date="2024-01-15T10:00:00Z"/>
  <w:rPr>
    <w:b/>
    <w:color w:val="FF0000"/>
  </w:rPr>
  <w:t>Edited text</w:t>
</w:r>
```

When deleting entire paragraphs, mark both the paragraph content AND the paragraph element itself as deleted to prevent empty rows from persisting after change acceptance:
```xml
<!-- Mark paragraph deletion at both content and element level -->
<w:del w:id="0" w:author="Editor" w:date="2024-01-15T10:00:00Z">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
    </w:pPr>
    <w:r>
      <w:annotationStart w:id="0"/>
      <w:t>Deleted paragraph</w:t>
      <w:annotationEnd w:id="0"/>
    </w:r>
  </w:p>
</w:del>
```

### Step 3: Pack

Repack the XML back into a .docx file with validation:
```bash
cd unpacked/
zip -r -q ../output.docx word/ _rels/ '[Content_Types].xml' customXml/ 2>/dev/null
cd ..
```

If validation errors occur, the library has auto-repair capabilities — repack and try again.

## Reading Documents

### Extract Text

Use `pandoc` to extract plain text while preserving document structure:
```bash
pandoc input.docx -t plain -o output.txt
```

### Access Raw XML

For programmatic content analysis, access the document's underlying XML structure directly via the unpacking method above.

## Important Constraints

**Line breaks** — Never use `\n` for line breaks within a paragraph. Instead, create separate Paragraph elements or use explicit line break elements.

**Page breaks** — PageBreak elements must nest within Paragraph containers; they cannot exist at document root level.

**ImageRun** — When adding images, always specify the explicit `type` parameter (e.g., `type: "picture"`).

**Heading styles** — Heading elements require `outlineLevel` attributes for table-of-contents generation:
```javascript
new Paragraph({
  text: "Section Title",
  style: "Heading1",
  outlineLevel: 0
})
```

**Built-in style overrides** — Override built-in Word styles using exact identifiers (e.g., `"Heading1"`, `"Normal"`), not custom names.

---

See REFERENCE.md for advanced techniques, more examples, and JavaScript library details.
