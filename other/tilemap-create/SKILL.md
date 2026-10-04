---
name: tilemap-create
description: Create a Grid GameObject with a child Tilemap + TilemapRenderer in the active scene. Optionally parent the Grid under an existing GameObject and name the tilemap. Returns the new tilemap GameObject reference and its instanceId.
---

# Tilemap / Create Grid + Tilemap

Create the standard 2D tilemap hierarchy: a `Grid` GameObject hosting a child GameObject with a `Tilemap` and `TilemapRenderer`. This is the minimal structure required before painting tiles.

## Inputs

- `gridName` — optional name for the Grid GameObject (default `Grid`).
- `tilemapName` — optional name for the Tilemap child GameObject (default `Tilemap`).
- `parentRef` — optional GameObject to parent the new Grid under.
- `cellSize` — optional Grid cell size (default `(1,1,0)`).

## Behavior

Creates the Grid + child Tilemap/TilemapRenderer, sets the cell size, parents under `parentRef` when supplied, marks the scene dirty, repaints, and returns references + the tilemap GameObject instanceId. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool tilemap-create --input '{
  "gridName": "string_value",
  "tilemapName": "string_value",
  "parentRef": "string_value",
  "cellSize": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool tilemap-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool tilemap-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gridName` | `string` | No | Name of the Grid GameObject. |
| `tilemapName` | `string` | No | Name of the child Tilemap GameObject. |
| `parentRef` | `any` | No | Optional GameObject to parent the new Grid under. |
| `cellSize` | `any` | No | Grid cell size. Defaults to (1,1,0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gridName": {
      "type": "string"
    },
    "tilemapName": {
      "type": "string"
    },
    "parentRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "cellSize": {
      "$ref": "#/$defs/UnityEngine.Vector3"
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
    },
    "UnityEngine.Vector3": {
      "type": "object",
      "properties": {
        "x": {
          "type": "number"
        },
        "y": {
          "type": "number"
        },
        "z": {
          "type": "number"
        }
      },
      "required": [
        "x",
        "y",
        "z"
      ],
      "additionalProperties": false
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-CreateResponse"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Tilemap-CreateResponse": {
      "type": "object",
      "properties": {
        "gridRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the created Grid GameObject."
        },
        "tilemapGameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the created Tilemap GameObject."
        },
        "tilemapRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the created Tilemap component."
        },
        "rendererRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the created TilemapRenderer component."
        },
        "instanceId": {
          "type": "integer",
          "description": "Instance id of the created Tilemap GameObject."
        },
        "gridName": {
          "type": "string",
          "description": "Name of the created Grid GameObject."
        },
        "tilemapName": {
          "type": "string",
          "description": "Name of the created Tilemap GameObject."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "instanceId",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

