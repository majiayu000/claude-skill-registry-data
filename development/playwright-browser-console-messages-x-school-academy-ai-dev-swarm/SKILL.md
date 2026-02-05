---
name: playwright-browser-console-messages
description: "To read console logs from the current page, retrieve console messages for debugging JavaScript output."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_console_messages","arguments":{}}
```

## Tool Description
Returns all console messages

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "level": {
      "type": "string",
      "enum": [
        "error",
        "warning",
        "info",
        "debug"
      ],
      "default": "info",
      "description": "Level of the console messages to return. Each level includes the messages of more severe levels. Defaults to \"info\"."
    }
  },
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
