---
name: shadcn-init
description: Setup shadcn/ui in React projects (Next.js, Vite, Astro). Use when initializing shadcn/ui, setting up Tailwind CSS v4, configuring path aliases, or when user mentions "setup shadcn", "install shadcn", "shadcn init", or starting a new shadcn project. NOT for adding components or customization.
---

# shadcn/ui Initialization

This skill guides you through setting up shadcn/ui for the first time in React projects.

## What shadcn/ui Is

shadcn/ui is a collection of unstyled, accessible React components built on Radix UI and styled with Tailwind CSS. Components are copied directly into your project, giving you full ownership and control.

## When to Use This Skill

Use this skill when:
- Setting up shadcn/ui for the first time
- User mentions "setup shadcn", "install shadcn", or "shadcn init"
- Configuring Tailwind CSS v4 for shadcn/ui
- Setting up path aliases for component imports
- Troubleshooting initialization errors

**Do NOT use this skill for:**
- Adding individual components (use shadcn-components skill)
- Customizing themes or styles (use shadcn-customize skill)
- Advanced patterns (use shadcn-patterns skill)

## Quick Start

1. **Detect the framework** (Next.js, Vite, or Astro)
2. **Follow framework-specific setup** (see sections below)
3. **Run validation script** to verify installation
4. **Installation complete** - ready to add components

## Framework Detection

Check for framework indicators:
- **Next.js**: `next.config.js` or `next.config.ts` present
- **Vite**: `vite.config.ts` or `vite.config.js` present
- **Astro**: `astro.config.mjs` present

---

## Framework-Specific Setup

### Next.js Setup

Next.js auto-detects configuration, so setup is minimal:

1. **Install Tailwind CSS (if not already installed):**
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

2. **Configure Tailwind in `tailwind.config.js`:**
   ```javascript
   export default {
     content: [
       "./app/**/*.{js,ts,jsx,tsx}",
       "./components/**/*.{js,ts,jsx,tsx}",
     ],
   }
   ```

3. **Add Tailwind directives to `app/globals.css` or your CSS file:**
   ```css
   @import "tailwindcss";
   ```

4. **Verify imports in your app entry:**
   - For App Router: Ensure `globals.css` is imported in `app/layout.tsx`
   - For Pages Router: Ensure CSS is imported in `pages/_app.tsx`

5. **Run initialization:**
   ```bash
   npx shadcn@latest init
   ```
   - Choose defaults when prompted (or use `-d` flag to skip)

6. **Verify installation succeeded** - Check these files exist:
   - `components/ui/button.tsx` (or similar component)
   - `lib/utils.ts`
   - `components.json`

---

### Vite Setup

Vite requires more explicit configuration:

#### Step 1: Install Dependencies

```bash
npm install -D tailwindcss @tailwindcss/vite
```

#### Step 2: Configure Tailwind in Vite

Update `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
```

**Key points:**
- `tailwindcss()` plugin processes Tailwind imports
- `resolve.alias` maps `@` to `/src` directory
- Plugin order: react first, then tailwindcss

#### Step 3: Configure TypeScript Path Aliases

Update root `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

If you have `tsconfig.app.json` (app-specific config), also add paths there:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Why both configs?** shadcn init validates the root config, but TypeScript uses both configs in project reference setups.

#### Step 4: Prepare Global CSS File

**This step is CRITICAL.** Add ONLY the Tailwind import to your global CSS (typically `src/index.css` or `src/globals.css`):

```css
@import "tailwindcss";
```

**⚠️ IMPORTANT:**
- **Add ONLY this line**
- Do NOT add CSS variables yet
- Do NOT add @layer blocks
- Do NOT add any other customizations

The `shadcn init` command will automatically add all theme configuration after it validates Tailwind v4.

Verify this file is imported in your app entry point (`src/main.tsx` or `src/main.ts`):

```typescript
import './index.css'
```

#### Step 5: Run Initialization

```bash
npx shadcn@latest init -d
```

The `-d` flag uses defaults (recommended):
- Style: `new-york`
- Base color: `neutral`
- CSS variables: `true`

Or run interactively without `-d` to choose options.

---

### Astro Setup

Astro requires React integration:

#### Step 1: Ensure React Integration

```bash
npx astro add react
```

This installs `@astrojs/react` and configures the integration.

#### Step 2: Install Tailwind CSS

```bash
npx astro add tailwind
```

This installs Tailwind and creates necessary configuration.

#### Step 3: Configure Path Aliases

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

#### Step 4: Initialize shadcn/ui

```bash
npx shadcn@latest init
```

When prompted:
- Choose `src` as component directory
- Choose defaults for other options

#### Step 5: Use Components in Astro

Components are used with the `client:` directive for interactivity:

```astro
---
import { Button } from '@/components/ui/button'
---

<Button client:load>Click me</Button>
```

**Important:** Use `client:load` or `client:visible` directives on interactive components.

---

## Running shadcn Init

After pre-configuration is complete, run initialization:

```bash
# Non-interactive (uses defaults)
npx shadcn@latest init -d

# Interactive (choose options)
npx shadcn@latest init
```

**What shadcn init creates:**
- `components.json` - Configuration file for component paths and settings
- `src/lib/utils.ts` - Utility file containing the `cn()` function for class merging
- **Updates your CSS file** - Adds theme configuration using CSS variables
- **Installs dependencies** - Adds `clsx`, `tailwind-merge`, and `class-variance-authority`

**During initialization, shadcn validates:**
- Framework detection (Next.js, Vite, Astro, etc.)
- Path aliases in `tsconfig.json`
- Tailwind CSS v4 installation and `@import "tailwindcss"` in CSS

If validation fails, check error message and review pre-configuration steps above.

---

## Verification

After running `shadcn init`, verify installation using the validation script:

```bash
bash .claude/skills/shadcn-init/scripts/validate-installation.sh
```

This script checks:
- `components.json` exists
- `src/lib/utils.ts` exists with `cn()` function
- Required dependencies installed (clsx, tailwind-merge, class-variance-authority)
- Tailwind CSS v4+ installed
- CSS file has Tailwind import and theme variables
- Path aliases configured in tsconfig

If validation fails, see the Troubleshooting section below.

---

## Troubleshooting

### "No import alias found"

**Cause:** Path aliases not configured in `tsconfig.json`

**Fix:**
1. Add to `tsconfig.json` and `tsconfig.app.json` (if exists):
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```
2. For Vite: Also add `resolve.alias` to `vite.config.ts`
3. Delete `components.json` if it exists
4. Re-run `npx shadcn@latest init -d`

### "Unable to find Tailwind CSS"

**Cause:** Tailwind not installed or missing CSS import

**Fix:**
1. Install: `npm install -D tailwindcss @tailwindcss/vite`
2. Add to global CSS (top of file): `@import "tailwindcss";`
3. Verify CSS file is imported in app entry point
4. Re-run `npx shadcn@latest init -d`

### Framework Not Detected

**Cause:** Framework detection failed

**Fix:**
1. Verify framework: `npm list react react-dom`
2. Delete `components.json` if exists
3. Run `npx shadcn@latest init` (interactive mode)
4. Manually select your framework

### Validation Script Fails

**Cause:** Missing configuration or dependencies

**Fix:**
1. Read error messages from validation script
2. Review framework-specific setup steps above
3. For Vite: Check BOTH `tsconfig.json` AND `tsconfig.app.json`
4. Delete `components.json` and retry

## What shadcn init Creates

The `npx shadcn@latest init` command:
- Creates `components.json` (configuration file)
- Creates `src/lib/utils.ts` (contains `cn()` utility for class merging)
- Updates your CSS file with theme variables
- Installs dependencies: `clsx`, `tailwind-merge`, `class-variance-authority`

## Advanced References

For detailed framework-specific guides:
- [Next.js Setup Guide](references/nextjs-setup.md)
- [Vite Setup Guide](references/vite-specific-guide.md)
- [Astro Setup Guide](references/astro-setup.md)
- [Troubleshooting Guide](references/troubleshooting-init.md)

## Next Steps

Once installation is verified:
1. Add your first component: `npx shadcn@latest add button`
2. Use shadcn-components skill for adding more components
3. Use shadcn-customize skill for theme customization

Installation is complete when validation script passes all checks.
