---
name: civil-3d-skill
description: >-
  Autodesk Civil 3D workflows — corridors, surfaces, alignments/profiles, pipe
  networks, grading, survey; COM and .NET APIs. Version detection before API
  advice.
license: Apache-2.0
compatibility: opencode
category: CAD & Hardware Design
---

# Civil 3D Workflow Guidance

Provenance: extracted from civil-3d-specialist-subagent. Domain knowledge for Civil 3D corridor design, surfaces, pipe networks, and survey workflows.

## CRITICAL: Version Detection (MANDATORY)

### Version Prompting Rules

You **MUST** determine the user's Civil 3D version **BEFORE** providing any guidance.

**If the user has NOT specified their Civil 3D version:**

```
STOP and ask:
"What version of Civil 3D are you using? (e.g., 2026, 2025, 2024, 2023)

This is required because feature availability, UI locations, and workflows 
differ between versions. Providing incorrect version guidance could lead to 
data loss or broken models."
```

**DO NOT proceed with any guidance until the user provides their version.**

### Supported Versions

| Version | Year | Build | Notes |
|---------|------|-------|-------|
| Civil 3D 2026 | 2026 | N.51.0 | Latest - includes new corridor workflows |
| Civil 3D 2025 | 2025 | N.49.0 | Pressure network improvements |
| Civil 3D 2024 | 2024 | N.47.0 | Dynamo integration updates |
| Civil 3D 2023 | 2023 | N.45.0 | Connected alignments |
| Civil 3D 2022 | 2022 | N.43.0 | Corridor overrides |

### Version-Sensitive Features

These features have significant differences between versions:
- **Corridor workflows** - Assembly and subassembly management changed in 2025+
- **Pressure networks** - Major overhaul in 2024+
- **Dynamo for Civil 3D** - Library expanded significantly in 2024+
- **Project management** - Data shortcuts behavior changed in 2023+
- **Survey workflows** - LINZ and local standards support varies by version


## Core Expertise Areas

### 1. Surface Management

#### Creating Surfaces
- Surface creation from DEM, contour, or point data
- Surface analysis (elevation, slope, aspect, watershed)
- Surface editing and smoothing operations
- Surface boundary management

#### Surface Best Practices
- Use appropriate point density for surface accuracy
- Apply surface boundaries to limit triangulation
- Use edit operations sparingly to maintain data integrity
- Verify surface with contour display and visual checks

### 2. Corridor Design

#### Corridor Workflow
1. Create alignment and profile
2. Design assembly with subassemblies
3. Build corridor from assembly along alignment
4. Create corridor surface
5. Extract cross sections
6. Calculate materials and quantities

#### Assembly Best Practices
- Keep assemblies simple and modular
- Use generic subassemblies where possible for flexibility
- Test assemblies with various target configurations
- Document lane widths, slopes, and material codes

### 3. Alignments and Profiles

#### Alignment Design
- Fixed, floating, and free line/curve combinations
- Superelevation calculations
- Design criteria file application
- Alignment label sets and styles

#### Profile Design
- Design profile with PVI and vertical curve constraints
- Profile display and style management
- Superimpose profiles for analysis
- Profile view band configuration

### 4. Pipe Networks

#### Gravity Pipe Networks
- Pipe network creation from objects or layout
- Pipe and structure editing
- Rules-based design (cover, slope, velocity)
- Interference checking

#### Pressure Pipe Networks
- Pressure network layout tools
- Fitting and appurtenance placement
- Pressure pipe sizing
- Parts list configuration (varies by version)

### 5. Grading and Site Design

#### Grading Tools
- Grading groups and criteria
- Feature line grading
- Elevation targets and slope targets
- Grading volume calculations

#### Site Design
- Parcels and parcel sizing
- Parcel numbering and labeling
- Right-of-way creation
- Lot grading strategies

### 6. Survey Workflows

#### Survey Data
- Import survey data (FBK, LIN, CSV, LandXML)
- Survey database management
- Survey point and figure management
- Traverse analysis and adjustment

#### Survey Best Practices
- Use consistent point numbering conventions
- Apply appropriate survey styles
- Verify control points before field-to-finish
- Use description keys for automated linework
## Civil 3D API Usage

### COM API (Python Example)

COM API PROGID version mapping (adjust based on user's Civil 3D version):
- Civil 3D 2026: AeccXUiLand.AeccApplication.13.6
- Civil 3D 2025: AeccXUiLand.AeccApplication.13.5
- Civil 3D 2024: AeccXUiLand.AeccApplication.13.4
- Civil 3D 2023: AeccXUiLand.AeccApplication.13.3

```python
import win32com.client

def create_surface(doc, name, version="13.6"):
    progid = f"AeccXUiLand.AeccApplication.{version}"
    civil = win32com.client.Dispatch(progid)
    civil.Documents.Open(doc)
    active_doc = civil.ActiveDocument
    
    surface = active_doc.Surfaces.Add(name)
    
    points = surface.Points
    points.Add(100.0, 200.0, 150.0, 0.0)
    points.Add(200.0, 200.0, 152.0, 0.0)
    points.Add(200.0, 100.0, 148.0, 0.0)
    
    surface.Rebuild()
    return surface
```

### .NET API (C# Example)

```csharp
using Autodesk.Civil;
using Autodesk.Civil.ApplicationServices;
using Autodesk.Civil.DatabaseServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;

[CommandMethod("CreateSurface")]
public void CreateSurface()
{
    var civilDoc = CivilApplication.ActiveDocument;
    var db = HostApplicationServices.WorkingDatabase;
    
    using (var tr = db.TransactionManager.StartTransaction())
    {
        ObjectId surfaceId = civilDoc.SurfaceCollection.Add("My Surface");
        tr.Commit();
    }
}
```
## Version-Specific Notes

### Civil 3D 2026
- Enhanced corridor target editing
- New subassembly composer features
- Improved data shortcut performance
- Updated Dynamo for Civil 3D library

### Civil 3D 2025
- Pressure network bending
- Enhanced intersection design
- New property set data support
- Improved grading optimization tools

### Civil 3D 2024
- Updated pressure network parts
- Enhanced Dynamo integration
- New project management features
- Improved quantity takeoff tools

### Civil 3D 2023
- Connected alignment improvements
- Enhanced corridor workflow
- New surface analysis tools
- Improved survey database functionality
## Workflow Templates

### New Corridor Project

```
1. Create alignment (fixed line + curves)
2. Create existing ground surface from survey/CAD
3. Create design profile (PVIs with vertical curves)
4. Build assembly (lanes, shoulders, ditches, sidewalks)
5. Create corridor targeting surface and alignment
6. Create corridor surface
7. Calculate cut/fill volumes
8. Extract cross sections for documentation
```

### Pipe Network Design

```
1. Set up parts list with appropriate pipe sizes
2. Create pipe network from object (alignment) or layout
3. Add structures (manholes, inlets, catch basins)
4. Apply design rules (cover, slope, velocity)
5. Run interference check
6. Edit pipe inverts and slopes
7. Generate profile view of pipe network
8. Create pipe network tables for documentation
```
## Documentation References

- Civil 3D Help: https://help.autodesk.com/view/CIV3D/
- Civil 3D Blog: https://www.autodesk.com/civil-3d-blog
- Civil 3D Forums: https://forums.autodesk.com/t5/civil-3d/ct-p/70
- Civil 3D API Reference: https://help.autodesk.com/view/CIV3D/{YEAR}/ENU/?guid=API_Guides
- Dynamo for Civil 3D: https://dynamobim.org/
- Autodesk Knowledge Network: https://knowledge.autodesk.com/
