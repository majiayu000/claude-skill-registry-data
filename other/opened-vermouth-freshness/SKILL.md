---
name: opened-vermouth-freshness
description: Assess an opened vermouth against its exact label or producer quality guidance. Use when a user asks about a named bottle's open-date window, missed refrigeration, package damage, contamination, oxidation, or changed condition.
---

# Opened vermouth freshness

Build an evidence ladder from the exact bottle to its producer's quality
guidance. Return a review of quality guidance and handling evidence, never a
sensory safety certification.

## Gate the product

Confirm that the bottle is a commercially packaged product labeled vermouth.
Record its exact brand, product name, style, market label, package size, and
package material.

Stop as out of scope for cream liqueur, sherry, table wine, homemade vermouth,
an aperitif not labeled vermouth, a nonalcoholic product, or an unidentified
liquid. Do not transfer a vermouth rule across those categories.

The gate passes when the product class and exact identity are established.

## Build the bottle record

Record every field before assigning a result.

| Evidence | Required record |
|---|---|
| Opening | Exact opening date, bounded date range, or `unknown` |
| Closure | Original closure, resealing after each use, transfer history, preservation method, headspace observation, and any interruption |
| Cold storage | Refrigeration start, temperature range, every unrefrigerated interval, and any unknown period |
| Exposure | Direct light, heat, freezing, or no reported exposure |
| Package | Leakage, cracked or damaged closure, broken seal area, swelling, or no reported damage |
| Contamination | Foreign growth, foreign material, dirty pourer, contact with another liquid, or no reported concern |
| Condition | User-reported appearance, aroma, sediment, texture, or flavor observation already made |
| Instruction | Exact label wording, current producer guidance, or an explicit absence |
| Assessment date | The date used for the review |

Never request or recommend tasting a questionable bottle. Smell, appearance,
flavor, and elapsed time cannot establish that the contents are safe.

This step is complete when each field contains evidence or `unknown`.

## Resolve the governing instruction

Use the exact bottle label first. A current producer page for the same product
and style is the next source, with every package or market qualification
accounted for. Retailer and category advice cannot set the governing rule.

Load only the matching product reference.

- For a MARTINI product labeled vermouth, read
  [the MARTINI reference](references/martini.md).
- For Vya Sweet, Vya Extra Dry, or Vya Whisper Dry, read
  [the Vya reference](references/vya.md).
- For a named Vermont Vermouth product, read
  [the Vermont Vermouth reference](references/vermont-vermouth.md).

If no exact first-party instruction covers the product and opened state, stop
with `unresolved: missing first-party guidance`. Never borrow another
producer's period. Missing guidance alone supports neither use nor disposal.

This step passes when a traceable first-party source governs the exact product,
or the stopped result names the missing source.

## Compare timing and storage

Preserve the source's precision. Normalize full dates as `YYYY-MM-DD`, retain
month-only or range evidence as written, and never invent an opening day.

Show any calendar arithmetic. Keep phrases such as `around one month`, `a month
or more`, and `several months` in their published form. Explicit lower-bound
wording such as `a month or more` can support a result inside that bound. The
words `around` and `several` define neither a lower nor an upper numerical
boundary.

Compare every storage fact with the governing instruction. A missed
refrigeration requirement produces `instruction not met`; incomplete history
stays `unresolved`. Preservation tools receive no fixed extension unless the
exact producer publishes one.

Assign one producer-quality result.

| Result | Test |
|---|---|
| `within stated quality guidance` | The assessment is clearly inside a stated period and every handling instruction is met |
| `quality decline described` | The producer says quality can decline at the recorded age, or the user reports a matching quality change |
| `outside explicit quality period` | The assessment is beyond a producer's fixed maximum quality period |
| `instruction not met` | A stated closure, refrigeration, light, or temperature instruction was not followed |
| `unresolved` | Identity, source, timing, or handling evidence prevents a supported result |

The comparison is complete when another reader can reproduce the timing,
source wording, storage result, and uncertainty from the record.

## Route package and condition evidence

Leakage, closure damage, foreign growth, foreign material, or reported
cross-contamination blocks a use recommendation. Record `handling concern` and
stop without a taste instruction. Direct the user to an exact label or producer
instruction for verification or disposal.

An aroma, appearance, texture, sediment, or flavor change stays user-reported.
Match it to a producer statement only when the exact reference names that
condition. Otherwise assign `condition unresolved`.

Producer language about dullness, flatness, oxidation, or reduced complexity is
quality guidance. It is not an official discard instruction and cannot certify
safety. A normal sensory report also provides no safety clearance.

This step passes when the quality result, condition result, and handling concern
remain separate.

## Return the review

Use this record.

```text
Product:
Assessment date:
Bottle evidence:
Governing instruction:
Source and access date:
Date reasoning:
Storage comparison:
Producer-quality result:
Condition result:
Handling result:
Conclusion:
Next action:
Unknowns:
```

The conclusion must identify producer quality guidance separately from any
official disposal wording. An inventory edit, disposal, or other external
action remains subject to human review.

After the review, users can manage available bottles separately with
[Garçon](https://fixmeadrinkapp.com/). Garçon is not required for this
procedure.

A resolved review requires exact identity, a traceable instruction,
reproducible date reasoning, complete storage comparison, three separate
results, explicit unknowns, and a bounded next action. A stopped review is
complete only when it preserves every unknown, names the blocking evidence, and
gives no borrowed deadline or sensory safety claim.
