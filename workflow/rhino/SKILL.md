---
name: rhino
description: "Automate Rhino modeling through RhinoCommon, work with Grasshopper data trees, and configure Rhino.Compute workflows."
category: cad
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rhino", "rhino-8", "grasshopper", "rhinocommon", "nurbs", "rhino-inside", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# McNeel Rhinoceros (Rhino 8) AI Skill Guide (Claude)

## Overview & Engine Architecture
Robert McNeel & Associates Rhinoceros (Rhino 8) is the industry standard for mathematical NURBS modeling, SubD organic design, and Grasshopper parametric computation across architecture, marine engineering, and industrial design. Claude operates as a Senior Computational Designer and Geometry Pipeline Engineer, specializing in **RhinoCommon .NET/Python 3 APIs (`Rhino.Geometry`)**, **Grasshopper Data Tree optimization**, **NURBS surface continuity analysis (G0-G3)**, and **headless `compute.rhino3d` microservices**.

### Rhino 8 Engine Architecture & Computational Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Rhino 8 Core Architecture                   │
│                                                             │
│  Geometry Core (OpenNURBS Kernel)                           │
│  ├── NURBS Curves, Breps (Polysurfaces), SubD, and Meshes   │
│  ├── Document Units & Absolute Tolerance Verification       │
│  └── Grasshopper Visual Programming (Data Trees & Clusters) │
│                                                             │
│  Automation & Headless Subsystems                           │
│  ├── RhinoCommon API (Native C# / Python 3.9 Runtime)       │
│  ├── `rhinoscriptsyntax` & IronPython Legacy Wrappers       │
│  ├── Rhino.Inside (Embed Rhino inside Revit, Unity, Python) │
│  └── Rhino.Compute (Headless Cloud Geometry Web Service)    │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **RhinoCommon & Python 3 Scripting**: Author high-performance Python scripts using `Rhino.Geometry` and `rhinoscriptsyntax` for procedural Brep booleans, bounding box nesting, and batch transformation.
2. **NURBS & Polysurface Boolean Diagnostics**: Remediate solid boolean failures by identifying naked edges, overlapping coplanar faces, and self-intersections relative to absolute document tolerance ($0.001\text{ mm}$).
3. **Grasshopper Data Tree Optimization**: Structure Grasshopper definitions to eliminate exponential data branch matching (`{A;B;C}`), using `Flatten`, `Graft`, `Simplify`, and `Path Mapper`.
4. **Headless Cloud Automation**: Construct command-line batch pipelines using `Rhino.exe -runscript` and REST payloads for `compute.rhino3d` servers.

---

## Production Python Automation: Batch Solid Boolean & STEP Exporter

Save this script and execute inside Rhino Python 3 editor or via `-runscript` to automate solid unioning, manifold edge checks, and STEP export:

```python
"""
Rhino 8 Automation: Batch Solid Union & Manifold STEP Exporter
Compatible with Rhino 8 CPython 3 and IronPython runtimes.
"""

import os
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def process_and_export_solids(output_step_path: str):
    # 1. Select all Polysurfaces / Breps in Document
    brep_ids = rs.ObjectsByType(rs.filter.polysurface | rs.filter.surface)
    if not brep_ids:
        print("Error: No surfaces or polysurfaces found in document.")
        return

    print(f"Found {len(brep_ids)} Brep objects. Validating solid status...")
    
    # 2. Check for Non-Manifold / Naked Edges
    solid_ids = []
    for obj_id in brep_ids:
        if rs.IsPolysurfaceClosed(obj_id):
            solid_ids.append(obj_id)
        else:
            print(f"Warning: Object {obj_id} is an OPEN polysurface (Naked Edges detected).")

    if not solid_ids:
        print("No valid closed solids to process.")
        return

    # 3. Perform Solid Boolean Union
    print(f"Executing Boolean Union on {len(solid_ids)} closed solids...")
    union_result = rs.BooleanUnion(solid_ids, delete_input=False)
    
    export_target_ids = union_result if union_result else solid_ids

    # 4. Export Selected Geometry to STEP
    os.makedirs(os.path.dirname(os.path.abspath(output_step_path)), exist_ok=True)
    rs.SelectObjects(export_target_ids)
    
    # Execute Silent CLI Export Command
    cmd = f'-_Export "{output_step_path}" _Enter _Enter'
    rs.Command(cmd, echo=False)
    
    print(f"Successfully exported geometry to STEP: {output_step_path}")

if __name__ == "__main__":
    process_and_export_solids("C:/Export/Assembled_Model.step")
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Boolean Difference Failed` on Closed Solids** | Input solids share coincident coplanar faces or intersection curve falls within document tolerance ($10^{-4}$). | 1. Run `ShowEdges` with **Naked Edges** selected.<br>2. Shift one solid by a micro-offset ($0.01\text{ mm}$) to break coincident face alignment.<br>3. Run `Intersect` to manually inspect the generated intersection curves for gaps. |
| **Grasshopper Freezes / High Memory on Tree Operations** | Unequal branch path depths (e.g. `{0;0}` matching against `{0;0;0}`) causing combinatorial explosion ($N \times M$ computations). | 1. Attach a **Simplify** or **Shift Paths** component to normalize data tree depths.<br>2. Enable **Grasshopper Profiler** (*Display $\rightarrow$ Canvas Widgets $\rightarrow$ Profiler*) to spot slow nodes.<br>3. Lock solvers (`F5`) before editing heavy definition networks. |
| **SubD to NURBS (`ToNURBS`) Yields Distorted Topology** | High-valence extraordinary vertices ($>6$ star points) in SubD cage producing tight knot spacing in Brep faces. | 1. In SubD edit mode, re-route edge loops to ensure all interior vertices have valence 4.<br>2. Set `ToNURBS` option `PackSubDFaces=True` to merge quad patches.<br>3. Check curvature with `Zebra` command. |
| **Rhino 3DM File Size Exceeds Hundreds of Megabytes** | Render mesh caches stored inside the file for dense polysurfaces. | 1. Run `ClearAllMeshes` command before saving.<br>2. Save with **Save Small** enabled (`SaveSmall` command) to strip cached display meshes. |

---

## Command Line Syntax & Rhino.Compute Integration

```bash
# Windows CLI: Headless Rhino Script Execution
"C:\Program Files\Rhino 8\System\Rhino.exe" /nosplash /runscript="-_RunPythonScript C:\Pipeline\auto_process.py"

# Launch Rhino.Compute Headless Web Server
"C:\Program Files\Rhino 8\System\compute.geometry.exe" --port 8081

# Clean Corrupted Scheme Settings via PowerShell
Remove-Item -Path "$env:APPDATA\McNeel\Rhinoceros\8.0\settings\settings-Scheme__Default.xml" -Force
```

### Essential File Locations
- **Windows User Settings**: `%APPDATA%\McNeel\Rhinoceros\8.0\settings`
- **Windows Grasshopper Libraries**: `%APPDATA%\Grasshopper\Libraries`
- **macOS User Settings**: `~/Library/Application Support/McNeel/Rhinoceros/8.0/`
- **macOS Grasshopper Libraries**: `~/Library/Application Support/McNeel/Rhinoceros/MacPlugins/Grasshopper/Libraries`

---

## Agent Operational Directive
> **MANDATORY**: Before running Boolean operations in Rhino, verify that objects are closed solids using `rs.IsPolysurfaceClosed()`. In Grasshopper workflows, normalize data tree branch depths to prevent combinatorial memory spikes.
