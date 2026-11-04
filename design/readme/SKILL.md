---
name: readme
description: Use when starting work on an AstroDeck project, needing to understand the project structure, or looking up available components, sections, and layouts.
---

# AstroDeck README Skill

This skill provides access to the complete AstroDeck project documentation.

## When to Use This Skill

- Starting work on an AstroDeck project
- Creating new pages or components
- Understanding available sections and layouts
- Troubleshooting installation or configuration
- Learning about the project structure
- Finding deployment instructions

## Instructions

1. Read the README.md file at the project root for comprehensive documentation
2. The README contains:
   - Project overview and features
   - Installation instructions
   - Development commands
   - Complete project structure
   - Usage guide for pages, components, and layouts
   - Component library overview (15+ sections)
   - Customization guide
   - Deployment instructions
   - Troubleshooting guide
   - AI-friendly development information

## Quick Reference

### Key Commands
```bash
npm install    # Install dependencies
npm run dev    # Start development server (localhost:4321)
npm run build  # Build for production
npm run preview # Preview production build
```

### Three-Tier Architecture

AstroDeck uses a three-tier hierarchy of building blocks:

| Tier | What | Count | Location |
|------|------|-------|----------|
| **Components** | Small UI primitives (Button, Dialog, Tabs...) | 11 | `src/components/ui/` |
| **Sections** | Full page sections (Hero, Pricing, FAQ...) | 16 | `src/components/sections/` |
| **Pages** | Complete page templates (SaaS, Portfolio...) | 11 | `src/pages/` |

Components are the smallest pieces. Sections combine components into full-width blocks. Pages assemble sections into complete websites.

### Project Structure
```
src/
├── components/sections/  # TIER 2: Hero, CTA, Features, Pricing, FAQ, etc.
├── components/ui/        # TIER 1: shadcn/ui components (Button, Card, Dialog...)
├── layouts/              # BaseLayout, FullWidthLayout, AuthLayout, ArticleLayout
├── pages/                # TIER 3: Complete pages with file-based routing
├── content/              # Content Collections (blog)
├── styles/globals.css    # Design tokens
└── lib/utils.ts          # Utility functions
```

### Available Layouts
- **BaseLayout** - Boxed, centered content (max-w-5xl)
- **FullWidthLayout** - Full-width for showcase pages
- **AuthLayout** - Minimal, no header/footer
- **ArticleLayout** - Blog/article pages

### Import Convention
Always use path aliases:
```typescript
import Component from "@/components/Component.astro";
import { Button } from "@/components/ui/button";
import Layout from "@/layouts/BaseLayout.astro";
```

## Action

When this skill is invoked, read the full README.md file from the project root to get complete, up-to-date documentation.
