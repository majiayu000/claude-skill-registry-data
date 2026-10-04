---
name: animation-get-data
description: Inspect a Unity `AnimationClip` asset — name, length, frame rate, wrap mode, looping/legacy/humanMotion flags, local bounds, and the full set of float curves, object-reference curves, and events. Pair with 'animation-modify' to write changes back.
---

# Animation / Get Data

Inspect a Unity `AnimationClip` asset. Returns the high-level clip metadata plus the complete set of float curve bindings, object-reference curve bindings, and animation events. Pair with 'animation-modify' to write changes back.

## Inputs

- `animRef` — reference to the `AnimationClip` asset (path must start with `Assets/` and end with `.anim`).

## Returned fields

- `name`, `length`, `frameRate`, `wrapMode`, `isLooping`, `hasGenericRootTransform`, `hasMotionCurves`, `hasMotionFloatCurves`, `hasRootCurves`, `humanMotion`, `legacy`, `localBounds`, `empty`.
- `curveBindings` — float curve bindings (`path`, `propertyName`, `type`, `isPPtrCurve`, `isDiscreteCurve`, `keyframeCount`).
- `objectReferenceBindings` — object-reference curve bindings (same shape as `curveBindings`).
- `events` — animation events (`time`, `functionName`, `intParameter`, `floatParameter`, `stringParameter`).

## How to Call

```bash
unity-mcp-cli run-tool animation-get-data --input '{
  "animRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool animation-get-data --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool animation-get-data --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `animRef` | `any` | Yes | Reference to the animation asset. The path should start with 'Assets/' and end with '.anim'. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "animRef": {
      "$ref": "#/$defs/AIGD.AssetObjectRef"
    }
  },
  "$defs": {
    "System.Type": {
      "type": "string"
    },
    "AIGD.AssetObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "type": "integer",
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
    }
  },
  "required": [
    "animRef"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-GetDataResponse"
    }
  },
  "$defs": {
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CurveBindingInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CurveBindingInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CurveBindingInfo": {
      "type": "object",
      "properties": {
        "path": {
          "type": "string"
        },
        "propertyName": {
          "type": "string"
        },
        "type": {
          "type": "string"
        },
        "isPPtrCurve": {
          "type": "boolean"
        },
        "isDiscreteCurve": {
          "type": "boolean"
        },
        "keyframeCount": {
          "type": "integer"
        }
      },
      "required": [
        "isPPtrCurve",
        "isDiscreteCurve",
        "keyframeCount"
      ]
    },
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-AnimationEventInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-AnimationEventInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-AnimationEventInfo": {
      "type": "object",
      "properties": {
        "time": {
          "type": "number"
        },
        "functionName": {
          "type": "string"
        },
        "intParameter": {
          "type": "integer"
        },
        "floatParameter": {
          "type": "number"
        },
        "stringParameter": {
          "type": "string"
        }
      },
      "required": [
        "time",
        "intParameter",
        "floatParameter"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-GetDataResponse": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "length": {
          "type": "number"
        },
        "frameRate": {
          "type": "number"
        },
        "wrapMode": {
          "type": "string"
        },
        "isLooping": {
          "type": "boolean"
        },
        "hasGenericRootTransform": {
          "type": "boolean"
        },
        "hasMotionCurves": {
          "type": "boolean"
        },
        "hasMotionFloatCurves": {
          "type": "boolean"
        },
        "hasRootCurves": {
          "type": "boolean"
        },
        "humanMotion": {
          "type": "boolean"
        },
        "legacy": {
          "type": "boolean"
        },
        "localBounds": {
          "type": "string"
        },
        "empty": {
          "type": "boolean"
        },
        "curveBindings": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CurveBindingInfo)"
        },
        "objectReferenceBindings": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CurveBindingInfo)"
        },
        "events": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-AnimationEventInfo)"
        }
      },
      "required": [
        "length",
        "frameRate",
        "isLooping",
        "hasGenericRootTransform",
        "hasMotionCurves",
        "hasMotionFloatCurves",
        "hasRootCurves",
        "humanMotion",
        "legacy",
        "empty"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

