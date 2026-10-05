---
name: pdf-document-generation
description: Generate professional PDF documents programmatically using Python and JavaScript libraries with precise layout control, typography, and multi-format.
---

# PDF Document Generation

Structured guidance for generating professional PDF documents programmatically using Python and JavaScript libraries. Covers library selection, document layout, typography, tables, images, HTML-to-PDF conversion, advanced features like form fields and digital signatures, and testing strategies for validating PDF output across viewers and use cases.

## When to Use This Skill

Use this skill for:

- Building invoice, receipt, or statement generators from structured data
- Creating report rendering pipelines that produce PDF output
- Generating contracts, certificates, or legal documents from templates
- Converting HTML/CSS content to PDF with precise layout control
- Adding form fields, digital signatures, or encryption to PDF documents
- Implementing PDF/A archival compliance or accessibility tagging
- Building batch PDF generation systems for high-volume document workflows
- Testing and validating PDF output for content correctness and visual fidelity

**Trigger phrases**: "PDF generation", "generate PDF", "create PDF", "invoice PDF", "report PDF", "HTML to PDF", "WeasyPrint", "ReportLab", "PDFKit", "Puppeteer PDF", "jsPDF", "PDF template", "PDF layout", "PDF forms", "digital signature", "PDF/A", "accessible PDF", "watermark", "table of contents PDF", "cover page"

## What This Skill Does

Provides PDF generation patterns including:

- **Library Selection**: Decision matrix for choosing between ReportLab, WeasyPrint, Puppeteer, PDFKit, and jsPDF based on project requirements
- **Python ReportLab**: Low-level PDF construction with platypus layouts, paragraph styles, tables, images, and multi-page templates
- **Python WeasyPrint**: HTML/CSS-to-PDF rendering with print media queries, custom stylesheets, and page break control
- **JavaScript PDFKit**: Node.js PDF generation with text, vector graphics, custom fonts, and streaming output
- **Puppeteer/Playwright**: Headless Chrome rendering for pixel-perfect HTML-to-PDF conversion with headers, footers, and waiting strategies
- **Document Design**: Cover pages, table of contents, page numbering, watermarks, bookmarks, and outline hierarchies
- **Advanced Features**: Form fields, digital signatures, PDF/A compliance, accessibility tagging, encryption, and permission controls
- **Testing and Validation**: Visual regression testing, content extraction for assertions, file size optimization, and cross-viewer compatibility

## Instructions

### Step 1: Library Selection Guide

Choosing the right PDF library depends on your language ecosystem, the complexity of your layouts, whether you need HTML/CSS input, and your deployment constraints. The following decision matrix covers the five most widely used libraries.

**Library Comparison Matrix**:

| Criterion | ReportLab (Python) | WeasyPrint (Python) | PDFKit (Node.js) | Puppeteer (Node.js) | jsPDF (Browser/Node) |
|---|---|---|---|---|---|
| Input format | Python API calls | HTML + CSS | JavaScript API calls | HTML + CSS | JavaScript API calls |
| Layout model | Absolute + flowable | CSS box model | Absolute positioning | Full browser rendering | Absolute positioning |
| Complex tables | Excellent | Good (HTML tables) | Manual positioning | Excellent (HTML tables) | Basic via plugin |
| Custom fonts | TTF embedding | WOFF/TTF via CSS | TTF/OTF embedding | System + web fonts | TTF embedding |
| Image support | PNG, JPEG, SVG | PNG, JPEG, SVG, GIF | PNG, JPEG | All browser formats | PNG, JPEG |
| PDF/A support | Yes (with pdfa module) | Limited | No | No | No |
| Form fields | Yes | No | No | No | No (plugin: AcroForm) |
| File size | Small (vector-native) | Medium | Small (vector-native) | Large (rasterized content) | Small |
| Server dependency | None | Cairo, Pango, GDK-Pixbuf | None | Headless Chromium (~300 MB) | None |
| Learning curve | Steep | Low (if you know CSS) | Moderate | Low (if you know HTML/CSS) | Moderate |
| Best for | Data-heavy reports, forms | Styled documents from HTML | Server-side Node.js docs | Pixel-perfect web-to-PDF | Client-side generation |

**Decision Flowchart**:

1. **Is the source content already HTML/CSS?** If yes, choose WeasyPrint (Python) or Puppeteer (Node.js). WeasyPrint is lighter weight and produces smaller files. Puppeteer handles JavaScript-rendered content and complex CSS (flexbox, grid).
2. **Do you need PDF form fields or PDF/A compliance?** If yes, choose ReportLab. It is the only library in this list with native support for both.
3. **Are you running in a browser environment?** If yes, choose jsPDF. It runs entirely client-side without a server round-trip.
4. **Do you need precise programmatic control over every element?** If yes, choose ReportLab (Python) or PDFKit (Node.js) depending on your language. Both offer coordinate-level placement.
5. **Do you need to render charts or dashboards that already exist as web pages?** If yes, choose Puppeteer or Playwright. They render exactly what a browser would show.

**Installation**:

```bash
# Python: ReportLab
pip install reportlab

# Python: WeasyPrint (requires system dependencies on Linux)
pip install weasyprint
# Debian/Ubuntu: apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0

# Node.js: PDFKit
npm install pdfkit

# Node.js: Puppeteer (downloads Chromium automatically)
npm install puppeteer

# Browser/Node.js: jsPDF
npm install jspdf
```

### Step 2: Python ReportLab Fundamentals

ReportLab provides two layers: a low-level canvas API for absolute positioning and a high-level "platypus" (Page Layout and Typography Using Scripts) framework for flowable document construction. Production systems almost always use platypus because it handles page breaks, text wrapping, and multi-page layouts automatically.

**Basic Document with Platypus**:

```python
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from pathlib import Path


def create_invoice(
    invoice_number: str,
    client_name: str,
    line_items: list[dict],
    output_path: str | Path,
) -> None:
    """Generate a professional invoice PDF.

    Each line_item dict has keys: description, quantity, unit_price, total.
    """
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=HexColor("#1a1a2e"),
        spaceAfter=6 * mm,
    )
    header_style = ParagraphStyle(
        "InvoiceHeader",
        parent=styles["Normal"],
        fontSize=10,
        textColor=HexColor("#555555"),
        spaceAfter=2 * mm,
    )
    body_style = ParagraphStyle(
        "InvoiceBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
    )

    elements: list = []

    # Company header
    elements.append(Paragraph("ACME Corporation", title_style))
    elements.append(Paragraph("123 Business Ave, Suite 100", header_style))
    elements.append(Paragraph("contact@acme.example.com", header_style))
    elements.append(Spacer(1, 10 * mm))

    # Invoice metadata
    elements.append(Paragraph(f"Invoice #{invoice_number}", styles["Heading2"]))
    elements.append(Paragraph(f"Bill to: {client_name}", body_style))
    elements.append(Spacer(1, 8 * mm))

    # Line items table
    table_data = [["Description", "Qty", "Unit Price", "Total"]]
    for item in line_items:
        table_data.append([
            item["description"],
            str(item["quantity"]),
            f"${item['unit_price']:.2f}",
            f"${item['total']:.2f}",
        ])

    # Summary row
    grand_total = sum(item["total"] for item in line_items)
    table_data.append(["", "", "Grand Total:", f"${grand_total:.2f}"])

    table = Table(table_data, colWidths=[80 * mm, 20 * mm, 30 * mm, 30 * mm])
    table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        # Body rows
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [HexColor("#f8f8f8"), HexColor("#ffffff")]),
        ("GRID", (0, 0), (-1, -2), 0.5, HexColor("#cccccc")),
        # Total row
        ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (2, -1), (-1, -1), 1.5, HexColor("#1a1a2e")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15 * mm))

    # Payment terms
    elements.append(Paragraph("Payment Terms", styles["Heading3"]))
    elements.append(Paragraph(
        "Payment is due within 30 days of invoice date. "
        "Please reference the invoice number in your payment.",
        body_style,
    ))

    doc.build(elements)
```

**Page Templates with Headers and Footers**:

```python
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import date


def header_footer(canvas, doc):
    """Draw header and footer on every page."""
    canvas.saveState()

    # Header: company name and horizontal rule
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(20 * mm, A4[1] - 15 * mm, "ACME Corporation")
    canvas.setStrokeColorRGB(0.1, 0.1, 0.18)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, A4[1] - 17 * mm, A4[0] - 20 * mm, A4[1] - 17 * mm)

    # Footer: page number and date
    canvas.setFont("Helvetica", 8)
    canvas.setFillColorRGB(0.4, 0.4, 0.4)
    canvas.drawString(20 * mm, 12 * mm, f"Generated {date.today().isoformat()}")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")

    canvas.restoreState()


def create_multi_page_report(output_path: str, content_elements: list) -> None:
    """Create a report with consistent headers and footers on every page."""
    doc = BaseDocTemplate(output_path, pagesize=A4)

    frame = Frame(
        20 * mm,                    # x
        20 * mm,                    # y
        A4[0] - 40 * mm,           # width
        A4[1] - 50 * mm,           # height (leaves room for header/footer)
        id="main_frame",
    )

    template = PageTemplate(
        id="standard",
        frames=[frame],
        onPage=header_footer,
    )
    doc.addPageTemplates([template])
    doc.build(content_elements)
```

**Embedding Images**:

```python
from reportlab.platypus import Image
from reportlab.lib.units import mm

# From file path
logo = Image("assets/logo.png", width=40 * mm, height=15 * mm)

# From URL or bytes (wrap in BytesIO)
from io import BytesIO
import httpx

response = httpx.get("https://example.com/chart.png", timeout=30)
chart_image = Image(BytesIO(response.content), width=160 * mm, height=100 * mm)
```

**Custom Fonts**:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a TrueType font family
pdfmetrics.registerFont(TTFont("Inter", "fonts/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "fonts/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Italic", "fonts/Inter-Italic.ttf"))

# Map font family for automatic bold/italic selection in paragraphs
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Inter", normal="Inter", bold="Inter-Bold", italic="Inter-Italic")

# Use in ParagraphStyle
style = ParagraphStyle("CustomBody", fontName="Inter", fontSize=10, leading=14)
```

### Step 3: Python WeasyPrint (HTML/CSS to PDF)

WeasyPrint converts HTML and CSS into PDF using the CSS Paged Media specification. If your document content is already structured as HTML (or can be rendered from a template engine like Jinja2), WeasyPrint produces high-quality PDF output with minimal code.

**Basic HTML-to-PDF Conversion**:

```python
import weasyprint
from pathlib import Path


def html_string_to_pdf(html_content: str, output_path: str | Path) -> None:
    """Convert an HTML string to PDF."""
    doc = weasyprint.HTML(string=html_content)
    doc.write_pdf(str(output_path))


def html_file_to_pdf(html_path: str | Path, output_path: str | Path) -> None:
    """Convert an HTML file to PDF, resolving relative asset paths."""
    doc = weasyprint.HTML(filename=str(html_path))
    doc.write_pdf(str(output_path))


def url_to_pdf(url: str, output_path: str | Path) -> None:
    """Convert a web page to PDF."""
    doc = weasyprint.HTML(url=url)
    doc.write_pdf(str(output_path))
```

**Jinja2 Template Rendering with WeasyPrint**:

```python
from jinja2 import Environment, FileSystemLoader
import weasyprint
from pathlib import Path
from decimal import Decimal


def render_invoice_pdf(
    template_dir: str | Path,
    invoice_data: dict,
    output_path: str | Path,
) -> None:
    """Render an invoice from a Jinja2 HTML template to PDF.

    invoice_data keys: number, date, client_name, client_address,
                       line_items (list of dicts), total.
    """
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("invoice.html")
    html_content = template.render(**invoice_data)

    # Base URL allows WeasyPrint to resolve relative CSS/image paths
    base_url = str(Path(template_dir).resolve())
    doc = weasyprint.HTML(string=html_content, base_url=base_url)
    doc.write_pdf(str(output_path))
```

**Invoice HTML Template** (`invoice.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    @page {
      size: A4;
      margin: 20mm 20mm 25mm 20mm;

      @top-right {
        content: "Invoice #{{ number }}";
        font-size: 8pt;
        color: #888;
      }
      @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #888;
      }
    }

    body {
      font-family: "Helvetica Neue", Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.5;
      color: #1a1a2e;
    }

    .header { margin-bottom: 20mm; }
    .header h1 { font-size: 22pt; margin: 0; }
    .header .subtitle { color: #666; font-size: 9pt; }

    table.line-items {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10mm;
    }
    table.line-items th {
      background: #1a1a2e;
      color: white;
      padding: 6px 10px;
      text-align: left;
      font-size: 9pt;
    }
    table.line-items td {
      padding: 6px 10px;
      border-bottom: 0.5px solid #ddd;
      font-size: 9pt;
    }
    table.line-items tr:nth-child(even) td {
      background: #f8f8f8;
    }
    .text-right { text-align: right; }
    .total-row td {
      font-weight: bold;
      border-top: 2px solid #1a1a2e;
      border-bottom: none;
    }

    .terms {
      margin-top: 15mm;
      font-size: 9pt;
      color: #555;
      page-break-inside: avoid;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>ACME Corporation</h1>
    <p class="subtitle">123 Business Ave, Suite 100</p>
  </div>

  <p><strong>Invoice #{{ number }}</strong> &mdash; {{ date }}</p>
  <p>Bill to: {{ client_name }}<br>{{ client_address }}</p>

  <table class="line-items">
    <thead>
      <tr>
        <th>Description</th>
        <th class="text-right">Qty</th>
        <th class="text-right">Unit Price</th>
        <th class="text-right">Total</th>
      </tr>
    </thead>
    <tbody>
      {% for item in line_items %}
      <tr>
        <td>{{ item.description }}</td>
        <td class="text-right">{{ item.quantity }}</td>
        <td class="text-right">${{ "%.2f"|format(item.unit_price) }}</td>
        <td class="text-right">${{ "%.2f"|format(item.total) }}</td>
      </tr>
      {% endfor %}
      <tr class="total-row">
        <td colspan="3" class="text-right">Grand Total:</td>
        <td class="text-right">${{ "%.2f"|format(total) }}</td>
      </tr>
    </tbody>
  </table>

  <div class="terms">
    <p><strong>Payment Terms:</strong> Net 30 days. Please reference invoice number in payment.</p>
  </div>
</body>
</html>
```

**CSS Paged Media Features**:

```css
/* Force page breaks before specific elements */
h1.chapter-title {
  page-break-before: always;
}

/* Prevent orphaned content */
p {
  orphans: 3;
  widows: 3;
}

/* Avoid breaking inside a table row or figure */
tr, figure {
  page-break-inside: avoid;
}

/* Named pages for different sections */
@page cover {
  margin: 0;
  @top-right { content: none; }
  @bottom-center { content: none; }
}
.cover-page {
  page: cover;
}

/* Landscape pages for wide tables */
@page landscape {
  size: A4 landscape;
}
.wide-table-section {
  page: landscape;
}

/* Print-specific adjustments */
@media print {
  nav, .no-print { display: none; }
  a[href]::after { content: " (" attr(href) ")"; font-size: 8pt; color: #666; }
}
```

**Custom Stylesheets as Separate Files**:

```python
import weasyprint

def html_to_pdf_with_styles(
    html_content: str,
    css_paths: list[str],
    output_path: str,
) -> None:
    """Convert HTML to PDF with external stylesheets."""
    stylesheets = [weasyprint.CSS(filename=path) for path in css_paths]
    doc = weasyprint.HTML(string=html_content)
    doc.write_pdf(output_path, stylesheets=stylesheets)
```

### Step 4: JavaScript PDFKit (Node.js)

PDFKit is a JavaScript library for creating PDF documents in Node.js and the browser. It uses a coordinate-based drawing model similar to ReportLab's canvas API, with support for text, vector graphics, images, and custom fonts.

**Basic Document Creation**:

```javascript
const PDFDocument = require("pdfkit");
const fs = require("fs");

function createInvoice(invoiceData, outputPath) {
  const doc = new PDFDocument({
    size: "A4",
    margins: { top: 72, bottom: 72, left: 72, right: 72 },
    info: {
      Title: `Invoice ${invoiceData.number}`,
      Author: "ACME Corporation",
      Subject: "Invoice",
      CreationDate: new Date(),
    },
  });

  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  // Company header
  doc
    .fontSize(22)
    .fillColor("#1a1a2e")
    .text("ACME Corporation", { align: "left" });
  doc
    .fontSize(9)
    .fillColor("#666666")
    .text("123 Business Ave, Suite 100")
    .text("contact@acme.example.com")
    .moveDown(2);

  // Invoice metadata
  doc
    .fontSize(14)
    .fillColor("#1a1a2e")
    .text(`Invoice #${invoiceData.number}`)
    .fontSize(10)
    .fillColor("#333333")
    .text(`Bill to: ${invoiceData.clientName}`)
    .text(`Date: ${invoiceData.date}`)
    .moveDown(1.5);

  // Table header
  const tableTop = doc.y;
  const col = { desc: 72, qty: 340, price: 400, total: 470 };

  doc
    .rect(72, tableTop, 468, 20)
    .fill("#1a1a2e");
  doc
    .fontSize(9)
    .fillColor("#ffffff")
    .text("Description", col.desc + 6, tableTop + 5)
    .text("Qty", col.qty, tableTop + 5, { width: 50, align: "right" })
    .text("Unit Price", col.price, tableTop + 5, { width: 60, align: "right" })
    .text("Total", col.total, tableTop + 5, { width: 60, align: "right" });

  // Table rows
  let rowY = tableTop + 24;
  doc.fillColor("#333333").fontSize(9);

  for (const [index, item] of invoiceData.lineItems.entries()) {
    const bgColor = index % 2 === 0 ? "#f8f8f8" : "#ffffff";
    doc.rect(72, rowY - 3, 468, 18).fill(bgColor);
    doc
      .fillColor("#333333")
      .text(item.description, col.desc + 6, rowY)
      .text(String(item.quantity), col.qty, rowY, { width: 50, align: "right" })
      .text(`$${item.unitPrice.toFixed(2)}`, col.price, rowY, { width: 60, align: "right" })
      .text(`$${item.total.toFixed(2)}`, col.total, rowY, { width: 60, align: "right" });
    rowY += 20;
  }

  // Total row
  doc
    .strokeColor("#1a1a2e")
    .lineWidth(1.5)
    .moveTo(col.price, rowY)
    .lineTo(540, rowY)
    .stroke();
  rowY += 6;
  doc
    .fontSize(10)
    .font("Helvetica-Bold")
    .text("Grand Total:", col.price, rowY, { width: 60, align: "right" })
    .text(`$${invoiceData.total.toFixed(2)}`, col.total, rowY, { width: 60, align: "right" });

  doc.end();

  return new Promise((resolve, reject) => {
    stream.on("finish", resolve);
    stream.on("error", reject);
  });
}
```

**Custom Fonts and Unicode**:

```javascript
const PDFDocument = require("pdfkit");
const fs = require("fs");
const path = require("path");

function createDocumentWithCustomFonts(outputPath) {
  const doc = new PDFDocument({ size: "A4" });
  doc.pipe(fs.createWriteStream(outputPath));

  // Register custom font families
  const fontsDir = path.join(__dirname, "fonts");
  doc.registerFont("Inter", path.join(fontsDir, "Inter-Regular.ttf"));
  doc.registerFont("Inter-Bold", path.join(fontsDir, "Inter-Bold.ttf"));
  doc.registerFont("Inter-Italic", path.join(fontsDir, "Inter-Italic.ttf"));
  doc.registerFont("NotoSansCJK", path.join(fontsDir, "NotoSansCJK-Regular.ttc"));

  // Use custom fonts
  doc.font("Inter-Bold").fontSize(18).text("Project Report");
  doc.font("Inter").fontSize(10).text("This document uses embedded Inter font.");

  // Unicode content (CJK characters require an appropriate font)
  doc.font("NotoSansCJK").fontSize(12).text("Japanese: PDF generation guide");

  doc.end();
}
```

**Vector Graphics**:

```javascript
function drawChart(doc, x, y, width, height, data) {
  // Background
  doc.rect(x, y, width, height).fill("#f0f0f0");

  // Simple bar chart
  const barWidth = (width - 20) / data.length - 5;
  const maxValue = Math.max(...data.map((d) => d.value));
  const chartHeight = height - 40;

  for (const [index, item] of data.entries()) {
    const barHeight = (item.value / maxValue) * chartHeight;
    const barX = x + 10 + index * (barWidth + 5);
    const barY = y + height - 20 - barHeight;

    doc.rect(barX, barY, barWidth, barHeight).fill(item.color || "#3366cc");

    // Label below bar
    doc
      .fontSize(7)
      .fillColor("#333")
      .text(item.label, barX, y + height - 15, {
        width: barWidth,
        align: "center",
      });
  }
}
```

**Streaming PDF to HTTP Response** (Express.js):

```javascript
const PDFDocument = require("pdfkit");

app.get("/api/invoices/:id/pdf", async (req, res) => {
  const invoice = await invoiceService.findById(req.params.id);
  if (!invoice) {
    return res.status(404).json({ error: "Invoice not found" });
  }

  res.setHeader("Content-Type", "application/pdf");
  res.setHeader(
    "Content-Disposition",
    `attachment; filename="invoice-${invoice.number}.pdf"`
  );

  const doc = new PDFDocument({ size: "A4" });
  doc.pipe(res);

  // Build document content...
  doc.fontSize(20).text(`Invoice #${invoice.number}`);
  // ... (rest of invoice rendering)

  doc.end();
});
```

### Step 5: Puppeteer/Playwright HTML-to-PDF

Puppeteer and Playwright launch a headless Chromium browser to render HTML and convert it to PDF. This approach produces pixel-perfect output that matches what a user sees in a browser, making it ideal for rendering complex layouts, charts (Chart.js, D3), and JavaScript-dependent content.

**Basic Puppeteer PDF Generation**:

```javascript
const puppeteer = require("puppeteer");

async function htmlToPdf(htmlContent, outputPath, options = {}) {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();
    await page.setContent(htmlContent, { waitUntil: "networkidle0" });

    await page.pdf({
      path: outputPath,
      format: "A4",
      printBackground: true,
      margin: {
        top: "20mm",
        bottom: "25mm",
        left: "20mm",
        right: "20mm",
      },
      displayHeaderFooter: true,
      headerTemplate: `
        <div style="font-size:8px; color:#888; width:100%; padding:0 20mm;">
          <span style="float:left;">ACME Corporation</span>
          <span style="float:right;">Confidential</span>
        </div>`,
      footerTemplate: `
        <div style="font-size:8px; color:#888; width:100%; text-align:center; padding:0 20mm;">
          Page <span class="pageNumber"></span> of <span class="totalPages"></span>
        </div>`,
      ...options,
    });
  } finally {
    await browser.close();
  }
}
```

**URL-to-PDF with Wait Strategies**:

```javascript
const puppeteer = require("puppeteer");

async function urlToPdf(url, outputPath, waitOptions = {}) {
  const browser = await puppeteer.launch({ headless: "new" });

  try {
    const page = await browser.newPage();

    // Set viewport for consistent rendering
    await page.setViewport({ width: 1200, height: 800 });

    await page.goto(url, {
      waitUntil: waitOptions.waitUntil || "networkidle0",
      timeout: waitOptions.timeout || 30000,
    });

    // Wait for specific content to be rendered (useful for JS-heavy pages)
    if (waitOptions.waitForSelector) {
      await page.waitForSelector(waitOptions.waitForSelector, {
        timeout: 10000,
      });
    }

    // Wait for custom "ready" signal from the page
    if (waitOptions.waitForReadySignal) {
      await page.waitForFunction(
        () => window.__PDF_READY === true,
        { timeout: 15000 }
      );
    }

    // Inject print-specific CSS
    await page.addStyleTag({
      content: `
        @media print {
          nav, .sidebar, .no-print { display: none !important; }
          body { font-size: 10pt; }
          a { color: inherit; text-decoration: none; }
        }
      `,
    });

    await page.pdf({
      path: outputPath,
      format: "A4",
      printBackground: true,
      margin: { top: "20mm", bottom: "20mm", left: "15mm", right: "15mm" },
    });
  } finally {
    await browser.close();
  }
}
```

**Playwright Equivalent** (Playwright has a nearly identical API and supports Chromium, Firefox, and WebKit):

```javascript
const { chromium } = require("playwright");

async function playwrightHtmlToPdf(htmlContent, outputPath) {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.setContent(htmlContent, { waitUntil: "networkidle" });

  await page.pdf({
    path: outputPath,
    format: "A4",
    printBackground: true,
    margin: { top: "20mm", bottom: "25mm", left: "20mm", right: "20mm" },
    displayHeaderFooter: true,
    headerTemplate: "<div></div>",
    footerTemplate: `
      <div style="font-size:8px; color:#888; width:100%; text-align:center;">
        Page <span class="pageNumber"></span> of <span class="totalPages"></span>
      </div>`,
  });

  await browser.close();
}
```

**Reusing a Browser Instance** (performance optimization for batch generation):

```javascript
const puppeteer = require("puppeteer");

class PdfGenerator {
  constructor() {
    this._browser = null;
  }

  async initialize() {
    this._browser = await puppeteer.launch({
      headless: "new",
      args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"],
    });
  }

  async generatePdf(htmlContent, options = {}) {
    if (!this._browser) {
      throw new Error("Browser not initialized. Call initialize() first.");
    }

    const page = await this._browser.newPage();
    try {
      await page.setContent(htmlContent, { waitUntil: "networkidle0" });
      const pdfBuffer = await page.pdf({
        format: options.format || "A4",
        printBackground: true,
        margin: options.margin || {
          top: "20mm", bottom: "20mm", left: "20mm", right: "20mm",
        },
      });
      return pdfBuffer;
    } finally {
      await page.close();
    }
  }

  async shutdown() {
    if (this._browser) {
      await this._browser.close();
      this._browser = null;
    }
  }
}

// Usage in a batch pipeline
async function generateBatchInvoices(invoices, templateFn) {
  const generator = new PdfGenerator();
  await generator.initialize();

  try {
    for (const invoice of invoices) {
      const html = templateFn(invoice);
      const pdfBuffer = await generator.generatePdf(html);
      fs.writeFileSync(`invoices/invoice-${invoice.number}.pdf`, pdfBuffer);
    }
  } finally {
    await generator.shutdown();
  }
}
```

### Step 6: Document Design Patterns

Production PDF documents require structural elements beyond raw content: cover pages, tables of contents, page numbering, watermarks, and navigational bookmarks. These patterns apply across all libraries.

**Cover Page** (ReportLab):

```python
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER


def build_cover_page(elements: list, title: str, subtitle: str, author: str) -> None:
    """Append cover page elements to the document flow."""
    cover_title = ParagraphStyle(
        "CoverTitle",
        fontSize=36,
        fontName="Helvetica-Bold",
        textColor=HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        spaceAfter=10 * mm,
    )
    cover_subtitle = ParagraphStyle(
        "CoverSubtitle",
        fontSize=16,
        fontName="Helvetica",
        textColor=HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=20 * mm,
    )
    cover_author = ParagraphStyle(
        "CoverAuthor",
        fontSize=12,
        fontName="Helvetica",
        textColor=HexColor("#888888"),
        alignment=TA_CENTER,
    )

    elements.append(Spacer(1, 80 * mm))
    elements.append(Paragraph(title, cover_title))
    elements.append(Paragraph(subtitle, cover_subtitle))
    elements.append(Paragraph(f"Prepared by: {author}", cover_author))
    elements.append(PageBreak())
```

**Table of Contents** (ReportLab):

```python
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, TableOfContents,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_report_with_toc(output_path: str, chapters: list[dict]) -> None:
    """Generate a report with an auto-generated table of contents.

    Each chapter: {"title": str, "level": int, "content": list[Flowable]}
    """
    doc = BaseDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()

    # TOC styles for each heading level
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOCLevel0", fontName="Helvetica-Bold", fontSize=12,
            leftIndent=0, spaceBefore=6,
        ),
        ParagraphStyle(
            "TOCLevel1", fontName="Helvetica", fontSize=10,
            leftIndent=20, spaceBefore=3,
        ),
        ParagraphStyle(
            "TOCLevel2", fontName="Helvetica", fontSize=9,
            leftIndent=40, spaceBefore=2,
        ),
    ]

    frame = Frame(
        20 * mm, 20 * mm,
        A4[0] - 40 * mm, A4[1] - 50 * mm,
        id="main",
    )
    template = PageTemplate(id="standard", frames=[frame])
    doc.addPageTemplates([template])

    elements = []

    # TOC page
    elements.append(Paragraph("Table of Contents", styles["Heading1"]))
    elements.append(toc)
    elements.append(PageBreak())

    # Chapter content
    heading_styles = {
        0: ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18),
        1: ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14),
        2: ParagraphStyle("H3", parent=styles["Heading3"], fontSize=12),
    }

    for chapter in chapters:
        level = chapter.get("level", 0)
        heading = Paragraph(chapter["title"], heading_styles[level])
        # Notify the TOC about this heading
        doc.notify("TOCEntry", (level, chapter["title"], doc.page))
        elements.append(heading)
        elements.extend(chapter["content"])

    doc.multiBuild(elements)
```

**Watermarks** (ReportLab canvas-level):

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color


def add_watermark(canvas, doc, text="DRAFT", opacity=0.08):
    """Draw a diagonal watermark across the page."""
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 72)
    canvas.setFillColor(Color(0, 0, 0, alpha=opacity))
    canvas.translate(A4[0] / 2, A4[1] / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, text)
    canvas.restoreState()


def header_footer_with_watermark(canvas, doc):
    """Combined header, footer, and watermark callback."""
    add_watermark(canvas, doc, text="CONFIDENTIAL", opacity=0.06)
    # Add regular header/footer
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()
```

**Bookmarks and Outlines** (PDFKit):

```javascript
function addBookmarkedSections(doc, sections) {
  for (const section of sections) {
    // Create an outline entry (bookmark) pointing to the current position
    const outlineRef = doc.outline.addItem(section.title);

    doc
      .fontSize(18)
      .font("Helvetica-Bold")
      .text(section.title);

    doc
      .fontSize(10)
      .font("Helvetica")
      .text(section.body)
      .moveDown(2);

    // Nested bookmarks for subsections
    if (section.subsections) {
      for (const sub of section.subsections) {
        outlineRef.addItem(sub.title);
        doc.fontSize(14).font("Helvetica-Bold").text(sub.title);
        doc.fontSize(10).font("Helvetica").text(sub.body).moveDown(1);
      }
    }

    doc.addPage();
  }
}
```

**Page Numbering with "Page X of Y"** (Puppeteer):

Puppeteer's `footerTemplate` supports built-in CSS classes that are replaced at render time:

```javascript
const footerTemplate = `
  <div style="font-size:8px; color:#666; width:100%;
              text-align:center; padding: 5mm 0;">
    Page <span class="pageNumber"></span>
    of <span class="totalPages"></span>
  </div>`;

// Available template variables:
// <span class="date"></span>        - formatted print date
// <span class="title"></span>       - document title
// <span class="url"></span>         - document URL
// <span class="pageNumber"></span>  - current page number
// <span class="totalPages"></span>  - total page count
```

### Step 7: Advanced Features

Production PDF workflows often require interactive form fields, digital signatures for legal validity, archival-format compliance, accessibility for screen readers, and encryption for document security.

**PDF Form Fields** (ReportLab):

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as canvas_module


def create_form_pdf(output_path: str) -> None:
    """Create a PDF with interactive form fields."""
    c = canvas_module.Canvas(output_path, pagesize=A4)
    form = c.acroForm

    c.setFont("Helvetica", 12)
    c.drawString(20 * mm, A4[1] - 30 * mm, "Contract Agreement Form")

    # Text input field
    c.drawString(20 * mm, A4[1] - 50 * mm, "Full Name:")
    form.textfield(
        name="full_name",
        tooltip="Enter your full legal name",
        x=60 * mm,
        y=A4[1] - 53 * mm,
        width=100 * mm,
        height=8 * mm,
        borderStyle="inset",
        forceBorder=True,
    )

    # Checkbox
    c.drawString(20 * mm, A4[1] - 70 * mm, "I agree to the terms:")
    form.checkbox(
        name="agree_terms",
        tooltip="Check to agree",
        x=75 * mm,
        y=A4[1] - 73 * mm,
        size=5 * mm,
        buttonStyle="check",
        borderColor=None,
        fillColor=None,
        forceBorder=True,
    )

    # Dropdown selection
    c.drawString(20 * mm, A4[1] - 90 * mm, "Contract Type:")
    form.choice(
        name="contract_type",
        tooltip="Select contract type",
        options=["Fixed Price", "Time and Materials", "Retainer"],
        value="Fixed Price",
        x=60 * mm,
        y=A4[1] - 93 * mm,
        width=80 * mm,
        height=8 * mm,
        forceBorder=True,
    )

    # Date field (text input with format hint)
    c.drawString(20 * mm, A4[1] - 110 * mm, "Effective Date:")
    form.textfield(
        name="effective_date",
        tooltip="YYYY-MM-DD",
        x=60 * mm,
        y=A4[1] - 113 * mm,
        width=50 * mm,
        height=8 * mm,
        forceBorder=True,
    )

    # Multi-line text area
    c.drawString(20 * mm, A4[1] - 130 * mm, "Additional Notes:")
    form.textfield(
        name="notes",
        tooltip="Enter any additional notes",
        x=20 * mm,
        y=A4[1] - 170 * mm,
        width=170 * mm,
        height=30 * mm,
        fieldFlags="multiline",
        forceBorder=True,
    )

    c.save()
```

**Digital Signatures** (using pyHanko for PAdES-compliant signatures):

```python
from pyhanko.sign import signers, fields
from pyhanko.sign.general import load_cert_list
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pathlib import Path


def sign_pdf(
    input_path: str | Path,
    output_path: str | Path,
    pfx_path: str | Path,
    pfx_password: str,
    signer_name: str,
    reason: str = "Document approval",
    location: str = "Remote",
) -> None:
    """Apply a PAdES-B digital signature to a PDF document.

    Requires a PKCS#12 (.pfx/.p12) file containing the signing certificate
    and private key.
    """
    signer = signers.SimpleSigner.load_pkcs12(
        pfx_file=str(pfx_path),
        passphrase=pfx_password.encode(),
    )

    with open(input_path, "rb") as inf:
        writer = IncrementalPdfFileWriter(inf)

        # Add a signature field if one does not already exist
        fields.append_signature_field(
            writer,
            sig_field_spec=fields.SigFieldSpec(
                sig_field_name="Signature1",
                on_page=0,
                box=(50, 50, 250, 100),  # x1, y1, x2, y2 in PDF points
            ),
        )

        meta = signers.PdfSignatureMetadata(
            field_name="Signature1",
            name=signer_name,
            reason=reason,
            location=location,
        )

        with open(output_path, "wb") as outf:
            signers.sign_pdf(
                writer,
                signature_meta=meta,
                signer=signer,
                output=outf,
            )
```

**PDF/A Compliance** (ReportLab):

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdfa_document(output_path: str, content_elements: list) -> None:
    """Create a PDF/A-1b compliant document for long-term archival.

    PDF/A requirements:
    - All fonts must be embedded (ReportLab embeds by default with TTF)
    - No JavaScript or executable content
    - No encryption
    - Color spaces must be explicitly defined
    - XMP metadata is required
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        title="Archived Report",
        author="ACME Corporation",
        subject="Archival Document",
    )

    # ReportLab does not produce PDF/A natively.
    # Use reportlab + pikepdf or pdfa-pillar for post-processing:
    doc.build(content_elements)

    # Post-process with pikepdf to add PDF/A metadata
    import pikepdf

    with pikepdf.open(output_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta["dc:title"] = "Archived Report"
            meta["dc:creator"] = ["ACME Corporation"]
            meta["pdfaid:part"] = "1"
            meta["pdfaid:conformance"] = "B"
        pdf.save(output_path)
```

**Accessibility Tagging** (marked content for screen readers):

```python
def create_tagged_content(canvas, doc):
    """Add tagged (accessible) content to a PDF.

    Tagged PDF associates structural tags (H1, P, Table, etc.) with content,
    enabling screen readers to navigate the document logically.

    Note: Full tagged PDF support requires low-level PDF manipulation.
    For production accessible PDFs, WeasyPrint + post-processing or
    Puppeteer (which inherits HTML semantics) are more practical than
    hand-tagging with ReportLab.
    """
    # ReportLab canvas supports basic marked content
    canvas.beginMarkedContent("H1")
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(72, 750, "Quarterly Report")
    canvas.endMarkedContent()

    canvas.beginMarkedContent("P")
    canvas.setFont("Helvetica", 10)
    canvas.drawString(72, 720, "This section summarizes Q4 performance metrics.")
    canvas.endMarkedContent()
```

**Practical approach to accessible PDFs**: The most reliable way to produce accessible PDFs is to start with well-structured semantic HTML (proper heading hierarchy, table headers with `<th scope>`, alt text on images, `lang` attribute) and convert it to PDF using Puppeteer or WeasyPrint. The HTML semantics carry over into the PDF structure, producing a document that screen readers can navigate. Post-process with a tool like PAC (PDF Accessibility Checker) to verify WCAG compliance.

**Encryption and Permissions** (pikepdf):

```python
import pikepdf


def encrypt_pdf(
    input_path: str,
    output_path: str,
    user_password: str = "",
    owner_password: str = "",
    allow_printing: bool = True,
    allow_copying: bool = False,
    allow_modification: bool = False,
) -> None:
    """Encrypt a PDF with password protection and permission controls.

    user_password: required to open the document (empty string = no open password)
    owner_password: required to change permissions or remove encryption
    """
    permissions = pikepdf.Permissions(
        print_lowres=allow_printing,
        print_highres=allow_printing,
        extract=allow_copying,
        modify_annotation=allow_modification,
        modify_form=allow_modification,
        modify_assembly=allow_modification,
        modify_other=allow_modification,
    )

    with pikepdf.open(input_path) as pdf:
        pdf.save(
            output_path,
            encryption=pikepdf.Encryption(
                user=user_password,
                owner=owner_password,
                R=6,               # AES-256 encryption (PDF 2.0)
                allow=permissions,
            ),
        )
```

### Step 8: Testing and Validation

PDF output must be validated for content correctness, visual fidelity, file size, and cross-viewer compatibility. Unlike web pages, PDFs cannot be inspected in a browser DevTools panel, so you need specialized tools and strategies.

**Content Extraction for Assertions** (Python, using pdfplumber):

```python
import pdfplumber
from pathlib import Path


def extract_pdf_text(pdf_path: str | Path) -> str:
    """Extract all text content from a PDF for assertion testing."""
    text_parts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_pdf_tables(pdf_path: str | Path, page_number: int = 0) -> list[list]:
    """Extract table data from a specific page."""
    with pdfplumber.open(str(pdf_path)) as pdf:
        page = pdf.pages[page_number]
        tables = page.extract_tables()
        return tables


def get_pdf_metadata(pdf_path: str | Path) -> dict:
    """Extract PDF metadata (title, author, page count, dimensions)."""
    with pdfplumber.open(str(pdf_path)) as pdf:
        return {
            "page_count": len(pdf.pages),
            "metadata": pdf.metadata,
            "pages": [
                {
                    "width": page.width,
                    "height": page.height,
                    "page_number": page.page_number,
                }
                for page in pdf.pages
            ],
        }
```

**Pytest Fixtures and Assertions for PDF Content**:

```python
import pytest
from pathlib import Path
from decimal import Decimal


@pytest.fixture
def invoice_data():
    return {
        "number": "INV-2025-001",
        "client_name": "Globex Corporation",
        "line_items": [
            {"description": "Consulting", "quantity": 40, "unit_price": 150.00, "total": 6000.00},
            {"description": "Development", "quantity": 80, "unit_price": 200.00, "total": 16000.00},
        ],
        "total": 22000.00,
    }


@pytest.fixture
def generated_invoice(tmp_path, invoice_data):
    output_path = tmp_path / "test_invoice.pdf"
    create_invoice(
        invoice_number=invoice_data["number"],
        client_name=invoice_data["client_name"],
        line_items=invoice_data["line_items"],
        output_path=output_path,
    )
    return output_path


def test_invoice_contains_invoice_number(generated_invoice, invoice_data):
    text = extract_pdf_text(generated_invoice)
    assert invoice_data["number"] in text


def test_invoice_contains_client_name(generated_invoice, invoice_data):
    text = extract_pdf_text(generated_invoice)
    assert invoice_data["client_name"] in text


def test_invoice_contains_line_items(generated_invoice, invoice_data):
    text = extract_pdf_text(generated_invoice)
    for item in invoice_data["line_items"]:
        assert item["description"] in text


def test_invoice_contains_total(generated_invoice, invoice_data):
    text = extract_pdf_text(generated_invoice)
    formatted_total = f"${invoice_data['total']:,.2f}"
    assert formatted_total in text


def test_invoice_page_count(generated_invoice):
    meta = get_pdf_metadata(generated_invoice)
    assert meta["page_count"] == 1


def test_invoice_page_size_is_a4(generated_invoice):
    meta = get_pdf_metadata(generated_invoice)
    page = meta["pages"][0]
    # A4 in PDF points: 595.28 x 841.89 (allow small tolerance)
    assert abs(page["width"] - 595.28) < 1
    assert abs(page["height"] - 841.89) < 1


def test_invoice_file_size_is_reasonable(generated_invoice):
    size_kb = generated_invoice.stat().st_size / 1024
    assert size_kb < 500, f"Invoice PDF is {size_kb:.1f} KB, expected under 500 KB"
```

**Visual Regression Testing** (comparing rendered pages as images):

```python
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import hashlib


def pdf_to_images(pdf_path: str | Path, dpi: int = 150) -> list[Image.Image]:
    """Convert each PDF page to a PIL Image for visual comparison."""
    return convert_from_path(str(pdf_path), dpi=dpi)


def image_hash(image: Image.Image) -> str:
    """Compute a perceptual hash for quick equality checks."""
    # Resize to a small thumbnail and hash the pixel data
    thumb = image.resize((64, 64)).convert("L")
    return hashlib.sha256(thumb.tobytes()).hexdigest()


def compare_pdf_visual(
    actual_path: str | Path,
    expected_path: str | Path,
    dpi: int = 150,
    pixel_threshold: float = 0.01,
) -> list[dict]:
    """Compare two PDFs page by page and report visual differences.

    Returns a list of diffs. Empty list means the PDFs are visually identical.
    pixel_threshold: fraction of pixels that may differ (0.01 = 1%).
    """
    actual_images = pdf_to_images(actual_path, dpi)
    expected_images = pdf_to_images(expected_path, dpi)
    diffs = []

    if len(actual_images) != len(expected_images):
        diffs.append({
            "type": "page_count_mismatch",
            "actual": len(actual_images),
            "expected": len(expected_images),
        })
        return diffs

    for page_num, (actual_img, expected_img) in enumerate(
        zip(actual_images, expected_images), start=1
    ):
        if actual_img.size != expected_img.size:
            diffs.append({
                "type": "size_mismatch",
                "page": page_num,
                "actual": actual_img.size,
                "expected": expected_img.size,
            })
            continue

        # Pixel-level comparison
        import numpy as np
        actual_arr = np.array(actual_img)
        expected_arr = np.array(expected_img)
        diff_pixels = np.sum(actual_arr != expected_arr)
        total_pixels = actual_arr.size
        diff_ratio = diff_pixels / total_pixels

        if diff_ratio > pixel_threshold:
            diffs.append({
                "type": "visual_difference",
                "page": page_num,
                "diff_ratio": diff_ratio,
            })

    return diffs


def test_invoice_visual_regression(generated_invoice, tmp_path):
    """Compare generated invoice against a known-good reference PDF.

    To update the reference: copy a manually verified PDF to
    tests/fixtures/invoice_reference.pdf
    """
    reference_path = Path("tests/fixtures/invoice_reference.pdf")
    if not reference_path.exists():
        pytest.skip("No reference PDF found. Generate one and save to tests/fixtures/.")

    diffs = compare_pdf_visual(generated_invoice, reference_path)
    assert diffs == [], f"Visual differences detected: {diffs}"
```

**File Size Optimization Strategies**:

```python
import pikepdf


def optimize_pdf(input_path: str, output_path: str) -> dict:
    """Optimize a PDF for smaller file size.

    Returns a dict with before/after sizes.
    """
    original_size = Path(input_path).stat().st_size

    with pikepdf.open(input_path) as pdf:
        # Remove unused objects
        pdf.remove_unreferenced_resources()

        # Compress streams
        pdf.save(
            output_path,
            linearize=True,              # optimize for web viewing (fast first page)
            compress_streams=True,        # deflate all content streams
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            recompress_flate=True,        # recompress with better settings
        )

    optimized_size = Path(output_path).stat().st_size
    return {
        "original_bytes": original_size,
        "optimized_bytes": optimized_size,
        "reduction_pct": round(
            (1 - optimized_size / original_size) * 100, 1
        ),
    }
```

**Image Compression Within PDFs**: The single largest contributor to PDF file size is images. Before embedding images in a PDF, resize them to the target display resolution (typically 150-300 DPI at the printed size) and compress them as JPEG for photographs or PNG for diagrams with transparency. A 4000x3000 pixel photograph displayed at 100mm wide only needs ~590 pixels wide at 150 DPI. Embedding the full-resolution image wastes space without improving print quality.

```python
from PIL import Image as PILImage
from io import BytesIO


def prepare_image_for_pdf(
    image_path: str,
    max_width_mm: float,
    dpi: int = 150,
    jpeg_quality: int = 85,
) -> BytesIO:
    """Resize and compress an image for PDF embedding.

    Returns a BytesIO buffer containing the optimized JPEG.
    """
    target_width_px = int(max_width_mm / 25.4 * dpi)

    with PILImage.open(image_path) as img:
        # Only downscale, never upscale
        if img.width > target_width_px:
            ratio = target_width_px / img.width
            new_size = (target_width_px, int(img.height * ratio))
            img = img.resize(new_size, PILImage.LANCZOS)

        # Convert RGBA to RGB (JPEG does not support transparency)
        if img.mode == "RGBA":
            background = PILImage.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=jpeg_quality, optimize=True)
        buffer.seek(0)
        return buffer
```

**Cross-Viewer Compatibility Checklist**:

When validating PDF output, test in multiple viewers because each renderer has different capabilities and quirks:

| Viewer | Key Differences |
|---|---|
| Adobe Acrobat Reader | Full spec support; most reliable reference. Test form fields and signatures here. |
| Chrome/Edge built-in | No form fill support; limited annotation rendering. Tests basic layout and text. |
| Firefox built-in (pdf.js) | JavaScript-based renderer; may differ on complex gradients, transparency, and fonts. |
| Preview (macOS) | Good general rendering but may struggle with advanced features (JavaScript actions, certain form types). |
| Evince/Okular (Linux) | Poppler-based; handles most features well. Test Unicode and CJK font embedding here. |

**Automated validation script** (run as part of CI):

```python
import subprocess
from pathlib import Path


def validate_pdf_structure(pdf_path: str | Path) -> dict:
    """Validate PDF structure using QPDF (must be installed).

    QPDF checks for structural errors, linearization, and encryption status.
    Install: apt install qpdf (Linux), brew install qpdf (macOS).
    """
    result = subprocess.run(
        ["qpdf", "--check", str(pdf_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "valid": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def validate_pdf_a_compliance(pdf_path: str | Path) -> dict:
    """Validate PDF/A compliance using VeraPDF (must be installed).

    VeraPDF is the industry-standard open-source PDF/A validator.
    Install: https://verapdf.org/software/
    """
    result = subprocess.run(
        ["verapdf", "--format", "text", str(pdf_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return {
        "compliant": "PASS" in result.stdout,
        "output": result.stdout.strip(),
    }
```

**Summary of Testing Strategy**:

| Test Type | Tool | What It Validates |
|---|---|---|
| Content assertions | pdfplumber, PyMuPDF | Text, tables, metadata are present and correct |
| Visual regression | pdf2image + Pillow/numpy | Layout has not shifted between code changes |
| Structural validation | QPDF | PDF is well-formed and not corrupted |
| PDF/A compliance | VeraPDF | Meets archival standard requirements |
| Accessibility | PAC (PDF Accessibility Checker) | Screen reader compatibility, tag structure |
| File size | pathlib stat | Output stays within budget (avoids image bloat) |
| Cross-viewer | Manual spot-check matrix | Renders correctly in Acrobat, Chrome, Firefox, Preview |
