---
name: animator-create
description: Create empty Unity `AnimatorController` assets at the given project paths. Each path must start with `Assets/` and end with `.controller`. Missing intermediate folders are created recursively. Pair with 'animator-modify' to add layers/states/parameters.
---

# Animator / Create

Create empty Unity `AnimatorController` assets at the given project paths. Each path must start with `Assets/` and end with `.controller`. Missing intermediate folders are created recursively, then `AssetDatabase.Refresh()` runs and the Editor windows repaint. Pair with 'animator-modify' to add layers, states, parameters, and transitions afterwards.

## Inputs

- `sourcePaths` — array of project-relative `.controller` paths to create.

## Behavior

Each path is validated independently: empty / non-`Assets/` / non-`.controller` paths are skipped and appended to `errors` instead of aborting the whole batch. Successfully created controllers are returned in `createdAssets` with their path, instance ID, and name.

## How to Call

```bash
unity-mcp-cli run-tool animator-create --input '{
  "sourcePaths": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool animator-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool animator-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sourcePaths` | `any` | Yes | The paths of the animator controller assets to create. Each path should start with 'Assets/' and end with '.controller'. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "sourcePaths": {
      "$ref": "#/$defs/System.String-1"
    }
  },
  "$defs": {
    "System.String-1": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "sourcePaths"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-CreateAnimatorResponse"
    }
  },
  "$defs": {
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-CreatedAnimatorInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-CreatedAnimatorInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-CreatedAnimatorInfo": {
      "type": "object",
      "properties": {
        "path": {
          "type": "string"
        },
        "instanceId": {
          "type": "integer"
        },
        "name": {
          "type": "string"
        }
      },
      "required": [
        "instanceId"
      ]
    },
    "System.Collections.Generic.List(System.String)": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-CreateAnimatorResponse": {
      "type": "object",
      "properties": {
        "createdAssets": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimatorTools-CreatedAnimatorInfo)"
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

