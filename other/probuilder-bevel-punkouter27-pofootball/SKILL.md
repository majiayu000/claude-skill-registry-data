---
name: probuilder-bevel
description: Bevel (chamfer) selected edges of a `ProBuilderMesh`, replacing each sharp edge with an angled face. Identify edges by their `[vertexA, vertexB]` index pairs — use 'probuilder-get-mesh-info' to discover them. `amount` is clamped to (0, 1).
---

# Bevel ProBuilder edges

Bevel (chamfer) selected edges of a `ProBuilderMesh`, replacing each sharp edge with an angled face for a smoother appearance. Use 'probuilder-get-mesh-info' first to discover edges by their vertex pairs.

## Inputs

- `gameObjectRef` — the GameObject hosting the `ProBuilderMesh` component.
- `edges` — array of edge definitions; each edge is `[vertexA, vertexB]`. Example: `[[0,1], [2,3]]` bevels two edges.
- `amount` — bevel strength in the range (0, 1). `0.001` is barely visible, `0.999` reaches face center. Recommended `0.05`–`0.2`. Internally clamped.

## Behavior

Vertex indices are validated against `vertexCount`. After `BevelEdges` runs, the mesh is rebuilt (`ToMesh` → `Refresh`), the `ProBuilderMesh` and GameObject are marked dirty, and Editor windows repaint. Returns the number of edges processed, the clamped amount, and post-op face/vertex/edge counts. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool probuilder-bevel --input '{
  "gameObjectRef": "string_value",
  "edges": "string_value",
  "amount": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool probuilder-bevel --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool probuilder-bevel --input-file - <<'EOF'
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
| `edges` | `any` | Yes | Array of edge definitions. Each edge is defined by two vertex indices [vertexA, vertexB]. Example: [[0,1], [2,3]] bevels edges from vertex 0 to 1 and from vertex 2 to 3. |
| `amount` | `number` | No | Bevel amount from 0 (no bevel) to 1 (maximum bevel reaching face center). Recommended values: 0.05 to 0.2. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "edges": {
      "$ref": "#/$defs/System.Int32-1-1"
    },
    "amount": {
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
    },
    "System.Int32-1": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    },
    "System.Int32-1-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/System.Int32-1"
      }
    }
  },
  "required": [
    "gameObjectRef",
    "edges"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_ProBuilder-BevelResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_ProBuilder-BevelResponse": {
      "type": "object",
      "properties": {
        "edgesBeveled": {
          "type": "integer"
        },
        "bevelAmount": {
          "type": "number"
        },
        "newFacesCreated": {
          "type": "integer"
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
        "edgesBeveled",
        "bevelAmount",
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

