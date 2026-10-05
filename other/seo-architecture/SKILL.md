---
name: seo-architecture
description: Use when auditing or designing site architecture, internal-link graphs, crawl depth, orphan pages, hubs, navigation, contextual anchors, pagination, facets, taxonomy, template links, or URL-to-query coverage at scale; require a bounded captured graph and business/user rationale rather than arbitrary click-depth, link-count, or PageRank-like score targets.
---

# SEO Architecture

Create and audit a bounded `site-graph.json` that explains how users and permitted crawlers discover important pages, how templates connect, and where query/entity coverage lives.

Read [site-graph-protocol.md](references/site-graph-protocol.md) before a formal architecture audit.

## Procedure

1. Define domain/subdomain scope, environments, URL patterns, crawl authorization, seed pages, locale, user tasks, business-critical templates, exclusions, and collection limits.
2. Capture nodes and crawlable link edges with source/target URLs, link location, anchor or accessible name, follow state, template/context classification, and observation time.
   A supported crawler CSV can be normalized with `python "<suite-root>/scripts/import_seo_exports.py" crawler-csv ...` using `<suite-root>/docs/DATA-IMPORT-ADAPTERS.md`, but that observation envelope is not a Site Graph: bind every node and edge to the raw captures and metadata required by the Site Graph contract.
3. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Validate the graph with `python "<suite-root>/scripts/validate_site_graph.py" validate-graph <bundle>/site-graph.json --bundle <bundle>`.
4. Inspect disconnected/orphan nodes, inbound-path evidence, hubs, crawl paths, pagination, facets, filters, parameter spaces, taxonomy, duplicate routes, canonical/index conflicts, and locale clusters.
5. Map the formal Query Corpus and entity/page ownership to nodes. Do not create a page or link merely because a keyword exists.
6. Propose the smallest user-meaningful navigation/contextual-link change. Avoid sitewide boilerplate links, manipulative anchors, hidden links, or arbitrary depth/count thresholds.
7. Route crawl/index defects to `seo-technical`, page/content ownership to `seo-page`/`seo-content`, programmatic templates to `seo-programmatic`, and authority work to `seo-authority`.
8. Package findings as SEO Findings `1.1.0` with `site_graph`, `site`, `template`, or `web_page` targets and `architecture`, `technical`, `content`, or `international` categories.

## Formal evidence handoff

After graph validation, package only supported observations as SEO Findings `1.1.0`. Using the same `<suite-root>` definition above, run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until both validators pass.

## Output

Return the validated graph, scope and coverage, important node/edge findings, orphan/discovery evidence, taxonomy/facet risks, query/entity mapping, owners, verification, rollback, and limitations. Do not publish a composite authority or architecture score.
