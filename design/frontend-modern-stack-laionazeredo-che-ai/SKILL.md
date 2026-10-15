---
name: "frontend-modern-stack"
description: "Master guide for modern frontend development using Next.js, React, Tailwind CSS, Shadcn UI, and Zod. Covers RSC boundaries, data fetching, accessibility, and performance optimization."
---

# Frontend Modern Stack Guide

This skill consolidates best practices for building high-performance, accessible, and maintainable web applications.

## ⚛️ React & Next.js (App Router)
- **RSC Boundaries**: Use React Server Components by default. Use `"use client"` only for interactivity, hooks, or browser APIs.
- **Data Fetching**: Fetch data in Server Components. Leverage Next.js cache and `revalidatePath`/`revalidateTag` for mutations.
- **Streaming & Suspense**: Use `loading.tsx` and `<Suspense>` for granular loading states.
- **Server Actions**: Use for form submissions and data mutations. Handle errors gracefully using `useFormState` or similar patterns.

## 🎨 Styling & UI
- **Tailwind CSS**: Use utility classes for responsive design. Follow a consistent naming convention for custom classes if needed.
- **Shadcn UI**: Use as the foundation for accessible, unstyled components. Customize according to the project's design system.
- **Dark Mode**: Implement using `next-themes`. Ensure contrast ratios meet WCAG AA standards.
- **Accessibility (a11y)**: Use semantic HTML. Ensure keyboard navigation and screen reader support (ARIA labels).

## 🛡 Validation & Type Safety
- **Zod**: Mandatory for schema validation (API responses, form data, env vars).
- **TypeScript**: Strict mode enabled. Avoid `any`. Use `z.infer<typeof schema>` for automatic type generation.
- **Forms**: Use `react-hook-form` with `@hookform/resolvers/zod` for robust form management.

## 🚀 Performance & Deployment
- **Optimization**: Use `next/image` for automatic image optimization. Leverage `next/font` for zero layout shift fonts.
- **Bundle Size**: Monitor with `next-bundle-analyzer`. Lazy load heavy components using `next/dynamic`.
- **Vercel Patterns**: Optimize for Edge Runtime where possible. Use Middleware for auth and redirects.

## 🔗 References
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Shadcn UI Documentation](https://ui.shadcn.com/)
- [Zod Documentation](https://zod.dev/)
