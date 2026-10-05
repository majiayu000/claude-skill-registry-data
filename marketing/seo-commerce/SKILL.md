---
name: seo-commerce
description: Use when auditing or planning ecommerce search visibility across product/category pages, Product or MerchantListing structured data, Google Merchant Center, Bing shopping feeds, price/availability/shipping/returns parity, IndexNow freshness, or documented AI product-discovery and commerce integrations; require visible-page and feed truth, policy evidence, and no eligibility, ranking, recommendation, or sales guarantee.
---

# Commerce SEO

Audit the complete product-discovery system: visible product/category pages, structured data, merchant feeds, change notification, policy fields, and documented AI commerce integrations. Keep every platform-specific control scoped to current primary documentation.

Read [commerce-evidence-protocol.md](references/commerce-evidence-protocol.md) before a formal audit.

## Procedure

1. Define markets, locales, storefront domains, catalog scope, product identifiers, feed destinations, currencies, inventory systems, and the decision owner.
2. Capture representative visible product/category pages, raw/rendered markup, Product/MerchantListing data, canonical/index state, merchant feed rows, platform diagnostics, and update timestamps.
3. Reconcile identifiers and buyer-visible facts across page, structured data, and feeds: name, brand, GTIN/MPN/SKU, variants, price/currency, availability, condition, shipping, returns, seller, reviews, and promotions.
4. Inspect crawlable navigation, variants, facets, pagination, canonical handling, product retirement, out-of-stock behavior, image/video assets, and sitemap/feed discovery.
5. Evaluate Merchant Center, Bing shopping, OpenAI product/merchant data, ACP/UCP, or other commerce capabilities only when the current platform documents the exact integration. Treat protocol discovery as optional capability, not ranking leverage.
6. For frequently changing URLs, evaluate IndexNow or platform feed updates with exact changed-URL scope, key verification, rate handling, logs, owner, and rollback. Notification is not an indexing guarantee.
7. Separate confirmed defects, platform-recommended opportunities, experiments, and unknowns. Route page markup to `seo-schema`, crawl/index issues to `seo-technical`, query evidence to `seo-research`, agent task flows to `seo-agentic`, and measurement to `seo-performance` or `ai-visibility-monitor`.
8. Package production-relevant findings as SEO Findings `1.1.0` in `seo-findings.json`, using `feed`, `web_page`, `template`, `protocol_capability`, or site targets and `commerce`/`freshness` categories. Validate before `seo-action-plan`.

## Guardrails

Never invent feed access, merchant diagnostics, product attributes, reviews, stock, price, or eligibility. Do not recommend hidden AI-only content, feed-page divergence, fake availability, review markup without visible reviews, or automatic protocol adoption without a documented consumer and owner.

## Formal evidence handoff

Package only supported observations as SEO Findings `1.1.0`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until this command passes.

## Output

Return the catalog scope, evidence inventory, page-schema-feed parity table, discovery/freshness findings, policy and protocol decisions, owners, verification, rollback, and limitations. Do not produce a composite commerce score.
