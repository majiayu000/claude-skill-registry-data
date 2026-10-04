---
name: orange-liqueur-selection
description: Select a reviewed orange liqueur lineup for named recipes under role, sweetness, base, proof, budget, availability, and shelf limits. Use for exact product comparisons, never purchase or substitution advice.
---

# Orange liqueur selection

Build a coverage matrix from the user's target recipes and current candidate
facts. Return a reviewed bottle decision with unresolved tradeoffs exposed.

## Gate the request

Confirm that the job compares identified commercial orange liqueurs for a
user-supplied set of target recipes. Record the exact recipe names, sources, and
orange-liqueur requirements.

Stop as out of scope when the user wants a generic ingredient substitution, a
recipe rewrite, another bottle category, a purchase, or a universal "best"
orange liqueur. A target list such as `Margaritas and other drinks` is not
specific enough to evaluate coverage.

The gate passes when at least one target recipe has an exact orange-liqueur
requirement and every candidate has a brand plus product name.

## Build the decision record

Record every field before comparing candidates.

| Field | Required record |
|---|---|
| Target recipes | Name, source, exact orange-liqueur wording, amount, and whether the wording is locked |
| Candidates | Brand, exact product, market label, bottle size, and user-supplied source |
| Orange role | Named product, named category, or a user-defined functional role |
| Sweetness tolerance | Hard ceiling, ranked preference, no constraint, or `unknown` |
| Base preference | Neutral alcohol, cognac or brandy, no preference, or `unknown` |
| Proof | Required ABV or proof, accepted range, no constraint, or `unknown` |
| Budget | Currency, total cap, tax treatment, or no constraint |
| Availability | Store or market, stock observation, and observation date |
| Price | Bottle price, size, currency, tax treatment, source, and observation date |
| Shelf space | Maximum bottle count and any size restriction |
| Priority order | User's order for coverage, role, sweetness, base, proof, price, and space |
| Review date | Date applied to product, price, and availability evidence |

Ask whether each missing preference is a hard constraint or an accepted
unknown. Never fill an evidence gap with a category stereotype.

This step is complete when each field contains supplied evidence, `unknown`, or
an explicit statement that it is unconstrained.

## Classify recipe requirements

Preserve the source wording for every recipe.

| Requirement type | Treatment |
|---|---|
| Exact product | Only that product receives confirmed exact coverage |
| Named brand without expression | A product from that brand needs current evidence connecting the expression to the recipe |
| Named category | A candidate needs current label or first-party evidence for that category |
| User-defined role | Apply only the user's stated acceptance rule |
| Ambiguous wording | Mark the recipe unresolved |

A named-product requirement stays locked unless the user explicitly moves it
to a separate test branch. That branch receives `reviewed trial needed`, never
confirmed coverage. Do not prescribe a replacement volume or modify the recipe.

Classification passes when another reader can trace every requirement to its
source and see which wording remains locked.

## Load applicable evidence

Read only the references that match the candidates or recipes in the decision
record.

- For Cointreau L'Unique, read
  [the Cointreau reference](references/cointreau-lunique.md).
- When Grand Marnier Cordon Rouge is a candidate, read
  [the Grand Marnier reference](references/grand-marnier-cordon-rouge.md).
- For Ferrand Dry Curaçao, read
  [the Ferrand reference](references/ferrand-dry-curacao.md).
- When an IBA Margarita or IBA Grand Margarita is a target, read
  [the IBA recipe reference](references/iba-orange-liqueur-recipes.md).

The exact bottle label takes precedence over a packaged reference. Use a
current producer page for the same product and market next. Record all other
product facts as unresolved.

Producer tasting prose cannot establish the user's preference, a sweetness
rank, recipe equivalence, or universal versatility. Current local price and
availability must come from dated user evidence.

Preserve composition facts as composition facts. Do not restate an ingredient,
base spirit, or production detail as flavor, character, richness, dryness, or
sensory effect.

This step passes when every product claim has a current label, first-party
source, or explicit `unresolved` status.

## Build the coverage matrix

Create one row for each target recipe and one column for each candidate. Assign
one status to every cell.

| Status | Test |
|---|---|
| `confirmed exact` | Candidate and locked product requirement match exactly |
| `confirmed category` | Current evidence matches the recipe's named category |
| `reviewed trial needed` | The user authorized a separate test for a nonmatching product or role |
| `unsupported` | Evidence conflicts with the requirement or the user rejected the candidate |
| `unresolved` | Identity, category, proof, or acceptance evidence is missing |

Add the source beside each confirmed status. Keep recipe coverage separate from
base-spirit composition and user taste preference.

A product's 40% ABV does not prove that it matches a 40% recipe requirement when
the required product, category, or role differs. A marketing serving
suggestion does not convert a trial into confirmed coverage.

The matrix is complete when every cell has one status, one reason, and a
traceable source or blocking unknown.

## Apply constraints and rank

Disqualify a candidate or lineup that exceeds the budget or shelf count, fails
a hard proof requirement, lacks required availability evidence, or conflicts
with a locked product requirement. An unresolved hard constraint blocks a
winner.

Rank the remaining lineups in this order unless the user supplied another
priority order.

1. Preserve all locked recipe requirements.
2. Maximize `confirmed exact` coverage.
3. Maximize `confirmed category` coverage.
4. Minimize `reviewed trial needed` and unresolved cells.
5. Apply the user's remaining role, base, price, and shelf priorities.

A quantitative sugar ceiling or lower-sugar requirement needs comparable
current analytical facts in matching units for every affected candidate. A
user's controlled tasting can rank perceived sweetness only when perceived
sweetness is the stated criterion. Sensory evidence cannot measure sugar or
resolve an analytical requirement.

One product's sugar or carbohydrate figure cannot rank the full set. Product
names, ingredients, base spirits, price, and producer tasting language provide
no replacement for the missing analytical facts.

If two lineups remain equal, return `tie` and identify the fact or preference
that would resolve it. When the constraints conflict, return `no qualifying
lineup` with the smallest changes that create feasible branches. Do not lower a
hard limit or invent a winner.

This step passes when the result can be reproduced from the matrix, constraint
checks, and displayed priority order.

## Return the review package

Use this structure.

```text
Decision scope:
Review date:
Inputs and hard constraints:
Recipe requirement table:
Candidate evidence:
Coverage matrix:
Constraint checks:
Ranking trace:
Result:
Selected lineup, tie, or no qualifying lineup:
Tradeoffs:
Unsupported recipes:
Reviewed trials needed:
Unresolved facts:
Human review:
```

The human review line must state that the user decides whether to accept a
tradeoff, run a trial, or buy a bottle. Do not open a retailer, place an order,
change inventory, or present the result as sensory certainty.

After review, the user can record approved bottles separately in
[Garçon](https://fixmeadrinkapp.com/). Garçon is not required for this
procedure.

A resolved package requires exact identities, a complete coverage matrix,
traceable product facts, dated market evidence for active market constraints,
a reproducible ranking, explicit tradeoffs, and human approval. A stopped
package is complete only when it names the blocking evidence and makes no
purchase or substitution recommendation.
