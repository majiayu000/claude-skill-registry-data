---
name: svg-diagram
description: Generate SVG diagrams, OG images, and dynamic graphics using Satori with Tailwind CSS. Use when creating programmatic images, social cards, or diagrams from JSX/React components.
---

# SVG Diagram Generation with Satori

Satori converts JSX/React components to SVG. It powers Vercel's OG Image Generation and is ideal for creating dynamic images programmatically.

## Quick Start

```typescript
import satori from 'satori'

const svg = await satori(
  <div tw="flex flex-col w-full h-full items-center justify-center bg-white">
    <h1 tw="text-6xl font-bold text-gray-900">Hello World</h1>
  </div>,
  {
    width: 1200,
    height: 630,
    fonts: [
      {
        name: 'Inter',
        data: await fetch('https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff').then(r => r.arrayBuffer()),
        weight: 400,
        style: 'normal',
      },
    ],
  }
)
```

## The `tw=` Prop (Tailwind Integration)

Use `tw=` instead of `style=` for cleaner, Tailwind-based styling:

```jsx
// with tw= prop (preferred)
<div tw="flex flex-col w-full h-full items-center justify-center bg-white">
  <h1 tw="text-4xl font-bold text-gray-900">Title</h1>
  <p tw="text-xl text-gray-600 mt-4">Subtitle</p>
</div>

// equivalent with style=
<div style={{
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  height: '100%',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: 'white',
}}>
  <h1 style={{ fontSize: 36, fontWeight: 700, color: '#111827' }}>Title</h1>
  <p style={{ fontSize: 20, color: '#4B5563', marginTop: 16 }}>Subtitle</p>
</div>
```

### Supported Tailwind Classes

**Layout:**
- `flex`, `flex-col`, `flex-row`, `flex-wrap`
- `items-center`, `items-start`, `items-end`, `items-stretch`
- `justify-center`, `justify-start`, `justify-end`, `justify-between`, `justify-around`
- `gap-*`, `gap-x-*`, `gap-y-*`

**Sizing:**
- `w-*`, `h-*`, `w-full`, `h-full`, `w-screen`, `h-screen`
- `min-w-*`, `max-w-*`, `min-h-*`, `max-h-*`

**Spacing:**
- `p-*`, `px-*`, `py-*`, `pt-*`, `pr-*`, `pb-*`, `pl-*`
- `m-*`, `mx-*`, `my-*`, `mt-*`, `mr-*`, `mb-*`, `ml-*`

**Typography:**
- `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl` ... `text-9xl`
- `font-thin`, `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold`, `font-black`
- `text-left`, `text-center`, `text-right`, `text-justify`
- `tracking-tight`, `tracking-normal`, `tracking-wide`
- `leading-tight`, `leading-normal`, `leading-relaxed`

**Colors:**
- `text-gray-900`, `text-blue-500`, `text-white`, etc.
- `bg-white`, `bg-gray-100`, `bg-blue-500`, etc.
- `border-gray-200`, `border-blue-500`, etc.

**Borders:**
- `border`, `border-2`, `border-4`
- `rounded`, `rounded-lg`, `rounded-xl`, `rounded-full`
- `border-solid`, `border-dashed`

**Effects:**
- `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`
- `opacity-*`

**Responsive Breakpoints:**
- `sm:`, `md:`, `lg:`, `xl:`, `2xl:` prefixes work based on width

## Supported CSS Properties

### Layout (Flexbox Only - No CSS Grid)

```jsx
<div tw="flex">           {/* display: flex (default) */}
<div tw="flex flex-col">  {/* flexDirection: column */}
<div tw="flex flex-wrap"> {/* flexWrap: wrap */}
```

### Positioning

```jsx
<div tw="relative">
  <div tw="absolute top-0 left-0">Positioned</div>
  <div tw="absolute bottom-4 right-4">Corner</div>
</div>
```

### Typography

```jsx
<p tw="text-4xl font-bold tracking-tight leading-tight">
  Large bold text
</p>
<p tw="text-sm text-gray-500 uppercase">
  Small caps
</p>
```

### Colors & Backgrounds

```jsx
// solid colors
<div tw="bg-blue-500 text-white">Blue background</div>

// gradients (use style for complex gradients)
<div style={{
  backgroundImage: 'linear-gradient(to right, #3b82f6, #8b5cf6)',
}}>
  Gradient
</div>
```

### Text Gradients

```jsx
<span style={{
  backgroundImage: 'linear-gradient(90deg, #3b82f6, #8b5cf6)',
  backgroundClip: 'text',
  color: 'transparent',
}}>
  Gradient Text
</span>
```

### Shadows

```jsx
<div tw="shadow-lg rounded-xl p-6 bg-white">
  Card with shadow
</div>
```

### Transforms (2D Only)

```jsx
<div style={{ transform: 'rotate(5deg)' }}>Rotated</div>
<div style={{ transform: 'scale(1.1)' }}>Scaled</div>
<div style={{ transform: 'translateX(10px) translateY(5px)' }}>Moved</div>
```

## Common Patterns

### Centered Card Layout

```jsx
<div tw="flex w-full h-full items-center justify-center bg-gray-100">
  <div tw="flex flex-col bg-white rounded-2xl shadow-xl p-12 max-w-2xl">
    <h1 tw="text-5xl font-bold text-gray-900 mb-4">Card Title</h1>
    <p tw="text-xl text-gray-600">Card description goes here</p>
  </div>
</div>
```

### OG Image with Logo

```jsx
<div tw="flex flex-col w-full h-full bg-white p-16">
  {/* header */}
  <div tw="flex items-center">
    <img src={logoBase64} width={48} height={48} />
    <span tw="ml-4 text-2xl font-semibold text-gray-900">Brand</span>
  </div>

  {/* main content */}
  <div tw="flex flex-1 items-center justify-center">
    <h1 tw="text-6xl font-bold text-gray-900 text-center max-w-4xl">
      Your Dynamic Title Here
    </h1>
  </div>

  {/* footer */}
  <div tw="flex justify-between items-center text-gray-500">
    <span>example.com</span>
    <span>@username</span>
  </div>
</div>
```

### Background Pattern (Dots)

```jsx
<div
  tw="flex w-full h-full items-center justify-center"
  style={{
    backgroundColor: 'white',
    backgroundImage: 'radial-gradient(circle at 25px 25px, #e5e7eb 2%, transparent 0%)',
    backgroundSize: '50px 50px',
  }}
>
  <h1 tw="text-5xl font-bold">Content over pattern</h1>
</div>
```

### Two Column Layout

```jsx
<div tw="flex w-full h-full bg-white">
  {/* left column */}
  <div tw="flex flex-col w-1/2 p-12 justify-center">
    <h1 tw="text-5xl font-bold text-gray-900 mb-4">Title</h1>
    <p tw="text-xl text-gray-600">Description text</p>
  </div>

  {/* right column */}
  <div tw="flex w-1/2 bg-blue-500 items-center justify-center">
    <img src={imageBase64} width={300} height={300} />
  </div>
</div>
```

### Component Composition

```jsx
const Badge = ({ children, color }) => (
  <span tw={`px-3 py-1 rounded-full text-sm font-medium bg-${color}-100 text-${color}-800`}>
    {children}
  </span>
)

const Card = ({ title, tags }) => (
  <div tw="flex flex-col bg-white rounded-xl shadow-lg p-8">
    <h2 tw="text-3xl font-bold text-gray-900 mb-4">{title}</h2>
    <div tw="flex gap-2">
      {tags.map(tag => <Badge color="blue">{tag}</Badge>)}
    </div>
  </div>
)
```

## Light/Dark Mode Build Script

Create diagrams in both light and dark variants automatically:

### `scripts/generate-diagrams.ts`

```typescript
import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readFileSync, writeFileSync, mkdirSync } from 'fs'
import { join } from 'path'

// load font once
const interRegular = readFileSync('./fonts/Inter-Regular.ttf')
const interBold = readFileSync('./fonts/Inter-Bold.ttf')

const fonts = [
  { name: 'Inter', data: interRegular, weight: 400, style: 'normal' as const },
  { name: 'Inter', data: interBold, weight: 700, style: 'normal' as const },
]

// theme definitions
const themes = {
  light: {
    bg: 'white',
    bgSecondary: '#f3f4f6',
    text: '#111827',
    textSecondary: '#6b7280',
    accent: '#3b82f6',
    border: '#e5e7eb',
  },
  dark: {
    bg: '#111827',
    bgSecondary: '#1f2937',
    text: '#f9fafb',
    textSecondary: '#9ca3af',
    accent: '#60a5fa',
    border: '#374151',
  },
}

type Theme = typeof themes.light

// your diagram component - receives theme colors
function createDiagram(theme: Theme) {
  return (
    <div
      tw="flex flex-col w-full h-full p-16"
      style={{ backgroundColor: theme.bg }}
    >
      <div tw="flex items-center mb-8">
        <div
          tw="w-12 h-12 rounded-xl flex items-center justify-center text-white text-2xl font-bold"
          style={{ backgroundColor: theme.accent }}
        >
          S
        </div>
        <span
          tw="ml-4 text-2xl font-bold"
          style={{ color: theme.text }}
        >
          My Diagram
        </span>
      </div>

      <div
        tw="flex flex-1 rounded-2xl p-8"
        style={{ backgroundColor: theme.bgSecondary }}
      >
        <div tw="flex flex-col justify-center">
          <h1
            tw="text-5xl font-bold mb-4"
            style={{ color: theme.text }}
          >
            Dynamic Content
          </h1>
          <p
            tw="text-xl"
            style={{ color: theme.textSecondary }}
          >
            Generated with Satori in light and dark mode
          </p>
        </div>
      </div>

      <div
        tw="flex justify-between items-center mt-8 text-sm"
        style={{ color: theme.textSecondary }}
      >
        <span>example.com</span>
        <span>Generated at {new Date().toISOString().split('T')[0]}</span>
      </div>
    </div>
  )
}

interface GenerateOptions {
  name: string
  width?: number
  height?: number
  outputDir?: string
  formats?: ('svg' | 'png')[]
}

async function generateDiagram(options: GenerateOptions) {
  const {
    name,
    width = 1200,
    height = 630,
    outputDir = './output',
    formats = ['svg', 'png'],
  } = options

  mkdirSync(outputDir, { recursive: true })

  for (const [themeName, theme] of Object.entries(themes)) {
    const element = createDiagram(theme)

    // generate SVG
    const svg = await satori(element, { width, height, fonts })

    if (formats.includes('svg')) {
      const svgPath = join(outputDir, `${name}-${themeName}.svg`)
      writeFileSync(svgPath, svg)
      console.log(`Created: ${svgPath}`)
    }

    if (formats.includes('png')) {
      // convert to PNG at 2x resolution for retina
      const resvg = new Resvg(svg, {
        fitTo: { mode: 'width', value: width * 2 },
      })
      const pngData = resvg.render()
      const pngPath = join(outputDir, `${name}-${themeName}.png`)
      writeFileSync(pngPath, pngData.asPng())
      console.log(`Created: ${pngPath}`)
    }
  }
}

// generate all diagrams
async function main() {
  await generateDiagram({ name: 'og-image' })
  await generateDiagram({ name: 'twitter-card', width: 1200, height: 600 })
  await generateDiagram({ name: 'square', width: 1080, height: 1080 })
}

main().catch(console.error)
```

### `package.json` Scripts

```json
{
  "scripts": {
    "generate:diagrams": "tsx scripts/generate-diagrams.ts",
    "generate:watch": "tsx watch scripts/generate-diagrams.ts"
  },
  "dependencies": {
    "satori": "^0.10.0",
    "@resvg/resvg-js": "^2.6.0"
  },
  "devDependencies": {
    "tsx": "^4.0.0",
    "@types/node": "^20.0.0"
  }
}
```

### Usage

```bash
# generate all diagrams
npm run generate:diagrams

# output:
# output/og-image-light.svg
# output/og-image-light.png
# output/og-image-dark.svg
# output/og-image-dark.png
# ...
```

## Converting to PNG

For high-quality PNG output, use `@resvg/resvg-js`:

```typescript
import { Resvg } from '@resvg/resvg-js'

const svg = await satori(element, options)

// 2x resolution for retina displays
const resvg = new Resvg(svg, {
  fitTo: { mode: 'width', value: 2400 },  // 2x of 1200
})

const pngBuffer = resvg.render().asPng()
```

## Standard Dimensions

| Platform | Size | Aspect Ratio |
|----------|------|--------------|
| Open Graph | 1200×630 | 1.91:1 |
| Twitter Card | 1200×600 | 2:1 |
| LinkedIn | 1200×627 | 1.91:1 |
| Instagram Square | 1080×1080 | 1:1 |
| Instagram Story | 1080×1920 | 9:16 |

## Limitations & Gotchas

### Not Supported
- **CSS Grid** - use Flexbox only
- **z-index** - elements render in document order
- **calc()** - no CSS calculations
- **Animations** - static output only
- **React hooks** - no useState, useEffect, etc.
- **WOFF2 fonts** - use TTF, OTF, or WOFF
- **RTL languages** - Arabic, Hebrew not supported
- **3D transforms** - 2D only (rotate, scale, translate, skew)

### Important Notes
- **Fonts required**: Always provide at least one font
- **Default display is flex**: All elements default to `display: flex`
- **Default flexWrap is wrap**: Unlike CSS default
- **Images need dimensions**: Always specify width/height on `<img>`
- **Use base64 for images**: Avoids network requests during render
- **No currentColor**: Except for the `color` property itself
- **Never pass `undefined` to style props**: Causes `trim()` crash. Build style objects conditionally instead.
- **Use flexbox, avoid hardcoded dimensions**: Let content determine size with padding. Use `flex-1`, `w-full`, `items-stretch` etc. Don't manually wrap text with multiple spans. Exception: icons need fixed sizes.

### Font Loading

```typescript
// good: load font once, reuse
const fontData = await fetch(fontUrl).then(r => r.arrayBuffer())
const fonts = [{ name: 'Inter', data: fontData, weight: 400, style: 'normal' }]

// use same fonts array for multiple renders
const svg1 = await satori(element1, { fonts, width: 1200, height: 630 })
const svg2 = await satori(element2, { fonts, width: 1200, height: 630 })
```

**Recommended: Use fontsource packages** for reliable local fonts (avoids network issues):
```bash
bun add @fontsource/inter @fontsource/jetbrains-mono
```
```typescript
import { readFileSync } from 'fs';
import { join } from 'path';

const FONT_DIR = join(__dirname, 'node_modules/@fontsource/inter/files');
const fonts = [{
  name: 'Inter',
  data: readFileSync(join(FONT_DIR, 'inter-latin-400-normal.woff')), // woff only, not woff2
  weight: 400 as const,
  style: 'normal' as const,
}];
```

### Image Handling

```typescript
// convert image to base64 for embedding
const imageBuffer = await fetch(imageUrl).then(r => r.arrayBuffer())
const base64 = `data:image/png;base64,${Buffer.from(imageBuffer).toString('base64')}`

// use in component
<img src={base64} width={200} height={200} />
```

## Custom Tailwind Config

```typescript
await satori(element, {
  width: 1200,
  height: 630,
  fonts,
  tailwindConfig: {
    theme: {
      extend: {
        colors: {
          brand: '#ff6b00',
        },
        fontFamily: {
          display: ['Custom Font'],
        },
      },
    },
  },
})
```

## Debug Mode

Enable bounding boxes to debug layout issues:

```typescript
await satori(element, {
  width: 1200,
  height: 630,
  fonts,
  debug: true,  // shows element boundaries
})
```

## Resources

- [Satori GitHub](https://github.com/vercel/satori)
- [Vercel OG Image Generation](https://vercel.com/docs/functions/og-image-generation)
- [Satori Playground](https://og-playground.vercel.app/)
