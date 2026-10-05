---
name: seo
description: The autonomous front door and end-to-end orchestrator for any SEO, AEO, GEO, or AI-search request. Translate ordinary user goals into a complete 27-skill coverage screen, execute every applicable specialist workflow, carry evidence and handoffs internally, and return one consolidated result to the authorized boundary; direct specialist invocation remains optional. Do not create a universal score, unsupported control, causal uplift claim, or placement guarantee.
---

# SEO Router

Use `seo` as the default front door and user-facing owner for every request in this suite: a narrow technical question, a content review, an AI-search investigation, a multi-team plan, or an end-to-end authorized change. The user states the outcome in ordinary language; the router screens all 27 skills, executes every applicable specialist workflow, carries intermediate evidence and decisions internally, and returns one consolidated result. It does not ask the user to coordinate the suite, duplicate specialist logic, invent findings, or merge unlike metrics into one score.

Read [autonomous-orchestration-contract.md](references/autonomous-orchestration-contract.md) for every request before selecting or executing specialist lanes.
Read [routing-matrix.md](references/routing-matrix.md) before routing a request through the suite.
Read [decision-and-release-contract.md](references/decision-and-release-contract.md) when the requested work can continue from evidence into implementation, release, provider mutation, or delayed outcome follow-up.

## User burden boundary

- Never require the user to know whether their problem is SEO, AEO, GEO, AI-search, technical, content, authority, or measurement.
- Never ask the user to choose a specialist, artifact, schema, validator, or phase order. Infer and manage those internally.
- Ask only for material business truth, inaccessible data/access, an outcome-changing choice, cost-bearing action, or authorization that cannot be safely inferred.
- A direct specialist call remains supported for expert users, but it is never a prerequisite for complete work through `seo`.

## Routing procedure

1. Translate the user's ordinary-language goal into the requested outcome and authorized boundary: answer, research, audit, decision, strategy, measurement, implementation, release verification, provider operation, follow-up, or end-to-end completion.
2. Inspect available site/repository/data context before asking questions. Infer the surface, locale, verticals, technical system, and affected scope; ask only for non-discoverable material facts or permissions.
3. Create the 27-skill coverage ledger from the autonomous orchestration contract. Mark every capability `required`, `active`, `completed`, `not-applicable`, `blocked`, or `deferred-by-owner` with evidence or a reason. A broad request cannot skip the screen; a narrow request still receives the screen internally.
4. Build the dependency graph and load each required specialist's full `SKILL.md` before executing that lane. The router—not the user—invokes or performs the next specialist workflow and transfers its evidence/artifacts.
5. For a broad request to rank higher, improve organic visibility, or optimize a site/page, establish the intended query families with `seo-research`, review the page's search-result presentation with `seo-page` and `seo-content`, and verify hostname-level favicon/site identity with `seo-technical`. Require two concurrent opportunity tracks: evidence-backed nearer-term gains and high-volume head-term/category leadership. Preserve every owner-declared relevant high-volume family as a required strategic target; current difficulty or an authority gap changes the work and sequence, not whether the target is analyzed. Do not let a broad closeout omit title, descriptive meta description, favicon, canonical/indexability, or query-to-page ownership merely because each item is individually simple. Do not let easier work replace or hide the head-term leadership track. A deliberately narrow request remains narrow.
6. For compound optimize-and-track work, use this phase order: `research -> audit -> baseline measurement -> product-owner decision -> action planning -> authorized implementation -> local acceptance -> authorized release -> live delivery verification -> authorized provider operation -> delayed outcome follow-up`.
7. Require each phase's real artifact or explicit limitation before starting a dependent phase. AEO/GEO work hands off a validated `optimization-brief.json`; conventional SEO lanes hand off a validated `seo-findings.json` bundle. Reuse an existing goal, issue, or Action Plan when it already records the full decision; otherwise add the short decision record defined in the decision-and-release contract. Do not let a downstream specialist silently repair missing upstream evidence or self-approve a change.
8. Continue through every safe read-only/local and explicitly authorized phase while useful work remains. Evaluate authorization separately for implementation, release, and provider mutation. When later authorization arrives, resume the same decision and candidate chain rather than restarting or substituting work.
9. Parallelize only independent lanes when the runtime permits it. Keep the final synthesis with the router, preserve disagreements instead of averaging them away, and do not expose intermediate handoff work as user homework.
10. Close critical and important findings before release; record minor findings in backlog. Review one candidate hash at most twice. Finish with one consolidated outcome and, for broad work, a compact 27-skill coverage summary.

For broad or end-to-end work, make the coverage screen executable when Python 3.11+ is available. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root`; otherwise use the absolute repository checkout. Create the draft with `python "<suite-root>/scripts/manage_orchestration_ledger.py" init --output <work-dir>/orchestration-ledger.json --request "<plain-language outcome>" --mode <broad|end-to-end> --authorized-boundary "<boundary>"`, fill every row from observed scope and lane evidence, then run `python "<suite-root>/scripts/manage_orchestration_ledger.py" validate <work-dir>/orchestration-ledger.json` before closeout. Do not expose this internal bookkeeping as user homework. If Python is unavailable, preserve the same ledger internally and label the formal coverage handoff provisional.

## AI-search routes

- Missing queries, sources, observations, ground truth, or engine/surface evidence -> `ai-search-research`.
- Direct-answer completeness, clarity, extractability, intent coverage, or answer structure -> `seo-aeo`.
- Entity consistency, evidence traceability, citation suitability, cited-source alignment, or documented engine controls -> `seo-geo`.
- Repeatable mention, citation, accuracy, referral, retrieval trace, consulted-source, citation-claim, access, uncertainty, baseline, comparison, or drift measurement -> `ai-visibility-monitor`.
- Approval-ready sequencing, ownership, risk, rollback, verification, or a cross-team implementation handoff -> `seo-action-plan`.

Do not treat AEO and GEO as synonyms. Do not send live research to an audit skill, implementation to the monitor, or measurement to an optimization audit.

## Existing SEO routes

- Full multi-lane site assessment -> `seo-audit`.
- One page with mixed on-page concerns -> `seo-page`.
- Crawlability, indexability, rendering, robots, canonicalization, performance, headers, or directives -> `seo-technical`.
- Content quality, helpfulness, E-E-A-T, topical coverage, or editorial remediation -> `seo-content`.
- Structured data detection, validation, or generation -> `seo-schema`.
- Image discovery, formats, dimensions, alt text, or media performance -> `seo-images`.
- XML sitemap analysis or generation -> `seo-sitemap`.
- International targeting and language-region annotations -> `seo-hreflang`.
- Strategic roadmap and prioritization -> `seo-plan`.
- Template-driven or large-scale landing-page systems -> `seo-programmatic`.
- Competitor comparison or alternative pages -> `seo-competitor-pages`.
- Long-form query and evidence discovery -> `seo-research` when AI-search Research Pack provenance is not required.
- Evidence-backed selection of primary query families, high-volume head-term/category leadership targets, near-win queries, snippet/CTR opportunities, coverage gaps, or cannibalization targets -> `seo-research`, using first-party query/page data when available and a dated locale/device SERP review before implementation. Add `seo-authority`, `seo-architecture`, and the relevant content/vertical owner when the leadership gap crosses those surfaces.
- Search Console, Bing Webmaster Tools, analytics, indexation, Core Web Vitals/RUM, conventional baseline, or comparison measurement -> `seo-performance`.
- Explicitly authorized Search Console, Bing Webmaster Tools, or IndexNow property mutation and its separate receipt -> `seo-performance`; implementation or deployment authorization alone is insufficient.
- Import or normalize an authorized Search Console, Bing, organic GA4, crawler CSV, or server log -> the matching `seo-performance`, `seo-architecture`, or `seo-technical` owner using the suite data-import adapter; import is evidence preparation, not a validated finding or outcome.
- Product/category pages, Product/MerchantListing data, merchant feeds, price/availability parity, shopping discovery, commerce protocols, or IndexNow catalog freshness -> `seo-commerce`.
- Business profiles, NAP/hours/categories, service areas, location pages, local schema, reviews, or location-aware queries -> `seo-local`.
- Watch pages, video players, VideoObject, video sitemaps, thumbnails, transcripts/captions, Key Moments, livestreams, or video indexing -> `seo-video`.
- News/Discover publisher policy, articles, dates/bylines/corrections, NewsArticle, news sitemaps/feeds, large images, paywalls, or freshness reporting -> `seo-news-discover`.
- Agent perception and task completion through DOM/accessibility/UI state, safe forms, auth/consent, or documented UCP/ACP/MCP/A2A capabilities -> `seo-agentic`.
- Site graphs, navigation, hubs, crawl paths, orphan evidence, facets, taxonomy, pagination, internal links, or query-to-page architecture -> `seo-architecture`.
- Backlinks, referring domains, source citations, brand/unlinked mentions, linkable evidence, digital PR, or link-scheme risk -> `seo-authority`.
- Optional `llms.txt` suitability, generation, validation, publishing, or maintenance -> `seo-technical`; offer it as a low-cost maintained publisher guide when public sources and a refresh owner exist, not as a universal crawler or visibility control.
- Site migration/replatforming, sudden traffic/indexation incident, manual action, or hacked-site search recovery -> `seo-technical`; involve the security incident owner for any suspected compromise.
- Controlled SEO experiment design, baseline, or evaluation -> `seo-performance`; require `seo-action-plan` before exposure and `seo-technical` when variant delivery, redirects, canonicals, or directives are involved.
- Broad implementation optimization after a validated, approved action plan -> `optimise-seo`.
- Release of an identified candidate and scope-matched live closeout -> `optimise-seo` coordinated with `seo-technical`; provider mutation remains separately owned by `seo-performance`.

## Compound-work rules

- If the request lacks current evidence, run `ai-search-research` before `seo-aeo`, `seo-geo`, or `ai-visibility-monitor`.
- AEO and GEO may run in parallel only after both receive the same validated Research Pack and immutable target captures.
- Convert validated findings into an action plan before implementation. Use a validated `optimization-brief.json` for AEO/GEO findings or a validated `seo-findings.json` bundle for conventional SEO findings. Run implementation only from an approved action with an explicit owner, acceptance criteria, verification, and rollback. Keep experiments separate from required changes.
- Preserve an explicit product-owner end state. “Smallest reversible change” limits implementation inside that decision; it does not authorize replacing a corpus-wide or otherwise explicit end state with a narrower one.
- Establish a formal Query Corpus and the correct baseline before implementation when the user wants change tracking. Use `seo-performance` for conventional first-party search/site metrics and `ai-visibility-monitor` for observed AI answers; never merge them into one score. A later comparison is observational drift, not causal proof.
- Keep `implemented-locally`, `delivered-and-verified`, and `provider-outcome-pending/observed` as separate closeout states. Deployment, sitemap submission, URL notification, or provider acceptance never proves crawling, indexing, ranking, retrieval, citation, referral, or conversion.
- Use the current validated platform-controls registry before feature, crawler, change-notification, or protocol recommendations. Route expired or unknown controls back to research instead of copying a stale rule.
- If access is blocked or unavailable, record the gap; never bypass authentication, paywalls, bot controls, or rate limits.

## Guardrails

Do not create a universal SEO score or blend technical, content, AEO, GEO, and visibility metrics into a false precision number. Decline mandatory `llms.txt`, fixed passage or word-count formulas, blanket crawler instructions, invented ranking factors, unsupported source percentages, guaranteed rankings, guaranteed mentions, guaranteed citations, or any guarantee of AI placement. Offer `llms.txt` as an optional, evidence-scoped publisher guide when trustworthy public sources, a defined scope, and a maintenance owner make it cheap to keep correct; a documented consumer is useful but not required. A bot request is not evidence of retrieval, citation, referral, or conversion.

When an existing specialist owns the next step, the router loads and executes that specialist workflow without duplicating its instructions or asking the user to make the handoff. Directly invoking that specialist remains available, but `seo` is the complete default entry point when the user wants one request handled through the full applicable system.
