---
name: executive-summary-formatter
description: Transform poorly formatted executive summaries into professionally formatted documents matching a specific brand template. Use when the user provides an executive summary (text, markdown, docx, or PDF) and wants it reformatted with precise brand styling including Work Sans fonts, branded color scheme (red #DA291C accent, navy #032340 table headers), specific table formatting, header/footer with logo graphics, and consistent spacing. This skill ensures pixel-perfect replication of the template's typography, tables, bullets, and page layout.
---

# Executive Summary Formatter

Transform any executive summary content into a professionally formatted .docx document matching the brand template exactly.

## Quick Start

1. Read the content from the user's input (text, markdown, or uploaded document)
2. Create a new document using docx-js with the specifications below
3. Apply all formatting rules precisely
4. Output to `/mnt/user-data/outputs/`

## Brand Specifications

### Fonts
- **Primary Font**: Work Sans (body text, tables, lists)
- **Light Variant**: Work Sans Light (document title only - 48pt)
- **Fallback**: Arial (if Work Sans unavailable)

### Color Palette
| Element | Color Code | Usage |
|---------|------------|-------|
| Section Headers | #DA291C (red) | Major section titles |
| Table Header BG | #032340 (navy) | Table header row background |
| Table Header Text | #FFFFFF (white) | Text in table headers |
| Body Text | #000000 (black) | Normal paragraph text |
| Subtitle/Caption | #808080 (gray) | Subtitle, secondary info |
| Table Borders (Data) | #CCCCCC (light gray) | Data row borders |
| Table Borders (Header) | #AAAAAA (medium gray) | Header row borders |
| Alternating Row BG | #F2F2F2 (very light gray) | Every other data row |
| Highlight Cell BG | #FFE3E3 (light pink) | Special emphasis cells |
| Hyperlink | #0563C1 (blue) | Links |

### Typography Scale (half-points)
| Element | Size | Weight | Additional |
|---------|------|--------|------------|
| Document Title | 48 (24pt) | Light | Work Sans Light, centered, NOT bold |
| Subtitle | 22 (11pt) | Regular | Italic, gray #808080, centered |
| Section Header (Large) | 48 (24pt) | Regular | Red #DA291C, NOT bold |
| Section Header (Small) | 28 (14pt) | Regular | Red #DA291C, NOT bold |
| Body Text | 22 (11pt) | Regular | Work Sans (inherited from defaults) |
| Table Header | 18 (9pt) | Bold | White on navy #032340 |
| Table Data | 18 (9pt) | Regular | Work Sans |
| Table Data (Small) | 16 (8pt) | Regular | Used in compact tables |
| Bullet Items | 22 (11pt) | Regular | Work Sans |

### Spacing (in twips, 1440 = 1 inch)
| Element | Before | After |
|---------|--------|-------|
| Document Title | 0 | 120 |
| Subtitle | 0 | 400 |
| Section Header (large) | 360 | 160 |
| Section Header (small) | 360 | 160 |
| Body Paragraph | 0 | 160 |
| Bullet Item | 0 | 120 |
| Table | 240 | 240 |

### Page Layout
- **Page Size**: A4 (11906 Ã— 16838 twips)
- **Margins**: 1440 twips (1 inch) all sides
- **Header Distance**: 708 twips
- **Footer Distance**: 708 twips

## Document Structure

### 1. Title Block
```
[Document Title - Work Sans Light 24pt, centered]
[Subtitle - Work Sans 11pt italic gray, centered]
[Blank line]
```

### 2. Section Pattern
```
[Section Header - Work Sans 24pt or 14pt red]
[Body paragraphs - Work Sans 11pt, 160 twips after]
[Tables as needed]
[Bullet lists as needed]
```

## docx-js Implementation Patterns

The skill uses the `docx` npm package. Here are working patterns:

### Required Imports

```javascript
const { 
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, WidthType, BorderStyle, 
  ShadingType, VerticalAlign, PageNumber, ImageRun,
  convertInchesToTwip
} = require('docx');
```

### Table Creation - CRITICAL RULES

1. **Always use percentage width for tables with explicit columnWidths:**
```javascript
const table = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: tableBorders,
  columnWidths: [1800, 850, 850, 850, 850], // REQUIRED - specify explicit widths
  rows: [...]
});
```

2. **Always specify `columnWidths` array** - Without this, columns will collapse or be uneven. This is the #1 cause of table rendering issues.

3. **Define borders once and reuse:**
```javascript
const tableBorders = {
  top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
  bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
  left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
  right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
  insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
  insideVertical: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" }
};
```

### Column Width Calculation Guidelines

**Total usable width for A4 with 1" margins: ~9300 DXA**

| Content Type | Recommended Width (DXA) | Examples |
|--------------|------------------------|----------|
| Single character / dash | 700-850 | "â€”", "3", "4" |
| Percentage values | 800-900 | "40%", "65%" |
| Short text (1-3 words) | 1000-1400 | "Production", "Live 2024" |
| Medium text (4-8 words) | 1600-2200 | "Shape standard & preserve IP" |
| Long text (sentences) | 2800-4500 | Full descriptions |
| Row labels (first column) | 1600-2000 | Category names |
| Highlight columns | 1000-1200 | "CDM Relevance" values |

**For multi-column tables (6+ columns):**
- Use abbreviated headers (e.g., "MS" not "Morgan Stanley", "BofA" not "Bank of America")
- Keep data columns uniform width (800-900 DXA each)
- Give first column extra width for row labels (1600-1800 DXA)
- Verify total width sums to ~9300 DXA

### Cell Shading for Alternating Rows

**CRITICAL:** Must include all three shading properties:
```javascript
shading: { 
  fill: "F2F2F2",           // The background color
  type: ShadingType.CLEAR,  // Required
  color: "auto"             // Required
}
```

### Highlight Column Rules

**CRITICAL:** When a column uses highlight formatting (e.g., pink background for "CDM Relevance"), ALL cells in that column must use the highlight cell function, including empty cells:

```javascript
// WRONG - leaves cell without highlight, breaks column consistency
createHighlightCell("", 1100)  

// CORRECT - maintains column consistency with placeholder
createHighlightCell("â€”", 1100)
```

### Multi-Paragraph Table Cells

For cells with multiple lines of content, pass an array:
```javascript
createDataCell(["Line 1.", "Line 2."], width, isFirstCol, isAltRow)

// Implementation adds spacing between paragraphs:
const children = paragraphs.map((para, idx) => new Paragraph({
  spacing: idx > 0 ? { before: 80 } : {},
  children: [new TextRun({ text: para, ... })]
}));
```

### Working Helper Functions

```javascript
// Brand colors constant
const COLORS = {
  RED_ACCENT: "DA291C",
  NAVY_HEADER: "032340",
  WHITE: "FFFFFF",
  BLACK: "000000",
  GRAY_SUBTITLE: "808080",
  BORDER_LIGHT: "CCCCCC",
  BORDER_HEADER: "AAAAAA",
  ALT_ROW_GRAY: "F2F2F2",
  HIGHLIGHT_PINK: "FFE3E3"
};

// Table header cell (navy background, white bold text)
function createHeaderCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: COLORS.NAVY_HEADER, type: ShadingType.CLEAR, color: "auto" },
    verticalAlign: VerticalAlign.CENTER,
    margins: { 
      top: convertInchesToTwip(0.03), 
      bottom: convertInchesToTwip(0.03), 
      left: convertInchesToTwip(0.06), 
      right: convertInchesToTwip(0.06) 
    },
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ 
        text, 
        bold: true, 
        color: COLORS.WHITE, 
        size: 18,
        font: "Work Sans" 
      })]
    })]
  });
}

// Data cell with alternating row support
function createDataCell(content, width, isFirstCol = false, isAlternateRow = false, centered = false) {
  const paragraphs = Array.isArray(content) ? content : [content];
  
  const children = paragraphs.map((para, idx) => new Paragraph({
    alignment: centered ? AlignmentType.CENTER : AlignmentType.LEFT,
    spacing: idx > 0 ? { before: 80 } : {},
    children: [new TextRun({ 
      text: para, 
      bold: isFirstCol, 
      size: 18, 
      font: "Work Sans" 
    })]
  }));

  const cell = new TableCell({
    width: { size: width, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { 
      top: convertInchesToTwip(0.04), 
      bottom: convertInchesToTwip(0.04), 
      left: convertInchesToTwip(0.06), 
      right: convertInchesToTwip(0.06) 
    },
    shading: isAlternateRow ? { fill: COLORS.ALT_ROW_GRAY, type: ShadingType.CLEAR, color: "auto" } : undefined,
    children: children
  });
  
  return cell;
}

// Highlight cell (pink background) - use for special emphasis columns
function createHighlightCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: COLORS.HIGHLIGHT_PINK, type: ShadingType.CLEAR, color: "auto" },
    verticalAlign: VerticalAlign.CENTER,
    margins: { 
      top: convertInchesToTwip(0.03), 
      bottom: convertInchesToTwip(0.03), 
      left: convertInchesToTwip(0.02), 
      right: convertInchesToTwip(0.02) 
    },
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ 
        text: text || "â€”",  // Always use placeholder for empty cells
        bold: true, 
        color: COLORS.BLACK, 
        size: 16, 
        font: "Work Sans" 
      })]
    })]
  });
}
```

## Table Formatting

### Table Structure
```javascript
// Table width: 100% with explicit columnWidths
// Cell margins (header): top 0.03", left 0.06", bottom 0.03", right 0.06"
// Cell margins (data): top 0.04", left 0.06", bottom 0.04", right 0.06"
// Cell margins (highlight): top 0.03", left 0.02", bottom 0.03", right 0.02"
```

### Header Row
- Background: #032340 (navy)
- Text: White (#FFFFFF), Bold, 9pt (18 half-pts), centered
- Borders: 4pt #CCCCCC
- Vertical align: center

### Data Rows - Alternating Colors
- **Odd rows (1, 3, 5...)**: No fill (white background)
- **Even rows (2, 4, 6...)**: Fill #F2F2F2 (light gray) with type: CLEAR, color: auto
- Text: Black, Regular, 9pt (18 half-pts)
- Borders: 4pt #CCCCCC
- First column: Bold (archetype/category names)
- Vertical align: center

### Special Highlight Cells
- Background: #FFE3E3 (light pink) with type: CLEAR, color: auto
- Used for emphasis columns like "CDM Relevance"
- Text: Bold, centered, 8pt (16 half-pts)
- **Apply to ALL cells in highlight column, use "â€”" for empty**

## Bullet List Formatting

- **Style**: Symbol bullet (â—)
- **Indent**: 360 twips left
- **Spacing**: 120 twips after each item
- **Font**: Work Sans 11pt

## Header/Footer

### Header
- Graphic bar spanning full page width at top
- Uses `assets/media/image2.svg` or `image1.png` (decorative header bar)
- Position: anchored to page, offset from top

### Footer
- Centered page numbering: "Page X of Y"
- Logo in right margin (`assets/media/image3.png`)
- Font: Default (Arial 11pt)

## Pre-Delivery Checklist

**Before outputting the document, verify:**

- [ ] All tables have `columnWidths` array specified
- [ ] Column widths sum to approximately 9300 DXA for A4
- [ ] Highlight columns have styling on ALL cells (no empty unstyled cells)
- [ ] Empty highlight cells use "â€”" placeholder
- [ ] Alternating row shading includes `type: ShadingType.CLEAR, color: "auto"`
- [ ] Long text content has adequate column width (2500+ DXA)
- [ ] Multi-column tables (6+) use abbreviated headers
- [ ] First column has adequate width for row labels (1600+ DXA)

## Workflow

1. **Parse Input**: Extract text content, identify structure (titles, sections, tables, bullets)
2. **Analyze Tables**: Count columns, estimate content length, calculate widths
3. **Map to Template**: Match content to template elements
4. **Build Document**: Use docx-js with exact specifications above
5. **Add Header/Footer**: Include branded graphics from `assets/media/`
6. **Validate**: Run through pre-delivery checklist
7. **Export**: Save as .docx to outputs directory

## Assets

The skill includes these brand assets in `assets/media/`:
- `image1.png` - Header bar / Footer logo (fallback)
- `image2.svg` - Header decorative bar
- `image3.png` - Footer logo

## Critical Rules

1. **ALWAYS use Work Sans** font family (Light variant for title only - NOT BOLD)
2. **ALWAYS use exact color codes** - no approximations
3. **ALWAYS apply precise spacing** - before/after values in twips
4. **Table headers MUST be navy #032340** with white bold text
5. **Section headers MUST be red #DA291C** - NOT bold
6. **Alternating table rows**: white, then #F2F2F2 (light gray)
7. **Never use default Word styles** - apply custom formatting explicitly
8. **Preserve content hierarchy** - don't flatten structure
9. **ALWAYS specify columnWidths** for tables - this is required for proper rendering
10. **Highlight columns**: style ALL cells including empty ones (use "â€”")
11. **Multi-paragraph table cells** use spacing before: 80 twips for 2nd+ paragraphs
12. **Body text inherits 11pt** from document defaults - don't set explicitly unless overriding

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Tables collapse/render incorrectly | Missing `columnWidths` | Always specify columnWidths array |
| Uneven column spacing | Widths don't match content | Use width guidelines by content type |
| Missing highlight on cells | Empty cell = no styling applied | Use "â€”" placeholder with highlight styling |
| Alternating rows not showing | Incomplete shading object | Include fill, type: CLEAR, and color: auto |
| Text overflow in cells | Column too narrow | Increase width, abbreviate headers if needed |