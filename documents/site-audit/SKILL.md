---
name: site-audit
description: "Crawl any website and produce a technical SEO health audit — health score, broken links, duplicate content, missing meta tags. Works like Ahrefs Site Audit."
allowed-tools: Bash, Write, Read
---

# Site Health Audit Skill

Crawl any website via its sitemap and produce a comprehensive technical SEO audit with an Ahrefs-style health score.

## When to Use

- User asks for a "site audit", "health check", or "technical SEO audit"
- User wants to find broken links on their website
- User asks about duplicate titles, missing meta descriptions, or other on-page SEO issues
- After a major site launch, redesign, or migration
- As a scheduled monthly audit to track site health over time

## How to Run

The script auto-discovers the sitemap and requires zero npm dependencies.

### Quick sample (50 pages)
```bash
bun .claude/skills/site-audit/scripts/site-audit.ts --url https://example.com --fix
```

### Full crawl with report file
```bash
bun .claude/skills/site-audit/scripts/site-audit.ts --url https://example.com --full --fix --output docs/seo/site-audit-$(date +%Y-%m-%d).md
```

### Custom sitemap URL
```bash
bun .claude/skills/site-audit/scripts/site-audit.ts --url https://example.com --sitemap https://example.com/custom-sitemap.xml --full
```

### Options
| Flag | Description |
|------|-------------|
| `--url <url>` | Base URL of the site to audit (required) |
| `--sitemap <url>` | Direct sitemap URL (skips auto-discovery) |
| `--sample N` | Randomly sample N URLs (default: 50) |
| `--full` | Crawl every URL in the sitemap |
| `--fix` | Show actionable fix suggestions per issue |
| `--verbose` | Print per-URL details |
| `--json` | Output results as JSON (for programmatic use) |
| `--output <path>` | Write structured markdown report to file |

## What It Checks (16 categories)

1. **HTTP Status** — 4xx/5xx errors
2. **Title** — missing, too short (<10), too long (>60)
3. **Meta Description** — missing, too short (<50), too long (>160)
4. **H1** — missing or multiple H1 tags
5. **Canonical** — missing or non-self-referencing
6. **Indexing** — noindex directives
7. **Open Graph** — missing og:title, og:description, og:image
8. **Twitter Card** — missing twitter:card
9. **Hreflang** — missing x-default, missing self-reference
10. **Images** — missing alt attributes
11. **Content** — thin content (<100 words)
12. **Performance** — slow responses (>1.5s), large pages (>500KB)
13. **Broken Links** — internal links pointing to 404s
14. **Duplicate Titles** — multiple pages sharing the same title (errors)
15. **Duplicate Descriptions** — multiple pages with same meta description
16. **Duplicate H1** — multiple pages sharing the same H1

## Health Score Formula

Uses the Ahrefs formula:
```
score = (total_pages - pages_with_errors) / total_pages * 100
```

**Only errors affect the score** — warnings and notices are informational.

## Where to Save Reports

Write audit reports to the Space filesystem so they persist and can be compared over time:
```
docs/seo/site-audit-YYYY-MM-DD.md
```

When running a follow-up audit, compare with the previous report to highlight improvements and regressions.
