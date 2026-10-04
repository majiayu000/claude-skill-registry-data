---
name: senternet-site-design
description: Convert a Claude Design export into React components and a design system.
---

# Site Design — Convert Claude Design Export to React Components

Take a Claude Design HTML export (or design from scratch) and implement it as a production-ready Vite + React + TypeScript codebase.

## What this skill does

Claude Design outputs a single self-contained HTML file with inline CSS and vanilla JS. This skill:
1. Extracts the design system (CSS variables, fonts, typography scale)
2. Converts each HTML section into a typed React component
3. Wires up routing in `src/App.tsx`
4. Starts the dev server so the user can verify visually

## Step 1 — Get the design source

Ask the user: "Do you have a Claude Design export? Provide the path to the zip file, exported directory, or HTML file. Otherwise, describe the brand (colors, fonts, tone) and I'll generate a design system from scratch."

If they provide a **zip file**: run `unzip -o <path> -d <path-without-extension>` to extract it, then locate the `index.html` (or the only `.html` file) inside the extracted directory.

If they provide a **directory**: look for `index.html` at its root, or the only `.html` file present.

If they provide a **single HTML file**: read it directly.

Everything below assumes you've read the HTML file.

## Step 2 — Extract the design system

Find the `:root { }` block in the HTML's `<style>` tag. Extract all CSS custom properties into `src/styles/design-system.css`:

```css
/* Generated from Claude Design export — edit tokens here, not inline */
:root {
  /* paste the --variable: value; lines here, verbatim */
}

/* Reset */
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
html { -webkit-text-size-adjust: 100%; }
body {
  /* copy the body { } block from the HTML */
}
::selection { /* copy */ }
a { color: inherit; text-decoration: none; }
.wrap { max-width: var(--max); margin: 0 auto; padding: 0 var(--pad); }
```

Import this file at the top of `src/index.css` (before the Tailwind import or replacing it if the design uses custom CSS instead of Tailwind).

**Detect the primary brand color.** After writing `design-system.css`, scan the CSS variables you extracted for the primary/accent color. Look for variables named `--primary`, `--accent`, `--color-primary`, `--brand`, `--highlight`, `--cta`, or any variable whose value is used on the most prominent button or hero element. If multiple candidates exist, pick the one used on the main CTA button or the most visually dominant non-neutral color. Record it (e.g. `PRIMARY_COLOR=#00d4ff`) — this value will be passed to later skills (meta tags `theme-color`, share image background, etc.). If the design has no obvious primary color, ask the user to confirm which CSS variable or hex value to treat as the brand color.

## Step 3 — Add fonts (prefer self-hosted)

Self-hosting fonts eliminates the external DNS lookup and connection overhead that Lighthouse flags under "Eliminate render-blocking resources." Use Option A unless the user explicitly prefers to keep Google Fonts.

### Option A — Self-hosted via @fontsource (recommended)

Search [fontsource.org](https://fontsource.org) for the exact package name of whatever font the design uses. Variable fonts use `@fontsource-variable/<name>`; static weights use `@fontsource/<name>`. Install it:

```bash
npm install @fontsource-variable/<font-name>
# or for static weights:
npm install @fontsource/<font-name>
```

Import it in `src/index.css` (or `src/main.tsx`):

```css
@import '@fontsource-variable/<font-name>';
```

Reference it in the design system CSS using the font family name from the design:

```css
body { font-family: 'Font Name Variable', sans-serif; }
```

Remove any Google Fonts `<link>` tags from `index.html` — they're not needed.

### Option B — Manual woff2 download (for fonts not on fontsource)

1. Use google-webfonts-helper or fontsquirrel to download woff2 files for the specific weights/styles used in the design.
2. Put the files in `public/fonts/`.
3. Add `@font-face` declarations to `src/styles/design-system.css`:

```css
@font-face {
  font-family: 'Font Name';
  src: url('/fonts/font-name-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

4. Remove any Google Fonts `<link>` tags from `index.html`.

### Option C — Keep Google Fonts (simplest, but Lighthouse will flag it)

If the user wants to skip self-hosting, add preconnect and link tags to `index.html` **above** any existing font links, before `</head>`. Keep `display=swap` on the font URL.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
```

Note: Lighthouse will report "Eliminate render-blocking resources" for this approach.

## Step 4 — Identify the page sections

Scan the HTML body. Each major `<section>`, `<header>`, `<footer>`, or logical block becomes a React component. Name each component after what it actually does in this design — derive the names from the content, not from a template.

General mapping rules:
- `<header>` / top nav → `src/components/SiteNav.tsx`
- `<footer>` → `src/components/SiteFooter.tsx`
- Each remaining `<section>` or named block → `src/pages/home/[DescriptiveName]Section.tsx`, where `[DescriptiveName]` reflects the actual content (e.g. `HeroSection`, `FeaturesSection`, `PricingSection`, `TestimonialsSection`, `CtaSection`)

Use the section's `id`, `class`, or heading text to pick a name. If a section has `id="pricing"`, call it `PricingSection`. If it has no id but contains a `<h2>What our customers say</h2>`, call it `TestimonialsSection`.

**Footer link organization (`SiteFooter.tsx`):** when the footer has more than ~4–5 links, group them into labeled categories under short headings instead of a single flat row. Common groupings:
- **Legal** — Terms, Privacy, AI Disclosure
- **Product** — Features, Pricing, Download, Changelog
- **Company** — About, Blog, Other Projects, Contact

Render each group as a column with a heading (e.g. `<h3>` or a styled label) above its links, and lay the groups out as a responsive multi-column grid (stacking on mobile). Keep a single flat row only while the footer is small; as later skills add links (AI Disclosure, Other Projects, blog, compare pages), migrate to grouped columns rather than letting the row grow unbounded. New footer links should be added into the category they belong to, not appended to the end.

## Step 5 — Convert HTML sections to React components

For each section, create the component file. Rules for conversion:

- `class=` → `className=`
- `for=` → `htmlFor=`
- Inline `style="..."` → `style={{ camelCasedProp: 'value' }}` (rare — prefer className)
- `href="#"` on interactive elements → keep as-is for now, wire up later
- `<img src="images/foo.jpg">` → use the actual image path or a placeholder; note that images from the export go in `src/assets/` or `public/images/`
- Self-closing tags: `<br>` → `<br />`, `<img>` → `<img />`
- HTML entities like `&rsquo;` → use the Unicode character directly (`'`) or a JSX expression
- `aria-*` attributes stay as-is (they're valid in JSX)
- Comments: `<!-- HTML comment -->` → `{/* JSX comment */}`
- The vanilla JS scroll reveal (`IntersectionObserver` with `.rv` / `.in` classes) → implement as a `useScrollReveal` hook (see Step 7)

Keep all the CSS class names exactly as they appear in the design's `<style>` block — don't rename them.

## Step 6 — Create the Home page

Create `src/pages/HomePage.tsx` that composes all the home sections:

```tsx
import SiteNav from '../components/SiteNav'
import HeroSection from './home/HeroSection'
// ... other sections
import SiteFooter from '../components/SiteFooter'

export default function HomePage() {
  return (
    <>
      <SiteNav />
      <div className="wrap">
        <HeroSection />
        {/* other sections */}
      </div>
      <SiteFooter />
    </>
  )
}
```

Adjust the `<div className="wrap">` wrapping to match whatever the HTML does — some designs wrap the whole page, some wrap each section individually.

## Step 7 — Implement scroll reveal hook (if the design uses it)

If the design uses an `IntersectionObserver` pattern (`rv` / `in` classes or similar), create `src/hooks/useScrollReveal.ts`:

```ts
import { useEffect } from 'react'

export function useScrollReveal(selector = '.rv') {
  useEffect(() => {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('in')
            io.unobserve(e.target)
          }
        })
      },
      { threshold: 0.1, rootMargin: '0px 0px -8% 0px' }
    )
    document.querySelectorAll<Element>(selector).forEach((el) => io.observe(el))
    return () => io.disconnect()
  }, [selector])
}
```

Call it in `HomePage` or a top-level layout component:

```tsx
import { useScrollReveal } from '../hooks/useScrollReveal'
// inside the component:
useScrollReveal()
```

Add the base animation CSS to `design-system.css` (copy the `.rv` / `.rv.in` / `@media prefers-reduced-motion` block from the HTML).

## Step 8 — Wire up smooth scroll links

If the design has `<a href="#section-id">` nav links, the HTML export likely handled them with vanilla JS. In React Router, replace the click handler with a helper:

```ts
function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (!el) return
  window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 16, behavior: 'smooth' })
  history.replaceState(null, '', '#' + id)
}
```

Call it in the nav `onClick` handlers.

## Step 9 — Copy images from the export

Images referenced in the HTML export (e.g. `images/hero.jpeg`, `images/logo.png`) need to be in `public/images/` in the Vite project.

If the user provided a zip or directory, the images are already on disk in the extracted folder. Run:
```bash
cp -r <extracted-dir>/images/* public/images/
```

Otherwise tell the user:

> "Copy the images from the Claude Design export's `images/` folder to `public/images/` in this project."

Then update the `<img src>` paths in the components to `/images/filename.ext` (absolute public path, no import needed).

For the portrait or hero image, add a `<link rel="preload" as="image" href="/images/main-hero.webp">` to `index.html` for LCP performance.

## Step 10 — Update `src/App.tsx`

Add the `HomePage` route (and lazy-load it):

```tsx
import React, { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

const HomePage = lazy(() => import('./pages/HomePage'))

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={null}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
```

## Step 11 — Build check and dev server

Run:
```bash
npx tsc --noEmit
```

Fix any TypeScript errors (usually missing `alt` props, wrong event types, or `href` on non-anchor elements).

Then run:
```bash
npm run dev
```

Tell the user: "Open http://localhost:PORT in your browser. The design should match the Claude Design export. Check each section: fonts loaded, colors correct, animations trigger on scroll, images display, responsive layout works at mobile widths."

## Step 12 — Responsive verification checklist

Ask the user to check each breakpoint the design defined (look for `@media (max-width: NNNpx)` rules in the HTML):

- [ ] Desktop (~1280px): full grid layouts, large type
- [ ] Tablet (~820px): reflow to narrower columns
- [ ] Mobile (~480px): single column, readable font sizes

If any layout breaks, the CSS class names should already be right — the issue is usually a missing `<div className="wrap">` wrapper or a component boundary that split a CSS grid across two render trees.

## Step 13 — Update `scripts/prerender.mjs` and sitemap

Add `/` to ROUTES if not already there. Prerendering a single-page portfolio doesn't need much, but running `npm run build:prod` should succeed without `✗ EMPTY` errors.

## Common pitfalls

- **Lighthouse flags external fonts**: Switch from Google Fonts CDN to `@fontsource` (Step 3, Option A). One `npm install` and one `@import` line eliminates the external origin penalty.
- **Fonts flash on first load**: If using self-hosted fonts, make sure the `@import` is at the top of `src/index.css`. If using Google Fonts (Option C), make sure the `<link rel="preconnect">` tags are in `index.html` before the CSS bundle.
- **Images 404**: Claude Design puts images in `images/` at the root; Vite public assets must be in `public/`. Absolute paths like `/images/foo.jpg` work once you copy the files there.
- **`.rv` elements don't animate**: the `IntersectionObserver` hook must run after the DOM is painted — putting `useScrollReveal()` in a component that renders conditionally can miss early elements. Put it in the top-level `HomePage` or a layout that always mounts.
- **Smooth scroll in React Router**: `<a href="#id">` without `onClick` will let the browser handle it, which works but adds `#id` to history. Use the `scrollTo` helper above to keep history clean.
- **TypeScript errors on HTML entities**: replace `&rsquo;` etc. with the actual Unicode character in JSX strings.

## Framework: Next.js track

The extraction work is identical — same design tokens, same component decomposition, same primary-color detection. Only where the output lands changes.

| Vite | Next.js |
|---|---|
| `src/styles/design-system.css` | `app/globals.css` (tokens alongside the Tailwind import) |
| `src/pages/Home.tsx` + a `<Route>` in `src/App.tsx` | `app/page.tsx` |
| `src/pages/About.tsx` + a `<Route>` | `app/about/page.tsx` |
| `src/components/` | `components/` |
| `src/components/Layout.tsx` wrapping routes | `app/layout.tsx` |
| `<a href>`/`<Link>` from react-router-dom | `<Link>` from `next/link` |
| `<img>` / `<picture>` | `next/image` |

Rules specific to this track:

- **Converted pages stay server components.** Add `'use client'` only to the leaf that needs state, an effect, or an event handler — a nav toggle, a carousel, a form. A design export usually converts to almost entirely static markup, so most components need no directive at all.
- **No `ScrollToTop` component.** The App Router resets scroll on navigation itself. Adding one is harmless but noise; adding `react-router-dom` to get it is not.
- **Fonts** go through `next/font` rather than a `<link>` to a font CDN — it self-hosts them and removes the render-blocking request. A design export that references Google Fonts by URL should be converted, not copied.
- **Interactive markup that breaks on the server** (anything touching `window`, `document`, or `localStorage` during render) must move inside a `'use client'` component and behind an effect. On the Vite track this fails only under prerender; here it fails the build.

See `/senternet-site-framework` for the full convention map.
