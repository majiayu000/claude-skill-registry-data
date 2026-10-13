---
name: mobile-responsive-analyzer
description: "Analyzes web applications for mobile responsive design issues including touch targets, typography, breakpoints, navigation, images, and performance. Provides file-by-file tactical recommendations and implements fixes for Next.js 15, Tailwind CSS 4, Radix UI, and shadcn/ui projects. Use when auditing mobile UX, optimizing responsive layouts, or ensuring mobile-first best practices."
---

# Mobile Responsive Design Analyzer

## Purpose
Systematically audits web applications for mobile responsive design issues and implements fixes to ensure optimal mobile user experience. Focuses on tactical, file-specific recommendations based on 2025 best practices for modern React frameworks.

## When to Use This Skill
- Auditing existing pages/components for mobile UX issues
- Before deploying new features to production
- Converting desktop-first designs to mobile-first
- Optimizing touch interactions and responsive layouts
- Ensuring compliance with 2025 mobile UX standards

## When NOT to Use This Skill
- Accessibility/WCAG compliance audits (use dedicated accessibility tools)
- Backend API or data pipeline analysis
- Security audits or performance profiling
- Desktop-only applications

## Core Principles

### 1. Mobile-First Foundation
All code should start with mobile base styles and progressively enhance for larger screens using Tailwind breakpoints (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`).

### 2. Touch-First Interactions
Interactive elements must meet minimum touch target sizes (44×44px) and be positioned within thumb-reach zones.

### 3. Framework-Aware Analysis
Recognizes patterns specific to Next.js 15, Tailwind CSS 4, Radix UI, and shadcn/ui to provide contextually appropriate recommendations.

### 4. Tactical Implementation
Provides specific code changes, not vague suggestions. Every issue includes the exact fix needed.

## Workflow

### Phase 1: Discovery
1. Ask user which part of the codebase to analyze (or default to full app)
2. Confirm project uses Next.js 15 + Tailwind CSS 4 + Radix/shadcn (or adjust standards)
3. Set analysis scope (pages only, components only, or both)

### Phase 2: Analysis
1. Scan UI-focused files (smart filtering):
   - `src/app/**/page.tsx` (pages)
   - `src/app/**/layout.tsx` (layouts)
   - `src/components/**/*.tsx` (components)
   - Skip: API routes, backend scripts, config files

2. For each file, check against standards (see `reference/standards.md`):
   - ✅ Layout & Responsiveness
   - ✅ Touch Targets
   - ✅ Typography
   - ✅ Navigation Patterns
   - ✅ Image Optimization
   - ✅ Component Responsive Props
   - ✅ Performance Patterns

3. Categorize issues by severity:
   - **Critical**: Blocks mobile usability (e.g., 24×24px buttons, text overflow)
   - **High**: Degrades experience (e.g., missing breakpoints, non-responsive images)
   - **Enhancement**: Nice-to-have improvements (e.g., container queries, fluid typography)

### Phase 3: Report
Generate file-by-file analysis in this format:

```markdown
## Analysis Summary
Found [X] issues across [Y] files:
- [N] critical (blocks mobile usability)
- [N] high priority (degrades experience)
- [N] enhancements (nice to have)

---

## src/app/companies/page.tsx

### Critical Issues
- ❌ **Touch Targets**: Action buttons are 36×36px (need 44×44px minimum)
  - Line 45: `<Button className="h-9 w-9">` → `<Button className="h-11 w-11">`

### High Priority
- ⚠️ **Responsive Breakpoints**: Table has no mobile layout
  - Line 78-92: Add mobile card view with `hidden md:table` and custom mobile UI

### Enhancements
- 💡 **Typography**: Consider fluid typography with clamp()
  - Line 12: `text-2xl` → `text-[clamp(1.5rem,4vw,2rem)]`

### ✅ Passing
- Responsive: Uses Tailwind mobile-first breakpoints correctly
- Images: Using next/image with proper sizing

---

## src/app/programs/page.tsx
[... repeat format ...]
```

### Phase 4: User Decision
Present options:
```
What would you like me to fix?
[1] All critical issues
[2] All issues (critical + high priority)
[3] All issues including enhancements
[4] Specific files only (you choose)
[5] Show me the full report first
```

### Phase 5: Implementation
1. Implement selected fixes file-by-file
2. Use Edit tool for precise changes
3. Maintain existing code style and patterns
4. Add comments for non-obvious responsive choices

### Phase 6: Verification
1. Re-analyze only modified files
2. Generate before/after comparison:
```markdown
## Verification Report

### src/app/companies/page.tsx
Before: 3 critical, 2 high, 1 enhancement
After: ✅ 0 critical, ✅ 0 high, 1 enhancement

Changes:
✓ Touch targets increased to 44×44px (lines 45, 67, 89)
✓ Added mobile card layout for table (lines 78-110)
✓ Image converted to next/image (line 34)

Remaining:
- Enhancement: Consider fluid typography (optional)
```

3. Ask: "Continue to next file?" or "Re-run full analysis?"

## Analysis Standards

See detailed standards in `reference/standards.md`, including:

### Touch Targets
- **Minimum**: 44×44px (176px² area)
- **Recommended**: 48×48px for primary actions
- **Spacing**: 8px minimum between targets

### Typography
- **Base font**: 16px minimum
- **Line height**: 1.5× minimum
- **Fluid sizing**: Use `clamp()` for headings

### Breakpoints (Tailwind CSS 4)
- **Mobile-first**: Base styles, then `sm:`, `md:`, etc.
- **No desktop-first**: Flag any max-width media queries

### Images
- **Component**: Require `next/image` for all images
- **Responsive**: Check `sizes` attribute
- **Formats**: Verify WebP/AVIF optimization

### Framework Patterns
See `reference/framework-patterns.md` for specific patterns in:
- Next.js 15 (Server Components, next/image)
- Tailwind CSS 4 (mobile-first utilities)
- Radix UI (responsive object syntax)
- shadcn/ui (Dialog→Drawer, responsive navigation)

## Common Patterns

### Pattern: Responsive Table → Card Stack
```tsx
{/* Desktop: table */}
<table className="hidden md:table">
  {/* ... */}
</table>

{/* Mobile: card stack */}
<div className="md:hidden space-y-4">
  {items.map(item => (
    <Card key={item.id}>
      {/* ... */}
    </Card>
  ))}
</div>
```

### Pattern: Touch-Friendly Button Sizing
```tsx
{/* Bad: 36×36px */}
<Button size="sm" className="h-9 w-9">

{/* Good: 44×44px minimum */}
<Button size="default" className="min-h-11 min-w-11 p-2">
```

### Pattern: Radix UI Responsive Props
```tsx
{/* Bad: fixed width */}
<Flex width="300px">

{/* Good: responsive object */}
<Flex width={{ initial: "100%", sm: "300px", md: "500px" }}>
```

### Pattern: shadcn Dialog → Drawer on Mobile
```tsx
{/* Show Dialog on desktop, Drawer on mobile */}
<div className="hidden md:block">
  <Dialog>{/* ... */}</Dialog>
</div>
<div className="md:hidden">
  <Drawer>{/* ... */}</Drawer>
</div>
```

### Pattern: Fluid Typography
```tsx
{/* Bad: fixed size */}
<h1 className="text-4xl">

{/* Good: fluid sizing */}
<h1 className="text-[clamp(2rem,5vw,4rem)]">
```

## Smart Filtering Logic

Include files with:
- `.tsx` or `.jsx` extensions
- Located in `src/app/` or `src/components/`
- Contains JSX/React components
- Has visual/UI elements (Button, div, Image, etc.)

Exclude files with:
- API routes (`/api/` paths)
- Server actions (`.ts` without JSX)
- Config files (`.config`, `.json`)
- Backend utilities
- Test files (`*.test.tsx`)

## Edge Cases

### Server Components (Next.js 15)
- Cannot use viewport detection hooks
- Must use CSS-only responsive patterns
- Flag any client-side viewport detection in Server Components

### Data Tables
- Always provide mobile alternative (cards, accordion, or horizontal scroll)
- Touch targets for sortable headers
- Sticky headers should be touch-friendly

### Navigation Menus
- Desktop: horizontal nav or dropdown
- Mobile: hamburger → drawer/sheet
- Touch targets for menu items (44×44px minimum)

### Forms
- Full-width inputs on mobile
- Stack labels vertically
- Touch-friendly spacing between fields (16px minimum)

## Output Style

- Use emojis for severity: ❌ Critical, ⚠️ High, 💡 Enhancement, ✅ Passing
- Include line numbers for every issue
- Provide exact code changes (before → after)
- Group issues by category within each file
- Keep descriptions concise and tactical

## Verification Checklist

After implementing fixes, verify:
- [ ] All touch targets ≥ 44×44px
- [ ] All text ≥ 16px base size
- [ ] Mobile-first breakpoint usage (no max-width)
- [ ] Images use next/image with sizes
- [ ] Tables have mobile alternative
- [ ] Navigation is touch-friendly on mobile
- [ ] No horizontal scroll on mobile (320px width)
- [ ] Radix/shadcn components use responsive props
- [ ] No client-side viewport hooks in Server Components

## Reference Files

- `reference/standards.md` - Complete 2025 mobile UX standards
- `reference/framework-patterns.md` - Next.js, Tailwind, Radix, shadcn patterns
- `reference/checklist.md` - Analysis checklist template

## Example Usage

**User**: "Analyze the companies page for mobile issues"

**Skill Response**:
1. Analyzes `src/app/companies/page.tsx` and related components
2. Finds: 2 critical (touch targets), 3 high (responsive layout), 1 enhancement
3. Generates file-by-file report
4. Asks: "What would you like me to fix?"
5. User selects: "All critical issues"
6. Implements touch target fixes
7. Re-analyzes and confirms: ✅ 0 critical issues remaining
8. Asks: "Fix high priority issues too?"
