---
name: senternet-site-ahrefs-audit
description: Pull Ahrefs Site Audit issues, apply the standard fix for each issue class, verify the trigger is gone, and commit.
---

# Ahrefs Site Audit Remediation

Read the latest Ahrefs Site Audit crawl for a site, resolve each fixable issue class with its
standard fix, confirm the condition that triggered the issue is gone from the source, then commit
and push. This runs against a **live site that already has an Ahrefs Site Audit project** — it is a
maintenance pass, not part of the initial build.

Requires the Ahrefs MCP server to be connected.

## Step 1 — Get the documented field names before calling any tool

The Ahrefs tools do **not** share one field vocabulary, and guessing field names silently returns
wrong or empty results. Call the `doc` tool for each Ahrefs tool **before** its first use and read
the real schema:

```
doc(tool="site-audit-projects")
doc(tool="site-audit-issues")
doc(tool="site-audit-page-explorer")
```

Two gotchas the docs make explicit — internalize both:

- In `site-audit-page-explorer`, the `select` and `order_by` parameters use the **outputSchema**
  column identifiers, but the `where` filter expression uses a **different** identifier set. They
  are not interchangeable.
- The affected-URL count on an issue is the `crawled` field (URLs currently affected) — not
  `added`, `change`, or a guessed `count`.

## Step 2 — Find the project and pull issues

Resolve the project id, then pull the issue list for the latest crawl:

```
site-audit-projects(project_url="https://www.example.com")   # → project_id
site-audit-issues(project_id=<id>)                            # latest crawl by default
```

`site-audit-issues` returns `issues[]`; the fields you act on are:

- `issue_id` — pass this to `site-audit-page-explorer` to get the affected URLs
- `name` — the human issue name (e.g. "Image file is broken", "Image has no alt text")
- `category` — one of `Images`, `Links`, `Internal pages`, `Redirects`, `Content`, … (see doc)
- `importance` — `Error`, `Warning`, or `Notice`
- `crawled` — number of URLs currently affected (work only issues where `crawled > 0`)

Work `Error` and `Warning` issues first; treat `Notice` as optional. If the response metadata
includes `render_with`, call the specified render tool rather than dumping the raw table.

## Step 3 — Get the affected URLs for each issue

For every issue you intend to fix, list the actual URLs so you know what to change:

```
site-audit-page-explorer(project_id=<id>, issue_id="<issue_id>", select="url", limit=1000)
```

Map each URL back to the source file/component that emits it (route, image ref, link).

## Step 4 — Apply the standard fix per issue class

| Issue class (category / name) | Standard fix |
|---|---|
| **Images** — "not using next-gen format", large image, uncompressed | Run the WebP conversion from `/senternet-site-image-webp`: convert to `.webp`, then update every reference. This fix **also strips leftover `.png`/`.jpg` refs and any format-fallback `<picture>` tags** — WebP is universal, so no PNG `<source>` fallbacks remain. `<picture>` stays only for art-direction (different crop/size per breakpoint), and even then the fallback `<img src>` must point at `.webp`. |
| **Images** — "Image has no alt text" / missing alt | Add descriptive, specific `alt` text to each affected `<img>`. Decorative-only images get `alt=""`. |
| **4xx** — broken internal link, broken image, "4xx page" (Links / Internal pages / Images) | Fix the target: correct the URL, restore the missing asset, or remove the dead link/reference. For a moved page, point the link at the new URL directly (don't rely on a redirect chain). |

### Out of scope: Shopify-hosted images

Images served from a Shopify CDN (`cdn.shopify.com` and similar third-party hosts) **cannot** be
converted or re-hosted from this repo — the source lives in Shopify, not here. When an image issue
resolves to a Shopify-hosted URL, **note it as out-of-scope and skip it**; do not attempt a local
WebP conversion. Call these out explicitly in your summary so they aren't mistaken for missed work.

## Step 5 — Verify the trigger condition is gone

Ahrefs re-crawls on its own schedule, so don't wait on a fresh crawl to prove the fix. Instead
verify the **local trigger** that produced each issue is gone from the source:

- Next-gen-format / PNG issues → no remaining `.png`/`.jpg` refs and no format-fallback `<picture>`
  (`grep -rn '\.png\|\.jpg' src/` and check `<picture>` blocks are art-direction only).
- Missing-alt issues → every affected `<img>` now has an `alt` attribute.
- 4xx issues → the offending link/asset resolves (build succeeds; the reference points somewhere real).

Then rebuild (`npm run build`) so prerendered HTML reflects the changes. The next Ahrefs crawl
confirms the issue drops out; local verification is what gates the commit.

## Step 6 — Commit and push

Commit the fixes with a message naming the issue classes resolved and the Shopify images left out
of scope, then push:

```bash
git add -A
git commit -m "Fix Ahrefs Site Audit issues: WebP conversion, alt text, 4xx links"
git push
```

Report a short summary: which issue classes were fixed, how many URLs each covered, and which
Shopify-hosted images were deliberately skipped.
