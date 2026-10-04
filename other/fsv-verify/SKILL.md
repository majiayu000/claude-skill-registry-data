---
name: fsv-verify
description: Apply slim PRE-ACT-POST-DIFF-HALT source-of-truth checks after mutations or claimed state changes.
when_to_use: >
  Use whenever files, database rows, portfolio state, risk decisions, prompts,
  tests, or configuration are changed or when a tool reports success without an
  independent source-of-truth reread.
---

# FSV Verify

A return value is a claim. The source of truth is the verdict.

## Doctrine

1. **PRE:** Read the authoritative source of truth before the mutation.
2. **ACT:** Perform exactly one scoped action.
3. **POST:** Reread the authoritative source of truth after the action.
4. **DIFF:** Compare the observed delta with the expected delta.
5. **HALT:** Stop on mismatch, missing evidence, or contradictory evidence.

## DegenExus Sources of Truth

- Filesystem changes: bytes on disk and `git diff`, not write return values.
- SQLite trade state: direct rows or `TradeStore` reads, not cached objects.
- Portfolio state: `Portfolio` properties, not agent summaries.
- Risk decisions: persisted or model-boundary `RiskDecision` data plus execution gate outcome.
- Claude internals: `.claude/README.md`, `.claude/settings.json`, `.claude/rules/synergy-contract.yml`, and `python .claude/hooks/validate-claude-config.py`.

## Escalation

This skill is intentionally slim and model-invocable. Use manual `fsv-verify-deep` for high-risk security, risk-control, SQLite, prompt-safety, context-compaction, or disputed-evidence situations.

## Output

Emit `.claude/rules/evidence-schema.yml` fields and explicitly name PRE evidence, ACT, POST evidence, expected delta, observed delta, and HALT/GO decision.
