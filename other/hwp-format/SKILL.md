---
name: hwp-format
description: Provides guidance on HWP/HWPX file formats and Korean government document formatting standards. Auto-activates in contexts like "HWP", "HWPX", "export document", "file conversion", "apply-export", and Korean terms "HWP", "HWPX", "한글 파일", "문서 내보내기", "파일 변환".
---

# HWP/HWPX File Format Guide

## HWP vs HWPX

| Item | HWP (Legacy) | HWPX (Modern) |
|------|-----------|------------|
| File Structure | Binary (OLE) | ZIP + XML (OOXML-like) |
| Programmatic Processing | Very difficult | Possible with Python/Java |
| 한컴오피스 Support | ✅ | ✅ (한컴오피스 2014+) |
| Government Submission | ✅ | ✅ (mostly accepted) |
| File Extension | .hwp | .hwpx |

**Default output format for this plugin:** HWPX

When HWP template files are available, we convert to HWPX using `hwp2hwpx` (Java library) before processing.

---

## HWPX File Structure

HWPX is a ZIP file containing XML files (similar to DOCX):

```
document.hwpx (ZIP)
├── Contents/
│   ├── content.hml        ← Document body content (XML)
│   ├── header.xml         ← Document header (styles, page settings)
│   └── section0.xml       ← Section content
├── BinData/               ← Binary data like images
├── Preview/
│   └── PrvImage.png       ← Preview image
└── [Content_Types].xml    ← MIME type definitions
```

---

## Korean Government Document Formatting Standard

When writing business plans (사업계획서), adhere to these formatting standards:

### Fonts

| Purpose | Font | Fallback |
|---------|------|----------|
| Body | 함초롬바탕 | Malgun Gothic, Batang |
| Headings/Subheadings | 함초롬돋움 | Malgun Gothic, Dotum |
| English/Numbers | HY중고딕 | Arial |

### Font Sizes

| Purpose | Size |
|---------|------|
| Main Title | 16pt |
| Subtitle | 13pt |
| Body | 11pt |
| Footnotes/Captions | 9pt |

### Line Spacing and Margins

| Item | Recommended |
|------|-------------|
| Body line spacing | 160~180% |
| Paper | A4 (210×297mm) |
| Top margin | 20mm |
| Bottom margin | 15mm |
| Left/Right margin | 20mm |
| Header | 10mm |
| Footer | 10mm |

---

## Business Plan Layout Rules

### Cover Page

```
[Top margin]
Program announcement name (16pt, center-aligned)
사업계획서 (20pt, bold, center-aligned)

[Center spacing]

Company: ○○주식회사
Representative: 홍길동
Submission date: 2026년 3월 1일
[Bottom margin]
```

### Table of Contents

Recommended: Use auto-TOC feature. If manual:
- Section numbering: 1. / 1.1 / 1.1.1 format
- Dotted line (……) + page number

### Body

- Main Heading: H1 style, bold, underline
- Secondary Heading: H2 style, bold
- Subheading: H3 style, bold
- Body: Normal style
- Page numbers: Footer, center-aligned

---

## HWP to HWPX Conversion Guide

Convert legacy .hwp template files to .hwpx:

```
Library used: hwp2hwpx (Java)
GitHub: https://github.com/neolord0/hwp2hwpx
```

**Requirements:**
- Java Runtime Environment (JRE) 11+
- hwp2hwpx.jar

**Conversion command:**
```bash
java -jar hwp2hwpx.jar input.hwp output.hwpx
```

The MCP server's `convert_hwp_to_hwpx` tool handles this automatically.
When Java is not available, we skip conversion and fall back to direct HWPX generation mode.

---

## hwp-generator MCP Server Tool Reference

MCP tools used by `/apply-export` command:

| Tool Name | Function | Key Parameters |
|-----------|----------|-----------------|
| `create_document` | Create new HWPX document | paper_size, margins, styles |
| `add_heading` | Insert heading | text, level (1~3) |
| `add_paragraph` | Insert body text | text, bold, italic, underline |
| `add_table` | Insert table | rows, cols, data, merge_cells |
| `add_image` | Insert image | file_path, width, height, align |
| `fill_template` | Fill blank fields in template HWPX | template_path, field_map |
| `set_page_setup` | Configure page settings | paper, margins, header, footer |
| `convert_hwp_to_hwpx` | HWP → HWPX conversion | input_path, output_path |
| `export_file` | Save final file | output_path, format (hwpx/pdf) |

---

## Template Blank Field Detection

Blank field patterns in government-provided HWP templates:

```xml
<!-- Common blank field patterns -->
<hp:t>○○○○○</hp:t>      ← Text field to fill
<hp:t>[ ]</hp:t>          ← Checkbox style
<hp:t>(                )</hp:t>   ← Parenthetical blank
```

The `fill_template` tool automatically detects these patterns and fills them with business plan content.

---

## Limitations and Workarounds

| Situation | Solution |
|-----------|----------|
| Complex forms (multi-column, special layout) | If auto-fill fails, provide Markdown draft + manual copy-paste instructions |
| Java not installed | Skip HWP conversion, generate HWPX directly |
| LibreOffice available | Use LibreOffice headless for DOCX → HWPX conversion (backup path) |
| Legacy agencies accept only .hwp | Generate HWPX, then save as .hwp in 한컴오피스 |
