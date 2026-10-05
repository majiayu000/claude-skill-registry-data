---
name: particle-system-modify
description: Modify a `UnityEngine.ParticleSystem` component on a GameObject. Pass `SerializedMember` payloads only for the modules you want to change; everything else is left alone. Use 'particle-system-get' first to inspect the current structure.
---

# ParticleSystem / Modify

Modify a `UnityEngine.ParticleSystem` component on a GameObject. Pass `SerializedMember` payloads only for the modules you want to change; omitted modules are left untouched. Use 'particle-system-get' first to inspect the current structure so the diff is targeted.

## Inputs

- `gameObjectRef` — the GameObject hosting the `ParticleSystem` component (required).
- `componentRef` — optional. Resolves a specific `ParticleSystem` when the GameObject has more than one; otherwise the first `ParticleSystem` found is used.
- `main`, `emission`, `shape`, `velocityOverLifetime`, `limitVelocityOverLifetime`, `inheritVelocity`, `lifetimeByEmitterSpeed`, `forceOverLifetime`, `colorOverLifetime`, `colorBySpeed`, `sizeOverLifetime`, `sizeBySpeed`, `rotationOverLifetime`, `rotationBySpeed`, `externalForces`, `noise`, `collision`, `trigger`, `subEmitters`, `textureSheetAnimation`, `lights`, `trails`, `customData`, `renderer` — optional `SerializedMember` payloads per module. Include only the properties you want to change.

## Behavior

Each non-null module is applied via `Reflector.TryModify` and logged with a `[ModuleName]` prefix in the response's `logs` array. The `renderer` payload targets the sibling `UnityEngine.ParticleSystemRenderer` component on the same GameObject; if absent, the call logs the miss instead of throwing. When at least one module was modified, the GameObject and the `ParticleSystem` are marked dirty so the change persists. The whole call runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool particle-system-modify --input '{
  "gameObjectRef": "string_value",
  "componentRef": "string_value",
  "main": "string_value",
  "emission": "string_value",
  "shape": "string_value",
  "velocityOverLifetime": "string_value",
  "limitVelocityOverLifetime": "string_value",
  "inheritVelocity": "string_value",
  "lifetimeByEmitterSpeed": "string_value",
  "forceOverLifetime": "string_value",
  "colorOverLifetime": "string_value",
  "colorBySpeed": "string_value",
  "sizeOverLifetime": "string_value",
  "sizeBySpeed": "string_value",
  "rotationOverLifetime": "string_value",
  "rotationBySpeed": "string_value",
  "externalForces": "string_value",
  "noise": "string_value",
  "collision": "string_value",
  "trigger": "string_value",
  "subEmitters": "string_value",
  "textureSheetAnimation": "string_value",
  "lights": "string_value",
  "trails": "string_value",
  "customData": "string_value",
  "renderer": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool particle-system-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool particle-system-modify --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `any` | Yes | Reference to the GameObject containing the ParticleSystem component. |
| `componentRef` | `any` | No | Optional reference to a specific ParticleSystem component if the GameObject has multiple. If not provided, uses the first ParticleSystem found. |
| `main` | `any` | No | Main module data to apply. Only include properties you want to change. |
| `emission` | `any` | No | Emission module data to apply. Only include properties you want to change. |
| `shape` | `any` | No | Shape module data to apply. Only include properties you want to change. |
| `velocityOverLifetime` | `any` | No | Velocity over Lifetime module data to apply. Only include properties you want to change. |
| `limitVelocityOverLifetime` | `any` | No | Limit Velocity over Lifetime module data to apply. Only include properties you want to change. |
| `inheritVelocity` | `any` | No | Inherit Velocity module data to apply. Only include properties you want to change. |
| `lifetimeByEmitterSpeed` | `any` | No | Lifetime by Emitter Speed module data to apply. Only include properties you want to change. |
| `forceOverLifetime` | `any` | No | Force over Lifetime module data to apply. Only include properties you want to change. |
| `colorOverLifetime` | `any` | No | Color over Lifetime module data to apply. Only include properties you want to change. |
| `colorBySpeed` | `any` | No | Color by Speed module data to apply. Only include properties you want to change. |
| `sizeOverLifetime` | `any` | No | Size over Lifetime module data to apply. Only include properties you want to change. |
| `sizeBySpeed` | `any` | No | Size by Speed module data to apply. Only include properties you want to change. |
| `rotationOverLifetime` | `any` | No | Rotation over Lifetime module data to apply. Only include properties you want to change. |
| `rotationBySpeed` | `any` | No | Rotation by Speed module data to apply. Only include properties you want to change. |
| `externalForces` | `any` | No | External Forces module data to apply. Only include properties you want to change. |
| `noise` | `any` | No | Noise module data to apply. Only include properties you want to change. |
| `collision` | `any` | No | Collision module data to apply. Only include properties you want to change. |
| `trigger` | `any` | No | Trigger module data to apply. Only include properties you want to change. |
| `subEmitters` | `any` | No | Sub Emitters module data to apply. Only include properties you want to change. |
| `textureSheetAnimation` | `any` | No | Texture Sheet Animation module data to apply. Only include properties you want to change. |
| `lights` | `any` | No | Lights module data to apply. Only include properties you want to change. |
| `trails` | `any` | No | Trails module data to apply. Only include properties you want to change. |
| `customData` | `any` | No | Custom Data module data to apply. Only include properties you want to change. |
| `renderer` | `any` | No | Renderer module data to apply. Only include properties you want to change. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "$ref": "#/$defs/AIGD.GameObjectRef"
    },
    "componentRef": {
      "$ref": "#/$defs/AIGD.ComponentRef"
    },
    "main": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "emission": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "shape": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "velocityOverLifetime": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "limitVelocityOverLifetime": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "inheritVelocity": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "lifetimeByEmitterSpeed": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "forceOverLifetime": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "colorOverLifetime": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "colorBySpeed": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "sizeOverLifetime": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "sizeBySpeed": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "rotationOverLifetime": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "rotationBySpeed": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "externalForces": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "noise": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "collision": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "trigger": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "subEmitters": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "textureSheetAnimation": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "lights": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "trails": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "customData": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
    },
    "renderer": {
      "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
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
    "com.IvanMurzak.ReflectorNet.Model.SerializedMemberList": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember"
      }
    },
    "com.IvanMurzak.ReflectorNet.Model.SerializedMember": {
      "type": "object",
      "properties": {
        "typeName": {
          "type": "string",
          "description": "Full type name. Eg: 'System.String', 'System.Int32', 'UnityEngine.Vector3', etc."
        },
        "name": {
          "type": "string",
          "description": "Object name."
        },
        "value": {
          "description": "Value of the object, serialized as a non stringified JSON element. Can be null if the value is not set. Can be default value if the value is an empty object or array json."
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember",
            "description": "Nested field value."
          },
          "description": "Fields of the object, serialized as a list of 'SerializedMember'."
        },
        "props": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/com.IvanMurzak.ReflectorNet.Model.SerializedMember",
            "description": "Nested property value."
          },
          "description": "Properties of the object, serialized as a list of 'SerializedMember'."
        }
      },
      "required": [
        "typeName"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.ParticleSystem.Editor.ModifyParticleSystemResponse",
      "description": "Response containing the result of modifying a ParticleSystem."
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
    "System.String-1": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "com.IvanMurzak.Unity.MCP.ParticleSystem.Editor.ModifyParticleSystemResponse": {
      "type": "object",
      "properties": {
        "success": {
          "type": "boolean",
          "description": "Whether the modification was successful."
        },
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the GameObject containing the ParticleSystem component."
        },
        "componentRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the modified ParticleSystem component."
        },
        "componentIndex": {
          "type": "integer",
          "description": "Index of the ParticleSystem component in the GameObject's component list."
        },
        "logs": {
          "$ref": "#/$defs/System.String-1",
          "description": "Log of modifications made and any warnings/errors encountered."
        }
      },
      "required": [
        "success",
        "componentIndex"
      ],
      "description": "Response containing the result of modifying a ParticleSystem."
    }
  },
  "required": [
    "result"
  ]
}
```

