---
name: qruiq-create-app
description: |
  Create a new Next.js app based on HeroUI template with Tailwind CSS v4, TypeScript, and dark mode.
  Use when asked to "create app", "new project", "init project", or "scaffold a Next.js app".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-create-app

> Tech stack: Next.js 15 + HeroUI v2 + Tailwind CSS v4 + TypeScript + next-themes

## Parameters

Collect before execution:

| Parameter | Required | Description | Example |
|---|---|---|---|
| `PROJECT_NAME` | Yes | Directory name (lowercase, hyphens) | `my-app` |
| `SITE_NAME` | Yes | Display name | `My App` |
| `SITE_DESCRIPTION` | Yes | Site description | `A web app for ...` |
| `TARGET_DIR` | Yes | Parent directory for the project | `/Users/xxx/dev` |

## Steps

**Execute all steps directly. Do not list as TODOs.**

### 1. Create project from template

```bash
cp -r ~/.qruiq/skills/skills/qruiq-create-app/template <TARGET_DIR>/<PROJECT_NAME>
```

### 2. Install dependencies

```bash
cd <TARGET_DIR>/<PROJECT_NAME>
yarn install
```

### 3. Update `package.json`

Set `"name"` to `<PROJECT_NAME>`.

### 4. Update `config/site.ts`

```ts
export const siteConfig = {
  name: "<SITE_NAME>",
  description: "<SITE_DESCRIPTION>",
  // Adjust navItems / navMenuItems / links as needed
};
```

### 5. Clean up example routes

```bash
rm -rf app/about app/blog app/docs app/pricing
```

### 6. Initialize git

```bash
git init
git add .
git commit -m "chore: init from heroui next-app-template"
```

## Project structure

```
<project>/
├── app/
│   ├── layout.tsx          # Root layout with Navbar + Providers
│   ├── page.tsx            # Homepage
│   ├── providers.tsx       # HeroUIProvider + ThemeProvider
│   └── error.tsx           # Global error boundary
├── components/
│   ├── navbar.tsx          # Top nav (with mobile menu)
│   ├── theme-switch.tsx    # Dark/light toggle
│   ├── icons.tsx           # SVG icons
│   ├── primitives.ts       # title/subtitle styles (tailwind-variants)
│   └── counter.tsx         # Example interactive component
├── config/
│   ├── site.ts             # Site name, nav items, external links
│   └── fonts.ts            # Google Fonts (Inter + Fira Code)
├── styles/
│   └── globals.css         # Tailwind v4 entry + theme vars
├── types/
│   └── index.ts            # Common types
├── next.config.mjs
├── tsconfig.json
└── package.json
```

## Key files

### `config/site.ts` — Customize site info here

```ts
export const siteConfig = {
  name: "My App",
  description: "App description here.",
  navItems: [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
  ],
  links: {
    github: "https://github.com/your-org/your-repo",
  },
};
```

### `app/providers.tsx` — Global providers

```tsx
"use client";
import { HeroUIProvider } from "@heroui/system";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { useRouter } from "next/navigation";

export function Providers({ children, themeProps }) {
  const router = useRouter();
  return (
    <HeroUIProvider navigate={router.push}>
      <NextThemesProvider {...themeProps}>{children}</NextThemesProvider>
    </HeroUIProvider>
  );
}
```

### `styles/globals.css` — Tailwind v4 config

```css
@import "tailwindcss";
@plugin '../hero.ts';
@source '../node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}';
@custom-variant dark (&:is(.dark *));

@theme {
  --font-sans: "Inter", sans-serif;
  --font-mono: "Fira Code", monospace;
}
```

## Composability

This skill is the foundation. Layer additional skills on top:

```
qruiq-create-app        → Project skeleton
    + qruiq-google-auth  → Google OAuth login
    + qruiq-github-ci    → CI/CD pipeline
    + qruiq-tke-deployment → K8s deployment config
```
