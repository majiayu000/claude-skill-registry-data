---
name: risk-control-audit
description: >
  Verify DegenExus risk controls, including RiskGate, ExecutionGate,
  RiskDecision expiry, exposure limits, position sizing, stop-loss/take-profit
  ordering, and bypass paths.
when_to_use: >
  Use when changes touch RiskGate, ExecutionGate, risk decisions, exposure, sizing,
  stop-loss/take-profit, order execution, or bypass paths.
---

# Risk Control Audit

## Workflow

1. Identify the proposal-to-execution path for the change.
2. Enumerate all hard invariants: max exposure, max open positions, risk/reward, confidence, direction-specific stop/take ordering, stale decision expiry, and execution preconditions.
3. Map each invariant to source files and tests.
4. Verify there is no route from `TradeProposal` to fill simulation that skips deterministic gates.
5. Require BVA/ECP tests at every threshold and malformed-input tests at every Pydantic boundary.
6. Produce `PASS` only with source-of-truth evidence from code and tests; otherwise produce `BLOCK`.

## Evidence Requirements

- Cite exact files and line ranges.
- Include at least three edge cases.
- Distinguish deterministic gate failures from LLM risk-assessment recommendations.
