---
name: print-styles
description: Write print-friendly CSS using @media print. Use when creating printable pages, invoices, receipts, articles, or any content users might print.
allowed-tools: Read, Write, Edit
---

# Print Styles Skill

This skill provides patterns for creating print-friendly stylesheets using `@media print`. Print styles are often overlooked but essential for articles, invoices, documentation, and any content users might want to print.

## Philosophy

Print stylesheets should:

1. **Remove the unnecessary** - Navigation, ads, interactive elements
2. **Optimize for paper** - Black text on white, appropriate fonts
3. **Preserve content** - Don't hide essential information
4. **Save ink/toner** - Minimize backgrounds and decorative elements

---

## Basic Print Stylesheet

### Separate Print File

```html
<head>
  <!-- Screen styles -->
  <link rel="stylesheet" href="/css/main.css"/>

  <!-- Print styles: non-blocking, only loaded when printing -->
  <link rel="stylesheet" href="/css/print.css" media="print"/>
</head>
```

### Inline Print Block

```css
/* In your main stylesheet */
@media print {
  /* Print-specific styles */
}
```

### With CSS Layers

```css
/* main.css */
@layer reset, tokens, layout, components, pages, responsive, print;

@import "print.css" layer(print);
```

```css
/* print.css */
@layer print {
  @media print {
    /* All print styles */
  }
}
```

---

## Essential Print Resets

### Hide Non-Essential Elements

```css
@media print {
  /* Navigation and interaction */
  nav,
  header nav,
  .site-header,
  .site-footer,
  .sidebar,
  .navigation,
  .menu,
  .breadcrumb,
  [role="navigation"] {
    display: none !important;
  }

  /* Interactive elements */
  button,
  .btn,
  input,
  select,
  textarea,
  form,
  .search,
  .filter,
  .pagination,
  [role="button"] {
    display: none !important;
  }

  /* Ads and promotional */
  .ad,
  .advertisement,
  .banner,
  .popup,
  .modal,
  .cookie-notice,
  .newsletter-signup {
    display: none !important;
  }

  /* Media that doesn't print well */
  video,
  audio,
  iframe,
  .video-embed,
  .map-embed {
    display: none !important;
  }

  /* Skip links and a11y helpers for screen */
  .skip-link,
  .sr-only,
  .visually-hidden,
  [aria-hidden="true"] {
    display: none !important;
  }
}
```

### Reset Colors and Backgrounds

```css
@media print {
  /* Reset to print-friendly defaults */
  * {
    background: transparent !important;
    color: #000 !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }

  /* Preserve essential backgrounds */
  img,
  svg,
  .logo,
  .chart,
  .diagram {
    background: initial !important;
  }
}
```

---

## Typography for Print

### Print-Optimized Fonts

```css
@media print {
  body {
    /* Serif fonts are more readable in print */
    font-family: Georgia, 'Times New Roman', Times, serif;

    /* Larger base size for readability */
    font-size: 12pt;

    /* Tighter line height than screen */
    line-height: 1.4;

    /* Black text on white */
    color: #000;
    background: #fff;
  }

  h1, h2, h3, h4, h5, h6 {
    /* Sans-serif for headings provides contrast */
    font-family: 'Helvetica Neue', Arial, sans-serif;

    /* Ensure headings stay with content */
    page-break-after: avoid;
    break-after: avoid;
  }

  h1 { font-size: 24pt; }
  h2 { font-size: 18pt; }
  h3 { font-size: 14pt; }
  h4 { font-size: 12pt; }

  /* Code blocks */
  pre, code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 10pt;
  }
}
```

### Optimal Line Length

```css
@media print {
  /* Optimal reading width for print */
  article,
  .content,
  main {
    max-width: 6.5in; /* Standard letter with margins */
    margin: 0 auto;
  }

  p {
    /* Slightly tighter than screen */
    margin: 0 0 0.75em;

    /* Justify for clean edges */
    text-align: justify;

    /* Prevent orphans and widows */
    orphans: 3;
    widows: 3;
  }
}
```

---

## Page Layout

### Page Margins

```css
@media print {
  @page {
    /* Standard margins */
    margin: 0.75in;

    /* Or specific margins */
    margin-top: 1in;
    margin-bottom: 0.75in;
    margin-left: 0.75in;
    margin-right: 0.75in;
  }

  /* First page might need different margins */
  @page :first {
    margin-top: 1.5in;
  }

  /* Left and right pages for booklet printing */
  @page :left {
    margin-left: 1in;
    margin-right: 0.5in;
  }

  @page :right {
    margin-left: 0.5in;
    margin-right: 1in;
  }
}
```

### Page Size

```css
@media print {
  @page {
    /* US Letter */
    size: letter portrait;
    /* or: size: 8.5in 11in; */

    /* A4 */
    /* size: A4 portrait; */

    /* Landscape */
    /* size: letter landscape; */
  }

  /* Force specific elements to landscape */
  .wide-table {
    page: landscape;
  }

  @page landscape {
    size: letter landscape;
  }
}
```

---

## Page Breaks

### Controlling Page Breaks

```css
@media print {
  /* Always start sections on new page */
  section,
  article,
  .chapter {
    page-break-before: always;
    break-before: page;
  }

  /* Don't break inside these elements */
  figure,
  table,
  blockquote,
  pre,
  .card,
  .testimonial {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Keep headings with following content */
  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;
    break-after: avoid;
  }

  /* Keep images with captions */
  figure {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Don't break after images */
  img {
    page-break-after: avoid;
    break-after: avoid;
  }
}
```

### Modern Break Properties

```css
@media print {
  /* Modern break properties (preferred) */
  .new-section {
    break-before: page;     /* Start on new page */
  }

  .keep-together {
    break-inside: avoid;    /* Don't split this element */
  }

  h2 {
    break-after: avoid;     /* Keep heading with content */
  }

  /* Values: auto | avoid | always | all | page | left | right | recto | verso */
}
```

---

## Links in Print

### Show URLs

```css
@media print {
  /* Show URL after link text */
  a[href]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    font-weight: normal;
    color: #666;
  }

  /* Don't show URL for internal links */
  a[href^="#"]::after,
  a[href^="javascript:"]::after {
    content: "";
  }

  /* Don't show URL for image links */
  a[href] img::after {
    content: "";
  }

  /* Abbreviate long URLs */
  a[href*="://"]:not([href*="yourdomain.com"])::after {
    content: " (external link)";
  }
}
```

### Link Styling

```css
@media print {
  a {
    color: #000 !important;
    text-decoration: underline;
  }

  /* Remove link styling for navigation that's hidden anyway */
  nav a::after {
    content: "" !important;
  }
}
```

---

## Tables for Print

### Print-Optimized Tables

```css
@media print {
  table {
    width: 100%;
    border-collapse: collapse;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  thead {
    /* Repeat header on each page */
    display: table-header-group;
  }

  tfoot {
    /* Keep footer at bottom */
    display: table-footer-group;
  }

  tr {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  th, td {
    border: 1px solid #000;
    padding: 0.25em 0.5em;
    text-align: left;
  }

  th {
    background: #eee !important;
    font-weight: bold;
  }

  /* Zebra stripes for readability */
  tbody tr:nth-child(even) {
    background: #f5f5f5 !important;
  }
}
```

### Wide Tables

```css
@media print {
  /* Reduce font size for wide tables */
  .data-table {
    font-size: 9pt;
  }

  /* Or rotate wide tables to landscape */
  .wide-table {
    page: landscape;
  }
}
```

---

## Images for Print

### Image Handling

```css
@media print {
  img {
    max-width: 100% !important;
    height: auto !important;

    /* Don't break images across pages */
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Ensure images print */
  img {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Hide decorative images */
  img[alt=""],
  img:not([alt]),
  .decorative-image,
  .background-image {
    display: none !important;
  }

  /* Show essential images */
  img.logo,
  img.chart,
  img.diagram,
  figure img {
    display: block !important;
  }
}
```

### Charts and Diagrams

```css
@media print {
  /* Force color printing for charts */
  .chart,
  .diagram,
  .graph {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Ensure SVG prints */
  svg {
    max-width: 100%;
    height: auto;
  }
}
```

---

## Invoices and Documents

### Invoice Template

```css
@media print {
  /* Invoice header */
  .invoice-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2em;
    padding-bottom: 1em;
    border-bottom: 2px solid #000;
  }

  .invoice-logo {
    max-width: 200px;
  }

  .invoice-details {
    text-align: right;
  }

  /* Address blocks */
  .address-block {
    margin-bottom: 2em;
  }

  .address-block h3 {
    font-size: 10pt;
    text-transform: uppercase;
    margin-bottom: 0.5em;
  }

  /* Line items table */
  .invoice-items {
    width: 100%;
    margin: 2em 0;
  }

  .invoice-items th {
    background: #000 !important;
    color: #fff !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .invoice-items .amount {
    text-align: right;
  }

  /* Totals */
  .invoice-totals {
    float: right;
    width: 250px;
  }

  .invoice-totals tr:last-child {
    font-weight: bold;
    font-size: 14pt;
  }

  /* Footer */
  .invoice-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 9pt;
    color: #666;
    padding-top: 1em;
    border-top: 1px solid #ccc;
  }
}
```

### Receipt Template

```css
@media print {
  @page receipt {
    size: 80mm auto; /* Thermal receipt width */
    margin: 5mm;
  }

  .receipt {
    page: receipt;
    font-family: 'Courier New', monospace;
    font-size: 10pt;
    width: 70mm;
  }

  .receipt-header {
    text-align: center;
    margin-bottom: 1em;
  }

  .receipt-items {
    width: 100%;
  }

  .receipt-items td {
    padding: 2px 0;
  }

  .receipt-total {
    border-top: 1px dashed #000;
    margin-top: 0.5em;
    padding-top: 0.5em;
    font-weight: bold;
  }

  .receipt-footer {
    text-align: center;
    margin-top: 1em;
    font-size: 9pt;
  }
}
```

---

## Articles and Blog Posts

### Article Print Styles

```css
@media print {
  /* Article layout */
  article {
    max-width: 6in;
    margin: 0 auto;
  }

  /* Article header */
  article header {
    margin-bottom: 2em;
    padding-bottom: 1em;
    border-bottom: 1px solid #000;
  }

  article h1 {
    font-size: 28pt;
    margin-bottom: 0.25em;
  }

  .article-meta {
    font-size: 10pt;
    color: #666;
  }

  /* Author info */
  .author {
    display: flex;
    align-items: center;
    gap: 1em;
    margin: 1em 0;
  }

  .author-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
  }

  /* Hide social sharing */
  .share-buttons,
  .social-links,
  .related-posts,
  .comments {
    display: none !important;
  }

  /* Pull quotes */
  blockquote {
    font-size: 14pt;
    font-style: italic;
    margin: 1.5em 0;
    padding-left: 1em;
    border-left: 3px solid #000;
  }

  /* Code blocks */
  pre {
    background: #f5f5f5 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    padding: 1em;
    font-size: 9pt;
    overflow: visible;
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  /* Footnotes */
  .footnotes {
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px solid #ccc;
    font-size: 10pt;
  }
}
```

---

## Testing Print Styles

### Browser DevTools

1. **Chrome**: DevTools → More tools → Rendering → Emulate CSS media type: print
2. **Firefox**: DevTools → Toggle print media simulation
3. **Safari**: Develop → Show Web Inspector → Elements → Toggle print styles

### Print Preview

Always test with actual Print Preview (Cmd+P / Ctrl+P) as it's the most accurate representation.

### Checklist

```css
/* Print styles checklist */
@media print {
  /* ✓ Hide navigation and interactive elements */
  /* ✓ Reset backgrounds to white */
  /* ✓ Set text to black */
  /* ✓ Use serif body font at 12pt */
  /* ✓ Control page breaks */
  /* ✓ Show URLs for links */
  /* ✓ Tables don't break across pages */
  /* ✓ Images have appropriate size */
  /* ✓ Essential content is visible */
  /* ✓ Decorative elements hidden */
}
```

---

## Complete Print Stylesheet

```css
/* print.css - Complete example */
@media print {
  /* === RESETS === */
  * {
    background: transparent !important;
    color: #000 !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }

  /* === HIDE NON-ESSENTIAL === */
  nav, .nav,
  header:not(.article-header),
  footer:not(.article-footer),
  aside,
  .sidebar,
  .menu,
  .search,
  .ad,
  .social,
  .comments,
  form,
  button,
  .no-print {
    display: none !important;
  }

  /* === PAGE SETUP === */
  @page {
    margin: 0.75in;
    size: letter portrait;
  }

  @page :first {
    margin-top: 1in;
  }

  /* === TYPOGRAPHY === */
  body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.4;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    page-break-after: avoid;
  }

  h1 { font-size: 24pt; }
  h2 { font-size: 18pt; }
  h3 { font-size: 14pt; }

  p {
    orphans: 3;
    widows: 3;
  }

  /* === LINKS === */
  a[href]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666 !important;
  }

  a[href^="#"]::after,
  a[href^="javascript:"]::after {
    content: "";
  }

  /* === IMAGES === */
  img {
    max-width: 100% !important;
    page-break-inside: avoid;
  }

  /* === TABLES === */
  table {
    border-collapse: collapse;
    width: 100%;
  }

  thead {
    display: table-header-group;
  }

  tr {
    page-break-inside: avoid;
  }

  th, td {
    border: 1px solid #000;
    padding: 0.25em 0.5em;
  }

  /* === PAGE BREAKS === */
  h2, h3 {
    break-after: avoid;
  }

  figure, blockquote, pre {
    break-inside: avoid;
  }

  /* === UTILITIES === */
  .print-only {
    display: block !important;
  }

  .no-print {
    display: none !important;
  }

  .page-break {
    break-before: page;
  }
}

/* Hidden by default, shown only in print */
.print-only {
  display: none;
}
```

---

## Print Utilities

### CSS Classes

```css
/* Screen only */
@media print {
  .no-print,
  .screen-only {
    display: none !important;
  }
}

/* Print only */
.print-only {
  display: none;
}

@media print {
  .print-only {
    display: block !important;
  }
}

/* Force page break */
.page-break,
.page-break-before {
  break-before: page;
}

.page-break-after {
  break-after: page;
}

/* Keep together */
.keep-together {
  break-inside: avoid;
}
```

### HTML for Print

```html
<!-- Show different content in print -->
<p class="screen-only">Click the button below to continue.</p>
<p class="print-only">Visit example.com/continue to proceed.</p>

<!-- Force page break -->
<div class="page-break"></div>

<!-- Print-specific section -->
<section class="print-only">
  <h2>Appendix</h2>
  <p>Additional information for printed version...</p>
</section>
```

---

## Checklist

When creating print styles:

- [ ] Created separate print.css or @media print block
- [ ] Hidden navigation, sidebars, and interactive elements
- [ ] Reset backgrounds and colors for ink saving
- [ ] Set appropriate fonts (serif body, 12pt)
- [ ] Configured page margins and size
- [ ] Added page break controls
- [ ] Links show URLs (for external links)
- [ ] Tables have header groups and don't break
- [ ] Images sized appropriately and don't break
- [ ] Tested in Print Preview
- [ ] Added .no-print and .print-only utilities

## Related Skills

- **css-author** - Modern CSS organization with native @import, @layer casca...
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
- **responsive-images** - Modern responsive image techniques using picture element,...
