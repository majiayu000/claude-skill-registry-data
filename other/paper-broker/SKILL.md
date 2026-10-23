---
name: paper-broker
description: Place exactly one paper order per approved ticket through exec.quote, exec.simulate, and exec.place, and report UNKNOWN RESULT instead of guessing.
bots:
  - bot-04-sniper
  - bot-06-exit
gates:
  - G-2
  - G-6
required_tools:
  - exec.quote
  - exec.simulate
  - exec.place
  - exec.cancel
  - exec.positions
  - market.price
  - onchain.priority_fee
required_data:
  - jupiter
  - solana_rpc
permissions:
  max_side_effect: paper-write
  network: true
  filesystem: var
fixtures:
  - tests/fixtures/http/jupiter_order.json
---

# Paper Broker

## L1 - Summary

SNIPER (buys) and EXIT (sells) place exactly one paper order per approved ticket. The path is fixed: quote, simulate, then place with the approval id. A repeat decision (remainder sell, re-decided buy) is a new decision id and a new order, never a replay of the first. On timeout or ambiguity, report UNKNOWN RESULT and reconcile by signature; never second-send.

```
APPROVED ticket -> exec.quote -> exec.simulate clean -> exec.place (approval_id) -> one Fill
timeout/error   -> UNKNOWN RESULT, reconcile by signature, wait for a new approval
```

## L2 - Method

1. S1 - Check the ticket: status APPROVED, RISK verdict CLEAR (or CONDITIONAL with every condition met), and a matching approval id for this exact ticket, mint, size, and slippage. Any mismatch stops the flow.
2. S2 - Read the market: take `market.price` for the live mid and `onchain.priority_fee` for the current fee level. The quote is informational (route plus priority); it is never the fill price.
3. S3 - Quote and simulate: call `exec.quote` for the route, then `exec.simulate` to prove the order would land. A failing simulation is a NO-GO, not a reason to skip simulation.
4. S4 - Place once: call `exec.place` with the ticket id, side, decision id, and approval id. The idempotency key derives from (ticket_id, side, decision_id); the same decision re-placed returns the first fill.
5. S5 - Confirm or reconcile: on success record the fill, fee paid, and route via `exec.positions`. On timeout or error report "UNKNOWN RESULT - reconcile by signature" and wait; never retry without a new human approval.
6. S6 - Cancel cleanly: if the ticket is withdrawn while ACCEPTED, `exec.cancel` once and record the outcome. After confirmation the order is final.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Approval mismatch | Ticket, mint, size, or slippage differs from the approval | Stop; request a fresh approval for the exact parameters |
| Simulation fails | Route illiquid or fee spike beyond tolerance | NO-GO; report the cause; never place an unsimulated order |
| UNKNOWN RESULT | Timeout or ambiguous response from place | Reconcile by signature via ledger read; never second-send |
| Duplicate decision id | Same (ticket, side, decision) placed twice | The registry returns the first fill; a genuinely new intent needs a new decision id |
| No approval id | Autonomous or human approval never issued | Refuse; paper buys require a valid approval id (G-6) |

## References

- Tools: `src/pumpgrok/tools/exec/` (quote, simulate, place, cancel, positions)
- Market and fees: `market.price`, `onchain.priority_fee` (Solana RPC reads)
- Data: Jupiter order quote plus Solana RPC (never a lite endpoint)
- Gates: G-2 (approvals), G-6 (single-send discipline)
- Companion skills: `desk-execution-protocol` (pre-send checklist), `jupiter-routing` (route preparation)
