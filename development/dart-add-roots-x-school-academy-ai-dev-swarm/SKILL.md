---
name: dart-add-roots
description: "To register project roots for Dart tooling access, add one or more root paths before using other Dart tools on those projects."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"add_roots","arguments":{}}
```

## Tool Description
Adds one or more project roots. Tools are only allowed to run under these roots, so you must call this function before passing any roots to any other tools.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "roots": {
      "type": "array",
      "description": "All the project roots to add to this server.",
      "items": {
        "type": "object",
        "properties": {
          "uri": {
            "type": "string",
            "description": "The URI of the root."
          },
          "name": {
            "type": "string",
            "description": "An optional name of the root."
          }
        },
        "required": [
          "uri"
        ]
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
