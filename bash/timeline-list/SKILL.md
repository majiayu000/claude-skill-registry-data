---
name: timeline-list
description: List every `TimelineAsset` in the project with its path, GUID, track count and duration. Read-only.
---

# Timeline / List TimelineAssets

Search the project AssetDatabase for `TimelineAsset` (.playable) assets and report each one's path, GUID, track count, and computed duration.

## Inputs

- `includeTrackCount` (bool, default true) — when true, load each asset to count its output tracks; when false, skip loading (faster, no counts).

## Behavior

Runs `AssetDatabase.FindAssets("t:TimelineAsset")`, resolves each to a path, and (optionally) loads it for track count + duration. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-list --input '{
  "includeTrackCount": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeTrackCount` | `boolean` | No | If true (default), load each asset to report its track count and duration; if false, skip loading. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "includeTrackCount": {
      "type": "boolean"
    }
  }
}
```

## Output

### Output JSON Schema

```json
{
  "type": "object",
  "properties": {
    "result": {
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-ListResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-ListItem-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-ListItem"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-ListItem": {
      "type": "object",
      "properties": {
        "assetPath": {
          "type": "string",
          "description": "Project path of the TimelineAsset."
        },
        "guid": {
          "type": "string",
          "description": "Asset GUID."
        },
        "trackCount": {
          "type": "integer",
          "description": "Number of output tracks (0 when includeTrackCount is false)."
        },
        "duration": {
          "type": "number",
          "description": "Computed duration in seconds (0 when includeTrackCount is false)."
        }
      },
      "required": [
        "trackCount",
        "duration"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-ListResponse": {
      "type": "object",
      "properties": {
        "count": {
          "type": "integer",
          "description": "Number of TimelineAssets found."
        },
        "timelines": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-ListItem-1",
          "description": "The TimelineAssets in the project."
        }
      },
      "required": [
        "count"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

