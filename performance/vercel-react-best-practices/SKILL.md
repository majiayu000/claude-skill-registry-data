---
name: vercel-react-best-practices
description: Guía de mejores prácticas de performance para React y Next.js de Vercel Engineering
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: development
---

## What I do
- Proporciona lineamientos de optimización de performance para React/Next.js
- Cubre Server Components, Client Components, data fetching, bundle optimization
- Ayuda a evitar problemas comunes de performance

## When to use me
Use this when:
- Writing or refactoring React/Next.js components
- Optimizing bundle size
- Implementing data fetching patterns
- Working with Server Components vs Client Components
- Performance issues are reported

## Key Patterns
- Prefer Server Components over Client Components
- Use `use client` only when interactivity is needed
- Implement proper loading states with `loading.tsx`
- Use `Suspense` boundaries for streaming
- Avoid unnecessary re-renders with `React.memo` and `useMemo`
- Use `next/image` for optimized images
- Implement proper caching strategies
