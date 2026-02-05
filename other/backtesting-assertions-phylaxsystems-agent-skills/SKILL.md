---
name: backtesting-assertions
description: "Runs Credible Layer assertion backtests against historical transactions. Use when validating assertions on real chain data or known exploits."
---

# Backtesting Assertions

Use Credible Layer backtesting to replay historical transactions with assertions enabled.

## When to Use
- You want to validate assertions against real mainnet transactions.
- You are testing a known exploit block or incident transaction.
- You need to confirm triggers match real protocol entrypoints.

## When NOT to Use
- You only need unit or fuzz tests. Use `testing-assertions`.
- You are designing invariants or triggers. Use `designing-assertions`.
- You only need Solidity implementation details. Use `implementing-assertions`.

## Quick Start
1. Create a test that inherits `CredibleTestWithBacktesting`.
2. Configure `BacktestingConfig` with target contract, block range, and assertion selector.
3. Call `executeBacktest` and assert failures are zero.
4. Run with `--ffi` or a profile that enables FFI.

## Workflow
- Pick a target contract (the assertion adopter address).
- Choose `endBlock` and `blockRange`.
- Verify RPC env vars; skip or fallback when missing.
- Prefer `useTraceFilter = true` to detect internal calls.
- Use `forkByTxHash = true` only when debugging state-dependent failures.
- Interpret results: `ASSERTION_FAIL` often indicates false positives or gas issues.
- If many `SKIP`, the selector/target does not match; adjust target or selector.

## Rationalizations to Reject
- "We only need unit tests." Backtesting catches real-world call patterns.
- "Trace filter is optional." Without it you miss internal calls.
- "forkByTxHash everywhere." It is slow and RPC-heavy; use it for debugging only.
- "RPC isn't needed." Backtesting requires a working RPC and FFI.

## References
- [Backtesting Template](references/backtesting-template.md)
