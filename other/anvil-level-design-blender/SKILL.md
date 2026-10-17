---
name: anvil-level-design-blender
description: Expert in Anvil Level Design Blender addon for Trenchbroom-inspired level design with automated material/UV management and geometry tools
triggers:
  - how do I use Anvil Level Design in Blender
  - set up material application with Anvil addon
  - apply textures automatically in Blender level design
  - create hotspot mapping for texture atlas
  - use Anvil geometry tools for level design
  - configure UV management in Anvil Blender
  - export levels with Anvil Level Design
  - troubleshoot Anvil texture application
---

# Anvil Level Design Blender Addon

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Anvil Level Design (Anvil LD) is a Blender addon combining Trenchbroom-inspired tools for video game level design. It features automated material application and UV management, hotspot mapping for texture atlases, camera and grid tools, geometry operators with backface culling selection, and improved GLB export workflow.

## Installation

**Requirements:**
- Blender 5.1 or higher
- Python (bundled with Blender)

**Installation steps:**

1. Download the repository as ZIP from GitHub
2. In Blender: Edit → Preferences → Add-ons
3. Click the v arrow → Install From Disk
4. Select the downloaded ZIP file
5. Enable the addon in preferences

**Initial setup:**

```python
# Access addon preferences to create workspaces
# Edit → Preferences → Add-ons → Anvil Level Design
# Click "Create Level Design Workspace" and "Create Hotspot Mapping Workspace"
```

The addon adds two custom workspaces:
- **Level Design** - Main workspace for level geometry and texturing
- **Hotspot Mapping** - Workspace for defining texture atlas hotspots

**Custom hotkey remapping:**

All addon hotkeys are collected in addon preferences for easy remapping. Common keys to customize:
- Camera tools
- Texture application tools
- Geometry operators

## Core Concepts

### Material and UV Management Philosophy

Anvil manages materials automatically to prevent duplicates. Materials are applied with automatic UV unwrapping that tiles seamlessly across faces. **Critical**: Do not resize in object mode using scale operator - resize by moving and extruding faces to maintain proper UV coordinates.

### Workspace Requirements

You must be in "Level Design" or "Hotspot Mapping" workspace to use Anvil features. Features are workspace-contextual.

## Key Commands - Material Application

### Basic Texture Application

**Apply texture from file browser:**
```python
# 1. Select a face in Edit mode
# 2. Choose image file in file browser
# Material is created and UV is automatically applied
```

**Copy material between faces:**
- `Alt + Left Mouse` on target face: Apply same material with seamless tiling
- `Alt + Right Mouse` on source face: Pick texture from face (works across objects)

**Stretched material application:**
- `Shift + Alt + Left Mouse`: Apply texture stretched to fit target face dimensions
- `Shift + Alt + Right Mouse`: Pick texture to be stretched

**UV-only operations (no material change):**
- `Ctrl + Alt + Left Mouse`: Apply UV without changing material
- `Ctrl + Alt + Right Mouse`: Pick UV without changing material

### Interactive UV Modes

**Face Snapping UV Mode (`T` key):**
```python
# 1. Select a face
# 2. Press T to enter mode
# 3. Move mouse near edges - texture bottom snaps to closest edge
# 4. WASD keys: Select different texture edges
# 5. Q/E keys: Set FIT modes
# 6. Click to apply
```

**Grid Snapping UV Mode:**
```python
# 1. Select multiple quad faces (single island only)
# 2. Press T
# 3. Snapping applies across entire quad grid
# 4. Same controls as Face Snapping mode
```

**UV Transform Mode (`Shift + T`):**
```python
# 1. Select faces
# 2. Press Shift+T
# 3. Hover over face to set as origin (for multi-face selection)
# 4. Drag handles to move/resize UV with live preview
# 5. Drag resize handle through opposite side to mirror texture (negative Scale U/V)
```

### Material Panel Settings

Access via `N` key → Anvil panel:

```python
# Manual UV adjustments
Scale U/V: 1.0  # At 1.0, pixels_per_meter controls texture size
Rotation: 0.0
Offset U/V: 0.0, 0.0

# Randomize offset: Click refresh icons next to Offset fields

# UV Lock toggle
UV_Lock: True   # Material warps with face adjustments
UV_Lock: False  # Material maintains world space (no stretching on extrusion)
```

**Utility operations:**
- Reset scale, rotation, offset (Face-Aligned project)
- Center material to face
- Fit material to face dimensions

**Material properties:**
```python
# Link transparency channel to shader
# Adjust roughness
# Enable vertex colors
# Premultiply alpha settings

# Fix Alpha Bleed tool: Edits source image to set transparent pixels to color
# Prevents visible edges on transparent cutout materials for GLB export
```

**Default material settings:**
- Panel: Anvil (Settings) - per-file defaults
- Addon Preferences - global defaults for new .blend files

### Material Cleanup

```python
# In Anvil panel
"Cleanup Unused Materials" button  # Removes orphaned materials
```

## Hotspot Mapping System

Hotspot mapping assigns UV coordinates by matching face shapes to predefined regions on a texture atlas. Hotspot UVs are never mirrored - always non-flipped mapping.

### Setting Up Hotspot Maps

**In Hotspot Mapping workspace:**

```python
# 1. Open texture atlas in Image Editor
# 2. Select Hotspot Edit tool (left sidebar)
# 3. Press N → Anvil panel
# 4. Click "Assign Hotspottable" to mark texture as hotspot source
# 5. Add lines in image to split into hotspots
#    - Normal line: Click and drag
#    - Non-grid line: Hold Ctrl + drag
# 6. Resize hotspots by dragging lines
# 7. Use [ and ] keys for pixel snapping
```

**Data storage:**
- Stored in .blend file by default
- Optional external JSON for cross-project sharing

### Hotspot Orientation Types

Click orientation button next to hotspot or icon on hotspot itself to cycle:

```python
Any      # Applies to any face, randomized rotation
Upwards  # Walls only (vertical), texture top points up - for bricks, siding
Floor    # Floor faces only (up-facing), randomized rotation
Ceiling  # Ceiling faces only (down-facing), randomized rotation
```

### Applying Hotspots

**In 3D viewport Anvil panel:**

```python
"Randomise Hotspots" button  # Manual trigger on selected faces (or all if none/object mode)

"Auto Apply Hotspots" toggle  # Auto-apply on geometry edits (moved geometry only)

"Fixed" property  # Toggle on selected faces to prevent randomization

"Choose Hotspot" button  # Manually select a fixed hotspot
```

### Combined Faces & Seam Mode

**Allow Combined Faces:**
```python
# Enabled (default): Algorithm treats connected faces as single face
# - Works on curved/bent face series
# - Attempts to find groups transformable to rectangle
# - Splits islands by normals and user seams

# Disabled: Each face processed individually
```

**Seam Mode:**
```python
"Maintain User Seams"  # Clears auto-seams (appears unchanged to user)
"Display All Seams"    # Shows auto-seams for debugging island detection
"Clear All Seams"      # Removes all seams
```

**Size Weight slider:**
```python
# Default (0.0): Closest aspect ratio match (preserves pixel aspect)
# Increase: Weight towards hotspots matching texel density
# Prevents blurry textures when small hotspots match aspect ratio
```

**Best practices:**
- Create wide variety of aspect ratios and sizes in atlas
- Ensures good hotspot matching on any geometry
- Algorithm doesn't split non-rectangular islands (e.g., L-shapes remain separate faces)

## Geometry Tools

### Selection Tools

**Backface Culling Override:**
```python
# Anvil overrides selection to ignore culled backfaces when not in X-ray mode
# Works with:
# - Box select (single click, Shift-click, Alt-click)
# - Lasso select (single click variants)
# 
# Limitations (Blender API):
# - Does NOT work with box/lasso dragging
# - Does NOT work with circle select or tweak tool
```

**Vertex Paint mode:**
```python
# Automatically enables face orientation if not already on
# Front face orientation color set to transparent in active theme
# Shows which faces cannot be painted through
```

**Paint Select (`Ctrl + Left Mouse`):**
```python
# Similar to circle select but respects backface culling
# Hold and drag to add crossed items to selection
```

**Select Connected:**
```python
L                 # Hover over element: Select all connected elements
Ctrl+L            # Hover over element: Select connected with matching normals
                  # Repeated presses select faces progressively by normal similarity
Ctrl+Shift+L      # Step backward in normal-based selection
Shift+L           # Add connected island to selection
```

### Context Aware Weld (`W` key)

```python
# Press W for context-aware welding
# Action varies based on selection context
# Next weld action flagged in Anvil panel
# Specific behaviors described in relevant README sections
```

### Cube Cut Mode (`C` key in Edit mode)

```python
# Enter cube cut mode
1. Press C in Edit mode
2. Click on face to start drawing
3. Move mouse and click to define rectangular face
4. Move mouse third time to define depth
5. Click third time to make cut

# Behavior:
# - Only affects selected faces (or all if none selected)
# - Drawing rectangle in orthogonal view creates infinite cut
```

### Basic Navigation

```python
Right Mouse Button  # Camera navigation
Tab                # Toggle Object/Edit mode
G                  # Move selection
E                  # Extrude selection
Alt+Click          # Select loops
B                  # Add cubes (works in Object and Edit mode)
L                  # Select connected faces (useful for multi-cube edit mode selections)
```

## Configuration

### Addon Preferences

**Access:** Edit → Preferences → Add-ons → Anvil Level Design

```python
# Workspace creation
"Create Level Design Workspace"
"Create Hotspot Mapping Workspace"

# Hotkey remapping
# All addon hotkeys collected here for convenience

# Default material settings (global for new .blend files)
Default_Pixels_Per_Meter: 100.0
Default_Roughness: 0.5
Default_Transparency_Mode: "OPAQUE"
```

### Per-File Settings

**Anvil (Settings) panel:**
```python
# Default material properties for new textures in current file
Pixels_Per_Meter: 100.0
Roughness: 0.5
Enable_Vertex_Colors: False
Transparency_Settings: {...}
```

## Code Examples

### Python API - Material Application

```python
import bpy

# Access Anvil operators through bpy.ops
def apply_texture_to_selected_face(image_path):
    """Apply texture from file to selected face"""
    # Load image
    img = bpy.data.images.load(image_path)
    
    # Anvil handles material creation and UV application
    # Typically done through UI, but can script:
    obj = bpy.context.active_object
    if obj and obj.mode == 'EDIT':
        # Select face and apply through Anvil operators
        # bpy.ops.anvil.apply_material_from_image()
        pass

def get_anvil_material_settings():
    """Access Anvil material settings"""
    prefs = bpy.context.preferences.addons['anvil-level-design'].preferences
    
    settings = {
        'pixels_per_meter': prefs.default_pixels_per_meter,
        'roughness': prefs.default_roughness,
    }
    return settings

# UV manipulation
def set_uv_scale_rotation(scale_u=1.0, scale_v=1.0, rotation=0.0):
    """Set UV transformation via Anvil properties"""
    obj = bpy.context.active_object
    if obj and obj.mode == 'EDIT':
        # Access Anvil UV properties
        # Properties stored in object/mesh data
        # bpy.ops.anvil.set_uv_transform(scale_u=scale_u, scale_v=scale_v, rotation=rotation)
        pass
```

### Python API - Hotspot Management

```python
import bpy
import json

def create_hotspot_data(image_name, hotspots):
    """Define hotspot data structure"""
    hotspot_data = {
        'image': image_name,
        'hotspots': []
    }
    
    for hs in hotspots:
        hotspot_data['hotspots'].append({
            'bounds': {
                'x_min': hs['x_min'],
                'y_min': hs['y_min'],
                'x_max': hs['x_max'],
                'y_max': hs['y_max']
            },
            'orientation': hs.get('orientation', 'Any'),  # Any, Upwards, Floor, Ceiling
            'name': hs.get('name', '')
        })
    
    return hotspot_data

def export_hotspot_json(data, filepath):
    """Export hotspot data to external JSON"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def apply_random_hotspots():
    """Trigger hotspot randomization on selected faces"""
    # bpy.ops.anvil.randomise_hotspots()
    pass

# Example hotspot definition
example_hotspots = [
    {
        'x_min': 0, 'y_min': 0, 'x_max': 512, 'y_max': 512,
        'orientation': 'Upwards',
        'name': 'brick_wall_01'
    },
    {
        'x_min': 512, 'y_min': 0, 'x_max': 1024, 'y_max': 256,
        'orientation': 'Floor',
        'name': 'floor_tile_01'
    }
]
```

### Python API - Geometry Operations

```python
import bpy

def context_aware_weld():
    """Execute context-aware weld"""
    # bpy.ops.anvil.context_weld()
    pass

def select_connected_by_normal():
    """Select connected faces with matching normals"""
    # bpy.ops.anvil.select_connected_normal()
    pass

def paint_select_setup():
    """Setup for paint select mode"""
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        # Ensure proper selection mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)  # Face mode
```

## Common Patterns

### Level Design Workflow

```python
# 1. Initial geometry blocking
# - Switch to Level Design workspace
# - Enter Edit mode (Tab)
# - Press B to add cubes
# - Use G (move) and E (extrude) to shape level
# - Alt+Click to select loops
# - L to select connected geometry

# 2. Texture application
# - Select face
# - Choose image in file browser (auto-applies material)
# - Alt+Left Mouse on other faces to copy texture
# - Press T for Face Snapping UV Mode to align texture edges
# - Use Shift+T for UV Transform Mode for manual fine-tuning

# 3. Detail with hotspots
# - Create texture atlas
# - Switch to Hotspot Mapping workspace
# - Use Hotspot Edit tool to define regions
# - Set orientation types (Upwards for walls, Floor/Ceiling for horizontals)
# - Back in Level Design workspace, enable Auto Apply Hotspots
# - Create detail geometry - hotspots apply automatically

# 4. Refinement
# - Use Ctrl+L to select by normal
# - Apply specific materials to groups
# - Mark important hotspots as Fixed
# - Manually Choose Hotspot where needed

# 5. Export
# - Use Anvil (Export) panel for GLB export
# - Materials configured for game engine compatibility
```

### Texture Atlas Setup

```python
# Best practices for hotspot atlases:
# 1. Include wide variety of aspect ratios
#    - Square (1:1)
#    - Wide rectangles (4:1, 8:1)
#    - Tall rectangles (1:4, 1:8)
#    - Common ratios (2:1, 3:2)

# 2. Include multiple size variants
#    - Large (1024x1024) for big surfaces
#    - Medium (512x512, 512x256) for common use
#    - Small (256x256, 128x256) for details
#    - This prevents blurry textures from small hotspots

# 3. Organize by orientation
#    - Group wall textures (Upwards orientation)
#    - Group floor textures (Floor orientation)
#    - Group ceiling textures (Ceiling orientation)
#    - Generic details (Any orientation)

# 4. Name hotspots descriptively
#    - Helps when manually choosing fixed hotspots
```

### Material Optimization

```python
# Material management strategy:

# 1. Use single atlas per material type
#    - One atlas for stone/brick
#    - One atlas for metal
#    - One atlas for wood
#    - Reduces material count

# 2. Leverage Anvil's duplicate prevention
#    - Addon automatically merges duplicate materials
#    - Periodically run "Cleanup Unused Materials"

# 3. Configure defaults early
#    - Set Pixels_Per_Meter for project scale
#    - Set default roughness per material type
#    - Configure transparency settings before texturing

# 4. Fix alpha bleed before export
#    - Use Fix Alpha Bleed tool on transparent textures
#    - Or enable premultiply alpha in material settings
#    - Test in target engine
```

## Troubleshooting

### Textures Not Applying Correctly

**Problem:** Alt+Left Mouse doesn't apply texture
```python
# Check:
1. Are you in Level Design workspace?
2. Is face actually selected (orange highlight)?
3. Is object in Edit mode?
4. Try Alt+Right Mouse to pick texture first

# If texture applies but looks wrong:
5. Check UV Lock setting in Anvil panel
6. Verify Scale U/V values (should typically be 1.0 or close)
7. Check if texture is mirrored (negative Scale U/V) - use panel to reset
```

**Problem:** Textures stretch when extruding
```python
# UV Lock is ON
# Solution: Turn UV Lock OFF in Anvil panel for world-space material behavior
# UV Lock ON: Material warps with geometry
# UV Lock OFF: Material maintains world space (preferred for level design)
```

### Hotspot Issues

**Problem:** Hotspots not applying
```python
# Check:
1. Is image marked as "Hotspottable" in Hotspot Mapping workspace?
2. Are hotspot regions properly defined (visible lines in Image Editor)?
3. Does face orientation match hotspot orientation type?
   - Use Shift+Z to toggle wireframe and see face normals
4. Is "Allow Combined Faces" causing unexpected island grouping?
   - Try disabling to process faces individually
```

**Problem:** Wrong hotspots selected
```python
# Issue: Small hotspots chosen, textures blurry
# Solution: Adjust Size Weight slider
#   - Higher values favor hotspots matching texel density
#   - Lower values favor aspect ratio matches only

# Issue: Hotspots randomize on every edit
# Solution: Mark preferred hotspots as Fixed
#   1. Select faces with good hotspots
#   2. Enable "Fixed" property in Anvil panel
```

**Problem:** Hotspots creating seams
```python
# Check Seam Mode setting:
"Maintain User Seams"  # Default, clears auto-seams
"Display All Seams"    # Shows what algorithm sees as islands
"Clear All Seams"      # Nuclear option

# If islands not forming as expected:
1. Switch to "Display All Seams" mode
2. See where algorithm splits geometry
3. Manually add seams where needed
4. Or disable "Allow Combined Faces" for per-face control
```

### Selection Problems

**Problem:** Selecting through geometry
```python
# Backface culling limitations:
1. Turn OFF X-ray mode (Alt+Z) for backface culling to work
2. Use single-click selections, not drag selections
3. Avoid circle select - use Paint Select (Ctrl+Left Mouse) instead
4. Box select and lasso work for clicks, not drags

# For vertex paint:
# Face orientation automatically enabled to show paintable faces
```

**Problem:** Cannot select specific faces
```python
# Use selection modes:
Ctrl+L  # Select by normal - progressively select similar-facing faces
L       # Select all connected
Shift+L # Add island to selection
Alt+Click  # Select loop

# Paint Select for precision:
Ctrl+Left Mouse  # Hold and drag, respects backface culling
```

### Performance Issues

**Problem:** Slow material application
```python
# Too many materials:
1. Use "Cleanup Unused Materials" in Anvil panel regularly
2. Consolidate similar materials to atlases
3. Check material count in Outliner

# Too many faces:
1. Use decimation modifier on detail geometry
2. Merge unnecessary faces
3. Use instancing for repeated elements
```

**Problem:** Hotspot randomization slow
```python
# Large texture atlas:
1. Reduce atlas resolution if possible
2. Reduce number of hotspot regions
3. Disable "Auto Apply Hotspots" during heavy modeling
4. Manually trigger with "Randomise Hotspots" when ready
```

### Export Issues

**Problem:** Transparent materials wrong in GLB
```python
# Alpha bleed visible:
1. Use "Fix Alpha Bleed" tool on source textures
2. Or enable premultiply alpha in material settings
3. Check material blend mode (should be appropriate for engine)

# Missing materials:
1. Verify all materials are assigned in Blender
2. Check Anvil (Export) panel settings
3. Test with simpler material setup first
```

### Workspace Lost

**Problem:** Level Design or Hotspot Mapping workspace missing
```python
# Solution:
1. Edit → Preferences → Add-ons → Anvil Level Design
2. Click "Create Level Design Workspace"
3. Click "Create Hotspot Mapping Workspace"
4. Workspaces appear at top of Blender window
```

### Keyboard Shortcuts Not Working

**Problem:** Hotkeys don't trigger Anvil features
```python
# Check:
1. Are you in correct workspace? (Level Design or Hotspot Mapping)
2. Are you in correct mode? (Object vs Edit mode)
3. Check addon preferences for hotkey conflicts
4. Remap conflicting keys in preferences
5. Verify addon is enabled in preferences
```

## Advanced Configuration

### Custom Hotkey Setup

```python
# Access: Edit → Preferences → Add-ons → Anvil Level Design
# All Anvil hotkeys collected in preferences

# Common remapping:
T         # Face Snapping UV Mode (might conflict with tools)
Shift+T   # UV Transform Mode
C         # Cube Cut (conflicts with circle select)
W         # Context Aware Weld
B         # Add Cube (conflicts with box select in some contexts)

# Consider remapping to:
# - Function keys (F1-F12)
# - Alt+key combinations
# - Numpad keys if not using for view
```

### Performance Tuning

```python
# For large levels:

# 1. Material management
Max_Materials_Before_Warning: 50  # Set lower for cleanup reminders

# 2. Hotspot settings
Size_Weight: 0.3  # Balance quality vs speed
Allow_Combined_Faces: False  # Faster processing, less smart grouping

# 3. Selection settings
Disable paint select if not needed  # Slight performance gain

# 4. UV settings
UV_Lock: False  # Default off for better performance on extrusions
```

### Integration with Version Control

```python
# Hotspot data in external JSON:

# In Hotspot Mapping workspace:
1. Define hotspots on texture atlas
2. Export hotspot data to JSON
3. Commit JSON to version control
4. Team members load same JSON
5. Consistent hotspot behavior across team

# .blend file considerations:
# - Store in Git LFS if using version control
# - Hotspot data embedded by default
# - External JSON optional for sharing
```

## Resources

- **Discord:** https://discord.gg/hHFZbDzR57
- **GitHub:** https://github.com/alexjhetherington/anvil-level-design
- **Example files:** Check `examples/hotspot_tutorial.blend` in repository

## Quick Reference Card

```python
# Material Application
Alt+Left Mouse         # Copy material to face (seamless tiling)
Alt+Right Mouse        # Pick material from face
Shift+Alt+Left Mouse   # Apply stretched to fit
Ctrl+Alt+Left Mouse    # Apply UV only (no material change)

# UV Modes
T                      # Face Snapping UV Mode
Shift+T                # UV Transform Mode
WASD (in UV mode)      # Select texture edges
Q/E (in UV mode)       # FIT modes

# Selection
L                      # Select connected
Ctrl+L                 # Select by normal
Shift+L                # Add island
Ctrl+Left Mouse        # Paint select

# Geometry
B                      # Add cube
C (Edit mode)          # Cube cut
E                      # Extrude
G                      # Move
W                      # Context aware weld

# Navigation
Right Mouse            # Camera
Tab                    # Object/Edit mode
Alt+Click              # Select loop
[ ]                    # Pixel snapping (in Hotspot workspace)
```
