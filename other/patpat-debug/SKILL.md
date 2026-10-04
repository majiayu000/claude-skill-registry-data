---
name: patpat-debug
description: Diagnose and fix a reproducible defect through root-cause evidence. Use for broken behavior, regressions, failing runtime paths, and unexplained mismatches when implementation is requested.
---

# Patpat Debug

For clear, bounded, reversible local work without delivery intent, use this skill and its relevant references. Otherwise read the [operating protocol](../patpat-loop/references/operating-protocol.md) and [execution graph](../patpat-loop/references/execution-graph.md) in full before acting. Escalate on uncertainty, security, auth, billing, secrets, architecture, cross-cutting work, or delivery intent. Define Claim, Surface, Action, Expect, and Cleanup before editing. Do not load the router or reread unchanged instructions already loaded in this session.

Read [repository truth](../patpat-loop/principles/repository-truth.md), [proof over proxy](../patpat-loop/principles/proof-over-proxy.md), [fix root causes](../patpat-loop/principles/fix-root-causes.md), [smallest safe change](../patpat-loop/principles/smallest-safe-change.md), and [preserve safety](../patpat-loop/principles/preserve-safety.md). Apply the [defect playbook](../patpat-loop/playbooks/defect.md). When the user requests test-first work or a cheap deterministic regression target exists, apply [regression first](../patpat-loop/playbooks/regression-first.md).

Observe the failure before any production edit, or record an explicit why-not; report fail-before and pass-after on the same check.

Reproduce before editing when safe and practical. Otherwise trace the contract or code path, or use an isolated non-harmful surrogate, and state that direct runtime proof is unavailable. Trace the earliest incorrect state instead of patching the last visible symptom.

If the user limited the request to diagnosis, stop after proving or bounding the root cause. Recommend the smallest patch without editing.

Change one causal variable at a time. Preserve only material failed hypotheses through the defect playbook as bounded, redacted evidence; do not retain raw logs or trivial attempts. Re-run the original reproduction when it remains safe and practical; otherwise run the predeclared non-triggering check and state the missing runtime proof. Never label an unobserved fix as verified.

When the defect is a mismatch against a reference image or migrated UI, apply the [visual equivalence playbook](../patpat-loop/playbooks/visual-equivalence.md) after reproducing the defect. Preserve the pre-edit reference and comparison harness.

## Proof closure

Define the five-field proof contract before any mutation. Close mutating work with:

- Always: [`patpat-verify`](../patpat-verify/SKILL.md), using authoritative evidence.
- When required: [`patpat-review`](../patpat-review/SKILL.md) for delivery intent, auth/security/billing/secrets, architecture or cross-cutting scope, durable-run completion, land/merge, or another operating-protocol review gate.

For clear, bounded, reversible local work with none of those review requirements, proceed from verification to REPORT without independent review.
