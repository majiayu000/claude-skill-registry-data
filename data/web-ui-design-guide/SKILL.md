---
name: web-ui-design-guide
description: Apply modern, professional web UI design principles when building any web UI component. Only execute this when the current project is a web project and involves UI-related work. Use this skill for UI tasks involving buttons, forms, cards, layouts, navigation, or any visual web component. Ensures clean minimal design, neutral color palettes with single accent color, 8px grid spacing, clear typography hierarchy, and subtle visual effects. Prevents common anti-patterns like rainbow gradients, tiny text, and inconsistent spacing.
---

# Web UI Design Guide

## Overview

Ensure every web UI component built looks modern and professional by applying systematic design principles. This skill provides comprehensive guidelines for color, spacing, typography, and component-specific patterns to achieve clean, minimal, and consistent user interfaces.

## When to Use This Skill

Activate this skill when:
- Building any web UI component (buttons, forms, cards, navigation, modals, etc.)
- Creating layouts or page designs
- Implementing design systems or component libraries
- Working with UI frameworks (React, Vue, Next.js, shadcn/ui, etc.)
- Receiving requests like:
  - "Create a login form"
  - "Design a dashboard card"
  - "Build a navigation header"
  - "Make this UI look modern"
  - "Style this component"

**Do NOT activate** for:
- Backend API development
- Database queries
- Server configuration
- Non-visual code tasks

## Core Design Philosophy

Follow these fundamental principles for all UI work:

1. **Clean and Minimal** - Prioritize whitespace, reduce visual clutter
2. **Neutral Color Palette** - Gray/off-white base (80-90%) + ONE accent color (5-10%)
3. **8px Grid System** - All spacing uses multiples of 8: 8, 16, 24, 32, 48, 64px
4. **Typography Hierarchy** - Minimum 16px body text, maximum 2 font families
5. **Subtle Effects** - Understated shadows, selective rounded corners
6. **Mobile-First** - Design for small screens first, expand to larger

## How to Use This Skill

### Step 1: Load Relevant Reference

Before implementing any UI component, load the appropriate reference file:

```
Read references/design-principles.md - Core philosophy and principles
Read references/color-palette.md - Color system and accent usage
Read references/spacing-system.md - 8px grid spacing scale
Read references/typography.md - Font sizes, weights, line heights
Read references/component-patterns.md - Component-specific best practices
Read references/anti-patterns.md - Common mistakes to avoid
```

**Recommendation**: Start with `design-principles.md` for overall philosophy, then load component-specific files as needed.

### Step 2: Apply Component-Specific Patterns

For each component type, reference the corresponding section in `component-patterns.md`:

- **Button**: `component-patterns.md` → Button section
- **Card**: `component-patterns.md` → Card section
- **Form**: `component-patterns.md` → Form section
- **Navigation**: `component-patterns.md` → Navigation section
- **Modal**: `component-patterns.md` → Modal section
- **Table**: `component-patterns.md` → Table section
- **Badge/Tag**: `component-patterns.md` → Badge section
- **Dropdown**: `component-patterns.md` → Dropdown section

### Step 3: Validate Against Anti-Patterns

Before finalizing implementation, check `anti-patterns.md` to ensure the design avoids:

- ❌ Rainbow gradients or generic purple/blue gradients
- ❌ Text smaller than 16px for body content
- ❌ Inconsistent spacing (non-8px multiples)
- ❌ More than 2 font families
- ❌ Border + shadow on the same element
- ❌ Unclear interactive states (hover, focus, active)

### Step 4: Ensure System Consistency

Apply the **8px grid system** for all spacing:
- Use only: 4px (rare), 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Reference `spacing-system.md` for component-specific spacing guidelines

Use **neutral color palette** as foundation:
- Base: #FFFFFF, #FAFAFA, #F5F5F5
- Grays: #E0E0E0, #CCCCCC, #999999, #666666, #333333, #1A1A1A
- ONE accent color for actions and emphasis
- Reference `color-palette.md` for detailed color usage

Maintain **typography hierarchy**:
- Body text: minimum 16px, line-height 1.6
- Maximum 2 font families
- Clear heading scales (32px H1, 24px H2, 20px H3)
- Reference `typography.md` for complete type scale

## Resources

### references/

Documentation loaded into context as needed to inform design decisions:

- **design-principles.md** - Core philosophy: clean minimal design, neutral palette, 8px grid, typography hierarchy, subtle effects, mobile-first
- **color-palette.md** - Neutral base colors, single accent color usage, semantic colors, examples and anti-patterns
- **spacing-system.md** - 8px grid scale, component spacing guidelines, responsive spacing
- **typography.md** - Font selection, type scale, weights, line lengths, component typography
- **component-patterns.md** - Design patterns for buttons, cards, forms, navigation, modals, tables, badges, dropdowns
- **anti-patterns.md** - Common design mistakes to avoid with alternatives

## Quick Decision Tree

```
UI Component Request
│
├─ What component? → Load component-patterns.md section
│
├─ What spacing? → Use 8px grid (spacing-system.md)
│
├─ What colors? → Neutral base + accent (color-palette.md)
│
├─ What typography? → 16px+ body, clear hierarchy (typography.md)
│
└─ Validation → Check anti-patterns.md
```

## Examples

**Good Request Flow**:
```
User: "Create a login form"
→ Read references/component-patterns.md (Form section)
→ Read references/spacing-system.md (Form spacing)
→ Apply: 16px input text, 8px label gap, 24px button spacing
→ Validate against anti-patterns.md
→ Implement with neutral colors + accent for primary button
```

**Component Implementation Checklist**:
- ✅ Spacing uses 8px multiples
- ✅ Text minimum 16px for body
- ✅ Neutral colors (80-90%) + accent color (5-10%)
- ✅ Clear hover/focus/active states
- ✅ No rainbow gradients or generic purple/blue
- ✅ Maximum 2 font families
- ✅ Mobile-first responsive design
