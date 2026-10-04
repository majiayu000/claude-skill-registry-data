---
name: tilemap-clear
description: "Clear tiles from a Tilemap: either every tile (ClearAllTiles) or a rectangular region (by erasing each cell in the inclusive min..max range). Destructive."
---

# Tilemap / Clear Tiles

Erase tiles from a `Tilemap`. By default clears the whole map; pass a region to clear only a rectangular block.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Tilemap` (required).
- `clearAll` (bool, default true) — when true, calls `Tilemap.ClearAllTiles()`; when false, erases the region defined by `minX/minY/maxX/maxY`.
- `minX`, `minY`, `maxX`, `maxY`, `z` — the inclusive region (used only when `clearAll` is false).

## Behavior

Either clears all tiles or sets each cell in the region to null, marks the scene dirty, and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool tilemap-clear --input '{
  "gameObjectRef": "string_value",
  "clearAll": false,
  "minX": 0,
  "minY": 0,
  "maxX": 0,
  "maxY": 0,
  "z": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool tilemap-clear --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool tilemap-clear --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `any` | Yes | Reference to the GameObject containing the Tilemap component. |
| `clearAll` | `boolean` | No | If true (default) clear the entire Tilemap; if false, clear the min..max region only. |
| `minX` | `integer` | No | Inclusive minimum cell X (region mode). |
| `minY` | `integer` | No | Inclusive minimum cell Y (region mode). |
| `maxX` | `integer` | No | Inclusive maximum cell X (region mode). |
| `maxY` | `integer` | No | Inclusive maximum cell Y (region mode). |
| `z` | `integer` | No | Cell Z coordinate (region mode, default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "clearAll": {
      "type": "boolean"
    },
    "minX": {
      "type": "integer"
    },
    "minY": {
      "type": "integer"
    },
    "maxX": {
      "type": "integer"
    },
    "maxY": {
      "type": "integer"
    },
    "z": {
      "type": "integer"
    }
  },
  "$defs": {
    "System.Type": {
      "type": "string"
    },
    "AIGD.GameObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "type": "integer",
          "description": "instanceID of the UnityEngine.Object. If it is '0' and 'path', 'name', 'assetPath' and 'assetGuid' is not provided, empty or null, then it will be used as 'null'. Priority: 1 (Recommended)"
        },
        "path": {
          "type": "string",
          "description": "Path of a GameObject in the hierarchy Sample 'character/hand/finger/particle'. Priority: 2."
        },
        "name": {
          "type": "string",
          "description": "Name of a GameObject in hierarchy. Priority: 3."
        },
        "assetType": {
          "$ref": "#/$defs/System.Type",
          "description": "Type of the asset."
        },
        "assetPath": {
          "type": "string",
          "description": "Path to the asset within the project. Starts with 'Assets/'"
        },
        "assetGuid": {
          "type": "string",
          "description": "Unique identifier for the asset."
        }
      },
      "required": [
        "instanceID"
      ],
      "description": "Find GameObject in opened Prefab or in the active Scene."
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

### Output JSON Schema

```json
{
  "type": "object",
  "properties": {
    "result": {
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ClearResponse"
    }
  },
  "$defs": {
    "AIGD.GameObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "type": "integer",
          "description": "instanceID of the UnityEngine.Object. If it is '0' and 'path', 'name', 'assetPath' and 'assetGuid' is not provided, empty or null, then it will be used as 'null'. Priority: 1 (Recommended)"
        },
        "path": {
          "type": "string",
          "description": "Path of a GameObject in the hierarchy Sample 'character/hand/finger/particle'. Priority: 2."
        },
        "name": {
          "type": "string",
          "description": "Name of a GameObject in hierarchy. Priority: 3."
        },
        "assetType": {
          "$ref": "#/$defs/System.Type",
          "description": "Type of the asset."
        },
        "assetPath": {
          "type": "string",
          "description": "Path to the asset within the project. Starts with 'Assets/'"
        },
        "assetGuid": {
          "type": "string",
          "description": "Unique identifier for the asset."
        }
      },
      "required": [
        "instanceID"
      ],
      "description": "Find GameObject in opened Prefab or in the active Scene."
    },
    "System.Type": {
      "type": "string"
    },
    "AIGD.ComponentRef": {
      "type": "object",
      "properties": {
        "index": {
          "type": "integer",
          "description": "Component 'index' attached to a gameObject. The first index is '0' and that is usually Transform or RectTransform. Priority: 2. Default value is -1."
        },
        "typeName": {
          "type": "string",
          "description": "Component type full name. Sample 'UnityEngine.Transform'. If the gameObject has two components of the same type, the output component is unpredictable. Priority: 3. Default value is null."
        },
        "instanceID": {
          "type": "integer",
          "description": "instanceID of the UnityEngine.Object. If this is '0', then it will be used as 'null'."
        }
      },
      "required": [
        "index",
        "instanceID"
      ],
      "description": "Component reference. Used to find a Component at GameObject."
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ClearResponse": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the Tilemap GameObject."
        },
        "tilemapRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the Tilemap component."
        },
        "clearedAll": {
          "type": "boolean",
          "description": "True when the whole map was cleared."
        },
        "clearedCount": {
          "type": "integer",
          "description": "Number of cells cleared in region mode; -1 when clearedAll."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "clearedAll",
        "clearedCount",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

