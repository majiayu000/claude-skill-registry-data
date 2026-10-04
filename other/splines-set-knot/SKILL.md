---
name: splines-set-knot
description: Set position, in/out tangents, and/or rotation of an existing knot in a spline. Only the fields you pass are changed; the rest are preserved.
---

# Splines / Set Knot

Edit an existing knot in place. `BezierKnot` is a value type, so this reads the current knot, applies only the provided fields, and writes it back through the spline indexer (which rebuilds the cached curve).

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `knotIndex` — the index of the knot to edit (required).
- `position` — optional new local-space position.
- `tangentIn` / `tangentOut` — optional new tangents.
- `rotation` — optional new euler-degrees rotation.
- `splineIndex` — which spline in the container (default 0).

## Behavior

Reads the knot, overrides only the supplied fields, writes it back, marks the scene dirty, repaints, and returns the resulting knot summary. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-set-knot --input '{
  "gameObjectRef": "string_value",
  "knotIndex": 0,
  "position": "string_value",
  "tangentIn": "string_value",
  "tangentOut": "string_value",
  "rotation": "string_value",
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-set-knot --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-set-knot --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `any` | Yes | Reference to the GameObject containing the SplineContainer component. |
| `knotIndex` | `integer` | Yes | Index of the knot to edit (0..knotCount-1). |
| `position` | `any` | No | New local-space position of the knot. |
| `tangentIn` | `any` | No | New in tangent relative to the knot position. |
| `tangentOut` | `any` | No | New out tangent relative to the knot position. |
| `rotation` | `any` | No | New knot rotation in euler angles (degrees). |
| `splineIndex` | `integer` | No | Index of the spline inside the container (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "knotIndex": {
      "type": "integer"
    },
    "position": {
      "$ref": "#/$defs/UnityEngine.Vector3"
    },
    "tangentIn": {
      "$ref": "#/$defs/UnityEngine.Vector3"
    },
    "tangentOut": {
      "$ref": "#/$defs/UnityEngine.Vector3"
    },
    "rotation": {
      "$ref": "#/$defs/UnityEngine.Vector3"
    },
    "splineIndex": {
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
  },
  "required": [
    "gameObjectRef",
    "knotIndex"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-KnotMutationResponse"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-KnotInfo": {
      "type": "object",
      "properties": {
        "index": {
          "type": "integer",
          "description": "Index of the knot inside the spline."
        },
        "position": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "Local-space position of the knot."
        },
        "tangentIn": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "In tangent (relative to the knot position)."
        },
        "tangentOut": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "Out tangent (relative to the knot position)."
        },
        "rotationEuler": {
          "$ref": "#/$defs/UnityEngine.Vector3",
          "description": "Knot rotation in euler angles (degrees)."
        },
        "tangentMode": {
          "type": "string",
          "description": "Tangent mode of the knot."
        }
      },
      "required": [
        "index",
        "position",
        "tangentIn",
        "tangentOut",
        "rotationEuler"
      ]
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-KnotMutationResponse": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the SplineContainer GameObject."
        },
        "containerRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the SplineContainer component."
        },
        "splineIndex": {
          "type": "integer",
          "description": "Index of the affected spline in the container."
        },
        "knotIndex": {
          "type": "integer",
          "description": "Index of the affected knot in the spline (-1 when not applicable)."
        },
        "knotCount": {
          "type": "integer",
          "description": "Resulting number of knots in the spline."
        },
        "knot": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-KnotInfo",
          "description": "Summary of the affected knot, when applicable."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "splineIndex",
        "knotIndex",
        "knotCount",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

