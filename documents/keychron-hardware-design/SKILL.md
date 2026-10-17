---
name: keychron-hardware-design
description: Access and work with Keychron keyboard and mouse industrial design files (STEP, DXF, DWG, PDF) for 135+ models to create compatible accessories, remixes, and modifications.
triggers:
  - open keychron hardware files
  - work with keychron cad models
  - modify keychron keyboard design
  - create keychron compatible accessory
  - remix keychron case or plate
  - access keychron step files
  - design keychron keyboard mod
  - export keychron design files
---

# Keychron Hardware Design Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill enables working with Keychron's production-grade hardware design files for 135+ keyboard and mouse models. The repository contains CAD assets in STEP, DXF, DWG, and PDF formats for cases, plates, keycaps, stabilizers, and full assemblies across all major Keychron series (Q, K, V, C, L, P, M, G).

## What This Project Provides

- **135+ device models** with industrial design files
- **734+ design files** across multiple CAD formats
- **Production-grade geometry** for cases, plates, stabilizers, encoders, and keycaps
- **Source-available license** allowing personal use, education, and original compatible accessories
- **Multiple keyboard series**: Q Series, Q Pro, Q HE, Q Max, Q Ultra 8K, K Pro, K Max, K HE, K QMK, V Max, V Ultra 8K, V 8K, C Pro 8K, L Series, P HE
- **Mouse series**: M1-M7, G1-G2 with shell and full model files

## Repository Structure

```
Keychron-Keyboards-Hardware-Design/
├── C-Pro-8K-Series/
│   ├── C1 Pro 8K/
│   ├── C2 Pro 8K/
│   └── C3 Pro 8K/
├── Q-Series/
│   ├── Q0 Plus/
│   ├── Q1/ through Q12/
│   ├── Q60/
│   └── Q65/
├── Q-Pro-Series/
│   └── Q1 Pro/ through Q14 Pro/
├── Q-HE-Series/
│   └── Q0 HE/ through Q12 HE/
├── Q-Max-Series/
│   └── Q0 Max/ through Q15 Max/
├── K-Pro-Series/
│   └── K1 Pro/ through K17 Pro/
├── K-Max-Series/
│   └── K0 Max/ through K17 Max/
├── K-HE-Series/
│   └── K2 HE/, K4 HE/, K6 HE/, K8 HE/, K10 HE/
├── K-QMK-Series/
│   └── K1 QMK/ through K10 QMK/
├── V-Max-Series/
│   └── V1 Max/ through V10 Max/
├── L-Series/
│   ├── L1/
│   └── L3/
├── P-HE-Series/
│   ├── P1 HE/
│   ├── P2 HE/
│   └── P3 HE/
├── Mice/
│   ├── M1/ through M7/
│   ├── G1/
│   └── G2/
├── Keycap Profiles/
│   ├── Cherry Profile/
│   ├── KSA/
│   ├── LSA/
│   ├── MDA/
│   ├── OEM/
│   └── OSA/
└── docs/
    ├── file-format-guide.md
    ├── getting-started.md
    ├── 3d-printing-guide.md
    ├── license-faq.md
    └── CONTRIBUTING.md
```

## Installation

Clone the repository to access design files:

```bash
git clone https://github.com/Keychron/Keychron-Keyboards-Hardware-Design.git
cd Keychron-Keyboards-Hardware-Design
```

For large repositories, use sparse checkout to download only specific models:

```bash
git clone --filter=blob:none --sparse https://github.com/Keychron/Keychron-Keyboards-Hardware-Design.git
cd Keychron-Keyboards-Hardware-Design
git sparse-checkout set "Q-Series/Q1"
```

## File Formats and CAD Software Compatibility

### STEP Files (.stp, .step)
Universal 3D CAD format for full geometry

**Compatible software:**
- **FreeCAD** (free, open source)
- **Fusion 360** (free for personal use)
- **SolidWorks** (commercial)
- **Onshape** (cloud-based, free tier)
- **Rhino** (commercial)
- **Blender** (free, with CAD add-ons)

### DXF/DWG Files
2D technical drawings for plates and cutouts

**Compatible software:**
- **QCAD** (free)
- **LibreCAD** (free, open source)
- **AutoCAD** (commercial)
- **DraftSight** (commercial)

### PDF Files
Technical documentation and dimension references

## Working with Design Files

### Opening STEP Files in FreeCAD

```python
# freecad_open_keychron.py
import FreeCAD
import Part

# Open a Keychron case STEP file
doc = FreeCAD.open("/path/to/Keychron-Keyboards-Hardware-Design/Q-Series/Q1/Q1-Case.stp")

# Access the imported shapes
objects = doc.Objects
print(f"Loaded {len(objects)} objects")

# Get bounding box dimensions
for obj in objects:
    if hasattr(obj, 'Shape'):
        bbox = obj.Shape.BoundBox
        print(f"Object: {obj.Label}")
        print(f"  Dimensions: {bbox.XLength:.2f} x {bbox.YLength:.2f} x {bbox.ZLength:.2f} mm")
```

### Extracting Plate Dimensions from DXF

```python
# dxf_plate_analysis.py
import ezdxf

# Load a Keychron plate DXF file
doc = ezdxf.readfile("K-Pro-Series/K8-Pro/K8-Pro-Plate.dxf")
msp = doc.modelspace()

# Extract all circles (switch holes and mounting holes)
circles = msp.query('CIRCLE')
print(f"Found {len(circles)} circular features")

for circle in circles:
    center = circle.dxf.center
    radius = circle.dxf.radius
    diameter = radius * 2
    print(f"Circle at ({center.x:.2f}, {center.y:.2f}), diameter: {diameter:.2f}mm")

# Find switch plate outline
polylines = msp.query('LWPOLYLINE')
for polyline in polylines:
    points = list(polyline.get_points())
    print(f"Polyline with {len(points)} vertices")
```

### Modifying Case Geometry in Python

```python
# modify_case_mounting.py
from OCP import gp, BRepPrimitivAPI, BRepAlgoAPI, BRepBuilderAPI
import cadquery as cq

# Load original Keychron case
original_case = cq.importers.importStep("Q-Series/Q3/Q3-Case.stp")

# Add custom mounting posts
post_height = 10.0
post_diameter = 5.0
post_positions = [(20, 20), (20, 100), (140, 20), (140, 100)]

for x, y in post_positions:
    post = cq.Workplane("XY").circle(post_diameter / 2).extrude(post_height)
    post = post.translate((x, y, 0))
    original_case = original_case.union(post)

# Export modified case
cq.exporters.export(original_case, "Q3-Case-Modified.step")
print("Modified case exported successfully")
```

### Creating Compatible Accessory Plate

```python
# create_accessory_plate.py
import cadquery as cq

# Reference Q1 case dimensions from STEP file
case = cq.importers.importStep("Q-Series/Q1/Q1-Case.stp")
bbox = case.val().BoundingBox()

# Create top plate accessory with matching outline
plate_thickness = 1.5
margin = 2.0

accessory_plate = (
    cq.Workplane("XY")
    .box(bbox.xlen - margin * 2, bbox.ylen - margin * 2, plate_thickness)
    .faces(">Z")
    .workplane()
    # Add mounting holes matching Keychron mount points
    .pushPoints([(0, 0), (60, 0), (-60, 0)])
    .circle(2.5)
    .cutThruAll()
)

# Export accessory
cq.exporters.export(accessory_plate, "Q1-Top-Plate-Accessory.step")
print(f"Accessory plate: {bbox.xlen:.1f} x {bbox.ylen:.1f} x {plate_thickness}mm")
```

## 3D Printing Workflow

### Preparing Case for 3D Printing

```python
# prepare_for_printing.py
import cadquery as cq
from cadquery import exporters

# Load Keychron case
case = cq.importers.importStep("K-Max-Series/K3-Max/K3-Max-Case.stp")

# Rotate for optimal printing orientation (largest face down)
case_oriented = case.rotate((0, 0, 0), (1, 0, 0), 180)

# Export as STL for slicing
exporters.export(case_oriented, "K3-Max-Case-Printable.stl")

# Check dimensions
bbox = case_oriented.val().BoundingBox()
print(f"Print bed requirements: {bbox.xlen:.1f} x {bbox.ylen:.1f} mm")
print(f"Print height: {bbox.zlen:.1f} mm")
```

### Generating Mounting Bracket

```python
# mounting_bracket.py
import cadquery as cq

# Design bracket to attach accessories to Keychron case
bracket = (
    cq.Workplane("XY")
    .box(30, 15, 3)
    .faces(">Z").workplane()
    .rect(20, 8).cutBlind(-1.5)
    # Add screw holes
    .faces(">Z").workplane()
    .pushPoints([(10, 0), (-10, 0)])
    .circle(1.5)
    .cutThruAll()
)

# Export STL
cq.exporters.export(bracket, "keychron-mount-bracket.stl", tolerance=0.01)
```

## Common Patterns

### Measuring Switch Plate Hole Spacing

```python
# analyze_plate_spacing.py
import ezdxf
import math

doc = ezdxf.readfile("Q-Series/Q6/Q6-Plate.dxf")
msp = doc.modelspace()

# Extract switch holes (typically 14mm diameter circles)
switch_holes = [c for c in msp.query('CIRCLE') if 13 < c.dxf.radius * 2 < 15]

# Calculate spacing between adjacent switches
centers = [(c.dxf.center.x, c.dxf.center.y) for c in switch_holes]
centers.sort(key=lambda p: (p[1], p[0]))  # Sort by row, then column

# Standard keyboard spacing is 19.05mm (0.75 inches)
for i in range(len(centers) - 1):
    dx = centers[i+1][0] - centers[i][0]
    dy = centers[i+1][1] - centers[i][1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance < 25:  # Adjacent switches
        print(f"Switch spacing: {distance:.2f}mm")
```

### Extracting Stabilizer Positions

```python
# extract_stabilizer_positions.py
import cadquery as cq
import json

# Load full keyboard model
keyboard = cq.importers.importStep("Q-Pro-Series/Q5-Pro/Q5-Pro-Full-Model.stp")

# Stabilizers are typically rectangular cutouts 6.5-7mm wide
# This example shows the pattern for finding them programmatically
def find_stabilizer_cutouts(assembly):
    """Extract stabilizer mounting positions from assembly"""
    positions = []
    
    # Iterate through all solid bodies in assembly
    for solid in assembly.solids().vals():
        bbox = solid.BoundingBox()
        
        # Stabilizer cutouts are typically:
        # - Rectangular holes ~6.5-7mm wide
        # - Located in the plate layer
        # - Paired on either side of large keys
        if 6 < bbox.xlen < 8 and bbox.zlen < 5:
            positions.append({
                "x": round((bbox.xmin + bbox.xmax) / 2, 2),
                "y": round((bbox.ymin + bbox.ymax) / 2, 2),
                "width": round(bbox.xlen, 2)
            })
    
    return positions

stabilizers = find_stabilizer_cutouts(keyboard)
print(json.dumps(stabilizers, indent=2))
```

### Creating Custom Keycap Profile

```python
# custom_keycap_profile.py
import cadquery as cq

# Reference Cherry profile dimensions from repository
cherry_ref = cq.importers.importStep("Keycap Profiles/Cherry Profile/Cherry-R1.stp")
ref_bbox = cherry_ref.val().BoundingBox()

# Create custom keycap based on Cherry dimensions
def create_custom_keycap(top_width=12, top_depth=12, height=8, angle=7):
    """Generate custom keycap with specified parameters"""
    keycap = (
        cq.Workplane("XY")
        # Base (standard 18x18mm)
        .box(18, 18, 1)
        .faces(">Z").workplane()
        # Tapered body
        .box(top_width, top_depth, height)
        .faces(">Z").workplane()
        # Angled top surface
        .transformed(rotate=(angle, 0, 0))
        # Slight dish
        .circle(top_width / 2).cutBlind(-0.5)
        # Stem mount (Cherry MX compatible)
        .faces("<Z").workplane()
        .rect(4, 1.2).extrude(4)
        .rect(1.2, 4).cutThruAll()
    )
    return keycap

custom_cap = create_custom_keycap(top_width=13, top_depth=13, height=9)
cq.exporters.export(custom_cap, "custom-keycap.step")
```

### Batch Processing Multiple Models

```python
# batch_export_cases.py
import os
import cadquery as cq
from pathlib import Path

# Process all Q-Series cases
q_series_path = Path("Q-Series")
output_dir = Path("exports/q-series-stl")
output_dir.mkdir(parents=True, exist_ok=True)

for model_dir in q_series_path.iterdir():
    if not model_dir.is_dir():
        continue
    
    # Look for case STEP files
    case_files = list(model_dir.glob("*Case*.stp")) + list(model_dir.glob("*Case*.step"))
    
    for case_file in case_files:
        try:
            print(f"Processing {case_file.name}...")
            case = cq.importers.importStep(str(case_file))
            
            # Export as STL
            output_file = output_dir / f"{case_file.stem}.stl"
            cq.exporters.export(case, str(output_file))
            print(f"  → Exported to {output_file.name}")
            
        except Exception as e:
            print(f"  ✗ Error processing {case_file.name}: {e}")
```

## Configuration and Environment

### Setting Up CAD Toolchain

```bash
# Install Python CAD libraries
pip install cadquery ezdxf numpy
pip install OCP  # OpenCascade bindings

# For FreeCAD Python API
pip install freecad  # or use system FreeCAD installation
```

### Environment Variables

```python
# config.py
import os
from pathlib import Path

# Repository location
KEYCHRON_REPO = Path(os.getenv("KEYCHRON_REPO_PATH", "./Keychron-Keyboards-Hardware-Design"))

# CAD export settings
EXPORT_TOLERANCE = float(os.getenv("CAD_EXPORT_TOLERANCE", "0.01"))
MESH_RESOLUTION = float(os.getenv("STL_MESH_RESOLUTION", "0.1"))

# 3D printing defaults
PRINT_LAYER_HEIGHT = float(os.getenv("PRINT_LAYER_HEIGHT", "0.2"))
PRINT_INFILL = int(os.getenv("PRINT_INFILL_PERCENT", "20"))
```

## License and Usage Guidelines

### Understanding the License

This repository is **source-available** with specific terms:

- ✅ **Allowed**: Personal use, educational use, studying designs
- ✅ **Allowed**: Original compatible accessories and add-ons (not subject to commercial restriction)
- ✅ **Allowed**: Modifications for personal builds
- ❌ **Not allowed**: Copying and selling Keychron keyboards or mice
- ❌ **Not allowed**: Using Keychron trademarks as your own branding

### Contribution Guidelines

```bash
# Fork and clone for contributions
git clone https://github.com/YOUR_USERNAME/Keychron-Keyboards-Hardware-Design.git
cd Keychron-Keyboards-Hardware-Design

# Create feature branch
git checkout -b fix/q1-plate-dimensions

# Make changes to CAD files
# Document changes in commit message

git add Q-Series/Q1/Q1-Plate.dxf
git commit -m "Fix Q1 plate switch hole spacing to 19.05mm standard"
git push origin fix/q1-plate-dimensions

# Create pull request on GitHub
```

## Troubleshooting

### STEP File Won't Open

```python
# validate_step_file.py
import OCP
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone

def validate_step_file(filepath):
    """Check if STEP file is valid and report issues"""
    reader = STEPControl_Reader()
    status = reader.ReadFile(str(filepath))
    
    if status == IFSelect_RetDone:
        print(f"✓ {filepath} is valid STEP file")
        reader.TransferRoots()
        shape = reader.OneShape()
        print(f"  Contains {shape.NbChildren()} root shapes")
        return True
    else:
        print(f"✗ {filepath} has errors (status code: {status})")
        return False

# Validate all STEP files in a directory
from pathlib import Path
for step_file in Path("Q-Series/Q1").glob("*.stp"):
    validate_step_file(step_file)
```

### Dimension Mismatches

```python
# verify_dimensions.py
import cadquery as cq

def compare_plate_case_fit(plate_path, case_path):
    """Verify plate fits within case boundaries"""
    plate = cq.importers.importStep(plate_path)
    case = cq.importers.importStep(case_path)
    
    plate_bbox = plate.val().BoundingBox()
    case_bbox = case.val().BoundingBox()
    
    # Check clearances
    clearance_x = case_bbox.xlen - plate_bbox.xlen
    clearance_y = case_bbox.ylen - plate_bbox.ylen
    
    print(f"Plate: {plate_bbox.xlen:.2f} x {plate_bbox.ylen:.2f} mm")
    print(f"Case:  {case_bbox.xlen:.2f} x {case_bbox.ylen:.2f} mm")
    print(f"Clearance: {clearance_x:.2f} x {clearance_y:.2f} mm")
    
    if clearance_x < 0 or clearance_y < 0:
        print("⚠ WARNING: Plate larger than case!")
        return False
    elif clearance_x < 1 or clearance_y < 1:
        print("⚠ WARNING: Very tight fit (<1mm clearance)")
    else:
        print("✓ Dimensions compatible")
    
    return True

compare_plate_case_fit(
    "K-Pro-Series/K8-Pro/K8-Pro-Plate.stp",
    "K-Pro-Series/K8-Pro/K8-Pro-Case.stp"
)
```

### Large File Handling

```bash
# Use Git LFS for large CAD files if contributing
git lfs install
git lfs track "*.stp"
git lfs track "*.step"
git lfs track "*.dwg"

# Clone with LFS support
git lfs clone https://github.com/Keychron/Keychron-Keyboards-Hardware-Design.git
```

## Resources

- **Repository**: https://github.com/Keychron/Keychron-Keyboards-Hardware-Design
- **Homepage**: https://www.keychron.com/
- **Discord Community**: https://discord.com/invite/HAYbRrTsjN
- **File Format Guide**: `/docs/file-format-guide.md`
- **Getting Started**: `/docs/getting-started.md`
- **3D Printing Guide**: `/docs/3d-printing-guide.md`
- **License FAQ**: `/docs/license-faq.md`
