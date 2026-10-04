---
name: cocktail-syrup-conversion
description: Convert a known pure-sucrose syrup to another known pure-sucrose concentration while preserving the sugar dose. Use when the user supplies mass-based composition evidence and needs a mass conversion plus a water correction.
---

# Cocktail syrup conversion

Convert one declared pure-sucrose-and-water syrup into another on a mass basis.
Preserve the original sucrose dose, expose the water difference, and refuse
composition guesses.

## 1. Gate the conversion

Accept the job only when every syrup in the calculation contains sucrose and
water with no other dissolved material.

| Request | Route |
|---|---|
| Honey, agave, invert syrup, gomme, fruit, spice, acid, salt, or mixed sweetener | Ingredient-specific formulation review |
| Unknown commercial syrup | Producer specification or laboratory measurement |
| Make a syrup from raw ingredients | Syrup preparation procedure |
| Rebalance a complete drink by taste | Recipe development |
| Convert a recipe to more servings | Cocktail recipe scaling |

A name such as `simple`, `rich`, `semi-rich`, `one-to-one`, or `two-to-one`
does not establish composition by itself. Require a declared mass ratio, a
producer mass fraction for the exact product, or a compatible measurement.
Do not suggest adding flavoring and treating its dissolved contribution as
negligible. A flavored result stays outside this exact branch.

Return `STOPPED: COMPOSITION NOT ESTABLISHED` when either concentration lacks
traceable evidence or when another solute is present. State the evidence needed
for a future run without issuing a substitute amount.

A specification that states sucrose mass does not move a flavored or mixed
commercial product into this pure-sucrose-water branch. Route that product to
an ingredient-specific formulation review.

Complete this step when the original and replacement products both pass the
pure-sucrose-and-water gate.

## 2. Establish the mass basis

Record the original syrup amount as mass. When the recipe gives a volume,
convert it only if the user supplies a density for that exact composition at
the stated temperature.

Read [the composition evidence](references/composition-evidence.md) when a
ratio, refractometer value, density, or volume enters the request.

Normalize each supported concentration to a sugar mass fraction between zero
and one.

```text
sugar mass fraction = sugar mass / final syrup mass
```

For a ratio declared as sugar mass to water mass:

```text
sugar mass fraction = sugar parts / (sugar parts + water parts)
```

Do not treat a ratio by volume as a ratio by mass. A refractometric dry
substance reading supports exact sucrose arithmetic only for a sucrose-water
solution under a compatible method. Other dissolved material makes the result
an approximation, which stays outside this exact conversion.

Return `STOPPED: MASS BASIS MISSING` when the original amount is volume-only
and compatible density evidence is absent.

Complete this step when the original syrup mass and both sugar mass fractions
are traceable.

## 3. Freeze the conversion contract

Record these inputs before calculating.

| Field | Required value |
|---|---|
| Original syrup | Identity, composition source, mass, sugar fraction |
| Replacement syrup | Identity, composition source, sugar fraction |
| Temperature | Required when density converts volume to mass |
| Precision | Scale resolution and requested rounding increment |
| Tolerance | Maximum accepted sucrose-dose deviation after rounding |
| Preservation target | Sugar dose only, or sugar dose plus recipe water |
| Adjustable water | Amount and location of independent water available for correction |

The default target preserves the sucrose dose. Preserving total recipe water
also requires an identified water component that can absorb the correction.

If the correction requires removing more independent water than the recipe
contains, return `STOPPED: WATER CORRECTION INFEASIBLE`. Do not remove spirit,
juice, or another ingredient to force the total.

Complete this step when the target and any adjustable water are explicit.

## 4. Calculate on mass

Use the deterministic script when the exact gate passes.

```bash
python3 scripts/convert_syrup.py --input /absolute/path/to/input.json
```

The calculation follows this contract.

```text
original sugar mass = original syrup mass * original sugar fraction
replacement syrup mass = original sugar mass / replacement sugar fraction
original water mass = original syrup mass - original sugar mass
replacement water mass = replacement syrup mass - original sugar mass
water correction = original water mass - replacement water mass
```

A positive water correction means add that mass of independent water. A
negative correction means remove its absolute mass from an identified water
component.

Show unrounded intermediate values and the rounded service values. Rounding
must respect the scale resolution. Never convert the mass result to volume
without compatible density evidence.

Complete this step when another reader can reproduce each value from the
supplied inputs.

## 5. Reconcile the recipe

When the user wants sugar dose only, replace the original syrup with the
calculated replacement mass and expose the changed water contribution.

When the user also wants recipe water preserved, apply the calculated
correction only to the declared independent water component. Recalculate its
remaining mass and verify it is not negative.

Report two checks.

| Check | Passing condition |
|---|---|
| Sugar equivalence | Rounded replacement sugar stays within the declared mass tolerance |
| Water equivalence | Original water equals replacement water plus the applied correction |

Volume, sensory balance, viscosity, acidity, flavor intensity, and finished
dilution remain outside the arithmetic result. A user-performed tasting or
recipe-development review owns those outcomes.

Complete this step when the revised ingredient masses pass the requested
equivalence checks without changing an undeclared component.

## 6. Return the worksheet

Use these sections in order.

1. Status
2. Evidence register
3. Normalized mass fractions
4. Sugar-dose calculation
5. Water correction
6. Revised recipe lines
7. Rounding and tolerance check
8. Unknowns and human review

Valid completion states are `EXACT MASS CONVERSION`, `EXACT SUGAR CONVERSION:
WATER CHANGE DISCLOSED`, or one documented stop state.

A stopped result can show an intermediate candidate mass when that value proves
a later feasibility failure. Label it `CALCULATED: NOT AUTHORIZED`, issue no
revised recipe, and keep the original recipe unchanged. A composition or mass
basis stop contains no substitute mass. An exact result contains no unsupported
volume, sensory, shelf-life, or commercial-product claim.

The skill is complete when the sugar dose is reproducible, the water difference
is visible, every composition source is traceable, and the user can review the
revised recipe before making it.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can supply a recipe for a separate
conversion exercise. Recipe discovery is outside this calculation.
