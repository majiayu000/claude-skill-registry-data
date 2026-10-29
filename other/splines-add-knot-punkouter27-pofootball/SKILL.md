---
name: splines-add-knot
description: Append a knot to a spline in a `SplineContainer`. A knot is a `BezierKnot` with a local position plus in/out tangents and a rotation. Returns the index of the appended knot.
---

# Splines / Add Knot

Append a new knot to the end of a spline. Knots define the control points the spline curve passes through.

## Inputs

- `gameObjectRef` — the GameObject hosting the `SplineContainer` (required).
- `position` — local-space `Vector3` position of the knot (default zero).
- `tangentIn` — optional in tangent relative to the position (default `(0,0,-1)`).
- `tangentOut` — optional out tangent relative to the position (default `(0,0,1)`).
- `rotation` — optional euler-degrees rotation of the knot (default zero).
- `splineIndex` — which spline in the container to append to (default 0).

## Behavior

Builds a `BezierKnot` from the inputs, appends it to the chosen spline, marks the scene dirty, repaints, and returns the appended knot index plus the spline's new knot count. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-add-knot --input '{
  "gameObjectRef": "string_value",
  "position": "string_value",
  "tangentIn": "string_value",
  "tangentOut": "string_value",
  "rotation": "string_value",
  "splineIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-add-knot --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-add-knot --input-file - <<'EOF'
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
| `position` | `any` | No | Local-space position of the new knot. |
| `tangentIn` | `any` | No | In tangent relative to the knot position. |
| `tangentOut` | `any` | No | Out tangent relative to the knot position. |
| `rotation` | `any` | No | Knot rotation in euler angles (degrees). |
| `splineIndex` | `integer` | No | Index of the spline inside the container to append to (default 0). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-KnotMutationResponse"
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

