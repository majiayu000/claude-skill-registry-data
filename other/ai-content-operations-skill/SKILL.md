---
name: ai-content-operations-skill
description: Design, implement, audit, or operate a complete AI-assisted website content system covering topic queues, scheduled article generation, editorial and factual quality gates, publishing, live verification, Google Sheets tracking, and weekly topic-cluster governance. Use when an agent needs to build or improve automated content operations, daily publishing workflows, content QA, editorial ledgers, SEO/AEO governance, internal-link governance, or cannibalization controls for a content website.
---

# AI Content Operations

Build a content supply chain, not a one-shot writing prompt. Keep generation, validation, publishing, live verification, tracking, and weekly governance as separate stages with explicit state transitions.

## Start here

1. Inspect the target repository, deployment path, content format, existing automation, analytics, and credentials interface.
2. Read [references/architecture.md](references/architecture.md) to map the system and ownership boundaries.
3. Read only the references needed for the requested work:
   - Daily generation and publishing: [references/daily-pipeline.md](references/daily-pipeline.md)
   - Editorial, factual, SEO, and public-copy gates: [references/quality-gates.md](references/quality-gates.md)
   - Google Sheets tracking and idempotent sync: [references/google-sheets.md](references/google-sheets.md)
   - Weekly clusters, internal links, and cannibalization: [references/weekly-governance.md](references/weekly-governance.md)
   - Installation and rollout: [references/adoption.md](references/adoption.md)
4. Copy and adapt the contracts in `assets/`; never hard-code a production spreadsheet ID, service-account JSON, provider key, site origin, or brand-specific prompt.
5. Run `scripts/validate_content_record.py` against representative records and `scripts/audit_content_clusters.py` against the full content index before enabling writes.

## Required operating model

Use this state machine:

`planned -> drafting -> generated -> validated -> committed -> deployed -> live_verified -> tracked`

Allow `blocked`, `failed`, and `needs_review` from every mutating stage. Never mark an item published or tracked before the corresponding evidence exists.

## Daily run

1. Lock the pipeline so two runs cannot publish the same topic.
2. Select one `planned` queue item or an explicit operator override.
3. Compare its primary intent with recent titles, summaries, FAQs, key insights, and cluster metadata. Refine or reject overlapping topics.
4. Generate structured output that separates public copy from internal governance metadata.
5. Create or select a unique cover image and keep article, Open Graph, and tracker URLs consistent.
6. Run deterministic gates before any commit. Fail closed on missing sources, invalid contracts, leaked internal metadata, broken links, or build failures.
7. Rebuild every derived artifact used by the live site: index, search data, HTML, structured data, sitemap, feed, and production build.
8. Commit and push only the validated artifact set. Rebase safely if the target branch moved.
9. Poll the canonical public URL and verify status, canonical, metadata, structured data, and visible content.
10. Upsert the tracking row by stable article ID or canonical URL. Record commit, deployment run, verification result, and review state.
11. Advance the queue item only after successful publication; send a concise notification if configured.

## Quality policy

- Treat model output as an untrusted draft.
- Require source URLs and freshness context for prices, laws, grants, health, finance, product specifications, research, comparisons, reviews, and affiliate claims.
- Distinguish hard failures from warnings. Hard failures block publication; warnings create review work.
- Keep `clusterRole`, `primaryIntent`, cannibalization notes, review notes, and link-role labels out of public copy.
- Require a clear reader problem, direct answer, actionable next step, limitations, disclosure where relevant, and intentional internal links.
- Validate repository artifacts and live behavior. A successful commit is not proof of a successful publication.

## Tracking policy

- Make the repository the source of truth for content; use Sheets as the operational view unless the adopter explicitly chooses another authority.
- Use deterministic headers and idempotent upserts. Update existing rows when metadata changes; append only when the stable key is absent.
- Provide dry-run mode and reject local production writes unless explicitly enabled.
- Support full backfill so missed webhook or workflow runs are recoverable.
- Store references to secrets, never secrets themselves.

## Weekly governance run

1. Rebuild all derived content artifacts.
2. Identify content created or materially changed during the review window.
3. Group the full corpus by cluster and role: `core`, `supporting`, `conversion`, `regional`, or `update`.
4. Detect intent overlap using normalized metadata; treat similarity as a review signal, not an automatic deletion decision.
5. Enforce a bounded set of core pages per hub and default new daily articles to `supporting`.
6. Review role-based internal links, orphan pages, missing cluster coverage, stale claims, and conversion paths.
7. Produce a human-readable governance report and machine-readable findings.
8. Apply only deterministic safe changes automatically. Route merges, redirects, canonical changes, noindex, and deletion to explicit review.

## Release safeguards

- Keep generation, deployment, tracking, and governance jobs independently retryable.
- Use concurrency groups and do not cancel an in-progress publishing mutation.
- Stage an explicit allowlist of generated files; do not commit unrelated worktree changes.
- Verify that deployed code, deployed content contracts, and live behavior agree after contract changes.
- Stop and report if tests fail, authentication is missing, a rebase conflicts, the live site remains stale, or the tracking destination rejects the contract.

## Completion evidence

Report the queue item, generated files, validation results, commit, deployment/run identifier, public URL, live verification, tracking upsert, and outstanding weekly-governance work. Do not report success from local generation alone.
