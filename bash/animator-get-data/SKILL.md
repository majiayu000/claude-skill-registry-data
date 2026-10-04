---
name: animator-get-data
description: Inspect a Unity `AnimatorController` asset — controller name, every parameter (name, type, defaults), every layer with its state machine, every state, and every transition. Pair with 'animator-modify' to write changes back.
---

# Animator / Get Data

Inspect a Unity `AnimatorController` asset. Returns the controller's name plus the full set of parameters, layers, states, and transitions — enough to drive a follow-up 'animator-modify' call with valid names.

## Inputs

- `animatorRef` — reference to the `AnimatorController` asset (path must start with `Assets/` and end with `.controller`).

## Returned fields

- `name` — controller asset name.
- `parameters` — every parameter (name, type, default value).
- `layers` — every layer with its state machine, default state, and weight.
- `states` — every state across all layers (name, speed, motion).
- `transitions` — every transition with its conditions, source, and destination.

## How to Call

```bash
unity-mcp-cli run-tool animator-get-data --input '{
  "animatorRef": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool animator-get-data --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool animator-get-data --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `animatorRef` | `any` | Yes | Reference to the AnimatorController asset. The path should start with 'Assets/' and end with '.controller'. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "animatorRef": {
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
    "animatorRef"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-GetAnimatorDataResponse"
    }
  },
  "$defs": {
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorParameterInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorParameterInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorParameterInfo": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "type": {
          "type": "string"
        },
        "defaultFloat": {
          "type": "number"
        },
        "defaultInt": {
          "type": "integer"
        },
        "defaultBool": {
          "type": "boolean"
        }
      },
      "required": [
        "defaultFloat",
        "defaultInt",
        "defaultBool"
      ]
    },
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorLayerInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorLayerInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorLayerInfo": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "defaultWeight": {
          "type": "number"
        },
        "blendingMode": {
          "type": "string"
        },
        "syncedLayerIndex": {
          "type": "integer"
        },
        "iKPass": {
          "type": "boolean"
        },
        "defaultStateName": {
          "type": "string"
        },
        "states": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorStateInfo)"
        },
        "subStateMachines": {
          "$ref": "#/$defs/System.Collections.Generic.List(System.String)"
        },
        "anyStateTransitions": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorTransitionInfo)"
        }
      },
      "required": [
        "defaultWeight",
        "syncedLayerIndex",
        "iKPass"
      ]
    },
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorStateInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorStateInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorStateInfo": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "tag": {
          "type": "string"
        },
        "speed": {
          "type": "number"
        },
        "speedParameterActive": {
          "type": "boolean"
        },
        "speedParameter": {
          "type": "string"
        },
        "cycleOffset": {
          "type": "number"
        },
        "cycleOffsetParameterActive": {
          "type": "boolean"
        },
        "cycleOffsetParameter": {
          "type": "string"
        },
        "mirror": {
          "type": "boolean"
        },
        "mirrorParameterActive": {
          "type": "boolean"
        },
        "mirrorParameter": {
          "type": "string"
        },
        "writeDefaultValues": {
          "type": "boolean"
        },
        "motionName": {
          "type": "string"
        },
        "transitions": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorTransitionInfo)"
        }
      },
      "required": [
        "speed",
        "speedParameterActive",
        "cycleOffset",
        "cycleOffsetParameterActive",
        "mirror",
        "mirrorParameterActive",
        "writeDefaultValues"
      ]
    },
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorTransitionInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorTransitionInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorTransitionInfo": {
      "type": "object",
      "properties": {
        "destinationStateName": {
          "type": "string"
        },
        "hasExitTime": {
          "type": "boolean"
        },
        "exitTime": {
          "type": "number"
        },
        "hasFixedDuration": {
          "type": "boolean"
        },
        "duration": {
          "type": "number"
        },
        "offset": {
          "type": "number"
        },
        "canTransitionToSelf": {
          "type": "boolean"
        },
        "conditions": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionInfo)"
        }
      },
      "required": [
        "hasExitTime",
        "exitTime",
        "hasFixedDuration",
        "duration",
        "offset",
        "canTransitionToSelf"
      ]
    },
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionInfo": {
      "type": "object",
      "properties": {
        "parameter": {
          "type": "string"
        },
        "mode": {
          "type": "string"
        },
        "threshold": {
          "type": "number"
        }
      },
      "required": [
        "threshold"
      ]
    },
    "System.Collections.Generic.List(System.String)": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-GetAnimatorDataResponse": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "parameters": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorParameterInfo)"
        },
        "layers": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorLayerInfo)"
        }
      }
    }
  },
  "required": [
    "result"
  ]
}
```

