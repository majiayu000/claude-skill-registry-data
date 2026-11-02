---
name: log-redaction-pii-audit
description: Audit application logging for personal data, credentials, sensitive identifiers, and unsafe retention across services.
---

# Log Redaction Pii Audit

## Goal

Preserve useful diagnostics while minimizing the chance that logs become an unintended sensitive-data store.

## Inputs to inspect

Logger configuration, representative logs, structured event schemas, retention/sinks, request middleware, and data classification policy.

## Workflow

1. Inventory log sources and sinks: application code, reverse proxy, errors, traces, analytics, queue workers, and third-party observability systems.
2. Compare logged fields against a data classification list for tokens, passwords, session IDs, email/address, user content, and tenant/customer identifiers.
3. Replace raw sensitive values with omission, truncation, tokenization, or keyed pseudonyms only when the diagnostic use case justifies it.
4. Test exception paths, validation failures, headers, query strings, crash dumps, and nested third-party errors because they often bypass normal redaction.
5. Review retention, access roles, export/download capabilities, and incident response for already-collected sensitive logs.

## Validation checklist

- [ ] Secrets and session credentials are not emitted in normal or failure logs.
- [ ] PII redaction is verified against actual representative output, not only logger configuration.
- [ ] Pseudonymous IDs cannot be casually reversed and have a documented use.
- [ ] Retention and access follow least privilege and data classification.
- [ ] Existing exposure leads to an incident/retention decision instead of only a future code fix.

## Required output

Produce a log-source inventory, sensitive-field matrix, redaction tests, retention findings, and remediation owners.

## Boundaries and failure handling

Do not include raw sensitive log samples in the audit output; do not remove fields needed for diagnostics without replacing them with safe correlation signals.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
