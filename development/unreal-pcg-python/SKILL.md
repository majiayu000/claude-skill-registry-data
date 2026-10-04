---
name: unreal-pcg-python
description: >
  Guide for Unreal Engine 5.x PCG (Procedural Content Generation) Python integration.
  Covers the PCGPythonInterop plugin, the Execute Python Script node, PCG Python API
  (PCGComponent, PCGBlueprintElement, PCGSpatialData, PCGPointData), editor automation,
  custom PCG nodes via Python, and known limitations.
  Use when the user asks about PCG Python, PCGPythonInterop, Execute Python Script node,
  Python scripting for procedural generation, automating PCG graphs with Python,
  or creating custom PCG nodes with Python/Blueprint.
---

# Unreal Engine PCG Python Integration Guide

## Overview

Python interacts with UE5's Procedural Content Generation (PCG) framework at **two levels**:

1. **PCGPythonInterop Plugin** (UE 5.5+, Beta) -- An editor-only PCG graph node ("Execute Python Script") that runs Python code mid-graph.
2. **PCG Python API** (UE 5.2+) -- Standard `unreal` module classes (`PCGComponent`, `PCGBlueprintElement`, etc.) for editor automation and custom node logic.

**Important:** All PCG Python functionality is **editor-only**. Python cannot run in packaged builds or at game runtime.

## Official Documentation

| Resource | URL |
|----------|-----|
| **PCG Framework Overview** | https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview |
| **PCG Framework Landing Page** | https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-in-unreal-engine |
| **PCG Development Guides** | https://dev.epicgames.com/documentation/en-us/unreal-engine/pcg-development-guides |
| **PCG Node Reference** | https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine |
| **PCG Data Types Reference** | https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-data-types-reference-in-unreal-engine |
| **PCGPythonInterop Plugin API** | https://dev.epicgames.com/documentation/en-us/unreal-engine/API/PluginIndex/PCGPythonInterop |
| **Python Editor Scripting** | https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python |
| **PCGComponent Python API** | https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGComponent |
| **PCGBlueprintElement Python API** | https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGBlueprintElement |
| **PCGBlueprintHelpers Python API** | https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGBlueprintHelpers |
| **PCGSpatialData Python API** | https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGSpatialData |
| **PCGPointData Python API** | https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGPointData |
| **Python Interop Roadmap** | https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/2213-python-interop-plugin |

### Community Resources

| Resource | URL |
|----------|-----|
| Forum: Create PCG Graph with Python | https://forums.unrealengine.com/t/create-pcg-graph-with-python/1714891 |
| Forum: Generate PCG through Python | https://forums.unrealengine.com/t/generate-pcg-through-python-script/2053107 |
| Forum: Change PCG Parameters from Python | https://forums.unrealengine.com/t/how-to-change-pcg-graph-parameters-from-python/2060532 |
| Custom PCG Nodes Guide (Blueshift) | https://blueshift-interactive.com/2025/09/03/how-to-create-custom-pcg-nodes/ |
| PCG Extended Toolkit (community C++ plugin) | https://github.com/PCGEx/PCGExtendedToolkit |
| Houdini to PCG Data Example | https://github.com/cgtoolbox/HoudiniToPCGDataExample |

---

## 1. PCGPythonInterop Plugin ("Execute Python Script" Node)

### Plugin Details

- **Location:** `Engine/Plugins/PCGInterops/PCGPythonInterop/`
- **Status:** Beta (`IsBetaVersion: true`, `EnabledByDefault: false`)
- **Module:** `PCGPythonInteropEditor` (Editor-only)
- **Dependencies:** `PCG` plugin + `PythonScriptPlugin`

### Enabling the Plugin

1. Enable **Python Editor Script Plugin** (under Plugins > Scripting)
2. Enable **PCG Python Interop** (under Plugins > Procedural Content Generation)
3. Restart the editor

### The "Execute Python Script" Node

This is the **only node** the plugin adds. It runs Python code within a PCG graph.

**Two input modes:**

| Mode | Description |
|------|-------------|
| `Input` | Reads Python source from an FString attribute on the "Source" pin, or uses an inline default script |
| `File` | Executes a `.py` file from disk |

**Key characteristics:**
- Runs on **main thread only** (Python GIL constraint)
- **Not cacheable** -- re-executes every time the graph runs
- **No data output** -- output pin is dependency-only (for execution ordering)
- Shows an editor toast on execution (suppressible via `bMuteEditorToast`)
- Default inline script: `print("Hello PCG World!")`

**Settings (UPROPERTY):**

```
ScriptInputMethod  -- EPCGPythonScriptInputMethod (Input or File)
ScriptSource       -- FPCGAttributePropertyInputSelector (which attribute holds the script)
ScriptPath         -- FFilePath (path to .py file, filtered to *.py)
bMuteEditorToast   -- bool (suppress editor notification)
```

All properties marked `PCG_Overridable` (can be set via PCG parameter overrides).

### Planned Future Features (from source TODOs)

- `EvaluateStatement` mode for line-by-line feedback
- Parameter inputs/outputs (get/set variables from within Python, like Blueprint/HLSL nodes)
- Generalized source editor in PCG for HLSL + Python
- Potential multi-thread support

---

## 2. PCG Python API (Editor Automation)

These classes are available via `import unreal` in any UE Python script, independent of the PCGPythonInterop plugin.

### Create PCG Graph Assets

```python
import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
graph = asset_tools.create_asset(
    'MyPCGGraph', '/Game/PCG',
    unreal.PCGGraph, unreal.PCGGraphFactory()
)
```

### Trigger PCG Generation

```python
# Get PCGComponent from an actor
pcg_comp = actor.get_component_by_class(unreal.PCGComponent)

pcg_comp.generate(True)          # force full regeneration
pcg_comp.generate_local(True)    # local only, no replication
pcg_comp.set_graph(my_graph)     # swap graph asset
pcg_comp.seed = 42               # set deterministic seed
pcg_comp.cleanup(True, False)    # cleanup generated components
```

### Work with Spatial Data

```python
# PCGSpatialData operations
spatial_data.to_point_data()              # convert to points
spatial_data.intersect_with(other)        # boolean intersection
spatial_data.union_with(other)            # boolean union
spatial_data.subtract(other)              # boolean subtraction
spatial_data.get_bounds()                 # get spatial bounds
spatial_data.get_density_at_position(pos) # sample density

# PCGPointData
point_data = unreal.PCGPointData()
points = point_data.get_points()          # -> Array[PCGPoint]
point_data.set_points(modified_points)
```

### PCGBlueprintHelpers (Utility Functions)

```python
helpers = unreal.PCGBlueprintHelpers
helpers.get_actor_data(context)
helpers.get_component(context)
helpers.get_random_stream_from_point(point, settings, component)
helpers.compute_seed_from_position(position)
helpers.create_pcg_data_from_actor(actor, parse_actor)
```

---

## 3. Custom PCG Nodes via PCGBlueprintElement

`PCGBlueprintElement` is the base class for custom PCG nodes in Blueprint (and theoretically Python). Available since UE 5.2.

### Key Overridable Methods

| Method | Purpose |
|--------|---------|
| `execute(input)` | Primary execution -- receives and returns `PCGDataCollection` |
| `execute_with_context(context, input)` | Execution with PCG context access |
| `point_loop_body(context, data, point, metadata, iteration)` | Per-point processing |
| `variable_loop_body(...)` | Per-point, returns variable number of output points |
| `iteration_loop_body(context, iteration, a, b, metadata)` | Fixed-count iteration |
| `node_title_override()` | Custom display name |
| `node_color_override()` | Custom node color |

### Configurable Properties

```python
element.custom_input_pins    # Array[PCGPinProperties]
element.custom_output_pins   # Array[PCGPinProperties]
element.has_default_in_pin   # bool
element.has_default_out_pin  # bool
element.is_cacheable         # bool
element.requires_game_thread # bool
```

---

## 4. Known Limitations

| Limitation | Details |
|-----------|---------|
| **Editor-only** | No Python in packaged builds or runtime. The node explicitly errors: "Editor-only, should not be used at runtime." |
| **No programmatic node creation** | Python cannot add/connect nodes within a PCG graph programmatically (Epic confirmed, as of 2024) |
| **No data output from Execute Python Script** | The node only provides execution ordering, not PCG data flow |
| **Main thread only** | Python execution blocks the main thread |
| **API churn** | Method names changed between 5.2-5.5 (e.g., `loop_on_points` -> `point_loop`) |
| **Parameter access is finicky** | Setting PCG graph parameters from Python via `ParametersOverrides` requires navigating complex property bags |

## 5. Version History

| UE Version | PCG Status | Python Notes |
|------------|-----------|--------------|
| 5.2 | Experimental | `PCGBlueprintElement`, `PCGComponent` Python API introduced |
| 5.3 | Experimental | `PCGSpatialData` documented, loop API stabilized |
| 5.4 | Beta | `PCGBlueprintHelpers` fully documented |
| 5.5 | Beta | GPU compute path, `PCGGeometryBlueprintElement` added |
| 5.7 | Production-Ready | `PCGPythonInterop` plugin formalized, PCG Editor Mode, ~2x perf |

## 6. Best Practices

- **Use Python for automation**: Batch asset creation, parameter sweeps, CI/CD pipelines
- **Use Blueprint for custom nodes**: More stable API, designer-friendly, works in editor
- **Use C++ for performance**: Multi-threaded, GPU HLSL support, full API access
- **Python + PCG sweet spot**: Triggering generation across many actors, managing seeds, integrating external data (Houdini, numpy), asset migration scripts
