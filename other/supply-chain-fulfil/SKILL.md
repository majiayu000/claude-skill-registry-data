---
name: supply-chain-fulfil
description: >
  Move a labs contract's goods and money: shipment, receipt, invoice, payment, confirmation. Needs contracts.
---

# Supply-chain fulfil

Takes the contracts `supply-chain-procure` signed and records what happens next: the supplier ships,
the central store receives (the event that creates stock), the supplier invoices, ACE pays what
arrived, and the supplier confirms the money came. Labs' three-way match (`contract_match`) is the
authority on what is owed, not ACE's arithmetic.

Platform reference: [`playbook/integrations/connect-labs-supply-chain.md`](../../playbook/integrations/connect-labs-supply-chain.md)
§ Logistics and § Finance. In `/ace:run` this is part of the optional `supply_chain` step (spec
`docs/superpowers/specs/2026-10-18-optional-labs-e2e-steps.md` § F4), run once in week 0 of the
backdated calendar, after procurement.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `program_id` | the labs programme | explicit arg; default: run_state `phases.execution-management.products.supply_chain.program_id` |
| `contract_ids` | the orders to fulfil | explicit arg; default: run_state `products.supply_chain.contract_ids` |
| `central_supply_point_id` | where goods arrive | explicit arg; default: run_state `products.supply_chain.supply_points.central` |
| `scope` | the `source.ref` scope | the run id inside `/ace:run`; outside one, `programScope(program_id)` (`lib/supply-chain-ref.ts`) |
| `simulated` | invent the supplier's side, label every write, backdate | `true` when Phase 9 `mode: simulated`; explicit arg otherwise |
| `sim_week0_start` | the Monday fulfilment is dated in | run_state `products.simulation.calendar.weeks[0].start` (`lib/sim-calendar.ts`, PR10); explicit arg otherwise |

No `run_state.yaml` is needed when every parameter is passed. Run-state write-back (Step 9) happens
only when a run is bound.

**Pipeline-only in one respect:** on the simulated track ACE invents the supplier's dispatch, its
invoice (including one deliberate over-billing) and its payment confirmation. Outside a simulation
each of those is recorded only when the supplier actually sends it, with `source` set to who told
you.

## Products

- `9-execution-manager/supply-chain-fulfil_plan.yaml`: per contract, the shipment, the receipt
  (accepted / rejected, with the planned partial rejection), the invoice (with the planned
  over-billing), and the payments, written **before any write**.
- `9-execution-manager/supply-chain-fulfil_record.md`: shipment, receipt, invoice and payment ids,
  each contract's three-way match as labs computed it after each stage, and the dispute and its
  resolution.
- run_state `phases.execution-management.products.supply_chain` (inside a run): adds
  `shipment_ids`, `receipt_ids`, `invoice_ids`, `payment_ids`.

## Process

1. **Precondition.** `supply_chain_programme_runner_get` must say `programme` (or `operator`).
   Read each contract (`supply_chain_contract_get`) and its `supply_chain_contract_match`; a
   contract already `fully_received` is skipped, not re-received.
2. **Plan** (Products, first file). On the simulated track, across the contracts:
   - **one partial rejection**: one receipt line rejects a small quantity (a few damaged units) with
     a `rejection_reason`, to exercise the loss path;
   - **one over-billing**: one invoice bills `quantity_billed` above what was accepted, so the
     three-way match flags it and Step 6 disputes it;
   - **one advance**: the contract procure placed on `payment_terms: advance` is paid before
     shipment.
3. **Advance** (advance-terms contracts only, before shipping).
   `supply_chain_payment_record({program_id, data: {contract_id, amount, currency, paid_on, method, source: "we_recorded"}, source})`
   for the agreed advance. The invoice later names it in `acknowledges_payment_ids`.
4. **Ship.** `supply_chain_shipment_record({program_id, data: {contract_id, lines: [{item_id, quantity, quantity_unit, batch, expiry}], dispatched_on, expected_on, carrier, status: "dispatched", source}, source})`
   with `data.source` = `supplier_reported` (the supplier told us). It posts nothing to stock. When
   it arrives: `supply_chain_shipment_update({shipment_id, data: {status: "delivered"}})`.
5. **Receive.** `supply_chain_receipt_record({program_id, data: {contract_id, shipment_id, supply_point_id: central, received_on, lines: [{item_id, batch, expiry, quantity_accepted, quantity_rejected, rejection_reason, quantity_unit}], source: "we_recorded"}, source})`.
   This is the event that creates stock: each accepted line posts a movement, and a rejected
   quantity stays on the line and never enters the ledger. Batch and expiry match the shipment's.
   Then read `supply_chain_contract_match` into the record.
6. **Invoice.** `supply_chain_invoice_record({program_id, data: {contract_id, reference, issued_on, quantity_billed, quantity_unit, unit_price, amount, currency, acknowledges_payment_ids?, source: "supplier_reported"}, source})`.
   Give `unit_price` and `quantity_billed` **as billed**; never correct them on entry. Read
   `contract_match` again: on the planned over-billing, `over_invoiced` is positive and
   `checks_list` carries `invoice_over_billed`.
   **Dispute** it: `supply_chain_invoice_dispute({invoice_id, reason, disputed_on, source})`. It
   marks the invoice `queried` and **sends nothing** to the supplier. On the simulated track the
   supplier's corrected bill arrives a day later:
   `supply_chain_invoice_update({invoice_id, data: {quantity_billed: <accepted>, amount, status: "approved"}, source})`,
   with `source.sender` the supplier and the excerpt quoting the (simulated) correction.
7. **Pay what arrived.** For each invoice, `supply_chain_payment_record({program_id, data: {invoice_id, amount, currency, paid_on, method, source: "we_recorded"}, source})`.
   `amount` = `contract_match.payable_now` **as labs returns it**, never the billed amount, and
   never minus the advance: `payable_now` is already net of every payment recorded, the advance
   included. Live, labs programme 361 contract 323 (814 received at UGX 41,500, an advance of
   10,000,000) read `payable_now` 23,781,000 = 33,781,000 − 10,000,000; subtracting the advance
   again would have paid 13,781,000 (ace#3260). Once paid, `payable_now` reads 0. An invoice's
   status follows from what has been paid; never set it to `paid` by hand.
8. **Confirm.** `supply_chain_payment_confirm({payment_id, confirmed_on, source})` for every
   payment, `confirmed_on` inside week 0 and not before `paid_on`. A backdated payment is already
   more than a fortnight old in real time, so an unconfirmed one shows in `checks_list` as
   `payment_unconfirmed` at once.
9. **Record.** Write the record file, then, inside a run, the ids into `products.supply_chain`
   with `update_yaml_file` and `merge: 'deep'`, resending each id array whole (deep merge replaces
   arrays).
10. **Hand to QA.** Dispatch `supply-chain-fulfil-qa`. Do not mark the step done on the write
    responses alone.

**Every write** carries `source = buildSource({scope, skill: "supply-chain-fulfil", step, key, sender, sentOn, simulated, today})`
from `lib/supply-chain-ref.ts`. The key is `<contract_id>` (plus `:advance`, `:correction`, the
payment's invoice id), so a re-run replays instead of writing twice. Dates are
`simulatedDate(sim_week0_start, n)` in order: advance, dispatch, delivery, receipt, invoice,
dispute, correction, payment, confirmation.

## MCP Tools Used

- connect-labs: `supply_chain_programme_runner_get`, `supply_chain_contract_get`,
  `supply_chain_contract_match`, `supply_chain_shipment_record`, `supply_chain_shipment_update`,
  `supply_chain_receipt_record`, `supply_chain_invoice_record`, `supply_chain_invoice_dispute`,
  `supply_chain_invoice_update`, `supply_chain_payment_record`, `supply_chain_payment_confirm`,
  `supply_chain_checks_list`
- ace-gdrive: `drive_create_file` (plan + record), `update_yaml_file` (run write-back only)

## Existing objects

- **Nothing here can be deleted** (spec § F6): not a shipment, receipt, invoice or payment. A wrong
  receipt is corrected with a stock movement (`supply_chain_movement_record`), a wrong invoice with
  `invoice_update` or a rejection, an overpayment is recovered against the next invoice. Never
  record a second receipt for goods already received.
- **A receipt is stock.** Recording one against a live programme changes what every stock read,
  forecast and resupply plan says. On a real programme, receive only what the store actually counted
  in.
- **A dispute sends nothing.** Telling a real supplier is a separate, human-approved email.
- **Never run against a programme ACE does not own** (§ F6).

## Mode Behavior

- **Auto:** Steps 1-10.
- **Review:** shows the Step 2 plan and waits before Step 3.

## Dry-Run Behavior

When `--dry-run` is active, run Step 1's reads and Step 2. Write the plan. Make no
`supply_chain_*` write.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-20 | Step 7 pays `payable_now` as returned: it is already net of the advance and every payment recorded (ace#3260) | ACE |
| 2026-10-18 | Initial version (optional-track PR8): advance, shipment, receipt (stock), invoice with dispute and correction, payment of what arrived, confirmation | ACE |
