---
name: terrain-get
description: Inspect a `Terrain` — its `TerrainData` size, heightmap / alphamap / detail resolutions, the list of TerrainLayers, tree/detail prototype counts, tree-instance count, and neighbor terrains. Read-only.
---

# Terrain / Get Terrain

Inspect a `Terrain` component in the active scene and report its `TerrainData` configuration.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).

## Behavior

Reads `TerrainData.size`, `heightmapResolution`, `alphamapResolution`, `detailResolution`, the `terrainLayers` (with their diffuse-texture names), the tree- and detail-prototype counts, the number of placed tree instances, and the left/top/right/bottom neighbor terrains. Read-only — nothing is mutated. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-get --input '{
  "gameObjectRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-get --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-get --input-file - <<'EOF'
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

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainGetResponse"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainLayerInfo-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainLayerInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainLayerInfo": {
      "type": "object",
      "properties": {
        "index": {
          "type": "integer",
          "description": "Index of the layer in the terrain's layer list."
        },
        "name": {
          "type": "string",
          "description": "Name of the TerrainLayer asset."
        },
        "assetPath": {
          "type": "string",
          "description": "Project asset path of the TerrainLayer, or null."
        },
        "diffuseTexture": {
          "type": "string",
          "description": "Name of the layer's diffuse texture, or null."
        }
      },
      "required": [
        "index"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainGetResponse": {
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
        "size": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "Terrain size (X=width, Y=height, Z=length) in world units."
        },
        "heightmapResolution": {
          "type": "integer",
          "description": "Heightmap resolution."
        },
        "alphamapResolution": {
          "type": "integer",
          "description": "Alphamap (splatmap) resolution."
        },
        "detailResolution": {
          "type": "integer",
          "description": "Detail resolution."
        },
        "layers": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainLayerInfo-1",
          "description": "The TerrainLayers assigned to the terrain."
        },
        "treePrototypeCount": {
          "type": "integer",
          "description": "Number of tree prototypes."
        },
        "detailPrototypeCount": {
          "type": "integer",
          "description": "Number of detail prototypes."
        },
        "treeInstanceCount": {
          "type": "integer",
          "description": "Number of placed tree instances."
        },
        "leftNeighbor": {
          "type": "string",
          "description": "Name of the left neighbor terrain, or null."
        },
        "topNeighbor": {
          "type": "string",
          "description": "Name of the top neighbor terrain, or null."
        },
        "rightNeighbor": {
          "type": "string",
          "description": "Name of the right neighbor terrain, or null."
        },
        "bottomNeighbor": {
          "type": "string",
          "description": "Name of the bottom neighbor terrain, or null."
        }
      },
      "required": [
        "size",
        "heightmapResolution",
        "alphamapResolution",
        "detailResolution",
        "treePrototypeCount",
        "detailPrototypeCount",
        "treeInstanceCount"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

