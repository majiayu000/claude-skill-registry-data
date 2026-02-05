---
name: layout-builder
description: Interactive Flexbox and Grid layout generator with real-time code output. Creates production-ready layouts based on your requirements with proper fallbacks and responsive considerations. Use when building layouts, grids, or complex positioning systems.
allowed-tools: Read, Write, Edit
---

# Layout Builder Skill

This skill helps you create modern CSS layouts using Flexbox and CSS Grid through an interactive process. I'll guide you through layout requirements and generate production-ready, responsive code.

## What I Can Help With

### Flexbox Layouts
- Horizontal and vertical navigation bars
- Card grids with flexible wrapping
- Holy grail layouts (header, footer, sidebar, main content)
- Centered content (horizontal, vertical, or both)
- Equal-height columns
- Space distribution patterns
- Flexible forms and button groups

### CSS Grid Layouts
- Responsive grid systems
- Dashboard layouts with named grid areas
- Magazine-style layouts
- Asymmetric grids
- Sidebar + content layouts
- Card masonry layouts
- Complex multi-column designs

### Responsive Patterns
- Mobile-first responsive layouts
- Container query-based layouts
- Fluid grids with auto-fit/auto-fill
- Breakpoint-based layout changes
- Responsive navigation patterns

## How To Use This Skill

I'll ask you questions about your layout needs and generate the CSS code. Here's what I need to know:

1. **Layout Type**: Flexbox, Grid, or combination?
2. **Purpose**: What are you building? (navigation, card grid, page layout, etc.)
3. **Responsiveness**: Mobile-first? Desktop-first? Specific breakpoints?
4. **Constraints**: Fixed widths, minimum/maximum sizes, gaps/spacing?
5. **Content**: Number of items, variable content lengths?

## Example Interactions

### Example 1: Card Grid

**You**: "I need a responsive card grid that shows 1 column on mobile, 2 on tablet, and 3 on desktop"

**I will provide**:
```css
/* Responsive card grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

/* Card styling */
.card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .card-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
```

### Example 2: Navbar

**You**: "Create a responsive navbar with logo on left, nav items in center, and button on right"

**I will provide**:
```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar__logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar__nav {
  display: flex;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar__nav a {
  text-decoration: none;
  color: inherit;
  transition: color 0.2s;
}

.navbar__nav a:hover {
  color: #0066cc;
}

.navbar__button {
  padding: 0.5rem 1.5rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
  }

  .navbar__nav {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
}
```

## Layout Patterns I Know

### Flexbox Patterns

#### Center Anything
```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

#### Sidebar Layout
```css
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  flex: 0 0 250px;
}

.main {
  flex: 1;
}
```

#### Card Row
```css
.card-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.card {
  flex: 1 1 300px;
}
```

### Grid Patterns

#### Holy Grail Layout
```css
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav main aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: 1rem;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }
```

#### Dashboard Grid
```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
}

.widget-large {
  grid-column: span 8;
}

.widget-small {
  grid-column: span 4;
}
```

## Best Practices I Follow

✓ **Mobile-first approach** - Start with mobile layout, enhance for larger screens
✓ **Semantic HTML** - Use appropriate HTML elements with layout CSS
✓ **Flexible units** - Use relative units (rem, %, fr) over fixed pixels
✓ **Gap instead of margins** - Use gap property for consistent spacing
✓ **Logical properties** - Support RTL languages with logical properties
✓ **Container queries** - Use when available for truly responsive components
✓ **Fallbacks** - Provide fallbacks for older browsers when needed
✓ **Accessibility** - Maintain logical DOM order, ensure keyboard navigation works

## When To Use Which Layout System

### Use Flexbox When:
- Creating one-dimensional layouts (rows or columns)
- Items need to wrap and reflow
- Content size should drive layout
- Building navigation, toolbars, or button groups
- Centering content
- Distributing space between items

### Use Grid When:
- Creating two-dimensional layouts (rows AND columns)
- Items need precise placement
- Creating responsive layouts without media queries
- Building page layouts with defined areas
- Creating complex asymmetric layouts
- Need alignment in both directions

### Use Both When:
- Grid for overall page structure
- Flexbox for components within grid cells
- Complex layouts requiring both approaches

## Just Ask!

Tell me what layout you need, and I'll guide you through creating it with modern, responsive CSS. I'll ask clarifying questions if needed and provide complete, production-ready code.

**Example requests:**
- "I need a 3-column responsive layout"
- "Create a centered modal dialog"
- "Build a sticky footer layout"
- "Make a magazine-style grid"
- "Design a responsive navigation menu"
- "Create a dashboard layout with widgets"
