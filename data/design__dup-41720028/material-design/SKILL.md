---
name: material-design
description: Create UI components and designs following Google Material Design 3 (Material You) guidelines. Use when building Material UI components, implementing Material theming, working with elevation, color systems, typography, motion, or creating Android/web interfaces with Material Design patterns.
---

# Material Design Implementation Guide

This skill helps you create beautiful, consistent user interfaces following Google's Material Design 3 (Material You) guidelines. It covers components, design tokens, theming, accessibility, and best practices.

## When to Use This Skill

Use this skill when:
- Creating new UI components with Material Design styling
- Implementing Material Design 3 (Material You) theming
- Setting up color schemes, typography, or elevation systems
- Building responsive layouts with Material Design patterns
- Converting designs to Material Design specifications
- Ensuring accessibility compliance with Material guidelines
- Working with React (MUI), Vue (Vuetify), or vanilla CSS/HTML
- Building Android apps with Material Components
- Implementing motion and animations per Material guidelines

## Core Material Design 3 Principles

### 1. **Material You (Personalization)**
- Dynamic color theming based on user preferences
- Adaptive layouts that respond to context
- Emphasis on personal expression

### 2. **Design Tokens**
- **Color**: Primary, Secondary, Tertiary, Error, Neutral colors with variants
- **Typography**: Display, Headline, Title, Body, Label scales
- **Elevation**: Surface levels 0-5
- **Shape**: Rounded corners (none, small, medium, large, extra-large)
- **Motion**: Duration and easing curves

### 3. **Key Concepts**
- **Surface**: Containers that hold content
- **State Layers**: Visual feedback for interaction states
- **Elevation**: Depth through shadows and tonal differences
- **Accessibility**: WCAG 2.1 AA compliance minimum

## Material Design 3 Color System

### Color Roles

```
Primary: Main brand color (buttons, active states)
├── On-Primary: Text/icons on primary color
├── Primary Container: Less prominent primary elements
└── On-Primary Container: Content on primary container

Secondary: Accent color (FABs, selection controls)
├── On-Secondary
├── Secondary Container
└── On-Secondary Container

Tertiary: Complementary accent
├── On-Tertiary
├── Tertiary Container
└── On-Tertiary Container

Error: Error states
├── On-Error
├── Error Container
└── On-Error Container

Surfaces:
├── Surface: Default background
├── Surface-Variant: Subtle differentiation
├── On-Surface: Text/icons on surface
├── On-Surface-Variant: Lower emphasis text
├── Outline: Borders and dividers
└── Outline-Variant: Decorative elements
```

### Dynamic Color Generation

Material Design 3 uses HCT (Hue, Chroma, Tone) color space:

```javascript
// Example: Generate color scheme from source color
const sourceColor = '#6750A4'; // Primary color

// Tonal Palette (0-100 tone scale)
const tones = {
  0: '#000000',    // Black
  10: '#21005D',   // Darkest
  20: '#381E72',
  30: '#4F378B',
  40: '#6750A4',   // Source
  50: '#7F67BE',
  60: '#9A82DB',
  70: '#B69DF8',
  80: '#D0BCFF',
  90: '#EADDFF',
  95: '#F6EDFF',
  99: '#FFFBFE',
  100: '#FFFFFF'  // White
};
```

## Typography Scale

### Type Scale Specifications

```css
/* Display - Large, impactful text */
.md-display-large {
  font-size: 57px;
  line-height: 64px;
  font-weight: 400;
  letter-spacing: -0.25px;
}

.md-display-medium {
  font-size: 45px;
  line-height: 52px;
  font-weight: 400;
}

.md-display-small {
  font-size: 36px;
  line-height: 44px;
  font-weight: 400;
}

/* Headline - High-emphasis text */
.md-headline-large {
  font-size: 32px;
  line-height: 40px;
  font-weight: 400;
}

.md-headline-medium {
  font-size: 28px;
  line-height: 36px;
  font-weight: 400;
}

.md-headline-small {
  font-size: 24px;
  line-height: 32px;
  font-weight: 400;
}

/* Title - Medium-emphasis text */
.md-title-large {
  font-size: 22px;
  line-height: 28px;
  font-weight: 400;
}

.md-title-medium {
  font-size: 16px;
  line-height: 24px;
  font-weight: 500;
  letter-spacing: 0.15px;
}

.md-title-small {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  letter-spacing: 0.1px;
}

/* Body - Main content */
.md-body-large {
  font-size: 16px;
  line-height: 24px;
  font-weight: 400;
  letter-spacing: 0.5px;
}

.md-body-medium {
  font-size: 14px;
  line-height: 20px;
  font-weight: 400;
  letter-spacing: 0.25px;
}

.md-body-small {
  font-size: 12px;
  line-height: 16px;
  font-weight: 400;
  letter-spacing: 0.4px;
}

/* Label - UI elements */
.md-label-large {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  letter-spacing: 0.1px;
}

.md-label-medium {
  font-size: 12px;
  line-height: 16px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.md-label-small {
  font-size: 11px;
  line-height: 16px;
  font-weight: 500;
  letter-spacing: 0.5px;
}
```

## Elevation System

Material Design 3 uses **tonal elevation** instead of shadows alone:

```css
/* Elevation Levels */
.md-elevation-0 {
  box-shadow: none;
  /* Surface tint: 0% opacity */
}

.md-elevation-1 {
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.3),
              0px 1px 3px 1px rgba(0, 0, 0, 0.15);
  /* Surface tint: 5% opacity */
}

.md-elevation-2 {
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.3),
              0px 2px 6px 2px rgba(0, 0, 0, 0.15);
  /* Surface tint: 8% opacity */
}

.md-elevation-3 {
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3),
              0px 4px 8px 3px rgba(0, 0, 0, 0.15);
  /* Surface tint: 11% opacity */
}

.md-elevation-4 {
  box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.3),
              0px 6px 10px 4px rgba(0, 0, 0, 0.15);
  /* Surface tint: 12% opacity */
}

.md-elevation-5 {
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.3),
              0px 8px 12px 6px rgba(0, 0, 0, 0.15);
  /* Surface tint: 14% opacity */
}
```

## Shape System

```css
/* Corner Radius Tokens */
:root {
  --md-shape-corner-none: 0px;
  --md-shape-corner-extra-small: 4px;
  --md-shape-corner-small: 8px;
  --md-shape-corner-medium: 12px;
  --md-shape-corner-large: 16px;
  --md-shape-corner-extra-large: 28px;
  --md-shape-corner-full: 9999px; /* Fully rounded */
}

/* Component-specific shapes */
.md-button {
  border-radius: var(--md-shape-corner-full); /* Fully rounded */
}

.md-card {
  border-radius: var(--md-shape-corner-medium); /* 12px */
}

.md-dialog {
  border-radius: var(--md-shape-corner-extra-large); /* 28px */
}

.md-chip {
  border-radius: var(--md-shape-corner-small); /* 8px */
}
```

## Common Components

### Button (Filled)

```html
<button class="md-button-filled">
  <span class="md-button-label">Button</span>
</button>
```

```css
.md-button-filled {
  /* Container */
  background-color: var(--md-sys-color-primary);
  border: none;
  border-radius: var(--md-shape-corner-full);
  padding: 10px 24px;
  min-height: 40px;

  /* Label */
  color: var(--md-sys-color-on-primary);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1px;

  /* State layers */
  position: relative;
  cursor: pointer;
  transition: box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-button-filled:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--md-sys-color-on-primary);
  opacity: 0.08;
  border-radius: inherit;
}

.md-button-filled:focus::before {
  opacity: 0.12;
}

.md-button-filled:active::before {
  opacity: 0.12;
}

.md-button-filled:disabled {
  background-color: rgba(var(--md-sys-color-on-surface-rgb), 0.12);
  color: rgba(var(--md-sys-color-on-surface-rgb), 0.38);
  cursor: not-allowed;
}
```

### Card (Elevated)

```html
<div class="md-card-elevated">
  <div class="md-card-content">
    <h3 class="md-title-large">Card Title</h3>
    <p class="md-body-medium">Card content goes here.</p>
  </div>
  <div class="md-card-actions">
    <button class="md-button-text">Action</button>
  </div>
</div>
```

```css
.md-card-elevated {
  background-color: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-shape-corner-medium);
  padding: 16px;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.3),
              0px 1px 3px 1px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-card-elevated:hover {
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3),
              0px 4px 8px 3px rgba(0, 0, 0, 0.15);
}

.md-card-content {
  margin-bottom: 16px;
}

.md-card-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
```

### Text Field (Filled)

```html
<div class="md-text-field-filled">
  <label class="md-text-field-label" for="input">Label</label>
  <input
    type="text"
    id="input"
    class="md-text-field-input"
    placeholder="Placeholder"
  >
  <div class="md-text-field-active-indicator"></div>
</div>
```

```css
.md-text-field-filled {
  position: relative;
  background-color: var(--md-sys-color-surface-container-highest);
  border-radius: var(--md-shape-corner-extra-small) var(--md-shape-corner-extra-small) 0 0;
  padding: 8px 16px 8px 16px;
}

.md-text-field-label {
  display: block;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0.4px;
  margin-bottom: 4px;
}

.md-text-field-input {
  width: 100%;
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
  outline: none;
  padding: 0;
}

.md-text-field-active-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background-color: var(--md-sys-color-on-surface-variant);
  transition: height 0.2s, background-color 0.2s;
}

.md-text-field-filled:focus-within .md-text-field-active-indicator {
  height: 2px;
  background-color: var(--md-sys-color-primary);
}
```

## Motion & Animation

### Duration Tokens

```css
:root {
  /* Short - Small UI elements */
  --md-motion-duration-short1: 50ms;
  --md-motion-duration-short2: 100ms;
  --md-motion-duration-short3: 150ms;
  --md-motion-duration-short4: 200ms;

  /* Medium - Moving UI elements */
  --md-motion-duration-medium1: 250ms;
  --md-motion-duration-medium2: 300ms;
  --md-motion-duration-medium3: 350ms;
  --md-motion-duration-medium4: 400ms;

  /* Long - Large/complex elements */
  --md-motion-duration-long1: 450ms;
  --md-motion-duration-long2: 500ms;
  --md-motion-duration-long3: 550ms;
  --md-motion-duration-long4: 600ms;

  /* Extra Long - Large screen transitions */
  --md-motion-duration-extra-long1: 700ms;
  --md-motion-duration-extra-long2: 800ms;
  --md-motion-duration-extra-long3: 900ms;
  --md-motion-duration-extra-long4: 1000ms;
}
```

### Easing Curves

```css
:root {
  /* Standard - Most common */
  --md-motion-easing-standard: cubic-bezier(0.4, 0, 0.2, 1);

  /* Emphasized - Important transitions */
  --md-motion-easing-emphasized: cubic-bezier(0.2, 0, 0, 1);

  /* Decelerated - Entering screen */
  --md-motion-easing-decelerated: cubic-bezier(0, 0, 0.2, 1);

  /* Accelerated - Exiting screen */
  --md-motion-easing-accelerated: cubic-bezier(0.4, 0, 1, 1);
}
```

### Example Animations

```css
/* Fade In */
@keyframes md-fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: md-fade-in var(--md-motion-duration-short4) var(--md-motion-easing-decelerated);
}

/* Scale Up */
@keyframes md-scale-up {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.scale-up {
  animation: md-scale-up var(--md-motion-duration-medium2) var(--md-motion-easing-emphasized);
}

/* Slide Up */
@keyframes md-slide-up {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.slide-up {
  animation: md-slide-up var(--md-motion-duration-medium4) var(--md-motion-easing-emphasized);
}
```

## Accessibility Guidelines

### Color Contrast

Material Design requires WCAG 2.1 AA compliance:

- **Normal text**: 4.5:1 contrast ratio minimum
- **Large text** (18px+ or 14px+ bold): 3:1 minimum
- **UI components**: 3:1 minimum

```javascript
// Check contrast ratio
function getContrastRatio(color1, color2) {
  // Returns ratio (e.g., 4.5)
  // Use online tools or libraries like 'color' npm package
}

// Material Design color roles ensure proper contrast by default
```

### Touch Targets

Minimum touch target size: **48x48 dp (density-independent pixels)**

```css
.md-button {
  min-width: 48px;
  min-height: 48px;
  /* Even if visual size is smaller, ensure interactive area is 48x48 */
}

/* For small icons, add padding */
.md-icon-button {
  width: 40px;
  height: 40px;
  padding: 4px; /* Total: 48x48 */
}
```

### Focus Indicators

Always provide visible focus indicators:

```css
.md-interactive:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}

/* State layer for focus */
.md-interactive:focus-visible::before {
  opacity: 0.12;
}
```

### ARIA Attributes

```html
<!-- Button with icon -->
<button aria-label="Close dialog">
  <svg>...</svg>
</button>

<!-- Input with label -->
<label for="email">Email</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-describedby="email-hint"
>
<span id="email-hint">We'll never share your email.</span>

<!-- Disabled state -->
<button disabled aria-disabled="true">
  Submit
</button>
```

## Responsive Design

### Breakpoints

```css
:root {
  --md-breakpoint-compact: 600px;   /* Phone */
  --md-breakpoint-medium: 840px;    /* Tablet */
  --md-breakpoint-expanded: 1200px; /* Desktop */
  --md-breakpoint-large: 1600px;    /* Large desktop */
}

/* Compact (0-599px) */
@media (max-width: 599px) {
  .md-container {
    padding: 16px;
  }
}

/* Medium (600-839px) */
@media (min-width: 600px) and (max-width: 839px) {
  .md-container {
    padding: 24px;
  }
}

/* Expanded (840-1199px) */
@media (min-width: 840px) and (max-width: 1199px) {
  .md-container {
    padding: 24px;
    max-width: 840px;
    margin: 0 auto;
  }
}

/* Large (1200px+) */
@media (min-width: 1200px) {
  .md-container {
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Adaptive Layouts

```css
/* Navigation Rail (Medium+) */
@media (min-width: 600px) {
  .md-nav-rail {
    display: flex;
    flex-direction: column;
    width: 80px;
  }

  .md-nav-drawer {
    display: none;
  }
}

/* Navigation Drawer (Expanded+) */
@media (min-width: 840px) {
  .md-nav-drawer {
    display: block;
    width: 256px;
  }

  .md-nav-rail {
    display: none;
  }
}
```

## AI Assistant Instructions

When this skill is activated, you should:

### 1. **Clarify Requirements**

Ask the user:
- Which framework are they using? (React/MUI, Vue/Vuetify, vanilla HTML/CSS, Android)
- Which Material Design version? (Prefer Material Design 3 unless specified)
- What component(s) do they need?
- Do they have an existing theme/color scheme?
- Are there specific accessibility requirements?

### 2. **Follow Material Design 3 Guidelines**

Always:
- Use Material Design 3 (Material You) specifications by default
- Apply proper design tokens (color roles, typography scale, elevation)
- Ensure 48x48dp minimum touch targets
- Provide accessible color contrast (WCAG 2.1 AA minimum)
- Include proper state layers (hover, focus, active, disabled)
- Use appropriate motion/animation with correct easing curves
- Follow component-specific guidelines from Material Design documentation

Never:
- Use arbitrary colors—always use semantic color roles
- Skip accessibility considerations
- Implement custom components without checking official Material specs
- Use outdated Material Design 2 patterns (unless explicitly requested)
- Forget state layers for interactive elements

### 3. **Provide Complete Implementations**

Each component should include:
- **HTML structure** (semantic, accessible markup)
- **CSS styles** (using design tokens, proper specificity)
- **Variants** (filled, outlined, text, etc.)
- **States** (default, hover, focus, active, disabled)
- **Responsive behavior** (if applicable)
- **ARIA attributes** (for accessibility)
- **Code comments** (explaining Material Design specifications)

### 4. **Reference Official Documentation**

When implementing components:
- Check [Material Design 3 Guidelines](https://m3.material.io/)
- Reference component specifications for exact measurements
- Use official design tokens and naming conventions
- Link to relevant documentation sections in comments

### 5. **Optimize for Framework**

For **React (MUI)**:
- Use MUI components and theming system
- Leverage `sx` prop or `styled` API
- Follow MUI's Material Design 3 migration guide

For **Vue (Vuetify)**:
- Use Vuetify 3+ components (Material Design 3)
- Apply theme customization via vuetify config
- Use Vuetify's built-in utilities

For **Vanilla HTML/CSS**:
- Provide self-contained, copy-paste ready code
- Use CSS custom properties for theming
- Include necessary JavaScript for interactions (if needed)

For **Android**:
- Use Material Components for Android library
- Provide XML layouts and Kotlin/Java code
- Reference Android-specific Material guidelines

### 6. **Offer Customization Guidance**

After providing base implementation:
- Show how to customize colors/theme
- Explain how to adjust spacing/sizing
- Provide variants (different sizes, styles)
- Suggest related components or patterns

### 7. **Validate Against Best Practices**

Before finalizing:
- ✅ Color contrast meets WCAG 2.1 AA
- ✅ Touch targets are 48x48dp minimum
- ✅ Focus indicators are visible and clear
- ✅ Component follows Material Design 3 specs
- ✅ Responsive design is considered
- ✅ Motion follows Material easing curves
- ✅ Code is clean, commented, and reusable

## Common Patterns

### Pattern 1: Full Page Layout with App Bar

See [examples/layout-app-bar.html](examples/layout-app-bar.html)

### Pattern 2: Form with Material Text Fields

See [examples/form-material-inputs.html](examples/form-material-inputs.html)

### Pattern 3: Card Grid with Responsive Layout

See [examples/card-grid.html](examples/card-grid.html)

### Pattern 4: Bottom Navigation

See [examples/bottom-navigation.html](examples/bottom-navigation.html)

## Troubleshooting

### Issue: Colors don't look right in dark mode

**Solution**: Ensure you're using semantic color roles (e.g., `var(--md-sys-color-primary)`) instead of hard-coded hex values. Material Design 3 color roles automatically adapt to light/dark themes.

### Issue: Text is hard to read

**Solution**: Check color contrast ratio (4.5:1 for normal text, 3:1 for large text). Use `on-*` color roles for text on colored backgrounds (e.g., `on-primary` for text on primary color).

### Issue: Buttons look flat/lack depth

**Solution**: Add proper elevation (box-shadow) and state layers. Filled buttons should have elevation level 0 at rest, level 1 on hover. Use `::before` pseudo-element for state layers.

### Issue: Animations feel choppy

**Solution**: Use Material Design easing curves (`cubic-bezier` values). Avoid linear animations. Choose appropriate durations (short: <200ms, medium: 200-400ms, long: 400-600ms).

### Issue: Touch targets too small on mobile

**Solution**: Ensure minimum 48x48dp interactive area. Add padding to visual elements if needed to reach 48x48dp total touchable area.

## Additional Resources

- [Material Design 3 Official Guidelines](https://m3.material.io/)
- [Material Theme Builder](https://m3.material.io/theme-builder) - Generate color schemes
- [Material Design Icons](https://fonts.google.com/icons) - Official icon library
- [Material Components Web](https://github.com/material-components/material-web) - Web Components
- [MUI (React)](https://mui.com/material-ui/) - React implementation
- [Vuetify (Vue)](https://vuetifyjs.com/) - Vue implementation
- [Material Components Android](https://github.com/material-components/material-components-android)
- [Figma Material 3 Design Kit](https://www.figma.com/community/file/1035203688168086460)

## Quick Reference: Design Tokens

```css
/* Color Roles */
--md-sys-color-primary
--md-sys-color-on-primary
--md-sys-color-primary-container
--md-sys-color-on-primary-container
--md-sys-color-secondary
--md-sys-color-tertiary
--md-sys-color-error
--md-sys-color-surface
--md-sys-color-on-surface
--md-sys-color-outline

/* Typography */
--md-sys-typescale-display-large
--md-sys-typescale-headline-large
--md-sys-typescale-title-large
--md-sys-typescale-body-large
--md-sys-typescale-label-large

/* Elevation */
--md-sys-elevation-level0: box-shadow: none;
--md-sys-elevation-level1: box-shadow: 0px 1px 2px...;
--md-sys-elevation-level2: box-shadow: 0px 1px 2px...;

/* Shape */
--md-shape-corner-extra-small: 4px;
--md-shape-corner-small: 8px;
--md-shape-corner-medium: 12px;
--md-shape-corner-large: 16px;
--md-shape-corner-extra-large: 28px;
```

---

**Note**: This skill focuses on Material Design 3 (Material You). For Material Design 2 implementations, please specify this explicitly.
