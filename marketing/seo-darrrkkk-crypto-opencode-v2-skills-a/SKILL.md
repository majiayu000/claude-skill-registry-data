---
name: seo
description: "\"Implement and diagnose search discoverability for Manus websites: crawler-visible HTML, per-route metadata, social previews, canonical URLs, sitemap and robots behavior. Use for public pages intended for search, SEO requests, link previews, or indexing problems.\""
compatibility: opencode
---

# Website SEO

Use this skill when public page content should be discoverable by search engines, or when the
user asks to implement or diagnose SEO. Keep private application content within its intended
access boundary.

## Make the intended content available

Identify which public URLs should be indexed and what distinct content each one represents.
Provide meaningful page-body HTML, descriptive titles and descriptions, and usable links between
those pages. A client-rendered shell with an empty mount element does not by itself contain
the content a crawler is meant to index.

Choose static generation when the framework can produce the content before a visit. Use SSR
when initial HTML must be generated for the current request. Browser interactivity can be added
to either result.
SEO does not imply one universal deployment architecture.

Use the actual public URL when declaring a canonical address. Keep sitemap entries consistent
with the intended indexable pages and robots behavior consistent with the site's access policy.
Do not expose private user URLs or private data merely to improve an SEO score.

## Initial HTML and per-route metadata

Build the following from each public route and its actual content, and include them in the
initial HTML rather than waiting for a browser effect:

| Item | What to provide |
| --- | --- |
| Page body | The meaningful public content for that URL, not only an empty app mount or loading placeholder. |
| Title and description | A route-specific `<title>` and `<meta name="description">`; detail pages use the loaded item's content. |
| Open Graph | Appropriate `og:type`, plus `og:title`, `og:description`, `og:url`, `og:site_name` and `og:image` for the intended preview. |
| Twitter Card | The intended `twitter:card` and matching title, description and image metadata. |
| Canonical | A `<link rel="canonical">` using the intended public URL. |
| HTTP status | A status that reflects the page result, including a real 404 for an unknown route or missing detail item. |

The intended preview must be available without executing application JS. Use publicly
reachable absolute URLs for canonical and sharing metadata. Escape dynamic head text and
attributes using the framework's metadata facilities or context-appropriate escaping.

Resolve missing content before sending the response. Carry a not-found result from route/data
loading to the page handler's status; add appropriate `noindex` metadata to the error page.
Returning a success status with a visible "not found" message creates a soft-404 problem.
Robots metadata is not a replacement for the correct status. Keep client-side navigation's
title and metadata consistent with the initial response for the same URL.

Only public data may enter public HTML or its embedded hydration state. Keep authenticated
rendering behind its access checks and private cache policy, and out of public indexing.

## Check the actual public response

When verification is required for the SEO task, request representative published pages without
executing JavaScript. Check their status, meaningful body content and page metadata, then inspect
the served sitemap and robots documents. Follow redirects and distinguish gateway restrictions
from missing application content. A rendered browser page or a Dashboard score alone does not
prove that the initial HTML contains the content to index.

Include a content-bearing public page, a dynamic detail page when present, and a missing route
or detail identifier. Check raw body text, per-route head tags and the actual HTTP status with
the normal visitor and relevant search/social crawler User-Agents. A 200 response is not enough:
SSR may have failed and returned a shell that the browser later filled in. Inspect render errors
when that happens. After a change to rendering, data loading or routing, repeat the affected
response checks rather than an unrelated full validation suite.

Platform HTML injection and CSP compatibility remain under
[published response handling](../references/routing-and-responses.md#platform-http-behavior).
The following sections describe the existing platform SEO behavior and implementation workflow.

## SEO panel and gateway documents

The Dashboard's Fix issues action sends failed SEO checks as an ordinary user chat message,
not a separate typed-action protocol. Its documented scoring thresholds are:

| Item | Panel result |
| --- | --- |
| Meta keywords | 3–8 pass; zero fails; 1–2 or more than 8 warns |
| Title | Missing fails; outside 30–60 characters warns |
| Meta description | Missing fails; outside 50–160 characters warns |
| H1 and H2 | Missing or longer than 80 characters fails |

Generated fix prompts target about 55 title characters and 150 description characters. The
panel scans rendered DOM; that is not a measurement of body content already present in the
raw HTML. The platform does not supply a prerendered crawler snapshot.

The gateway handles `/sitemap.xml` and `/robots.txt`, preferring a supplied project document
and otherwise generating a default. The transparent path prefers the backend's document before
object storage. The `x-manus-seo-source` header identifies `cdn`, `server`, or `generated`.
The separate Dashboard scan can warn about a missing file while the gateway serves a default.

A generated sitemap lists known project routes. On the canonical domain, generated robots
contains `User-Agent: *`, `Allow: /`, `Disallow: /api/*`, and a `Sitemap:` line. A non-canonical
domain gets `User-Agent: *` and `Disallow: /`. Literal route declarations for those paths are
restricted by [routes](../references/routing-and-responses.md#reserved-paths).

## SEO implementation

When discoverability is in scope, ensure meaningful page-body HTML is available without
requiring a crawler to run JavaScript. Prefer complete HTML produced by the existing framework's
static-generation support; a plain HTML site does not need a new framework or bundler for this.
If choosing server rendering would enable a one-way server capability, explain that change
before making it and respect explicitly staged requirements.

An alternative is to prerender in the development environment and commit the generated HTML
for static publication. Do not put browser-based prerendering in `build.command`; the hosted
static build does not provide that browser and shares its time budget with clone/upload.
Keep the prerendered files and the declared output consistent.

Canonical, `og:url`, and sitemap absolute addresses must use an explicitly configured real
public origin, never an internal request-derived address. Until that origin is configured,
omit those absolute tags rather than emitting a guessed/internal URL. The complete Preview
origin contract is separate from the SEO panel's thresholds above.
