---
name: houdini
description: "Automate Houdini procedural workflows with VEX, the hou Python API, PDG/TOPs, and Solaris/Karma rendering."
category: 3d
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["houdini", "vex", "hou-python", "solaris-karma", "pdg-tops", "vellum", "flip-fluids"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# SideFX Houdini AI Skill Guide (Claude)

## Overview & Engine Architecture
SideFX Houdini is the industry-standard procedural VFX, procedural modeling, dynamic simulation, and USD-native pipeline tool. Claude operates as a Senior Houdini TD (Technical Director), specializing in **VEX syntax and vector math**, **Python `hou` scripting via `hython`**, **Solaris USD / Karma XPU rendering**, **PDG/TOPs task-graph automation**, and **headless CLI simulation baking**.

### Houdini Context Architecture & Execution Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Houdini Context Architecture                │
│                                                             │
│  Context Domains                                            │
│  ├── SOPs (Surface Operators - Geometry & Modeling)         │
│  ├── DOPs (Dynamic Operators - FLIP, Pyro, Vellum, RBD)     │
│  ├── LOPs / Solaris (USD Scene Composition & Lighting)      │
│  ├── TOPs / PDG (Procedural Dependency Graph & Wedging)     │
│  └── Karma XPU (Hydra Delegate CPU/GPU Renderer)            │
│                                                             │
│  Programming & Scripting Interfaces                         │
│  ├── VEX (High-Performance SIMD Vector Expression Language) │
│  ├── `hou` (Python 3.11 Houdini Object Model API)           │
│  └── Hython / HBatch (Headless Batch Execution Interpreters)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **VEX Code Generation & Optimization**: Write vectorized, thread-safe VEX snippets for Attribute Wranglers, Volume Wranglers, and Point Deformation routines using `@P`, `@v`, `@orient`, and `@pscale`.
2. **Headless Python Automation (`hython`)**: Script standalone pipeline tools using `hou` to inspect scenes, dirty/cook TOP networks, parameterize HDAs, and trigger ROP nodes.
3. **Simulation Solver Tuning**: Troubleshoot substepping, collision margins, pressure projection convergence, and spatial oversampling in Vellum, FLIP, and RBD solvers.
4. **Solaris & MaterialX USD Pipeline**: Construct USD primitive hierarchies, configure Karma XPU shaders using MaterialX (`mtlxstandard_surface`), and set up AOV cryptomatte passes.

---

## Production Python Automation: Headless Simulation Baker (`hython`)

Save this script as `bake_simulation.py` and run via `hython` to cook and cache heavy simulations to disk without opening the GUI:

```python
"""
Headless Houdini Simulation & ROP Baker
Run via: hython bake_simulation.py <hip_file> <rop_node_path> [start_frame] [end_frame]
"""

import sys
import os
import hou

def bake_rop_node(hip_path: str, rop_path: str, start_frame: int = None, end_frame: int = None):
    if not os.path.exists(hip_path):
        print(f"Error: HIP file not found: {hip_path}")
        sys.exit(1)

    print(f"Loading scene: {hip_path}...")
    hou.hipFile.load(hip_path, suppress_save_prompt=True, ignore_load_warnings=True)

    target_node = hou.node(rop_path)
    if not target_node:
        print(f"Error: Node '{rop_path}' does not exist in scene.")
        sys.exit(1)

    # Set frame range override if specified
    if start_frame is not None and end_frame is not None:
        target_node.parm("trange").set(1) # Specific frame range
        target_node.parm("f1").set(start_frame)
        target_node.parm("f2").set(end_frame)
        target_node.parm("f3").set(1)

    print(f"Cooking node: {target_node.path()} from frame {target_node.evalParm('f1')} to {target_node.evalParm('f2')}...")
    
    try:
        # Execute ROP cook
        target_node.render(verbose=True, output_progress=True)
        print("Baking completed successfully.")
    except hou.Error as e:
        print(f"Cook failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: hython bake_simulation.py <scene.hip> <rop_path> [start] [end]")
        sys.exit(1)
        
    start = int(sys.argv[3]) if len(sys.argv) > 3 else None
    end = int(sys.argv[4]) if len(sys.argv) > 4 else None
    bake_rop_node(sys.argv[1], sys.argv[2], start, end)
```

---

## Production VEX Snippet: Quaternion Point Rotation & Noise Advection

Use this snippet in a **Point Wrangle** SOP to orient instanced particles along a curl noise velocity vector:

```c
// Calculate 3D Curl Noise Velocity Field
vector freq = chv("frequency");
vector offset = chv("offset") + @P * freq;
vector noise_v = curlnoise(offset);

// Blend existing velocity with noise
float blend = chf("noise_blend");
@v = lerp(@v, noise_v * chf("speed"), blend);

// Update Point Orientation Quaternion (@orient) to face velocity
vector up = {0, 1, 0};
if (length(@v) > 0.001) {
    matrix3 m = maketransform(normalize(@v), up);
    @orient = quaternion(m);
}

// Age-based scale falloff
float life_ratio = @age / @life;
@pscale = chf("base_scale") * (1.0 - smooth(0.7, 1.0, life_ratio));
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **FLIP Fluid Explosion at Frame 1** | Particle separation too coarse relative to narrow collision geometry, or initial velocity creates divergence spikes. | 1. Decrease **Particle Separation** on FLIP Object.<br>2. In FLIP Solver $\rightarrow$ *Volume Motion*, set **Min Substeps** to 2-4.<br>3. Enable **Collision Separation** on static collision objects. |
| **Vellum Cloth Collision Penetration / Sticking** | Insufficient substeps or collision thickness is greater than distance between overlapping folds. | 1. Increase **Substeps** on Vellum Solver (default is 10; increase to 25-40 for fine cloth).<br>2. Reduce `thickness` attribute on Vellum Cloth constraints.<br>3. Enable **Layer Shock Absorber** for multi-layered garments. |
| **Karma XPU Shader Falling Back to CPU** | MaterialX network contains VEX-only VOP nodes unsupported on GPU hardware acceleration. | 1. Replace classic VOP nodes with native **MaterialX standard nodes** (`mtlxstandard_surface`).<br>2. Check Houdini Console for `XPU_WARNING_UNSUPPORTED_NODE`.<br>3. Ensure GPU drivers match NVIDIA Studio / CUDA 12 requirements. |
| **PDG / TOPs Work Items Hanging / Deadlock** | Work item output files were not written to the path expected by downstream dependency nodes. | 1. Open **PDG Service Monitor**.<br>2. Inspect work item log: verify token `$HIP` or `$PDG_DIR` expansion matches output directory.<br>3. Select TOP node $\rightarrow$ Right-Click $\rightarrow$ **Dirty and Cook Selected Node**. |

---

## Command Line Syntax & Batch Processing

```bash
# Windows CLI: Headless Python Script Execution
"C:\Program Files\Side Effects Software\Houdini 20.5.278\bin\hython.exe" "C:\Pipeline\bake_pyro.py"

# Linux CLI: Render Solaris LOP USD Stage via Karma
hython -c "import hou; hou.hipFile.load('scene.hip'); hou.node('/stage/karma1').render()"

# Run HScript Command Line Engine
hbatch -c "render -Va /out/geometry_cache" "C:\Projects\destruction.hip"
```

### Environment Configuration & Package Locations
- **Windows Environment**: `%USERPROFILE%\Documents\houdini20.5\houdini.env`
- **Windows JSON Packages**: `%USERPROFILE%\Documents\houdini20.5\packages\*.json`
- **Linux Environment**: `$HOME/houdini20.5/houdini.env`
- **Critical Environment Variables**:
 - `HOUDINI_PATH`: Custom tools, HDAs, and plugin search paths
 - `HOUDINI_DSO_ERROR=1`: Displays verbose C++ plugin/DSO load errors
 - `OCIO`: Path to custom ACES OpenColorIO configuration file

---

## Agent Operational Directive
> **MANDATORY**: For high-performance geometry deformation and point manipulation, write vectorized VEX wranglers rather than Python SOPs. When scripting headless batch pipelines, use `hython` and handle exceptions with explicit error logging.
