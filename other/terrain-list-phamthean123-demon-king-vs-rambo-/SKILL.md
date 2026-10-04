---
name: terrain-list
description: List every `Terrain` in the active scene with its name, world size, heightmap resolution, and TerrainLayer count. Read-only.
---

# Terrain / List Terrains

List every `Terrain` in the active scene.

## Inputs

- `includeInactive` (bool, default true) — include Terrains on inactive/disabled GameObjects.

## Behavior

Finds all `Terrain` instances, and for each returns the GameObject reference, the name, the `TerrainData.size`, the heightmap resolution, and the number of TerrainLayers. Read-only. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include Terrains on inactive/disabled GameObjects; if false, only active ones. |

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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainListResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainListItem-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainListItem"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainListItem": {
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
        "name": {
          "type": "string",
          "description": "Name of the terrain GameObject."
        },
        "size": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "Terrain size (X=width, Y=height, Z=length)."
        },
        "heightmapResolution": {
          "type": "integer",
          "description": "Heightmap resolution."
        },
        "layerCount": {
          "type": "integer",
          "description": "Number of TerrainLayers assigned."
        }
      },
      "required": [
        "size",
        "heightmapResolution",
        "layerCount"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainListResponse": {
      "type": "object",
      "properties": {
        "count": {
          "type": "integer",
          "description": "Number of Terrains found."
        },
        "terrains": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Terrain-TerrainListItem-1",
          "description": "The Terrains in the active scene."
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

