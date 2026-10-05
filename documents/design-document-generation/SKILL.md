---
type: Skill
name: design-document-generation
description: Generate professional documents — PDF, Word (.docx), Excel (.xlsx), and invoices — from natural language descriptions or structured data. Covers AI-powered and simple document creation, HTML-to-PDF conversion, PDF extraction/OCR, merging, watermarking, and data export. Use when you need to create campaign decks, reports, proposals, invoices, spreadsheets, or any shareable document — especially for Step 7 monthly presentations, campaign briefs, and analytics reports.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Document Generation

Use this skill when creating professional documents — campaign decks, reports, proposals, or any structured document for print or sharing.

## Available Tools

### Document Creation

| Tool | Output | Complexity | Best For |
|---|---|---|---|
| `pro_pdf_document` | PDF | Advanced | Campaign decks, branded reports, presentations |
| `pro_word_document` | .docx | Advanced | Editable drafts, templates, collaborative docs |
| `generate_pdf` | PDF | Simple | Quick PDF from plain content |
| `generate_word` | .docx | Simple | Quick Word doc from plain content |
| `generate_excel` | .xlsx | Simple | Quick spreadsheet from CSV/JSON data |
| `excel_data_export` | .xlsx | Structured | Export arrays with headers to formatted Excel |
| `html_to_pdf` | PDF | Conversion | Convert HTML/CSS content to PDF |
| `generate_invoice_pdf` | PDF | Specialized | Professional invoices with line items and tax |

### Document Processing

| Tool | Purpose |
|---|---|
| `extract_pdf_text` | Extract text from PDFs (auto-detects scanned + OCR) |
| `ocr_pdf_text` | OCR for scanned/image-only PDF documents |
| `pro_document_ocr` | Advanced batch OCR with structured output (JSON/Markdown/HTML) |
| `extract_image_text` | OCR text from images (screenshots, documents, handwriting) |
| `merge_pdfs` | Combine multiple PDFs into one |
| `add_watermark_to_pdf` | Add text/image watermarks to PDFs for branding/security |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for document workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify document generation tools are registered |
| `wp mcp-ai log` | Check document generation success/failure logs |
| `wp mcp-ai bulk` | Batch-process document exports from post types |
| `wp media import` | Import generated documents into the media library |

## When to use this skill

Trigger when ANY of the following is true:

- Creating a monthly campaign presentation (SOP Step 7).
- The task asks to "generate a PDF", "create a report", "make a document", or "create a spreadsheet".
- Building a campaign brief for approval.
- Generating an analytics report from data.
- Creating brand guidelines or strategy documents.
- The task mentions "presentation deck", "campaign proposal", "deliverable", or "invoice".
- Exporting structured content (calendar, product list, strategy doc) to a shareable format.
- Converting HTML content to PDF.
- Extracting text from PDFs or images (OCR).
- Merging multiple PDFs or adding watermarks.

## `pro_pdf_document` — PDF Generation

Creates polished, print-ready PDF documents from descriptions or structured data.

### Parameters

```
operation    — "generate" (from description), "structure" (from sections), "format" (apply styling)
description  — Natural language description of the document to create
content      — Plain text or structured content
title        — Document title (metadata + optional first page)
author       — Document author (metadata)
sections     — Array of { heading, content } objects (for "structure" operation)
formatting   — { font_size, font_family, color, line_height }
page_size    — "A4" (default), "Letter", "Legal", "A3", "A5"
orientation  — "portrait" (default) or "landscape"
model        — AI model override (optional)
upload       — Upload to WordPress media library (default: true)
```

### Operation Modes

| Operation | Use When | Input |
|---|---|---|
| **generate** | "Make me a campaign deck for August" | `description` — natural language |
| **structure** | "Here's my content, format it nicely" | `sections` — structured array |
| **format** | "I have raw text, apply branding to it" | `content` + `formatting` |

### Sophie's Core Documents

#### 1. Monthly Campaign Deck (SOP Step 7)

```
pro_pdf_document {
  operation: "structure"
  title: "August 2026 — The Parfumerie Monthly Campaign Plan"
  author: "Sophie — Digital Marketing"
  sections: [
    { heading: "1. Monthly Theme", content: "'Scents of Sri Lanka' — celebrating island-inspired fragrances..." },
    { heading: "2. Product Selection", content: "Hero: Carolina Herrera Good Girl (Rs. 27,500, 6 units)\nSupport: Conatural Rose Face Wash (Rs. 1,500, 3 units)\nSlow Mover Push: CN29 Lavender & Chamomile (Rs. 2,750, 4 units)" },
    { heading: "3. Weekly Content Calendar", content: "Week 1: Theme launch + Islandwide Delivery post\nWeek 2: Product deep-dive carousel + Reel\nWeek 3: Weekend flash sale promo\nWeek 4: Gift guide + E-Gift Vouchers" },
    { heading: "4. Reel Storyboards", content: "Reel 1: 'Morning Ritual' — skincare routine with Conatural products\nReel 2: 'Scent of the Day' — Carolina Herrera Good Girl unboxing\nReel 3: 'Behind the Counter' — store lifestyle, gift wrapping in action" },
    { heading: "5. Campaign & Promo Calendar", content: "Aug 15–17: Weekend flash sale — 15% off all fragrances\nAug 22: GWP launch — free mini with orders over Rs. 10,000\nSMS blast: Aug 14 (sale teaser), Aug 16 (last chance)" },
    { heading: "6. Asset Checklist", content: "Images needed: 3 reels, 8 static posts, 15 story slides\nCopy needed: All captions, email newsletter, SMS\nStatus: [ ] In Progress  [ ] Ready for Review  [ ] Approved" }
  ]
  page_size: "A4"
  orientation: "portrait"
  upload: true
}
```

#### 2. Campaign Brief (One-Page)

```
pro_pdf_document {
  operation: "generate"
  description: "A clean, professional one-page campaign brief for The Parfumerie.
  Dark navy header with gold accent. Sections: Campaign Name, Dates, Theme,
  Hero Products (with prices), Content Plan (reels + statics + stories),
  Success Metrics. Modern luxury aesthetic. Footer with brand logo space."
  title: "Campaign Brief — August 2026"
  page_size: "A4"
}
```

#### 3. Analytics Report

```
pro_pdf_document {
  operation: "structure"
  title: "July 2026 — Monthly Performance Report"
  author: "Sophie — Digital Marketing"
  sections: [
    { heading: "Executive Summary", content: "July revenue: Rs. XXX,XXX (+12% MoM). Top performer: Instagram Reels (3.2% engagement). Slow mover flagged: SKU CN29." },
    { heading: "Social Media Performance", content: "Instagram: 24 posts, 45K reach, 2.8% engagement\nFacebook: 12 posts, 18K reach, 1.2% engagement\nTop post: Reel — 'Date Night Scent' (12K reach, 4.1% engagement)" },
    { heading: "E-Commerce Dashboard", content: "Total orders: 47\nRevenue: Rs. XXX,XXX\nAOV: Rs. X,XXX\nTop seller: Carolina Herrera Good Girl (8 units)\nSlowest: CN29 (0 units in 60 days — action needed)" },
    { heading: "Product Velocity", content: "Fast: Carolina Herrera Good Girl (2.0 units/week)\nHealthy: Hyaluronic Acid Shampoo (0.8 units/week)\nSlow: CN29 Lavender Face Wash (0.0 units/week — feature in August)" },
    { heading: "Learnings & Next Month", content: "Keep: Friday 6 PM reels (highest engagement)\nStop: Static posts on Monday mornings (lowest reach)\nTry: Carousel format for product comparisons" }
  ]
}
```

## `pro_word_document` — Editable Documents

Creates .docx files that recipients can edit — ideal for collaborative drafts, templates, and client-facing documents.

### Parameters

```
operation    — "generate", "structure", "format", "template"
description  — Natural language description
content      — Text or structured content
title        — Document title
author       — Author metadata
sections     — Array of { heading, content, level }
formatting   — { font_size, font_family, color, bold, italic }
template     — "business_letter", "report", "resume", "memo", "proposal"
orientation  — "portrait" or "landscape"
page_margins — { top, bottom, left, right } in inches
upload       — Upload to media library (default: true)
```

### When to Use Word vs PDF

| Scenario | Format |
|---|---|
| Final presentation, sharing with stakeholders | PDF (`pro_pdf_document`) |
| Collaborative draft, needs editing | Word (`pro_word_document`) |
| Printed handout, brand document | PDF |
| Template to reuse and adapt | Word |
| Monthly campaign deck (Step 7) | PDF |
| Team meeting agenda / notes | Word |

### Template Presets

```
business_letter — Formal correspondence, supplier communications
report          — Analytics reports, performance summaries
memo            — Internal communications, quick updates
proposal        — Campaign proposals, partnership pitches
```

### Example: Campaign Proposal

```
pro_word_document {
  operation: "template"
  template: "proposal"
  title: "Q3 Fragrance Campaign Proposal — The Parfumerie"
  author: "Sophie"
  description: "A proposal for a Q3 multi-channel fragrance campaign targeting
  Sri Lankan luxury buyers aged 25–45. Includes Instagram/Facebook strategy,
  email sequence, influencer collaboration plan, and projected ROI."
  upload: true
}
```

## Simple Document Tools

For quick one-off documents without needing structured sections:

### `generate_pdf` — Quick PDF

```
generate_pdf {
  content: "Plain text or markdown content here..."
  title: "Quick Report"
}
```

### `generate_word` — Quick Word Doc

```
generate_word {
  content: "Plain text content..."
  title: "Meeting Notes"
}
```

### `generate_excel` — Quick Spreadsheet

```
generate_excel {
  data: "[{\"Product\":\"CH Good Girl\",\"Price\":27500,\"Stock\":6},...]"
  title: "Product Inventory — August 2026"
}
```

### `excel_data_export` — Structured Data Export

Exports arrays with headers to formatted .xlsx. Best for WooCommerce data exports or analytics:

```
excel_data_export {
  data: [
    ["CH Good Girl", 27500, 6, "instock"],
    ["CN29 Face Wash", 2750, 4, "instock"]
  ]
  headers: ["Product", "Price", "Stock", "Status"]
  title: "The Parfumerie — Product Stock Report"
  filename: "parfumerie-stock-august-2026"
}
```

## HTML to PDF

Convert HTML/CSS content directly to styled PDF — ideal for branded documents with custom formatting:

```
html_to_pdf {
  html: "<h1 style='color: #1a1a2e;'>Monthly Campaign Plan</h1><p>...</p>"
  title: "August 2026 Campaign Plan"
  filename: "campaign-plan-august"
  page_size: "a4"
  orientation: "portrait"
}
```

## Invoice Generation

Create professional branded invoices for clients or partner billing:

```
generate_invoice_pdf {
  invoice_number: "INV-2026-08-001"
  date: "2026-08-11"
  due_date: "2026-08-25"
  bill_to: { name: "Client Name", address: "Colombo, Sri Lanka" }
  items: [
    { description: "Monthly Marketing Retainer", quantity: 1, rate: 45000, amount: 45000 },
    { description: "Social Media Ad Management", quantity: 1, rate: 25000, amount: 25000 }
  ]
  subtotal: 70000
  tax_rate: 0
  total: 70000
  currency: "LKR"
}
```

## PDF Processing & OCR

### Extract Text from PDFs

Read and extract text from PDF documents for analysis or repurposing:

```
extract_pdf_text {
  attachment_id: 12345
  enable_ocr: true  // auto-detects scanned PDFs
  max_pages: 10
}
```

### OCR for Scanned Documents

Extract text from image-only or scanned PDFs:

```
ocr_pdf_text {
  url: "https://example.com/scanned-brochure.pdf"
  provider: "auto"
  preprocess: true  // enhances contrast for better accuracy
}
```

### Advanced Batch OCR

Process multiple documents with structured output:

```
pro_document_ocr {
  source: { urls: ["url1.pdf", "url2.pdf"] }
  options: { output_format: "markdown", preserve_layout: true }
}
```

## PDF Merging & Watermarking

### Combine Multiple PDFs

```
merge_pdfs {
  attachment_ids: [101, 102, 103]
  title: "August 2026 — Complete Campaign Package"
  filename: "parfumerie-august-campaign-bundle"
}
```

### Add Watermarks

```
add_watermark_to_pdf {
  attachment_id: 12345
  text: "THE PARFUMERIE — CONFIDENTIAL"
  opacity: 0.2
  position: "diagonal"
}
```

## Document Delivery Workflow

```
1. GENERATE
   pro_pdf_document or pro_word_document → returns attachment_id

2. REVIEW
   Download from WordPress Media Library → review content

3. SHARE
   Upload to Google Drive (see gws-drive skill)
   or
   Share WordPress attachment URL directly
   or
   Email as attachment
```

## Critical Rules

- **PDF for final, Word for drafts** — match the format to the recipient's needs.
- **Always set title and author** — metadata matters for professional documents.
- **Use `structure` operation with clear sections** — produces the most predictable, well-formatted output.
- **Upload to media library by default** — keeps documents accessible via WordPress.
- **One document per purpose** — don't try to make a single PDF serve as both a campaign deck and an analytics report.
- **Review before sharing** — always download and check formatting before sending.

## Common Mistakes

```
WRONG:
  ● Using Word for a final presentation (unintended edits, formatting shifts)
  ● No title or author set (document metadata shows "Untitled")
  ● Overly vague description in "generate" mode (unpredictable output)
  ● Forgetting to upload (can't find the file later)
  ● One massive document with 5 unrelated sections

RIGHT:
  ✅ PDF for final deliverables, Word for collaborative editing
  ✅ Title + author set on every document
  ✅ "structure" mode with clear heading/content pairs for predictable output
  ✅ upload: true (default) — file saved to Media Library
  ✅ One clear purpose per document
```

## What This Skill Does NOT Cover

- **Image generation** — use `design-image-generation` to create visuals for document inclusion.
- **Data analysis and reporting** — use `design-analytics-reporting` to compile metrics before generating report documents.
- **Campaign planning** — use `design-campaign-orchestration` to build the monthly plan before generating the deck.
- **Email delivery** — use `design-email-marketing` to send generated documents as email attachments.
- **CRM or project documents** — use `design-project-management` for project reports or `design-crm` for deal/client documents tied to CRM records.
- **Brand identity design** — use `design-brand-kit` for logo placement, brand colors, and typography in documents.

## Cross-references

- Run **`design-campaign-orchestration`** to build the monthly plan before generating the deck.
- Run **`design-analytics-reporting`** to compile metrics before generating a report document.
- Run **`design-product-research`** for product data that feeds into campaign documents.
- Run **`design-brand-kit`** to ensure document styling uses correct brand colors and fonts.
- Run **`gws-drive`** to upload generated documents to Google Drive "Approved" folders.
- Run **`design-project-management`** to generate project reports and task plans from `mcp_ai_project` and `mcp_ai_task` CPT records.
- Run **`design-crm`** to generate deal summaries, lead profiles, and customer-facing documents from CRM records.
