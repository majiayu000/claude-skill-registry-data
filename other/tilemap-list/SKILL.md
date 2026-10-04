---
name: tilemap-list
description: List every Tilemap in the active scene with its name, painted-tile count, cell bounds, and orientation. Read-only.
---

# Tilemap / List Tilemaps

Enumerate all `Tilemap` components in the active scene.

## Inputs

- `includeInactive` (bool, default true) — include Tilemaps on inactive GameObjects.

## Behavior

Finds all `Tilemap` instances, reads each one's `GetUsedTilesCount`, `cellBounds`, and `orientation`, and returns them. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool tilemap-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool tilemap-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool tilemap-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include Tilemaps on inactive GameObjects. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "includeInactive": {
      "type": "boolean"
    }
  }
}
```

## Output

### Output JSON Schema

```json
{
  "type": "object",
  "properties": {
    "result": {
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ListResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ListItem-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ListItem"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ListItem": {
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
        "name": {
          "type": "string",
          "description": "Name of the Tilemap GameObject."
        },
        "tileCount": {
          "type": "integer",
          "description": "Number of painted (used) tiles."
        },
        "boundsMin": {
          "$ref": "#/$defs/UnityEngine.Vector3Int",
          "description": "Inclusive minimum cell bound."
        },
        "boundsMax": {
          "$ref": "#/$defs/UnityEngine.Vector3Int",
          "description": "Exclusive maximum cell bound."
        },
        "orientation": {
          "type": "string",
          "description": "Layout orientation."
        }
      },
      "required": [
        "tileCount",
        "boundsMin",
        "boundsMax"
      ]
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
    "UnityEngine.Vector3Int": {
      "type": "object",
      "properties": {
        "x": {
          "type": "integer"
        },
        "y": {
          "type": "integer"
        },
        "z": {
          "type": "integer"
        }
      },
      "required": [
        "x",
        "y",
        "z"
      ],
      "additionalProperties": false
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ListResponse": {
      "type": "object",
      "properties": {
        "count": {
          "type": "integer",
          "description": "Number of Tilemaps found."
        },
        "tilemaps": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-ListItem-1",
          "description": "The Tilemaps in the active scene."
        }
      },
      "required": [
        "count"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

