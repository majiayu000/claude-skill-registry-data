---
name: cae
description: Computer-aided engineering analysis
license: MIT
compatibility: opencode
metadata:
  audience: engineers, analysts, designers
  category: engineering
---

## What I do

- Perform finite element analysis (FEA) for structural analysis
- Conduct computational fluid dynamics (CFD) simulations
- Run thermal and heat transfer analyses
- Perform modal analysis and vibration studies
- Support optimization and topology optimization

## When to use me

- When validating designs against physical loads
- When analyzing stress and deformation in structures
- When simulating fluid flow and heat transfer
- When optimizing designs for weight or performance
- When predicting product behavior before physical testing

## Key Concepts

### FEA Fundamentals

```python
# Basic FEA workflow
class FEAAnalysis:
    def __init__(self, geometry, mesh_params):
        self.geometry = geometry
        self.mesh_params = mesh_params
        self.boundary_conditions = []
        self.loads = []
    
    def mesh(self):
        """Generate finite element mesh"""
        return {
            "nodes": self._generate_nodes(),
            "elements": self._generate_elements(),
            "element_type": self.mesh_params.get("type", "tetrahedral")
        }
    
    def apply_boundary_conditions(self, bcs):
        """Apply displacement constraints"""
        self.boundary_conditions = bcs
    
    def apply_loads(self, loads):
        """Apply forces, pressures, temperatures"""
        self.loads = loads
    
    def solve(self):
        """Solve system of equations"""
        # K * u = F
        stiffness_matrix = self._assemble_stiffness()
        load_vector = self._assemble_loads()
        displacement = self._solve(stiffness_matrix, load_vector)
        return displacement
    
    def postprocess(self, results):
        """Calculate stresses, strains"""
        return {
            "displacement": results,
            "stress": self._compute_stress(results),
            "strain": self._compute_strain(results)
        }
```

### Element Types

| Element | DOFs | Applications |
|---------|------|--------------|
| Tetrahedron (3D) | 3/node | Complex 3D solids |
| Hexahedron (3D) | 3/node | Structured meshes |
| Triangle (2D) | 2/node | 2D plane stress/strain |
| Quadrilateral (2D) | 2/node | 2D with bending |
| Beam | 6/node | Structural frames |
| Shell | 5-6/node | Thin structures |

### Analysis Types

```python
# Static structural analysis
STATIC_ANALYSIS = {
    "equation": "[K]{u} = {F}",
    "assumptions": "Linear, time-independent",
    "outputs": ["displacement", "stress", strain"]
}

# Modal analysis
MODAL_ANALYSIS = {
    "equation": "[K]{phi} = omega^2 [M]{phi}",
    "purpose": "Natural frequencies, mode shapes",
    "outputs": ["frequencies", "mode_shapes"]
}

# Thermal analysis
THERMAL_ANALYSIS = {
    "types": ["steady-state", "transient"],
    "equation": "[K]{T} = {Q}",
    "outputs": ["temperature", "heat_flux"]
}
```

### Mesh Quality Metrics

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Aspect ratio | < 3 | < 5 | > 10 |
| Jacobian | > 0.5 | > 0.3 | < 0.1 |
| Skewness | < 20° | < 40° | > 60° |
| Warpage | < 5° | < 15° | > 30° |

### Common CAE Software

| Software | Analysis Types |
|----------|----------------|
| ANSYS | Structural, Thermal, CFD, Multi-physics |
| ABAQUS | Structural, Nonlinear, Dynamic |
| COMSOL | Multi-physics coupling |
| NASTRAN | Structural, Aeroelasticity |
| STAR-CCM+ | CFD, Multi-physics |
| Altair HyperWorks | Optimization, Structural |
