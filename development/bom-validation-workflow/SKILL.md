---
name: bom-validation-workflow
description: |-
  Use when validating a Bill of Materials (BOM) for a Maker-3D project — an embedded controller project, a speaker/audio build, a smart-home build, or any other physical build with more than 5 components. Trigger on phrases like "check the BOM", "validate the parts list", "review the parts list", "missing components", "reconcile parts inventory", "check hardware stock", "what still needs to be ordered", "check BOM against stock", "audio build BOM", "BOM review". Do NOT load for software dependency lists (use package.json/requirements.txt tooling), for pure schematic checks without physical components, or when the project has only 1-2 components (cost/benefit ratio too low). Encodes the end-to-end-builder pattern: before ordering, check against the hardware stock; do not forget connections + consumables.
---

# BOM Validation Workflow

When a Maker-3D project (embedded controller, audio build, smart-home build) has its component list defined, the typical next step is: create an order list. A frequent failure point: connection parts (cables, connectors, screws), consumables (filament, solder, thermal paste), and existing stock are forgotten. Result: 2-3 deliveries instead of one, plus blocked wait time.

This skill brings a disciplined workflow: extract the BOM, reconcile with the hardware stock, identify missing components CATEGORIZED (main parts, connections, consumables), deliver an order list with estimated prices + sources.

## When to use

- A spec note has a component table or list (>5 items)
- Before an order at a parts retailer / Amazon / AliExpress
- During the transition from design phase to build phase (see `design-first-iteration` + `cad-construction`)
- When the user asks "can I build this now?" or "what's still missing?"
- Cross-project check: ordering a part useful for multiple projects together

## When NOT to use

- Pure software projects with `requirements.txt`/`package.json` — other tools
- Schematic reviews without a physical component question (schematic check is separate)
- Projects with 1-2 components — discipline overhead not justified
- The spec note doesn't have a BOM table yet — first finish design, then extract BOM

## Workflow (4 phases)

### Phase 1: BOM extraction from spec

Read the project spec note and extract ALL components. Pay particular attention to:

- **Main parts**: microcontrollers, sensors, actuators, displays, batteries
- **Structural parts**: printed parts (with material + quantity), aluminium profiles, wood
- **Connection parts** (often forgotten): cables with lengths, connectors (JST/Dupont/XT60), screws (size + length + material), nuts, standoffs
- **Consumables**: filament quantities (in grams), solder, flux, thermal paste, cable ties, heat-shrink tubing
- **Hidden prerequisites**: power supply (adapter + plug), tools you don't yet own, programming adapters

Output as a structured table:

```markdown
| Category | Component | Quantity | Spec | Source in note |
|---|---|---|---|---|
| Main part | ESP32-S3-WROOM-1 | 1 | 16 MB Flash | line 45 |
| Connection | JST-PH 4-pin | 5 | with 200mm cable | line 67 |
| ... | | | | |
```

**Mandatory**: every component documented with source line in the spec. If unclear → ask explicitly, don't guess.

### Phase 2: Hardware-stock reconciliation

Read the hardware-stock inventory (typically a vault note such as `Hardware-Lager.md` or an equivalent inventory file).

Per BOM entry: is stock available?

```markdown
| Component | Required | In stock | Difference | Status |
|---|---|---|---|---|
| ESP32-S3-WROOM-1 | 1 | 3 | +2 | ✓ available |
| JST-PH 4-pin cable | 5 | 0 | -5 | ❌ to order |
| WS2812B LED strip 1m | 1 | 0.5 m | -0.5 m | ❌ to order (or shorten design) |
| M3x10 hex socket | 12 | 50 | +38 | ✓ available |
```

**Important**: check not only existence but also sufficient quantity. The user has an installation history in the stock — existing parts may be earmarked for other projects.

### Phase 3: Order list with categorization

From the ❌ items: consolidated order list, sorted by source (minimizes shipping costs):

```markdown
## Order

### Parts retailer (≈ €8-12 shipping)
| Component | Qty | Unit price | Total | Article No |
|---|---|---|---|---|
| JST-PH 4-pin cable 200mm | 5 | €1.20 | €6.00 | JST-PH-4-200 |
| ... | | | | |
| **Sum retailer** | | | **€23.40** | |

### Amazon (often Prime → no shipping)
| ... | | | | |

### AliExpress (long, plan ahead!)
- Delivery time: 2-4 weeks
| ... | | | | |

## Total
- Parts retailer: €23.40
- Amazon: €12.99
- AliExpress: €8.50
- **TOTAL: €44.89** + shipping ≈ €60
```

### Phase 4: Plausibility check + reminder

Before order submit, check explicitly:

1. **Are all connection parts included?** (cables, connectors, screws)
2. **Consumables not forgotten?** (filament reserve, solder if needed)
3. **Tools?** (crimpers, soldering-iron tips)
4. **Reserve factor**: critical small parts (LEDs, resistors, microcontrollers) always order +1 or +20% — shipping frustration when one breaks
5. **Cross-check**: other open projects with similar components? Synergy order possible?
6. **Finish/material conformity**: if the project has a required accent color or material spec, check that stock is on hand before ordering the rest

Output: confirmed order list + update suggestion for hardware stock (what will be earmarked WHEN for WHICH project).

## Anti-patterns

- ❌ **Ordering on the fly without stock check**: leads to duplicate orders, forgotten small parts, blocked wait times
- ❌ **Overlooking connection parts**: "I probably have the cables somewhere" → at build start they're missing → one-week delay
- ❌ **Forgetting consumables**: 200g filament reserve missing mid-print → print lost
- ❌ **One order per source without synergy check**: 4 deliveries instead of 1, €30 shipping burned
- ❌ **Not updating hardware stock after order**: next session doesn't know what's available
- ❌ **Ignoring reserve factor on critical parts**: one dead ESP32 without spare = 1 week wait
- ❌ **Not checking required accent material stock**: the spec'd accent color/material is empty, the build silently defaults to a generic filament → finish drift
- ❌ **Omitting BOM source evidence**: later it's unclear where which component decision came from

## Relation to related topics

- **`mechanical-design-principles`**: defines WHICH components even make sense (standard screws vs. odd sizes, snap-fit vs. screws)
- **`cad-construction`**: often delivers the spec table from which the BOM is extracted
- **`design-first-iteration`**: upstream — BOM validation starts only when design is finished
- **A hardware-stock inventory**: keep a single source of truth for stock levels (a spreadsheet, a notes file, or a small database) and check the BOM against it before ordering

## Real-world impact (projection)

**Expected use cases**:
- **Audio build** (planned): >20 components (drivers + amp + housing print parts + wiring + battery) — BOM validation would reduce 2-3 order iterations to 1
- **Embedded controller extensions**: PT100-sensor extensions, new heating elements — small components often in stock
- **Smart-home variant**: ESP32-P4 + pool sensors + LCD — mix of stock + order
- **Future smart-home builds**: typical 5-10 components with high connection-part share

**Design note**: BOM validation is implemented as a skill rather than a sub-agent — the validation logic needs no tool-restriction overhead, so a skill is the lighter-weight home for it.
