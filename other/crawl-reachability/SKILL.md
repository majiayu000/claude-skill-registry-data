---
name: crawl-reachability
description: Reachability stage for AI crawlers. Use when pages are missing from AI results, appear empty to machines, or need sitemap and indexability checks. Discovers and samples pages, audits sitemap defects, and diagnoses JavaScript render faults without executing JavaScript. Writes the shared page inventory.
license: MIT
---

# Crawl & Reachability

The first gate in the pipeline, and the one most likely to make everything
downstream moot. A page that cannot be retrieved, or that arrives without its
content, cannot be selected as a source no matter how good the content is.

arXiv:2604.25707 §4.1 reports a **76.44% fetch success rate** across pages that
answer engines had *already chosen* to cite. Roughly one in four selected pages
could not be retrieved. Reachability is not a hygiene item; it is a hard gate
with a measured failure rate.

## When to use

After `url-validation` clears the target. Run it standalone to answer "can a
crawler read this site at all" or "does this page render server-side".

## Inputs

| Input | Required | Notes |
|---|---|---|
| `--workspace` | no | Run directory. Defaults to the most recent run. |
| `--max-pages` | no | Overrides the preflight page budget. |
| `--json` | no | Machine-readable output. |

Reads `01-url-validation.json` for the target, scope, robots policy and budget.
Refuses to run if preflight has not cleared.

## Procedure

1. **Discover.** robots.txt `Sitemap:` directives, then the conventional
   sitemap paths, expanding at most three sitemap indexes; fall back to a
   bounded same-scope homepage crawl when discovery yields fewer than 12 URLs.
   Probe for `llms.txt`.
2. **Sample.** Round-robin across page types so the sample spans product,
   pricing, article, docs, about and hub pages rather than 20 blog posts. This
   is what makes a later population claim defensible.
3. **Fetch**, honouring robots.txt per URL and the crawl-delay, saving each
   page's HTML into the workspace for downstream skills. No JavaScript is
   executed — deliberately, because that is what a crawler sees.
4. **Audit the sitemap** in depth (see the table below).
5. **Diagnose render faults** per page.
6. **Check per-page reachability**: status, canonical correctness,
   `X-Robots-Tag`, `noindex`, soft-404s, redirect behaviour.
7. **Write** `02-crawl-reachability.json` including the page inventory.

Run it:

```
python3 scripts/check_reachability.py [--workspace PATH] [--max-pages N] [--json]
```

## Checks performed

### Sitemap

| Check id | Detects | Severity | Claim level |
|---|---|---|---|
| `sitemap_missing` | No retrievable sitemap | high | 1 |
| `sitemap_not_declared` | Sitemap exists but robots.txt does not point to it | medium | 1 |
| `sitemap_malformed` | Bad namespace, unwrapped `<loc>`, over size limits | medium | 1 |
| `sitemap_empty` | Zero `<url>` entries | high | 1 |
| `sitemap_broken_entries` | Listed URLs returning 4xx/5xx | high/medium | 1 |
| `sitemap_redirect_heavy` | Over 30% of sampled entries redirect | medium | 1 |
| `sitemap_orphans` | Crawlable pages missing from the sitemap | high/medium | 1 |
| `sitemap_off_scope` | Entries outside the serving host | medium | 1 |
| `sitemap_scheme_mismatch` | `http` entries on an `https` site | medium | 1 |
| `sitemap_bad_lastmod` | `lastmod` not a valid W3C datetime | low | 1 |
| `sitemap_future_lastmod` | `lastmod` in the future | medium | 1 |
| `sitemap_stale` | Median `lastmod` older than a year | medium | 1 |
| `sitemap_uniform_lastmod` | Every entry shares one `lastmod` | low | 1 |

### Render faults

| Check id | Detects | Recoverable | Severity |
|---|---|---|---|
| `empty_shell` | Empty mount point, no server-rendered content | no | critical |
| `state_blob` | Content present only inside a client state payload | yes | high |
| `script_heavy_shell` | Script-dominated document, nothing recoverable | no | high |
| `thin_served_html` | Visible text under 5% of served bytes | no | high |
| `meta_only` | Metadata renders, body does not | no | medium |
| `lazy_content` | Primary content deferred behind loading placeholders | no | medium |
| `client_routing` | Hash-fragment routes; sub-pages have no own URL | no | high |
| `noscript_gap` | Framework present, no `<noscript>` fallback | no | medium |

The `state_blob` / `empty_shell` distinction is the point of this section. Both
look identical to a browser-free reader, but the fixes differ by an order of
magnitude of effort: `state_blob` means the text already ships with the page
and needs hydrating into markup; `empty_shell` means it never left the server.

### Page reachability

| Check id | Detects | Severity | Claim level |
|---|---|---|---|
| `page_unreachable` | Sampled pages returning errors | high | 1 |
| `noindex_on_public_page` | `noindex` on a page that should be indexed | high | 1 |
| `x_robots_blocks` | `X-Robots-Tag` blocking indexing or AI agents | high | 1 |
| `canonical_mismatch` | `rel=canonical` pointing elsewhere unexpectedly | medium | 1 |
| `canonical_missing` | No `rel=canonical` on a site with URL variants | low | 2 |
| `soft_404` | 200 response whose content says "not found" | medium | 2 |
| `slow_response` | Median response time over 3 seconds | medium | 2 |

## Output

`02-crawl-reachability.json`, including the page inventory downstream skills
read:

```json
{
  "pages": [ { "url": "...", "page_type": "product", "status": 200, "html_path": "pages/003.html" } ],
  "discovery": { "sitemap_found": true, "candidates": 214, "llms_txt": false },
  "sitemap": { ...deep audit... },
  "render": { "pages_with_blocking_faults": 3, "fault_counts": { ... } },
  "findings": [ ... ]
}
```

## Guardrails

Read-only. `robots.txt` is enforced per URL, not merely reported. Crawl-delay
is honoured. Requests are rate-limited and the page, byte and wall-clock
budgets are hard limits. Never authenticates, never submits a form, never
leaves the registrable domain.

## Grounding

- Fetch success rate 76.44% across cited pages (§4.1) — reachability is a
  measured failure mode, not a theoretical one.
- Search-trigger rates 98.64% / 99.67% / 100% (§6) — retrieval is attempted on
  nearly every prompt, so a retrieval-time failure is a citation failure.
- Handout appendix C — content assembled after load is invisible to a reader
  that does not execute scripts.
