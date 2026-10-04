---
name: cinemachine-set-lens
description: Set lens fields of a `CinemachineCamera`'s `LensSettings` — field of view (perspective) or orthographic size, near / far clip planes, and Dutch (roll) angle. Only the fields you pass are changed.
---

# Cinemachine / Set Lens

Set lens fields on a `CinemachineCamera`. The `LensSettings` controls how the resulting Unity Camera is configured while this virtual camera is live.

## Inputs

- `gameObjectRef` — the GameObject hosting the `CinemachineCamera` (required).
- `fieldOfView` — optional vertical FOV in degrees (perspective cameras).
- `orthographicSize` — optional orthographic half-height (orthographic cameras).
- `nearClipPlane`, `farClipPlane` — optional clip plane distances.
- `dutch` — optional Dutch (roll) angle in degrees.

## Behavior

Reads the current `LensSettings`, applies only the provided fields, writes it back, marks the scene dirty, and repaints the Editor. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool cinemachine-set-lens --input '{
  "gameObjectRef": "string_value",
  "fieldOfView": "string_value",
  "orthographicSize": "string_value",
  "nearClipPlane": "string_value",
  "farClipPlane": "string_value",
  "dutch": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool cinemachine-set-lens --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool cinemachine-set-lens --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `any` | Yes | Reference to the GameObject containing the CinemachineCamera component. |
| `fieldOfView` | `any` | No | Vertical field of view in degrees (perspective). |
| `orthographicSize` | `any` | No | Orthographic size (half-height) for orthographic cameras. |
| `nearClipPlane` | `any` | No | Near clip plane distance. |
| `farClipPlane` | `any` | No | Far clip plane distance. |
| `dutch` | `any` | No | Dutch (roll) angle in degrees. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "fieldOfView": {
      "$ref": "#/$defs/System.Single"
    },
    "orthographicSize": {
      "$ref": "#/$defs/System.Single"
    },
    "nearClipPlane": {
      "$ref": "#/$defs/System.Single"
    },
    "farClipPlane": {
      "$ref": "#/$defs/System.Single"
    },
    "dutch": {
      "$ref": "#/$defs/System.Single"
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
    "System.Single": {
      "type": "number"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Cinemachine-SetLensResponse"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Cinemachine-SetLensResponse": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the CinemachineCamera GameObject."
        },
        "cameraRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the CinemachineCamera component."
        },
        "fieldOfView": {
          "type": "number",
          "description": "Resulting field of view."
        },
        "orthographicSize": {
          "type": "number",
          "description": "Resulting orthographic size."
        },
        "nearClipPlane": {
          "type": "number",
          "description": "Resulting near clip plane."
        },
        "farClipPlane": {
          "type": "number",
          "description": "Resulting far clip plane."
        },
        "dutch": {
          "type": "number",
          "description": "Resulting Dutch (roll) angle."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "fieldOfView",
        "orthographicSize",
        "nearClipPlane",
        "farClipPlane",
        "dutch",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

