---
name: push-design
description: Push GameGen Game Design to Godot by parsing AI responses and generating .tscn scene files. Consumes AI responses to build Godot objects/controls.
allowed-tools: Read, Write, Bash(python3:*), Glob, Grep, mcp__dynamodb__get_item, mcp__dynamodb__query_table, mcp__dynamodb__scan_table, mcp__dynamodb__put_item
---

# Push Design Skill

Parses AI Game Design responses and generates initial Godot project structure.

**This is an infrequent operation** for setting up a new project or restructuring based on AI-generated designs. For regular syncing of layout changes, use `project-sync` instead.

## What This Skill Does

1. **Reads Game Design prompts** from the AIPrompts table
2. **Parses AI responses** to extract scene hierarchies (tree structures like `Root (Node2D) → UI (Control) → ...`)
3. **Merges with existing layouts** preserving user-set positions/sizes
4. **Generates .tscn files** in proper Godot 4.x format
5. **Updates project.godot** with the main scene

## When to Use

Use `push-design` when:
- Setting up a new project from AI Game Design
- Restructuring the scene hierarchy based on new AI design
- Initial project scaffolding

Use `project-sync` when:
- Syncing layout changes (positions, sizes, styles) to Godot
- Regular development workflow
- Exporting current DynamoDB state to .tscn

## Usage

Ask Claude to:
- "Push design for project 2"
- "Build Godot project from the Game Design response"
- "Generate .tscn files from the AI design for project 1"

### Workflow

1. **Create Game Design** in GameGen (right-click [PRJ] → Game Design)
2. **Generate AI response** describing the scene structure
3. **Run push-design** to convert AI response to .tscn files

### Command Line

```bash
cd .claude/skills/push-design/scripts

# Parse AI Game Design and generate .tscn
python3 sync.py --project-id 2 --from-game-design

# Dry run to preview output
python3 sync.py --project-id 2 --from-game-design --dry-run

# Custom output directory
python3 sync.py --project-id 2 --from-game-design --output-dir /path/to/godot/project
```

## Architecture

### Module Structure

```
push-design/
├── SKILL.md           # This file
└── scripts/
    ├── models.py      # Data classes (SceneNode, NodeProperties)
    ├── parser.py      # AI response parser (extracts tree structures)
    ├── generator.py   # .tscn file generator (shared with project-sync)
    └── sync.py        # Main orchestrator
```

### Parser (parser.py)

Extracts scene hierarchies from AI responses. Handles formats like:

```
Root (Node2D)
├── UI (Control)
│   ├── ToolbarLeft (HBoxContainer)
│   │   └── Button_NewGame (Button)
│   └── StatusBar (HBoxContainer)
└── SlotMachine (Node2D)
```

### Generator (generator.py)

Converts SceneNode trees to Godot .tscn format. This module is shared with `project-sync`.

## DynamoDB Tables

| Table | Keys | Used For |
|-------|------|----------|
| Projects | ID (N) | Project name, GodotProjectPath |
| SceneLayout | projectID (N) | Existing scene hierarchy (sceneRoot) |
| AIPrompts | projectObjectID (S), promptID (S) | Game Design responses |

### Finding Game Design Prompts

Game Design prompts have:
- `projectObjectID`: `"{projectID}_0"` (e.g., "2_0")
- `title`: "Game Design"
- `response`: The AI-generated design document

## Merging Behavior

When parsing Game Design with existing SceneLayout:
- **Structure**: Adopts the new AI-generated hierarchy
- **Layout properties**: Preserves user-set positions/sizes from existing nodes
- **New nodes**: Added with default properties
- **Removed nodes**: Dropped from the merged result

This allows iterative refinement: regenerate Game Design to restructure, keep manual layout adjustments.

## Related Skills

- **project-sync**: Regular sync from DynamoDB to Godot (frequent)
- **project-importer**: Import Godot changes back to DynamoDB (reverse sync)
