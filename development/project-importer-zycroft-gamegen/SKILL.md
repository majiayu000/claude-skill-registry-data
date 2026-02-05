---
name: project-importer
description: Import entire Godot projects (.tscn scenes + .gd scripts) and convert to GameGen's format for DynamoDB. Detects programmatic position/size assignments and flags them.
allowed-tools: Read, Bash(python:*), Glob, Grep, mcp__dynamodb__put_item, mcp__dynamodb__scan_table
---

# Project Importer Skill

Imports entire Godot projects into GameGen's scene hierarchy format, including:
- All `.tscn` scene files in the project
- Associated `.gd` script files for programmatic position/size detection
- Automatic project name detection from `project.godot`

## What this Skill does

1. Scans a Godot project directory for all `.tscn` and `.gd` files
2. Parses each scene's node hierarchy (containers, widgets, 2D nodes)
3. Analyzes GDScript files to detect programmatic position/size assignments
4. Flags nodes with `positionProgrammatic` or `sizeProgrammatic` when code modifies them
5. Extracts approximate values from code when possible
6. **Calculates absolute positions** based on container layout rules (VBox/HBox stacking)
7. Uploads to DynamoDB with all scenes merged under a project root

## Layout Position Calculation

The importer automatically calculates absolute positions for nodes based on their parent container type:

- **VBoxContainer**: Children are stacked vertically. Each child's Y position equals the sum of all previous siblings' heights.
- **HBoxContainer**: Children are stacked horizontally. Each child's X position equals the sum of all previous siblings' widths.
- **Other containers**: Children inherit their parent's position offset added to their own relative position.

This ensures that when viewing individual nodes in GameGen, they appear at their correct absolute positions within the viewport.

## Usage

Ask Claude to:
- "Import the Godot project at /path/to/project"
- "Import all scenes from my Godot project into GameGen"
- "Parse the GameGen project and upload to DynamoDB with ID 5"
- "Do a dry run import of the project to see what would be uploaded"

### Command Line Usage

```bash
# Import entire project
python .claude/skills/project-importer/scripts/import_godot_scene.py /path/to/project --project-id 1

# Import with custom name
python .claude/skills/project-importer/scripts/import_godot_scene.py /path/to/project --project-id 1 --project-name "My Game"

# Dry run (parse only, don't upload)
python .claude/skills/project-importer/scripts/import_godot_scene.py /path/to/project --project-id 1 --dry-run

# Output to JSON file
python .claude/skills/project-importer/scripts/import_godot_scene.py /path/to/project --project-id 1 --output scenes.json

# Verbose output with full JSON
python .claude/skills/project-importer/scripts/import_godot_scene.py /path/to/project --project-id 1 --dry-run -v
```

## Programmatic Detection

The importer analyzes GDScript files for patterns that modify position or size at runtime:

### Position Patterns Detected
```gdscript
node.position = Vector2(x, y)
node.global_position = Vector2(x, y)
$NodeName.position = Vector2(x, y)
offset_left = value
offset_top = value
```

### Size Patterns Detected
```gdscript
node.size = Vector2(x, y)
node.size = Vector2i(x, y)
$NodeName.size = Vector2(x, y)
custom_minimum_size = Vector2(x, y)
offset_right = value
offset_bottom = value
```

When these patterns are found:
1. The node is flagged with `positionProgrammatic: true` or `sizeProgrammatic: true`
2. If the code contains literal values (e.g., `Vector2(340, 100)`), those become the approximated position/size
3. If the code uses variables or expressions, the flag is set but scene file values are preserved

## Supported Node Types

### 2D Nodes
- Node2D, Sprite2D, AnimatedSprite2D
- CharacterBody2D, RigidBody2D, StaticBody2D, Area2D
- Camera2D, TileMap, TileMapLayer, Polygon2D, Line2D

### Container Types
- VBoxContainer, HBoxContainer, GridContainer
- FlowContainer (HFlowContainer, VFlowContainer)
- MarginContainer, PanelContainer, CenterContainer
- AspectRatioContainer, HSplitContainer, VSplitContainer
- TabContainer, ScrollContainer, SubViewportContainer

### Widget Types
- Button, Label, LineEdit, TextEdit
- CheckBox, CheckButton, OptionButton
- SpinBox, HSlider, VSlider, ProgressBar
- ColorRect, TextureRect, ColorPickerButton
- RichTextLabel, ItemList, Tree, GraphEdit
- MenuButton, LinkButton, TextureButton

### Animation
- AnimationPlayer, AnimationTree

## Output Format

### Single Scene
```json
{
  "projectID": 1,
  "projectName": "My Project",
  "sceneRoot": {
    "id": 1,
    "type": "Node2D",
    "name": "Main",
    "_scenePath": "main.tscn",
    "positionProgrammatic": false,
    "sizeProgrammatic": true,
    "children": [...],
    "widgets": [...],
    "properties": {
      "positionX": 0,
      "positionY": 0,
      "sizeX": 200,
      "sizeY": 150
    }
  },
  "sceneCount": 1,
  "savedAt": "2025-12-28T10:30:00"
}
```

### Multiple Scenes
When a project has multiple scenes, they are merged under a `ProjectRoot` node:

```json
{
  "projectID": 1,
  "projectName": "My Project",
  "sceneRoot": {
    "id": 1,
    "type": "Node2D",
    "name": "ProjectRoot",
    "children": [
      {
        "id": 2,
        "name": "Main",
        "_scenePath": "main.tscn",
        ...
      },
      {
        "id": 15,
        "name": "UI",
        "_scenePath": "ui/menu.tscn",
        ...
      }
    ]
  },
  "sceneCount": 2
}
```

### Widget with Programmatic Flag
```json
{
  "id": 5,
  "type": "Button",
  "name": "StartButton",
  "positionProgrammatic": true,
  "sizeProgrammatic": false,
  "properties": {
    "text": "Start Game",
    "minSizeX": 80,
    "minSizeY": 30
  }
}
```

## DynamoDB Storage

- Endpoint: `http://zycroft.duckdns.org:8001`
- Table: `SceneLayout`
- Primary Key: `projectID` (Number)

Data uses native DynamoDB types:
- Numbers (N) for numeric values
- Strings (S) for text
- Maps (M) for nested objects
- Lists (L) for arrays
- Booleans (BOOL) for flags like `positionProgrammatic`

## Project Structure Requirements

The importer expects a standard Godot project structure:

```
project/
├── project.godot          # Project config (optional, for name detection)
├── main.tscn              # Scene files
├── main.gd                # Associated scripts
├── ui/
│   ├── menu.tscn
│   └── menu.gd
└── characters/
    └── player.tscn
```

The `.godot/` directory is automatically excluded from scanning.

## Related Skills

- **project-sync**: Export DynamoDB SceneLayout to Godot .tscn (reverse of this skill)
- **push-design**: Initial project setup from AI Game Design (infrequent)
