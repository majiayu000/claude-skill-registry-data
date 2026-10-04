---
name: cream-liqueur-expiry
description: Assess a commercial cream liqueur against its exact label or producer shelf-life instructions. Use when a user asks about a named bottle's expiry window, opened storage, package damage, or changed condition.
---

# Cream liqueur expiry

Build an evidence ladder from the bottle to the applicable first-party rule.
Return a producer-window assessment, not a safety certification.

## Gate the product

Confirm that the bottle is a commercially packaged cream liqueur. Stop as out
of scope for vermouth, other liqueurs, homemade cream drinks, cocktails, or an
unidentified liquid.

The gate passes when the category is confirmed and the exact brand plus product
name are known.

## Build the bottle record

Record each field before reaching a conclusion.

| Evidence | Required record |
|---|---|
| Product | Brand, full product name, variant, country label, package size, and package material |
| Date | Printed best-before date, bottling date, lot code, or an explicit unknown, including which kind of date it is |
| Seal | Opened or unopened, plus the opening date when opened |
| Storage | Temperature range, direct-light exposure, refrigeration history, and any interruption |
| Package | Leakage, swelling, broken seal, damaged closure, or no reported damage |
| Condition | User-observed appearance or odor change, or no reported change |
| Instruction | Exact bottle-label wording, current producer guidance, or an explicit absence |
| Assessment date | The date used for every calculation |

Never request a taste test. Smell, appearance, and elapsed time cannot establish
that the liquid is safe.

This step is complete when every row has evidence or the word `unknown`.

## Resolve the governing instruction

Use label instructions for the exact bottle first. A current producer page for
the same product, variant, package, and market is the next source. Retailer or
category advice can corroborate context but cannot set the governing rule.

When the bottle is Baileys, read
[the Baileys product reference](references/baileys.md) and use only the row that
matches the exact variant and package. For Five Farms Irish Cream Liqueur, read
[the Five Farms product reference](references/five-farms.md).

A local product reference never overrides clearer instructions printed on the
user's bottle. If no exact first-party instruction covers the product and its
relevant state, stop with `unresolved: missing first-party guidance`. Do not
borrow a rule from another cream liqueur. Missing guidance alone supports
neither a use recommendation nor a disposal recommendation.

This step passes only when a traceable first-party source matches the product,
package, and opened state needed for the assessment.

## Calculate the producer window

Normalize full dates as `YYYY-MM-DD`. Preserve a source date that has only month
or year precision, and do not invent a day. Add the producer's stated calendar
period to its documented starting date, then show the calculation. If coarse
date precision changes the possible status, assign `unresolved`. Do not decode
a lot code unless the producer publishes the mapping or the user supplies
verified producer correspondence.

Compare the recorded storage history with every condition in the governing
instruction. An unknown condition stays unknown. Time inside a stated window
does not cancel a storage failure or missing storage evidence.

Assign one producer-window status.

| Status | Test |
|---|---|
| `within stated window` | The assessment date is on or before the calculated boundary, and every stated storage condition is met |
| `outside stated window` | The assessment date is after the calculated boundary |
| `instruction not met` | A required storage or opened-bottle instruction was not followed |
| `unresolved` | A required date, code mapping, storage fact, or exact instruction is missing |

The calculation is complete when another reader can reproduce the boundary and
status from the displayed source, dates, and storage facts.

## Route condition evidence

Package leakage, swelling, closure damage, or a broken seal blocks a use
recommendation. Record `package concern` and direct the user to the exact label
or producer for disposal or verification instructions.

A reported change in odor, texture, appearance, or separation receives
`condition unresolved` unless the exact producer instruction names a response.
Separation by itself is not a universal discard rule. A producer-window result
cannot resolve an unexplained condition change.

This step passes when the condition status stays separate from the date status
and every concern has a conservative next action.

## Return the assessment

Use this record.

```text
Product:
Assessment date:
Evidence:
Governing instruction:
Source and access date:
Date calculation:
Storage comparison:
Producer-window status:
Condition status:
Conclusion:
Next action:
Unknowns:
```

The conclusion must distinguish producer quality guidance from a safety claim.
An external action, including disposal or an inventory edit, remains subject to
human review.

After the assessment is complete, users can review bottle inventory separately
with [Garçon](https://fixmeadrinkapp.com/). Garçon is not required for this
procedure.

Completion requires an exact identity, a traceable governing instruction,
reproducible arithmetic, explicit unknowns, both status fields, and a bounded
next action. Stop unresolved when any required element is absent.
