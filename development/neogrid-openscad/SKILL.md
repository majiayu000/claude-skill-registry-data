---
name: neogrid-openscad
description: Interpretive guidance for generating OpenSCAD code for NeoGrid drawer divider connectors. This is a HYBRID system - print connectors, buy dividers (MDF, plywood, acrylic). Provides material selection guidance, connector type decisions, and base system integration. Use when generating OpenSCAD files for NeoGrid junction pieces.
---

# NeoGrid OpenSCAD Code Generation

Generates OpenSCAD code for 3D-printed connectors that join store-bought divider materials (MDF, plywood, acrylic) into custom drawer organization layouts.

## Required Reading Before Generating Code

**CRITICAL: NeoGrid is a HYBRID system:**

- **3D-print**: Connectors only (~50g filament per piece)
- **Buy/cut**: Divider material (MDF, plywood, acrylic, uPVC) from hardware store

**Official NeoGrid 2.0 implementation:**

- **QuackWorks GitHub**: https://github.com/AndyLevesque/QuackWorks/tree/main/NeoGrid
- **Local clone**: `/Users/aaron/workspace/infra/neat-little-package/.tmp/QuackWorks/NeoGrid/`
- **Main files**: `Neogrid.scad` (connectors), `DrawerLabelsAndHandles.scad` (labels)
- **License**: CC BY-NC-SA 4.0

**System references:**

- home-organization/neogrid-reference.md - System overview and material selection
- Fetch QuackWorks repo for current parameter syntax

## Core Understanding (Critical Architecture)

### What Makes NeoGrid Different: Hybrid Economics

**NOT a fully 3D-printed system**. NeoGrid separates components by manufacturing efficiency:

**3D-print the connectors:**

- Junctions (X, T, L, I, End pieces)
- ~50g filament per connector
- Print time: 1-3 hours depending on connector type
- Functional geometry (channels, retention, base mounting)

**Buy the dividers:**

- 8.5mm uPVC utility board (UK standard)
- 6.35mm (1/4") plywood (US standard)
- 3mm-9mm+ MDF, acrylic, foam board
- Cost: ~$10-20 for entire drawer system vs hundreds in filament
- Faster: Cut to length vs 50+ hours printing sheets

**Why this works:**

- Connectors require precision geometry (print it)
- Dividers are simple rectangles (buy it cheap)
- Material cost: 90% savings vs fully printed
- Assembly time: Cut dividers once, reuse connectors anywhere

### Critical Parameter: Material Thickness

**Most important parameter** in entire system:

```openscad
Material_Thickness = 8.5;  // MEASURE YOUR ACTUAL MATERIAL!
```

**Why it's critical:**

- Even 0.2mm variation affects friction fit
- Tolerance: ±0.15mm for proper grip
- Too loose: Dividers wobble, layout collapses
- Too tight: Dividers won't insert, connectors crack

**Process:**

1. Buy material from hardware store
2. Measure with calipers (NOT ruler)
3. If painted: Measure AFTER painting (adds thickness)
4. Print ONE test connector
5. Verify fit before batch printing
6. Adjust parameter by 0.1-0.2mm if needed

**Common materials and actual measurements:**

| Material         | Nominal | Actual (measure!) | Setting |
| ---------------- | ------- | ----------------- | ------- |
| UK utility board | 8.5mm   | 8.3-8.7mm         | Measure |
| US 1/4" plywood  | 6.35mm  | 6.0-6.5mm         | Measure |
| 6mm MDF          | 6mm     | 5.8-6.2mm         | Measure |
| 3mm acrylic      | 3mm     | 2.9-3.1mm         | Measure |

### Base System Integration

**Connectors attach to drawer bottom** via one of four base types:

**Gridfinity** (42mm grid):

- Snaps onto Gridfinity baseplate
- Allows repositioning without re-taping
- Grid alignment ensures straight layouts
- Use for drawers with existing Gridfinity setup

**OpenGrid** (25mm grid):

- Vertical wall mounting option
- Less common for drawer use
- Two variants: Full (6.8mm) or Lite (3.4mm)
- Optional directional snaps for vertical strength

**Flat** (30mm grid or custom):

- No snap features, just flat base
- Use adhesive/tape to secure
- Flexible grid sizing
- Simple, universal option

**None** (no base):

- For non-drawer applications
- Dividers rest on surface directly
- Minimal filament usage

## Connector Type Navigation

**NeoGrid has 6 connector types** (plus drawer label holders). Each has dedicated subpage:

| Connector          | Use case                                     | Read                                  |
| ------------------ | -------------------------------------------- | ------------------------------------- |
| **X Intersection** | 4-way junctions (interior grid points)       | ./connector-types/x-intersection.md   |
| **T Intersection** | 3-way junctions (edges, perpendicular joins) | ./connector-types/t-intersection.md   |
| **L Intersection** | Corner junctions (90° turns)                 | ./connector-types/l-intersection.md   |
| **I Junction**     | Straight-through connections (in-line)       | ./connector-types/straight-through.md |
| **Straight End**   | Terminators (open ends with buffer)          | ./connector-types/straight-end.md     |
| **Vertical Trim**  | Edge trim for drawer openings                | ./connector-types/vertical-trim.md    |

**Drawer labels** (bonus accessory):

- Label holders that mount to drawer fronts
- Hook mount (standard) or adhesive tape
- Not part of divider system, but commonly paired
- Read: ./drawer-labels.md

## Material Selection Guide

**Choose divider material** based on budget, availability, and drawer use:

### Detailed material comparison: ./hybrid-approach.md

**Quick reference:**

| Material           | Thickness     | Cost     | Pros                        | Cons                          |
| ------------------ | ------------- | -------- | --------------------------- | ----------------------------- |
| uPVC utility board | 8.5mm         | Low      | Minimal paint, long lengths | UK-specific                   |
| Plywood            | 6mm, 8mm      | Low      | Strong, natural look        | Needs finish                  |
| MDF                | 3mm, 6mm, 8mm | Very low | Cheap, smooth               | Heavy, needs retention spikes |
| Acrylic            | 3mm, 6mm      | Medium   | Transparent, clean          | Brittle, expensive            |
| Foam board         | 5mm           | Very low | Lightweight                 | Low strength                  |

**Critical reminder**: Measure actual material thickness before printing. Nominal ≠ actual.

## Base Selection Guide

**Choose base system** based on drawer setup:

### Detailed base options: ./base-options.md

**Quick decision framework:**

```
Do you have Gridfinity baseplate in drawer?
├─ Yes → Use Gridfinity base (42mm)
└─ No
   ├─ Want to add Gridfinity later? → Use Gridfinity base (future-proof)
   └─ No Gridfinity needed
      ├─ Want easy repositioning? → Use Flat base + adhesive (30mm)
      └─ Permanent install → Use None (minimal filament)
```

**Multi-tile support (Gridfinity only):**

```openscad
grid_x = 2;  // 2 tiles wide (84mm)
grid_y = 3;  // 3 tiles deep (126mm)
```

Only X Intersection connectors support multi-tile bases currently.

## Connector Selection Framework (Decision Layer)

### When User Describes Drawer Layout

Use this decision tree to select connector types:

**Ask these questions:**

1. **How many dividers meet at junction?**

   - Four (cross pattern) → X Intersection
   - Three (T pattern) → T Intersection
   - Two (corner) → L Intersection
   - Two (straight line) → I Junction
   - One (end of divider) → Straight End

2. **Where is junction located?**

   - Interior grid point → X Intersection (most versatile)
   - Edge with perpendicular divider → T Intersection
   - Corner → L Intersection
   - Drawer opening edge → Vertical Trim

3. **What's the layout pattern?**

   - Regular grid → Mostly X Intersections + edges (T, L, End)
   - Asymmetric compartments → Mix of all types as needed

**Example layout analysis:**

```
User: "3×3 grid in my drawer"

Analysis:
- Interior: 4 X Intersections (where grid lines cross)
- Edges: 8 T Intersections (where dividers meet drawer edge)
- Corners: 4 L Intersections (drawer corners)
- Total: 4 X + 8 T + 4 L = 16 connectors + 16 top pieces
```

**Start with X Intersections**: Most versatile, works for testing material fit.

## Code Generation Best Practices

### Parameter Organization

**Always declare these parameters** at top of file:

```openscad
// CRITICAL: Material measurement
Material_Thickness = 8.5;      // MEASURE actual material with calipers!
Channel_Depth = 20;            // How deep material sits in connector
Wall_Thickness = 4;            // Connector wall thickness

// Base system selection
Selected_Base = "Gridfinity";  // Gridfinity | openGrid | Flat | None
grid_size = 42;                // Auto-set based on Selected_Base
grid_x = 1;                    // Tiles horizontally (Gridfinity only)
grid_y = 1;                    // Tiles vertically (Gridfinity only)

// Gridfinity-specific
Added_Base_Thickness = 1;      // Extra base height beyond profile

// OpenGrid-specific
openGrid_Full_or_Lite = "Lite";                     // Full | Lite
openGrid_Directional_Snap = false;                   // Vertical mounting
openGrid_Directional_Snap_Orientation = 1;           // 1-4 rotation

// Flat base
Flat_Base_Thickness = 1.4;     // Base thickness in mm

// Material retention
Retention_Spike = false;       // Add spikes for MDF (soft materials)
Spike_Scale = 1;               // Scale spike size

// Part selection
Select_Part = "X Intersection"; // See connector type options
Top_or_Bottom = "Both";        // Top | Bottom | Both

// Top chamfers
Top_Chamfers = true;           // Ease material insertion
```

**Why this order**: Critical material parameter first, base system second, optional features last.

### Two-Piece System (Base + Top)

**All connectors use two-piece design** (except Vertical Trim):

```openscad
// Bottom piece (has base attachment - Gridfinity/openGrid/Flat)
NeoGrid_X_Intersection_Base(
    Material_Thickness,
    Channel_Depth = Channel_Depth,
    Wall_Thickness = Wall_Thickness,
    grid_size = grid_size
);

// Top piece (caps the junction, no base)
NeoGrid_X_Intersection_Top(
    Material_Thickness,
    Channel_Depth = Channel_Depth,
    Wall_Thickness = Wall_Thickness,
    grid_size = grid_size
);
```

**Why two pieces:**

- Base provides stability and positioning
- Top locks dividers in place vertically
- Allows swapping divider materials without reprinting bases
- Separate prints = less support material

**Assembly**: Insert dividers into base channels → Place top piece over junction.

### Material Thickness Workflow

**When user says "I need connectors for X dividers"**:

1. **Ask about material type and measurement**:

   - "What material? (MDF, plywood, acrylic, uPVC)"
   - "Have you measured thickness with calipers?"
   - "If painted, measure after painting"

2. **Set Material_Thickness parameter**:

   ```openscad
   Material_Thickness = 8.5;  // User's measured value
   ```

3. **Recommend test print**:

   - "Print ONE X Intersection (base + top) to verify fit"
   - "Divider should friction-fit securely without forcing"
   - "Adjust parameter by ±0.1-0.2mm if needed"

4. **Batch printing guidance**:

   - "After fit verified, print remaining connectors"
   - "All connectors use same Material_Thickness"
   - "Orientation: Parts print upright as displayed in QuackWorks"

### Connector Module Integration

**Read the QuackWorks source, don't reinvent**:

```openscad
// DON'T write connector geometry from scratch
// DO fetch current modules from QuackWorks repo

// Option 1: Direct include (if user has BOSL2)
include <BOSL2/std.scad>
include <BOSL2/rounding.scad>
include <path/to/Neogrid.scad>

NeoGrid_X_Intersection_Base(...);

// Option 2: Paste relevant module from QuackWorks
// (if user wants standalone file)
module NeoGrid_X_Intersection_Base(...) {
    // [copied from Neogrid.scad]
}
```

**When to use each connector type**: See connector-types/\*.md for detailed geometry and use cases.

## Common Pitfalls

### Pitfall #1: Hardcoding Material Thickness Instead of Measuring

**Problem**: User says "I have 1/4 inch plywood", code uses `Material_Thickness = 6.35`, connectors don't fit.

**Why it fails**: Nominal thickness ≠ actual thickness. 1/4" plywood can be 6.0-6.5mm depending on manufacturer.

**Better approach**:

```openscad
// DON'T assume nominal:
Material_Thickness = 6.35;  // "It's 1/4 inch"

// DO ask user to measure:
echo("CRITICAL: Measure actual material with calipers!");
echo("Even 0.2mm variation affects fit.");
Material_Thickness = 6.4;  // User's measured value
```

### Pitfall #2: Skipping Test Print

**Problem**: User prints 20 connectors, discovers material doesn't fit, wastes filament.

**Why it fails**: Material variation, printer tolerance, measurement errors compound.

**Better approach**:

```openscad
// Workflow guidance:
// 1. Print ONE X Intersection (base + top)
// 2. Test material fit
// 3. Adjust Material_Thickness ±0.1-0.2mm if needed
// 4. THEN batch print remaining connectors
```

**Include in code comments**: Remind user to test before batch printing.

### Pitfall #3: Wrong Base System for User's Drawer

**Problem**: User has no Gridfinity baseplate, code generates Gridfinity base, connectors don't sit flat.

**Why it fails**: Didn't ask about existing drawer setup.

**Better approach**:

```openscad
// Ask before generating:
// "Do you have Gridfinity baseplate in this drawer?"
// ├─ Yes → Selected_Base = "Gridfinity"
// └─ No → Selected_Base = "Flat"  // Use adhesive to secure
```

### Pitfall #4: Forgetting Retention Spikes for Soft Materials

**Problem**: User has MDF dividers, connectors don't grip firmly, layout sags.

**Why it fails**: MDF is soft, benefits from retention spikes for friction.

**Better approach**:

```openscad
// Check material type:
// "What divider material?"
// ├─ MDF → Retention_Spike = true;
// ├─ Plywood → Retention_Spike = false; (optional)
// └─ Acrylic → Retention_Spike = false; (never)
```

### Pitfall #5: Multi-Tile Grid Without Gridfinity Base

**Problem**: User wants 2×3 connector grid, code sets `grid_x=2, grid_y=3` with `Selected_Base="Flat"`, parameters ignored.

**Why it fails**: Multi-tile support is Gridfinity-only (currently).

**Better approach**:

```openscad
// Warn user:
if (grid_x > 1 || grid_y > 1) {
    echo("WARNING: Multi-tile (grid_x/grid_y) only supported with Gridfinity base");
    echo("For Flat/None base, use grid_x=1, grid_y=1");
}
```

## Quality Checklist

**Before delivering OpenSCAD code:**

**Required elements:**

- ✓ Material_Thickness parameter clearly documented with measurement reminder
- ✓ Base system selected based on user's drawer setup
- ✓ Appropriate connector type(s) for layout described
- ✓ Top_or_Bottom set correctly (usually "Both")
- ✓ Retention_Spike evaluated based on material type
- ✓ Test print workflow mentioned in comments

**Parameter validation:**

- ✓ Material_Thickness: User measured actual material (not assumed nominal)
- ✓ Channel_Depth: Default 20mm (adequate for most drawers)
- ✓ Wall_Thickness: Default 4mm (adequate strength)
- ✓ grid_size: Auto-set based on Selected_Base (don't override unless custom)

**Base system compliance:**

- ✓ Selected_Base matches user's drawer setup
- ✓ If Gridfinity: grid_x/grid_y set for multi-tile (if needed)
- ✓ If openGrid: Full/Lite and directional snap configured
- ✓ If Flat: Flat_Base_Thickness set
- ✓ If None: User understands no base attachment

**Code quality:**

- ✓ Parameterized (uses Material_Thickness variable, not hardcoded values)
- ✓ Clear variable names
- ✓ Comments explain hybrid system approach
- ✓ Module calls use QuackWorks functions (don't reinvent)
- ✓ BOSL2 library referenced (required dependency)

**User communication:**

- ✓ Explained hybrid approach (print connectors, buy dividers)
- ✓ Material measurement workflow emphasized
- ✓ Test print recommended before batch
- ✓ Assembly instructions (base → dividers → top)
- ✓ Connector count calculated if layout specified

## Assembly Workflow

**Standard NeoGrid assembly process**:

1. **Design layout**: Measure drawer, plan divider pattern
2. **Measure material**: Use calipers on actual divider material
3. **Test print**: ONE connector type (X Intersection recommended)
4. **Verify fit**: Material should friction-fit with slight resistance
5. **Adjust if needed**: ±0.1-0.2mm on Material_Thickness parameter
6. **Cut dividers**: Standard length 160mm (or `42mm × N - Material_Thickness`)
7. **Batch print**: All connectors for layout
8. **Assemble**: Place bases → insert dividers → add tops
9. **Install**: Place in drawer (on baseplate or with adhesive)

## Documentation References

**NeoGrid Ecosystem**:

- NeoGrid 2.0: Hybrid drawer organization system
- Created by Hands on Katie (Katie)
- Licensed CC BY-NC-SA 4.0
- This skill focuses on CODE GENERATION for connectors

**Related skills**:

- home-organization/neogrid-reference.md - System overview, material selection, use cases
- For system selection guidance, defer to that skill
- This skill is only for "generate OpenSCAD code for NeoGrid connectors"

**Official resources**:

- https://handsonkatie.com/neogrid-organise-your-big-items-with-this-free-and-open-source-system/
- https://github.com/AndyLevesque/QuackWorks/tree/main/NeoGrid (authoritative code)
- https://makerworld.com/en/models/1501061-neogrid-2-0-drawer-management-system
