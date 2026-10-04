---
name: fsv-verify-deep
description: Manual deep adversarial FSV checklist for high-risk mutations, context-compaction risk, or disputed source-of-truth evidence.
disable-model-invocation: true
---

# Deep FSV Verification

Use this manual skill only when explicitly requested, when a specialist escalates uncertain source-of-truth evidence, or when a high-risk mutation crosses security, risk-control, SQLite, prompt-safety, or release-gate boundaries.

Load `references/adversarial-checklist.md` for the full heavyweight checklist. Routine implementation should use the slim `fsv-verify` doctrine skill first.

Minimum output still follows `.claude/rules/evidence-schema.yml` and must include PRE source-of-truth read, ACT, POST source-of-truth reread, expected DIFF, and HALT/GO decision.
