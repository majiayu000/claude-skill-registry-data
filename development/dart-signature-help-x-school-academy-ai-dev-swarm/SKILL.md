---
name: dart-signature-help
description: "To see function or method signatures at a cursor position, get signature help for the API being called."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"signature_help","arguments":{}}
```

## Tool Description
Get signature help for an API being used at a given cursor position in a file.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "uri": {
      "type": "string",
      "description": "The URI of the file."
    },
    "line": {
      "type": "integer",
      "description": "The zero-based line number of the cursor position."
    },
    "column": {
      "type": "integer",
      "description": "The zero-based column number of the cursor position."
    }
  },
  "required": [
    "uri",
    "line",
    "column"
  ]
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
