---
name: blender
description: "Automate Blender scenes with the bpy Python API, build Geometry Nodes workflows, configure Cycles or EEVEE renders, and troubleshoot headless batch jobs."
category: 3d
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["blender", "bpy", "python-api", "cycles", "eevee", "geometry-nodes", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Blender 4.x 3D Creation Suite AI Skill Guide (Claude)

## Overview & Engine Architecture
Blender 4.x is an open-source 3D creation suite covering modeling, sculpting, animation, simulation, compositing, and rendering. Its core automation surface is the **`bpy` Python API** embedded in every Blender build, plus **Geometry Nodes** (node-based procedural mesh/instance graphs), **Shader Nodes**, and two primary renderers: **EEVEE** (real-time) and **Cycles** (path-traced). Claude operates as a Principal Technical Artist and Pipeline TD, specializing in **headless `blender --background --python` batch jobs**, **idempotent scene setup scripts**, **addon packaging (`bl_info`)**, and **render farm-ready CLI flags**.

### Blender Runtime & Automation Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Blender 4.x Engine Architecture             │
│                                                             │
│  Data Model (DNA / RNA)                                     │
│  ├── bpy.data (meshes, materials, objects, scenes, images)  │
│  ├── bpy.context (active object, mode, selected, view_layer)│
│  └── bpy.ops (operator layer; prefer data API for scripts)  │
│                                                             │
│  Evaluation & Nodes                                         │
│  ├── Geometry Nodes / Shader Nodes / Compositor             │
│  ├── Dependency Graph (depsgraph) evaluation                │
│  └── Animation / Drivers / Constraints                      │
│                                                             │
│  Render & CLI                                               │
│  ├── EEVEE / Cycles / Workbench                             │
│  ├── blender -b file.blend -P script.py -o //out -a         │
│  └── Addon system (scripts/addons, bl_info, register())     │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Prefer Data API over Operators**: For production scripts, mutate `bpy.data` / object properties directly; reserve `bpy.ops` for interactive or mode-dependent actions only.
2. **Headless Batch Pipelines**: Author scripts that run under `blender --background --python` with zero UI assumptions (`bpy.context.view_layer` still valid).
3. **Deterministic Scene Setup**: Create collections, materials, cameras, and lights idempotently (delete-or-reuse by name before creating).
4. **Render Configuration**: Set Cycles samples, denoiser, resolution, filepath, and file format before calling `bpy.ops.render.render()`.
5. **Addon Hygiene**: Ship `bl_info`, `register()` / `unregister()`, and avoid writing outside Blender's user scripts path without explicit user consent.

---

## Production Python: Headless Mesh + Cycles Still Render

Save as `batch_setup_and_render.py` and run:
`blender --background --python batch_setup_and_render.py`

```python
# ==============================================================================
# Blender 4.x bpy: create a lit scene and render a Cycles still
# ==============================================================================
import bpy
from mathutils import Euler
from math import radians

# Reset to empty scene
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = "//render_out/hero_still"
scene.render.image_settings.file_format = "PNG"

# Geometry
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 1))
sphere = bpy.context.active_object
sphere.name = "HeroSphere"

bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
bpy.context.active_object.name = "Ground"

# Material
mat = bpy.data.materials.new(name="HeroMat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.15, 0.45, 0.85, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.35
sphere.data.materials.append(mat)

# Camera + light
cam_data = bpy.data.cameras.new("HeroCam")
cam_obj = bpy.data.objects.new("HeroCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (4.5, -4.5, 3.2)
cam_obj.rotation_euler = Euler((radians(65), 0, radians(45)), "XYZ")
scene.camera = cam_obj

light_data = bpy.data.lights.new(name="KeyLight", type="AREA")
light_data.energy = 400
light_obj = bpy.data.objects.new("KeyLight", light_data)
bpy.context.collection.objects.link(light_obj)
light_obj.location = (2.5, -2.0, 4.0)

bpy.ops.render.render(write_still=True)
print("Render complete:", scene.render.filepath)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`AttributeError` on bpy context in background** | Script assumed UI-only context fields or active 3D View. | Use `bpy.data` / `scene` explicitly; pass `override` dicts only when required. |
| **Operators fail with "context is incorrect"** | Wrong mode, no active object, or wrong area type. | Switch modes via data API where possible, or set `bpy.context.view_layer.objects.active`. |
| **Cycles render is black** | Missing camera, lights, or wrong world/shader setup. | Assert `scene.camera`, add Area/Sun light, check material node links. |
| **Addon not listed after install** | Missing/invalid `bl_info` or `register()` exception. | Check System Console / terminal traceback; verify Blender version tuple. |

---

## Essential CLI Patterns

```bash
# Background script (no UI)
blender --background project.blend --python pipeline/export_fbx.py

# Frame range animation render
blender -b project.blend -o //renders/frame_#### -F PNG -s 1 -e 120 -a

# Factory reset + script (CI-safe)
blender --factory-startup --background --python tests/smoke_bpy.py
```

### Essential Paths
- **User addons**: `~/AppData/Roaming/Blender Foundation/Blender/<version>/scripts/addons` (Windows)
- **Preferences**: Blender Preferences → File Paths / System
- **Python console**: Scripting workspace → Interactive Console

---

## Agent Operational Directive
> **MANDATORY**: Prefer `bpy.data` mutations over `bpy.ops` in automation. Always set `scene.camera`, output path, and engine before rendering. Never assume an interactive 3D Viewport exists in `--background` mode.
