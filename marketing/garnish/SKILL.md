---
name: garnish
version: 0.1.0
license: MIT
description: Use when auditing or fixing discoverability metadata for a website before publication, including titles, descriptions, canonical URLs, robots policy, Open Graph, structured data, and sitemaps. Not for content strategy or keyword research.
---

# garnish

Garnish checks the metadata and indexing controls that surround a site's actual content. It works with the framework and policy already present in the target repository. It does not carry domains, account names, brand values, or fleet conventions from one site into another.

## Choose the mode

- **AUDIT** is read-only. Use it when the user asks what is wrong, whether a site is ready, or why a page is not appearing correctly in search or social previews.
- **FIX** applies an accepted audit backlog, or a narrowly requested metadata change. Use the site's existing components and conventions before adding anything.

If the request says only "audit", stop after the report. Never turn an indexing review into an unrequested production change.

## Read project policy first

Before checking tags, find the site's declared policy and public identity:

- framework configuration and deployment configuration
- the shared layout or head component
- repository instructions, docs, or an SEO reference file
- the production site URL and canonical path policy
- robots, sitemap, and preview-environment rules

Project policy wins over generic advice. If the repository does not declare a production domain or indexing policy, report that gap and stop before inventing one.

## AUDIT

Walk five stations. Score each 0-5, where 5 is correct and verified, 3 works with material gaps, 1 is mostly absent, and 0 actively blocks discovery.

| # | Station | What to verify |
|---|---|---|
| 1 | Page identity | One useful title and description per indexable page, one canonical URL, declared language, and no duplicate head tags |
| 2 | Social metadata | Open Graph type, title, description, URL, image, and image alt text; platform-specific tags only when project policy requires them |
| 3 | Indexing policy | Production robots directives match intent; previews and private environments are not indexed; `robots.txt` does not contradict page metadata |
| 4 | URL inventory | Sitemap exists when the site needs one; sitemap URLs, canonical URLs, redirects, and trailing-slash policy agree |
| 5 | Structured and rendered output | Structured data matches visible content and parses; a production build renders the expected tags without duplicates |

Read rendered output when the framework generates metadata at build time. A correct-looking component import is not evidence that each route receives correct values.

For cross-page checks, collect titles, descriptions, canonicals, and indexability across the route set. One page cannot reveal duplicates or contradictory URL forms.

### Audit report

```markdown
# garnish audit: <site> (<date>)

## Verdict
State whether metadata is ready, drifted, or blocking discovery. Name the first fix.

## Scorecard
| Station | Score (0-5) | Evidence |

## Findings
### [SEVERITY] Imperative title
- **Station:** one of the five stations
- **Where:** exact file, route, or rendered page
- **What:** the observed mismatch
- **Why it matters:** the concrete search, preview, or indexing effect
- **Fix:** the smallest action that resolves it
- **Effort:** S / M / L

## Not checked
List live indexing systems, webmaster consoles, or production responses that were unavailable.
```

Severity is critical for an unintended production `noindex` or a canonical that sends an entire site to the wrong host, high for missing or conflicting core metadata, medium for page-level duplication or invalid structured data, and low for presentation polish.

## FIX

Work the accepted backlog in impact order:

1. Start from a clean branch or worktree.
2. Reuse the existing head, metadata, routing, and sitemap primitives.
3. Change one finding at a time. Keep unrelated content and visual redesign out of the diff.
4. Run the narrowest rendered check after each change.
5. Build the site using its documented production command.
6. Inspect representative rendered pages and machine-readable outputs.
7. Re-run AUDIT over the changed scope.

Do not change the production domain, indexing status, redirect policy, analytics identity, or account metadata unless the user explicitly approved that value.

## Verification gate

Use [check](../check/SKILL.md) before any readiness claim. Evidence must include the build command and rendered output for the tags or files changed. A source diff alone does not prove what a crawler receives.

Run public prose through [plate](../plate/SKILL.md), including descriptions, social preview copy, `robots.txt` comments, and public examples.

## Stop conditions

Stop and ask when:

- the production host cannot be established from repository or deployment evidence
- two project documents prescribe different canonical or indexing policies
- fixing the finding would change live indexing for an existing site
- metadata is generated by an external system that is not available in the session

## Common mistakes

- Assuming one framework or component name across every site.
- Copying account handles, domains, colors, or image dimensions from another project.
- Treating a component import as rendered-page verification.
- Checking one route and claiming titles or descriptions are unique site-wide.
- Adding tags because a generic checklist mentions them when project policy deliberately excludes them.
- Fixing source metadata without rebuilding and inspecting the result.
