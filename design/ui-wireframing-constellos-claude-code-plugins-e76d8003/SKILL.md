---
name: UI Wireframing
description: This skill should be used when the user asks to "create a wireframe", "design a layout", "plan UI structure", "sketch component layout", "create WIREFRAME.md", "mobile-first wireframe", or mentions ASCII wireframes, layout planning, or UI structure before implementation. Provides mobile-first ASCII wireframe methodology for visualizing layouts before code.
version: 0.1.0
---

# UI Wireframing

Mobile-first ASCII wireframe methodology for planning UI layouts before implementation.

## Purpose

Wireframing is the first step in the UI development workflow. Create visual ASCII representations of component and page layouts in WIREFRAME.md files before writing any code. This ensures alignment on structure, hierarchy, and interaction patterns.

## When to Use

- Before implementing any new UI component or page
- When planning responsive layouts across breakpoints
- To communicate component structure and data flow
- When refactoring existing UI for better organization

## Core Principles

### Mobile-First Design

Always start with the smallest viewport (375px mobile). Design for mobile constraints first, then progressively enhance for larger screens:

1. **Mobile (375px)** - Primary design target, single column
2. **Tablet (768px)** - Two column layouts where appropriate
3. **Desktop (1024px+)** - Full multi-column layouts

### WIREFRAME.md File Location

Create WIREFRAME.md files in the component or page directory:

```
components/
└── feature-card/
    ├── WIREFRAME.md      # Wireframe documentation
    ├── feature-card.tsx  # Implementation
    └── index.ts

app/
└── dashboard/
    ├── WIREFRAME.md      # Page wireframe
    └── page.tsx
```

## Wireframe Workflow

### Step 1: Identify Components

Before drawing, list the key elements:

```markdown
## Components

- Header with logo and navigation
- Hero section with title and CTA
- Feature cards (3x grid on desktop)
- Footer with links
```

### Step 2: Create Mobile Layout (375px)

Start with the mobile viewport using ASCII art:

```markdown
## Mobile Layout (375px)

┌─────────────────────────────────────┐
│ [Logo]              [☰ Menu]        │
├─────────────────────────────────────┤
│                                     │
│         Hero Image                  │
│                                     │
│    Welcome to Our App               │
│    ─────────────────                │
│    Subtitle text here               │
│                                     │
│    [ Get Started → ]                │
│                                     │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │  Feature 1                  │    │
│  │  Description text           │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Feature 2                  │    │
│  │  Description text           │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Feature 3                  │    │
│  │  Description text           │    │
│  └─────────────────────────────┘    │
├─────────────────────────────────────┤
│  Links | Privacy | Terms            │
│  © 2025 Company                     │
└─────────────────────────────────────┘
```

### Step 3: Expand to Tablet (768px)

Show how layout adapts:

```markdown
## Tablet Layout (768px)

┌─────────────────────────────────────────────────┐
│ [Logo]                    [Nav] [Nav] [Nav]     │
├─────────────────────────────────────────────────┤
│                                                 │
│              Hero Image                         │
│                                                 │
│         Welcome to Our App                      │
│         ─────────────────                       │
│                                                 │
│            [ Get Started → ]                    │
│                                                 │
├─────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐     │
│  │  Feature 1       │  │  Feature 2       │     │
│  │  Description     │  │  Description     │     │
│  └──────────────────┘  └──────────────────┘     │
│                                                 │
│  ┌──────────────────┐                           │
│  │  Feature 3       │                           │
│  │  Description     │                           │
│  └──────────────────┘                           │
└─────────────────────────────────────────────────┘
```

### Step 4: Expand to Desktop (1024px+)

Full layout with all columns:

```markdown
## Desktop Layout (1024px+)

┌────────────────────────────────────────────────────────────────┐
│ [Logo]                              [Nav] [Nav] [Nav] [CTA]    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                       Hero Image                               │
│                                                                │
│                  Welcome to Our App                            │
│                  ─────────────────                             │
│                  Subtitle text here                            │
│                                                                │
│                    [ Get Started → ]                           │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │  Feature 1     │  │  Feature 2     │  │  Feature 3     │    │
│  │  Description   │  │  Description   │  │  Description   │    │
│  │  text here     │  │  text here     │  │  text here     │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
├────────────────────────────────────────────────────────────────┤
│  Links | Privacy | Terms                    © 2025 Company     │
└────────────────────────────────────────────────────────────────┘
```

### Step 5: Annotate Interactions

Document interactive elements and data flow:

```markdown
## Interactions

### Navigation
- Mobile: Hamburger menu opens full-screen overlay
- Tablet+: Horizontal nav bar visible

### CTA Button
- onClick: Navigate to /signup
- Hover: Scale 1.02, shadow increase

### Feature Cards
- Hover: Lift effect with shadow
- Click: Navigate to /features/{id}

## Data Requirements

- `features[]`: Array of feature objects
  - `id`: string
  - `title`: string
  - `description`: string
  - `icon`: IconName
```

## ASCII Art Reference

### Box Drawing Characters

```
Corners:  ┌ ┐ └ ┘
Lines:    │ ─
T-joints: ├ ┤ ┬ ┴ ┼
```

### Common Elements

```
Button:     [ Button Text ]  or  [ → ]
Input:      [_______________]
Checkbox:   [✓] Label  or  [ ] Label
Radio:      (●) Selected  or  ( ) Unselected
Dropdown:   [Option      ▼]
Icon:       [☰]  [✕]  [→]  [←]  [↑]  [↓]
Image:      ┌─────────┐
            │  IMG    │
            └─────────┘
```

### Spacing Indicators

```
Padding:    │ ← 16px → │
Gap:        [Card]  ← 24px →  [Card]
Margin:     ↑ 32px margin
```

## Complete WIREFRAME.md Template

```markdown
# Component/Page Name Wireframe

## Overview

Brief description of the component/page purpose.

## Components

- Component 1: Description
- Component 2: Description

## Mobile Layout (375px)

[ASCII wireframe]

## Tablet Layout (768px)

[ASCII wireframe]

## Desktop Layout (1024px+)

[ASCII wireframe]

## Interactions

### Element Name
- Event: Behavior

## Data Requirements

- `propName`: type - description

## States

### Loading
[ASCII for loading state]

### Empty
[ASCII for empty state]

### Error
[ASCII for error state]

## Accessibility Notes

- Keyboard navigation: Tab order, focus states
- Screen reader: ARIA labels, semantic HTML
- Color contrast: Minimum 4.5:1 ratio
```

## Best Practices

### Layout Guidelines

1. **Use consistent spacing** - Define a spacing scale (8px, 16px, 24px, 32px)
2. **Align elements** - Use a grid system in the ASCII
3. **Show hierarchy** - Larger text for headings, visual weight for CTAs
4. **Consider touch targets** - Minimum 44x44px for mobile buttons

### Documentation Guidelines

1. **Keep wireframes updated** - Modify when requirements change
2. **Include all states** - Loading, empty, error, success
3. **Document interactions** - What happens on click, hover, focus
4. **Specify data needs** - Props, API responses, state

### Review Checklist

Before proceeding to implementation:

- [ ] Mobile layout complete and usable
- [ ] Tablet and desktop layouts defined
- [ ] All interactive elements documented
- [ ] Data requirements specified
- [ ] Accessibility considerations noted
- [ ] All UI states represented

## Next Steps

After wireframe approval, proceed to the **ui-design** skill for implementing the static UI with compound components and TypeScript interfaces.
