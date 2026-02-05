---
name: fusion360
description: Control Autodesk Fusion 360 CAD software via the Claude Bridge add-in. Create sketches, draw shapes, extrude 3D objects, and build complex models interactively.
---

# Fusion 360 Interactive Control

This skill enables Claude to control Autodesk Fusion 360 through the Claude Bridge add-in. You can create 3D models by sending commands that are automatically executed in Fusion 360.

## Prerequisites

1. **Fusion 360** must be running with a design open
2. **ClaudeBridge add-in** must be active (Shift+S → Add-Ins → ClaudeBridge → Run)

## How It Works

Claude sends commands by writing JSON to:
```
<ClaudeBridge-directory>/commands.json
```

The bridge polls every second and executes commands. Results appear in:
```
<ClaudeBridge-directory>/results.json
```

## Sending Commands

To send a command, write a JSON file with this structure:

```json
{
  "id": <incrementing_number>,
  "action": "<command_name>",
  "params": { <parameters> }
}
```

**Important**: The `id` must be higher than the previous command, or it will be ignored.

## Workflow Pattern

1. **Check the last command ID** by reading `results.json`
2. **Send command** with incremented ID
3. **Read results** to confirm success
4. **Repeat** for next command

## Available Commands

See [reference.md](./reference.md) for the complete API reference.

### Getting Design Data
- `export_session` - **Export all design data to a timestamped folder** (replaces all individual query commands)

### Connection
- `ping` - Test connection
- `message` - Display a message in Fusion 360

### Construction Geometry
- `create_offset_plane` - Create plane at Z offset (for multi-level geometry)
- `create_plane_at_angle` - Create angled construction plane

### Sketch Commands
- `create_sketch` - Create sketch on plane (supports plane_index for offset planes)
- `create_sketch_on_face` - Create sketch on existing body face
- `draw_circle` - Draw a circle
- `draw_rectangle` - Draw a rectangle
- `draw_line` - Draw a line
- `draw_polygon` - Draw a regular polygon
- `draw_arc` / `draw_arc_sweep` / `draw_arc_three_points` - Draw arcs
- `list_profiles` - List profiles in a sketch

### Sketch Constraints
- `add_constraint_midpoint` - Constrain point to line midpoint
- `add_constraint_coincident` - Constrain point to curve
- `add_constraint_coincident_points` - Constrain two line endpoints together
- `add_constraint_vertical` - Make line vertical
- `add_constraint_horizontal` - Make line horizontal
- `get_sketch_constraints` - List all constraints in a sketch
- `delete_constraint` - Delete a constraint by index

### 3D Operations
- `extrude` - Extrude a profile into 3D
- `revolve` - Revolve a profile around an axis
- `loft` / `loft_rails` - Create smooth transitions between profiles
- `fillet` - Round edges
- `chamfer` - Bevel edges
- `shell` - Hollow out a body

### Parameters
- `set_parameter` - Create/update a user parameter

## Example: Create a Box

See [examples.md](./examples.md) for complete workflow examples.

## Units

All dimensions are in **centimeters** (Fusion 360's internal unit):
- 1 cm = 10 mm
- To create a 50mm object, use `5` (cm)

## Tips

- Always create a sketch before drawing shapes
- Use `list_profiles` to find the correct profile index before extruding
- If a command fails, check `results.json` for error details
