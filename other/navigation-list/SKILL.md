---
name: navigation-list
description: List every `NavMeshSurface` and `NavMeshAgent` in the active scene with their key settings (agent type, baked-data presence for surfaces; speed, on-NavMesh state for agents). Read-only.
---

# Navigation / List Surfaces and Agents

Enumerate the NavMesh components in the active scene so you can inspect what is set up.

## Inputs

- `includeInactive` (bool, default true) — include components on inactive/disabled GameObjects.

## Behavior

Finds all `NavMeshSurface` and `NavMeshAgent` instances, reports each surface's agent-type id and whether it has baked NavMeshData, and each agent's agent-type id, speed, and whether it is currently on a NavMesh. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool navigation-list --input '{
  "includeInactive": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool navigation-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool navigation-list --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `includeInactive` | `boolean` | No | If true (default), include components on inactive/disabled GameObjects. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "includeInactive": {
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
      "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-NavigationListResponse"
    }
  },
  "$defs": {
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-SurfaceListItem-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-SurfaceListItem"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-SurfaceListItem": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the surface GameObject."
        },
        "surfaceRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the NavMeshSurface component."
        },
        "name": {
          "type": "string",
          "description": "Name of the GameObject."
        },
        "agentTypeId": {
          "type": "integer",
          "description": "Agent-type id this surface bakes for."
        },
        "hasNavMeshData": {
          "type": "boolean",
          "description": "Whether the surface has baked NavMeshData."
        }
      },
      "required": [
        "agentTypeId",
        "hasNavMeshData"
      ]
    },
    "AIGD.GameObjectRef": {
      "type": "object",
      "properties": {
        "instanceID": {
          "type": "integer",
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
          "type": "integer",
          "description": "instanceID of the UnityEngine.Object. If this is '0', then it will be used as 'null'."
        }
      },
      "required": [
        "index",
        "instanceID"
      ],
      "description": "Component reference. Used to find a Component at GameObject."
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-AgentListItem-1": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-AgentListItem"
      }
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-AgentListItem": {
      "type": "object",
      "properties": {
        "gameObjectRef": {
          "$ref": "#/$defs/AIGD.GameObjectRef",
          "description": "Reference to the agent GameObject."
        },
        "agentRef": {
          "$ref": "#/$defs/AIGD.ComponentRef",
          "description": "Reference to the NavMeshAgent component."
        },
        "name": {
          "type": "string",
          "description": "Name of the GameObject."
        },
        "agentTypeId": {
          "type": "integer",
          "description": "Agent-type id of the agent."
        },
        "speed": {
          "type": "number",
          "description": "Movement speed of the agent."
        },
        "isOnNavMesh": {
          "type": "boolean",
          "description": "Whether the agent is currently on a baked NavMesh."
        }
      },
      "required": [
        "agentTypeId",
        "speed",
        "isOnNavMesh"
      ]
    },
    "com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-NavigationListResponse": {
      "type": "object",
      "properties": {
        "surfaceCount": {
          "type": "integer",
          "description": "Number of NavMeshSurfaces found."
        },
        "agentCount": {
          "type": "integer",
          "description": "Number of NavMeshAgents found."
        },
        "surfaces": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-SurfaceListItem-1",
          "description": "The NavMeshSurfaces in the active scene."
        },
        "agents": {
          "$ref": "#/$defs/com.IvanMurzak.Unity.MCP.Editor.API.Tool_Navigation-AgentListItem-1",
          "description": "The NavMeshAgents in the active scene."
        }
      },
      "required": [
        "surfaceCount",
        "agentCount"
      ]
    }
  },
  "required": [
    "result"
  ]
}
```

