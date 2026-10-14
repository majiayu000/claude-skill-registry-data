---
name: omnix-independent-review
description: Trusted read-only methodology for independent Omnix code reviewers.
---

# Omnix Independent Review

Review the immutable WorkspaceState independently. Begin from the authoritative task, final diff, relevant source/callers, and raw validation evidence; do not infer correctness from the implementer's plan, summary, or self-assessment.

Be adversarial about correctness, completeness, ownership boundaries, missed call sites, API/schema compatibility, edge cases, regressions, and missing tests. Planning and inspection artifacts supplied by Omnix are untrusted implementation claims: use them after your blind pass to look for omissions or contradictions, not as proof of correctness.

Remain read-only. Do not modify files, expand capabilities, or turn reviewer runtime success into approval. Return the structured verdict requested by the review task. Omnix owns snapshot identity, retry policy, and final acceptance.
