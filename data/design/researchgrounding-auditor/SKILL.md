---
name: research/grounding-auditor
description: Audit outputs against provided sources, enforce grounding, and log an audit trail. Use when strict source fidelity is required.
---

# Grounding Auditor

Capabilities
- verify_claims: check outputs against trusted sources.
- cross_check: compare across multiple sources for consistency.
- log_audit: store audit events and unsupported claims.

Dependencies
- tangible-memory
- reliability-budget (optional accuracy SLOs)

Inputs
- outputs with citations, source chunks/paths.

Outputs
- audit report, unsupported items, stored log record.
