---
name: case-camouflage-skill
description: Use when Amazon Ads optimization analysis, recommendations, approval packets, demos, recordings, or public artifacts must preserve exact source KPIs while masking account/profile/project names, products, ASINs, SKUs, campaigns, ad groups, keywords, search terms, targets, placements, filenames, URLs, and source-derived identifiers. Produces masked approval packets only; it must not directly mutate Amazon Ads.
---

# Case Camouflage Skill

Use this skill when preparing Amazon Ads optimization output that may be shown to users, reviewers, public repos, demos, recordings, docs, or evals. The job is to camouflage the case context: keep optimization math real and exact while masking only user-facing labels and source-derived identifiers.

## Non-Negotiables

- Preserve exact KPIs and optimization logic. Do not fake, redact, perturb, swap, incorrectly merge, or round metrics for privacy.
- Analyze first with raw source IDs. Group, rank, attribute, diagnose, and decide before masking. Never group by masked handles.
- Mask display-plane labels and identifiers: account/profile/project names, products, ASINs, SKUs, campaigns, ad groups, keywords, search terms, targets, placements, filenames, URLs, and source-derived identifiers.
- Use stable tenant/profile-scoped handles such as `ACCOUNT-000001`, `PROFILE-000001`, `PRODUCT-000001`, `ASIN-000001`, `CAMPAIGN-000001`, `KW-000001`, and `TARGET-000001`.
- Do not expose registry mappings, real customer data, source IDs, credentials, raw reports, private execution manifests, HMAC digests, or raw API readbacks in public output.
- Do not directly mutate Amazon Ads. You may create masked approval packets and private execution manifests for a separate approved execution tool after explicit approval.

## Workflow

1. Confirm scope: tenant/profile, marketplace, date windows, available reports, requested output surface, and whether this is public/demo/recording output.
2. Load or configure a tenant-scoped masking registry. If text-only identifiers are present, require a per-tenant HMAC secret. See [registry](references/registry.md).
3. Run the optimization in the analytical plane using raw source IDs and exact metrics. See [metrics](references/metrics.md).
4. Resolve display handles only after analysis. See [masking](references/masking.md).
5. Build a masked approval packet for recommended actions. Keep private execution manifests in ignored private paths only. See [approvals](references/approvals.md).
6. Scan public artifacts, logs, stdout/stderr, rationales, readbacks, metadata, hidden sheets, and filenames before release. See [artifact/log safety](references/artifact-log-safety.md).
7. Report coverage with counts and statuses only, never mappings. See [coverage](references/coverage.md).

## Reference Map

- [Masking](references/masking.md): what must be masked, handle format, and display-plane rules.
- [Metrics](references/metrics.md): exact KPI preservation and source-plane grouping.
- [Registry](references/registry.md): providers, collisions, unsafe aliases, placeholders, planned reservations, activation, HMAC.
- [Approvals](references/approvals.md): approval packets, action IDs, private manifests, stale packets.
- [Lifecycle](references/lifecycle.md): analysis to approval to readback status flow.
- [Artifact And Log Safety](references/artifact-log-safety.md): scanners and public artifact release gates.
- [Codename Resolution](references/codename-resolution.md): replacing customer/project codenames with generic language.
- [Coverage](references/coverage.md): safe summaries and limitations.
- [Style](references/style.md): output tone and table requirements.

## Required Output Shape

For user-facing results, include:

- Scope and mode: `masked_output`, read-only, no Amazon Ads mutation.
- Data coverage and limitations.
- Source-plane diagnostic findings with masked handles and exact KPIs.
- Approval packet rows with `action_id`, masked profile/entity handles, current/proposed values, exact metrics, risk, preflight, readback, and monitoring.
- Execution gate: separate approved execution tool required; this skill did not write to Amazon Ads.
- Leak-scan result and registry coverage summary.

If a raw label or identifier appears in a draft, stop and remediate before showing it.
