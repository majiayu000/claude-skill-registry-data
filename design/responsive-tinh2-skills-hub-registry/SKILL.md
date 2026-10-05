---
name: responsive
description: "Audit and fix responsive design issues across all breakpoints. Scans for fixed widths that cause mobile overflow, missing media query variants, non-responsive images, undersized touch targets below 48px, unreadable typography, and horizontal scroll violations.."
version: "2.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Audit the current project for responsive design issues across standard breakpoints.
Find and fix fixed widths that break on mobile, missing media queries, non-responsive
images, overflow problems, undersized touch targets, and unreadable text on small screens.
Verify no horizontal scroll at any breakpoint.

INPUT:
$ARGUMENTS

The user may specify:
1. Specific screens or components to audit.
2. Custom breakpoints (default: mobile 375, tablet 768, desktop 1280, wide 1920).
3. A focus area -- "mobile-first", "tablet", "desktop-down".
If no arguments, audit the entire project across all default breakpoints.

============================================================
PHASE 1 -- FRAMEWORK AND LAYOUT DETECTION
============================================================

Detect the frontend framework and existing responsive patterns:

| Indicator | Framework | Responsive System |
|-----------|-----------|------------------|
| pubspec.yaml | Flutter | MediaQuery, LayoutBuilder, Expanded, Flexible |
| tailwind.config.* | Tailwind CSS | Breakpoint prefixes (sm:, md:, lg:, xl:, 2xl:) |
| package.json with "next" or "react" | React/Next.js | CSS media queries, Container queries |
| package.json with "vue" | Vue | CSS media queries, Container queries |
| package.json with "@angular/core" | Angular | CSS media queries, Angular CDK BreakpointObserver |
| *.module.css | CSS Modules | CSS media queries within modules |
| styled-components/emotion | CSS-in-JS | Media query helpers |

Check for existing responsive infrastructure:
- Breakpoint constants or configuration
- Responsive utility classes or hooks (useMediaQuery, useBreakpoint)
- Layout components (Container, Grid, ResponsiveBuilder)
- Existing media queries and their values

Record: FRAMEWORK, RESPONSIVE_SYSTEM, BREAKPOINTS, SRC_DIR

Define working breakpoints (override with user input if provided):
- **mobile:** 375px (iPhone SE / small Android)
- **mobile-lg:** 428px (iPhone Pro Max)
- **tablet:** 768px (iPad portrait)
- **tablet-lg:** 1024px (iPad landscape)
- **desktop:** 1280px (standard laptop)
- **wide:** 1920px (full HD monitor)

============================================================
PHASE 2 -- RESPONSIVE ISSUE SCAN
============================================================

Scan every screen and component file for responsive design violations.

Step 2.1 -- Fixed Width Issues

Search for elements with fixed widths that will break on smaller screens:
- CSS: `width: Npx` where N > 375 without a max-width or responsive wrapper
- Tailwind: `w-[Npx]` or `w-96` etc. without responsive variants
- Flutter: `SizedBox(width: N)` or `Container(width: N)` where N > screen width
- Inline styles: `style="width: Npx"`

For each fixed width found, classify:
- BREAKING: Will cause horizontal overflow on mobile (width > 375px with no flex/scroll parent)
- RISKY: May cause issues on small screens (width > 300px in a constrained layout)
- SAFE: Inside a scrollable container or has responsive fallback

Step 2.2 -- Missing Responsive Variants

Check for styles that lack breakpoint-appropriate variants:
- Font sizes that are too large on mobile (>24px body text, >40px headings without scaling)
- Padding/margins that consume too much space on mobile (>32px horizontal padding on mobile)
- Grid layouts that do not collapse to single column on mobile
- Flex layouts that do not wrap on narrow screens
- Multi-column layouts without responsive column counts

Step 2.3 -- Image Responsiveness

Check all images for responsive handling:
- Missing `max-width: 100%` or equivalent
- Fixed width/height without aspect ratio preservation
- No `srcset` or responsive image component usage
- Large images loaded on mobile without size optimization
- Flutter: Image widgets without `fit` property or without constraints

Step 2.4 -- Overflow Detection

Search for elements that may cause horizontal scroll:
- `overflow: hidden` that cuts content rather than handling it properly
- `overflow-x: auto` that creates unexpected scroll areas
- `white-space: nowrap` on text that could be long
- Tables without horizontal scroll wrapper
- Code blocks without overflow handling
- Flutter: Row without Expanded/Flexible children, unbounded width

Step 2.5 -- Touch Target Audit

Scan all interactive elements for minimum touch target size:
- Buttons, links, icons, checkboxes, radio buttons, toggles
- Minimum size: 48x48px (Material guideline) / 44x44pt (Apple HIG)
- Adjacent touch targets must have at least 8px spacing
- Small icon buttons without adequate padding
- Flutter: IconButton, GestureDetector, InkWell hit areas

Step 2.6 -- Typography Scaling

Check text readability across breakpoints:
- Body text below 14px on mobile
- Line lengths exceeding 80 characters on wide screens (needs max-width constraint)
- Line height too tight on mobile (below 1.4 for body text)
- Text truncation that hides important content
- Flutter: Text that does not respect textScaleFactor

============================================================
PHASE 3 -- RESPONSIVE FIXES
============================================================

Fix all issues found in Phase 2, ordered by severity.

Step 3.1 -- Fix Breaking Width Issues

For each BREAKING fixed width:
- Replace fixed width with responsive alternatives:
  - CSS: `width: 100%` with `max-width: Npx`
  - Tailwind: `w-full max-w-lg` or responsive variants `w-full md:w-96`
  - Flutter: Use `Expanded`, `Flexible`, `ConstrainedBox`, or `MediaQuery` based sizing
- Wrap wide content in scrollable containers where fixed width is intentional (tables, code)
- Ensure parent containers use responsive layout (Flexbox, Grid, Wrap)

Step 3.2 -- Add Responsive Variants

For layouts missing responsive behavior:
- **Grid layouts:** Add responsive column counts
  - CSS: `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`
  - Tailwind: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
  - Flutter: Use `LayoutBuilder` to switch between column counts
- **Font sizes:** Scale down headings on mobile
  - CSS: Use `clamp()` for fluid typography: `font-size: clamp(1.5rem, 4vw, 2.5rem)`
  - Tailwind: `text-xl md:text-2xl lg:text-4xl`
  - Flutter: Scale with `MediaQuery.textScalerOf(context)` awareness
- **Spacing:** Reduce padding on mobile
  - CSS: `padding: 16px` at mobile, `padding: 32px` at desktop
  - Tailwind: `p-4 md:p-8`
  - Flutter: Use `MediaQuery.sizeOf(context)` to adjust EdgeInsets
- **Navigation:** Collapse desktop nav to hamburger/bottom nav on mobile

Step 3.3 -- Fix Image Responsiveness

For each non-responsive image:
- Add `max-width: 100%; height: auto;` or equivalent
- Add `srcset` and `sizes` attributes for resolution switching
- Use `<picture>` element or framework image component (next/image, CachedNetworkImage)
- Set appropriate `loading="lazy"` for below-fold images
- Flutter: Add `fit: BoxFit.cover` or `BoxFit.contain` with constrained parent

Step 3.4 -- Fix Overflow Issues

For each overflow violation:
- Tables: Wrap in a horizontally scrollable container with visual scroll indicator
- Long text: Add `overflow-wrap: break-word` or `text-overflow: ellipsis` as appropriate
- Wide content: Add horizontal scroll or responsive sizing
- Flutter: Wrap Row in SingleChildScrollView or use Expanded/Flexible

Step 3.5 -- Fix Touch Targets

For each undersized touch target:
- Increase padding to meet 48x48px minimum
- Add `min-height` and `min-width` to interactive elements
- Flutter: Use `constraints: BoxConstraints(minWidth: 48, minHeight: 48)` on tappable widgets
- Ensure 8px minimum spacing between adjacent targets

Step 3.6 -- Fix Typography Issues

For each typography problem:
- Set minimum body text size to 16px on mobile (prevents iOS zoom on input focus)
- Add `max-width: 65ch` to text containers on wide screens
- Adjust line height for mobile (minimum 1.5 for body text)
- Ensure text scales with system font size settings

Commit per category:
- "fix(responsive): replace fixed widths with responsive layouts"
- "fix(responsive): add breakpoint variants for grid and typography"
- "fix(responsive): make images responsive with proper sizing"
- "fix(responsive): fix overflow and horizontal scroll issues"
- "fix(responsive): increase touch target sizes to 48px minimum"

============================================================
PHASE 4 -- BREAKPOINT VERIFICATION
============================================================

Walk through every screen at each breakpoint and verify:

| Screen | 375px | 428px | 768px | 1024px | 1280px | 1920px |
|--------|-------|-------|-------|--------|--------|--------|
| Home | OK/ISSUE | OK/ISSUE | OK/ISSUE | OK/ISSUE | OK/ISSUE | OK/ISSUE |

For each screen at each breakpoint, check:
1. No horizontal scroll (critical -- automatic fail if present)
2. Content is readable without zooming
3. Interactive elements are reachable and tappable
4. Images are properly sized
5. Layout is appropriate for the viewport
6. No content is cut off or hidden unintentionally

Fix any remaining issues discovered during verification.

============================================================
PHASE 5 -- STATIC ANALYSIS
============================================================

Run the framework's static analysis:
- Flutter: `flutter analyze`
- TypeScript: `tsc --noEmit`
- ESLint / Stylelint if configured
- Tailwind: Check for unused or conflicting responsive classes

Fix all errors and warnings introduced by responsive changes.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate:

1. Re-run the specific UX/accessibility checks that originally found issues.
2. Run the project's test suite to verify fixes didn't break functionality.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat up to 3 iterations.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context

============================================================
OUTPUT
============================================================

```
## Responsive Audit Complete

### Framework: [detected]
### Breakpoints Tested: 375px, 428px, 768px, 1024px, 1280px, 1920px

### Issues Found and Fixed
| Category | Found | Fixed | Remaining |
|----------|-------|-------|-----------|
| Fixed widths (breaking) | N | N | N |
| Missing responsive variants | N | N | N |
| Non-responsive images | N | N | N |
| Overflow / horizontal scroll | N | N | N |
| Touch targets < 48px | N | N | N |
| Typography scaling issues | N | N | N |

### Breakpoint Verification Matrix
| Screen | Mobile | Tablet | Desktop | Wide |
|--------|--------|--------|---------|------|
| [name] | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |

### Files Modified
| File | Changes |
|------|---------|
| [path] | [description] |

### Verdict
RESPONSIVE READY: All screens pass at all breakpoints. No horizontal scroll.
NEEDS WORK: [N] screens have remaining issues at [breakpoints].
```

============================================================
NEXT STEPS
============================================================

After responsive audit:
- "Run `/ux` for a full UX and accessibility audit."
- "Run `/dark-mode` to verify dark mode works across all breakpoints."
- "Run `/design-system` to ensure responsive tokens are part of the design system."
- "Run `/qa` to verify responsive changes did not break functionality."
- Test on actual devices -- code-level audit catches most issues but device testing confirms.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /responsive — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT hide content on mobile with `display: none` unless it is truly optional -- provide an alternative way to access it.
- Do NOT use viewport units (vw/vh) for font sizes without a clamp or min/max -- they can become unreadable at extremes.
- Do NOT disable zoom with `user-scalable=no` or `maximum-scale=1` -- this is an accessibility violation.
- Do NOT assume all mobile users are on phones -- tablets in portrait mode are 768px wide.
- Do NOT add horizontal scroll to the page body -- only use it for specific content blocks (tables, code, carousels).
- Do NOT change the visual order of content at different breakpoints unless the reading order remains logical.
- Do NOT apply responsive fixes only to specific pages -- apply fixes to shared components and layouts that affect all pages.
- Do NOT use CSS `!important` to fix responsive issues -- fix the specificity or cascade instead.
