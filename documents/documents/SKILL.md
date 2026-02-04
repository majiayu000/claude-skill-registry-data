---
name: documents
description: Generate PDF and Word documents programmatically. Use for invoices, reports, contracts, or data exports.
---

# Documents

Generate documents (PDF, DOCX) programmatically.

## Status: Early Stage

This skill is a placeholder. Patterns will evolve with use.

## Potential Use Cases

- Invoices for clients
- Reports from app data
- Contracts/proposals
- Data exports

## Stack Options to Explore

### PDF Generation

```bash
pnpm add @react-pdf/renderer
```

```tsx
import { Document, Page, Text, View } from '@react-pdf/renderer'

const Invoice = () => (
  <Document>
    <Page>
      <View>
        <Text>Invoice #001</Text>
      </View>
    </Page>
  </Document>
)
```

### Word Documents

```bash
pnpm add docx
```

```tsx
import { Document, Paragraph, TextRun } from 'docx'

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [new TextRun('Hello World')],
      }),
    ],
  }],
})
```

### HTML → PDF (via Puppeteer)

```bash
pnpm add puppeteer
```

```tsx
const browser = await puppeteer.launch()
const page = await browser.newPage()
await page.goto('http://localhost:3000/invoice/123')
await page.pdf({ path: 'invoice.pdf', format: 'A4' })
```

## Reference

- Anthropic's docx skill: https://github.com/anthropics/skills/tree/main/skills/docx
- Anthropic's pdf skill: https://github.com/anthropics/skills/tree/main/skills/pdf
- react-pdf docs: https://react-pdf.org/

## TODO

- [ ] Pick preferred stack after first real use case
- [ ] Add invoice template
- [ ] Add report template
- [ ] Integrate with tRPC for data fetching
