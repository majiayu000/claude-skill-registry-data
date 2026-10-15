---
name: inputsystem-save
description: Re-serialize a `.inputactions` InputActionAsset to disk and re-import it. Useful to force-persist an asset after external edits.
---

# InputSystem / Save Asset

Persist an `InputActionAsset` to its `.inputactions` file. The mutation tools save automatically; this tool is an explicit save for cases where the on-disk JSON should be regenerated (e.g. after edits made outside these tools).

## Inputs

- `assetPath` — required. Path to the existing `.inputactions` asset.

## Behavior

Loads the asset, re-serializes it to JSON via `ToJson()`, writes the file, and re-imports it into the AssetDatabase. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool inputsystem-save --input '{
  "assetPath": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool inputsystem-save --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool inputsystem-save --input-file - <<'EOF'
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-SaveResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_InputSystem-SaveResponse": {
      "type": "object",
      "properties": {
        "assetPath": {
          "type": "string",
          "description": "Path of the saved asset."
        },
        "actionMapCount": {
          "type": "integer",
          "description": "Number of ActionMaps in the saved asset."
        },
        "controlSchemeCount": {
          "type": "integer",
          "description": "Number of control schemes in the saved asset."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "actionMapCount",
        "controlSchemeCount",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

