---
name: cargo-securement
description: |
  Use this skill when the user asks about cargo securement requirements under 49 CFR 393 Subpart I — Working Load Limit (WLL), tiedown counts, tiedown types, commodity-specific securement rules (lumber, metal coils, paper rolls, concrete pipe, intermodal containers, vehicles, large boulders, dressed lumber, building materials), CVSA out-of-service criteria, and how to calculate aggregate WLL. Cite 49 CFR 393.100-136.
---

# Cargo Securement — 49 CFR 393 Subpart I

Cargo securement violations are one of the most common roadside findings + can cause OOS. Subpart I sets:

- General requirements that apply to all loads
- **Commodity-specific** rules for 8 categories of cargo (each with its own subsection)

## Working Load Limit (WLL)

Every tiedown, anchor point, edge protector, and other securement device has a manufacturer-rated **WLL**. The aggregate WLL of all tiedowns must equal at least HALF the cargo weight.

```
Aggregate WLL  ≥  Cargo Weight ÷ 2
```

Example: 40,000 lb cargo requires aggregate WLL of ≥ 20,000 lb.

Each tiedown's WLL is marked on the device by the manufacturer (chain, strap, wire rope, etc.). If the marking has worn off, you can't use it.

## Tiedown count minimum (49 CFR 393.110)

In addition to the WLL requirement:

- **Minimum 1 tiedown** for every 10 feet of cargo length AND 1 for each piece
- Or per commodity-specific rules

So an 18-foot piece of equipment requires at least 2 tiedowns (one for each 10 feet of length).

## Tiedown types

- **Chain** with grade marking (e.g., G70, G80, G100)
- **Synthetic web strap** (most common)
- **Steel cable / wire rope**
- **Manila / synthetic rope** (rarely; not for heavy loads)
- **Steel strapping**

WLL is set by the WEAKEST component in the tiedown system (chain + binder + hook + anchor — whichever has the lowest WLL).

## Commodity-specific rules

| Cargo Type | Section | Key requirement |
|---|---|---|
| Lumber / Dressed lumber | 393.118 | Width of stack, height limits, special tiedown placement |
| Metal coils | 393.120 | Side-by-side coils need separate securement; longitudinal vs transverse rules |
| Paper rolls | 393.122 | Special stacking + tiedown for vertical and horizontal coils |
| Concrete pipe | 393.124 | End cap tiedowns + side tiedowns; size-dependent |
| Intermodal containers | 393.126 | Twist-lock requirements; size-dependent |
| Automobiles / light vehicles | 393.128 | Wheel chocks + tiedowns at each corner |
| Heavy machinery | 393.130 | Multi-point tiedowns; chain rated to commodity weight |
| Crushed cars (e.g., for scrap) | 393.132 | Side panel + ceiling tiedowns |
| Roll-on / Roll-off containers | 393.134 | Twist-lock + chain |
| Boulders / Large rocks | 393.136 | Wedging + tiedown |

## General rules that apply to all cargo (49 CFR 393.102-110)

1. **No leakage / shifting** during transport
2. **No falling, blowing off, leaking** of cargo
3. **No interference with driver's freedom of movement**
4. **No obstruction of view** to front/sides/mirrors
5. **Securement system must withstand:**
   - 0.8g forward deceleration
   - 0.5g lateral acceleration
   - 0.5g rearward acceleration
   - 0.2g downward

## Edge protectors

For straps tightened over angular edges (e.g., I-beams, lumber stacks), edge protectors are required. They preserve the WLL of the strap by reducing point load on the strap fiber.

## Driver inspection requirements (49 CFR 392.9)

The driver must:

- Inspect cargo securement before each trip
- Re-inspect after the first 50 miles
- Re-inspect every 150 miles thereafter OR every 3 hours OR when the duty status changes (whichever first)
- Document re-inspections (typically in the DVIR)

## OOS criteria (CVSA / 49 CFR 393)

Common cargo securement OOS findings:

- Aggregate WLL < 50% of cargo weight
- Tiedown count insufficient for cargo length
- Damaged tiedown (visible wear, frayed strap, cracked chain link)
- Missing or improperly installed edge protectors
- Improperly secured commodity-specific items (e.g., metal coil without proper side restraint)

## Calculating aggregate WLL — example

40,000 lb cargo. Driver has:

- 4 chain tiedowns @ 5,000 lb WLL each = 20,000 lb aggregate

Aggregate WLL = 20,000 lb. Cargo weight = 40,000 lb. Half = 20,000 lb. **Meets requirement (just).**

But the cargo is 12 feet long, so 2 tiedowns minimum required (1 per 10 feet). 4 tiedowns is more than enough on count. WLL is the binding constraint.

If the cargo were 22 feet long, 3 tiedowns minimum. WLL still met because 4 tiedowns × 5,000 = 20,000 lb.

## Common mistakes

1. **WLL marking not legible.** If you can't read it at roadside, inspector treats as zero WLL. Re-mark or replace.
2. **Chain or strap visibly damaged.** Even within WLL spec, visible wear = OOS.
3. **Wrong commodity-specific rule applied.** E.g., a steel coil treated as generic cargo missing the side restraints required by 393.120.
4. **No mid-trip re-inspection.** Roadside inspector asks "when was last re-inspection?" — driver shrug = violation.
5. **Single chain through both axles of a vehicle counts as one tiedown** for the multi-point requirement — not enough.

## Where this fits in X3

X3 doesn't track cargo securement directly (that's an in-cab tool, not a fleet management feature). But cargo-securement violations DO show up on roadside inspection reports + feed the Vehicle Maintenance BASIC. X3's `inspections.html` surfaces these violations to safety managers for coaching.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=cargo-securement

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
