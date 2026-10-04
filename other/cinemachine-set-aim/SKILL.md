---
name: cinemachine-set-aim
description: Add or replace the rotation-control (Aim) component of a `CinemachineCamera`, chosen by `AimType` (RotationComposer, HardLookAt, PanTilt, or None). Applies common params (screen X/Y, damping) to RotationComposer where applicable.
---

# Cinemachine / Set Aim

Add or replace the Aim (rotation-control) component of a `CinemachineCamera`. Any existing Aim component is removed first, then the chosen one is added — so this is destructive to the previous Aim component.

## Inputs

- `gameObjectRef` — the GameObject hosting the `CinemachineCamera` (required).
- `aimType` — `AimType` enum: `RotationComposer`, `HardLookAt`, `PanTilt`, or `None` (removes the Aim component).
- `screenX`, `screenY` — optional normalized on-screen target position for `RotationComposer` (`Composition.ScreenPosition`). Typically in the range -0.5..0.5 (0,0 = center).
- `damping` — optional uniform damping value (applies to `RotationComposer.Damping`).

## Behavior

Removes every existing `CinemachineRotationComposer`, `CinemachineHardLookAt`, and `CinemachinePanTilt` on the GameObject, then adds the requested one and applies the optional params. Marks the scene dirty and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool cinemachine-set-aim --input '{
  "gameObjectRef": "string_value",
  "aimType": "string_value",
  "screenX": "string_value",
  "screenY": "string_value",
  "damping": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool cinemachine-set-aim --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool cinemachine-set-aim --input-file - <<'EOF'
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
| `aimType` | `string` | Yes | Which rotation-control (Aim) component to use. |
| `screenX` | `any` | No | Normalized on-screen X target position for RotationComposer (Composition.ScreenPosition.x). |
| `screenY` | `any` | No | Normalized on-screen Y target position for RotationComposer (Composition.ScreenPosition.y). |
| `damping` | `any` | No | Uniform damping value applied where the component supports damping (RotationComposer). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "aimType": {
      "type": "string",
      "enum": [
        "None",
        "RotationComposer",
        "HardLookAt",
        "PanTilt"
      ]
    },
    "screenX": {
      "$ref": "#/$defs/System.Single"
    },
    "screenY": {
      "$ref": "#/$defs/System.Single"
    },
    "damping": {
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
    "gameObjectRef",
    "aimType"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Cinemachine-SetAimResponse"
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
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Cinemachine-SetAimResponse": {
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
        "aimType": {
          "type": "string",
          "description": "The AimType that was applied."
        },
        "componentName": {
          "type": "string",
          "description": "The Cinemachine component type name that was added (or 'None')."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

