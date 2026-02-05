---
name: implementing-assertions
description: "Implements Phylax Credible Layer assertions in Solidity using cheatcodes, triggers, and event/state inspection. Use when writing or refactoring assertion contracts."
---

# Implementing Assertions

Turn a written invariant spec into a correct, gas-safe assertion contract.

## When to Use
- Writing a new assertion contract from a defined invariant.
- Refactoring or optimizing existing assertions.
- Adding trigger logic, call input parsing, or event/state checks.

## When NOT to Use
- You only need invariant ideation or trigger selection. Use `designing-assertions`.
- You only need testing patterns. Use `testing-assertions`.

## Quick Start
```solidity
contract MyAssertion is Assertion {
    function triggers() external view override {
        registerCallTrigger(this.assertInvariant.selector, ITarget.doThing.selector);
    }

    function assertInvariant() external {
        ITarget target = ITarget(ph.getAssertionAdopter());
        ph.forkPreTx();
        uint256 pre = target.totalAssets();
        ph.forkPostTx();
        uint256 post = target.totalAssets();
        require(post >= pre, "Invariant violated");
    }
}
```

## Implementation Checklist
- **Triggers**: use the narrowest possible trigger; avoid global triggers.
- **Pre/Post**: call `forkPreTx()` only when needed; default is post-state.
- **Call-Scoped Checks**: use `getCallInputs` + `forkPreCall`/`forkPostCall` for per-call invariants.
- **Preconditions**: use `before*` hook triggers or `forkPreCall` to assert pre-state requirements.
- **Baselines**: for intra-tx stability, read `forkPreTx()` once and compare per-call post snapshots.
- **Event Parsing**: filter by `emitter` and `topics[0]`; decode indexed vs data fields correctly.
- **Storage Slots**: use `ph.load` for EIP-1967 slots, packed fields, and mappings.
- **State Changes**: `getStateChanges*` includes the initial value at index 0; length 0 means no changes.
- **Nested Calls**: avoid double counting; prefer `getCallInputs` to avoid proxy duplicates.
- **Batch Dedupe**: deduplicate targets/accounts when a batch can repeat entries.
- **Tolerances**: use minimal, documented tolerances for price/decimals rounding.
- **Optional Interfaces**: use `staticcall` probing and skip when unsupported.
- **Token Quirks**: validate using balance deltas; handle fee-on-transfer and rebasing tokens.
- **Packed Calldata**: decode using protocol packing logic (assetId, amount, mode) and map ids via helpers.
- **Delta-Based Supply Checks**: compare totalSupply delta to sum of per-call amounts instead of enumerating users.
- **Id Mapping Guards**: if a packed id maps to `address(0)`, skip or fail early to avoid false positives.
- **Sentinel Amounts**: normalize `max`/sentinel values (e.g., full repay/withdraw) using pre-state.
- **Gas**: assertion gas cap is 300k; happy path is often most expensive; early return, cache reads, and limit loops.

## Rationalizations to Reject
- "Use getAllCallInputs everywhere." It can double-count proxy calls.
- "I can ignore nested calls." Batched flows are common and must be handled.
- "Events are enough." If events can be skipped, back them with state checks.
- "We can rely on storage layout guesses." Always derive slots from layout.

## References
- [Cheatcodes and Traces](references/cheatcodes-and-traces.md)
- [Storage Layouts and Slots](references/storage-layouts-and-slots.md)
- [Event Parsing](references/event-parsing.md)
- [Tolerance and Rounding](references/tolerance-and-rounding.md)
- [Token Integration Safety](references/token-integration-safety.md)
