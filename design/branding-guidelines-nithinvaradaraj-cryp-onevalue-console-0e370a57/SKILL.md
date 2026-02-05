---
name: branding-guidelines
description: Apply corporate branding standards including blue color palette, dark/light theme support, and shadcn UI component library. Use when implementing UI components, styling elements, or ensuring brand consistency.
allowed-tools: Read, Edit, Grep, Glob
---

# OneValue Corporate Branding Guidelines

This skill provides comprehensive branding guidelines including corporate blue color palette, typography, theme system, and shadcn UI component usage.

## Corporate Color Palette

### Primary Blue (Corporate)
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Primary | `#0066CC` | rgb(0, 102, 204) | Main brand color, primary buttons |
| Primary Light | `#4D94FF` | rgb(77, 148, 255) | Hover states, highlights |
| Primary Dark | `#0052A3` | rgb(0, 82, 163) | Pressed states, dark accents |
| Primary Darker | `#003D7A` | rgb(0, 61, 122) | Dark mode primary |

### Extended Blue Scale (Tailwind-compatible)
```javascript
primary: {
  50: '#F0F7FF',
  100: '#E0EFFF',
  200: '#C7DFFF',
  300: '#A4CCFF',
  400: '#7EB3FF',
  500: '#4D94FF',
  600: '#0066CC',  // Main brand color
  700: '#0052A3',
  800: '#003D7A',
  900: '#002B57',
  950: '#001A3D',
}
```

### Semantic Colors
| Purpose | Light Mode | Dark Mode |
|---------|------------|-----------|
| Success | `#10B981` | `#34D399` |
| Warning | `#F59E0B` | `#FBBF24` |
| Error | `#EF4444` | `#F87171` |
| Info | `#3B82F6` | `#60A5FA` |

### Neutral Grays
```javascript
gray: {
  50: '#F9FAFB',
  100: '#F3F4F6',
  200: '#E5E7EB',
  300: '#D1D5DB',
  400: '#9CA3AF',
  500: '#6B7280',
  600: '#4B5563',
  700: '#374151',
  800: '#1F2937',
  900: '#111827',
  950: '#030712',
}
```

## Theme Configuration

### Light Theme
```css
:root {
  --background: #FFFFFF;
  --foreground: #111827;
  --card: #FFFFFF;
  --card-foreground: #111827;
  --primary: #0066CC;
  --primary-foreground: #FFFFFF;
  --secondary: #F3F4F6;
  --secondary-foreground: #111827;
  --muted: #F3F4F6;
  --muted-foreground: #6B7280;
  --accent: #F3F4F6;
  --accent-foreground: #111827;
  --destructive: #EF4444;
  --border: #E5E7EB;
  --ring: #0066CC;
  --radius: 12px;
}
```

### Dark Theme
```css
[data-theme="dark"], .dark {
  --background: #111827;
  --foreground: #F3F4F6;
  --card: #1F2937;
  --card-foreground: #F3F4F6;
  --primary: #4D94FF;
  --primary-foreground: #111827;
  --secondary: #374151;
  --secondary-foreground: #F3F4F6;
  --muted: #374151;
  --muted-foreground: #9CA3AF;
  --accent: #374151;
  --accent-foreground: #F3F4F6;
  --destructive: #F87171;
  --border: #374151;
  --ring: #4D94FF;
}
```

## Shadcn UI Components

### Required Components
Install these shadcn components for the design system:

```bash
npx shadcn@latest add button card badge tabs dialog toast select input textarea avatar dropdown-menu separator skeleton
```

### Button Variants
```tsx
// Primary action
<Button className="bg-primary-600 hover:bg-primary-700">Primary</Button>

// Secondary action
<Button variant="outline">Secondary</Button>

// Ghost/subtle
<Button variant="ghost">Subtle</Button>

// Destructive
<Button variant="destructive">Delete</Button>
```

### Card Usage
```tsx
<Card className="backdrop-blur-lg bg-white/70 dark:bg-gray-900/70 border-white/20">
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
</Card>
```

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
```

### Scale
| Name | Size | Weight | Line Height |
|------|------|--------|-------------|
| Display | 36px | 700 | 1.2 |
| H1 | 30px | 700 | 1.3 |
| H2 | 24px | 600 | 1.35 |
| H3 | 20px | 600 | 1.4 |
| Body | 16px | 400 | 1.5 |
| Small | 14px | 400 | 1.5 |
| Caption | 12px | 400 | 1.4 |

## Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing |
| sm | 8px | Compact elements |
| md | 16px | Default spacing |
| lg | 24px | Section spacing |
| xl | 32px | Large gaps |
| 2xl | 48px | Page sections |

## Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| sm | 6px | Small elements, badges |
| md | 8px | Buttons, inputs |
| lg | 12px | Cards, dialogs |
| xl | 16px | Large panels |
| full | 9999px | Pills, avatars |

## Shadows (Elevation)
```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

## Glass Morphism
```css
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.dark .glass {
  background: rgba(17, 24, 39, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

## Animation Standards
```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-normal: 200ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
```

## Accessibility Requirements
- Minimum contrast ratio: 4.5:1 for text
- Focus rings: 2px solid primary color
- Touch targets: minimum 44x44px
- Reduced motion: respect `prefers-reduced-motion`
