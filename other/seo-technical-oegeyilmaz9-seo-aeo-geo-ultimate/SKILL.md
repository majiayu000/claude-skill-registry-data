---
name: seo-technical
description: Use when investigating crawlability, indexability, canonicalization, rendering, performance, redirects, directives, sitemaps, crawler controls, site migrations, sudden traffic/index incidents, manual actions, hacked-site recovery, or when evaluating, generating, validating, publishing, and maintaining an evidence-scoped llms.txt publisher guide; return safe, testable implementation recommendations rather than a generic technical score.
---

# Technical SEO

## Purpose

Diagnose concrete technical behavior from headers, raw and rendered pages, robots files, sitemap inventories, application configuration, field data, logs, and platform documentation. Create scoped implementation recommendations; do not deploy code, alter production directives, or claim an indexing/ranking outcome.

For an optional `llms.txt` request, create a maintained publisher guide—not a crawler directive or promised visibility control. Recommend it as a reasonable low-cost future-readiness layer when it can stay aligned with truthful public sources and has a maintenance owner; a documented consumer strengthens the case but is not mandatory.

Read `references/technical-evidence-protocol.md` before a formal technical audit.
Read [external-claim-adjudication.md](references/external-claim-adjudication.md) when evaluating third-party audit or scanner claims.
Read [live-verification-matrix.md](references/live-verification-matrix.md) before closing a released technical, template, redirect, sitemap, canonical, hreflang, or indexability change.
Read [favicon-search-protocol.md](references/favicon-search-protocol.md) when a site lacks a search-result icon, has the wrong icon, or a broad site optimization includes hostname identity.
For feature lifecycle, crawler, IndexNow/change notification, or protocol-capability work, also read [platform-control-protocol.md](references/platform-control-protocol.md) and validate the current registry before recommending a control.
For `llms.txt` suitability, generation, validation, or publishing, read [llms-txt-protocol.md](references/llms-txt-protocol.md) and use its bundled template and validator.
For a migration/replatforming, sudden traffic or indexation incident, manual action, or hacked-site recovery, read [migration-and-recovery-protocol.md](references/migration-and-recovery-protocol.md) before recommending or approving a response.

## Evidence before recommendations

Collect the affected URLs, expected state, locale/device where relevant, timestamp, HTTP response/headers, raw HTML, rendered output when JavaScript is involved, canonicals/robots directives, sitemap membership, redirects, and any authorized first-party reporting. For performance, distinguish lab diagnostics from field/user data. For crawler behavior, distinguish a request in logs from a search/index/AI-answer outcome.

Supported crawler CSV and Apache/Nginx access logs can be normalized with `python "<suite-root>/scripts/import_seo_exports.py" crawler-csv ...` or `server-log ...`; follow `<suite-root>/docs/DATA-IMPORT-ADAPTERS.md`. These adapters preserve provenance and privacy boundaries but deliberately do not fabricate HTML captures, a Site Graph, indexation, crawler identity, or performance outcomes.

If evidence is unavailable, give a safe collection plan—not a guessed fix. Never bypass authentication, rate limits, paywalls, WAF controls, or robots rules to create evidence.

## Workflow

1. **State the expected behavior.** Is the URL intended to be indexable, canonical, localized, discoverable, rendered, fast enough for users, or excluded? Identify the owner/system that can change it.
2. **Capture the actual behavior.** Record raw response, directives, canonical, rendered content, redirect chain, linked/sitemap evidence, hosting/CDN behavior, and relevant device/locale. Keep transient tool errors separate from confirmed defects and identify the layer each claim measures.
3. **Find the smallest cause.** Test conflict pairs such as `noindex` vs canonical, raw vs JavaScript-injected metadata, redirect target vs sitemap URL, or locale target vs hreflang cluster. Do not infer a cause from a single score or generic audit rule.
4. **Classify the change or external claim.** Use confirmed defect, layer mismatch, supported opportunity, false positive, or unverified. Only a confirmed defect is automatically required. Link platform-specific controls to current primary documentation.
5. **Plan the implementation.** For every recommendation state the affected URLs/templates, owner, precondition, exact desired state, verification capture, risk, approval, and rollback. Route cross-team work through `seo-action-plan`.
6. **Verify after change.** Match the verification universe to the change universe: one page for a page-only edit, the affected route class for a shared template/resolver, and the full corpus or justified closed population for sitemap/index contracts. Re-capture raw, hydrated, hosting/CDN, and provider layers in scope. Verify redirects by status, `Location`, sitemap exclusion, and target state rather than by document-only metadata. Discovery, crawling, indexing, performance, and AI visibility are separate outcomes.

For migrations and incidents, preserve a last-known-good state, exact change timeline, affected cohorts, launch/rollback criteria, and unresolved competing hypotheses. For a compromise, security containment and root-cause remediation own the response; SEO verification follows rather than replacing them.

## Technical domains

- **Crawl/discovery:** robots handling, internal discovery, server health, sitemap inclusion, redirects, and crawl-access failures.
- **Index/canonical:** canonical/noindex conflicts, duplicate URL handling, status codes, redirects, and content availability.
- **Rendering:** raw versus rendered title, robots, canonical, meaningful content, and structured data; use actual captures rather than framework assumptions.
- **Search-result identity:** hostname home-page favicon declaration, icon response/format/dimensions, stable URL, crawl access, and representative brand asset. Do not mark favicon work complete from a file existing somewhere in the repository.
- **Experience:** responsive layout, interaction and rendering diagnostics, and field data where available. Core Web Vitals and tests guide improvement; they do not guarantee a ranking result.
- **International:** send locale clusters and annotations to `seo-hreflang`; do not repair language targeting from a single URL.
- **Structured data:** send truthful markup changes to `seo-schema`; validate the visible page and eligible documentation first.
- **Optional machine-readable guide:** for `llms.txt`, assess public source-of-truth coverage, inclusion/exclusion policy, freshness, owner, and release path. When upkeep is low-cost and reliable, offer and generate it as future-readiness even without a confirmed consumer. Keep it separate from robots, access controls, and promises of ranking, retrieval, or citation.

## llms.txt publication workflow

Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout.

1. Inventory the canonical public resources a client should understand; exclude private, authenticated, staging, personalized, ephemeral, and security-sensitive URLs.
2. Name the maintenance owner and the source changes that must trigger regeneration or review.
3. Copy `<suite-root>/skills/seo-technical/assets/llms.txt.template`, replace every placeholder from the public source of truth, and keep only useful absolute HTTPS links.
4. Validate the candidate with `python "<suite-root>/scripts/validate_llms_txt.py" validate-file <site-root>/llms.txt`.
5. Deliver or publish it at `/llms.txt` only within the authorized scope. Verify the live response and add the file to the ordinary documentation/content release path.
6. Describe the file as an optional publisher guide. Google currently documents that it ignores the file for Search visibility; do not convert its existence into a ranking, retrieval, citation, or traffic claim.

## Crawler-control policy

Treat crawler controls as an explicit business, legal, privacy, and technical decision. Identify the exact current documented user-agent and its declared purpose before proposing a rule. Training, search indexing, user-initiated fetches, and product-specific controls can be different agents. The Robots Exclusion Protocol is crawler guidance, not authorization or proof of downstream behavior.

Do not copy a blanket AI-bot block/allow template, assume a bot token is stable, or claim that blocking/allowing a bot changes citations. Crawler-control, `noindex`, canonical, robots, and WAF changes are high-risk and require an approved action plan, test URL, rollout/rollback, and current vendor documentation.

Using the same `<suite-root>` definition, before a feature, crawler, change-notification, or protocol decision, run `python "<suite-root>/scripts/validate_platform_controls.py" validate-registry "<suite-root>/manifests/platform-controls.json" --bundle "<suite-root>/manifests" --as-of <current-UTC-time>`. Treat an expired registry or unknown control as a research gap. Copy a registry row into a site-specific decision only after adding the actual owner, evidence, scope, and approval; the shipped registry deliberately leaves business decisions undecided.

For IndexNow or another notification path, submit only added, updated, or deleted URLs within the documented scope. Verify key/endpoint ownership, response receipts, rate/error handling, logs, and rollback. Notification proves a request was sent or received, not crawling or indexing.

## Formal evidence handoff

When this work needs a cross-team, approval-ready plan, package evidence-bound findings as an immutable `seo-findings.json` bundle using the checked-out suite contract. Keep every referenced capture/source below `raw/`, retain declined claims and limitations, and run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Send only a passing bundle to `seo-action-plan`; otherwise label the handoff `provisional`.

## Live release verification

After a separately authorized release, verify the exact candidate/deployment identity using [live-verification-matrix.md](references/live-verification-matrix.md). For the raw HTTP and sitemap layer, run `python "<suite-root>/scripts/verify_live_release.py" verify --plan <release-plan.json> --output <live-release-report.json>`. Bind approved per-page copy with `expected_title`, `expected_description`, and `expected_h1` overrides so a stale, generic, or truncated live value cannot pass merely because the element exists. When hostname identity is in scope, declare `site_identity` in the plan so the verifier checks the home-page icon link, exact favicon response, content type, square dimensions, and configured quality floor. A passing report proves only the declared live delivery checks; it does not prove crawl, index, rank, retrieval, citation, referral, or conversion.

## Output

For each finding provide: observed evidence and timestamp; expected state; scope; confidence/limitation; proposed owner/action; verification; risk; and rollback. When requested and supportable, also return the validated `llms.txt`, its included/excluded source map, owner, and refresh triggers. Group only by priority/owner, never a blended technical score. Route broader page/editorial questions to `seo-page` or `seo-content`.
