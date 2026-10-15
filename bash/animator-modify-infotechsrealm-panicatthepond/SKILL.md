---
name: animator-modify
description: Apply a batch of modifications to a Unity `AnimatorController` — add/remove parameters, layers, states, and transitions; set default states; set state motion/speed. Use 'animator-get-data' first to discover valid names.
---

# Animator / Modify

Apply a batch of modifications to a Unity `AnimatorController` asset. Each modification is dispatched by its `AnimatorModificationType` discriminator. Use 'animator-get-data' first to discover valid names so the diff is targeted.

## Inputs

- `animatorRef` — reference to the `AnimatorController` asset (path must start with `Assets/` and end with `.controller`).
- `modifications` — array of `AnimatorModification` entries.

## Supported modification types

- `AddParameter` / `RemoveParameter` — manage controller parameters (float, int, bool, trigger).
- `AddLayer` / `RemoveLayer` — manage animator layers.
- `AddState` / `RemoveState` — manage states inside a specific layer.
- `SetDefaultState` — pick the default state for a layer.
- `AddTransition` / `RemoveTransition` — manage state-to-state transitions.
- `AddAnyStateTransition` — add a transition from Any State.
- `SetStateMotion` — assign an `AnimationClip` as a state's motion.
- `SetStateSpeed` — set a state's speed multiplier.

## Behavior

Per-modification errors are accumulated in the response's `errors` array instead of aborting the whole batch. The controller asset is marked dirty and saved after the modifications complete.

## How to Call

```bash
unity-mcp-cli run-tool animator-modify --input '{
  "animatorRef": "string_value",
  "modifications": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool animator-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool animator-modify --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `animatorRef` | `any` | Yes | Reference to the AnimatorController asset to modify. |
| `modifications` | `any` | Yes | Array of modifications to apply to the controller. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "animatorRef": {
      "$ref": "#/$defs/AIGD.AssetObjectRef"
    },
    "modifications": {
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorModification-1"
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
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorModification": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "AddParameter",
            "RemoveParameter",
            "AddLayer",
            "RemoveLayer",
            "AddState",
            "RemoveState",
            "SetDefaultState",
            "AddTransition",
            "RemoveTransition",
            "AddAnyStateTransition",
            "SetStateMotion",
            "SetStateSpeed"
          ],
          "description": "Modification type. Properties below are used conditionally based on this value."
        },
        "parameterName": {
          "type": "string",
          "description": "Parameter name. Required for: AddParameter, RemoveParameter."
        },
        "parameterType": {
          "type": "string",
          "description": "Parameter type: Float, Int, Bool, Trigger. Required for: AddParameter."
        },
        "defaultFloat": {
          "type": "number",
          "description": "Default float value. Optional for: AddParameter (Float type)."
        },
        "defaultInt": {
          "type": "integer",
          "description": "Default int value. Optional for: AddParameter (Int type)."
        },
        "defaultBool": {
          "type": "boolean",
          "description": "Default bool value. Optional for: AddParameter (Bool type)."
        },
        "layerName": {
          "type": "string",
          "description": "Layer name. Required for: AddLayer, RemoveLayer, AddState, RemoveState, SetDefaultState, AddTransition, RemoveTransition, AddAnyStateTransition, SetStateMotion, SetStateSpeed."
        },
        "stateName": {
          "type": "string",
          "description": "State name. Required for: AddState, RemoveState, SetDefaultState, SetStateMotion, SetStateSpeed."
        },
        "motionAssetPath": {
          "type": "string",
          "description": "Asset path to AnimationClip. Optional for: AddState. Required for: SetStateMotion."
        },
        "speed": {
          "type": "number",
          "description": "Speed multiplier. Required for: SetStateSpeed."
        },
        "sourceStateName": {
          "type": "string",
          "description": "Source state name. Required for: AddTransition, RemoveTransition."
        },
        "destinationStateName": {
          "type": "string",
          "description": "Destination state name. Required for: AddTransition, RemoveTransition, AddAnyStateTransition."
        },
        "hasExitTime": {
          "type": "boolean",
          "description": "Whether transition waits for exit time. Optional for: AddTransition, AddAnyStateTransition."
        },
        "exitTime": {
          "type": "number",
          "description": "Normalized exit time (0-1). Optional for: AddTransition, AddAnyStateTransition."
        },
        "duration": {
          "type": "number",
          "description": "Transition blend duration. Optional for: AddTransition, AddAnyStateTransition."
        },
        "hasFixedDuration": {
          "type": "boolean",
          "description": "Whether duration is in seconds (true) or normalized (false). Optional for: AddTransition, AddAnyStateTransition."
        },
        "conditions": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionData-1",
          "description": "Transition conditions. Optional for: AddTransition, AddAnyStateTransition."
        }
      },
      "required": [
        "type"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionData-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionData"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorConditionData": {
      "type": "object",
      "properties": {
        "parameter": {
          "type": "string",
          "description": "Parameter name for the condition."
        },
        "mode": {
          "type": "string",
          "description": "Condition mode: If, IfNot, Greater, Less, Equals, NotEqual."
        },
        "threshold": {
          "type": "number",
          "description": "Threshold value for the condition."
        }
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorModification-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorModification"
      }
    }
  },
  "required": [
    "animatorRef",
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-ModifyAnimatorResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Animation.ModifyAnimatorInfo": {
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
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-ModifyAnimatorResponse": {
      "type": "object",
      "properties": {
        "modifiedAsset": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.ModifyAnimatorInfo"
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

