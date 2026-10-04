---
name: tilemap-box-fill
description: Fill a rectangular region of a Tilemap with a single TileBase asset using Tilemap.BoxFill. The region is defined by an inclusive min and max cell coordinate.
---

# Tilemap / Box Fill

Fill a rectangular block of cells of a `Tilemap` with one tile via `Tilemap.BoxFill`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Tilemap` (required).
- `minX`, `minY` — inclusive minimum cell coordinate.
- `maxX`, `maxY` — inclusive maximum cell coordinate.
- `z` — cell Z coordinate (default 0).
- `tileAssetPath` — `Assets/`-rooted path to the `TileBase` asset to fill with (required).

## Behavior

Loads the tile, calls `Tilemap.BoxFill(start, tile, minX, minY, maxX, maxY)`, marks the scene dirty, and repaints. Returns the filled cell count. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool tilemap-box-fill --input '{
  "gameObjectRef": "string_value",
  "tileAssetPath": "string_value",
  "minX": 0,
  "minY": 0,
  "maxX": 0,
  "maxY": 0,
  "z": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool tilemap-box-fill --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool tilemap-box-fill --input-file - <<'EOF'
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
| `tileAssetPath` | `string` | Yes | Assets/-rooted path to the TileBase asset to fill the region with. |
| `minX` | `integer` | Yes | Inclusive minimum cell X coordinate. |
| `minY` | `integer` | Yes | Inclusive minimum cell Y coordinate. |
| `maxX` | `integer` | Yes | Inclusive maximum cell X coordinate. |
| `maxY` | `integer` | Yes | Inclusive maximum cell Y coordinate. |
| `z` | `integer` | No | Cell Z coordinate (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "tileAssetPath": {
      "type": "string"
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
    "gameObjectRef",
    "tileAssetPath",
    "minX",
    "minY",
    "maxX",
    "maxY"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-BoxFillResponse"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-BoxFillResponse": {
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
        "minX": {
          "type": "integer",
          "description": "Resolved minimum X."
        },
        "minY": {
          "type": "integer",
          "description": "Resolved minimum Y."
        },
        "maxX": {
          "type": "integer",
          "description": "Resolved maximum X."
        },
        "maxY": {
          "type": "integer",
          "description": "Resolved maximum Y."
        },
        "cellZ": {
          "type": "integer",
          "description": "Cell Z coordinate."
        },
        "filledCount": {
          "type": "integer",
          "description": "Number of cells filled."
        },
        "tileAssetPath": {
          "type": "string",
          "description": "Path of the tile asset used."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "minX",
        "minY",
        "maxX",
        "maxY",
        "cellZ",
        "filledCount",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

