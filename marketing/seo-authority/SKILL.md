---
name: seo-authority
description: Use when auditing backlinks, referring domains, source citations, brand mentions, unlinked mentions, linkable assets, digital PR evidence, or off-site source landscapes from authorized first-party, Bing, vendor, or public evidence; preserve vendor metric definitions, detect manipulative risk, and never treat a proprietary authority score as universal truth or recommend link schemes.
---

# Authority and Source Landscape

Audit off-site evidence that helps users and systems verify an entity: genuine links, mentions, citations, source coverage, and risk. This skill does not manufacture authority.

Read [authority-evidence-protocol.md](references/authority-evidence-protocol.md) before a formal audit.

## Procedure

1. Define entity, domains, markets/locales, comparison scope, authorized data sources, time window, and the decision to make.
2. Preserve each link/mention row with source URL/domain, target URL/entity, anchor or mention text, first/last seen date when supplied, link attributes, source type, collection method, and limitations.
3. Normalize URLs without discarding raw values. Separate backlinks, citations, unlinked mentions, syndication, scraper copies, social/profile links, and self-controlled properties.
4. Evaluate source relevance, editorial independence, claim support, topical/locale fit, target-page usefulness, and visible context. Keep proprietary authority/risk/traffic metrics labeled with vendor and date.
5. Identify broken earned links, incorrect entity facts, missing first-party evidence, unsupported claims, spam patterns, paid/sponsored disclosure, and link-scheme risk.
6. Recommend source-worthy first-party assets, corrections, reclamation, documentation, partnerships, or editorial outreach only when truthful and policy-safe. Do not prescribe volume quotas or paid/manipulative links.
7. Route entity/citation suitability to `seo-geo`, competitor-page copy to `seo-competitor-pages`, content assets to `seo-content`, and internal links to `seo-architecture`.
8. Package findings as SEO Findings `1.1.0` with `backlink_profile`, `content_set`, `web_page`, or `site` targets and `authority`, `entity`, `content`, or `policy` categories.

## Formal evidence handoff

Package only supported observations as SEO Findings `1.1.0`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until this command passes.

## Output

Return the source and scope, normalized link/mention inventory, source-quality and claim-support observations, risk patterns, evidence gaps, owners, verification, and limitations. Never collapse the result into a universal domain-authority score.
