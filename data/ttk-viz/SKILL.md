---
name: ttk-viz
description: >
  Headless topological data analysis and visualization with the Topology ToolKit (TTK) on top of ParaView. Use this skill when Claude needs to:
  (1) Compute and visualize persistence diagrams, contour trees, merge trees, and Morse-Smale segmentations,
  (2) Extract and render critical points of scalar/vector fields,
  (3) Apply persistence-based topological simplification to denoise scalar fields,
  (4) Run TTK filters headlessly via pvpython (loading TTK plugins and using the Scalars_ naming convention).
---

# TTK Headless Topology Visualization

Execute all TTK tasks via self-contained Python scripts run with `pvpython`. Use batch/headless mode — never open a GUI.

TTK extends ParaView with topological analysis filters. Always import `from paraview.simple import *` and ensure TTK plugins are loaded before using TTK filters.

## Rules

1. **Never open a GUI** — always use `pvpython` for headless batch execution
2. Use `from paraview.simple import *` at the top of every script
3. Load TTK plugins explicitly before using TTK filters (see Canonical Template)
4. TTK filters expect the scalar array to be named `Scalars_` — rename on load if needed
5. Always call `UpdatePipeline()` after filters before accessing data information
6. After taking a screenshot, use the Read tool to view the image and verify correctness
7. For visual matching tasks, iterate: screenshot → assess → adjust → re-screenshot (max 5 rounds)
8. Use `pvpython` (not `python`) to run scripts

## Canonical Script Template

```python
from paraview.simple import *

# Load TTK plugins (required before using any TTK filter)
LoadPlugin("TopologyToolKit", remote=False, ns=globals())

# ============= Load Data =============
reader = XMLImageDataReader(FileName=['/path/to/data.vti'])
reader.PointArrayStatus = ['array_name']
reader.UpdatePipeline()

# Rename to standard name expected by TTK filters
rename = RenameArrays(Input=reader)
rename.PointArrays = ['array_name', 'Scalars_']
rename.UpdatePipeline()

# ============= TTK Filters =============
# (see sections below)

# ============= Render View =============
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.Background = [0.1, 0.1, 0.15]

layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# ============= Display =============
display = Show(rename, renderView)
ResetCamera(renderView)

# ============= Save Output =============
SaveScreenshot('/path/to/output.png', renderView,
               ImageResolution=[1920, 1080],
               OverrideColorPalette='WhiteBackground')
```

---

## Loading Data

```python
# VTI (VTK Image Data — standard for TTK scalar/vector/tensor fields)
reader = XMLImageDataReader(FileName=['/path/to/field.vti'])
reader.PointArrayStatus = ['Pressure']   # activate desired arrays
reader.TimeArray = 'None'
reader.UpdatePipeline()

# Rename to convention TTK expects
rename = RenameArrays(Input=reader)
rename.PointArrays = ['Pressure', 'Scalars_']   # [old_name, new_name, ...]
rename.UpdatePipeline()

# For vector fields (2D), rename components to 'u' and 'v'
rename = RenameArrays(Input=reader)
rename.PointArrays = ['velocity_x', 'u', 'velocity_y', 'v']

# VTU / PVTU (unstructured grids)
reader = XMLPartitionedUnstructuredGridReader(FileName=['/path/to/data.pvtu'])

# PVD (time series)
reader = PVDReader(FileName='/path/to/timeseries.pvd')
```

### Get Data Range

```python
reader.UpdatePipeline()
pd = reader.PointData
min_val, max_val = pd.GetArray('Scalars_').GetRange()

bounds = reader.GetDataInformation().GetBounds()
center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]
```

---

## TTK Filters

### Persistence Diagram

```python
# Computes persistence diagram of a scalar field
pd_filter = TTKPersistenceDiagram(Input=rename)
pd_filter.ScalarField = ['POINTS', 'Scalars_']
pd_filter.InputOffsetField = ['POINTS', 'Scalars_']
pd_filter.Backend = 'FTM (IEEE TPDS 2019)'
pd_filter.UpdatePipeline()

# Get persistence pairs range
pd_data = pd_filter.PointData
# PersistenceDiagram output arrays: 'ttkVertexScalarField', 'CriticalType',
#   'Persistence', 'Birth', 'IsFinite', 'PairIdentifier', 'PairType', 'Coordinates'

# Visualize as spheres (birth-death pairs)
spheres = TTKIcospheresFromPoints(Input=pd_filter)
spheres.Radius = 0.02   # as fraction of data range
sphereDisplay = Show(spheres, renderView)
ColorBy(sphereDisplay, ('POINTS', 'Persistence'))
sphereDisplay.RescaleTransferFunctionToDataRange(True)

# Visualize connecting arcs (surface of pd_filter → tubes)
surf = ExtractSurface(Input=pd_filter)
tube = Tube(Input=surf)
tube.Radius = 0.01
Show(tube, renderView)
```

### Contour Tree

```python
# Computes the contour tree (join+split tree merged) of a scalar field
ct = TTKContourTree(Input=rename)
ct.ScalarField = ['POINTS', 'Scalars_']
ct.InputOffsetField = ['POINTS', 'Scalars_']
ct.UpdatePipeline()

# Output ports:
#   Port 0: tree nodes (vertices — critical points)
#   Port 1: tree edges (arcs connecting critical points)
ct_nodes = OutputPort(ct, 0)
ct_edges = OutputPort(ct, 1)

# Visualize nodes as spheres
spheres = TTKIcospheresFromPoints(Input=ct_nodes)
spheres.Radius = 0.5
sphereDisplay = Show(spheres, renderView)
# Color by CriticalType: 0=min, 1=1-saddle, 2=2-saddle, 3=max, 4=degenerate
ColorBy(sphereDisplay, ('POINTS', 'CriticalType'))

# Visualize edges as tubes
surf = ExtractSurface(Input=ct_edges)
tube = Tube(Input=surf)
tube.Radius = 0.1
Show(tube, renderView)

# Apply custom discrete color map for CriticalType
lut = GetColorTransferFunction('CriticalType')
# [value, R, G, B, ...] — minima=blue, 1-saddle=light blue,
#                          2-saddle=pink, maxima=red, degenerate=black
lut.RGBPoints = [
    0, 0.0, 0.188, 1.0,
    1, 0.459, 0.561, 1.0,
    2, 1.0, 0.871, 0.906,
    3, 1.0, 0.0, 0.275,
    4, 0.0, 0.0, 0.0,
]
lut.ColorSpace = 'RGB'
lut.ScalarRangeInitialized = 1.0
sphereDisplay.LookupTable = lut
```

### Merge Tree (Join or Split)

```python
# Join tree: tracks minima as scalar grows
join = TTKMergeTree(Input=rename)
join.ScalarField = ['POINTS', 'Scalars_']
join.InputOffsetField = ['POINTS', 'Scalars_']
# join.TreeType is 'Join Tree' by default

# Split tree: tracks maxima as scalar grows
split = TTKMergeTree(Input=rename)
split.ScalarField = ['POINTS', 'Scalars_']
split.InputOffsetField = ['POINTS', 'Scalars_']
split.TreeType = 'Split Tree'

# Visualize exactly like contour tree (ports 0=nodes, 1=edges)
```

### Scalar Field Critical Points

```python
cp = TTKScalarFieldCriticalPoints(Input=rename)
cp.ScalarField = ['POINTS', 'Scalars_']
cp.InputOffsetField = ['POINTS', 'Scalars_']
cp.UpdatePipeline()
# Output: point cloud with 'CriticalType' array
# CriticalType values: 0=min, 1=1-saddle, 2=2-saddle, 3=max, 4=degenerate

# Visualize all critical points as spheres
spheres = TTKIcospheresFromPoints(Input=cp)
spheres.Radius = 0.3
cpDisplay = Show(spheres, renderView)
ColorBy(cpDisplay, ('POINTS', 'CriticalType'))

# Filter to specific type (e.g., only minima = type 0)
thresh = Threshold(Input=cp)
thresh.Scalars = ['POINTS', 'CriticalType']
thresh.ThresholdMethod = 'Between'
thresh.LowerThreshold = 0        # 0=minima only
thresh.UpperThreshold = 0
minSpheres = TTKIcospheresFromPoints(Input=thresh)
minSpheres.Radius = 0.3
Show(minSpheres, renderView)
```

### Topological Simplification by Persistence

```python
# Remove topological noise below a persistence threshold
# PersistenceThreshold is a fraction of the function range (0-1) unless
# ThresholdIsAbsolute = 1, which switches it to scalar-field units
simplified = TTKTopologicalSimplificationByPersistence(Input=rename)
simplified.InputArray = ['POINTS', 'Scalars_']
simplified.PersistenceThreshold = 0.1   # 10% of scalar range
simplified.UpdatePipeline()

# 'simplified' outputs the same grid with a simplified Scalars_ field
# Use it as input to downstream TTK filters for denoised analysis
ct = TTKContourTree(Input=simplified)
ct.ScalarField = ['POINTS', 'Scalars_']
```

### Morse-Smale Segmentation

```python
# TTKPathCompression computes the Morse-Smale complex segmentation
# Each cell is assigned a region label in 'Scalars__MorseSmaleManifold'
msc = TTKPathCompression(Input=rename)
msc.ScalarField = ['POINTS', 'Scalars_']
msc.OffsetField = ['POINTS', 'Scalars_']
msc.UpdatePipeline()

# Visualize segmentation (for 2D data, Slice representation is ideal)
display = Show(msc, renderView, 'UniformGridRepresentation')
display.Representation = 'Slice'
ColorBy(display, ('POINTS', 'Scalars__MorseSmaleManifold'))
display.RescaleTransferFunctionToDataRange(True)
```

### TTK Icospheres from Points

```python
# Generates sphere geometry centered at each input point
# Used to visualize critical points, tree nodes, persistence pairs, etc.
spheres = TTKIcospheresFromPoints(Input=point_data)
spheres.Radius = 0.5   # world-space radius
```

---

## Render View & Camera

```python
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.Background = [0.1, 0.1, 0.15]

layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Fit everything in view
ResetCamera(renderView)

# Manual camera
renderView.CameraPosition = [cx + d, cy, cz]
renderView.CameraFocalPoint = [cx, cy, cz]
renderView.CameraViewUp = [0, 0, 1]

SaveScreenshot('/path/to/output.png', renderView,
               ImageResolution=[1920, 1080],
               OverrideColorPalette='WhiteBackground')
```

---

## Color Transfer Functions

```python
# Continuous colormap (e.g., scalar field)
lut = GetColorTransferFunction('Scalars_')
lut.ApplyPreset('Cool to Warm', True)
# Or manually:
lut.RGBPoints = [min_val, 0.0, 0.0, 1.0,
                 (min_val+max_val)/2, 1.0, 1.0, 1.0,
                 max_val, 1.0, 0.0, 0.0]
lut.ScalarRangeInitialized = 1.0

# Discrete colormap for CriticalType (5 types: 0–4)
lut = GetColorTransferFunction('CriticalType')
lut.RGBPoints = [
    0, 0.0,   0.188, 1.0,   # minima — blue
    1, 0.459, 0.561, 1.0,   # 1-saddle — light blue
    2, 1.0,   0.871, 0.906, # 2-saddle — pink
    3, 1.0,   0.0,   0.275, # maxima — red
    4, 0.0,   0.0,   0.0,   # degenerate — black
]
lut.ColorSpace = 'RGB'
lut.ScalarRangeInitialized = 1.0

# Discrete colormap for vector critical point types (6 types: 0–5)
# 0=source, 1=saddle, 2=sink, 3=source spiral, 4=center, 5=sink spiral
lut = GetColorTransferFunction('CriticalType')
lut.RGBPoints = [
    0, 0.616, 0.173, 0.0,
    1, 0.941, 0.773, 0.443,
    2, 0.043, 0.506, 0.635,
    3, 0.886, 0.341, 0.349,
    4, 0.494, 0.278, 0.580,
    5, 0.349, 0.659, 0.612,
]
lut.ColorSpace = 'RGB'
lut.ScalarRangeInitialized = 1.0

# Scalar bar
colorBar = GetScalarBar(lut, renderView)
colorBar.Title = 'CriticalType'
colorBar.Visibility = 1
```

---

## Outline & Background

```python
# Draw a bounding box outline around the data
outline = Outline(Input=rename)
outlineDisplay = Show(outline, renderView)
outlineDisplay.DiffuseColor = [0.5, 0.5, 0.5]

# Thin tube for a cleaner outline
tube = Tube(Input=outline)
tube.Radius = max_dimension * 0.0025
Show(tube, renderView)
```

---

## Common Workflow Patterns

### Persistence Diagram Visualization

```python
from paraview.simple import *
LoadPlugin("TopologyToolKit", remote=False, ns=globals())

reader = XMLImageDataReader(FileName=['/path/to/field.vti'])
reader.PointArrayStatus = ['density']
reader.UpdatePipeline()

rename = RenameArrays(Input=reader)
rename.PointArrays = ['density', 'Scalars_']
rename.UpdatePipeline()

min_val, max_val = rename.PointData.GetArray('Scalars_').GetRange()
data_range = max_val - min_val

pd_filter = TTKPersistenceDiagram(Input=rename)
pd_filter.ScalarField = ['POINTS', 'Scalars_']
pd_filter.InputOffsetField = ['POINTS', 'Scalars_']
pd_filter.UpdatePipeline()

renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Spheres for birth-death pairs, sized relative to data range
spheres = TTKIcospheresFromPoints(Input=pd_filter)
spheres.Radius = data_range * 0.02
sDisp = Show(spheres, renderView)
ColorBy(sDisp, ('POINTS', 'Persistence'))
sDisp.RescaleTransferFunctionToDataRange(True)

# Tubes for arcs
surf = ExtractSurface(Input=pd_filter)
tube = Tube(Input=surf)
tube.Radius = data_range * 0.01
Show(tube, renderView)

ResetCamera(renderView)
SaveScreenshot('/path/to/pd.png', renderView, ImageResolution=[1920, 1080])
```

### Contour Tree with Simplified Input

```python
from paraview.simple import *
LoadPlugin("TopologyToolKit", remote=False, ns=globals())

reader = XMLImageDataReader(FileName=['/path/to/field.vti'])
reader.PointArrayStatus = ['pressure']
rename = RenameArrays(Input=reader)
rename.PointArrays = ['pressure', 'Scalars_']
rename.UpdatePipeline()

min_val, max_val = rename.PointData.GetArray('Scalars_').GetRange()
data_range = max_val - min_val   # used below for glyph radii, not for the threshold

# Remove noise below 5% persistence
simplified = TTKTopologicalSimplificationByPersistence(Input=rename)
simplified.InputArray = ['POINTS', 'Scalars_']
simplified.PersistenceThreshold = 0.05

ct = TTKContourTree(Input=simplified)
ct.ScalarField = ['POINTS', 'Scalars_']
ct.InputOffsetField = ['POINTS', 'Scalars_']
ct.UpdatePipeline()

renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Background scalar field
fieldDisplay = Show(rename, renderView, 'UniformGridRepresentation')
fieldDisplay.Representation = 'Slice'
ColorBy(fieldDisplay, ('POINTS', 'Scalars_'))
lut = GetColorTransferFunction('Scalars_')
lut.ApplyPreset('Cool to Warm', True)
fieldDisplay.RescaleTransferFunctionToDataRange(True)
fieldDisplay.Opacity = 0.4

# Tree nodes as spheres
spheres = TTKIcospheresFromPoints(Input=OutputPort(ct, 0))
spheres.Radius = 0.01 * data_range
ctNodeDisp = Show(spheres, renderView)
ctLut = GetColorTransferFunction('CriticalType')
ctLut.RGBPoints = [
    0, 0.0, 0.188, 1.0,    # min
    1, 0.459, 0.561, 1.0,  # 1-saddle
    2, 1.0, 0.871, 0.906,  # 2-saddle
    3, 1.0, 0.0, 0.275,    # max
    4, 0.0, 0.0, 0.0,      # degenerate
]
ctLut.ScalarRangeInitialized = 1.0
ctNodeDisp.LookupTable = ctLut
ctNodeDisp.ColorArrayName = ['POINTS', 'CriticalType']

# Tree edges as tubes
surf = ExtractSurface(Input=OutputPort(ct, 1))
tube = Tube(Input=surf)
tube.Radius = 0.005 * data_range
Show(tube, renderView)

ResetCamera(renderView)
SaveScreenshot('/path/to/ct.png', renderView, ImageResolution=[1920, 1080])
```

### Critical Points Overlay on Scalar Field

```python
from paraview.simple import *
LoadPlugin("TopologyToolKit", remote=False, ns=globals())

reader = XMLImageDataReader(FileName=['/path/to/field.vti'])
reader.PointArrayStatus = ['temperature']
rename = RenameArrays(Input=reader)
rename.PointArrays = ['temperature', 'Scalars_']
rename.UpdatePipeline()

bounds = rename.GetDataInformation().GetBounds()
max_dim = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])

renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Scalar field background
fieldDisp = Show(rename, renderView, 'UniformGridRepresentation')
fieldDisp.Representation = 'Slice'
ColorBy(fieldDisp, ('POINTS', 'Scalars_'))
GetColorTransferFunction('Scalars_').ApplyPreset('Viridis (matplotlib)', True)
fieldDisp.RescaleTransferFunctionToDataRange(True)

# All critical points
cp = TTKScalarFieldCriticalPoints(Input=rename)
cp.ScalarField = ['POINTS', 'Scalars_']
cp.InputOffsetField = ['POINTS', 'Scalars_']
cp.UpdatePipeline()

spheres = TTKIcospheresFromPoints(Input=cp)
spheres.Radius = max_dim * 0.01
cpDisp = Show(spheres, renderView)

lut = GetColorTransferFunction('CriticalType')
lut.RGBPoints = [
    0, 0.0, 0.188, 1.0,
    1, 0.459, 0.561, 1.0,
    2, 1.0, 0.871, 0.906,
    3, 1.0, 0.0, 0.275,
    4, 0.0, 0.0, 0.0,
]
lut.ScalarRangeInitialized = 1.0
cpDisp.LookupTable = lut
cpDisp.ColorArrayName = ['POINTS', 'CriticalType']

ResetCamera(renderView)
SaveScreenshot('/path/to/cp.png', renderView, ImageResolution=[1920, 1080])
```

### Morse-Smale Segmentation

```python
from paraview.simple import *
LoadPlugin("TopologyToolKit", remote=False, ns=globals())

reader = XMLImageDataReader(FileName=['/path/to/field.vti'])
reader.PointArrayStatus = ['elevation']
rename = RenameArrays(Input=reader)
rename.PointArrays = ['elevation', 'Scalars_']
rename.UpdatePipeline()

msc = TTKPathCompression(Input=rename)
msc.ScalarField = ['POINTS', 'Scalars_']
msc.OffsetField = ['POINTS', 'Scalars_']
msc.UpdatePipeline()

renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

display = Show(msc, renderView, 'UniformGridRepresentation')
display.Representation = 'Slice'
ColorBy(display, ('POINTS', 'Scalars__MorseSmaleManifold'))
display.RescaleTransferFunctionToDataRange(True)

ResetCamera(renderView)
SaveScreenshot('/path/to/msc.png', renderView, ImageResolution=[1920, 1080])
```

---

## Export

```python
# Export tree nodes/edges
SaveData('/path/to/tree_nodes.vtk', proxy=OutputPort(ct, 0))
SaveData('/path/to/tree_edges.vtk', proxy=OutputPort(ct, 1))

# Export critical points
SaveData('/path/to/critical_points.vtk', proxy=cp)

# Export Morse-Smale segmentation (preserves grid + MSC array)
SaveData('/path/to/msc.vti', proxy=msc)

# Export persistence diagram
SaveData('/path/to/pd.vtk', proxy=pd_filter)
```

---

## Debugging & Error Handling

| Problem | Solution |
|---------|----------|
| `TTKPersistenceDiagram` not found | Call `LoadPlugin("TopologyToolKit", ...)` before any TTK filter — a bare filename is matched against registered plugin *names* and never resolves |
| TTK filter returns empty output | Check `UpdatePipeline()` was called; verify `ScalarField` array name is `Scalars_` |
| Array not found in filter | Use `RenameArrays` to rename input array to `Scalars_` before passing to TTK |
| Empty spheres / no geometry | `TTKIcospheresFromPoints` needs non-empty point input — check upstream filter output |
| Blank screenshot | Call `ResetCamera(renderView)` before `SaveScreenshot` |
| Wrong output port | Use `OutputPort(filter, 0)` for nodes, `OutputPort(filter, 1)` for edges (contour/merge tree) |
| `pvpython` not found | Add `$PARAVIEW_HOME/bin` to PATH or use full path |
| Plugin already loaded warning | Safe to ignore; TTK is loaded |

---

## Key Array Name Reference

| Source | Array Name | Values |
|--------|-----------|--------|
| After `RenameArrays` | `Scalars_` | Raw scalar values |
| `TTKScalarFieldCriticalPoints` | `CriticalType` | 0=min, 1=1-saddle, 2=2-saddle, 3=max, 4=degenerate |
| `TTKContourTree` (nodes port) | `CriticalType`, `Scalar`, `NodeId` | See above |
| `TTKPersistenceDiagram` | `Persistence`, `Birth`, `CriticalType`, `PairType` | — |
| `TTKPathCompression` | `Scalars__MorseSmaleManifold` | Region label integers |

---

## Task Execution

When given $ARGUMENTS:
1. Parse the task from the arguments
2. Write a self-contained Python script following the template above
3. Execute it with `pvpython script.py` (or `$PARAVIEW_HOME/bin/pvpython script.py`)
4. Read the output image with the Read tool to verify correctness
5. If the result needs adjustment, iterate (max 5 rounds)
6. Report the result to the user
