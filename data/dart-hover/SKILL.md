---
name: dart-hover
description: "To view hover details such as docs and types at a cursor position, get hover information for a file location."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"hover","arguments":{}}
```

## Tool Description
Get hover information at a given cursor position in a file. This can include documentation, type information, etc for the text at that position.

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
