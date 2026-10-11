---
name: cpq-quote-templates
description: "Use when designing or troubleshooting Salesforce CPQ (SBQQ) quote templates: building template sections, configuring line columns, conditionally showing sections, generating branded PDFs, or handling multi-language output. Triggers: 'CPQ quote template', 'SBQQ template', 'CPQ PDF', 'line columns', 'quote template sections', 'conditional section', 'CPQ quote document'. NOT for standard Salesforce quote templates (Setup > Quote Templates), Visualforce-only PDF customization, or CPQ pricing rules and price books."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - User Experience
  - Operational Excellence
triggers:
  - "how do I add line item columns to a CPQ quote template PDF"
  - "CPQ quote template section is not showing up conditionally on the PDF"
  - "how do I build a branded PDF output for Salesforce CPQ quotes with a logo and custom sections"
  - "CPQ quote PDF shows blank line items table even though quote has products"
  - "how do I support multiple languages in CPQ quote documents"
  - "what is the difference between HTML, Line Items, and Quote Terms content types in CPQ templates"
tags:
  - cpq
  - cpq-quote-templates
  - sbqq
  - pdf-generation
  - line-columns
  - conditional-sections
  - quote-documents
inputs:
  - "Whether Salesforce CPQ (managed package SBQQ) is installed and licensed"
  - "Existing SBQQ__QuoteTemplate__c records and their current section/content structure"
  - "Which SBQQ__QuoteLine__c fields need to appear in the line items table"
  - "Any conditional visibility requirements (which sections should print under what circumstances)"
  - "Branding requirements: logo dimensions, fonts, color palette"
  - "Multi-language or multi-locale requirements"
outputs:
  - "Configured SBQQ__QuoteTemplate__c with sections and content records"
  - "SBQQ__LineColumn__c records defining the line items table columns"
  - "Conditional visibility field configuration on SBQQ__TemplateSection__c"
  - "PDF generation guidance and known CSS limitations"
  - "Multi-language template strategy"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-07
---

# CPQ Quote Templates

Use this skill when a practitioner needs to design, configure, or troubleshoot Salesforce CPQ (SBQQ) quote templates: building the section and content hierarchy, defining which quote line fields appear in the line items table, controlling conditional section visibility, producing branded PDF output, or supporting multiple languages. This skill does NOT cover standard Salesforce quote templates configured in Setup > Quote Templates — those use `QuoteLineItem` and are covered by the `admin/quotes-and-quote-templates` skill.

---

## Before Starting

Gather this context before working on anything in this domain:

- **CPQ managed package must be installed**: All CPQ template objects (`SBQQ__QuoteTemplate__c`, `SBQQ__TemplateSection__c`, `SBQQ__TemplateContent__c`, `SBQQ__LineColumn__c`) exist only when the SBQQ managed package is installed. Confirm the package is present before any configuration.
- **Standard quote templates do not work for CPQ**: The most common mistake is directing practitioners to Setup > Quote Templates. Standard templates query `QuoteLineItem`; CPQ lines live in `SBQQ__QuoteLine__c`. The result is a PDF with an empty line items table every time.
- **HTML in CPQ templates is converted to XSL-FO**: CPQ's PDF engine converts HTML content to XSL-FO before rendering. CSS class-based styling, flexbox, CSS grid, and many positioning properties are silently ignored. All styling must use inline styles on every element.
- **Image size limit is 5 MB per image**: Images embedded in template HTML or stored as Salesforce Files referenced in templates must be under 5 MB. Larger images cause PDF generation to fail silently or time out.
- **Multi-language requires separate templates per locale**: CPQ has no native translation layer for quote templates. Each language requires a separate `SBQQ__QuoteTemplate__c` record. Template selection logic must be implemented in a Flow or Process Builder that sets the template lookup field on the quote based on the quote's locale or account language.

---

## Core Concepts

### Template Object Hierarchy

CPQ quote templates are structured across three related objects:

```
SBQQ__QuoteTemplate__c  (the top-level template record)
  └── SBQQ__TemplateSection__c  (ordered sections: Header, Cover Page, Body, Footer)
        └── SBQQ__TemplateContent__c  (content blocks within each section)
```

**SBQQ__QuoteTemplate__c** is the entry point. A quote record has a lookup to a template; when a user clicks "Preview" or generates the document, CPQ walks this hierarchy to build the PDF.

**SBQQ__TemplateSection__c** defines a printable region. Each section has a `SBQQ__Type__c` field that controls its role:
- **Header** — appears at the top of every page
- **Cover Page** — full first-page section, printed before body content
- **Body** — the main content area; Body sections marked as "Line Items" repeat for each group of quote lines
- **Footer** — appears at the bottom of every page

Sections have an `SBQQ__Orientation__c` field (Portrait / Landscape) and an `SBQQ__PageBreakBefore__c` checkbox to force page breaks between sections.

**SBQQ__TemplateContent__c** is the leaf node. Each content record belongs to one section and has a `SBQQ__Type__c` that determines what it renders:
- **HTML** — rich-text / custom HTML rendered inline; supports company logo, custom messaging, fields merged using `{!Quote.FieldName}` merge syntax
- **Line Items** — renders a table of `SBQQ__QuoteLine__c` records; column definitions come from `SBQQ__LineColumn__c` records
- **Quote Terms** — renders the master Terms and Conditions text stored on the template
- **Custom** — references a Visualforce page by name; the page must use `renderAs="pdf"` and accept the quote ID as a parameter

### Line Columns (SBQQ__LineColumn__c)

Line columns define which fields from `SBQQ__QuoteLine__c` appear in the Line Items content type table. Each `SBQQ__LineColumn__c` record specifies:

- `SBQQ__FieldName__c` — the API name of the field on `SBQQ__QuoteLine__c` (standard, custom, or formula)
- `SBQQ__Heading__c` — the column header text printed in the PDF
- `SBQQ__DisplayWidth__c` — percentage of the table width this column occupies (all columns should sum to 100)
- `SBQQ__Alignment__c` — Left, Center, Right
- `SBQQ__FormatType__c` — controls number/currency/percent formatting

Custom fields added to `SBQQ__QuoteLine__c` are fully supported. Formula fields that reference parent `SBQQ__Quote__c` fields are also supported, but complex multi-hop formulas can slow PDF rendering.

### Conditional Visibility

Each `SBQQ__TemplateSection__c` has a `SBQQ__ConditionalPrintField__c` field that accepts the API name of a field on `SBQQ__Quote__c`. The section is shown only when that field evaluates to "truthy" by these exact rules:

| Field type | Condition to show the section |
|---|---|
| Checkbox | Field value = `true` |
| Text | Field value = the exact string `"true"` (case-sensitive) |
| Number / Currency / Percent | Field value != `0` and is not null |

If `SBQQ__ConditionalPrintField__c` is blank, the section always prints. This mechanism is declarative-only — no Apex or formula is evaluated at PDF time beyond the single field lookup.

---

## Common Patterns

### Pattern 1: Branded Cover Page with Company Logo

**When to use:** The org requires a professional first page with the company logo, rep name, account name, and quote expiry date before the line items table.

**How it works:**
1. Create a `SBQQ__TemplateSection__c` with `SBQQ__Type__c = Cover Page` and `SBQQ__PageBreakBefore__c = false`.
2. Create a `SBQQ__TemplateContent__c` child with `SBQQ__Type__c = HTML`.
3. In the HTML content block, reference the logo as a base64-encoded inline `<img>` tag or as a Salesforce Files URL. Keep the file under 5 MB.
4. Use CPQ merge fields (`{!Quote.SBQQ__Account__r.Name}`, `{!Quote.SBQQ__ExpirationDate__c}`) directly in the HTML body.
5. Use only inline CSS (`style="..."`) — no `<style>` blocks and no CSS classes.
6. Click "Preview" on the template to generate a sample PDF before saving the final version.

**Why not a standard Header section:** Headers repeat on every page. A Cover Page section prints once, giving full control over page layout for the introduction.

### Pattern 2: Conditional Discount Summary Section

**When to use:** Show a dedicated "Volume Discount Summary" section only when the quote contains a discount above a threshold — for example, when a custom checkbox field `Show_Discount_Summary__c` is checked by a pricing rule.

**How it works:**
1. Add a custom checkbox field `Show_Discount_Summary__c` to `SBQQ__Quote__c`.
2. Create a CPQ Price Rule or Flow that sets this checkbox to `true` when any line's discount exceeds the threshold.
3. Create a Body `SBQQ__TemplateSection__c` for the discount summary.
4. Set `SBQQ__ConditionalPrintField__c = Show_Discount_Summary__c` on the section.
5. Add an HTML content block inside the section with the discount summary layout.

**Why not use HTML visibility tricks:** CSS `display:none` and `visibility:hidden` are not reliably honored by the XSL-FO renderer. The server-side conditional field is the only reliable mechanism.

### Pattern 3: Multi-Language Templates via Flow

**When to use:** The org sells in multiple countries and needs quote PDFs in the customer's language.

**How it works:**
1. Create one `SBQQ__QuoteTemplate__c` per language with all content authored in that language.
2. Add a custom picklist `Quote_Language__c` to `SBQQ__Quote__c` (or read from `Account.BillingCountry` / `Contact.Language__c`).
3. Build a Record-Triggered Flow on `SBQQ__Quote__c` that fires on create/update of the language field.
4. Use Decision elements to branch by language and use Assignment elements to set `SBQQ__Quote__c.SBQQ__Template__c` to the correct template record ID.
5. Users can still manually override the template on the quote if needed.

**Why not translate within one template:** CPQ's template engine has no translation table. All text in HTML and Quote Terms content blocks is static.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Org has CPQ (SBQQ) installed, needs branded PDF | Use `SBQQ__QuoteTemplate__c` hierarchy | Standard Setup > Quote Templates will produce empty line items |
| Need to show/hide a section based on quote data | Use `SBQQ__ConditionalPrintField__c` on the section | CSS visibility is not reliable in XSL-FO rendering |
| Need complex Apex-driven layout or dynamic tables | Use Custom content type pointing to a Visualforce page | Only option for Apex-driven content; HTML content type cannot call Apex |
| Need to include custom `SBQQ__QuoteLine__c` fields in table | Add `SBQQ__LineColumn__c` records to the Line Items content | Standard configuration; no code required |
| Need to support 3 languages | Create 3 separate `SBQQ__QuoteTemplate__c` records, use Flow to assign | No native translation layer in CPQ templates |
| Image is over 5 MB | Resize/compress before uploading, or use an external CDN URL | 5 MB per-image limit; exceeding it silently breaks PDF |
| Need page breaks between sections | Set `SBQQ__PageBreakBefore__c = true` on the section | Declarative; no custom code needed |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on CPQ quote template design:

1. **Verify CPQ installation and existing templates**: Confirm `SBQQ__QuoteTemplate__c` is accessible in the org. Run a SOQL query or check Setup > Installed Packages for the Salesforce CPQ managed package. List any existing templates to avoid duplicating work.
2. **Define the section structure**: Map out which sections the PDF needs — Cover Page, Header, one or more Body sections (line items, pricing notes, discount summary), Footer. Decide which sections are conditional and identify the controlling field on `SBQQ__Quote__c` for each.
3. **Create the template and section records**: Create the `SBQQ__QuoteTemplate__c` record, then create ordered `SBQQ__TemplateSection__c` children with correct `SBQQ__Type__c`, `SBQQ__DisplayOrder__c`, and `SBQQ__ConditionalPrintField__c` values.
4. **Author content blocks**: For each section, create `SBQQ__TemplateContent__c` records. For HTML blocks, write all styles inline and test merge field syntax using `{!Quote.FieldAPIName}`. For Line Items blocks, create `SBQQ__LineColumn__c` records pointing to the required `SBQQ__QuoteLine__c` fields; verify column width percentages sum to 100.
5. **Preview against a real quote**: Open an existing CPQ quote in the org, set the `SBQQ__Template__c` lookup to the new template, and click "Preview" to generate a sample PDF. Check that all sections render, line items are populated, and conditional sections appear or hide correctly.
6. **Fix CSS and image issues**: If sections appear garbled, inspect the HTML and replace any class-based or block-level CSS with inline styles. If images are missing, verify file size is under 5 MB and the image URL is publicly accessible or base64-encoded.
7. **Set up template assignment logic**: If the org needs multi-language support or automated template selection, build the Record-Triggered Flow that sets `SBQQ__Quote__c.SBQQ__Template__c` based on the relevant criteria. Test by changing the controlling field and regenerating the PDF.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] CPQ managed package (SBQQ) confirmed installed; NOT using Setup > Quote Templates
- [ ] All `SBQQ__TemplateSection__c` records have correct `SBQQ__Type__c` and `SBQQ__DisplayOrder__c`
- [ ] All conditional sections have a valid `SBQQ__ConditionalPrintField__c` pointing to a real field on `SBQQ__Quote__c`
- [ ] Line Items content type has corresponding `SBQQ__LineColumn__c` records; column widths sum to 100
- [ ] All HTML content uses inline styles only (no `<style>` blocks, no CSS classes)
- [ ] All images are under 5 MB; logo renders correctly in Preview
- [ ] "Preview" button used to verify the PDF before deploying; line items table is not empty
- [ ] Multi-language templates (if needed) each have a separate `SBQQ__QuoteTemplate__c`; Flow assigns the correct template to the quote

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Standard Setup > Quote Templates produces empty line items in a CPQ org** — Standard quote templates query `QuoteLineItem`. CPQ stores lines in `SBQQ__QuoteLine__c`. Even if the template renders everything else correctly, the line items table will always be blank. You must use the CPQ template objects under the SBQQ namespace.
2. **CSS classes are silently ignored by the XSL-FO renderer** — CPQ converts HTML to XSL-FO for PDF output. CSS classes defined in a `<style>` block, external stylesheets, or `class=""` attributes are stripped before rendering. Only inline `style=""` attributes are applied. This includes font-family, color, padding, and border properties that practitioners assume will carry through.
3. **Conditional Print Field text comparison is exact and case-sensitive** — If the controlling field is a Text field, the section only prints when the value is exactly `"true"` (lowercase). A value of `"True"`, `"TRUE"`, `"Yes"`, or `"1"` will not trigger visibility. This is a common source of sections that never appear in production PDFs.
4. **Images over 5 MB cause silent PDF generation failure** — When an image in the template exceeds 5 MB, CPQ may generate an empty PDF, a PDF without images, or time out without an error message. There is no explicit validation error in Setup. Always compress images and verify size before uploading.
5. **Multi-hop formula fields on SBQQ__QuoteLine__c slow PDF rendering** — Formula fields that traverse multiple relationships (e.g., `SBQQ__Product__r.Family` is fine, but crossing three or more objects) can add significant time to PDF generation per line. On quotes with 50+ lines this becomes noticeable. Use simpler formulas or pre-populate a custom field via Flow instead.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `SBQQ__QuoteTemplate__c` record | The top-level template; holds name, logo, and terms text |
| `SBQQ__TemplateSection__c` records | Ordered sections defining structure; each has type and optional conditional field |
| `SBQQ__TemplateContent__c` records | Content blocks (HTML, Line Items, Quote Terms, Custom VF) within each section |
| `SBQQ__LineColumn__c` records | Column definitions for Line Items tables; mapped to `SBQQ__QuoteLine__c` fields |
| Template assignment Flow | Record-Triggered Flow that sets `SBQQ__Quote__c.SBQQ__Template__c` for multi-language routing |

---

## Related Skills

- `admin/quotes-and-quote-templates` — standard Salesforce quote templates for non-CPQ orgs; covers Setup > Quote Templates and `QuoteLineItem`-backed PDFs
- `apex/quote-pdf-customization` — Visualforce-based custom PDF rendering; use when CPQ Custom content type (Visualforce page) is needed for Apex-driven layouts
- `architect/cpq-vs-standard-products-decision` — decision framework for whether an org should use CPQ or standard Products/Quotes
