---
name: nextjs-fsd-starter
description: Create a new Next.js project with FSD (Feature-Sliced Design) architecture, TypeScript, Tailwind CSS, ESLint (flat config), Prettier, and Husky. Use when user asks to create/scaffold/initialize a Next.js project with FSD architecture, or when they want a production-ready Next.js boilerplate with modern tooling setup.
---

# Next.js FSD Starter

Create a production-ready Next.js project with FSD architecture and modern tooling.

## Stack

- Next.js (latest, App Router)
- TypeScript
- Tailwind CSS
- ESLint (flat config) with FSD rules
- Prettier
- Husky (pre-commit lint)
- pnpm
- date-fns (date utilities)
- zustand (state management)
- es-toolkit (modern lodash alternative)
- react-hook-form (form handling)
- tw-animate-css (Tailwind animations)
- lucide-react (icons)
- @radix-ui (headless UI primitives)
- tailwind-merge (class merging)
- clsx (conditional classes)
- zod (schema validation)
- @tanstack/react-query (data fetching)

## Setup Process

### 1. Create Next.js Project

```bash
pnpm create next-app@latest <project-name> --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-pnpm
cd <project-name>
```

### 2. Install Dependencies

```bash
# Dev dependencies
pnpm add -D prettier eslint-config-prettier eslint-plugin-prettier husky lint-staged prettier-plugin-tailwindcss

# ESLint 9 dependencies
pnpm add -D @eslint/js typescript-eslint eslint-plugin-react-hooks @next/eslint-plugin-next eslint-import-resolver-typescript eslint-plugin-import

# React Compiler
pnpm add -D babel-plugin-react-compiler eslint-plugin-react-compiler

# Runtime dependencies
pnpm add date-fns zustand es-toolkit react-hook-form tw-animate-css lucide-react tailwind-merge clsx zod @hookform/resolvers @tanstack/react-query @tanstack/react-query-devtools

# Radix UI primitives
pnpm add @radix-ui/react-dialog @radix-ui/react-popover @radix-ui/react-tooltip @radix-ui/react-select @radix-ui/react-checkbox @radix-ui/react-slot @radix-ui/react-tabs
```

### 3. Enable React Compiler

Update `next.config.ts` to enable React Compiler:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
};

export default nextConfig;
```

### 4. Create FSD Directory Structure

Copy `assets/fsd-structure/` to `src/` directory. The structure uses `.gitkeep` files to preserve empty folders in git.

### 5. Apply Configuration Files

Copy these config files from `assets/configs/` to project root:

- `eslint.config.mjs` - ESLint flat config with FSD rules
- `.prettierrc` - Prettier config
- `.prettierignore` - Prettier ignore patterns

### 6. Update `src/app/globals.css`

Replace content with `assets/configs/globals.css` (shadcn-compatible with light/dark mode).

### 7. Setup Husky

```bash
pnpm exec husky init
```

Replace `.husky/pre-commit` content with:

```bash
pnpm lint-staged
```

### 8. Update package.json

Add these scripts and lint-staged config:

```json
{
  "scripts": {
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

### 9. Create CLAUDE.md and AGENT.md

Copy `assets/configs/CLAUDE.md` to project root as both `CLAUDE.md` and `AGENT.md`.

### 10. Update tsconfig.json paths

Ensure these path aliases exist:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/shared": ["./src/shared"],
      "@/shared/server": ["./src/shared/server"],
      "@/entities/*": ["./src/entities/*"],
      "@/features/*": ["./src/features/*"],
      "@/widgets/*": ["./src/widgets/*"],
      "@/views/*": ["./src/views/*"]
    }
  }
}
```

### 11. Final Verification

```bash
pnpm lint
pnpm format:check
```

### 12. Format Project

Run the formatter to ensure all generated and copied files follow the project style.

```bash
pnpm format
pnpm lint:fix
```

## FSD Layer Overview

| Layer       | Purpose               | Import Rule                                         |
| ----------- | --------------------- | --------------------------------------------------- |
| `views/`    | Page-level components | Can import from widgets, features, entities, shared |
| `widgets/`  | Complex UI blocks     | Can import from features, entities, shared          |
| `features/` | User interactions     | Can import from entities, shared                    |
| `entities/` | Business entities     | Can import from shared only                         |
| `shared/`   | Reusable utilities    | Cannot import from other layers                     |

## Slice Internal Structure

Each slice (entities, features, widgets, views) has the following internal structure:

```
<slice-name>/
├── index.ts      # Public API (barrel file)
├── api/          # API calls, server actions
├── model/        # Types, validation schemas, default values
├── ui/           # React components
├── lib/          # Utilities, custom hooks
└── config/       # Slice-specific configuration
```

### Directory Purposes

| Directory | Purpose                                                  |
| --------- | -------------------------------------------------------- |
| `api/`    | API calls, server actions, data fetching                 |
| `model/`  | TypeScript types, Zod schemas, default values, constants |
| `ui/`     | React components (presentational and container)          |
| `lib/`    | Utility functions, custom hooks                          |
| `config/` | Slice-specific settings, feature flags, constants        |

## Shared Layer Structure

```
shared/
├── index.ts      # Main barrel (client-safe exports)
├── server.ts     # Server-only exports
├── api/          # Shared API utilities (fetch wrapper, etc.)
├── config/       # Global configuration
├── lib/          # Utilities (cn, formatters, etc.)
├── model/        # Shared types, validation schemas
└── ui/           # Common UI components (Button, Input, etc.)
```

## Barrel File Convention

- `shared/index.ts` - Main barrel for shared (client-safe exports)
- `shared/server.ts` - Server-only exports (use `"use server"` or server components)
- Other layers: `<layer>/<slice>/index.ts` (e.g., `features/auth/index.ts`)
