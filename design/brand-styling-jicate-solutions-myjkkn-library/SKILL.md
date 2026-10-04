---
name: brand-styling
description: Comprehensive brand styling system for standardizing design across all projects. Implements brand colors, typography, spacing, responsive design, and dark mode using Tailwind CSS and Next.js themes. Use when creating new projects, implementing UI components, or ensuring design consistency across web applications. (project)
---

# Brand Styling Skill

## Purpose

This skill provides a comprehensive, standardized brand styling system for JKKN COE and related web development projects. It ensures visual consistency across applications by defining brand colors, typography scales, spacing systems, responsive breakpoints, and complete dark mode implementation using Tailwind CSS and Next.js themes.

## When to Use This Skill

Use this skill when:

- **Starting a new web project** - Set up the complete styling foundation
- **Creating UI components** - Ensure components follow brand guidelines
- **Implementing dark mode** - Apply proper dark mode color schemes
- **Responsive design** - Follow standardized breakpoints and mobile-first approach
- **Design consistency** - Reference brand colors, typography, and spacing standards
- **Refactoring existing styles** - Migrate to standardized brand styling
- **Onboarding new developers** - Provide clear styling guidelines and standards

## Brand Identity

### Brand Colors

**Primary Green**: `#0b6d41` (brand-green-500)
- Main brand color for primary actions, headers, and key UI elements
- Use for buttons, links, active states, and brand accents
- HSL: `152 82% 24%` (light mode) / `152 76% 42%` (dark mode - lighter for visibility)

**Color Scale (brand-green)**:
| Shade | Hex | Usage |
|-------|-----|-------|
| 50 | `#e6f5ee` | Backgrounds, hover states |
| 100 | `#b3e0cc` | Light accents |
| 200 | `#80cbaa` | Borders, dividers |
| 300 | `#4db688` | Secondary elements |
| 400 | `#2a9966` | Active states |
| 500 | `#0b6d41` | **Primary (DEFAULT)** |
| 600 | `#095a35` | Hover states |
| 700 | `#074829` | Pressed states |
| 800 | `#05351d` | Dark accents |
| 900 | `#032211` | Very dark accents |

**Secondary Yellow**: `#ffde59` (brand-yellow-500)
- Complementary accent color for highlights and secondary actions
- Use for warnings, highlights, badges, and call-to-action accents
- HSL: `48 100% 68%`

**Color Scale (brand-yellow)**:
| Shade | Hex | Usage |
|-------|-----|-------|
| 50 | `#fffdf0` | Subtle backgrounds |
| 100 | `#fffae0` | Light highlights |
| 200 | `#fff5c2` | Badges, tags |
| 300 | `#fff0a3` | Warnings light |
| 400 | `#ffeb85` | Accent borders |
| 500 | `#ffde59` | **Secondary (DEFAULT)** |
| 600 | `#ffd033` | Hover states |
| 700 | `#ffc20d` | Active states |
| 800 | `#e6a600` | Dark accents |
| 900 | `#b38000` | Very dark accents |

**Background Cream**: `#fbfbee` (brand-cream-200)
- Neutral background color for light theme
- Use for page backgrounds, cards, and subtle containers

**Color Scale (brand-cream)**:
| Shade | Hex | Usage |
|-------|-----|-------|
| 50 | `#fefef9` | Lightest backgrounds |
| 100 | `#fdfdf4` | Card backgrounds |
| 200 | `#fbfbee` | **Page background (DEFAULT)** |
| 300 | `#f9f9e8` | Muted surfaces |
| 400 | `#f7f7e2` | Borders |
| 500 | `#f5f5dc` | Darker cream |

### Semantic Colors (CSS Variables)

These colors use HSL values in CSS variables for consistent theming:

**Light Mode**:
```css
--primary: 152 82% 24%;        /* Brand Green */
--secondary: 48 100% 68%;      /* Brand Yellow */
--background: 60 10% 98%;      /* Cream-tinted */
--success: 152 82% 24%;        /* Brand Green */
--warning: 38 92% 50%;
--destructive: 0 84.2% 60.2%;
--info: 217.2 91.2% 59.8%;
```

**Dark Mode**:
```css
--primary: 152 76% 42%;        /* Lighter Brand Green */
--secondary: 48 100% 68%;      /* Same Yellow */
--background: 222.2 84% 4.9%;  /* Dark background */
--success: 152 76% 42%;        /* Lighter Brand Green */
--warning: 38 92% 50%;
--destructive: 0 62.8% 50%;
--info: 217.2 91.2% 59.8%;
```

### Color System Philosophy

- **Accessibility First**: All color combinations meet WCAG AA standards
- **Dark Mode Support**: Every color has a dark mode variant
- **Semantic Usage**: Colors follow semantic naming (success, error, warning, info)
- **Consistent Opacity**: Use standardized opacity levels: `bg-primary/10`, `bg-primary/20`, `bg-primary/50`

## Typography Standards

### Font Families

| Font | CSS Variable | Tailwind Class | Usage |
|------|-------------|----------------|-------|
| **Inter** | `--font-inter` | `font-inter`, `font-sans` | Body text, UI elements |
| **Space Grotesk** | `--font-space-grotesk` | `font-heading`, `font-grotesk` | Headings, display text |

### Font Configuration (Tailwind)

```js
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  display: ['Space Grotesk', 'sans-serif'],
  inter: ['var(--font-inter)', 'Helvetica Neue', 'Arial', 'sans-serif'],
  grotesk: ['var(--font-space-grotesk)', 'Space Grotesk', 'sans-serif'],
  heading: ['var(--font-space-grotesk)', 'Space Grotesk', 'Segoe UI', 'Arial', 'sans-serif']
}
```

### Type Scale (Tailwind classes)

| Class | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `text-xs` | 12px | 16px | Small labels, captions |
| `text-sm` | 14px | 20px | Secondary text, metadata |
| `text-base` | 16px | 24px | Body text (default) |
| `text-lg` | 18px | 28px | Subheadings, emphasized text |
| `text-xl` | 20px | 28px | Card titles, section headers |
| `text-2xl` | 24px | 32px | Page subheadings |
| `text-3xl` | 30px | 36px | Page headings |
| `text-4xl` | 36px | 40px | Hero headings |
| `text-5xl` | 48px | 48px | Display headings |

### Custom Typography Classes

Use these predefined component classes from `globals.css`:

```css
.text-display     /* 4xl/5xl bold tracking-tight font-heading */
.text-heading     /* 2xl semibold tracking-tight font-heading */
.text-heading-lg  /* 3xl bold tracking-tight font-heading */
.text-subheading  /* lg semibold text-muted-foreground font-heading */
.text-body        /* base leading-7 normal font-inter */
.text-caption     /* sm text-muted-foreground normal font-inter */
```

### Font Weights

| Class | Weight | Usage |
|-------|--------|-------|
| `font-light` | 300 | De-emphasized text |
| `font-normal` | 400 | Body text (default) |
| `font-medium` | 500 | Emphasized text |
| `font-semibold` | 600 | Headings, buttons |
| `font-bold` | 700 | Strong emphasis |

## Component Styling Patterns

### Brand Buttons

```tsx
// Primary Button - Brand Green
<button className="btn-brand-primary">
  Primary Action
</button>

// Or manually:
<button className="
  bg-brand-green hover:bg-brand-green-600
  text-white font-medium
  px-6 py-3 rounded-lg
  transition-colors duration-200
  dark:bg-brand-green-400 dark:hover:bg-brand-green-500
">
  Primary Action
</button>

// Secondary Button - Brand Yellow
<button className="btn-brand-secondary">
  Secondary Action
</button>

// Outline Button
<button className="btn-brand-outline">
  Outline Action
</button>
```

### Brand Cards

```tsx
// Standard Card
<div className="card-brand">
  {/* Card content */}
</div>

// Or manually:
<div className="
  bg-white dark:bg-gray-800
  border border-gray-200 dark:border-gray-700
  rounded-lg shadow-sm
  p-6
  hover:shadow-md transition-shadow
">
  {/* Card content */}
</div>

// Highlight Card with Brand Gradient
<div className="card-brand-highlight">
  {/* Highlighted content */}
</div>
```

### Brand Gradients

```tsx
// Primary gradient
<div className="gradient-brand-primary text-white">
  {/* Content */}
</div>

// Secondary gradient
<div className="gradient-brand-secondary text-gray-900">
  {/* Content */}
</div>

// Hero gradient
<div className="gradient-brand-hero text-white">
  {/* Content */}
</div>
```

### Form Inputs

```tsx
<input className="
  w-full px-4 py-2
  bg-white dark:bg-gray-900
  border border-gray-300 dark:border-gray-600
  rounded-md
  focus:ring-2 focus:ring-brand-green focus:border-transparent
  dark:text-gray-100
" />
```

### Brand Badges

```tsx
// Green badge
<span className="badge-brand-green">Active</span>

// Yellow badge (highlight)
<span className="badge-brand-yellow">Featured</span>
```

### Status Indicators

```tsx
<div className="status-success">Success message</div>
<div className="status-warning">Warning message</div>
<div className="status-error">Error message</div>
<div className="status-info">Info message</div>
<div className="status-highlight">Highlighted message</div>
```

## Dark Mode Implementation

### Component-Level Dark Mode

```tsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
  <h1 className="text-brand-green dark:text-brand-green-400">Title</h1>
  <p className="text-gray-600 dark:text-gray-300">Body text</p>
</div>
```

### Using Theme Hook

```tsx
import { useTheme } from 'next-themes';

const { theme, setTheme } = useTheme();

// Toggle theme
<button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
  Toggle Theme
</button>
```

### Dark Mode Color Adjustments

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Background | `bg-white` | `bg-gray-800` or `bg-gray-900` |
| Text | `text-gray-900` | `text-gray-100` |
| Brand Green | `text-brand-green` | `text-brand-green-400` |
| Borders | `border-gray-200` | `border-gray-700` |
| Muted text | `text-gray-600` | `text-gray-300` |

## Hover & Animation Effects

### Hover Effects

```tsx
// Lift on hover
<div className="hover-lift">...</div>

// Glow on hover (green)
<div className="hover-glow">...</div>

// Glow on hover (yellow)
<div className="hover-glow-yellow">...</div>

// Scale on hover
<div className="hover-scale">...</div>
```

### Focus States

```tsx
// Brand green focus ring
<button className="focus-ring">...</button>

// Yellow focus ring
<button className="focus-ring-yellow">...</button>
```

### Animations

```tsx
// Fade in
<div className="animate-fadeIn">...</div>

// Slide up
<div className="animate-slideUp">...</div>

// Slide down
<div className="animate-slideDown">...</div>

// Scale in
<div className="animate-scaleIn">...</div>

// Subtle bounce
<div className="animate-bounceSubtle">...</div>

// Shimmer loading
<div className="loading-shimmer">...</div>
```

## Spacing System

Use Tailwind's default spacing scale based on 4px increments, plus custom values:

### Custom Spacing Values

```js
spacing: {
  '0.5': '0.125rem',   // 2px
  '4.5': '1.125rem',   // 18px
  '18': '4.5rem',      // 72px
  '88': '22rem',       // 352px
  '112': '28rem',      // 448px
  '128': '32rem',      // 512px
}
```

### Common Patterns

```tsx
// Card padding
<div className="p-4 md:p-6">...</div>

// Section spacing
<div className="space-y-6 md:space-y-8">...</div>

// Container
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">...</div>

// Button padding
<button className="px-4 py-2">Small</button>
<button className="px-6 py-3">Large</button>
```

## Responsive Design

### Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| `sm` | 640px | Small tablets, large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large desktops |

### Mobile-First Approach

```tsx
<div className="
  p-4 sm:p-6 md:p-8 lg:p-10
  text-sm sm:text-base md:text-lg
  grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3
">
  {/* Mobile-first responsive content */}
</div>
```

## Border Radius

Custom border radius values for consistent rounding:

```js
borderRadius: {
  none: '0',
  sm: '0.25rem',     // 4px
  DEFAULT: '0.5rem', // 8px
  md: '0.625rem',    // 10px
  lg: '0.75rem',     // 12px - DEFAULT for cards
  xl: '1rem',        // 16px
  '2xl': '1.25rem',  // 20px
  '3xl': '1.5rem',   // 24px
  full: '9999px',    // Fully rounded (circles, pills)
}
```

## Box Shadows

Custom shadow scale for depth:

```js
boxShadow: {
  xs: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  sm: '0 1px 3px 0 rgb(0 0 0 / 0.08)',
  DEFAULT: '0 2px 8px -2px rgb(0 0 0 / 0.1)',
  md: '0 4px 12px -2px rgb(0 0 0 / 0.12)',
  lg: '0 8px 24px -4px rgb(0 0 0 / 0.15)',
  xl: '0 12px 32px -8px rgb(0 0 0 / 0.18)',
  '2xl': '0 20px 40px -12px rgb(0 0 0 / 0.2)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
}
```

## Section Headers

```tsx
<div className="section-header">
  <Icon className="h-6 w-6 text-brand-green" />
  <h2 className="section-title">Section Title</h2>
</div>
<div className="section-divider" />
```

## Quality Checks

Before finalizing any component:

1. **Dark Mode Test**: Toggle theme and verify all elements are visible
2. **Responsive Test**: Check on mobile (375px), tablet (768px), and desktop (1440px)
3. **Contrast Test**: Verify text meets WCAG AA standards (4.5:1 for normal text)
4. **Touch Target Test**: Ensure interactive elements are at least 44x44px on mobile
5. **Hover/Focus States**: All interactive elements have clear hover and focus states

## Best Practices

### Color Usage
- Never hardcode hex colors in components
- Always use Tailwind color classes or CSS variables
- Ensure sufficient contrast for text readability
- Use opacity utilities for subtle variations: `bg-brand-green/10`

### Typography
- Maintain consistent heading hierarchy (h1 > h2 > h3)
- Use appropriate line-height for readability: `leading-relaxed` for body text
- Limit line length to 65-75 characters for optimal reading
- Use `font-heading` for all headings, `font-sans` for body

### Dark Mode
- Test every component in both light and dark themes
- Use lighter shades (400, 300) for brand colors in dark mode
- Increase contrast for text in dark mode
- Use subtle borders instead of heavy shadows in dark mode

### Performance
- Use CSS transitions for smooth interactions
- Prefer Tailwind utilities over custom CSS
- Minimize custom CSS and leverage Tailwind's tree-shaking

## Troubleshooting

**Dark mode not working?**
- Ensure ThemeProvider wraps your app
- Check `next-themes` is installed: `npm install next-themes`
- Verify `darkMode: ["class"]` in tailwind.config.ts

**Colors not showing correctly?**
- Confirm Tailwind config is properly imported
- Run `npm run build` to regenerate Tailwind CSS
- Check for CSS specificity conflicts

**Custom classes not applying?**
- Ensure `globals.css` is imported in your root layout
- Check that the class is defined in `@layer components`

**Font not loading?**
- Verify font imports in Next.js layout (next/font)
- Check CSS variable definitions in globals.css
- Clear browser cache and reload

## File References

- **Tailwind Config**: `tailwind.config.ts` - Complete configuration with brand colors
- **Global Styles**: `styles/globals.css` - CSS variables and component classes
- **Theme Provider**: `components/providers/theme-provider.tsx` - Dark mode support
