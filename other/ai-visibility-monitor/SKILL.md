---
name: ai-visibility-monitor
description: Measure repeatable AI-search mention, citation, answer accuracy, cited-source share, referral, retrieval traces, citation-to-claim support, uncertainty, and non-causal drift from a frozen, hash-pinned Query Corpus and contract-valid Research Pack. Use for AI visibility baselines, repeated engine/surface observations, citation monitoring, grounding-query or consulted-source capture when disclosed, access-gap reporting, or comparison runs. Do not use for live research, query discovery, optimization, access-control bypass, rankings, guarantees, or causal attribution.
---

# AI Visibility Monitor

Produce a hash-pinned Visibility Run from immutable research, a formal frozen Query Corpus, repeated raw answer captures, retrieval traces where the surface exposes them, and citation reviews. This skill measures what was observed; it does not prescribe changes or claim why a metric moved. Legacy `1.0.0` runs remain readable; create new work with schema `2.0.0`.

## Required inputs

- Require a contract-valid Research Pack produced by `ai-search-research`; bind its bundle-relative path and SHA-256 into every run.
- Require a valid `query-corpus.json` whose Research Pack hash matches, whose `frozen_at` precedes every observation, and whose selected query text, locale, engine, surface, entities, and `fact_ids` resolve. Do not invent hidden fan-out queries.
- Require dated raw answer captures for observed cells. Preserve inaccessible, blocked, unavailable, and error states as explicit null-answer observations.
- For a comparison, require the prior Visibility Run as an immutable hash-pinned artifact.
- Read [measurement-protocol.md](references/measurement-protocol.md) before collecting, scoring, or comparing observations.

## Procedure

1. Validate the complete Research Pack and its semantic provenance before measurement.
2. Freeze the query corpus before collection. Record timezone-aware `frozen_at`, hash it, and require `frozen_at <= observed_at` for every cell; never add, remove, reword, translate, or silently substitute a query during a run.
3. Declare planned/completed repeats, confidence method, confidence level, and fresh-session policy. Collect every query/engine/surface/locale/repeat cell without choosing the most favorable answer.
4. Record `observed_at`, access state, disclosed model, conversation turn, user location, device, authentication/personalization state, retrieval mode, collection method, and either a hash-pinned raw answer or access-attempt receipt.
5. Preserve only actually disclosed executed/grounding queries and consulted sources. Keep consulted sources distinct from visible citations. Never reconstruct hidden retrieval behavior.
6. Preserve every cited URL exactly as observed, derive its canonical form separately, and review each citation-to-claim link with a hash-pinned support verdict. Citation presence is not claim support.
7. Resolve mentioned entities only when a supplied Research Pack name or alias appears in the raw answer. Do not infer mentions from citations alone.
8. Score only explicit metrics using the canonical versioned `definition_id` and exact definition for that metric, with visible numerators, denominators, sample size, repeat count, confidence interval or a declared `not-estimated` state, results, and uncertainty notes. Missing access is not a negative result.
9. Check every fact declared for every observed corpus cell/repeat against Research Pack ground truth. Automatic `correct` requires both the extracted claim and complete normalized answer to equal the accepted value; bind every other verdict to a hash-pinned review artifact.
10. For comparisons, verify prior hash, identity, chronology, Research Pack and corpus hashes, repeat profile, metric definition, score target, access profile, and referral source/method/window duration. Mark changed cohorts non-comparable and explain the warning.
11. Describe movement as observational drift. Never state or imply that an optimization, publication, schema change, crawler setting, or other intervention caused movement.
12. Create schema `2.0.0` `visibility-run.json` with stable IDs, hash-pinned artifacts, explicit limitations, and no optimization recommendations.
13. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout. Run `python "<suite-root>/scripts/validate_ai_visibility_monitor.py" validate-run <artifact> --bundle <bundle>` and close all critical or important findings. Put minor findings in backlog.

## Metric boundaries

- `mention_rate`: share of eligible observed answers that explicitly mention one Research Pack entity.
- `citation_rate`: share of eligible observed answers containing at least one citation.
- `cited_source_share`: share of distinct canonical sources per observed answer matching one declared canonical source URL.
- `answer_accuracy`: share of all declared fact-to-observation checks assessed `correct`; `partial` and `unverifiable` remain in the denominator.
- `referral_rate`: use only when a hash-pinned referral envelope binds a supported raw event export. Recompute the numerator and denominator from eligible `ai`/`non_ai` events inside the declared window. Otherwise omit it.

Do not combine these metrics into a universal visibility score. Do not compare percentages whose corpora, access states, time windows, locales, or metric definitions are not comparable.

## Ownership boundaries

- Route new query discovery, source collection, or Research Pack repair to `ai-search-research`.
- Route direct-answer and extractability audits to `seo-aeo`.
- Route entity, evidence, citation-suitability, and documented engine-control audits to `seo-geo`.
- Route a validated audit and any needed baseline evidence to `seo-action-plan` before implementation; this monitor does not rewrite, optimize, or approve a change.

Never bypass authentication, bot controls, rate limits, paywalls, or unavailable product access. Record the access state and continue with the observable cohort.

## Severity and review rule

- `critical`: the run would be materially false, fabricated, unsafe, or unusable.
- `important`: provenance, denominator, raw-evidence binding, comparison integrity, or ownership is materially incomplete or misleading.
- `minor`: a non-blocking clarity or maintainability improvement.

Close critical and important findings. Backlog minor findings. Review each candidate hash at most twice.
