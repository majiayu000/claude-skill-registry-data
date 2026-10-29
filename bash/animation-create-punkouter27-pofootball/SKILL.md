---
name: animation-create
description: Create empty Unity `AnimationClip` assets at the given project paths. Each path must start with `Assets/` and end with `.anim`. Missing intermediate folders are created recursively. Pair with 'animation-modify' to populate curves and events.
---

# Animation / Create

Create empty Unity `AnimationClip` assets at the given project paths. Each path must start with `Assets/` and end with `.anim`. Missing intermediate folders are created recursively, then `AssetDatabase.Refresh()` runs and the Editor windows repaint. Pair with 'animation-modify' to populate curves and events afterwards.

## Inputs

- `sourcePaths` — array of project-relative `.anim` paths to create.

## Behavior

Each path is validated independently: empty / non-`Assets/` / non-`.anim` paths are skipped and appended to `errors` instead of aborting the whole batch. Successfully created clips are returned in `createdAssets` with their path, instance ID, and name.

## How to Call

```bash
unity-mcp-cli run-tool animation-create --input '{
  "sourcePaths": "string_value"
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool animation-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool animation-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sourcePaths` | `any` | Yes | The paths of the animation assets to create. Each path should start with 'Assets/' and end with '.anim'. |

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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CreateAnimationResponse"
    }
  },
  "$defs": {
    "System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CreatedAnimationInfo)": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CreatedAnimationInfo"
      }
    },
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CreatedAnimationInfo": {
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
    "com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CreateAnimationResponse": {
      "type": "object",
      "properties": {
        "createdAssets": {
          "$ref": "#/$defs/System.Collections.Generic.List(com.IvanMurzak.Unity.MCP.Animation.AnimationTools-CreatedAnimationInfo)"
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

