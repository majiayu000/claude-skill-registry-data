---
name: terrain-create
description: Create a new GameObject with a `Terrain` + `TerrainCollider` backed by a freshly created `TerrainData` asset. Set heightmap resolution and the terrain world size (width/height/length). Returns the new GameObject reference and instanceId.
---

# Terrain / Create Terrain

Create a new GameObject hosting a `Terrain` and a `TerrainCollider` in the active scene, backed by a new `TerrainData` asset saved to the project.

## Inputs

- `name` — optional GameObject name (default `Terrain`).
- `terrainDataAssetPath` — project path for the new `TerrainData` asset (default `Assets/TerrainData_<name>.asset`). Must start with `Assets/` and end with `.asset`.
- `heightmapResolution` — heightmap resolution; rounded to a valid `2^n + 1` value (default 513).
- `width` / `length` — horizontal terrain size in world units (X / Z, default 1000 each).
- `height` — vertical terrain size in world units (Y, default 600).
- `position` — optional world position of the terrain GameObject (default zero).

## Behavior

Creates the `TerrainData`, sets its `heightmapResolution` and `size`, writes it as an asset, then creates the GameObject via `Terrain.CreateTerrainGameObject`, positions it, marks the scene dirty, repaints, and returns the new GameObject reference and instanceId. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-create --input '{
  "name": "string_value",
  "terrainDataAssetPath": "string_value",
  "heightmapResolution": 0,
  "width": 0,
  "length": 0,
  "height": 0,
  "position": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | `string` | No | Name of the new Terrain GameObject. |
| `terrainDataAssetPath` | `string` | No | Project path for the new TerrainData asset (Assets/...asset). Defaults to Assets/TerrainData_<name>.asset. |
| `heightmapResolution` | `integer` | No | Heightmap resolution. Rounded up to a valid (2^n + 1) value. |
| `width` | `number` | No | Terrain width in world units (X axis). |
| `length` | `number` | No | Terrain length in world units (Z axis). |
| `height` | `number` | No | Terrain height in world units (Y axis). |
| `position` | `any` | No | World-space position of the terrain GameObject. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "terrainDataAssetPath": {
      "type": "string"
    },
    "heightmapResolution": {
      "type": "integer"
    },
    "width": {
      "type": "number"
    },
    "length": {
      "type": "number"
    },
    "height": {
      "type": "number"
    },
    "position": {
      "$ref": "#/$defs/UnityEngine.Vector3"
    }
  },
  "$defs": {
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainCreateResponse"
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
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainCreateResponse": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the created Terrain GameObject."
        },
        "terrainRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the created Terrain component."
        },
        "instanceId": {
          "type": "integer",
          "description": "Instance id of the created GameObject."
        },
        "gameObjectName": {
          "type": "string",
          "description": "Name of the created GameObject."
        },
        "terrainDataAssetPath": {
          "type": "string",
          "description": "Project path of the created TerrainData asset."
        },
        "heightmapResolution": {
          "type": "integer",
          "description": "Resolved heightmap resolution."
        },
        "size": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "Resolved terrain size (X=width, Y=height, Z=length)."
        }
      },
      "required": [
        "instanceId",
        "heightmapResolution",
        "size"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

