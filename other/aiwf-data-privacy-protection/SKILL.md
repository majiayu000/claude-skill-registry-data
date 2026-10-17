---
name: aiwf-data-privacy-protection
description: Use for personal, customer, employee, model, dataset, telemetry, marketing, support, payment, credential, and agent-context data inventories; classification, minimization, consent, access, encryption, retention, deletion, backups, vendors, privacy notices, and audit-readiness evidence.
---

# AIWF Data Privacy Protection

## Core Rule

Know what data exists, why it is needed, where it moves, who can access it, how long it remains, and how it is deleted or restored. Do not collect data merely because it may become useful.

## Workflow

1. Define business purpose, subjects, jurisdictions, systems, vendors, owners, and decision scope.
2. Inventory each data class from collection through processing, sharing, storage, backup, export, deletion, and disposal.
3. Record sensitivity, purpose, source, fields, subject, volume, location, access, encryption, key owner, retention, deletion, backup, and incident owner.
4. Remove unnecessary collection and access before adding complex controls.
5. Compare actual behavior with product copy, consent, contracts, privacy notices, platform terms, and user controls.
6. Define access reviews, retention jobs, deletion verification, backup handling, vendor evidence, and incident linkage.
7. Build audit evidence without declaring legal compliance or certification.

Validate structured inventories with `python scripts/validate_data_inventory.py --input <inventory.json>`. Read `references/source-register.json` before legal or framework claims.

## Guardrails

- Use a practical US baseline and identify sector, state, child, health, biometric, financial, international-transfer, and breach-notification questions for current qualified review.
- Do not store raw sensitive data in reports when field names, counts, hashes, or redacted samples suffice.
- Explicit approval is required before collecting, exporting, sharing, deleting, reclassifying, changing retention, or modifying production access/encryption.
- Do not promise anonymity when data is merely pseudonymous or claim a backup is recoverable without a restore test.
- Exact SOC 2 or ISO control mappings require current authorized source material; evidence readiness is not certification.

## Output

Return the data-flow inventory, gaps, minimized target state, retention/deletion matrix, access and encryption controls, audit evidence, legal questions, and validation plan.
