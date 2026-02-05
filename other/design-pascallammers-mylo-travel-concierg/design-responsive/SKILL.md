---
name: design-responsive
description: |
  Mobile-first responsive design for beautiful, multi-device UIs. Breakpoints, fluid layouts,
  touch optimization, and creative responsive patterns for distinctive experiences across screens.

  Use when building responsive UIs or adapting for mobile/tablet/desktop:
  - Creating mobile-first layouts, responsive landing pages, web apps
  - Defining breakpoints and fluid typography (mobile/tablet/desktop sizes)
  - Optimizing for touch devices, mobile users, smartphone/tablet interactions
  - Responsive component patterns (navigation, tables, forms, images)
  - User mentions "mobile", "responsive", "tablet", "multi-device", "touch"

  Keywords: responsive, mobile-first, mobile, tablet, desktop, breakpoints, touch, multi-device

  Mobile-first approach: Design for mobile constraints first, enhance progressively.
  Integrates with design-fundamentals: Apply spacing, typography, color systems responsively.
---

# Responsive Design

## Purpose
Create beautiful, functional UIs that adapt gracefully across all device sizes through mobile-first approach.

---

## Core Principle

**Mobile-First Approach**

Design for mobile first, enhance for larger screens.

**Why:**
- Most users on mobile devices
- Easier to enhance than to strip down
- Forces focus on essential content
- Better performance on mobile
- Encourages progressive enhancement

---

## Creative Responsive Patterns

### Maintain Aesthetic Across Devices

**Principle:** Your chosen aesthetic (from design-fundamentals) should feel consistent across all screen sizes.

**Minimal/Refined aesthetic:**
- Mobile: Generous whitespace, elegant typography
- Desktop: Maximum whitespace, elevated elegance

**Bold/Vibrant aesthetic:**
- Mobile: Strong colors, compact energy
- Desktop: Full boldness, dramatic scale

**Playful/Friendly aesthetic:**
- Mobile: Rounded shapes, cozy spacing
- Desktop: Full playfulness with space for delight

### Beyond Stack→Row: Creative Layouts

**Standard pattern** (functional but predictable):
- Mobile: Stack vertically
- Desktop: Side-by-side columns

**Creative patterns:**

**Asymmetric Responsive:**
- Mobile: Single column with visual hierarchy through size
- Desktop: Asymmetric grid with unexpected placement

**Diagonal Flow:**
- Mobile: Vertical flow with diagonal visual elements
- Desktop: Diagonal layouts, overlapping sections

**Responsive Visual Hierarchy:**
- Scale dramatically: Primary CTAs, hero headings (2-3x increase)
- Scale subtly: Body text, labels (minimal change)
- Spacing hierarchy: Tight on mobile, generous on desktop

---

## Breakpoint System

### Defining Breakpoints

**Common approach (adjust to your content):**
- **Mobile**: ~320-640px (default, no media query)
- **Small/Tablet**: ~640-768px+
- **Medium**: ~768-1024px+
- **Large**: ~1024-1280px+
- **XLarge**: ~1280px+

**Guidelines:**
- Use 3-4 major breakpoints
- Choose values based on where YOUR content breaks
- Avoid device-specific breakpoints
- Use `min-width` queries (mobile-first)

### Mobile-First Pattern

**Progression:**
1. Mobile (default): Single column, stacked, touch-optimized
2. Tablet: 2 columns, more spacing
3. Desktop: Multi-column, hover states

---

## Responsive Typography

### Fluid Typography

**Approaches:**
- Viewport units: Scale proportionally
- clamp(): Define min, preferred, max sizes
- Stepped sizes: Different fixed sizes per breakpoint

**Guidelines:**
- Body text: 16px+ on mobile
- Scale up slightly on desktop (18-20px)
- Headings scale more than body
- Maintain hierarchy ratios across breakpoints

### Line Length

**Guidelines:**
- Mobile: 45-75 characters per line acceptable
- Desktop: 50-75 characters optimal
- Use max-width to constrain long-form content

---

## Responsive Layout Patterns

### Stack → Row

**Pattern:** Vertical on mobile, horizontal on larger screens.

**Use cases:** Navigation, form layouts, card grids, content + sidebar

### Fluid Grids

**Patterns:**
- Auto-fit: Columns wrap as needed
- Percentage-based: Columns use % width
- Flexible: Columns grow/shrink with flexbox

**Mobile:** 1 column
**Tablet:** 2 columns
**Desktop:** 3+ columns

### Sidebar Layouts

**Mobile:** Sidebar below main (stacked)
**Desktop:** Fixed sidebar + scrollable main

---

## Component Responsive Patterns

### Navigation

**Mobile:**
- Hamburger menu
- Full-screen overlay or drawer
- Touch-optimized tap targets

**Desktop:**
- Horizontal navigation bar
- Hover dropdowns
- Keyboard accessible

### Data Tables

**Mobile:**
- Transform to card layout
- Horizontal scroll (when cards inappropriate)
- Show only essential columns

**Desktop:**
- Full table with all columns
- Hover states on rows

### Forms

**Mobile:**
- Full-width inputs
- Single column layout
- Large touch targets (44x44px minimum)
- Vertical button groups

**Desktop:**
- Multi-column forms (when logical)
- Side-by-side labels and inputs

### Images and Media

**Responsive Images:**
- Multiple sizes for different screens
- Lazy loading for below-fold content
- Maintain consistent aspect ratios

---

## Touch Optimization

### Tap Target Sizes

**Standards (verify with your platform):**
- 44x44px (Apple/Google baseline)
- 48x48px (WCAG 2.1 AAA)
- Spacing between targets: 8px minimum

**Why:** Finger taps less precise than mouse (~9mm average finger pad)

**Applies to:** Buttons, links, form inputs, checkboxes/radios, icons

### Touch Gestures

**Standard gestures:**
- Tap: Activate/select
- Scroll: Navigate content
- Swipe: Navigate between items, dismiss
- Pinch: Zoom (when appropriate)

**Don't require:** Hover for critical functionality

### Touch Feedback

**Patterns:**
- Slight scale or opacity change on tap
- Ripple effect
- Brief highlight or color shift

**Timing:** 100-200ms, feels immediate

### Mobile Considerations

**Input focus:**
- iOS auto-zooms on inputs with font size < 16px
- Solution: Use 16px+ for input fields

**Viewport meta tag:**
- Always include: `<meta name="viewport" content="width=device-width, initial-scale=1">`

---

## Container Queries (Modern)

**Principle:** Components respond to their container size, not viewport.

**Why better:**
- Component-based (matches modern architecture)
- Reusable components adapt to any container

**Use cases:** Card components, nested layouts, design system components

---

## Responsive Spacing

### Fluid Spacing

**Approaches:**
- clamp(): Define min, preferred, max spacing
- Viewport units: Scale proportionally
- Stepped values: Different spacing per breakpoint

**Guidelines:**
- Mobile: Tighter spacing (conserve space)
- Desktop: Generous spacing (utilize available space)
- Maintain spacing scale ratios from design-fundamentals

---

## Performance Considerations

### Lazy Loading

**Load content as needed:**
- Images below fold
- Heavy components (charts, maps)
- Large lists (virtual scrolling)

### Image Optimization

**Best practices:**
- Use appropriate formats (WebP, AVIF)
- Serve different sizes per device
- Compress images aggressively
- Use CDN for delivery

---

## Testing Checklist

### Device Testing
- [ ] Real mobile devices (iOS, Android)
- [ ] Real tablets
- [ ] Desktop at various sizes
- [ ] Landscape and portrait orientations

### Browser DevTools
- [ ] Responsive design mode
- [ ] Test all major breakpoints
- [ ] Zoom to 200% (accessibility)
- [ ] Network throttling (performance)

### Touch Interaction
- [ ] All tap targets meet minimum size
- [ ] Adequate spacing between targets (8px+)
- [ ] Touch feedback visible
- [ ] No hover-only interactions for critical features

### Content & Aesthetic
- [ ] Text readable on all screen sizes
- [ ] Images scale properly
- [ ] No unintended horizontal scroll
- [ ] No content cut off
- [ ] Chosen aesthetic maintained across devices
- [ ] Visual hierarchy clear at all sizes

---

## Common Mistakes

1. **Desktop-first** - Start mobile, enhance up
2. **Fixed widths** - Use max-width instead
3. **Too many breakpoints** - 3-4 is enough
4. **Hover-only interactions** - Not accessible on touch
5. **Small touch targets** - Verify minimum size
6. **Horizontal scroll** - Only use intentionally
7. **Ignoring landscape** - Test both orientations
8. **No real device testing** - Emulators aren't enough
9. **Losing aesthetic on mobile** - Maintain distinctiveness
10. **Copying breakpoints blindly** - Base on YOUR content

---

## Key Takeaway

**Principles over prescriptive values. Fluidity over rigidity.**

Common standards (44px, 640px, 16px) are starting points, not absolute rules. Adjust to your design system, platform, and content needs.

Start with mobile constraints, enhance progressively. Maintain your aesthetic identity across all devices—adapted to each device's strengths.
