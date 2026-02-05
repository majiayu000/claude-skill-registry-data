---
name: tailwind-shadcn-ui-setup
description: This skill should be used when setting up, configuring, or initializing Tailwind CSS (v3 or v4) and shadcn/ui for Next.js 16 App Router projects. Configure dark mode, design tokens, base layout with header/sidebar, accessibility defaults, and generate example components. Includes comprehensive setup automation, theme customization, and production-ready patterns. Use when the user requests "setup Tailwind", "configure shadcn/ui", "add dark mode", "initialize design system", or "setup UI framework" for Next.js projects.
---

# Tailwind + shadcn/ui Setup for Next.js 16

## Overview

Configure a production-ready Tailwind CSS (v3/v4) + shadcn/ui setup for Next.js 16 App Router projects. This skill automates dependency installation, configuration, component generation, and provides:

- **Tailwind CSS v4-ready configuration** (v3 with forward-compatible patterns)
- **shadcn/ui components** (Radix UI-based, fully accessible)
- **Dark mode** with `next-themes` (class strategy)
- **Base application layout** (header, optional sidebar, responsive)
- **Design token system** (CSS variables for easy theming)
- **Accessibility defaults** (WCAG 2.1 AA compliant)
- **Example pages** (forms, dialogs, theme showcase)

## Prerequisites

Before running this skill, verify:

1. **Next.js 16 project exists** with App Router (`app/` directory)
2. **Package manager**: npm (script uses `npm install`)
3. **Project structure**: Valid `package.json` at project root
4. **TypeScript**: Recommended (all templates use `.tsx`/`.ts`)

To verify:

```bash
# Check Next.js version
cat package.json | grep "\"next\":"

# Confirm app/ directory exists
ls -la app/
```

## Setup Workflow

### Step 1: Gather User Requirements

Use `AskUserQuestion` tool to collect configuration preferences:

1. **Enable dark mode?** (default: yes)
   - Installs `next-themes`, adds `ThemeProvider`, creates mode toggle
2. **Theme preset** (zinc | slate | neutral, default: zinc)
   - Determines base color palette in CSS variables
3. **Include sidebar layout?** (default: yes)
   - Adds responsive sidebar navigation using `Sheet` component
4. **Include example pages?** (default: yes)
   - Generates example pages for forms, dialogs, theme showcase

### Step 2: Run Automation Script

Execute the Python setup script to install dependencies and initialize shadcn/ui:

```bash
cd /path/to/nextjs-project
python /path/to/skill/scripts/setup_tailwind_shadcn.py
```

The script will:
- Detect existing Tailwind/shadcn installations
- Install required npm packages (non-interactive)
- Create `components.json` for shadcn/ui
- Add baseline shadcn components (button, card, input, label, dialog, separator)
- Create `lib/utils.ts` with `cn()` helper

### Step 3: Copy Configuration Files

Copy and process template files from `assets/` directory:

1. **Tailwind Configuration**
   ```bash
   # Copy and create
   cp assets/tailwind.config.ts.template project/tailwind.config.ts
   cp assets/postcss.config.js.template project/postcss.config.js
   ```

2. **Global Styles**
   ```bash
   # Copy and replace {{THEME_PRESET}} with user's choice
   cp assets/globals.css.template project/app/globals.css
   # Replace: {{THEME_PRESET}} → zinc | slate | neutral
   ```

3. **Utility Functions**
   ```bash
   cp assets/lib/utils.ts project/lib/utils.ts
   ```

### Step 4: Add Core Components

Copy theme and layout components from `assets/components/`:

1. **Theme Provider** (if dark mode enabled)
   ```bash
   cp assets/components/theme-provider.tsx project/components/theme-provider.tsx
   cp assets/components/mode-toggle.tsx project/components/mode-toggle.tsx
   ```

2. **App Shell** (if sidebar layout enabled)
   ```bash
   cp assets/components/app-shell.tsx project/components/app-shell.tsx
   ```

### Step 5: Update App Layout

Update or create `app/layout.tsx`:

```bash
# If layout.tsx exists, carefully merge changes
# If not, copy template
cp assets/app/layout.tsx.template project/app/layout.tsx
```

**Key additions:**
- Import `globals.css`
- Wrap with `ThemeProvider` (if dark mode enabled)
- Add skip link for accessibility
- Include `<Toaster />` from Sonner for notifications

**Merge strategy if layout exists:**
- Add missing imports at top
- Wrap existing content with `ThemeProvider`
- Add skip link before main content
- Add `Toaster` before closing `body` tag
- Ensure `suppressHydrationWarning` on `<html>` tag

### Step 6: Generate Example Pages (Optional)

If user requested examples, copy example pages:

```bash
# Copy home page
cp assets/app/page.tsx.template project/app/page.tsx

# Copy examples directory structure
cp -r assets/app/examples/ project/app/examples/
```

**Example pages include:**
- **Homepage** (`app/page.tsx`): Hero, features grid, CTA
- **Forms** (`app/examples/forms/page.tsx`): Contact form, validation patterns
- **Dialogs** (`app/examples/dialogs/page.tsx`): Modal examples, A11y notes
- **Theme** (`app/examples/theme/page.tsx`): Color tokens, customization guide

### Step 7: Add Additional shadcn Components

Install additional components as needed:

```bash
# Common components for examples
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add sheet
npx shadcn-ui@latest add separator

# Optional: Form components
npx shadcn-ui@latest add form
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add select
```

Consult `references/shadcn-component-list.md` for full component catalog.

### Step 8: Verify Installation

Run checks to ensure setup is complete:

```bash
# Check for TypeScript errors
npx tsc --noEmit

# Start dev server
npm run dev

# Open browser to http://localhost:3000
```

**Visual verification:**
- Page loads without errors
- Dark mode toggle works (if enabled)
- Colors match theme preset
- Example pages render correctly (if included)
- No accessibility warnings in console

### Step 9: Document Changes

Add a "Design System & UI" section to project `README.md`:

````markdown
## Design System & UI

This project uses Tailwind CSS and shadcn/ui for styling and components.

### Customizing Colors

Edit CSS variables in `app/globals.css`:

```css
:root {
  --primary: 270 80% 45%;  /* Your brand color (HSL) */
  --radius: 0.75rem;        /* Border radius */
}
```

Test contrast ratios: https://webaim.org/resources/contrastchecker/

### Adding Components

```bash
# Add any shadcn/ui component
npx shadcn-ui@latest add [component-name]

# Example: Add a combobox
npx shadcn-ui@latest add combobox
```

Available components: https://ui.shadcn.com/docs/components

### Dark Mode

Toggle theme programmatically:

```tsx
import { useTheme } from 'next-themes'

export function Example() {
  const { theme, setTheme } = useTheme()
  // theme: 'light' | 'dark' | 'system'
  // setTheme('dark')
}
```

### Accessibility

- All components meet WCAG 2.1 Level AA
- Focus indicators on all interactive elements
- Keyboard navigation supported
- Screen reader compatible

See `references/accessibility-checklist.md` for full guidelines.
````

## Configuration Options

### Theme Presets

**Zinc (default)** - Cool, neutral gray tones:
```css
--primary: 240 5.9% 10%;
--muted: 240 4.8% 95.9%;
```

**Slate** - Slightly cooler, tech-focused:
```css
--primary: 222.2 47.4% 11.2%;
--muted: 210 40% 96.1%;
```

**Neutral** - True neutral grays:
```css
--primary: 0 0% 9%;
--muted: 0 0% 96.1%;
```

Customize further by editing `app/globals.css` `:root` and `.dark` blocks.

### Tailwind v4 Considerations

Check Tailwind version before setup:

```bash
npm view tailwindcss version
```

**If v4.0.0+ is available:**
- Use v4 configuration format (`@theme` directive)
- Consult `references/tailwind-v4-migration.md`

**If v4 not available (current default):**
- Use v3 with forward-compatible CSS variables
- Add comments in generated files: `// TODO: Upgrade to Tailwind v4 when stable`

### Sidebar Layout Options

If `sidebarLayout = true`:
- Uses `AppShell` component with responsive sidebar
- Mobile: Hamburger menu → `Sheet` (slide-over)
- Desktop: Fixed sidebar with navigation items

If `sidebarLayout = false`:
- Simple header + content layout
- Header contains site title + actions (mode toggle)

Users can customize navigation in layout files by passing `navigation` prop:

```tsx
<AppShell
  navigation={[
    { title: 'Home', href: '/', icon: Home },
    { title: 'About', href: '/about', icon: Info },
  ]}
  siteTitle="My App"
>
  {children}
</AppShell>
```

## Troubleshooting

### Issue: npm install fails

**Cause**: Network issues, registry timeout, or package conflicts

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Retry with verbose logging
npm install --verbose

# Or use specific registry
npm install --registry https://registry.npmjs.org/
```

### Issue: TypeScript errors in components

**Cause**: Missing type definitions or tsconfig issues

**Solution**:
```bash
# Install missing types
npm install --save-dev @types/react @types/react-dom @types/node

# Check tsconfig.json paths
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### Issue: Dark mode not working

**Cause**: ThemeProvider not wrapping content, or `suppressHydrationWarning` missing

**Solution**:
1. Verify `<html suppressHydrationWarning>` in layout
2. Ensure `ThemeProvider` wraps `{children}`
3. Check `tailwind.config.ts` has `darkMode: 'class'`

### Issue: shadcn components not found

**Cause**: `components.json` misconfigured or components not installed

**Solution**:
```bash
# Reinitialize shadcn/ui
npx shadcn-ui@latest init

# Re-add components
npx shadcn-ui@latest add button card input
```

### Issue: Focus styles not visible

**Cause**: Global CSS focus styles not applied

**Solution**:
- Verify `app/globals.css` includes focus styles layer
- Check `*:focus-visible` rule is present
- Ensure `--ring` CSS variable is defined

## Resources

This skill bundles comprehensive resources for reference:

### References (Loaded as Needed)

- **`tailwind-v4-migration.md`**: Tailwind v3 vs v4 differences, migration guide
- **`shadcn-component-list.md`**: Complete shadcn/ui component catalog with usage examples
- **accessibility-checklist.md**: WCAG 2.1 AA compliance checklist, best practices
- **`theme-tokens.md`**: Design token system, color customization guide

To read a reference:
```bash
# From skill directory
cat references/theme-tokens.md
```

### Scripts (Executable)

- **`setup_tailwind_shadcn.py`**: Main automation script for dependency installation and configuration

Execute directly:
```bash
python scripts/setup_tailwind_shadcn.py
```

### Assets (Templates for Output)

- **Config templates**: `tailwind.config.ts.template`, `postcss.config.js.template`, `globals.css.template`
- **Component templates**: `theme-provider.tsx`, `mode-toggle.tsx`, `app-shell.tsx`
- **Utility templates**: `lib/utils.ts`
- **Page templates**: `app/layout.tsx.template`, `app/page.tsx.template`
- **Example pages**: `app/examples/forms/`, `app/examples/dialogs/`, `app/examples/theme/`

Copy and customize as needed for the target project.

## Best Practices

### 1. Always Test Both Themes

After setup, manually toggle dark mode and verify:
- Color contrast ratios meet WCAG standards
- All text remains readable
- Focus indicators are visible
- Components render correctly

### 2. Use Semantic Tokens

```tsx
[OK] Good (semantic)
<div className="bg-primary text-primary-foreground">

[ERROR] Bad (hard-coded)
<div className="bg-blue-600 text-white">
```

### 3. Maintain Type Safety

Use TypeScript for all components:
```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline'
}
```

### 4. Keep Accessibility in Mind

- Always pair labels with inputs
- Provide `aria-label` for icon-only buttons
- Test keyboard navigation
- Use semantic HTML

### 5. Document Customizations

When customizing tokens or components, document changes in project README or inline comments.

## Post-Setup Tasks

After running this skill, recommend users:

1. **Customize brand colors**
   - Edit `--primary` in `app/globals.css`
   - Test contrast ratios

2. **Add more components**
   - Run `npx shadcn-ui add [component]` as needed
   - See `references/shadcn-component-list.md` for options

3. **Configure responsive breakpoints**
   - Adjust Tailwind `screens` in `tailwind.config.ts` if needed

4. **Set up linting**
   - Install `eslint-plugin-jsx-a11y` for accessibility linting
   - Add Prettier + Tailwind plugin for formatting

5. **Test production build**
   ```bash
   npm run build
   npm start
   ```

## Summary

This skill provides a complete, production-ready Tailwind CSS + shadcn/ui setup for Next.js 16 App Router projects. It handles:

[OK] Dependency installation (Tailwind, shadcn/ui, next-themes)
[OK] Configuration (Tailwind config, PostCSS, global CSS)
[OK] Dark mode setup (ThemeProvider, toggle component)
[OK] Base layout (responsive header, optional sidebar)
[OK] Design tokens (semantic CSS variables)
[OK] Accessibility (WCAG 2.1 AA, keyboard nav, screen readers)
[OK] Example pages (forms, dialogs, theme showcase)
[OK] Documentation (README updates, customization guides)

The setup is forward-compatible with Tailwind v4 and follows official Anthropic skill best practices.
