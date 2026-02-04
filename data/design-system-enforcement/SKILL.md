---
name: design-system-enforcement
description: Mandatory design system guidelines for shadcn/ui with Tailwind v4. Enforces 4 font sizes, 2 weights, 8pt grid spacing, 60/30/10 color rule, OKLCH colors, and accessibility standards. Use when creating components, pages, or any UI elements. ALL agents MUST read and validate against design system before generating code.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Design System Enforcement

**Purpose:** Enforce consistent, accessible, and beautiful UI across all Next.js projects using shadcn/ui with Tailwind v4.

**Activation Triggers:**

- Creating new components or pages
- Generating UI elements
- Styling React components
- Setting up project design system
- Before ANY UI code generation
- Component library initialization
- Design system validation needed

**Key Resources:**

- `scripts/setup-design-system.sh` - Interactive design system configuration
- `scripts/validate-design-system.sh` - Validate code against design system
- `templates/design-system-template.md` - Template with placeholders
- `examples/taskflow-ai-example.md` - Complete example configuration

## Core Design Principles (MANDATORY)

### 1. Typography: 4 Sizes, 2 Weights ONLY

**STRICTLY ENFORCED:**

- ✅ Size 1: Large headings
- ✅ Size 2: Subheadings
- ✅ Size 3: Body text
- ✅ Size 4: Small text/labels

- ✅ Semibold: Headings and emphasis
- ✅ Regular: Body text and UI

**❌ FORBIDDEN:**

- More than 4 font sizes
- Additional font weights (bold, light, etc.)
- Inconsistent size application

### 2. 8pt Grid System

**STRICTLY ENFORCED:**

- ALL spacing MUST be divisible by 8 or 4
- ✅ Allowed: 8, 16, 24, 32, 40, 48, 56, 64px
- ❌ Forbidden: 25, 11, 7, 13, 15, 19px

**Tailwind Classes:**

```
p-2 (8px)   | m-2 (8px)   | gap-2 (8px)
p-4 (16px)  | m-4 (16px)  | gap-4 (16px)
p-6 (24px)  | m-6 (24px)  | gap-6 (24px)
p-8 (32px)  | m-8 (32px)  | gap-8 (32px)
```

### 3. 60/30/10 Color Rule

**STRICTLY ENFORCED:**

- 60% Neutral (`bg-background`) - White/dark backgrounds
- 30% Complementary (`text-foreground`) - Text and icons
- 10% Accent (`bg-primary`) - CTAs and highlights only

**❌ FORBIDDEN:**

- Overusing accent colors (>10%)
- Multiple competing accent colors
- Insufficient contrast ratios

### 4. Clean Visual Structure

**REQUIRED:**

- Logical grouping of related elements
- Deliberate spacing following 8pt grid
- Proper alignment within containers
- Simplicity over flashiness

## Setup Workflow

### 1. Initialize Design System

Run setup script during project initialization:

```bash
# Interactive setup
./scripts/setup-design-system.sh

# Guided configuration:
# 1. Project name and brand color
# 2. Typography scale (4 sizes)
# 3. Color configuration (OKLCH format)
# 4. Dark mode colors
# 5. Figma design system URL

# Generates: design-system.md in project root
```

**What Gets Configured:**

- Project-specific brand colors
- Font size scale (must be 4 sizes)
- OKLCH color values
- Dark mode palette
- globals.css color variables
- Design system metadata

### 2. Validate Existing Code

Check if existing code follows design system:

```bash
# Validate all components
./scripts/validate-design-system.sh

# Checks performed:
# - Font size count (must be ≤ 4)
# - Font weight usage (must be 2)
# - Spacing divisibility (by 8 or 4)
# - Color distribution (60/30/10)
# - Custom CSS usage (should use Tailwind)
# - shadcn/ui component usage
# - Accessibility compliance
```

**Validation Output:**

```
✅ Typography: 4 sizes, 2 weights
✅ Spacing: All divisible by 8/4
❌ Colors: Accent usage at 15% (exceeds 10%)
❌ Custom CSS: Found 3 instances, use Tailwind utilities
⚠️  Accessibility: Missing ARIA labels on 2 components
```

### 3. Before Creating UI

**MANDATORY AGENT WORKFLOW:**

```bash
# 1. Read design system (REQUIRED)
cat design-system.md

# 2. Understand constraints
# - Only 4 font sizes from config
# - Only 2 font weights
# - All spacing divisible by 8/4
# - Color distribution 60/30/10
# - OKLCH colors only
# - shadcn/ui components only

# 3. Generate code following design system

# 4. Self-validate before completion
./scripts/validate-design-system.sh app/components/MyNewComponent.tsx
```

## Design System Configuration

### Typography Configuration

**From Template:**

```markdown
Size 1: {{FONT_SIZE_1}} - Large headings
Size 2: {{FONT_SIZE_2}} - Subheadings
Size 3: {{FONT_SIZE_3}} - Body text
Size 4: {{FONT_SIZE_4}} - Small text
```

**After Setup (Example):**

```markdown
Size 1: text-2xl (24px) - Large headings
Size 2: text-lg (18px) - Subheadings
Size 3: text-base (16px) - Body text
Size 4: text-sm (14px) - Small text
```

### Color Configuration

**Template (OKLCH format):**

```css
:root {
  --background: {{BACKGROUND_OKLCH}};
  --foreground: {{FOREGROUND_OKLCH}};
  --primary: {{PRIMARY_OKLCH}};
  --primary-foreground: {{PRIMARY_FOREGROUND_OKLCH}};
}
```

**After Setup:**

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.549 0.175 252.417);
  --primary-foreground: oklch(0.985 0 0);
}

@theme {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
}
```

## Agent Enforcement Rules

### Before Generating ANY UI Code

**MANDATORY CHECKLIST:**

1. [ ] Read `design-system.md` file
2. [ ] Understand font size constraints (4 only)
3. [ ] Understand font weight constraints (2 only)
4. [ ] Understand spacing constraints (divisible by 8/4)
5. [ ] Understand color distribution (60/30/10)
6. [ ] Know OKLCH color variables
7. [ ] Use only shadcn/ui components

### During Code Generation

**ENFORCE:**

- Use only configured font sizes
- Use only Semibold or Regular weights
- All spacing values divisible by 8 or 4
- 60% `bg-background`, 30% `text-foreground`, 10% `bg-primary`
- OKLCH colors from globals.css
- shadcn/ui components from `@/components/ui/`
- Proper accessibility (ARIA labels, keyboard nav)

### After Code Generation

**VALIDATE:**

```bash
# Self-validation
./scripts/validate-design-system.sh path/to/component.tsx

# Must pass all checks before completion:
# ✅ Typography constraints
# ✅ Spacing constraints
# ✅ Color distribution
# ✅ No custom CSS
# ✅ Accessibility
```

**❌ AUTOMATIC REJECTION:**

- More than 4 font sizes
- Font weights other than Semibold/Regular
- Spacing not divisible by 4 or 8
- Accent color usage > 10%
- Custom CSS instead of Tailwind
- Non-shadcn/ui components

## Example Component (Compliant)

```tsx
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function ExampleComponent() {
  return (
    <Card className="p-6 bg-background">
      {' '}
      {/* 24px padding - ✅ divisible by 8 */}
      <CardHeader className="mb-4">
        {' '}
        {/* 16px margin - ✅ divisible by 8 */}
        <CardTitle className="text-2xl font-semibold">
          {' '}
          {/* ✅ Size 1, Semibold */}
          Welcome to TaskFlow
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {' '}
        {/* 16px gap - ✅ divisible by 8 */}
        <p className="text-base font-normal text-foreground">
          {' '}
          {/* ✅ Size 3, Regular, 60% */}
          Manage your tasks efficiently with AI-powered workflows.
        </p>
        <div className="flex gap-4">
          {' '}
          {/* 16px gap - ✅ divisible by 8 */}
          <Button className="bg-primary text-primary-foreground">
            {' '}
            {/* ✅ 10% accent */}
            Get Started
          </Button>
          <Button variant="outline" className="text-foreground">
            {' '}
            {/* ✅ 30% complementary */}
            Learn More
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

**Validation:**

- ✅ Typography: 2 sizes (text-2xl, text-base), 2 weights (semibold, normal)
- ✅ Spacing: All divisible by 8 (p-6=24px, mb-4=16px, space-y-4=16px, gap-4=16px)
- ✅ Colors: 60% bg-background, 30% text-foreground, 10% bg-primary
- ✅ Components: shadcn/ui Button and Card
- ✅ No custom CSS
- ✅ Accessible: Proper semantic HTML

## Integration with Commands

### add-page.md Integration

```markdown
Phase 1: Parse Arguments
Actions:

- **FIRST**: Read design system: !{bash cat design-system.md}
- Parse page name from $ARGUMENTS

Phase 4: Page Generation

- Agent MUST validate against design system before completion
```

### add-component.md Integration

```markdown
Phase 1: Parse Arguments
Actions:

- **FIRST**: Read design system: !{bash cat design-system.md}
- Parse component name from $ARGUMENTS

Phase 4: Implementation

- Agent MUST enforce all design system constraints
- Self-validate before returning component
```

## Troubleshooting

### Violation: Too Many Font Sizes

**Error:**

```
❌ Found 6 font sizes: text-xs, text-sm, text-base, text-lg, text-xl, text-2xl
Expected: 4 font sizes only
```

**Fix:**

1. Review configured sizes in `design-system.md`
2. Consolidate to 4 sizes (typically: 2xl, lg, base, sm)
3. Update components to use only allowed sizes

### Violation: Invalid Spacing

**Error:**

```
❌ Found spacing not divisible by 8/4:
  - padding: 15px (line 42)
  - margin: 25px (line 58)
```

**Fix:**

```tsx
// ❌ Before
<div className="p-[15px] mb-[25px]">

// ✅ After
<div className="p-4 mb-6"> {/* 16px and 24px */}
```

### Violation: Color Distribution

**Error:**

```
❌ Accent color usage: 18% (exceeds 10% limit)
Found 12 instances of bg-primary
```

**Fix:**

1. Review component layout
2. Reduce accent color to CTAs and highlights only
3. Use `bg-background` and `text-foreground` for majority

## Resources

**Scripts:** `scripts/` directory:

- `setup-design-system.sh` - Interactive configuration
- `validate-design-system.sh` - Code validation
- `update-colors.sh` - Batch color updates
- `check-typography.sh` - Typography audit

**Templates:** `templates/` directory:

- `design-system-template.md` - Base template with placeholders
- `globals-css-template.css` - Color variable template
- `components-json-template.json` - shadcn/ui config

**Examples:** `examples/` directory:

- `taskflow-ai-example.md` - Complete configured example
- `e-commerce-example.md` - E-commerce design system
- `dashboard-example.md` - Admin dashboard design system

---

**Framework:** Next.js 13+ with App Router
**UI Library:** shadcn/ui (Radix UI + Tailwind CSS v4)
**Color Format:** OKLCH
**Enforcement:** Mandatory for all agents
**Version:** 1.0.0
