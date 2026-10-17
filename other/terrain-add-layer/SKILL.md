---
name: terrain-add-layer
description: Add a `TerrainLayer` to a `Terrain`. Provide either the asset path of an existing `.terrainlayer` asset, or a texture asset path to build a new TerrainLayer from. Returns the index of the added layer.
---

# Terrain / Add Layer

Append a `TerrainLayer` to a `Terrain`'s `TerrainData.terrainLayers`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `terrainLayerAssetPath` — optional project path to an existing `.terrainlayer` asset to add.
- `diffuseTextureAssetPath` — optional project path to a `Texture2D`. When `terrainLayerAssetPath` is omitted, a new `TerrainLayer` is created in-memory with this diffuse texture and added.
- `tileSizeX` / `tileSizeY` — tile size (world units) for a newly-created layer (default 15,15).

## Behavior

Loads or creates the `TerrainLayer`, appends it to `TerrainData.terrainLayers`, marks the asset + scene dirty, repaints, and returns the new layer index. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-add-layer --input '{
  "gameObjectRef": "string_value",
  "terrainLayerAssetPath": "string_value",
  "diffuseTextureAssetPath": "string_value",
  "tileSizeX": 0,
  "tileSizeY": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-add-layer --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-add-layer --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `any` | Yes | Reference to the GameObject containing the Terrain component. |
| `terrainLayerAssetPath` | `string` | No | Optional project path to an existing .terrainlayer asset to add. |
| `diffuseTextureAssetPath` | `string` | No | Optional project path to a Texture2D used to build a new TerrainLayer (when no asset path is given). |
| `tileSizeX` | `number` | No | Tile size X (world units) for a newly-created layer. |
| `tileSizeY` | `number` | No | Tile size Y (world units) for a newly-created layer. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "terrainLayerAssetPath": {
      "type": "string"
    },
    "diffuseTextureAssetPath": {
      "type": "string"
    },
    "tileSizeX": {
      "type": "number"
    },
    "tileSizeY": {
      "type": "number"
    }
  },
  "$defs": {
    "UnityEngine.EntityId": {
      "type": "string",
      "pattern": "^[0-9]+$"
    },
    "System.Type": {
      "type": "string"
    },
    "AIGD.GameObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "$ref": "#/$defs/UnityEngine.EntityId",
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainAddLayerResponse"
    }
  },
  "$defs": {
    "AIGD.GameObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "$ref": "#/$defs/UnityEngine.EntityId",
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
    "UnityEngine.EntityId": {
      "type": "string",
      "pattern": "^[0-9]+$"
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
          "$ref": "#/$defs/UnityEngine.EntityId",
          "description": "instanceID of the UnityEngine.Object. If this is '0', then it will be used as 'null'."
        }
      },
      "required": [
        "index",
        "instanceID"
      ],
      "description": "Component reference. Used to find a Component at GameObject."
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainAddLayerResponse": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the Terrain GameObject."
        },
        "terrainRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the Terrain component."
        },
        "layerIndex": {
          "type": "integer",
          "description": "Index of the added TerrainLayer."
        },
        "layerCount": {
          "type": "integer",
          "description": "Total number of TerrainLayers after the add."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "layerIndex",
        "layerCount",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

