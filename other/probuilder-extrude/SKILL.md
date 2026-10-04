---
name: probuilder-extrude
description: Extrude selected faces of a `ProBuilderMesh` along their normals, creating new geometry. Supply either `faceIndices` (explicit) or `faceDirection` (semantic); exactly one is required. Positive `distance` extrudes outward, negative inward.
---

# Extrude ProBuilder faces

Extrude selected faces of a `ProBuilderMesh` along their normals, creating new geometry by pushing faces outward (positive distance) or inward (negative distance). Faces can be selected explicitly by index or semantically by direction.

## Inputs

- `gameObjectRef` — the GameObject hosting the `ProBuilderMesh` component.
- `faceIndices` — explicit array of face indices to extrude.
- `faceDirection` — semantic alternative (`Up`, `Down`, `Left`, `Right`, `Forward`, `Back`). Exactly one of `faceIndices` / `faceDirection` is required.
- `distance` — extrusion distance. Positive = outward, negative = inward. Default `0.5`.
- `extrudeMethod` — `IndividualFaces` (each face extrudes independently), `FaceNormal` (faces extrude as a group along the averaged normal — the default), or `VertexNormal` (vertices move along their normals).

## Examples

- Extrude the top face up by 1 unit: `faceDirection="up"`, `distance=1`.
- Extrude specific faces: `faceIndices=[0, 2, 4]`.

## Behavior

The mesh is rebuilt (`ToMesh` → `Refresh`), dirty-flagged, and the Editor repaints. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool probuilder-extrude --input '{
  "gameObjectRef": "string_value",
  "faceIndices": "string_value",
  "faceDirection": "string_value",
  "distance": 0,
  "extrudeMethod": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool probuilder-extrude --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool probuilder-extrude --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `any` | Yes | Reference to the GameObject with a ProBuilderMesh component. |
| `faceIndices` | `any` | No | Array of face indices to extrude. Use this OR faceDirection, not both. Use ProBuilder_GetMeshInfo to get valid face indices. |
| `faceDirection` | `any` | No | Semantic face selection by direction. Use this OR faceIndices, not both. |
| `distance` | `number` | No | Distance to extrude the faces. Positive values extrude outward along face normals, negative values extrude inward. |
| `extrudeMethod` | `string` | No | Extrusion method: IndividualFaces (each face extrudes independently), FaceNormal (faces extrude as a group along averaged normal), VertexNormal (vertices move along their normals). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "faceIndices": {
      "$ref": "#/$defs/System.Int32-1"
    },
    "faceDirection": {
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.FaceDirection"
    },
    "distance": {
      "type": "number"
    },
    "extrudeMethod": {
      "type": "string",
      "enum": [
        "IndividualFaces",
        "VertexNormal",
        "FaceNormal"
      ]
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
    "System.Int32-1": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.FaceDirection": {
      "type": "string",
      "enum": [
        "Up",
        "Down",
        "Left",
        "Right",
        "Forward",
        "Back"
      ]
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_ProBuilder-ExtrudeResponse"
    }
  },
  "$defs": {
    "System.Int32-1": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_ProBuilder-ExtrudeResponse": {
      "type": "object",
      "properties": {
        "extrudedFaceCount": {
          "type": "integer"
        },
        "selectionMethod": {
          "type": "string"
        },
        "extrudedFaceIndices": {
          "$ref": "#/$defs/System.Int32-1"
        },
        "extrudeMethod": {
          "type": "string"
        },
        "distance": {
          "type": "number"
        },
        "newFacesCreated": {
          "type": "integer"
        },
        "newFaceIndices": {
          "$ref": "#/$defs/System.Int32-1"
        },
        "totalFaceCount": {
          "type": "integer"
        },
        "totalVertexCount": {
          "type": "integer"
        },
        "totalEdgeCount": {
          "type": "integer"
        }
      },
      "required": [
        "extrudedFaceCount",
        "distance",
        "newFacesCreated",
        "totalFaceCount",
        "totalVertexCount",
        "totalEdgeCount"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

