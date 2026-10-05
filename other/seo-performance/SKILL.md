---
name: seo-performance
description: Use when establishing or comparing conventional SEO performance from authorized Google Search Console, Bing Webmaster Tools, analytics, server-log, indexation, or Core Web Vitals/RUM evidence, or when designing and evaluating a controlled SEO experiment; preserve dimensions and data-quality limits, keep metric families separate, and never turn observational movement into a causal or composite SEO score.
---

# SEO Performance

Build a hash-pinned `seo-performance-run.json` from authorized first-party exports. Measure conventional search behavior, indexation, user experience, and organic outcomes without blending them into AI visibility metrics or implying that an intervention caused movement.

Read [performance-measurement-protocol.md](references/performance-measurement-protocol.md) before normalizing, comparing, or interpreting data.
For a controlled SEO experiment, also read [controlled-seo-experiment-protocol.md](references/controlled-seo-experiment-protocol.md) before assigning cohorts or declaring an outcome.
For an explicitly authorized Search Console, Bing Webmaster Tools, or IndexNow operation, read [provider-operations-protocol.md](references/provider-operations-protocol.md) immediately before touching the property.

## Required inputs

- Require the exact property, source, time window, timezone, dimensions, export method, and collection time.
- Preserve the provider export, then create the versioned normalized JSON source envelope used by the run and bind that envelope with SHA-256. The run's rows, indexation observations, and Web Vitals must match it exactly.
- Record query anonymization, row limits, sampling, canonical aggregation, and missing dimensions explicitly.
- Require the prior hash-pinned run for comparisons. Never compare unlike properties, sources, dimensions, or window durations without marking them non-comparable.

## Procedure

1. Define the decision and the smallest useful metric family: search performance, indexation, field experience, organic sessions, conversion, or a bounded combination. For broad organic growth, preserve separate cohorts for nearer-term opportunities and the approved high-volume head-term leadership families; a currently absent head term remains a measured zero/unknown visibility target rather than disappearing from the baseline.
2. Capture the authorized provider export without changing its rows. Redact secrets, personal data, account identifiers, and sensitive query data where required; record the resulting limitation. Create a normalized JSON source envelope with source/property/window/dimensions plus the exact rows, indexation, and Web Vitals used by the run; hash-pin it and retain the provider export beside it when permitted.
   When the input is a supported Google Search Console, Bing Webmaster Tools, or organic GA4 CSV, use `python "<suite-root>/scripts/import_seo_exports.py" <adapter> ...` and follow `<suite-root>/docs/DATA-IMPORT-ADAPTERS.md`. Inspect the normalized envelope before using it; an imported envelope is evidence input, not a validated Performance Run.
3. Normalize only declared dimensions. Keep query, page, country, device, search appearance, and date distinct. Preserve platform aggregation rules.
4. Recompute CTR from clicks and impressions. Keep clicks, impressions, CTR, average position, sessions, conversions, revenue, indexation, and Web Vitals as separate measures.
   When an eligible property exposes Google Search Console's dedicated generative-AI performance preview or Bing's AI Performance report, preserve its availability, preview status, platform definitions, and supported dimensions as a separate first-party metric view. Do not infer unavailable queries or merge provider-reported visibility with observed AI answers.
5. For a baseline, record no prior run or drift. For a comparison, verify prior identity, hash, chronology, property, source, dimensions, and equal window duration before calculating descriptive deltas.
6. Describe movement as observational association. Record confounders such as demand, seasonality, reporting changes, access changes, migrations, campaigns, or incomplete query data.
7. Create `seo-performance-run.json`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_performance.py" validate-run <bundle>/seo-performance-run.json --bundle <bundle>`.
8. Route evidence-backed issues to the relevant audit owner and then `seo-action-plan`. Route AI mention/citation observations to `ai-visibility-monitor`; never merge the two reports into one score.

## Provider operations mode

Treat provider mutation as a separate mode, not as measurement or implied closeout. Verify the exact property and current documented capability at mutation time; capture pre-state; restate the authorized action and target set; execute only that set; record the provider receipt/time/status, partial failures, and post-state; then validate a separate `provider-operation-receipt.json`. Search Console sitemap submission, URL Inspection, recrawl/validation UI flows, Google's restricted Indexing API, Bing submission, and IndexNow have different capabilities—never substitute one for another.

Let `<suite-root>` use the same resolution rule as above, then run `python "<suite-root>/scripts/validate_provider_operation.py" validate-receipt <bundle>/provider-operation-receipt.json --bundle <bundle>`. A receipt is not a Performance Run. Provider acceptance is not crawl, indexing, serving, citation, referral, traffic, or conversion; schedule those as separately observed follow-ups and preserve provider lag.

For an experiment, predeclare the hypothesis, assignment unit, eligible cohort, primary outcome, guardrails, duration/stopping rule, confounders, and rollback before implementation. Require verified exposure and a comparable holdout or label the result observational; do not retrofit causation after seeing a favorable delta.

## Boundaries

Search Console and Bing metrics are platform-defined observations. Average position is not a fixed rank. A canonical URL row is not proof of every variant's behavior. A crawler request is not indexation, citation, referral, or conversion. An answer citation is not an organic visit.

Do not invent missing exports, reconstruct hidden queries, bypass property access, or claim ranking, traffic, revenue, or conversion guarantees.

## Output

Return the validated run, source and window, measured dimensions, separate metric tables, data-quality limits, comparable drift when available, and the next evidence owner. When broad-growth tracks were declared, report nearer-term and head-term cohorts separately and retain missing/zero-visibility strategic queries as explicit limitations or research/measurement dependencies. In provider-operations mode return the separately validated receipt, exact property/targets, response and failures, pending outcome states, and follow-up owner. Keep conclusions no stronger than the supplied data.
