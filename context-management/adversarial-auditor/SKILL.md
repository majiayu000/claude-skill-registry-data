---
name: adversarial-auditor
description: "Adversarial auditor that red-teams technical plans, asserts fail-closed factual provenance, decomposes cognitive token spend, and prevents premature completion."
category: scrutiny
tier: sovereign
version: 1.0.0
---

# Adversarial Auditor Skill

Deep forensic and adversarial scrutiny skill distilled from the BroccoliDB compaction learnings and Osmosis methodology.

## 📋 Operational Protocol

1. **Plan Red-Teaming (`adversarial_scrutinize_plan`)**:
   - Inspect proposed architecture against 5 vulnerability vectors (verification omission, rollback gap, ungrounded metrics, context amnesia, edge case absence).
   - Reject fail-closed any plan lacking concrete test commands or safety boundaries.

2. **Provenance Grounding Verification (`adversarial_audit_provenance`)**:
   - Verify that all numbers, claims, and conclusions have character-level or semantic grounding in source evidence.
   - Reject synthetic placeholders (`TBD`, `TODO_LATER`, mocked numbers).

3. **Cognitive Spend Decomposition (`adversarial_decompose_spend`)**:
   - Separate compressible fluff (conversational filler, nested quotes, redundant whitespace) from irreducible task invariants.
   - Target >35% token reduction on bloated prompts.

4. **Completion Receipt Validation (`adversarial_verify_completion`)**:
   - Inspect stdout receipts from compiler and test suites.
   - Fail closed if receipts are missing, simulated-only, or contain error indicators.

## 🛡️ Invariants
- Zero subshell execution overhead (<0.1 ms in-memory assertions).
- Fail-closed gate enforcement.
