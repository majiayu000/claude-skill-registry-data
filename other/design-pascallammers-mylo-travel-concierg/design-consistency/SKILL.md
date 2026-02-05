---
name: Design Consistency
description: Analyze design system usage, identify inconsistencies across patterns, generate fixes, and maintain visual coherence with automated style guide generation
---

# Design Consistency Skill

This skill ensures all 24 AI design patterns maintain visual and interaction consistency across your application by analyzing design system usage, identifying deviations, and applying fixes automatically.

## When to Use This Skill

Claude will automatically invoke this skill when:
- You ask to "check design consistency"
- You request "analyze design system"
- You want to "fix design issues"
- You say "generate style guide"
- You mention "design audit"

## What Gets Analyzed

Your design system uses **Tailwind CSS v4** with custom utilities. This skill checks:

```
Design System Analysis
├── Colors
│   ├── Primary blues, secondary grays
│   ├── Accent colors for CTAs
│   ├── Semantic colors (success, error, warning)
│   └── Dark mode palette
├── Typography
│   ├── Font sizes (xs, sm, base, lg, xl, 2xl, 3xl)
│   ├── Font weights (regular, medium, semibold, bold)
│   ├── Line heights for readability
│   └── Letter spacing
├── Spacing
│   ├── Padding consistency (2, 4, 6, 8, 12, 16, 24, 32)
│   ├── Margin consistency
│   ├── Gap between elements
│   └── Component margins
├── Components
│   ├── Button variants (primary, secondary, outline, ghost)
│   ├── Card patterns and shadows
│   ├── Badge styles
│   ├── Input field consistency
│   └── Navigation patterns
├── Effects
│   ├── Box shadows (sm, md, lg)
│   ├── Border radius (sm, md, lg)
│   ├── Transitions and animations
│   ├── Hover states
│   └── Disabled states
├── Animations
│   ├── Framer motion durations
│   ├── Easing functions
│   ├── Transform values
│   └── Stagger patterns
└── Dark Mode
    ├── Contrast ratios
    ├── Color adjustments
    ├── Text readability
    └── Semantic color mapping
```

## Design Analysis Workflow

### Step 1: Run Design Analysis

```bash
npm run design-analyze
```

Output shows:
- Consistency score per component
- Issues found (with severity)
- Files requiring fixes
- Recommendations

### Step 2: Review Design Report

```bash
npm run design-report
```

Generates comprehensive report:

```
📋 Design Consistency Report
├── Overall Score: 78/100
├── Critical Issues: 3
├── Warnings: 12
├── Minor Issues: 8
└── Recommendations: 15

Files Requiring Fixes
├── src/components/examples/PredictiveAnticipationExample.tsx
│   └── ⚠️ Wrong spacing (p-3 should be p-4)
│   └── ⚠️ Wrong color (text-gray-500 should be text-gray-600)
├── src/components/examples/AmbientIntelligenceExample.tsx
│   └── 🔴 Shadow inconsistency
│   └── ⚠️ Animation duration mismatch
└── ... more files
```

### Step 3: Review Style Guide

```bash
npm run design-style-guide
```

Generates documentation of your design system:

```markdown
# Style Guide

## Colors

### Primary Palette
- Primary: bg-blue-600 (used for main CTAs)
- Primary Dark: bg-blue-700 (hover state)
- Primary Light: bg-blue-50 (backgrounds)

### Secondary Palette
- Secondary: bg-gray-600 (secondary actions)
- Secondary Dark: bg-gray-700 (hover)

### Semantic Colors
- Success: bg-green-500 (positive feedback)
- Error: bg-red-500 (errors)
- Warning: bg-yellow-500 (warnings)
- Info: bg-blue-500 (information)

### Dark Mode
- Background: dark:bg-gray-900
- Surface: dark:bg-gray-800
- Text: dark:text-gray-100

## Typography

### Font Sizes
- xs: 12px (labels, small text)
- sm: 14px (body text)
- base: 16px (default text)
- lg: 18px (section titles)
- xl: 20px (headings)

### Font Weights
- Regular: font-normal (400)
- Medium: font-medium (500)
- Semibold: font-semibold (600)
- Bold: font-bold (700)

## Spacing
... and more
```

## Common Design Issues & Fixes

### Issue 1: Inconsistent Padding

❌ **Inconsistent:**
```typescript
<Card className="p-2">  {/* Some cards */}
<Card className="p-4">  {/* Other cards */}
<Card className="p-6">  {/* Yet more */}
```

✅ **Consistent:**
```typescript
<Card className="p-6">  {/* All cards use p-6 */}
```

**Fix Command:**
```bash
npm run design-fix  # Fix one issue at a time
# or
npm run design-fix-all  # Fix all at once
```

### Issue 2: Color Palette Deviation

❌ **Inconsistent:**
```typescript
<button className="bg-blue-400">  {/* Random blue */}
<button className="bg-blue-600">  {/* Primary blue */}
<button className="bg-blue-800">  {/* Dark blue */}
```

✅ **Consistent:**
```typescript
<button className="bg-blue-600">  {/* Primary */}
<button className="bg-blue-600 hover:bg-blue-700">  {/* Primary + hover */}
```

**Tailwind Color System Used:**
- `blue-600` → Primary color
- `blue-700` → Primary hover
- `blue-50` → Primary light background
- `gray-600` → Secondary color
- `gray-700` → Secondary hover

### Issue 3: Typography Inconsistency

❌ **Inconsistent:**
```typescript
<h1 className="text-lg font-semibold">  {/* Should be xl + bold */}
<h1 className="text-2xl font-normal">  {/* Wrong weight */}
<p className="text-base font-bold">    {/* Wrong weight */}
```

✅ **Consistent:**
```typescript
<h1 className="text-2xl font-bold">        {/* Page title */}
<h2 className="text-xl font-semibold">    {/* Section title */}
<p className="text-base font-normal">     {/* Body text */}
<span className="text-sm font-medium">   {/* Labels */}
```

### Issue 4: Spacing Inconsistency

❌ **Inconsistent:**
```typescript
<div className="space-y-2">     {/* Tight */}
<div className="space-y-8">     {/* Loose */}
<div className="gap-3">         {/* Random */}
```

✅ **Consistent:**
```typescript
<div className="space-y-6">     {/* Standard section spacing */}
<div className="flex gap-4">    {/* Component spacing */}
<div className="px-6 py-4">     {/* Card padding */}
```

### Issue 5: Component State Inconsistency

❌ **Inconsistent:**
```typescript
{/* Disabled state - different for each component */}
<button disabled className="opacity-50">
<button disabled className="bg-gray-400">
<button disabled className="cursor-not-allowed">
```

✅ **Consistent:**
```typescript
{/* All disabled buttons use same pattern */}
<button disabled className="opacity-50 cursor-not-allowed">
```

### Issue 6: Dark Mode Issues

❌ **Incomplete:**
```typescript
<div className="bg-white text-black">
  {/* No dark mode support */}
</div>
```

✅ **Complete:**
```typescript
<div className="bg-white dark:bg-gray-900 text-black dark:text-white">
  {/* Full dark mode support */}
</div>
```

## Manual Fixes Using Design Agent

### Fix Single Issue

```bash
npm run design-fix
```

Prompts you to:
1. Select file to fix
2. Review issue description
3. Apply fix automatically
4. Verify in browser

### Fix All Issues

```bash
npm run design-fix-all
```

Automatically:
1. Analyzes all components
2. Identifies all design issues
3. Applies fixes across codebase
4. Updates style guide
5. Reports improvements

## Design System Documentation

### Color Variables
```typescript
// Tailwind config provides these utilities
Primary:     bg-blue-600, text-blue-600
Primary Alt: bg-blue-700, hover:bg-blue-700
Primary BG:  bg-blue-50, dark:bg-blue-900
Secondary:   bg-gray-600, text-gray-600
Success:     bg-green-500, text-green-500
Error:       bg-red-500, text-red-500
Warning:     bg-yellow-500, text-yellow-500
```

### Component Sizing
```typescript
// Consistent sizing system
sm:  max-w-sm (24rem)   {/* Modals, cards */}
md:  max-w-md (28rem)   {/* Medium containers */}
lg:  max-w-lg (32rem)   {/* Large sections */}
xl:  max-w-xl (36rem)   {/* Full-width content */}
2xl: max-w-2xl (42rem)  {/* Wide content */}
```

### Border Radius
```typescript
// Consistent roundness
rounded-sm:  2px    {/* Subtle curves */}
rounded:     4px    {/* Default buttons */}
rounded-md:  6px    {/* Cards, inputs */}
rounded-lg:  8px    {/* Large components */}
rounded-full: 9999px {/* Circles, pills */}
```

### Shadows
```typescript
// Elevation hierarchy
shadow-sm:  0 1px 2px   {/* Subtle */}
shadow:     0 1px 3px   {/* Default */}
shadow-md:  0 4px 6px   {/* Medium lift */}
shadow-lg:  0 10px 15px {/* High lift */}
```

## Integration with Pattern Development

When working on patterns (using Pattern Development skill):
- **Initial Pattern Review**: Check existing pattern components against design system
- **Demo Component Creation**: Use design system consistently in demo
- **Visual Verification**: Compare pattern UI against style guide
- **Before Completion**: Run design analysis to ensure consistency

## Automated Quality Gates

Design consistency checks run:
- ✅ Before commits (pre-commit hook)
- ✅ During tests (`npm test`)
- ✅ During build (`npm run build`)
- ✅ Before deployment to Vercel

## Commands Reference

```bash
# Analyze design system usage
npm run design-analyze

# Generate design consistency report
npm run design-report

# Generate/update style guide
npm run design-style-guide

# Fix single design issue (interactive)
npm run design-fix

# Fix all design issues automatically
npm run design-fix-all

# View current style guide
cat docs/style-guide.md
```

## Design System File Locations

```
Design System Files
├── Tailwind Config: tailwind.config.mjs
├── Global Styles: src/app/globals.css
├── Design Tokens: (in Tailwind config)
├── Component Examples:
│   ├── src/components/ui/Button.tsx
│   ├── src/components/ui/Card.tsx
│   ├── src/components/ui/Badge.tsx
│   └── ... more
├── Generated Style Guide: docs/style-guide.md
└── Reports: design-consistency-report.json
```

## Consistency Metrics

Track improvement:

| Metric | Baseline | Target | Current |
|--------|----------|--------|---------|
| Color Consistency | 65% | 95% | - |
| Typography Consistency | 70% | 95% | - |
| Spacing Consistency | 60% | 95% | - |
| Dark Mode Coverage | 50% | 100% | - |
| Component States | 75% | 100% | - |

---

**Goal**: Maintain visual and interaction consistency across all 24 AI design patterns, ensuring a cohesive, professional user experience with systematic design system adherence.
