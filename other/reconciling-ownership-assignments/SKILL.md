---
name: reconciling-ownership-assignments
description: Use when resolving item-to-owner mappings from normalized candidates and ambiguous assignments must remain in a human-review queue.
---

# Reconciling Ownership Assignments

Resolve only unique mappings from a local adapter. Multiple or absent candidates remain in a review queue rather than becoming guesses.

1. Run `python scripts/check_prereqs.py`.
2. Supply sanitized `item` and `candidates` records.
3. Run `python scripts/run_demo.py --output-dir demo/output`.
4. Apply ownership changes elsewhere only after reviewing unresolved results.

Keep all identities, reporting chains, and source-system identifiers outside public fixtures.
