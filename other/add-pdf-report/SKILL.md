---
name: add-pdf-report
description: Generate a branded Arabic PDF report from an HTML template using Puppeteer. Use for contracts, invoices, CMA reports, commission statements.
---

# add-pdf-report

Creates a new PDF report template with Arabic RTL support, org branding, and data binding. Uses Puppeteer to render HTML → PDF server-side.

## Inputs to gather

- **Report type** — e.g., "contract", "invoice", "cma-report", "commission-statement"
- **Data source** — which entity/query provides the data (dealId, propertyId, agentId + period)
- **Sections** — what the PDF contains (header, table, summary, footer, signatures)
- **Page size** — A4 (default) or custom

## Steps

1. **Check PDF engine exists.** Read `apps/api/libs/pdf-engine.ts`. If missing, create:
   ```typescript
   import puppeteer from "puppeteer";
   export async function generatePDF(html: string): Promise<Buffer> {
     const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox"] });
     const page = await browser.newPage();
     await page.setContent(html, { waitUntil: "networkidle0" });
     const pdf = await page.pdf({ format: "A4", printBackground: true });
     await browser.close();
     return Buffer.from(pdf);
   }
   ```

2. **Create the HTML template** at `apps/api/templates/{report-type}.ts`:
   - RTL direction: `<html dir="rtl" lang="ar">`
   - Font: IBM Plex Sans Arabic (embedded via base64 or CDN)
   - Org branding: logo, tradeName, licenseNo in header
   - CSS: print-optimized, no scrollbars, page-break-inside: avoid
   - Data binding: template literal with typed parameters

3. **Create the API endpoint:**
   ```typescript
   router.get("/documents/{type}/:entityId", authenticateToken, async (req, res) => {
     // Fetch data from Prisma
     // Render HTML template with data
     // Generate PDF
     res.setHeader("Content-Type", "application/pdf");
     res.setHeader("Content-Disposition", `attachment; filename="${type}-${entityId}.pdf"`);
     res.send(pdfBuffer);
   });
   ```

4. **Add frontend download button:**
   ```typescript
   const handleDownload = async () => {
     const blob = await apiGetBlob(`/api/documents/{type}/${entityId}`);
     const url = URL.createObjectURL(blob);
     const a = document.createElement("a");
     a.href = url; a.download = `${type}.pdf`; a.click();
   };
   ```

5. **Install Puppeteer** if not already: `pnpm add puppeteer`

## Verification checklist

- [ ] PDF renders correctly in Arabic (RTL text, proper font)
- [ ] Tables and numbers display correctly
- [ ] Org branding (logo, name, license) appears in header
- [ ] PDF downloads with correct filename
- [ ] Works with empty/null optional fields (graceful fallbacks)
- [ ] `/typecheck` passes

## Anti-patterns

- Don't use `@react-pdf/renderer` for complex layouts — Puppeteer handles Arabic RTL much better
- Don't generate PDFs synchronously on heavy endpoints — consider background job for large reports
- Don't embed large images as base64 in templates — use URLs or compress first
- Don't hardcode org info — always fetch from the database
