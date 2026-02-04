---
name: tailwind-styling
description: Tailwind CSS styling patterns, dark theme implementation, and theme management for this project. Use when styling components, implementing UI changes, or working with the design system.
---

# Tailwind Styling

## Core Principles

**NEVER HARDCODE COLORS** - Always use Tailwind config tokens and CSS custom properties for consistent theming and easy dark mode support.

## Theme Structure

### CSS Custom Properties

All colors are defined in `client/styles/index.css` using CSS custom properties:

```css
:root {
  /* Background Colors */
  --color-bg-base: 15 15 56; /* #0F0F38 */
  --color-bg-surface: 26 26 74; /* #1A1A4A */
  --color-bg-surface-light: 37 37 96; /* #252560 */

  /* Accent Colors */
  --color-accent: 45 129 255; /* #2D81FF */
  --color-accent-hover: 74 148 255; /* #4A94FF */

  /* Text Colors */
  --color-text-primary: 255 255 255;
  --color-text-secondary: 160 160 192;
  --color-text-muted: 107 107 141;
}
```

### Tailwind Color Tokens

Use the color tokens defined in `tailwind.config.js`:

```typescript
// ✅ GOOD - Using config tokens
className = 'bg-base text-text-primary border-accent';

// ❌ BAD - Hardcoded colors
className = 'bg-gray-900 text-white border-blue-500';
```

## Color System

### Backgrounds

- `bg-base` - Main background (darkest)
- `bg-surface` - Card/panel backgrounds
- `bg-surface-light` - Hover states, subtle backgrounds

### Text

- `text-text-primary` - Primary text (white)
- `text-text-secondary` - Secondary text (light gray)
- `text-text-muted` - Muted/disabled text

### Accent Colors

- `text-accent` / `bg-accent` - Primary accent (blue)
- `text-accent-hover` / `bg-accent-hover` - Hover state
- `text-accent-light` / `bg-accent-light` - Lighter variant

### Semantic Colors

- `text-error` / `bg-error` - Error states (red)
- `text-success` / `bg-success` - Success states (green)
- `text-warning` / `bg-warning` - Warning states (yellow)

### Borders

- `border-white/10` - Subtle borders
- `border-accent` - Accent borders

## Dark Mode

The project uses forced dark mode. Always ensure components work well with dark backgrounds.

```css
/* Automatically applied */
html {
  color-scheme: dark;
}
```

## Common Patterns

### Glass Morphism Effect

```typescript
className = 'glass rounded-2xl p-6';
```

### CTA Buttons

Multiple styles available in CSS:

```typescript
// Gradient buttons
className = 'gradient-cta shine-effect px-6 py-3 rounded-lg';

// 3D effect button
className = 'cta-3d px-6 py-3 rounded-lg';

// Neon effect
className = 'cta-neon px-6 py-3 rounded-lg';

// Simple accent button
className = 'bg-accent hover:bg-accent-hover text-white glow-blue';
```

### Cards

```typescript
className = 'glass-card';
// Expands to: glass rounded-2xl p-6 transition-all duration-300
```

### Hover Effects

```typescript
// Glow effects
className = 'glow-blue hover:glow-blue-lg';

// Animated borders
className = 'animated-border rounded-lg p-4';
```

## Animations

### Built-in Animations

```typescript
// Fade animations
className = 'animate-fade-in';
className = 'animate-fade-in-up';

// Gradient animation
className = 'animate-gradient bg-gradient-to-r from-accent to-cyan-500';

// Float animation
className = 'animate-float';

// Delays for staggered animations
className = 'animation-delay-200';
className = 'animation-delay-400';
```

### Custom Animation Delays

```typescript
// Create custom delay classes if needed
className = '[animation-delay:0.3s]';
```

## Responsive Design

### Breakpoints

- `xs:` - 475px (custom)
- `sm:` - 640px (default)
- `md:` - 768px (default)
- `lg:` - 1024px (default)
- `xl:` - 1280px (default)

### Example

```typescript
className = 'text-base md:text-lg lg:text-xl';
```

## Typography

### Font Families

- `font-sans` - Inter (default)
- `font-display` - DM Sans (for headings)

### Sizing

Use Tailwind's default font size classes with text color tokens:

```typescript
className = 'font-display text-4xl font-bold text-text-primary';
className = 'font-sans text-sm text-text-secondary';
```

## Component Styling Best Practices

### 1. Use Composition

```typescript
// ✅ GOOD - Compose utility classes
<div className="glass-card border-accent/20">
  <h2 className="text-xl font-bold text-text-primary">Title</h2>
  <p className="text-sm text-text-secondary mt-2">Description</p>
</div>
```

### 2. Avoid Inline Styles

```typescript
// ❌ BAD
<div style={{ backgroundColor: '#0F0F38', color: '#FFFFFF' }}>

// ✅ GOOD
<div className="bg-base text-text-primary">
```

### 3. Consistent Spacing

Use Tailwind's spacing scale consistently:

- `p-4`, `p-6`, `p-8` for padding
- `m-2`, `m-4`, `m-6` for margins
- `gap-2`, `gap-4`, `gap-6` for flex/grid gaps

### 4. Border Radius

- `rounded-lg` - Standard radius (8px)
- `rounded-xl` - Large radius (12px)
- `rounded-2xl` - Extra large radius (16px)
- `rounded-full` - Circle

## Extending the Theme

### Adding New Colors

1. Add CSS variable to `client/styles/index.css`
2. Update `tailwind.config.js` to reference the variable

```css
/* client/styles/index.css */
:root {
  --color-new-brand: 123 45 67;
}
```

```javascript
/* tailwind.config.js */
colors: {
  'brand': 'rgb(var(--color-new-brand) / <alpha-value>)',
}
```

### Adding New Animations

1. Define keyframes in CSS
2. Add to Tailwind config or use @layer utilities

```css
/* client/styles/index.css */
@layer utilities {
  @keyframes custom-slide {
    from {
      transform: translateX(-100%);
    }
    to {
      transform: translateX(0);
    }
  }

  .animate-custom-slide {
    animation: custom-slide 0.3s ease-out;
  }
}
```

## Common Use Cases

### Navigation/Header

```typescript
className = 'glass border-b border-white/10 px-6 py-4';
```

### Buttons

```typescript
// Primary button
className = 'bg-accent hover:bg-accent-hover text-white px-6 py-2 rounded-lg transition-colors';

// Secondary button
className = 'glass hover:bg-surface-light text-text-primary px-6 py-2 rounded-lg transition-colors';

// Ghost button
className = 'text-accent hover:text-accent-hover px-6 py-2 rounded-lg transition-colors';
```

### Forms

```typescript
// Input field
className =
  'bg-surface border border-white/10 rounded-lg px-4 py-2 text-text-primary placeholder:text-text-muted focus:border-accent focus:outline-none';

// Label
className = 'block text-sm font-medium text-text-secondary mb-2';

// Error message
className = 'text-sm text-error mt-1';
```

### Modal/Dialog

```typescript
// Overlay
className = 'fixed inset-0 bg-black/50 backdrop-blur-sm z-50';

// Content
className = 'glass-card max-w-md mx-auto relative';
```

## Testing Dark Mode

Always test components with:

- Different text color combinations
- Hover states
- Focus states
- Disabled states
- Error/success states

## Migration from Hardcoded Values

When updating existing components:

1. Identify hardcoded colors (hex codes, named colors)
2. Map to appropriate theme token
3. Test in both light and dark contexts (if applicable)
4. Ensure hover/focus states use theme tokens

Example migration:

```typescript
// Before
className = 'bg-gray-900 text-gray-100 border-gray-700 hover:bg-gray-800';

// After
className = 'bg-base text-text-primary border-white/10 hover:bg-surface-light';
```
