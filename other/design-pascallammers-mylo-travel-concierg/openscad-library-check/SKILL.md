---
name: openscad-library-check
description: Verify OpenSCAD libraries (BOSL2, Round-Anything) are installed, troubleshoot common issues, understand best practices for spiral generation, and evaluate designs against professional CAD quality standards.
version: 1.2
---

# OpenSCAD Library Check Skill

## Overview
This skill verifies that OpenSCAD libraries (BOSL2, Round-Anything, etc.) are properly installed and provides guidance on common usage issues.

## When to Use This Skill
- User mentions OpenSCAD library issues
- "Can't open library" errors in OpenSCAD
- Before starting projects that require BOSL2 or Round-Anything
- When debugging geometry generation errors

## Library Locations
User's OpenSCAD libraries are located at:
`/Users/aaronmontgomery/Documents/OpenSCAD/libraries/`

Current installed libraries:
- **BOSL2**: v2.0.716 (91 files, installed March 2025)
- **Round-Anything**: 25 files (installed May 2025)

## Verification Process

### Step 1: Check Library Installation
```bash
ls -la ~/Documents/OpenSCAD/libraries/
```

Expected output should show:
- `BOSL2/` directory
- `Round-Anything/` directory

### Step 2: Create Test File
Generate a test file that imports both libraries and renders basic shapes:

```openscad
include <BOSL2/std.scad>
include <Round-Anything/polyround.scad>

// Test BOSL2
echo("BOSL2 Version: ", BOSL_VERSION);
cuboid([20, 20, 20], rounding=2);

// Test Round-Anything
translate([30, 0, 0])
    polyRoundExtrude([[0,0,2], [10,0,2], [10,10,2], [0,10,2]], 5);
```

### Step 3: Verify in OpenSCAD
- Open test file in OpenSCAD
- Check Console for version info
- Verify both shapes render without errors

## BOSL2 Usage Notes

### Primitive Overrides ⚠️
BOSL2 replaces standard OpenSCAD primitives with "attachable" versions:
- `cube()` → attachable cube with anchor/spin/orient parameters
- `cylinder()` → attachable cylinder
- `sphere()` → attachable sphere

**Common Error:**
```
ERROR: Assertion '!approx(spin_dir, [0, 0, 0])' failed:
"spin direction is parallel to anchor"
```

**Cause:** Using standard OpenSCAD syntax with BOSL2-overridden primitives.

**Solutions:**

**Option 1 - Use BOSL2 Primitives:**
```openscad
include <BOSL2/std.scad>

// Instead of: cube([10, 10, 10]);
cuboid([10, 10, 10]);

// Instead of: cylinder(h=20, d=10);
cyl(h=20, d=10);
```

**Option 2 - Don't Include BOSL2 for Simple Models:**
If you only need basic primitives, avoid including BOSL2:
```openscad
// Use standard OpenSCAD only
cube([10, 10, 10]);
cylinder(h=20, d=10);
```

**Option 3 - Use Standard Namespace:**
```openscad
include <BOSL2/std.scad>

// Explicitly use standard version
translate([0,0,0]) cube([10,10,10]);  // Standard cube
```

### When to Use BOSL2
Use BOSL2 when you need:
- Advanced attachments (attach(), position(), orient())
- Complex shapes (rounded boxes, threads, gears)
- Path operations (path_sweep, spiral paths)
- Transformations (move(), up(), back())

Don't use BOSL2 if:
- You're only using basic primitives
- The model is very simple
- You want standard OpenSCAD behavior

## Spiral Generation Best Practices

### Segment-Based Spirals
When creating spirals with discrete segments:

**Critical Rules:**
1. **Segment width must exceed angular spacing:**
   ```
   segment_width ≥ (360 / steps) * radius * π/180 * overlap_factor
   ```
   - For 200 steps, 35mm radius: minimum ~3mm width
   - Recommend 1.5-2x minimum for reliable overlap

2. **Use hull() for continuity:**
   ```openscad
   for (i = [0 : steps-1]) {
       hull() {
           rotate([0, 0, i * angle_step]) segment();
           rotate([0, 0, (i+1) * angle_step]) segment();
       }
   }
   ```

3. **Avoid thin radial slices:**
   - 2mm segments with 4.5° spacing = gaps (BAD)
   - 20-30mm segments with 4.5° spacing = continuous (GOOD)

### Entry/Exit Design
**Use difference() for openings:**
```openscad
difference() {
    union() {
        // Build complete spiral
        spiral_ramp();
    }
    // Cut entry slot
    entry_slot_cut();
}
```

Don't try to skip segments during generation - creates edge cases and gaps.

## Common Pitfalls

### 1. Library Path Issues
**Symptom:** "Can't open library" error
**Solution:** Verify libraries are in `~/Documents/OpenSCAD/libraries/`

### 2. Version Conflicts
**Symptom:** Functions don't work as expected
**Solution:** Check BOSL2 version: `echo(BOSL_VERSION);`

### 3. Primitive Syntax Errors
**Symptom:** "spin direction is parallel to anchor"
**Solution:** Use BOSL2 primitives (`cuboid()`) or avoid including BOSL2

### 4. Non-Manifold Geometry
**Symptom:** "Object may not be a valid 2-manifold"
**Cause:** Overlapping segments without proper union
**Solution:** Usually printable if Preview looks correct, but verify with Render (F6)

### 5. Thin Segment Gaps
**Symptom:** Spiral looks like a picket fence
**Solution:** Increase segment_width to ≥1.5x angular spacing

## Testing Workflow

1. **Preview (F5):** Quick iteration, catches syntax errors
2. **Console Check:** Look for warnings/errors
3. **Visual Inspection:** Rotate model, check from 4+ angles
4. **Full Render (F6):** Catches geometry errors, tests manifold
5. **Export STL:** Final validation before printing

## Reference Links

- User's Repository: https://github.com/Euda1mon1a/parametric_projects
- BOSL2 Documentation: https://github.com/BelfrySCAD/BOSL2/wiki
- OpenSCAD Manual: https://openscad.org/documentation.html

## Script: Library Test Generator

The skill includes a Python script to generate test files:

```python
# scripts/create_library_test.py
import os

test_code = '''include <BOSL2/std.scad>
include <Round-Anything/polyround.scad>

echo("BOSL2 Version: ", BOSL_VERSION);

cuboid([20, 20, 20], rounding=2);

translate([30, 0, 0])
    polyRoundExtrude([[0,0,2], [10,0,2], [10,10,2], [0,10,2]], 5);
'''

output_path = os.path.expanduser('~/Documents/OpenSCAD/library-test.scad')
with open(output_path, 'w') as f:
    f.write(test_code)

print(f"Created test file: {output_path}")
```

## Troubleshooting Decision Tree

```
OpenSCAD error?
├─ "Can't open library"
│  └─ Check ~/Documents/OpenSCAD/libraries/ exists
│     └─ Verify BOSL2/ and Round-Anything/ folders present
│
├─ "spin direction is parallel to anchor"
│  └─ Using cube() with BOSL2 included
│     └─ Replace with cuboid() or remove BOSL2 include
│
├─ Gaps in spiral/surface
│  └─ Check segment_width calculation
│     └─ Increase to ≥1.5x angular spacing
│
└─ Non-manifold geometry
   └─ Check Preview looks correct
      ├─ If yes: Usually printable, proceed
      └─ If no: Check for floating pieces, missing unions
```

## Professional CAD Quality Standard

It is a common pitfall to believe a model is "done" simply because it renders without CGAL errors and is printable. This is the standard for a **functional prototype**, not a **professional product**.

When evaluating your design, apply the "Human Standard" test: **Would a professional CAD designer at a major toy or consumer product company ship this design?**

### The Gap Between Functional and Professional

| Feature | Functional Prototype Standard (e.g., v1.4) | Professional Product Standard (e.g., proposed v1.6) |
| :--- | :--- | :--- |
| **Edges** | Sharp, mathematical corners. | All touchable edges have fillets or chamfers for comfort and safety. |
| **Terminations** | Cylinders and walls end abruptly with flat faces. | Terminations are capped, domed, or tapered (e.g., a rounded funnel lip). |
| **Transitions** | Components intersect at sharp 90° angles. | Major intersections have generous fillets to distribute stress and look deliberate (e.g., pillar-to-base transition). |
| **Thickness** | Minimum thickness required for printing. | Substantial thickness that conveys robustness and quality. |
| **Functional Ends** | Paths end abruptly, creating steps or drops. | Paths have smooth "runouts" that blend tangentially into the next surface. |

**Key Takeaway:** Achieving professional quality often requires significantly more effort (e.g., 2x-3x more code) using advanced techniques like `minkowski()` smoothing, custom `rotate_extrude` profiles, and careful boolean operations to manage transitions without breaking geometry.

Don't settle for "raw geometry" if the goal is a finished product.

## Version History

- **v1.2 (2024-12-08):** Added "Professional CAD Quality Standard" section based on dice tower project learnings.
- v1.1 (2024-12-07): Added BOSL2 usage notes, spiral generation best practices, common pitfalls
- v1.0 (2024-12-07): Initial creation with BOSL2/Round-Anything verification

---

*Last Updated: 2024-12-08*
