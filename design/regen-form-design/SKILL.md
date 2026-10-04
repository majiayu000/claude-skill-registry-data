---
name: regen-form-design
description: Use when building, fixing, or auditing any form on the ReGen Civics site. Triggers on form readability issues, new form creation, contrast problems on dark backgrounds, input styling, label visibility, placeholder text, radio buttons, checkboxes, select dropdowns, file uploads, multi-step forms, or any UI where users enter data. Also use when the form looks bad, text is hard to read, or accessibility is a concern.
---

# ReGen Civics Form Design Standards

## Overview

Every form on regencivics.earth must be readable, beautiful, and accessible on both light and dark backgrounds. The site uses a dark forest theme (`.dark` class) where cards render on dark green backgrounds. Forms that use hardcoded light-mode colors (gray-600, amber-900, etc.) become unreadable in dark mode. This skill defines the standard for all form work.

## The Core Problem

The site's CSS theme variables change based on `.dark` class:

| Variable | Light Mode | Dark Mode |
|----------|-----------|-----------|
| `--card` | white | dark green (oklch 0.18) |
| `--card-foreground` | dark green | near-white (oklch 0.95) |
| `--background` | cream | very dark green (oklch 0.12) |
| `--input` | light gray | dark green (oklch 0.22) |
| `--muted-foreground` | medium gray | medium light (oklch 0.70) |

Forms that hardcode `text-gray-700` or `bg-amber-50` break in dark mode. Use theme-aware classes instead.

## Quick Reference: Theme-Aware Form Classes

### Text Colors (use these, never hardcode grays/ambers)

| Purpose | Class | Why |
|---------|-------|-----|
| Primary text (labels, headings) | `text-foreground` | Maps to --foreground, works both modes |
| Secondary text (descriptions, hints) | `text-muted-foreground` | Maps to --muted-foreground |
| Error text | `text-destructive` | Maps to --destructive |
| Link text | `text-primary hover:text-primary/80` | Maps to --primary (green) |

### Input Fields

Standard input override for dark-compatible forms:

```tsx
// For forms on dark/themed backgrounds (glass panels, cards in dark mode)
const themedInput = "bg-input/30 text-foreground placeholder:text-muted-foreground/70 border-input focus-visible:border-ring focus-visible:ring-ring/50";

// For forms on explicit light backgrounds (rare - only when you force bg-white)
const lightInput = "bg-white text-[#1a472a] placeholder:text-[#1a472a]/50 border-input";
```

### Containers and Panels

| Purpose | Class | Contrast Ratio |
|---------|-------|---------------|
| Info box (light mode) | `bg-primary/10 border-primary/20 text-foreground` | 7:1+ |
| Info box (dark mode safe) | `bg-muted border-border text-foreground` | 7:1+ |
| Warning box | `bg-destructive/10 border-destructive/20 text-foreground` | 7:1+ |
| Success box | `bg-primary/10 border-primary/20 text-foreground` | 7:1+ |
| Glass panel (dark bg) | `bg-white/10 border-white/20 backdrop-blur-sm` | varies |

### Labels

```tsx
// Standard label - inherits from theme
<Label className="text-foreground font-medium">Field Name</Label>

// Description below label
<p className="text-sm text-muted-foreground">Helper text here</p>
```

### Radio Groups and Checkboxes

```tsx
// Radio label text must be readable
<Label htmlFor="option-id" className="font-normal text-foreground">
  Option text here
</Label>

// Question text above radio group
<p className="font-medium text-foreground">
  Your question here?
</p>
```

### Buttons

| Type | Class |
|------|-------|
| Primary action | `bg-primary text-primary-foreground hover:bg-primary/90` |
| Secondary/back | `variant="outline"` (uses theme border + text) |
| Destructive | `bg-destructive text-destructive-foreground` |
| Amber accent (legacy) | `bg-amber-600 hover:bg-amber-700 text-white` |

## Form Layout Standards

### Spacing

- Between form sections: `space-y-8`
- Between fields within a section: `space-y-4` or `space-y-6`
- Between label and input: `space-y-2`
- Between label and description: `space-y-1`
- Section padding: `p-4` or `p-6`

### Cards (multi-step forms)

```tsx
<Card className="border-primary/30">
  <CardHeader>
    <CardTitle className="text-2xl text-foreground">Step Title</CardTitle>
    <CardDescription className="text-muted-foreground">
      Description text
    </CardDescription>
  </CardHeader>
  <CardContent className="space-y-6">
    {/* form fields */}
  </CardContent>
</Card>
```

### Step Indicators

```tsx
// Active step
"bg-primary text-primary-foreground"
// Completed step
"bg-primary/80 text-primary-foreground"
// Future step
"bg-muted text-muted-foreground"
// Step label
"text-xs text-muted-foreground mt-2"
```

### Navigation Footer

```tsx
<div className="flex gap-3 pt-6 border-t border-border">
  <Button variant="outline">
    <ArrowLeft className="w-4 h-4 mr-2" />
    Back
  </Button>
  <Button className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90">
    Continue
    <ArrowRight className="w-4 h-4 ml-2" />
  </Button>
</div>
```

## Tables Inside Forms

```tsx
<table className="w-full text-sm">
  <thead>
    <tr className="border-b border-border">
      <th className="text-left py-2 font-medium text-foreground">Column</th>
    </tr>
  </thead>
  <tbody>
    <tr className="border-b border-border/50">
      <td className="py-3 text-muted-foreground">Secondary data</td>
      <td className="py-3 text-foreground">Primary data</td>
      <td className="py-3">
        <a className="text-primary hover:text-primary/80 underline">Link</a>
      </td>
    </tr>
  </tbody>
</table>
```

## WCAG Contrast Minimums

All form elements must meet these ratios:

| Element | Minimum Ratio | Standard |
|---------|--------------|----------|
| Normal text (labels, descriptions) | 4.5:1 | WCAG AA |
| Large text (18px+ or 14px+ bold) | 3:1 | WCAG AA |
| UI components (borders, icons) | 3:1 | WCAG AA |
| Placeholder text | 4.5:1 | WCAG AA |
| Disabled elements | No minimum | Exempt |

### How to Check

Use the theme variables. If `--foreground` on `--card` passes (it does, by design), then `text-foreground` on `bg-card` is always safe. The danger is hardcoded colors that bypass the theme.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `text-gray-700` on dark card | Use `text-foreground` or `text-muted-foreground` |
| `bg-amber-50` info box in dark mode | Use `bg-muted` or `bg-primary/10` |
| `placeholder:text-white/30` (30% opacity) | Use `placeholder:text-muted-foreground/70` (minimum) |
| `text-amber-900` on dark background | Use `text-foreground` with theme |
| `border-gray-200` invisible in dark mode | Use `border-border` |
| `bg-blue-50 text-blue-900` info box | Use `bg-muted text-foreground` |
| `bg-white rounded-lg` summary panel | Use `bg-muted rounded-lg` |
| Forcing `from-amber-50 to-white` page bg | Remove; let theme `--background` work |

## Existing Glass Panel Pattern (dark backgrounds)

From ProfileEditForm, the established pattern for forms on explicit dark/glass backgrounds:

```tsx
const glassInput = "text-white placeholder:text-white/50 bg-white/10 border-white/20 focus-visible:border-[#7dd87d]/50";
```

Use this only when the form sits on an explicit dark panel (not a themed card). For themed cards, use the theme-aware classes above.

## Checklist Before Shipping Any Form

1. Does every text element use theme-aware color classes?
2. Do info/warning boxes use `bg-muted` or `bg-primary/10` instead of hardcoded colors?
3. Are placeholder colors at least `text-muted-foreground/70`?
4. Do table headers and cells use `text-foreground` / `text-muted-foreground`?
5. Do borders use `border-border` instead of hardcoded gray/amber?
6. Is the page background using theme `--background` (not forced light)?
7. Do radio/checkbox labels use `text-foreground`?
8. Are step indicators using theme primary/muted colors?
9. Does the form look good in BOTH light and dark mode?
10. Are all interactive elements (links, buttons) using theme primary color?
