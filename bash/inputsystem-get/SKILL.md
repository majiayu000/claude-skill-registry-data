---
name: inputsystem-get
description: Read the full structure of a `.inputactions` InputActionAsset — its ActionMaps, Actions (type / expectedControlType), Bindings (path / groups / interactions / processors / index) and Control Schemes. Read-only.
---

# InputSystem / Get Asset Structure

Inspect an `InputActionAsset` and return its structure so you can discover map names, action names, and binding indices to drive the other tools.

## Inputs

- `assetPath` — required. Path to the existing `.inputactions` asset.

## Behavior

Loads the asset and walks its ActionMaps → Actions → Bindings plus its Control Schemes, returning a compact structured summary (including each binding's zero-based index, whether it is a composite, and its part metadata). Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool inputsystem-get --input '{
  "assetPath": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool inputsystem-get --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool inputsystem-get --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assetPath` | `string` | Yes | 'Assets/'-rooted path to the existing '.inputactions' asset. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "assetPath": {
      "type": "string"
    }
  },
  "required": [
    "assetPath"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-GetResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-MapInfo-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-MapInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-MapInfo": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "ActionMap name."
        },
        "actions": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-ActionInfo-1",
          "description": "Actions in the map."
        }
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-ActionInfo-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-ActionInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-ActionInfo": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Action name."
        },
        "type": {
          "type": "string",
          "description": "Action type (Button / Value / PassThrough)."
        },
        "expectedControlType": {
          "type": "string",
          "description": "Expected control type, or null."
        },
        "bindings": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-BindingInfo-1",
          "description": "Bindings on the action (with their indices)."
        }
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-BindingInfo-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-BindingInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-BindingInfo": {
      "type": "object",
      "properties": {
        "index": {
          "type": "integer",
          "description": "Zero-based index of the binding within the action."
        },
        "path": {
          "type": "string",
          "description": "Control path, or empty for a composite root."
        },
        "name": {
          "type": "string",
          "description": "Binding/part name (e.g. composite part 'up'), or empty."
        },
        "groups": {
          "type": "string",
          "description": "Control-scheme group(s)."
        },
        "interactions": {
          "type": "string",
          "description": "Interactions."
        },
        "processors": {
          "type": "string",
          "description": "Processors."
        },
        "isComposite": {
          "type": "boolean",
          "description": "True if this binding is a composite root."
        },
        "isPartOfComposite": {
          "type": "boolean",
          "description": "True if this binding is a part of a composite."
        }
      },
      "required": [
        "index",
        "isComposite",
        "isPartOfComposite"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-SchemeInfo-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-SchemeInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-SchemeInfo": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Control scheme name."
        },
        "bindingGroup": {
          "type": "string",
          "description": "Binding group string for the scheme."
        },
        "devices": {
          "$ref": "#/$defs/System.String-1",
          "description": "Device requirements (prefixed '(optional)' when optional)."
        }
      }
    },
    "System.String-1": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-GetResponse": {
      "type": "object",
      "properties": {
        "assetPath": {
          "type": "string",
          "description": "Path of the inspected asset."
        },
        "actionMaps": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-MapInfo-1",
          "description": "ActionMaps in the asset."
        },
        "controlSchemes": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-SchemeInfo-1",
          "description": "Control schemes in the asset."
        }
      }
    }
  },
  "required": [
    "result"
  ]
}
```

