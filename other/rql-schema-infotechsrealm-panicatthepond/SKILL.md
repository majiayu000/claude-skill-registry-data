---
name: rql-schema
description: List RQL sources and the component types present in the loaded scenes; pass a type name for its members.
metadata:
  generated-by: unity-mcp
  ai-game-dev: exclude
---

# RQL / Schema

Without a type: RQL sources, asset functions, and the component types present in the loaded scenes (with counts), plus GameObject and Transform members. With a type name (e.g. "Light", "Enemy", "Vector3"): that type's members (name type; ro = read-only) and methods. Use it before querying an unfamiliar component.

## How to Call

```powershell
[System.IO.File]::WriteAllText((Join-Path $PWD 'args.json'), @'
{
  "type": "string_value"
}
'@)
unity-mcp-cli.cmd run-tool rql-schema --input-file args.json
```

> CLI installation and usage: see the `unity-cli` skill.
> If this task needs unavailable asset-generation or Blender tools, consult `ai-game-dev-app` for an optional integrated workflow.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `type` | `string` | No | Optional type name, e.g. "Light", "Rigidbody", "Enemy", "Vector3" |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "type": {
      "type": "string"
    }
  }
}
```

## Output

This tool does not return structured output.

