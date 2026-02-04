---
name: taurinext-shadcn
description: taurinext-shadcn template reference doc. Use this when to find in-depth information about this template.
---

# TauriNext-shadcn

This document provides context for AI assistants (like Claude) working on this `taurinext-shadcn` template codebase.

## Project Architecture

This TauriNext-shadcn is a template repository for building cross-platform applications that run as:

1. **Web app** (SPA in browser)
2. **Desktop app** (native via Tauri)

Both targets share the same Next.js codebase with **shadcn/ui** components.

### Tech Stack

- **Frontend Framework**: Next.js 15.5.5 (App Router)
- **UI Library**: React 19.1.0
- **Component System**: shadcn/ui (New York style)
- **Styling**: Tailwind CSS v3.4.18 (**CRITICAL: NOT v4**)
- **CSS Utilities**:
  - `class-variance-authority` - Component variants
  - `clsx` + `tailwind-merge` - Class name merging
  - `tailwindcss-animate` - Animations
- **Icons**: Lucide React
- **Desktop Runtime**: Tauri v2
- **Language**: TypeScript (strict mode)
- **Build Mode**: Static Export (CSR only, NO SSR)

## CRITICAL Configuration Details

### 1. Tailwind & PostCSS Config Location

**MUST BE IN `src-next/` DIRECTORY, NOT ROOT**

```
✅ CORRECT:
src-next/tailwind.config.cjs
src-next/postcss.config.cjs

❌ WRONG:
tailwind.config.cjs (at root)
postcss.config.cjs (at root)
```

**Why:**
- `npm run dev:next` executes `cd src-next && next dev`
- Next.js runs from inside `src-next/` directory
- It looks for configs in its working directory
- If configs are at root, Tailwind won't process CSS

### 2. Config File Format: CommonJS (.cjs)

**MUST USE `.cjs` EXTENSION, NOT `.js`**

```javascript
// ✅ CORRECT: tailwind.config.cjs
module.exports = {
  darkMode: ["class"],
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}"],
  // ...
}

// ❌ WRONG: tailwind.config.js with ES modules
export default {
  // This will NOT work
}
```

**Why:**
- Root `package.json` has `"type": "module"`
- This makes `.js` files use ES module syntax by default
- PostCSS loader requires CommonJS format
- `.cjs` explicitly forces CommonJS, overriding package.json setting

### 3. Tailwind CSS Version

**MUST BE v3.4.x, NEVER v4.x**

```json
{
  "devDependencies": {
    "tailwindcss": "^3.4.18",        // ✅ CORRECT
    "tailwindcss-animate": "^1.0.7"   // ✅ Required
  }
}
```

**Why:**
- shadcn/ui components built for Tailwind v3
- Tailwind v4 uses completely different config format (`@import` in CSS)
- v4 incompatible with current shadcn/ui components
- v4 config syntax is radically different

**If v4 accidentally installed:**
```bash
npm uninstall tailwindcss
npm install -D tailwindcss@^3.4.18
```

### 4. shadcn/ui CLI Limitation

**THE SHADCN CLI DOES NOT WORK WITH THIS PROJECT**

**Reason:**
- CLI expects standard Next.js structure (project root = Next.js root)
- This project has Next.js in `src-next/` subdirectory
- CLI cannot find `tsconfig.json` at root level
- CLI fails with "Couldn't find tsconfig.json"

**Solution: Manual Component Installation**

1. Visit https://ui.shadcn.com/docs/components/[component-name]
2. Find component code (often linked to GitHub)
3. Check for required dependencies (e.g., `@radix-ui` packages)
4. Install dependencies: `npm install @radix-ui/react-dialog`
5. Create file in `src-next/components/ui/[name].tsx`
6. Copy component code
7. Verify imports use `@/` aliases

**Example:** Installing Dialog component
```bash
# 1. Install dependencies
npm install @radix-ui/react-dialog

# 2. Create file
# File: src-next/components/ui/dialog.tsx

# 3. Copy code from https://ui.shadcn.com/docs/components/dialog
# or from GitHub: https://github.com/shadcn-ui/ui/blob/main/apps/www/registry/new-york/ui/dialog.tsx

# 4. Verify imports
import { cn } from "@/lib/utils"  // ✅ Uses @ alias
```

## Directory Structure

```
taurinext-shadcn/
├── src-next/                        # Next.js application
│   ├── app/                         # App Router
│   │   ├── layout.tsx               # Root layout (NO 'use client')
│   │   ├── page.tsx                 # Counter demo ('use client')
│   │   └── globals.css              # Tailwind + CSS variables
│   ├── components/                  # React components
│   │   └── ui/                      # shadcn/ui components
│   │       ├── button.tsx           # Installed
│   │       ├── card.tsx             # Installed
│   │       └── badge.tsx            # Installed
│   ├── lib/                         # Utilities
│   │   └── utils.ts                 # cn() helper
│   ├── public/                      # Static assets
│   ├── tailwind.config.cjs          # ⚠️ MUST be .cjs in src-next/
│   ├── postcss.config.cjs           # ⚠️ MUST be .cjs in src-next/
│   ├── next.config.ts               # Next.js config
│   └── tsconfig.json                # TypeScript config
├── src-tauri/                       # Tauri Rust code
├── components.json                  # shadcn config (root level)
└── package.json                     # "type": "module"
```

## Installed shadcn/ui Components

### Button (`src-next/components/ui/button.tsx`)

**Dependencies:**
```json
{
  "dependencies": {
    "@radix-ui/react-slot": "^1.x"
  }
}
```

**Variants:** default, destructive, outline, secondary, ghost, link

**Sizes:** default, sm, lg, icon

**Key Features:**
- Polymorphic via `asChild` prop (uses Radix Slot)
- Uses `cva` (class-variance-authority) for variants
- Supports all button HTML attributes

**Usage:**
```tsx
import { Button } from "@/components/ui/button"

<Button variant="outline" size="lg">Click Me</Button>
<Button asChild><Link href="/page">Link Button</Link></Button>
```

### Card (`src-next/components/ui/card.tsx`)

**Dependencies:** None (pure Tailwind)

**Exports:** Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter

**Usage:**
```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content here</CardContent>
</Card>
```

### Badge (`src-next/components/ui/badge.tsx`)

**Dependencies:** None

**Variants:** default, secondary, destructive, outline

**Usage:**
```tsx
import { Badge } from "@/components/ui/badge"

<Badge variant="secondary">New</Badge>
```

## Styling System

### CSS Variables (HSL Format)

**File:** `src-next/app/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;           /* HSL values (no hsl() wrapper) */
    --foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    /* ... more colors */
  }

  .dark {
    --background: 0 0% 3.9%;           /* Dark mode values */
    --foreground: 0 0% 98%;
    /* ... more colors */
  }
}

body {
  background-color: hsl(var(--background));   /* Wrap in hsl() here */
  color: hsl(var(--foreground));
}
```

**Format Notes:**
- Variables defined as bare HSL values: `0 0% 100%`
- Used with `hsl()` wrapper: `hsl(var(--background))`
- Allows Tailwind opacity modifiers: `bg-primary/50`

### Tailwind Color Mappings

**File:** `src-next/tailwind.config.cjs`

```javascript
module.exports = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... all color mappings
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

**This enables:**
- `bg-background` class → `background-color: hsl(var(--background))`
- `text-primary` class → `color: hsl(var(--primary))`
- `bg-primary/50` class → `background-color: hsl(var(--primary) / 0.5)`

### cn() Utility Function

**File:** `src-next/lib/utils.ts`

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Purpose:**
- Combines `clsx` (conditional classes) + `twMerge` (deduplication)
- Properly merges Tailwind classes
- Later classes override earlier ones

**Usage:**
```tsx
// Conditional classes
cn("base-class", condition && "conditional-class")

// Merging with prop classes
cn("px-4 py-2", className)  // className from props can override

// Complex example
cn(
  "inline-flex items-center",
  variant === "default" && "bg-primary text-white",
  variant === "outline" && "border border-input",
  disabled && "opacity-50 cursor-not-allowed",
  className
)
```

## Critical Constraints

### 1. Static Export Mode (CSR Only)

**Configuration:**
```typescript
// src-next/next.config.ts
output: 'export',
images: { unoptimized: true },
```

**Allowed:**
- ✅ Client Components (`'use client'`)
- ✅ Static generation at build time
- ✅ Client-side routing
- ✅ Client-side data fetching
- ✅ Tailwind CSS
- ✅ shadcn/ui components

**NOT Allowed:**
- ❌ Server Components requiring runtime
- ❌ API Routes
- ❌ Server Actions
- ❌ SSR, ISR
- ❌ Middleware

### 2. TypeScript Strict Mode

```json
// src-next/tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**Requirements:**
- Explicit types (no `any`)
- Proper null/undefined handling
- Function return types (e.g., `: void`, `: Promise<void>`)

### 3. Path Aliases

**Configuration:** Already set in `src-next/tsconfig.json`

**Usage:**
```tsx
import { Button } from "@/components/ui/button"     // ✅
import { cn } from "@/lib/utils"                    // ✅

import { Button } from "../../components/ui/button" // ❌ Avoid
```

## Common Development Tasks

### Adding a New Page

```tsx
// src-next/app/newpage/page.tsx
'use client';

import { Card, CardContent } from "@/components/ui/card";

export default function NewPage() {
  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardContent className="p-6">
          <h1 className="text-2xl font-bold">New Page</h1>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Adding Client-Side Data Fetching

```tsx
'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';

interface Post {
  id: number;
  title: string;
}

export default function Posts() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch('https://api.example.com/posts')
      .then((res) => res.json())
      .then((data: Post[]) => setPosts(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="space-y-4">
      {posts.map((post) => (
        <Card key={post.id}>
          <CardContent className="p-4">
            <h2 className="font-semibold">{post.title}</h2>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

### Using Tauri APIs

```tsx
'use client';

import { invoke } from '@tauri-apps/api/core';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

export default function TauriDemo() {
  const [result, setResult] = useState<string>('');

  const handleClick = async (): Promise<void> => {
    try {
      const message = await invoke<string>('greet', { name: 'World' });
      setResult(message);
    } catch (error) {
      console.error('Tauri command failed:', error);
    }
  };

  return (
    <div>
      <Button onClick={handleClick}>Call Tauri</Button>
      {result && <p>{result}</p>}
    </div>
  );
}
```

## Dark Mode

Dark mode is configured but NOT automatically implemented. To add:

### Option 1: Simple useState Toggle

```tsx
'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const [dark, setDark] = useState<boolean>(false);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  return (
    <Button variant="ghost" size="icon" onClick={() => setDark(!dark)}>
      {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  );
}
```

### Option 2: next-themes Package (Recommended)

```bash
npm install next-themes
```

See `TauriNextShadcn.md` for full implementation.

## Troubleshooting Guide

### Tailwind Styles Not Applying

**Symptoms:**
- Components render as unstyled HTML
- No visual styling from Tailwind classes

**Common Causes & Solutions:**

1. **Configs in wrong location**
   ```bash
   # Check files exist in src-next/
   ls src-next/tailwind.config.cjs
   ls src-next/postcss.config.cjs
   ```

2. **Wrong file extension**
   - Must be `.cjs` (CommonJS)
   - NOT `.js` or `.mjs`

3. **Missing Tailwind directives**
   ```css
   /* src-next/app/globals.css must have: */
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

4. **Cache issues**
   ```bash
   rm -rf src-next/.next
   npm run dev:next
   ```

### Component Import Errors

**Error:** `Cannot find module '@/components/ui/button'`

**Solutions:**
1. Verify file exists: `src-next/components/ui/button.tsx`
2. Check tsconfig.json has path aliases
3. Restart TypeScript server in VS Code
4. Check import statement uses exact filename

### Tailwind v4 Accidentally Installed

**Symptoms:**
- Config using `@import "tailwindcss"` in CSS
- Different config syntax errors

**Solution:**
```bash
npm uninstall tailwindcss
npm install -D tailwindcss@^3.4.18
```

### shadcn CLI Errors

**Error:** "Couldn't find tsconfig.json"

**Solution:** Don't use the CLI. Install components manually (see section above).

## Build Process

### Development

```bash
# Web only (fast iteration)
npm run dev:next

# Desktop app
npm run dev
```

### Production

```bash
# Build desktop app (includes Next.js build)
npm run build

# Or just Next.js static export
npm run build:next
```

**Output:** `src-next/out/` contains:
- `index.html`
- `_next/static/` (compiled CSS, JS)
- All routes as HTML files

## Best Practices for AI Assistants

1. **Always check config locations** before making changes
2. **Use `.cjs` extension** for Tailwind/PostCSS configs
3. **Install components manually** - don't suggest using shadcn CLI
4. **Check Tailwind version** - must be v3, never v4
5. **Use explicit TypeScript types** - follow strict mode
6. **Add `'use client'`** to interactive components
7. **Use `@/` path aliases** for imports
8. **Use `cn()` utility** for conditional classes
9. **Test in both web and desktop** modes when possible


## Summary Checklist for AI Assistants

When working on this codebase, remember:

- [ ] Configs in `src-next/`, not root
- [ ] Configs use `.cjs` extension
- [ ] Tailwind CSS v3 (NOT v4)
- [ ] shadcn CLI doesn't work - manual install only
- [ ] Static export mode (CSR only, no SSR)
- [ ] TypeScript strict mode enforced
- [ ] Use `@/` path aliases
- [ ] Use `cn()` for class merging
- [ ] Dark mode requires manual implementation

**When uncertain:** Refer to `SETUP.md` or `TauriNextShadcn.md` for detailed guidance.

