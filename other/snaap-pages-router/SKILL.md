---
name: snaap-pages-router
description: >
  Use when creating or editing any file under next-frontend/src/pages. Covers the data-fetching,
  <Head> and crawlable-navigation rules for this Next.js 16 Pages Router app.
---
# Pages Router rules (Next 16, JavaScript)

**The stack is settled:** Pages Router + JavaScript. Do not propose App Router or TypeScript.

**Every indexable route needs:**
1. `getStaticProps` (preferred) with `revalidate` for ISR, or `getServerSideProps` when data is
   per-request. Content fetched only in `useEffect` does NOT reach crawlers.
2. A `<Head>` with a unique `<title>`, `<meta name="description">` and `<link rel="canonical">`.
   Add OG and Twitter tags for shareable pages.
3. A single `<h1>`.

**Crawlable navigation:** every link to another page of ours is a real `<a href>` via `next/link`.
Never `router.push()` or `window.location` as the only path — that bug made 197 product pages
invisible to Google.

**JSON-LD:** emit server-side inside `<Head>` via `dangerouslySetInnerHTML`. Never inject after
hydration.

**noindex pages** (e.g. `/admin`, unapproved placeholder copy): add
`<meta name="robots" content="noindex,nofollow">` and exclude them from the sitemap.

**Business facts** come from `@/constants/business` — never hardcode phone, address, hours,
delivery or prices.

`"use client"` directives are inert in the Pages Router (leftovers from the abandoned App Router
attempt) — harmless, but don't add more.

Static content pages use `export async function getStaticProps() { return { props: {} }; }` so
they are statically generated and satisfy the SSR rule.
