---
name: data-quality
description: Define and enforce data quality from explicit contracts and business invariants across completeness, validity, uniqueness, consistency, freshness, volume, and referential behavior.
---
# Data Quality

Use when a dataset or pipeline can technically complete while still producing incorrect, incomplete, stale, or misleading data.

## Procedure
1. Identify the dataset's consumers and decisions so quality rules protect meaningful outcomes rather than generic cleanliness.
2. Define required fields, types, domains, units, keys, uniqueness, referential relationships, temporal constraints, freshness, expected volume, and business invariants as applicable.
3. Classify checks by severity: reject/quarantine data that cannot be safely consumed, alert on suspicious drift, and record informational anomalies separately.
4. Place checks at the earliest boundary that can identify the responsible source while also validating important transformed/aggregate outputs downstream.
5. Establish baselines for distributions, volume, null rates, cardinality, lateness, and other signals where static rules cannot capture abnormal behavior.
6. Preserve bad records or diagnostic samples safely enough to investigate without allowing them to contaminate trusted outputs.
7. Attach owner, source, partition/batch/run, transformation revision, and other lineage context to failures so they can be traced.
8. Define response and recovery: source correction, quarantine release, rerun/backfill, downstream invalidation, or consumer notification depending on impact.
9. Test quality rules with intentionally bad fixtures and verify pipeline failure/quarantine semantics, not only rule logic.
10. Review rules as products, sources, and schemas change so stale checks do not create false confidence.

## Decision rules
- A successful job is not evidence that its data is correct.
- Quality rules should protect consumer semantics, not merely formatting preferences.
- Do not silently coerce invalid values into plausible defaults unless that behavior is part of the accepted contract.
- Quality alerts need ownership and recovery action or they become ignored noise.

## Quality gate
Data quality is adequate when important consumer invariants are encoded, failures are caught at useful boundaries, invalid data cannot silently enter trusted outputs, diagnostics identify source/run/context, recovery is defined, and injected bad-data tests demonstrate the controls work.