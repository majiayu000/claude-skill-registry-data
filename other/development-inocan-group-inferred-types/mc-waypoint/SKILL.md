---
name: mc-waypoint
type: python
description: "Labels a coordinate with a waypoint name for reasoning about spatial relationships. Use to mark important locations for navigation and planning"
---

# Minecraft Waypoint Tool

Labels a coordinate with a waypoint name for reasoning about spatial relationships. Stores waypoints in persistent spatial memory.

## Purpose

Spatial memory labeling for navigation and planning. Creates named waypoints that can be queried later for navigation and spatial reasoning.

## Input

- `name`: Waypoint name string (required)
- `dx`, `dy`, `dz`: World-relative offsets from agent (optional - defaults to 0,0,0 = current position)
  - See coordinate system documentation in jill-minecraft.yaml for details
- `value`: Ignored

## Output

Returns uniform_return format with:
- `value`: Text summary (success message with waypoint name and location)
- `data`: Structured data dict (machine-readable). Key fields:
  - `waypoint`: String (waypoint name)
  - `location`: `{x: int, y: int, z: int}`
  - `all_waypoints`: List of all waypoint names at this location

## Behavior & Performance

- Stores waypoint in SpatialMap cell at specified coordinates
- Creates cell if it doesn't exist
- Multiple waypoints can be stored at the same location
- Waypoints persist in SpatialMap and can be queried via cell data
- Auto-saves SpatialMap after update
- If coordinates not provided, automatically queries mc-status for current position

## Guidelines

- Use meaningful waypoint names (e.g., "Base_Camp", "Pit_Exit_1")
- Waypoints enable spatial reasoning and navigation
- Waypoints are stored in SpatialMap cells and persist across sessions
- Omit `dx, dy, dz` to mark current position, or specify relative offsets (see coordinate system in jill-minecraft.yaml)

## Usage Examples

Create waypoint at current position:
```json
{"type":"mc-waypoint","name":"Base_Camp","out":"$result"}
```

Create waypoint at relative position:
```json
{"type":"mc-waypoint","name":"Pit_Exit_1","dx":2,"dy":-6,"dz":3,"out":"$result"}
```
