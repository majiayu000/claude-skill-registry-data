---
name: timeline-create
description: Create a new empty `TimelineAsset` (.playable) at a project path. Optionally set the frame rate and a fixed duration mode. Returns the created asset path and GUID.
---

# Timeline / Create TimelineAsset

Create a new `TimelineAsset` and save it to disk at an `Assets/`-rooted `.playable` path. A `TimelineAsset` is the authoring container holding tracks, clips, and markers for a cutscene or sequence; a scene `PlayableDirector` plays it.

## Inputs

- `assetPath` — required `Assets/...`-rooted path ending in `.playable`. Missing folders are created.
- `frameRate` — optional editor frame rate of the timeline (default 60).
- `durationMode` — optional `BasedOnClips` (default) or `FixedLength`.
- `fixedDuration` — optional duration in seconds, used when `durationMode` is `FixedLength`.

## Behavior

Creates the intermediate folders, instantiates a `TimelineAsset`, applies the editor settings, writes it via `AssetDatabase.CreateAsset`, saves, and returns the path + GUID. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-create --input '{
  "assetPath": "string_value",
  "frameRate": 0,
  "durationMode": "string_value",
  "fixedDuration": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-create --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-create --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assetPath` | `string` | Yes | Assets-rooted path ending in '.playable' (e.g. 'Assets/Timelines/Intro.playable'). |
| `frameRate` | `number` | No | Editor frame rate of the timeline (default 60). |
| `durationMode` | `string` | No | Duration mode: 'BasedOnClips' (default) or 'FixedLength'. |
| `fixedDuration` | `number` | No | Fixed duration in seconds, used only when durationMode is 'FixedLength'. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "assetPath": {
      "type": "string"
    },
    "frameRate": {
      "type": "number"
    },
    "durationMode": {
      "type": "string"
    },
    "fixedDuration": {
      "type": "number"
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-CreateResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Timeline-CreateResponse": {
      "type": "object",
      "properties": {
        "assetPath": {
          "type": "string",
          "description": "Project path of the created TimelineAsset."
        },
        "guid": {
          "type": "string",
          "description": "GUID of the created asset."
        },
        "frameRate": {
          "type": "number",
          "description": "Resolved editor frame rate of the timeline."
        },
        "durationMode": {
          "type": "string",
          "description": "Resolved duration mode."
        },
        "success": {
          "type": "boolean",
          "description": "Whether the operation succeeded."
        }
      },
      "required": [
        "frameRate",
        "success"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

