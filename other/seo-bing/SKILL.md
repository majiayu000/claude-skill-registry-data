---
name: seo-bing
description: "Audit Bing search visibility, Webmaster Tools evidence, and IndexNow readiness when authorized tools are available. Use for Bing indexing, link, crawl, or Microsoft search visibility work; not for Google indexing assumptions."
license: Apache-2.0
metadata:
  version: "1.0.0"
  domain: "seo-geo"
  provenance: "marketing-agent-os"
---

# Bing SEO Analysis

Keep Bing evidence separate from Google and other engines because their submission and reporting surfaces differ.

## Workflow

1. Confirm site ownership, target market, date range, and whether the task is diagnostic or submission-related.
2. Use connected Bing Webmaster data when available; otherwise limit findings to public technical checks.
3. Validate sitemap, robots, canonical, status, and indexability before recommending submission.
4. Treat IndexNow submission as an external side effect. Preview URLs and obtain authorization before submitting.
5. Never claim that submission guarantees crawling, indexing, ranking, or AI citation.
6. Route Google-specific work to `seo-google` and multi-source backlink analysis to `seo-backlinks`.

## Output

Return observed evidence, engine-specific interpretation, proposed action, submission status if authorized, and follow-up validation.
