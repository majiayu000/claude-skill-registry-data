---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: react-pdf
description: >
  Generate professional PDF reports using @react-pdf/renderer in Node.js scripts.
  Produces clean, document-style output similar to academic papers or business reports.
  Covers headings, paragraphs, lists, images, page numbers, and the Node API
  (renderToFile, renderToBuffer). Use this skill when the user asks to generate,
  create, or build PDF reports from TypeScript/Node scripts.
---

# react-pdf

Generate professional PDF reports from TypeScript scripts using `@react-pdf/renderer`. Runs in Node.js, no browser required.

**Style goal: clean, professional documents.** Think academic papers, business reports, technical documentation. No web-like colored components, badges, cards, or decorative elements. Just proper typography, clear hierarchy, and appropriate whitespace.

**Density matters.** Default spacing values in this skill are intentionally conservative. For documents that need to fit more content per page (evidence packets, data-heavy reports, long timelines), scale down aggressively: 9pt body, 11pt headings, 1.3-1.4 line height, 36-48pt margins. Test the output visually and adjust; the defaults are starting points, not rules.

## Setup

```bash
pnpm add @react-pdf/renderer react
```

Run scripts with `tsx` or `bun`. The project must have `"type": "module"` in package.json.

```bash
npx tsx ./scripts/generate-report.tsx
```

## Core components

| Component | Purpose |
|---|---|
| `Document` | Root wrapper, must be top-level |
| `Page` | Single page. `size="A4"` or `size="LETTER"` |
| `View` | Container with flexbox layout |
| `Text` | Text content. Nest `<Text>` inside `<Text>` for inline bold/italic |
| `Image` | JPG/PNG from file path, URL, or Buffer |
| `Link` | Hyperlinks |

## Node API

```tsx
import { renderToFile, renderToBuffer } from '@react-pdf/renderer'

await renderToFile(<MyReport />, './report.pdf')
const buffer = await renderToBuffer(<MyReport />)
```

## Typography and sizing

Use a serif font for professional reports. Register **Lora** from Google Fonts (closest to Georgia, elegant and warm):

```tsx
import { Font } from '@react-pdf/renderer'

Font.register({
  family: 'Lora',
  fonts: [
    { src: 'https://fonts.gstatic.com/s/lora/v37/0QI6MX1D_JOuGQbT0gvTJPa787weuyJG.ttf', fontWeight: 400 },
    { src: 'https://fonts.gstatic.com/s/lora/v37/0QI8MX1D_JOuMw_hLdO6T2wV9KnW-MoFkqg.ttf', fontWeight: 400, fontStyle: 'italic' },
    { src: 'https://fonts.gstatic.com/s/lora/v37/0QI6MX1D_JOuGQbT0gvTJPa787zAvCJG.ttf', fontWeight: 600 },
    { src: 'https://fonts.gstatic.com/s/lora/v37/0QI6MX1D_JOuGQbT0gvTJPa787z5vCJG.ttf', fontWeight: 700 },
  ],
})

Font.registerHyphenationCallback((word) => [word])
```

Then use `fontFamily: 'Lora'` in page style, `fontWeight: 700` for bold headings, `fontStyle: 'italic'` for captions.

Heading sizes should follow a clear hierarchy. Two presets depending on how much content you need to fit:

**Standard** (reports, papers):

```tsx
const s = StyleSheet.create({
  page: {
    paddingTop: 72, paddingBottom: 60, paddingHorizontal: 72,
    fontFamily: 'Lora', fontSize: 11, lineHeight: 1.5, color: '#1a1a1a',
  },
  h1: { fontSize: 22, fontWeight: 700, marginBottom: 16 },
  h2: { fontSize: 16, fontWeight: 700, marginTop: 24, marginBottom: 10 },
  h3: { fontSize: 13, fontWeight: 600, marginTop: 16, marginBottom: 6 },
  paragraph: { marginBottom: 8 },
})
```

**Compact** (evidence packets, data-heavy documents, long timelines):

```tsx
const s = StyleSheet.create({
  page: {
    paddingTop: 36, paddingBottom: 36, paddingHorizontal: 48,
    fontFamily: 'Lora', fontSize: 9, lineHeight: 1.4, color: '#1a1a1a',
  },
  h1: { fontSize: 16, fontWeight: 700, marginBottom: 2 },
  h2: { fontSize: 11, fontWeight: 700, marginTop: 10, marginBottom: 4 },
  h3: { fontSize: 10, fontWeight: 700, marginTop: 8, marginBottom: 3 },
  paragraph: { marginBottom: 4 },
})
```

The compact preset fits roughly 2x the content per page. Use it when the document has many tables, timelines, or lists and you want to keep page count low.

For sans-serif reports, register **Inter** instead:

```tsx
Font.register({
  family: 'Inter',
  fonts: [
    { src: 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf', fontWeight: 400 },
    { src: 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYMZg.ttf', fontWeight: 600 },
    { src: 'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf', fontWeight: 700 },
  ],
})
```

## Built-in fonts

- **Serif**: Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic
- **Sans**: Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique
- **Mono**: Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique

Only TTF/WOFF custom fonts are supported. No variable fonts.

## Images

Images are always block-level. Set width to control size; height is derived from aspect ratio.

```tsx
<Image src="./figures/architecture.png" style={{ width: '100%', marginVertical: 16 }} />

<Image src="https://example.com/chart.png" style={{ width: 300, marginVertical: 16 }} />

// Caption below image
<Text style={{ fontSize: 9, color: '#666', textAlign: 'center', marginTop: 6 }}>
  Figure 1. System architecture overview.
</Text>
```

## Lists

Build lists manually with flexbox rows:

```tsx
const Bullet = ({ children }: { children: React.ReactNode }) => (
  <View style={{ flexDirection: 'row', marginBottom: 5 }}>
    <Text style={{ width: 16 }}>•</Text>
    <Text style={{ flex: 1 }}>{children}</Text>
  </View>
)

const Numbered = ({ n, children }: { n: number; children: React.ReactNode }) => (
  <View style={{ flexDirection: 'row', marginBottom: 5 }}>
    <Text style={{ width: 20 }}>{n}.</Text>
    <Text style={{ flex: 1 }}>{children}</Text>
  </View>
)
```

## Page numbers

```tsx
<Text
  fixed
  style={{ position: 'absolute', bottom: 32, left: 0, right: 0, fontSize: 9, textAlign: 'center', color: '#666' }}
  render={({ pageNumber }) => `${pageNumber}`}
/>
```

## Horizontal rule

```tsx
<View style={{ borderBottomWidth: 0.5, borderBottomColor: '#999', marginVertical: 20 }} />
```

## Page wrapping

Pages wrap automatically. Use `minPresenceAhead` on headings to prevent orphaned headers:

```tsx
<Text style={s.h2} minPresenceAhead={60}>Section Title</Text>
```

Use `wrap={false}` on a View to keep it together on one page (e.g. a figure with its caption).

## Inline bold and italic

Nest Text components for inline formatting:

```tsx
<Text style={s.paragraph}>
  This sentence has <Text style={{ fontFamily: 'Times-Bold' }}>bold text</Text> and{' '}
  <Text style={{ fontFamily: 'Times-Italic' }}>italic text</Text> inline.
</Text>
```

## Code blocks

Use Courier (built-in monospace) with a light border to distinguish code from body text:

```tsx
const CodeBlock = ({ children }: { children: string }) => (
  <View style={{ borderWidth: 0.5, borderColor: '#ccc', padding: 10, marginVertical: 12 }}>
    <Text style={{ fontFamily: 'Courier', fontSize: 9, lineHeight: 1.7 }}>
      {children}
    </Text>
  </View>
)

// Usage
<CodeBlock>{`const client = createClient({
  apiKey: process.env.API_KEY,
  region: 'us-east-1',
})

const result = await client.query('SELECT * FROM users')`}</CodeBlock>
```

For inline code within a paragraph:

```tsx
<Text style={s.paragraph}>
  Run the command <Text style={{ fontFamily: 'Courier', fontSize: 9.5 }}>npm install</Text> to
  install dependencies.
</Text>
```

## Tables

Build tables with flexbox rows. Use a thin border and bold header row:

```tsx
const TableRow = ({ cells, header }: { cells: string[]; header?: boolean }) => (
  <View style={{
    flexDirection: 'row',
    borderBottomWidth: 0.5,
    borderBottomColor: '#999',
    paddingVertical: 6,
  }}>
    {cells.map((cell, i) => (
      <Text key={i} style={{
        flex: 1,
        paddingHorizontal: 8,
        fontSize: 10,
        fontWeight: header ? 700 : 400,
      }}>
        {cell}
      </Text>
    ))}
  </View>
)

// Usage
<View style={{ marginVertical: 12 }}>
  <TableRow cells={['Endpoint', 'P50 (ms)', 'P99 (ms)']} header />
  <TableRow cells={['/api/projects', '12', '45']} />
  <TableRow cells={['/api/deploy', '89', '210']} />
  <TableRow cells={['/api/search', '156', '890']} />
</View>

// Add a caption below if needed
<Text style={{ fontSize: 9, color: '#666', textAlign: 'center', marginTop: 4 }}>
  Table 1. API latency benchmarks over a 30-day window.
</Text>
```

## Valid CSS properties

Flexbox (alignItems, justifyContent, flexDirection, gap), dimensions (width, height, min/max), spacing (margin, padding + Horizontal/Vertical), borders (borderWidth, borderColor), text (fontSize, fontFamily, fontWeight, fontStyle, textAlign, textDecoration, letterSpacing, lineHeight, textIndent), positioning (position absolute/relative, top/right/bottom/left).

**Units**: `pt` (default, 72 dpi), `in`, `mm`, `cm`, `%`, `vw`, `vh`.

## Style rules for professional reports

- **No colors** on text except subtle gray for captions and page numbers. Body text is near-black (#1a1a1a).
- **No background colors**, badges, cards, or decorative borders.
- **No border-radius** on anything. This is a document, not a website.
- **Margins**: 72pt (1 inch) for standard reports. 36-48pt for compact/dense documents.
- **Line height**: 1.4-1.5 for body text. Avoid 1.6+ which wastes vertical space.
- **Heading hierarchy**: maintain clear size steps between heading levels. The absolute sizes depend on the preset (standard vs compact).
- **Images**: full width or sized appropriately, with italic captions below.
- **White space**: use marginTop on headings to separate sections, but keep it proportional to font size. Excessive spacing between sections pushes content to extra pages.
- **Test visually**: always open the generated PDF and check page breaks, orphaned headings, and overall density before finalizing the styles.

## Callout boxes

Use a left-border accent for executive summaries or key callouts:

```tsx
<View style={{ borderLeftWidth: 2.5, borderLeftColor: '#1a1a1a', paddingLeft: 10, paddingVertical: 4 }}>
  <Text style={{ fontSize: 11, fontWeight: 700, marginBottom: 3 }}>Investigation Summary</Text>
  <Text style={{ marginBottom: 4 }}>Key narrative goes here.</Text>
</View>
```

For bold key facts with arrow prefixes:

```tsx
const KeyFact = ({ children }: { children: React.ReactNode }) => (
  <View style={{ flexDirection: 'row', marginBottom: 2, marginLeft: 2 }}>
    <Text style={{ width: 14, fontWeight: 700 }}>{'\u25B6'}</Text>
    <Text style={{ flex: 1, fontWeight: 700 }}>{children}</Text>
  </View>
)
```

## Full example

See `example/generate-pdf.tsx` in this skill folder for a complete working report with title page, headings, paragraphs, bullet lists, numbered lists, images with captions, and page numbers. Run it with:

```bash
npx tsx ~/.config/opencode/skills/react-pdf/example/generate-pdf.tsx
```
