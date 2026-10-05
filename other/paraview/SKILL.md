---
name: paraview
description: >
  ParaView scientific visualization for volume data and meshes. Use this skill when Claude needs to:
  (1) Visualize 3D volume data (CT, MRI, scientific simulations), (2) Create isosurfaces, slices, volume renderings,
  (3) Visualize vector fields with streamlines/glyphs, (4) Generate publication-quality screenshots,
  (5) Work with VTK, EXODUS, RAW, or other scientific data formats
---

# ParaView Scientific Visualization

> **API Documentation Version: 5.12.1** (ParaView has since released 6.0 and 6.1; this reference has not been re-verified against them)
>
> This skill's API reference is based on ParaView 5.12.1. If you're using a different version, some functions may not be available or behave differently. Notably, **ParaView 6.0** replaced the boolean `UseGradientBackground`/`UseTexturedBackground`/`UseSkyboxBackground` render-view properties with a single `BackgroundColorMode` enum — the simple `renderView.Background = [r, g, b]` calls in this skill are unaffected, but code touching those boolean flags directly will need updating.
>
> Check version: `from paraview.simple import GetParaViewVersion; print(GetParaViewVersion())`

## Rules

1. **Never open a GUI** — always use `pvpython` for headless batch execution
2. Use `from paraview.simple import *` at the top of every script
3. Always call `UpdatePipeline()` after loading EXODUS/IOSS files before accessing data information
4. Always call `ResetCamera(renderView)` before `SaveScreenshot` to ensure all data is in frame
5. Prerequisites assumed: `pvpython` available on PATH (or `$PARAVIEW_HOME/bin/pvpython`)
6. For visual matching tasks, iterate with: screenshot → assess → adjust → re-screenshot
7. After taking a screenshot, use the Read tool to view the image and verify correctness
8. Use `pvpython` (not `python`) to run ParaView scripts
9. Optimize color/opacity mapping first; change camera only when well-motivated

---

## Workflow Decision Tree

### Interactive Visualization (GUI)
Use the **Opening ParaView GUI** section to launch ParaView with pvserver

### Batch Processing (Script Generation)
1. Generate a ParaView Python script following examples
2. Execute with pvpython: `$PARAVIEW_HOME/bin/pvpython script.py`

---

## Opening ParaView GUI

> **Known limitation:** the pvserver↔client connection below relies on a synchronization mechanism that upstream ParaView has deprecated in recent versions. On current ParaView releases this can cause the GUI to not display pvserver content correctly, or general instability. Prefer the headless `pvpython` batch workflow (Rule 1) whenever possible; only fall back to this GUI path when interactive inspection is truly required, and expect to troubleshoot connection issues.

When the user says "Open ParaView GUI" or requests to launch ParaView:

1. Start pvserver first:
   ```bash
   $PARAVIEW_HOME/bin/pvserver --server-port=11111 --multi-clients &
   ```

2. Launch ParaView GUI with auto-connect:
   ```bash
   $PARAVIEW_HOME/bin/paraview --server-url=cs://localhost:11111 &
   ```

---

## Canonical Script Template

```python
from paraview.simple import *

# ============= Configuration =============
INPUT_FILE = '/path/to/input.vtk'
OUTPUT_FILE = '/path/to/screenshot.png'
IMAGE_SIZE = [1920, 1080]

# ============= Load Data =============
data = LegacyVTKReader(FileNames=[INPUT_FILE])
# data = IOSSReader(FileName=[INPUT_FILE])
# data.UpdatePipeline()  # Required for EXODUS

# ============= Get Data Info =============
bounds = data.GetDataInformation().GetBounds()
center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]

# ============= Create Filters =============
# Add your filters here (Contour, Slice, Clip, StreamTracer, Glyph, etc.)

# ============= Create View =============
renderView = CreateView('RenderView')
renderView.ViewSize = IMAGE_SIZE
renderView.Background = [0.1, 0.1, 0.15]

layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# ============= Display =============
display = Show(data, renderView)
# Configure display properties

# ============= Save Output =============
ResetCamera(renderView)
SaveScreenshot(OUTPUT_FILE, renderView,
               ImageResolution=IMAGE_SIZE,
               OverrideColorPalette='WhiteBackground')
```

---

## Core Operations

### Loading Data

```python
from paraview.simple import *

# Auto-detect file type
data = OpenDataFile('path/to/file.vtk')

# VTK Legacy files
data = LegacyVTKReader(FileNames=['path/to/file.vtk'])

# EXODUS files (must UpdatePipeline before accessing bounds)
data = IOSSReader(FileName=['path/to/file.ex2'])
data.UpdatePipeline()

# RAW volume files (parse dimensions from filename like data_256x256x256_uint8.raw)
reader = ImageReader(FileNames=['path/to/file.raw'])
reader.DataExtent = [0, 255, 0, 255, 0, 255]  # dims - 1
reader.DataScalarType = 'unsigned char'  # uint8/uint16/float32
reader.DataByteOrder = 'LittleEndian'
reader.FileDimensionality = 3
reader.NumberOfScalarComponents = 1
reader.UpdatePipeline()
```

### Get Data Information

```python
source = GetActiveSource()

# Get bounds
bounds = source.GetDataInformation().GetBounds()
# Returns: [xmin, xmax, ymin, ymax, zmin, zmax]

# Get array range
pd = source.PointData
min_val, max_val = pd.GetArray('fieldName').GetRange()
# Or by index: pd.GetArray(0).GetRange()

# Calculate center
center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]
```

### Volume Rendering

```python
# Get data range
source = GetActiveSource()
pd = source.PointData
min_val, max_val = pd.GetArray(0).GetRange()

# Color transfer function
lut = GetColorTransferFunction('fieldName')
lut.RGBPoints = [min_val, 0.0, 0.0, 0.75,      # blue at min
                 (min_val + max_val)/2, 0.75, 0.75, 0.75,  # gray at mid
                 max_val, 0.75, 0.0, 0.0]      # red at max

# Opacity transfer function
# Format: [value, opacity, midpoint, sharpness, ...]
pwf = GetOpacityTransferFunction('fieldName')
pwf.Points = [min_val, 0.0, 0.5, 0.0,
              (min_val + max_val)/2, 0.5, 0.5, 0.0,
              max_val, 1.0, 0.5, 0.0]

# Display as volume
display = Show(source, renderView)
display.Representation = 'Volume'
display.ColorArrayName = ['POINTS', 'fieldName']
display.LookupTable = lut
display.ScalarOpacityFunction = pwf
```

### Isosurfaces (Contours)

```python
contour = Contour(Input=source)
contour.ContourBy = ['POINTS', 'fieldName']
contour.Isosurfaces = [0.5]  # Single or multiple isovalues: [0.3, 0.5, 0.7]
contour.PointMergeMethod = 'Uniform Binning'
Show(contour, renderView)
```

### Multiple Contour Lines (sampled range)

```python
import numpy as np

# Linear spacing
contour_values = np.linspace(min_val, max_val, 8).tolist()
# Log spacing (requires min_val > 0)
# contour_values = np.logspace(np.log10(min_val), np.log10(max_val), 8).tolist()

contour = Contour(Input=source)
contour.ContourBy = ['POINTS', 'fieldName']
contour.Isosurfaces = contour_values
display = Show(contour, renderView)
display.Opacity = 0.6
```

### Slices

```python
slice_filter = Slice(Input=source)
slice_filter.SliceType = 'Plane'
slice_filter.SliceType.Origin = [x, y, z]  # or use data center
slice_filter.SliceType.Normal = [0, 0, 1]  # slice normal
Show(slice_filter, renderView)
```

### Clip

```python
clip = Clip(Input=source)
clip.ClipType = 'Plane'
clip.ClipType.Origin = [0.0, 0.0, 0.0]
clip.ClipType.Normal = [1.0, 0.0, 0.0]
clip.InsideOut = False  # Flip which side to keep
Show(clip, renderView)
```

### Threshold

```python
thresh = Threshold(Input=source)
thresh.Scalars = ['POINTS', 'fieldName']
thresh.ThresholdRange = [min_value, max_value]
Show(thresh, renderView)
```

### Streamlines

```python
# Get bounds for seed placement
bounds = source.GetDataInformation().GetBounds()
center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]

# Create stream tracer
tracer = StreamTracer(Input=source, SeedType='Point Cloud')
tracer.Vectors = ['POINTS', 'vectorField']
tracer.IntegrationDirection = 'BOTH'  # 'FORWARD', 'BACKWARD', 'BOTH'
tracer.MaximumStreamlineLength = 50.0
tracer.SeedType.Center = center
tracer.SeedType.NumberOfPoints = 100
tracer.SeedType.Radius = 1.0

# Add tubes for visibility
tube = Tube(Input=tracer)
tube.Radius = 0.1
tubeDisplay = Show(tube, renderView)
ColorBy(tubeDisplay, ('POINTS', 'scalarField'))
```

### Glyphs

```python
# GlyphType options: 'Arrow', 'Cone', 'Sphere', 'Cylinder', 'Line'
glyph = Glyph(Input=source, GlyphType='Arrow')
glyph.OrientationArray = ['POINTS', 'vectorField']
glyph.ScaleArray = ['POINTS', 'vectorField']  # scale by vector magnitude
glyph.ScaleFactor = 0.05
glyph.MaximumNumberOfSamplePoints = 5000     # limit density
glyphDisplay = Show(glyph, renderView)
ColorBy(glyphDisplay, ('POINTS', 'vectorField'))
```

### Warp By Vector

```python
warp = WarpByVector(Input=source)
warp.Vectors = ['POINTS', 'displacementField']
warp.ScaleFactor = 1.0
Show(warp, renderView)
```

### Calculator (Derived Field)

```python
# Create a new field from an expression
calc = Calculator(Input=source)
calc.ResultArrayName = 'velocity_mag'
calc.Function = 'sqrt(velocity_X^2 + velocity_Y^2 + velocity_Z^2)'
calc.AttributeType = 'Point Data'  # or 'Cell Data'
Show(calc, renderView)
```

### Transform (Translate / Rotate / Scale)

```python
t = Transform(Input=source)
t.Transform = 'Transform'
t.Transform.Translate = [dx, dy, dz]
t.Transform.Rotate = [rx, ry, rz]   # degrees
t.Transform.Scale = [sx, sy, sz]
Show(t, renderView)
```

### Gradient & Field Analysis

```python
# Gradient (scalar or vector field)
grad = GradientOfUnstructuredDataSet(Input=source)
grad.SelectInputScalars = ['POINTS', 'pressure']
grad.ComputeVorticity = True    # only meaningful for vector input
grad.ComputeDivergence = True   # only meaningful for vector input
grad.ComputeQCriterion = True   # Q-criterion for vortex identification
Show(grad, renderView)

# Connectivity (label connected regions)
conn = ConnectivityFilter(Input=source)
Show(conn, renderView)
```

### Delaunay Triangulation (Points to Surface)

```python
# alpha=0 → convex hull; alpha>0 → only tetrahedra within alpha radius
delaunay = Delaunay3D(Input=points)
delaunay.Alpha = 0.0
delaunay.Offset = 2.0
delaunay.Tolerance = 0.001
display = Show(delaunay, renderView)
display.SetRepresentationType('Wireframe')   # Wireframe shows mesh structure clearly
```

### Plot Over Line (Line Probe)

```python
plot = PlotOverLine(Input=source)
plot.Point1 = [x1, y1, z1]
plot.Point2 = [x2, y2, z2]
plot.Resolution = 100

# Display in a separate XY chart view
chartView = CreateView('XYChartView')
Show(plot, chartView, 'XYChartRepresentation')
AssignViewToLayout(view=chartView)
```

---

## Render View Setup

```python
# Create view
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.Background = [0.1, 0.1, 0.15]  # RGB background

# Create layout
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Camera for isometric view
renderView.CameraPosition = [3.86, 3.86, 3.86]
renderView.CameraViewUp = [-0.408, 0.816, -0.408]

# Camera for +X direction view
renderView.CameraPosition = [center[0] - 1.5*max_dim, center[1], center[2]]
renderView.CameraFocalPoint = center
renderView.CameraViewUp = [0.0, 0.0, 1.0]

# Reset camera to fit all data
ResetCamera(renderView)

# Save screenshot
SaveScreenshot('output.png', renderView, ImageResolution=[1920, 1080],
               OverrideColorPalette='WhiteBackground')
```

---

## Display Properties

```python
display = GetDisplayProperties(source, renderView)

# Representation types
display.SetRepresentationType('Surface')
# Options: 'Surface', 'Surface With Edges', 'Wireframe', 'Points', 'Volume', 'Outline'

# Color by array
ColorBy(display, ('POINTS', 'fieldName'))  # or ('CELLS', 'fieldName')
display.RescaleTransferFunctionToDataRange(True)

# Solid color
ColorBy(display, None)
display.DiffuseColor = [1.0, 0.0, 0.0]  # RGB

# Opacity
display.Opacity = 0.5  # 0.0 to 1.0

# Visibility
display.Visibility = 1  # 1=visible, 0=hidden
```

---

## Color Map Presets

```python
from paraview.simple import ApplyPreset

lut = GetColorTransferFunction('fieldName')
ApplyPreset(lut, 'Cool to Warm', True)

# Available presets:
# 'Blue-Red', 'Cool to Warm', 'Viridis', 'Plasma', 'Magma', 
# 'Inferno', 'Rainbow', 'Grayscale'
```

---

## Scalar Bar (Color Legend)

```python
lut = GetColorTransferFunction('fieldName')
colorBar = GetScalarBar(lut, renderView)
colorBar.Title = 'Field Name'
colorBar.ComponentTitle = ''
colorBar.Visibility = 1
colorBar.ScalarBarLength = 0.3
```

---

## Complete Example Scripts

### Volume Rendering

```python
from paraview.simple import *

# Load data
data = LegacyVTKReader(FileNames=['/path/to/volume.vtk'])

# Get range
source = GetActiveSource()
pd = source.PointData
min_val, max_val = pd.GetArray(0).GetRange()

# Transfer functions
lut = GetColorTransferFunction('var0')
lut.RGBPoints = [min_val, 0.0, 0.0, 0.75,
                 (min_val + max_val)/2, 0.75, 0.75, 0.75,
                 max_val, 0.75, 0.0, 0.0]

pwf = GetOpacityTransferFunction('var0')
pwf.Points = [min_val, 0.0, 0.5, 0.0,
              (min_val + max_val)/2, 0.5, 0.5, 0.0,
              max_val, 1.0, 0.5, 0.0]

# Create view
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.CameraPosition = [3.86, 3.86, 3.86]
renderView.CameraViewUp = [-0.408, 0.816, -0.408]

layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Display as volume
display = Show(data, renderView)
display.Representation = 'Volume'
display.ColorArrayName = ['POINTS', 'var0']
display.LookupTable = lut
display.ScalarOpacityFunction = pwf

ResetCamera(renderView)
SaveScreenshot('/path/to/dvr.png', renderView, ImageResolution=[1920, 1080])
```

### Streamlines with Tubes

```python
from paraview.simple import *

# Load data
data = IOSSReader(FileName=['/path/to/disk.ex2'])
data.UpdatePipeline()

# Get bounds
bounds = data.GetDataInformation().GetBounds()
center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]
max_dim = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])

# Create stream tracer
tracer = StreamTracer(Input=data, SeedType='Point Cloud')
tracer.Vectors = ['POINTS', 'V']
tracer.MaximumStreamlineLength = 20.0
tracer.SeedType.Center = center
tracer.SeedType.Radius = 2.0

# Add glyphs
glyph = Glyph(Input=tracer, GlyphType='Cone')
glyph.OrientationArray = ['POINTS', 'V']
glyph.ScaleArray = ['POINTS', 'V']
glyph.ScaleFactor = 0.06

# Add tubes
tube = Tube(Input=tracer)
tube.Radius = 0.075

# Create view
renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
renderView.CameraPosition = [center[0] - 1.5*max_dim, center[1], center[2]]
renderView.CameraFocalPoint = center
renderView.CameraViewUp = [0.0, 0.0, 1.0]

layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

# Display
tubeDisplay = Show(tube, renderView)
glyphDisplay = Show(glyph, renderView)
ColorBy(tubeDisplay, ('POINTS', 'Temp'))
ColorBy(glyphDisplay, ('POINTS', 'Temp'))
tubeDisplay.RescaleTransferFunctionToDataRange(True)
glyphDisplay.RescaleTransferFunctionToDataRange(True)

ResetCamera(renderView)
SaveScreenshot('/path/to/streamlines.png', renderView, ImageResolution=[1920, 1080])
```

### RAW Volume File

```python
from paraview.simple import *

# Parse dimensions from filename: tooth_103x94x161_uint8.raw
raw_file = '/path/to/tooth_103x94x161_uint8.raw'

reader = ImageReader(FileNames=[raw_file])
reader.DataScalarType = 'unsigned char'
reader.DataByteOrder = 'LittleEndian'
reader.DataExtent = [0, 102, 0, 93, 0, 160]  # dimensions - 1
reader.FileDimensionality = 3
reader.NumberOfScalarComponents = 1
reader.UpdatePipeline()

# Continue with visualization...
```

### Color Map from JSON File

```python
from paraview.simple import *

data = LegacyVTKReader(FileNames=['/path/to/volume.vtk'])

renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

display = Show(data, renderView)
display.Representation = 'Volume'
display.ColorArrayName = ['POINTS', 'fieldName']

# Load a color map exported from ParaView GUI (.json)
# JSON format: [{"RGBPoints": [v0,r0,g0,b0, v1,r1,g1,b1, ...], "Points": [v,a,0.5,0, ...]}]
import json
with open('/path/to/colormap.json') as f:
    cm = json.load(f)[0]

lut = GetColorTransferFunction('fieldName')
lut.RGBPoints = cm['RGBPoints']      # flat list: [val, R, G, B, val, R, G, B, ...]

if 'Points' in cm:                    # optional opacity
    pwf = GetOpacityTransferFunction('fieldName')
    pwf.Points = cm['Points']         # flat list: [val, alpha, midpoint, sharpness, ...]
    display.ScalarOpacityFunction = pwf

display.LookupTable = lut
ResetCamera(renderView)
SaveScreenshot('/path/to/output.png', renderView, ImageResolution=[1920, 1080])
```

### Export Data

```python
from paraview.simple import *

data = LegacyVTKReader(FileNames=['/path/to/input.vtk'])

# Apply a contour filter to get a surface
contour = Contour(Input=data)
contour.ContourBy = ['POINTS', 'fieldName']
contour.Isosurfaces = [0.5]

# Export as STL (surface mesh)
SaveData('/path/to/output.stl', proxy=contour)

# Export as CSV (point data)
SaveData('/path/to/output.csv', proxy=data)

# Export as VTK binary (full data with arrays)
SaveData('/path/to/output.vtk', proxy=data, DataMode='Binary')

# Export as OBJ / PLY (surface mesh formats)
# SaveData('/path/to/output.obj', proxy=contour)
# SaveData('/path/to/output.ply', proxy=contour)
```

### Save Animation (Time Series)

```python
from paraview.simple import *

# Load a time-varying dataset (e.g., PVD file pointing to a series)
data = OpenDataFile('/path/to/timeseries.pvd')

renderView = CreateView('RenderView')
renderView.ViewSize = [1920, 1080]
layout = CreateLayout(name='Layout')
layout.AssignView(0, renderView)

display = Show(data, renderView)
ColorBy(display, ('POINTS', 'fieldName'))
display.RescaleTransferFunctionToDataRange(True)
ResetCamera(renderView)

# Save animation as image sequence (animation0000.png, animation0001.png, ...)
scene = GetAnimationScene()
scene.PlayMode = 'Snap To TimeSteps'
SaveAnimation('/path/to/animation.png', renderView,
              ImageResolution=[1920, 1080],
              FrameRate=24)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `PARAVIEW_HOME` not set | `export PARAVIEW_HOME=/path/to/ParaView` |
| `pvpython` not found | Add `$PARAVIEW_HOME/bin` to PATH or use full path |
| pvserver not found | Check PARAVIEW_HOME path is correct |
| Port already in use | Use `--port` to specify different port |
| Connection failed | Check firewall, try checking PARAVIEW_HOME status |
| "No active source" | Load data first before applying filters |
| Transfer function not working | Check field name matches array name exactly |
| Blank/empty screenshot | Call `ResetCamera(renderView)` before `SaveScreenshot` |
| Wrong bounds/range | Call `UpdatePipeline()` after loading data (required for EXODUS) |
| `ModuleNotFoundError: paraview` | Run with `pvpython`, not plain `python` |
| `Threshold` field not found | Use `['POINTS', name]` or `['CELLS', name]` to match array location |
| `GradientOfUnstructuredDataSet` fails | Only works on unstructured grids; use `Gradient` for structured data |
| `WarpByVector` produces no output | Check vector field has 3 components; verify field name |
| `PlotOverLine` view blank | Create an `XYChartView` and assign it via `AssignViewToLayout` |
| `SaveAnimation` — no timesteps | Data must have multiple time steps; single-timestep data cannot be animated |
| `SaveData` to STL/OBJ fails | Input must be a surface (PolyData); apply `Contour` or `ExtractSurface` first |

---

## Task Execution

When given $ARGUMENTS:
1. Parse the task from the arguments
2. Write a self-contained Python script following the template above
3. Execute it with `pvpython script.py` (or `$PARAVIEW_HOME/bin/pvpython script.py`)
4. Read the output image with the Read tool to verify correctness
5. If the result needs adjustment, iterate (max 5 rounds)
6. Report the result to the user

---

## Resources

- `references/api-reference-5.12.1.md` - Complete Python API reference (v5.12.1)
- `references/operations.md` - Common operations quick reference
- `references/examples.md` - Complete example scripts
