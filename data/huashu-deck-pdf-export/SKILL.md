---
name: huashu-deck-pdf-export
description: "PDF generation from web layouts. Use when exporting web layouts or dashboard reports directly to print or PDF format."
version: "2.0.0"
verified_date: 2026-04-29
category: core
---

# Web to PDF Export (Redesigned)

## Purpose
Generate high-fidelity, print-ready PDF layouts directly from the browser using strict CSS `@media print` rules.

## When to Use This Skill
Use when:
- Exporting dashboard analytics, tables, or structured reporting data to PDF/print.
- Injecting strict `@media print` CSS layers into web layouts.

Do NOT use when:
- The user asks for automated backend Puppeteer or Playwright scripting.

## Phase 1: Print-Stylesheet Enforcement
1. **Abandon Puppeteer Scripting**: Do not generate backend Node.js scraping scripts to render PDFs.
2. **CSS Print Media**: Inject a strict `@media print` CSS layer into the application.
3. **Break Controls**: Enforce `break-inside: avoid` on all major container blocks (cards, charts, tables) to prevent layout tearing across pages.
4. **Fixed Layouts**: Rely on strict A4/16:9 CSS aspect ratios combined with `page-break-before` and `page-break-after`.

## Output Format / Delivery
- High-fidelity `@media print` CSS stylesheets and native browser print triggers (`window.print()`).

## Behavior Rules
1. Never generate backend headless browser scrapers or scripts.
2. Reset all sticky/fixed headers to static within `@media print` to prevent layout bugs.
3. Abort output and self-reject if asked to write Puppeteer/Playwright scripts.

## Maintenance Notes
- Complete redesign from v1. Deprecated Puppeteer automation in favor of robust CSS `@media print` engineering.