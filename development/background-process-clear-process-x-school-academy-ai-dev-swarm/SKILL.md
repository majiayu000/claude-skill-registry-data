---
name: background-process-clear-process
description: "To remove a finished background process from the manager list, clear a stopped process after it exits so it no longer appears in listings."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"backgroundProcess","tool_name":"clear_process","arguments":{}}
```

## Tool Description
Clears a stopped background process from the list.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "processId": {
      "type": "string",
      "format": "uuid"
    }
  },
  "required": [
    "processId"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"backgroundProcess","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
