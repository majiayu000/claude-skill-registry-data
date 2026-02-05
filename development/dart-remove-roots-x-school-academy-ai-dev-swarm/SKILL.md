---
name: dart-remove-roots
description: "To remove previously registered Dart project roots, revoke tool access by removing those roots."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"remove_roots","arguments":{}}
```

## Tool Description
Removes one or more project roots previously added via the add_roots tool.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "uris": {
      "type": "array",
      "description": "All the project roots to remove from this server.",
      "items": {
        "type": "string",
        "description": "The URIs of the roots to remove."
      }
    }
  }
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
