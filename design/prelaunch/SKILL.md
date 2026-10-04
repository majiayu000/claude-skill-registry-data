---
name: prelaunch
description: Pre-launch review for web apps. Code-level audit covering accessibility, responsive design, SEO, error states, performance, and common issues. Run before deploying.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
argument-hint: [project-path-or-name]
---

# Pre-Launch Review

Run a comprehensive code-level audit on a web app before it goes live.

**Argument**: `$ARGUMENTS` is the project path or name (e.g., `~/projects/my-app`). If not provided, ask.

## Process

### 1. Identify the project
- Resolve the project path from the argument
- Read `package.json` to understand the stack (Next.js, Vite, etc.)
- Identify the main entry point and page components

### 2. Run the build
```bash
cd [project-path]
npm run build 2>&1
```
- Capture and report any build errors or warnings
- Note bundle size warnings if present

### 3. Audit these 8 categories

Scan all page/component files and check each category. Use Glob and Grep to find issues efficiently. Be specific — reference exact files and line numbers.

#### A. Accessibility
- Images missing `alt` attributes
- Interactive elements missing labels or `aria-*` attributes
- Missing focus styles (check for `outline: none` without replacement)
- Color contrast issues (flag hardcoded light-on-light or dark-on-dark text)
- Missing `lang` attribute on `<html>`
- Form inputs without associated labels
- Heading hierarchy skips (h1 → h3)

#### B. Responsive & Mobile
- Missing `<meta name="viewport">` tag
- Fixed pixel widths that would break on mobile (look for `width: [large number]px` without max-width)
- Text too small for mobile (font-size below 14px on body text)
- Touch targets too small (buttons/links smaller than 44x44px)
- Horizontal overflow risks (wide tables, code blocks, images without max-width)
- Missing responsive breakpoints for key layouts

#### C. Error & Loading States
- API calls / data fetching without error handling
- Missing loading indicators for async operations
- Empty state handling (what shows when there's no data?)
- Form submission without disabled state or feedback
- Missing 404 / error page

#### D. SEO & Meta
- Missing or generic `<title>` tag
- Missing `<meta name="description">`
- Missing OG tags (`og:title`, `og:description`, `og:image`)
- Missing favicon
- Missing canonical URL
- Broken or placeholder text in meta tags ("Lorem ipsum", "TODO", "My App")

#### E. Links & Assets
- Broken internal links (references to routes/pages that don't exist)
- Dead imports (importing from files that don't exist)
- Hardcoded `localhost` or development URLs
- Placeholder content still in the code ("lorem", "test", "TODO", "FIXME")
- Console.log statements left in production code
- Commented-out code blocks that should be cleaned up

#### F. Performance
- Unoptimized images (large PNGs/JPGs without lazy loading or sizing)
- Missing `loading="lazy"` on below-fold images
- Large dependencies that could be lighter (check bundle if available)
- Missing font `display: swap` for custom fonts
- Render-blocking resources

#### G. Interface Polish
- Missing `text-wrap: balance` on headings (prevents orphaned words)
- Nested elements with mismatched border radius (outer should = inner + padding)
- Missing `-webkit-font-smoothing: antialiased` on body/layout
- Numbers that shift on update — missing `font-variant-numeric: tabular-nums`
- Interactive animations using keyframes instead of CSS transitions (breaks interruptibility)
- Entry animations that move as one block — should split & stagger (80-100ms delay per element)
- Exit animations as prominent as entry — exits should be subtler (smaller translateY)
- Geometric centering that looks off — check optical alignment (especially icon buttons, play icons)
- Solid borders where layered box-shadows would add better depth
- Images without subtle outline (`outline: 1px solid rgba(0,0,0,0.1)` + negative offset)

#### H. Security & Best Practices
- Exposed API keys or secrets in client-side code
- Missing `rel="noopener noreferrer"` on external `target="_blank"` links
- Forms without CSRF protection (if applicable)
- Missing HTTPS references (hardcoded `http://` URLs)
- `dangerouslySetInnerHTML` or equivalent without sanitization

### 4. Output format

Present results as a scored checklist. Group by category.

```
## Pre-Launch Review: [Project Name]

### Summary
[X/8 categories passed] — [one-line verdict: Ready to ship / Needs fixes / Needs work]

### A. Accessibility — [Pass ✓ / Warning ⚠ / Fail ✗]
- ✓ All images have alt text
- ⚠ `src/components/Button.tsx:14` — missing focus style
- ✗ `src/pages/index.tsx:1` — missing lang attribute on html

### B. Responsive & Mobile — [Pass ✓ / Warning ⚠ / Fail ✗]
...

[continue for all 8 categories]

### Priority Fixes
1. [Most critical issue — file:line — what to change]
2. [Second most critical — file:line — what to change]
3. [Third — file:line — what to change]
```

**Scoring:**
- **Pass ✓** = No issues found in this category
- **Warning ⚠** = Minor issues that won't block launch but should be fixed
- **Fail ✗** = Issues that should be fixed before going live

## Rules
- Be specific: always include file paths and line numbers
- Don't flag framework-handled things (e.g., Next.js handles viewport meta automatically)
- Don't flag things that are clearly intentional design choices
- Lead with the issues that would block launch; fold repeats of the same defect into one item with a count
- If screenshots are provided, review them visually too (mobile readability, visual bugs, layout issues)
- Stack-aware: adjust checks based on the framework (Next.js, Vite, Astro, etc.)
