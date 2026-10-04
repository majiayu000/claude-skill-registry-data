---
name: seo-geo
description: "Improve search and answer-engine visibility. Use for technical SEO, metadata, crawl/indexing, structured data, canonicals, sitemaps, local/ecommerce, migrations, AEO/GEO, and measurement."
---
# SEO/GEO
Improve discoverability without hacks: make pages crawlable, indexable, understandable, useful to humans, and easy for answer engines to cite accurately.
## Core Rules
1. Ask only when missing context changes the market, audience, crawl/indexing risk, migration plan, or claims.
2. Inspect rendered output, templates, routes, metadata, canonicals, robots, and sitemaps before recommending changes when available.
3. Match solution weight to search risk. Prefer exact, low-risk fixes over speculative visibility work.
4. Preserve URL, canonical, metadata, and content contracts unless a migration or cleanup intentionally changes them.
5. Flag freshness, evidence, and platform uncertainty; verify current rules when exact external requirements matter.
## Workflow
1. Classify the request:
   - technical SEO audit or implementation
   - on-page SEO and metadata
   - content structure, search intent, or internal linking
   - structured data or rich result eligibility
   - migration, redirects, canonicals, noindex, sitemap, or robots review
   - local, ecommerce, docs, blog, or landing-page visibility
   - generative search, AI Overviews, AEO, GEO, answer inclusion, or citation readiness
2. Gather the minimum context that changes the recommendation:
   - target audience, market, language, and geography
   - primary entities, products, services, locations, and competitors
   - site stack, rendered HTML, routes, sitemap, robots, canonicals, and metadata templates
   - Search Console, analytics, crawl, or rank data if provided
   - launch, migration, or traffic-risk timeline
3. Read Company Context when repository or brand guidance may change the recommendation.
4. Prioritize fixes by impact, confidence, and risk. Separate blockers from nice-to-have optimizations.
5. Prefer implementation-ready recommendations: exact metadata, route rules, schema type, redirect map, content section, internal link, or test command.
6. Avoid manipulative tactics: keyword stuffing, doorway pages, mass query-variant pages, fake reviews, inauthentic mentions, hidden text, or claims without evidence.

## Verification Loop

1. Validate changed rendered HTML, headers, robots, sitemaps, structured data, and canonical behavior before release.
2. If a signal is absent, contradictory, or blocked, correct the implementation and recrawl or rerun the relevant inspection.
3. After release, monitor the named baseline and rollback or forward-fix only with evidence; do not claim crawl or ranking outcomes without it.
4. Before reporting done, load [references/verification.md](references/verification.md) and run its rendered-output floor and evidence checklist.
## Company Context
When repo work touches public content, search visibility, launch behavior, migrations, analytics, brand claims, localization, or compliance-sensitive wording, read root `company.md` if present. Follow its brand, content, compliance, localization, platform, analytics, and release constraints unless higher-priority instructions or search quality conflict.
## Reference Map
Load [references/technical-seo.md](references/technical-seo.md) for crawl/indexing, metadata, canonicals, robots, sitemaps, structured data, JavaScript SEO, migrations, local/ecommerce/docs visibility, launch audits, and post-release checks.

Load [references/generative-search.md](references/generative-search.md) for AI Overviews, AEO/GEO, answer inclusion, entity clarity, citation readiness, freshness, evidence, and brand visibility in answer engines.

Load [references/local-ecommerce.md](references/local-ecommerce.md) for local business, ecommerce, merchant feeds, product variants, business profiles, reviews, store/location pages, and structured-data parity.

Load [references/measurement.md](references/measurement.md) for Search Console, analytics, baselines, launch annotations, migration monitoring, traffic-loss diagnosis, and experiment reporting.
## Tool Output
- Use `scripts/extract-page-seo.py` for a quick local HTML extraction of title, meta tags, canonicals, robots directives, hreflang links, Open Graph/Twitter tags, and JSON-LD script count.
- Use `--json` when another tool or CI job should consume extracted page signals.
- Use RTK when available for verbose, non-destructive crawl, build, lint, test, or log output.
- Inspect raw rendered HTML, headers, robots, sitemap, schema, and Search Console or analytics exports when exact tags, URLs, or evidence matter.
## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.
## Output Shape
For audits:

1. verdict and highest-impact fix
2. prioritized issues with evidence
3. exact recommended changes
4. validation steps and tools
5. residual risks or data needed

For implementation:

1. files or routes changed
2. behavior/search-signal change
3. how to validate rendered output, schema, crawl/indexing, and analytics
4. remaining rollout or monitoring gap
