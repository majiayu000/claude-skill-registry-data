---
name: cad
description: Computer-aided design principles and tools
license: MIT
compatibility: opencode
metadata:
  audience: engineers, designers, manufacturers
  category: engineering
---

## What I do

- Create 2D drawings and 3D models of mechanical parts
- Generate technical documentation and manufacturing files
- Perform geometric constraint solving and parametric modeling
- Support assembly design and component routing
- Export designs for manufacturing or simulation

## When to use me

- When creating mechanical designs for manufacturing
- When generating detailed engineering drawings
- When building 3D models for visualization or simulation
- When designing assemblies with multiple components
- When preparing files for CNC machining or 3D printing

## Key Concepts

### CAD File Formats

| Format | Type | Applications |
|--------|------|--------------|
| STEP | 3D neutral | Exchange, CAD interoperability |
| IGES | 3D neutral | Legacy CAD exchange |
| STL | 3D mesh | 3D printing, rapid prototyping |
| DXF | 2D | Drawing exchange |
| DWG | 2D | AutoCAD native format |
| OBJ | 3D mesh | Visualization, 3D graphics |
| Parasolid | 3D | Siemens NX, SolidWorks |

### Parametric Modeling

```python
# Example: Creating a parameterized part
class ParametricPart:
    def __init__(self, **dimensions):
        self.dimensions = dimensions
    
    def create_sketch(self, points):
        """Create 2D profile from points"""
        return {
            "type": "sketch",
            "entities": points,
            "constraints": []
        }
    
    def extrude(self, sketch, depth):
        """Extrude sketch to create 3D feature"""
        return {
            "type": "extrude",
            "profile": sketch,
            "depth": depth,
            "direction": "positive"
        }
    
    def create_hole(self, location, diameter, depth):
        """Create a hole feature"""
        return {
            "type": "hole",
            "center": location,
            "diameter": diameter,
            "depth": depth
        }
```

### Geometric Constraints

- **Coincident**: Two points occupy same location
- **Collinear**: Points lie on same line
- **Parallel**: Lines have same direction
- **Perpendicular**: Lines intersect at 90°
- **Concentric**: Centers coincide
- **Equal**: Dimensions or radii match
- **Tangent**: Curves touch without crossing

### Assembly Design

```python
# Assembly constraint types
ASSEMBLY_CONSTRAINTS = {
    "mate": {
        "description": "Two faces in contact, opposite directions",
        "degrees_removed": 3
    },
    "flush": {
        "description": "Two faces coplanar",
        "degrees_removed": 2
    },
    "angle": {
        "description": "Constrained angular relationship",
        "degrees_removed": 2
    },
    "insert": {
        "description": "Axial insertion (e.g., pin in hole)",
        "degrees_removed": 2
    }
}
```

### Common CAD Software

| Software | Vendor | Strengths |
|----------|--------|-----------|
| SolidWorks | Dassault Systèmes | Mechanical, assemblies |
| CATIA | Dassault Systèmes | Complex surfaces, aerospace |
| NX | Siemens | Advanced manufacturing |
| Inventor | Autodesk | Mechanical, simulation |
| Fusion 360 | Autodesk | Cloud, accessible |
| Onshape | PTC | Web-based, collaboration |
| FreeCAD | Open source | Free, parametric |
