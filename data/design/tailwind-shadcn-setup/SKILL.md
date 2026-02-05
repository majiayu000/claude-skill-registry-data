---
name: tailwind-shadcn-setup
description: Setup Tailwind CSS and shadcn/ui component library for Next.js projects. Use when configuring Tailwind CSS, installing shadcn/ui, setting up design tokens, configuring dark mode, initializing component library, or when user mentions Tailwind setup, shadcn/ui installation, component system, design system, or theming.
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# tailwind-shadcn-setup

## Instructions

This skill provides complete setup and configuration for Tailwind CSS and shadcn/ui in Next.js projects. It covers installation, configuration, theming, dark mode, and component integration following modern best practices.

### 1. Tailwind CSS Installation

Install and configure Tailwind CSS for Next.js:

```bash
# Run automated installation script
bash ./skills/tailwind-shadcn-setup/scripts/install-tailwind.sh

# Or manually install dependencies
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**What This Does:**
- Installs Tailwind CSS, PostCSS, and Autoprefixer
- Creates `tailwind.config.ts` and `postcss.config.mjs`
- Configures content paths for Next.js
- Sets up CSS imports in global styles

### 2. shadcn/ui Initialization

Initialize shadcn/ui component library:

```bash
# Run automated shadcn/ui setup
bash ./skills/tailwind-shadcn-setup/scripts/init-shadcn.sh

# Or use shadcn CLI directly
npx shadcn@latest init
```

**Configuration Prompts:**
- TypeScript: Yes (recommended)
- Style: Default or New York
- Base color: Slate, Zinc, Neutral, Stone, or Gray
- CSS variables: Yes (recommended for theming)
- Tailwind config: tailwind.config.ts
- Components location: @/components
- Utils location: @/lib/utils

**What Gets Created:**
- `components.json` - shadcn/ui configuration
- `lib/utils.ts` - Utility functions (cn helper)
- `app/globals.css` - CSS variables and theme definitions
- Base component structure

### 3. Design Tokens & Theme Configuration

Configure design tokens using CSS variables:

```bash
# Apply comprehensive theme configuration
bash ./skills/tailwind-shadcn-setup/scripts/setup-theme.sh
```

**Theme Configuration Includes:**
- Primary, secondary, accent colors
- Background and foreground pairs
- Border, input, ring colors
- Muted, destructive, card, popover colors
- Chart colors (chart-1 through chart-5)
- Sidebar colors for navigation components

**Using CSS Variables Template:**
```typescript
// Copy and customize base theme
cp ./skills/tailwind-shadcn-setup/templates/globals.css app/globals.css
```

**Color System:**
- Uses OKLCH color space for better perceptual uniformity
- Separate light and dark mode definitions
- Foreground colors automatically calculated for accessibility

### 4. Dark Mode Configuration

Set up dark mode with class-based or system-based detection:

```bash
# Configure dark mode
bash ./skills/tailwind-shadcn-setup/scripts/setup-dark-mode.sh
```

**Dark Mode Strategies:**
1. **Class-based** (Recommended): Uses `.dark` class for manual toggle
2. **Media-based**: Respects system preference automatically
3. **Hybrid**: Manual toggle with system default

**Provider Setup:**
```typescript
// Copy theme provider template
cp ./skills/tailwind-shadcn-setup/templates/theme-provider.tsx components/theme-provider.tsx
```

**Theme Toggle Component:**
```bash
# Add theme toggle button
npx shadcn@latest add dropdown-menu
cp ./skills/tailwind-shadcn-setup/examples/theme-toggle.tsx components/theme-toggle.tsx
```

### 5. Adding Components

Install shadcn/ui components as needed:

```bash
# Add individual components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add form

# Add multiple components at once
npx shadcn@latest add button card input form dialog sheet
```

**Common Component Sets:**
- **Forms**: button, input, label, select, textarea, checkbox, radio-group, form
- **Layout**: card, separator, aspect-ratio, scroll-area
- **Navigation**: navigation-menu, menubar, dropdown-menu, tabs
- **Feedback**: toast, alert, alert-dialog, dialog
- **Data**: table, data-table, pagination

### 6. Custom Component Configuration

Create custom components using shadcn/ui primitives:

```typescript
// Example: Custom button variant
import { Button } from "@/components/ui/button"

<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
```

**Extending Components:**
```typescript
// Add custom variants in tailwind.config.ts
// Components automatically use CSS variables for theming
```

## Examples

### Example 1: Complete Setup for New Next.js Project

```bash
# 1. Install Tailwind CSS
bash ./skills/tailwind-shadcn-setup/scripts/install-tailwind.sh

# 2. Initialize shadcn/ui
bash ./skills/tailwind-shadcn-setup/scripts/init-shadcn.sh

# 3. Setup theme and dark mode
bash ./skills/tailwind-shadcn-setup/scripts/setup-dark-mode.sh

# 4. Add common components
npx shadcn@latest add button card input form dialog toast

# 5. Copy theme toggle component
cp ./skills/tailwind-shadcn-setup/examples/theme-toggle.tsx components/theme-toggle.tsx
```

**Result:** Fully configured Next.js project with Tailwind, shadcn/ui, dark mode, and essential components

### Example 2: Custom Theme with Brand Colors

```bash
# 1. Run theme setup
bash ./skills/tailwind-shadcn-setup/scripts/setup-theme.sh

# 2. Edit CSS variables for brand colors
# Modify app/globals.css to use your brand colors
# Example: Primary color = oklch(0.5 0.2 250) for brand blue

# 3. Test theme with sample components
cp ./skills/tailwind-shadcn-setup/examples/theme-showcase.tsx app/page.tsx
```

**Result:** Custom-branded design system using your colors while maintaining shadcn/ui components

### Example 3: Form-Heavy Application Setup

```bash
# 1. Complete base setup
bash ./skills/tailwind-shadcn-setup/scripts/install-tailwind.sh
bash ./skills/tailwind-shadcn-setup/scripts/init-shadcn.sh

# 2. Add all form-related components
npx shadcn@latest add form input label select textarea checkbox radio-group switch slider

# 3. Install react-hook-form and zod (form dependencies)
npm install react-hook-form zod @hookform/resolvers

# 4. Copy form example template
cp ./skills/tailwind-shadcn-setup/examples/sample-form.tsx components/forms/sample-form.tsx
```

**Result:** Complete form setup with validation, accessibility, and consistent styling

## Requirements

**Dependencies:**
- Next.js 13.4+ (App Router or Pages Router)
- React 18+
- Node.js 18.17+ or 20+
- TypeScript (recommended)

**Package Manager:**
- npm, pnpm, yarn, or bun (any modern package manager)

**Project Structure:**
- Next.js project initialized with `create-next-app`
- `app/` directory (App Router) or `pages/` directory (Pages Router)
- `components/` directory for UI components
- `lib/` directory for utilities

**For Dark Mode:**
- `next-themes` package (automatically installed by shadcn CLI)
- Client-side provider component

## Configuration Files Created

**tailwind.config.ts:**
```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      // CSS variable-based theming
    },
  },
  plugins: [require("tailwindcss-animate")],
}
export default config
```

**components.json:**
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

**app/globals.css:**
- `:root` variables for light mode
- `.dark` variables for dark mode
- Base layer imports
- Tailwind directives

## Best Practices

**CSS Variables Over Utility Classes:**
- Use `cssVariables: true` in components.json
- Allows runtime theme switching
- Better for multi-theme applications
- Easier to customize without recompiling

**Component Organization:**
```
components/
├── ui/              # shadcn/ui components (auto-generated)
│   ├── button.tsx
│   ├── card.tsx
│   └── input.tsx
├── theme-provider.tsx
├── theme-toggle.tsx
└── [custom-components]/
```

**Theming Strategy:**
1. Start with a base color (Slate, Zinc, etc.)
2. Customize CSS variables for brand colors
3. Use OKLCH color space for consistency
4. Test in both light and dark modes
5. Ensure foreground colors meet WCAG contrast ratios

**Performance:**
- Only install components you actually use
- shadcn/ui copies components to your codebase (not a dependency)
- Tree-shaking automatically removes unused Tailwind classes
- PostCSS processes CSS at build time (zero runtime cost)

**Dark Mode UX:**
- Persist user preference in localStorage
- Respect system preference as default
- Provide manual toggle for user control
- Avoid flash of unstyled content (FOUC) with theme script

## Integration with Next.js Features

**Server Components:**
- shadcn/ui components work with Server Components
- Theme provider must be Client Component (`'use client'`)
- Form components require Client Components for interactivity

**Route Handlers:**
- Use consistent styling across API-driven UIs
- Theme variables accessible in CSS for generated content

**Metadata API:**
- Configure theme-color meta tag based on dark mode
- Integrate with app manifest for PWA support

---

**Plugin:** nextjs-frontend
**Version:** 1.0.0
**Category:** UI & Styling
**Skill Type:** Setup & Configuration
