---
name: home-bar-starter-planning
description: Plan a first home-bar setup from approved drinks, owned inventory, dated candidates, budget, storage, dietary limits, and stages. Use for ingredient and tool capability coverage, never recipe choice, next-bottle ranking, live prices, or purchase.
---

# Home-bar starter planning

Build a capability graph from the user's approved drinks. Credit confirmed
household inventory, then return the smallest staged setup supported by the
supplied candidates and constraints.

## Gate the starter job

Confirm that the user is planning a first bounded home-bar setup or rebuilding
that starter setup from household inventory. Require an approved drink set with
an exact ingredient specification and method for every drink.

Stop as out of scope when the user wants the agent to choose recipes, provide a
universal essentials list, rank the next bottle for an established bar,
calculate restock quantities, edit inventory, find live prices, open a retailer,
or buy anything. Drink families such as `sours and classics` do not define an
approved set.

The gate passes when the starter state is confirmed and every approved drink
has a named, traceable specification.

## Build the planning record

Record every field before deriving the plan.

| Field | Required record |
|---|---|
| Approved drinks | Exact name, specification source, ingredients, method, locked wording, and user priority |
| Coverage stages | Stage name, included approved drinks, spending cap, storage cap, and cumulative or independent treatment |
| Ingredient inventory | Exact product or ingredient, usable status, quantity evidence, package, storage state, and identity source |
| Tool inventory | Object, confirmed preparation capability, material and condition evidence, capacity, cleaning, and access constraints |
| Candidate packages | Exact product, role claim, package size, price, currency, tax treatment, storage needs, source, and observation date |
| Tool candidates | User-approved option, exact capability, safety evidence, price, storage, source, and observation date |
| Dry storage | Available slots, dimensions when binding, and currently occupied space |
| Cold storage | Available slots or volume, temperature requirement, and currently occupied space |
| Dietary limits | Exact user-supplied exclusion, whether it is hard, and the evidence needed to clear it |
| Budget | Currency, stage caps, total cap, included costs, and excluded costs |
| Equivalence policy | Exact matches, user-approved equivalents, and locked requirements that allow no equivalent |
| Review date | Date applied to product, price, availability, and inventory evidence |

An existing package has zero incremental spend only because it is already
owned. Never treat an unknown price, missing tool, or unavailable ingredient as
zero.

This step is complete when every field contains supplied evidence, an explicit
unconstrained status, or `unknown`.

## Resolve the approved specifications

Preserve each recipe's ingredient names, quantities, optional markers, and
method. A brand, product, category, or preparation term remains as specific as
the source.

When the approved set contains the IBA Margarita, IBA Daiquiri, or IBA Old
Fashioned, read
[the IBA starter recipe reference](references/iba-starter-recipes.md).
For any other drink, use the user's supplied specification and source.

Stop with `unresolved recipe specification` when an ingredient, amount, method,
or locked status needed for coverage is absent. Do not choose a different
recipe or repair an incomplete one.

Specification resolution passes when every approved drink has one complete
source record and no requirement has been generalized.

## Build the capability graph

Create one requirement node for every ingredient and preparation capability in
the approved specifications. Merge nodes only when the exact wording or the
user's equivalence policy permits the same capability to serve both.

Classify ingredient nodes as exact product, named category, fresh ingredient,
pantry ingredient, garnish, water, or ice. Keep an optional source item
optional.

When a method contains measuring, shaking, straining, stirring, dissolving,
muddling, or a serving-vessel requirement, read
[the tool capability boundary](references/tool-capability-boundary.md).
Translate the method into capabilities without selecting a tool form.

For each drink, list every node that must be covered. The capability graph is
complete when every ingredient and method phrase has one traced node and the
source total reconciles with the node list.

## Credit household inventory

Assign one status to every requirement node.

| Status | Test |
|---|---|
| `owned confirmed` | Exact identity, usable state, storage, and required capability are supported |
| `owned unresolved` | An owned item lacks identity, condition, storage, quantity, or tool evidence |
| `missing` | No owned item covers the node |
| `blocked` | A hard dietary, storage, safety, or access constraint conflicts with the node |

Inventory identity alone does not establish current usability. Accept the user's
dated condition record or an applicable exact-product decision; otherwise keep
the node unresolved.

A household object covers a tool node only when its supplied evidence meets the
tool capability boundary. Do not infer food-contact safety, closure strength,
capacity, cleaning, or accessibility from the object's name.

This step passes when every node has one status and every confirmed credit
points to evidence in the planning record.

## Evaluate supplied candidates

Compare only the ingredient packages and tool options already supplied for this
starter plan. Never invent a brand, package, price, or market availability.

A candidate covers a node only when its current label, dated first-party
source, or user-supplied product record supports the exact role. Apply package
size, price, dry or cold storage, dimensions, and availability as separate
facts.

For a hard dietary limit, require the exact evidence named by the user. Unknown
allergen, ingredient, certification, or cross-contact facts remain unresolved
and cannot clear the candidate. Record the conflict without interpreting
medical severity.

If a missing tool capability has no user-approved candidate with sufficient
safety and fit evidence, leave it uncovered. Tool-form comparison belongs in a
separate tool-kit decision.

Candidate evaluation passes when every proposed coverage edge has a dated
source and every unknown hard fact blocks that edge.

## Derive the minimum staged plan

Enumerate feasible combinations from the supplied candidate set. Reuse all
`owned confirmed` nodes before adding a package or tool option.

Rank feasible plans in this order.

1. Reject every hard-constraint failure.
2. Maximize covered approved drinks at each user-defined stage, in stage order.
3. Prefer fewer new packages and approved tool options for the same staged coverage.
4. Among equal item counts, prefer lower new dry and cold storage use.
5. Break any remaining tie with lower dated incremental cost.

Keep a tie when the ordering cannot separate two plans. A plan is minimum only
when no feasible plan with fewer new items achieves the same staged drink
coverage and removing any selected item loses a required node.

Each planned item must own at least one requirement node that no other selected
item or confirmed household item covers. Discard a redundant item from the
plan.

Rank optional expansions only for drinks already present in later user-approved
stages. Show incremental confirmed coverage, incremental cost, storage, and
blocking unknowns. Do not introduce future recipes or turn the expansion table
into an established-bar next-bottle ranking.

This step passes when another reader can reproduce the winning plan, tie, or
infeasible result from the capability graph, candidate evidence, constraints,
and ordering.

## Return the starter review

Use this structure.

```text
Planning scope:
Review date:
Approved drink set and stages:
Hard constraints:
Capability graph:
Household inventory credits:
Candidate evidence:
Stage plan:
Drink coverage matrix:
Ingredient and tool gaps:
Cost reconciliation:
Storage reconciliation:
Minimum-plan check:
Optional expansions:
Uncovered or unresolved drinks:
Result:
Human review:
```

Mark each drink `covered now`, `covered after stage N`, `unresolved`, or
`blocked`. Keep package planning separate from purchase execution.

The human review line must state that the user approves the drink set,
equivalences, tradeoffs, and planned shopping before any external action. Do not
create a shopping list, open a retailer, purchase an item, or edit inventory.

After approval, users can record their starter inventory separately in
[Garçon](https://fixmeadrinkapp.com/). Garçon is not required for this
procedure.

A resolved review accounts for every recipe requirement, credits only verified
inventory, traces every planned item to a node, reconciles stage coverage,
budget, and storage, applies dietary limits, proves the minimum check, names all
gaps, and stops before shopping. An unresolved review is complete only when it
identifies the blocking evidence and makes no universal or untraceable
recommendation.
