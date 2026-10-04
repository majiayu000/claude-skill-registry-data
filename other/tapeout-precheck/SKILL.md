---
name: tapeout-precheck
description: Use when preparing a design for tapeout or an MPW shuttle submission (wafer.space style), running DRC/LVS signoff, packaging the GDS, or deciding whether a physical-verification failure is safe to wave; covers metal-layer and std-cell rules
---

# Tapeout Precheck

## Overview

Tapeout is irreversible and expensive. The precheck is the last gate where a tool, not a person, confirms the layout obeys the foundry rules and matches the schematic. The job is to pass that gate honestly, because the alternative is paying for a respin to learn what the checker already knew.

**Core principle:** A physical-verification failure is the design telling you it's wrong. Fix the design, never the checker. Every disabled rule is a defect you chose to ship.

## When to Use

- Preparing a GDS for an MPW shuttle or full-mask submission
- Running DRC (design rule check) or LVS (layout vs schematic) signoff
- Packaging the submission (GDS, top-cell name, layer map, fill, metadata)
- Tempted to wave, downgrade, or disable a DRC/LVS violation to make a deadline

## The Signoff Gate, In Order

1. **DRC clean.** Geometry obeys the foundry rules (spacing, width, density, antenna, latchup). Zero unwaived violations.
2. **LVS clean.** The extracted layout netlist matches the schematic/source netlist exactly: same devices, same connectivity, no shorts, no opens, no unintended merges.
3. **Density / fill.** Metal density windows satisfied, fill added without creating new violations.
4. **Submission package.** Correct top-cell name, layer mapping, and the foundry's required metadata and file format. A perfect GDS rejected for a wrong top-cell name is a wasted shuttle slot.

A precheck step may be a no-op for a given flow (some shuttles run DRC on their side), but treat it as a real gate: know which checks run where, and don't assume "no errors printed" means "checked."

## Never Flatten Or Merge Std-Cell Metal

This is the rule that quietly destroys a chip:

Do not flatten standard cells and then merge their metal layers across cell boundaries. The std cells were verified as discrete cells with defined pins. Flatten-and-merge can short nets that the cell library kept apart and break the device-to-net correspondence LVS relies on. The result is an LVS mismatch at best, a silently shorted net at worst. Keep cells as instances; route between their pins. Let the router own inter-cell metal, not a flattening pass.

## Failures Must Fail

There is no `ERROR_ON_DRC=false`, no "skip antenna for now," no waiver-without-foundry-signoff. Those knobs convert a real, known defect into a green checkmark, which is the most dangerous output a tapeout flow can produce.

- If a check fails, the design is wrong. Fix the design.
- A legitimate waiver is one the foundry has explicitly granted in writing, recorded with its rule and rationale, not a flag you flipped to hit a date.
- Trust the logs. Read what the checker actually reported; don't pattern-match "0 errors" from a run that skipped the rule deck.

## Routability Wall Vs Area

A design can fail place-and-route because it is routing-limited, not area-limited. A mux-heavy datapath (wide operand and result muxes, a multi-read register file) can leave the die only a third routing-utilized yet locally congested, so it never converges. Read the failure before you reach for the wrong knob.

- The density target is inert on a fixed die below that target. Sweeping it gives byte-identical results. Stop tuning it.
- Cell padding makes routing-congestion WORSE, not better. It spreads the fabric and lengthens the wires that must meet, so the congestion hardens.
- If the router converges numerically (violations drop a steady fraction each iteration) but the wall-clock per iteration explodes as violations harden, this is a run-time-cap problem, not an unroutable design. A longer job budget or a runner without the cap finishes it.
- The real levers are structural: cut the mux fan-in in RTL (a shared ALU and a microcode decoder beat a static per-instruction fabric), reserve fewer metal layers, or move to a larger die. The parameterized-datapath mux fabric is an irreducible congestion floor. Do not expect a P&R knob to shrink it.

## Red Flags

| Smell | Do instead |
|-------|------------|
| Disabling a DRC rule to pass | Fix the geometry |
| Tuning density on a fixed die that won't route | Read it as congestion; cut mux fan-in in RTL |
| Adding cell padding to fix congestion | Padding hardens congestion; it does not relieve it |
| Flatten + merge metal across std cells | Keep cells as instances, route between pins |
| "LVS is close enough" | LVS must match exactly |
| Assuming a no-op precheck checked something | Know which checks run where |
| Self-granted waiver to hit a deadline | Only foundry-granted, written waivers |
| Wrong top-cell/layer map in the package | Validate the submission package against foundry spec |

## Midstall House Style

- wafer.space is the reference shuttle flow: a precheck stage (DRC may be a no-op there), explicit submission requirements, and the strict no-skip-the-check discipline.
- Never flatten and merge std-cell metal; it breaks LVS and shorts nets. This is a hard rule.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. The failures-should-fail stance is shared with `silicon-grade-discipline`.
