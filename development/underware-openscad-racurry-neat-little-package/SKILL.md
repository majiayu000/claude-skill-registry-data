---
name: underware-openscad
description: Reference guide for generating Underware cable management channel OpenSCAD code. Provides channel type selection, parameter quick reference, and QuackWorks integration. Use when generating OpenSCAD files for Underware cable routing systems.
---

# Underware OpenSCAD Code Generation

Generates OpenSCAD code for parametric cable management channels compatible with OpenGrid/Multiboard wall-mounted systems.

## Required Reading Before Generating Code

**Authoritative source (fetch every time):**

- **QuackWorks Underware Repository**: https://github.com/AndyLevesque/QuackWorks/tree/main/Underware
  - Reference implementation for all channel types
  - Licensed CC BY-NC-SA 4.0
  - Active development with bug fixes and enhancements

**Local reference clone** (if GitHub unavailable):

- `/Users/aaron/workspace/infra/neat-little-package/.tmp/QuackWorks/Underware/*.scad`

**Related documentation:**

- Hands on Katie guide: https://handsonkatie.com/underware-2-0-the-made-to-measure-collection/
- OpenGrid integration: See home-organization/SKILL.md for system compatibility

## Core Understanding (Critical Architecture)

### What Makes Underware Different From Generic Cable Channels

**Two-part snap system**: Every channel consists of separate Base + Top pieces:

- **Base**: Mounts to wall/surface with various mounting methods
- **Top**: Clips onto base, removable for cable access
- **Snap profile**: Precision-engineered interlock (~3mm overlap)
- **Why this matters**: User can route cables, snap on tops, remove tops later without unmounting

**Path-sweep construction**: All channels use BOSL2 `path_sweep()` for complex geometries:

```openscad
// Profile defines cross-section shape
// Turtle commands define path through space
path_sweep(baseProfile(widthMM = 25), turtle(["move", lengthMM]))
```

**Profile scaling for width**: Multi-unit channels expand by stretching center rectangle:

```openscad
// 1-unit channel: 25mm wide (standard profile)
// 2-unit channel: 50mm wide (profile halves moved apart, rectangle fills gap)
function baseProfile(widthMM = 25) =
    union(
        left((widthMM-25)/2, selectBaseProfile),  // Left half
        right((widthMM-25)/2, mirror([1,0], selectBaseProfile)),  // Right half mirrored
        back(3.5/2, rect([widthMM-25+0.02, 3.5]))  // Center fill rectangle
    );
```

**Grid-based dimensioning**: All dimensions in 25mm grid units (OpenGrid/Multiboard standard):

- `Grid_Size = 25` (constant, do not modify)
- `Channel_Width_in_Units = 1` → 25mm wide channel
- `Channel_Length_Units = 5` → 125mm long straight channel

### BOSL2 Dependencies (Required)

All channel files require:

```openscad
include <BOSL2/std.scad>
include <BOSL2/rounding.scad>
include <BOSL2/threading.scad>
```

**Why these specific libraries:**

- `std.scad`: Core geometry operations (path_sweep, turtle, attachable)
- `rounding.scad`: Smooth corners on profiles
- `threading.scad`: Threaded snap connector generation

## Channel Type Selection Framework (Decision Layer)

### By Cable Routing Need

| Routing Need                        | Channel Type             | Key File                               | Read Subpage            |
| ----------------------------------- | ------------------------ | -------------------------------------- | ----------------------- |
| Straight run with cord exits        | I Channel                | `Underware_I_Channel.scad`             | ./straight-runs.md      |
| 90° corner, independent arm lengths | L Channel                | `Underware_L_Channel.scad`             | ./corners-junctions.md  |
| 3-way intersection                  | T Channel                | `Underware_T_Channel.scad`             | ./corners-junctions.md  |
| 4-way cross                         | X Channel                | `Underware_X_Channel.scad`             | ./corners-junctions.md  |
| Split one path to two               | Y Channel (Branch Split) | `Underware_Branch_Split_Channel.scad`  | ./corners-junctions.md  |
| Smooth diagonal transition          | S Channel                | `Underware_S_Channel.scad`             | ./curves-transitions.md |
| Quarter/half/full circle            | C Channel                | `Underware_C_Channel.scad`             | ./curves-transitions.md |
| 45° angled corner                   | Mitre Channel            | `Underware_Mitre_Channel.scad`         | ./curves-transitions.md |
| Vertical level change               | Height Change Channel    | `Underware_Height_Change_Channel.scad` | ./curves-transitions.md |

### By Use Case Examples

| User wants to                        | Recommended approach        | Notes                                                              |
| ------------------------------------ | --------------------------- | ------------------------------------------------------------------ |
| Route desk power cables horizontally | I Channel with cord cutouts | Use `Both Sides` cutouts for multiple exit points                  |
| Turn corner around desk edge         | L Channel                   | Set `L_Channel_Length_in_Units_Y/X_Axis` independently             |
| Create cable junction box            | T or X Channel              | T for 3-way, X for 4-way crossroads                                |
| Branch to two monitor cables         | Y Channel                   | `Y_Output_Direction = "Forward"` keeps both outputs same direction |
| Gradually shift cable run diagonally | S Channel                   | Bezier curve, specify `Units_Over` and `Units_Up`                  |
| Route around circular desk leg       | C Channel                   | Set `Arc_Angle` for quarter (90°) or half (180°) circle            |
| Transition cables up/down wall       | Height Change Channel       | Smooth vertical transitions                                        |

### When Pattern Is Unclear

**Ask these questions:**

1. **Path shape**: Straight, corner, curve, or multi-junction?
2. **Exit points**: Where do cables enter/exit the channel?
3. **Direction changes**: 90°, 45°, or smooth curve?
4. **Mounting surface**: Flat wall, under desk, around obstacles?

**Default**: When unclear, use I Channel (straight) - user can connect multiple segments later.

## Universal Parameters (All Channels)

### Required Parameters (Always Define)

```openscad
/*[Choose Part]*/
Base_Top_or_Both = "Both"; // [Base, Top, Both] - Export control

/*[Channel Size]*/
Channel_Width_in_Units = 1;          // Width in grid units (25mm each)
Channel_Internal_Height = 12;        // Interior height 12-72mm (6mm increments)

/*[Mounting Options]*/
Mounting_Method = "Threaded Snap Connector";
// Options: Threaded Snap Connector, Direct Multiboard Screw,
//          Direct Multipoint Screw, Magnet, Wood Screw, Flat
```

### Mounting Method Selection

| Method                  | Use When                            | Parameters Needed                     | Print Orientation                |
| ----------------------- | ----------------------------------- | ------------------------------------- | -------------------------------- |
| Threaded Snap Connector | OpenGrid/Multiboard with connectors | None (default)                        | Base flat, Top upside-down       |
| Direct Multiboard Screw | Screw directly into board holes     | None                                  | Base flat (pre-drilled holes)    |
| Direct Multipoint Screw | Honeycomb Storage Wall              | None                                  | Base flat (larger holes)         |
| Magnet                  | Curved surfaces, repositionable     | `Magnet_Diameter`, `Magnet_Thickness` | Base flat (magnet recesses)      |
| Wood Screw              | Direct wall/desk mounting           | `Wood_Screw_Thread_Diameter`          | Base flat (countersink holes)    |
| Flat                    | Adhesive mounting, testing          | None                                  | Base flat (no mounting features) |

**Common mistake**: Using `Flat` for production installs. This removes all mounting features - only use for adhesive mounting or prototyping.

### Advanced Options (Modify Rarely)

```openscad
/*[Advanced Options]*/
Grid_Size = 25;                      // ALWAYS 25 for OpenGrid compatibility
Profile_Type = "Original";           // [Original, v2.5] - BETA: v2.5 inverse clip
Flex_Compensation_Scaling = 0.99;    // For wide/tall channels, reduce flex
Additional_Holding_Strength = 0.0;   // [0:0.1:1.5] - Increase for larger channels
```

**When to use Advanced Options:**

- `Profile_Type = "v2.5"`: BETA feature, inverse inside clip (not backwards compatible)
- `Flex_Compensation_Scaling`: Channels wider than 1 unit or taller than 18mm may flex - scale to 0.99
- `Additional_Holding_Strength`: Wide channels (2+ units) benefit from 0.6 extra holding strength

## Code Generation Workflow

### Step 1: Determine Channel Type

Use decision framework above → select appropriate channel file as reference.

### Step 2: Read Channel-Specific Subpage

Navigate to relevant subpage for detailed parameter reference:

- **./straight-runs.md**: I Channel (cord cutouts, length parameters)
- **./corners-junctions.md**: L, T, X, Y Channels (arm lengths, mitered corners)
- **./curves-transitions.md**: S, C, Mitre, Height Change (curve parameters, angles)
- **./mounting-accessories.md**: Keyholes, Hooks, Item Holders, Connectors

### Step 3: Gather User Requirements

**Dimension questions:**

- How wide should the channel be? (units × 25mm)
- How tall inside? (12mm min, 72mm max, 6mm increments)
- Length/distance for straight sections? (units × 25mm)

**Mounting questions:**

- Where mounting? (OpenGrid board, direct wall, desk underside)
- Mounting hardware available? (snap connectors, screws, magnets)

**Cable exit questions:**

- Where do cables exit? (for I Channel cord cutouts)
- How many cables? (affects cutout count/spacing)

### Step 4: Generate OpenSCAD Code

**Code structure pattern:**

```openscad
/*Created by [Your context]
Based on QuackWorks Underware by BlackjackDuck (Andy) and Hands on Katie
Licensed Creative Commons 4.0 Attribution Non-Commercial Share-Alike (CC-BY-NC-SA)

Documentation: https://handsonkatie.com/underware-2-0-the-made-to-measure-collection/
*/

include <BOSL2/std.scad>
include <BOSL2/rounding.scad>
include <BOSL2/threading.scad>

/*[Choose Part]*/
Base_Top_or_Both = "Both";

/*[Channel Size]*/
Channel_Width_in_Units = 1;
Channel_Internal_Height = 12;
// ... channel-specific size parameters

/*[Mounting Options]*/
Mounting_Method = "Threaded Snap Connector";
// ... mounting-specific parameters

/*[Advanced Options]*/
Grid_Size = 25;
Global_Color = "SlateBlue";
Profile_Type = "Original";

// ... include complete module code from QuackWorks reference
```

**DO NOT write modules from scratch** - copy/adapt from QuackWorks repository:

1. Fetch latest `.scad` file from QuackWorks
2. Preserve all module code (profiles, path_sweep operations)
3. Only modify user-facing parameters section
4. Keep attribution comments intact (CC BY-NC-SA license requirement)

## Common Pitfalls

### Pitfall #1: Hardcoding Dimensions Instead of Grid Units

**Problem**: User requests 75mm long channel, code sets `lengthMM = 75`.

**Why it fails**: Underware uses grid units for mounting alignment. 75mm doesn't align to 25mm grid - mounting holes won't match OpenGrid.

**Better approach**:

```openscad
// User wants 75mm → suggest 75mm = 3 grid units
Channel_Length_Units = 3;  // 3 × 25mm = 75mm

// Or: User wants 80mm → explain rounding
Channel_Length_Units = 3;  // 75mm (closest grid alignment)
// Note to user: "Using 3 units (75mm) for grid alignment.
//                For 100mm use 4 units."
```

### Pitfall #2: Ignoring Two-Part Export

**Problem**: Code generates only base or only top, user can't assemble.

**Why it fails**: Underware requires both parts to function. Base alone has no cable retention, top alone can't mount.

**Better approach**:

```openscad
// ALWAYS default to Both for user convenience
Base_Top_or_Both = "Both";

// Explain in comments:
// For printing: Export "Both", slice with parts separated
// For troubleshooting: Export "Base" or "Top" individually
```

### Pitfall #3: Wrong Mounting Method for Use Case

**Problem**: User mounting to OpenGrid, code uses `Flat` method.

**Why it fails**: No mounting features generated - channel won't attach.

**Better approach**:

```openscad
// Ask about mounting surface first
// OpenGrid/Multiboard → "Threaded Snap Connector"
// Direct wall → "Wood Screw" with Wood_Screw_Thread_Diameter = 3.5
// Metal desk → "Magnet" with Magnet_Diameter = 4.0, Magnet_Thickness = 1.5
```

### Pitfall #4: Forgetting BOSL2 Dependencies

**Problem**: User can't render code, errors about undefined `path_sweep`.

**Why it fails**: BOSL2 library not included or not installed in OpenSCAD.

**Better approach**:

```openscad
// ALWAYS include these three at top of file:
include <BOSL2/std.scad>
include <BOSL2/rounding.scad>
include <BOSL2/threading.scad>

// Add comment explaining BOSL2 requirement:
// Requires BOSL2 library: https://github.com/BelfrySCAD/BOSL2
// Install: Download and place in OpenSCAD libraries folder
```

### Pitfall #5: Using Beta Features Without Warning

**Problem**: Code sets `Profile_Type = "v2.5"` without explaining implications.

**Why it fails**: v2.5 inverse clip is not backwards compatible with Original profile. User can't mix old and new channels.

**Better approach**:

```openscad
// Only use beta features if explicitly requested
Profile_Type = "Original";  // Default, backwards compatible

// If user wants stronger hold:
Additional_Holding_Strength = 0.6;  // Stable, works with Original

// If user explicitly requests beta:
// Profile_Type = "v2.5";  // BETA: Inverse clip, NOT compatible with Original profile
```

## Quality Checklist

**Before delivering OpenSCAD code:**

**QuackWorks compliance:**

- ✓ Code copied from QuackWorks reference (not written from scratch)
- ✓ Attribution comments intact (CC BY-NC-SA license)
- ✓ BOSL2 includes present (`std.scad`, `rounding.scad`, `threading.scad`)
- ✓ Module structure preserved (baseProfile, topProfile functions)

**Parameter validation:**

- ✓ `Grid_Size = 25` (never modified)
- ✓ `Channel_Width_in_Units` is integer (1, 2, 3, not 1.5)
- ✓ `Channel_Internal_Height` in 6mm increments (12, 18, 24, ... 72)
- ✓ Mounting method appropriate for user's surface
- ✓ `Base_Top_or_Both = "Both"` unless user needs individual parts

**Dimensional sanity:**

- ✓ Dimensions specified in grid units (not raw mm)
- ✓ Channel width accounts for cable bundle size + clearance
- ✓ Internal height sufficient for thickest cable + movement
- ✓ Length/arm dimensions align to 25mm grid for mounting

**Channel-specific requirements:**

- ✓ I Channel: Cord cutout count/spacing matches cable exit needs
- ✓ L Channel: X and Y axis lengths set independently
- ✓ T/X Channels: Mitered corners option considered for thick cables
- ✓ Y Channel: Output direction (Forward/Turn) matches user's layout
- ✓ S/C Channels: Curve parameters create smooth transitions (no sharp bends)

**User communication:**

- ✓ Explained channel type selection rationale
- ✓ Noted any dimension rounding to grid units
- ✓ Documented mounting method choice
- ✓ Warned if using beta features (v2.5 profile)
- ✓ Provided print orientation guidance (Base flat, Top upside-down)

## Navigation: Channel-Specific Reference

**Read these subpages for detailed parameter reference:**

| Subpage                       | Contains                                  | Use For                                                   |
| ----------------------------- | ----------------------------------------- | --------------------------------------------------------- |
| **./straight-runs.md**        | I Channel (straight with cord cutouts)    | Linear cable runs, desktop cable management               |
| **./corners-junctions.md**    | L, T, X, Y Channels                       | Corner turns, multi-path junctions, cable splits          |
| **./curves-transitions.md**   | S, C, Mitre, Height Change Channels       | Smooth curves, diagonal transitions, vertical routing     |
| **./mounting-accessories.md** | Keyholes, Hooks, Item Holders, Connectors | Wall mounting, accessory integration, modular connections |

## Documentation References

**Official Underware sources:**

- QuackWorks GitHub: https://github.com/AndyLevesque/QuackWorks/tree/main/Underware
- Hands on Katie guide: https://handsonkatie.com/underware-2-0-the-made-to-measure-collection/
- License: CC BY-NC-SA 4.0

**BOSL2 library:**

- GitHub: https://github.com/BelfrySCAD/BOSL2
- Documentation: https://github.com/BelfrySCAD/BOSL2/wiki
- Required for all Underware code generation

**Related spirograph skills:**

- home-organization/SKILL.md: System selection (when to use Underware vs other systems)
- opengrid-openscad/SKILL.md: OpenGrid accessory code generation (complementary system)

**Ecosystem integration:**

- Underware integrates natively with OpenGrid mounting systems
- Use OpenGrid boards under desk, snap Underware channels into grid
- See home-organization skill for Underware + OpenGrid combination strategies
