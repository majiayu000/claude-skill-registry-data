---
name: animation-modify
description: Apply a batch of modifications to a Unity `AnimationClip` — set/remove float curves, clear all curves, set frame rate / wrap mode / legacy flag, add or clear animation events. Use 'animation-get-data' first to discover valid curve bindings.
---

# Animation / Modify

Apply a batch of modifications to a Unity `AnimationClip` asset. Each modification is dispatched by its `ModificationType` discriminator. Use 'animation-get-data' first to discover valid property names and existing curves so the diff is targeted.

## Inputs

- `animRef` — reference to the `AnimationClip` asset (path must start with `Assets/` and end with `.anim`).
- `modifications` — array of `AnimationModification` entries.

## Supported modification types

- `SetCurve` — add or replace a float animation curve (`path`, `propertyName`, `type`, `keyframes`).
- `RemoveCurve` — remove a specific binding.
- `ClearCurves` — remove every curve from the clip.
- `SetFrameRate` — set the clip's frame rate.
- `SetWrapMode` — set the clip's `WrapMode`.
- `SetLegacy` — toggle the legacy animation flag.
- `AddEvent` — append an animation event (`time`, `functionName`, `intParameter`, `floatParameter`, `stringParameter`).
- `ClearEvents` — remove every animation event.

## Behavior

Per-modification errors are accumulated in the response's `errors` array instead of aborting the whole batch. Events are applied as a single rewrite after all per-entry mutations finish.

## How to Call

```bash
unity-mcp-cli run-tool animation-modify --input '{
  "animRef": "string_value",
  "modifications": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool animation-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool animation-modify --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `animRef` | `any` | Yes | Reference to the AnimationClip asset to modify. |
| `modifications` | `any` | Yes | Array of modifications to apply to the clip. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "animRef": {
      "$ref": "#/$defs/AIGD.AssetObjectRef"
    },
    "modifications": {
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationModification-1"
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
    "AIGD.AssetObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "$ref": "#/$defs/UnityEngine.EntityId",
          "description": "instanceID of the UnityEngine.Object. If this is '0' and 'assetPath' and 'assetGuid' is not provided, empty or null, then it will be used as 'null'."
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
      "description": "Reference to UnityEngine.Object asset instance. It could be Material, ScriptableObject, Prefab, and any other Asset. Anything located in the Assets and Packages folders."
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationModification": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "SetCurve",
            "RemoveCurve",
            "ClearCurves",
            "SetFrameRate",
            "SetWrapMode",
            "SetLegacy",
            "AddEvent",
            "ClearEvents"
          ],
          "description": "Modification type. Properties below are used conditionally based on this value."
        },
        "relativePath": {
          "type": "string",
          "description": "Path to target GameObject relative to the root (empty for root). Used by: SetCurve, RemoveCurve."
        },
        "componentType": {
          "type": "string",
          "description": "Component type name (e.g., 'Transform', 'SpriteRenderer'). Required for: SetCurve, RemoveCurve."
        },
        "propertyName": {
          "type": "string",
          "description": "Property to animate (e.g., 'localPosition.x', 'm_LocalScale.y'). Required for: SetCurve, RemoveCurve."
        },
        "keyframes": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationKeyframe-1",
          "description": "Keyframes for the curve. Required for: SetCurve."
        },
        "frameRate": {
          "type": "number",
          "description": "Frames per second. Required for: SetFrameRate."
        },
        "wrapMode": {
          "type": "string",
          "enum": [
            "Default",
            "Clamp",
            "Clamp",
            "Loop",
            "PingPong",
            "ClampForever"
          ],
          "description": "How animation behaves at boundaries. Required for: SetWrapMode."
        },
        "legacy": {
          "type": "boolean",
          "description": "Use legacy animation system. Required for: SetLegacy."
        },
        "time": {
          "type": "number",
          "description": "Event trigger time in seconds. Required for: AddEvent."
        },
        "functionName": {
          "type": "string",
          "description": "Function to invoke. Required for: AddEvent."
        },
        "stringParameter": {
          "type": "string",
          "description": "String parameter passed to the function. Optional for: AddEvent."
        },
        "floatParameter": {
          "type": "number",
          "description": "Float parameter passed to the function. Optional for: AddEvent."
        },
        "intParameter": {
          "type": "integer",
          "description": "Integer parameter passed to the function. Optional for: AddEvent."
        }
      },
      "required": [
        "type"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationKeyframe-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationKeyframe"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationKeyframe": {
      "type": "object",
      "properties": {
        "time": {
          "type": "number",
          "description": "Time in seconds."
        },
        "value": {
          "type": "number",
          "description": "Value at this keyframe."
        },
        "inTangent": {
          "type": "number",
          "description": "Incoming tangent (slope). Default: 0."
        },
        "outTangent": {
          "type": "number",
          "description": "Outgoing tangent (slope). Default: 0."
        },
        "weightedMode": {
          "type": "string",
          "enum": [
            "None",
            "In",
            "Out",
            "Both"
          ],
          "description": "Weighted mode: None (0), In (1), Out (2), Both (3). Default: None."
        },
        "inWeight": {
          "type": "number",
          "description": "Incoming weight. Default: 0.33."
        },
        "outWeight": {
          "type": "number",
          "description": "Outgoing weight. Default: 0.33."
        }
      },
      "required": [
        "time",
        "value"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationModification-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationModification"
      }
    }
  },
  "required": [
    "animRef",
    "modifications"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-ModifyAnimationResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-ModifyAnimationInfo": {
      "type": "object",
      "properties": {
        "path": {
          "type": "string"
        },
        "instanceId": {
          "$ref": "#/$defs/UnityEngine.EntityId"
        },
        "name": {
          "type": "string"
        }
      },
      "required": [
        "instanceId"
      ]
    },
    "UnityEngine.EntityId": {
      "type": "string",
      "pattern": "^[0-9]+$"
    },
    "System.Collections.Generic.List(System.String)": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-ModifyAnimationResponse": {
      "type": "object",
      "properties": {
        "modifiedAsset": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-ModifyAnimationInfo"
        },
        "errors": {
          "$ref": "#/$defs/System.Collections.Generic.List(System.String)"
        }
      }
    }
  },
  "required": [
    "result"
  ]
}
```

