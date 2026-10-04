---
name: new-page
description: Scaffold a new public page following project conventions. Use when adding a new route under (public).
user-invocable: true
allowed-tools: Read, Write, Grep, Glob
---

Create a new page at `src/app/(public)/$ARGUMENTS/page.tsx`.

## Rules (from CLAUDE.md)

- Keep the page as a Server Component unless interactivity is needed
- Push "use client" to leaf components only
- Use `tenantConfig` for any tenant-specific text (never hardcode)
- Use shadcn/ui components and semantic CSS classes (bg-primary, text-muted-foreground)
- Check feature flags before rendering optional sections
- Follow the design chain: Tokens -> Tailwind -> Radix/shadcn -> Domain -> Patterns -> Pages

## Process

Before creating:
1. Read `src/lib/config/tenant.config.ts` for available config values
2. Check existing pages in `src/app/(public)/` for patterns to follow
3. Create the page file following conventions
4. If the page needs client interactivity, create a separate client component in `src/components/` and import it from the server page
