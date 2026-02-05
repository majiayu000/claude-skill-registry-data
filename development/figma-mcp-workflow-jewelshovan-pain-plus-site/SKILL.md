---
name: figma-mcp-workflow
description: Standardize Figma-to-code workflow using Figma MCP - always get_design_context first, then screenshot, use project tokens not hardcoded values, validate 1:1 parity
---

# Figma MCP Workflow

This skill standardizes the Figma-to-code workflow using the Figma MCP (Model Context Protocol). Follow this process to ensure high-fidelity implementations that respect project conventions and design systems.

## Workflow Overview

The workflow consists of 6 mandatory steps that must be executed in order:

1. **Fetch Design Context** - Get structured node data from Figma
2. **Handle Truncation** - Fetch metadata and re-query specific nodes if needed
3. **Get Visual Reference** - Capture screenshot for validation
4. **Download Assets** - Retrieve images/SVGs from localhost sources
5. **Implement** - Build using project conventions and tokens
6. **Validate** - Ensure 1:1 parity with Figma design

---

## Step-by-Step Process

### Step 1: Fetch Design Context

**ALWAYS start with `get_design_context`** to retrieve structured node data including styles, layout, and component hierarchy.

```typescript
// Call the Figma MCP tool
mcp__figma-desktop__get_design_context({
  nodeId: "123:456", // Extract from URL or use current selection
  clientLanguages: "typescript,javascript",
  clientFrameworks: "react"
})
```

**What you'll receive:**
- Component hierarchy and structure
- Style properties (colors, typography, spacing, borders)
- Layout data (flexbox, grid, positioning)
- Text content and asset references
- React + Tailwind code (use as reference, not final implementation)

**Important:** The returned React + Tailwind code is a **design reference**, not production-ready code. You must adapt it to project conventions.

---

### Step 2: Handle Truncation (If Needed)

If the response is too large and gets truncated, you'll see a message indicating this. When this happens:

1. **Fetch metadata** to get a node map:
```typescript
mcp__figma-desktop__get_metadata({
  nodeId: "123:456", // Parent node or page
  clientLanguages: "typescript,javascript",
  clientFrameworks: "react"
})
```

2. **Identify specific child nodes** from the XML structure

3. **Re-fetch each node individually** using `get_design_context`:
```typescript
// Fetch specific nodes that were truncated
mcp__figma-desktop__get_design_context({
  nodeId: "123:789", // Specific child node
  clientLanguages: "typescript,javascript",
  clientFrameworks: "react"
})
```

---

### Step 3: Get Visual Reference

**Always capture a screenshot** for visual validation:

```typescript
mcp__figma-desktop__get_screenshot({
  nodeId: "123:456",
  clientLanguages: "typescript,javascript",
  clientFrameworks: "react"
})
```

**Use the screenshot to:**
- Verify spacing and alignment
- Validate color accuracy
- Confirm typography hierarchy
- Check responsive behavior
- Reference during implementation

---

### Step 4: Download Assets

If Figma MCP returns localhost sources for images or SVGs:

**DO:**
- Download assets from provided localhost URLs
- Save to appropriate project directories (`public/assets/`, `src/assets/`)
- Use relative paths in implementation
- Optimize assets if needed (compress images, clean SVGs)

**DO NOT:**
- Create placeholder images when real assets are provided
- Import new icon packages (Lucide, Heroicons, etc.)
- Use external CDN links for assets available locally

**Example:**
```typescript
// Figma MCP provides: http://localhost:PORT/asset.svg
// Download and save to: /public/assets/icons/logo.svg
// Use in code:
<img src="/assets/icons/logo.svg" alt="Logo" />
```

---

### Step 5: Implement Using Project Conventions

This is where you translate the Figma design into production code. Follow these rules:

#### 5.1 Use Project Color Tokens

**NEVER hardcode colors.** Use project tokens from `src/index.css` (Tailwind v4 @theme block).

**Wrong:**
```tsx
<div className="bg-blue-500 text-white border-gray-200">
```

**Correct:**
```tsx
<div className="bg-[hsl(var(--color-primary))] text-[hsl(var(--color-primary-foreground))] border-[hsl(var(--color-border))]">
```

**Common project tokens:**
```css
/* From src/index.css @theme block */
--color-background: /* Page background */
--color-foreground: /* Main text color */
--color-primary: /* Brand primary */
--color-primary-foreground: /* Text on primary */
--color-secondary: /* Secondary accent */
--color-secondary-foreground: /* Text on secondary */
--color-muted: /* Muted backgrounds */
--color-muted-foreground: /* Muted text */
--color-accent: /* Accent color */
--color-accent-foreground: /* Text on accent */
--color-border: /* Border color */
--color-input: /* Input borders */
--color-ring: /* Focus rings */
--color-destructive: /* Error/delete */
--color-destructive-foreground: /* Text on destructive */
```

**Token usage examples:**
```tsx
// Backgrounds
className="bg-[hsl(var(--color-background))]"
className="bg-[hsl(var(--color-primary))]"
className="bg-[hsl(var(--color-muted))]"

// Text colors
className="text-[hsl(var(--color-foreground))]"
className="text-[hsl(var(--color-primary))]"
className="text-[hsl(var(--color-muted-foreground))]"

// Borders
className="border-[hsl(var(--color-border))]"
className="border-[hsl(var(--color-input))]"

// Focus states
className="focus:ring-[hsl(var(--color-ring))]"
```

#### 5.2 Reuse Existing Components

**NEVER reinvent shadcn components.** Check `components/ui/` first.

**Available components:**
- `Button` - All button variants
- `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`
- `Input`, `Textarea`, `Select`
- `Badge` - Labels and tags
- `Dialog`, `Sheet`, `Popover`, `DropdownMenu`
- `Tabs`, `Accordion`, `Collapsible`
- `Avatar`, `Separator`, `Skeleton`
- `Toast`, `Alert`, `AlertDialog`
- And more...

**Wrong:**
```tsx
<div className="rounded-lg bg-[hsl(var(--color-primary))] px-4 py-2 text-[hsl(var(--color-primary-foreground))] hover:bg-[hsl(var(--color-primary))]/90">
  Click me
</div>
```

**Correct:**
```tsx
import { Button } from "@/components/ui/button"

<Button>Click me</Button>
```

**Component reuse checklist:**
- [ ] Check if shadcn component exists in `components/ui/`
- [ ] Use component variants (size, variant props)
- [ ] Extend with composition, not duplication
- [ ] Import types for proper TypeScript support

#### 5.3 Use Typography and Spacing Tokens

**Typography scale:**
```tsx
// Headings
<h1 className="text-4xl font-bold">
<h2 className="text-3xl font-semibold">
<h3 className="text-2xl font-semibold">
<h4 className="text-xl font-semibold">

// Body text
<p className="text-base">
<p className="text-sm text-[hsl(var(--color-muted-foreground))]">
<p className="text-xs text-[hsl(var(--color-muted-foreground))]">
```

**Spacing scale:**
```tsx
// Use Tailwind's spacing scale (based on 0.25rem units)
gap-4  // 1rem
gap-6  // 1.5rem
gap-8  // 2rem

p-4    // padding: 1rem
px-6   // padding-left/right: 1.5rem
py-8   // padding-top/bottom: 2rem

space-y-4  // vertical spacing between children
```

#### 5.4 Respect Project Architecture

**Routing:**
- Use React Router patterns already in the project
- Don't introduce new routing libraries

**State Management:**
- Follow existing patterns (Context, hooks, etc.)
- Don't introduce Redux/Zustand unless discussed

**File Structure:**
- Components in `src/components/`
- Pages/routes in `src/pages/`
- Utilities in `src/lib/`
- Types in component files or `src/types/`

**TypeScript:**
- Always use TypeScript
- Define proper interfaces for props
- Avoid `any` types

---

### Step 6: Validate 1:1 Parity

Before marking implementation complete, validate against the Figma screenshot:

#### Validation Checklist

**Visual Parity:**
- [ ] Layout matches Figma (spacing, alignment, sizing)
- [ ] Colors match exactly (use screenshot color picker if needed)
- [ ] Typography hierarchy is correct (sizes, weights, line heights)
- [ ] Borders, shadows, and effects match
- [ ] Icons and images are positioned correctly
- [ ] Responsive behavior matches design intentions

**Code Quality:**
- [ ] No hardcoded colors (all using CSS variables)
- [ ] No hardcoded spacing values (using Tailwind scale)
- [ ] Reusing shadcn components where applicable
- [ ] Proper TypeScript types defined
- [ ] Assets downloaded and referenced correctly
- [ ] No new icon packages imported
- [ ] Follows project file structure

**Accessibility:**
- [ ] Semantic HTML elements used
- [ ] Proper ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Color contrast meets WCAG standards

**Performance:**
- [ ] Images optimized
- [ ] No unnecessary re-renders
- [ ] Proper React key props in lists
- [ ] Lazy loading for heavy components

---

## Complete Example

### Scenario
User provides Figma URL: `https://figma.com/design/ABC123/MyApp?node-id=1-2`

### Implementation

**Step 1: Extract node ID and fetch design context**
```
Node ID: 1:2
```

Call `get_design_context` with:
- nodeId: "1:2"
- clientLanguages: "typescript,javascript"
- clientFrameworks: "react"

**Step 2: Analyze response**
Response includes:
- Card component with button
- Primary color: #3B82F6
- Text: "Get Started"
- Icon: ChevronRight

**Step 3: Get screenshot**
Call `get_screenshot` with nodeId "1:2" for visual reference

**Step 4: Download assets**
If icon is provided as localhost source, download to `public/assets/icons/`

**Step 5: Implement**

**Wrong approach (using Figma MCP output as-is):**
```tsx
// Don't do this!
<div className="bg-blue-500 text-white rounded-lg p-6">
  <h2 className="text-2xl font-bold mb-2">Welcome</h2>
  <p className="text-gray-100 mb-4">Get started with our platform</p>
  <button className="bg-white text-blue-500 px-4 py-2 rounded-md flex items-center gap-2">
    Get Started
    <ChevronRight /> {/* New icon import! */}
  </button>
</div>
```

**Correct approach (project conventions):**
```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function WelcomeCard() {
  return (
    <Card className="bg-[hsl(var(--color-primary))] text-[hsl(var(--color-primary-foreground))]">
      <CardHeader>
        <CardTitle className="text-2xl">Welcome</CardTitle>
        <CardDescription className="text-[hsl(var(--color-primary-foreground))]/90">
          Get started with our platform
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Button
          variant="secondary"
          className="flex items-center gap-2"
        >
          Get Started
          <img
            src="/assets/icons/chevron-right.svg"
            alt=""
            className="w-4 h-4"
          />
        </Button>
      </CardContent>
    </Card>
  )
}
```

**Step 6: Validate**
- [x] Card component reused from shadcn
- [x] Button component reused with variant
- [x] Colors use CSS variables (--color-primary)
- [x] Icon downloaded from localhost, not imported
- [x] Layout matches screenshot
- [x] TypeScript interface defined (if props needed)

---

## Anti-Patterns to Avoid

### Don't Hardcode Colors
```tsx
// WRONG
<div className="bg-blue-500 text-white border-gray-200">

// CORRECT
<div className="bg-[hsl(var(--color-primary))] text-[hsl(var(--color-primary-foreground))] border-[hsl(var(--color-border))]">
```

### Don't Import New Icon Libraries
```tsx
// WRONG
import { ChevronRight } from "lucide-react"

// CORRECT - Use asset from Figma
<img src="/assets/icons/chevron-right.svg" alt="" className="w-4 h-4" />
```

### Don't Recreate Existing Components
```tsx
// WRONG
<div className="inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold">
  New
</div>

// CORRECT
import { Badge } from "@/components/ui/badge"
<Badge>New</Badge>
```

### Don't Skip Visual Validation
```tsx
// WRONG - Implementing without screenshot reference

// CORRECT - Always get screenshot and validate against it
```

### Don't Create Placeholders When Assets Exist
```tsx
// WRONG
<div className="w-full h-64 bg-gray-200 flex items-center justify-center">
  Image placeholder
</div>

// CORRECT - Use provided localhost asset
<img src="/assets/images/hero.png" alt="Hero" className="w-full h-64 object-cover" />
```

---

## Quick Reference

### Token Mapping

| Figma MCP Output | Project Token |
|------------------|---------------|
| `bg-blue-500` | `bg-[hsl(var(--color-primary))]` |
| `text-white` | `text-[hsl(var(--color-primary-foreground))]` |
| `bg-gray-100` | `bg-[hsl(var(--color-muted))]` |
| `text-gray-600` | `text-[hsl(var(--color-muted-foreground))]` |
| `border-gray-200` | `border-[hsl(var(--color-border))]` |
| `bg-red-500` | `bg-[hsl(var(--color-destructive))]` |

### Component Mapping

| Figma MCP Pattern | shadcn Component |
|-------------------|------------------|
| Card with header/body | `Card`, `CardHeader`, `CardContent` |
| Button | `Button` with variants |
| Input field | `Input` or `Textarea` |
| Dropdown | `Select` or `DropdownMenu` |
| Modal | `Dialog` or `Sheet` |
| Tag/Label | `Badge` |
| Divider | `Separator` |
| Loading state | `Skeleton` |

### Workflow Checklist

- [ ] 1. Fetch design context with `get_design_context`
- [ ] 2. Handle truncation if needed with `get_metadata`
- [ ] 3. Get screenshot with `get_screenshot`
- [ ] 4. Download all localhost assets
- [ ] 5. Map colors to project tokens
- [ ] 6. Reuse shadcn components
- [ ] 7. Follow project structure
- [ ] 8. Validate against screenshot
- [ ] 9. Check TypeScript types
- [ ] 10. Verify no hardcoded values

---

## Summary

**Always remember:**
1. Figma MCP output is a **reference**, not final code
2. **Never** hardcode colors - use CSS variables
3. **Never** import new icon packages - use Figma assets
4. **Always** reuse shadcn components
5. **Always** validate against screenshot
6. Strive for **pixel-perfect parity**

By following this workflow, you'll ensure consistent, maintainable implementations that respect both the design system and project conventions.
