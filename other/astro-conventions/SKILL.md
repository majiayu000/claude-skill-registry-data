---
name: astro-conventions
description: "Use when writing or reviewing an Astro site: static by default versus on-demand rendering, client and server islands and their hydration directives, scripts and styles, environment variables and secrets, content collections, middleware and locals, actions, the origin check, and what an Astro component may and may not do."
paths: "**/*.astro, **/astro.config.*, **/src/content.config.*, **/src/middleware.*, **/src/actions/**, **/src/pages/**"
---

# astro-conventions

Step 6 of the pipeline (`WORKFLOW.md`), for the content-first, islands-based web framework. **Status: a base to
confront with real work**, no in-house project behind it yet (same status as `go-conventions`). Pinned to the
Astro documentation read on 2026-10-02 from the default branch (latest release on the package registry that day:
7.3.5; 7.4.1 on 2026-10-20, when the points below were re-checked, see Origin). The UI
framework used inside islands (React, Vue, Svelte, Solid) has its own block; the bundler under it is
`skills/vite-bundler-conventions`.

## When
As soon as an `.astro` file, `astro.config.*`, a content collection, middleware, an action or an endpoint is
written or modified, during `code` (6) and `review` (8).

## Steps

### 1. Rendering mode
1. **The default is a fully prerendered site.** Pages, routes and endpoints are rendered to static files at build
   time. Opt a route out with `export const prerender = false` (this needs a server adapter), or switch the whole
   project to `output: 'server'` and opt routes in. Choose per route: a page reading cookies or per-request data is
   on demand; a marketing page is not.
2. **Cookies, headers, sessions and the request-time APIs exist only on demand.** In a prerendered page they run
   at build time. Middleware runs at build time for prerendered pages and at request time otherwise.
3. **An adapter is required** for on-demand pages and for server islands; the platform's adapter may also enable
   image and caching services even for a static site.

### 2. Islands
1. **Astro components render to HTML with no client runtime.** A framework component (React, Vue, Svelte, …) ships
   no JavaScript to the browser unless it carries a `client:*` directive; the directive makes it a client island,
   hydrated separately from the rest of the page. Do not add a directive "to be safe".
2. **Pick the lowest priority that works.** `client:load` hydrates at once (immediately visible, immediately
   interactive); `client:idle` when the browser is idle (optional `timeout`); `client:visible` when it enters the
   viewport (optional `rootMargin` to hydrate slightly early and limit layout shift); `client:media` when a CSS
   media query matches; `client:only="framework"` skips server rendering entirely, so there is no HTML for
   crawlers or first paint: give a `slot="fallback"` and name the framework.
3. **Islands are independent**; share state between them with a store or events, not through the page. Several
   frameworks may coexist on a page; each costs its runtime, so mix only with a reason.
4. **Server islands** (`server:defer`, adapter needed) render a component on demand outside the page render: the
   page ships at once with its fallback slot, and the personal part (a profile picture from a cookie) arrives
   after, which lets the rest be cached hard. Props must be serialisable; functions and circular objects cannot be
   passed.

### 3. Scripts, styles and HTML
1. **A plain `<script>` in an `.astro` file is processed**: bundled, TypeScript-capable, typed as a module, deduplicated
   across components (included once per page, so attach listeners with a query over all matches rather than by
   id), and inlined when small. `is:inline` opts out; scripts outside `src/` also need it.
2. **Component styles are scoped by default**; `is:global` opts out. Prefer scoped styles and name a global style
   deliberately.
3. **`set:html` injects a raw HTML string like `innerHTML`; `set:text` escapes.** Use `set:html` only on trusted
   or sanitised content (a CMS field you control is still content; sanitise it). The JSON-LD case
   (`set:html={JSON.stringify(...)}` on a script tag) is the legitimate use.

### 4. Environment and secrets
1. **Only variables prefixed `PUBLIC_` reach client code**; every variable is available on the server. A secret
   never carries the prefix. Plain `import.meta.env` values are statically replaced at build time by the underlying
   bundler; under on-demand rendering, runtime reads depend on the adapter (usually `process.env`, not on every
   platform), which the type-safe schema API abstracts.
2. **Declare variables in the environment schema** (`astro:env`, `envField`) with a context (client or server)
   and an access (public or secret). Public client variables end up in client and server bundles; secret server
   variables stay out of the bundle and are read on the server; a secret client variable is not allowed because
   there is no safe way to send it. Secrets are validated when the server module is first imported, or at start
   with `validateSecrets`. In `astro.config`, `import.meta.env` does not see `.env` files: use `process.env` for
   variables set outside, or the bundler's `loadEnv` helper.
3. **Use `import.meta.env`, not `process.env`**, in Astro code; branch on `DEV`/`PROD`, never on a copy.

### 5. Content collections
1. **Content that is a set of similar items is a collection** with a loader (the built-in file/glob loaders, a
   community loader, or your own) and a schema that validates every entry and types the queries. Without a
   schema the types and the validation are lost.
2. **Query with `getCollection()` and `getEntry()`**, not by globbing imports. Build-time collections are right
   when content changes at deploy time; **live collections** (queried at request time) cost performance and have
   fewer features: use them only for data that must be current.
3. **Do not make a collection for a handful of one-off pages**, or for a source with its own client library that
   offers no loader and that you would rather call directly.

### 6. Server code
1. **Middleware** exports a named `onRequest(context, next)` from the middleware file (not a default export),
   shares request data through `context.locals`, and runs for every on-demand request; compose several with the
   `sequence` helper. Keep `locals` free of secrets that a template might print.
2. **Actions** (`defineAction`) are typed server functions with validated input (a schema; JSON by default, form
   data when `accept: 'form'`). Return data; throw the library's action error for expected failures (not found,
   unauthorised) instead of returning `undefined`. Check the caller's authorisation inside the handler: an action
   is a public endpoint, reachable under a path derived from its name (`/_actions/<name>`), and the actions guide says
   the same authorisation checks as for any endpoint must be made in the handler.
3. **CSRF**: on-demand pages check the `Sec-Fetch-Site` header of modern browsers, falling back to the `Origin`
   header, for `POST`, `PATCH`, `DELETE` and `PUT` with no content type or a form-style one (urlencoded, multipart,
   plain text), and answer 403 when the request is cross-origin. It is on by default and runs only for pages rendered on
   demand. Turning it off
   (`security.checkOrigin: false`) needs a stated reason; behind a proxy, the `allowedDomains` option makes Astro
   trust the forwarded host header only when it matches a listed pattern, which guards against host-header
   injection (it is about `Astro.url`, not a replacement for the origin check).
4. **Endpoints** return a `Response`; validate input as for any boundary (`skills/security-hardening`).

## Output / checkpoint
A route-by-route statement of its rendering mode; the `client:*` directive of each island with its reason; the
env schema; the collection schemas. No dedicated checkpoint: `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the package, the person runs `pnpm add <package>`
(`CONVENTIONS.md`). Never a secret behind `PUBLIC_`. Never `set:html` on unsanitised input. Never a `client:*`
directive without a reason. A rule with a number or a default is the pinned major's; read `package.json` before
applying it to another.

## Mechanical checks

```
grep -rnE "client:(load|idle|visible|media|only)" src
grep -rnE "set:html" src
grep -rnE "PUBLIC_[A-Z_]*(SECRET|KEY|TOKEN|PASSWORD)" .env* src
grep -rnE "export const prerender" src
grep -rnE "checkOrigin" astro.config.*
grep -rnE "process\.env" src
grep -rnE "getCollection|getLiveCollection|import\.meta\.glob" src
grep -rnE "export default" src/middleware.*
```

- A `client:load` on an island below the fold is a candidate for `visible`; a `client:only` with no fallback
  hurts first paint and crawlers.
- A secret-looking name behind `PUBLIC_` is a finding even with a placeholder value.

## Origin
Re-verified on 2026-10-20 against the same repository's default branch (licence file read: MIT, "Copyright (c)
2022 withastro"; latest release that day 7.4.1): the directives reference (every `client:*` directive, its options and
the `client:only` fallback slot), the on-demand rendering guide (default prerender, `prerender = false`, adapter, the
`'server'` output mode), the server-islands guide (serialisable props, fallback slot, adapter), the client-side
scripts guide (processing, deduplication, `is:inline`, scripts outside `src/`), the environment-variables guide
(`PUBLIC_`, `astro:env` contexts and access, secret validation, `loadEnv`, `process.env` in the config), the
content-collections guide (loader, optional schema, build-time against live), the middleware guide and reference
(named `onRequest`, `locals`, `sequence`, build-time run), the actions guide (accept, `ActionError`, public path,
authorisation), the configuration reference (`security.checkOrigin`, `security.allowedDomains`, `output`), the
styling guide (scoped by default) and the version 7 upgrade guide (nothing there touches these rules). Nothing was
found wrong except the CSRF description (corrected above) and the claim that the authorisation rule for actions was
ours (the guide states it). Two points rest on inference: that a middleware must not be a default export (the
reference documents the named export only), and the `PUBLIC_`-secret mechanical check. Original source note: rewritten from the official Astro documentation (the `withastro/docs` repository, `src/content/docs/en`, MIT
licence), read from a shallow clone of the default branch on 2026-10-02: the islands concept page, rendering
(on-demand rendering and output), the directives reference, client-side scripts, environment variables and the
`astro:env` module, content collections, middleware, actions, server islands, and the security options of the
configuration reference. Mechanisms and defaults are the framework's; grouping and wording are ours; no text was
copied. **Facts that move, with their pin (Astro 7 documentation):** the client directive set, the origin-check
default and its content types, the live collection limits, the server-island serialisable types, the adapter
requirement. **Not read, a stated gap:** images and fonts, view transitions and prefetch, internationalisation,
routing details, sessions, the caching page, the deployment guides, testing, and any UI-framework integration;
nothing about them was written. Refresh with `skills/source-freshness` on the next major. Written 2026-10-02,
never run on real work.

Independent verification 2026-10-21: 17 checked, 17 matched, 0 corrected, 0 unverified
