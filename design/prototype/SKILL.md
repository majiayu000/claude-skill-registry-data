---
name: prototype
description: Create quick React prototypes that bundle to a single HTML file. Use for demos, interactive experiments, or shareable artifacts - NOT for full apps (use audreygen/Next.js for those).
---

# Prototype

> Adapted from [Anthropic's web-artifacts-builder skill](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder)

Create lightweight React prototypes that bundle to a single shareable HTML file.

## When to Use This vs. Other Tools

| Use `prototype` | Use `audreygen` | Use `Astro` |
|-----------------|-----------------|-------------|
| Quick prototype | Full app | Static site |
| Interactive demo | Needs database | Content-heavy |
| Shareable single file | Needs API/auth | Blog, docs |
| Claude artifacts | Production app | Marketing |

## Stack

- React 18 + TypeScript + Vite
- Tailwind CSS + shadcn/ui
- Parcel for bundling
- 40+ shadcn components pre-installed

## Workflow

### 1. Initialize Project

```bash
bash scripts/init-artifact.sh my-demo
cd my-demo
pnpm dev
```

### 2. Develop

Edit files in `src/`. All shadcn/ui components available:

```tsx
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog'
```

### 3. Bundle to Single HTML

```bash
bash scripts/bundle-artifact.sh
```

Creates `bundle.html` - single file with all JS/CSS inlined.

### 4. Share

- Open in browser
- Share file directly
- Paste into Claude.ai as artifact

## Setup Required

Before first use, download the shadcn components tarball:

```bash
curl -L -o scripts/shadcn-components.tar.gz \
  https://github.com/anthropics/skills/raw/main/skills/web-artifacts-builder/scripts/shadcn-components.tar.gz
```

## Design Notes

Same guidelines as your other projects:
- Use theme tokens (`text-muted-foreground`) not hardcoded colors
- `@/` imports
- No semicolons
- shadcn/ui patterns

For distinctive/creative UI, combine with the `creative-design` skill.
