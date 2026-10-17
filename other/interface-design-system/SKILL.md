---
name: interface-design-system
description: Design engineering skill for Claude Code that enforces consistent UI patterns through memory, craft principles, and systematic design tokens.
triggers:
  - "set up interface design system"
  - "create consistent UI components"
  - "establish design system patterns"
  - "audit interface consistency"
  - "load design system memory"
  - "build dashboard with design principles"
  - "extract design patterns from code"
  - "initialize interface design craft"
---

# Interface Design System

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill enables you to build interfaces with systematic consistency using the Interface Design framework. It provides principle-based craft, cross-session memory through `system.md`, and enforcement of design patterns for dashboards, admin panels, and application UIs.

## What This Does

Interface Design prevents design drift across sessions by:

1. **Craft** — Applying professional design principles (spacing grids, depth strategies, surface elevation)
2. **Memory** — Persisting decisions in `.interface-design/system.md` that auto-load each session
3. **Consistency** — Ensuring every component follows the same patterns

**Key difference:** Without this system, button heights drift (36px, 38px, 40px...). With it, decisions are made once and applied consistently.

## Installation

### Plugin Method (Recommended)

```bash
# Add the marketplace
/plugin marketplace add Dammyjay93/interface-design

# Install via plugin menu
/plugin menu
# Select 'interface-design' from the menu
```

Restart Claude Code after installation.

### Manual Method

```bash
git clone https://github.com/Dammyjay93/interface-design.git
cd interface-design
cp -r .claude/* ~/.claude/
cp -r .claude-plugin/* ~/.claude-plugin/
```

Restart Claude Code.

## Core Workflow

### First Session (No system.md)

When building UI for the first time:

```
1. Assess project context (data-heavy dashboard vs. consumer app)
2. Suggest design direction
3. Ask for confirmation
4. State design choices before building each component
5. Build with consistent principles
6. Offer to save system.md
```

**Example:**

```
User: "Build a user dashboard with metrics cards"

Agent Response:
---
This feels like a data-heavy dashboard — I'd suggest:
- Depth: Borders-only (clean, technical)
- Surfaces: Subtle elevation shifts (7% → 9% → 11%)
- Spacing: 8px base grid
- Foundation: Cool tones (slate)

Does this direction fit? (y/n)

[User: y]

Design Tokens:
- Depth: borders-only
- Surfaces: 7% → 9% → 11% lightness scale
- Borders: rgba(255,255,255,0.06)
- Spacing: 8px base (8, 16, 24, 32)
- Radius: 6px/8px

Building dashboard...
---

[Builds components consistently]

Want me to save these patterns to .interface-design/system.md? (y/n)
```

### Subsequent Sessions (system.md exists)

```
User: "Add a settings page"

Agent Response:
---
✓ Loaded .interface-design/system.md

Active System:
- Depth: borders-only
- Surfaces: 7% → 9% → 11% scale
- Spacing: 8px base grid
- Borders: rgba(255,255,255,0.06)

Building settings page with established patterns...
---
```

## System File Structure

After establishing direction, patterns are saved to `.interface-design/system.md`:

```markdown
# Design System

## Direction
Personality: Precision & Density
Foundation: Cool (slate)
Depth: Borders-only

## Tokens

### Spacing
Base: 4px
Scale: 4, 8, 12, 16, 24, 32, 48

### Colors
--background: hsl(222, 47%, 7%)
--foreground: hsl(210, 20%, 98%)
--secondary: hsl(215, 16%, 65%)
--accent: hsl(217, 91%, 60%)
--border: rgba(255,255,255,0.06)

### Surfaces
Card: +2% lightness (9%)
Panel: +4% lightness (11%)
Elevated: +6% lightness (13%)

### Typography
Base: 14px
Scale: 12, 14, 16, 20, 24

### Depth
Strategy: Borders-only
Border: 0.5px solid var(--border)

## Patterns

### Button Primary
- Height: 36px
- Padding: 12px 16px
- Radius: 6px
- Font: 14px medium
- Usage: Primary actions only

### Card Default
- Border: 0.5px solid var(--border)
- Padding: 16px
- Radius: 8px
- Background: var(--card)

### Input Text
- Height: 36px
- Padding: 8px 12px
- Radius: 6px
- Border: 0.5px solid var(--border)
```

This file auto-loads at session start.

## Commands

### Initialize Design System

```bash
/interface-design:init
```

Starts the design process with principle assessment and direction selection.

### Check Current System

```bash
/interface-design:status
```

Displays active design tokens, patterns, and system file location.

### Audit Code Consistency

```bash
/interface-design:audit src/components
```

Checks existing code against system.md for inconsistencies:

```
Audit Results:
✓ Button.tsx - matches pattern
✗ Card.tsx - padding 18px (expected 16px)
✗ Input.tsx - height 40px (expected 36px)
```

### Extract Patterns from Code

```bash
/interface-design:extract
```

Scans existing codebase to generate system.md from patterns:

```
Detected Patterns:
- Spacing: 8px base (found: 8, 16, 24, 32)
- Button height: 36px (5 instances)
- Card padding: 16px (3 instances)
- Radius: 6px/8px

Generate system.md from these patterns? (y/n)
```

## Design Directions

The system infers direction from context, but you can specify:

### Precision & Density
```markdown
Personality: Technical, tight spacing
Foundation: Cool (slate)
Depth: Borders-only
Use: Developer tools, admin dashboards
```

### Warmth & Approachability
```markdown
Personality: Generous spacing, soft shadows
Foundation: Warm (amber/orange)
Depth: Layered shadows
Use: Collaborative tools, consumer apps
```

### Sophistication & Trust
```markdown
Personality: Cool tones, refined depth
Foundation: Blue-gray
Depth: Subtle shadows + borders
Use: Finance, enterprise B2B
```

### Boldness & Clarity
```markdown
Personality: High contrast, dramatic space
Foundation: Pure grayscale
Depth: Strong shadows
Use: Modern dashboards, data-heavy
```

### Utility & Function
```markdown
Personality: GitHub-style utility
Foundation: Muted grays
Depth: Minimal borders
Use: Developer tools, technical UIs
```

## Code Examples

### React Component with System

**Button.tsx** (following Precision & Density system):

```tsx
// Design checkpoint:
// - Height: 36px (from system)
// - Padding: 12px 16px (from system)
// - Radius: 6px (from system)
// - Spacing: 8px base grid

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', children }: ButtonProps) {
  return (
    <button
      className={`
        h-9 px-4
        rounded-md
        text-sm font-medium
        transition-colors
        ${variant === 'primary' 
          ? 'bg-accent text-white hover:bg-accent/90' 
          : 'border border-border bg-card hover:bg-card/80'
        }
      `}
    >
      {children}
    </button>
  );
}

// Tailwind config should use system tokens:
// theme: {
//   extend: {
//     spacing: {
//       '4': '16px', // 8px base * 2
//     },
//     borderRadius: {
//       'md': '6px',
//     }
//   }
// }
```

### Card Component

**Card.tsx**:

```tsx
// Design checkpoint:
// - Border: 0.5px solid var(--border)
// - Padding: 16px (2 * 8px base)
// - Radius: 8px
// - Surface: +2% lightness elevation

interface CardProps {
  children: React.ReactNode;
  elevated?: boolean;
}

export function Card({ children, elevated = false }: CardProps) {
  return (
    <div
      className={`
        border border-border
        rounded-lg
        p-4
        ${elevated ? 'bg-elevated' : 'bg-card'}
      `}
    >
      {children}
    </div>
  );
}
```

### CSS Variables Setup

**globals.css**:

```css
/* Design system tokens from .interface-design/system.md */

:root {
  /* Spacing base: 8px */
  --spacing-1: 0.25rem; /* 4px */
  --spacing-2: 0.5rem;  /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem;    /* 16px */
  --spacing-6: 1.5rem;  /* 24px */
  --spacing-8: 2rem;    /* 32px */

  /* Colors - Cool foundation */
  --background: hsl(222, 47%, 7%);
  --foreground: hsl(210, 20%, 98%);
  --secondary: hsl(215, 16%, 65%);
  --accent: hsl(217, 91%, 60%);
  
  /* Surfaces - Elevation scale */
  --card: hsl(222, 47%, 9%);      /* +2% */
  --panel: hsl(222, 47%, 11%);    /* +4% */
  --elevated: hsl(222, 47%, 13%); /* +6% */
  
  /* Borders */
  --border: rgba(255, 255, 255, 0.06);
  
  /* Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

### Dashboard Example

**Dashboard.tsx** (full implementation):

```tsx
import { Card } from './Card';
import { Button } from './Button';

// Design checkpoint:
// - Grid: 24px gap (3 * 8px base)
// - Cards: 16px padding (system pattern)
// - Metrics: 32px vertical spacing (4 * 8px)

export function Dashboard() {
  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <header className="mb-8">
        <h1 className="text-2xl font-semibold text-foreground">
          Dashboard
        </h1>
        <p className="text-sm text-secondary mt-2">
          Overview of your metrics
        </p>
      </header>

      {/* Metrics Grid - 24px gap */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        <Card>
          <div className="space-y-2">
            <p className="text-sm text-secondary">Total Users</p>
            <p className="text-2xl font-semibold text-foreground">
              12,549
            </p>
            <p className="text-xs text-accent">+12% from last month</p>
          </div>
        </Card>

        <Card>
          <div className="space-y-2">
            <p className="text-sm text-secondary">Revenue</p>
            <p className="text-2xl font-semibold text-foreground">
              $45,231
            </p>
            <p className="text-xs text-accent">+8% from last month</p>
          </div>
        </Card>

        <Card>
          <div className="space-y-2">
            <p className="text-sm text-secondary">Active Sessions</p>
            <p className="text-2xl font-semibold text-foreground">
              573
            </p>
            <p className="text-xs text-secondary">Currently online</p>
          </div>
        </Card>
      </div>

      {/* Data Table */}
      <Card elevated>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">
            Recent Activity
          </h2>
          <Button variant="secondary">View All</Button>
        </div>
        
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left py-3 text-sm text-secondary font-medium">
                User
              </th>
              <th className="text-left py-3 text-sm text-secondary font-medium">
                Action
              </th>
              <th className="text-left py-3 text-sm text-secondary font-medium">
                Time
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-border">
              <td className="py-3 text-sm text-foreground">john@example.com</td>
              <td className="py-3 text-sm text-secondary">Logged in</td>
              <td className="py-3 text-sm text-secondary">2 min ago</td>
            </tr>
          </tbody>
        </table>
      </Card>
    </div>
  );
}
```

## Common Patterns

### Before Building a Component

Always state design choices:

```
Design checkpoint for FormInput:
- Height: 36px (system standard)
- Padding: 8px 12px (vertical/horizontal from 8px grid)
- Border: 0.5px solid var(--border) (system depth)
- Radius: 6px (system sm radius)
- Focus: 1px accent outline (interactive state)
```

### After Building Components

Offer to persist new patterns:

```
Built 3 new components following system principles.

New patterns detected:
- FormInput: 36px height, 8px/12px padding
- Select: 36px height, matches FormInput
- Checkbox: 16px size (2 * 8px base)

Save these patterns to system.md? (y/n)
```

### Spacing Grid Adherence

Always use multiples of base grid:

```tsx
// ✓ Correct (8px base grid)
<div className="space-y-4">  {/* 16px = 8 * 2 */}
  <div className="p-6">       {/* 24px = 8 * 3 */}
    <div className="mb-8">    {/* 32px = 8 * 4 */}

// ✗ Incorrect (off-grid values)
<div className="space-y-5">  {/* 20px - not on 8px grid */}
  <div className="p-7">       {/* 28px - not on 8px grid */}
```

### Surface Elevation

Use consistent lightness shifts:

```css
/* Base background: 7% lightness */
--background: hsl(222, 47%, 7%);

/* +2% elevation (cards) */
--card: hsl(222, 47%, 9%);

/* +4% elevation (panels) */
--panel: hsl(222, 47%, 11%);

/* +6% elevation (modals) */
--elevated: hsl(222, 47%, 13%);
```

### Depth Strategy

**Borders-only** (technical/minimal):
```css
border: 0.5px solid var(--border);
box-shadow: none;
```

**Layered shadows** (consumer/warm):
```css
box-shadow: 
  0 1px 2px rgba(0, 0, 0, 0.05),
  0 4px 8px rgba(0, 0, 0, 0.08);
```

**Subtle shadows + borders** (enterprise):
```css
border: 0.5px solid var(--border);
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
```

## Configuration

### Custom Direction

Edit `.interface-design/system.md` to customize:

```markdown
## Direction
Personality: Custom Technical
Foundation: Purple (for brand alignment)
Depth: Borders + subtle glow

## Tokens
### Colors
--accent: hsl(270, 70%, 60%)  # Brand purple
--glow: 0 0 8px rgba(138, 43, 226, 0.2)
```

### Multi-Theme Support

Create theme variants:

```markdown
## Themes

### Light
--background: hsl(0, 0%, 98%)
--foreground: hsl(222, 47%, 11%)
--border: rgba(0, 0, 0, 0.08)

### Dark
--background: hsl(222, 47%, 7%)
--foreground: hsl(210, 20%, 98%)
--border: rgba(255, 255, 255, 0.06)
```

## Troubleshooting

### System Not Loading

**Problem:** Claude doesn't acknowledge system.md at session start.

**Solution:**
```bash
# Verify file exists
ls -la .interface-design/system.md

# Check plugin installation
/plugin menu  # Should show 'interface-design'

# Manually load
/interface-design:status
```

### Inconsistent Components

**Problem:** Components built in same session have different values.

**Solution:**
```bash
# Audit all components
/interface-design:audit src/components

# Re-establish tokens
/interface-design:init
```

### Migration from Old System

**Problem:** Upgrading from `claude-design-skill`.

**Solution:**
```bash
# Rename directory
mv .ds-engineer .interface-design

# Update system file reference
# Change any @ds-engineer mentions to @interface-design

# Reinstall plugin
/plugin marketplace add Dammyjay93/interface-design
/plugin menu
```

### Extract Not Finding Patterns

**Problem:** `/interface-design:extract` returns no patterns.

**Solution:**
```bash
# Ensure components use consistent values
# Look for:
# - Repeated spacing (8px, 16px, 24px)
# - Same button heights (36px appears 5+ times)
# - Consistent border radius (6px/8px)

# If values are scattered, manually create system.md:
mkdir -p .interface-design
cp ~/.claude/skills/interface-design/reference/examples/system-precision.md \
   .interface-design/system.md
```

## Reference Examples

### Precision & Density (Admin/Dashboard)

```markdown
Direction: Technical precision
Foundation: Cool slate
Depth: Borders-only
Spacing: 8px base
Components: Tight, data-dense
```

### Warmth & Approachability (Consumer)

```markdown
Direction: Friendly collaboration
Foundation: Warm amber
Depth: Soft shadows
Spacing: 12px base
Components: Generous, relaxed
```

See full templates in `reference/examples/`:
- `system-precision.md`
- `system-warmth.md`
- `system-trust.md`
- `system-bold.md`
