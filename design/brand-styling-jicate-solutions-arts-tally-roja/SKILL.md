---
name: brand-styling
description: Comprehensive brand styling system for standardizing design across all projects. Implements brand colors, typography, spacing, responsive design, and dark mode using Tailwind CSS and Next.js themes. Use when creating new projects, implementing UI components, or ensuring design consistency across web applications. (project)
---

# Brand Styling Skill

## Purpose

This skill provides a comprehensive, standardized brand styling system for all web development projects. It ensures visual consistency across applications by defining brand colors, typography scales, spacing systems, responsive breakpoints, and complete dark mode implementation using Tailwind CSS and Next.js themes.

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

**Primary Green**: `#0b6d41`
- Main brand color for primary actions, headers, and key UI elements
- Use for buttons, links, active states, and brand accents

**Secondary Yellow**: `#ffde59`
- Complementary accent color for highlights and secondary actions
- Use for warnings, highlights, badges, and call-to-action accents

**Background Cream**: `#fbfbee`
- Neutral background color for light theme
- Use for page backgrounds, cards, and subtle containers

### Color System Philosophy

- **Accessibility First**: All color combinations meet WCAG AA standards
- **Dark Mode Support**: Every color has a dark mode variant
- **Semantic Usage**: Colors follow semantic naming (success, error, warning, info)
- **Consistent Opacity**: Use standardized opacity levels (10%, 20%, 50%, 80%)

## How to Use This Skill

### 1. Initial Project Setup

When starting a new project or migrating an existing one:

1. **Copy Tailwind Configuration**
   - Use `assets/tailwind.config.js` as the base Tailwind configuration
   - Includes all brand colors, spacing, typography, and breakpoints
   - Extended with custom utilities for dark mode

2. **Install Theme Provider**
   - Copy `assets/theme-provider.tsx` to `components/providers/`
   - Wrap the application with ThemeProvider for dark mode support
   - Provides `useTheme()` hook for theme management

3. **Apply Global Styles**
   - Copy `assets/globals.css` to your styles directory
   - Includes CSS variables for light/dark themes
   - Imports Google Fonts (Inter for UI, Poppins for headings)

4. **Reference Brand Guidelines**
   - Review `references/brand-guidelines.md` for complete design system
   - Follow typography scales, spacing rules, and color usage
   - Use component examples as templates

### 2. Implementing Dark Mode

Follow the patterns in `references/dark-mode-patterns.md`:

**Component-Level Dark Mode**:
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
  <h1 className="text-primary dark:text-primary-light">Title</h1>
</div>
```

**Using Theme Hook**:
```tsx
import { useTheme } from 'next-themes';

const { theme, setTheme } = useTheme();
```

**CSS Variables Approach**:
```css
.card {
  background-color: var(--color-surface);
  color: var(--color-text-primary);
}
```

### 3. Responsive Design Implementation

Use mobile-first approach with Tailwind breakpoints:

```tsx
<div className="
  p-4 sm:p-6 md:p-8 lg:p-10
  text-sm sm:text-base md:text-lg
  grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3
">
  {/* Mobile-first responsive content */}
</div>
```

**Standard Breakpoints**:
- `sm`: 640px (Small tablets, large phones)
- `md`: 768px (Tablets)
- `lg`: 1024px (Laptops)
- `xl`: 1280px (Desktops)
- `2xl`: 1536px (Large desktops)

### 4. Typography Standards

**Font Families**:
- **Body Text**: Inter (Google Font)
- **Headings**: Poppins (Google Font)
- **Monospace**: Fira Code

**Type Scale** (Tailwind classes):
- `text-xs`: 12px - Small labels, captions
- `text-sm`: 14px - Secondary text, metadata
- `text-base`: 16px - Body text (default)
- `text-lg`: 18px - Subheadings, emphasized text
- `text-xl`: 20px - Card titles, section headers
- `text-2xl`: 24px - Page subheadings
- `text-3xl`: 30px - Page headings
- `text-4xl`: 36px - Hero headings
- `text-5xl`: 48px - Display headings

**Font Weights**:
- `font-light`: 300
- `font-normal`: 400 (body default)
- `font-medium`: 500 (emphasized text)
- `font-semibold`: 600 (headings)
- `font-bold`: 700 (strong emphasis)

### 5. Spacing System

Use Tailwind's default spacing scale based on 4px increments:

**Common Patterns**:
- Card padding: `p-4 md:p-6`
- Section spacing: `space-y-6 md:space-y-8`
- Container margin: `mx-auto max-w-7xl px-4 sm:px-6 lg:px-8`
- Button padding: `px-4 py-2` or `px-6 py-3` for larger buttons

### 6. Component Styling Patterns

**Buttons**:
```tsx
// Primary button
<button className="
  bg-primary hover:bg-primary-dark
  text-white font-medium
  px-6 py-3 rounded-lg
  transition-colors duration-200
  dark:bg-primary-light dark:hover:bg-primary
">
  Primary Action
</button>

// Secondary button
<button className="
  bg-secondary hover:bg-secondary-dark
  text-gray-900 font-medium
  px-6 py-3 rounded-lg
  transition-colors duration-200
">
  Secondary Action
</button>
```

**Cards**:
```tsx
<div className="
  bg-white dark:bg-gray-800
  border border-gray-200 dark:border-gray-700
  rounded-lg shadow-sm
  p-6
  hover:shadow-md transition-shadow
">
  {/* Card content */}
</div>
```

**Forms**:
```tsx
<input className="
  w-full px-4 py-2
  bg-white dark:bg-gray-900
  border border-gray-300 dark:border-gray-600
  rounded-md
  focus:ring-2 focus:ring-primary focus:border-transparent
  dark:text-gray-100
" />
```

### 7. Generating Color Palettes

Use `scripts/generate-palette.py` to generate color variations:

```bash
python scripts/generate-palette.py --color "#0b6d41" --output src/styles/colors.js
```

This generates light/dark variants, opacity variations, and accessibility-tested combinations.

### 8. Quality Checks

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
- Use opacity utilities for subtle variations: `bg-primary/10`

### Typography
- Maintain consistent heading hierarchy (h1 > h2 > h3)
- Use appropriate line-height for readability: `leading-relaxed` for body text
- Limit line length to 65-75 characters for optimal reading

### Spacing
- Use consistent spacing between sections (multiples of 4px)
- Maintain proper whitespace for visual breathing room
- Group related elements with tighter spacing

### Dark Mode
- Test every component in both light and dark themes
- Reduce brightness of backgrounds in dark mode
- Increase contrast for text in dark mode
- Use subtle borders instead of heavy shadows

### Responsive Design
- Design for mobile first, then enhance for larger screens
- Use fluid typography: `text-base sm:text-lg lg:text-xl`
- Stack layouts vertically on mobile, horizontally on desktop
- Touch targets should be larger on mobile devices

### Performance
- Use CSS transitions for smooth interactions
- Prefer Tailwind utilities over custom CSS
- Minimize custom CSS and leverage Tailwind's tree-shaking
- Load Google Fonts with `font-display: swap`

## Troubleshooting

**Dark mode not working?**
- Ensure ThemeProvider wraps your app
- Check `next-themes` is installed: `npm install next-themes`
- Verify `darkMode: 'class'` in tailwind.config.js

**Colors not showing correctly?**
- Confirm Tailwind config is properly imported
- Run `npm run build` to regenerate Tailwind CSS
- Check for CSS specificity conflicts

**Responsive design breaking?**
- Use Tailwind's mobile-first approach
- Verify breakpoints are applied in correct order
- Test on actual devices, not just browser resize

**Font not loading?**
- Check Google Fonts import in globals.css
- Verify font-family in Tailwind config
- Clear browser cache and reload

## References

- **Brand Guidelines**: `references/brand-guidelines.md` - Complete brand design system
- **Dark Mode Patterns**: `references/dark-mode-patterns.md` - Dark mode implementation examples
- **Component Library**: Examples of common component patterns
- **Accessibility Guide**: WCAG compliance standards and testing

## Assets

- **tailwind.config.js**: Complete Tailwind configuration with brand colors
- **theme-provider.tsx**: Next.js theme provider for dark mode
- **globals.css**: Global styles with CSS variables and font imports

## Scripts

- **generate-palette.py**: Generate color variations and accessibility testing
