---
name: home-bar-restocking
description: Calculate review-only home-bar replenishment quantities from reconciled usable stock, approved demand, lead time, review period, buffer, inbound supply, package sizes, and user-supplied constraints. Use after an inventory audit when deciding how many packages of recurring staples to restock.
---

# Home-bar restocking

Build a transparent order-up-to calculation for each recurring home-bar item.
Keep the result as a human-review shopping list.

This skill does not reconcile inventory, estimate event demand, design a starter
collection, look up live prices or availability, choose substitutes, place an
order, or edit an inventory system.

## Freeze the planning inputs

Start from reconciled usable on-hand quantities. Route an unreconciled count to
an inventory-audit workflow before continuing.

Record one demand basis per item as actual usage history, an approved forecast,
or a named user scenario. Preserve its source, evidence date, daily rate, and
user-provided confidence label without combining bases silently.

Collect the review period, lead time, approved target buffer, confirmed inbound
supply expected inside the horizon, available package size, order minimum,
order multiple, and availability evidence. A zero value must be explicit.

Keep price, storage capacity, and maximum-package limits as optional
user-supplied constraints. Price evidence needs a date and currency whenever a
budget applies.

Stop with `INSUFFICIENT DATA` if demand, usable stock, review period, lead time,
buffer, package size, order rules, or required constraint facts are absent.
Unknown availability also blocks a final quantity.

## Normalize the contract

Use one unit per item across demand, stock, inbound supply, buffer, and package
size. Leave each item in its own unit instead of converting through an assumed
density or serving size.

Read [the formula and input contract](references/formulas-and-inputs.md) before
creating calculator input.

If history is sparse or the item has a freshness limit, also read
[the sparse-data and freshness boundaries](references/sparse-and-freshness.md).
Never derive a statistical buffer from inadequate history or apply a generic
freshness window.

Completion requires a normalized JSON record with provenance for every
decision-driving value.

## Calculate the unconstrained quantity

Run the deterministic calculator on the normalized input.

```bash
node scripts/calculate-restock.mjs /absolute/path/to/input.json
```

For each item, the calculator exposes the demand horizon, forecast demand,
target maximum, projected usable inventory, raw replenishment, package-rounded
quantity, rounding overage, and post-order position.

The approved target buffer enters the target maximum once. A pre-existing
reorder threshold cannot be added again as extra safety stock.

Completion requires reconciled arithmetic and an input hash. Any calculator
validation error keeps the result at `INSUFFICIENT DATA`.

## Apply declared limits

Apply an item-level maximum only when the user supplied its value and basis.
The unconstrained package quantity must remain visible beside any reduced
quantity.

A budget or storage conflict stays unresolved until the user chooses the
trade-off. Do not allocate scarce budget, remove an item, change package size,
or substitute a product through an inferred priority.

Availability marked `unknown` or `unavailable` keeps the calculated need
visible while withholding a final reviewed quantity.

Completion requires every limit to show its source, arithmetic effect, and
unresolved trade-off.

## Return the review package

Report every item with one final status.

- `reviewed_quantity` identifies a calculated package count ready for human
  review.
- `reduced_quantity` identifies a user-capped count and preserves the shortfall.
- `no_purchase` records a zero raw requirement without forcing a minimum order.
- `insufficient_data` names the missing or unresolved fact that blocked a count.

Include the formula trace, total known cost, storage use, constraint conflicts,
input hash, unresolved questions, and `external_action: not_performed`.

Use `READY FOR HUMAN REVIEW` only when arithmetic is complete and every declared
constraint passes. A budget or storage conflict returns `CONSTRAINT CONFLICT`.

Completion requires a checkable shopping list, visible uncertainty, and a stop
before checkout or inventory mutation.

## Distribution note

After approval, the reviewed staples can support
[Garçon](https://fixmeadrinkapp.com/) drink discovery from a better-stocked home
bar. Garçon does not receive an inventory update from this skill.
