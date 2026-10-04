---
name: cocktail-tool-kit-planning
description: Plan a minimum cocktail-tool capability set from approved recipes, verified owned equipment, measured substitutes, constraints, and supplied candidates. Use for a first kit or equipment-gap audit; exclude recipe, bottle, shaker-type, glassware-set, live-price, and checkout decisions.
---

# Cocktail tool-kit planning

Build a coverage map from the user's approved recipe methods. Credit verified
owned capabilities, then identify the smallest required capability set and any
feasible implementation from supplied product facts.

## Gate the capability job

Confirm that the user wants a first cocktail-tool plan or an audit of equipment
for a bounded, user-approved recipe set. Require one exact ingredient
specification and method source for every target recipe.

Stop with `unresolved target methods` when the user supplies drink families,
asks the agent to choose recipes, or omits a method needed for capability
extraction. Do not replace the missing recipe or infer a standard edition.

Treat bottle choice, ingredient substitution, universal bartender kits,
shaker-type comparison, glassware-set selection, current market search,
shopping-list creation, inventory editing, retailer access, and checkout as
separate jobs.

The gate passes when the target recipes and method editions are fixed and the
requested result is capability coverage rather than a universal product list.

## Build the planning record

Record each field before assigning coverage.

| Field | Required record |
|---|---|
| Target recipes | Exact name, source, ingredient quantities, method, optional markers, batch or serve count, and user priority |
| Technique limits | Locked method wording, user-authorized technique equivalence, and prohibited changes |
| Owned tools | Exact identity, intended use evidence, material, condition, measured capacity or precision, cleaning state, storage, and accessibility |
| Household substitutes | Object identity plus the same evidence required for a purpose-built tool |
| Supplied candidates | Exact model, claimed capabilities, manufacturer source, dimensions, capacity, material, cleaning instructions, price, currency, tax treatment, availability, and observation date |
| Constraints | Budget, storage dimensions, cleaning method, dexterity, reach, grip, noise, power, heat, and breakage limits |
| Hazard review | Sharp, pressure, heat, glass, powered-equipment, food-contact, and qualified-review evidence |
| Review date | Date applied to product facts, prices, availability, condition, and measurements |

Use `unknown` for absent facts. A missing price, capacity, safety fact, or
storage dimension never becomes zero or an assumed pass.

Planning input is complete when each field contains supplied evidence, an
explicit unconstrained status, or `unknown`.

## Extract the coverage map

Preserve every method verb, quantity, vessel requirement, batch count, and
optional marker. When the approved set names the current IBA Margarita, IBA
Daiquiri, or IBA Stinger, read
[the IBA method fixtures](references/iba-method-fixtures.md).
Use the user's exact sourced specification for any other recipe.

Create one node for each preparation capability. Separate actions that need
different evidence, even when one object can cover both. Measurement range and
precision, working capacity, closure behavior, mixing action, separation,
serving capacity, cleaning, and access remain distinct attributes.

Classify a node `required` when failure prevents the sourced method. Mark it
`optional` only when the source or user explicitly allows omission. Convenience,
speed, appearance, and upgrade value cannot turn an optional node into a
requirement.

Read [the capability evidence gates](references/capability-evidence-gates.md)
when translating a method, evaluating an owned object, or checking a supplied
candidate.

Capability extraction passes when every method phrase traces to a required or
optional node, recipe liquid amounts reconcile, and no product form has been
selected.

## Audit owned capability

Assign one status to every owned tool and household substitute.

| Status | Test |
|---|---|
| `owned verified` | A purpose-built tool has current evidence for the exact capability, load, condition, cleaning, storage, and access constraints |
| `substitute verified` | A household object clears the same evidence gates for the exact capability and measured load |
| `unresolved` | Identity, intended use, material, condition, measurement, cleaning, storage, or access evidence is incomplete |
| `out of service` | Damage, contamination, incompatibility, or a supplied restriction prevents use |
| `not owned` | No owned object was supplied for the node |

An object's name proves nothing beyond its identity. Do not credit a jar,
kitchen glass, spoon, knife, sieve, blender, or other household item from common
use alone.

Sharp, pressure, heat, glass, and powered-equipment capabilities require exact
manufacturer guidance for the model and intended operation or a supplied
qualified review. Missing guidance leaves the object unresolved. Never propose
a trial that exposes the user to the unresolved hazard.

Map each verified object to every capability it supports and count its storage
once. Current capability review is complete when every owned object has one
status and each credited edge points to exact evidence.

## Derive the minimum capability set

Combine equal capability nodes only when one verified object can satisfy every
linked recipe at its stated batch, precision, cleaning, and access limits.
Preserve separate nodes when loads, methods, hazards, or user constraints
conflict.

Reuse `owned verified` and `substitute verified` capabilities before adding a
missing requirement. Required gaps form the minimum capability set. Optional
nodes stay in a separate useful-later section and never count as recipe
coverage.

Mark each target recipe `covered now`, `missing capability`, `unresolved
evidence`, or `blocked`. Name every node behind a non-covered status.

The set is minimum when each required node is covered exactly once or by a
documented multifunction edge, no optional node enters the requirement count,
and removing any added capability leaves at least one approved recipe
unsupported.

## Evaluate supplied implementation candidates

Evaluate only candidates that the user supplied after the capability set is
fixed. Never invent a model, price, material, dimension, certification,
availability fact, or retailer.

A candidate covers a node only when its dated manufacturer evidence clears the
exact capability and all applicable evidence gates. Record product facts
separately from capability requirements.

Enumerate feasible combinations from the supplied candidates. Apply the
ordering below without making a universal product judgment.

1. Reject safety, access, cleaning, storage, and budget failures.
2. Maximize required recipe coverage in user priority order.
3. Prefer fewer added objects for equal coverage.
4. Use lower occupied storage when object counts tie.
5. Break any remaining tie with lower dated incremental cost.

Retain tied combinations. A comparison between tool forms, materials, brands,
or aesthetics belongs to a separate product-selection decision unless the user
already supplied a binding criterion.

Run a deletion check on each proposed object. Removing it must break a required
coverage edge that no verified owned object or remaining candidate covers.

Candidate evaluation is complete when every proposed edge is evidence-backed,
cost and storage totals reconcile, ties remain visible, and unsupported recipes
keep their gaps.

## Return the review package

Use this structure.

```text
Planning scope:
Review date:
Approved recipes and methods:
Constraints:
Required capability map:
Optional capability map:
Owned-tool audit:
Verified substitutes:
Unresolved or out-of-service objects:
Minimum capability set:
Recipe coverage:
Supplied candidate evidence:
Feasible implementation scenarios:
Cost reconciliation:
Storage and cleaning reconciliation:
Safety and access review:
Deletion check:
Unsupported recipes:
Result:
Human review:
```

Keep the capability result separate from the supplied-product scenario. The
human review line must request approval of recipe scope, capability
equivalences, evidence judgments, tradeoffs, and any planned product choice.

Stop before a shopping list, retailer visit, checkout, purchase, inventory
change, or tool-use trial involving an unresolved hazard.

A complete review accounts for every method phrase, credits only verified
objects, separates required and optional capabilities, traces each added object
to a unique required edge, reconciles constraints, names unsupported recipes,
and stops before external action. An unresolved review is complete only when it
identifies the missing evidence without recommending an unsafe substitute.
