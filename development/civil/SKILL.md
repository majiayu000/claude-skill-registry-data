---
name: civil
description: Civil infrastructure and construction
license: MIT
compatibility: opencode
metadata:
  audience: engineers, contractors, project managers
  category: engineering
---

## What I do

- Provide civil infrastructure domain knowledge
- Explain construction methods and materials
- Guide on building codes and permits
- Assist with site development and planning
- Support infrastructure project management

## When to use me

- When working on building or infrastructure projects
- When understanding construction methodologies
- When navigating regulatory requirements
- When selecting construction materials
- When planning site development

## Key Concepts

### Construction Materials

| Material | Properties | Common Uses |
|----------|------------|-------------|
| Concrete | High compressive strength, low tensile | Foundations, slabs, columns |
| Steel | High strength, ductile | Frames, reinforcement |
| Masonry | Compressive strength, fire resistant | Walls, foundations |
| Wood | Renewable, easy to work | Framing, formwork |
| Asphalt | Flexible, waterproof | Pavements, roofing |

### Project Phases

```python
PROJECT_PHASES = {
    "pre_design": {
        "activities": ["Feasibility study", "Site selection", "Budget estimate"],
        "deliverable": "Project charter"
    },
    "design": {
        "activities": ["Schematic design", "Design development", "Construction documents"],
        "deliverable": "Drawings, specifications"
    },
    "procurement": {
        "activities": ["Bidding", "Contractor selection", "Material ordering"],
        "deliverable": "Contracts"
    },
    "construction": {
        "activities": ["Site preparation", "Foundation", "Structure", "MEP", "Finishes"],
        "deliverable": "Completed facility"
    },
    "closeout": {
        "activities": ["Testing", "Commissioning", "Training", "Documentation"],
        "deliverable": "Final project"
    }
}
```

### Building Systems

- **Structural**: Load-bearing elements (foundation, frame, roof)
- **Envelope**: Walls, windows, doors, roofing
- **MEP**: Mechanical, Electrical, Plumbing
- **Fire Protection**: Detection, suppression, egress
- **Communication**: Data, security, AV systems

### Infrastructure Types

- **Transportation**: Roads, bridges, railways, airports, ports
- **Water Resources**: Dams, levees, canals, water treatment
- **Utilities**: Power, gas, telecommunications, sanitation
- **Public Buildings**: Schools, hospitals, government facilities

### Construction Contracts

| Type | Payment | Risk |
|------|---------|------|
| Lump Sum | Fixed price | Contractor |
| Cost Plus | Actual cost + fee | Owner |
| Time & Materials | Hourly rates | Shared |
| Unit Price | Per unit quantity | Shared |
| Design-Build | Single contract | Contractor |
| EPC | Turnkey | Contractor |

### Site Development

```python
# Grading calculations
def cut_fill_volumes(grid, target_elevation):
    """Calculate cut and fill volumes from grid"""
    cut_volume = 0
    fill_volume = 0
    
    for cell in grid:
        elevation_diff = cell.elevation - target_elevation
        volume = elevation_diff * cell.area
        
        if elevation_diff > 0:
            cut_volume += volume
        else:
            fill_volume += abs(volume)
    
    return {"cut": cut_volume, "fill": fill_volume}
```

### Regulatory Framework

- **Zoning**: Land use regulations
- **Building Codes**: Safety standards (IBC, IRC)
- **Environmental**: NEPA, EPA regulations
- **Accessibility**: ADA requirements
- **Permits**: Building, grading, utility connections
