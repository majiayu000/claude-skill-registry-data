---
name: responsive
description: Test a web app at mobile, tablet, and desktop breakpoints. Screenshots each size, flags overflow, small touch targets, tiny text, and viewport issues. Use before shipping or after layout changes.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_resize, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_evaluate, mcp__plugin_playwright_playwright__browser_snapshot
argument-hint: [url-or-project-path]
---

# Responsive Tester

Test a web app at three breakpoints and report issues.

**Argument**: `$ARGUMENTS` is either a URL (e.g., `http://localhost:3000`) or a project path to start a dev server for. If not provided, ask.

## Breakpoints

Test at these three sizes:
- **Mobile**: 375 × 812 (iPhone baseline)
- **Tablet**: 768 × 1024 (iPad portrait)
- **Desktop**: 1280 × 800 (standard laptop)

## Process

### 0. Pick a browser tool

This skill needs a way to drive a browser. Use the first one available in the session:
- **Playwright MCP plugin** (`browser_navigate`, `browser_resize`, `browser_take_screenshot`, `browser_evaluate`) — the tool names below assume this. Install with `/plugin install playwright` if missing.
- **Claude in Chrome extension** (`mcp__claude-in-chrome__*`) — same steps; use `navigate`, `resize_window`, `computer` screenshot, and `javascript_tool` in place of the Playwright names.
- **Neither** — fall back to the CLI for screenshots and skip the JS checks:
  ```bash
  npx playwright screenshot --viewport-size=375,812 --full-page <url> mobile.png
  npx playwright screenshot --viewport-size=768,1024 --full-page <url> tablet.png
  npx playwright screenshot --viewport-size=1280,800 --full-page <url> desktop.png
  ```
  Then read the three PNGs and review them visually.

### 1. Get a running preview

If given a URL, open it with `browser_navigate`.

If given a project path, start the dev server from `package.json` scripts in the background, wait for it to listen, then `browser_navigate` to its URL.

### 2. Pre-flight checks (static analysis)

Before opening the browser, grep for common issues:

```bash
# Missing viewport meta
grep -L "viewport" src/app/layout.* public/index.html 2>/dev/null

# Fixed pixel widths that break on mobile
grep -rn "width: [0-9]\{3,4\}px" --include="*.css" --include="*.tsx" --include="*.jsx"

# Absolute positioning without responsive alternatives
grep -rn "position: absolute" src/ --include="*.css" --include="*.tsx"
```

Note anything suspicious for the browser phase.

### 3. Test each breakpoint

For each of mobile / tablet / desktop:

**a. Resize the viewport:** `browser_resize` to 375×812, 768×1024, or 1280×800.

**b. Take a screenshot:** `browser_take_screenshot`.

**c. Check for horizontal overflow:**
```javascript
// Via browser_evaluate:
({
  docWidth: document.documentElement.scrollWidth,
  viewWidth: window.innerWidth,
  overflow: document.documentElement.scrollWidth > window.innerWidth,
  overflowingElements: Array.from(document.querySelectorAll('*'))
    .filter(el => el.scrollWidth > window.innerWidth)
    .slice(0, 5)
    .map(el => ({
      tag: el.tagName.toLowerCase(),
      class: el.className,
      width: el.scrollWidth
    }))
})
```

**d. Check touch target sizes (mobile only):**
```javascript
// Via browser_evaluate:
Array.from(document.querySelectorAll('button, a, input, [role="button"]'))
  .map(el => {
    const r = el.getBoundingClientRect();
    return { tag: el.tagName, text: el.textContent?.slice(0, 30), w: r.width, h: r.height };
  })
  .filter(el => (el.w > 0 && el.w < 44) || (el.h > 0 && el.h < 44))
  .slice(0, 10)
```

**e. Check for tiny text:**
```javascript
// Via browser_evaluate:
Array.from(document.querySelectorAll('p, span, li, a, button, input'))
  .map(el => {
    const size = parseFloat(getComputedStyle(el).fontSize);
    return { tag: el.tagName, text: el.textContent?.slice(0, 40), size };
  })
  .filter(el => el.size > 0 && el.size < 14)
  .slice(0, 10)
```

### 4. Additional checks

**Viewport meta tag** (once, any breakpoint):
```javascript
document.querySelector('meta[name="viewport"]')?.content || 'MISSING'
```

Expected: `width=device-width, initial-scale=1` (or similar).

**Image sizing** (mobile):
```javascript
Array.from(document.querySelectorAll('img'))
  .map(img => ({
    src: img.src.slice(0, 60),
    natural: img.naturalWidth,
    rendered: img.width,
    oversized: img.naturalWidth > img.width * 2
  }))
  .filter(img => img.oversized)
  .slice(0, 5)
```

### 5. Report

Format as a scored report:

```markdown
## Responsive Test: [URL]

### Summary
- Mobile (375px): [Pass ✓ / Issues ⚠ / Broken ✗]
- Tablet (768px): [Pass ✓ / Issues ⚠ / Broken ✗]
- Desktop (1280px): [Pass ✓ / Issues ⚠ / Broken ✗]

### Viewport meta
✓ Correct: `width=device-width, initial-scale=1`

### Mobile (375px)
**Horizontal overflow**: ✗ Yes — page is 412px wide
- Element: `<div class="hero-grid">` renders at 420px

**Touch targets**: ⚠ 3 elements under 44px
- `<button>Subscribe</button>` — 32×32
- `<a>Read more</a>` — 28×20
- `<input type="email">` — 40×36

**Text sizes**: ⚠ 2 elements under 14px
- Footer copyright: 12px
- Badge labels: 11px

**Images**: ⚠ 1 oversized
- hero.jpg — natural 2400w, rendered 375w (load 6x data)

### Tablet (768px)
✓ No overflow
✓ All touch targets adequate
✓ Text sizes readable

### Desktop (1280px)
✓ Layout looks correct
⚠ Hero text-wrap may orphan — consider `text-wrap: balance`

### Priority fixes
1. **hero-grid overflow on mobile** — `src/components/Hero.tsx:42` — set `max-width: 100%` and use fluid sizing
2. **Subscribe button too small** — `src/components/CTA.tsx:18` — increase padding to 12px vertical minimum
3. **Oversized hero image** — use `next/image` or add responsive `srcset`
```

## Rules
- Always test all three breakpoints — never skip one
- Take screenshots at each breakpoint (for visual verification)
- Don't flag intentional choices (e.g., sticky footer, fixed navbar)
- Lead with the issues that would break the page; fold repeats of the same defect into one item with a count
- File paths + line numbers for every actionable item
- Touch target threshold is 44×44px (Apple HIG standard)
- Text size threshold is 14px for body, can be 12px for labels/badges
- If no server is running, ask before starting one
