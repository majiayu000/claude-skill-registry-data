---
name: splines-list
description: List every `SplineContainer` in the active scene with its name, spline count, and the knot count of each spline. Read-only.
---

# Splines / List Containers

Enumerate the `SplineContainer`s in the active scene. For each, returns a reference, the name, the number of splines, and per-spline knot counts and closed flags.

## Inputs

- `includeInactive` (bool, default true) — include containers on inactive/disabled GameObjects.

## Behavior

Finds all `SplineContainer` instances and summarizes them. Read-only. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool splines-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool splines-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool splines-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include containers on inactive/disabled GameObjects. |

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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-ListResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-ContainerListItem-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-ContainerListItem"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-ContainerListItem": {
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
        "name": {
          "type": "string",
          "description": "Name of the container GameObject."
        },
        "splineCount": {
          "type": "integer",
          "description": "Number of splines in the container."
        },
        "splines": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-SplineSummary-1",
          "description": "Per-spline summaries."
        }
      },
      "required": [
        "splineCount"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-SplineSummary-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-SplineSummary"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-SplineSummary": {
      "type": "object",
      "properties": {
        "splineIndex": {
          "type": "integer",
          "description": "Index of the spline in the container."
        },
        "knotCount": {
          "type": "integer",
          "description": "Number of knots in the spline."
        },
        "closed": {
          "type": "boolean",
          "description": "Whether the spline is a closed loop."
        }
      },
      "required": [
        "splineIndex",
        "knotCount",
        "closed"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-ListResponse": {
      "type": "object",
      "properties": {
        "count": {
          "type": "integer",
          "description": "Number of SplineContainers found."
        },
        "containers": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Splines-ContainerListItem-1",
          "description": "The SplineContainers in the active scene."
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

