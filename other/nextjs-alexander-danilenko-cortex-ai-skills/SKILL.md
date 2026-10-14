---
name: nextjs
description: "Apply these opinionated Next.js conventions whenever writing or reviewing App Router code (14+): Server Components by default, where the 'use client' boundary belongs, the caching defaults that changed in Next 15, tag-based revalidation, treating Server Actions as public endpoints, the Metadata API, and next/image and next/font."
---

# Next.js

House conventions for Next.js App Router (14+). Apply them to code you are writing or changing — don't migrate untouched routes unless asked.

## Conventions

- **App Router only.** Never add to `pages/`. If a project still has one, new work goes in `app/` and the two coexist until someone schedules the migration.
- **Server Components by default.** `'use client'` marks a leaf that needs interactivity, not a page. Everything above that marker ships to the browser too, so the boundary belongs as deep in the tree as it will go.
- **Verify caching behaviour against the installed version — it changed.** Through Next 14, `fetch` was cached by default and you opted out; from Next 15, `fetch`, Route Handlers, and client navigation are uncached by default and you opt in. Assuming the wrong default gives you either stale pages or an origin taking every request. Check `package.json`, then set the intent explicitly (`cache`, `next.revalidate`, or route segment config) rather than relying on whatever the default happens to be.
- **`params` and `searchParams` are Promises from Next 15 on** — `const { slug } = await params`. Code written against 14 destructures them synchronously and breaks on upgrade, so check the installed major before copying either form.
- **A `layout.tsx` auth check is not a security boundary.** Layouts don't re-render on every navigation between their child routes, so the check can be skipped on client-side transitions. Enforce access in middleware and again where the data is read; the layout check is UX, not enforcement.
- **Tag what you fetch, revalidate by tag.** `next: { tags: ['user'] }` plus `revalidateTag('user')` after a mutation invalidates exactly the affected data. Time-based revalidation is a guess about staleness; tags are a fact about it.
- **Server Actions are public endpoints.** They are reachable by anyone who can find the action ID, so every one re-checks auth and re-validates its input server-side. The form it was rendered behind proves nothing about the caller.
- **Fetch in the component that renders the data.** React dedupes identical requests within a render pass, so prop-drilling data down to avoid a "duplicate" fetch buys nothing and couples the tree.
- **Metadata through the Metadata API** — `export const metadata` or `generateMetadata`. Hand-written `<head>` tags in a component don't merge across nested layouts and silently lose out to the framework's.
- **`next/image` and `next/font` always.** They exist for the two largest Core Web Vitals costs: unsized images causing layout shift, and font loading blocking first paint. A raw `<img>` gives up both.
- **`loading.tsx` and `error.tsx` per meaningful route segment.** The route boundary is where a failure should be contained; without `error.tsx`, one segment's error takes down the layout around it.
